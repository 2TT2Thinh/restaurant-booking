// src/services/auth.service.js
import apiClient from '../api/axios';

export const authService = {

  /**
   * Gọi API đăng nhập, trả về { access_token, token_type }
   * KHÔNG lưu localStorage ở đây — Store sẽ lo việc đó
   */
  async login(email, password) {
    const response = await apiClient.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  /**
   * Gọi API đăng ký, trả về thông tin user vừa tạo
   */
  async register(userData) {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },

};