<template>
  <Card>
    <CardHeader>
      <CardTitle class="text-base">数据统计</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="grid grid-cols-2 gap-6">
        <!-- 当日任务完成率 -->
        <div class="flex flex-col items-center">
          <div class="text-xs font-medium text-muted-foreground mb-3 text-center">
            当日任务
          </div>
          <div class="relative w-24 h-24">
            <!-- 扇形图 -->
            <svg class="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
              <!-- 已完成任务部分 -->
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="hsl(142, 76%, 36%)"
                stroke-width="12"
                :stroke-dasharray="251.2"
                :stroke-dashoffset="todayCompletedOffset"
                class="transition-all duration-500"
              />
              <!-- 未完成任务部分 -->
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="hsl(217, 33%, 17%)"
                stroke-width="12"
                :stroke-dasharray="251.2"
                :stroke-dashoffset="todayUncompletedOffset"
                class="opacity-20 transition-all duration-500"
                opacity="0.2"
              />
            </svg>
            
            <!-- 中心文字 -->
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-center">
                <div class="text-lg font-semibold text-foreground">{{ todayStats.completionRate }}%</div>
                <div class="text-xs text-muted-foreground">{{ todayStats.completedTasks }}/{{ todayStats.totalTasks }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 总体任务完成率 -->
        <div class="flex flex-col items-center">
          <div class="text-xs font-medium text-muted-foreground mb-3 text-center">
            总体任务
          </div>
          <div class="relative w-24 h-24">
            <!-- 扇形图 -->
            <svg class="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
              <!-- 已完成任务部分 -->
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="hsl(142, 76%, 36%)"
                stroke-width="12"
                :stroke-dasharray="251.2"
                :stroke-dashoffset="overallCompletedOffset"
                class="transition-all duration-500"
              />
              <!-- 未完成任务部分 -->
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="hsl(217, 33%, 17%)"
                stroke-width="12"
                :stroke-dasharray="251.2"
                :stroke-dashoffset="overallUncompletedOffset"
                class="opacity-20 transition-all duration-500"
                opacity="0.2"
              />
            </svg>
            
            <!-- 中心文字 -->
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-center">
                <div class="text-lg font-semibold text-foreground">{{ overallStats.completionRate }}%</div>
                <div class="text-xs text-muted-foreground">{{ overallStats.completedTasks }}/{{ overallStats.totalTasks }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="mt-4 pt-4 border-t border-border">
        <div class="grid grid-cols-2 gap-4 text-center">
          <div>
            <div class="text-sm font-semibold text-foreground">{{ overallStats.totalTasks }}</div>
            <div class="text-xs text-muted-foreground">总任务数</div>
          </div>
          <div>
            <div class="text-sm font-semibold text-foreground">{{ todayStats.totalTasks }}</div>
            <div class="text-xs text-muted-foreground">今日任务数</div>
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
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

// 计算当日任务统计
const todayStats = computed(() => {
  const today = store.selectedDate.toISOString().split('T')[0]
  const todayTasks = store.tasks.filter(t => t.date === today)
  const completedTasks = todayTasks.filter(t => t.completed).length
  const totalTasks = todayTasks.length
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0
  
  return {
    completedTasks,
    totalTasks,
    completionRate
  }
})

// 计算总体任务统计
const overallStats = computed(() => {
  const completedTasks = store.tasks.filter(t => t.completed).length
  const totalTasks = store.tasks.length
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0
  
  return {
    completedTasks,
    totalTasks,
    completionRate
  }
})

// 圆周率常量
const CIRCUMFERENCE = 251.2 // 2 * Math.PI * 40

// 计算当日扇形图的偏移量
const todayCompletedOffset = computed(() => {
  const percent = todayStats.value.completionRate
  return CIRCUMFERENCE - (CIRCUMFERENCE * percent / 100)
})

const todayUncompletedOffset = computed(() => {
  const percent = todayStats.value.completionRate
  return CIRCUMFERENCE - (CIRCUMFERENCE * (100 - percent) / 100)
})

// 计算总体扇形图的偏移量
const overallCompletedOffset = computed(() => {
  const percent = overallStats.value.completionRate
  return CIRCUMFERENCE - (CIRCUMFERENCE * percent / 100)
})

const overallUncompletedOffset = computed(() => {
  const percent = overallStats.value.completionRate
  return CIRCUMFERENCE - (CIRCUMFERENCE * (100 - percent) / 100)
})
</script>
