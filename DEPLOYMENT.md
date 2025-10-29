# Todo 系统部署文档

本文档介绍如何使用 Docker 部署 Todo 系统的前后端应用。

## 📋 目录

- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [部署步骤](#部署步骤)
- [访问应用](#访问应用)
- [数据备份与恢复](#数据备份与恢复)
- [常见问题](#常见问题)

## 🔧 系统要求

### 必需软件
- **Docker**: 20.10 或更高版本
- **Docker Compose**: 2.0 或更高版本

### 系统资源
- **CPU**: 至少 2 核
- **内存**: 至少 2GB RAM
- **磁盘**: 至少 10GB 可用空间

### 端口要求
确保以下端口未被占用：
- `80` - 前端服务（可通过环境变量修改）
- `8000` - 后端API服务（可通过环境变量修改）
- `3306` - MySQL数据库（可通过环境变量修改）

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd todo
```

### 2. 配置环境变量

复制环境变量示例文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，根据需要修改配置：

```env
# 数据库配置
DB_HOST=db
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_secure_password_here
DB_NAME=todo_db

# 后端端口
BACKEND_PORT=8000

# 前端端口
FRONTEND_PORT=80

# 前端API地址（构建时使用）
VITE_API_BASE_URL=http://localhost:8000/api

# DeepSeek AI配置（可选）
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

### 3. 启动服务

使用 Docker Compose 一键启动所有服务：

```bash
docker-compose up -d
```

这会启动以下服务：
- MySQL 数据库
- FastAPI 后端服务
- Vue.js 前端服务（Nginx）

### 4. 查看服务状态

```bash
docker-compose ps
```

### 5. 查看日志

查看所有服务日志：
```bash
docker-compose logs -f
```

查看特定服务日志：
```bash
# 后端日志
docker-compose logs -f backend

# 前端日志
docker-compose logs -f frontend

# 数据库日志
docker-compose logs -f db
```

## ⚙️ 配置说明

### 数据库配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `DB_HOST` | `db` | 数据库主机（在Docker网络中应为`db`） |
| `DB_PORT` | `3306` | 数据库端口 |
| `DB_USER` | `root` | 数据库用户名 |
| `DB_PASSWORD` | `12345678` | 数据库密码（**强烈建议修改**） |
| `DB_NAME` | `todo_db` | 数据库名称 |

### 服务端口配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `BACKEND_PORT` | `8000` | 后端API服务端口 |
| `FRONTEND_PORT` | `80` | 前端服务端口 |

### AI服务配置（可选）

如果需要使用AI助手功能，需要配置 DeepSeek API：

| 环境变量 | 说明 |
|---------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 |
| `DEEPSEEK_BASE_URL` | DeepSeek API基础URL |
| `DEEPSEEK_MODEL` | 使用的模型名称 |

## 📝 部署步骤详解

### 步骤 1: 构建镜像

首次部署或更新代码后，需要重新构建镜像：

```bash
# 构建所有服务
docker-compose build

# 只构建特定服务
docker-compose build backend
docker-compose build frontend
```

### 步骤 2: 启动服务

```bash
# 后台启动
docker-compose up -d

# 查看启动日志
docker-compose up
```

### 步骤 3: 初始化数据库

数据库会在首次启动时自动初始化。如果需要手动初始化：

```bash
# 进入后端容器
docker-compose exec backend bash

# 运行初始化脚本
python scripts/init_database.py
```

### 步骤 4: 验证部署

检查服务健康状态：

```bash
# 后端健康检查
curl http://localhost:8000/health

# 前端访问
curl http://localhost
```

## 🌐 访问应用

### 应用地址

- **前端应用**: http://localhost (或 http://your-server-ip)
- **后端API文档**: http://localhost:8000/docs (Swagger UI)
- **后端API文档 (ReDoc)**: http://localhost:8000/redoc

### 默认账号

系统首次启动会自动创建超级管理员账号：

- **用户名**: `super_admin`
- **密码**: `super_admin`

**⚠️ 重要**: 部署到生产环境后，请立即修改默认密码！

## 💾 数据备份与恢复

### 备份数据库

```bash
# 备份MySQL数据
docker-compose exec db mysqldump -u root -p${DB_PASSWORD} todo_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

或使用 Docker 卷备份：

```bash
# 备份Docker卷
docker run --rm -v todo_mysql_data:/data -v $(pwd):/backup alpine tar czf /backup/mysql_backup_$(date +%Y%m%d_%H%M%S).tar.gz /data
```

### 恢复数据库

```bash
# 从SQL文件恢复
docker-compose exec -T db mysql -u root -p${DB_PASSWORD} todo_db < backup_file.sql
```

### 备份上传文件

```bash
# 备份后端上传的文件
docker cp todo_backend:/app/uploads ./backup_uploads_$(date +%Y%m%d_%H%M%S)
```

## 🔄 更新部署

### 更新代码

```bash
# 1. 拉取最新代码
git pull

# 2. 重新构建镜像
docker-compose build

# 3. 重启服务
docker-compose up -d
```

### 只更新特定服务

```bash
# 只更新后端
docker-compose up -d --build backend

# 只更新前端
docker-compose up -d --build frontend
```

## 🛠️ 管理命令

### 停止服务

```bash
# 停止所有服务
docker-compose stop

# 停止并删除容器
docker-compose down
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

### 清理资源

```bash
# 停止并删除容器、网络（保留数据卷）
docker-compose down

# 停止并删除容器、网络、数据卷（⚠️ 会删除所有数据）
docker-compose down -v

# 清理未使用的镜像
docker image prune -a
```

## 🔍 故障排查

### 查看容器状态

```bash
docker-compose ps
```

### 查看容器日志

```bash
# 所有服务日志
docker-compose logs

# 最近100行日志
docker-compose logs --tail=100

# 实时跟踪日志
docker-compose logs -f
```

### 进入容器调试

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入数据库容器
docker-compose exec db bash

# 进入前端容器
docker-compose exec frontend sh
```

### 常见问题

#### 1. 数据库连接失败

**问题**: 后端无法连接数据库

**解决方案**:
```bash
# 检查数据库容器状态
docker-compose ps db

# 检查数据库日志
docker-compose logs db

# 检查环境变量
docker-compose exec backend env | grep DB_
```

#### 2. 前端无法访问后端API

**问题**: 前端页面报错，无法获取数据

**解决方案**:
- 检查nginx配置中的API代理设置
- 确认后端服务正常运行：`curl http://localhost:8000/health`
- 检查浏览器控制台的网络请求

#### 3. 端口已被占用

**问题**: 启动时提示端口被占用

**解决方案**:
- 修改 `.env` 文件中的端口配置
- 或停止占用端口的其他服务

#### 4. 构建失败

**问题**: 构建Docker镜像时失败

**解决方案**:
```bash
# 清理构建缓存
docker-compose build --no-cache

# 检查Dockerfile语法
docker build -t test ./backend
```

## 📦 生产环境建议

### 安全配置

1. **修改默认密码**: 强烈建议修改数据库和超级管理员密码
2. **使用HTTPS**: 配置反向代理（如Nginx）启用SSL/TLS
3. **限制访问**: 使用防火墙限制数据库端口的外部访问
4. **环境变量安全**: 不要在代码仓库中提交 `.env` 文件

### 性能优化

1. **数据库优化**: 根据数据量调整MySQL配置
2. **资源限制**: 在 `docker-compose.yml` 中添加资源限制
3. **日志管理**: 配置日志轮转，避免日志文件过大
4. **缓存策略**: 考虑添加Redis缓存层

### 监控建议

1. **健康检查**: 定期检查 `/health` 端点
2. **日志监控**: 使用日志收集工具（如ELK）
3. **性能监控**: 监控容器资源使用情况

### 示例：添加资源限制

修改 `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## 📚 相关文档

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [Vue.js文档](https://vuejs.org/)

## 🆘 获取帮助

如果遇到问题，请：

1. 查看本文档的[故障排查](#故障排查)部分
2. 检查容器日志：`docker-compose logs`
3. 在项目Issues中提交问题

---

**最后更新**: 2025-01-XX
**版本**: 1.0.0

