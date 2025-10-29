<template>
  <Card class="ai-chat-container flex flex-col overflow-hidden" style="height: 600px; max-height: 600px; min-height: 600px;">
    <CardHeader class="bg-white dark:bg-[#0a0f1a] border-b border-gray-100 dark:border-gray-900 flex-shrink-0 py-2">
      <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
          <img src="/ai-avatar.png" alt="AI" class="w-7 h-7 rounded-full object-cover" />
          <CardTitle class="text-base font-semibold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
            AI智能助手
          </CardTitle>
        </div>
        <Button variant="outline" size="sm" class="h-7 text-xs hover:bg-white/80 dark:hover:bg-white/10 dark:text-white dark:border-white/20 transition-colors" @click="clearChat">
          <RotateCcw class="h-3 w-3 mr-1" />
          清空对话
        </Button>
      </div>
    </CardHeader>
    <CardContent class="p-0 bg-white dark:bg-[#0a0f1a] flex-1 flex flex-col overflow-hidden min-h-0">
      <div class="ai-chat-scroll-container flex-1 overflow-y-auto" style="min-height: 0; max-height: 100%;">
        <!-- 聊天消息列表 -->
          <div class="p-4 space-y-3">
          <div v-if="messages.length === 0" class="text-center py-6">
            <div class="w-12 h-12 mx-auto mb-3 rounded-full overflow-hidden shadow-lg">
              <img src="/ai-avatar.png" alt="AI" class="w-full h-full object-cover" />
            </div>
            <h3 class="text-base font-semibold text-gray-800 dark:text-white/70 mb-1">你好！我是你的AI智能助手</h3>
            <p class="text-xs text-gray-500 dark:text-white/50 mb-3">我可以帮助你管理任务、安排课程、分析数据</p>
            <div class="flex flex-wrap gap-1.5 justify-center">
              <span class="px-2 py-0.5 bg-blue-100 dark:bg-[#0f1625] text-blue-700 dark:text-blue-400/70 rounded-full text-[10px] border dark:border-gray-800">任务管理</span>
              <span class="px-2 py-0.5 bg-purple-100 dark:bg-[#0f1625] text-purple-700 dark:text-purple-400/70 rounded-full text-[10px] border dark:border-gray-800">课程安排</span>
              <span class="px-2 py-0.5 bg-green-100 dark:bg-[#0f1625] text-green-700 dark:text-green-400/70 rounded-full text-[10px] border dark:border-gray-800">数据分析</span>
              <span class="px-2 py-0.5 bg-orange-100 dark:bg-[#0f1625] text-orange-700 dark:text-orange-400/70 rounded-full text-[10px] border dark:border-gray-800">时间规划</span>
            </div>
          </div>
          
          <div
            v-for="message in messages"
            :key="message.id"
            :class="cn(
              'flex gap-3 animate-in slide-in-from-bottom-2 duration-300 mb-4 last:mb-0',
              message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
            )"
          >
            <!-- 头像 - 分离出来 -->
            <div class="flex-shrink-0 mt-1">
              <div :class="cn(
                'w-7 h-7 rounded-full overflow-hidden flex items-center justify-center',
                message.role === 'user' 
                  ? 'bg-gray-200 dark:bg-gray-700' 
                  : ''
              )">
                <img 
                  v-if="message.role !== 'user'"
                  src="/ai-avatar.png" 
                  alt="AI" 
                  class="w-full h-full object-cover"
                />
                <User v-else class="h-3.5 w-3.5 text-gray-600 dark:text-gray-300" />
              </div>
            </div>
            
            <!-- 消息气泡 -->
            <div :class="cn('flex flex-col', message.role === 'user' ? 'items-end' : 'items-start')">
              <div
                :class="cn(
                  'rounded-2xl px-4 py-2.5 text-sm transition-all duration-200',
                  message.role === 'user'
                    ? 'bg-white dark:bg-[#0f1625] text-gray-800 dark:text-white border border-gray-100 dark:border-gray-800 markdown-user-content max-w-[85%]'
                    : 'bg-white dark:bg-[#0f1625] text-gray-800 dark:text-white border border-gray-100 dark:border-gray-800 markdown-assistant-content max-w-[75%]'
                )"
              >
                <div 
                  v-if="message.content"
                  :class="cn(
                    'markdown-content leading-relaxed prose prose-sm max-w-none',
                    message.role === 'user' ? 'text-gray-800 dark:text-white' : 'text-gray-800 dark:text-white dark:prose-invert'
                  )"
                  v-html="parseMarkdown(message.content || '')"
                ></div>
                <div 
                  v-else-if="message.role === 'assistant' && isLoading && message.id === currentStreamingMessage?.id"
                  class="flex items-center gap-1.5"
                >
                  <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                  <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                  <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  <span class="text-xs text-gray-400 dark:text-white/60 ml-1">正在思考...</span>
                </div>
                <!-- 注入的消息样式（通过scoped style标签）会在这里生效 -->
              </div>
              <span :class="cn(
                'text-xs mt-1.5 px-2',
                message.role === 'user' ? 'text-gray-400 dark:text-white/50 text-right' : 'text-gray-400 dark:text-white/50'
              )">
                {{ formatTime(message.timestamp) }}
              </span>
            </div>
          </div>
          
          <!-- 加载状态 - 只在没有AI消息占位符时显示（作为后备） -->
          <div v-if="isLoading && !messages.some(m => m.role === 'assistant' && m.id === currentStreamingMessage?.id)" class="flex gap-2 animate-in slide-in-from-bottom-2 duration-300">
            <!-- 头像 -->
            <div class="flex-shrink-0 mt-1">
              <div class="w-7 h-7 rounded-full overflow-hidden">
                <img src="/ai-avatar.png" alt="AI" class="w-full h-full object-cover" />
              </div>
            </div>
            <!-- 加载气泡 -->
            <div class="flex flex-col">
              <div class="bg-white dark:bg-[#0f1625] text-gray-800 dark:text-white rounded-2xl px-3 py-2 text-sm border border-gray-100 dark:border-gray-800">
                <div class="flex items-center gap-1.5">
                  <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                  <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                  <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  <span class="text-xs text-gray-400 dark:text-white/60 ml-1">正在思考...</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 输入框 -->
      <div class="border-t border-gray-200 dark:border-gray-900 bg-white dark:bg-[#0a0f1a] px-3 py-2 flex-shrink-0">
        <div class="flex items-end gap-2 bg-gray-50 dark:bg-[#0f1625] rounded-xl px-2.5 py-2 border border-gray-200 dark:border-gray-800 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500/20 transition-all duration-200">
          <div class="flex-1">
            <textarea
              v-model="inputMessage"
              placeholder="输入消息..."
              class="w-full bg-transparent border-none outline-none resize-none text-xs placeholder-gray-400 dark:placeholder-white/40 text-gray-900 dark:text-white min-h-[32px] max-h-20 leading-5"
              style="caret-color: hsl(var(--foreground));"
              @keydown.enter.exact.prevent="sendMessage"
              @keydown.enter.shift.exact="inputMessage += '\n'"
              :disabled="isLoading"
              rows="1"
              ref="textareaRef"
            ></textarea>
          </div>
          <div class="flex-shrink-0 pb-0.5">
            <Button 
              size="sm" 
              @click="sendMessage"
              :disabled="!inputMessage.trim() || isLoading"
                class="w-7 h-7 p-0 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send class="h-3.5 w-3.5" />
            </Button>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { User, Send, RotateCcw } from 'lucide-vue-next'
