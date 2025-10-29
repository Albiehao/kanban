import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { courseApi, taskApi, financeApi, mockApi, type FinanceStatsApiData } from '@/services/api'

export interface Course {
  id: number
  name: string
  time: string
  timeSlots: string[] // 多个连续时间段
  location: string
  color: string
  date: string
  day?: string // 星期几
  teacher?: string // 教师
  periods?: string // 节次信息
}

export interface Task {
  id: number
  title: string
  completed: boolean
  priority: 'high' | 'medium' | 'low'
  date: string
  time?: string  // 时间段，例如 "09:00-11:00"
  hasReminder?: boolean  // 是否有提醒标志（前端使用）
  has_reminder?: boolean  // 后端返回的字段名
  description?: string
  reminder_time?: string
}

export interface Transaction {
  id: number
  type: 'income' | 'expense'
  amount: number
  category: string
  description: string
  date: string
  time?: string // 具体时间，格式：HH:MM，如 "14:30"，可选
}

export interface ModuleConfig {
  id: string
  name: string
  visible: boolean
  column: 'left' | 'middle' | 'right'
}

// 获取指定日期所在周的指定星期几的日期
const getWeekDate = (selectedDate: Date, dayOfWeek: number) => {
  const currentDay = selectedDate.getDay() // 0=周日, 1=周一, ..., 6=周六
  const mondayOffset = currentDay === 0 ? -6 : 1 - currentDay // 计算到周一的偏移
  const monday = new Date(selectedDate)
  monday.setDate(selectedDate.getDate() + mondayOffset)
  
  const targetDate = new Date(monday)
  targetDate.setDate(monday.getDate() + dayOfWeek - 1) // dayOfWeek: 1=周一, 2=周二, ...
  
  // 使用本地日期格式，避免时区问题
  const year = targetDate.getFullYear()
  const month = String(targetDate.getMonth() + 1).padStart(2, '0')
  const day = String(targetDate.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 获取星期几名称
const getDayName = (dayOfWeek: number) => {
  const dayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  return dayNames[dayOfWeek - 1] // dayOfWeek: 1=周一, 2=周二, ...
}

// 从API加载课程数据的函数
const loadCoursesFromApi = async () => {
  try {
    const response = await courseApi.getCourses()
    // 从统一格式 {data: [...]} 中提取数据
    return response.data || response || []
  } catch (error) {
    console.error('加载课程数据失败:', error)
    return null
  }
}

// 从API加载任务数据的函数 - 一次性加载3页数据优化体验
const loadTasksFromApi = async () => {
  try {
    // 静默加载任务数据（一次性加载3页）
    
    // 默认每页20条，一次性加载3页共60条
    const defaultLimit = 20
    
    // 一次性加载3页数据
    const [page1, page2, page3] = await Promise.all([
      taskApi.getTasks({ page: 1, limit: defaultLimit }),
      taskApi.getTasks({ page: 2, limit: defaultLimit }).catch(() => ({ items: [], pagination: { has_next: false } })),
      taskApi.getTasks({ page: 3, limit: defaultLimit }).catch(() => ({ items: [], pagination: { has_next: false } }))
    ])
    
    // 合并所有页的数据
    const allItems: any[] = []
    
    // 添加第1页数据
    if (page1.items && Array.isArray(page1.items)) {
      allItems.push(...page1.items)
    }
    
    // 添加第2页数据（如果存在）
    if (page2.items && Array.isArray(page2.items) && page2.items.length > 0) {
      allItems.push(...page2.items)
    }
    
    // 添加第3页数据（如果存在）
    if (page3.items && Array.isArray(page3.items) && page3.items.length > 0) {
      allItems.push(...page3.items)
    }
    
    // 去重（基于id）
    const uniqueItems = Array.from(
      new Map(allItems.map(item => [item.id, item])).values()
    )
    
    // 静默加载完成，不显示日志
    
    return uniqueItems
  } catch (error) {
    console.error('❌ 加载任务数据失败:', error)
    // 如果批量加载失败，尝试只加载第1页
    try {
      const response = await taskApi.getTasks({ page: 1, limit: 20 })
      return response.items || []
    } catch (fallbackError) {
      console.error('❌ 备用加载方案也失败:', fallbackError)
      return []
    }
  }
}

// 从API加载财务数据的函数（API未实现时静默失败）
const loadTransactionsFromApi = async () => {
  try {
    const response = await financeApi.getTransactions()
    // 从统一格式 {data: [...]} 中提取数据
    return response.data || response || []
  } catch (error: any) {
    // API未实现时（404错误）静默处理，不显示错误
    if (error?.status === 404 || error?.isNotFound || error?.message?.includes('404')) {
      return [] // 后端未实现API时返回空数组
    }
    console.error('加载财务数据失败:', error)
    return []
  }
}

  // 从API加载财务统计数据的函数（API未实现时静默失败）
  const loadFinanceStatsFromApi = async () => {
    try {
      const response = await financeApi.getFinanceStats()
      // 从统一格式 {data: {...}} 中提取数据
      return response.data || response || null
    } catch (error: any) {
      // API未实现时（404错误）静默处理，不显示错误
      if (error?.status === 404 || error?.isNotFound || error?.message?.includes('404')) {
        return null // 后端未实现API时返回null
      }
      console.error('加载财务统计数据失败:', error)
      return null
    }
  }

export const useDashboardStore = defineStore('dashboard', () => {
  // 状态
  const selectedDate = ref(new Date())
  const courses = ref<Course[]>([])
  const tasks = ref<Task[]>([]) // 初始化为空数组，只显示数据库真实数据
  const transactions = ref<Transaction[]>([])
  const financeStats = ref<FinanceStatsApiData | null>(null)
  const isLoading = ref(false)
  const showTransactionModal = ref(false)
  const editingTransaction = ref<Transaction | null>(null)
  const isDarkMode = ref(false)
  
  // 自动刷新相关
  const autoRefreshEnabled = ref(false) // 自动刷新开关
  const autoRefreshInterval = ref(30000) // 自动刷新间隔（毫秒），默认30秒
  let autoRefreshTimer: NodeJS.Timeout | null = null

const modules = ref<ModuleConfig[]>([
  { id: "calendar", name: "日历", visible: true, column: "left" },
  { id: "task-stats", name: "任务统计", visible: true, column: "left" },
  { id: "finance-stats", name: "财务统计", visible: true, column: "left" },
  { id: "stats", name: "数据统计", visible: true, column: "left" },
  { id: "tasks", name: "任务列表", visible: true, column: "middle" },
  { id: "courses", name: "课程表", visible: true, column: "middle" },
  { id: "finance", name: "账本", visible: true, column: "right" },
  { id: "ai-chat", name: "AI助手", visible: true, column: "right" },
  { id: "reminders", name: "事件提醒", visible: true, column: "right" },
  { id: "chart", name: "完成量图表", visible: true, column: "right" },
])

  // 计算属性 - 使用本地时间格式化日期字符串，避免时区问题
  const selectedDateStr = computed(() => {
    const date = selectedDate.value
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  })

  const filteredCourses = computed(() => 
    courses.value.filter(course => course.date === selectedDateStr.value)
  )

  const filteredTasks = computed(() => 
    tasks.value.filter(task => task.date === selectedDateStr.value)
  )

  const filteredTransactions = computed(() => {
    const filtered = transactions.value.filter(transaction => transaction.date === selectedDateStr.value)
    console.log('Store - 当前选中日期:', selectedDateStr.value)
    console.log('Store - 过滤后的交易记录数量:', filtered.length)
    return filtered
  })

  // 方法
  const setSelectedDate = (date: Date) => {
    selectedDate.value = date
    // 数据现在通过API动态加载，不需要重新生成
  }

  const toggleTask = (id: number) => {
    const task = tasks.value.find(t => t.id === id)
    if (task) {
      task.completed = !task.completed
    }
  }

  const toggleModule = (id: string) => {
    const module = modules.value.find(m => m.id === id)
    if (module) {
      module.visible = !module.visible
    }
  }

  const addTask = async (task: Omit<Task, 'id'>) => {
    try {
      // 通过API层添加任务（会写入localStorage）
      const newTask = await taskApi.addTask(task)
      
      // 更新本地状态
      tasks.value.push({
        id: newTask.id,
        title: newTask.title,
        completed: newTask.completed,
        priority: newTask.priority,
        date: newTask.date,
        time: newTask.time,
        hasReminder: newTask.hasReminder
      } as Task)
      
      console.log('任务已添加到store:', newTask)
    } catch (error) {
      console.error('添加任务失败:', error)
      throw error
    }
  }

  const updateTask = async (id: number, updates: Partial<Task>) => {
    try {
      // 通过API层更新任务
      await taskApi.updateTask(id, updates)
      
      // 更新本地状态
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = { ...tasks.value[index], ...updates }
      }
      
      console.log('任务已更新:', id)
    } catch (error) {
      console.error('更新任务失败:', error)
      throw error
    }
  }

  const deleteTask = async (id: number) => {
    try {
      // 通过API层删除任务
      await taskApi.deleteTask(id)
      
      // 从本地状态中移除
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value.splice(index, 1)
      }
      
      console.log('任务已删除:', id)
    } catch (error) {
      console.error('删除任务失败:', error)
      throw error
    }
  }

  const batchDeleteTasks = async (taskIds: number[]) => {
    try {
      // 通过API层批量删除任务
      await taskApi.batchDeleteTasks(taskIds)
      
      // 从本地状态中移除
      tasks.value = tasks.value.filter(t => !taskIds.includes(t.id))
      
      console.log('批量删除任务成功:', taskIds)
    } catch (error) {
      console.error('批量删除任务失败:', error)
      throw error
    }
  }

  const addTransaction = async (transaction: Omit<Transaction, 'id'>) => {
    try {
      // 通过API层添加交易记录
      const newTransaction = await financeApi.addTransaction(transaction)
      // 添加到本地状态
      transactions.value.push(newTransaction)
      
      // 更新财务统计数据（如果API可用）
      try {
        const updatedStats = await financeApi.getFinanceStats()
        financeStats.value = updatedStats
      } catch (statsError: any) {
        // 统计API失败时不影响添加交易（静默处理404）
        if (statsError?.status !== 404 && !statsError?.isNotFound) {
          console.error('刷新财务统计失败:', statsError)
        }
      }
      
      return newTransaction
    } catch (error: any) {
      // API未实现时给出友好提示
      if (error?.status === 404 || error?.isNotFound || error?.message?.includes('404')) {
        throw new Error('财务模块API尚未实现，请参考财务模块后端API需求文档')
      }
      console.error('添加交易记录失败:', error)
      throw error
    }
  }

  const updateTransaction = async (id: number, updates: Partial<Transaction>) => {
    try {
      // 通过API层更新交易记录
      const updatedTransaction = await financeApi.updateTransaction(id, updates)
      // 更新本地状态
      const index = transactions.value.findIndex(t => t.id === id)
      if (index !== -1) {
        transactions.value[index] = updatedTransaction
      }
      
      // 更新财务统计数据（如果API可用）
      try {
        const updatedStats = await financeApi.getFinanceStats()
        financeStats.value = updatedStats
      } catch (statsError: any) {
        // 统计API失败时不影响更新交易（静默处理404）
        if (statsError?.status !== 404 && !statsError?.isNotFound) {
          console.error('刷新财务统计失败:', statsError)
        }
      }
      
      return updatedTransaction
    } catch (error: any) {
      // API未实现时给出友好提示
      if (error?.status === 404 || error?.isNotFound || error?.message?.includes('404')) {
        throw new Error('财务模块API尚未实现，请参考财务模块后端API需求文档')
      }
      console.error('更新交易记录失败:', error)
      throw error
    }
  }

  const deleteTransaction = async (id: number) => {
    try {
      // 通过API层删除交易记录（退款）
      await financeApi.deleteTransaction(id)
      // 从本地状态中移除
      transactions.value = transactions.value.filter(t => t.id !== id)
      
      // 更新财务统计数据（如果API可用）
      try {
        const updatedStats = await financeApi.getFinanceStats()
        financeStats.value = updatedStats
      } catch (statsError: any) {
        // 统计API失败时不影响删除交易（静默处理404）
        if (statsError?.status !== 404 && !statsError?.isNotFound) {
          console.error('刷新财务统计失败:', statsError)
        }
      }
    } catch (error: any) {
      // API未实现时给出友好提示
      if (error?.status === 404 || error?.isNotFound || error?.message?.includes('404')) {
        throw new Error('财务模块API尚未实现，请参考财务模块后端API需求文档')
      }
      console.error('删除交易记录失败:', error)
      throw error
    }
  }

  // 解析JSON格式的课程数据
  const parseCourseData = (jsonData: any) => {
    let courseArray: any[] = []
    
    // 处理统一格式 {data: [...]}
    if (jsonData && jsonData.data) {
      courseArray = jsonData.data
    } else if (Array.isArray(jsonData)) {
      // 兼容旧格式（直接数组）
      courseArray = jsonData
    } else {
      console.warn('课程数据格式无效，使用空数组')
      courseArray = []
    }

    const newCourses: Course[] = []
    const courseColors = ['bg-chart-1', 'bg-chart-2', 'bg-chart-3', 'bg-chart-4', 'bg-chart-5']
    let colorIndex = 0

    courseArray.forEach((item: any, index: number) => {
      // 跳过无效数据
      if (item.course_name === 'string' || !item.course_name || item.course_name.trim() === '') {
        return
      }

      // 解析节次信息
      const periods = item.periods || ''
      const timeSlots = parsePeriodsToTimeSlots(periods)
      
      // 获取星期几
      const date = new Date(item.date)
      const dayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
      const dayName = dayNames[date.getDay()]

      // 分配颜色
      const color = courseColors[colorIndex % courseColors.length]
      colorIndex++

      // 计算ID：如果现有课程为空，从1开始；否则取最大值+1
      const maxId = (courses.value && Array.isArray(courses.value) && courses.value.length > 0)
        ? Math.max(...courses.value.map(c => c.id))
        : 0

      const course: Course = {
        id: maxId + index + 1,
        name: item.course_name,
        time: timeSlots[0] || '08:00-08:40', // 使用第一个时间段作为显示时间
        timeSlots: timeSlots,
        location: item.classroom,
        color: color,
        date: item.date,
        day: dayName,
        teacher: item.teacher,
        periods: item.periods
      }

      newCourses.push(course)
    })

    // 返回新课程数组，不直接修改 courses.value（由调用者处理）
    return newCourses
  }

  // 将节次信息转换为时间段
  const parsePeriodsToTimeSlots = (periods: string): string[] => {
    if (!periods) return ['08:00-08:40']
    
    // 解析节次范围，如 "1-2节", "8-10节"
    const match = periods.match(/(\d+)-(\d+)节/)
    if (!match) return ['08:00-08:40']
    
    const startPeriod = parseInt(match[1])
    const endPeriod = parseInt(match[2])
    
    // 徐海学院作息时间表 - 严格按每个时间段
    const timeSlotMap: { [key: number]: string } = {
      1: '08:00-08:40',  // 第1节
      2: '08:45-09:25',  // 第2节
      3: '09:45-10:25',  // 第3节
      4: '10:30-11:10',  // 第4节
      5: '11:15-11:55',  // 第5节
      6: '14:00-14:40',  // 第6节
      7: '14:45-15:25',  // 第7节
      8: '15:45-16:25',  // 第8节
      9: '16:30-17:10',  // 第9节
      10: '17:15-17:55', // 第10节
      11: '19:00-19:40', // 第11节
      12: '19:45-20:25', // 第12节
      13: '20:35-21:15', // 第13节
      14: '21:20-22:00'  // 第14节
    }
    
    const timeSlots: string[] = []
    for (let i = startPeriod; i <= endPeriod; i++) {
      if (timeSlotMap[i]) {
        timeSlots.push(timeSlotMap[i])
      }
    }
    
    // 返回时间段（可能包含多个连续节次）
    return timeSlots.length > 0 ? timeSlots : ['08:00-08:40']
  }

  // 数据加载方法
  const loadAllData = async () => {
    if (isLoading.value) return // 防止重复加载
    
    isLoading.value = true
    try {
      // 静默加载所有数据
      
      // 并行加载所有数据
      const [coursesData, tasksData, transactionsData, financeStatsData] = await Promise.all([
        loadCoursesFromApi(),
        loadTasksFromApi(),
        loadTransactionsFromApi(),
        loadFinanceStatsFromApi()
      ])
      
      // 解析课程数据
      parseCourseData(coursesData)
      
      // 设置任务数据
      tasks.value = tasksData.map(task => ({
        ...task,
        // 确保日期格式正确
        date: task.date || new Date().toISOString().split('T')[0]
      }))
      
      // 设置财务数据
      transactions.value = transactionsData.map(transaction => ({
        ...transaction,
        // 确保日期格式正确
        date: transaction.date || new Date().toISOString().split('T')[0]
      }))
      
      // 财务数据已加载（静默处理）
      
      // 设置财务统计数据
      financeStats.value = financeStatsData
      
      // 所有数据静默加载完成
    } catch (error) {
      console.error('加载数据失败:', error)
    } finally {
      isLoading.value = false
    }
  }

  const loadCourses = async () => {
    try {
      const coursesData = await loadCoursesFromApi()
      parseCourseData(coursesData)
    } catch (error) {
      console.error('加载课程数据失败:', error)
    }
  }

  const loadTasks = async () => {
    try {
      const tasksData = await loadTasksFromApi()
      // 任务数据已加载
      
      // 确保返回数组
      if (!Array.isArray(tasksData)) {
        console.error('❌ 任务数据格式错误:', tasksData)
        tasks.value = []
        return
      }
      
      tasks.value = tasksData.map(task => ({
        ...task,
        date: task.date || new Date().toISOString().split('T')[0],
        // 处理字段名映射：后端返回 has_reminder，前端使用 hasReminder
        hasReminder: task.has_reminder
      }))
      // 任务列表已更新
    } catch (error) {
      console.error('❌ 加载任务数据失败:', error)
      tasks.value = [] // 失败时设为空数组
    }
  }

  const loadTransactions = async () => {
    try {
      const transactionsData = await loadTransactionsFromApi()
      transactions.value = transactionsData.map(transaction => ({
        ...transaction,
        date: transaction.date || new Date().toISOString().split('T')[0]
      }))
    } catch (error) {
      console.error('加载财务数据失败:', error)
    }
  }

  const loadFinanceStats = async () => {
    try {
      const financeStatsData = await loadFinanceStatsFromApi()
      financeStats.value = financeStatsData
    } catch (error) {
      console.error('加载财务统计数据失败:', error)
    }
  }

  // 切换夜间模式
  const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value
    // 保存到localStorage
    localStorage.setItem('darkMode', isDarkMode.value.toString())
    // 更新HTML class
    updateThemeClass()
  }

  // 更新主题类
  const updateThemeClass = () => {
    // 添加transition类来启用过渡
    document.documentElement.classList.add('transition-colors')
    
    if (isDarkMode.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // 初始化主题
  const initTheme = () => {
    const savedTheme = localStorage.getItem('darkMode')
    if (savedTheme !== null) {
      isDarkMode.value = savedTheme === 'true'
    } else {
      // 检查系统主题偏好
      isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    updateThemeClass()
  }

  // 自动刷新所有数据（任务、课程、财务统计和交易记录）
  const refreshAllData = async () => {
    try {
      // 静默刷新，不显示错误（避免轮询时产生过多错误提示）
      await Promise.all([
        loadCoursesFromApi().then(data => {
          // 确保总是设置一个数组，避免 undefined
          // data 可能是数组，也可能是 {data: [...]} 格式
          const courseArray = Array.isArray(data) ? data : (data?.data || [])
          if (courseArray && Array.isArray(courseArray) && courseArray.length > 0) {
            try {
              const parsed = parseCourseData(courseArray)
              if (Array.isArray(parsed)) {
                courses.value = parsed
              } else {
                courses.value = []
              }
            } catch (parseError) {
              // 解析失败时保持现有数据
              if (!courses.value || !Array.isArray(courses.value)) {
                courses.value = []
              }
            }
          } else {
            // 如果数据为空或无效，保持现有数据，但不设置为 undefined
            if (!courses.value || !Array.isArray(courses.value)) {
              courses.value = []
            }
          }
        }).catch(() => {
          // 错误时保持现有数据，但不设置为 undefined
          if (!courses.value || !Array.isArray(courses.value)) {
            courses.value = []
          }
        }),
        loadTasksFromApi().then(data => {
          // 确保总是设置一个数组，避免 undefined
          if (data && Array.isArray(data) && data.length > 0) {
            tasks.value = data.map((item: any) => ({
              id: item.id,
              title: item.title,
              completed: item.completed || false,
              priority: item.priority || 'medium',
              date: item.date,
              time: item.time,
              hasReminder: item.has_reminder || false,
              has_reminder: item.has_reminder || false,
              description: item.description,
              reminder_time: item.reminder_time
            }))
          } else {
            // 如果数据为空或无效，保持现有数据，但不设置为 undefined
            if (!tasks.value || !Array.isArray(tasks.value)) {
              tasks.value = []
            }
          }
        }).catch(() => {
          // 错误时保持现有数据，但不设置为 undefined
          if (!tasks.value || !Array.isArray(tasks.value)) {
            tasks.value = []
          }
        }),
        // 刷新交易记录
        loadTransactionsFromApi().then(data => {
          if (data && Array.isArray(data) && data.length > 0) {
            transactions.value = data.map((item: any) => ({
              id: item.id,
              type: item.type,
              amount: item.amount,
              category: item.category,
              description: item.description,
              date: item.date,
              time: item.time
            }))
          } else {
            // 如果数据为空或无效，保持现有数据，但不设置为 undefined
            if (!transactions.value || !Array.isArray(transactions.value)) {
              transactions.value = []
            }
          }
        }).catch(() => {
          // 错误时保持现有数据，但不设置为 undefined
          if (!transactions.value || !Array.isArray(transactions.value)) {
            transactions.value = []
          }
        }),
        // 刷新财务统计
        loadFinanceStatsFromApi().then(data => {
          if (data) {
            financeStats.value = data
          } else {
            // 如果数据为null，保持现有数据，但不设置为 undefined
            if (financeStats.value === undefined) {
              financeStats.value = null
            }
          }
        }).catch(() => {
          // 错误时保持现有数据，但不设置为 undefined
          if (financeStats.value === undefined) {
            financeStats.value = null
          }
        })
      ])
    } catch (error) {
      // 静默处理错误，不输出日志（避免轮询时产生过多日志）
      // 确保值始终是有效的数据类型
      if (!courses.value || !Array.isArray(courses.value)) {
        courses.value = []
      }
      if (!tasks.value || !Array.isArray(tasks.value)) {
        tasks.value = []
      }
      if (!transactions.value || !Array.isArray(transactions.value)) {
        transactions.value = []
      }
      if (financeStats.value === undefined) {
        financeStats.value = null
      }
    }
  }

  // 启动自动刷新
  const startAutoRefresh = (interval?: number) => {
    if (autoRefreshTimer) {
      clearInterval(autoRefreshTimer)
    }
    
    autoRefreshEnabled.value = true
    if (interval !== undefined) {
      autoRefreshInterval.value = interval
    }
    
    // 立即执行一次刷新
    refreshAllData()
    
    // 设置定时器
    autoRefreshTimer = setInterval(() => {
      if (autoRefreshEnabled.value) {
        refreshAllData()
      }
    }, autoRefreshInterval.value) as unknown as NodeJS.Timeout
  }

  // 停止自动刷新
  const stopAutoRefresh = () => {
    autoRefreshEnabled.value = false
    if (autoRefreshTimer) {
      clearInterval(autoRefreshTimer)
      autoRefreshTimer = null
    }
  }

  // 设置自动刷新间隔
  const setAutoRefreshInterval = (interval: number) => {
    autoRefreshInterval.value = interval
    // 如果正在运行，重新启动以应用新间隔
    if (autoRefreshEnabled.value) {
      startAutoRefresh(interval)
    }
  }

  return {
    // 状态
    selectedDate,
    courses,
    tasks,
    transactions,
    financeStats,
    modules,
    isLoading,
    showTransactionModal,
    editingTransaction,
    isDarkMode,
    // 自动刷新相关
    autoRefreshEnabled,
    autoRefreshInterval,
    // 计算属性
    selectedDateStr,
    filteredCourses,
    filteredTasks,
    filteredTransactions,
    // 方法
    setSelectedDate,
    toggleTask,
    toggleModule,
    addTask,
    updateTask,
    deleteTask,
    batchDeleteTasks,
    addTransaction,
    updateTransaction,
    deleteTransaction,
    parseCourseData,
    // 数据加载方法
    loadAllData,
    loadCourses,
    loadTasks,
    loadTransactions,
    loadFinanceStats,
    // 自动刷新方法
    refreshAllData,
    startAutoRefresh,
    stopAutoRefresh,
    setAutoRefreshInterval,
    // 主题相关方法
    toggleDarkMode,
    initTheme,
  }
})
