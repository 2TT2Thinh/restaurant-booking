import axios from 'axios'

const apiClient = axios.create({
  // import.meta.env.VITE_API_BASE_URL sẽ lấy giá trị từ file .env
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  }
})

export default apiClient