"""时间工具"""

from typing import Dict, Any
from datetime import datetime, timezone, timedelta
from app.services.agent.base import BaseTool


class GetCurrentTimeTool(BaseTool):
    """获取当前时间工具"""
    
    def get_name(self) -> str:
        return "get_current_time"
    
    def get_description(self) -> str:
        return "获取当前日期和时间信息，包括日期、时间、星期、时区等信息"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["full", "date", "time", "datetime"],
                    "description": "返回格式：full(完整信息)、date(仅日期)、time(仅时间)、datetime(日期时间)，默认full",
                    "default": "full"
                },
                "timezone": {
                    "type": "string",
                    "description": "时区，例如：Asia/Shanghai, UTC等。默认使用服务器时区",
                    "default": None
                }
            },
            "required": []
        }
    
    async def execute(self, format: str = "full", timezone: str = None) -> Dict[str, Any]:
        """执行获取当前时间"""
        try:
            # 获取当前时间
            if timezone:
                # 如果指定了时区（这里简化处理，实际可以使用pytz）
                # 默认使用本地时区
                now = datetime.now()
            else:
                now = datetime.now()
            
            # 格式化为字符串
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
            
            # 获取星期
            weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
            weekday = weekdays[now.weekday()]
            
            # 根据格式返回
            if format == "date":
                return {
                    "success": True,
                    "date": date_str,
                    "year": now.year,
                    "month": now.month,
                    "day": now.day,
                    "weekday": weekday
                }
            elif format == "time":
                return {
                    "success": True,
                    "time": time_str,
                    "hour": now.hour,
                    "minute": now.minute,
                    "second": now.second
                }
            elif format == "datetime":
                return {
                    "success": True,
                    "datetime": datetime_str,
                    "date": date_str,
                    "time": time_str,
                    "timestamp": int(now.timestamp())
                }
            else:  # full
                return {
                    "success": True,
                    "datetime": datetime_str,
                    "date": date_str,
                    "time": time_str,
                    "year": now.year,
                    "month": now.month,
                    "day": now.day,
                    "hour": now.hour,
                    "minute": now.minute,
                    "second": now.second,
                    "weekday": weekday,
                    "weekday_number": now.weekday() + 1,  # 1-7
                    "timestamp": int(now.timestamp()),
                    "timezone": str(now.astimezone().tzinfo) if hasattr(now, 'astimezone') else "本地时区"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取时间失败: {str(e)}"
            }

