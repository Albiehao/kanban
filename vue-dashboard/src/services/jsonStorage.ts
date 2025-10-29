// JSON存储服务 - 使用localStorage模拟JSON文件的读写
// 在浏览器环境中，使用localStorage来模拟JSON文件的持久化存储

import type { TransactionApiData, FinanceStatsApiData, TaskApiData, UserApiData } from './types'

const STORAGE_KEY = 'finance_data'
const INITIAL_TRANSACTIONS_KEY = 'initial_transactions_loaded'
const TASKS_STORAGE_KEY = 'tasks_data'
const USER_DATA_STORAGE_KEY = 'user_data'

// 初始化数据接口
interface InitialData {
  transactions: TransactionApiData[]
  financeStats: FinanceStatsApiData | null
}

// 从localStorage读取所有交易记录
export const readTransactions = (): TransactionApiData[] => {
  try {
    const data = localStorage.getItem(STORAGE_KEY)
    if (data) {
      const parsed = JSON.parse(data)
      return parsed.transactions || []
    }
  } catch (error) {
    console.error('读取交易记录失败:', error)
  }
  return []
}

// 写入交易记录到localStorage
export const writeTransactions = (transactions: TransactionApiData[]): void => {
  try {
    // 读取当前存储的数据
    const data = localStorage.getItem(STORAGE_KEY)
    const currentData = data ? JSON.parse(data) : { transactions: [], financeStats: null }
    
    // 更新交易记录
    currentData.transactions = transactions
    
    // 保存到localStorage
    localStorage.setItem(STORAGE_KEY, JSON.stringify(currentData))
    console.log('已保存交易记录到本地存储:', transactions.length, '条记录')
  } catch (error) {
    console.error('保存交易记录失败:', error)
    throw error
  }
}

// 从JSON文件加载初始数据
export const loadInitialData = async (): Promise<InitialData> => {
  try {
    // 检查是否已经加载过初始数据
    const hasLoaded = localStorage.getItem(INITIAL_TRANSACTIONS_KEY)
    
    if (!hasLoaded) {
      console.log('首次加载，从JSON文件读取初始数据')
      
      // 从JSON文件加载初始数据
      const response = await fetch('/course-data-sample.json')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const jsonData = await response.json()
      
      // 保存初始数据到localStorage
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        transactions: jsonData.transactions || [],
        financeStats: jsonData.financeStats || null
      }))
      
      // 标记已加载
      localStorage.setItem(INITIAL_TRANSACTIONS_KEY, 'true')
      
      console.log('初始数据已加载:', jsonData.transactions?.length || 0, '条交易记录')
      
      return {
        transactions: jsonData.transactions || [],
        financeStats: jsonData.financeStats
      }
    } else {
      // 从localStorage读取数据
      const data = readTransactions()
      return {
        transactions: data,
        financeStats: null
      }
    }
  } catch (error) {
    console.error('加载初始数据失败:', error)
    // 返回空数据
    return {
      transactions: [],
      financeStats: null
    }
  }
}

// 添加新交易记录
export const addTransactionToStorage = (transaction: Omit<TransactionApiData, 'id'>): TransactionApiData => {
  try {
    // 读取当前所有交易记录
    const transactions = readTransactions()
    
    // 生成新ID
    const newId = transactions.length > 0 
      ? Math.max(...transactions.map(t => t.id)) + 1 
      : 1
    
    // 创建新交易记录
    const newTransaction: TransactionApiData = {
      ...transaction,
      id: newId
    }
    
    // 添加到列表
    const updatedTransactions = [...transactions, newTransaction]
    
    // 保存到localStorage
    writeTransactions(updatedTransactions)
    
    console.log('已添加交易记录:', newTransaction)
    return newTransaction
  } catch (error) {
    console.error('添加交易记录失败:', error)
    throw error
  }
}

// 更新交易记录
export const updateTransactionInStorage = (
  id: number, 
  updates: Partial<TransactionApiData>
): TransactionApiData => {
  try {
    const transactions = readTransactions()
    const index = transactions.findIndex(t => t.id === id)
    
    if (index === -1) {
      throw new Error(`交易记录 ${id} 不存在`)
    }
    
    // 更新交易记录
    const updatedTransaction = {
      ...transactions[index],
      ...updates,
      id // 确保ID不变
    }
    
    // 保存更新后的列表
    const updatedTransactions = [
      ...transactions.slice(0, index),
      updatedTransaction,
      ...transactions.slice(index + 1)
    ]
    
    writeTransactions(updatedTransactions)
    
    console.log('已更新交易记录:', updatedTransaction)
    return updatedTransaction
  } catch (error) {
    console.error('更新交易记录失败:', error)
    throw error
  }
}

