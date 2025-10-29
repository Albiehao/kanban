"""智能日程工具 - 空闲时间查询和智能任务添加"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta, time
from app.services.agent.base import BaseTool
from app.database import Task
from app.services.agent.tools.course_tool import GetCoursesTool


class FindFreeTimeTool(BaseTool):
    """查询空闲时间工具"""
    
    def get_name(self) -> str:
        return "find_free_time"
    
    def get_description(self) -> str:
        return "根据课程表和已有任务，查询指定日期的空闲时间段"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "查询日期，格式：YYYY-MM-DD（必填）"
                },
                "min_duration_minutes": {
                    "type": "integer",
                    "description": "最小空闲时长（分钟），默认30分钟",
                    "default": 30
                }
            },
            "required": ["date"]
        }
    
    async def execute(self, date: str, min_duration_minutes: int = 30) -> Dict[str, Any]:
        """执行查询空闲时间"""
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "日期格式错误，应为 YYYY-MM-DD"}
        
        # 获取当日的课程
        course_tool = GetCoursesTool(self.db, self.user)
        courses_result = await course_tool.execute(date=date)
        courses = courses_result.get("courses", [])
        
        # 获取当日的任务
        tasks = self.db.query(Task).filter(
            Task.user_id == self.user.id,
            Task.date == target_date
        ).all()
        
        # 解析占用时间段
        occupied_periods = []
        
        # 从课程中提取时间段
        for course in courses:
            periods_str = course.get("periods", "")
            if periods_str:
                # 解析节次，例如："1-2"表示第1-2节
                try:
                    # 根据节次计算时间（简化版，实际应根据学校作息时间表）
                    period_start, period_end = map(int, periods_str.split("-"))
                    start_time = time(8 + (period_start - 1) * 2, 0)  # 假设8:00开始，每节课2小时
                    end_time = time(8 + period_end * 2, 0)
                    occupied_periods.append((start_time, end_time))
                except:
                    pass
        
        # 从任务中提取时间段
        for task in tasks:
            if task.time:
                try:
                    # 解析时间范围，例如："09:00-11:00"
                    time_parts = task.time.split("-")
                    if len(time_parts) == 2:
                        start_str, end_str = time_parts
                        start_time = datetime.strptime(start_str.strip(), "%H:%M").time()
                        end_time = datetime.strptime(end_str.strip(), "%H:%M").time()
                        occupied_periods.append((start_time, end_time))
                except:
                    pass
        
        # 合并重叠的时间段
        occupied_periods.sort()
        merged_periods = []
        for start, end in occupied_periods:
            if merged_periods and start <= merged_periods[-1][1]:
                merged_periods[-1] = (merged_periods[-1][0], max(merged_periods[-1][1], end))
            else:
                merged_periods.append((start, end))
        
        # 计算空闲时间段（全天8:00-22:00）
        day_start = time(8, 0)
        day_end = time(22, 0)
        free_periods = []
        
        current_time = day_start
        for occupied_start, occupied_end in merged_periods:
            if current_time < occupied_start:
                duration = (datetime.combine(target_date, occupied_start) - 
                           datetime.combine(target_date, current_time)).total_seconds() / 60
                if duration >= min_duration_minutes:
                    free_periods.append({
                        "start": current_time.strftime("%H:%M"),
                        "end": occupied_start.strftime("%H:%M"),
                        "duration_minutes": int(duration)
                    })
            current_time = max(current_time, occupied_end)
        
        # 检查最后一段空闲时间
        if current_time < day_end:
            duration = (datetime.combine(target_date, day_end) - 
                       datetime.combine(target_date, current_time)).total_seconds() / 60
            if duration >= min_duration_minutes:
                free_periods.append({
                    "start": current_time.strftime("%H:%M"),
                    "end": day_end.strftime("%H:%M"),
                    "duration_minutes": int(duration)
                })
        
        return {
            "date": date,
            "free_periods": free_periods,
            "total_free_minutes": sum(p["duration_minutes"] for p in free_periods),
            "occupied_count": len(merged_periods)
        }


class CreateTaskInFreeTimeTool(BaseTool):
    """在空闲时间创建任务工具"""
    
    def get_name(self) -> str:
        return "create_task_in_free_time"
    
    def get_description(self) -> str:
        return "智能创建任务：先查询空闲时间，然后在合适的空闲时间段创建任务"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "任务标题（必填）"
                },
                "date": {
                    "type": "string",
                    "description": "任务日期，格式：YYYY-MM-DD（必填）"
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "任务所需时长（分钟），默认60分钟",
                    "default": 60
                },
                "description": {
                    "type": "string",
                    "description": "任务描述（可选）"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "优先级，默认medium",
                    "default": "medium"
                },
                "prefer_time": {
                    "type": "string",
                    "description": "偏好时间段，格式：HH:MM，例如：14:00，表示偏好下午2点开始（可选）"
                }
            },
            "required": ["title", "date"]
        }
    
    async def execute(self, title: str, date: str, duration_minutes: int = 60,
                     description: Optional[str] = None, priority: str = "medium",
                     prefer_time: Optional[str] = None) -> Dict[str, Any]:
        """执行在空闲时间创建任务"""
        # 先查询空闲时间
        find_tool = FindFreeTimeTool(self.db, self.user)
        free_time_result = await find_tool.execute(date=date, min_duration_minutes=duration_minutes)
        
        if "error" in free_time_result:
            return free_time_result
        
        free_periods = free_time_result.get("free_periods", [])
        
        if not free_periods:
            return {
                "error": f"{date} 没有足够长的空闲时间（需要至少{duration_minutes}分钟）",
                "suggestion": "请选择其他日期或缩短任务时长"
            }
        
        # 选择合适的时间段
        selected_period = None
        if prefer_time:
            # 如果有偏好时间，找最接近的
            prefer_datetime = datetime.strptime(prefer_time, "%H:%M").time()
            best_match = None
            min_diff = float('inf')
            
            for period in free_periods:
                period_start = datetime.strptime(period["start"], "%H:%M").time()
                if period["duration_minutes"] >= duration_minutes:
                    diff = abs((datetime.combine(datetime.today(), prefer_datetime) - 
                              datetime.combine(datetime.today(), period_start)).total_seconds() / 60)
                    if diff < min_diff:
                        min_diff = diff
                        best_match = period
            
            selected_period = best_match
        
        if not selected_period:
            # 选择第一个足够长的空闲时间段
            for period in free_periods:
                if period["duration_minutes"] >= duration_minutes:
                    selected_period = period
                    break
        
        if not selected_period:
            return {
                "error": f"没有找到至少{duration_minutes}分钟的空闲时间段"
            }
        
        # 计算结束时间
        start_datetime = datetime.strptime(f"{date} {selected_period['start']}", "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        end_time_str = end_datetime.strftime("%H:%M")
        
        # 创建任务
        from app.services.agent.tools.task_tool import CreateTaskTool
        create_tool = CreateTaskTool(self.db, self.user)
        result = await create_tool.execute(
            title=title,
            date=date,
            description=description,
            time=f"{selected_period['start']}-{end_time_str}",
            priority=priority
        )
        
        if "error" in result:
            return result
        
        result["scheduled_in_free_time"] = True
        result["free_time_period"] = selected_period
        
        return result

