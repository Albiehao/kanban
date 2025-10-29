# Agent流式传输接口前端调用文档

## 一、接口概述

**接口路径**: `POST /api/ai/chat/stream`  
**接口类型**: Server-Sent Events (SSE)  
**认证方式**: Bearer Token (JWT)  
**功能**: 与AI Agent进行流式对话，支持工具调用（任务管理、财务管理、课程查询等）

---

## 二、请求格式

### 2.1 请求头

```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
Accept: text/event-stream
```

**注意**: 如果使用 `EventSource` API，可能无法设置自定义请求头。可以使用以下方式：
1. 在URL中传递token参数：`/api/ai/chat/stream?token=<JWT_TOKEN>`
2. 使用 `fetch` + `ReadableStream` 的方式（推荐）

### 2.2 请求体

```json
{
  "message": "用户的消息内容"
}
```

**字段说明**:
- `message` (string, 必填): 用户输入的消息，最大长度2000字符

### 2.3 请求示例

**使用 fetch + ReadableStream (推荐)**:

```typescript
async function chatWithAgent(message: string, token: string) {
  const response = await fetch(
    'http://127.0.0.1:8000/api/ai/chat/stream',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify({ message })
    }
  );
  
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  let buffer = '';
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n\n');
    buffer = lines.pop() || ''; // 保留最后一个不完整的行
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6); // 移除 "data: " 前缀
        
        if (data === '[DONE]') {
          // 流式传输结束
          return;
        }
        
        try {
          const parsed = JSON.parse(data);
          
          if (parsed.error) {
            // 错误处理
            console.error('AI错误:', parsed.error);
            onError(parsed.error);
          } else if (parsed.content) {
            // 正常内容
            onContent(parsed.content);
          }
        } catch (e) {
          console.error('解析错误:', e);
        }
      }
    }
  }
}

// 使用示例
chatWithAgent('帮我创建一个明天的任务', token)
  .then(() => console.log('对话完成'))
  .catch(err => console.error('连接错误:', err));
```

**使用 EventSource (不推荐，因为无法设置Authorization头)**:

```typescript
// 注意：EventSource不支持POST和自定义请求头
// 如果后端支持GET + query参数，可以这样使用：
const token = localStorage.getItem('token');
const eventSource = new EventSource(
  `http://127.0.0.1:8000/api/ai/chat/stream?token=${token}&message=${encodeURIComponent(message)}`
);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.content) {
    onContent(data.content);
  }
};

eventSource.onerror = (error) => {
  console.error('SSE错误:', error);
  eventSource.close();
};
```

---

## 三、响应格式

### 3.1 SSE格式

响应使用 **Server-Sent Events (SSE)** 格式：

```
data: {"content": "我"}
data: {"content": "来"}
data: {"content": "帮"}
data: {"content": "您"}
...
data: [DONE]
```

### 3.2 数据格式

**正常内容**:
```json
{
  "content": "文本内容片段"
}
```

**错误信息**:
```json
{
  "error": "错误描述",
  "code": "ERROR_CODE"
}
```

**结束标记**:
```
[DONE]
```

### 3.3 状态码

- `200 OK`: 正常，开始流式传输
- `400 Bad Request`: 请求格式错误（消息为空或过长）
- `401 Unauthorized`: 未授权，需要重新登录
- `429 Too Many Requests`: 请求频率过高，需要等待
- `500 Internal Server Error`: 服务器内部错误

---

## 四、完整调用示例

### 4.1 Vue 3 Composition API 示例

```typescript
import { ref } from 'vue';