// 删除交易记录
export const deleteTransactionFromStorage = (id: number): void => {
  try {
    const transactions = readTransactions()
    const filtered = transactions.filter(t => t.id !== id)
    
    if (filtered.length === transactions.length) {
      throw new Error(`交易记录 ${id} 不存在`)
    }
    
    writeTransactions(filtered)
    console.log('已删除交易记录:', id)
  } catch (error) {
    console.error('删除交易记录失败:', error)
    throw error
  }
}

// 获取交易记录（通过ID）
export const getTransactionById = (id: number): TransactionApiData | null => {
  const transactions = readTransactions()
  return transactions.find(t => t.id === id) || null
}

// 根据日期过滤交易记录
export const getTransactionsByDate = (date: string): TransactionApiData[] => {
  const transactions = readTransactions()
  return transactions.filter(t => t.date === date)
}

// 重置为初始数据（清空用户添加的数据）
export const resetToInitialData = async (): Promise<void> => {
  try {
    // 清除localStorage中的数据
    localStorage.removeItem(STORAGE_KEY)
    localStorage.removeItem(INITIAL_TRANSACTIONS_KEY)
    
    console.log('已重置为初始数据')
  } catch (error) {
    console.error('重置数据失败:', error)
    throw error
  }
}

// 任务存储相关函数
// 从localStorage读取所有任务
export const readTasks = (): TaskApiData[] => {
  try {
    const data = localStorage.getItem(TASKS_STORAGE_KEY)
    if (data) {
      const parsed = JSON.parse(data)
      return parsed.tasks || []
    }
  } catch (error) {
    console.error('读取任务失败:', error)
  }
  return []
}

// 写入任务到localStorage
export const writeTasks = (tasks: TaskApiData[]): void => {
  try {
    localStorage.setItem(TASKS_STORAGE_KEY, JSON.stringify({ tasks }))
    console.log('已保存任务到本地存储:', tasks.length, '条任务')
  } catch (error) {
    console.error('保存任务失败:', error)
    throw error
  }
}

// 添加任务到存储
export const addTaskToStorage = (task: Omit<TaskApiData, 'id'>): TaskApiData => {
  try {
    // 读取当前所有任务
    const tasks = readTasks()
    
    // 生成新ID
    const newId = tasks.length > 0 
      ? Math.max(...tasks.map(t => t.id)) + 1 
      : 1
    
    // 创建新任务
    const newTask: TaskApiData = {
      ...task,
      id: newId
    }
    
    // 添加到列表
    const updatedTasks = [...tasks, newTask]
    
    // 保存到localStorage
    writeTasks(updatedTasks)
    
    console.log('已添加任务:', newTask)
    return newTask
  } catch (error) {
    console.error('添加任务失败:', error)
    throw error
  }
}

// 从JSON文件加载初始任务数据
export const loadInitialTasks = async (): Promise<TaskApiData[]> => {
  try {
    console.log('从JSON文件读取初始任务数据')
    
    // 从JSON文件加载初始数据
    const response = await fetch('/course-data-sample.json')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const jsonData = await response.json()
    
    // 保存初始数据到localStorage（如果还没有）
    if (!localStorage.getItem(TASKS_STORAGE_KEY)) {
      localStorage.setItem(TASKS_STORAGE_KEY, JSON.stringify({
        tasks: jsonData.tasks || []
      }))
      
      console.log('初始任务数据已加载:', jsonData.tasks?.length || 0, '条任务')
      return jsonData.tasks || []
    }
    
    // 如果已有数据，则返回localStorage中的数据
    return readTasks()
  } catch (error) {
    console.error('加载初始任务数据失败:', error)
    return []
  }
}

// 用户数据存储相关函数
// 从localStorage读取用户数据
export const readUserData = (): UserApiData | null => {
  try {
    const data = localStorage.getItem(USER_DATA_STORAGE_KEY)
    if (data) {
      return JSON.parse(data)
    }
  } catch (error) {
    console.error('读取用户数据失败:', error)
  }
  return null
}

// 写入用户数据到localStorage
export const writeUserData = (userData: UserApiData): void => {
  try {
    localStorage.setItem(USER_DATA_STORAGE_KEY, JSON.stringify(userData))
    console.log('已保存用户数据到本地存储')
  } catch (error) {
    console.error('保存用户数据失败:', error)
    throw error
  }
}

// 从JSON文件加载初始用户数据
export const loadInitialUserData = async (): Promise<UserApiData | null> => {
  try {
    console.log('从JSON文件读取初始用户数据')
    
    // 从JSON文件加载初始数据
    const response = await fetch('/course-data-sample.json')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const jsonData = await response.json()
    
    // 保存初始数据到localStorage（如果还没有）
    if (!localStorage.getItem(USER_DATA_STORAGE_KEY) && jsonData.userData) {
      localStorage.setItem(USER_DATA_STORAGE_KEY, JSON.stringify(jsonData.userData))
      console.log('初始用户数据已加载')
      return jsonData.userData
    }
    
    // 如果已有数据，则返回localStorage中的数据
    return readUserData()
  } catch (error) {
    console.error('加载初始用户数据失败:', error)
    return null
  }
}

