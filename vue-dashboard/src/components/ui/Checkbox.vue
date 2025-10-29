<template>
  <div class="flex items-center space-x-2">
    <input
      :id="id"
      type="checkbox"
      :checked="checked"
      :class="cn(
        'peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground',
        $attrs.class
      )"
      v-bind="$attrs"
      @change="$emit('update:checked', ($event.target as HTMLInputElement).checked)"
    />
    <label
      v-if="label"
      :for="id"
      class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
    >
      {{ label }}
    </label>
  </div>
</template>

<script setup lang="ts">
import { cn } from '@/utils'

interface Props {
  id?: string
  checked?: boolean
  label?: string
}

defineProps<Props>()
defineEmits<{
  'update:checked': [value: boolean]
}>()
</script>
