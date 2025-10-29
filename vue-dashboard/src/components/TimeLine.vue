<template>
  <Card class="timeline-container">
    <CardHeader>
      <CardTitle class="text-base">时间轴</CardTitle>
    </CardHeader>
    <CardContent class="p-4">
      <!-- 横向滚动容器 -->
      <div class="timeline-scroll-wrapper">
        <div class="timeline-content-wrapper" :style="{ width: `${timelineWidth}px` }">
           <div class="relative h-20 mb-4">
             <!-- Background grid lines - 只显示有任务的时间点 -->
             <div class="absolute inset-0 flex">
               <div
                 v-for="time in actualTimeMarks"
                 :key="`grid-${time}`"
                 class="absolute top-0 bottom-0 w-px bg-gray-200 dark:bg-gray-600 opacity-60"
                 :style="{ left: `${getActualGridPosition(time)}%` }"
               />
             </div>

             <!-- 当前时间指示线 -->
             <div
               v-if="currentTimePosition !== null"
               class="absolute top-0 bottom-0 w-0.5 bg-red-500 dark:bg-red-400 z-20"
               :style="{ left: `${currentTimePosition}%` }"
             />

             <!-- Task blocks -->
             <div
               v-for="task in timelineTasks"
               :key="task.id"
               :class="cn(
                 'absolute top-3 h-14 rounded-lg border-2',
                 'flex flex-col items-start justify-center px-1.5 py-0.5',
                 'transition-all duration-200 hover:shadow-lg hover:scale-[1.02] cursor-pointer',
                 'backdrop-blur-sm shadow-sm'
               )"
               :style="{
                 left: task.left,
                 width: task.width,
                 backgroundColor: task.color,
                 borderColor: task.borderColor,
                 minHeight: '56px'
               }"
               @click="showTaskDetails(task)"
             >
              <!-- 第一行：课程名称 -->
              <span class="font-semibold text-[10px] text-black dark:text-black truncate w-full leading-tight block">{{ task.title }}</span>
              <!-- 第二行：教师和教室 -->
              <span v-if="task.teacher || task.location" class="text-[8px] text-gray-700 dark:text-gray-800 mt-0.5 leading-tight truncate w-full block">
                {{ task.teacher || '' }}{{ task.teacher && task.location ? ' · ' : '' }}{{ task.location || '' }}
              </span>
              <!-- 第三行：时间段 -->
              <span class="text-[8px] text-gray-700 dark:text-gray-800 mt-0.5 leading-tight block">
                {{ task.startTime }}-{{ task.endTime }}
              </span>
             </div>
           </div>

           <!-- Time marks - 只显示实际任务的时间点 -->
           <div class="relative h-8 border-t-2 border-gray-200 dark:border-gray-600 pt-1.5">
             <div
               v-for="time in actualTimeMarks"
               :key="time"
               class="absolute flex flex-col items-center -translate-x-1/2"
               :style="{ left: `${getActualTimePosition(time)}%` }"
             >
               <div class="h-2 w-0.5 bg-gray-400 dark:bg-gray-500 mb-0.5 rounded-full" />
               <span class="text-[9px] font-medium text-gray-700 dark:text-white tabular-nums">
                 {{ formatTime(time) }}
               </span>
             </div>
           </div>
        </div>
      </div>
    </CardContent>

    <!-- 详情模态框 -->
    <Transition name="modal-fade">
      <div 
        v-if="showDetails" 
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 dark:bg-black/70"
        @click="closeDetails"
      >
        <Transition name="modal-scale">
          <div 
            v-if="showDetails"
            class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-4 p-6 modal-content"
            @click.stop
          >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-foreground">详情信息</h3>
          <button 
            @click="closeDetails"
            class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div v-if="selectedTask" class="space-y-3">
          <div>
            <span class="text-sm text-muted-foreground">名称</span>
            <p class="text-base font-medium text-foreground mt-1">{{ selectedTask.title }}</p>
          </div>
          
          <div v-if="selectedTask.teacher || selectedTask.location">
            <span class="text-sm text-muted-foreground">教师/教室</span>
            <p class="text-base text-foreground mt-1">
              {{ selectedTask.teacher || '' }}{{ selectedTask.teacher && selectedTask.location ? ' · ' : '' }}{{ selectedTask.location || '' }}
            </p>
          </div>
          
          <div>
            <span class="text-sm text-muted-foreground">时间</span>
            <p class="text-base text-foreground mt-1">{{ selectedTask.startTime }} - {{ selectedTask.endTime }}</p>
          </div>
          
          <div v-if="selectedTask.type === 'course'">
            <span class="text-sm text-muted-foreground">类型</span>
            <p class="text-base text-foreground mt-1">课程</p>
          </div>
          
          <div v-if="selectedTask.type === 'task'">
            <span class="text-sm text-muted-foreground">类型</span>
            <p class="text-base text-foreground mt-1">任务</p>
          </div>
          
          <div v-if="selectedTask.priority">
            <span class="text-sm text-muted-foreground">优先级</span>
            <p class="text-base text-foreground mt-1">
              {{ selectedTask.priority === 'high' ? '高' : selectedTask.priority === 'medium' ? '中' : '低' }}
            </p>
          </div>
        </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import { cn } from '@/utils'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