export function useAgentChat() {
  const content = ref('');
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  
  async function sendMessage(message: string) {
    isLoading.value = true;
    error.value = null;
    content.value = '';
    
    const token = localStorage.getItem('token');
    if (!token) {
      error.value = '未登录';
      return;
    }
    
    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/ai/chat/stream',
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify({ message })
        }
      );
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            
            if (data === '[DONE]') {
              isLoading.value = false;
              return;
            }
            
            try {
              const parsed = JSON.parse(data);
              
              if (parsed.error) {
                error.value = parsed.error;
                isLoading.value = false;
                return;
              }
              
              if (parsed.content) {
                content.value += parsed.content;
              }
            } catch (e) {
              console.error('解析错误:', e);
            }
          }
        }
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : '连接失败';
    } finally {
      isLoading.value = false;
    }
  }
  
  return {
    content,
    isLoading,
    error,
    sendMessage
  };
}
```

**在组件中使用**:

```vue
<template>
  <div class="chat-container">
    <div class="messages">
      <div v-if="error" class="error">{{ error }}</div>
      <div class="message" v-html="formatContent(content)"></div>
    </div>
    
    <div class="input-area">
      <input 
        v-model="inputMessage" 
        @keyup.enter="handleSend"
        :disabled="isLoading"
        placeholder="输入消息..."
      />
      <button @click="handleSend" :disabled="isLoading || !inputMessage">
        {{ isLoading ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAgentChat } from '@/composables/useAgentChat';

const { content, isLoading, error, sendMessage } = useAgentChat();
const inputMessage = ref('');

function handleSend() {
  if (!inputMessage.value.trim()) return;
  
  const message = inputMessage.value;
  inputMessage.value = '';
  
  sendMessage(message);
}

function formatContent(text: string) {
  // 简单的格式化，支持换行
  return text.replace(/\n/g, '<br>');
}
</script>
```

### 4.2 React Hook 示例

```typescript
import { useState, useCallback } from 'react';

export function useAgentChat() {
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const sendMessage = useCallback(async (message: string) => {
    setIsLoading(true);
    setError(null);
    setContent('');
    
    const token = localStorage.getItem('token');
    if (!token) {
      setError('未登录');
      return;
    }
    
    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/ai/chat/stream',
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify({ message })
        }
      );
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            
            if (data === '[DONE]') {
              setIsLoading(false);
              return;
            }
            
            try {
              const parsed = JSON.parse(data);
              
              if (parsed.error) {
                setError(parsed.error);
                setIsLoading(false);
                return;
              }
              
              if (parsed.content) {
                setContent(prev => prev + parsed.content);
              }
            } catch (e) {
              console.error('解析错误:', e);
            }
          }
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '连接失败');
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  return { content, isLoading, error, sendMessage };
}
```

---

## 五、Agent功能说明

Agent支持以下功能，用户可以通过自然语言与Agent交互：

### 5.1 任务管理
- **创建任务**: "帮我创建一个明天的会议任务"、"创建一个高优先级的任务：完成报告"
- **查询任务**: "查看今天的任务"、"显示未完成的任务"
- **更新任务**: "把任务5标记为完成"、"更新任务3的优先级为高"
- **删除任务**: "删除任务123"

### 5.2 财务管理
- **记账**: "记录一笔支出：午餐50元，类别餐饮"、"记录收入：工资5000元"
- **查账**: "查看本月的收支情况"、"显示今天的支出"
- **退款**: "删除交易记录456"（退款）
- **统计**: "查看本月的财务统计"

### 5.3 课程表查询
- **查询课程**: "查看今天的课程"、"明天的课程安排是什么"
- **注意**: 需要先绑定教务系统API密钥

### 5.4 智能功能
- **查询空闲时间**: "明天什么时候有空"、"查找这周的空闲时间段"
- **智能安排**: "明天有空的时候帮我安排一个学习任务，需要1小时"

### 5.5 时间查询
- **当前时间**: "现在几点了？"、"今天是几号？"

---

## 六、错误处理

### 6.1 常见错误

**401 Unauthorized**:
```javascript
if (response.status === 401) {
  // Token过期或无效，跳转到登录页
  router.push('/login');
}
```

**429 Too Many Requests**:
```javascript
if (response.status === 429) {
  // 请求频率过高，提示用户等待
  error.value = '请求过于频繁，请稍后再试';
}
```

**400 Bad Request**:
```javascript
if (response.status === 400) {
  // 消息为空或过长
  error.value = '消息不能为空且长度不能超过2000字符';
}
```

### 6.2 流式传输中断处理

```typescript
// 添加超时检测
let timeoutId: NodeJS.Timeout | null = null;

function resetTimeout() {
  if (timeoutId) clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    console.warn('流式传输超时');
    reader.cancel();
    error.value = '连接超时，请重试';
  }, 60000); // 60秒超时
}

// 每次收到数据时重置超时
// ... 在接收到数据的地方调用 resetTimeout()
```

---

## 七、性能优化建议

### 7.1 节流处理

如果前端需要频繁更新UI，可以使用节流：

```typescript
import { throttle } from 'lodash-es';

const throttledUpdate = throttle((newContent: string) => {
  content.value = newContent;
}, 50); // 每50ms更新一次

// 在接收数据时
if (parsed.content) {
  throttledUpdate(content.value + parsed.content);
}
```

### 7.2 加载状态

显示加载状态和打字效果：

```vue
<template>
  <div class="message">
    <span v-html="formatContent(content)"></span>
    <span v-if="isLoading" class="typing-indicator">▊</span>
  </div>
</template>

