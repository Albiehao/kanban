# Todo Backend API

这是一个使用 FastAPI 构建的待办事项后端API服务，提供任务管理、财务统计、课程表、AI助手等功能。

## 功能特性

- ✅ 健康检查
- ✅ 任务与提醒管理
- ✅ 财务统计与交易记录
- ✅ 课程表管理
- ✅ AI智能助手（模拟）
- ✅ 个人设置管理
- ✅ 管理员系统管理

## 技术栈

- FastAPI
- Python 3.8+
- 内存数据存储（不使用数据库）

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行服务器

```bash
python main.py
```

或者使用 uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问API文档

启动后访问：
sk-9cb005b49aae4cba91a717cf8420bb5f
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API端点

### 健康检查
- `GET /health` - 检查服务器状态

### 任务API
- `GET /api/tasks` - 获取所有任务
- `GET /api/tasks?date=2025-10-28` - 获取指定日期的任务
- `POST /api/tasks` - 添加新任务
- `PUT /api/tasks/{id}` - 更新任务
- `DELETE /api/tasks/{id}` - 删除任务
- `PATCH /api/tasks/{id}/toggle` - 切换任务完成状态

### 财务API
- `GET /api/transactions` - 获取所有交易记录
- `POST /api/transactions` - 添加交易记录
- `PUT /api/transactions/{id}` - 更新交易记录
- `DELETE /api/transactions/{id}` - 删除交易记录
- `GET /api/finance/stats` - 获取财务统计数据

### 课程表API
- `GET /api/courses` - 获取所有课程
- `GET /api/courses?date=2025-10-28` - 获取指定日期的课程
- `POST /api/courses` - 添加课程
- `PUT /api/courses/{id}` - 更新课程
- `DELETE /api/courses/{id}` - 删除课程

### AI助手API
- `POST /api/ai/chat` - 发送消息给AI
- `GET /api/ai/conversations` - 获取所有对话
- `GET /api/ai/conversations/{id}/messages` - 获取对话消息
- `POST /api/ai/conversations` - 创建新对话
- `DELETE /api/ai/conversations/{id}` - 删除对话
- `DELETE /api/ai/conversations/{id}/clear` - 清除对话消息

### 用户设置API
- `GET /api/user/settings` - 获取用户设置
- `PUT /api/user/profile` - 更新用户资料
- `PUT /api/user/preferences` - 更新偏好设置
- `PUT /api/user/password` - 修改密码
- `POST /api/user/avatar` - 上传头像

### 管理员API
- `GET /api/admin/data` - 获取所有管理员数据
- `GET /api/admin/stats` - 获取统计数据
- `GET /api/admin/users` - 获取用户列表
- `GET /api/admin/settings` - 获取系统设置
- `PUT /api/admin/settings` - 更新系统设置
- `GET /api/admin/status` - 获取系统状态
- `GET /api/admin/logs` - 获取系统日志
- `PUT /api/admin/users/{id}/status` - 更新用户状态
- `PUT /api/admin/users/{id}` - 更新用户信息
- `DELETE /api/admin/users/{id}` - 删除用户

## 数据格式

### 任务格式
```json
{
  "id": 1,
  "title": "完成数学作业",
  "completed": false,
  "priority": "high",
  "date": "2025-10-28",
  "time": "19:00-21:00",
  "hasReminder": true
}
```

### 交易记录格式
```json
{
  "id": 1,
  "type": "expense",
  "amount": 45.50,
  "category": "餐饮",
  "description": "午餐",
  "date": "2025-10-28"
}
```

### 课程格式
```json
{
  "id": 1,
  "course_name": "软件工程",
  "classroom": "好学楼B209",
  "date": "2025-10-28",
  "teacher": "孙锦程",
  "periods": "1-2节"
}
```

## 注意事项

- 当前版本使用内存存储，重启服务器后数据会重置
- AI助手功能为模拟实现，不调用真实的AI服务
- 所有数据在 `storage.py` 中初始化
- 生产环境请使用数据库持久化数据

## 开发

项目结构：

```
backend/
├── main.py          # 应用入口
├── requirements.txt # 依赖包
├── .gitignore       # Git忽略文件
├── README.md        # 项目说明
├── app/             # 应用主目录
│   ├── __init__.py
│   ├── main.py      # FastAPI应用主文件
│   ├── schemas.py   # Pydantic数据模型
│   ├── storage.py   # 内存数据存储
│   ├── database.py  # 数据库配置
│   └── auth.py      # 认证相关
├── tests/           # 测试文件
│   ├── test_login.py
│   ├── test_register.py
│   ├── login_example.py
│   ├── test_api.ps1
│   └── login_example.ps1
├── scripts/         # 脚本文件
│   ├── init_database.py
│   ├── init_database.bat
│   └── init_db.sql
└── docs/            # 文档
    ├── LOGIN_GUIDE.md
    ├── REGISTER_FEATURE.md
    ├── POWERSHELL_API_TEST.md
    └── SETUP.md
```

## 许可证

MIT

