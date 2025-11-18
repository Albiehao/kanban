# 本地MySQL连接配置说明

## 🔍 问题描述

在本地开发时，服务器尝试连接到数据库主机 `db`（Docker网络主机名），导致连接失败：

```
sqlalchemy.exc.OperationalError: (2003, "Can't connect to MySQL server on 'db' ([Errno 11001] getaddrinfo failed)")
```

## ✅ 解决方案

### 问题原因

`.env` 文件配置了 `DB_HOST=db`，这是为 Docker 容器环境准备的。在本地 Windows 环境开发时，应使用 `127.0.0.1` 或 `localhost`。

### 配置文件位置

`.env` 文件位于父目录：`G:\play\todo\.env`

### 配置修改

**Docker 环境配置**（适用于 Docker Compose）：
```env
DB_HOST=db
DB_PORT=3306
DB_USER=root
DB_PASSWORD=12345678
DB_NAME=todo_db
```

**本地开发配置**（适用于本地 Windows 环境）：
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=12345678
DB_NAME=todo_db
```

## 🚀 快速修复

### 方式1：修改 `.env` 文件

编辑 `G:\play\todo\.env` 文件，将：
```env
DB_HOST=db
```

改为：
```env
DB_HOST=127.0.0.1
```

### 方式2：使用命令行

```powershell
# PowerShell
$content = Get-Content ..\.env -Raw
$content = $content -replace 'DB_HOST=db', 'DB_HOST=127.0.0.1'
$content | Set-Content ..\.env -NoNewline
```

## 📋 配置说明

### 数据库配置参数

| 参数 | Docker环境 | 本地环境 | 说明 |
|------|-----------|---------|------|
| `DB_HOST` | `db` | `127.0.0.1` | 数据库主机地址 |
| `DB_PORT` | `3306` | `3306` | 数据库端口 |
| `DB_USER` | `root` | `root` | 数据库用户名 |
| `DB_PASSWORD` | `12345678` | `12345678` | 数据库密码 |
| `DB_NAME` | `todo_db` | `todo_db` | 数据库名称 |

### 其他配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `BACKEND_PORT` | `8000` | 后端服务端口 |
| `FRONTEND_PORT` | `80` | 前端服务端口 |
| `VITE_API_BASE_URL` | `/api` | 前端API基础路径 |
| `DEEPSEEK_API_KEY` | (空) | DeepSeek API密钥（可选） |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com` | DeepSeek API地址 |
| `DEEPSEEK_MODEL` | `deepseek-chat` | DeepSeek模型名称 |

## 🐛 常见问题

### 1. MySQL 未启动

**问题**：修改配置后仍然无法连接

**解决**：确保 MySQL 服务正在运行

```powershell
# 检查 MySQL 服务状态
Get-Service -Name MySQL*

# 启动 MySQL 服务
Start-Service -Name MySQL
```

### 2. 数据库不存在

**问题**：数据库 `todo_db` 不存在

**解决**：运行初始化脚本

```powershell
# 方式1：使用 Python 脚本
python scripts/init_database.py

# 方式2：使用批处理文件
.\scripts\init_database.bat
```

### 3. 端口被占用

**问题**：3306 端口被其他程序占用

**解决**：
1. 检查端口占用：`netstat -ano | findstr :3306`
2. 修改 `.env` 中的 `DB_PORT` 为其他端口（如 `3307`）
3. 或者在 MySQL 配置文件中修改端口

### 4. 用户名或密码错误

**问题**：连接认证失败

**解决**：检查 `.env` 中的 `DB_USER` 和 `DB_PASSWORD` 是否正确

## 📝 完整配置文件示例

### 本地开发环境配置

创建或编辑 `G:\play\todo\.env`：

```env
# 数据库配置（本地开发）
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=12345678
DB_NAME=todo_db

# 服务端口
BACKEND_PORT=8000
FRONTEND_PORT=80

# 前端API地址 (Docker内部使用相对路径)
VITE_API_BASE_URL=/api

# DeepSeek AI配置 (可选)
DEEPSEEK_API_KEY=
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

### Docker 环境配置

如需在 Docker 环境中运行，修改为：

```env
# 数据库配置（Docker环境）
DB_HOST=db
DB_PORT=3306
DB_USER=root
DB_PASSWORD=12345678
DB_NAME=todo_db

# 其他配置保持不变
...
```

## ✅ 验证配置

修改配置后，验证是否生效：

```powershell
# 检查配置是否正确加载
python -c "from app.database import DB_HOST; print(f'DB_HOST: {DB_HOST}')"

# 输出应为：
# DB_HOST: 127.0.0.1 (本地开发)
# 或
# DB_HOST: db (Docker环境)

# 启动服务器
python main.py

# 如果成功，应该能看到：
# [INFO] 初始化数据库...
# [INFO] 超级管理员已创建或已存在
# [INFO] 应用启动完成！
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 📚 相关文档

- [数据库初始化说明](./使用Docker启动MySQL.md)（如果有）
- [WSL MySQL配置](./WSL中MySQL连接配置.md)（如果有）

## 🎯 总结

- **本地开发**：使用 `DB_HOST=127.0.0.1`
- **Docker环境**：使用 `DB_HOST=db`
- 修改 `.env` 文件后需要重启服务器
- 确保 MySQL 服务正在运行
- 确保数据库 `todo_db` 已创建

最后更新：2025-10-30


