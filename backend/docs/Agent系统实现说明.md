# Agent系统实现说明

## 概述

已实现一个模块化的智能Agent系统，集成了任务管理、财务管理、课程表查询和智能日程功能。系统使用DeepSeek API作为LLM引擎，支持Function Calling（工具调用）。

---

## 架构设计

### 1. 基础类（Base Classes）

**位置**: `app/services/agent/base.py`

#### BaseTool（工具基类）
- **作用**: 所有工具的统一基类，便于扩展
- **关键方法**:
  - `get_name()` - 返回工具名称
  - `get_description()` - 返回工具描述
  - `get_parameters_schema()` - 返回参数Schema（OpenAI格式）
  - `execute(**kwargs)` - 执行工具逻辑
  - `to_function_definition()` - 转换为OpenAI Function格式

#### BaseAgent（Agent基类）
- **作用**: 所有Agent的统一基类
- **关键功能**:
  - 工具注册和管理
  - 对话历史管理
  - 消息格式转换
  - 工具查找和执行

### 2. 工具模块（Tools）

**位置**: `app/services/agent/tools/`

#### 任务管理工具 (`task_tool.py`)
- `GetTasksTool` - 查询任务列表（支持筛选）
- `CreateTaskTool` - 创建任务
- `UpdateTaskTool` - 更新任务
- `DeleteTaskTool` - 删除任务
- `CompleteTaskTool` - 标记任务完成/未完成

#### 财务管理工具 (`finance_tool.py`)
- `GetTransactionsTool` - 查询交易记录（查账）
- `CreateTransactionTool` - 创建交易记录（记账）
- `DeleteTransactionTool` - 删除交易记录（退款）
- `GetFinanceStatsTool` - 获取财务统计

#### 课程表工具 (`course_tool.py`)
- `GetCoursesTool` - 查询课程表（支持按日期筛选）

#### 智能日程工具 (`schedule_tool.py`)
- `FindFreeTimeTool` - 查询空闲时间段（基于课程表和任务）
- `CreateTaskInFreeTimeTool` - 智能创建任务（自动选择空闲时间）

### 3. Agent主类

**位置**: `app/services/agent/agent.py`

#### TodoAgent
- **继承**: `BaseAgent`
- **功能**: 
  - 注册所有工具
  - 处理用户消息流
  - 支持工具调用和流式响应
  - 对话历史管理

---

## 功能特性

### 1. 任务管理
- ✅ 查询任务（支持日期、完成状态、优先级筛选）
- ✅ 创建任务（支持提醒、时间、优先级）
- ✅ 更新任务
- ✅ 删除任务
- ✅ 标记完成/未完成

### 2. 财务管理
- ✅ 查询交易记录（支持多种筛选）
- ✅ 记账（收入/支出）
- ✅ 退款（删除交易记录）
- ✅ 财务统计（月度收入/支出/结余）

### 3. 课程表查询
- ✅ 获取课程表
- ✅ 按日期筛选课程

### 4. 智能功能
- ✅ 空闲时间查询（结合课程表和任务）
- ✅ 智能任务添加（自动选择空闲时间段）

---

## 使用示例

### 用户对话示例

**1. 创建任务**
```
用户: "帮我创建一个明天下午2点的会议任务"
Agent: [调用 create_task] → 创建成功并回复用户
```

**2. 查询任务**
```
用户: "查看我今天未完成的任务"
Agent: [调用 get_tasks] → 返回任务列表并总结
```

**3. 记账**
```
用户: "记录一笔支出：午餐50元，类别餐饮"
Agent: [调用 create_transaction] → 记账成功
```

**4. 查账**
```
用户: "查看本月的收支情况"
Agent: [调用 get_finance_stats] → 返回统计数据
```

**5. 智能安排**
```
用户: "明天有空的时候帮我安排一个学习任务，需要1小时"
Agent: [调用 find_free_time] → [调用 create_task_in_free_time] → 智能创建任务
```

---

## 技术实现

### 1. Function Calling流程

```
用户消息 → Agent → DeepSeek API（检测是否需要调用工具）
    ↓
如果需要工具调用
    ↓
执行工具 → 获取结果 → 再次调用DeepSeek API（基于工具结果生成回复）
    ↓
流式返回回复给用户
```

### 2. 流式响应
- 使用SSE（Server-Sent Events）实现流式传输
- 支持逐字输出，提供良好的用户体验

### 3. 对话历史
- 维护完整的对话历史（用户消息、助手回复、工具调用、工具结果）
- 支持多轮对话和上下文理解

---

## 扩展指南

### 添加新工具

1. 在 `app/services/agent/tools/` 下创建新工具文件
2. 继承 `BaseTool` 类
3. 实现必需方法：
   ```python
   class MyNewTool(BaseTool):
       def get_name(self) -> str:
           return "my_new_tool"
       
       def get_description(self) -> str:
           return "工具描述"
       
       def get_parameters_schema(self) -> Dict[str, Any]:
           return {
               "type": "object",
               "properties": {
                   "param1": {"type": "string", "description": "参数1"}
               },
               "required": ["param1"]
           }
       
       async def execute(self, param1: str) -> Dict[str, Any]:
           # 实现工具逻辑
           return {"result": "执行结果"}
   ```

4. 在 `TodoAgent.__init__()` 中注册工具：
   ```python
   self.register_tool(MyNewTool(db, user))
   ```

### 创建新的Agent

如果需要不同类型的Agent（例如专门的客服Agent），可以：

1. 创建新类继承 `BaseAgent`
2. 实现 `get_system_prompt()` 方法
3. 注册需要的工具
4. 在路由中使用新Agent

---

## API接口

### 流式聊天接口
**POST** `/api/ai/chat/stream`

**请求**:
```json
{
  "message": "帮我创建一个明天的任务"
}
```

**响应** (SSE格式):
```
data: {"content": "我"}
data: {"content": "来"}
data: {"content": "帮您"}
...
data: [DONE]
```

---

## 注意事项

1. **限流**: Agent继承DeepSeek服务的限流机制（每分钟10次，每日500次）
2. **错误处理**: 所有工具调用都有错误处理和友好提示
3. **数据隔离**: 所有操作都基于当前用户，确保数据安全
4. **扩展性**: 基于统一基类设计，便于后续扩展新功能

---

## 已完成功能清单

- ✅ Agent基础架构（BaseAgent, BaseTool）
- ✅ 任务管理工具（5个）
- ✅ 财务管理工具（4个）
- ✅ 课程表工具（1个）
- ✅ 智能日程工具（2个）
- ✅ 流式响应支持
- ✅ Function Calling集成
- ✅ 对话历史管理
- ✅ 错误处理
- ✅ AI路由集成

---

## 下一步计划

- [ ] 对话历史持久化（数据库存储）
- [ ] 工具调用日志记录
- [ ] 性能优化（工具调用缓存）
- [ ] 更多智能功能（自动提醒、任务推荐等）

