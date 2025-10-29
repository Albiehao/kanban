// 通用类型定义

// 交易记录接口
export interface TransactionApiData {
  id: number
  type: 'income' | 'expense'
  amount: number
  category: string
  description: string
  date: string
}

// 财务统计接口
export interface FinanceStatsApiData {
  monthlyIncome: number
  monthlyExpense: number
  balance: number
  expenseByCategory: Array<{
    category: string
    amount: number
    color: string
  }>
}

// 任务接口
export interface TaskApiData {
  id: number
  title: string
  completed: boolean
  priority: 'high' | 'medium' | 'low'
  date: string
  time?: string  // 时间段，例如 "09:00-11:00"
  hasReminder?: boolean  // 是否有提醒标志
}

// 通知接口
export interface NotificationApiData {
  id: number
  title: string
  message: string
  type: 'info' | 'warning' | 'error' | 'success'
  timestamp: string
  read: boolean
  category: 'system' | 'course' | 'task' | 'user'
  actionUrl?: string
}

// 用户数据接口
export interface UserApiData {
  profile: {
    username: string
    email: string
    bio: string
    avatar: string
    completedTasks: number
    inProgressTasks: number
    daysJoined: number
  }
  preferences: {
    darkMode: boolean
    emailNotifications: boolean
    desktopNotifications: boolean
  }
}

// 管理员数据接口
export interface AdminApiData {
  stats: {
    totalUsers: number
    activeCourses: number
    pendingTasks: number
    systemWarnings: number
  }
  users: Array<{
    id: number
    username: string
    email: string
    status: 'active' | 'inactive'
  }>
  systemSettings: {
    maintenanceMode: boolean
    autoBackup: boolean
    emailNotifications: boolean
  }
  systemStatus: {
    cpu: number
    memory: number
    disk: number
  }
  systemLogs: Array<{
    id: number
    level: 'info' | 'warning' | 'error'
    message: string
    timestamp: string
  }>
}

