<template>
  <div class="min-h-screen" style="background-color: hsl(var(--background))">
    <DashboardHeader />
    
    <!-- 自定义消息弹框 -->
    <MessageModal
      v-model:visible="showModal"
      :type="modalType"
      :title="modalTitle"
      :message="modalMessage"
      :show-cancel="showCancel"
      confirm-text="确定"
      cancel-text="取消"
      @confirm="handleModalConfirm"
      @cancel="handleModalCancel"
    />

    <main class="container mx-auto p-6">
      <div class="max-w-4xl mx-auto">
        <!-- 页面标题 -->
        <div class="mb-8">
          <div class="flex items-center gap-4 mb-4">
            <router-link 
              to="/" 
              class="flex items-center gap-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
              <span>返回首页</span>
            </router-link>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">个人中心</h1>
          <p class="text-gray-600 dark:text-gray-300">管理您的个人信息和偏好设置</p>
        </div>

        <div class="grid gap-6 lg:grid-cols-3 items-stretch">
          <!-- 左侧 - 偏好设置 -->
          <div class="lg:col-span-1 space-y-6 flex flex-col">

            <!-- 偏好设置 -->
            <Card class="flex flex-col flex-1">
              <CardHeader class="flex-shrink-0 border-b border-gray-200 dark:border-gray-700">
                <CardTitle>偏好设置</CardTitle>
              </CardHeader>
              <CardContent class="space-y-4 flex-1 flex flex-col">
                <div class="flex-1 space-y-4">
                  <div class="flex items-center justify-between py-2">
                    <div class="flex-1">
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">深色模式</label>
                      <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">切换到深色主题</p>
                    </div>
                    <Checkbox :checked="preferences.darkMode" @update:checked="(value) => preferences.darkMode = value" class="ml-4 flex-shrink-0" />
                  </div>
                  
                  <div class="flex items-center justify-between py-2">
                    <div class="flex-1">
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">邮件通知</label>
                      <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">接收任务提醒邮件</p>
                    </div>
                    <Checkbox :checked="preferences.emailNotifications" @update:checked="(value) => preferences.emailNotifications = value" class="ml-4 flex-shrink-0" />
                  </div>
                  
                  <div class="flex items-center justify-between py-2">
                    <div class="flex-1">
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">桌面通知</label>
                      <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">显示桌面通知</p>
                    </div>
                    <Checkbox :checked="preferences.desktopNotifications" @update:checked="(value) => preferences.desktopNotifications = value" class="ml-4 flex-shrink-0" />
                  </div>
                </div>
                
                <div class="mt-auto pt-4 flex-shrink-0">
                  <Button @click="savePreferences" class="w-full">保存设置</Button>
                </div>
              </CardContent>
            </Card>
          </div>

          <!-- 右侧 - 个人信息和安全设置 -->
          <div class="lg:col-span-2 space-y-6 flex flex-col">
            <!-- 个人信息设置 -->
            <Card class="flex flex-col flex-1">
              <CardHeader class="flex items-center justify-between border-b border-gray-200 dark:border-gray-700 pb-4 flex-shrink-0">
                <CardTitle class="flex-1">个人信息</CardTitle>
                <Button 
                  v-if="!isEditingProfile" 
                  @click="isEditingProfile = true"
                  variant="outline"
                  size="sm"
                  class="flex items-center gap-2 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors ml-auto"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  编辑
                </Button>
              </CardHeader>
              <CardContent class="space-y-6 pt-6 flex-1 flex flex-col">
                <!-- 只读模式 -->
                <div v-if="!isEditingProfile" class="space-y-6 flex-1 flex flex-col">
                  <div class="grid gap-6 md:grid-cols-2">
                    <div class="space-y-3">
                      <label class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">用户名</label>
                      <div class="bg-gray-50 dark:bg-gray-800/50 rounded-lg px-4 py-3 border border-gray-200 dark:border-gray-700">
                        <p class="text-base text-gray-900 dark:text-white font-medium">{{ profile.username }}</p>
                      </div>
                    </div>
                    <div class="space-y-3">
                      <label class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">邮箱</label>
                      <div class="bg-gray-50 dark:bg-gray-800/50 rounded-lg px-4 py-3 border border-gray-200 dark:border-gray-700">
                        <p class="text-base text-gray-900 dark:text-white font-medium break-all">{{ profile.email }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="space-y-3 flex-1">
                    <label class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">个人简介</label>
                    <div class="bg-gray-50 dark:bg-gray-800/50 rounded-lg px-4 py-4 border border-gray-200 dark:border-gray-700 h-[140px] overflow-y-auto">
                      <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed">{{ profile.bio || '暂无简介' }}</p>
                    </div>
                  </div>
                </div>

                <!-- 编辑模式 -->
                <div v-else class="space-y-6 flex-1 flex flex-col">
                  <div class="grid gap-6 md:grid-cols-2">
                    <div class="space-y-2">
                      <label class="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">用户名</label>
                      <Input v-model="profile.username" placeholder="请输入用户名" />
                    </div>
                    <div class="space-y-2">
                      <label class="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">邮箱</label>
                      <Input v-model="profile.email" type="email" placeholder="请输入邮箱" />
                    </div>
                  </div>
                  <div class="space-y-2">
                    <label class="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">个人简介</label>
                    <textarea 
                      v-model="profile.bio" 
                      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                      rows="4"
                      placeholder="介绍一下自己..."
                    ></textarea>
                  </div>
                  
                  <div class="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700 mt-auto flex-shrink-0">
                    <Button @click="cancelEditProfile" variant="outline" class="px-6">取消</Button>
                    <Button @click="saveProfile" class="px-6">保存更改</Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            <!-- 教务系统绑定 -->
            <Card class="flex flex-col flex-1">
              <CardHeader class="flex-shrink-0 border-b border-gray-200 dark:border-gray-700">
                <CardTitle>教务系统绑定</CardTitle>
              </CardHeader>
              <CardContent class="space-y-4 flex-1 flex flex-col pt-6">
                  <div class="flex-1 space-y-4">
                  <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    配置第三方API密钥，系统将自动同步您的课程信息
                  </p>
                  
                  <div>
                    <label class="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-2 block">API 路径</label>
                    <Input v-model="eduAccount.apiPath" placeholder="http://160.202.229.142:8000/api/v1/api/courses" />
                    <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      第三方课程API的完整地址
                    </p>
                  </div>
                  
                  <div>
                    <label class="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-2 block">API Key</label>
                    <Input v-model="eduAccount.apiKey" type="password" placeholder="请输入第三方API密钥" />
                  </div>
                  
                  <div v-if="eduAccount.isBound" class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-3">
                    <div class="flex items-center gap-2 text-green-600 dark:text-green-400 text-sm">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <div class="flex-1">
                        <div>API Key已配置</div>
                        <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          数据来源：第三方API
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="flex justify-end pt-4 border-t border-gray-200 dark:border-gray-700 mt-auto flex-shrink-0">
                  <Button @click="saveEduAccount" class="px-6">
                    {{ eduAccount.isBound ? '更新绑定' : '保存绑定' }}
                  </Button>
                </div>
              </CardContent>
            </Card>

            <!-- 安全设置 -->
            <Card class="flex flex-col flex-1">
              <CardHeader class="flex-shrink-0 border-b border-gray-200 dark:border-gray-700">
                <CardTitle>安全设置</CardTitle>
              </CardHeader>
              <CardContent class="space-y-4 flex-1 flex flex-col pt-6">
                <div class="flex-1 space-y-4">
                  <div>
                    <label class="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-2 block">当前密码</label>
                    <Input v-model="security.currentPassword" type="password" placeholder="请输入当前密码" />
                  </div>
                  <div>
                    <label class="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-2 block">新密码</label>
                    <Input v-model="security.newPassword" type="password" placeholder="请输入新密码" />
                  </div>
                  <div>
                    <label class="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-2 block">确认新密码</label>
                    <Input v-model="security.confirmPassword" type="password" placeholder="请再次输入新密码" />
                  </div>
                </div>
                <div class="flex justify-end pt-4 border-t border-gray-200 dark:border-gray-700 mt-auto flex-shrink-0">
                  <Button @click="changePassword" class="px-6">修改密码</Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import DashboardHeader from '@/components/DashboardHeader.vue'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Checkbox from '@/components/ui/Checkbox.vue'
import MessageModal from '@/components/ui/MessageModal.vue'
import { userApi } from '@/services/api'
import { userSettingsApi } from '@/services/userSettingsApi'
import type { UserApiData } from '@/services/types'

// 用户数据
const userData = ref<UserApiData>({
  profile: {
    username: '用户名',
    email: 'user@example.com',
    bio: '这是一个个人简介的示例...',
    avatar: 'U',
    completedTasks: 0,
    inProgressTasks: 0,
    daysJoined: 0
  },
  preferences: {
    darkMode: false,
    emailNotifications: true,
    desktopNotifications: true
  }
})

// 个人信息
const profile = ref({
  username: '',
  email: '',
  bio: ''
})

// 偏好设置
const preferences = ref({
  darkMode: false,
  emailNotifications: false,
  desktopNotifications: false
})

// 原始偏好设置（用于取消编辑）
const originalPreferences = ref({
  darkMode: false,
  emailNotifications: false,
  desktopNotifications: false
})

// 安全设置
const security = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 教务系统API Key绑定
const eduAccount = reactive({
  apiPath: 'http://160.202.229.142:8000/api/v1/api/courses',
  apiKey: '',
  isBound: false
})

// 编辑状态
const isEditingProfile = ref(false)
const originalProfile = ref({
  username: '',
  email: '',
  bio: ''
})

// 模态框状态
const showModal = ref(false)
const modalType = ref<'success' | 'error' | 'warning' | 'info'>('info')
const modalTitle = ref('提示')
const modalMessage = ref('')
const showCancel = ref(false)

// 待确认的操作
let pendingAction: (() => void) | null = null

// 初始化用户数据
const initUserData = async () => {
  try {
    console.log('开始获取用户数据...')
    const data = await userApi.getUser()
    
    console.log('API返回的原始数据:', JSON.stringify(data, null, 2))
    
    userData.value = data
    
    // 安全检查数据
    if (!data) {
      console.error('❌ API返回的数据为空')
      return
    }
    
    // 填充表单数据（API返回的是扁平结构，不是嵌套的profile）
    profile.value = {
      username: data.username || '',
      email: data.email || '',
      bio: data.bio || ''
    }
    
    // 保存原始数据
    originalProfile.value = {
      username: profile.value.username,
      email: profile.value.email,
      bio: profile.value.bio
    }
    
    // 更新偏好设置（如果有，API返回的是JSON字符串或对象）
    const prefs = data.preferences
    if (prefs && typeof prefs === 'object') {
      preferences.value = {
        darkMode: prefs.darkMode ?? false,
        emailNotifications: prefs.emailNotifications ?? true,
        desktopNotifications: prefs.desktopNotifications ?? false
      }
    } else if (typeof prefs === 'string') {
      try {
        const parsedPrefs = JSON.parse(prefs)
        preferences.value = {
          darkMode: parsedPrefs.darkMode ?? false,
          emailNotifications: parsedPrefs.emailNotifications ?? true,
          desktopNotifications: parsedPrefs.desktopNotifications ?? false
        }
      } catch (e) {
        console.warn('无法解析preferences:', e)
      }
    }
    
    // 保存原始偏好设置
    originalPreferences.value = {
      darkMode: preferences.value.darkMode,
      emailNotifications: preferences.value.emailNotifications,
      desktopNotifications: preferences.value.desktopNotifications
    }
    
    // 更新教务系统绑定信息
    if (data.eduBinding) {
      eduAccount.isBound = data.eduBinding.isBound || false
    }
    
    console.log('✅ 用户数据加载成功')
    console.log('教务系统绑定状态:', eduAccount.isBound)
  } catch (error) {
    console.error('加载用户数据失败:', error)
  }
}

// 模态框处理函数
const showMessageModal = (type: 'success' | 'error' | 'warning' | 'info', title: string, message: string, needConfirm = false) => {
  modalType.value = type
  modalTitle.value = title
  modalMessage.value = message
  showCancel.value = needConfirm
  showModal.value = true
}

const handleModalConfirm = () => {
  if (pendingAction) {
    pendingAction()
    pendingAction = null
  }
}

const handleModalCancel = () => {
  pendingAction = null
}

// 保存个人信息
const saveProfile = async () => {
  // 检查是否修改了用户名
  const usernameChanged = profile.value.username !== originalProfile.value.username
  
  if (usernameChanged) {
    // 使用自定义模态框确认
    showMessageModal(
      'warning',
      '确认修改用户名',
      `确定要将用户名修改为 "${profile.value.username}" 吗？`,
      true
    )
    
    // 等待用户确认
    pendingAction = async () => {
      await executeSaveProfile()
    }
    return
  }
  
  await executeSaveProfile()
}

// 执行保存操作
const executeSaveProfile = async () => {
  try {
    // 使用专门的个人资料API
    await userSettingsApi.updateProfile({
      username: profile.value.username,
      email: profile.value.email,
      bio: profile.value.bio
    })
    
    userData.value.profile = {
      ...userData.value.profile,
      username: profile.value.username,
      email: profile.value.email,
      bio: profile.value.bio
    }
    
    // 更新原始数据
    originalProfile.value = {
      username: profile.value.username,
      email: profile.value.email,
      bio: profile.value.bio
    }
    
    // 退出编辑模式
    isEditingProfile.value = false
    
    console.log('保存个人信息成功')
    showMessageModal('success', '保存成功', '个人信息已更新')
  } catch (error: any) {
    console.error('保存个人信息失败:', error)
    
    // 检查是否是用户名冲突
    const errorMessage = error?.message || String(error)
    
    if (errorMessage.includes('已被使用') || errorMessage.includes('重复') || errorMessage.includes('已存在')) {
      showMessageModal('error', '保存失败', '用户名已被占用，请尝试其他用户名')
    } else if (errorMessage.includes('格式')) {
      showMessageModal('error', '保存失败', '用户名格式不正确\n\n用户名规则：\n• 只能包含字母、数字和下划线\n• 长度必须在3-20个字符之间')
    } else if (errorMessage.includes('邮箱')) {
      showMessageModal('error', '保存失败', '邮箱已被占用或格式不正确')
    } else {
      showMessageModal('error', '保存失败', errorMessage)
    }
  }
}

// 取消编辑
const cancelEditProfile = () => {
  // 恢复原始数据
  profile.value = {
    username: originalProfile.value.username,
    email: originalProfile.value.email,
    bio: originalProfile.value.bio
  }
  isEditingProfile.value = false
}

// 保存偏好设置
const savePreferences = async () => {
  try {
    console.log('当前偏好设置值:', preferences.value)
    
    // 使用专门的偏好设置API
    const result = await userSettingsApi.updatePreferences(preferences.value)
    console.log('API返回结果:', result)
    
    userData.value.preferences = preferences.value
    
    // 更新原始偏好设置
    originalPreferences.value = {
      darkMode: preferences.value.darkMode,
      emailNotifications: preferences.value.emailNotifications,
      desktopNotifications: preferences.value.desktopNotifications
    }
    
    console.log('保存偏好设置成功')
    showMessageModal('success', '保存成功', '偏好设置已更新')
  } catch (error: any) {
    console.error('保存偏好设置失败:', error)
    const errorMessage = error?.message || String(error)
    showMessageModal('error', '保存失败', `保存偏好设置失败：${errorMessage}`)
  }
}

// 重置偏好设置
const resetPreferences = () => {
  preferences.value = {
    darkMode: originalPreferences.value.darkMode,
    emailNotifications: originalPreferences.value.emailNotifications,
    desktopNotifications: originalPreferences.value.desktopNotifications
  }
}

// 修改密码
const changePassword = async () => {
  // 验证输入
  if (!security.value.currentPassword) {
    showMessageModal('error', '验证失败', '请输入原密码')
    return
  }
  
  if (security.value.newPassword !== security.value.confirmPassword) {
    showMessageModal('error', '验证失败', '两次输入的密码不一致')
    return
  }
  
  if (!security.value.newPassword || security.value.newPassword.length < 6) {
    showMessageModal('error', '验证失败', '密码长度至少为6位')
    return
  }
  
  if (security.value.newPassword.length > 100) {
    showMessageModal('error', '验证失败', '密码长度不能超过100个字符')
    return
  }
  
  // 使用确认模态框
  showMessageModal(
    'warning',
    '确认修改密码',
    '确定要修改密码吗？修改后需要使用新密码登录。',
    true
  )
  
  pendingAction = async () => {
    try {
      await userSettingsApi.updatePassword(
        security.value.currentPassword,
        security.value.newPassword
      )
      
      console.log('密码修改成功')
      showMessageModal('success', '密码修改成功', '密码已成功修改，请使用新密码登录')
      
      // 清空表单
      security.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    } catch (error: any) {
      console.error('密码修改失败:', error)
      
      const errorMessage = error?.message || String(error)
      
      if (errorMessage.includes('原密码错误')) {
        showMessageModal('error', '修改失败', '原密码错误，请重新输入')
      } else if (errorMessage.includes('太短')) {
        showMessageModal('error', '修改失败', '新密码长度至少为6个字符')
      } else if (errorMessage.includes('太长')) {
        showMessageModal('error', '修改失败', '新密码长度不能超过100个字符')
      } else if (errorMessage.includes('相同')) {
        showMessageModal('error', '修改失败', '新密码不能与原密码相同')
      } else if (errorMessage.includes('不一致')) {
        showMessageModal('error', '修改失败', '两次输入的新密码不一致')
      } else {
        showMessageModal('error', '修改失败', errorMessage)
      }
    }
  }
}

// 切换深色模式的函数
const toggleDarkMode = (enabled: boolean) => {
  if (enabled) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('darkMode', 'true')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('darkMode', 'false')
  }
}

