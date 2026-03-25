// src/api/axios.js
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  }
})

// ── Request interceptor ───────────────────────────────────────────
// Tự động đính kèm token vào mỗi request
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('user_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// ── Response interceptor ──────────────────────────────────────────
// Khi token hết hạn (401) → tự động logout + redirect về login
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error.response?.status

    if (status === 401) {
      // Import động để tránh circular dependency
      const { useAuthStore } = await import('@/stores/auth')
      const authStore = useAuthStore()

      // Chỉ logout nếu user đang đăng nhập (tránh loop ở trang login)
      if (authStore.isLoggedIn) {
        authStore.logout()
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient