<template>
  <div 
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 dark:bg-black/70"
    @click="close"
  >
    <Transition name="modal-scale">
      <div 
        v-if="isOpen"
        class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-4 p-6 modal-content"
        @click.stop
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-foreground">添加任务</h3>
          <button 
            @click="close"
            class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- 任务标题 -->
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">任务名称</label>
            <input
              v-model="taskData.title"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="输入任务名称"
            />
          </div>

          <!-- 日期 -->
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">日期</label>
            <input
              v-model="taskData.date"
              type="date"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <!-- 时间段 -->
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">时间段 (可选)</label>
            <div class="flex gap-2">
              <input
                v-model="taskData.startTime"
                type="time"
                class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <span class="self-center text-gray-500">至</span>
              <input
                v-model="taskData.endTime"
                type="time"
                class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
          </div>

          <!-- 优先级 -->
          <div>
            <label class="block text-sm font-medium text-foreground mb-2">优先级</label>
            <div class="flex gap-2">
              <button
                type="button"
                :class="cn(
                  'flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                  taskData.priority === 'high' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-100 dark:bg-gray-700 text-foreground hover:bg-gray-200 dark:hover:bg-gray-600'
                )"
                @click="taskData.priority = 'high'"
              >
                高
              </button>
              <button
                type="button"
                :class="cn(
                  'flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                  taskData.priority === 'medium' 
                    ? 'bg-yellow-500 text-white' 
                    : 'bg-gray-100 dark:bg-gray-700 text-foreground hover:bg-gray-200 dark:hover:bg-gray-600'
                )"
                @click="taskData.priority = 'medium'"
              >
                中
              </button>
              <button
                type="button"
                :class="cn(
                  'flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors',
                  taskData.priority === 'low' 
                    ? 'bg-green-500 text-white' 
                    : 'bg-gray-100 dark:bg-gray-700 text-foreground hover:bg-gray-200 dark:hover:bg-gray-600'
                )"
                @click="taskData.priority = 'low'"
              >
                低
              </button>
            </div>
          </div>

          <!-- 是否提醒 -->
          <div class="space-y-2">
            <div class="flex items-center gap-2">
              <input
                v-model="taskData.hasReminder"
                type="checkbox"
                id="hasReminder"
                class="w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary"
              />
              <label for="hasReminder" class="text-sm text-foreground cursor-pointer">
                添加提醒
              </label>
            </div>
            
            <!-- 提醒时间 -->
            <div v-if="taskData.hasReminder" class="ml-6">
              <label class="block text-sm font-medium text-foreground mb-2">提醒时间</label>
              <input
                v-model="taskData.reminderTime"
                type="datetime-local"
                :min="currentDateTime"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
          </div>

          <!-- 按钮 -->
          <div class="flex gap-2 pt-2">
            <button
              type="button"
              @click="close"
              class="flex-1 px-4 py-2 bg-gray-100 dark:bg-gray-700 text-foreground rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              class="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
            >
              添加
            </button>
          </div>
        </form>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { cn } from '@/utils'
import { useDashboardStore } from '@/stores/dashboard'

const props = defineProps<{
  isOpen: boolean
  defaultDate?: string
}>()

const emit = defineEmits<{
  close: []
  submit: [task: any]
}>()

const store = useDashboardStore()

const taskData = ref({
  title: '',
  date: props.defaultDate || store.selectedDate.toISOString().split('T')[0],
  startTime: '',
  endTime: '',
  priority: 'medium' as 'high' | 'medium' | 'low',
  hasReminder: false,
  completed: false,
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

// 监听defaultDate变化
watch(() => props.defaultDate, (newDate) => {
  if (newDate) {
    taskData.value.date = newDate
  }
})

// 监听store.selectedDate变化
watch(() => store.selectedDate, () => {
  taskData.value.date = store.selectedDate.toISOString().split('T')[0]
})

const close = () => {
  emit('close')
}

const handleSubmit = () => {
  const task = {
    ...taskData.value,
    time: taskData.value.startTime && taskData.value.endTime 
      ? `${taskData.value.startTime}-${taskData.value.endTime}` 
      : undefined,
    // 处理提醒时间和字段映射
    has_reminder: taskData.value.hasReminder,
    reminder_time: taskData.value.hasReminder && taskData.value.reminderTime 
      ? taskData.value.reminderTime 
      : undefined
  }
  
  // 删除前端使用的字段名，只保留后端需要的
  delete task.hasReminder
  delete task.reminderTime
  
  emit('submit', task)
  
  // 重置表单
  taskData.value = {
    title: '',
    date: store.selectedDate.toISOString().split('T')[0],
    startTime: '',
    endTime: '',
    priority: 'medium',
    hasReminder: false,
    completed: false,
    reminderTime: ''
  }
}
</script>

<style scoped>
/* 模态框动画 */
.modal-scale-enter-active,
.modal-scale-leave-active {
  transition: all 0.3s ease;
}

.modal-scale-enter-from,
.modal-scale-leave-to {
  transform: scale(0.8);
  opacity: 0;
}

.modal-content {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: scale(0.9) translateY(-20px);
    opacity: 0;
  }
  to {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}
</style>

