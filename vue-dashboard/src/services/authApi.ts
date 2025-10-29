// 认证API - 使用JWT
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  success: boolean
  token: string
  user: {
    id: number
    username: string
    email: string
    role: 'admin' | 'teacher' | 'student'
    permissions: string[]
  }
  message?: string
}

export interface VerifyTokenResponse {
  valid: boolean
  user?: {
    id: number
    username: string
    email: string
    role: 'admin' | 'teacher' | 'student'
    permissions: string[]
  }
}

// Token管理
export const tokenManager = {
  // 保存token到localStorage
  setToken: (token: string) => {
    localStorage.setItem('auth_token', token)
  },

  // 从localStorage获取token
  getToken: (): string | null => {
    return localStorage.getItem('auth_token')
  },

  // 删除token
  removeToken: () => {
    localStorage.removeItem('auth_token')
  },

  // 检查token是否存在
  hasToken: (): boolean => {
    return !!localStorage.getItem('auth_token')
  }
}

// 请求拦截器：自动添加JWT token
export const requestWithAuth = async <T>(
  endpoint: string, 
  options: RequestInit = {}
): Promise<T> => {
  const token = tokenManager.getToken()
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
    },
    ...options
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, defaultOptions)
    
    // 如果返回401未授权，清除token
    if (response.status === 401) {
      tokenManager.removeToken()
      // 可以触发登出逻辑
      window.dispatchEvent(new CustomEvent('auth:unauthorized'))
    }
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error(`API请求失败 [${endpoint}]:`, error)
    throw error
  }
}

export const authApi = {
  // 登录
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
      })

      // 先读取响应内容以便调试
      const responseText = await response.text()
      console.log('登录API响应:', response.status, responseText)

      if (!response.ok) {
        let errorMessage = '登录失败'
        try {
          const error = JSON.parse(responseText)
          errorMessage = error.message || error.detail || '登录失败'
        } catch {
          errorMessage = responseText || `HTTP ${response.status}`
        }
        throw new Error(errorMessage)
      }

      const data = JSON.parse(responseText)
      
      // 保存token
      if (data.token) {
        tokenManager.setToken(data.token)
      }
      
      return data
    } catch (error: any) {
      console.error('登录API错误:', error)
      throw error
    }
  },

  // 登出
  logout: async (): Promise<void> => {
    try {
      const token = tokenManager.getToken()
      if (token) {
        await fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        })
      }
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      // 无论成功与否，都清除本地token
      tokenManager.removeToken()
    }
  },

  // 验证token
  verifyToken: async (): Promise<VerifyTokenResponse> => {
    const token = tokenManager.getToken()
    
    if (!token) {
      return { valid: false }
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/verify`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        return { valid: true, user: data.user }
      } else {
        return { valid: false }
      }
    } catch (error) {
      console.error('验证token失败:', error)
      return { valid: false }
    }
  },

  // 刷新token
  refreshToken: async (): Promise<string | null> => {
    const token = tokenManager.getToken()
    
    if (!token) {
      throw new Error('没有可用的token')
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        if (data.token) {
          tokenManager.setToken(data.token)
          return data.token
        }
      }
      
      return null
    } catch (error) {
      console.error('刷新token失败:', error)
      return null
    }
  },

  // 注册
  register: async (userData: {
    username: string
    email: string
    password: string
    role?: string
  }): Promise<LoginResponse> => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.message || '注册失败')
    }

    const data = await response.json()
    
    // 保存token
    if (data.token) {
      tokenManager.setToken(data.token)
    }
    
    return data
  }
}

