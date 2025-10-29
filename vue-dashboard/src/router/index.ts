import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Profile from '@/views/Profile.vue'
import Admin from '@/views/Admin.vue'
import Login from '@/views/Login.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
      meta: { requiresAuth: true, requiresAdmin: true }
    }
  ]
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 初始化认证状态（检查token）
  if (!authStore.isAuthenticated) {
    await authStore.initAuth()
  }

  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    console.log('未登录，重定向到登录页')
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // 检查是否需要管理员权限
  if (to.meta.requiresAdmin && !authStore.canAccessAdmin) {
    console.log('需要管理员权限，当前角色:', authStore.currentUser?.role)
    console.log('canAccessAdmin值:', authStore.canAccessAdmin)
    console.log('用户信息:', authStore.currentUser)
    next('/')
    return
  }

  // 如果已登录且访问登录页面，重定向到首页或返回原页面
  if (to.name === 'login' && authStore.isAuthenticated) {
    // 如果有redirect参数，返回原页面
    const redirect = to.query.redirect as string
    if (redirect) {
      next(redirect)
      return
    }
    
    // 根据角色跳转
    if (authStore.isAdmin) {
      next('/admin')
    } else {
      next('/')
    }
    return
  }

  next()
})

export default router
