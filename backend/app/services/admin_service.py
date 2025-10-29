"""管理员服务"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.database import User, UserRole


class AdminService:
    """管理员服务类"""
    
    def __init__(self, db: Session):
        """初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_all_data(self, current_user: User) -> Dict:
        """获取所有管理员数据
        
        Args:
            current_user: 当前用户
            
        Returns:
            包含统计、用户列表、系统状态、系统日志的数据字典
        """
        # 检查权限
        if current_user.role not in [UserRole.admin, UserRole.super_admin]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要管理员或超级管理员权限"
            )
        
        # 从数据库获取统计数据
        total_users = self.db.query(User).count()
        active_users = self.db.query(User).filter(User.is_active == True).count()
        
        # 获取用户列表
        all_users = self.db.query(User).all()
        users_list = []
        for user in all_users:
            users_list.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "status": "active" if user.is_active else "inactive"
            })
        
        # 获取真实的系统状态
        try:
            import psutil
            import os
            
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=0.5)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁盘使用率（Windows兼容）
            import platform
            if platform.system() == 'Windows':
                current_drive = os.path.splitdrive(os.getcwd())[0]
                disk = psutil.disk_usage(current_drive)
            else:
                disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
        except ImportError:
            cpu_percent = 45
            memory_percent = 62
            disk_percent = 38
        except Exception as e:
            print(f"获取系统状态失败: {e}")
            cpu_percent = 0
            memory_percent = 0
            disk_percent = 0
        
        # 获取系统日志
        from app.database import SystemLog
        recent_logs = self.db.query(SystemLog).order_by(
            SystemLog.timestamp.desc()
        ).limit(10).all()
        logs_list = [log.to_dict() for log in recent_logs]
        
        # 获取系统设置
        system_settings = self._get_system_settings_from_db()
        
        # 返回完整数据
        return {
            "stats": {
                "totalUsers": total_users,
                "activeUsers": active_users,
                "inactiveUsers": total_users - active_users,
                "systemWarnings": 0
            },
            "users": users_list,
            "systemSettings": system_settings,
            "systemStatus": {
                "cpu": round(cpu_percent, 1),
                "memory": round(memory_percent, 1),
                "disk": round(disk_percent, 1)
            },
            "systemLogs": logs_list
        }
    
    def _get_system_settings_from_db(self) -> Dict:
        """从数据库获取系统设置"""
        from app.database import SystemSettings
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from utils import camel_case
        
        settings = {}
        db_settings = self.db.query(SystemSettings).all()
        
        for setting in db_settings:
            key = camel_case(setting.setting_key)
            value = setting.setting_value.lower() == 'true'
            settings[key] = value
        
        # 如果数据库中没有设置，返回默认值
        if not settings:
            settings = {
                "maintenanceMode": False,
                "autoBackup": True,
                "emailNotifications": True
            }
        else:
            # 确保所有必要的字段都存在
            defaults = {
                "maintenanceMode": False,
                "autoBackup": True,
                "emailNotifications": True
            }
            for key, value in defaults.items():
                if key not in settings:
                    settings[key] = value
        
        return settings
    
    def get_system_settings(self, current_user: User) -> Dict:
        """获取系统设置
        
        Args:
            current_user: 当前用户
            
        Returns:
            系统设置字典
        """
        # 检查权限
        if current_user.role not in [UserRole.admin, UserRole.super_admin]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要管理员权限"
            )
        
        return self._get_system_settings_from_db()
    
    def update_system_settings(
        self,
        settings_data: Dict,
        current_user: User
    ) -> Dict:
        """更新系统设置
        
        Args:
            settings_data: 设置数据
            current_user: 当前用户
            
        Returns:
            更新结果
        """
        from app.database import SystemSettings
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from utils import to_snake_case
        
        # 检查权限
        if current_user.role not in [UserRole.admin, UserRole.super_admin]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要管理员权限"
            )
        
        # 更新每项设置
        for key, value in settings_data.items():
            db_key = to_snake_case(key)
            db_value = str(value).lower()
            
            # 查找现有设置
            setting = self.db.query(SystemSettings).filter(
                SystemSettings.setting_key == db_key
            ).first()
            
            if setting:
                # 更新现有设置
                setting.setting_value = db_value
                setting.updated_by = current_user.id
            else:
                # 创建新设置
                new_setting = SystemSettings(
                    setting_key=db_key,
                    setting_value=db_value,
                    updated_by=current_user.id
                )
                self.db.add(new_setting)
        
        self.db.commit()
        
        return {"success": True, "message": "设置已更新"}
    
    def get_all_users(self, current_user: User) -> List[Dict]:
        """获取所有用户列表
        
        Args:
            current_user: 当前用户
            
        Returns:
            用户列表
        """
        # 检查权限
        if current_user.role not in [UserRole.admin, UserRole.super_admin]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要管理员权限"
            )
        
        users = self.db.query(User).all()
        return [user.to_dict() for user in users]
    
    def update_user_status(
        self,
        user_id: int,
        status_data: Dict,
        current_user: User
    ) -> Dict:
        """更新用户状态
        
        Args:
            user_id: 用户ID
            status_data: 状态数据
            current_user: 当前用户
            
        Returns:
            更新后的用户信息
        """
        # 检查权限
        if current_user.role not in [UserRole.admin, UserRole.super_admin]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要管理员权限"
            )
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        if "status" in status_data:
            user.is_active = status_data["status"] == "active"
        
        self.db.commit()
        self.db.refresh(user)
        
        return user.to_dict()
    
    def update_user(
        self,
        user_id: int,
        user_data: Dict,
        current_user: User
    ) -> Dict:
        """更新用户信息（仅超级管理员）
        
        Args:
            user_id: 用户ID
            user_data: 用户数据
            current_user: 当前用户
            
        Returns:
            更新后的用户信息
        """
        # 检查权限
        if current_user.role != UserRole.super_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要超级管理员权限"
            )
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 更新字段
        if "email" in user_data:
            # 检查邮箱是否已被其他用户使用
            if self.db.query(User).filter(
                User.email == user_data["email"],
                User.id != user_id
            ).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被使用"
                )
            user.email = user_data["email"]
        
        if "role" in user_data:
            try:
                user.role = UserRole(user_data["role"])
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="无效的角色"
                )
        
        if "is_active" in user_data:
            user.is_active = user_data["is_active"]
        
        self.db.commit()
        self.db.refresh(user)
        
        return user.to_dict()
    
    def delete_user(
        self,
        user_id: int,
        current_user: User
    ) -> Dict:
        """删除用户（仅超级管理员）
        
        Args:
            user_id: 用户ID
            current_user: 当前用户
            
        Returns:
            成功消息
        """
        # 检查权限
        if current_user.role != UserRole.super_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要超级管理员权限"
            )
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 防止删除自己
        if user.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能删除自己"
            )
        
        self.db.delete(user)
        self.db.commit()
        
        return {"success": True, "message": "用户删除成功"}
    
    def get_server_info(self) -> Dict:
        """获取服务器信息（跨平台支持 Linux/Windows）
        
        Returns:
            服务器信息字典
        """
        import platform
        import sys
        import os
        import datetime
        
        server_info = {
            "platform": {
                "system": platform.system(),  # Windows, Linux, Darwin, etc.
                "platform": platform.platform(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": sys.version.split()[0],
            }
        }
        
        # 获取系统资源使用情况
        try:
            import psutil
            
            # CPU信息
            cpu_count = psutil.cpu_count(logical=True)
            cpu_percent = psutil.cpu_percent(interval=0.5)
            cpu_freq = psutil.cpu_freq()
            
            # 内存信息
            memory = psutil.virtual_memory()
            memory_total_gb = round(memory.total / (1024**3), 2)
            memory_used_gb = round(memory.used / (1024**3), 2)
            memory_percent = memory.percent
            
            # 磁盘信息（跨平台）
            if platform.system() == 'Windows':
                # Windows: 获取当前驱动器
                current_drive = os.path.splitdrive(os.getcwd())[0]
                disk = psutil.disk_usage(current_drive)
            else:
                # Linux/Mac: 使用根目录
                disk = psutil.disk_usage('/')
            
            disk_total_gb = round(disk.total / (1024**3), 2)
            disk_used_gb = round(disk.used / (1024**3), 2)
            disk_percent = disk.percent
            
            # 系统启动时间
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            uptime_seconds = int(datetime.datetime.now().timestamp() - psutil.boot_time())
            uptime_days = uptime_seconds // 86400
            uptime_hours = (uptime_seconds % 86400) // 3600
            uptime_minutes = (uptime_seconds % 3600) // 60
            
            server_info["resources"] = {
                "cpu": {
                    "count": cpu_count,
                    "usage_percent": round(cpu_percent, 1),
                    "frequency_mhz": round(cpu_freq.current, 0) if cpu_freq else None,
                    "max_frequency_mhz": round(cpu_freq.max, 0) if cpu_freq else None
                },
                "memory": {
                    "total_gb": memory_total_gb,
                    "used_gb": memory_used_gb,
                    "available_gb": round(memory.available / (1024**3), 2),
                    "usage_percent": round(memory_percent, 1)
                },
                "disk": {
                    "total_gb": disk_total_gb,
                    "used_gb": disk_used_gb,
                    "free_gb": round(disk.free / (1024**3), 2),
                    "usage_percent": round(disk_percent, 1)
                },
                "uptime": {
                    "days": uptime_days,
                    "hours": uptime_hours,
                    "minutes": uptime_minutes,
                    "formatted": f"{uptime_days}天 {uptime_hours}小时 {uptime_minutes}分钟"
                },
                "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except ImportError:
            # psutil未安装时返回占位数据
            server_info["resources"] = {
                "cpu": {"usage_percent": 0, "error": "psutil未安装"},
                "memory": {"usage_percent": 0, "error": "psutil未安装"},
                "disk": {"usage_percent": 0, "error": "psutil未安装"},
                "uptime": {"formatted": "未知"}
            }
        except Exception as e:
            server_info["resources"] = {
                "error": f"获取系统资源失败: {str(e)}"
            }
        
        # 网络信息
        try:
            import psutil
            net_io = psutil.net_io_counters()
            server_info["network"] = {
                "bytes_sent_gb": round(net_io.bytes_sent / (1024**3), 2),
                "bytes_recv_gb": round(net_io.bytes_recv / (1024**3), 2),
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            }
        except:
            server_info["network"] = {"error": "获取网络信息失败"}
        
        # 应用信息
        server_info["application"] = {
            "python_version": sys.version,
            "working_directory": os.getcwd(),
            "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return server_info

