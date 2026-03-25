// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/home/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ==================== PUBLIC ====================
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

    // ==================== CUSTOMER (cần login) ====================
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/booking/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bookings/new',
      name: 'BookingCreate',
      component: () => import('../views/booking/BookingCreateView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bookings/edit/:id',
      name: 'BookingEdit',
      component: () => import('../views/booking/BookingEditView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'UserProfile',
      component: () => import('../views/user/UserProfileView.vue'),
      meta: { requiresAuth: true }
    },

    // ==================== ADMIN (cần role admin) ====================
    {
      path: '/admin',
      component: () => import('../views/admin/AdminLayout.vue'),
      meta: { requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'AdminDashboard',
          component: () => import('../views/admin/AdminDashboard.vue')
        },
        {
          path: 'restaurants',
          name: 'AdminRestaurants',
          component: () => import('../views/admin/AdminRestaurants.vue')
        },
        {
          path: 'bookings',
          name: 'AdminBookings',
          component: () => import('../views/admin/AdminBookings.vue')
        },
        {
          path: 'users',
          name: 'AdminUsers',
          component: () => import('../views/admin/AdminUsers.vue')
        },
      ]
    },

    // ==================== 404 ====================
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      redirect: '/'
    }
  ]
})

// ==================== NAVIGATION GUARD ====================
// Dùng import động để tránh circular dependency (store dùng router, router dùng store)
router.beforeEach(async (to, from, next) => {
  const { useAuthStore } = await import('@/stores/auth')
  const authStore = useAuthStore()

  // Trang cần login
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return next('/login')
  }

  // Trang cần admin
  if (to.meta.requiresAdmin) {
    if (!authStore.isLoggedIn) return next('/login')
    if (!authStore.isAdmin)    return next('/dashboard')
  }

  next()
})

export default router