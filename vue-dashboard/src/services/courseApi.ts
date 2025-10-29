// 课程API服务 - 已迁移到统一的API层
// 这个文件现在作为向后兼容的包装器

import { courseApi, mockApi } from './api'
import { useDashboardStore } from '@/stores/dashboard'

// 向后兼容的接口
export interface CourseApiResponse {
  course_name: string
  classroom: string
  date: string
  teacher: string
  periods: string
}

// 使用新的API层获取课程数据
export const fetchCourseData = async (): Promise<CourseApiResponse[]> => {
  try {
    // 优先使用真实API，如果失败则使用模拟数据
    try {
      const response = await courseApi.getCourses()
      return response.data
    } catch (error) {
      console.warn('真实API不可用，使用模拟数据:', error)
      const response = await mockApi.getCourses()
      return response.data
    }
  } catch (error) {
    console.error('获取课程数据失败:', error)
    throw error
  }
}

// 在组件中使用API的示例
export const useCourseApi = () => {
  const store = useDashboardStore()

  const loadCoursesFromApi = async () => {
    try {
      // 显示加载状态
      console.log('正在加载课程数据...')
      
      // 调用API获取数据
      const courseData = await fetchCourseData()
      
      // 解析并存储到store
      store.parseCourseData(courseData)
      
      console.log('课程数据加载成功')
    } catch (error) {
      console.error('加载课程数据失败:', error)
      // 错误处理由调用方负责（不再使用alert）
      throw error
    }
  }

  return {
    loadCoursesFromApi
  }
}

// 使用示例：
// 在Vue组件中：
// import { useCourseApi } from '@/services/courseApi'
// 
// const { loadCoursesFromApi } = useCourseApi()
// 
// // 在组件挂载时或用户点击按钮时调用
// onMounted(() => {
//   loadCoursesFromApi()
// })
//
// 或者添加一个按钮：
// <Button @click="loadCoursesFromApi">刷新课程表</Button>