<style>
.typing-indicator {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
</style>
```

---

## 八、注意事项

1. **Token管理**: 
   - Token存储在localStorage或sessionStorage
   - Token过期时自动刷新或跳转登录

2. **连接管理**:
   - 组件卸载时关闭连接
   - 避免同时创建多个连接

3. **错误重试**:
   - 网络错误时自动重试（最多3次）
   - 显示友好的错误提示

4. **内容安全**:
   - 使用 `v-html` 时注意XSS防护
   - 对用户输入的内容进行过滤

5. **跨域问题**:
   - 确保后端CORS配置正确
   - 开发环境可能需要配置代理

---

## 九、完整示例（Vue组件）

```vue
<template>
  <div class="agent-chat">
    <div class="chat-header">
      <h3>AI智能助手</h3>
    </div>
    
    <div class="chat-messages" ref="messagesContainer">
      <div 
        v-for="(msg, index) in messages" 
        :key="index"
        :class="['message', msg.role]"
      >
        <div class="message-content" v-html="formatContent(msg.content)"></div>
        <div v-if="msg.role === 'assistant' && index === messages.length - 1 && isLoading" 
             class="typing-indicator">▊</div>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
    
    <div class="chat-input">
      <textarea
        v-model="inputMessage"
        @keydown.enter.exact.prevent="handleSend"
        @keydown.shift.enter.exact.prevent="inputMessage += '\n'"
        placeholder="输入消息... (Enter发送, Shift+Enter换行)"
        :disabled="isLoading"
        rows="3"
      />
      <button 
        @click="handleSend" 
        :disabled="isLoading || !inputMessage.trim()"
        class="send-button"
      >
        {{ isLoading ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const router = useRouter();
const messages = ref<Message[]>([]);
const inputMessage = ref('');
const isLoading = ref(false);
const error = ref<string | null>(null);
const messagesContainer = ref<HTMLElement>();
let reader: ReadableStreamDefaultReader<Uint8Array> | null = null;

async function sendMessage(message: string) {
  if (!message.trim()) return;
  
  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: message
  });
  
  // 添加空的助手消息占位
  const assistantMessageIndex = messages.value.length;
  messages.value.push({
    role: 'assistant',
    content: ''
  });
  
  isLoading.value = true;
  error.value = null;
  
  const token = localStorage.getItem('token');
  if (!token) {
    router.push('/login');
    return;
  }
  
  try {
    const response = await fetch(
      'http://127.0.0.1:8000/api/ai/chat/stream',
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream'
        },
        body: JSON.stringify({ message })
      }
    );
    
    if (response.status === 401) {
      router.push('/login');
      return;
    }
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    reader = response.body!.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n\n');
      buffer = lines.pop() || '';
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          
          if (data === '[DONE]') {
            isLoading.value = false;
            scrollToBottom();
            return;
          }
          
          try {
            const parsed = JSON.parse(data);
            
            if (parsed.error) {
              error.value = parsed.error;
              messages.value[assistantMessageIndex].content = `错误: ${parsed.error}`;
              isLoading.value = false;
              return;
            }
            
            if (parsed.content) {
              messages.value[assistantMessageIndex].content += parsed.content;
              await nextTick();
              scrollToBottom();
            }
          } catch (e) {
            console.error('解析错误:', e);
          }
        }
      }
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : '连接失败';
    messages.value[assistantMessageIndex].content = `错误: ${error.value}`;
  } finally {
    isLoading.value = false;
    reader = null;
  }
}

function handleSend() {
  if (!inputMessage.value.trim() || isLoading.value) return;
  
  const message = inputMessage.value.trim();
  inputMessage.value = '';
  
  sendMessage(message);
}

function formatContent(text: string): string {
  if (!text) return '';
  // 支持换行、Markdown格式化（简单版）
  return text
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>');
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
}

onUnmounted(() => {
  if (reader) {
    reader.cancel();
  }
});
</script>

<style scoped>
.agent-chat {
  display: flex;
  flex-direction: column;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.chat-header {
  padding: 16px;
  background: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.message {
  margin-bottom: 16px;
}

.message.user {
  text-align: right;
}

.message.user .message-content {
  display: inline-block;
  background: #007bff;
  color: white;
  padding: 8px 12px;
  border-radius: 12px;
  max-width: 70%;
}

.message.assistant .message-content {
  display: inline-block;
  background: #f0f0f0;
  padding: 8px 12px;
  border-radius: 12px;
  max-width: 70%;
}

.typing-indicator {
  display: inline-block;
  animation: blink 1s infinite;
  margin-left: 4px;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.error-message {
  color: red;
  padding: 8px;
  background: #ffe0e0;
  border-radius: 4px;
  margin-top: 8px;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #ddd;
  display: flex;
  gap: 8px;
}

.chat-input textarea {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
}

.send-button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.send-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
```

---

## 十、测试工具

可以使用以下curl命令测试接口：

```bash
curl -N -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -X POST \
  -d '{"message": "你好"}' \
  http://127.0.0.1:8000/api/ai/chat/stream
```

---

**文档版本**: v1.0.0  
**最后更新**: 2025-10-29

