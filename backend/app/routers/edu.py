"""教务系统绑定路由（符合需求文档路径）"""

from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.auth import get_current_active_user
from app.services.edu_binding_service import EduBindingService

router = APIRouter(prefix="/api/edu", tags=["教务系统"])


@router.post("/bind")
async def bind_edu_account(
    binding_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """绑定教务系统账号（符合需求文档）"""
    service = EduBindingService(db)
    
    # 支持多种字段名格式
    edu_username = binding_data.get("edu_username") or binding_data.get("eduUsername") or binding_data.get("username")
    edu_password = binding_data.get("edu_password") or binding_data.get("eduPassword") or binding_data.get("password")
    
    if not edu_username or not edu_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供教务系统用户名和密码"
        )
    
    # 使用API密钥模式（兼容现有实现）
    api_key = binding_data.get("apiKey") or binding_data.get("api_key") or edu_password
    api_url = binding_data.get("apiPath") or binding_data.get("api_path") or binding_data.get("api_url")
    refresh_frequency = binding_data.get("refreshFrequency", 1.0)
    
    # 验证刷新频率
    valid_frequencies = [0.5, 1.0, 2.0, 6.0, 24.0]
    if refresh_frequency not in valid_frequencies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"刷新频率无效，可选值: {valid_frequencies}"
        )
    
    result = service.bind_account(current_user.id, api_key, api_url, refresh_frequency)
    
    return {
        "is_bound": True,
        "edu_username": edu_username,
        "is_active": result.get("is_active", True),
        "last_sync": result.get("updated_at")
    }


@router.get("/bind/status")
async def get_bind_status(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取绑定状态（符合需求文档）"""
    service = EduBindingService(db)
    binding = service.get_binding(current_user.id)
    
    if not binding:
        return {
            "is_bound": False,
            "edu_username": None,
            "is_active": False,
            "last_sync": None
        }
    
    return {
        "is_bound": True,
        "edu_username": binding.get("api_key", "")[:10] + "...",  # 部分显示
        "is_active": binding.get("is_active", True),
        "last_sync": binding.get("updated_at")
    }


@router.put("/bind")
async def update_edu_bind(
    binding_data: Dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新绑定信息（符合需求文档）"""
    service = EduBindingService(db)
    
    edu_username = binding_data.get("edu_username") or binding_data.get("eduUsername")
    edu_password = binding_data.get("edu_password") or binding_data.get("eduPassword")
    
    if not edu_username or not edu_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供教务系统用户名和新密码"
        )
    
    api_key = binding_data.get("apiKey") or binding_data.get("api_key") or edu_password
    api_url = binding_data.get("apiPath") or binding_data.get("api_path") or binding_data.get("api_url")
    refresh_frequency = binding_data.get("refreshFrequency", 1.0)
    
    # 验证刷新频率
    valid_frequencies = [0.5, 1.0, 2.0, 6.0, 24.0]
    if refresh_frequency not in valid_frequencies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"刷新频率无效，可选值: {valid_frequencies}"
        )
    
    result = service.bind_account(current_user.id, api_key, api_url, refresh_frequency)
    
    return {
        "is_bound": True,
        "edu_username": edu_username,
        "is_active": result.get("is_active", True),
        "last_sync": result.get("updated_at")
    }


@router.delete("/bind")
async def unbind_edu_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取消绑定（符合需求文档）"""
    service = EduBindingService(db)
    service.unbind_account(current_user.id)
    
    return {
        "success": True,
        "message": "已取消绑定"
    }

