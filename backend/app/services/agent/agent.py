"""智能Agent主类"""

from typing import AsyncGenerator, Dict, Any
import json
from app.services.agent.base import BaseAgent
from app.services.agent.tools.task_tool import (
    GetTasksTool, CreateTaskTool, UpdateTaskTool, DeleteTaskTool, CompleteTaskTool
)
from app.services.agent.tools.finance_tool import (
    GetTransactionsTool, CreateTransactionTool, DeleteTransactionTool, GetFinanceStatsTool
)
from app.services.agent.tools.course_tool import GetCoursesTool
from app.services.agent.tools.schedule_tool import FindFreeTimeTool, CreateTaskInFreeTimeTool
from app.services.agent.tools.time_tool import GetCurrentTimeTool
from app.services.deepseek_service import DeepSeekService


class TodoAgent(BaseAgent):
    """待办事项智能Agent"""
    
    def __init__(self, db, user):
        """初始化Agent"""
        super().__init__(db, user)
        self.deepseek_service = DeepSeekService(db)
        
        # 调用统一工具注册方法
        self._register_all_tools(db, user)
    
    def _register_all_tools(self, db, user):
        """统一注册所有工具到工具列表
        
        Args:
            db: 数据库会话
            user: 当前用户
        """
        # 注册所有工具
        self.register_tool(GetTasksTool(db, user))
        self.register_tool(CreateTaskTool(db, user))
        self.register_tool(UpdateTaskTool(db, user))
        self.register_tool(DeleteTaskTool(db, user))
        self.register_tool(CompleteTaskTool(db, user))
        
        self.register_tool(GetTransactionsTool(db, user))
        self.register_tool(CreateTransactionTool(db, user))
        self.register_tool(DeleteTransactionTool(db, user))
        self.register_tool(GetFinanceStatsTool(db, user))
        
        self.register_tool(GetCoursesTool(db, user))
        
        self.register_tool(FindFreeTimeTool(db, user))
        self.register_tool(CreateTaskInFreeTimeTool(db, user))
        
        self.register_tool(GetCurrentTimeTool(db, user))
        
        print(f"[Agent] 已注册 {len(self.tools)} 个工具")
    
    def get_system_prompt(self) -> str:
        """返回系统提示词"""
        # 获取当前时间信息（如果已获取）
        time_info = ""
        if hasattr(self, 'current_time_info') and self.current_time_info:
            current_time_info = self.current_time_info
            if current_time_info.get("success"):
                time_info = f"\n当前系统时间：{current_time_info.get('datetime')}，今天是{current_time_info.get('weekday')}\n"
        
        return f"""你是一个智能待办事项助手，可以帮助用户管理任务、记账、查询课程表、安排时间。
{time_info}
重要提示：
1. 所有工具调用必须使用真实数据，不要编造任何信息
2. 当用户询问日期或时间时，你可以直接使用上面提供的当前系统时间，无需再次调用 get_current_time 工具
3. 当用户询问课程、课表、课程安排时，必须调用 get_courses 工具获取真实的课程数据
4. 当需要执行特定的操作时（如创建任务、记账等），必须先收集完整信息，然后再调用相应工具

工具说明：
- get_current_time: 获取当前日期和时间（通常不需要调用，系统已提供当前时间）
- get_courses: 获取课程表信息（必须用于所有课程相关查询）
- get_tasks: 查询任务列表
- create_task: 创建新任务
- update_task: 更新任务
- delete_task: 删除任务
- complete_task: 完成任务
- get_transactions: 查询交易记录
- create_transaction: 创建交易记录
- delete_transaction: 删除交易记录
- get_finance_stats: 获取财务统计
- find_free_time: 查找空闲时间
- create_task_in_free_time: 在空闲时间创建任务

请以友好、专业的方式与用户交流，并提供准确的帮助。"""
    
    async def process_message_stream(self, user_message: str) -> AsyncGenerator[str, None]:
        """流式处理用户消息
        
        工作流程：
        1. 收到用户提示词，添加到历史
        2. 先调用 get_current_time 获取当前时间
        3. 将当前时间信息添加到系统提示中
        4. 通过LLM判断是否需要调用工具
        5. 如果需要，调用工具获取信息
        6. 将工具输出传给LLM，LLM输出结果流式传输给用户
        
        Args:
            user_message: 用户消息
            
        Yields:
            流式返回的文本块
        """
        # 先获取当前时间
        try:
            current_time_tool = next((tool for tool in self.tools if tool.get_name() == "get_current_time"), None)
            if current_time_tool:
                time_result = await current_time_tool.execute(format="full")
                if time_result.get("success"):
                    self.current_time_info = time_result
                    print(f"[Agent] 已获取当前时间: {time_result.get('datetime')}")
                else:
                    self.current_time_info = {}
                    print(f"[Agent] 获取当前时间失败: {time_result.get('error')}")
            else:
                self.current_time_info = {}
                print(f"[Agent] 未找到 get_current_time 工具")
        except Exception as e:
            self.current_time_info = {}
            print(f"[Agent] 获取当前时间异常: {str(e)}")
        
        # 添加用户消息到历史
        self.add_message_to_history("user", user_message)
        
        # 获取工具定义
        tools_list = self.get_available_functions()
        
        # 持续处理，直到没有更多工具调用（保留最多5轮上下文）
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n[Agent] ===== 迭代 {iteration} =====")
            
            # 如果对话历史过长，清除最早的消息，保留最近的10条（大约5轮）
            if len(self.conversation_history) > 10:
                removed_count = len(self.conversation_history) - 10
                print(f"[Agent] 对话历史过长，清除最早的 {removed_count} 条消息")
                # 保留最近的10条消息（5轮对话：用户+助手/工具）
                recent_history = self.conversation_history[-10:]
                self.conversation_history = recent_history
            
            try:
                # 步骤1: 通过LLM判断是否需要调用工具
                messages = self.get_conversation_messages()
                
                print(f"[Agent] 发送给LLM的消息数量: {len(messages)}")
                print(f"[Agent] 可用工具数量: {len(tools_list)}")
                
                # 调用DeepSeek API（非流式，便于检测工具调用）
                response = await self.deepseek_service.client.chat.completions.create(
                    model=self.deepseek_service.model,
                    messages=messages,
                    tools=tools_list,  # 提供工具定义，让LLM判断
                    temperature=0.7,
                    max_tokens=2000
                )
                
                assistant_message = response.choices[0].message
                tool_calls = assistant_message.tool_calls
                
                print(f"[Agent] LLM判断结果:")
                print(f"  - 文本内容: {assistant_message.content}")
                print(f"  - 工具调用数: {len(tool_calls) if tool_calls else 0}")
                
                # 步骤2: 如果需要调用工具，执行工具并获取信息
                if tool_calls:
                    print(f"[Agent] LLM决定调用工具，开始执行...")
                    
                    # 记录LLM的回复（可能包含文本内容）
                    assistant_text = assistant_message.content or ""
                    
                    # 构建工具调用消息（用于历史记录）
                    tool_call_msg = {
                        "role": "assistant",
                        "content": assistant_text,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": tc.type,
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            } for tc in tool_calls
                        ]
                    }
                    # 注意：这里先不添加到历史，等工具执行完再一起添加
                    
                    # 执行所有工具
                    tool_results = []
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        arguments_str = tool_call.function.arguments
                        
                        print(f"[Agent] 调用工具: {function_name}")
                        print(f"[Agent] 参数: {arguments_str}")
                        
                        try:
                            # 执行工具
                            arguments = json.loads(arguments_str) if arguments_str else {}
                            tool_result = await self.find_and_execute_tool(function_name, arguments)
                            
                            result_str = json.dumps(tool_result, ensure_ascii=False)
                            print(f"[Agent] 工具返回值: {result_str[:200]}...")
                            
                            # 保存工具结果
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": result_str
                            })
                            
                        except Exception as e:
                            print(f"[Agent] 工具执行失败: {str(e)}")
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps({"error": str(e)}, ensure_ascii=False)
                            })
                    
                    # 添加到对话历史
                    self.conversation_history.append(tool_call_msg)
                    self.conversation_history.extend(tool_results)
                    
                    # 继续循环，让LLM基于工具结果生成回复
                    print(f"[Agent] 工具执行完成，等待LLM生成回复...")
                    continue
                
                # 步骤3: 不需要调用工具，LLM直接生成流式回复
                else:
                    print(f"[Agent] LLM不需要调用工具，开始流式生成最终回复...")
                    
                    # 使用流式API生成最终回复
                    final_content = ""
                    async for chunk in self._generate_streaming_response(messages, tools_list):
                        final_content += chunk
                        yield chunk
                    
                    # 添加到对话历史
                    if final_content:
                        self.add_message_to_history("assistant", final_content)
                    else:
                        default_msg = "抱歉，我无法理解您的问题，请重新描述。"
                        self.add_message_to_history("assistant", default_msg)
                    
                    # 结束循环
                    break
            
            except Exception as e:
                print(f"[Agent] 处理错误: {str(e)}")
                error_msg = f"抱歉，处理请求时出现错误: {str(e)}"
                async for chunk in self._stream_content(error_msg):
                    yield chunk
                break
        
        if iteration >= max_iterations:
            print(f"[Agent] 达到最大迭代次数，自动清空对话历史并开启新对话")
            # 清空对话历史
            self.clear_history()
            warning_msg = "\n抱歉，工具调用次数过多，对话已重置。请重新描述您的问题。"
            async for chunk in self._stream_content(warning_msg):
                yield chunk
    
    async def _stream_content(self, content: str, chunk_size: int = 10) -> AsyncGenerator[str, None]:
        """模拟流式传输内容
        
        Args:
            content: 要传输的内容
            chunk_size: 每次传输的字符数
            
        Yields:
            文本块
        """
        # 将内容分块传输
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            yield chunk
    
    async def _generate_streaming_response(self, messages: list, tools_list: list) -> AsyncGenerator[str, None]:
        """使用流式API生成响应
        
        Args:
            messages: 消息列表
            tools_list: 工具列表
            
        Yields:
            文本块
        """
        try:
            stream_response = await self.deepseek_service.client.chat.completions.create(
                model=self.deepseek_service.model,
                messages=messages,
                tools=None,  # 最后一次回复不需要工具
                stream=True,
                temperature=0.7,
                max_tokens=2000
            )
            
            async for chunk in stream_response:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content:
                        yield delta.content
        
        except Exception as e:
            print(f"[Agent] 流式生成响应失败: {str(e)}")
            yield f"抱歉，生成回复时出现错误: {str(e)}"
