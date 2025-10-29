"""用户路由"""

from typing import Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.auth import get_current_active_user
from app.schemas import UserProfileUpdate, UserPreferencesUpdate
from app.services.user_service import UserService
import os
import uuid
from pathlib import Path

router = APIRouter(prefix="/api/user", tags=["用户"])

# 头像上传目录
UPLOAD_DIR = Path("uploads/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/profile")
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取用户资料（符合需求文档）"""
    service = UserService(db)
    return service.get_user_profile(current_user.id)


@router.get("/settings")
async def get_user_settings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取用户设置（兼容旧接口）"""
    service = UserService(db)
    return service.get_user_profile(current_user.id)


@router.put("/profile")
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新用户资料"""
    service = UserService(db)
    return service.update_profile(
        current_user.id,
        username=profile_data.username,
        email=profile_data.email,
        bio=profile_data.bio,
        avatar_url=profile_data.avatar_url
    )


@router.put("/username")
async def update_username(
    username_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新用户名"""
    service = UserService(db)
    username = username_data.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名不能为空"
        )
    return service.update_profile(current_user.id, username=username)


@router.put("/email")
async def update_email(
    email_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新邮箱"""
    service = UserService(db)
    email = email_data.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱不能为空"
        )
    return service.update_profile(current_user.id, email=email)


@router.post("/password")
async def change_password_post(
    password_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """修改密码（POST方法，符合需求文档）"""
    service = UserService(db)
    current_password = password_data.get("currentPassword") or password_data.get("current_password") or password_data.get("old_password")
    new_password = password_data.get("newPassword") or password_data.get("new_password")
    
    if not current_password or not new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供当前密码和新密码"
        )
    
    return service.change_password(
        current_user.id,
        current_password,
        new_password
    )


@router.put("/password")
async def change_password_put(
    password_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """修改密码（PUT方法，兼容旧接口）"""
    service = UserService(db)
    old_password = password_data.get("old_password")
    new_password = password_data.get("new_password")
    
    if not old_password or not new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供旧密码和新密码"
        )
    
    return service.change_password(
        current_user.id,
        old_password,
        new_password
    )


@router.post("/avatar")
async def upload_avatar(
    avatar: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """上传用户头像（POST方法，符合需求文档）"""
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
    if avatar.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型，仅支持: {', '.join(allowed_types)}"
        )
    
    # 验证文件大小（最大5MB）
    contents = await avatar.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小不能超过5MB"
        )
    
    # 生成唯一文件名
    file_extension = Path(avatar.filename).suffix or ".jpg"
    unique_filename = f"{current_user.id}_{uuid.uuid4().hex[:8]}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # 保存文件
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # 生成URL
    avatar_url = f"/uploads/avatars/{unique_filename}"
    
    # 保存到数据库
    service = UserService(db)
    service.update_profile(current_user.id, avatar_url=avatar_url)
    
    return {"avatarUrl": avatar_url, "avatar_url": avatar_url}


@router.get("/avatar")
async def get_user_avatar(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取用户头像URL（兼容旧接口）"""
    if current_user.avatar_url:
        return {"avatar_url": current_user.avatar_url}
    
    # 如果没有头像，生成Gravatar URL
    import hashlib
    hash_value = hashlib.md5(current_user.email.encode()).hexdigest()
    avatar_url = f"https://www.gravatar.com/avatar/{hash_value}?d=identicon"
    
    # 保存到数据库
    service = UserService(db)
    service.update_profile(current_user.id, avatar_url=avatar_url)
    
    return {"avatar_url": avatar_url}


@router.put("/preferences")
async def update_preferences(
    preferences_data: UserPreferencesUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新用户偏好设置"""
    service = UserService(db)
    return service.update_preferences(
        current_user.id,
        preferences_data.dict(exclude_unset=True)
    )


@router.post("/bind-edu")
async def bind_edu_account(
    binding_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """绑定第三方API密钥
    
    请求体示例:
    {
        "apiKey": "your_api_key_here",
        "apiPath": "http://160.202.229.142:8000/api/v1/api/courses",  // 可选
        "refreshFrequency": 1.0  // 可选，默认1.0
    }
    """
    from app.services.edu_binding_service import EduBindingService
    
    api_key = binding_data.get("apiKey") or binding_data.get("api_key")
    api_url = binding_data.get("apiPath") or binding_data.get("api_path") or binding_data.get("apiUrl")
    refresh_frequency = binding_data.get("refreshFrequency", 1.0)
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="API密钥不能为空"
        )
    
    # 验证刷新频率
    valid_frequencies = [0.5, 1.0, 2.0, 6.0, 24.0]
    if refresh_frequency not in valid_frequencies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"刷新频率无效，可选值: {valid_frequencies}"
        )
    
    service = EduBindingService(db)
    return service.bind_account(current_user.id, api_key, api_url, refresh_frequency)


@router.get("/bind-edu")
async def get_edu_binding(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取教务系统绑定状态"""
    from app.services.edu_binding_service import EduBindingService
    
    service = EduBindingService(db)
    return service.get_binding(current_user.id)


@router.delete("/bind-edu")
async def unbind_edu_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """解绑教务系统账号"""
    from app.services.edu_binding_service import EduBindingService
    
    service = EduBindingService(db)
    return service.unbind_account(current_user.id)