// @ts-ignore - marked类型定义问题
import { marked } from 'marked'
// @ts-ignore - dompurify类型定义问题
import DOMPurify from 'dompurify'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Button from '@/components/ui/Button.vue'
import { cn } from '@/lib/utils'
import { tokenManager } from '@/services/authApi'

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  injectedStyles?: string // 注入的CSS样式
}

const messages = ref<Message[]>([])
const inputMessage = ref('')
const isLoading = ref(false)
const textareaRef = ref<HTMLTextAreaElement>()
const currentStreamingMessage = ref<Message | null>(null)
let messageId = 0

// 配置marked
marked.setOptions({
  breaks: true, // 支持换行
  gfm: true, // 支持GitHub风格的Markdown
})

// 提取并注入CSS样式
const extractAndInjectStyles = (content: string): { html: string; styles: string[] } => {
  const styles: string[] = []
  
  // 提取<style>标签中的CSS
  const styleTagRegex = /<style[^>]*>([\s\S]*?)<\/style>/gi
  let match
  while ((match = styleTagRegex.exec(content)) !== null) {
    if (match[1]) {
      styles.push(match[1])
    }
  }
  
  // 移除<style>标签，保留其他内容
  const htmlWithoutStyles = content.replace(styleTagRegex, '')
  
  return { html: htmlWithoutStyles, styles }
}

