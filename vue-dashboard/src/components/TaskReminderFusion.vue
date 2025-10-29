<template>
  <Card class="task-reminder-container">
    <CardHeader>
      <div class="flex items-center justify-between">
        <CardTitle class="text-base">{{ formatDateShort(selectedDate) }} 任务与提醒</CardTitle>
        <div class="flex gap-1">
          <Button 
            variant="outline"
            size="sm" 
            class="h-7 text-xs" 
            @click="refreshTasks"
            :disabled="isRefreshing"
          >
            <RefreshCw :class="['h-3 w-3 mr-1', isRefreshing && 'animate-spin']" />
            <span v-if="!isRefreshing">刷新</span>
          </Button>
          <Button size="sm" class="h-7 text-xs" @click="showAddTaskModal = true">
            <Plus class="h-3 w-3 mr-1" />
            添加任务
          </Button>
        </div>
      </div>
    </CardHeader>

    <!-- 添加任务模态框 -->
    <AddTaskModal 
      :is-open="showAddTaskModal"
      :default-date="selectedDateStr"
      @close="showAddTaskModal = false"
      @submit="handleAddTask"
    />

    <!-- 自定义消息模态框 -->
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

    <!-- 任务详情模态框 -->
    <Transition name="modal-fade">
      <div 
        v-if="showTaskDetailsModal && selectedTaskDetail"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 dark:bg-black/70"
        @click="closeTaskDetail"
      >
        <Transition name="modal-scale">
          <div 
            v-if="showTaskDetailsModal && selectedTaskDetail"
            class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-4 p-6 modal-content"
            @click.stop
          >
              <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-foreground">{{ isReminder ? '提醒详情' : '任务详情' }}</h3>
              <div class="flex items-center gap-2">
                <button 
                  v-if="!isEditMode"
                  @click="handleDeleteTask"
                  class="px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20 rounded-md transition-colors"
                >
                  <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  删除
                </button>
                <button 
                  v-if="!isReminder && !isEditMode"
                  @click="toggleEditMode"
                  class="px-3 py-1.5 text-sm text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/20 rounded-md transition-colors"
                >
                  <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  编辑
                </button>
                <button 
                  v-if="isEditMode"
                  @click="cancelEdit"
                  class="px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50 dark:text-gray-400 dark:hover:bg-gray-900/20 rounded-md transition-colors"
                >
                  取消
                </button>
                <button 
                  @click="closeTaskDetail"
                  class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            <Transition name="edit-fade" mode="out-in">
              <div v-if="!isEditMode" key="view" class="space-y-4">
                <div>
                <span class="text-sm text-muted-foreground">任务名称</span>
                <p class="text-base font-medium text-foreground mt-1">{{ selectedTaskDetail.title }}</p>
              </div>
              
              <div>
                <span class="text-sm text-muted-foreground">日期</span>
                <p class="text-base text-foreground mt-1">{{ selectedTaskDetail.date }}</p>
              </div>
              
              <div v-if="selectedTaskDetail.time">
                <span class="text-sm text-muted-foreground">时间段</span>
                <p class="text-base text-foreground mt-1">{{ selectedTaskDetail.time }}</p>
              </div>
              
              <div>
                <span class="text-sm text-muted-foreground">优先级</span>
                <p class="text-base text-foreground mt-1">
                  <span :class="cn(
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    selectedTaskDetail.priority === 'high' 
                      ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                      : selectedTaskDetail.priority === 'medium'
                      ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                      : 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                  )">
                    {{ selectedTaskDetail.priority === 'high' ? '高' : selectedTaskDetail.priority === 'medium' ? '中' : '低' }}
                  </span>
                </p>
              </div>
              
              <div>
                <span class="text-sm text-muted-foreground">完成状态</span>
                <p class="text-base text-foreground mt-1">
                  <span :class="cn(
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    selectedTaskDetail.completed
                      ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                      : 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
                  )">
                    {{ selectedTaskDetail.completed ? '已完成' : '未完成' }}
                  </span>
                </p>
              </div>
              
              <div v-if="selectedTaskDetail.hasReminder">
                <span class="text-sm text-muted-foreground">提醒设置</span>
                <p class="text-base text-foreground mt-1">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
                    已设置提醒
                  </span>
                </p>
              </div>
            </div>
            
            <div v-else key="edit" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-foreground mb-2">任务名称</label>
                <input
                  v-model="editTaskData.title"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-foreground mb-2">日期</label>
                <input
                  v-model="editTaskData.date"
                  type="date"
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-foreground mb-2">时间段 (可选)</label>
                <div class="flex gap-2">
                  <input
                    v-model="editTaskData.startTime"
                    type="time"
                    class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                  <span class="self-center text-gray-500">至</span>
                  <input
                    v-model="editTaskData.endTime"
                    type="time"
                    class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-foreground mb-2">优先级</label>
                <div class="flex gap-2">
                  <button
                    type="button"
                    :class="cn(
                      'flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                      editTaskData.priority === 'high' 
                        ? 'bg-red-500 text-white' 
                        : 'bg-gray-100 dark:bg-gray-700 text-foreground hover:bg-gray-200 dark:hover:bg-gray-600'
                    )"
                    @click="editTaskData.priority = 'high'"
                  >
                    高
                  </button>
                  <button
                    type="button"
                    :class="cn(
                      'flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                      editTaskData.priority === 'medium' 
                        ? 'bg-yellow-500 text-white' 
                        : 'bg-gray-100 dark:bg-gray-700 text-foreground hover:bg-gray-200 dark:hover:bg-gray-600'
                    )"
                    @click="editTaskData.priority = 'medium'"
                  >
                    中
                  </button>
                  <button
                    type="button"
                    :class="cn(
                      'flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                      editTaskData.priority === 'low' 
                        ? 'bg-green-500 text-white' 
                        : 'bg-gray-100 dark:bg-gray-700 text-foreground hover:bg-gray-200 dark:hover:bg-gray-600'
                    )"
                    @click="editTaskData.priority = 'low'"
                  >
                    低
                  </button>
                </div>
              </div>

              <div class="space-y-2">
                <div class="flex items-center gap-2">
                  <input
                    v-model="editTaskData.hasReminder"
                    type="checkbox"
                    id="editHasReminder"
                    class="w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary"
                  />
                  <label for="editHasReminder" class="text-sm text-foreground cursor-pointer">
                    添加提醒
                  </label>
                </div>
                
                <!-- 提醒时间 -->
                <div v-if="editTaskData.hasReminder" class="ml-6">
                  <label class="block text-sm font-medium text-foreground mb-2">提醒时间</label>
                  <input
                    v-model="editTaskData.reminderTime"
                    type="datetime-local"
                    :min="currentDateTime"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>
              </div>

              <!-- 保存和取消按钮 -->
              <div class="flex gap-2 pt-2">
                <button
                  type="button"
                  @click="cancelEdit"
                  class="flex-1 px-4 py-2 bg-gray-100 dark:bg-gray-700 text-foreground rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                >
                  取消
                </button>
                <button
                  type="button"
                  @click="saveEdit"
                  class="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                >
                  保存
                </button>
        </div>
      </div>
            </Transition>
          </div>
        </Transition>
      </div>
    </Transition>

    <CardContent class="p-0">
      <div class="task-reminder-scroll-container">
        <div class="grid grid-cols-2 gap-0 h-full">
          <!-- 左侧：任务部分 -->
          <div class="p-2 border-r border-gray-200">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-2 h-2 rounded-full bg-blue-500"></div>
              <span class="text-xs font-medium text-gray-700">任务</span>
              <span class="text-xs text-gray-500">({{ filteredTasks.length }})</span>
            </div>
            
            <div v-if="filteredTasks.length === 0" class="text-center py-2 text-muted-foreground text-xs">
              暂无任务
            </div>
            <div v-else class="space-y-1">
              <div
                v-for="task in filteredTasks"
                :key="task.id"
                :class="cn(
                  'flex items-start gap-1.5 p-1.5 rounded-lg transition-colors cursor-pointer',
                  'hover:bg-muted/50',
                  task.completed && 'opacity-60'
                )"
                @click="showTaskDetail(task)"
              >
                <div @click.stop>
                <Checkbox 
                  :checked="task.completed" 
                  @update:checked="store.toggleTask(task.id)"
                  class="mt-0.5"
                />
                </div>
                <div class="flex-1 min-w-0">
                  <p :class="cn(
                    'text-xs font-medium',
                    task.completed && 'line-through text-muted-foreground'
                  )">
                    {{ task.title }}
                  </p>
                  <div class="flex items-center gap-2 mt-0.5">
                    <Flag :class="cn('h-2.5 w-2.5', priorityColors[task.priority])" />
                    <span :class="cn('text-xs', priorityColors[task.priority])">
                      {{ task.priority === 'high' ? '高' : task.priority === 'medium' ? '中' : '低' }}
                    </span>
                    <span v-if="task.time" class="text-xs text-muted-foreground">
                      {{ task.time }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 右侧：提醒部分 -->
          <div class="p-2">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-2 h-2 rounded-full bg-orange-500"></div>
              <span class="text-xs font-medium text-gray-700">提醒</span>
              <span class="text-xs text-gray-500">({{ reminders.length }})</span>
            </div>
            
            <div v-if="reminders.length === 0" class="text-center py-2 text-muted-foreground text-xs">
              暂无提醒
            </div>
            <div v-else class="space-y-1">
              <div
                v-for="reminder in reminders"
                :key="reminder.id"
                class="flex items-start gap-1.5 p-1.5 rounded-lg bg-muted/50 hover:bg-muted transition-colors cursor-pointer"
                @click="showTaskDetail(findTaskById(reminder.id), true)"
              >
                <div :class="`w-1.5 h-1.5 rounded-full mt-1 ${reminder.color}`" />
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-medium">{{ reminder.title }}</p>
                  <p class="text-xs text-muted-foreground">{{ reminder.time }}</p>
                </div>
                <Badge :variant="reminder.priority === 'high' ? 'destructive' : 'secondary'" class="text-xs">
                  {{ reminder.priority === 'high' ? '紧急' : '普通' }}
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Plus, Flag, RefreshCw } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Button from '@/components/ui/Button.vue'
import Checkbox from '@/components/ui/Checkbox.vue'
import Badge from '@/components/ui/Badge.vue'
import { cn } from '@/lib/utils'
import { useDashboardStore } from '@/stores/dashboard'
import AddTaskModal from './AddTaskModal.vue'
import MessageModal from '@/components/ui/MessageModal.vue'

