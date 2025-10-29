import { defineStore } from 'pinia'
import { ref, computed, onMounted } from 'vue'
import { notificationApi } from '@/services/api'

export interface Notification {
  id: number
  title: string
  message: string
  type: 'info' | 'warning' | 'error' | 'success'
  timestamp: string
  read: boolean
  category: 'system' | 'course' | 'task' | 'user'
  actionUrl?: string
}

export const useNotificationStore = defineStore('notifications', () => {
  // 状态
  const notifications = ref<Notification[]>([])

  const showNotifications = ref(false)
  const isLoading = ref(false)

  // 加载通知数据
  const loadNotifications = async (unreadOnly?: boolean) => {
    try {
      isLoading.value = true
      const response = await notificationApi.getNotifications(unreadOnly)
      // 从响应中提取 data 字段
      const data = response.data || []
      notifications.value = data
      console.log('通知数据加载完成:', data.length, '条通知')
    } catch (error) {
      console.error('加载通知数据失败:', error)
      notifications.value = [] // 错误时设置为空数组
    } finally {
      isLoading.value = false
    }
  }

  // 初始化时加载数据
  onMounted(() => {
    loadNotifications()
  })

  // 计算属性
  const unreadCount = computed(() => 
    notifications.value.filter(n => !n.read).length
  )

  const recentNotifications = computed(() => 
    notifications.value.slice(0, 5)
  )

  const unreadNotifications = computed(() => 
    notifications.value.filter(n => !n.read)
  )

  const notificationsByCategory = computed(() => {
    const categories = {
      system: notifications.value.filter(n => n.category === 'system'),
      course: notifications.value.filter(n => n.category === 'course'),
      task: notifications.value.filter(n => n.category === 'task'),
      user: notifications.value.filter(n => n.category === 'user')
    }
    return categories
  })

  // 方法
  const addNotification = (notification: Omit<Notification, 'id'>) => {
    const newId = Math.max(...notifications.value.map(n => n.id), 0) + 1
    notifications.value.unshift({
      ...notification,
      id: newId
    })
  }

  const markAsRead = async (id: number) => {
    try {
      await notificationApi.markAsRead(id)
      const notification = notifications.value.find(n => n.id === id)
      if (notification) {
        notification.read = true
      }
    } catch (error) {
      console.error('标记通知为已读失败:', error)
      // 即使API失败，也更新本地状态
      const notification = notifications.value.find(n => n.id === id)
      if (notification) {
        notification.read = true
      }
    }
  }

  const markAllAsRead = async () => {
    try {
      await notificationApi.markAllAsRead()
      notifications.value.forEach(n => n.read = true)
    } catch (error) {
      console.error('标记所有通知为已读失败:', error)
      // 即使API失败，也更新本地状态
      notifications.value.forEach(n => n.read = true)
    }
  }

  const deleteNotification = (id: number) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const clearAllNotifications = () => {
    notifications.value = []
  }

  const toggleNotifications = () => {
    showNotifications.value = !showNotifications.value
  }

  const closeNotifications = () => {
    showNotifications.value = false
  }

  // 模拟实时通知
  const simulateRealtimeNotification = () => {
    const types: Notification['type'][] = ['info', 'warning', 'success', 'error']
    const categories: Notification['category'][] = ['system', 'course', 'task', 'user']
    const messages = [
      { title: '新消息', message: '您收到了一条新消息' },
      { title: '课程更新', message: '课程内容已更新' },
      { title: '任务完成', message: '任务已完成' },
      { title: '系统通知', message: '系统运行正常' }
    ]

    const randomType = types[Math.floor(Math.random() * types.length)]
    const randomCategory = categories[Math.floor(Math.random() * categories.length)]
    const randomMessage = messages[Math.floor(Math.random() * messages.length)]

    addNotification({
      title: randomMessage.title,
      message: randomMessage.message,
      type: randomType,
      timestamp: new Date().toLocaleString('zh-CN'),
      read: false,
      category: randomCategory
    })
  }

  // 获取通知图标
  const getNotificationIcon = (type: Notification['type']) => {
    switch (type) {
      case 'success':
        return 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
      case 'warning':
        return 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z'
      case 'error':
        return 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z'
      case 'info':
      default:
        return 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
    }
  }

  // 获取通知颜色
  const getNotificationColor = (type: Notification['type']) => {
    switch (type) {
      case 'success':
        return 'text-green-600 bg-green-100'
      case 'warning':
        return 'text-yellow-600 bg-yellow-100'
      case 'error':
        return 'text-red-600 bg-red-100'
      case 'info':
      default:
        return 'text-blue-600 bg-blue-100'
    }
  }

  return {
    // 状态
    notifications,
    showNotifications,
    isLoading,
    // 方法
    loadNotifications,
    // 计算属性
    unreadCount,
    recentNotifications,
    unreadNotifications,
    notificationsByCategory,
    // 方法
    addNotification,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    clearAllNotifications,
    toggleNotifications,
    closeNotifications,
    simulateRealtimeNotification,
    getNotificationIcon,
    getNotificationColor
  }
})

