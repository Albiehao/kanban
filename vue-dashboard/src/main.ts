import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// 初始化主题（在应用挂载前）
const initTheme = () => {
  const savedTheme = localStorage.getItem('darkMode')
  if (savedTheme !== null) {
    if (savedTheme === 'true') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  } else {
    // 检查系统主题偏好
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    if (prefersDark) {
      document.documentElement.classList.add('dark')
    }
  }
}

// 在挂载前初始化主题
initTheme()

app.mount('#app')
