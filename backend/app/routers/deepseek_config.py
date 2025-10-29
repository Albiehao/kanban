"""DeepSeek配置管理路由（管理员专用）"""

from typing import Dict, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db, DeepSeekConfig, User, UserRole
from app.auth import get_current_active_user
from app.services.log_service import LogService
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/admin/deepseek", tags=["DeepSeek配置"])


class DeepSeekConfigCreate(BaseModel):
    """DeepSeek配置创建模型"""
    api_key: str = Field(..., min_length=1, description="DeepSeek API密钥（必填）")
    base_url: Optional[str] = Field("https://api.deepseek.com", description="API基础URL")
    model: Optional[str] = Field("deepseek-chat", description="模型名称")
    is_active: Optional[bool] = Field(True, description="是否启用")
    rate_limit_per_minute: Optional[int] = Field(10, ge=1, description="每分钟请求限制")
    rate_limit_per_day: Optional[int] = Field(500, ge=1, description="每日请求限制")


class DeepSeekConfigUpdate(BaseModel):
    """DeepSeek配置更新模型"""
    api_key: Optional[str] = Field(None, min_length=1, description="DeepSeek API密钥")
    base_url: Optional[str] = None
    model: Optional[str] = None
    is_active: Optional[bool] = None
    rate_limit_per_minute: Optional[int] = Field(None, ge=1)
    rate_limit_per_day: Optional[int] = Field(None, ge=1)


def check_admin_permission(current_user: User):
    """检查管理员权限"""
    if current_user.role not in [UserRole.admin, UserRole.super_admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )


@router.get("/configs")
async def list_deepseek_configs(
    include_inactive: bool = Query(False, description="是否包含已禁用的配置"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取所有DeepSeek配置列表（管理员权限）"""
    check_admin_permission(current_user)
    
    query = db.query(DeepSeekConfig)
    if not include_inactive:
        query = query.filter(DeepSeekConfig.is_active == True)
    
    configs = query.order_by(DeepSeekConfig.created_at.desc()).all()
    
    return {
        "count": len(configs),
        "configs": [config.to_dict(include_api_key=True) for config in configs]
    }


@router.get("/config")
async def get_deepseek_config(
    config_id: Optional[int] = Query(None, description="配置ID，不提供则返回当前启用的配置"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取DeepSeek配置（管理员权限）"""
    check_admin_permission(current_user)
    
    if config_id:
        config = db.query(DeepSeekConfig).filter(DeepSeekConfig.id == config_id).first()
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="配置不存在"
            )
    else:
        config = db.query(DeepSeekConfig).filter(
            DeepSeekConfig.is_active == True
        ).first()
        
        if not config:
            # 返回默认值或空配置
            return {
                "id": None,
                "api_key": "****",
                "base_url": "https://api.deepseek.com",
                "model": "deepseek-chat",
                "is_active": False,
                "rate_limit_per_minute": 10,
                "rate_limit_per_day": 500,
                "message": "未配置，使用默认值或环境变量"
            }
    
    return config.to_dict(include_api_key=True)


@router.post("/config")
async def create_deepseek_config(
    config_data: DeepSeekConfigCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建DeepSeek配置（管理员权限）"""
    check_admin_permission(current_user)
    
    # 检查是否已有启用的配置
    existing_active = db.query(DeepSeekConfig).filter(
        DeepSeekConfig.is_active == True
    ).first()
    
    if existing_active and config_data.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已有启用的配置，请先禁用现有配置或更新现有配置"
        )
    
    # 创建新配置
    config = DeepSeekConfig(
        api_key=config_data.api_key,
        base_url=config_data.base_url,
        model=config_data.model,
        is_active=config_data.is_active if config_data.is_active is not None else True,
        rate_limit_per_minute=config_data.rate_limit_per_minute,
        rate_limit_per_day=config_data.rate_limit_per_day
    )
    
    db.add(config)
    db.commit()
    db.refresh(config)
    
    # 记录日志（使用warning级别，因为创建配置是重要操作）
    log_service = LogService(db)
    log_service.add_log(
        f"管理员 {current_user.username} 创建了DeepSeek配置 (ID: {config.id})",
        level="warning",
        module="deepseek_config",
        user_id=current_user.id
    )
    
    return {
        "success": True,
        "message": "配置创建成功",
        "config": config.to_dict(include_api_key=True)
    }


@router.put("/config/{config_id}")
async def update_deepseek_config(
    config_id: int,
    config_update: DeepSeekConfigUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新DeepSeek配置（管理员权限）"""
    check_admin_permission(current_user)
    
    config = db.query(DeepSeekConfig).filter(DeepSeekConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置不存在"
        )
    
    update_data = config_update.dict(exclude_unset=True)
    
    # 如果要启用此配置，需要先禁用其他启用的配置
    if update_data.get("is_active") is True:
        db.query(DeepSeekConfig).filter(
            DeepSeekConfig.id != config_id,
            DeepSeekConfig.is_active == True
        ).update({"is_active": False})
    
    # 更新配置
    for key, value in update_data.items():
        if value is not None:
            setattr(config, key, value)
    
    db.commit()
    db.refresh(config)
    
    # 记录日志（使用warning级别，因为更新配置是重要操作）
    log_service = LogService(db)
    log_service.add_log(
        f"管理员 {current_user.username} 更新了DeepSeek配置 (ID: {config_id})",
        level="warning",
        module="deepseek_config",
        user_id=current_user.id
    )
    
    return {
        "success": True,
        "message": "配置更新成功",
        "config": config.to_dict(include_api_key=True)
    }


@router.delete("/config/{config_id}")
async def delete_deepseek_config(
    config_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除DeepSeek配置（管理员权限）"""
    check_admin_permission(current_user)
    
    config = db.query(DeepSeekConfig).filter(DeepSeekConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置不存在"
        )
    
    # 记录删除的配置信息
    config_info = f"API Key: {config.api_key[:4]}****, Base URL: {config.base_url}, Model: {config.model}"
    
    db.delete(config)
    db.commit()
    
    # 记录日志
    log_service = LogService(db)
    log_service.add_log(
        f"管理员 {current_user.username} 删除了DeepSeek配置 (ID: {config_id}, {config_info})",
        level="warning",
        module="deepseek_config",
        user_id=current_user.id
    )
    
    return {
        "success": True,
        "message": "配置删除成功"
    }


@router.post("/config/{config_id}/toggle")
async def toggle_deepseek_config(
    config_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """切换DeepSeek配置的启用状态（管理员权限）"""
    check_admin_permission(current_user)
    
    config = db.query(DeepSeekConfig).filter(DeepSeekConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置不存在"
        )
    
    # 如果要启用，先禁用其他配置
    if not config.is_active:
        db.query(DeepSeekConfig).filter(
            DeepSeekConfig.id != config_id,
            DeepSeekConfig.is_active == True
        ).update({"is_active": False})
    
    # 切换状态
    config.is_active = not config.is_active
    db.commit()
    db.refresh(config)
    
    # 记录日志（使用warning级别，因为切换配置状态是重要操作）
    log_service = LogService(db)
    action = "启用" if config.is_active else "禁用"
    log_service.add_log(
        f"管理员 {current_user.username} {action}了DeepSeek配置 (ID: {config_id})",
        level="warning",
        module="deepseek_config",
        user_id=current_user.id
    )
    
    return {
        "success": True,
        "message": f"配置已{action}",
        "config": config.to_dict(include_api_key=True)
    }

