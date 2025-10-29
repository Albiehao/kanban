"""Agent基础类和工具基类"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.database import User
import json


class BaseTool(ABC):
    """工具基类 - 所有工具都应继承此类"""
    
    def __init__(self, db: Session, user: User):
        """初始化工具
        
        Args:
            db: 数据库会话
            user: 当前用户
        """
        self.db = db
        self.user = user
    
    @abstractmethod
    def get_name(self) -> str:
        """返回工具名称"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """返回工具描述"""
        pass
    
    @abstractmethod
    def get_parameters_schema(self) -> Dict[str, Any]:
        """返回工具参数Schema（符合OpenAI Function Calling格式）
        
        Returns:
            {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "参数描述"
                    }
                },
                "required": ["param1"]
            }
        """
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """执行工具
        
        Args:
            **kwargs: 工具参数
            
        Returns:
            执行结果字典
        """
        pass
    
    def to_function_definition(self) -> Dict[str, Any]:
        """转换为OpenAI Function Calling格式
        
        Returns:
            函数定义字典
        """
        return {
            "type": "function",
            "function": {
                "name": self.get_name(),
                "description": self.get_description(),
                "parameters": self.get_parameters_schema()
            }
        }


class BaseAgent(ABC):
    """Agent基类 - 所有Agent都应继承此类"""
    
    def __init__(self, db: Session, user: User):
        """初始化Agent
        
        Args:
            db: 数据库会话
            user: 当前用户
        """
        self.db = db
        self.user = user
        self.tools: List[BaseTool] = []
        self.conversation_history: List[Dict[str, str]] = []
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """返回系统提示词"""
        pass
    
    def register_tool(self, tool: BaseTool):
        """注册工具
        
        Args:
            tool: 工具实例
        """
        self.tools.append(tool)
    
    def get_available_functions(self) -> List[Dict[str, Any]]:
        """获取所有可用函数的定义（OpenAI格式）"""
        return [tool.to_function_definition() for tool in self.tools]
    
    async def find_and_execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """查找并执行工具
        
        Args:
            function_name: 函数名称
            arguments: 函数参数
            
        Returns:
            执行结果
        """
        for tool in self.tools:
            if tool.get_name() == function_name:
                try:
                    result = await tool.execute(**arguments)
                    return {
                        "success": True,
                        "tool": function_name,
                        "result": result
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "tool": function_name,
                        "error": str(e)
                    }
        
        return {
            "success": False,
            "tool": function_name,
            "error": f"工具 '{function_name}' 不存在"
        }
    
    def add_message_to_history(self, role: str, content: Any):
        """添加消息到对话历史
        
        Args:
            role: 角色 (user/assistant/system/tool)
            content: 消息内容（可以是字符串或字典）
        """
        if isinstance(content, dict):
            # 如果content是字典，直接添加，但确保有role字段
            msg = content.copy()
            msg["role"] = role
            self.conversation_history.append(msg)
        else:
            # 如果是字符串或其他类型，转换为标准格式
            self.conversation_history.append({
                "role": role,
                "content": str(content) if content is not None else ""
            })
    
    def get_conversation_messages(self, include_system: bool = True) -> List[Dict[str, Any]]:
        """获取对话消息列表（用于LLM调用）
        
        Args:
            include_system: 是否包含系统提示词
            
        Returns:
            消息列表
        """
        messages = []
        
        if include_system:
            messages.append({
                "role": "system",
                "content": self.get_system_prompt()
            })
        
        # 处理对话历史（确保格式正确）
        for msg in self.conversation_history:
            if isinstance(msg, dict) and "role" in msg:
                # 直接是消息字典，确保格式正确
                formatted_msg = msg.copy()
                # 确保content字段存在
                if "content" not in formatted_msg:
                    formatted_msg["content"] = None
                messages.append(formatted_msg)
            else:
                # 其他情况，转换为标准格式
                content = str(msg) if msg is not None else ""
                messages.append({
                    "role": "user",
                    "content": content
                })
        
        return messages
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []

