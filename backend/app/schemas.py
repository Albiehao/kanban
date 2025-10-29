from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime, date as date_type
import re


# ============ 健康检查 ============
class HealthResponse(BaseModel):
    status: str


# ============ 认证模型 ============
class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="用户名，3-20个字符，只能包含字母、数字和下划线")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=6, max_length=100, description="密码，至少6个字符")
    role: str = Field("user", description="用户角色")
    
    @validator('username', always=True)
    def validate_username(cls, v):
        """验证用户名格式"""
        if v and not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v
    
    @validator('password', always=True)
    def validate_password(cls, v):
        """验证密码长度"""
        if v and len(v) < 6:
            raise ValueError('密码长度至少为6个字符')
        return v
    
    @validator('role', always=True)
    def validate_role(cls, v):
        """验证角色"""
        allowed_roles = ['user', 'admin', 'super_admin']
        if v and v not in allowed_roles:
            return 'user'
        return v or 'user'
    
    class Config:
        schema_extra = {
            "example": {
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "role": "user"
            }
        }


class TokenResponse(BaseModel):
    success: bool
    token: str
    user: dict
    message: str


class RefreshTokenResponse(BaseModel):
    token: str
    success: bool


class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    role: str
    permissions: List[str]


class VerifyResponse(BaseModel):
    valid: bool
    user: UserInfo


# ============ 任务模型 ============
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    date: str
    time: Optional[str] = None
    has_reminder: bool = False
    reminder_time: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    has_reminder: Optional[bool] = None
    reminder_time: Optional[str] = None


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    priority: str
    date: str
    time: Optional[str] = None
    has_reminder: bool = False
    reminder_time: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ============ 财务模型 ============
class TransactionCreate(BaseModel):
    type: str
    amount: float = Field(..., gt=0, description="金额必须大于0")
    category: str
    description: str = Field(..., max_length=255, description="描述信息，最大255字符")
    date: str
    time: Optional[str] = None  # 可选，格式：HH:MM 或 HH:MM:SS
    
    @validator('type')
    def validate_type(cls, v):
        if v not in ['income', 'expense']:
            raise ValueError('type必须是income或expense')
        return v
    
    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError('date格式错误，应为YYYY-MM-DD')
        return v
    
    @validator('time')
    def validate_time(cls, v):
        if v is not None:
            # 支持 HH:MM 或 HH:MM:SS 格式
            time_formats = ["%H:%M", "%H:%M:%S"]
            valid = False
            for fmt in time_formats:
                try:
                    datetime.strptime(v, fmt)
                    valid = True
                    break
                except ValueError:
                    continue
            if not valid:
                raise ValueError('time格式错误，应为HH:MM或HH:MM:SS')
        return v


class TransactionUpdate(BaseModel):
    type: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0, description="金额必须大于0")
    category: Optional[str] = None
    description: Optional[str] = Field(None, max_length=255)
    date: Optional[str] = None
    time: Optional[str] = None  # 可选，格式：HH:MM 或 HH:MM:SS
    
    @validator('type')
    def validate_type(cls, v):
        if v is not None and v not in ['income', 'expense']:
            raise ValueError('type必须是income或expense')
        return v
    
    @validator('date')
    def validate_date(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError('date格式错误，应为YYYY-MM-DD')
        return v
    
    @validator('time')
    def validate_time(cls, v):
        if v is not None:
            # 支持 HH:MM 或 HH:MM:SS 格式
            time_formats = ["%H:%M", "%H:%M:%S"]
            valid = False
            for fmt in time_formats:
                try:
                    datetime.strptime(v, fmt)
                    valid = True
                    break
                except ValueError:
                    continue
            if not valid:
                raise ValueError('time格式错误，应为HH:MM或HH:MM:SS')
        return v


class Transaction(BaseModel):
    id: int
    type: str
    amount: float
    category: str
    description: str
    date: str
    time: Optional[str] = None  # 时间，格式：HH:MM:SS
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ============ 课程模型 ============
class CourseCreate(BaseModel):
    course_name: str
    classroom: str
    date: str
    teacher: str
    periods: str


class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    classroom: Optional[str] = None
    date: Optional[str] = None
    teacher: Optional[str] = None
    periods: Optional[str] = None


class Course(BaseModel):
    id: Optional[int] = None
    course_name: str
    classroom: str
    date: str
    teacher: str
    periods: str


# ============ AI助手模型 ============
class ChatRequest(BaseModel):
    """AI聊天请求"""
    message: str = Field(..., min_length=1, max_length=2000, description="用户消息，长度限制1-2000字符")


class ChatMessage(BaseModel):
    id: int
    role: str
    content: str
    timestamp: str


class ConversationCreate(BaseModel):
    title: str


class Conversation(BaseModel):
    id: int
    messages: List[ChatMessage]
    title: str
    createdAt: str
    updatedAt: str


# ============ 用户设置模型 ============
class UserProfile(BaseModel):
    username: str
    email: str
    bio: str
    avatar: str
    completedTasks: int
    inProgressTasks: int
    daysJoined: int


class UserProfileUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    email: Optional[EmailStr] = None
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None
    
    @validator('username')
    def validate_username(cls, v):
        """验证用户名格式"""
        if v is not None:
            if not re.match(r'^[a-zA-Z0-9_]+$', v):
                raise ValueError('用户名只能包含字母、数字和下划线')
            if len(v) < 3 or len(v) > 20:
                raise ValueError('用户名长度必须在3-20个字符之间')
        return v


class UserPreferences(BaseModel):
    darkMode: bool
    emailNotifications: bool
    desktopNotifications: bool


class UserPreferencesUpdate(BaseModel):
    darkMode: Optional[bool] = None
    emailNotifications: Optional[bool] = None
    desktopNotifications: Optional[bool] = None


# ============ 通知模型 ============
class Notification(BaseModel):
    id: int
    type: str
    title: str
    message: Optional[str] = None
    read: bool
    created_at: Optional[str] = None


# ============ 管理员模型 ============
class AdminStats(BaseModel):
    totalUsers: int
    activeCourses: int
    pendingTasks: int
    systemWarnings: int


class AdminUser(BaseModel):
    id: int
    username: str
    email: str
    status: str


class AdminSettings(BaseModel):
    maintenanceMode: bool
    autoBackup: bool
    emailNotifications: bool


class SystemStatus(BaseModel):
    cpu: int
    memory: int
    disk: int


class SystemLog(BaseModel):
    id: int
    level: str
    message: str
    timestamp: str

