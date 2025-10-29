"""任务服务"""

from typing import List, Dict, Optional
from app.schemas import TaskCreate, TaskUpdate
from app.storage import Storage


class TaskService:
    """任务服务类"""
    
    def __init__(self, storage: Storage):
        """初始化服务
        
        Args:
            storage: 存储实例
        """
        self.storage = storage
    
    def get_tasks(self) -> List[Dict]:
        """获取所有任务"""
        return self.storage.get_tasks()
    
    def create_task(self, task: TaskCreate) -> Dict:
        """创建任务"""
        return self.storage.create_task(task)
    
    def update_task(self, task_id: int, task: TaskUpdate) -> Optional[Dict]:
        """更新任务"""
        return self.storage.update_task(task_id, task)
    
    def delete_task(self, task_id: int) -> bool:
        """删除任务"""
        return self.storage.delete_task(task_id)
    
    def toggle_task(self, task_id: int) -> Optional[Dict]:
        """切换任务完成状态"""
        return self.storage.toggle_task(task_id)

