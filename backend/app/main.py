"""主应用入口 - 模块化版本"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables, User, UserRole, SessionLocal
from app.auth import get_password_hash, get_user_by_username
from app.schemas import HealthResponse

# 导入所有路由模块
from app.routers import (
    auth, user, admin, task, course, notifications, finance, finance_stats, edu, ai, updates, deepseek_config
)

import time
from sqlalchemy import text
from app.database import engine

# 创建应用
app = FastAPI(
    title="Todo Backend API",
    version="2.0.0",
    description="模块化重构版本"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有路由
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(task.router)
app.include_router(finance.router)
app.include_router(finance_stats.router)
app.include_router(ai.router)
app.include_router(course.router)
app.include_router(notifications.router)
app.include_router(edu.router)
app.include_router(updates.router)
app.include_router(deepseek_config.router)


@app.on_event("startup")
async def startup_event():
    """启动时初始化数据库"""
    print("[INFO] 初始化数据库...")

    # 等待数据库就绪（避免容器首次启动时连接失败导致应用退出）
    max_attempts = 30
    for attempt in range(1, max_attempts + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"[INFO] 数据库连接成功（第 {attempt} 次尝试）")
            break
        except Exception as e:
            print(f"[WARN] 数据库未就绪，重试中（第 {attempt}/{max_attempts} 次）：{e}")
            time.sleep(2)
    else:
        # 超出重试次数
        print("[ERROR] 数据库长时间未就绪，启动继续但可能导致功能异常")

    try:
        create_tables()
    except Exception as e:
        print(f"[ERROR] 创建数据表失败：{e}")

    # 初始化超级管理员
    db = SessionLocal()
    try:
        super_admin_user = get_user_by_username("super_admin", db)
        if not super_admin_user:
            # 创建超级管理员
            super_admin_user = User(
                username="super_admin",
                email="super_admin@example.com",
                password_hash=get_password_hash("super_admin"),
                role=UserRole.super_admin,
                is_active=True
            )
            db.add(super_admin_user)
            db.commit()
            print("[INFO] 超级管理员已创建: username=super_admin, password=super_admin")
        else:
            print("[INFO] 超级管理员已存在")
    except Exception as e:
        print(f"[ERROR] 初始化超级管理员失败: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("[INFO] 应用启动完成！")


@app.get("/health", response_model=HealthResponse, tags=["健康检查"])
async def health_check():
    """健康检查"""
    return HealthResponse(status="ok")


@app.get("/", tags=["根路径"])
async def root():
    """根路径"""
    return {
        "message": "Todo Backend API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/api/info", tags=["信息"])
async def api_info():
    """API信息"""
    return {
        "name": "Todo Backend API",
        "version": "2.0.0",
        "architecture": "modular",
        "routes": {
            "auth": "认证相关路由",
            "user": "用户管理路由",
            "admin": "管理员路由",
            "task": "任务管理路由（数据库存储）",
            "finance": "财务管理路由（数据库存储）",
            "course": "课程管理路由（第三方API）",
            "notifications": "通知路由",
            "edu": "教务系统绑定路由",
            "ai": "AI智能助手路由（DeepSeek流式传输）"
        },
        "removed_routes": {}
    }

