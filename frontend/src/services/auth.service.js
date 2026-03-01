import apiClient from '../api/axios';

export const authService = {
  // HÀM ĐĂNG NHẬP
  async login(email, password) {
    // Gọi đến endpoint /auth/login mà bạn đã sửa lỗi ở Backend
    const response = await apiClient.post('/auth/login', {
      email: email,
      password: password
    });
    
    // Nếu đăng nhập thành công, lưu Token vào LocalStorage
    if (response.data.access_token) {
      localStorage.setItem('user_token', response.data.access_token);
      // LƯU THÊM DÒNG NÀY ĐỂ TRANG DASHBOARD LẤY ĐƯỢC
      localStorage.setItem('user_email', email);
    }
    return response.data;
  },


    // HÀM ĐĂNG KÝ
  async register(userData) {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  }
  
};




