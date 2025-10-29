"""课程数据库服务"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.database import Course


class CourseDbService:
    """课程数据库服务类"""
    
    def __init__(self, db: Session):
        """初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_courses_by_user(self, user_id: int) -> List[Dict]:
        """获取用户的所有课程
        
        Args:
            user_id: 用户ID
            
        Returns:
            课程列表
        """
        courses = self.db.query(Course).filter(
            Course.user_id == user_id
        ).all()
        return [course.to_dict() for course in courses]
    
    def get_all_courses(self) -> List[Dict]:
        """获取所有课程
        
        Returns:
            课程列表
        """
        courses = self.db.query(Course).all()
        return [course.to_dict() for course in courses]
    
    def create_course(self, course_data: Dict, user_id: int) -> Dict:
        """创建课程
        
        Args:
            course_data: 课程数据
            user_id: 用户ID
            
        Returns:
            创建的课程
        """
        # 字段映射
        course = Course(
            user_id=user_id,
            course_name=course_data.get("course_name") or course_data.get("name") or "",
            classroom=course_data.get("classroom") or course_data.get("room") or "",
            date=course_data.get("date") or course_data.get("day") or "",
            teacher=course_data.get("teacher") or course_data.get("instructor") or "",
            periods=course_data.get("periods") or course_data.get("time") or ""
        )
        
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        
        return course.to_dict()
    
    def batch_create_courses(self, courses_data: List[Dict], user_id: int) -> List[Dict]:
        """批量创建课程
        
        Args:
            courses_data: 课程数据列表
            user_id: 用户ID
            
        Returns:
            创建的课程列表
        """
        created_courses = []
        
        for course_data in courses_data:
            # 字段映射
            course = Course(
                user_id=user_id,
                course_name=course_data.get("course_name") or course_data.get("name") or "",
                classroom=course_data.get("classroom") or course_data.get("room") or "",
                date=course_data.get("date") or course_data.get("day") or "",
                teacher=course_data.get("teacher") or course_data.get("instructor") or "",
                periods=course_data.get("periods") or course_data.get("time") or ""
            )
            self.db.add(course)
            created_courses.append(course)
        
        self.db.commit()
        
        return [course.to_dict() for course in created_courses]
    
    def delete_user_courses(self, user_id: int) -> int:
        """删除用户的所有课程
        
        Args:
            user_id: 用户ID
            
        Returns:
            删除的课程数量
        """
        deleted_count = self.db.query(Course).filter(
            Course.user_id == user_id
        ).delete()
        self.db.commit()
        return deleted_count
    
    def get_course_by_id(self, course_id: int) -> Optional[Dict]:
        """根据ID获取课程
        
        Args:
            course_id: 课程ID
            
        Returns:
            课程信息或None
        """
        course = self.db.query(Course).filter(Course.id == course_id).first()
        return course.to_dict() if course else None
    
    def delete_course_by_id(self, course_id: int) -> bool:
        """删除课程
        
        Args:
            course_id: 课程ID
            
        Returns:
            是否删除成功
        """
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if course:
            self.db.delete(course)
            self.db.commit()
            return True
        return False

