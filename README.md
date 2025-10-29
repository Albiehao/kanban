# Todo 个人管理系统

一个功能完整的个人任务管理系统，包含任务管理、财务管理、课程管理、AI助手等功能。

## ✨ 功能特性

- 📝 **任务管理**: 创建、编辑、完成任务，支持优先级和提醒
- 💰 **财务管理**: 记录收支，生成财务报表和统计图表
- 📚 **课程管理**: 课程表管理，教务系统绑定
- 🤖 **AI助手**: 集成DeepSeek AI，智能对话助手
- 🔔 **通知系统**: 实时通知提醒
- 👤 **用户管理**: 多用户支持，角色权限管理
- 📊 **数据统计**: 丰富的图表和统计信息

## 🏗️ 技术栈

### 后端
- **FastAPI** - 现代Python Web框架
- **SQLAlchemy** - ORM数据库操作
- **MySQL** - 关系型数据库
- **JWT** - 身份认证
- **Python 3.11+**

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript
- **Vite** - 快速构建工具
- **Tailwind CSS** - 实用优先的CSS框架
- **Pinia** - Vue状态管理

## 📦 项目结构

```
todo/
├── backend/              # 后端服务
│   ├── app/             # 应用主目录
│   │   ├── routers/     # API路由
│   │   ├── services/    # 业务逻辑服务
│   │   ├── schemas.py   # 数据模型
│   │   └── database.py  # 数据库配置
│   ├── scripts/         # 工具脚本
│   ├── Dockerfile       # 后端Docker配置
│   └── requirements.txt # Python依赖
│
├── vue-dashboard/       # 前端应用
│   ├── src/
│   │   ├── components/  # Vue组件
│   │   ├── services/    # API服务
│   │   ├── stores/      # 状态管理
│   │   └── views/       # 页面视图
│   ├── Dockerfile       # 前端Docker配置
│   └── package.json     # Node依赖
│
└── docker-compose.yml   # Docker编排配置
```

## 🚀 快速开始

### 使用 Docker 部署（推荐）

详细的部署说明请参考 [DEPLOYMENT.md](./DEPLOYMENT.md)

#### 1. 克隆项目

```bash
git clone <your-repo-url>
cd todo
```

#### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库密码等
```

#### 3. 启动服务

```bash
docker-compose up -d
```

#### 4. 访问应用

- 前端: http://localhost
- 后端API文档: http://localhost:8000/docs

默认账号: `super_admin` / `super_admin`

### 本地开发

#### 后端开发

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置数据库
# 编辑 app/database.py 或设置环境变量

# 初始化数据库
python scripts/init_database.py

# 启动服务
python main.py
# 或
uvicorn app.main:app --reload
```

#### 前端开发

```bash
cd vue-dashboard

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 📖 API文档

启动后端服务后，访问以下地址查看API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 配置说明

### 环境变量

主要环境变量说明（完整列表请参考 `.env.example`）：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DB_HOST` | 数据库主机 | `127.0.0.1` |
| `DB_PORT` | 数据库端口 | `3306` |
| `DB_USER` | 数据库用户 | `root` |
| `DB_PASSWORD` | 数据库密码 | `12345678` |
| `DB_NAME` | 数据库名 | `todo_db` |
| `VITE_API_BASE_URL` | 前端API地址 | `http://127.0.0.1:8000/api` |
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | - |

## 📝 开发指南

### 添加新功能

1. **后端API**:
   - 在 `backend/app/routers/` 创建新的路由文件
   - 在 `backend/app/services/` 实现业务逻辑
   - 在 `backend/app/schemas.py` 定义数据模型

2. **前端页面**:
   - 在 `vue-dashboard/src/views/` 创建新页面
   - 在 `vue-dashboard/src/components/` 创建组件
   - 在 `vue-dashboard/src/services/` 添加API调用

### 数据库迁移

```bash
# 手动执行SQL脚本
python scripts/init_database.py

# 或直接操作数据库
mysql -u root -p todo_db < scripts/init_db.sql
```

## 🧪 测试

### 后端测试

```bash
cd backend
pytest tests/
```

### API测试

```bash
# 使用curl测试
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"super_admin","password":"super_admin"}'
```

## 📄 许可证

本项目采用 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题或建议，请在项目Issues中提出。

---

**最后更新**: 2025-01-XX

