<template>
  <Card class="finance-tracker-container">
    <CardHeader class="pb-2">
      <div class="flex items-center justify-between">
        <CardTitle class="text-base">{{ formatDateShort(selectedDate) }} 账本</CardTitle>
        <div class="flex gap-1">
          <Button size="sm" class="h-7 text-xs" @click="store.showTransactionModal = true">
            <Plus class="h-3 w-3 mr-1" />
            记账
          </Button>
          <Button size="sm" class="h-7 text-xs" @click="refreshTransactions">
            <RefreshCw class="h-3 w-3 mr-1" />
            刷新
          </Button>
        </div>
      </div>
    </CardHeader>
    <CardContent class="p-3 pt-2 flex flex-col h-full">
      <!-- Summary Cards -->
      <div class="grid grid-cols-3 gap-1 mb-3">
        <div class="p-2 rounded-lg bg-muted/50 dark:bg-gray-800/50">
          <div class="flex items-center gap-1 mb-0.5">
            <TrendingUp class="h-2.5 w-2.5 text-chart-5" />
            <span class="text-xs text-muted-foreground dark:text-gray-400">收入</span>
          </div>
          <p class="text-xs font-semibold text-chart-5">¥{{ totalIncome.toFixed(2) }}</p>
        </div>
        <div class="p-2 rounded-lg bg-muted/50 dark:bg-gray-800/50">
          <div class="flex items-center gap-1 mb-0.5">
            <TrendingDown class="h-2.5 w-2.5 text-destructive" />
            <span class="text-xs text-muted-foreground dark:text-gray-400">支出</span>
          </div>
          <p class="text-xs font-semibold text-destructive">¥{{ totalExpense.toFixed(2) }}</p>
        </div>
        <div class="p-2 rounded-lg bg-muted/50 dark:bg-gray-800/50">
          <div class="flex items-center gap-1 mb-0.5">
            <Wallet class="h-2.5 w-2.5 text-primary" />
            <span class="text-xs text-muted-foreground dark:text-gray-400">结余</span>
          </div>
          <p :class="cn(
            'text-xs font-semibold',
            balance >= 0 ? 'text-chart-5' : 'text-destructive'
          )">
            ¥{{ balance.toFixed(2) }}
          </p>
        </div>
      </div>


      <!-- Transaction List -->
      <div class="flex-1 overflow-hidden">
        <div
          v-if="filteredTransactions.length === 0"
          class="text-center py-3 text-muted-foreground dark:text-gray-400 text-xs"
        >
          该日期暂无账目记录
        </div>
        <div
          v-else
          class="h-full overflow-y-auto space-y-1 scrollbar-hide"
          style="max-height: 180px; padding-bottom: 8px;"
        >
          <div
            v-for="transaction in filteredTransactions"
            :key="transaction.id"
            class="flex items-center gap-2 p-2 rounded-lg bg-muted/50 dark:bg-gray-800/50 hover:bg-muted dark:hover:bg-gray-700 transition-colors cursor-pointer"
            @click="handleViewDetail(transaction)"
          >
            <div
              :class="cn(
                'w-5 h-5 rounded-lg flex items-center justify-center',
                categoryColors[transaction.category] || categoryColors['其他']
              )"
            >
              <TrendingUp v-if="transaction.type === 'income'" class="h-2.5 w-2.5 text-white" />
              <TrendingDown v-else class="h-2.5 w-2.5 text-white" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-1 mb-0.5">
                <p class="text-xs font-medium dark:text-gray-200">{{ transaction.description }}</p>
                <Badge variant="outline" class="text-xs px-1 py-0">
                  {{ transaction.category }}
                </Badge>
              </div>
              <p class="text-xs text-muted-foreground dark:text-gray-400">
                {{ transaction.type === 'income' ? '收入' : '支出' }}
              </p>
            </div>
            <p
              :class="cn(
                'text-xs font-semibold',
                transaction.type === 'income' ? 'text-chart-5' : 'text-destructive'
              )"
            >
              {{ transaction.type === 'income' ? '+' : '-' }}¥{{ transaction.amount.toFixed(2) }}
            </p>
            <div class="flex gap-1" @click.stop>
              <Button
                size="sm"
                variant="ghost"
                class="h-6 w-6 p-0 text-primary hover:text-primary hover:bg-primary/10"
                @click="handleEditTransaction(transaction)"
              >
                <Edit class="h-3 w-3" />
              </Button>
              <Button
                size="sm"
                variant="ghost"
                class="h-6 w-6 p-0 text-destructive hover:text-destructive hover:bg-destructive/10"
                @click="handleDeleteTransaction(transaction)"
              >
                <Trash2 class="h-3 w-3" />
              </Button>
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
      :show-cancel="showConfirmModal"
      confirm-text="确定"
      cancel-text="取消"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
    
    <!-- 交易记录详情弹窗 -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div 
          v-if="showDetailModal"
          class="fixed inset-0 bg-black/50 dark:bg-black/70 flex items-center justify-center z-50"
          @click="showDetailModal = false"
        >
          <Transition name="modal-scale">
            <div 
              class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-4 p-6"
              @click.stop
            >
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">交易详情</h3>
                <Button variant="ghost" size="sm" @click="showDetailModal = false">
                  <X class="h-4 w-4" />
                </Button>
              </div>
              
              <div v-if="detailTransaction" class="space-y-4">
                <!-- 类型 -->
                <div class="flex items-center gap-3">
                  <span class="text-sm font-medium text-gray-500 dark:text-gray-400 w-20">类型：</span>
                  <div class="flex items-center gap-2">
                    <div
                      :class="cn(
                        'w-6 h-6 rounded-lg flex items-center justify-center',
                        categoryColors[detailTransaction.category] || categoryColors['其他']
                      )"
                    >
                      <TrendingUp v-if="detailTransaction.type === 'income'" class="h-3 w-3 text-white" />
                      <TrendingDown v-else class="h-3 w-3 text-white" />
                    </div>
                    <span :class="cn(
                      'text-sm font-semibold',
                      detailTransaction.type === 'income' ? 'text-chart-5' : 'text-destructive'
                    )">
                      {{ detailTransaction.type === 'income' ? '收入' : '支出' }}
                    </span>
                  </div>
                </div>
                
                <!-- 金额 -->
                <div class="flex items-center gap-3">
                  <span class="text-sm font-medium text-gray-500 dark:text-gray-400 w-20">金额：</span>
                  <span :class="cn(
                    'text-lg font-bold',
                    detailTransaction.type === 'income' ? 'text-chart-5' : 'text-destructive'
                  )">
                    {{ detailTransaction.type === 'income' ? '+' : '-' }}¥{{ detailTransaction.amount.toFixed(2) }}
                  </span>
                </div>
                
                <!-- 类别 -->
                <div class="flex items-center gap-3">
                  <span class="text-sm font-medium text-gray-500 dark:text-gray-400 w-20">类别：</span>
                  <Badge variant="outline" class="text-xs">
                    {{ detailTransaction.category }}
                  </Badge>
                </div>
                
                <!-- 描述 -->
                <div class="flex items-start gap-3">
                  <span class="text-sm font-medium text-gray-500 dark:text-gray-400 w-20">描述：</span>
                  <p class="text-sm text-gray-900 dark:text-white flex-1">{{ detailTransaction.description || '无' }}</p>
                </div>
                
                <!-- 日期 -->
                <div class="flex items-center gap-3">
                  <span class="text-sm font-medium text-gray-500 dark:text-gray-400 w-20">日期：</span>
                  <span class="text-sm text-gray-900 dark:text-white">{{ detailTransaction.date }}</span>
                </div>
                
                <!-- 时间 -->
                <div v-if="detailTransaction.time" class="flex items-center gap-3">
                  <span class="text-sm font-medium text-gray-500 dark:text-gray-400 w-20">时间：</span>
                  <span class="text-sm text-gray-900 dark:text-white">{{ detailTransaction.time }}</span>
                </div>
                
                <!-- 操作按钮 -->
                <div class="flex justify-end gap-2 pt-4 border-t border-gray-200 dark:border-gray-700 mt-4">
                  <Button variant="outline" @click="showDetailModal = false">
                    关闭
                  </Button>
                  <Button @click="handleEditFromDetail">
                    <Edit class="h-4 w-4 mr-1" />
                    编辑
                  </Button>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </Card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Teleport, Transition } from 'vue'
