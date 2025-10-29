<template>
  <Card>
    <CardHeader>
      <CardTitle class="text-lg">{{ formatDate(selectedDate) }} 课程</CardTitle>
    </CardHeader>
    <CardContent class="space-y-3">
      <div
        v-if="filteredCourses.length === 0"
        class="text-center py-8 text-muted-foreground"
      >
        该日期暂无课程安排
      </div>
      <div
        v-for="course in filteredCourses"
        :key="course.id"
        class="flex items-start gap-3 p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
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
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { Clock, MapPin } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Badge from '@/components/ui/Badge.vue'
import { formatDate } from '@/utils'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

const selectedDate = computed(() => store.selectedDate)
const filteredCourses = computed(() => store.filteredCourses)
</script>
