<template>
  <Card class="task-stats-container">
    <CardHeader>
      <CardTitle class="text-base">任务统计</CardTitle>
    </CardHeader>
    <CardContent class="p-0">
      <div class="task-stats-scroll-container">
        <div class="grid grid-cols-1 gap-2">
          <!-- 总任务数 -->
          <div class="flex items-center justify-between p-2 rounded-lg bg-muted/50">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-primary"></div>
              <span class="text-xs text-muted-foreground">总任务</span>
            </div>
            <span class="text-sm font-semibold text-primary">{{ totalTasks }}</span>
          </div>

          <!-- 紧急任务数 -->
          <div class="flex items-center justify-between p-2 rounded-lg bg-muted/50">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-destructive"></div>
              <span class="text-xs text-muted-foreground">紧急任务</span>
            </div>
            <span class="text-sm font-semibold text-destructive">{{ urgentTasks }}</span>
          </div>

          <!-- 完成任务数 -->
          <div class="flex items-center justify-between p-2 rounded-lg bg-muted/50">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-chart-5"></div>
              <span class="text-xs text-muted-foreground">已完成</span>
            </div>
            <span class="text-sm font-semibold text-chart-5">{{ completedTasks }}</span>
          </div>

          <!-- 进行中任务数 -->
          <div class="flex items-center justify-between p-2 rounded-lg bg-muted/50">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-chart-3"></div>
              <span class="text-xs text-muted-foreground">进行中</span>
            </div>
            <span class="text-sm font-semibold text-chart-3">{{ inProgressTasks }}</span>
          </div>

          <!-- 完成率 -->
          <div class="p-2 rounded-lg bg-muted/50">
            <div class="flex items-center justify-between mb-1">
              <span class="text-xs text-muted-foreground">完成率</span>
              <span class="text-sm font-semibold">{{ completionRate }}%</span>
            </div>
            <div class="w-full bg-muted rounded-full h-1.5">
              <div 
                class="bg-chart-5 h-1.5 rounded-full transition-all duration-300" 
                :style="{ width: `${completionRate}%` }"
              ></div>
            </div>
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

// 计算任务统计
const totalTasks = computed(() => store.tasks.length)

const urgentTasks = computed(() => 
  store.tasks.filter(task => task.priority === 'high').length
)

const completedTasks = computed(() => 
  store.tasks.filter(task => task.completed).length
)

const inProgressTasks = computed(() => 
  store.tasks.filter(task => !task.completed).length
)

const completionRate = computed(() => {
  if (totalTasks.value === 0) return 0
  return Math.round((completedTasks.value / totalTasks.value) * 100)
})
</script>