// 解析Markdown和HTML为安全HTML，支持CSS
const parseMarkdown = (content: string): string => {
  if (!content || typeof content !== 'string') {
    return ''
  }
  
  // 清理内容，移除可能导致渲染问题的字符
  content = content.trim()
  if (!content) {
    return ''
  }
  
  // 防止单独的数字被误解析为HTML实体
  if (/^\d+$/.test(content) && content.length <= 3) {
    return content
  }
  
  try {
    // 检查是否包含HTML标签（包括完整的HTML文档结构）
    const hasHtmlTags = /<[^>]+>/g.test(content)
    const hasHtmlDocStructure = /<!DOCTYPE|<\s*html|<\s*body|<\s*head/i.test(content)
    
    // 检查是否是不完整或无效的HTML标签（如 <div></di 或 <div><div）
    // 不完整标签特征：以<开头但没有>结尾
    // 更严格的检查：确保所有标签都是完整的
    const incompleteTagPattern = /<[^>]*$/gm  // 多行模式，检查每行末尾的不完整标签
    const hasIncompleteTags = incompleteTagPattern.test(content)
    
    
    let html: string
    let extractedStyles: string[] = []
    
    if (hasHtmlDocStructure) {
      // 如果是完整的HTML文档，尝试提取body内容和CSS
      try {
        const tempDiv = document.createElement('div')
        tempDiv.innerHTML = content
        
        // 提取CSS样式
        const styleResult = extractAndInjectStyles(content)
        extractedStyles = styleResult.styles
        
        const bodyContent = tempDiv.querySelector('body')?.innerHTML || 
                           tempDiv.querySelector('html')?.innerHTML || 
                           styleResult.html
        
        // 清理提取的内容，保留常用HTML标签和style属性
        html = DOMPurify.sanitize(bodyContent, {
          ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'del', 'span', 'div'],
          ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'style', 'id']
        })
        
        // 如果提取后为空，尝试直接清理原内容
        if (!html || !html.trim()) {
          html = DOMPurify.sanitize(styleResult.html, {
            ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'del', 'span', 'div'],
            ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'style', 'id']
          })
        }
      } catch {
        // 如果解析失败，提取CSS并清理HTML
        const styleResult = extractAndInjectStyles(content)
        extractedStyles = styleResult.styles
        html = DOMPurify.sanitize(styleResult.html, {
          ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'del', 'span', 'div'],
          ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'style', 'id']
        })
      }
    } else if (hasHtmlTags && !hasIncompleteTags) {
      // 如果包含完整HTML标签且不是不完整标签，提取CSS并处理
      try {
        const styleResult = extractAndInjectStyles(content)
        extractedStyles = styleResult.styles
        
        const sanitizedHtml = DOMPurify.sanitize(styleResult.html, {
          ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'del', 'span', 'div'],
          ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'style', 'id']
        })
        // 如果清理后还有内容，先用Markdown解析（可能混合了Markdown语法）
        if (sanitizedHtml && sanitizedHtml.trim() && sanitizedHtml !== styleResult.html.replace(/<(?!\/?[a-z][^>]*>)/gi, '&lt;')) {
          html = marked.parse(sanitizedHtml) as string
        } else {
          html = sanitizedHtml
        }
      } catch {
        html = marked.parse(content) as string
      }
    } else if (hasIncompleteTags && hasHtmlTags) {
      // 不完整的HTML标签，转义显示为文本
      html = content.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      // 然后解析为Markdown（支持代码块等格式）
      html = marked.parse(html) as string
    } else {
      // 纯文本或Markdown，直接用Markdown解析（会自动处理HTML转义）
      html = marked.parse(content) as string
    }
    
    // 最后再次清理，确保安全
    html = DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'del', 'span', 'div'],
      ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'style', 'id']
    })
    
    // 如果有提取的CSS样式，注入到HTML中
    let styleHtml = ''
    if (extractedStyles.length > 0) {
      const sanitizedStyles = extractedStyles
        .map(style => DOMPurify.sanitize(style, { ALLOWED_TAGS: [], ALLOWED_ATTR: [] }))
        .filter(s => s && s.trim())
        .join('\n')
      
      if (sanitizedStyles) {
        // 使用唯一ID作用域CSS
        const styleId = `ai-message-style-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
        // 为CSS添加作用域（使用消息容器的唯一类名）
        const scopedStyles = sanitizedStyles
          .replace(/([^{}]+)\{/g, (_match, selector) => {
            // 为每个选择器添加作用域前缀
            return `.ai-message-content-${styleId} ${selector.trim()} {`
          })
        styleHtml = `<style class="ai-message-style" data-style-id="${styleId}">${scopedStyles}</style>`
        html = `<div class="ai-message-content-${styleId}">${html}</div>`
      }
    }
    
    return styleHtml + html
  } catch (error) {
    console.error('Markdown/HTML解析失败:', error)
    // 如果解析失败，尝试直接清理HTML作为备选
    try {
      const styleResult = extractAndInjectStyles(content)
      let result = DOMPurify.sanitize(styleResult.html, {
        ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'del', 'span', 'div'],
        ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'style', 'id']
      })
      
      // 注入CSS
      if (styleResult.styles.length > 0) {
        const sanitizedStyles = styleResult.styles
          .map(style => DOMPurify.sanitize(style, { ALLOWED_TAGS: [], ALLOWED_ATTR: [] }))
          .filter(s => s && s.trim())
          .join('\n')
        if (sanitizedStyles) {
          const styleId = `ai-message-style-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
          const scopedStyles = sanitizedStyles
            .replace(/([^{}]+)\{/g, (_match, selector) => {
              return `.ai-message-content-${styleId} ${selector.trim()} {`
            })
          result = `<style class="ai-message-style" data-style-id="${styleId}">${scopedStyles}</style><div class="ai-message-content-${styleId}">${result}</div>`
        }
      }
      
      return result
    } catch {
      // 最后保底：转义HTML字符（确保显示为文本）
      return content.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/&/g, '&amp;')
    }
  }
}


