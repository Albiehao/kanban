"""课程表工具"""

from typing import Dict, Any, Optional
from app.services.agent.base import BaseTool
from app.services.edu_binding_service import EduBindingService
import requests


class GetCoursesTool(BaseTool):
    """获取课程表工具"""
    
    def get_name(self) -> str:
        return "get_courses"
    
    def get_description(self) -> str:
        return "获取用户的课程表，支持按日期筛选。当用户询问课程、课表、课程安排、明天上什么课、今天的课程时必须调用此工具获取真实数据。不要提供示例数据。"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "日期筛选，格式：YYYY-MM-DD（可选）"
                }
            },
            "required": []
        }
    
    async def execute(self, date: Optional[str] = None) -> Dict[str, Any]:
        """执行获取课程表"""
        print(f"[GetCoursesTool] 开始获取课程表, 用户ID: {self.user.id}, 日期: {date}")
        
        edu_service = EduBindingService(self.db)
        binding = edu_service.get_binding_for_crawler(self.user.id)
        
        if not binding:
            print(f"[GetCoursesTool] 用户 {self.user.id} 未绑定API密钥")
            return {
                "error": "未绑定API密钥，无法获取课程表。请先在设置中绑定教务系统API密钥。",
                "courses": [],
                "success": False
            }
        
        api_key = binding.get("api_key")
        api_url = binding.get("api_url", "http://160.202.229.142:8000/api/v1/api/courses")
        
        print(f"[GetCoursesTool] 调用第三方API: {api_url}, Key: {api_key[:4] if api_key else 'None'}***")
        
        try:
            headers = {"X-API-Key": api_key}
            params = {}
            if date:
                params["date"] = date
            
            print(f"[GetCoursesTool] 请求参数: {params}")
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            
            print(f"[GetCoursesTool] API响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"[GetCoursesTool] API响应数据: {str(result)[:500]}...")
                
                courses = result.get("data", [])
                
                # 如果有日期筛选，在后端再次过滤
                if date and courses:
                    filtered_courses = [c for c in courses if c.get("date") == date]
                    courses = filtered_courses
                    print(f"[GetCoursesTool] 日期筛选后课程数: {len(courses)}")
                
                return {
                    "success": True,
                    "count": len(courses),
                    "courses": courses,
                    "message": f"成功获取 {len(courses)} 门课程"
                }
            else:
                error_msg = f"第三方API错误: HTTP {response.status_code}"
                if response.text:
                    error_msg += f", 响应: {response.text[:200]}"
                print(f"[GetCoursesTool] {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "courses": []
                }
        except requests.exceptions.Timeout:
            error_msg = "请求超时，第三方API无响应"
            print(f"[GetCoursesTool] {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "courses": []
            }
        except requests.exceptions.ConnectionError as e:
            error_msg = f"无法连接到第三方API: {str(e)}"
            print(f"[GetCoursesTool] {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "courses": []
            }
        except Exception as e:
            error_msg = f"获取课程失败: {str(e)}"
            print(f"[GetCoursesTool] 异常: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "courses": []
            }

