// 个人设置页 API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export interface UserProfile {
  username: string
  email: string
  bio: string
  avatar: string
  completedTasks: number
  inProgressTasks: number
  daysJoined: number
}

export interface UserPreferences {
  darkMode: boolean
  emailNotifications: boolean
  desktopNotifications: boolean
}

export interface UserSettingsData {
  profile: UserProfile
  preferences: UserPreferences
}

// 获取JWT token
const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token')
}

const request = async <T>(endpoint: string, options: RequestInit = {}): Promise<T> => {
  const token = getAuthToken()
  console.log('API请求:', endpoint, 'Token:', token ? '存在' : '不存在')
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
    },
    ...options
  }

  console.log('请求配置:', {
    url: `${API_BASE_URL}${endpoint}`,
    method: options.method || 'GET',
    headers: defaultOptions.headers
  })

  // 直接请求真实服务器
  const response = await fetch(`${API_BASE_URL}${endpoint}`, defaultOptions)
  
  console.log('API响应状态:', response.status, response.statusText)
  
  if (!response.ok) {
    const errorText = await response.text()
    console.error('API请求失败:', response.status, errorText)
    
    // 尝试解析错误详情
    try {
      const errorJson = JSON.parse(errorText)
      // 如果后端返回了detail字段（FastAPI格式）
      const errorMessage = errorJson.detail || errorJson.message || errorJson.error || `HTTP error! status: ${response.status}`
      throw new Error(errorMessage)
    } catch (parseError) {
      // 如果不是JSON格式，直接抛出文本
      throw new Error(errorText || `HTTP error! status: ${response.status}`)
    }
  }

  const data = await response.json()
  return data
}

export const userSettingsApi = {
  // 获取用户设置（支持新旧路径）
  getUserSettings: async (): Promise<UserSettingsData> => {
    try {
      // 优先使用新路径 /api/user/profile
      return request<UserSettingsData>('/user/profile')
    } catch (error: any) {
      // 如果新路径失败，尝试旧路径 /api/user/settings（向后兼容）
      console.warn('新路径失败，尝试旧路径:', error)
      return request<UserSettingsData>('/user/settings')
    }
  },

  // 更新用户个人资料
  updateProfile: async (profile: Partial<UserProfile>): Promise<UserProfile> => {
    console.log('更新个人资料 - 请求数据:', profile)
    try {
      const result = await request<UserProfile>('/user/profile', {
        method: 'PUT',
        body: JSON.stringify(profile)
      })
      console.log('更新个人资料 - 响应数据:', result)
      return result
    } catch (error: any) {
      console.error('更新个人资料 - 错误详情:', error)
      
      // 尝试获取更详细的错误信息
      if (error.message) {
        // 尝试解析可能的响应体
        throw new Error(error.message)
      }
      throw error
    }
  },

  // 更新用户偏好设置
  updatePreferences: async (preferences: Partial<UserPreferences>): Promise<UserPreferences> => {
    console.log('更新偏好设置 - 请求数据:', preferences)
    const result = await request<UserPreferences>('/user/preferences', {
      method: 'PUT',
      body: JSON.stringify(preferences)
    })
    console.log('更新偏好设置 - 响应数据:', result)
    return result
  },

  // 更新密码（POST方法，向后兼容PUT）
  updatePassword: async (oldPassword: string, newPassword: string): Promise<void> => {
    console.log('修改密码 - 请求数据')
    try {
      // 优先使用POST方法（新API）
      const result = await request<void>('/user/password', {
        method: 'POST',
        body: JSON.stringify({ 
          currentPassword: oldPassword,  // 新API使用currentPassword和newPassword
          newPassword: newPassword
        })
      })
      console.log('修改密码 - 响应数据:', result)
      return result
    } catch (error: any) {
      // 如果POST失败，尝试PUT方法（向后兼容）
      console.warn('POST方法失败，尝试PUT方法:', error)
      try {
        const result = await request<void>('/user/password', {
          method: 'PUT',
          body: JSON.stringify({ 
            old_password: oldPassword,  // 旧API使用old_password和new_password
            new_password: newPassword
          })
        })
        console.log('修改密码 - 响应数据（PUT）:', result)
        return result
      } catch (putError: any) {
        console.error('修改密码 - 错误详情:', putError)
        throw putError
      }
    }
  },

  // 更新个人介绍
  updateBio: async (bio: string): Promise<void> => {
    return request<void>('/user/bio', {
      method: 'PUT',
      body: JSON.stringify({ bio })
    })
  },

  // 更新用户名
  updateUsername: async (username: string): Promise<{username: string, message: string}> => {
    return request<{username: string, message: string}>('/user/username', {
      method: 'PUT',
      body: JSON.stringify({ username })
    })
  },

  // 更新邮箱
  updateEmail: async (email: string): Promise<{email: string, message: string}> => {
    return request<{email: string, message: string}>('/user/email', {
      method: 'PUT',
      body: JSON.stringify({ email })
    })
  },

  // 绑定教务系统API配置
  bindEduAccount: async (params: { apiPath: string; apiKey: string }): Promise<void> => {
    console.log('绑定教务系统API配置 - 请求数据:', params)
    return request<void>('/user/bind-edu', {
      method: 'POST',
      body: JSON.stringify(params)
    })
  },

  // 上传头像
  uploadAvatar: async (file: File): Promise<string> => {
    const formData = new FormData()
    formData.append('avatar', file)
    
    const response = await fetch(`${API_BASE_URL}/user/avatar`, {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    return data.avatarUrl
  }
}

