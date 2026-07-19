import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

// Global error handler – catches any uncaught error in component render, watchers, lifecycle hooks, etc.
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err)
  console.error('Component:', instance)
  console.error('Info:', info)
  // In a real app you could send this to a logging service (Sentry, LogRocket, etc.)
}

app.use(createPinia())
app.use(router)
app.mount('#app')
