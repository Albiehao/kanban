# AI接口配置确认

## ✅ API Key配置

**已确认配置的DeepSeek API Key**:
```
sk-9cb005b49aae4cba91a717cf8420bb5f
```

**配置文件位置**: `app/services/deepseek_service.py`

**配置内容**:
```python
DEEPSEEK_API_KEY = "sk-9cb005b49aae4cba91a717cf8420bb5f"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"
```

---

## ✅ 功能确认

1. **API Key**: 已正确配置为您提供的key
2. **Base URL**: 正确指向DeepSeek API
3. **Model**: 使用 `deepseek-chat` (DeepSeek-V3.2-Exp)
4. **流式传输**: 已实现SSE流式传输
5. **认证**: 已实现JWT Token认证
6. **限流**: 已实现请求频率限制

---

## 🚀 使用方法

### 1. 确保已安装依赖
```bash
pip install openai>=1.0.0
```

### 2. 重启服务器
重启后端服务器以加载AI路由。

### 3. 测试接口
```bash
# 获取Token（先登录）
TOKEN="your_token_here"

# 测试流式传输
curl -X POST "http://127.0.0.1:8000/api/ai/chat/stream" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"你好，请介绍一下你自己"}' \
  --no-buffer
```

---

## 📝 注意事项

1. **API Key安全**: 当前API Key直接写在代码中。如需更安全的配置，可以：
   - 使用环境变量：`os.getenv("DEEPSEEK_API_KEY", "sk-9cb005b49aae4cba91a717cf8420bb5f")`
   - 使用配置文件（不提交到Git）

2. **配额限制**: 
   - 每分钟最多10次请求
   - 每日最多500次请求

3. **流式传输**: 
   - 使用SSE (Server-Sent Events)协议
   - 响应类型：`text/event-stream`
   - 每条消息以 `\n\n` 结尾
   - 结束时发送 `[DONE]` 标记

---

## ✅ 配置确认

**您的API Key已正确配置在系统中！**

接口路径：`POST /api/ai/chat/stream`

可以直接使用该接口进行AI对话测试。

