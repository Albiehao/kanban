"""实时更新路由（SSE）"""

from typing import Optional, Set
from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.auth import get_current_active_user
from app.services.updates_service import updates_service
from datetime import datetime
import json

router = APIRouter(prefix="/api/updates", tags=["实时更新"])


@router.get("/stream")
async def updates_stream(
    types: Optional[str] = Query(None, description="订阅的数据类型，多个用逗号分隔，如：tasks,courses"),
    since: Optional[str] = Query(None, description="ISO 8601时间戳，只接收此时间之后的更新"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    实时更新流接口（Server-Sent Events）
    
    订阅用户的实时数据变更（任务、课程等）
    """
    # 解析订阅类型
    subscribed_types: Set[str] = set()
    if types:
        subscribed_types = {t.strip() for t in types.split(",") if t.strip()}
    else:
        # 默认订阅所有类型
        subscribed_types = {"tasks", "courses"}
    
    # 验证订阅类型
    valid_types = {"tasks", "courses"}
    subscribed_types = {t for t in subscribed_types if t in valid_types}
    
    if not subscribed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="至少订阅一种数据类型（tasks或courses）"
        )
    
    async def event_stream():
        """生成SSE事件流"""
        try:
            async for event_data in updates_service.event_stream(
                db,
                current_user.id,
                subscribed_types,
                since
            ):
                yield event_data
        except Exception as e:
            # 发送错误信息
            error_data = json.dumps({
                "error": str(e),
                "code": "INTERNAL_ERROR"
            }, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 禁用Nginx缓冲
        }
    )


@router.post("/trigger/{type}")
async def trigger_update(
    type: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    手动触发更新事件（用于测试或外部触发）
    
    注意：此接口需要管理员权限或在特定场景下使用
    """
    # 验证类型
    if type not in ["tasks", "courses"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="类型必须是tasks或courses"
        )
    
    # 广播更新事件（示例：通知所有连接有新数据）
    event = {
        "type": type,
        "action": "updated",
        "message": "数据已更新，请刷新",
        "timestamp": datetime.now().isoformat()
    }
    
    await updates_service.broadcast_update(current_user.id, event)
    
    return {
        "success": True,
        "message": f"已触发 {type} 更新事件"
    }

