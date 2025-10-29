"""课程服务"""

from typing import List, Dict
from app.schemas import CourseCreate, CourseUpdate
from app.storage import Storage


class CourseService:
    """课程服务类"""
    
    def __init__(self, storage: Storage):
        """初始化服务
        
        Args:
            storage: 存储实例
        """
        self.storage = storage
    
    def get_courses(self) -> List[Dict]:
        """获取所有课程"""
        return self.storage.get_courses()
    
    def create_course(self, course: CourseCreate) -> Dict:
        """创建课程"""
        return self.storage.create_course(course)
    
    def update_course(self, course_id: int, course: CourseUpdate) -> Dict:
        """更新课程"""
        return self.storage.update_course(course_id, course)
    
    def delete_course(self, course_id: int) -> bool:
        """删除课程"""
        return self.storage.delete_course(course_id)

