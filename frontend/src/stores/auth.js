// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services/auth.service'
import apiClient from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {

  // ── State ────────────────────────────────────────────────────────
  const token = ref(localStorage.getItem('user_token') || null)
  const user  = ref(null)   // { id, email, full_name, phone, role }

  // ── Getters ──────────────────────────────────────────────────────
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin    = computed(() => user.value?.role === 'admin')
  const userRole   = computed(() => user.value?.role || null)

  // ── Actions ──────────────────────────────────────────────────────

  /**
   * Đăng nhập: lưu token + fetch thông tin user
   */
  async function login(email, password) {
    const data = await authService.login(email, password)

    // Lưu token vào state + localStorage
    token.value = data.access_token
    localStorage.setItem('user_token', data.access_token)

    // Fetch full user info (bao gồm role, full_name, phone...)
    await fetchUser()

    return data
  }

  /**
   * Đăng ký: chỉ gọi API, không tự login
   */
  async function register(userData) {
    return await authService.register(userData)
  }

  /**
   * Lấy thông tin user hiện tại từ API
   * Gọi khi: sau login, hoặc khi app khởi động lại (còn token)
   */
  async function fetchUser() {
    try {
      const res = await apiClient.get('/users/me')
      user.value = res.data

      // Đồng bộ localStorage để router guard vẫn dùng được
      localStorage.setItem('user_email', res.data.email)
      localStorage.setItem('user_role',  res.data.role)
    } catch {
      // Token hết hạn hoặc không hợp lệ → logout
      logout()
    }
  }

  /**
   * Đăng xuất: xóa toàn bộ state + localStorage
   */
  function logout() {
    token.value = null
    user.value  = null
    localStorage.removeItem('user_token')
    localStorage.removeItem('user_email')
    localStorage.removeItem('user_role')
  }

  /**
   * Khởi tạo: gọi trong App.vue một lần khi app load
   * Nếu còn token → tự động fetch lại user info
   */
  async function init() {
    if (token.value && !user.value) {
      await fetchUser()
    }
  }

  return {
    // state
    token,
    user,
    // getters
    isLoggedIn,
    isAdmin,
    userRole,
    // actions
    login,
    register,
    fetchUser,
    logout,
    init,
  }
})