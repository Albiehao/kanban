<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">任务紧急程度</h3>
    
    <!-- 图表 -->
    <div class="space-y-4">
      <div v-for="(level, index) in urgencyLevels" :key="level.name" class="space-y-2">
        <div class="flex items-center gap-3">
          <!-- 图标 -->
          <div :class="`w-6 h-6 rounded-full flex items-center justify-center ${level.color}`">
            <Flag class="w-4 h-4 text-white" />
          </div>
          <!-- 数值 -->
          <div class="text-2xl font-bold text-gray-900">{{ level.count }}</div>
        </div>
        <!-- 进度条 -->
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div 
            :class="`h-2 rounded-full ${level.bgColor}`"
            :style="{ width: `${(level.count / maxCount) * 100}%` }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Flag } from 'lucide-vue-next'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

const urgencyLevels = computed(() => {
  const tasks = store.tasks
  
  return [
    {
      name: '低优先级',
      count: tasks.filter(t => t.priority === 'low').length,
      color: 'bg-yellow-400',
      bgColor: 'bg-yellow-400'
    },
    {
      name: '中优先级',
      count: tasks.filter(t => t.priority === 'medium').length,
      color: 'bg-orange-400',
      bgColor: 'bg-orange-400'
    },
    {
      name: '高优先级',
      count: tasks.filter(t => t.priority === 'high').length,
      color: 'bg-red-500',
      bgColor: 'bg-red-500'
    },
    {
      name: '紧急',
      count: tasks.filter(t => t.priority === 'high').length,
      color: 'bg-pink-400',
      bgColor: 'bg-pink-400'
    }
  ]
})

const maxCount = computed(() => {
  return Math.max(...urgencyLevels.value.map(level => level.count))
})
</script>
