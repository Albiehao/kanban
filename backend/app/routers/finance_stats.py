"""财务统计路由"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.auth import get_current_user
from app.services.finance_service import FinanceService

router = APIRouter(prefix="/api/finance", tags=["财务"])


def get_service(db: Session = Depends(get_db)) -> FinanceService:
    """依赖注入：获取财务服务"""
    return FinanceService(db)


@router.get("/stats")
async def get_finance_stats(
    month: Optional[str] = Query(None, description="月份过滤 YYYY-MM，默认当前月"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取财务统计数据"""
    
    try:
        service = get_service(db)
        stats = service.get_finance_stats(user_id=current_user.id, month=month)
        return {"data": stats}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
