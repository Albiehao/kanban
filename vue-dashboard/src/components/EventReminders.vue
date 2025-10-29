<template>
  <Card>
    <CardHeader>
      <CardTitle class="text-base">事件提醒</CardTitle>
    </CardHeader>
    <CardContent class="space-y-2">
      <div
        v-for="reminder in reminders"
        :key="reminder.id"
        class="flex items-start gap-2 p-2 rounded-lg bg-muted/50 dark:bg-gray-800 hover:bg-muted dark:hover:bg-gray-700 transition-colors"
      >
        <div :class="`w-1.5 h-1.5 rounded-full mt-1.5 ${reminder.color}`" />
        <div class="flex-1 min-w-0">
          <p class="text-xs font-medium dark:text-gray-100">{{ reminder.title }}</p>
          <p class="text-xs text-muted-foreground dark:text-gray-300">{{ reminder.time }}</p>
        </div>
        <Badge :variant="reminder.priority === 'high' ? 'destructive' : 'secondary'" class="text-xs">
          {{ reminder.priority === 'high' ? '紧急' : '普通' }}
        </Badge>
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
import Badge from '@/components/ui/Badge.vue'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

// 将任务转换为提醒格式 - 只显示未完成且有提醒标志的任务
const reminders = computed(() => {
  return store.tasks
    .filter(task => task.hasReminder === true && !task.completed)
    .map((task, index) => {
      // 计算相对时间
      const taskDate = new Date(task.date)
      const today = new Date()
      const diffDays = Math.ceil((taskDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
      
      let timeStr = ''
      if (diffDays === 0) timeStr = '今天'
      else if (diffDays === 1) timeStr = '明天'
      else if (diffDays === 2) timeStr = '2天后'
      else if (diffDays > 0) timeStr = `${diffDays}天后`
      else if (diffDays === -1) timeStr = '昨天'
      else timeStr = `${Math.abs(diffDays)}天前`
      
      // 显示完整日期时间
      if (task.time) {
        const time = task.time.split('-')[0]  // 取开始时间
        timeStr = `${task.date} ${time}`
      } else {
        timeStr = `${task.date} ${timeStr}`
      }
      
      const colors = ['bg-destructive', 'bg-chart-5', 'bg-chart-2', 'bg-chart-3', 'bg-chart-4']
      
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
