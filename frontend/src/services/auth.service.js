// src/services/auth.service.js
import apiClient from '../api/axios'

export const authService = {
  /**
   * Login — must use application/x-www-form-urlencoded to match
   * FastAPI OAuth2PasswordRequestForm.
   * The field name is 'username' (OAuth2 standard), but we pass email as its value.
   */
  async login(email, password) {
    const params = new URLSearchParams()
    params.append('username', email)   // OAuth2 spec calls this field 'username'
    params.append('password', password)

    const response = await apiClient.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    return response.data  // { access_token, token_type }
  },

  /**
   * Register — stays as JSON, no change needed here.
   */
  async register(userData) {
    const response = await apiClient.post('/auth/register', userData)
    return response.data
  },
}