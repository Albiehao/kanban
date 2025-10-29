<template>
  <div :class="cn('p-2 pt-0', $attrs.class)">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { cn } from '@/utils'
</script>