// 自动调整textarea高度
const adjustTextareaHeight = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    textareaRef.value.style.height = Math.min(textareaRef.value.scrollHeight, 80) + 'px'
  }
}

// 监听输入内容变化，自动调整高度
watch(inputMessage, () => {
  nextTick(() => {
    adjustTextareaHeight()
  })
})

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value) return
  
  const currentInput = inputMessage.value.trim()
  const userMessage: Message = {
    id: messageId++,
    role: 'user',
    content: currentInput,
    timestamp: new Date()
  }
  
  // 立即添加用户消息，使用响应式赋值确保触发渲染
  messages.value = [...messages.value, userMessage]
  
  // 清空输入框
  inputMessage.value = ''
  
  // 立即触发一次强制更新（首次发送时特别重要）
  await nextTick()
  // 如果是第一次消息（数组长度为1），再等待一次tick确保初始化完成
  if (messages.value.length === 1) {
    await nextTick()
  }
  
  // 重置textarea高度并滚动到底部
  if (textareaRef.value) {
    textareaRef.value.style.height = '32px'
  }
  
  scrollToBottom()
  
  isLoading.value = true
  currentStreamingMessage.value = null
  
  // 创建AI消息占位符
  const aiMessageId = messageId++
  const aiMessage: Message = {
    id: aiMessageId,
    role: 'assistant',
    content: '',
    timestamp: new Date()
  }
  
  // 添加AI消息占位符
  messages.value.push(aiMessage)
  currentStreamingMessage.value = aiMessage
  
  await nextTick()
  scrollToBottom()
  
  try {
    // 构造对话历史（排除当前正在生成的AI消息）
    const conversationHistory = messages.value
      .filter(msg => msg.id !== aiMessageId && msg.content.trim())
      .map(msg => ({
        role: msg.role,
        content: msg.content
      }))
    
    // 尝试使用流式传输，传递对话历史作为上下文
    await streamAIResponse(currentInput, aiMessage, conversationHistory)
  } catch (error) {
    console.error('AI回复失败:', error)
    // 更新AI消息为错误提示
    const index = messages.value.findIndex(msg => msg.id === aiMessageId)
    if (index !== -1) {
      let errorMessage = '抱歉，AI服务暂时不可用，请稍后重试。'
      // 如果是401错误，提示用户重新登录
      if (error instanceof Error && error.message.includes('认证失败')) {
        errorMessage = '认证失败，请重新登录后再试。'
      } else if (error instanceof Error && error.message.includes('401')) {
        errorMessage = '认证失败，请重新登录后再试。'
      }
      messages.value[index] = { 
        ...messages.value[index], 
        content: errorMessage 
      }
    }
  } finally {
    isLoading.value = false
    currentStreamingMessage.value = null
    await nextTick()
    scrollToBottom()
  }
}

