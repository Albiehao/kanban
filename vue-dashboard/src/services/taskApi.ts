// 任务与提醒 API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export interface TaskApiData {
  id: number
  user_id?: number
  title: string
  description?: string
  completed: boolean
  priority: 'high' | 'medium' | 'low'
  date: string
  time?: string
  has_reminder?: boolean
  reminder_time?: string
  created_at?: string
  updated_at?: string
}

// 分页响应格式
export interface TaskListResponse {
  items: TaskApiData[]
  pagination: {
    page: number
    limit: number
    total: number
    total_pages: number
    has_next: boolean
    has_prev: boolean
  }
}

// 获取JWT token
const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token')
}

const request = async <T>(endpoint: string, options: RequestInit = {}): Promise<T> => {
  const token = getAuthToken()
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
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

export const taskApi = {
  // 获取任务列表（支持分页和过滤）
  getTasks: async (params?: {
    page?: number
    limit?: number
    date?: string
    completed?: boolean
    priority?: string
    has_reminder?: boolean
  }): Promise<TaskListResponse> => {
    const queryParams = new URLSearchParams()
    if (params?.page) queryParams.append('page', params.page.toString())
    if (params?.limit) queryParams.append('limit', params.limit.toString())
    if (params?.date) queryParams.append('date', params.date)
    if (params?.completed !== undefined) queryParams.append('completed', params.completed.toString())
    if (params?.priority) queryParams.append('priority', params.priority)
    if (params?.has_reminder !== undefined) queryParams.append('has_reminder', params.has_reminder.toString())
    
    const url = `/tasks${queryParams.toString() ? '?' + queryParams.toString() : ''}`
    console.log('🌐 请求任务API:', url)
    
    const response = await request<any>(url)
    console.log('📦 API原始响应:', JSON.stringify(response, null, 2))
    
    // 从统一格式中提取数据
    let result = response.data || response
    console.log('📋 第一次解析后的数据:', result)
    
    // 检查是否是数组格式（后端直接返回数组）
    if (Array.isArray(result)) {
      console.log('✅ 检测到数组格式，包装成分页格式')
      return {
        items: result,
        pagination: {
          page: 1,
          limit: 100,
          total: result.length,
          total_pages: 1,
          has_next: false,
          has_prev: false
        }
      }
    }
    
    // 检查是否是分页格式 {items: [], pagination: {}}
    if (result && result.items && Array.isArray(result.items)) {
      console.log('✅ 检测到分页格式')
      return result as TaskListResponse
    }
    
    // 如果都不符合，返回空数组
    console.warn('⚠️ 响应格式不符合预期，返回空数组')
    return {
      items: [],
      pagination: {
        page: 1,
        limit: 100,
        total: 0,
        total_pages: 0,
        has_next: false,
        has_prev: false
      }
    }
  },

  // 获取指定日期的任务（简化接口）
  getTasksByDate: async (date: string): Promise<TaskApiData[]> => {
    const response = await taskApi.getTasks({ date, limit: 100 })
    return response.items
  },

  // 添加任务
  addTask: async (task: Omit<TaskApiData, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<TaskApiData> => {
    const response = await request<{ data: TaskApiData }>('/tasks', {
      method: 'POST',
      body: JSON.stringify(task)
    })
    return response.data || response
  },

  // 更新任务
  updateTask: async (id: number, updates: Partial<TaskApiData>): Promise<TaskApiData> => {
    const response = await request<{ data: TaskApiData }>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates)
    })
    return response.data || response
  },

  // 删除任务
  deleteTask: async (id: number): Promise<{ message: string; data: { id: number; title: string } }> => {
    const response = await request<{ message: string; data: { id: number; title: string } }>(`/tasks/${id}`, {
      method: 'DELETE'
    })
    return response.data || response
  },

  // 批量删除任务
  batchDeleteTasks: async (taskIds: number[]): Promise<{ message: string; data: { deleted_count: number; deleted_tasks: Array<{ id: number; title: string }> } }> => {
    const response = await request<{ message: string; data: { deleted_count: number; deleted_tasks: Array<{ id: number; title: string }> } }>('/tasks/batch', {
      method: 'DELETE',
      body: JSON.stringify({ task_ids: taskIds })
    })
    return response.data || response
  },

  // 切换任务完成状态
  toggleTask: async (id: number): Promise<TaskApiData> => {
    const response = await request<{ data: TaskApiData }>(`/tasks/${id}/toggle`, {
      method: 'PATCH'
    })
    return response.data || response
  }
}

