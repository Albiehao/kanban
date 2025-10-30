# DeepSeek API密钥认证失败解决方案

## 🔍 问题描述

调用 DeepSeek API 时出现认证失败错误：

```
Error code: 401 - {
  'error': {
    'message': 'Authentication Fails, Your api key: ****bb5f is invalid', 
    'type': 'authentication_error', 
    'param': None, 
    'code': 'invalid_request_error'
  }
}
```

## 📋 问题原因

1. **API密钥无效**：当前使用的 API 密钥 `sk-9cb005b49aae4cba91a717cf8420bb5f` 已经过期或被禁用
2. **API密钥错误**：密钥格式不正确或不属于有效的 DeepSeek 账户
3. **配额已用完**：API 密钥的配额已经用尽
4. **账户问题**：DeepSeek 账户被禁用或存在问题

## ✅ 解决方案

### 方案1：获取新的有效 API 密钥（推荐）

1. **访问 DeepSeek 官网**
   - 官网地址：https://www.deepseek.com
   - 或者 API 文档：https://platform.deepseek.com

2. **注册/登录账户**
   - 如果没有账户，需要先注册
   - 如果已有账户，直接登录

3. **获取 API 密钥**
   - 进入控制台或设置页面
   - 找到 API 密钥管理
   - 创建新的 API 密钥
   - 复制密钥（格式通常为 `sk-xxxxxxxxxxxxxxxx`）

4. **更新配置文件**

   **方式1：通过管理后台更新（推荐）**
   
   打开前端管理页面：
   - 以管理员身份登录
   - 进入"DeepSeek 配置"页面
   - 编辑现有配置，更新 API 密钥
   - 保存配置

   **方式2：直接更新数据库**

   使用 Python 脚本：
   ```python
   from app.database import SessionLocal, DeepSeekConfig
   
   db = SessionLocal()
   
   # 更新配置
   config = db.query(DeepSeekConfig).first()
   config.api_key = "your-new-api-key-here"
   db.commit()
   db.close()
   ```

   **方式3：使用 API 更新**

   使用管理员权限调用 API：
   ```bash
   # 更新配置
   curl -X PUT "http://127.0.0.1:8000/api/admin/deepseek/config/1" \
     -H "Authorization: Bearer <admin_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "api_key": "your-new-api-key-here"
     }'
   ```

   **方式4：使用 Python 脚本**
   
   创建 `scripts/update_deepseek_key.py`：
   ```python
   #!/usr/bin/env python
   # -*- coding: utf-8 -*-
   """更新DeepSeek API密钥"""
   
   import sys
   import os
   sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   
   from app.database import SessionLocal, DeepSeekConfig
   
   # 新的API密钥
   NEW_API_KEY = "your-new-api-key-here"
   
   db = SessionLocal()
   try:
       config = db.query(DeepSeekConfig).first()
       if config:
           print(f"当前密钥: {config.api_key[:4]}****{config.api_key[-4:]}")
           config.api_key = NEW_API_KEY
           db.commit()
           print(f"更新成功！新密钥: {config.api_key[:4]}****{config.api_key[-4:]}")
       else:
           print("未找到配置文件，请先创建配置")
   except Exception as e:
       print(f"更新失败: {e}")
       db.rollback()
   finally:
       db.close()
   ```

5. **重启服务器**
   ```bash
   # 停止当前服务器（Ctrl+C）
   # 重新启动
   python main.py
   ```

### 方案2：使用环境变量配置

如果不想更新数据库，可以使用环境变量：

1. **修改 `.env` 文件**

   编辑 `G:\play\todo\.env`：
   ```env
   # 添加或修改以下配置
   DEEPSEEK_API_KEY=your-new-api-key-here
   DEEPSEEK_BASE_URL=https://api.deepseek.com
   DEEPSEEK_MODEL=deepseek-chat
   ```

2. **重启服务器**

   注意：这种方式只在数据库中没有配置时生效。如果数据库中有配置，会优先使用数据库配置。

### 方案3：禁用 DeepSeek 配置

如果暂时不想使用 DeepSeek API，可以禁用配置：

```python
from app.database import SessionLocal, DeepSeekConfig

db = SessionLocal()
config = db.query(DeepSeekConfig).first()
if config:
    config.is_active = False
    db.commit()
    print("已禁用 DeepSeek 配置")
db.close()
```

或者在管理后台直接禁用配置。

## 🧪 测试验证

### 测试 API 密钥是否有效

**方式1：使用 curl**

```bash
# 替换 YOUR_API_KEY 为实际密钥
curl -X POST "https://api.deepseek.com/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

**方式2：使用 Python**

```python
import openai

client = openai.OpenAI(
    api_key="your-api-key-here",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Hello"}]
)

print(response.choices[0].message.content)
```

### 测试后端接口

更新配置后，测试后端 AI 接口：

```bash
# 先登录获取 token
TOKEN=$(curl -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"super_admin","password":"super_admin"}' \
  | jq -r '.token')

# 测试 AI 聊天接口
curl -X POST "http://127.0.0.1:8000/api/ai/chat/stream" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"你好"}' \
  --no-buffer
```

## 📚 DeepSeek API 资源

- **官网**：https://www.deepseek.com
- **API 文档**：https://platform.deepseek.com/docs
- **获取 API 密钥**：https://platform.deepseek.com/api_keys
- **定价**：https://www.deepseek.com/pricing

## 📝 注意事项

1. **API密钥安全**
   - 不要在代码中硬编码 API 密钥
   - 不要在公开场合分享 API 密钥
   - 定期更换 API 密钥
   - 使用数据库管理密钥，而不是环境变量

2. **配额限制**
   - DeepSeek 有配额限制，免费用户有额度限制
   - 注意监控使用量
   - 避免超限导致服务中断

3. **错误处理**
   - API 密钥无效时返回 401 错误
   - 配额不足时返回 429 错误
   - 网络问题返回相应错误码
   - 做好错误处理和用户提示

4. **配置优先级**
   - 数据库配置 > 环境变量 > 代码默认值
   - 如果数据库有启用配置，优先使用数据库配置
   - 只有在数据库没有配置时，才使用环境变量

## 🔄 快速修复步骤总结

1. ✅ 获取新的有效 DeepSeek API 密钥
2. ✅ 登录管理后台或使用 API 更新配置
3. ✅ 重启服务器
4. ✅ 测试 AI 接口是否正常工作

## 📊 当前配置状态

```sql
-- 查看当前配置
SELECT 
    id,
    api_key,
    base_url,
    model,
    is_active,
    created_at,
    updated_at
FROM deepseek_configs;
```

当前配置：
- ID: 1
- API Key: sk-9cb005b49aae4cba91a717cf8420bb5f ❌ (无效)
- Base URL: https://api.deepseek.com ✅
- Model: deepseek-chat ✅
- Is Active: True

## 🎯 下一步

立即操作：
1. 访问 https://platform.deepseek.com/api_keys 获取新的 API 密钥
2. 使用管理员账号登录系统
3. 进入 DeepSeek 配置页面更新密钥
4. 重启服务器并测试

最后更新：2025-10-30

