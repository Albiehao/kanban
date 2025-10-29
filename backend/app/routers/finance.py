"""财务路由"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, Transaction, User
from app.schemas import TransactionCreate, TransactionUpdate
from app.auth import get_current_user
from app.services.finance_service import FinanceService
from datetime import datetime

router = APIRouter(prefix="/api/transactions", tags=["财务"])


def get_service(db: Session = Depends(get_db)) -> FinanceService:
    """依赖注入：获取财务服务"""
    return FinanceService(db)


@router.get("")
async def get_transactions(
    date: Optional[str] = Query(None, description="日期过滤 YYYY-MM-DD"),
    type: Optional[str] = Query(None, description="类型过滤 income/expense"),
    category: Optional[str] = Query(None, description="类别过滤"),
    month: Optional[str] = Query(None, description="月份过滤 YYYY-MM"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(100, ge=1, le=500, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取交易记录列表，支持分页和过滤"""
    
    try:
        service = get_service(db)
        result = service.get_transactions(
            user_id=current_user.id,
            date=date,
            type=type,
            category=category,
            month=month,
            page=page,
            limit=limit
        )
        # 按照需求文档，直接返回数组格式，不包含分页信息
        return {"data": result["items"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单条交易记录"""
    
    service = get_service(db)
    transaction = service.get_transaction(transaction_id, current_user.id)
    
    if not transaction:
        raise HTTPException(status_code=404, detail="交易记录不存在")
    
    return {"data": transaction}


@router.post("", status_code=201)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建交易记录"""
    
    try:
        service = get_service(db)
        result = service.create_transaction(transaction, current_user.id)
        return {
            "message": "交易记录创建成功",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{transaction_id}")
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新交易记录"""
    
    try:
        service = get_service(db)
        result = service.update_transaction(
            transaction_id,
            transaction_update,
            current_user.id
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="交易记录不存在或不属于当前用户")
        
        return {
            "message": "交易记录更新成功",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除交易记录"""
    
    service = get_service(db)
    transaction_info = service.delete_transaction(transaction_id, current_user.id)
    
    if not transaction_info:
        raise HTTPException(status_code=404, detail="交易记录不存在或不属于当前用户")
    
    return {
        "message": "交易记录删除成功",
        "data": transaction_info
    }
