# AI流式传输接口实现说明

## ✅ 已实现功能

### 1. 流式传输聊天接口

**接口路径**: `POST /api/ai/chat/stream`

**功能特性**:
- ✅ 使用Server-Sent Events (SSE)实现流式传输
- ✅ 集成DeepSeek API（兼容OpenAI格式）
- ✅ JWT Token认证
- ✅ 请求限流（每分钟10次，每日500次）
- ✅ 输入验证（消息长度1-2000字符）
- ✅ 错误处理

### 2. DeepSeek API集成

**配置信息**:
- API Key: `sk-9cb005b49aae4cba91a717cf8420bb5f`
- Base URL: `https://api.deepseek.com`
- Model: `deepseek-chat` (DeepSeek-V3.2-Exp)
- 流式模式: `stream=True`

### 3. 限流机制

- **每分钟限制**: 10次请求
- **每日限制**: 500次请求
- 超出限制返回 `429 Too Many Requests`

---

## 📋 API使用示例

### 请求示例

```bash
curl -X POST "http://127.0.0.1:8000/api/ai/chat/stream" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "帮我制定一个学习计划"
  }'
```

### 响应示例（SSE格式）

```
data: {"content": "我理解"}\n\n
data: {"content": "你的需求"}\n\n
data: {"content": "。"}\n\n
data: [DONE]\n\n
```

### JavaScript/前端示例

```javascript
const response = await fetch('http://127.0.0.1:8000/api/ai/chat/stream', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: '帮我制定一个学习计划'
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = line.slice(6);
      if (data === '[DONE]') {
        console.log('流式传输结束');
      } else {
        const parsed = JSON.parse(data);
        if (parsed.content) {
          console.log('收到内容:', parsed.content);
          // 在前端UI中显示内容
        } else if (parsed.error) {
          console.error('错误:', parsed.error);
        }
      }
    }
  }
}
```

---

## 🔧 技术实现

### 1. 服务层

**文件**: `app/services/deepseek_service.py`

- `DeepSeekService` 类：封装DeepSeek API调用
- `check_rate_limit()`: 限流检查
- `generate_stream()`: 流式生成响应

### 2. 路由层

**文件**: `app/routers/ai.py`

- `POST /api/ai/chat/stream`: 流式传输接口
- `POST /api/ai/chat`: 非流式接口（兼容旧代码）

### 3. 依赖项

**requirements.txt**:
```
openai>=1.0.0
```

---

## 🔒 安全特性

1. **认证**: JWT Token验证（Bearer Token）
2. **输入验证**: 消息长度限制（1-2000字符）
3. **限流**: 防止API滥用
4. **错误处理**: 友好的错误消息

---

## 📊 错误处理

### HTTP状态码

- `200 OK`: 流式传输成功
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未认证
- `429 Too Many Requests`: 请求频率过高
- `500 Internal Server Error`: 服务器错误

### 错误响应格式

**非流式错误**:
```json
{
  "detail": "错误消息"
}
```

**流式传输中的错误**:
```
data: {"error": "错误消息", "code": "ERROR_CODE"}\n\n
data: [DONE]\n\n
```

---

## 🚀 部署说明

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 环境变量（可选）

可以在`.env`文件中配置：

```env
DEEPSEEK_API_KEY=sk-9cb005b49aae4cba91a717cf8420bb5f
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

### 3. 启动服务器

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📝 注意事项

1. **API Key安全**: 当前API Key硬编码在代码中，生产环境应使用环境变量
2. **限流存储**: 当前使用内存存储限流记录，重启后会重置。生产环境建议使用Redis
3. **对话历史**: 当前未保存对话历史，如需实现可添加数据库表
4. **成本控制**: DeepSeek API按Token计费，建议监控使用量

---

## 🔄 后续优化建议

1. **对话历史**: 实现数据库存储对话记录
2. **上下文管理**: 支持多轮对话上下文
3. **Token统计**: 记录每次请求的Token消耗
4. **限流优化**: 使用Redis实现分布式限流
5. **API Key管理**: 支持多用户使用不同的API Key
6. **错误重试**: 实现自动重试机制

---

## ✅ 测试

### 测试命令

```bash
# 获取Token（先登录）
TOKEN=$(curl -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password"}' \
  | jq -r '.token')

# 测试流式传输
curl -X POST "http://127.0.0.1:8000/api/ai/chat/stream" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"你好"}' \
  --no-buffer
```

---

**实现完成日期**: 2025-10-29  
**版本**: v1.0.0

