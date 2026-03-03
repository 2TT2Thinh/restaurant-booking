import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/home/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/booking/DashboardView.vue')
    },
    {
      path: '/bookings/edit/:id', // Dấu :id là bắt buộc để nhận id từ Dashboard
      name: 'BookingEdit',
      component: () => import('../views/booking/BookingEditView.vue')
    }
  ]
})

export default router