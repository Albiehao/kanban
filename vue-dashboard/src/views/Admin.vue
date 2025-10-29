<template>
  <div class="min-h-screen" style="background-color: hsl(var(--background))">
    <DashboardHeader />

    <main class="container mx-auto p-6">
      <div class="max-w-7xl mx-auto">
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
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">管理员控制台</h1>
          <p class="text-gray-600 dark:text-gray-300">系统管理和数据监控</p>
        </div>

        <!-- 统计卡片 -->
        <div class="grid gap-6 mb-8 md:grid-cols-2 lg:grid-cols-4">
          <Card class="p-6">
            <div class="flex items-center">
              <div class="p-2 bg-blue-100 rounded-lg">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">总用户数</p>
                <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.totalUsers }}</p>
              </div>
            </div>
          </Card>

          <Card class="p-6">
            <div class="flex items-center">
              <div class="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
                <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">活跃课程</p>
                <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.activeCourses }}</p>
              </div>
            </div>
          </Card>

          <Card class="p-6">
            <div class="flex items-center">
              <div class="p-2 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg">
                <svg class="w-6 h-6 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">待处理任务</p>
                <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.pendingTasks }}</p>
              </div>
            </div>
          </Card>

          <Card class="p-6">
            <div class="flex items-center">
              <div class="p-2 bg-red-100 dark:bg-red-900/30 rounded-lg">
                <svg class="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">系统警告</p>
                <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ stats.systemWarnings }}</p>
              </div>
            </div>
          </Card>
        </div>

        <!-- 主要内容区域 -->
        <div class="grid gap-6 lg:grid-cols-3">
          <!-- 左侧 - 用户管理 -->
          <div class="lg:col-span-2 space-y-6">
            <!-- 用户管理 -->
            <Card>
              <CardHeader>
                <CardTitle>用户管理</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="space-y-4">
                  <!-- 搜索和筛选 -->
                  <div class="flex gap-4">
                    <Input 
                      v-model="userSearchQuery" 
                      placeholder="搜索用户..." 
                      class="flex-1"
                    />
                    <Button @click="refreshUsers">刷新</Button>
                  </div>

                  <!-- 用户列表 -->
                  <div class="overflow-auto max-h-96 scrollbar-hide">
                    <table class="w-full text-sm">
                      <thead class="sticky top-0 bg-white dark:bg-gray-900">
                        <tr class="border-b border-gray-200 dark:border-gray-700">
                          <th class="text-left p-2 text-gray-600 dark:text-gray-400">用户ID</th>
                          <th class="text-left p-2 text-gray-600 dark:text-gray-400">用户名</th>
                          <th class="text-left p-2 text-gray-600 dark:text-gray-400">邮箱</th>
                          <th class="text-left p-2 text-gray-600 dark:text-gray-400">状态</th>
                          <th class="text-left p-2 text-gray-600 dark:text-gray-400">操作</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr 
                          v-for="user in filteredUsers" 
                          :key="user.id"
                          class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50"
                        >
                          <td class="p-2 text-gray-900 dark:text-white">{{ user.id }}</td>
                          <td class="p-2 text-gray-900 dark:text-white">{{ user.username }}</td>
                          <td class="p-2 text-gray-700 dark:text-gray-300">{{ user.email }}</td>
                          <td class="p-2">
                            <Badge :variant="user.status === 'active' ? 'default' : 'secondary'">
                              {{ user.status === 'active' ? '活跃' : '禁用' }}
                            </Badge>
                          </td>
                          <td class="p-2">
                            <div class="flex gap-2">
                              <Button 
                                variant="outline" 
                                size="sm" 
                                @click="editUser(user)"
                              >
                                编辑
                              </Button>
                              <Button 
                                variant="outline" 
                                size="sm" 
                                :class="user.status === 'active' ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'"
                                @click="toggleUserStatus(user)"
                              >
                                {{ user.status === 'active' ? '禁用' : '启用' }}
                              </Button>
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </CardContent>
            </Card>

            <!-- DeepSeek 配置管理 -->
            <Card>
              <CardHeader>
                <div class="flex items-center justify-between">
                  <CardTitle>DeepSeek 配置管理</CardTitle>
                  <div class="flex gap-2">
                    <Button variant="outline" size="sm" @click="refreshDeepSeekConfigs">刷新</Button>
                    <Button size="sm" @click="showCreateDeepSeekConfig">创建配置</Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div v-if="deepSeekConfigs.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400 text-sm">
                  暂无配置，点击"创建配置"添加第一个配置
                </div>
                <div v-else class="space-y-3">
                  <div 
                    v-for="config in deepSeekConfigs" 
                    :key="config.id"
                    :class="`p-4 rounded-lg border-2 transition-colors ${
                      config.is_active 
                        ? 'border-green-500 bg-green-50 dark:bg-green-900/20' 
                        : 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50'
                    }`"
                  >
                    <div class="flex items-start justify-between mb-3">
                      <div class="flex-1">
                        <div class="flex items-center gap-2 mb-2">
                          <span class="text-sm font-semibold text-gray-900 dark:text-white">配置 #{{ config.id }}</span>
                          <Badge v-if="config.is_active" variant="default" class="bg-green-600">启用中</Badge>
                          <Badge v-else variant="secondary">已禁用</Badge>
                        </div>
                        <div class="space-y-1 text-xs text-gray-600 dark:text-gray-400">
                          <div><span class="font-medium">API Key:</span> {{ maskApiKey(config.api_key) }}</div>
                          <div><span class="font-medium">Base URL:</span> {{ config.base_url }}</div>
                          <div><span class="font-medium">Model:</span> {{ config.model }}</div>
                          <div><span class="font-medium">限流:</span> {{ config.rate_limit_per_minute }}/分钟, {{ config.rate_limit_per_day }}/天</div>
                          <div><span class="font-medium">创建时间:</span> {{ formatDateTime(config.created_at) }}</div>
                        </div>
                      </div>
                      <div class="flex gap-2 ml-4">
                        <Button variant="outline" size="sm" @click="editDeepSeekConfig(config)">编辑</Button>
                        <Button 
                          variant="outline" 
                          size="sm" 
                          :class="config.is_active ? 'text-orange-600 dark:text-orange-400' : 'text-green-600 dark:text-green-400'"
                          @click="toggleDeepSeekConfig(config.id)"
                        >
                          {{ config.is_active ? '禁用' : '启用' }}
                        </Button>
                        <Button 
                          variant="outline" 
                          size="sm" 
                          class="text-red-600 dark:text-red-400"
                          @click="deleteDeepSeekConfig(config.id)"
                        >
                          删除
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <!-- 系统日志 -->
            <Card>
              <CardHeader>
                <div class="flex items-center justify-between">
                  <CardTitle>系统日志</CardTitle>
                  <div class="flex gap-2">
                    <select 
                      v-model="logLevelFilter" 
                      @change="refreshSystemLogs"
                      class="h-8 px-2 text-xs border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                    >
                      <option value="">全部</option>
                      <option value="warning">警告</option>
                      <option value="error">错误</option>
                    </select>
                    <Button variant="outline" size="sm" @click="refreshSystemLogs">刷新</Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div v-if="systemLogs.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400 text-sm">
                  暂无系统日志
                </div>
                <div v-else class="space-y-1 max-h-64 overflow-y-auto scrollbar-hide pr-2">
                  <div 
                    v-for="log in systemLogs" 
                    :key="log.id"
                    class="flex items-start gap-2 p-2 bg-gray-50 dark:bg-gray-800/50 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors"
                  >
                    <div :class="`w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0 ${getLogColor(log.level)}`"></div>
                    <div class="flex-1 min-w-0">
                      <div class="flex flex-wrap items-center gap-2 mb-0.5">
                        <span :class="getLogLevelColor(log.level)" class="text-xs font-semibold uppercase">
                          {{ log.level }}
                        </span>
                        <span v-if="log.module" class="text-[10px] text-gray-500 dark:text-gray-400 px-1.5 py-0.5 bg-gray-200 dark:bg-gray-700 rounded">
                          {{ log.module }}
                        </span>
                        <span class="text-[10px] text-gray-500 dark:text-gray-400">
                          {{ formatLogTimestamp(log.timestamp) }}
                        </span>
                      </div>
                      <p class="text-xs text-gray-700 dark:text-gray-300 leading-relaxed break-words">{{ log.message }}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <!-- 右侧 - 系统设置和快捷操作 -->
          <div class="space-y-6">
            <!-- 系统设置 -->
            <Card>
              <CardHeader>
                <CardTitle>系统设置</CardTitle>
              </CardHeader>
              <CardContent class="space-y-4">
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm font-medium text-gray-700 dark:text-gray-200">维护模式</label>
                      <p class="text-xs text-gray-500 dark:text-gray-400">启用后将暂停用户访问</p>
                    </div>
                    <Checkbox v-model="systemSettings.maintenanceMode" />
                  </div>
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm font-medium text-gray-700 dark:text-gray-200">自动备份</label>
                      <p class="text-xs text-gray-500 dark:text-gray-400">每日自动备份数据</p>
                    </div>
                    <Checkbox v-model="systemSettings.autoBackup" />
                  </div>
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm font-medium text-gray-700 dark:text-gray-200">邮件通知</label>
                      <p class="text-xs text-gray-500 dark:text-gray-400">发送系统通知邮件</p>
                    </div>
                    <Checkbox v-model="systemSettings.emailNotifications" />
                  </div>
                </div>
                <div class="pt-4">
                  <Button @click="saveSystemSettings" class="w-full">
                    保存设置
                  </Button>
                </div>
              </CardContent>
            </Card>

            <!-- 快捷操作 -->
            <Card>
              <CardHeader>
                <CardTitle>快捷操作</CardTitle>
              </CardHeader>
              <CardContent class="space-y-3">
                <Button variant="outline" class="w-full justify-start" @click="clearCache">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  清除缓存
                </Button>
                <Button variant="outline" class="w-full justify-start" @click="exportData">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  导出数据
                </Button>
                <Button variant="outline" class="w-full justify-start" @click="restartSystem">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  重启系统
                </Button>
              </CardContent>
            </Card>

            <!-- 系统状态 -->
            <Card>
              <CardHeader>
                <CardTitle>系统状态</CardTitle>
              </CardHeader>
              <CardContent class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">CPU使用率</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ systemStatus.cpu }}%</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    class="bg-blue-600 dark:bg-blue-500 h-2 rounded-full" 
                    :style="{ width: systemStatus.cpu + '%' }"
                  ></div>
                </div>
                
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">内存使用率</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ systemStatus.memory }}%</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    class="bg-green-600 dark:bg-green-500 h-2 rounded-full" 
                    :style="{ width: systemStatus.memory + '%' }"
                  ></div>
                </div>
                
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">磁盘使用率</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ systemStatus.disk }}%</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    class="bg-yellow-600 dark:bg-yellow-500 h-2 rounded-full" 
                    :style="{ width: systemStatus.disk + '%' }"
                  ></div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </main>

    <!-- 编辑用户对话框 -->
    <div
      v-if="showEditUser"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click="closeEditDialog"
    >
      <div
        class="bg-white rounded-lg p-6 max-w-md w-full mx-4"
        @click.stop
      >
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold">编辑用户</h2>
          <Button variant="ghost" size="icon" @click="closeEditDialog">
            <X class="h-4 w-4" />
          </Button>
        </div>

        <form @submit.prevent="saveUser" class="space-y-4">
          <div>
            <label class="text-sm font-medium mb-2 block">用户名</label>
            <Input v-model="editingUser.username" required />
          </div>
          <div>
            <label class="text-sm font-medium mb-2 block">邮箱</label>
            <Input v-model="editingUser.email" type="email" required />
          </div>
          <div>
            <label class="text-sm font-medium mb-2 block">状态</label>
            <select
              v-model="editingUser.status"
              class="w-full h-10 px-3 py-2 border border-gray-300 rounded-md bg-white text-sm"
            >
              <option value="active">活跃</option>
              <option value="inactive">禁用</option>
            </select>
          </div>
          <div class="flex gap-2 pt-4">
            <Button type="submit" class="flex-1">保存</Button>
            <Button type="button" variant="outline" @click="closeEditDialog">取消</Button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- DeepSeek 配置编辑/创建对话框 -->
    <div
      v-if="showDeepSeekConfigDialog"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click="closeDeepSeekConfigDialog"
    >
      <div
        class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto"
        @click.stop
      >
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ editingDeepSeekConfig.id ? '编辑配置' : '创建配置' }}
          </h2>
          <Button variant="ghost" size="icon" @click="closeDeepSeekConfigDialog">
            <X class="h-4 w-4" />
          </Button>
        </div>

        <form @submit.prevent="saveDeepSeekConfig" class="space-y-4">
          <div>
            <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">API Key *</label>
            <Input 
              v-model="editingDeepSeekConfig.api_key" 
              type="password"
              placeholder="sk-xxxxxxxxxxxxx"
              required 
            />
          </div>
          <div>
            <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">Base URL</label>
            <Input 
              v-model="editingDeepSeekConfig.base_url" 
              placeholder="https://api.deepseek.com"
            />
          </div>
          <div>
            <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">Model</label>
            <Input 
              v-model="editingDeepSeekConfig.model" 
              placeholder="deepseek-chat"
            />
          </div>
          <div>
            <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">每分钟限流</label>
            <Input 
              v-model.number="editingDeepSeekConfig.rate_limit_per_minute" 
              type="number"
              placeholder="10"
            />
          </div>
          <div>
            <label class="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">每天限流</label>
            <Input 
              v-model.number="editingDeepSeekConfig.rate_limit_per_day" 
              type="number"
              placeholder="500"
            />
          </div>
          <div class="flex items-center gap-2">
            <Checkbox v-model="editingDeepSeekConfig.is_active" />
            <label class="text-sm text-gray-700 dark:text-gray-300">启用此配置</label>
          </div>
          <div class="flex gap-2 pt-4">
            <Button type="submit" class="flex-1">保存</Button>
            <Button type="button" variant="outline" @click="closeDeepSeekConfigDialog">取消</Button>
          </div>
        </form>
      </div>
    </div>

    <!-- 消息提示弹框 -->
    <MessageModal
      v-model:visible="showMessageModal"
      :type="messageModalType"
      :title="messageModalTitle"
      :message="messageModalMessage"
      :show-cancel="messageModalShowCancel"
      :confirm-text="messageModalConfirmText"
      :cancel-text="messageModalCancelText"
      @confirm="handleMessageConfirm"
      @cancel="handleMessageCancel"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, onBeforeUnmount } from 'vue'
import DashboardHeader from '@/components/DashboardHeader.vue'
import Card from '@/components/ui/Card.vue'
import MessageModal from '@/components/ui/MessageModal.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Badge from '@/components/ui/Badge.vue'
import Checkbox from '@/components/ui/Checkbox.vue'
import { X } from 'lucide-vue-next'
import { adminApi } from '@/services/api'
import { adminManagementApi, type DeepSeekConfig } from '@/services/adminManagementApi'
import type { AdminApiData } from '@/services/types'

// 统计数据
const stats = reactive({
  totalUsers: 0,
  activeCourses: 0,
  pendingTasks: 0,
  systemWarnings: 0
})

// 用户数据
const users = ref<Array<{id: number, username: string, email: string, status: 'active' | 'inactive'}>>([])

const userSearchQuery = ref('')
const showEditUser = ref(false)
const editingUser = ref({
  id: 0,
  username: '',
  email: '',
  status: 'active'
})

// 系统设置
const systemSettings = reactive({
  maintenanceMode: false,
  autoBackup: true,
  emailNotifications: true
})

// 系统状态
const systemStatus = reactive({
  cpu: 0,
  memory: 0,
  disk: 0,
  uptime: ''
})

// 消息弹框状态
const showMessageModal = ref(false)
const messageModalType = ref<'success' | 'error' | 'warning' | 'info'>('info')
const messageModalTitle = ref('提示')
const messageModalMessage = ref('')
const messageModalShowCancel = ref(false)
const messageModalConfirmText = ref('确定')
const messageModalCancelText = ref('取消')

let pendingAction: (() => void) | null = null

const showMessage = (
  type: 'success' | 'error' | 'warning' | 'info',
  title: string,
  message: string,
  showCancel = false,
  confirmText = '确定',
  cancelText = '取消'
) => {
  messageModalType.value = type
  messageModalTitle.value = title
  messageModalMessage.value = message
  messageModalShowCancel.value = showCancel
  messageModalConfirmText.value = confirmText
  messageModalCancelText.value = cancelText
  showMessageModal.value = true
}

const handleMessageConfirm = () => {
  if (pendingAction) {
    pendingAction()
    pendingAction = null
  }
}

const handleMessageCancel = () => {
  pendingAction = null
}

// 系统日志
const systemLogs = ref<Array<{id: number, level: 'info' | 'warning' | 'error', message: string, module?: string, user_id?: number | null, timestamp: string}>>([])
const logLevelFilter = ref<'warning' | 'error' | ''>('')

// DeepSeek 配置管理
const deepSeekConfigs = ref<DeepSeekConfig[]>([])
const showDeepSeekConfigDialog = ref(false)
const editingDeepSeekConfig = ref<Partial<DeepSeekConfig & { api_key: string }>>({
  api_key: '',
  base_url: 'https://api.deepseek.com',
  model: 'deepseek-chat',
  is_active: true,
  rate_limit_per_minute: 10,
  rate_limit_per_day: 500
})

// 计算属性
const filteredUsers = computed(() => {
  if (!userSearchQuery.value) return users.value
  return users.value.filter(user => 
    user.username.toLowerCase().includes(userSearchQuery.value.toLowerCase()) ||
    user.email.toLowerCase().includes(userSearchQuery.value.toLowerCase())
  )
})

// 方法
const refreshUsers = async () => {
  try {
    console.log('刷新用户列表')
    const usersData = await adminManagementApi.getUsers()
    if (usersData && Array.isArray(usersData)) {
      users.value = usersData
      stats.totalUsers = usersData.length
      console.log('✅ 用户列表刷新成功，共', usersData.length, '个用户')
    }
  } catch (error) {
    console.error('❌ 刷新用户列表失败:', error)
    showMessage('error', '错误', '刷新用户列表失败，请稍后重试')
  }
}

const editUser = (user: any) => {
  editingUser.value = { ...user }
  showEditUser.value = true
}

const saveUser = () => {
  const index = users.value.findIndex(u => u.id === editingUser.value.id)
  if (index > -1) {
    users.value[index] = { ...editingUser.value }
  }
  closeEditDialog()
}

const toggleUserStatus = (user: any) => {
  user.status = user.status === 'active' ? 'inactive' : 'active'
}

const closeEditDialog = () => {
  showEditUser.value = false
  editingUser.value = {
    id: 0,
    username: '',
    email: '',
    status: 'active'
  }
}

// 保存系统设置
const saveSystemSettings = async () => {
  try {
    console.log('保存系统设置:', systemSettings)
    
    // 调用API保存到后端
    await adminManagementApi.updateSystemSettings(systemSettings)
    
    console.log('✅ 系统设置已保存到数据库')
    showMessage('success', '成功', '系统设置已保存')
  } catch (error: any) {
    console.error('❌ 保存系统设置失败:', error)
    showMessage('error', '错误', '保存失败：' + (error.message || '未知错误'))
  }
}

const clearCache = () => {
  console.log('清除缓存')
  showMessage('success', '成功', '缓存已清除')
}

const exportData = () => {
  console.log('导出数据')
  showMessage('info', '提示', '数据导出已开始')
}

const restartSystem = () => {
  showMessage('warning', '确认重启', '确定要重启系统吗？这将影响所有用户。', true, '重启', '取消')
  pendingAction = () => {
    console.log('重启系统')
    showMessage('info', '提示', '系统重启中...')
  }
}

const getLogColor = (level: string) => {
  switch (level) {
    case 'error': return 'bg-red-500'
    case 'warning': return 'bg-yellow-500'
    case 'info': return 'bg-blue-500'
    default: return 'bg-gray-500'
  }
}

const getLogLevelColor = (level: string) => {
  switch (level) {
    case 'error': return 'text-red-600 dark:text-red-400'
    case 'warning': return 'text-yellow-600 dark:text-yellow-400'
    case 'info': return 'text-blue-600 dark:text-blue-400'
    default: return 'text-gray-600 dark:text-gray-400'
  }
}

// 格式化日志时间戳
const formatLogTimestamp = (timestamp: string) => {
  if (!timestamp) return ''
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const seconds = Math.floor(diff / 1000)
    const minutes = Math.floor(seconds / 60)
    const hours = Math.floor(minutes / 60)
    
    if (seconds < 60) return '刚刚'
    if (minutes < 60) return `${minutes}分钟前`
    if (hours < 24) return `${hours}小时前`
    
    // 超过24小时显示完整日期
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const h = String(date.getHours()).padStart(2, '0')
    const m = String(date.getMinutes()).padStart(2, '0')
    return `${month}-${day} ${h}:${m}`
  } catch (e) {
    return timestamp
  }
}

// 定时器引用
let systemStatusTimer: number | null = null

// 单独刷新系统状态
const refreshSystemStatus = async () => {
  try {
    // 获取服务器信息
    const serverInfo = await adminManagementApi.getServerInfo()
    
    if (serverInfo && serverInfo.resources) {
      // 更新系统状态
      systemStatus.cpu = serverInfo.resources.cpu.usage_percent
      systemStatus.memory = serverInfo.resources.memory.usage_percent
      systemStatus.disk = serverInfo.resources.disk.usage_percent
      
      if (serverInfo.resources.uptime) {
        systemStatus.uptime = serverInfo.resources.uptime.formatted || ''
      }
    }
  } catch (error) {
    console.error('❌ 刷新系统状态失败:', error)
  }
}

// DeepSeek 配置管理方法
const refreshDeepSeekConfigs = async () => {
  try {
    const response = await adminManagementApi.getDeepSeekConfigs(true)
    if (response && response.configs) {
      deepSeekConfigs.value = response.configs
      console.log('✅ DeepSeek 配置列表刷新成功，共', response.configs.length, '个配置')
    }
  } catch (error: any) {
    console.error('❌ 刷新 DeepSeek 配置列表失败:', error)
    if (error?.status !== 404) {
      showMessage('error', '错误', '刷新配置列表失败：' + (error.message || '未知错误'))
    }
  }
}

const showCreateDeepSeekConfig = () => {
  editingDeepSeekConfig.value = {
    api_key: '',
    base_url: 'https://api.deepseek.com',
    model: 'deepseek-chat',
    is_active: true,
    rate_limit_per_minute: 10,
    rate_limit_per_day: 500
  }
  showDeepSeekConfigDialog.value = true
}

const editDeepSeekConfig = (config: DeepSeekConfig) => {
  editingDeepSeekConfig.value = { ...config }
  showDeepSeekConfigDialog.value = true
}

const saveDeepSeekConfig = async () => {
  try {
    if (editingDeepSeekConfig.value.id) {
      // 更新配置
      await adminManagementApi.updateDeepSeekConfig(
        editingDeepSeekConfig.value.id,
        editingDeepSeekConfig.value
      )
      showMessage('success', '成功', '配置已更新')
    } else {
      // 创建配置
      await adminManagementApi.createDeepSeekConfig(
        editingDeepSeekConfig.value as Omit<DeepSeekConfig, 'id' | 'created_at' | 'updated_at'>
      )
      showMessage('success', '成功', '配置已创建')
    }
    closeDeepSeekConfigDialog()
    await refreshDeepSeekConfigs()
  } catch (error: any) {
    console.error('❌ 保存 DeepSeek 配置失败:', error)
    showMessage('error', '错误', '保存失败：' + (error.message || '未知错误'))
  }
}

const toggleDeepSeekConfig = async (configId: number) => {
  try {
    await adminManagementApi.toggleDeepSeekConfig(configId)
    showMessage('success', '成功', '配置状态已切换')
    await refreshDeepSeekConfigs()
  } catch (error: any) {
    console.error('❌ 切换配置状态失败:', error)
    showMessage('error', '错误', '操作失败：' + (error.message || '未知错误'))
  }
}

const deleteDeepSeekConfig = (configId: number) => {
  showMessage('warning', '确认删除', '确定要删除此配置吗？此操作不可恢复。', true, '删除', '取消')
  pendingAction = async () => {
    try {
      await adminManagementApi.deleteDeepSeekConfig(configId)
      showMessage('success', '成功', '配置已删除')
      await refreshDeepSeekConfigs()
    } catch (error: any) {
      console.error('❌ 删除配置失败:', error)
      showMessage('error', '错误', '删除失败：' + (error.message || '未知错误'))
    }
  }
}

const closeDeepSeekConfigDialog = () => {
  showDeepSeekConfigDialog.value = false
  editingDeepSeekConfig.value = {
    api_key: '',
    base_url: 'https://api.deepseek.com',
    model: 'deepseek-chat',
    is_active: true,
    rate_limit_per_minute: 10,
    rate_limit_per_day: 500
  }
}

const maskApiKey = (apiKey: string): string => {
  if (!apiKey || apiKey.length < 8) return '****'
  const prefix = apiKey.substring(0, 7)
  const suffix = apiKey.substring(apiKey.length - 4)
  return `${prefix}****${suffix}`
}

const formatDateTime = (dateString: string): string => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day} ${hours}:${minutes}`
  } catch (e) {
    return dateString
  }
}

// 刷新系统日志（只显示 warning 和 error）
const refreshSystemLogs = async () => {
  try {
    const options: { level?: 'warning' | 'error'; limit?: number } = {
      limit: 50
    }
    // 只允许查询 warning 或 error，不允许 info
    if (logLevelFilter.value === 'warning' || logLevelFilter.value === 'error') {
      options.level = logLevelFilter.value
    }
    const logs = await adminManagementApi.getSystemLogs(options)
    systemLogs.value = logs || []
    console.log('✅ 系统日志刷新成功，共', logs?.length || 0, '条日志')
  } catch (error: any) {
    console.error('❌ 刷新系统日志失败:', error)
    if (error?.status !== 404) {
      showMessage('error', '错误', '刷新日志失败：' + (error.message || '未知错误'))
    }
  }
}

// 初始化管理员数据
const initAdminData = async () => {
  try {
    console.log('开始加载管理员数据...')
    
    // 分别加载用户列表和服务器信息
    const [usersData, serverInfo] = await Promise.all([
      adminManagementApi.getUsers().catch(err => {
        console.error('加载用户列表失败:', err)
        return []
      }),
      adminManagementApi.getServerInfo().catch(err => {
        console.error('加载服务器信息失败:', err)
        return null
      })
    ])
    
    console.log('获取到的数据:', {
      users: usersData?.length || 0,
      serverInfo: serverInfo ? '已加载' : '未加载'
    })
    
    // 更新用户数据
    if (usersData && Array.isArray(usersData)) {
      users.value = usersData
      stats.totalUsers = usersData.length
    }
    
    // 更新系统状态（从服务器信息）
    if (serverInfo && serverInfo.resources) {
      systemStatus.cpu = serverInfo.resources.cpu.usage_percent
      systemStatus.memory = serverInfo.resources.memory.usage_percent
      systemStatus.disk = serverInfo.resources.disk.usage_percent
      
      // 如果有运行时间信息，也更新到系统状态中
      if (serverInfo.resources.uptime) {
        systemStatus.uptime = serverInfo.resources.uptime.formatted || ''
      }
    }
    
    // 加载系统日志（只显示 warning 和 error）
    await refreshSystemLogs()
    
    // 加载 DeepSeek 配置列表
    await refreshDeepSeekConfigs()
    
    console.log('✅ 管理员数据加载完成')
  } catch (error) {
    console.error('加载管理员数据失败:', error)
  }
}

// 组件挂载时加载数据
onMounted(() => {
  // 首次加载所有数据
  initAdminData()
  
  // 每隔5秒自动刷新系统状态
  systemStatusTimer = window.setInterval(() => {
    refreshSystemStatus()
  }, 5000)
})

// 组件卸载时清除定时器
onBeforeUnmount(() => {
  if (systemStatusTimer) {
    clearInterval(systemStatusTimer)
  }
})

</script>

