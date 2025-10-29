// 教务系统绑定 API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export interface EduBindingStatus {
  is_bound: boolean
  edu_username?: string
  is_active?: boolean
  last_sync?: string
}

export interface EduBindingRequest {
  edu_username: string
  edu_password: string
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

  const response = await fetch(`${API_BASE_URL}${endpoint}`, defaultOptions)
  
  if (!response.ok) {
    const errorText = await response.text()
    try {
      const errorJson = JSON.parse(errorText)
      const errorMessage = errorJson.detail || errorJson.message || errorJson.error || `HTTP error! status: ${response.status}`
      throw new Error(errorMessage)
    } catch (parseError) {
      throw new Error(errorText || `HTTP error! status: ${response.status}`)
    }
  }

  const data = await response.json()
  return data
}

export const eduApi = {
  // 绑定教务系统账号（新API路径）
  bindAccount: async (requestData: EduBindingRequest): Promise<{ success: boolean; message: string }> => {
    try {
      // 优先使用新路径 /api/edu/bind
      return request<{ success: boolean; message: string }>('/edu/bind', {
        method: 'POST',
        body: JSON.stringify(requestData)
      })
    } catch (error: any) {
      // 如果新路径失败，尝试旧路径 /api/user/bind-edu（向后兼容）
      console.warn('新路径失败，尝试旧路径:', error)
      return request<{ success: boolean; message: string }>('/user/bind-edu', {
        method: 'POST',
        body: JSON.stringify(requestData)
      })
    }
  },

  // 获取绑定状态（新API路径）
  getBindingStatus: async (): Promise<EduBindingStatus> => {
    try {
      // 优先使用新路径 /api/edu/bind/status
      const response = await request<{ data: EduBindingStatus } | EduBindingStatus>('/edu/bind/status')
      return 'data' in response ? response.data : response
    } catch (error: any) {
      // 如果新路径失败，尝试旧路径 /api/user/bind-edu（向后兼容）
      console.warn('新路径失败，尝试旧路径:', error)
      const response = await request<{ data: EduBindingStatus } | EduBindingStatus>('/user/bind-edu')
      return 'data' in response ? response.data : response
    }
  },

  // 更新绑定信息（新API路径）
  updateBinding: async (requestData: EduBindingRequest): Promise<{ success: boolean; message: string }> => {
    return request<{ success: boolean; message: string }>('/edu/bind', {
      method: 'PUT',
      body: JSON.stringify(requestData)
    })
  },

  // 取消绑定（新API路径）
  unbindAccount: async (): Promise<{ success: boolean; message: string }> => {
    return request<{ success: boolean; message: string }>('/edu/bind', {
      method: 'DELETE'
    })
  }
}

