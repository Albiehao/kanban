"""认证路由"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.auth import get_current_active_user
from app.database import User, UserRole
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """用户登录"""
    service = AuthService(db)
    return service.authenticate_user(login_data.username, login_data.password)


@router.post("/register")
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """用户注册"""
    service = AuthService(db)
    user = service.register_user(
        register_data.username,
        register_data.email,
        register_data.password,
        register_data.role
    )
    return {"success": True, "message": "注册成功", "user": user}


@router.get("/verify")
async def verify_token(
    current_user: User = Depends(get_current_active_user)
):
    """验证Token"""
    return {
        "valid": True,
        "user": current_user.to_dict(),
        "permissions": []
    }


@router.get("/me", response_model=dict)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取当前用户信息"""
    from app.services.user_service import UserService
    
    service = UserService(db)
    return service.get_user_profile(current_user.id)

