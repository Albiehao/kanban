"""财务管理工具"""

from typing import Dict, Any, Optional
from app.services.agent.base import BaseTool
from app.services.finance_service import FinanceService
from app.schemas import TransactionCreate, TransactionUpdate


class GetTransactionsTool(BaseTool):
    """获取交易记录工具"""
    
    def get_name(self) -> str:
        return "get_transactions"
    
    def get_description(self) -> str:
        return "获取用户的交易记录列表，支持按日期、类型、类别、月份筛选"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "日期筛选，格式：YYYY-MM-DD"
                },
                "type": {
                    "type": "string",
                    "enum": ["income", "expense"],
                    "description": "类型筛选，income表示收入，expense表示支出"
                },
                "category": {
                    "type": "string",
                    "description": "类别筛选，如：餐饮、学习、交通、娱乐、兼职、其他"
                },
                "month": {
                    "type": "string",
                    "description": "月份筛选，格式：YYYY-MM，例如：2025-10"
                },
                "limit": {
                    "type": "integer",
                    "description": "返回数量限制，默认100",
                    "default": 100
                }
            },
            "required": []
        }
    
    async def execute(self, date: Optional[str] = None, type: Optional[str] = None,
                     category: Optional[str] = None, month: Optional[str] = None,
                     limit: int = 100) -> Dict[str, Any]:
        """执行获取交易记录"""
        service = FinanceService(self.db)
        result = service.get_transactions(
            user_id=self.user.id,
            date=date,
            type=type,
            category=category,
            month=month,
            page=1,
            limit=limit
        )
        
        return {
            "count": len(result["items"]),
            "transactions": result["items"]
        }


class CreateTransactionTool(BaseTool):
    """创建交易记录工具"""
    
    def get_name(self) -> str:
        return "create_transaction"
    
    def get_description(self) -> str:
        return "创建新的交易记录（记账），可以是收入或支出"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["income", "expense"],
                    "description": "交易类型，income表示收入，expense表示支出（必填）"
                },
                "amount": {
                    "type": "number",
                    "description": "金额，必须大于0（必填）"
                },
                "category": {
                    "type": "string",
                    "description": "类别，如：餐饮、学习、交通、娱乐、兼职、其他（必填）"
                },
                "description": {
                    "type": "string",
                    "description": "描述信息，最大255字符（必填）"
                },
                "date": {
                    "type": "string",
                    "description": "交易日期，格式：YYYY-MM-DD（必填）"
                },
                "time": {
                    "type": "string",
                    "description": "交易时间，格式：HH:MM或HH:MM:SS（可选）"
                }
            },
            "required": ["type", "amount", "category", "description", "date"]
        }
    
    async def execute(self, type: str, amount: float, category: str,
                     description: str, date: str, time: Optional[str] = None) -> Dict[str, Any]:
        """执行创建交易记录"""
        try:
            transaction = TransactionCreate(
                type=type,
                amount=amount,
                category=category,
                description=description,
                date=date,
                time=time
            )
            service = FinanceService(self.db)
            result = service.create_transaction(transaction, self.user.id)
            
            return {
                "success": True,
                "message": "交易记录创建成功",
                "transaction": result
            }
        except ValueError as e:
            return {"error": str(e)}


class DeleteTransactionTool(BaseTool):
    """删除交易记录工具（退款）"""
    
    def get_name(self) -> str:
        return "delete_transaction"
    
    def get_description(self) -> str:
        return "删除交易记录（退款功能）"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "transaction_id": {
                    "type": "integer",
                    "description": "要删除的交易记录ID（必填）"
                }
            },
            "required": ["transaction_id"]
        }
    
    async def execute(self, transaction_id: int) -> Dict[str, Any]:
        """执行删除交易记录"""
        service = FinanceService(self.db)
        result = service.delete_transaction(transaction_id, self.user.id)
        
        if not result:
            return {"error": "交易记录不存在或不属于当前用户"}
        
        return {
            "success": True,
            "message": "交易记录删除成功（退款）",
            "transaction": result
        }


class GetFinanceStatsTool(BaseTool):
    """获取财务统计工具"""
    
    def get_name(self) -> str:
        return "get_finance_stats"
    
    def get_description(self) -> str:
        return "获取财务统计数据，包括月度收入、支出、结余和分类统计（查账）"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "month": {
                    "type": "string",
                    "description": "查询月份，格式：YYYY-MM，例如：2025-10，默认当前月"
                }
            },
            "required": []
        }
    
    async def execute(self, month: Optional[str] = None) -> Dict[str, Any]:
        """执行获取财务统计"""
        service = FinanceService(self.db)
        stats = service.get_finance_stats(self.user.id, month)
        
        return {
            "success": True,
            "stats": stats
        }

