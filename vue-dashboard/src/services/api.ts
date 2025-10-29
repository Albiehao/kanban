// API服务层 - 重新导出所有独立的API模块
// 所有数据现在都通过真实后端服务器获取（127.0.0.1:8000）

// 导入并重新导出类型定义
import type { TransactionApiData, FinanceStatsApiData, TaskApiData, NotificationApiData, UserApiData, AdminApiData } from './types'
export type { TransactionApiData, FinanceStatsApiData, TaskApiData, NotificationApiData, UserApiData, AdminApiData }

// 导入所有独立的API模块
import { taskApi } from './taskApi'
import { financeApi } from './financeApi'
import { courseScheduleApi } from './courseScheduleApi'
import { userSettingsApi, type UserSettingsData } from './userSettingsApi'
import { adminManagementApi, type AdminData } from './adminManagementApi'
import { aiAssistantApi } from './aiAssistantApi'
import { eduApi } from './eduApi'

// 重新导出类型
export type { UserSettingsData, AdminData } from './userSettingsApi'

// API基础配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

// HTTP请求工具函数
const request = async <T>(url: string, options: RequestInit = {}): Promise<T> => {
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options
  }

  const response = await fetch(`${API_BASE_URL}${url}`, defaultOptions)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  const data = await response.json()
  return data
}

// 课程相关API - 使用独立的courseScheduleApi
export const courseApi = courseScheduleApi

// 任务相关API - 使用独立的taskApi
export { taskApi }

// 通知相关API
export const notificationApi = {
  // 获取通知数据 - 从后端API获取（支持unread_only参数）
  getNotifications: async (unreadOnly?: boolean): Promise<{data: NotificationApiData[]}> => {
    const url = unreadOnly ? '/notifications?unread_only=true' : '/notifications'
    return request<{data: NotificationApiData[]}>(url)
  },

  // 添加通知
  addNotification: async (notification: Omit<NotificationApiData, 'id'>): Promise<NotificationApiData> => {
    return request<NotificationApiData>('/notifications', {
      method: 'POST',
      body: JSON.stringify(notification)
    })
  },

  // 更新通知
  updateNotification: async (id: number, notification: Partial<NotificationApiData>): Promise<NotificationApiData> => {
    return request<NotificationApiData>(`/notifications/${id}`, {
      method: 'PUT',
      body: JSON.stringify(notification)
    })
  },

  // 删除通知
  deleteNotification: async (id: number): Promise<void> => {
    return request<void>(`/notifications/${id}`, {
      method: 'DELETE'
    })
  },

  // 标记为已读（PUT方法）
  markAsRead: async (id: number): Promise<NotificationApiData> => {
    return request<NotificationApiData>(`/notifications/${id}/read`, {
      method: 'PUT'
    })
  },

  // 标记所有通知为已读
  markAllAsRead: async (): Promise<void> => {
    return request<void>('/notifications/read-all', {
      method: 'PUT'
    })
  }
}

// 财务相关API - 使用独立的financeApi
export { financeApi }

// 用户相关API - 使用独立的userSettingsApi
export const userApi = {
  getUser: async (): Promise<UserSettingsData> => {
    return userSettingsApi.getUserSettings()
  },
  
  updateUser: async (user: Partial<UserSettingsData>): Promise<UserSettingsData> => {
    if (user.profile) {
      return userSettingsApi.updateProfile(user.profile)
    } else if (user.preferences) {
      return userSettingsApi.updatePreferences(user.preferences)
    }
    throw new Error('无效的用户更新数据')
  }
}

// 管理员相关API - 使用独立的adminManagementApi
export const adminApi = {
  getAdminData: () => adminManagementApi.getAdminData(),
  updateAdminData: (data: Partial<AdminData>) => adminManagementApi.getAdminData()
}

// AI助手API - 使用独立的aiAssistantApi
export { aiAssistantApi }

// 教务系统绑定API - 使用独立的eduApi
export { eduApi }

// 不再使用模拟数据API
export const mockApi = {
  getCourses: async () => { throw new Error('请使用真实API') },
  getTasks: async () => { throw new Error('请使用真实API') },
  getTransactions: async () => { throw new Error('请使用真实API') },
  getFinanceStats: async () => { throw new Error('请使用真实API') }
}

// 导出默认API配置
export default {
  courseApi: courseScheduleApi,
  taskApi,
  financeApi,
  userApi,
  notificationApi,
  adminApi,
  aiAssistantApi,
  eduApi,
  mockApi
}
