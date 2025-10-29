<template>
  <div class="bg-white rounded-lg shadow-sm">
    <!-- 表格头部 -->
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">任务明细</h3>
        <div class="flex items-center gap-3">
          <button class="px-3 py-1.5 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">
            + 添加记录
          </button>
          <button class="px-3 py-1.5 border border-gray-300 text-gray-700 text-sm rounded hover:bg-gray-50">
            筛选
          </button>
          <button class="px-3 py-1.5 border border-gray-300 text-gray-700 text-sm rounded hover:bg-gray-50">
            1 分组
          </button>
          <button class="px-3 py-1.5 border border-gray-300 text-gray-700 text-sm rounded hover:bg-gray-50">
            排序
          </button>
          <button class="px-3 py-1.5 border border-gray-300 text-gray-700 text-sm rounded hover:bg-gray-50">
            行高
          </button>
        </div>
      </div>
    </div>

    <!-- 表格内容 -->
    <div class="p-6">
      <!-- 表头 -->
      <div class="grid grid-cols-12 gap-4 pb-3 border-b border-gray-200 text-sm text-gray-600 font-medium">
        <div class="col-span-1">
          <input type="checkbox" class="rounded border-gray-300" />
        </div>
        <div class="col-span-1">
          <Lock class="w-4 h-4" />
        </div>
        <div class="col-span-6">任务名称</div>
        <div class="col-span-2">任务标签</div>
        <div class="col-span-2">状态</div>
      </div>

      <!-- 任务分组 -->
      <div class="mt-4">
        <!-- 未开始任务 -->
        <div class="mb-4">
          <div 
            class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-2 rounded"
            @click="toggleGroup('notStarted')"
          >
            <ChevronRight 
              :class="`w-4 h-4 transition-transform ${expandedGroups.notStarted ? 'rotate-90' : ''}`" 
            />
            <span class="text-sm text-gray-600">未...</span>
            <span class="text-sm text-gray-500">{{ notStartedTasks.length }}条记录</span>
          </div>
          
          <div v-if="expandedGroups.notStarted" class="ml-6 space-y-2 mt-2">
            <div 
              v-for="task in notStartedTasks" 
              :key="task.id"
              class="grid grid-cols-12 gap-4 py-3 hover:bg-gray-50 rounded"
            >
              <div class="col-span-1 flex items-center">
                <input type="checkbox" class="rounded border-gray-300" />
              </div>
              <div class="col-span-1 flex items-center">
                <Lock class="w-4 h-4 text-gray-400" />
              </div>
              <div class="col-span-6 text-sm text-gray-900">{{ task.title }}</div>
              <div class="col-span-2">
                <span :class="getPriorityBadgeClass(task.priority)">
                  {{ getPriorityText(task.priority) }}
                </span>
              </div>
              <div class="col-span-2">
                <span class="text-sm text-gray-600">未开始</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 进行中任务 -->
        <div class="mb-4">
          <div 
            class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-2 rounded"
            @click="toggleGroup('inProgress')"
          >
            <ChevronRight 
              :class="`w-4 h-4 transition-transform ${expandedGroups.inProgress ? 'rotate-90' : ''}`" 
            />
            <span class="text-sm text-gray-600">进行中</span>
            <span class="text-sm text-gray-500">{{ inProgressTasks.length }}条记录</span>
          </div>
          
          <div v-if="expandedGroups.inProgress" class="ml-6 space-y-2 mt-2">
            <div 
              v-for="task in inProgressTasks" 
              :key="task.id"
              class="grid grid-cols-12 gap-4 py-3 hover:bg-gray-50 rounded"
            >
              <div class="col-span-1 flex items-center">
                <input type="checkbox" class="rounded border-gray-300" />
              </div>
              <div class="col-span-1 flex items-center">
                <Lock class="w-4 h-4 text-gray-400" />
              </div>
              <div class="col-span-6 text-sm text-gray-900">{{ task.title }}</div>
              <div class="col-span-2">
                <span :class="getPriorityBadgeClass(task.priority)">
                  {{ getPriorityText(task.priority) }}
                </span>
              </div>
              <div class="col-span-2">
                <span class="text-sm text-blue-600">进行中</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 已完成任务 -->
        <div class="mb-4">
          <div 
            class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-2 rounded"
            @click="toggleGroup('completed')"
          >
            <ChevronRight 
              :class="`w-4 h-4 transition-transform ${expandedGroups.completed ? 'rotate-90' : ''}`" 
            />
            <span class="text-sm text-gray-600">已完成</span>
            <span class="text-sm text-gray-500">{{ completedTasks.length }}条记录</span>
          </div>
          
          <div v-if="expandedGroups.completed" class="ml-6 space-y-2 mt-2">
            <div 
              v-for="task in completedTasks" 
              :key="task.id"
              class="grid grid-cols-12 gap-4 py-3 hover:bg-gray-50 rounded"
            >
              <div class="col-span-1 flex items-center">
                <input type="checkbox" class="rounded border-gray-300" />
              </div>
              <div class="col-span-1 flex items-center">
                <Lock class="w-4 h-4 text-gray-400" />
              </div>
              <div class="col-span-6 text-sm text-gray-900 line-through">{{ task.title }}</div>
              <div class="col-span-2">
                <span :class="getPriorityBadgeClass(task.priority)">
                  {{ getPriorityText(task.priority) }}
                </span>
              </div>
              <div class="col-span-2">
                <span class="text-sm text-green-600">已完成</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ChevronRight, Lock } from 'lucide-vue-next'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

const expandedGroups = ref({
  notStarted: true,
  inProgress: false,
  completed: false
})

const toggleGroup = (group: keyof typeof expandedGroups.value) => {
  expandedGroups.value[group] = !expandedGroups.value[group]
}

const notStartedTasks = computed(() => 
  store.tasks.filter(task => !task.completed)
)

const inProgressTasks = computed(() => 
  store.tasks.filter(task => !task.completed)
)

const completedTasks = computed(() => 
  store.tasks.filter(task => task.completed)
)

const getPriorityText = (priority: string) => {
  const priorityMap = {
    'low': '不重要不紧急',
    'medium': '重要不紧急',
    'high': '重要紧急'
  }
  return priorityMap[priority as keyof typeof priorityMap] || priority
}

const getPriorityBadgeClass = (priority: string) => {
  const classMap = {
    'low': 'px-2 py-1 text-xs rounded-full bg-green-100 text-green-800',
    'medium': 'px-2 py-1 text-xs rounded-full bg-orange-100 text-orange-800',
    'high': 'px-2 py-1 text-xs rounded-full bg-red-100 text-red-800'
  }
  return classMap[priority as keyof typeof classMap] || 'px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-800'
}
</script>
