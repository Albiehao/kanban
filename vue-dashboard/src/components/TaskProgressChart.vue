<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">任务进度</h3>
    
    <!-- 图例 -->
    <div class="flex flex-wrap gap-4 mb-4 text-sm">
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 bg-gray-200 rounded"></div>
        <span class="text-gray-600">空值</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 bg-yellow-400 rounded"></div>
        <span class="text-gray-600">未开始</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 bg-blue-500 rounded"></div>
        <span class="text-gray-600">进行中</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 bg-teal-500 rounded"></div>
        <span class="text-gray-600">已完成</span>
      </div>
    </div>

    <!-- 图表 -->
    <div class="space-y-4">
      <div v-for="category in categories" :key="category.name" class="space-y-2">
        <div class="text-sm text-gray-600">{{ category.name }}</div>
        <div class="flex gap-2">
          <!-- 未开始 -->
          <div class="flex-1 bg-gray-100 rounded h-8 flex items-center justify-center">
            <div class="w-full bg-yellow-400 rounded h-full flex items-center justify-center text-white text-xs font-medium">
              {{ category.notStarted }}
            </div>
          </div>
          <!-- 已完成 -->
          <div class="flex-1 bg-gray-100 rounded h-8 flex items-center justify-center">
            <div class="w-full bg-teal-500 rounded h-full flex items-center justify-center text-white text-xs font-medium">
              {{ category.completed }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

const categories = computed(() => {
  const tasks = store.tasks
  
  return [
    {
      name: '不重要不紧急',
      notStarted: tasks.filter(t => !t.completed && t.priority === 'low').length,
      completed: tasks.filter(t => t.completed && t.priority === 'low').length
    },
    {
      name: '重要紧急',
      notStarted: tasks.filter(t => !t.completed && t.priority === 'high').length,
      completed: tasks.filter(t => t.completed && t.priority === 'high').length
    },
    {
      name: '重要不紧急',
      notStarted: tasks.filter(t => !t.completed && t.priority === 'medium').length,
      completed: tasks.filter(t => t.completed && t.priority === 'medium').length
    },
    {
      name: '不重要紧急',
      notStarted: tasks.filter(t => !t.completed && t.priority === 'low').length,
      completed: tasks.filter(t => t.completed && t.priority === 'low').length
    }
  ]
})
</script>