const store = useDashboardStore()

const showAddTaskModal = ref(false)
const showTaskDetailsModal = ref(false)
const selectedTaskDetail = ref<any>(null)
const isEditMode = ref(false)
const isReminder = ref(false) // 标记是否是查看提醒
const isRefreshing = ref(false) // 刷新状态

// 消息模态框相关
const showMessageModal = ref(false)
const messageModalType = ref<'success' | 'error' | 'warning' | 'info'>('info')
const messageModalTitle = ref('提示')
const messageModalMessage = ref('')
const messageModalShowCancel = ref(false)
const messageModalConfirmText = ref('确定')
const messageModalCancelText = ref('取消')
let pendingAction: (() => void) | null = null
const editTaskData = ref({
  title: '',
  date: '',
  startTime: '',
  endTime: '',
  priority: 'medium' as 'high' | 'medium' | 'low',
  hasReminder: false,
  reminderTime: '' // 提醒时间
})

// 计算当前日期时间作为最小值
const currentDateTime = computed(() => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
})

// 格式化日期为本地时间字符串（避免时区问题）
const formatDateLocal = (date: Date): string => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const selectedDateStr = computed(() => {
  return formatDateLocal(store.selectedDate)
})

// 处理添加任务
const handleAddTask = async (taskData: any) => {
  try {
    // 添加到store
    await store.addTask(taskData)
    console.log('任务添加成功:', taskData)
    showAddTaskModal.value = false
    
    // 刷新任务列表（自动更新提醒）
    await store.loadTasks()
    
    // 显示成功提示
    showMessage('success', '成功', '任务添加成功！')
  } catch (error) {
    console.error('添加任务失败:', error)
    showMessage('error', '错误', '添加任务失败，请稍后重试')
  }
}

