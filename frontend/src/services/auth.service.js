import apiClient from '../api/axios';

export const authService = {

  // HÀM ĐĂNG NHẬP
  async login(email, password) {
    const response = await apiClient.post('/auth/login', {
      email: email,
      password: password
    });

    if (response.data.access_token) {
      localStorage.setItem('user_token', response.data.access_token);
      localStorage.setItem('user_email', email);

      // Lấy thêm role để router guard phân quyền admin/customer
      const meRes = await apiClient.get('/users/me');
      localStorage.setItem('user_role', meRes.data.role);
    }

    return response.data;
  },

  // HÀM ĐĂNG KÝ
  async register(userData) {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },

  // HÀM ĐĂNG XUẤT
  logout() {
    localStorage.removeItem('user_token');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_role');
  }

};