import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, tokenManager, type LoginRequest } from '@/services/authApi'

export interface AuthUser {
  id: number
  username: string
  email: string
  role: 'super_admin' | 'admin' | 'teacher' | 'student'
  permissions: string[]
}

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const currentUser = ref<AuthUser | null>(null)
  const isAuthenticated = ref(false)

  // 计算属性
  const isSuperAdmin = computed(() => 
    currentUser.value?.role === 'super_admin'
  )

  const isAdmin = computed(() => 
    currentUser.value?.role === 'admin'
  )

  const isTeacher = computed(() => 
    currentUser.value?.role === 'teacher'
  )

  const isStudent = computed(() => 
    currentUser.value?.role === 'student'
  )

  // 检查是否有管理员权限（包括超级管理员和管理员）
  const canAccessAdmin = computed(() => 
    currentUser.value?.role === 'super_admin' || currentUser.value?.role === 'admin'
  )

  const userPermissions = computed(() => 
    currentUser.value?.permissions || []
  )

  // 方法 - 使用JWT登录
  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      console.log('Auth Store - 登录请求:', { username })
      
      const response = await authApi.login({ username, password })
      
      if (response.success && response.user) {
        currentUser.value = response.user
        isAuthenticated.value = true
        
        // 保存用户信息
        saveUserToStorage()
        
        console.log('Auth Store - 登录成功:', response.user.username)
        return true
      }
      
      console.log('Auth Store - 登录失败')
      return false
    } catch (error) {
      console.error('Auth Store - 登录错误:', error)
      return false
    }
  }

  // 使用JWT登出
  const logout = async () => {
    try {
      // 调用API登出
      await authApi.logout()
    } catch (error) {
      console.error('登出API失败:', error)
    } finally {
      // 无论API成功与否，都清除本地状态
      currentUser.value = null
      isAuthenticated.value = false
      clearStorage()
    }
  }

  const hasPermission = (permission: string) => {
    return userPermissions.value.includes(permission)
  }

  const hasRole = (role: string) => {
    return currentUser.value?.role === role
  }


  // 初始化时验证JWT token
  const initAuth = async () => {
    // 检查localStorage中的用户信息
    const savedUser = localStorage.getItem('auth_user')
    
    // 如果有token，验证其有效性
    if (tokenManager.hasToken()) {
      try {
        const verifyResult = await authApi.verifyToken()
        
        if (verifyResult.valid && verifyResult.user) {
          // Token有效，恢复用户状态
          currentUser.value = verifyResult.user
          isAuthenticated.value = true
          
          console.log('Auth - Token验证成功，已恢复登录状态')
        } else {
          // Token无效，清除本地数据
          console.log('Auth - Token已失效，清除本地数据')
          tokenManager.removeToken()
          clearStorage()
        }
      } catch (error) {
        console.error('Auth - 验证token失败:', error)
        tokenManager.removeToken()
        clearStorage()
      }
    } else if (savedUser) {
      // 没有token但有保存的用户信息（兼容旧数据）
      try {
        currentUser.value = JSON.parse(savedUser)
        isAuthenticated.value = true
      } catch (error) {
        console.error('Failed to parse saved user:', error)
        localStorage.removeItem('auth_user')
      }
    }
  }

  // 保存用户信息到本地存储
  const saveUserToStorage = () => {
    if (currentUser.value) {
      localStorage.setItem('auth_user', JSON.stringify(currentUser.value))
    }
  }

  // 清除本地存储
  const clearStorage = () => {
    localStorage.removeItem('auth_user')
  }

  return {
    // 状态
    currentUser,
    isAuthenticated,
    // 计算属性
    isSuperAdmin,
    isAdmin,
    isTeacher,
    isStudent,
    canAccessAdmin,
    userPermissions,
    // 方法
    login,
    logout,
    hasPermission,
    hasRole,
    initAuth,
    saveUserToStorage,
    clearStorage
  }
})