const selectedDate = computed(() => store.selectedDate)

const formatDateShort = (date: Date) => {
  return date.toLocaleDateString("zh-CN", {
    month: "numeric",
    day: "numeric",
  })
}

const filteredTasks = computed(() => {
  // 使用本地时间格式化，避免时区问题
  const dateStr = formatDateLocal(selectedDate.value)
  // 显示选中日期的所有任务（包括有提醒的）
  return store.tasks.filter(task => task.date === dateStr)
})

const priorityColors = {
  high: 'text-destructive',
  medium: 'text-chart-3',
  low: 'text-chart-5'
}

// 显示任务详情
const showTaskDetail = (task: any, isReminderView = false) => {
  if (!task) return
  selectedTaskDetail.value = task
  isEditMode.value = false
  isReminder.value = isReminderView
  // 初始化编辑数据
  editTaskData.value = {
    title: task.title,
    date: task.date,
    startTime: task.time ? task.time.split('-')[0] : '',
    endTime: task.time ? task.time.split('-')[1] : '',
    priority: task.priority,
    hasReminder: task.hasReminder || task.has_reminder || false,
    reminderTime: task.reminder_time || task.reminderTime || ''
  }
  showTaskDetailsModal.value = true
}

// 切换编辑模式
const toggleEditMode = () => {
  isEditMode.value = !isEditMode.value
}

