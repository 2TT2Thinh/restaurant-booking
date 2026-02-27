import axios from 'axios';

const apiClient = axios.create({
  // Địa chỉ Backend FastAPI của bạn
  baseURL: 'http://127.0.0.1:8000/api/v1', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;