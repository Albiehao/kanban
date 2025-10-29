"""AI助手服务"""

from typing import List, Dict, Optional
from app.schemas import ConversationCreate
from app.storage import Storage


class AIService:
    """AI助手服务类"""
    
    def __init__(self, storage: Storage):
        """初始化服务
        
        Args:
            storage: 存储实例
        """
        self.storage = storage
    
    def create_chat_response(self, message: str, conversation_id: int) -> Dict:
        """创建AI回复"""
        return self.storage.create_chat_response(message, conversation_id)
    
    def get_conversations(self) -> List[Dict]:
        """获取所有对话"""
        return self.storage.get_conversations()
    
    def get_conversation_messages(self, conversation_id: int) -> Optional[List[Dict]]:
        """获取对话消息"""
        return self.storage.get_conversation_messages(conversation_id)
    
    def create_conversation(self, conversation: ConversationCreate) -> Dict:
        """创建对话"""
        return self.storage.create_conversation(conversation)
    
    def delete_conversation(self, conversation_id: int) -> bool:
        """删除对话"""
        return self.storage.delete_conversation(conversation_id)
    
    def clear_conversation(self, conversation_id: int) -> bool:
        """清空对话"""
        return self.storage.clear_conversation(conversation_id)

