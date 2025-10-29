"""系统日志服务"""

from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from datetime import datetime


class LogService:
    """系统日志服务类"""
    
    def __init__(self, db: Session):
        """初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def add_log(
        self,
        message: str,
        level: str = "info",
        module: str = None,
        user_id: int = None
    ) -> None:
        """添加系统日志
        
        注意：只保存warning和error级别的日志到数据库，info级别不保存
        
        Args:
            message: 日志消息
            level: 日志级别 (info/warning/error)
            module: 模块名称
            user_id: 用户ID
        """
        # 只保存warning和error级别的日志
        if level not in ["warning", "error"]:
            # info级别只打印到控制台，不保存到数据库
            print(f"[{level.upper()}] [{module or 'system'}] {message}")
            return
        
        try:
            from app.database import SystemLog
            
            log = SystemLog(
                level=level,
                message=message,
                module=module,
                user_id=user_id,
                timestamp=datetime.now()
            )
            
            self.db.add(log)
            self.db.commit()
            
            # 同时在控制台输出
            print(f"[{level.upper()}] [{module or 'system'}] {message}")
        except Exception as e:
            self.db.rollback()
            print(f"记录日志失败: {e}")
            # 即使数据库保存失败，也在控制台输出
            print(f"[{level.upper()}] [{module or 'system'}] {message}")
    
    def get_logs(
        self,
        level: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """获取系统日志
        
        注意：数据库中只有warning和error级别的日志
        
        Args:
            level: 日志级别过滤 (warning/error)
            limit: 返回日志条数
            
        Returns:
            日志列表（只包含warning和error级别）
        """
        from app.database import SystemLog
        
        query = self.db.query(SystemLog)
        
        # 如果指定了级别，过滤（只允许warning和error）
        if level:
            if level not in ["warning", "error"]:
                raise ValueError("只能查询warning或error级别的日志（数据库中没有info级别）")
            query = query.filter(SystemLog.level == level)
        else:
            # 默认只返回warning和error
            query = query.filter(SystemLog.level.in_(["warning", "error"]))
        
        # 按时间倒序，限制数量
        logs = query.order_by(SystemLog.timestamp.desc()).limit(limit).all()
        
        # 转换为字典
        return [log.to_dict() for log in logs]
    
    def get_recent_logs(self, limit: int = 10) -> List[Dict]:
        """获取最近日志
        
        Args:
            limit: 返回条数
            
        Returns:
            日志列表
        """
        return self.get_logs(limit=limit)

