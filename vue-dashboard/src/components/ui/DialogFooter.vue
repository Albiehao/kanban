<template>
  <div :class="cn('flex justify-end gap-2 mt-4', className)">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { cn } from '@/utils'

defineProps<{
  className?: string
}>()
</script>


