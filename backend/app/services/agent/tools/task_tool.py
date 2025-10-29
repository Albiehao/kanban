"""任务管理工具"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from app.services.agent.base import BaseTool
from app.database import Task
from app.schemas import TaskCreate, TaskUpdate


class GetTasksTool(BaseTool):
    """获取任务列表工具"""
    
    def get_name(self) -> str:
        return "get_tasks"
    
    def get_description(self) -> str:
        return "获取用户的任务列表，支持按日期、完成状态、优先级等条件筛选"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "日期筛选，格式：YYYY-MM-DD，例如：2025-10-29"
                },
                "completed": {
                    "type": "boolean",
                    "description": "完成状态筛选，true表示已完成，false表示未完成"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "优先级筛选"
                },
                "has_reminder": {
                    "type": "boolean",
                    "description": "是否有提醒筛选"
                },
                "limit": {
                    "type": "integer",
                    "description": "返回数量限制，默认20，最大100",
                    "default": 20
                }
            },
            "required": []
        }
    
    async def execute(self, date: Optional[str] = None, completed: Optional[bool] = None,
                     priority: Optional[str] = None, has_reminder: Optional[bool] = None,
                     limit: int = 20) -> Dict[str, Any]:
        """执行获取任务列表"""
        query = self.db.query(Task).filter(Task.user_id == self.user.id)
        
        if date:
            try:
                filter_date = datetime.strptime(date, "%Y-%m-%d").date()
                query = query.filter(Task.date == filter_date)
            except ValueError:
                return {"error": "日期格式错误，应为 YYYY-MM-DD", "tasks": []}
        
        if completed is not None:
            query = query.filter(Task.completed == completed)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        if has_reminder is not None:
            query = query.filter(Task.has_reminder == has_reminder)
        
        tasks = query.order_by(Task.date.desc(), Task.created_at.desc()).limit(min(limit, 100)).all()
        
        return {
            "count": len(tasks),
            "tasks": [task.to_dict() for task in tasks]
        }


class CreateTaskTool(BaseTool):
    """创建任务工具"""
    
    def get_name(self) -> str:
        return "create_task"
    
    def get_description(self) -> str:
        return "创建新任务，可以设置标题、日期、时间、优先级、提醒等"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "任务标题（必填）"
                },
                "description": {
                    "type": "string",
                    "description": "任务描述（可选）"
                },
                "date": {
                    "type": "string",
                    "description": "任务日期，格式：YYYY-MM-DD（必填）"
                },
                "time": {
                    "type": "string",
                    "description": "任务时间，格式：HH:MM-HH:MM，例如：09:00-11:00（可选）"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "优先级，默认medium",
                    "default": "medium"
                },
                "has_reminder": {
                    "type": "boolean",
                    "description": "是否设置提醒，默认false",
                    "default": False
                },
                "reminder_time": {
                    "type": "string",
                    "description": "提醒时间，格式：YYYY-MM-DDTHH:MM:SS，例如：2025-10-29T08:30:00（可选）"
                }
            },
            "required": ["title", "date"]
        }
    
    async def execute(self, title: str, date: str, description: Optional[str] = None,
                     time: Optional[str] = None, priority: str = "medium",
                     has_reminder: bool = False, reminder_time: Optional[str] = None) -> Dict[str, Any]:
        """执行创建任务"""
        try:
            task_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "日期格式错误，应为 YYYY-MM-DD"}
        
        reminder_datetime = None
        if reminder_time:
            try:
                reminder_datetime = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
            except ValueError:
                return {"error": "提醒时间格式错误"}
        
        db_task = Task(
            user_id=self.user.id,
            title=title,
            description=description,
            priority=priority,
            date=task_date,
            time=time,
            has_reminder=has_reminder,
            reminder_time=reminder_datetime
        )
        
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        
        return {
            "success": True,
            "message": "任务创建成功",
            "task": db_task.to_dict()
        }


class UpdateTaskTool(BaseTool):
    """更新任务工具"""
    
    def get_name(self) -> str:
        return "update_task"
    
    def get_description(self) -> str:
        return "更新任务信息，可以更新标题、完成状态、优先级、日期、时间、提醒等"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "任务ID（必填）"
                },
                "title": {
                    "type": "string",
                    "description": "任务标题"
                },
                "description": {
                    "type": "string",
                    "description": "任务描述"
                },
                "completed": {
                    "type": "boolean",
                    "description": "完成状态"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "优先级"
                },
                "date": {
                    "type": "string",
                    "description": "任务日期，格式：YYYY-MM-DD"
                },
                "time": {
                    "type": "string",
                    "description": "任务时间，格式：HH:MM-HH:MM"
                },
                "has_reminder": {
                    "type": "boolean",
                    "description": "是否设置提醒"
                },
                "reminder_time": {
                    "type": "string",
                    "description": "提醒时间，格式：YYYY-MM-DDTHH:MM:SS"
                }
            },
            "required": ["task_id"]
        }
    
    async def execute(self, task_id: int, title: Optional[str] = None,
                     description: Optional[str] = None, completed: Optional[bool] = None,
                     priority: Optional[str] = None, date: Optional[str] = None,
                     time: Optional[str] = None, has_reminder: Optional[bool] = None,
                     reminder_time: Optional[str] = None) -> Dict[str, Any]:
        """执行更新任务"""
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == self.user.id
        ).first()
        
        if not task:
            return {"error": "任务不存在或不属于当前用户"}
        
        if title:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        if priority:
            task.priority = priority
        if date:
            try:
                task.date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return {"error": "日期格式错误"}
        if time is not None:
            task.time = time
        if has_reminder is not None:
            task.has_reminder = has_reminder
        if reminder_time is not None:
            if reminder_time:
                try:
                    task.reminder_time = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
                except ValueError:
                    return {"error": "提醒时间格式错误"}
            else:
                task.reminder_time = None
        
        self.db.commit()
        self.db.refresh(task)
        
        return {
            "success": True,
            "message": "任务更新成功",
            "task": task.to_dict()
        }


class DeleteTaskTool(BaseTool):
    """删除任务工具"""
    
    def get_name(self) -> str:
        return "delete_task"
    
    def get_description(self) -> str:
        return "删除指定的任务"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "要删除的任务ID（必填）"
                }
            },
            "required": ["task_id"]
        }
    
    async def execute(self, task_id: int) -> Dict[str, Any]:
        """执行删除任务"""
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == self.user.id
        ).first()
        
        if not task:
            return {"error": "任务不存在或不属于当前用户"}
        
        task_info = {
            "id": task.id,
            "title": task.title
        }
        
        self.db.delete(task)
        self.db.commit()
        
        return {
            "success": True,
            "message": "任务删除成功",
            "task": task_info
        }


class CompleteTaskTool(BaseTool):
    """完成任务工具"""
    
    def get_name(self) -> str:
        return "complete_task"
    
    def get_description(self) -> str:
        return "标记任务为已完成或未完成"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "任务ID（必填）"
                },
                "completed": {
                    "type": "boolean",
                    "description": "完成状态，true表示完成，false表示未完成，默认true",
                    "default": True
                }
            },
            "required": ["task_id"]
        }
    
    async def execute(self, task_id: int, completed: bool = True) -> Dict[str, Any]:
        """执行完成任务"""
        return await UpdateTaskTool(self.db, self.user).execute(
            task_id=task_id,
            completed=completed
        )

