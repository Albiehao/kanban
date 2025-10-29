"""DeepSeek AI服务"""

import os
from typing import AsyncGenerator, Optional
import openai
from datetime import datetime, timedelta
from collections import defaultdict
from sqlalchemy.orm import Session
from app.database import DeepSeekConfig, SessionLocal

# 默认配置（用于向后兼容或数据库未配置时）
DEFAULT_API_KEY = "sk-9cb005b49aae4cba91a717cf8420bb5f"
DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_RATE_LIMIT_PER_MINUTE = 10
DEFAULT_RATE_LIMIT_PER_DAY = 500

# 请求记录（用于限流）
request_records = defaultdict(list)  # {user_id: [timestamps...]}


class DeepSeekService:
    """DeepSeek AI服务类"""
    
    def __init__(self, db: Optional[Session] = None):
        """初始化DeepSeek客户端
        
        Args:
            db: 数据库会话（可选），如果不提供则从数据库读取配置
        """
        # 从数据库读取配置
        self.api_key, self.base_url, self.model, self.rate_limit_per_minute, self.rate_limit_per_day = self._load_config(db)
        
        # 初始化OpenAI客户端
        self.client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def _load_config(self, db: Optional[Session] = None) -> tuple:
        """从数据库加载配置
        
        Returns:
            (api_key, base_url, model, rate_limit_per_minute, rate_limit_per_day)
        """
        # 如果没有提供db，创建临时会话
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False
        
        try:
            # 查询启用的配置（应该只有一个）
            config = db.query(DeepSeekConfig).filter(
                DeepSeekConfig.is_active == True
            ).first()
            
            if config:
                return (
                    config.api_key,
                    config.base_url or DEFAULT_BASE_URL,
                    config.model or DEFAULT_MODEL,
                    config.rate_limit_per_minute or DEFAULT_RATE_LIMIT_PER_MINUTE,
                    config.rate_limit_per_day or DEFAULT_RATE_LIMIT_PER_DAY
                )
            else:
                # 数据库中没有配置，使用默认值或环境变量
                api_key = os.getenv("DEEPSEEK_API_KEY", DEFAULT_API_KEY)
                base_url = os.getenv("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL)
                model = os.getenv("DEEPSEEK_MODEL", DEFAULT_MODEL)
                rate_limit_per_minute = int(os.getenv("AI_RATE_LIMIT_PER_MINUTE", str(DEFAULT_RATE_LIMIT_PER_MINUTE)))
                rate_limit_per_day = int(os.getenv("AI_RATE_LIMIT_PER_DAY", str(DEFAULT_RATE_LIMIT_PER_DAY)))
                
                return (api_key, base_url, model, rate_limit_per_minute, rate_limit_per_day)
        except Exception as e:
            print(f"[DeepSeekService] 加载配置失败，使用默认值: {e}")
            # 发生错误时使用默认值
            return (
                os.getenv("DEEPSEEK_API_KEY", DEFAULT_API_KEY),
                os.getenv("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL),
                os.getenv("DEEPSEEK_MODEL", DEFAULT_MODEL),
                int(os.getenv("AI_RATE_LIMIT_PER_MINUTE", str(DEFAULT_RATE_LIMIT_PER_MINUTE))),
                int(os.getenv("AI_RATE_LIMIT_PER_DAY", str(DEFAULT_RATE_LIMIT_PER_DAY)))
            )
        finally:
            if should_close:
                db.close()
    
    def check_rate_limit(self, user_id: int) -> tuple:
        """检查用户请求频率限制
        
        Returns:
            (是否允许, 错误消息)
        """
        now = datetime.now()
        user_requests = request_records[user_id]
        
        # 清理过期记录（1分钟前的）
        cutoff_time = now - timedelta(minutes=1)
        user_requests[:] = [t for t in user_requests if t > cutoff_time]
        
        # 检查每分钟限制（使用数据库配置的值）
        if len(user_requests) >= self.rate_limit_per_minute:
            return False, f"请求频率过高，每分钟最多{self.rate_limit_per_minute}次请求"
        
        # 检查每日限制（简化版，实际应使用Redis或数据库）
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_requests = [t for t in user_requests if t >= today_start]
        if len(today_requests) >= self.rate_limit_per_day:
            return False, f"每日请求配额已用完，每日最多{self.rate_limit_per_day}次请求"
        
        # 记录请求
        user_requests.append(now)
        
        return True, ""
    
    async def generate_stream(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        tools: Optional[list] = None,
        tool_choice: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """生成流式响应（支持工具调用）
        
        Args:
            message: 用户消息
            system_prompt: 系统提示词（可选）
            tools: 工具定义列表（可选，用于function calling）
            tool_choice: 工具选择模式，None表示自动，"none"表示不调用工具
            
        Yields:
            文本片段
        """
        # 构建消息
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        try:
            # 构建API参数
            api_params = {
                "model": self.model,
                "messages": messages,
                "stream": True,
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            # 如果提供了工具，添加工具参数
            if tools:
                api_params["tools"] = tools
                api_params["tool_choice"] = tool_choice if tool_choice else "auto"
            
            # 调用DeepSeek API（流式模式）
            stream = await self.client.chat.completions.create(**api_params)
            
            # 流式返回内容
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    yield content
        
        except Exception as e:
            error_msg = str(e)
            # 如果是API错误，返回友好提示
            if "rate_limit" in error_msg.lower():
                yield f"[错误: API请求频率限制，请稍后再试]"
            elif "insufficient_quota" in error_msg.lower():
                yield f"[错误: API配额不足]"
            else:
                yield f"[错误: {error_msg}]"
            raise

