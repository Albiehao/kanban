// AI智能助手 API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export interface AIMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export interface AIConversation {
  id: number
  messages: AIMessage[]
  title: string
  createdAt: string
  updatedAt: string
}

const request = async <T>(endpoint: string, options: RequestInit = {}): Promise<T> => {
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options
  }

  // 直接请求真实服务器
  const response = await fetch(`${API_BASE_URL}${endpoint}`, defaultOptions)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  const data = await response.json()
  return data
}

export const aiAssistantApi = {
  // 发送消息
  sendMessage: async (message: string, conversationId?: number): Promise<AIMessage> => {
    return request<AIMessage>('/ai/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversationId
      })
    })
  },

  // 获取对话历史
  getConversations: async (): Promise<AIConversation[]> => {
    return request<AIConversation[]>('/ai/conversations')
  },

  // 获取特定对话的消息
  getMessages: async (conversationId: number): Promise<AIMessage[]> => {
    return request<AIMessage[]>(`/ai/conversations/${conversationId}/messages`)
  },

  // 创建新对话
  createConversation: async (title: string): Promise<AIConversation> => {
    return request<AIConversation>('/ai/conversations', {
      method: 'POST',
      body: JSON.stringify({ title })
    })
  },

  // 删除对话
  deleteConversation: async (conversationId: number): Promise<void> => {
    return request<void>(`/ai/conversations/${conversationId}`, {
      method: 'DELETE'
    })
  },

  // 清除对话
  clearConversation: async (conversationId: number): Promise<void> => {
    return request<void>(`/ai/conversations/${conversationId}/clear`, {
      method: 'DELETE'
    })
  }
}

