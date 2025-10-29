// 课程表 API - 使用第三方API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

export interface CourseApiData {
  id: number
  course_name: string
  classroom: string
  date: string
  teacher: string
  periods: string
}

export interface CourseApiResponse {
  success: boolean
  data: CourseApiData[]
  total?: number
  message?: string
}

// 获取JWT token
const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token')
}

export const courseScheduleApi = {
  // 获取所有课程（通过我们的后端）
  async getCourses(startDate?: string, endDate?: string): Promise<CourseApiData[]> {
    console.log('📚 Fetching courses from backend API...')
    
    try {
      const token = getAuthToken()
      
      // 构建查询参数
      const params = new URLSearchParams()
      if (startDate) params.append('start_date', startDate)
      if (endDate) params.append('end_date', endDate)
      
      const url = params.toString() ? `/courses?${params.toString()}` : '/courses'
      
      // 调用我们自己的后端API
      const response = await fetch(`${API_BASE_URL}${url}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        }
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const result = await response.json()
      console.log('📊 后端返回的原始数据:', result)
      
      const coursesData = result.data || result
      console.log('📚 解析后的课程数据:', coursesData)
      console.log('📈 课程数量:', coursesData?.length || 0)
      
      return coursesData || []
    } catch (error) {
      console.error('❌ Failed to load courses:', error)
      throw error
    }
  },

  // 获取指定日期的课程
  async getCoursesByDate(date: string): Promise<CourseApiData[]> {
    return courseScheduleApi.getCourses(date, date)
  }
}
