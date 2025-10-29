<template>
  <header class="bg-card dark:bg-card border-b" style="background-color: hsl(var(--card)); border-color: hsl(var(--border))">
    <div class="container mx-auto px-4 py-2">
      <div class="flex items-center justify-between">
        <h1 class="text-xl font-semibold" style="color: hsl(var(--foreground))">个人任务看板</h1>
        
        <div class="flex items-center gap-2">
          <!-- 夜间模式切换按钮 -->
          <button 
            @click="toggleDarkMode"
            class="p-1.5 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors group"
            :title="isDarkMode ? '切换到浅色模式' : '切换到夜间模式'"
          >
            <!-- 浅色模式下显示月亮，点击后切换到夜间 -->
            <Moon v-if="!isDarkMode" class="h-5 w-5 text-gray-600 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors" />
            <!-- 夜间模式下显示太阳，点击后切换到浅色 -->
            <Sun v-else class="h-5 w-5 text-yellow-500 group-hover:text-yellow-600 transition-colors" />
          </button>
          
          <!-- 通知组件 -->
          <NotificationDropdown />
          
          <!-- 用户信息下拉菜单 -->
          <div class="relative">
            <button 
              @click="showUserMenu = !showUserMenu"
              class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center hover:bg-blue-700 transition-colors cursor-pointer"
            >
              <span class="text-white text-sm font-medium">
                {{ authStore.currentUser?.username?.charAt(0).toUpperCase() || 'U' }}
              </span>
            </button>
            
            <!-- 下拉菜单 -->
            <div 
              v-if="showUserMenu"
              class="absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 z-50 dark:bg-gray-800"
              style="background-color: hsl(var(--card))"
            >
              <div class="px-4 py-2 text-sm border-b" style="color: hsl(var(--foreground)); border-color: hsl(var(--border))">
                <div class="font-medium">{{ authStore.currentUser?.username }}</div>
                <div class="text-xs" style="color: hsl(var(--muted-foreground))">{{ authStore.currentUser?.email }}</div>
                <div class="text-xs text-blue-500 dark:text-blue-400">{{ authStore.currentUser?.role }}</div>
              </div>
              <!-- 管理员入口 -->
              <router-link 
                v-if="authStore.canAccessAdmin"
                to="/admin" 
                class="block px-4 py-2 text-sm hover:opacity-80 transition-opacity border-b"
                style="color: hsl(var(--foreground)); border-color: hsl(var(--border))"
                @click="showUserMenu = false"
              >
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  管理员界面
                </div>
              </router-link>
              <router-link 
                to="/profile" 
                class="block px-4 py-2 text-sm hover:opacity-80 transition-opacity"
                style="color: hsl(var(--foreground))"
                @click="showUserMenu = false"
              >
                个人设置
              </router-link>
              <button 
                @click="handleLogout"
                class="block w-full text-left px-4 py-2 text-sm hover:opacity-80 transition-opacity"
                style="color: hsl(var(--foreground))"
              >
                退出登录
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- Settings Dialog -->
  <div
    v-if="showSettings"
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    @click="showSettings = false"
  >
    <div
      class="rounded-lg p-6 max-w-2xl max-h-[80vh] overflow-y-auto"
      style="background-color: hsl(var(--card))"
      @click.stop
    >
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold" style="color: hsl(var(--foreground))">看板设置</h2>
        <Button variant="ghost" size="icon" @click="showSettings = false">
          <X class="h-4 w-4" />
        </Button>
      </div>
      <p class="text-sm mb-6" style="color: hsl(var(--muted-foreground))">自定义显示的模块和布局</p>
      <ModuleSettings />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Settings, X, Moon, Sun } from 'lucide-vue-next'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import ModuleSettings from './ModuleSettings.vue'
import NotificationDropdown from './NotificationDropdown.vue'
import { useAuthStore } from '@/stores/auth'
import { useDashboardStore } from '@/stores/dashboard'

const router = useRouter()
const authStore = useAuthStore()
const dashboardStore = useDashboardStore()

const { isDarkMode, toggleDarkMode } = dashboardStore

const showSettings = ref(false)
const showUserMenu = ref(false)

const currentDate = new Date()
const dateString = computed(() => 
  currentDate.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "long",
  })
)

const handleLogout = () => {
  authStore.logout()
  authStore.clearStorage()
  showUserMenu.value = false
  router.push('/login')
}

// 点击外部关闭用户菜单
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  if (!target.closest('.relative')) {
    showUserMenu.value = false
  }
}

// 添加全局点击事件监听
if (typeof window !== 'undefined') {
  document.addEventListener('click', handleClickOutside)
}
</script>
