# 实时更新API实现说明

## 概述

已实现基于 **Server-Sent Events (SSE)** 的实时更新功能，支持任务和课程表的实时数据推送。

---

## 实现的功能

### 1. SSE流式更新接口

**接口路径**: `GET /api/updates/stream`

**功能**:
- 提供实时数据更新推送
- 支持订阅多种数据类型（tasks, courses）
- 自动心跳保持连接
- 自动检测数据库变更

**请求参数**:
- `types` (可选): 订阅的数据类型，多个用逗号分隔，如：`tasks,courses`
- `since` (可选): ISO 8601时间戳，只接收此时间之后的更新

**示例请求**:
```bash
GET /api/updates/stream?types=tasks,courses
Authorization: Bearer <JWT_TOKEN>
Accept: text/event-stream
```

**响应格式** (SSE):
```
data: {"status": "connected", "types": ["tasks", "courses"]}

: heartbeat

data: {"type": "task", "action": "created", "data": {...}, "timestamp": "2025-10-29T10:30:00"}

data: {"type": "task", "action": "updated", "data": {...}, "timestamp": "2025-10-29T10:30:00"}

data: {"type": "task", "action": "deleted", "id": 123, "timestamp": "2025-10-29T10:30:00"}
```

### 2. 自动事件触发

已集成到以下任务操作：
- ✅ **创建任务** (`POST /api/tasks`) - 自动触发 `task.created` 事件
- ✅ **更新任务** (`PUT /api/tasks/{id}`) - 自动触发 `task.updated` 事件
- ✅ **删除任务** (`DELETE /api/tasks/{id}`) - 自动触发 `task.deleted` 事件

### 3. 数据库变更检测

服务会自动检测数据库变更（轮询方式）：
- 每2秒检查一次数据库变更
- 检测最近更新的任务
- 自动区分创建和更新操作

---

## 技术实现

### 1. UpdatesService (`app/services/updates_service.py`)

**核心功能**:
- 连接管理（订阅/取消订阅）
- 事件广播
- 数据库变更检测
- SSE事件流生成

**关键方法**:
- `subscribe(user_id, callback)` - 订阅用户更新
- `broadcast_update(user_id, event)` - 广播更新事件
- `check_changes(db, user_id, types, since)` - 检查数据库变更
- `event_stream(db, user_id, types, since)` - 生成SSE事件流

### 2. Updates Router (`app/routers/updates.py`)

**路由**:
- `GET /api/updates/stream` - SSE流式更新接口
- `POST /api/updates/trigger/{type}` - 手动触发更新（测试用）

---

## 事件格式

### 任务创建事件
```json
{
  "type": "task",
  "action": "created",
  "data": {
    "id": 123,
    "title": "新任务",
    "date": "2025-10-29",
    "priority": "high",
    ...
  },
  "timestamp": "2025-10-29T10:30:00"
}
```

### 任务更新事件
```json
{
  "type": "task",
  "action": "updated",
  "data": {
    "id": 123,
    "title": "更新后的任务",
    ...
  },
  "timestamp": "2025-10-29T10:30:00"
}
```

### 任务删除事件
```json
{
  "type": "task",
  "action": "deleted",
  "id": 123,
  "timestamp": "2025-10-29T10:30:00"
}
```

---

## 前端集成示例

### 使用EventSource连接SSE

```typescript
// 创建EventSource连接
const token = localStorage.getItem('token')
const eventSource = new EventSource(
  `${API_BASE_URL}/updates/stream?types=tasks,courses`,
  {
    withCredentials: true,
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
)

// 监听事件
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data)
  
  if (data.type === 'task') {
    switch (data.action) {
      case 'created':
        // 添加新任务到列表
        addTaskToList(data.data)
        break
      case 'updated':
        // 更新任务
        updateTaskInList(data.data)
        break
      case 'deleted':
        // 删除任务
        removeTaskFromList(data.id)
        break
    }
  }
}

// 处理错误和重连
eventSource.onerror = () => {
  // 重连逻辑
  setTimeout(() => {
    // 重新创建连接
  }, 5000)
}

// 关闭连接
eventSource.close()
```

**注意**: 标准EventSource API不支持自定义请求头，需要使用fetch + ReadableStream或第三方库。

### 使用fetch + ReadableStream（推荐）

```typescript
async function connectSSE() {
  const token = localStorage.getItem('token')
  
  const response = await fetch(
    `${API_BASE_URL}/updates/stream?types=tasks,courses`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'text/event-stream'
      }
    }
  )
  
  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    
    const text = decoder.decode(value)
    const lines = text.split('\n\n')
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6))
        handleUpdate(data)
      } else if (line.startsWith(': ')) {
        // 心跳
        console.log('Heartbeat received')
      }
    }
  }
}
```

---

## 性能考虑

### 1. 连接管理
- 每个用户可以有多个SSE连接
- 服务会自动管理连接的生命周期
- 客户端断开时自动清理

### 2. 数据库轮询
- 轮询间隔：2秒（可配置）
- 检查最近1分钟内的变更（可配置）
- 使用索引字段 (`updated_at`) 提高查询效率

### 3. 心跳机制
- 每30秒发送一次心跳
- 保持连接活跃
- 客户端可用于检测连接状态

---

## 与前端轮询方案的对比

### 轮询方案（当前前端已实现）
- ✅ 实现简单
- ✅ 兼容性好
- ⚠️ 有延迟（最多30秒）
- ⚠️ 可能产生不必要的请求

### SSE方案（后端已实现）
- ✅ 实时性好（2秒内检测到变更）
- ✅ 服务器主动推送
- ✅ 减少不必要的请求
- ⚠️ 需要维护长连接

### 推荐策略
1. **默认使用轮询**（已实现，稳定可靠）
2. **可选切换到SSE**（更实时，但需要维护连接）
3. **前端可以同时使用两种方案**，优先使用SSE，失败时回退到轮询

---

## 测试

### 测试SSE接口

```bash
# 获取Token
TOKEN="your_token_here"

# 连接SSE流
curl -N -H "Authorization: Bearer $TOKEN" \
  "http://127.0.0.1:8000/api/updates/stream?types=tasks"

# 在另一个终端创建任务，应该能看到实时更新
curl -X POST "http://127.0.0.1:8000/api/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "测试任务", "date": "2025-10-29", "priority": "high"}'
```

---

## 后续优化建议

1. **数据库触发器**：使用数据库触发器 + 消息队列（如Redis Pub/Sub）替代轮询
2. **增量更新**：只传输变更的数据而不是完整数据
3. **事件过滤**：支持更细粒度的事件订阅（如只订阅特定日期范围的任务）
4. **WebSocket支持**：如果需要双向通信，可以添加WebSocket支持
5. **连接数限制**：防止单个用户创建过多连接

---

## 总结

✅ **已实现**:
- SSE流式更新接口
- 任务变更自动触发
- 数据库变更检测
- 心跳机制
- 连接管理

📋 **使用方式**:
- 前端可以继续使用轮询（已实现）
- 或者切换到SSE（更实时）
- 或两者结合使用

---

**文档版本**: v1.0.0  
**创建日期**: 2025-10-29

