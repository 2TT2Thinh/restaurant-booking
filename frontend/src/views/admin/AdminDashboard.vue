<template>
  <div class="admin-bg min-h-screen pa-10">

    <!-- HEADER -->
    <div class="d-flex flex-column flex-md-row justify-space-between align-md-end mb-10 gap-4">
      <div>
        <div class="text-caption font-weight-black text-indigo mb-1" style="letter-spacing: 0.15em; text-transform: uppercase;">
          System Overview
        </div>
        <h1 class="text-h3 font-weight-black text-dark tracking-tight">Architect Admin</h1>
        <p class="text-body-2 text-grey-darken-1 mt-1">Manage your restaurant booking platform.</p>
      </div>
      <div class="d-flex gap-3">
        <v-btn
          variant="outlined"
          rounded="lg"
          class="text-none font-weight-bold"
          color="grey-darken-2"
          prepend-icon="mdi-download-outline"
        >Download Report</v-btn>
        <v-btn
          color="indigo-darken-3"
          variant="flat"
          rounded="lg"
          class="text-none font-weight-bold shadow-indigo"
          prepend-icon="mdi-plus"
          @click="$router.push('/admin/restaurants')"
        >Add Restaurant</v-btn>
      </div>
    </div>

    <!-- STATS BENTO GRID -->
    <v-row class="mb-10">
      <!-- Total Users -->
      <v-col cols="12" sm="6" lg="3">
        <v-card variant="flat" rounded="xl" class="stat-card pa-8 overflow-hidden" style="background:#fff;">
          <div class="d-flex justify-space-between align-start mb-6">
            <v-sheet color="indigo-lighten-5" rounded="lg" width="40" height="40"
              class="d-flex align-center justify-center">
              <v-icon color="indigo-darken-3" size="20">mdi-account-group-outline</v-icon>
            </v-sheet>
            <v-chip size="x-small" color="indigo" variant="tonal" class="font-weight-bold">
              Total
            </v-chip>
          </div>
          <div class="text-h3 font-weight-black text-dark mb-1">{{ stats.total_users }}</div>
          <div class="text-caption font-weight-bold text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">
            Total Users
          </div>
        </v-card>
      </v-col>

      <!-- Total Restaurants -->
      <v-col cols="12" sm="6" lg="3">
        <v-card variant="flat" rounded="xl" class="stat-card pa-8 overflow-hidden" style="background:#fff;">
          <div class="d-flex justify-space-between align-start mb-6">
            <v-sheet color="orange-lighten-5" rounded="lg" width="40" height="40"
              class="d-flex align-center justify-center">
              <v-icon color="orange-darken-2" size="20">mdi-silverware-fork-knife</v-icon>
            </v-sheet>
            <v-chip size="x-small" color="orange" variant="tonal" class="font-weight-bold">
              Active
            </v-chip>
          </div>
          <div class="text-h3 font-weight-black text-dark mb-1">{{ stats.total_restaurants }}</div>
          <div class="text-caption font-weight-bold text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">
            Restaurants
          </div>
        </v-card>
      </v-col>

      <!-- Active Bookings -->
      <v-col cols="12" sm="6" lg="3">
        <v-card variant="flat" rounded="xl" class="stat-card pa-8 overflow-hidden" style="background:#fff;">
          <div class="d-flex justify-space-between align-start mb-6">
            <v-sheet color="green-lighten-5" rounded="lg" width="40" height="40"
              class="d-flex align-center justify-center">
              <v-icon color="green-darken-2" size="20">mdi-calendar-check-outline</v-icon>
            </v-sheet>
            <v-chip size="x-small" color="green" variant="tonal" class="font-weight-bold">
              Confirmed
            </v-chip>
          </div>
          <div class="text-h3 font-weight-black text-dark mb-1">{{ stats.confirmed_bookings }}</div>
          <div class="text-caption font-weight-bold text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">
            Confirmed Bookings
          </div>
        </v-card>
      </v-col>

      <!-- Total Bookings - Highlight card -->
      <v-col cols="12" sm="6" lg="3">
        <v-card variant="flat" rounded="xl" class="pa-8 overflow-hidden shadow-indigo" color="indigo-darken-3">
          <div class="d-flex justify-space-between align-start mb-6">
            <v-sheet color="white" rounded="lg" width="40" height="40" style="opacity:0.15"
              class="d-flex align-center justify-center position-absolute"></v-sheet>
            <v-icon color="white" size="20" style="opacity:0.9">mdi-chart-bar</v-icon>
            <v-chip size="x-small" color="white" variant="tonal" class="font-weight-bold text-indigo-darken-3">
              All time
            </v-chip>
          </div>
          <div class="text-h3 font-weight-black text-white mb-1">{{ stats.total_bookings }}</div>
          <div class="text-caption font-weight-bold text-white" style="text-transform:uppercase; letter-spacing:0.1em; opacity:0.7;">
            Total Bookings
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- SECOND ROW STATS -->
    <v-row class="mb-10">
      <v-col cols="12" sm="4">
        <v-card variant="flat" rounded="xl" class="stat-card pa-6" style="background:#fff;">
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-caption font-weight-bold text-grey mb-1" style="text-transform:uppercase; letter-spacing:0.1em;">Pending</div>
              <div class="text-h4 font-weight-black" style="color:#f59e0b;">{{ stats.pending_bookings }}</div>
            </div>
            <v-avatar color="amber-lighten-4" size="48" rounded="lg">
              <v-icon color="amber-darken-3">mdi-clock-outline</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card variant="flat" rounded="xl" class="stat-card pa-6" style="background:#fff;">
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-caption font-weight-bold text-grey mb-1" style="text-transform:uppercase; letter-spacing:0.1em;">Cancelled</div>
              <div class="text-h4 font-weight-black text-error">{{ stats.cancelled_bookings }}</div>
            </div>
            <v-avatar color="red-lighten-4" size="48" rounded="lg">
              <v-icon color="red-darken-2">mdi-close-circle-outline</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card variant="flat" rounded="xl" class="stat-card pa-6" style="background:#fff;">
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-caption font-weight-bold text-grey mb-1" style="text-transform:uppercase; letter-spacing:0.1em;">Active Users</div>
              <div class="text-h4 font-weight-black text-success">{{ stats.active_users }}</div>
            </div>
            <v-avatar color="green-lighten-4" size="48" rounded="lg">
              <v-icon color="green-darken-2">mdi-account-check-outline</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- RECENT BOOKINGS TABLE -->
    <v-card variant="flat" rounded="xl" class="overflow-hidden" style="background:#fff;">
      <div class="d-flex align-center justify-space-between px-8 py-5 border-b">
        <h3 class="text-h6 font-weight-bold text-dark">Recent Bookings</h3>
        <v-btn
          variant="text"
          color="indigo-darken-3"
          class="text-none font-weight-bold text-caption"
          @click="$router.push('/admin/bookings')"
        >View All →</v-btn>
      </div>

      <v-table>
        <thead>
          <tr class="table-header">
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Customer</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Restaurant</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Date & Time</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Guests</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Status</th>
            <th class="text-caption font-weight-black text-grey text-right" style="text-transform:uppercase; letter-spacing:0.1em;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loadingBookings">
            <td colspan="6" class="text-center py-8">
              <v-progress-circular indeterminate color="indigo" size="32"></v-progress-circular>
            </td>
          </tr>
          <tr v-else v-for="booking in recentBookings" :key="booking.id" class="table-row">
            <td class="py-5">
              <div class="d-flex align-center gap-3">
                <v-avatar color="indigo-lighten-4" size="32" rounded="lg">
                  <span class="text-indigo-darken-3 text-caption font-weight-black">
                    {{ booking.user?.full_name?.charAt(0) || 'U' }}
                  </span>
                </v-avatar>
                <span class="text-body-2 font-weight-bold">{{ booking.user?.full_name || 'User #' + booking.user_id }}</span>
              </div>
            </td>
            <td class="text-body-2 font-weight-medium text-grey-darken-2">
              {{ booking.restaurant?.name || '—' }}
            </td>
            <td>
              <div class="text-body-2 font-weight-bold">{{ booking.booking_date }}</div>
              <div class="text-caption text-grey">{{ booking.booking_time?.slice(0,5) }}</div>
            </td>
            <td>
              <v-chip size="small" variant="tonal" color="grey">
                {{ booking.number_of_guests }} guests
              </v-chip>
            </td>
            <td>
              <v-chip
                :color="getStatusColor(booking.status)"
                size="small"
                variant="flat"
                class="font-weight-bold text-uppercase"
                label
              >{{ booking.status }}</v-chip>
            </td>
            <td class="text-right">
              <div class="d-flex justify-end gap-2">
                <v-btn
                  v-if="booking.status === 'pending'"
                  icon size="small"
                  color="indigo"
                  variant="tonal"
                  @click="confirmBooking(booking.id)"
                >
                  <v-icon size="16">mdi-check</v-icon>
                </v-btn>
                <v-btn
                  icon size="small"
                  color="grey"
                  variant="tonal"
                  @click="$router.push('/admin/bookings')"
                >
                  <v-icon size="16">mdi-eye-outline</v-icon>
                </v-btn>
              </div>
            </td>
          </tr>
          <tr v-if="!loadingBookings && recentBookings.length === 0">
            <td colspan="6" class="text-center py-8 text-grey">Chưa có booking nào</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <!-- SNACKBAR -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" rounded="lg" timeout="3000" location="bottom right">
      {{ snackbar.message }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/axios'

const stats = ref({
  total_bookings: 0,
  pending_bookings: 0,
  confirmed_bookings: 0,
  cancelled_bookings: 0,
  total_restaurants: 0,
  total_users: 0,
  active_users: 0,
})
const recentBookings = ref([])
const loadingBookings = ref(false)
const snackbar = ref({ show: false, message: '', color: 'success' })

const showSnackbar = (message, color = 'success') => {
  snackbar.value = { show: true, message, color }
}

const getStatusColor = (status) => {
  switch (status) {
    case 'confirmed': return 'success'
    case 'pending':   return 'warning'
    case 'cancelled': return 'error'
    default:          return 'grey'
  }
}

const fetchStats = async () => {
  try {
    const res = await apiClient.get('/admin/stats')
    stats.value = res.data
  } catch (err) {
    console.error('Stats error:', err)
  }
}

const fetchRecentBookings = async () => {
  loadingBookings.value = true
  try {
    const res = await apiClient.get('/admin/bookings', { params: { limit: 8 } })
    recentBookings.value = res.data
  } catch (err) {
    console.error('Bookings error:', err)
  } finally {
    loadingBookings.value = false
  }
}

const confirmBooking = async (bookingId) => {
  try {
    await apiClient.patch(`/admin/bookings/${bookingId}`, { status: 'confirmed' })
    showSnackbar('Đã xác nhận booking!')
    await fetchRecentBookings()
    await fetchStats()
  } catch (err) {
    showSnackbar('Lỗi xác nhận booking!', 'error')
  }
}

onMounted(async () => {
  await Promise.all([fetchStats(), fetchRecentBookings()])
})
</script>

<style scoped>
.admin-bg { background-color: #f8f9fc !important; }
.text-dark { color: #1a1c1c !important; }
.text-indigo { color: #3730a3 !important; }
.tracking-tight { letter-spacing: -0.02em !important; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

.stat-card {
  border: 1px solid #f1f5f9 !important;
  transition: box-shadow 0.2s ease;
}
.stat-card:hover {
  box-shadow: 0 8px 24px rgba(36, 56, 156, 0.08) !important;
}

.shadow-indigo {
  box-shadow: 0 8px 24px rgba(55, 48, 163, 0.25) !important;
}

.table-header th {
  background-color: #f8fafc !important;
  padding: 16px 24px !important;
}
.table-row:hover {
  background-color: #f8fafc !important;
}
.table-row td {
  padding: 0 24px !important;
  border-bottom: 1px solid #f1f5f9 !important;
}
</style>