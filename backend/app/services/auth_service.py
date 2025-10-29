"""认证服务"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.database import User
from app.auth import verify_password, create_access_token


class AuthService:
    """认证服务类"""
    
    def __init__(self, db: Session):
        """初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def authenticate_user(self, username: str, password: str) -> dict:
        """用户认证
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            包含token和用户信息的字典
            
        Raises:
            HTTPException: 认证失败
        """
        # 查找用户
        user = self.db.query(User).filter(User.username == username).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 验证密码
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 检查用户是否激活
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户已被停用"
            )
        
        # 创建token
        access_token = create_access_token(data={"sub": user.username})
        
        return {
            "success": True,
            "token": access_token,
            "user": user.to_dict(),
            "message": "登录成功"
        }
    
    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        role: str = "user"
    ) -> dict:
        """用户注册
        
        Args:
            username: 用户名
            email: 邮箱
            password: 密码
            role: 角色
            
        Returns:
            用户信息
            
        Raises:
            HTTPException: 注册失败
        """
        from app.auth import get_password_hash
        from app.database import UserRole
        
        # 检查用户名是否已存在
        if self.db.query(User).filter(User.username == username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if self.db.query(User).filter(User.email == email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
        
        # 创建新用户
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            role=UserRole(role)
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user.to_dict()

