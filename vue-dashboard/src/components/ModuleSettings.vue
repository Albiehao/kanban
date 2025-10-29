<template>
  <div class="space-y-4">
    <h3 class="text-lg font-semibold">模块设置</h3>
    <div class="space-y-3">
      <div
        v-for="module in modules"
        :key="module.id"
        class="flex items-center justify-between p-3 rounded-lg border"
      >
        <div>
          <p class="font-medium">{{ module.name }}</p>
          <p class="text-sm text-muted-foreground">{{ module.column }} 列</p>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-sm text-muted-foreground">
            {{ module.visible ? '显示' : '隐藏' }}
          </span>
          <Button
            variant="outline"
            size="sm"
            @click="store.toggleModule(module.id)"
          >
            {{ module.visible ? '隐藏' : '显示' }}
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Button from '@/components/ui/Button.vue'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()
const modules = computed(() => store.modules)
</script>
