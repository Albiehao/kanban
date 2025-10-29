"""AI助手路由"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json
from datetime import datetime
from app.database import get_db, User
from app.auth import get_current_active_user
from app.schemas import ChatMessage, Conversation, ConversationCreate, ChatRequest
from app.services.deepseek_service import DeepSeekService
from app.services.agent.agent import TodoAgent
from app.database import get_db

router = APIRouter(prefix="/api/ai", tags=["AI助手"])

# 注意：DeepSeekService现在需要在路由中实例化，因为它需要数据库会话


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    http_request: Request = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """AI流式聊天接口（SSE）
    
    使用Server-Sent Events实现流式传输
    支持从Authorization头或query参数获取token
    """
    # 创建DeepSeek服务实例（从数据库读取配置）
    deepseek_service = DeepSeekService(db)
    
    # 检查限流
    allowed, error_msg = deepseek_service.check_rate_limit(current_user.id)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_msg
        )
    
    # 验证消息
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="消息不能为空"
        )
    
    if len(request.message) > 2000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="消息长度不能超过2000字符"
        )
    
    async def generate_response():
        """生成流式响应（使用Agent）"""
        try:
            # 创建Agent实例
            agent = TodoAgent(db, current_user)
            
            # 使用Agent处理消息并流式返回
            async for content_chunk in agent.process_message_stream(request.message):
                # 发送SSE格式数据
                data = json.dumps({"content": content_chunk}, ensure_ascii=False)
                yield f"data: {data}\n\n"
            
            # 发送结束标记
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            # 发送错误信息
            error_data = json.dumps({
                "error": str(e),
                "code": "INTERNAL_ERROR"
            }, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
            yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 禁用Nginx缓冲
        }
    )


@router.post("/chat", response_model=ChatMessage)
async def chat(
    message_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """发送消息给AI（非流式，兼容旧接口）"""
    message = message_data.get("message")
    
    if not message:
        raise HTTPException(status_code=400, detail="消息不能为空")
    
    # 创建DeepSeek服务实例（从数据库读取配置）
    deepseek_service = DeepSeekService(db)
    
    # 检查限流
    allowed, error_msg = deepseek_service.check_rate_limit(current_user.id)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_msg
        )
    
    # 使用流式接口但收集完整内容
    full_content = ""
    try:
        system_prompt = "你是一个有用的AI助手。"
        async for chunk in deepseek_service.generate_stream(message, system_prompt):
            full_content += chunk
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI服务错误: {str(e)}"
        )
    
    return {
        "id": 1,
        "role": "assistant",
        "content": full_content,
        "timestamp": datetime.now().isoformat()
    }


# 以下接口保留以兼容旧代码，但对话历史功能需要数据库支持
@router.get("/conversations", response_model=List[Conversation])
async def get_conversations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取所有对话（暂时返回空列表，未来可实现）"""
    return []


@router.get("/conversations/{conversation_id}/messages", response_model=List[ChatMessage])
async def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取对话消息（暂时返回空列表，未来可实现）"""
    return []


@router.post("/conversations", response_model=Conversation, status_code=201)
async def create_conversation(
    conversation: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建对话（暂时返回模拟数据，未来可实现）"""
    return {
        "id": 1,
        "messages": [],
        "title": conversation.title if hasattr(conversation, 'title') else "新对话"
    }


@router.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除对话"""
    pass


@router.delete("/conversations/{conversation_id}/clear", status_code=204)
async def clear_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """清空对话"""
    pass