import { Plus, TrendingUp, TrendingDown, Wallet, RefreshCw, Trash2, Edit, X } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Button from '@/components/ui/Button.vue'
import Badge from '@/components/ui/Badge.vue'
import MessageModal from '@/components/ui/MessageModal.vue'
import { cn, formatDateShort } from '@/utils'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

const selectedDate = computed(() => store.selectedDate)
const filteredTransactions = computed(() => {
  console.log('FinanceTracker - 当前选中日期:', store.selectedDate)
  console.log('FinanceTracker - 所有交易记录数量:', store.transactions.length)
  console.log('FinanceTracker - 过滤后的交易记录数量:', store.filteredTransactions.length)
  return store.filteredTransactions
})


const totalIncome = computed(() => 
  filteredTransactions.value
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0)
)

const totalExpense = computed(() => 
  filteredTransactions.value
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0)
)

const balance = computed(() => totalIncome.value - totalExpense.value)

const categoryColors: Record<string, string> = {
  餐饮: 'bg-chart-1',
  学习: 'bg-chart-2',
  交通: 'bg-chart-3',
  娱乐: 'bg-chart-4',
  兼职: 'bg-chart-5',
  其他: 'bg-muted',
}

// 消息弹框状态
const showMessageModal = ref(false)
const messageModalType = ref<'success' | 'error' | 'warning' | 'info'>('error')
const messageModalTitle = ref('错误')
const messageModalMessage = ref('')
const showConfirmModal = ref(false)
const pendingTransactionId = ref<number | null>(null)

