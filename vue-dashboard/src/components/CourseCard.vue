<template>
  <div
    :class="cn(
      'h-full rounded-md p-0.5 flex flex-col text-[10px] overflow-hidden',
      'transition-all duration-200 ease-in-out transform',
      'hover:scale-105 hover:shadow-lg',
      highlighted ? 'ring-2 ring-primary ring-offset-1 shadow-lg' : '',
      getColorClass(course.color)
    )"
  >
    <div class="font-medium leading-tight mb-0 line-clamp-2 text-[9px]">
      {{ course.name }}
    </div>
    <div v-if="course.location" class="text-[7px] leading-tight opacity-90 mt-0">
      {{ course.location }}
    </div>
    <div v-if="course.teacher" class="text-[7px] leading-tight opacity-90 mt-0">
      {{ course.teacher }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/utils'
import type { Course } from '@/stores/dashboard'

interface Props {
  course: Course
  highlighted?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  highlighted: false
})

// 颜色映射
const colorClasses: Record<string, string> = {
  'bg-chart-1': 'bg-[rgb(200,180,230)] text-[rgb(80,50,120)]',
  'bg-chart-2': 'bg-[rgb(180,220,240)] text-[rgb(40,90,140)]',
  'bg-chart-3': 'bg-[rgb(180,240,220)] text-[rgb(40,120,90)]',
  'bg-chart-4': 'bg-[rgb(255,220,180)] text-[rgb(140,80,20)]',
  'bg-chart-5': 'bg-[rgb(255,200,220)] text-[rgb(140,40,80)]',
  purple: 'bg-[rgb(200,180,230)] text-[rgb(80,50,120)]',
  blue: 'bg-[rgb(180,220,240)] text-[rgb(40,90,140)]',
  green: 'bg-[rgb(180,240,220)] text-[rgb(40,120,90)]',
  orange: 'bg-[rgb(255,220,180)] text-[rgb(140,80,20)]',
  pink: 'bg-[rgb(255,200,220)] text-[rgb(140,40,80)]',
  yellow: 'bg-[rgb(255,240,180)] text-[rgb(140,110,20)]'
}

const getColorClass = (color: string) => {
  return colorClasses[color] || colorClasses['bg-chart-1']
}
</script>