// 取消编辑
const cancelEdit = () => {
  isEditMode.value = false
  // 恢复原始数据
  if (selectedTaskDetail.value) {
    editTaskData.value = {
      title: selectedTaskDetail.value.title,
      date: selectedTaskDetail.value.date,
      startTime: selectedTaskDetail.value.time ? selectedTaskDetail.value.time.split('-')[0] : '',
      endTime: selectedTaskDetail.value.time ? selectedTaskDetail.value.time.split('-')[1] : '',
      priority: selectedTaskDetail.value.priority,
      hasReminder: selectedTaskDetail.value.hasReminder || selectedTaskDetail.value.has_reminder || false,
      reminderTime: selectedTaskDetail.value.reminder_time || selectedTaskDetail.value.reminderTime || ''
    }
  }
}

// 保存编辑
const saveEdit = async () => {
  if (!selectedTaskDetail.value) return
  
  try {
    // 构建更新数据，使用后端字段名
    const updatedTask = {
      title: editTaskData.value.title,
      date: editTaskData.value.date,
      time: editTaskData.value.startTime && editTaskData.value.endTime 
        ? `${editTaskData.value.startTime}-${editTaskData.value.endTime}` 
        : undefined,
      priority: editTaskData.value.priority,
      // 使用后端字段名
      has_reminder: editTaskData.value.hasReminder,
      reminder_time: editTaskData.value.hasReminder && editTaskData.value.reminderTime 
        ? editTaskData.value.reminderTime 
        : undefined
    }
    
    // 更新任务
    await store.updateTask(selectedTaskDetail.value.id, updatedTask)
    
    // 重新加载任务列表以获取最新数据（自动更新提醒）
    await store.loadTasks()
    
    // 更新选中任务的详情（从store中重新获取）
    const updatedTaskFromStore = store.tasks.find(t => t.id === selectedTaskDetail.value.id)
    if (updatedTaskFromStore) {
      selectedTaskDetail.value = updatedTaskFromStore
    }
    
    isEditMode.value = false
    showMessage('success', '成功', '任务更新成功！')
  } catch (error) {
    console.error('更新任务失败:', error)
    showMessage('error', '错误', '更新任务失败，请稍后重试')
  }
}

// 通过ID查找任务
const findTaskById = (id: number) => {
  return store.tasks.find(t => t.id === id) || null
}

// 关闭任务详情模态框
const closeTaskDetail = () => {
  showTaskDetailsModal.value = false
  selectedTaskDetail.value = null
  isEditMode.value = false
}

// 删除任务
const handleDeleteTask = () => {
  if (!selectedTaskDetail.value) return
  
  // 使用自定义模态框确认删除
  showMessage(
    'warning',
    '确认删除',
    `确定要删除任务"${selectedTaskDetail.value.title}"吗？此操作不可恢复。`,
    true,
    '删除',
    '取消'
  )
  
  // 保存删除操作
  pendingAction = async () => {
    try {
      await store.deleteTask(selectedTaskDetail.value!.id)
      
      // 刷新任务列表（自动更新提醒）
      await store.loadTasks()
      
      showMessage('success', '成功', '任务删除成功！')
      closeTaskDetail()
    } catch (error) {
      console.error('删除任务失败:', error)
      showMessage('error', '错误', '删除任务失败，请稍后重试')
    }
  }
}

// 显示消息模态框
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

// 处理消息确认
const handleMessageConfirm = () => {
  if (pendingAction) {
    pendingAction()
    pendingAction = null
  }
}

