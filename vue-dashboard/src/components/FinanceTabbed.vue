<template>
  <Card class="finance-tabbed-container flex flex-col overflow-hidden" style="height: 360px; max-height: 360px; min-height: 360px;">
    <CardHeader class="flex-shrink-0">
      <div class="flex items-center justify-between">
        <CardTitle class="text-base flex items-center gap-2">
          <div class="w-2 h-2 bg-chart-5 rounded-full"></div>
          财务统计
        </CardTitle>
        <div v-if="activeTab === 'tracker'" class="flex gap-1">
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

    <!-- 标签导航 -->
    <div class="border-b border-gray-200 dark:border-gray-700 px-4 flex-shrink-0">
      <div class="flex gap-1">
        <button
          @click="activeTab = 'stats'"
          :class="cn(
            'px-3 py-2 text-sm font-medium transition-colors',
            'border-b-2',
            activeTab === 'stats'
              ? 'border-primary text-primary'
              : 'border-transparent text-muted-foreground hover:text-foreground hover:border-gray-300 dark:hover:border-gray-600'
          )"
        >
          财务统计
        </button>
        <button
          @click="activeTab = 'tracker'"
          :class="cn(
            'px-3 py-2 text-sm font-medium transition-colors',
            'border-b-2',
            activeTab === 'tracker'
              ? 'border-primary text-primary'
              : 'border-transparent text-muted-foreground hover:text-foreground hover:border-gray-300 dark:hover:border-gray-600'
          )"
        >
          账本
        </button>
      </div>
    </div>

    <!-- 标签内容 -->
    <CardContent class="p-0 flex-1 min-h-0 overflow-hidden flex flex-col">
      <!-- 财务统计标签 -->
      <div v-show="activeTab === 'stats'" class="finance-stats-content flex-1 min-h-0 overflow-hidden flex flex-col">
        <div class="finance-scroll-container flex-1 min-h-0 overflow-y-auto">
          <div class="p-4">
            <!-- 财务统计内容 -->
            <div v-if="store.financeStats" class="flex gap-4 items-start">
              <!-- 左侧：收入支出概览 -->
              <div class="flex-1 space-y-2">
                <!-- 收入卡片 -->
                <div class="income-card">
                  <div class="card-icon income-icon">
                    <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div class="card-content">
                    <p class="card-label">本月收入</p>
                    <p class="card-value income-value">¥{{ store.financeStats.monthlyIncome.toLocaleString() }}</p>
                  </div>
                </div>
                
                <!-- 支出卡片 -->
                <div class="expense-card">
                  <div class="card-icon expense-icon">
                    <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div class="card-content">
                    <p class="card-label">本月支出</p>
                    <p class="card-value expense-value">¥{{ store.financeStats.monthlyExpense.toLocaleString() }}</p>
                  </div>
                </div>
                
                <!-- 结余卡片 -->
                <div class="balance-card">
                  <div class="card-icon balance-icon">
                    <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div class="card-content">
                    <p class="card-label">结余</p>
                    <p class="card-value balance-value">¥{{ store.financeStats.balance.toLocaleString() }}</p>
                  </div>
                </div>
              </div>
              
              <!-- 右侧：扇形图 -->
              <div class="flex-1 flex justify-center">
                <PieChart :data="expenseData" :size="140" />
              </div>
            </div>
            <div v-else class="flex gap-4 opacity-0">
              <!-- 数据未加载时不显示，静默等待 -->
            </div>
          </div>
        </div>
      </div>

      <!-- 账本标签 -->
      <div v-show="activeTab === 'tracker'" class="p-3 pt-3 flex flex-col flex-1 min-h-0 overflow-hidden">
        <!-- Summary Cards -->
        <div class="grid grid-cols-3 gap-1 mb-3 flex-shrink-0">
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
        <div class="flex-1 overflow-hidden min-h-0">
          <div
            v-if="filteredTransactions.length === 0"
            class="text-center py-3 text-muted-foreground dark:text-gray-400 text-xs"
          >
            该日期暂无账目记录
          </div>
          <div
            v-else
            class="h-full overflow-y-auto space-y-1 scrollbar-hide"
            style="padding-bottom: 12px; padding-right: 4px;"
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
import { computed, ref, Teleport, Transition } from 'vue'
import { Plus, TrendingUp, TrendingDown, Wallet, RefreshCw, Edit, Trash2, X } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Button from '@/components/ui/Button.vue'
import Badge from '@/components/ui/Badge.vue'
import PieChart from '@/components/PieChart.vue'
import MessageModal from '@/components/ui/MessageModal.vue'
import { cn } from '@/utils'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

const activeTab = ref<'stats' | 'tracker'>('stats')

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

const filteredTransactions = computed(() => store.filteredTransactions)

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

// 财务统计数据
const expenseData = computed(() => {
  if (!store.financeStats) {
    return []
  }
  
  return store.financeStats.expenseByCategory.map(item => ({
    label: item.category,
    value: item.amount,
    color: item.color
  }))
})

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

// 处理查看详情
const handleViewDetail = (transaction: any) => {
  detailTransaction.value = transaction
  showDetailModal.value = true
}

// 从详情弹窗进入编辑
const handleEditFromDetail = () => {
  if (detailTransaction.value) {
    store.editingTransaction = detailTransaction.value
    showDetailModal.value = false
    store.showTransactionModal = true
  }
}
</script>

<style scoped>
/* 高度由 flex-1 控制，不再固定 */

.finance-scroll-container {
  @apply h-full overflow-y-auto scrollbar-hide;
}

.income-card,
.expense-card,
.balance-card {
  @apply flex items-center gap-2 p-2 rounded-lg transition-all duration-200 hover:shadow-md;
}

.income-card {
  @apply bg-green-50 border border-green-200 hover:bg-green-100 dark:bg-green-900/20 dark:border-green-800 dark:hover:bg-green-900/30;
}

.expense-card {
  @apply bg-red-50 border border-red-200 hover:bg-red-100 dark:bg-red-900/20 dark:border-red-800 dark:hover:bg-red-900/30;
}

.balance-card {
  @apply bg-blue-50 border border-blue-200 hover:bg-blue-100 dark:bg-blue-900/20 dark:border-blue-800 dark:hover:bg-blue-900/30;
}

.card-icon {
  @apply w-6 h-6 rounded-full flex items-center justify-center text-white flex-shrink-0;
}

.income-icon {
  @apply bg-green-500;
}

.expense-icon {
  @apply bg-red-500;
}

.balance-icon {
  @apply bg-blue-500;
}

.card-content {
  @apply flex-1;
}

.card-label {
  @apply text-xs text-muted-foreground mb-0.5 dark:text-gray-400;
}

.card-value {
  @apply text-base font-bold;
}

.income-value {
  @apply text-green-600 dark:text-green-400;
}

.expense-value {
  @apply text-red-600 dark:text-red-400;
}

.balance-value {
  @apply text-blue-600 dark:text-blue-400;
}

.finance-tabbed-container {
  height: 360px !important;
  max-height: 360px !important;
  min-height: 360px !important;
}

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

