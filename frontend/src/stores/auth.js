// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services/auth.service'
import apiClient from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {

  const token = ref(localStorage.getItem('user_token') || null)
  const user = ref(null)

  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const userRole = computed(() => user.value?.role || null)

  async function login(email, password) {
    console.log('1. Store login called')
    try {
      const data = await authService.login(email, password)
      console.log('2. Login response:', data)
      
      // Lưu token
      token.value = data.access_token
      localStorage.setItem('user_token', data.access_token)
      
      // ✅ QUAN TRỌNG: Set token cho axios ngay lập tức
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`
      console.log('3. Token set in axios headers')
      
      // Fetch user profile
      console.log('4. Fetching user...')
      await fetchUser()
      
      console.log('5. Final user:', user.value)
      console.log('6. isLoggedIn:', isLoggedIn.value)
      
      return data
    } catch (error) {
      console.error('Login error in store:', error)
      token.value = null
      localStorage.removeItem('user_token')
      delete apiClient.defaults.headers.common['Authorization']
      throw error
    }
  }

  async function register(userData) {
    const response = await authService.register(userData)
    if (response && userData.email && userData.password) {
      await login(userData.email, userData.password)
    }
    return response
  }

  async function fetchUser() {
    if (!token.value) {
      console.log('No token, skipping fetchUser')
      return null
    }
    
    try {
      console.log('Fetching user with token:', token.value)
      const res = await apiClient.get('/users/me')
      console.log('Fetch user response:', res.data)
      
      // ✅ FIX: Kiểm tra cấu trúc response
      if (res.data && res.data.data) {
        user.value = res.data.data
        console.log('User set from res.data.data')
      } else if (res.data) {
        user.value = res.data
        console.log('User set from res.data directly')
      } else {
        console.error('Invalid response structure:', res.data)
        throw new Error('Invalid user data response')
      }
      
      console.log('User after fetch:', user.value)
      
      if (user.value) {
        localStorage.setItem('user_email', user.value.email)
        localStorage.setItem('user_role', user.value.role)
      }
      
      return user.value
    } catch (error) {
      console.error('Failed to fetch user:', error)
      console.error('Error response:', error.response?.data)
      logout()
      throw error
    }
  }

  function logout() {
    console.log('Logging out')
    token.value = null
    user.value = null
    localStorage.removeItem('user_token')
    localStorage.removeItem('user_email')
    localStorage.removeItem('user_role')
    delete apiClient.defaults.headers.common['Authorization']
  }

  async function init() {
    console.log('Init called, token:', !!token.value, 'user:', !!user.value)
    if (token.value && !user.value) {
      try {
        await fetchUser()
      } catch (error) {
        console.error('Init fetch user failed:', error)
      }
    }
  }

  return { 
    token, 
    user, 
    isLoggedIn, 
    isAdmin, 
    userRole, 
    login, 
    register, 
    fetchUser, 
    logout, 
    init 
  }
})