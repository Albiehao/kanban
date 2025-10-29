"""任务路由"""

from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db, Task, User
from app.schemas import TaskCreate, TaskUpdate
from app.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/tasks", tags=["任务"])


@router.get("")
async def get_tasks(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    date: Optional[str] = Query(None, description="日期过滤 YYYY-MM-DD"),
    completed: Optional[bool] = Query(None, description="完成状态过滤"),
    priority: Optional[str] = Query(None, description="优先级过滤"),
    has_reminder: Optional[bool] = Query(None, description="是否有提醒"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务列表，支持分页和过滤"""
    
    # 构建查询
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    # 应用过滤条件
    if date:
        try:
            filter_date = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(Task.date == filter_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，应为 YYYY-MM-DD")
    
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    if priority:
        query = query.filter(Task.priority == priority)
    
    if has_reminder is not None:
        query = query.filter(Task.has_reminder == has_reminder)
    
    # 获取总数
    total = query.count()
    
    # 计算分页
    offset = (page - 1) * limit
    total_pages = (total + limit - 1) // limit if total > 0 else 0
    
    # 获取任务列表，按创建时间倒序
    tasks = query.order_by(Task.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "data": {
            "items": [task.to_dict() for task in tasks],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
    }


@router.post("", status_code=201)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建任务"""
    
    # 调试日志：接收到的原始数据
    print(f"[DEBUG] 创建任务 - 用户ID: {current_user.id}")
    print(f"[DEBUG] 接收到的任务数据:")
    print(f"  - title: {task.title}")
    print(f"  - date: {task.date}")
    print(f"  - has_reminder: {task.has_reminder} (类型: {type(task.has_reminder)})")
    print(f"  - reminder_time: {task.reminder_time} (类型: {type(task.reminder_time)})")
    
    # 解析日期和时间
    try:
        task_date = datetime.strptime(task.date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，应为 YYYY-MM-DD")
    
    reminder_time = None
    if task.reminder_time:
        try:
            reminder_time = datetime.fromisoformat(task.reminder_time.replace('Z', '+00:00'))
            print(f"[DEBUG] 解析后的提醒时间: {reminder_time}")
        except ValueError as e:
            print(f"[DEBUG] 提醒时间解析失败: {e}")
            raise HTTPException(status_code=400, detail="提醒时间格式错误")
    else:
        print(f"[DEBUG] 未设置提醒时间（reminder_time 为 None 或空）")
    
    # 创建任务
    db_task = Task(
        user_id=current_user.id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        date=task_date,
        time=task.time,
        has_reminder=task.has_reminder,
        reminder_time=reminder_time
    )
    
    print(f"[DEBUG] 准备保存到数据库:")
    print(f"  - has_reminder: {db_task.has_reminder}")
    print(f"  - reminder_time: {db_task.reminder_time}")
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    print(f"[DEBUG] 任务已保存到数据库:")
    print(f"  - ID: {db_task.id}")
    print(f"  - has_reminder: {db_task.has_reminder}")
    print(f"  - reminder_time: {db_task.reminder_time}")
    
    # 触发实时更新事件
    try:
        from app.services.updates_service import updates_service
        import asyncio
        event = {
            "type": "task",
            "action": "created",
            "data": db_task.to_dict(),
            "timestamp": datetime.now().isoformat()
        }
        asyncio.create_task(updates_service.broadcast_update(current_user.id, event))
    except Exception as e:
        print(f"[DEBUG] 触发更新事件失败: {e}")
    
    result = {
        "data": db_task.to_dict()
    }
    
    print(f"[DEBUG] 返回给前端的数据: {result}")
    
    return result


@router.put("/{task_id}")
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任务"""
    
    # 获取任务
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 更新字段
    update_data = task_update.dict(exclude_unset=True)
    
    if "date" in update_data and update_data["date"]:
        try:
            db_task.date = datetime.strptime(update_data["date"], "%Y-%m-%d").date()
            del update_data["date"]
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，应为 YYYY-MM-DD")
    
    if "reminder_time" in update_data:
        reminder_time_value = update_data["reminder_time"]
        if reminder_time_value is None:
            # 取消提醒
            db_task.reminder_time = None
        elif reminder_time_value:
            # 设置提醒时间
            try:
                db_task.reminder_time = datetime.fromisoformat(
                    reminder_time_value.replace('Z', '+00:00')
                )
            except ValueError:
                raise HTTPException(status_code=400, detail="提醒时间格式错误")
        del update_data["reminder_time"]
    
    # 更新其他字段
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    
    # 触发实时更新事件
    try:
        from app.services.updates_service import updates_service
        import asyncio
        event = {
            "type": "task",
            "action": "updated",
            "data": db_task.to_dict(),
            "timestamp": datetime.now().isoformat()
        }
        asyncio.create_task(updates_service.broadcast_update(current_user.id, event))
    except Exception as e:
        print(f"[DEBUG] 触发更新事件失败: {e}")
    
    return {
        "data": db_task.to_dict()
    }


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除任务"""
    
    # 获取任务
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 记录删除前的信息
    task_title = db_task.title
    task_id_val = db_task.id
    
    # 删除任务
    db.delete(db_task)
    db.commit()
    
    print(f"[INFO] 用户 {current_user.username} (ID: {current_user.id}) 删除了任务: ID={task_id_val}, 标题={task_title}")
    
    # 触发实时更新事件
    try:
        from app.services.updates_service import updates_service
        import asyncio
        event = {
            "type": "task",
            "action": "deleted",
            "id": task_id_val,
            "timestamp": datetime.now().isoformat()
        }
        asyncio.create_task(updates_service.broadcast_update(current_user.id, event))
    except Exception as e:
        print(f"[DEBUG] 触发更新事件失败: {e}")
    
    return {
        "message": "任务删除成功",
        "data": {
            "id": task_id_val,
            "title": task_title
        }
    }


@router.patch("/{task_id}/toggle")
async def toggle_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """切换任务完成状态"""
    
    # 获取任务
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 切换状态
    db_task.completed = not db_task.completed
    
    db.commit()
    db.refresh(db_task)
    
    return {
        "data": db_task.to_dict()
    }


# 批量删除请求模型
class BatchDeleteRequest(BaseModel):
    task_ids: List[int]


@router.delete("/batch", status_code=200)
async def batch_delete_tasks(
    request: BatchDeleteRequest = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量删除任务"""
    
    if not request.task_ids:
        raise HTTPException(status_code=400, detail="任务ID列表不能为空")
    
    # 查询要删除的任务（只能删除当前用户的任务）
    tasks_to_delete = db.query(Task).filter(
        Task.id.in_(request.task_ids),
        Task.user_id == current_user.id
    ).all()
    
    if not tasks_to_delete:
        raise HTTPException(status_code=404, detail="未找到要删除的任务")
    
    # 记录删除的任务信息
    deleted_tasks = []
    for task in tasks_to_delete:
        deleted_tasks.append({
            "id": task.id,
            "title": task.title
        })
        db.delete(task)
    
    db.commit()
    
    print(f"[INFO] 用户 {current_user.username} (ID: {current_user.id}) 批量删除了 {len(deleted_tasks)} 个任务")
    
    return {
        "message": f"成功删除 {len(deleted_tasks)} 个任务",
        "data": {
            "deleted_count": len(deleted_tasks),
            "deleted_tasks": deleted_tasks
        }
    }

