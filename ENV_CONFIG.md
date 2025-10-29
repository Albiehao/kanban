# 环境变量配置说明

本文档说明如何配置项目的环境变量。

## 配置文件

将以下内容保存为项目根目录的 `.env` 文件：

```env
# ============================================
# 数据库配置
# ============================================
DB_HOST=db
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_secure_password_here
DB_NAME=todo_db

# ============================================
# 服务端口配置
# ============================================
BACKEND_PORT=8000
FRONTEND_PORT=80

# ============================================
# 前端API地址配置
# ============================================
# 在Docker环境中，使用 /api 让nginx代理到后端
# 在本地开发中，使用完整URL（如 http://127.0.0.1:8000/api）
VITE_API_BASE_URL=/api

# ============================================
# DeepSeek AI配置（可选）
# ============================================
# 如果需要使用AI助手功能，请配置以下变量
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

## 配置说明

### 数据库配置

| 变量名 | 说明 | 示例值 | 必需 |
|--------|------|--------|------|
| `DB_HOST` | 数据库主机地址 | `db`（Docker环境）或 `127.0.0.1`（本地） | ✅ |
| `DB_PORT` | 数据库端口 | `3306` | ✅ |
| `DB_USER` | 数据库用户名 | `root` | ✅ |
| `DB_PASSWORD` | 数据库密码 | 请设置强密码 | ✅ |
| `DB_NAME` | 数据库名称 | `todo_db` | ✅ |

### 服务端口

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `BACKEND_PORT` | 后端API服务端口 | `8000` | ❌ |
| `FRONTEND_PORT` | 前端服务端口 | `80` | ❌ |

**注意**: 如果在本地开发时端口被占用，可以修改这些端口值。

### 前端API地址

| 变量名 | 说明 | Docker环境 | 本地开发 |
|--------|------|-----------|----------|
| `VITE_API_BASE_URL` | 前端API基础地址 | `/api` | `http://127.0.0.1:8000/api` |

在Docker环境中，前端通过nginx反向代理访问后端，所以使用相对路径 `/api`。
在本地开发时，需要指定完整的后端URL。

### AI服务配置（可选）

如果不需要AI助手功能，可以忽略以下配置：

| 变量名 | 说明 | 示例值 | 必需 |
|--------|------|--------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | `sk-xxxxxxxx` | ❌ |
| `DEEPSEEK_BASE_URL` | DeepSeek API地址 | `https://api.deepseek.com` | ❌ |
| `DEEPSEEK_MODEL` | 使用的模型 | `deepseek-chat` | ❌ |

## 使用方法

### Docker环境

1. 在项目根目录创建 `.env` 文件
2. 复制上述配置模板
3. 根据需要修改配置值
4. 运行 `docker-compose up -d`

### 本地开发

#### 后端

后端会从以下位置读取环境变量：
1. `.env` 文件（项目根目录）
2. 系统环境变量

可以在 `backend/` 目录下创建 `.env` 文件，或直接设置系统环境变量。

#### 前端

前端在**构建时**读取 `VITE_` 开头的环境变量。

**开发模式**：
```bash
# 在 vue-dashboard/ 目录下创建 .env.local 文件
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

**生产构建**：
```bash
# 通过环境变量传入
VITE_API_BASE_URL=/api npm run build
```

## 安全建议

1. **不要将 `.env` 文件提交到版本控制系统**
2. **使用强密码**：数据库密码应足够复杂
3. **生产环境**：使用密钥管理服务（如AWS Secrets Manager）存储敏感信息
4. **定期更换密码**：特别是数据库和API密钥

## 环境变量加载顺序

### 后端（Python）

后端使用 `python-dotenv` 加载环境变量，加载顺序：
1. 系统环境变量
2. `.env` 文件（项目根目录）
3. 代码中的默认值

### 前端（Vite）

前端在构建时内嵌环境变量，需要以 `VITE_` 开头。

加载顺序：
1. `.env.production`（生产环境）
2. `.env.local`（本地，会被git忽略）
3. `.env`（通用配置）

参考：[Vite环境变量文档](https://vitejs.dev/guide/env-and-mode.html)

## 常见问题

### Q: Docker环境中前端无法访问后端？

**A**: 检查 `VITE_API_BASE_URL` 是否设置为 `/api`，nginx配置是否正确。

### Q: 本地开发时前端无法连接后端？

**A**: 
1. 确保后端服务运行在 `http://127.0.0.1:8000`
2. 确保 `VITE_API_BASE_URL=http://127.0.0.1:8000/api`
3. 检查CORS配置

### Q: 数据库连接失败？

**A**: 
1. 检查数据库服务是否运行
2. 验证 `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` 是否正确
3. 在Docker环境中，确保使用服务名称 `db` 作为 `DB_HOST`

---

**最后更新**: 2025-01-XX

