<template>
  <Card>
    <CardHeader>
      <CardTitle class="text-base">完成量图表</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-xs text-muted-foreground">本周完成率</span>
          <span class="text-sm font-semibold">85%</span>
        </div>
        <div class="w-full bg-muted rounded-full h-1.5">
          <div class="bg-chart-1 h-1.5 rounded-full" style="width: 85%"></div>
        </div>
        <div class="grid grid-cols-2 gap-2 text-xs">
          <div>
            <p class="text-muted-foreground">已完成</p>
            <p class="font-semibold text-chart-1">17</p>
          </div>
          <div>
            <p class="text-muted-foreground">进行中</p>
            <p class="font-semibold text-chart-5">3</p>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
</script>
