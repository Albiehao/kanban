from typing import List, Dict, Optional, Any
from datetime import datetime
from app.schemas import (
    Task, TaskCreate, TaskUpdate,
    Transaction, TransactionCreate, TransactionUpdate,
    Course, CourseCreate, CourseUpdate,
    UserProfile, UserProfileUpdate, UserPreferences, UserPreferencesUpdate,
    AdminStats, AdminUser, AdminSettings, SystemStatus, SystemLog,
    ChatMessage, Conversation, ConversationCreate
)


class Storage:
    def __init__(self):
        # 初始化模拟数据
        self._init_data()
    
    def _init_data(self):
        """初始化模拟数据"""
        # 任务数据
        self.tasks = [
            {"id": 1, "title": "完成数学作业", "completed": False, "priority": "high", "date": "2025-10-28", "time": "19:00-21:00", "hasReminder": True},
            {"id": 2, "title": "准备英语演讲", "completed": True, "priority": "high", "date": "2025-10-28", "time": "14:00-16:00", "hasReminder": True},
            {"id": 3, "title": "复习计算机网络", "completed": True, "priority": "medium", "date": "2025-10-28", "time": "10:00-12:00", "hasReminder": False},
            {"id": 4, "title": "准备小组项目讨论", "completed": False, "priority": "medium", "date": "2025-10-29", "time": "15:00-17:00", "hasReminder": True},
            {"id": 5, "title": "完成实验报告", "completed": False, "priority": "high", "date": "2025-10-30", "time": "09:00-11:00", "hasReminder": False},
            {"id": 6, "title": "整理课程笔记", "completed": False, "priority": "low", "date": "2025-10-31", "time": "20:00-22:00", "hasReminder": False},
            {"id": 7, "title": "复习期末考试", "completed": False, "priority": "high", "date": "2025-11-01", "time": "18:00-20:00", "hasReminder": True}
        ]
        
        # 交易记录数据（已在用户提供的JSON中）
        self.transactions = [
            {"id": 1, "type": "expense", "amount": 45.5, "category": "餐饮", "description": "午餐", "date": "2025-01-20"},
            {"id": 9, "type": "expense", "amount": 25.0, "category": "餐饮", "description": "早餐", "date": "2025-01-21"},
            {"id": 10, "type": "income", "amount": 200, "category": "兼职", "description": "今日兼职收入", "date": "2025-01-21"},
            {"id": 11, "type": "expense", "amount": 35.0, "category": "餐饮", "description": "早餐", "date": "2025-10-28"},
            {"id": 12, "type": "expense", "amount": 68.0, "category": "餐饮", "description": "午餐", "date": "2025-10-28"},
            {"id": 13, "type": "income", "amount": 300, "category": "兼职", "description": "今日兼职收入", "date": "2025-10-28"},
            {"id": 14, "type": "expense", "amount": 25.0, "category": "交通", "description": "地铁费", "date": "2025-10-28"},
            {"id": 2, "type": "income", "amount": 500, "category": "兼职", "description": "周末兼职工资", "date": "2025-01-19"},
            {"id": 3, "type": "expense", "amount": 320, "category": "学习", "description": "购买教材", "date": "2025-01-18"},
            {"id": 4, "type": "expense", "amount": 180, "category": "交通", "description": "地铁卡充值", "date": "2025-01-17"},
            {"id": 5, "type": "expense", "amount": 200, "category": "娱乐", "description": "电影票", "date": "2025-01-16"},
            {"id": 6, "type": "income", "amount": 800, "category": "奖学金", "description": "学期奖学金", "date": "2025-01-15"},
            {"id": 7, "type": "expense", "amount": 120, "category": "餐饮", "description": "聚餐", "date": "2025-01-14"},
            {"id": 8, "type": "expense", "amount": 150, "category": "学习", "description": "在线课程", "date": "2025-01-13"}
        ]
        
        # 课程数据
        self.courses = [
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-09-01", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-01", "teacher": "刘丹", "periods": "8-10节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼B409", "date": "2025-09-02", "teacher": "聂小燕", "periods": "3-5节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-02", "teacher": "刘丹", "periods": "6-7节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-09-03", "teacher": "聂小燕", "periods": "1-2节"},
            {"course_name": "马克思主义基本原理", "classroom": "德润讲堂", "date": "2025-09-03", "teacher": "陈惠珍", "periods": "3-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-09-03", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-09-04", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-04", "teacher": "刘丹", "periods": "3-5节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-09-04", "teacher": "聂小燕", "periods": "6-7节"},
            {"course_name": "四史教育", "classroom": "德润讲堂", "date": "2025-09-05", "teacher": "王镖", "periods": "1-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-09-05", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-06", "teacher": "刘丹", "periods": "1-2节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-09-08", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-09-08", "teacher": "聂小燕", "periods": "3-5节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-08", "teacher": "刘丹", "periods": "8-10节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-09", "teacher": "刘丹", "periods": "6-7节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-09-10", "teacher": "聂小燕", "periods": "1-2节"},
            {"course_name": "马克思主义基本原理", "classroom": "德润讲堂", "date": "2025-09-10", "teacher": "陈惠珍", "periods": "3-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-09-10", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-10", "teacher": "刘丹", "periods": "8-9节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-09-11", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-09-11", "teacher": "聂小燕", "periods": "6-7节"},
            {"course_name": "四史教育", "classroom": "德润讲堂", "date": "2025-09-12", "teacher": "王镖", "periods": "1-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-09-12", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-09-15", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-09-15", "teacher": "聂小燕", "periods": "3-5节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-15", "teacher": "刘丹", "periods": "8-10节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-16", "teacher": "刘丹", "periods": "6-7节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-09-17", "teacher": "聂小燕", "periods": "1-2节"},
            {"course_name": "马克思主义基本原理", "classroom": "好学楼B100", "date": "2025-09-17", "teacher": "陈惠珍", "periods": "3-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-09-17", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-09-18", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-09-18", "teacher": "聂小燕", "periods": "6-7节"},
            {"course_name": "马克思主义基本原理", "classroom": "好学楼B100", "date": "2025-09-19", "teacher": "陈惠珍", "periods": "3-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-09-19", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-09-22", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼B400", "date": "2025-09-22", "teacher": "聂小燕", "periods": "3-4节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-22", "teacher": "刘丹", "periods": "8-10节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼B409", "date": "2025-09-23", "teacher": "聂小燕", "periods": "3-5节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-23", "teacher": "刘丹", "periods": "6-7节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-09-24", "teacher": "聂小燕", "periods": "1-2节"},
            {"course_name": "马克思主义基本原理", "classroom": "好学楼B100", "date": "2025-09-24", "teacher": "陈惠珍", "periods": "3-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-09-24", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-24", "teacher": "刘丹", "periods": "8-9节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-09-25", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-09-25", "teacher": "聂小燕", "periods": "6-7节"},
            {"course_name": "马克思主义基本原理", "classroom": "好学楼B100", "date": "2025-09-26", "teacher": "陈惠珍", "periods": "3-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-09-26", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-09-29", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-09-29", "teacher": "孙宁", "periods": "3-4节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-29", "teacher": "刘丹", "periods": "8-10节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼B409", "date": "2025-09-30", "teacher": "聂小燕", "periods": "3-5节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-09-30", "teacher": "刘丹", "periods": "6-7节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-10-09", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-10-10", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-10-10", "teacher": "刘丹", "periods": "8-10节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-10-13", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-10-13", "teacher": "刘丹", "periods": "6-7节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼B409", "date": "2025-10-14", "teacher": "聂小燕", "periods": "3-5节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-10-15", "teacher": "聂小燕", "periods": "1-2节"},
            {"course_name": "马克思主义基本原理", "classroom": "好学楼B100", "date": "2025-10-15", "teacher": "陈惠珍", "periods": "3-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-10-15", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-10-15", "teacher": "刘丹", "periods": "8-10节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-10-16", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "Linux原理与应用", "classroom": "力行楼B400", "date": "2025-10-16", "teacher": "韩旭东", "periods": "6-7节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-10-17", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-10-20", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼B409", "date": "2025-10-21", "teacher": "聂小燕", "periods": "3-5节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-10-22", "teacher": "聂小燕", "periods": "1-2节"},
            {"course_name": "马克思主义基本原理", "classroom": "好学楼B100", "date": "2025-10-22", "teacher": "陈惠珍", "periods": "3-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-10-22", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-10-22", "teacher": "刘丹", "periods": "8-10节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-10-23", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "Linux原理与应用", "classroom": "力行楼B400", "date": "2025-10-23", "teacher": "韩旭东", "periods": "6-7节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-10-24", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-10-27", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼B409", "date": "2025-10-28", "teacher": "聂小燕", "periods": "3-5节"},
            {"course_name": "移动应用开发技术", "classroom": "力行楼A400", "date": "2025-10-29", "teacher": "聂小燕", "periods": "1-2节"},
            {"course_name": "马克思主义基本原理", "classroom": "好学楼B100", "date": "2025-10-29", "teacher": "陈惠珍", "periods": "3-4节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-10-29", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-10-30", "teacher": "孙锦程", "periods": "1-2节"},
            {"course_name": "Linux原理与应用", "classroom": "力行楼B400", "date": "2025-10-30", "teacher": "韩旭东", "periods": "6-7节"},
            {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-10-31", "teacher": "孙宁", "periods": "6-7节"},
            {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-10-31", "teacher": "刘丹", "periods": "8-10节"}
        ]  # 仅显示部分课程数据
        
        # 用户配置
        self.user_profile = {
            "username": "admin",
            "email": "user@example.com",
            "bio": "我是人",
            "avatar": "U",
            "completedTasks": 156,
            "inProgressTasks": 8,
            "daysJoined": 365
        }
        
        self.user_preferences = {
            "darkMode": False,
            "emailNotifications": True,
            "desktopNotifications": True
        }
        
        # 管理员数据
        self.admin_stats = {
            "totalUsers": 1247,
            "activeCourses": 89,
            "pendingTasks": 23,
            "systemWarnings": 3
        }
        
        self.admin_users = [
            {"id": 1, "username": "admin", "email": "admin@example.com", "status": "active"},
            {"id": 2, "username": "user1", "email": "user1@example.com", "status": "active"},
            {"id": 3, "username": "user2", "email": "user2@example.com", "status": "inactive"},
            {"id": 4, "username": "teacher1", "email": "teacher1@example.com", "status": "active"},
            {"id": 5, "username": "student1", "email": "student1@example.com", "status": "active"}
        ]
        
        self.system_settings = {
            "maintenanceMode": False,
            "autoBackup": True,
            "emailNotifications": True
        }
        
        self.system_status = {
            "cpu": 45,
            "memory": 67,
            "disk": 23
        }
        
        self.system_logs = [
            {"id": 1, "level": "error", "message": "系统启动失败", "timestamp": "2025-01-27 10:30:15"},
            {"id": 2, "level": "warning", "message": "CPU使用率超过80%", "timestamp": "2025-01-27 10:25:42"},
            {"id": 3, "level": "error", "message": "数据库连接超时", "timestamp": "2025-01-27 10:20:18"},
            {"id": 4, "level": "info", "message": "用户登录成功", "timestamp": "2025-01-27 10:15:33"},
            {"id": 5, "level": "info", "message": "数据备份完成", "timestamp": "2025-01-27 10:10:55"}
        ]
        
        # AI对话数据
        self.conversations = {}
        self.chat_messages = {}
        self.message_id_counter = 1
        self.conversation_id_counter = 1
    
    # ============ 任务方法 ============
    def get_tasks(self) -> List[Dict]:
        return self.tasks
    
    def create_task(self, task: TaskCreate) -> Dict:
        new_id = max([t["id"] for t in self.tasks], default=0) + 1
        task_dict = task.dict()
        task_dict["id"] = new_id
        self.tasks.append(task_dict)
        return task_dict
    
    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Dict]:
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                update_data = task_update.dict(exclude_unset=True)
                self.tasks[i].update(update_data)
                return self.tasks[i]
        return None
    
    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                return True
        return False
    
    def toggle_task(self, task_id: int) -> Optional[Dict]:
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                return task
        return None
    
    # ============ 财务方法 ============
    def get_transactions(self) -> List[Dict]:
        return self.transactions
    
    def create_transaction(self, transaction: TransactionCreate) -> Dict:
        new_id = max([t["id"] for t in self.transactions], default=0) + 1
        transaction_dict = transaction.dict()
        transaction_dict["id"] = new_id
        self.transactions.append(transaction_dict)
        return transaction_dict
    
    def update_transaction(self, transaction_id: int, transaction_update: TransactionUpdate) -> Optional[Dict]:
        for i, transaction in enumerate(self.transactions):
            if transaction["id"] == transaction_id:
                update_data = transaction_update.dict(exclude_unset=True)
                self.transactions[i].update(update_data)
                return self.transactions[i]
        return None
    
    def delete_transaction(self, transaction_id: int) -> bool:
        for i, transaction in enumerate(self.transactions):
            if transaction["id"] == transaction_id:
                self.transactions.pop(i)
                return True
        return False
    
    def get_finance_stats(self) -> Dict:
        # 计算当月统计
        monthly_income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
        monthly_expense = sum(t["amount"] for t in self.transactions if t["type"] == "expense")
        balance = monthly_income - monthly_expense
        
        # 按类别统计支出
        expense_by_category = {}
        colors = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"]
        color_idx = 0
        
        for transaction in self.transactions:
            if transaction["type"] == "expense":
                category = transaction["category"]
                if category not in expense_by_category:
                    expense_by_category[category] = {"category": category, "amount": 0, "color": colors[color_idx % len(colors)]}
                    color_idx += 1
                expense_by_category[category]["amount"] += transaction["amount"]
        
        return {
            "monthlyIncome": monthly_income,
            "monthlyExpense": monthly_expense,
            "balance": balance,
            "expenseByCategory": list(expense_by_category.values())
        }
    
    # ============ 课程方法 ============
    def get_courses(self) -> List[Dict]:
        return self.courses
    
    def create_course(self, course: CourseCreate) -> Dict:
        course_dict = course.dict()
        self.courses.append(course_dict)
        # 返回时添加临时ID
        course_dict["id"] = len(self.courses)
        return course_dict
    
    def update_course(self, course_id: int, course_update: CourseUpdate) -> Optional[Dict]:
        if 0 < course_id <= len(self.courses):
            i = course_id - 1
            update_data = course_update.dict(exclude_unset=True)
            self.courses[i].update(update_data)
            return self.courses[i]
        return None
    
    def delete_course(self, course_id: int) -> bool:
        if 0 < course_id <= len(self.courses):
            self.courses.pop(course_id - 1)
            return True
        return False
    
    # ============ AI助手方法 ============
    def create_chat_response(self, message: str, conversation_id: int) -> Dict:
        """模拟AI回复"""
        # 简单的模拟回复
        responses = [
            "你好！有什么我可以帮助你的吗？",
            "我理解你的问题。",
            "这是一个很好的问题。",
            "让我来帮你解答。",
            "很高兴为你服务。"
        ]
        import random
        response_text = random.choice(responses)
        
        msg = {
            "id": self.message_id_counter,
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        }
        self.message_id_counter += 1
        
        if conversation_id not in self.chat_messages:
            self.chat_messages[conversation_id] = []
        self.chat_messages[conversation_id].append(msg)
        
        return msg
    
    def get_conversations(self) -> List[Dict]:
        if not self.conversations:
            # 创建默认对话
            default_conv = {
                "id": 1,
                "messages": [],
                "title": "新对话",
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat()
            }
            self.conversations[1] = default_conv
            return [default_conv]
        return list(self.conversations.values())
    
    def get_conversation_messages(self, conversation_id: int) -> Optional[List[Dict]]:
        return self.chat_messages.get(conversation_id, [])
    
    def create_conversation(self, conversation: ConversationCreate) -> Dict:
        new_id = self.conversation_id_counter
        self.conversation_id_counter += 1
        
        conv = {
            "id": new_id,
            "messages": [],
            "title": conversation.title,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        self.conversations[new_id] = conv
        return conv
    
    def delete_conversation(self, conversation_id: int) -> bool:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            if conversation_id in self.chat_messages:
                del self.chat_messages[conversation_id]
            return True
        return False
    
    def clear_conversation(self, conversation_id: int) -> bool:
        if conversation_id in self.chat_messages:
            self.chat_messages[conversation_id] = []
            return True
        return False
    
    # ============ 用户设置方法 ============
    def get_user_profile(self) -> Dict:
        return self.user_profile
    
    def get_user_preferences(self) -> Dict:
        return self.user_preferences
    
    def update_user_profile(self, profile: UserProfileUpdate) -> Dict:
        update_data = profile.dict(exclude_unset=True)
        self.user_profile.update(update_data)
        return self.user_profile
    
    def update_user_preferences(self, preferences: UserPreferencesUpdate) -> Dict:
        update_data = preferences.dict(exclude_unset=True)
        self.user_preferences.update(update_data)
        return self.user_preferences
    
    # ============ 管理员方法 ============
    def get_admin_stats(self) -> Dict:
        return self.admin_stats
    
    def get_admin_users(self) -> List[Dict]:
        return self.admin_users
    
    def get_system_settings(self) -> Dict:
        return self.system_settings
    
    def get_system_status(self) -> Dict:
        return self.system_status
    
    def get_system_logs(self) -> List[Dict]:
        return self.system_logs
    
    def update_system_settings(self, settings: dict) -> Dict:
        self.system_settings.update(settings)
        return self.system_settings
    
    def update_user_status(self, user_id: int, status_data: dict) -> Optional[Dict]:
        for user in self.admin_users:
            if user["id"] == user_id:
                user.update(status_data)
                return user
        return None
    
    def update_admin_user(self, user_id: int, user_data: dict) -> Optional[Dict]:
        for user in self.admin_users:
            if user["id"] == user_id:
                user.update(user_data)
                return user
        return None
    
    def delete_admin_user(self, user_id: int) -> bool:
        for i, user in enumerate(self.admin_users):
            if user["id"] == user_id:
                self.admin_users.pop(i)
                return True
        return False

