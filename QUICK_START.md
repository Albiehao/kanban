# 快速开始指南

## 🚀 使用Docker部署（3步完成）

### 1. 配置环境变量

在项目根目录创建 `.env` 文件：

```env
DB_PASSWORD=your_secure_password
VITE_API_BASE_URL=/api
```

### 2. 启动服务

```bash
docker-compose up -d
```

### 3. 访问应用

- **前端**: http://localhost
- **后端API文档**: http://localhost:8000/docs
- **默认账号**: `super_admin` / `super_admin`

## 📚 详细文档

- [完整部署文档](./DEPLOYMENT.md) - 详细的部署步骤和配置说明
- [环境变量配置](./ENV_CONFIG.md) - 环境变量详细说明
- [项目README](./README.md) - 项目介绍和功能说明

## ❓ 遇到问题？

查看 [DEPLOYMENT.md](./DEPLOYMENT.md) 中的 [故障排查](#故障排查) 部分。

