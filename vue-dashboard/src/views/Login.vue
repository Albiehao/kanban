<template>
  <div class="min-h-screen flex">
    <!-- 左侧欢迎区域 -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-600 to-blue-500 relative">
      <div class="flex flex-col justify-between p-12 text-white relative z-10">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
            </svg>
          </div>
          <span class="text-xl font-semibold">Dashboard Kit</span>
        </div>

        <!-- 欢迎内容 -->
        <div class="flex-1 flex items-center">
          <div>
            <h1 class="text-4xl font-bold mb-4">欢迎回来</h1>
            <p class="text-blue-100 text-lg">
              为了继续，请使用您的账户详情登录。
            </p>
          </div>
        </div>

        <!-- 底部指示器 -->
        <div class="flex gap-2">
          <div class="w-2 h-2 rounded-full bg-white"></div>
          <div class="w-2 h-2 rounded-full bg-white/50"></div>
        </div>
      </div>
    </div>

    <!-- 右侧登录表单区域 -->
    <div class="flex-1 flex flex-col justify-center py-12 px-6 sm:px-12 lg:px-24 bg-white">
      <div class="w-full max-w-md">
        <h2 class="text-3xl font-bold text-gray-900 mb-2">登录到Dashboard Kit</h2>
        <p class="text-gray-600 mb-8">请输入您的账户信息继续</p>

        <form v-if="!isRegisterMode" @submit.prevent="handleLogin" class="space-y-6">
          <!-- 用户名 -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
              用户名
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path>
                </svg>
              </div>
              <input
                id="username"
                v-model="loginForm.username"
                type="text"
                required
                placeholder="用户名"
                class="pl-11 w-full h-10 rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <!-- 密码 -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              密码
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
              </div>
              <input
                id="password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="密码"
                class="pl-11 pr-16 w-full h-10 rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-4 flex items-center text-sm text-blue-600 hover:text-blue-700"
              >
                {{ showPassword ? '隐藏' : '显示' }}
              </button>
            </div>
          </div>

          <!-- 记住我 -->
          <div class="flex items-center">
            <input
              type="checkbox"
              id="remember"
              v-model="rememberMe"
              class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label for="remember" class="ml-2 text-sm text-gray-700 cursor-pointer">
              保持登录状态
            </label>
          </div>

          <!-- 错误提示 -->
          <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 text-sm p-4 rounded-lg">
            {{ errorMessage }}
          </div>

          <!-- 登录按钮 -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 disabled:cursor-not-allowed"
          >
            <span v-if="!isLoading">开始使用</span>
            <span v-else>登录中...</span>
          </button>

          <!-- 注册链接 -->
          <div class="text-center">
            <p class="text-sm text-gray-600">
              还没有账户？
              <button
                type="button"
                @click="isRegisterMode = true"
                class="text-blue-600 hover:text-blue-700 font-medium"
              >
                立即注册
              </button>
            </p>
          </div>
        </form>

        <!-- 注册表单 -->
        <form v-else @submit.prevent="handleRegister" class="space-y-6">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">创建账户</h2>
          <p class="text-gray-600 mb-8">请填写以下信息</p>

          <div>
            <label for="register-username" class="block text-sm font-medium text-gray-700 mb-2">
              用户名
            </label>
              <input
                id="register-username"
                v-model="registerForm.username"
                type="text"
                required
                placeholder="用户名"
                class="w-full h-10 rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
          </div>

          <div>
            <label for="register-email" class="block text-sm font-medium text-gray-700 mb-2">
              邮箱
            </label>
              <input
                id="register-email"
                v-model="registerForm.email"
                type="email"
                required
                placeholder="邮箱"
                class="w-full h-10 rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
          </div>

          <div>
            <label for="register-password" class="block text-sm font-medium text-gray-700 mb-2">
              密码
            </label>
              <input
                id="register-password"
                v-model="registerForm.password"
                type="password"
                required
                placeholder="密码"
                class="w-full h-10 rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
          </div>

          <div>
            <label for="register-confirm-password" class="block text-sm font-medium text-gray-700 mb-2">
              确认密码
            </label>
              <input
                id="register-confirm-password"
                v-model="registerForm.confirmPassword"
                type="password"
                required
                placeholder="确认密码"
                class="w-full h-10 rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
          </div>

          <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 text-sm p-4 rounded-lg">
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 disabled:cursor-not-allowed"
          >
            <span v-if="!isLoading">创建账户</span>
            <span v-else>注册中...</span>
          </button>

          <div class="text-center">
            <p class="text-sm text-gray-600">
              已有账户？
              <button
                type="button"
                @click="isRegisterMode = false"
                class="text-blue-600 hover:text-blue-700 font-medium"
              >
                立即登录
              </button>
            </p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Input from '@/components/ui/Input.vue'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/services/authApi'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 登录表单
const loginForm = reactive({
  username: '',
  password: ''
})

// 注册表单
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const isLoading = ref(false)
const errorMessage = ref('')
const isRegisterMode = ref(false)
const showPassword = ref(false)
const rememberMe = ref(false)

// 获取重定向地址
const getRedirectPath = (): string => {
  const redirect = route.query.redirect as string
  if (redirect) {
    return redirect
  }
  
  // 根据用户角色返回默认路径
  if (authStore.isAdmin) {
    return '/admin'
  }
  return '/'
}

// 处理登录
const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const success = await authStore.login(loginForm.username, loginForm.password)
    
    if (success) {
      const redirectPath = getRedirectPath()
      router.push(redirectPath)
    } else {
      errorMessage.value = '用户名或密码错误'
    }
  } catch (error) {
    console.error('登录错误:', error)
    errorMessage.value = '登录失败，请稍后重试'
  } finally {
    isLoading.value = false
  }
}

// 处理注册
const handleRegister = async () => {
  isLoading.value = true
  errorMessage.value = ''

  // 验证密码
  if (registerForm.password !== registerForm.confirmPassword) {
    errorMessage.value = '两次输入的密码不一致'
    isLoading.value = false
    return
  }

  if (registerForm.password.length < 6) {
    errorMessage.value = '密码长度至少为6位'
    isLoading.value = false
    return
  }

  try {
    // 调用注册API
    const response = await authApi.register({
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password,
      role: 'student'
    })

    if (response.success) {
      // 注册成功，设置用户信息
      authStore.currentUser = response.user
      authStore.isAuthenticated = true
      
      // 保存用户信息
      localStorage.setItem('auth_user', JSON.stringify(response.user))

      // 跳转到重定向页面或默认页面
      const redirectPath = getRedirectPath()
      router.push(redirectPath)
    } else {
      errorMessage.value = response.message || '注册失败'
    }
  } catch (error: any) {
    console.error('注册错误:', error)
    errorMessage.value = error.message || '注册失败，请稍后重试'
  } finally {
    isLoading.value = false
  }
}
</script>
