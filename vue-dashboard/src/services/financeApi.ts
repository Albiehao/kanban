// 财务统计 API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export interface TransactionApiData {
  id: number
  type: 'income' | 'expense'
  amount: number
  category: string
  description: string
  date: string
  time?: string // 具体时间，格式：HH:MM，如 "14:30"，可选
}

export interface FinanceStatsApiData {
  monthlyIncome: number
  monthlyExpense: number
  balance: number
  expenseByCategory: Array<{
    category: string
    amount: number
    color: string
  }>
}

// 获取JWT token
const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token')
}

const request = async <T>(endpoint: string, options: RequestInit = {}): Promise<T> => {
  const token = getAuthToken()
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
    },
    ...options
  }

  // 直接请求真实服务器
  const response = await fetch(`${API_BASE_URL}${endpoint}`, defaultOptions)
  
  // 404错误静默处理，不抛出（财务API尚未实现时）
  if (response.status === 404) {
    const error = new Error(`HTTP error! status: ${response.status}`)
    ;(error as any).status = 404
    ;(error as any).isNotFound = true
    throw error
  }
  
  if (!response.ok) {
    const error = new Error(`HTTP error! status: ${response.status}`)
    ;(error as any).status = response.status
    throw error
  }

  const data = await response.json()
  return data
}

export const financeApi = {
  // 获取所有交易记录
  getTransactions: async (): Promise<TransactionApiData[]> => {
    const response = await request<{ data: TransactionApiData[] }>('/transactions')
    return response.data || response
  },

  // 获取财务统计数据
  getFinanceStats: async (): Promise<FinanceStatsApiData> => {
    const response = await request<{ data: FinanceStatsApiData }>('/finance/stats')
    return response.data || response
  },

  // 添加交易记录
  addTransaction: async (transaction: Omit<TransactionApiData, 'id'>): Promise<TransactionApiData> => {
    const response = await request<{ data: TransactionApiData }>('/transactions', {
      method: 'POST',
      body: JSON.stringify(transaction)
    })
    return response.data || response
  },

  // 更新交易记录
  updateTransaction: async (id: number, updates: Partial<TransactionApiData>): Promise<TransactionApiData> => {
    const response = await request<{ data: TransactionApiData }>(`/transactions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates)
    })
    return response.data || response
  },

  // 删除交易记录
  deleteTransaction: async (id: number): Promise<void> => {
    await request(`/transactions/${id}`, {
      method: 'DELETE'
    })
  }
}

