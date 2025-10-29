<template>
  <Teleport to="body">
    <Transition name="dialog">
      <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- 遮罩层 -->
        <div
          class="fixed inset-0 bg-black/60 transition-opacity"
          @click="$emit('update:open', false)"
        />
        
        <!-- 对话框内容 -->
        <div
          :class="cn(
            'relative z-50 w-full max-w-lg bg-background shadow-2xl rounded-lg',
            'border border-border p-6 mx-auto',
            'transform transition-all'
          )"
          @click.stop
        >
          <slot />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import { cn } from '@/utils'

defineProps<{
  open: boolean
}>()

defineEmits<{
  'update:open': [value: boolean]
}>()
</script>

<style scoped>
/* 对话框进入动画 */
.dialog-enter-active {
  transition: opacity 0.3s ease;
}

.dialog-enter-from {
  opacity: 0;
}

.dialog-enter-to {
  opacity: 1;
}

.dialog-enter-active .bg-background {
  animation: dialogSlideIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.dialog-leave-active {
  transition: opacity 0.2s ease;
}

.dialog-leave-from {
  opacity: 1;
}

.dialog-leave-to {
  opacity: 0;
}

.dialog-leave-active .bg-background {
  animation: dialogSlideOut 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes dialogSlideIn {
  from {
    opacity: 0;
    transform: scale(0.92) translateY(-15px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes dialogSlideOut {
  from {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: scale(0.94) translateY(-8px);
  }
}
</style>


