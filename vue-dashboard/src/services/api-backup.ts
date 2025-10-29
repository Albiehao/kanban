// API服务层 - 统一管理所有数据获取
// 这个文件将替代组件中的硬编码数据，提供统一的数据接口

// API基础配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api'

// 通用API响应接口
export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
  total?: number
}

// 课程数据接口
export interface CourseApiData {
  course_name: string
  classroom: string
  date: string
  teacher: string
  periods: string
}

export interface CourseApiResponse {
  header: {
    status: string
    message: string
    total_count: number
  }
  data: CourseApiData[]
}

// 任务数据接口
export interface TaskApiData {
  id: number
  title: string
  completed: boolean
  priority: 'high' | 'medium' | 'low'
  date: string
}

// 财务数据接口
export interface TransactionApiData {
  id: number
  type: 'income' | 'expense'
  amount: number
  category: string
  description: string
  date: string
}

// 用户数据接口
export interface UserApiData {
  id: number
  username: string
  email: string
  role: string
}

// HTTP请求工具函数
const request = async <T>(url: string, options: RequestInit = {}): Promise<T> => {
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      // 如果需要认证，可以在这里添加token
      // 'Authorization': `Bearer ${getToken()}`
    },
    ...options
  }

  try {
    const response = await fetch(`${API_BASE_URL}${url}`, defaultOptions)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error(`API请求失败 [${url}]:`, error)
    throw error
  }
}

// 课程相关API
export const courseApi = {
  // 获取课程数据 - 直接返回JSON数据
  getCourses: async (): Promise<CourseApiResponse> => {
    // 直接返回JSON数据，不进行网络请求
    return {
      header: {
        status: "success",
        message: "获取课程表成功",
        total_count: 134
      },
      data: [
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-01",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-01",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-09-02",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-02",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-09-03",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "德润讲堂",
          "date": "2025-09-03",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-03",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-04",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-04",
          "teacher": "刘丹",
          "periods": "3-5节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-04",
          "teacher": "聂小燕",
          "periods": "6-7节"
        },
        {
          "course_name": "\"四史\"教育",
          "classroom": "德润讲堂",
          "date": "2025-09-05",
          "teacher": "王镖",
          "periods": "1-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-05",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-06",
          "teacher": "刘丹",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-08",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-08",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-08",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-09",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-10",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "德润讲堂",
          "date": "2025-09-10",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-10",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-10",
          "teacher": "刘丹",
          "periods": "8-9节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-11",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-11",
          "teacher": "聂小燕",
          "periods": "6-7节"
        },
        {
          "course_name": "\"四史\"教育",
          "classroom": "德润讲堂",
          "date": "2025-09-12",
          "teacher": "王镖",
          "periods": "1-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-12",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-15",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-15",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-15",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-16",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-17",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-09-17",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-17",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-18",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-18",
          "teacher": "聂小燕",
          "periods": "6-7节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-09-19",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-19",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-22",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B400",
          "date": "2025-09-22",
          "teacher": "聂小燕",
          "periods": "3-4节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-22",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-09-23",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-23",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-24",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-09-24",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-24",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-24",
          "teacher": "刘丹",
          "periods": "8-9节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-25",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-25",
          "teacher": "聂小燕",
          "periods": "6-7节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-09-26",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-26",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-29",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-29",
          "teacher": "孙宁",
          "periods": "3-4节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-29",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-09-30",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-30",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-09",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-10",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-10-10",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-13",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-10-13",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-10-14",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-10-15",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-10-15",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-15",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-10-15",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-16",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-10-16",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-17",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-20",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-10-21",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-10-22",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-10-22",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-22",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-10-22",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-23",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-10-23",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-24",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-27",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-10-28",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-10-29",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-10-29",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-29",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-30",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-10-30",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-31",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-10-31",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-11-03",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-03",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-11-05",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-11-05",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-11-06",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-06",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-06",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-11-07",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-11-10",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-10",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-11-12",
          "teacher": "孙宁",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-11-12",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-11-13",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-13",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-13",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-11-14",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-17",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-18",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-11-19",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-20",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-20",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-24",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-24",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-25",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-11-26",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-27",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-27",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-01",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-01",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-02",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-12-03",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-04",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-04",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-08",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-08",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-09",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-12-10",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-11",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-11",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-15",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-15",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-16",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-12-17",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-18",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-18",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-22",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-22",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-25",
          "teacher": "孙锦程",
          "periods": "3-5节"
        }
      ]
    }
  },

  // 获取指定日期的课程
  getCoursesByDate: async (date: string): Promise<CourseApiData[]> => {
    const response = await request<CourseApiResponse>(`/courses?date=${date}`)
    return response.data
  },

  // 添加课程
  addCourse: async (course: Omit<CourseApiData, 'id'>): Promise<CourseApiData> => {
    return request<CourseApiData>('/courses', {
      method: 'POST',
      body: JSON.stringify(course)
    })
  },

  // 更新课程
  updateCourse: async (id: number, course: Partial<CourseApiData>): Promise<CourseApiData> => {
    return request<CourseApiData>(`/courses/${id}`, {
      method: 'PUT',
      body: JSON.stringify(course)
    })
  },

  // 删除课程
  deleteCourse: async (id: number): Promise<void> => {
    return request<void>(`/courses/${id}`, {
      method: 'DELETE'
    })
  }
}

// 任务相关API
export const taskApi = {
  // 获取任务数据
  getTasks: async (): Promise<TaskApiData[]> => {
    return request<TaskApiData[]>('/tasks')
  },

  // 获取指定日期的任务
  getTasksByDate: async (date: string): Promise<TaskApiData[]> => {
    return request<TaskApiData[]>(`/tasks?date=${date}`)
  },

  // 添加任务
  addTask: async (task: Omit<TaskApiData, 'id'>): Promise<TaskApiData> => {
    return request<TaskApiData>('/tasks', {
      method: 'POST',
      body: JSON.stringify(task)
    })
  },

  // 更新任务
  updateTask: async (id: number, task: Partial<TaskApiData>): Promise<TaskApiData> => {
    return request<TaskApiData>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(task)
    })
  },

  // 删除任务
  deleteTask: async (id: number): Promise<void> => {
    return request<void>(`/tasks/${id}`, {
      method: 'DELETE'
    })
  },

  // 切换任务完成状态
  toggleTask: async (id: number): Promise<TaskApiData> => {
    return request<TaskApiData>(`/tasks/${id}/toggle`, {
      method: 'PATCH'
    })
  }
}

// 财务统计接口
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

// 财务相关API
export const financeApi = {
  // 获取财务数据
  getTransactions: async (): Promise<TransactionApiData[]> => {
    return request<TransactionApiData[]>('/transactions')
  },

  // 获取财务统计数据
  getFinanceStats: async (): Promise<FinanceStatsApiData> => {
    return request<FinanceStatsApiData>('/finance/stats')
  },

  // 获取指定日期的财务数据
  getTransactionsByDate: async (date: string): Promise<TransactionApiData[]> => {
    return request<TransactionApiData[]>(`/transactions?date=${date}`)
  },

  // 添加财务记录
  addTransaction: async (transaction: Omit<TransactionApiData, 'id'>): Promise<TransactionApiData> => {
    return request<TransactionApiData>('/transactions', {
      method: 'POST',
      body: JSON.stringify(transaction)
    })
  },

  // 更新财务记录
  updateTransaction: async (id: number, transaction: Partial<TransactionApiData>): Promise<TransactionApiData> => {
    return request<TransactionApiData>(`/transactions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(transaction)
    })
  },

  // 删除财务记录
  deleteTransaction: async (id: number): Promise<void> => {
    return request<void>(`/transactions/${id}`, {
      method: 'DELETE'
    })
  }
}

// 用户相关API
export const userApi = {
  // 获取用户信息
  getUser: async (): Promise<UserApiData> => {
    return request<UserApiData>('/user/profile')
  },

  // 更新用户信息
  updateUser: async (user: Partial<UserApiData>): Promise<UserApiData> => {
    return request<UserApiData>('/user/profile', {
      method: 'PUT',
      body: JSON.stringify(user)
    })
  }
}

// 模拟数据API（用于开发阶段）
export const mockApi = {
  // 加载模拟数据
  loadMockData: async () => {
    try {
      const response = await fetch('/data/mock-data.json')
      if (!response.ok) {
        throw new Error('Failed to load mock data')
      }
      return await response.json()
    } catch (error) {
      console.error('加载模拟数据失败:', error)
      throw error
    }
  },

  // 模拟获取课程数据
  getCourses: async (): Promise<CourseApiResponse> => {
    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 100))
    
    try {
      const mockData = await mockApi.loadMockData()
      return mockData.courses
    } catch (error) {
      console.warn('使用内置模拟数据:', error)
      // 降级到内置数据
      return {
        header: {
          status: "success",
          message: "获取课程表成功",
          total_count: 3
        },
        data: [
          {
            "course_name": "软件工程",
            "classroom": "好学楼B209",
            "date": "2025-09-01",
            "teacher": "孙锦程",
            "periods": "1-2节"
          },
          {
            "course_name": "操作系统",
            "classroom": "好学楼B210",
            "date": "2025-09-01",
            "teacher": "刘丹",
            "periods": "8-10节"
          },
          {
            "course_name": "移动应用开发技术",
            "classroom": "力行楼B409",
            "date": "2025-09-02",
            "teacher": "聂小燕",
            "periods": "3-5节"
          }
        ]
      }
    }
  },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-09-02",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-02",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-09-03",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "德润讲堂",
          "date": "2025-09-03",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-03",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-04",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-04",
          "teacher": "刘丹",
          "periods": "3-5节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-04",
          "teacher": "聂小燕",
          "periods": "6-7节"
        },
        {
          "course_name": "\"四史\"教育",
          "classroom": "德润讲堂",
          "date": "2025-09-05",
          "teacher": "王镖",
          "periods": "1-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-05",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-06",
          "teacher": "刘丹",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-08",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-08",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-08",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-09",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-10",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "德润讲堂",
          "date": "2025-09-10",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-10",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-10",
          "teacher": "刘丹",
          "periods": "8-9节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-11",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-11",
          "teacher": "聂小燕",
          "periods": "6-7节"
        },
        {
          "course_name": "\"四史\"教育",
          "classroom": "德润讲堂",
          "date": "2025-09-12",
          "teacher": "王镖",
          "periods": "1-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-12",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-15",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-15",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-15",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-16",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-17",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-09-17",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-17",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-18",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-18",
          "teacher": "聂小燕",
          "periods": "6-7节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-09-19",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-19",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-22",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B400",
          "date": "2025-09-22",
          "teacher": "聂小燕",
          "periods": "3-4节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-22",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-09-23",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-23",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-24",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-09-24",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-24",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-24",
          "teacher": "刘丹",
          "periods": "8-9节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-25",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-09-25",
          "teacher": "聂小燕",
          "periods": "6-7节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-09-26",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-26",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-09-29",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-09-29",
          "teacher": "孙宁",
          "periods": "3-4节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-29",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-09-30",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-09-30",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-09",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-10",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-10-10",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-13",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-10-13",
          "teacher": "刘丹",
          "periods": "6-7节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-10-14",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-10-15",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-10-15",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-15",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-10-15",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-16",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-10-16",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-17",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-20",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-10-21",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-10-22",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-10-22",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-22",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-10-22",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-23",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-10-23",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-24",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-27",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼B409",
          "date": "2025-10-28",
          "teacher": "聂小燕",
          "periods": "3-5节"
        },
        {
          "course_name": "移动应用开发技术",
          "classroom": "力行楼A400",
          "date": "2025-10-29",
          "teacher": "聂小燕",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-10-29",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-29",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-10-30",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-10-30",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-10-31",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "操作系统",
          "classroom": "好学楼B210",
          "date": "2025-10-31",
          "teacher": "刘丹",
          "periods": "8-10节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-11-03",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-03",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-11-05",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-11-05",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-11-06",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-06",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-06",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-11-07",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-11-10",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-10",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-11-12",
          "teacher": "孙宁",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-11-12",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程",
          "classroom": "好学楼B209",
          "date": "2025-11-13",
          "teacher": "孙锦程",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-13",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-13",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "JavaEE基础",
          "classroom": "力行楼A400",
          "date": "2025-11-14",
          "teacher": "孙宁",
          "periods": "6-7节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-17",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-18",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-11-19",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-20",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-20",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-24",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-24",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-25",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-11-26",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-11-27",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-11-27",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-01",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-01",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-02",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-12-03",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-04",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-04",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-08",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-08",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-09",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-12-10",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-11",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-11",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-15",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-15",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-16",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "马克思主义基本原理",
          "classroom": "好学楼B100",
          "date": "2025-12-17",
          "teacher": "陈惠珍",
          "periods": "3-4节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-18",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-18",
          "teacher": "韩旭东",
          "periods": "6-7节"
        },
        {
          "course_name": "Linux原理与应用",
          "classroom": "力行楼B400",
          "date": "2025-12-22",
          "teacher": "韩旭东",
          "periods": "1-2节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-22",
          "teacher": "孙锦程",
          "periods": "3-5节"
        },
        {
          "course_name": "软件工程课程设计",
          "classroom": "力行楼A409",
          "date": "2025-12-25",
          "teacher": "孙锦程",
          "periods": "3-5节"
        }
      ]
    }
  },

  // 模拟获取任务数据
  getTasks: async (): Promise<TaskApiData[]> => {
    await new Promise(resolve => setTimeout(resolve, 100))
    
    try {
      const mockData = await mockApi.loadMockData()
      return mockData.tasks
    } catch (error) {
      console.warn('使用内置任务数据:', error)
      // 降级到内置数据
      return [
        { id: 1, title: "完成数学作业", completed: false, priority: "high", date: "2025-01-20" },
        { id: 2, title: "准备英语演讲", completed: false, priority: "high", date: "2025-01-20" },
        { id: 3, title: "复习计算机网络", completed: true, priority: "medium", date: "2025-01-20" }
      ]
    }
  },

  // 模拟获取财务数据
  getTransactions: async (): Promise<TransactionApiData[]> => {
    await new Promise(resolve => setTimeout(resolve, 100))
    
    try {
      const mockData = await mockApi.loadMockData()
      return mockData.transactions
    } catch (error) {
      console.warn('使用内置财务数据:', error)
      // 降级到内置数据
      return [
        {
          id: 1,
          type: "expense",
          amount: 45.5,
          category: "餐饮",
          description: "午餐",
          date: "2025-01-20"
        },
        {
          id: 2,
          type: "income",
          amount: 500,
          category: "兼职",
          description: "周末兼职工资",
          date: "2025-01-19"
        }
      ]
    }
  },

  // 模拟获取财务统计数据
  getFinanceStats: async (): Promise<FinanceStatsApiData> => {
    await new Promise(resolve => setTimeout(resolve, 100))
    
    try {
      const mockData = await mockApi.loadMockData()
      return mockData.financeStats
    } catch (error) {
      console.warn('使用内置财务统计数据:', error)
      // 降级到内置数据
      return {
        monthlyIncome: 2500,
        monthlyExpense: 1800,
        balance: 700,
        expenseByCategory: [
          { category: '餐饮', amount: 450, color: '#ef4444' },
          { category: '学习', amount: 320, color: '#3b82f6' },
          { category: '交通', amount: 180, color: '#10b981' },
          { category: '娱乐', amount: 200, color: '#f59e0b' }
        ]
      }
    }
  },

  // 模拟获取用户数据
  getUser: async (): Promise<UserApiData> => {
    await new Promise(resolve => setTimeout(resolve, 100))
    
    try {
      const mockData = await mockApi.loadMockData()
      return mockData.user
    } catch (error) {
      console.warn('使用内置用户数据:', error)
      // 降级到内置数据
      return {
        id: 1,
        username: "student001",
        email: "student@university.edu.cn",
        role: "student"
      }
    }
  }
}

// 导出默认API配置
export default {
  courseApi,
  taskApi,
  financeApi,
  userApi,
  mockApi
}
