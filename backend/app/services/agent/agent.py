"""智能Agent主类"""

from typing import Dict, Any, Optional, AsyncGenerator
from sqlalchemy.orm import Session
from app.database import User
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
import json


class TodoAgent(BaseAgent):
    """待办事项智能Agent"""
    
    def __init__(self, db: Session, user: User):
        """初始化Agent"""
        super().__init__(db, user)
        
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
        
        # DeepSeek服务（从数据库读取配置）
        self.deepseek_service = DeepSeekService(db)
    
    def get_system_prompt(self) -> str:
        """返回系统提示词"""
        return """你是一个智能待办事项助手，可以帮助用户：
1. 管理任务：查询、创建、更新、删除任务，设置提醒
2. 管理财务：记账（收入/支出）、查账、退款、查看统计
3. 查询课程表：查看课程安排
4. 智能功能：查询空闲时间，智能安排任务

重要规则：
- 当用户询问课程表、任务、财务数据时，必须调用相应的工具函数获取真实数据
- 绝对不要编造或示例数据
- 如果工具调用失败，如实告诉用户错误信息，不要提供示例数据

工具调用说明：
- 使用get_current_time获取当前日期和时间信息
- 使用get_courses查询课程表（必须调用，不要提供示例）
- 使用get_tasks查询任务
- 使用create_task创建任务
- 使用complete_task标记任务完成
- 使用delete_task删除任务
- 使用get_transactions查询交易记录
- 使用create_transaction记账
- 使用delete_transaction退款
- 使用get_finance_stats查看财务统计
- 使用find_free_time查询空闲时间
- 使用create_task_in_free_time智能安排任务

当用户询问课程安排时：
1. 必须调用get_courses工具获取真实课程数据
2. 如果用户提供了日期，传递给工具的date参数
3. 根据工具返回的真实数据回复用户
4. 如果工具返回错误，如实告知用户错误原因

始终以用户友好、专业的方式回复，用中文与用户交流。"""
    
    async def process_message_stream(
        self,
        user_message: str
    ) -> AsyncGenerator[str, None]:
        """处理用户消息并流式返回响应（支持工具调用）
        
        Args:
            user_message: 用户消息
            
        Yields:
            AI响应文本片段或工具调用结果
        """
        # 添加用户消息到历史
        self.add_message_to_history("user", user_message)
        
        # 构建消息列表（包含对话历史和工具定义）
        messages = self.get_conversation_messages(include_system=True)
        
        # 获取可用函数定义
        functions = self.get_available_functions()
        
        max_iterations = 5  # 最大迭代次数，防止无限循环
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            try:
                # 构建工具定义（OpenAI格式）
                # 注意：tools应该包含完整的工具对象，包括type字段
                tools_list = None
                if functions:
                    # 直接使用完整的工具定义，每个工具已经包含type和function字段
                    tools_list = functions
                
                # 首先检测是否需要调用工具（使用非流式快速检测）
                print(f"[Agent] 调用DeepSeek API检测工具调用, 工具数量: {len(tools_list) if tools_list else 0}")
                
                # 先快速检测是否需要调用工具（只检测，不生成完整回复）
                detect_response = await self.deepseek_service.client.chat.completions.create(
                    model=self.deepseek_service.model,
                    messages=messages,
                    tools=tools_list,
                    tool_choice="auto",
                    stream=False,
                    temperature=0.7,
                    max_tokens=10  # 极少量token，只用于检测工具调用
                )
                
                detect_message = detect_response.choices[0].message
                tool_calls = detect_message.tool_calls if hasattr(detect_message, 'tool_calls') and detect_message.tool_calls else None
                
                print(f"[Agent] 检测结果 - 工具调用数: {len(tool_calls) if tool_calls else 0}")
                
                # 如果有工具调用，执行工具
                if tool_calls:
                    # 执行所有工具调用
                    tool_results = []
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        arguments_str = tool_call.function.arguments
                        
                        # 调试日志
                        print(f"[Agent] 调用工具: {function_name}, 参数: {arguments_str}")
                        
                        try:
                            arguments = json.loads(arguments_str) if arguments_str else {}
                            tool_result = await self.find_and_execute_tool(function_name, arguments)
                            
                            # 调试日志
                            result_str = json.dumps(tool_result, ensure_ascii=False)[:200]  # 截取前200字符
                            print(f"[Agent] 工具 {function_name} 执行结果: {result_str}...")
                            
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(tool_result, ensure_ascii=False)
                            })
                        except json.JSONDecodeError as e:
                            error_msg = f"参数解析失败: {str(e)}"
                            print(f"[Agent] 工具 {function_name} 错误: {error_msg}")
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps({"error": error_msg}, ensure_ascii=False)
                            })
                        except Exception as e:
                            error_msg = f"工具执行失败: {str(e)}"
                            print(f"[Agent] 工具 {function_name} 执行异常: {error_msg}")
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps({"error": error_msg}, ensure_ascii=False)
                            })
                    
                    # 添加助手消息到历史（包含工具调用）
                    # 注意：检测阶段的响应可能没有content，只有tool_calls
                    assistant_msg = {
                        "role": "assistant",
                        "content": None,  # 工具调用时通常没有content
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
                    self.add_message_to_history("assistant", assistant_msg)
                    
                    # 添加工具结果到历史（直接添加字典）
                    for tool_result in tool_results:
                        self.conversation_history.append(tool_result)
                    
                    # 继续对话，让AI基于工具结果生成流式回复
                    messages = self.get_conversation_messages(include_system=True)
                    # 添加工具结果消息到对话历史（ensure_ascii=False用于中文）
                    for tool_result in tool_results:
                        messages.append(tool_result)
                    
                    # 使用流式模式生成最终回复
                    try:
                        stream_response = await self.deepseek_service.client.chat.completions.create(
                            model=self.deepseek_service.model,
                            messages=messages,
                            tools=tools_list,
                            tool_choice="none",  # 这次不再调用工具，只生成回复
                            stream=True,  # 使用流式模式
                            temperature=0.7,
                            max_tokens=2000
                        )
                        
                        # 流式返回内容
                        final_content = ""
                        async for chunk in stream_response:
                            if chunk.choices and len(chunk.choices) > 0:
                                delta = chunk.choices[0].delta
                                if hasattr(delta, 'content') and delta.content:
                                    content = delta.content
                                    final_content += content
                                    yield content
                        
                        # 添加到历史
                        if final_content:
                            self.add_message_to_history("assistant", final_content)
                        
                        # 流式传输完成
                        break
                    except Exception as e:
                        error_msg = f"生成回复失败: {str(e)}"
                        print(f"[Agent] {error_msg}")
                        yield error_msg
                        break
                
                # 没有工具调用，直接使用流式模式生成并返回回复
                # 使用流式API生成完整回复
                try:
                    stream_response = await self.deepseek_service.client.chat.completions.create(
                        model=self.deepseek_service.model,
                        messages=messages,
                        tools=tools_list,
                        tool_choice="none",  # 不调用工具
                        stream=True,  # 使用流式模式
                        temperature=0.7,
                        max_tokens=2000
                    )
                    
                    # 流式返回内容
                    final_content = ""
                    async for chunk in stream_response:
                        if chunk.choices and len(chunk.choices) > 0:
                            delta = chunk.choices[0].delta
                            if hasattr(delta, 'content') and delta.content:
                                content = delta.content
                                final_content += content
                                yield content
                    
                    # 添加到历史
                    if final_content:
                        self.add_message_to_history("assistant", final_content)
                    
                    # 流式传输完成
                    break
                except Exception as e:
                    error_msg = f"生成流式回复失败: {str(e)}"
                    print(f"[Agent] {error_msg}")
                    yield error_msg
                    break
                
            except Exception as e:
                error_msg = f"处理错误: {str(e)}"
                yield error_msg
                break

