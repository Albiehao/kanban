<template>
  <Card class="task-list-container">
    <CardHeader>
      <div class="flex items-center justify-between">
        <CardTitle class="text-base">{{ formatDateShort(selectedDate) }} 任务</CardTitle>
        <Button size="sm" class="h-7 text-xs" @click="refreshTasks">
          <RefreshCw class="h-3 w-3 mr-1" />
          刷新
        </Button>
      </div>
    </CardHeader>
    <CardContent class="p-0">
      <div class="task-scroll-container">
        <div
          v-if="filteredTasks.length === 0"
          class="text-center py-4 text-muted-foreground dark:text-gray-400 text-xs"
        >
          该日期暂无任务
        </div>
        <div
          v-for="task in filteredTasks"
          :key="task.id"
          :class="cn(
            'flex items-start gap-1.5 p-1.5 rounded-lg transition-colors',
            'hover:bg-muted/50 dark:hover:bg-gray-800/50',
            task.completed && 'opacity-60'
          )"
        >
          <Checkbox 
            :checked="task.completed" 
            @update:checked="store.toggleTask(task.id)"
            class="mt-0.5"
          />
          <div class="flex-1 min-w-0">
            <p :class="cn(
              'text-sm font-medium dark:text-gray-200',
              task.completed && 'line-through text-muted-foreground dark:text-gray-500'
            )">
              {{ task.title }}
            </p>
            <div class="flex items-center gap-2 mt-0.5">
              <div class="flex items-center gap-1">
                <Flag :class="cn('h-3 w-3', priorityColors[task.priority])" />
                <span :class="cn('text-xs', priorityColors[task.priority])">
                  {{ task.priority === 'high' ? '高' : task.priority === 'medium' ? '中' : '低' }}
                </span>
              </div>
              <span v-if="task.time" class="text-xs text-muted-foreground dark:text-gray-400">
                {{ task.time }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
    
    <!-- 消息提示弹框 -->
    <MessageModal
      v-model:visible="showMessageModal"
      :type="messageModalType"
      :title="messageModalTitle"
      :message="messageModalMessage"
    />
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
import MessageModal from '@/components/ui/MessageModal.vue'
import { cn, formatDateShort } from '@/utils'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

const selectedDate = computed(() => store.selectedDate)
const filteredTasks = computed(() => store.filteredTasks)

const priorityColors = {
  high: 'text-destructive',
  medium: 'text-chart-5',
  low: 'text-muted-foreground',
}

// 消息弹框状态
const showMessageModal = ref(false)
const messageModalType = ref<'success' | 'error' | 'warning' | 'info'>('error')
const messageModalTitle = ref('错误')
const messageModalMessage = ref('')

const showMessage = (type: 'success' | 'error' | 'warning' | 'info', title: string, message: string) => {
  messageModalType.value = type
  messageModalTitle.value = title
  messageModalMessage.value = message
  showMessageModal.value = true
}

// 刷新任务数据
const refreshTasks = async () => {
  try {
    await store.loadTasks()
  } catch (error) {
    console.error('刷新任务数据失败:', error)
    showMessage('error', '错误', '刷新任务数据失败，请稍后重试')
  }
}
</script>