// 处理消息取消
const handleMessageCancel = () => {
  pendingAction = null
}

// 刷新任务数据
const refreshTasks = async () => {
  if (isRefreshing.value) return
  
  isRefreshing.value = true
  try {
    await store.loadTasks()
    showMessage('success', '成功', '任务列表已刷新')
  } catch (error) {
    console.error('刷新任务数据失败:', error)
    showMessage('error', '错误', '刷新任务数据失败，请稍后重试')
  } finally {
    isRefreshing.value = false
  }
}

// 从任务数据中生成提醒 - 只显示未完成且有提醒标志的任务
const reminders = computed(() => {
  // 使用本地时间格式化，避免时区问题
  const dateStr = formatDateLocal(selectedDate.value)
  return store.tasks
    .filter(task => {
      // 筛选选中日期的任务
      if (task.date !== dateStr) return false
      // 筛选有提醒且未完成的任务
      const hasReminder = task.hasReminder || task.has_reminder || false
      return hasReminder === true && !task.completed
    })
    .map((task, index) => {
      let timeStr = ''
      
      // 优先显示提醒时间
      if (task.reminder_time) {
        try {
          const reminderDate = new Date(task.reminder_time)
          // 使用选中的日期作为基准，而不是系统当前时间
          const selectedDateOnly = new Date(selectedDate.value)
          selectedDateOnly.setHours(0, 0, 0, 0)  // 重置为当天00:00:00
          
          // 将提醒日期也重置为当天00:00:00，用于比较日期部分
          const reminderDateOnly = new Date(reminderDate)
          reminderDateOnly.setHours(0, 0, 0, 0)
          
          // 计算日期差（基于选中日期）
          const diffMs = reminderDateOnly.getTime() - selectedDateOnly.getTime()
          const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
          
          // 格式化提醒时间
          const hours = String(reminderDate.getHours()).padStart(2, '0')
          const minutes = String(reminderDate.getMinutes()).padStart(2, '0')
          const month = String(reminderDate.getMonth() + 1).padStart(2, '0')
          const day = String(reminderDate.getDate()).padStart(2, '0')
          
          // 格式化显示时间（基于选中日期）
          if (diffDays === 0) {
            // 提醒时间在选中日期的当天，显示"今天"
            timeStr = `今天 ${hours}:${minutes}`
          } else if (diffDays === 1) {
            timeStr = `明天 ${hours}:${minutes}`
          } else if (diffDays === 2) {
            timeStr = `后天 ${hours}:${minutes}`
          } else if (diffDays > 0) {
            timeStr = `${month}-${day} ${hours}:${minutes}`
          } else {
            // 过去的日期
            timeStr = `${month}-${day} ${hours}:${minutes}`
          }
        } catch (e) {
          // 如果解析失败，使用原始字符串
          timeStr = task.reminder_time
        }
      } else if (task.time) {
        // 如果没有提醒时间，显示任务时间
        const time = task.time.split('-')[0]
        timeStr = `${task.date} ${time}`
      } else {
        // 都没有，显示任务日期
        const taskDate = new Date(task.date)
        const today = new Date()
        const diffDays = Math.ceil((taskDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
        
        if (diffDays === 0) timeStr = '今天'
        else if (diffDays === 1) timeStr = '明天'
        else if (diffDays === 2) timeStr = '后天'
        else if (diffDays > 0) timeStr = `${diffDays}天后`
        else timeStr = task.date
      }
      
      const colors = ['bg-red-500', 'bg-orange-500', 'bg-green-500']
      
      return {
        id: task.id,
        title: task.title,
        time: timeStr,
        priority: task.priority as 'high' | 'medium' | 'low',
        color: colors[index % colors.length]
      }
    })
})
</script>

<style scoped>
/* 模态框动画 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-scale-enter-active,
.modal-scale-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-scale-enter-from,
.modal-scale-leave-to {
  transform: scale(0.85) translateY(20px);
  opacity: 0;
}

.modal-content {
  animation: slideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideIn {
  from {
    transform: scale(0.85) translateY(30px) rotate(2deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.05) translateY(-10px) rotate(-1deg);
  }
  to {
    transform: scale(1) translateY(0) rotate(0deg);
    opacity: 1;
  }
}

/* 编辑模式内容动画 */
.edit-fade-enter-active,
.edit-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.edit-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.edit-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
