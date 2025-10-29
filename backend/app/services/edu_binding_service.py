"""教务系统绑定服务"""

from typing import Dict, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.database import EduAccountBinding


class EduBindingService:
    """教务系统绑定服务类"""
    
    def __init__(self, db: Session):
        """初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def bind_account(self, user_id: int, api_key: str, api_url: str = None, refresh_frequency: float = 1.0) -> Dict:
        """绑定第三方API密钥
        
        Args:
            user_id: 用户ID
            api_key: 第三方API密钥
            api_url: 第三方API服务器地址（可选）
            refresh_frequency: 刷新频率（小时）
            
        Returns:
            绑定结果
        """
        # 如果没有提供 api_url，使用默认值
        if not api_url:
            api_url = "http://160.202.229.142:8000/api/v1/api/courses"
        
        # 检查是否已存在绑定
        existing = self.db.query(EduAccountBinding).filter(
            EduAccountBinding.user_id == user_id
        ).first()
        
        if existing:
            # 更新现有绑定
            existing.api_key = api_key
            existing.api_url = api_url
            existing.refresh_frequency = str(refresh_frequency)
            existing.is_active = True
        else:
            # 创建新绑定
            binding = EduAccountBinding(
                user_id=user_id,
                api_key=api_key,
                api_url=api_url,
                refresh_frequency=str(refresh_frequency),
                is_active=True
            )
            self.db.add(binding)
        
        try:
            self.db.commit()
            return {"success": True, "message": "教务系统账号绑定成功"}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="绑定失败"
            )
    
    def get_binding(self, user_id: int) -> Dict:
        """获取绑定状态
        
        Args:
            user_id: 用户ID
            
        Returns:
            绑定状态
        """
        binding = self.db.query(EduAccountBinding).filter(
            EduAccountBinding.user_id == user_id,
            EduAccountBinding.is_active == True
        ).first()
        
        if binding:
            # 密钥脱敏处理
            api_key = binding.api_key
            if api_key and len(api_key) > 8:
                masked_key = api_key[:4] + "****" + api_key[-4:]
            elif api_key:
                masked_key = "****"
            else:
                masked_key = None
            
            return {
                "isBound": True,
                "apiPath": binding.api_url or "http://160.202.229.142:8000/api/v1/api/courses",
                "apiKey": masked_key,
                "boundAt": binding.created_at.isoformat() if binding.created_at else None,
                "refreshFrequency": float(binding.refresh_frequency) if binding.refresh_frequency else 1.0
            }
        else:
            return {
                "isBound": False,
                "apiPath": None,
                "apiKey": None,
                "boundAt": None,
                "refreshFrequency": None
            }
    
    def get_binding_for_crawler(self, user_id: int) -> Optional[Dict]:
        """获取绑定信息供爬虫使用（包含密码）
        
        Args:
            user_id: 用户ID
            
        Returns:
            绑定信息（包含密码）或None
        """
        binding = self.db.query(EduAccountBinding).filter(
            EduAccountBinding.user_id == user_id,
            EduAccountBinding.is_active == True
        ).first()
        
        if binding:
            return {
                "api_key": binding.api_key,
                "api_url": binding.api_url or "http://160.202.229.142:8000/api/v1/api/courses",
                "refresh_frequency": float(binding.refresh_frequency) if binding.refresh_frequency else 1.0
            }
        return None
    
    def unbind_account(self, user_id: int) -> Dict:
        """解绑教务系统账号
        
        Args:
            user_id: 用户ID
            
        Returns:
            解绑结果
        """
        binding = self.db.query(EduAccountBinding).filter(
            EduAccountBinding.user_id == user_id,
            EduAccountBinding.is_active == True
        ).first()
        
        if binding:
            binding.is_active = False
            try:
                self.db.commit()
                return {"success": True, "message": "已解绑教务系统账号"}
            except Exception as e:
                self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="解绑失败"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到绑定信息"
            )

