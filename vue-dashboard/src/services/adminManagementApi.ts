// 管理员 API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export interface AdminStats {
  totalUsers: number
  activeCourses: number
  pendingTasks: number
  systemWarnings: number
}

export interface AdminUser {
  id: number
  username: string
  email: string
  status: 'active' | 'inactive'
}

export interface SystemSettings {
  maintenanceMode: boolean
  autoBackup: boolean
  emailNotifications: boolean
}

export interface SystemStatus {
  cpu: number
  memory: number
  disk: number
}

export interface SystemLog {
  id: number
  level: 'info' | 'warning' | 'error'
  message: string
  module?: string
  user_id?: number | null
  timestamp: string
}

export interface AdminData {
  stats: AdminStats
  users: AdminUser[]
  systemSettings: SystemSettings
  systemStatus: SystemStatus
  systemLogs: SystemLog[]
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

export const adminManagementApi = {
  // 获取所有管理员数据
  getAdminData: async (): Promise<AdminData> => {
    return request<AdminData>('/admin/data')
  },

  // 获取统计数据
  getStats: async (): Promise<AdminStats> => {
    return request<AdminStats>('/admin/stats')
  },

  // 获取用户列表
  getUsers: async (): Promise<AdminUser[]> => {
    const response = await request<{ data: Array<{
      id: number
      username: string
      email: string
      role: string
      is_active: boolean
      bio?: string | null
      avatar_url?: string | null
      created_at: string
      updated_at: string
    }> }>('/admin/users')
    // 映射后端数据格式到前端格式
    return (response.data || []).map(user => ({
      id: user.id,
      username: user.username,
      email: user.email,
      status: user.is_active ? 'active' : 'inactive' as 'active' | 'inactive'
    }))
  },

  // 获取系统设置
  getSystemSettings: async (): Promise<SystemSettings> => {
    return request<SystemSettings>('/admin/settings')
  },

  // 更新系统设置
  updateSystemSettings: async (settings: Partial<SystemSettings>): Promise<SystemSettings> => {
    return request<SystemSettings>('/admin/settings', {
      method: 'PUT',
      body: JSON.stringify(settings)
    })
  },

  // 获取系统状态（旧接口，保留兼容性）
  getSystemStatus: async (): Promise<SystemStatus> => {
    // 从服务器信息中提取数据
    const serverInfo = await adminManagementApi.getServerInfo()
    return {
      cpu: serverInfo.resources.cpu.usage_percent,
      memory: serverInfo.resources.memory.usage_percent,
      disk: serverInfo.resources.disk.usage_percent
    }
  },

  // 获取服务器信息（新接口）
  getServerInfo: async (): Promise<{
    platform: {
      system: string
      platform: string
      machine: string
      processor: string
      python_version: string
    }
    resources: {
      cpu: {
        count: number
        usage_percent: number
        frequency_mhz: number
        max_frequency_mhz: number
      }
      memory: {
        total_gb: number
        used_gb: number
        available_gb: number
        usage_percent: number
      }
      disk: {
        total_gb: number
        used_gb: number
        free_gb: number
        usage_percent: number
      }
      uptime: {
        days: number
        hours: number
        minutes: number
        formatted: string
      }
      boot_time: string
    }
    network: {
      bytes_sent_gb: number
      bytes_recv_gb: number
      packets_sent: number
      packets_recv: number
    }
    application: {
      python_version: string
      working_directory: string
      server_time: string
    }
  }> => {
    const response = await request<{ data: any }>('/admin/server/info')
    return response.data || response
  },

  // 获取系统日志
  getSystemLogs: async (options?: { level?: string; limit?: number; offset?: number }): Promise<SystemLog[]> => {
    let url = '/admin/logs'
    const params = new URLSearchParams()
    
    if (options?.level) params.append('level', options.level)
    if (options?.limit) params.append('limit', options.limit.toString())
    if (options?.offset) params.append('offset', options.offset.toString())
    
    if (params.toString()) {
      url += '?' + params.toString()
    }
    
    return request<SystemLog[]>(url)
  },

  // 创建系统日志
  createSystemLog: async (log: { level: 'info' | 'warning' | 'error'; message: string }): Promise<SystemLog> => {
    return request<SystemLog>('/admin/logs', {
      method: 'POST',
      body: JSON.stringify(log)
    })
  },

  // 删除单条日志
  deleteSystemLog: async (logId: number): Promise<void> => {
    return request<void>(`/admin/logs/${logId}`, {
      method: 'DELETE'
    })
  },

  // 清空所有日志
  clearSystemLogs: async (level?: string): Promise<void> => {
    const options: RequestInit = { method: 'DELETE' }
    
    if (level) {
      options.body = JSON.stringify({ level })
    }
    
    return request<void>('/admin/logs', options)
  },

  // 更新用户状态
  updateUserStatus: async (userId: number, status: 'active' | 'inactive'): Promise<AdminUser> => {
    return request<AdminUser>(`/admin/users/${userId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status })
    })
  },

  // 编辑用户
  updateUser: async (userId: number, updates: Partial<AdminUser>): Promise<AdminUser> => {
    return request<AdminUser>(`/admin/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(updates)
    })
  },

  // 删除用户
  deleteUser: async (userId: number): Promise<void> => {
    return request<void>(`/admin/users/${userId}`, {
      method: 'DELETE'
    })
  },

  // ========== DeepSeek 配置管理 ==========
  
  // DeepSeek 配置接口类型
  getDeepSeekConfigs: async (includeInactive?: boolean): Promise<{
    count: number
    configs: DeepSeekConfig[]
  }> => {
    const url = includeInactive 
      ? '/admin/deepseek/configs?include_inactive=true'
      : '/admin/deepseek/configs'
    return request<{ count: number; configs: DeepSeekConfig[] }>(url)
  },

  // 获取单个配置
  getDeepSeekConfig: async (configId?: number): Promise<DeepSeekConfig> => {
    const url = configId
      ? `/admin/deepseek/config?config_id=${configId}`
      : '/admin/deepseek/config'
    return request<DeepSeekConfig>(url)
  },

  // 创建配置
  createDeepSeekConfig: async (config: Omit<DeepSeekConfig, 'id' | 'created_at' | 'updated_at'>): Promise<DeepSeekConfig> => {
    return request<DeepSeekConfig>('/admin/deepseek/config', {
      method: 'POST',
      body: JSON.stringify(config)
    })
  },

  // 更新配置
  updateDeepSeekConfig: async (configId: number, config: Partial<Omit<DeepSeekConfig, 'id' | 'created_at' | 'updated_at'>>): Promise<DeepSeekConfig> => {
    return request<DeepSeekConfig>(`/admin/deepseek/config/${configId}`, {
      method: 'PUT',
      body: JSON.stringify(config)
    })
  },

  // 删除配置
  deleteDeepSeekConfig: async (configId: number): Promise<void> => {
    return request<void>(`/admin/deepseek/config/${configId}`, {
      method: 'DELETE'
    })
  },

  // 切换配置状态
  toggleDeepSeekConfig: async (configId: number): Promise<DeepSeekConfig> => {
    return request<DeepSeekConfig>(`/admin/deepseek/config/${configId}/toggle`, {
      method: 'POST'
    })
  }
}

// DeepSeek 配置类型定义
export interface DeepSeekConfig {
  id: number
  api_key: string
  base_url: string
  model: string
  is_active: boolean
  rate_limit_per_minute: number
  rate_limit_per_day: number
  created_at: string
  updated_at: string
}