// 监听深色模式变化，实时更新界面
watch(() => preferences.value.darkMode, (newValue) => {
  toggleDarkMode(newValue)
})

// 初始化时设置深色模式
onMounted(() => {
  initUserData()
  
  // 根据当前偏好设置初始化深色模式
  if (preferences.value.darkMode) {
    toggleDarkMode(true)
  }
})

// 格式化刷新频率文本

// 保存教务系统API Key绑定
const saveEduAccount = async () => {
  // 验证输入
  if (!eduAccount.apiPath) {
    showMessageModal('error', '验证失败', '请输入API路径')
    return
  }
  if (!eduAccount.apiKey) {
    showMessageModal('error', '验证失败', '请输入API Key')
    return
  }
  
  try {
    // 调用API保存绑定（传递API路径和Key）
    await userSettingsApi.bindEduAccount({
      apiPath: eduAccount.apiPath,
      apiKey: eduAccount.apiKey
    })
    
    eduAccount.isBound = true
    eduAccount.apiKey = '' // 清空API Key
    
    showMessageModal('success', '配置成功', 'API配置已保存')
  } catch (error: any) {
    console.error('配置失败:', error)
    const errorMessage = error?.message || String(error)
    showMessageModal('error', '配置失败', errorMessage)
  }
}
</script>
