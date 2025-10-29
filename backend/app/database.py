from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Enum, Text, Date, Time, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import enum
import os
from decimal import Decimal
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# MySQL数据库配置（支持环境变量）
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345678")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "todo_db")

# 构建数据库连接URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# 用户角色枚举
class UserRole(str, enum.Enum):
    user = "user"  # 普通用户
    admin = "admin"  # 管理员
    super_admin = "super_admin"  # 超级管理员


# 用户模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    is_active = Column(Boolean, default=True)
    bio = Column(String(500), nullable=True)  # 个人介绍
    avatar_url = Column(String(255), nullable=True)  # 头像URL
    preferences = Column(Text, nullable=True)  # 偏好设置（JSON格式）
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "is_active": self.is_active,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# 系统日志模型
class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False, index=True)  # info, warning, error
    message = Column(String(500), nullable=False)
    module = Column(String(50), nullable=True)  # 模块名称，如 "auth", "admin"等
    user_id = Column(Integer, nullable=True)  # 关联用户ID
    timestamp = Column(DateTime, default=datetime.now, index=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level,
            "message": self.message,
            "module": self.module,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


# 通知模型
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    type = Column(String(50), nullable=False)  # task_reminder, system, etc.
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, index=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "message": self.message,
            "read": self.read,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# 系统设置模型
class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(50), unique=True, nullable=False, index=True)
    setting_value = Column(Text, nullable=False)
    description = Column(String(200), nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    updated_by = Column(Integer, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "setting_key": self.setting_key,
            "setting_value": self.setting_value,
            "description": self.description,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "updated_by": self.updated_by
        }


# DeepSeek API配置模型（系统级别配置）
class DeepSeekConfig(Base):
    __tablename__ = "deepseek_configs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    api_key = Column(String(255), nullable=False, comment="DeepSeek API密钥")
    base_url = Column(String(255), nullable=False, default="https://api.deepseek.com", comment="DeepSeek API基础URL")
    model = Column(String(50), nullable=False, default="deepseek-chat", comment="使用的模型名称")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    rate_limit_per_minute = Column(Integer, default=10, nullable=False, comment="每分钟请求限制")
    rate_limit_per_day = Column(Integer, default=500, nullable=False, comment="每日请求限制")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def to_dict(self, include_api_key=False):
        """转换为字典"""
        result = {
            "id": self.id,
            "base_url": self.base_url,
            "model": self.model,
            "is_active": self.is_active,
            "rate_limit_per_minute": self.rate_limit_per_minute,
            "rate_limit_per_day": self.rate_limit_per_day,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        if include_api_key:
            # 脱敏处理
            if self.api_key and len(self.api_key) > 8:
                result["api_key"] = self.api_key[:4] + "****" + self.api_key[-4:]
            else:
                result["api_key"] = "****"
        return result


# 教务系统绑定模型（用于存储第三方API配置）
class EduAccountBinding(Base):
    __tablename__ = "edu_account_bindings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    api_key = Column(String(255), nullable=False)  # 第三方API密钥
    api_url = Column(String(255), nullable=True)  # 第三方API服务器地址
    refresh_frequency = Column(String(10), default="1.0")  # 刷新频率（小时）
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self, include_api_key=False):
        result = {
            "id": self.id,
            "user_id": self.user_id,
            "api_url": self.api_url or "http://160.202.229.142:8000/api/v1/api/courses",
            "refresh_frequency": float(self.refresh_frequency) if self.refresh_frequency else 1.0,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        if include_api_key:
            result["api_key"] = self.api_key
        return result


# 课程表模型
class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    course_name = Column(String(100), nullable=False)
    classroom = Column(String(50), nullable=True)
    date = Column(String(50), nullable=False)
    teacher = Column(String(50), nullable=True)
    periods = Column(String(50), nullable=True)  # 节次
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_name": self.course_name,
            "classroom": self.classroom,
            "date": self.date,
            "teacher": self.teacher,
            "periods": self.periods,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# 任务优先级枚举
class TaskPriority(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"


# 任务模型
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(String(50), nullable=True)
    has_reminder = Column(Boolean, default=False)
    reminder_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority.value if isinstance(self.priority, TaskPriority) else self.priority,
            "date": self.date.isoformat() if self.date else None,
            "time": self.time,
            "has_reminder": self.has_reminder,
            "reminder_time": self.reminder_time.isoformat() if self.reminder_time else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# 交易类型枚举
class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"


# 交易记录模型
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=True)  # 具体时间，可选
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type.value if isinstance(self.type, TransactionType) else self.type,
            "amount": float(self.amount) if isinstance(self.amount, Decimal) else self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
            "time": self.time.strftime("%H:%M:%S") if self.time else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# 创建数据库表
def create_tables():
    Base.metadata.create_all(bind=engine)


# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

