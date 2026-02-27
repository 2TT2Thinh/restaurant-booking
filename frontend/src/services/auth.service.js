import apiClient from '../api/axios';

export const authService = {
  async login(email, password) {
    // Gọi đến endpoint /auth/login mà bạn đã sửa lỗi ở Backend
    const response = await apiClient.post('/auth/login', {
      email: email,
      password: password
    });
    
    // Nếu đăng nhập thành công, lưu Token vào LocalStorage
    if (response.data.access_token) {
      localStorage.setItem('user_token', response.data.access_token);
    }
    return response.data;
  }
};