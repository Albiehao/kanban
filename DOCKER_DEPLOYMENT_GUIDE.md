# Docker 部署指南

## 📋 部署前准备

### 1. 创建环境变量文件

如果还没有 `.env` 文件，请复制 `env.template` 并修改：

```bash
cp env.template .env
```

然后编辑 `.env` 文件，修改数据库密码等配置。

### 2. 配置 Docker 镜像源（如果网络有问题）

如果无法访问 Docker Hub，可以配置国内镜像源：

**Windows (Docker Desktop)**：
1. 右键点击 Docker Desktop 图标 → Settings
2. 选择 Docker Engine
3. 添加以下配置：

```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
```

4. 点击 "Apply & Restart"

## 🚀 部署步骤

### 方法一：一键部署（推荐）

```bash
# 进入项目目录
cd G:\play\todo

# 停止并清理旧容器（如果有）
docker-compose down

# 构建并启动所有服务
docker-compose up -d --build
```

### 方法二：分步部署

```bash
# 1. 只构建镜像（不启动）
docker-compose build

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

## 📊 检查部署状态

```bash
# 查看所有容器状态
docker-compose ps

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# 查看所有日志（实时）
docker-compose logs -f
```

## ✅ 验证部署

部署成功后，访问以下地址：

- **前端应用**: http://localhost
- **后端API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 🔧 常用命令

```bash
# 停止所有服务
docker-compose stop

# 停止并删除容器
docker-compose down

# 停止并删除容器、数据卷（⚠️ 会删除所有数据）
docker-compose down -v

# 重启服务
docker-compose restart

# 查看容器状态
docker-compose ps

# 进入容器
docker-compose exec backend bash
docker-compose exec db bash
```

## 🐛 常见问题

### 1. 无法拉取镜像

**问题**: `failed to resolve reference "docker.io/library/mysql:8.0"`

**解决方案**:
- 检查网络连接
- 配置 Docker 镜像源（见上方）
- 重试拉取镜像：`docker pull mysql:8.0`

### 2. 端口被占用

**问题**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**解决方案**:
- 修改 `.env` 文件中的端口配置
- 或停止占用端口的其他服务

### 3. 数据库连接失败

**问题**: 后端无法连接数据库

**解决方案**:
```bash
# 检查数据库容器是否运行
docker-compose ps db

# 查看数据库日志
docker-compose logs db

# 等待数据库完全启动（约30秒）
docker-compose logs -f db
```

### 4. 前端无法访问后端API

**问题**: 前端页面报错，无法获取数据

**解决方案**:
- 检查后端服务是否运行：`curl http://localhost:8000/health`
- 检查浏览器控制台的网络请求
- 确认 `VITE_API_BASE_URL=/api` 在 `.env` 中已配置

## 📝 默认账号

系统首次启动会自动创建：

- **用户名**: `super_admin`
- **密码**: `super_admin`

⚠️ **重要**: 部署到生产环境后，请立即修改默认密码！

## 🔄 更新部署

```bash
# 1. 停止服务
docker-compose down

# 2. 拉取最新代码（如果有）
git pull

# 3. 重新构建并启动
docker-compose up -d --build
```

---

**部署完成后请访问**: http://localhost

