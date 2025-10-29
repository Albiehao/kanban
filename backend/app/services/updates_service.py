"""实时更新服务"""

from typing import Dict, Set, Optional, AsyncGenerator, Callable
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import Task, User
import asyncio


class UpdatesService:
    """实时更新服务类"""
    
    def __init__(self):
        """初始化更新服务"""
        # 存储活跃的SSE连接（用户ID -> 回调函数列表）
        self.connections: Dict[int, list] = {}
        
        # 上次检查时间（用于轮询数据库）
        self.last_check: Dict[int, datetime] = {}
    
    def subscribe(self, user_id: int, callback: Callable):
        """订阅用户更新
        
        Args:
            user_id: 用户ID
            callback: 回调函数，接收更新事件
        """
        if user_id not in self.connections:
            self.connections[user_id] = []
        self.connections[user_id].append(callback)
    
    def unsubscribe(self, user_id: int, callback: Callable):
        """取消订阅
        
        Args:
            user_id: 用户ID
            callback: 要移除的回调函数
        """
        if user_id in self.connections:
            try:
                self.connections[user_id].remove(callback)
                if not self.connections[user_id]:
                    del self.connections[user_id]
            except ValueError:
                pass
    
    async def broadcast_update(self, user_id: int, event: Dict):
        """广播更新事件给用户的所有连接
        
        Args:
            user_id: 用户ID
            event: 更新事件字典
        """
        if user_id in self.connections:
            for callback in self.connections[user_id]:
                try:
                    await callback(event)
                except Exception as e:
                    print(f"[UpdatesService] 广播更新失败: {e}")
    
    async def check_changes(
        self,
        db: Session,
        user_id: int,
        subscribed_types: Set[str],
        since: Optional[datetime] = None
    ) -> list:
        """检查数据库变更
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            subscribed_types: 订阅的数据类型集合
            since: 检查变更的时间起点
            
        Returns:
            变更事件列表
        """
        events = []
        
        if since is None:
            # 如果没有指定时间，检查最近1分钟的数据
            since = datetime.now() - timedelta(minutes=1)
        
        # 检查任务变更
        if "tasks" in subscribed_types:
            try:
                # 查询自指定时间后创建或更新的任务
                tasks = db.query(Task).filter(
                    Task.user_id == user_id,
                    Task.updated_at >= since
                ).all()
                
                for task in tasks:
                    # 判断是创建还是更新
                    # 简单判断：如果创建时间和更新时间很接近（1秒内），认为是创建
                    time_diff = (task.updated_at - task.created_at).total_seconds()
                    action = "created" if time_diff < 2 else "updated"
                    
                    events.append({
                        "type": "task",
                        "action": action,
                        "data": task.to_dict(),
                        "timestamp": task.updated_at.isoformat() if task.updated_at else datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"[UpdatesService] 检查任务变更失败: {e}")
        
        # 课程变更检查（课程来自第三方API，这里主要是通知有新数据）
        # 实际实现可能需要缓存或定时检查
        
        return events
    
    async def event_stream(
        self,
        db: Session,
        user_id: int,
        subscribed_types: Set[str],
        since: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """生成SSE事件流
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            subscribed_types: 订阅的数据类型集合
            since: ISO格式的时间戳字符串
            
        Yields:
            SSE格式的事件字符串
        """
        import json
        
        # 解析since时间
        since_time = None
        if since:
            try:
                since_time = datetime.fromisoformat(since.replace('Z', '+00:00'))
            except:
                pass
        
        # 初始化检查时间
        if user_id not in self.last_check:
            self.last_check[user_id] = datetime.now() - timedelta(minutes=1)
        
        # 发送连接确认
        yield f"data: {json.dumps({'status': 'connected', 'types': list(subscribed_types)})}\n\n"
        
        # 回调函数用于接收外部广播的更新
        received_events = []
        
        async def update_callback(event: Dict):
            """更新回调"""
            received_events.append(event)
        
        # 订阅更新
        self.subscribe(user_id, update_callback)
        
        try:
            last_heartbeat = datetime.now()
            check_interval = 2  # 每2秒检查一次数据库变更
            
            while True:
                # 发送心跳（每30秒）
                now = datetime.now()
                if (now - last_heartbeat).total_seconds() >= 30:
                    yield ": heartbeat\n\n"
                    last_heartbeat = now
                
                # 检查外部广播的更新
                while received_events:
                    event = received_events.pop(0)
                    if event.get("type") in subscribed_types:
                        yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
                
                # 检查数据库变更
                changes = await self.check_changes(
                    db,
                    user_id,
                    subscribed_types,
                    self.last_check.get(user_id)
                )
                
                for event in changes:
                    yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
                
                # 更新检查时间
                if changes:
                    self.last_check[user_id] = datetime.now()
                
                # 等待一段时间再检查
                await asyncio.sleep(check_interval)
                
        except asyncio.CancelledError:
            # 客户端断开连接
            pass
        finally:
            # 取消订阅
            self.unsubscribe(user_id, update_callback)
            # 清理检查时间（可选）
            if user_id in self.last_check:
                del self.last_check[user_id]


# 全局服务实例
updates_service = UpdatesService()