// 详情弹窗状态
const showDetailModal = ref(false)
const detailTransaction = ref<any>(null)

const showMessage = (type: 'success' | 'error' | 'warning' | 'info', title: string, message: string) => {
  messageModalType.value = type
  messageModalTitle.value = title
  messageModalMessage.value = message
  showMessageModal.value = true
}

// 刷新财务数据
const refreshTransactions = async () => {
  try {
    await store.loadTransactions()
  } catch (error) {
    console.error('刷新财务数据失败:', error)
    showMessage('error', '错误', '刷新财务数据失败，请稍后重试')
  }
}

// 处理删除交易记录（退款）
const handleDeleteTransaction = (transaction: any) => {
  pendingTransactionId.value = transaction.id
  messageModalType.value = 'warning'
  messageModalTitle.value = '确认删除'
  messageModalMessage.value = `确定要删除该${transaction.type === 'income' ? '收入' : '支出'}记录吗？\n\n描述：${transaction.description}\n金额：¥${transaction.amount.toFixed(2)}\n类别：${transaction.category}`
  showConfirmModal.value = true
  showMessageModal.value = true
}

// 确认删除
const confirmDelete = async () => {
  if (pendingTransactionId.value === null) return
  
  showConfirmModal.value = false
  const transactionId = pendingTransactionId.value
  pendingTransactionId.value = null
  showMessageModal.value = false
  
  try {
    await store.deleteTransaction(transactionId)
    showMessage('success', '成功', '交易记录已删除（退款成功）')
  } catch (error: any) {
    console.error('删除交易记录失败:', error)
    showMessage('error', '错误', error.message || '删除交易记录失败，请稍后重试')
  }
}

// 取消删除
const cancelDelete = () => {
  showConfirmModal.value = false
  showMessageModal.value = false
  pendingTransactionId.value = null
}

// 处理编辑交易记录
const handleEditTransaction = (transaction: any) => {
  store.editingTransaction = transaction
  store.showTransactionModal = true
}

// 从详情弹窗进入编辑
const handleEditFromDetail = () => {
  if (detailTransaction.value) {
    store.editingTransaction = detailTransaction.value
    showDetailModal.value = false
    store.showTransactionModal = true
  }
}

// 处理查看详情（阻止事件冒泡）
const handleViewDetail = (transaction: any) => {
  detailTransaction.value = transaction
  showDetailModal.value = true
}
</script>

<style scoped>
.scrollbar-hide {
  /* Firefox */
  scrollbar-width: none;
  /* IE and Edge */
  -ms-overflow-style: none;
}

.scrollbar-hide::-webkit-scrollbar {
  /* Chrome, Safari, Opera */
  display: none;
}

/* 详情弹窗过渡动画 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-scale-enter-active,
.modal-scale-leave-active {
  transition: all 0.3s ease;
}

.modal-scale-enter-from,
.modal-scale-leave-to {
  transform: scale(0.9);
  opacity: 0;
}
</style>
