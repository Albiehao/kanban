<template>
  <Card class="finance-stats-container">
    <CardHeader>
      <CardTitle class="text-base flex items-center gap-2">
        <div class="w-2 h-2 bg-chart-5 rounded-full"></div>
        财务统计
      </CardTitle>
    </CardHeader>
    <CardContent class="p-0">
      <div class="finance-scroll-container">
        <div class="p-4">
          <!-- 财务统计内容 -->
          <div v-if="store.financeStats" class="flex gap-6 items-start">
            <!-- 左侧：收入支出概览 -->
            <div class="flex-1 space-y-4">
              <!-- 收入卡片 -->
              <div class="income-card">
                <div class="card-icon income-icon">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
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
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
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
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
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
              <PieChart :data="expenseData" :size="180" />
            </div>
          </div>
          <div v-else class="flex gap-6 opacity-0">
            <!-- 数据未加载时不显示，静默等待 -->
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import PieChart from '@/components/PieChart.vue'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

// 从 store 获取消费数据
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
</script>

<style scoped>
.income-card,
.expense-card,
.balance-card {
  @apply flex items-center gap-3 p-3 rounded-lg transition-all duration-200 hover:shadow-md;
}

.income-card {
  @apply bg-green-50 border border-green-200 hover:bg-green-100;
}

.expense-card {
  @apply bg-red-50 border border-red-200 hover:bg-red-100;
}

.balance-card {
  @apply bg-blue-50 border border-blue-200 hover:bg-blue-100;
}

.card-icon {
  @apply w-8 h-8 rounded-full flex items-center justify-center text-white;
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
  @apply text-xs text-muted-foreground mb-1;
}

.card-value {
  @apply text-lg font-bold;
}

.income-value {
  @apply text-green-600;
}

.expense-value {
  @apply text-red-600;
}

.balance-value {
  @apply text-blue-600;
}
</style>
