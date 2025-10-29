"""用户服务"""

from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.database import User


class UserService:
    """用户服务类"""
    
    def __init__(self, db: Session):
        """初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_user_profile(self, user_id: int) -> Dict:
        """获取用户资料
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户资料
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 获取偏好设置
        preferences = {}
        if user.preferences:
            import json
            try:
                preferences = json.loads(user.preferences)
            except:
                preferences = {}
        
        # 获取教务系统绑定信息
        from app.database import EduAccountBinding
        edu_binding = self.db.query(EduAccountBinding).filter(
            EduAccountBinding.user_id == user_id,
            EduAccountBinding.is_active == True
        ).first()
        
        edu_binding_info = {
            "isBound": False,
            "refreshFrequency": None,
            "boundAt": None
        }
        
        if edu_binding:
            edu_binding_info = {
                "isBound": True,
                "refreshFrequency": float(edu_binding.refresh_frequency) if edu_binding.refresh_frequency else 1.0,
                "boundAt": edu_binding.created_at.isoformat() if edu_binding.created_at else None
            }
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "is_active": user.is_active,
            "bio": user.bio,
            "avatar_url": user.avatar_url,
            "preferences": preferences,
            "eduBinding": edu_binding_info,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    
    def update_profile(
        self,
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
        bio: Optional[str] = None,
        avatar_url: Optional[str] = None
    ) -> Dict:
        """更新用户资料
        
        Args:
            user_id: 用户ID
            username: 新用户名
            email: 新邮箱
            bio: 个人介绍
            avatar_url: 头像URL
            
        Returns:
            更新后的用户信息
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 更新字段
        if username is not None:
            # 检查用户名是否已被其他用户使用
            if self.db.query(User).filter(
                User.username == username,
                User.id != user_id
            ).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名已被使用"
                )
            user.username = username
        
        if email is not None:
            # 检查邮箱是否已被其他用户使用
            if self.db.query(User).filter(
                User.email == email,
                User.id != user_id
            ).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被使用"
                )
            user.email = email
        
        if bio is not None:
            if len(bio) > 500:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="个人介绍长度不能超过500字符"
                )
            user.bio = bio
        
        if avatar_url is not None:
            user.avatar_url = avatar_url
        
        self.db.commit()
        self.db.refresh(user)
        
        return user.to_dict()
    
    def update_preferences(self, user_id: int, preferences: Dict) -> Dict:
        """更新用户偏好设置
        
        Args:
            user_id: 用户ID
            preferences: 偏好设置字典
            
        Returns:
            更新后的偏好设置
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 读取现有偏好
        import json
        existing_preferences = {}
        if user.preferences:
            try:
                existing_preferences = json.loads(user.preferences)
            except:
                existing_preferences = {}
        
        # 合并新偏好
        existing_preferences.update(preferences)
        
        # 保存到数据库
        user.preferences = json.dumps(existing_preferences)
        self.db.commit()
        self.db.refresh(user)
        
        return existing_preferences
    
    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> Dict:
        """修改密码
        
        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            成功消息
        """
        from app.auth import verify_password, get_password_hash
        
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 验证旧密码
        if not verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="旧密码不正确"
            )
        
        # 检查新密码长度
        if len(new_password) < 6 or len(new_password) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="新密码长度必须在6-50个字符之间"
            )
        
        # 检查新旧密码是否相同
        if verify_password(new_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="新密码不能与旧密码相同"
            )
        
        # 更新密码
        user.password_hash = get_password_hash(new_password)
        self.db.commit()
        
        return {"success": True, "message": "密码修改成功"}

