<template>
  <div class="relative">
    <!-- 通知按钮 -->
    <button 
      @click="toggleNotifications"
      class="p-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-800 rounded relative transition-colors"
    >
      <Bell class="h-5 w-5" />
      <!-- 未读通知数量提示 -->
      <span 
        v-if="notificationStore.unreadCount > 0"
        class="absolute -top-1 -right-1 h-5 w-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center font-medium"
      >
        {{ notificationStore.unreadCount > 99 ? '99+' : notificationStore.unreadCount }}
      </span>
    </button>

    <!-- 通知下拉面板 -->
    <div 
      v-if="notificationStore.showNotifications"
      class="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50 max-h-96 overflow-hidden"
    >
      <!-- 通知头部 -->
      <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-200">通知中心</h3>
          <div class="flex items-center gap-2">
            <span class="text-xs text-gray-500 dark:text-gray-400">
              {{ notificationStore.unreadCount }} 条未读
            </span>
            <Button 
              v-if="notificationStore.unreadCount > 0"
              variant="ghost" 
              size="sm" 
              @click="markAllAsRead"
              class="text-xs h-6 px-2"
            >
              全部已读
            </Button>
          </div>
        </div>
      </div>

      <!-- 通知列表 -->
      <div class="max-h-80 overflow-y-auto">
        <div v-if="notificationStore.notifications.length === 0" class="p-4 text-center text-gray-500 dark:text-gray-400 text-sm">
          暂无通知
        </div>
        
        <div v-else>
          <div 
            v-for="notification in notificationStore.recentNotifications" 
            :key="notification.id"
            :class="[
              'px-4 py-3 border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors',
              !notification.read ? 'bg-blue-50 dark:bg-blue-900/30' : ''
            ]"
            @click="handleNotificationClick(notification)"
          >
            <div class="flex items-start gap-3">
              <!-- 通知图标 -->
              <div :class="[
                'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                notificationStore.getNotificationColor(notification.type)
              ]">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="notificationStore.getNotificationIcon(notification.type)"></path>
                </svg>
              </div>

              <!-- 通知内容 -->
              <div class="flex-1 min-w-0">
                <div class="flex items-start justify-between gap-2">
                  <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                    {{ notification.title }}
                  </h4>
                  <div class="flex items-center gap-2 flex-shrink-0">
                    <!-- 未读标识 -->
                    <div 
                      v-if="!notification.read"
                      class="w-2 h-2 bg-blue-500 rounded-full"
                    ></div>
                    <!-- 删除按钮 -->
                    <button 
                      @click.stop="deleteNotification(notification.id)"
                      class="text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 transition-colors"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                      </svg>
                    </button>
                  </div>
                </div>
                
                <p class="text-xs text-gray-600 dark:text-gray-300 mt-1 line-clamp-2">
                  {{ notification.message }}
                </p>
                
                <div class="flex items-center justify-between mt-2">
                  <span class="text-xs text-gray-500 dark:text-gray-400">
                    {{ formatTime(notification.timestamp) }}
                  </span>
                  <span :class="[
                    'text-xs px-2 py-1 rounded-full',
                    getCategoryColor(notification.category)
                  ]">
                    {{ getCategoryName(notification.category) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 通知底部 -->
      <div class="px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
        <div class="flex items-center justify-between">
          <Button 
            variant="outline" 
            size="sm" 
            @click="clearAllNotifications"
            class="text-xs h-7"
          >
            清空所有
          </Button>
        </div>
      </div>
    </div>

    <!-- 点击外部关闭 -->
    <div 
      v-if="notificationStore.showNotifications"
      class="fixed inset-0 z-40"
      @click="closeNotifications"
      ></div>
    
    <!-- 消息提示弹框 -->
    <MessageModal
      v-model:visible="showMessageModal"
      :type="messageModalType"
      :title="messageModalTitle"
      :message="messageModalMessage"
      :show-cancel="messageModalShowCancel"
      :confirm-text="messageModalConfirmText"
      :cancel-text="messageModalCancelText"
      @confirm="handleMessageConfirm"
      @cancel="handleMessageCancel"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Bell } from 'lucide-vue-next'
import Button from '@/components/ui/Button.vue'
import MessageModal from '@/components/ui/MessageModal.vue'
import { useNotificationStore, type Notification } from '@/stores/notifications'

const notificationStore = useNotificationStore()

// 消息弹框状态
const showMessageModal = ref(false)
const messageModalType = ref<'success' | 'error' | 'warning' | 'info'>('warning')
const messageModalTitle = ref('确认')
const messageModalMessage = ref('')
const messageModalShowCancel = ref(true)
const messageModalConfirmText = ref('确定')
const messageModalCancelText = ref('取消')

let pendingAction: (() => void) | null = null

const showMessage = (
  type: 'success' | 'error' | 'warning' | 'info',
  title: string,
  message: string,
  showCancel = false,
  confirmText = '确定',
  cancelText = '取消'
) => {
  messageModalType.value = type
  messageModalTitle.value = title
  messageModalMessage.value = message
  messageModalShowCancel.value = showCancel
  messageModalConfirmText.value = confirmText
  messageModalCancelText.value = cancelText
  showMessageModal.value = true
}

const handleMessageConfirm = () => {
  if (pendingAction) {
    pendingAction()
    pendingAction = null
  }
}

const handleMessageCancel = () => {
  pendingAction = null
}

// 方法
const toggleNotifications = () => {
  notificationStore.toggleNotifications()
}

const closeNotifications = () => {
  notificationStore.closeNotifications()
}

const markAllAsRead = () => {
  notificationStore.markAllAsRead()
}

const deleteNotification = (id: number) => {
  notificationStore.deleteNotification(id)
}

const clearAllNotifications = () => {
  showMessage('warning', '确认清空', '确定要清空所有通知吗？', true, '清空', '取消')
  pendingAction = () => {
    notificationStore.clearAllNotifications()
  }
}

const handleNotificationClick = (notification: Notification) => {
  // 标记为已读
  notificationStore.markAsRead(notification.id)
  
  // 如果有操作链接，跳转到对应页面
  if (notification.actionUrl) {
    // 这里可以使用 router.push(notification.actionUrl)
    console.log('跳转到:', notification.actionUrl)
  }
  
  // 关闭通知面板
  notificationStore.closeNotifications()
}

const formatTime = (timestamp: string) => {
  const now = new Date()
  const time = new Date(timestamp)
  const diff = now.getTime() - time.getTime()
  
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  
  return time.toLocaleDateString('zh-CN')
}

const getCategoryName = (category: string) => {
  const names = {
    system: '系统',
    course: '课程',
    task: '任务',
    user: '用户'
  }
  return names[category as keyof typeof names] || category
}

const getCategoryColor = (category: string) => {
  const colors = {
    system: 'bg-gray-100 text-gray-700',
    course: 'bg-blue-100 text-blue-700',
    task: 'bg-green-100 text-green-700',
    user: 'bg-purple-100 text-purple-700'
  }
  return colors[category as keyof typeof colors] || 'bg-gray-100 text-gray-700'
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

