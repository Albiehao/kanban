<template>
  <div class="min-h-screen flex flex-col" style="background-color: hsl(var(--background))">
    <DashboardHeader />

    <main class="container mx-auto px-4 py-3 flex-1 flex flex-col min-h-0">
        <!-- 三列布局 - 先显示UI，数据异步加载 -->
      <div class="grid gap-2 md:gap-4 lg:grid-cols-12 flex-1 min-h-0 items-stretch">
        <!-- Left Column - Calendar, Stats & Finance -->
        <div class="lg:col-span-4 space-y-2 md:space-y-4 flex flex-col min-h-0">
          <CalendarWidget v-if="isVisible('calendar')" class="flex-shrink-0" />
          <StatsOverview v-if="isVisible('stats')" class="flex-shrink-0" />
          <FinanceTabbed v-if="isVisible('finance') || isVisible('finance-stats')" class="flex-shrink-0" />
        </div>

        <!-- Middle Column - Task & Reminder Fusion & Course Schedule -->
        <div class="lg:col-span-4 space-y-2 md:space-y-4 flex flex-col min-h-0">
          <TaskReminderFusion v-if="isVisible('tasks')" class="flex-shrink-0" />
          <WeeklySchedule v-if="isVisible('courses')" class="flex-shrink-0 mt-2" />
        </div>

        <!-- Right Column - TimeLine & AI Chat -->
        <div class="lg:col-span-4 space-y-2 md:space-y-4 flex flex-col min-h-0">
          <TimeLine v-if="isVisible('timeline')" class="flex-shrink-0" />
          <AIChat v-if="isVisible('ai-chat')" class="flex-shrink-0" />
        </div>
      </div>
    </main>

    <!-- Global Transaction Modal -->
    <TransactionModal 
      :is-open="store.showTransactionModal" 
      :editing-transaction="store.editingTransaction"
      @close="() => { store.showTransactionModal = false; store.editingTransaction = null }" 
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'
import DashboardHeader from '@/components/DashboardHeader.vue'
import CalendarWidget from '@/components/CalendarWidget.vue'
import TaskReminderFusion from '@/components/TaskReminderFusion.vue'
import WeeklySchedule from '@/components/WeeklySchedule.vue'
import FinanceTabbed from '@/components/FinanceTabbed.vue'
import StatsOverview from '@/components/StatsOverview.vue'
import TimeLine from '@/components/TimeLine.vue'
import AIChat from '@/components/AIChat.vue'
import TransactionModal from '@/components/TransactionModal.vue'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

// 组件挂载时先初始化主题，然后异步加载数据
onMounted(() => {
  // 先初始化主题（立即执行）
  store.initTheme()
  
  // 异步加载数据（不阻塞UI渲染）
  const loadData = async () => {
    try {
      console.log('Dashboard组件挂载，开始加载数据...')
      console.log('Store状态:', {
        courses: store.courses.length,
        tasks: store.tasks.length,
        transactions: store.transactions.length,
        isLoading: store.isLoading
      })
      
      await store.loadAllData()
      
      console.log('Dashboard数据加载完成')
      console.log('加载后的Store状态:', {
        courses: store.courses.length,
        tasks: store.tasks.length,
        transactions: store.transactions.length,
        isLoading: store.isLoading
      })
    } catch (error) {
      console.error('Dashboard数据加载失败:', error)
    }
  }
  
  // 使用 setTimeout 确保 UI 先渲染
  setTimeout(() => {
    loadData().then(() => {
      // 数据加载完成后启动自动刷新
      // 默认30秒刷新一次任务和课程数据
      store.startAutoRefresh(30000)
      console.log('自动刷新已启动（30秒间隔）')
    })
  }, 100)
})

// 组件卸载时停止自动刷新
onBeforeUnmount(() => {
  store.stopAutoRefresh()
})

const isVisible = (id: string) => {
  const module = store.modules.find(m => m.id === id)
  return module?.visible ?? true
}
</script>
