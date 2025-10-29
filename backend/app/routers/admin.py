"""管理员路由"""

from typing import Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db, User, UserRole
from app.auth import get_current_active_user
from app.services.admin_service import AdminService
from app.services.log_service import LogService

router = APIRouter(prefix="/api/admin", tags=["管理员"])


@router.get("/data")
async def get_admin_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取所有管理员数据"""
    service = AdminService(db)
    return service.get_all_data(current_user)


@router.get("/logs")
async def get_system_logs(
    level: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取系统日志"""
    # 检查权限
    if current_user.role not in [UserRole.admin, UserRole.super_admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    
    service = LogService(db)
    return service.get_logs(level=level, limit=limit)


@router.post("/logs")
async def create_system_log(
    log_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建系统日志"""
    # 检查权限
    if current_user.role not in [UserRole.admin, UserRole.super_admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    
    message = log_data.get("message")
    level = log_data.get("level", "warning")  # 默认warning，因为info不会保存到数据库
    module = log_data.get("module")
    user_id = log_data.get("user_id", current_user.id)
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="日志消息不能为空"
        )
    
    # 验证级别（只允许warning和error保存到数据库）
    if level not in ["warning", "error"]:
        if level == "info":
            # info级别不保存到数据库，只打印
            print(f"[INFO] [{module or 'system'}] {message}")
            return {"success": True, "message": "日志已记录到控制台（info级别不保存到数据库）"}
        else:
            level = "warning"
    
    service = LogService(db)
    service.add_log(message, level, module, user_id)
    
    return {"success": True, "message": "日志记录成功"}


@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    status_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新用户状态"""
    service = AdminService(db)
    return service.update_user_status(user_id, status_data, current_user)


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新用户信息（仅超级管理员）"""
    service = AdminService(db)
    return service.update_user(user_id, user_data, current_user)


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除用户（仅超级管理员）"""
    service = AdminService(db)
    return service.delete_user(user_id, current_user)


@router.post("/users")
async def create_user(
    user_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建用户（仅超级管理员）"""
    # 检查权限
    if current_user.role != UserRole.super_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要超级管理员权限"
        )
    
    from app.services.auth_service import AuthService
    service = AuthService(db)
    
    user = service.register_user(
        user_data["username"],
        user_data["email"],
        user_data["password"],
        user_data.get("role", "user")
    )
    
    return {"success": True, "message": "用户创建成功", "user": user}


@router.get("/settings")
async def get_system_settings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取系统设置"""
    service = AdminService(db)
    return service.get_system_settings(current_user)


@router.put("/settings")
async def update_system_settings(
    settings_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新系统设置"""
    service = AdminService(db)
    return service.update_system_settings(settings_data, current_user)


@router.get("/users")
async def get_users(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    service = AdminService(db)
    return {
        "data": service.get_all_users(current_user)
    }


@router.get("/server/info")
async def get_server_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取服务器信息（跨平台支持 Linux/Windows）"""
    # 检查权限
    if current_user.role not in [UserRole.admin, UserRole.super_admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    
    service = AdminService(db)
    return {
        "data": service.get_server_info()
    }
