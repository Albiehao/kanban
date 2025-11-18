// AI智能助手 API
import { requestWithAuth as request } from './authApi'

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

