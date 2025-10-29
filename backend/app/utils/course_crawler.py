"""课程表爬虫工具"""

from typing import List, Dict
from app.utils.crawler import Crawler
import re
import json
from datetime import datetime


class CourseCrawler(Crawler):
    """课程表爬虫工具
    
    用于从各种数据源爬取课程表数据
    """
    
    def __init__(self, timeout: int = 30):
        """初始化课程表爬虫
        
        Args:
            timeout: 请求超时时间（秒）
        """
        super().__init__(timeout)
    
    def parse_data(self, content: str) -> List[Dict]:
        """解析课程表数据
        
        Args:
            content: 原始内容（HTML、JSON或文本）
            
        Returns:
            课程列表
        """
        # 尝试解析为JSON
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return self._parse_from_dict(data)
        except (json.JSONDecodeError, ValueError):
            pass
        
        # 尝试解析为HTML
        if '<html' in content.lower() or '<table' in content.lower():
            return self._parse_html(content)
        
        # 尝试解析为文本
        return self._parse_text(content)
    
    def _parse_from_dict(self, data: Dict) -> List[Dict]:
        """从字典解析课程数据
        
        Args:
            data: 字典数据
            
        Returns:
            课程列表
        """
        courses = []
        
        # 尝试不同的键名
        for key in ['courses', 'data', 'items', 'list']:
            if key in data and isinstance(data[key], list):
                courses = data[key]
                break
        
        # 如果数据本身就是列表
        if not courses and isinstance(data, list):
            courses = data
        
        # 规范化课程数据
        normalized_courses = []
        for course in courses:
            normalized_courses.append(self._normalize_course(course))
        
        return normalized_courses
    
    def _parse_html(self, content: str) -> List[Dict]:
        """解析HTML内容
        
        Args:
            content: HTML内容
            
        Returns:
            课程列表
        """
        courses = []
        
        try:
            # 使用正则表达式提取表格数据
            # 匹配 <tr>...</tr> 模式
            pattern = r'<tr[^>]*>.*?</tr>'
            rows = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            
            for row in rows:
                # 提取 <td>...</td> 内容
                cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL | re.IGNORECASE)
                cells = [self._clean_html(cell) for cell in cells]
                
                if len(cells) >= 3:
                    course = {
                        "course_name": cells[0] if len(cells) > 0 else "",
                        "teacher": cells[1] if len(cells) > 1 else "",
                        "classroom": cells[2] if len(cells) > 2 else "",
                        "time": cells[3] if len(cells) > 3 else "",
                        "day": cells[4] if len(cells) > 4 else ""
                    }
                    courses.append(course)
                    
        except Exception as e:
            print(f"解析HTML失败: {e}")
        
        return courses
    
    def _parse_text(self, content: str) -> List[Dict]:
        """解析文本内容
        
        Args:
            content: 文本内容
            
        Returns:
            课程列表
        """
        courses = []
        
        try:
            lines = content.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 尝试匹配常见格式
                # 格式1: 周一|数学|10:00-11:00|A101|张老师
                if '|' in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 3:
                        course = {
                            "day": parts[0],
                            "course_name": parts[1],
                            "time": parts[2] if len(parts) > 2 else "",
                            "classroom": parts[3] if len(parts) > 3 else "",
                            "teacher": parts[4] if len(parts) > 4 else ""
                        }
                        courses.append(course)
                
                # 格式2: 周一: 数学 10:00-11:00 A101 张老师
                elif ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        day = parts[0].strip()
                        rest = parts[1].strip()
                        
                        # 简单的空格分割
                        tokens = rest.split()
                        if len(tokens) >= 1:
                            course = {
                                "day": day,
                                "course_name": tokens[0],
                                "time": tokens[1] if len(tokens) > 1 else "",
                                "classroom": tokens[2] if len(tokens) > 2 else "",
                                "teacher": tokens[3] if len(tokens) > 3 else ""
                            }
                            courses.append(course)
                            
        except Exception as e:
            print(f"解析文本失败: {e}")
        
        return courses
    
    def _normalize_course(self, course: Dict) -> Dict:
        """规范化课程数据
        
        Args:
            course: 原始课程数据
            
        Returns:
            规范化后的课程数据
        """
        normalized = {
            "course_name": course.get("course_name") or course.get("name") or course.get("title") or "",
            "teacher": course.get("teacher") or course.get("instructor") or "",
            "classroom": course.get("classroom") or course.get("room") or "",
            "time": course.get("time") or course.get("periods") or course.get("schedule") or "",
            "day": course.get("day") or course.get("weekday") or ""
        }
        return normalized
    
    def _clean_html(self, html: str) -> str:
        """清理HTML标签
        
        Args:
            html: HTML字符串
            
        Returns:
            纯文本
        """
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', html)
        # 清理空白字符
        text = ' '.join(text.split())
        return text.strip()
    
    def parse_json_courses(self, json_data) -> List[Dict]:
        """解析JSON格式的课程数据
        
        Args:
            json_data: JSON字符串或字典
            
        Returns:
            课程列表
        """
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        
        return self._parse_from_dict(json_data)
    
    def import_courses(self, courses: List[Dict], user_id: int) -> List[Dict]:
        """导入课程数据
        
        Args:
            courses: 课程列表
            user_id: 用户ID
            
        Returns:
            导入后的课程列表（添加用户ID和时间戳）
        """
        imported_courses = []
        current_time = datetime.now()
        
        for course in courses:
            imported_course = {
                **course,
                "user_id": user_id,
                "created_at": current_time.isoformat(),
                "updated_at": current_time.isoformat()
            }
            imported_courses.append(imported_course)
        
        return imported_courses

