import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id: number
  username: string
  email: string
  status: 'active' | 'inactive'
  role: 'admin' | 'teacher' | 'student'
  createdAt: string
  lastLogin?: string
}

export interface SystemLog {
  id: number
  level: 'info' | 'warning' | 'error'
  message: string
  timestamp: string
  userId?: number
}

export interface SystemSettings {
  maintenanceMode: boolean
  autoBackup: boolean
  emailNotifications: boolean
  maxUsers: number
  sessionTimeout: number
}

export interface SystemStatus {
  cpu: number
  memory: number
  disk: number
  uptime: string
  version: string
}

export const useAdminStore = defineStore('admin', () => {
  // 状态
  const users = ref<User[]>([
    { id: 1, username: 'admin', email: 'admin@example.com', status: 'active', role: 'admin', createdAt: '2025-01-01' },
    { id: 2, username: 'teacher1', email: 'teacher1@example.com', status: 'active', role: 'teacher', createdAt: '2025-01-02' },
    { id: 3, username: 'student1', email: 'student1@example.com', status: 'active', role: 'student', createdAt: '2025-01-03' },
    { id: 4, username: 'student2', email: 'student2@example.com', status: 'inactive', role: 'student', createdAt: '2025-01-04' },
    { id: 5, username: 'teacher2', email: 'teacher2@example.com', status: 'active', role: 'teacher', createdAt: '2025-01-05' }
  ])

  const systemLogs = ref<SystemLog[]>([
    { id: 1, level: 'info', message: '系统启动成功', timestamp: '2025-01-27 10:30:15' },
    { id: 2, level: 'warning', message: 'CPU使用率超过80%', timestamp: '2025-01-27 10:25:42' },
    { id: 3, level: 'error', message: '数据库连接超时', timestamp: '2025-01-27 10:20:18' },
    { id: 4, level: 'info', message: '用户登录成功', timestamp: '2025-01-27 10:15:33', userId: 1 },
    { id: 5, level: 'info', message: '数据备份完成', timestamp: '2025-01-27 10:10:55' }
  ])

  const systemSettings = ref<SystemSettings>({
    maintenanceMode: false,
    autoBackup: true,
    emailNotifications: true,
    maxUsers: 1000,
    sessionTimeout: 30
  })

  const systemStatus = ref<SystemStatus>({
    cpu: 45,
    memory: 67,
    disk: 23,
    uptime: '15天 8小时 32分钟',
    version: 'v1.2.3'
  })

  const stats = ref({
    totalUsers: 1247,
    activeUsers: 892,
    activeCourses: 89,
    pendingTasks: 23,
    systemWarnings: 3
  })

  // 计算属性
  const activeUsers = computed(() => 
    users.value.filter(user => user.status === 'active')
  )

  const adminUsers = computed(() => 
    users.value.filter(user => user.role === 'admin')
  )

  const recentLogs = computed(() => 
    systemLogs.value.slice(0, 10)
  )

  // 方法
  const addUser = (user: Omit<User, 'id'>) => {
    const newId = Math.max(...users.value.map(u => u.id), 0) + 1
    users.value.push({ ...user, id: newId })
  }

  const updateUser = (id: number, updates: Partial<User>) => {
    const index = users.value.findIndex(user => user.id === id)
    if (index > -1) {
      users.value[index] = { ...users.value[index], ...updates }
    }
  }

  const deleteUser = (id: number) => {
    const index = users.value.findIndex(user => user.id === id)
    if (index > -1) {
      users.value.splice(index, 1)
    }
  }

  const toggleUserStatus = (id: number) => {
    const user = users.value.find(u => u.id === id)
    if (user) {
      user.status = user.status === 'active' ? 'inactive' : 'active'
    }
  }

  const addSystemLog = (log: Omit<SystemLog, 'id'>) => {
    const newId = Math.max(...systemLogs.value.map(l => l.id), 0) + 1
    systemLogs.value.unshift({ ...log, id: newId })
  }

  const updateSystemSettings = (settings: Partial<SystemSettings>) => {
    systemSettings.value = { ...systemSettings.value, ...settings }
  }

  const updateSystemStatus = (status: Partial<SystemStatus>) => {
    systemStatus.value = { ...systemStatus.value, ...status }
  }

  const clearSystemLogs = () => {
    systemLogs.value = []
  }

  const exportUserData = () => {
    const dataStr = JSON.stringify(users.value, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `users-${new Date().toISOString().split('T')[0]}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  const refreshStats = () => {
    // 模拟刷新统计数据
    stats.value.totalUsers = users.value.length
    stats.value.activeUsers = activeUsers.value.length
    stats.value.systemWarnings = systemLogs.value.filter(log => log.level === 'warning' || log.level === 'error').length
  }

  return {
    // 状态
    users,
    systemLogs,
    systemSettings,
    systemStatus,
    stats,
    // 计算属性
    activeUsers,
    adminUsers,
    recentLogs,
    // 方法
    addUser,
    updateUser,
    deleteUser,
    toggleUserStatus,
    addSystemLog,
    updateSystemSettings,
    updateSystemStatus,
    clearSystemLogs,
    exportUserData,
    refreshStats
  }
})

