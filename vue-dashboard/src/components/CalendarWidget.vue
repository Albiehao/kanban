<template>
  <Card class="compact-calendar flex flex-col max-h-80">
    <CardHeader class="pb-1 flex-shrink-0">
      <div class="flex items-center justify-between">
        <CardTitle class="text-xs">
          {{ year }}年 {{ monthNames[month] }}
        </CardTitle>
        <div class="flex gap-0.5">
          <Button variant="ghost" size="icon" class="h-5 w-5" @click="previousMonth">
            <ChevronLeft class="h-2.5 w-2.5" />
          </Button>
          <Button variant="ghost" size="icon" class="h-5 w-5" @click="nextMonth">
            <ChevronRight class="h-2.5 w-2.5" />
          </Button>
        </div>
      </div>
    </CardHeader>
    <CardContent class="p-1 flex-1 overflow-y-auto scrollbar-hide">
      <div class="grid grid-cols-7 gap-0.5">
        <div
          v-for="day in weekDays"
          :key="day"
          class="text-center text-xs font-medium text-muted-foreground dark:text-gray-400 pb-0.5"
        >
          {{ day }}
        </div>
        <div
          v-for="i in firstDay"
          :key="`empty-${i}`"
          class="h-6"
        />
        <button
          v-for="day in daysInMonth"
          :key="day"
          :class="cn(
            'h-6 rounded text-xs font-medium transition-colors relative flex items-center justify-center',
            'hover:bg-accent hover:text-accent-foreground dark:hover:bg-gray-800',
            isSelected(day) && 'bg-primary text-primary-foreground hover:bg-primary/90',
            isToday(day) && !isSelected(day) && 'ring-1 ring-primary ring-inset',
            !isSelected(day) && 'text-foreground dark:text-gray-300'
          )"
          @click="handleDateClick(day)"
        >
          {{ day }}
          <span
            v-if="hasEvent(day) && !isSelected(day)"
            class="absolute bottom-0 left-1/2 -translate-x-1/2 h-0.5 w-0.5 rounded-full bg-chart-1"
          />
        </button>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Button from '@/components/ui/Button.vue'
import { cn } from '@/utils'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

const currentDate = ref(new Date())
const year = computed(() => currentDate.value.getFullYear())
const month = computed(() => currentDate.value.getMonth())

const firstDay = computed(() => new Date(year.value, month.value, 1).getDay())
const daysInMonth = computed(() => new Date(year.value, month.value + 1, 0).getDate())
const today = computed(() => new Date().getDate())
const isCurrentMonth = computed(() => 
  new Date().getMonth() === month.value && new Date().getFullYear() === year.value
)

const selectedDay = computed(() => store.selectedDate.getDate())
const isSelectedMonth = computed(() => 
  store.selectedDate.getMonth() === month.value && store.selectedDate.getFullYear() === year.value
)

const monthNames = [
  "一月", "二月", "三月", "四月", "五月", "六月",
  "七月", "八月", "九月", "十月", "十一月", "十二月"
]
const weekDays = ["日", "一", "二", "三", "四", "五", "六"]

// 监听 store.selectedDate 的变化，如果选中的日期不在当前显示的月份，自动切换月份
watch(() => store.selectedDate, (newDate) => {
  const selectedMonth = newDate.getMonth()
  const selectedYear = newDate.getFullYear()
  
  // 如果选中的日期不在当前显示的月份/年份，切换到对应的月份
  if (selectedMonth !== month.value || selectedYear !== year.value) {
    currentDate.value = new Date(selectedYear, selectedMonth, 1)
  }
}, { immediate: true })

const previousMonth = () => {
  currentDate.value = new Date(year.value, month.value - 1)
}

const nextMonth = () => {
  currentDate.value = new Date(year.value, month.value + 1)
}

// 将日期格式化为 YYYY-MM-DD 字符串（本地时间）
const formatDateLocal = (date: Date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const handleDateClick = (day: number) => {
  // 创建日期时避免时区问题 - 使用本地时间构造
  const newDate = new Date(year.value, month.value, day)
  // 重置为本地时间的午夜，避免时区偏移
  newDate.setHours(0, 0, 0, 0)
  store.setSelectedDate(newDate)
}

const isToday = (day: number) => isCurrentMonth.value && day === today.value
const isSelected = (day: number) => isSelectedMonth.value && day === selectedDay.value

// 检查指定日期是否有课程
const hasEvent = (day: number) => {
  if (!store.courses || !Array.isArray(store.courses)) {
    return false
  }
  const date = new Date(year.value, month.value, day)
  const dateStr = formatDateLocal(date)
  return store.courses.some(course => course.date === dateStr)
}
</script>
