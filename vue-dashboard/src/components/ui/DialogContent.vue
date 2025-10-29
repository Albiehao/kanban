<template>
  <div :class="cn('', className)">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { cn } from '@/utils'

defineProps<{
  className?: string
}>()
</script>


