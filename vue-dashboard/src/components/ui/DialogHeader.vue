<template>
  <div :class="cn('mb-4', className)">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { cn } from '@/utils'

defineProps<{
  className?: string
}>()
</script>