// 流式传输AI回复
const streamAIResponse = async (
  userInput: string, 
  message: Message, 
  history: Array<{role: 'user' | 'assistant', content: string}> = []
) => {
  // @ts-ignore - Vite 环境变量类型
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'
  // 使用tokenManager统一获取token
  const token = tokenManager.getToken()
  
  try {
    // 构造请求体，包含当前消息和对话历史
    const requestBody: {
      message: string
      history?: Array<{role: 'user' | 'assistant', content: string}>
    } = {
      message: userInput
    }
    
    // 如果有对话历史，添加到请求中
    if (history.length > 0) {
      requestBody.history = history
    }
    
    const response = await fetch(`${API_BASE_URL}/ai/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
      body: JSON.stringify(requestBody)
    })
    
    if (!response.ok) {
      // 如果是401错误，提供更详细的提示
      if (response.status === 401) {
        throw new Error('认证失败，请重新登录')
      }
      // 如果是404，说明后端可能还没有实现流式接口
      if (response.status === 404) {
        throw new Error('流式传输接口未实现，请检查后端服务')
      }
      const errorText = await response.text().catch(() => '')
      throw new Error(`HTTP error! status: ${response.status}${errorText ? ` - ${errorText}` : ''}`)
    }
    
    // 检查响应类型是否为流式传输
    const contentType = response.headers.get('content-type')
    if (!contentType || !contentType.includes('text/event-stream')) {
      console.warn('警告: 响应不是 SSE 格式，但继续处理')
    }
    
    const reader = response.body?.getReader()
    const decoder = new TextDecoder()
    
    if (!reader) {
      throw new Error('无法获取响应流')
    }
    
    let accumulatedContent = ''
    let buffer = '' // 用于存储不完整的行
    
    // 设置当前流式消息
    currentStreamingMessage.value = message
    
    while (true) {
      const { done, value } = await reader.read()
      
      if (done) {
        // 处理剩余的缓冲区内容
        if (buffer.trim()) {
          const lines = buffer.split('\n')
          for (const line of lines) {
            const trimmedLine = line.trim()
            if (trimmedLine.startsWith('data: ')) {
              const data = trimmedLine.slice(6)
              if (data === '[DONE]') {
                break
              }
              if (data && data !== '[DONE]') {
                try {
                  const parsed = JSON.parse(data)
                  if (parsed.error) {
                    const index = messages.value.findIndex(m => m.id === message.id)
                    if (index !== -1) {
                      messages.value[index].content = accumulatedContent + `\n\n❌ 错误: ${parsed.error}`
                    }
                  } else if (parsed.content) {
                    accumulatedContent += parsed.content
                    // 更新剩余内容
                    const index = messages.value.findIndex(m => m.id === message.id)
                    if (index !== -1) {
                      messages.value[index].content = accumulatedContent
                    }
                  }
                } catch (e) {
                  // 如果不是JSON，直接追加文本（容错处理）
                  accumulatedContent += data
                  const index = messages.value.findIndex(m => m.id === message.id)
                  if (index !== -1) {
                    messages.value[index].content = accumulatedContent
                  }
                }
              }
            }
          }
        }
        break
      }
      
      // 解码当前块并添加到缓冲区
      const chunk = decoder.decode(value, { stream: true })
      buffer += chunk
      
      // SSE 格式：每行以 "data: " 开头，行之间用 \n 分隔
      // 每个完整的事件（data: {...}）可能以 \n 或 \n\n 结尾
      // 为了实时显示，我们逐行处理
      const lines = buffer.split('\n')
      // 保留最后一个不完整的行在缓冲区中
      buffer = lines.pop() || ''
      
      // 处理每一行，实时更新UI - 每个片段立即更新
      for (const line of lines) {
        const trimmedLine = line.trim()
        if (!trimmedLine) continue
        
        // SSE 格式: data: {...} 或 data: [DONE]
        if (trimmedLine.startsWith('data: ')) {
          const data = trimmedLine.slice(6) // 移除 "data: " 前缀
          
          // 处理结束标记
          if (data === '[DONE]') {
            isLoading.value = false
            currentStreamingMessage.value = null
            // 确保最终内容被设置
            const finalIndex = messages.value.findIndex(m => m.id === message.id)
            if (finalIndex !== -1) {
              messages.value[finalIndex].content = accumulatedContent
            }
            await nextTick()
            scrollToBottom()
            return // 流式传输结束
          }
          
          if (!data) continue
          
          try {
            // 尝试解析 JSON
            const parsed = JSON.parse(data)
            
            // 处理错误响应
            if (parsed.error) {
              const errorMsg = parsed.error || '未知错误'
              const index = messages.value.findIndex(m => m.id === message.id)
              if (index !== -1) {
                messages.value[index].content = accumulatedContent + `\n\n❌ 错误: ${errorMsg}`
              }
              isLoading.value = false
              currentStreamingMessage.value = null
              await nextTick()
              scrollToBottom()
              console.error('AI错误:', parsed.error)
              return
            }
            
            // 处理正常内容（按照文档，使用 content 字段）
            if (parsed.content) {
              // 立即追加内容
              accumulatedContent += parsed.content
              
              // 立即更新UI - 关键：每个片段立即更新！
              const index = messages.value.findIndex(m => m.id === message.id)
              if (index !== -1) {
                // 方法1：直接更新属性（Vue 3应该能检测到）
                messages.value[index].content = accumulatedContent
                
                // 方法2：如果方法1不行，强制替换整个消息对象（确保响应式更新）
                // messages.value[index] = { 
                //   ...messages.value[index], 
                //   content: accumulatedContent 
                // }
                
                // 调试日志（可以在浏览器控制台看到实时更新）
                // console.log('实时更新:', parsed.content, '累计:', accumulatedContent)
                
                // 立即触发滚动（异步执行确保DOM已更新）
                setTimeout(() => {
                  scrollToBottom()
                }, 0)
              }
            }
          } catch (e) {
            // 如果不是 JSON，可能是纯文本响应（兼容处理）
            console.warn('解析数据失败，尝试作为纯文本处理:', e, data)
            if (data && data !== '[DONE]') {
              // 立即追加并更新
              accumulatedContent += data
              const index = messages.value.findIndex(m => m.id === message.id)
              if (index !== -1) {
                messages.value[index].content = accumulatedContent
                Promise.resolve().then(() => {
                  scrollToBottom()
                })
              }
            }
          }
        }
      }
    }
    
    // 确保最终内容被设置
    const finalIndex = messages.value.findIndex(m => m.id === message.id)
    if (finalIndex !== -1) {
      messages.value[finalIndex].content = accumulatedContent
    }
    
    // 清除流式消息标记
    currentStreamingMessage.value = null
    isLoading.value = false
    
    // 最终滚动到底部
    await nextTick()
    scrollToBottom()
  } catch (error: any) {
    console.error('流式传输错误:', error)
    
    // 设置错误消息
    const index = messages.value.findIndex(m => m.id === message.id)
    if (index !== -1) {
      messages.value[index].content = messages.value[index].content || `错误: ${error.message || '流式传输失败'}`
    }
    
    // 清除状态
    currentStreamingMessage.value = null
    isLoading.value = false
    
    throw error
  }
}

const formatTime = (date: Date): string => {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}小时前`
  
  return date.toLocaleDateString('zh-CN', { 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const clearChat = () => {
  messages.value = []
  inputMessage.value = ''
  isLoading.value = false
  currentStreamingMessage.value = null
  messageId = 0
}

// 自动滚动到底部
const scrollToBottom = () => {
  // 使用 requestAnimationFrame 确保在DOM更新后滚动
  requestAnimationFrame(() => {
    const scrollContainer = document.querySelector('.ai-chat-scroll-container')
    if (scrollContainer) {
      scrollContainer.scrollTop = scrollContainer.scrollHeight
    }
  })
}

// 监听消息变化，自动滚动
watch(messages, () => {
  scrollToBottom()
}, { deep: true })

watch(isLoading, (newVal) => {
  if (!newVal) {
    scrollToBottom()
  }
})
</script>

<style scoped>
.ai-chat-container {
  height: 605px !important;
  max-height: 602px !important;
  min-height: 600px !important;
}

.ai-chat-scroll-container {
  /* 显示滚动条，确保内容可以滚动 */
  overflow-y: auto;
  overflow-x: hidden;
}

.ai-chat-scroll-container::-webkit-scrollbar {
  width: 6px;
}

.ai-chat-scroll-container::-webkit-scrollbar-track {
  background: transparent;
}

.ai-chat-scroll-container::-webkit-scrollbar-thumb {
  background: hsl(var(--muted-foreground));
  border-radius: 3px;
}

.ai-chat-scroll-container::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--foreground));
}

/* Markdown内容样式 */
.markdown-content {
  overflow-wrap: break-word;
  white-space: normal;
  word-break: normal;
  line-height: 1.6;
  width: 100%;
}

/* 用户消息气泡样式 - 优化显示 */
.markdown-user-content {
  min-width: 80px;
}

.markdown-user-content .markdown-content {
  line-height: 1.6;
  white-space: normal;
  word-break: normal;
  overflow-wrap: break-word;
  text-align: left;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  font-weight: 600;
  margin-top: 0.75em;
  margin-bottom: 0.5em;
  line-height: 1.25;
}

.markdown-content h1 { font-size: 1.5em; }
.markdown-content h2 { font-size: 1.25em; }
.markdown-content h3 { font-size: 1.1em; }

.markdown-content p {
  margin: 0.5em 0;
  line-height: 1.6;
}

.markdown-content p:first-child {
  margin-top: 0;
}

.markdown-content p:last-child {
  margin-bottom: 0;
}

.markdown-content ul,
.markdown-content ol {
  margin: 0.75em 0;
  padding-left: 1.5em;
  line-height: 1.8;
}

.markdown-content li {
  margin: 0.4em 0;
  line-height: 1.6;
}

.markdown-content code {
  background: hsl(var(--muted));
  padding: 0.2em 0.4em;
  border-radius: 0.25em;
  font-size: 0.9em;
  font-family: 'Courier New', monospace;
  line-height: 1.5;
}

.markdown-content pre {
  background: hsl(var(--muted));
  padding: 0.75em;
  border-radius: 0.5em;
  overflow-x: auto;
  margin: 0.75em 0;
}

.markdown-content pre code {
  background: none;
  padding: 0;
}

.markdown-content blockquote {
  border-left: 3px solid hsl(var(--primary));
  padding-left: 1em;
  margin: 0.75em 0;
  color: hsl(var(--muted-foreground));
  font-style: italic;
  line-height: 1.6;
}

.markdown-content a {
  color: hsl(var(--primary));
  text-decoration: underline;
}

.markdown-content a:hover {
  opacity: 0.8;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.75em 0;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid hsl(var(--border));
  padding: 0.5em;
  text-align: left;
}

.markdown-content th {
  background: hsl(var(--muted));
  font-weight: 600;
}

/* 用户消息（白色背景）的Markdown样式 */
.markdown-user-content .markdown-content {
  color: hsl(var(--foreground));
}

.markdown-user-content .markdown-content h1,
.markdown-user-content .markdown-content h2,
.markdown-user-content .markdown-content h3,
.markdown-user-content .markdown-content h4,
.markdown-user-content .markdown-content h5,
.markdown-user-content .markdown-content h6 {
  color: hsl(var(--foreground));
}

.markdown-user-content .markdown-content code {
  background: hsl(var(--muted));
  color: hsl(var(--foreground));
}

.markdown-user-content .markdown-content pre {
  background: hsl(var(--muted));
  color: hsl(var(--foreground));
}

.markdown-user-content .markdown-content pre code {
  background: none;
  color: hsl(var(--foreground));
}

.markdown-user-content .markdown-content blockquote {
  border-left-color: hsl(var(--primary));
  color: hsl(var(--muted-foreground));
}

.markdown-user-content .markdown-content a {
  color: hsl(var(--primary));
  text-decoration: underline;
}

.markdown-user-content .markdown-content a:hover {
  opacity: 0.8;
}

.markdown-user-content .markdown-content th,
.markdown-user-content .markdown-content td {
  border-color: hsl(var(--border));
  color: hsl(var(--foreground));
}

.markdown-user-content .markdown-content th {
  background: hsl(var(--muted));
}

/* AI消息（浅色背景）的Markdown样式 */
.markdown-assistant-content .markdown-content {
  color: hsl(var(--foreground));
}

.markdown-assistant-content .markdown-content code {
  background: hsl(var(--muted));
  color: hsl(var(--foreground));
}

/* 消息中的scoped样式会在这里生效 */
.markdown-content style[scoped] {
  display: none; /* 隐藏style标签本身 */
}

/* 确保注入的样式能够作用到消息内容 */
.markdown-content {
  position: relative;
}

/* 支持消息内注入的样式 */
.markdown-content style {
  display: none !important;
}

/* 移除所有消息气泡的阴影 */
.markdown-user-content,
.markdown-assistant-content {
  box-shadow: none !important;
}

/* 移除Card容器的阴影 */
.ai-chat-container {
  box-shadow: none !important;
}

/* 移除所有可能的阴影效果 */
.ai-chat-container * {
  box-shadow: none !important;
}

/* 确保Card组件内部没有阴影 */
.ai-chat-container .rounded-lg {
  box-shadow: none !important;
}
</style>