// 详情模态框状态
const selectedTask = ref<any>(null)
const showDetails = ref(false)

// 当前时间在时间轴上的位置
const currentTimePosition = computed(() => {
  const now = new Date()
  const currentHours = now.getHours() + now.getMinutes() / 60
  
  // 如果当前时间不在显示的范围内，返回 null
  if (currentHours < startHour.value || currentHours > endHour.value) {
    return null
  }
  
  const totalHours = endHour.value - startHour.value
  if (totalHours <= 0) return null
  
  const position = ((currentHours - startHour.value) / totalHours) * 100
  return Math.max(0, Math.min(100, position))
})

// 显示任务详情
const showTaskDetails = (task: any) => {
  selectedTask.value = task
  showDetails.value = true
  console.log('显示详情:', task)
}

// 关闭详情
const closeDetails = () => {
  showDetails.value = false
  selectedTask.value = null
}

// 将时间字符串转换为小时数（支持小数）
const timeToHours = (time: string): number => {
  const [hours, minutes] = time.split(':').map(Number)
  return hours + minutes / 60
}

// 格式化小时为时间字符串
const formatTime = (hours: number): string => {
  const h = Math.floor(hours)
  const m = Math.round((hours - h) * 60)
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`
}

// 格式化日期为本地时间字符串（避免时区问题）
const formatDateLocal = (date: Date): string => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 获取实际使用的时间范围 - 只扫描选中日期的数据
const getActualTimeRange = computed(() => {
  // 使用本地时间格式化，避免时区问题
  const dateStr = formatDateLocal(store.selectedDate)
  let minTime = 24
  let maxTime = 0

  // 只扫描选中日期的课程
  if (!store.courses || !Array.isArray(store.courses)) {
    return { minTime: 8, maxTime: 20 }
  }
  store.courses
    .filter(course => course.date === dateStr)
    .forEach(course => {
      const periods = parsePeriods(course.periods)
      if (periods) {
        const startTime = periodToTime(periods.start)
        const endTime = periodToTime(periods.end + 1)
        const startHours = timeToHours(startTime)
        const endHours = timeToHours(endTime)
        minTime = Math.min(minTime, startHours)
        maxTime = Math.max(maxTime, endHours)
      }
    })

  // 只扫描选中日期的任务
  store.tasks
    .filter(task => task.date === dateStr && task.time && !task.completed)
    .forEach(task => {
      const [startTime, endTime] = task.time.split('-')
      const startHours = timeToHours(startTime)
      const endHours = timeToHours(endTime)
      minTime = Math.min(minTime, startHours)
      maxTime = Math.max(maxTime, endHours)
    })

  // 如果没有数据，使用默认范围
  if (minTime === 24 && maxTime === 0) {
    minTime = 8
    maxTime = 20
  } else {
    // 添加一些边界
    minTime = Math.max(0, Math.floor(minTime) - 1)
    maxTime = Math.ceil(maxTime) + 1
  }

  return { minTime, maxTime }
})

// 时间范围
const startHour = computed(() => getActualTimeRange.value.minTime)
const endHour = computed(() => getActualTimeRange.value.maxTime)

// 获取实际的时间刻度（只包含任务的时间点）
const actualTimeMarks = computed(() => {
  const marks = new Set<number>()
  
  // 添加所有任务的时间点
  timelineTasks.value.forEach(task => {
    marks.add(timeToHours(task.startTime))
    marks.add(timeToHours(task.endTime))
  })

  return Array.from(marks).sort((a, b) => a - b)
})

// 计算时间轴宽度 - 高度压缩
const timelineWidth = computed(() => {
  const totalHours = endHour.value - startHour.value
  // 每个小时40px，非常紧凑
  const width = totalHours * 40
  // 确保最小宽度
  return Math.max(600, width)
})

// 计算实际网格位置
const getActualGridPosition = (time: number) => {
  if (endHour.value === startHour.value) return 0
  const totalHours = endHour.value - startHour.value
  const position = ((time - startHour.value) / totalHours) * 100
  return Math.max(0, Math.min(100, position))
}

// 计算实际时间标记位置
const getActualTimePosition = (time: number) => {
  if (endHour.value === startHour.value) return 50
  const totalHours = endHour.value - startHour.value
  const position = ((time - startHour.value) / totalHours) * 100
  return Math.max(0, Math.min(100, position))
}

// 节次到时间的映射 - 徐海学院作息时间表
const periodToTime = (period: number) => {
  const timeSlots: Record<number, string> = {
    // 上午
    1: '08:00',   // 第1节 8:00-8:40
    2: '08:45',   // 第2节 8:45-9:25
    3: '09:45',   // 第3节 9:45-10:25
    4: '10:30',   // 第4节 10:30-11:10
    5: '11:15',   // 第5节 11:15-11:55
    // 下午
    6: '14:00',   // 第6节 14:00-14:40
    7: '14:45',   // 第7节 14:45-15:25
    8: '15:45',   // 第8节 15:45-16:25
    9: '16:30',   // 第9节 16:30-17:10
    10: '17:15',  // 第10节 17:15-17:55
    // 晚上
    11: '19:00',  // 第11节 19:00-19:40
    12: '19:45',  // 第12节 19:45-20:25
    13: '20:35',  // 第13节 20:35-21:15
    14: '21:20'   // 第14节 21:20-22:00
  }
  return timeSlots[period] || '08:00'
}

// 解析节次字符串
const parsePeriods = (periods: string) => {
  const match = periods.match(/(\d+)-(\d+)节/)
  if (!match) return null
  const start = parseInt(match[1])
  const end = parseInt(match[2])
  return { start, end }
}

// 生成任务数据
const timelineTasks = computed(() => {
  // 使用本地时间格式化，避免时区问题
  const dateStr = formatDateLocal(store.selectedDate)
  const tasks: any[] = []

  // 添加课程
  if (!store.courses || !Array.isArray(store.courses)) {
    return tasks
  }
  store.courses
    .filter(course => course.date === dateStr)
    .forEach(course => {
      const periods = parsePeriods(course.periods)
      if (periods) {
        const startTime = periodToTime(periods.start)
        const endTime = periodToTime(periods.end + 1)
        
        const taskStart = timeToHours(startTime)
        const taskEnd = timeToHours(endTime)
        const totalHours = endHour.value - startHour.value

        if (totalHours > 0) {
          const left = ((taskStart - startHour.value) / totalHours) * 100
          const width = ((taskEnd - taskStart) / totalHours) * 100

          // 根据节次分配颜色
          const colors = ['#e0f2fe', '#ddd6fe', '#fef3c7', '#d1fae5', '#fecaca']
          const color = colors[(periods.start - 1) % 5]

          tasks.push({
            id: `course-${course.date}-${course.periods}`,
            title: course.name || '未命名课程', // 使用 course.name 而不是 course.course_name
            startTime,
            endTime,
            left: `${Math.max(0, Math.min(100, left))}%`,
            width: `${Math.max(0, Math.min(100, width))}%`,
            color,
            borderColor: 'transparent',
            teacher: course.teacher,
            location: course.location // 使用 course.location 而不是 course.classroom
          })
        }
      }
    })

  // 添加任务
  store.tasks
    .filter(task => task.date === dateStr && task.time && !task.completed)
    .forEach(task => {
      const [startTime, endTime] = task.time.split('-')
      
      const taskStart = timeToHours(startTime)
      const taskEnd = timeToHours(endTime)
      const totalHours = endHour.value - startHour.value

      if (totalHours > 0) {
        const left = ((taskStart - startHour.value) / totalHours) * 100
        const width = ((taskEnd - taskStart) / totalHours) * 100

        // 任务颜色根据优先级
        let color = '#e0f2fe'
        if (task.priority === 'high') color = '#fecaca'
        if (task.priority === 'medium') color = '#fef3c7'
        if (task.priority === 'low') color = '#d1fae5'

        tasks.push({
          id: `task-${task.id}`,
          title: task.title,
          startTime,
          endTime,
          left: `${Math.max(0, Math.min(100, left))}%`,
          width: `${Math.max(0, Math.min(100, width))}%`,
          color,
          borderColor: 'transparent'
        })
      }
    })

  return tasks.sort((a, b) => parseFloat(a.left) - parseFloat(b.left))
})
</script>

<style scoped>
.timeline-container {
  @apply flex flex-col;
}

.timeline-scroll-wrapper {
  @apply overflow-x-auto overflow-y-hidden;
  width: 100%;
}

/* 自定义滚动条样式 */
.timeline-scroll-wrapper::-webkit-scrollbar {
  height: 6px; /* 滚动条高度 */
}

.timeline-scroll-wrapper::-webkit-scrollbar-track {
  @apply bg-gray-100 dark:bg-gray-800 rounded-full;
}

.timeline-scroll-wrapper::-webkit-scrollbar-thumb {
  @apply bg-gray-400 dark:bg-gray-600 rounded-full;
}

.timeline-scroll-wrapper::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-500 dark:bg-gray-500;
}

.timeline-content-wrapper {
  @apply relative;
  min-height: 120px;
}

/* 模态框动画 */
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
  transform: scale(0.8);
  opacity: 0;
}

.modal-content {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: scale(0.9) translateY(-20px);
    opacity: 0;
  }
  to {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

/* 当前时间指示线脉冲动画 */
@keyframes pulse-dot {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>

