<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg w-full max-w-md mx-4">
      <!-- Header -->
      <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ editingTransaction ? '编辑交易记录' : '添加交易记录' }}</h3>
        <Button variant="ghost" size="sm" @click="closeModal">
          <X class="h-4 w-4" />
        </Button>
      </div>
      
      <!-- Form -->
      <div class="p-4 space-y-4">
        <!-- 交易类型 -->
        <div>
          <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">交易类型</label>
          <div class="flex gap-2">
            <Button
              :variant="formData.type === 'income' ? 'default' : 'outline'"
              size="sm"
              @click="formData.type = 'income'"
            >
              收入
            </Button>
            <Button
              :variant="formData.type === 'expense' ? 'default' : 'outline'"
              size="sm"
              @click="formData.type = 'expense'"
            >
              支出
            </Button>
          </div>
        </div>
        
        <!-- 金额 -->
        <div>
          <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">金额</label>
          <input
            v-model.number="formData.amount"
            type="number"
            step="0.01"
            min="0"
            placeholder="请输入金额"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        
        <!-- 分类 -->
        <div>
          <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">分类</label>
          <select
            v-model="formData.category"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>
        
        <!-- 描述 -->
        <div>
          <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">描述</label>
          <input
            v-model="formData.description"
            type="text"
            placeholder="请输入描述"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        
        <!-- 日期和时间 -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">日期</label>
            <input
              v-model="formData.date"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">时间 <span class="text-xs text-gray-400">(可选)</span></label>
            <input
              v-model="formData.time"
              type="time"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>
      </div>
      
      <!-- Footer -->
      <div class="flex justify-end gap-2 p-4 border-t border-gray-200 dark:border-gray-700">
        <Button variant="outline" @click="closeModal">
          取消
        </Button>
        <Button @click="handleSubmit" :disabled="isSubmitting">
          {{ isSubmitting ? (editingTransaction ? '更新中...' : '添加中...') : (editingTransaction ? '更新' : '添加') }}
        </Button>
      </div>
    </div>
    
    <!-- 消息提示弹框 -->
    <MessageModal
      v-model:visible="showMessageModal"
      :type="messageModalType"
      :title="messageModalTitle"
      :message="messageModalMessage"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { X } from 'lucide-vue-next'
import Button from '@/components/ui/Button.vue'
import MessageModal from '@/components/ui/MessageModal.vue'
import { useDashboardStore } from '@/stores/dashboard'

interface Props {
  isOpen: boolean
  editingTransaction?: {
    id: number
    type: 'income' | 'expense'
    amount: number
    category: string
    description: string
    date: string
    time?: string
  } | null
}

interface Emits {
  (e: 'close'): void
}

const props = withDefaults(defineProps<Props>(), {
  editingTransaction: null
})

const emit = defineEmits<Emits>()

const store = useDashboardStore()

const isSubmitting = ref(false)

// 消息弹框状态
const showMessageModal = ref(false)
const messageModalType = ref<'success' | 'error' | 'warning' | 'info'>('info')
const messageModalTitle = ref('提示')
const messageModalMessage = ref('')

const showMessage = (type: 'success' | 'error' | 'warning' | 'info', title: string, message: string) => {
  messageModalType.value = type
  messageModalTitle.value = title
  messageModalMessage.value = message
  showMessageModal.value = true
}

const formData = ref({
  type: 'expense' as 'income' | 'expense',
  amount: 0,
  category: '餐饮',
  description: '',
  date: store.selectedDateStr.value,
  time: '' // 具体时间，可选
})

const categories = ['餐饮', '学习', '交通', '娱乐', '兼职', '其他']

// 监听弹框打开，重置表单或加载编辑数据
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    if (props.editingTransaction) {
      // 编辑模式：加载现有数据
      formData.value = {
        type: props.editingTransaction.type,
        amount: props.editingTransaction.amount,
        category: props.editingTransaction.category,
        description: props.editingTransaction.description,
        date: props.editingTransaction.date,
        time: props.editingTransaction.time || ''
      }
    } else {
      // 添加模式：重置表单
      formData.value = {
        type: 'expense',
        amount: 0,
        category: '餐饮',
        description: '',
        date: store.selectedDateStr.value,
        time: ''
      }
    }
  }
})

const closeModal = () => {
  emit('close')
}

const handleSubmit = async () => {
  if (!formData.value.description || formData.value.amount <= 0) {
    showMessage('warning', '提示', '请填写完整的交易信息')
    return
  }
  
  isSubmitting.value = true
  
  try {
    if (props.editingTransaction) {
      // 更新交易记录
      await store.updateTransaction(props.editingTransaction.id, {
        type: formData.value.type,
        amount: formData.value.amount,
        category: formData.value.category,
        description: formData.value.description,
        date: formData.value.date,
        time: formData.value.time || undefined
      })
      closeModal()
      showMessage('success', '成功', '交易记录更新成功')
    } else {
      // 添加交易记录
      await store.addTransaction({
        type: formData.value.type,
        amount: formData.value.amount,
        category: formData.value.category,
        description: formData.value.description,
        date: formData.value.date,
        time: formData.value.time || undefined
      })
      closeModal()
      showMessage('success', '成功', '交易记录添加成功')
    }
  } catch (error: any) {
    console.error(props.editingTransaction ? '更新交易记录失败:' : '添加交易记录失败:', error)
    const errorMessage = error?.message || (props.editingTransaction ? '更新失败，请重试' : '添加失败，请重试')
    showMessage('error', '错误', errorMessage)
  } finally {
    isSubmitting.value = false
  }
}
</script>
