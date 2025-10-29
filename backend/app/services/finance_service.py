"""财务服务"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, date as date_type, time as time_type
from decimal import Decimal
from app.database import Transaction, TransactionType
from app.schemas import TransactionCreate, TransactionUpdate


class FinanceService:
    """财务服务类"""
    
    def __init__(self, db: Session):
        """初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_transactions(
        self,
        user_id: int,
        date: Optional[str] = None,
        type: Optional[str] = None,
        category: Optional[str] = None,
        month: Optional[str] = None,
        page: int = 1,
        limit: int = 100
    ) -> Dict:
        """获取交易记录列表
        
        Args:
            user_id: 用户ID
            date: 日期过滤 (YYYY-MM-DD)
            type: 类型过滤 (income/expense)
            category: 类别过滤
            month: 月份过滤 (YYYY-MM)
            page: 页码
            limit: 每页数量
            
        Returns:
            交易记录列表和分页信息
        """
        # 构建查询
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        
        # 应用过滤条件
        if date:
            try:
                filter_date = datetime.strptime(date, "%Y-%m-%d").date()
                query = query.filter(Transaction.date == filter_date)
            except ValueError:
                raise ValueError("日期格式错误，应为 YYYY-MM-DD")
        
        if month:
            try:
                year, month_num = map(int, month.split('-'))
                # 月份的第一天和最后一天
                from calendar import monthrange
                start_date = date_type(year, month_num, 1)
                days_in_month = monthrange(year, month_num)[1]
                end_date = date_type(year, month_num, days_in_month)
                query = query.filter(
                    and_(Transaction.date >= start_date, Transaction.date <= end_date)
                )
            except ValueError:
                raise ValueError("月份格式错误，应为 YYYY-MM")
        
        if type:
            if type not in ['income', 'expense']:
                raise ValueError("type必须是income或expense")
            query = query.filter(Transaction.type == TransactionType(type))
        
        if category:
            query = query.filter(Transaction.category == category)
        
        # 获取总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * limit
        transactions = query.order_by(Transaction.date.desc(), Transaction.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "items": [t.to_dict() for t in transactions],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit if total > 0 else 0
            }
        }
    
    def get_transaction(self, transaction_id: int, user_id: int) -> Optional[Dict]:
        """获取单条交易记录
        
        Args:
            transaction_id: 交易记录ID
            user_id: 用户ID
            
        Returns:
            交易记录字典或None
        """
        transaction = self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()
        
        return transaction.to_dict() if transaction else None
    
    def create_transaction(self, transaction: TransactionCreate, user_id: int) -> Dict:
        """创建交易记录
        
        Args:
            transaction: 交易记录数据
            user_id: 用户ID
            
        Returns:
            创建的交易记录
        """
        # 解析日期
        try:
            transaction_date = datetime.strptime(transaction.date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("日期格式错误，应为 YYYY-MM-DD")
        
        # 解析时间（可选）
        transaction_time = None
        if transaction.time:
            # 支持 HH:MM 或 HH:MM:SS 格式
            time_formats = ["%H:%M", "%H:%M:%S"]
            for fmt in time_formats:
                try:
                    parsed_time = datetime.strptime(transaction.time, fmt).time()
                    transaction_time = parsed_time
                    break
                except ValueError:
                    continue
            if transaction_time is None:
                raise ValueError("时间格式错误，应为HH:MM或HH:MM:SS")
        
        # 创建交易记录
        db_transaction = Transaction(
            user_id=user_id,
            type=TransactionType(transaction.type),
            amount=Decimal(str(transaction.amount)),
            category=transaction.category,
            description=transaction.description,
            date=transaction_date,
            time=transaction_time
        )
        
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        
        print(f"[INFO] 用户 {user_id} 创建了交易记录: ID={db_transaction.id}, 类型={transaction.type}, 金额={transaction.amount}, 类别={transaction.category}")
        
        return db_transaction.to_dict()
    
    def update_transaction(
        self,
        transaction_id: int,
        transaction_update: TransactionUpdate,
        user_id: int
    ) -> Optional[Dict]:
        """更新交易记录
        
        Args:
            transaction_id: 交易记录ID
            transaction_update: 更新数据
            user_id: 用户ID
            
        Returns:
            更新后的交易记录或None
        """
        # 获取交易记录
        db_transaction = self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()
        
        if not db_transaction:
            return None
        
        # 更新字段
        update_data = transaction_update.dict(exclude_unset=True)
        
        if "date" in update_data and update_data["date"]:
            try:
                db_transaction.date = datetime.strptime(update_data["date"], "%Y-%m-%d").date()
                del update_data["date"]
            except ValueError:
                raise ValueError("日期格式错误，应为 YYYY-MM-DD")
        
        if "time" in update_data:
            if update_data["time"] is None:
                # 允许设置为None取消时间
                db_transaction.time = None
            else:
                # 解析时间（支持 HH:MM 或 HH:MM:SS 格式）
                time_formats = ["%H:%M", "%H:%M:%S"]
                parsed_time = None
                for fmt in time_formats:
                    try:
                        parsed_time = datetime.strptime(update_data["time"], fmt).time()
                        break
                    except ValueError:
                        continue
                if parsed_time is None:
                    raise ValueError("时间格式错误，应为HH:MM或HH:MM:SS")
                db_transaction.time = parsed_time
            del update_data["time"]
        
        if "type" in update_data:
            db_transaction.type = TransactionType(update_data["type"])
            del update_data["type"]
        
        if "amount" in update_data:
            db_transaction.amount = Decimal(str(update_data["amount"]))
            del update_data["amount"]
        
        # 更新其他字段
        for key, value in update_data.items():
            setattr(db_transaction, key, value)
        
        self.db.commit()
        self.db.refresh(db_transaction)
        
        print(f"[INFO] 用户 {user_id} 更新了交易记录: ID={transaction_id}")
        
        return db_transaction.to_dict()
    
    def delete_transaction(self, transaction_id: int, user_id: int) -> Optional[Dict]:
        """删除交易记录
        
        Args:
            transaction_id: 交易记录ID
            user_id: 用户ID
            
        Returns:
            删除前的交易记录信息，如果不存在返回None
        """
        # 获取交易记录
        db_transaction = self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()
        
        if not db_transaction:
            return None
        
        transaction_info = {
            "id": db_transaction.id,
            "type": db_transaction.type.value,
            "description": db_transaction.description
        }
        
        self.db.delete(db_transaction)
        self.db.commit()
        
        print(f"[INFO] 用户 {user_id} 删除了交易记录: ID={transaction_id}, 类型={transaction_info['type']}")
        
        return transaction_info
    
    def get_finance_stats(self, user_id: int, month: Optional[str] = None) -> Dict:
        """获取财务统计数据
        
        Args:
            user_id: 用户ID
            month: 月份 (YYYY-MM)，默认当前月
            
        Returns:
            财务统计数据
        """
        from calendar import monthrange
        
        # 确定统计月份
        if month:
            try:
                year, month_num = map(int, month.split('-'))
            except ValueError:
                raise ValueError("月份格式错误，应为 YYYY-MM")
        else:
            now = datetime.now()
            year = now.year
            month_num = now.month
        
        # 月份的第一天和最后一天
        start_date = date_type(year, month_num, 1)
        days_in_month = monthrange(year, month_num)[1]
        end_date = date_type(year, month_num, days_in_month)
        
        # 查询该月的所有交易记录
        transactions = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).all()
        
        # 计算统计数据
        monthly_income = Decimal('0')
        monthly_expense = Decimal('0')
        expense_by_category = {}
        
        # 类别颜色映射
        category_colors = {
            "餐饮": "#ef4444",
            "学习": "#3b82f6",
            "交通": "#10b981",
            "娱乐": "#f59e0b",
            "兼职": "#8b5cf6",
            "其他": "#6b7280"
        }
        
        # 默认颜色列表（用于未定义的类别）
        default_colors = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#6b7280"]
        color_index = 0
        
        for transaction in transactions:
            amount = transaction.amount if isinstance(transaction.amount, Decimal) else Decimal(str(transaction.amount))
            
            if transaction.type == TransactionType.income:
                monthly_income += amount
            else:  # expense
                monthly_expense += amount
                
                # 按类别统计支出
                category = transaction.category
                if category not in expense_by_category:
                    expense_by_category[category] = {
                        "category": category,
                        "amount": Decimal('0'),
                        "color": category_colors.get(category, default_colors[color_index % len(default_colors)])
                    }
                    if category not in category_colors:
                        color_index += 1
                
                expense_by_category[category]["amount"] += amount
        
        # 转换为float用于返回
        return {
            "monthlyIncome": float(monthly_income),
            "monthlyExpense": float(monthly_expense),
            "balance": float(monthly_income - monthly_expense),
            "expenseByCategory": [
                {
                    "category": item["category"],
                    "amount": float(item["amount"]),
                    "color": item["color"]
                }
                for item in expense_by_category.values()
            ]
        }
