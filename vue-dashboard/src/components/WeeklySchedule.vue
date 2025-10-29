<template>
  <Card class="schedule-container flex flex-col overflow-hidden">
    <CardHeader class="pb-3 flex-shrink-0">
      <div class="flex items-center justify-between">
        <CardTitle class="text-base">课程表</CardTitle>
        <div class="flex gap-1">
          <Button 
            variant="outline" 
            size="sm" 
            class="h-7 text-xs" 
            @click="refreshCourseData"
            :disabled="isRefreshing"
          >
            <RefreshCw :class="['h-3 w-3', isRefreshing && 'animate-spin']" />
            <span v-if="!isRefreshing" class="ml-1">刷新</span>
          </Button>
          <Button variant="outline" size="sm" class="h-7 text-xs" @click="toggleView">
            {{ viewMode === 'week' ? '日视图' : '周视图' }}
          </Button>
        </div>
      </div>
    </CardHeader>
    <CardContent class="p-0 flex-1 min-h-0 overflow-hidden">
      <!-- 周视图 -->
      <div v-if="viewMode === 'week'" class="flex flex-col h-full">
        <!-- 表头 - 固定在顶部 -->
        <div class="sticky top-0 z-10 bg-background border-b border-border">
          <div class="flex">
            <!-- 月份列 - 固定宽度 -->
            <div class="flex flex-col items-center justify-center py-1 px-2 text-[10px] text-muted-foreground w-14 shrink-0">
              <span class="leading-tight">{{ currentMonth }}</span>
              <span class="leading-tight">月</span>
           </div>
            <!-- 星期和日期列 - 平均分配 -->
            <div class="flex flex-1">
           <div
                v-for="(dayData, index) in weekDays"
             :key="dayData.date"
             :class="cn(
                  'flex flex-col items-center justify-center py-1 text-[10px] cursor-pointer transition-colors flex-1',
                  'hover:bg-muted/50',
                  selectedDayIndex === index && 'text-primary font-semibold'
                )"
                @click="selectDay(index)"
              >
                <span class="text-muted-foreground">{{ dayData.day }}</span>
                <span
                  :class="cn(
                    'mt-0.5 text-xs',
                    selectedDayIndex === index &&
                      'bg-primary text-primary-foreground rounded-full w-5 h-5 flex items-center justify-center'
                  )"
                >
                  {{ dayData.dateNum }}
                </span>
              </div>
            </div>
           </div>
         </div>

        <!-- 课程网格 - 可滚动 -->
        <div class="flex-1 overflow-auto scrollbar-hide">
          <div class="relative">
            <!-- 时间轴列 - 固定在左侧 -->
            <div class="absolute left-0 top-0 w-14 z-10 bg-background">
              <div
                v-for="(slot, index) in timeSlots"
                :key="index"
                class="flex flex-col items-center justify-start py-0.5 text-[10px] text-muted-foreground border-b border-border/50"
                :style="{ height: `${slotHeight}px` }"
              >
                <span class="font-medium text-[11px]">{{ slot.period }}</span>
                <span class="text-[9px] mt-0.5 leading-tight">{{ slot.start }}</span>
                <span class="text-[9px] leading-tight">{{ slot.end }}</span>
              </div>
            </div>

            <!-- 课程网格 - 使用 table 布局确保对齐 -->
            <div class="ml-14 relative">
              <div class="grid grid-cols-7">
             <div
                  v-for="(dayData, dayIndex) in weekDays"
               :key="dayData.date"
                  class="relative"
                >
                  <!-- 网格线 -->
                  <div
                    v-for="(slot, slotIndex) in timeSlots"
                    :key="slotIndex"
                    class="border-b border-border/50"
                    :style="{ height: `${slotHeight}px` }"
                  />
                 </div>
               </div>

              <!-- 课程卡片 - 使用 grid 布局 -->
              <template v-for="course in courses" :key="course.id">
                <div
                  v-if="course.startPeriod && course.duration"
                  class="absolute cursor-pointer"
                  :style="{
                    left: `${(100 / 7) * course.dayIndex}%`,
                    top: `${(course.startPeriod - 1) * slotHeight}px`,
                    width: `calc(${100 / 7}% - 2px)`,
                    height: `${course.duration * slotHeight - 4}px`,
                    padding: '2px'
                  }"
                  @click="showCourseDetails(course)"
                >
                  <CourseCard :course="course" :highlighted="course.dayIndex === selectedDayIndex" />
                </div>
              </template>
             </div>
          </div>
        </div>
      </div>

      <!-- 日视图 -->
      <div v-else class="p-4">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-medium">{{ formatDate(selectedDate) }} 课程</h3>
          </div>
        <div v-if="dayCourses.length === 0" class="text-center py-8 text-sm text-muted-foreground">
          该日期暂无课程安排
        </div>
        <div v-else class="space-y-3">
        <div
            v-for="course in dayCourses"
          :key="course.id"
            class="flex items-start gap-3 p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors cursor-pointer"
          @click="showCourseDetails(course)"
        >
            <div :class="`w-1 h-full rounded-full ${course.color} min-h-[60px]`" />
          <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2 mb-2">
                <h4 class="font-semibold text-foreground">{{ course.name }}</h4>
                <Badge variant="secondary" class="text-xs shrink-0">
                  已安排
                </Badge>
              </div>
              <div class="flex flex-col gap-1 text-sm text-muted-foreground">
              <div class="flex items-center gap-2">
                <Clock class="h-3.5 w-3.5" />
                <span>{{ course.time }}</span>
              </div>
              <div class="flex items-center gap-2">
                <MapPin class="h-3.5 w-3.5" />
                <span>{{ course.location }}</span>
              </div>
              <div v-if="course.teacher" class="flex items-center gap-2">
                  <span>教师: {{ course.teacher }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </CardContent>

    <!-- 课程详情对话框 -->
    <Dialog v-model:open="showCourseDetailsDialog">
      <DialogContent v-if="selectedCourse" class="sm:max-w-md">
        <DialogHeader>
          <DialogTitle class="text-xl">{{ selectedCourse.name }}</DialogTitle>
        </DialogHeader>
        <Transition name="fade">
          <div v-if="selectedCourse" class="space-y-4 py-4">
            <div class="flex items-center gap-3 text-sm">
              <div class="w-20 font-medium text-muted-foreground">教师：</div>
              <div class="flex-1">{{ selectedCourse.teacher || '暂无' }}</div>
            </div>
            <div class="flex items-center gap-3 text-sm">
              <div class="w-20 font-medium text-muted-foreground">时间：</div>
              <div class="flex-1">{{ selectedCourse.time || '暂无' }}</div>
            </div>
            <div class="flex items-center gap-3 text-sm">
              <div class="w-20 font-medium text-muted-foreground">地点：</div>
              <div class="flex-1">{{ selectedCourse.location || '暂无' }}</div>
            </div>
            <div class="flex items-center gap-3 text-sm">
              <div class="w-20 font-medium text-muted-foreground">节次：</div>
              <div class="flex-1">{{ selectedCourse.periods || '暂无' }}</div>
        </div>
          </div>
        </Transition>
        <DialogFooter>
          <Button variant="outline" @click="showCourseDetailsDialog = false">关闭</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
    
    <!-- 消息提示弹框 -->
    <MessageModal
      v-model:visible="showMessageModal"
      :type="messageModalType"
      :title="messageModalTitle"
      :message="messageModalMessage"
    />
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { cn } from '@/utils'
import { useDashboardStore, type Course } from '@/stores/dashboard'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Dialog from '@/components/ui/Dialog.vue'
import DialogContent from '@/components/ui/DialogContent.vue'
import DialogHeader from '@/components/ui/DialogHeader.vue'
import DialogTitle from '@/components/ui/DialogTitle.vue'
import DialogFooter from '@/components/ui/DialogFooter.vue'
import { RefreshCw, Clock, MapPin } from 'lucide-vue-next'
import CourseCard from './CourseCard.vue'
import Badge from '@/components/ui/Badge.vue'
import MessageModal from '@/components/ui/MessageModal.vue'

const store = useDashboardStore()

const viewMode = ref<'week' | 'day'>('week')
const isRefreshing = ref(false)
const showCourseDetailsDialog = ref(false)
const selectedCourse = ref<Course | null>(null)

// 消息弹框状态
const showMessageModal = ref(false)
const messageModalType = ref<'success' | 'error' | 'warning' | 'info'>('error')
const messageModalTitle = ref('错误')
const messageModalMessage = ref('')

const showMessage = (type: 'success' | 'error' | 'warning' | 'info', title: string, message: string) => {
  messageModalType.value = type
  messageModalTitle.value = title
  messageModalMessage.value = message
  showMessageModal.value = true
}

// 将日期格式化为 YYYY-MM-DD 字符串（本地时间）
const formatDateLocal = (date: Date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 徐海学院作息时间表
const timeSlots = [
  { period: 1, start: '08:00', end: '08:40' },
  { period: 2, start: '08:45', end: '09:25' },
  { period: 3, start: '09:45', end: '10:25' },
  { period: 4, start: '10:30', end: '11:10' },
  { period: 5, start: '11:15', end: '11:55' },
  { period: 6, start: '14:00', end: '14:40' },
  { period: 7, start: '14:45', end: '15:25' },
  { period: 8, start: '15:45', end: '16:25' },
  { period: 9, start: '16:30', end: '17:10' },
  { period: 10, start: '17:15', end: '17:55' },
  { period: 11, start: '19:00', end: '19:40' },
  { period: 12, start: '19:45', end: '20:25' },
  { period: 13, start: '20:35', end: '21:15' },
  { period: 14, start: '21:20', end: '22:00' }
]

const slotHeight = 45 // 每个时间段的高度（像素）- 已压缩

// 当前月份 - 使用选中日期所在周的第一天（周一）的月份
const currentMonth = computed(() => {
  if (weekDays.value.length > 0) {
    const mondayDate = new Date(weekDays.value[0].date)
    return mondayDate.getMonth() + 1
  }
  const now = new Date()
  return now.getMonth() + 1
})

// 获取本周的日期信息
// 日期常量
const dayNames = ['一', '二', '三', '四', '五', '六', '日']

const weekDays = computed(() => {
  const selectedDate = store.selectedDate
  const currentDay = selectedDate.getDay() // 0=周日, 1=周一, ..., 6=周六
  const mondayOffset = currentDay === 0 ? -6 : 1 - currentDay // 计算到周一的偏移
  const monday = new Date(selectedDate)
  monday.setDate(selectedDate.getDate() + mondayOffset)
  
  const weekDays = []
  
  for (let i = 0; i < 7; i++) {
    const date = new Date(monday)
    date.setDate(monday.getDate() + i)
    const actualDay = date.getDay() // 0=周日, 1=周一, ..., 6=周六
    const dayName = dayNames[actualDay === 0 ? 6 : actualDay - 1]
    
    weekDays.push({
      date: formatDateLocal(date),
      day: dayName,
      dateNum: date.getDate()
    })
  }
  
  return weekDays
})

// 计算选中的日期索引 - 与 store.selectedDate 同步（必须在 weekDays 之后定义）
const selectedDayIndex = computed(() => {
  const selectedDateStr = formatDateLocal(store.selectedDate)
  const index = weekDays.value.findIndex(day => day.date === selectedDateStr)
  return index >= 0 ? index : 2 // 如果找不到，默认今天
})

// 获取当前选中的日期
const selectedDate = computed(() => {
  return weekDays.value[selectedDayIndex.value].date
})

// 获取今日课程（日视图）
const dayCourses = computed(() => {
  return store.courses.filter(course => course.date === selectedDate.value)
})

// 课程列表（周视图）- 需要转换格式
const courses = computed<Array<Course & { dayIndex: number; startPeriod: number; duration: number }>>(() => {
  if (!store.courses || !Array.isArray(store.courses)) {
    return []
  }
  return store.courses
    .filter(course => {
      // 使用日期字符串比较，避免时区问题
      const courseDateStr = course.date
      const weekStartStr = weekDays.value[0].date
      const weekEndStr = weekDays.value[6].date
      
      return courseDateStr >= weekStartStr && courseDateStr <= weekEndStr
    })
    .map(course => {
      // 解析时间信息以获取开始节次和持续节次
      const { startPeriod, duration } = parseTimeSlots(course.timeSlots || [])
      
      // 通过查找匹配的日期来确定 dayIndex（0-6，0=周一）
      const courseDateStr = course.date
      let dayIndex = 0
      
      for (let i = 0; i < weekDays.value.length; i++) {
        if (weekDays.value[i].date === courseDateStr) {
          dayIndex = i
          break
        }
      }
      
      return {
        ...course,
        dayIndex,
        startPeriod,
        duration
      }
    })
})

// 解析时间段获取开始节次和持续节次
const parseTimeSlots = (courseTimeSlots: string[]) => {
  if (!courseTimeSlots || courseTimeSlots.length === 0) {
    return { startPeriod: 1, duration: 1 }
  }
  
  // 根据时间段字符串查找对应的节次索引
  const firstSlot = courseTimeSlots[0]
  let startPeriod = 1
  
  // 在预定义的 timeSlots 数组中查找匹配的时间段
  const slotIndex = timeSlots.findIndex(slot => {
    const slotStr = `${slot.start}-${slot.end}`
    return slotStr === firstSlot
  })
  
  if (slotIndex >= 0) {
    startPeriod = slotIndex + 1
  } else {
    // 如果没有找到，尝试从开始时间推断
    const [start] = firstSlot.split('-')
    const matchingIndex = timeSlots.findIndex(slot => slot.start === start)
    if (matchingIndex >= 0) {
      startPeriod = matchingIndex + 1
    }
  }
  
  return {
    startPeriod,
    duration: courseTimeSlots.length
  }
}

// 切换视图
const toggleView = () => {
  viewMode.value = viewMode.value === 'week' ? 'day' : 'week'
}

// 选择某一天
const selectDay = (index: number) => {
  // 更新 store 的选中日期，实现双向绑定
  const selectedDateStr = weekDays.value[index].date
  // 解析日期字符串 YYYY-MM-DD，使用本地时间避免时区问题
  const [year, month, day] = selectedDateStr.split('-').map(Number)
  const newDate = new Date(year, month - 1, day)
  newDate.setHours(0, 0, 0, 0) // 重置为本地时间的午夜
  store.setSelectedDate(newDate)
}

// 刷新课程数据（静默加载，不显示加载提示）
const refreshCourseData = async () => {
  if (isRefreshing.value) return
  
  isRefreshing.value = true
  try {
    await store.loadCourses()
    // 静默加载完成，不显示提示
  } catch (error) {
    console.error('刷新课程数据失败:', error)
    // 只在失败时显示错误提示
    showMessage('error', '错误', '刷新课程数据失败，请稍后重试')
  } finally {
    isRefreshing.value = false
  }
}

// 显示课程详情
const showCourseDetails = (course: Course) => {
  selectedCourse.value = course
  showCourseDetailsDialog.value = true
}

// 格式化日期
const formatDate = (date: string) => {
  const d = new Date(date)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

// 监听 store.selectedDate 的变化，当日期改变时重新加载课程数据
watch(() => store.selectedDate, async (newDate, oldDate) => {
  // 如果日期发生了实质性变化（不是同一周内）
  if (oldDate) {
    const oldDateStr = oldDate.toISOString().split('T')[0]
    const newDateStr = newDate.toISOString().split('T')[0]
    
    // 计算是否是同一周
    const oldWeek = getWeekRange(oldDate)
    const newWeek = getWeekRange(newDate)
    
    // 如果不在同一周，重新加载课程数据
    if (oldWeek.start !== newWeek.start || oldWeek.end !== newWeek.end) {
      if (!isRefreshing.value) {
        await refreshCourseData()
      }
    }
  }
}, { immediate: false })

// 获取日期所在周的范围
const getWeekRange = (date: Date) => {
  const currentDay = date.getDay()
  const mondayOffset = currentDay === 0 ? -6 : 1 - currentDay
  const monday = new Date(date)
  monday.setDate(date.getDate() + mondayOffset)
  const sunday = new Date(monday)
  sunday.setDate(monday.getDate() + 6)
  
  return {
    start: monday.toISOString().split('T')[0],
    end: sunday.toISOString().split('T')[0]
  }
}

// 组件挂载
onMounted(() => {
  // 自动加载课程数据
  if (store.courses.length === 0) {
    refreshCourseData()
  }
})
</script>

<style scoped>
.schedule-container {
  height: 510px !important;
  max-height: 550px !important;
  min-height: 460px !important;
}

/* 隐藏滚动条 */
.scrollbar-hide {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.scrollbar-hide::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

/* 内容淡入动画 */
.fade-enter-active {
  transition: all 0.4s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-enter-to {
  opacity: 1;
  transform: translateY(0);
}
</style>
