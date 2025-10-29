<template>
  <div :class="cn('flex flex-col space-y-1 p-2', $attrs.class)">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { cn } from '@/utils'
</script>
