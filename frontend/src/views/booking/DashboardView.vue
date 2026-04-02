<template>
  <v-container fluid class="bg-background-light min-h-screen pa-6 pa-md-10">
    <v-row justify="center">
      <v-col cols="12" lg="10" xl="8">

        <!-- HEADER -->
        <header class="d-flex align-center justify-space-between mb-6 pb-4 border-b">
          <div class="d-flex align-center gap-4">
            <v-sheet width="48" height="48" color="orange-lighten-5" rounded="lg"
              class="d-flex align-center justify-center">
              <v-icon color="primary" size="28">mdi-calendar-check</v-icon>
            </v-sheet>
            <div>
              <h1 class="text-h4 font-weight-bold tracking-tight">My Bookings</h1>
              <p class="text-body-2 text-medium-emphasis">
                Welcome back,
                <span class="font-weight-bold text-primary">
                  {{ authStore.user?.full_name || authStore.user?.email || 'User' }}
                </span>
              </p>
            </div>
          </div>

          <div class="d-flex align-center gap-3">
            <v-btn color="primary" prepend-icon="mdi-plus" size="large" rounded="lg"
              class="text-none font-weight-bold d-none d-sm-flex" style="margin-right: 45px;"
              @click="router.push('/bookings/new')">
              Create New
            </v-btn>
            <v-btn color="primary" icon="mdi-plus" size="small" class="d-flex d-sm-none" rounded="lg"
              @click="router.push('/bookings/new')"></v-btn>

            <v-menu min-width="220px" rounded="xl" transition="slide-y-transition">
              <template v-slot:activator="{ props }">
                <v-btn icon v-bind="props" variant="text">
                  <v-avatar color="primary" size="44" class="elevation-2">
                    <span class="text-white text-h6 font-weight-bold">
                      {{ avatarLetter }}
                    </span>
                  </v-avatar>
                </v-btn>
              </template>
              <v-card class="mt-2">
                <v-list class="pa-2">
                  <v-list-item
                    prepend-icon="mdi-account-circle-outline"
                    :title="authStore.user?.full_name || authStore.user?.email"
                    subtitle="Logged in"
                    class="mb-2"
                  ></v-list-item>
                  <v-divider class="mb-2"></v-divider>
                  <v-list-item link prepend-icon="mdi-badge-account-outline" title="My Profile"
                    @click="router.push('/profile')"></v-list-item>
                  <v-list-item link prepend-icon="mdi-logout" title="Logout" color="error"
                    @click="handleLogout"></v-list-item>
                </v-list>
              </v-card>
            </v-menu>
          </div>
        </header>

        <!-- STATS CARDS -->
        <v-row class="mb-6">
          <v-col cols="6" sm="3">
            <v-card variant="outlined" rounded="xl" class="pa-4 text-center border-thin bg-white">
              <v-icon color="primary" size="28" class="mb-2">mdi-calendar-check</v-icon>
              <div class="text-h5 font-weight-black text-primary">{{ stats.total }}</div>
              <div class="text-caption text-medium-emphasis font-weight-bold">Total</div>
            </v-card>
          </v-col>
          <v-col cols="6" sm="3">
            <v-card variant="outlined" rounded="xl" class="pa-4 text-center border-thin bg-white">
              <v-icon color="warning" size="28" class="mb-2">mdi-clock-outline</v-icon>
              <div class="text-h5 font-weight-black text-warning">{{ stats.pending }}</div>
              <div class="text-caption text-medium-emphasis font-weight-bold">Pending</div>
            </v-card>
          </v-col>
          <v-col cols="6" sm="3">
            <v-card variant="outlined" rounded="xl" class="pa-4 text-center border-thin bg-white">
              <v-icon color="success" size="28" class="mb-2">mdi-check-decagram</v-icon>
              <div class="text-h5 font-weight-black text-success">{{ stats.confirmed }}</div>
              <div class="text-caption text-medium-emphasis font-weight-bold">Confirmed</div>
            </v-card>
          </v-col>
          <v-col cols="6" sm="3">
            <v-card variant="outlined" rounded="xl" class="pa-4 text-center border-thin bg-white">
              <v-icon color="error" size="28" class="mb-2">mdi-close-circle</v-icon>
              <div class="text-h5 font-weight-black text-error">{{ stats.cancelled }}</div>
              <div class="text-caption text-medium-emphasis font-weight-bold">Cancelled</div>
            </v-card>
          </v-col>
        </v-row>

        <!-- FILTER + SEARCH -->
        <v-row class="mb-4 align-center">
          <v-col cols="12" md="6">
            <v-tabs v-model="activeTab" color="primary" align-tabs="start" @update:model-value="() => fetchBookings(true)">
              <v-tab value="all" class="text-none font-weight-bold">
                All
                <v-chip size="x-small" variant="tonal" class="ml-2">{{ stats.total }}</v-chip>
              </v-tab>
              <v-tab value="pending" class="text-none font-weight-bold">
                Pending
                <v-chip size="x-small" color="warning" variant="flat" class="ml-2">{{ stats.pending }}</v-chip>
              </v-tab>
              <v-tab value="confirmed" class="text-none font-weight-bold">
                Confirmed
                <v-chip size="x-small" color="success" variant="flat" class="ml-2">{{ stats.confirmed }}</v-chip>
              </v-tab>
              <v-tab value="cancelled" class="text-none font-weight-bold">
                Cancelled
                <v-chip size="x-small" color="error" variant="flat" class="ml-2">{{ stats.cancelled }}</v-chip>
              </v-tab>
            </v-tabs>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="search"
              prepend-inner-icon="mdi-magnify"
              label="Search restaurant name..."
              variant="outlined"
              density="comfortable"
              rounded="lg"
              hide-details
              bg-color="white"
              @update:model-value="onSearch"
            ></v-text-field>
          </v-col>
        </v-row>

        <!-- TABLE -->
        <v-card variant="outlined" rounded="xl" class="border-thin overflow-hidden">
          <v-table>
            <thead class="bg-grey-lighten-5">
              <tr>
                <th class="text-uppercase text-caption font-weight-bold">Restaurant</th>
                <th class="text-uppercase text-caption font-weight-bold">Address</th>
                <th class="text-uppercase text-caption font-weight-bold">Date / Time</th>
                <th class="text-uppercase text-caption font-weight-bold">Guests</th>
                <th class="text-uppercase text-caption font-weight-bold">Status</th>
                <th class="text-uppercase text-caption font-weight-bold text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="6" class="text-center py-6">
                  <v-progress-circular indeterminate color="primary" size="32"></v-progress-circular>
                </td>
              </tr>

              <tr v-else v-for="booking in bookings" :key="booking.id">
                <td class="font-weight-bold">{{ booking.restaurant?.name || '—' }}</td>
                <td class="text-body-2 text-medium-emphasis">{{ booking.restaurant?.address || '—' }}</td>
                <td>
                  <div class="text-body-2">{{ booking.booking_date }}</div>
                  <div class="text-caption text-grey">{{ booking.booking_time }}</div>
                </td>
                <td>
                  <v-chip size="small" variant="text" prepend-icon="mdi-account-group">
                    {{ booking.number_of_guests }}
                  </v-chip>
                </td>
                <td>
                  <v-chip
                    :color="getStatusColor(booking.status, booking.booking_date, booking.booking_time)"
                    size="small"
                    class="font-weight-bold text-uppercase"
                    label
                  >
                    {{ getStatusLabel(booking.status, booking.booking_date, booking.booking_time) }}
                  </v-chip>
                </td>
                <td class="text-right">
                  <v-btn icon="mdi-pencil-outline" variant="text" size="small" color="grey"
                    @click="router.push(`/bookings/edit/${booking.id}`)"></v-btn>
                  <v-btn icon="mdi-delete-outline" variant="text" size="small" color="red-lighten-1"
                    @click="confirmDelete(booking.id)"></v-btn>
                </td>
              </tr>

              <tr v-if="!loading && bookings.length === 0">
                <td colspan="6" class="text-center py-8 text-grey">
                  <v-icon size="48" color="grey-lighten-2" class="mb-2">mdi-calendar-blank</v-icon>
                  <div>No bookings found.</div>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>

        <!-- PAGINATION INFO -->
        <div class="d-flex justify-space-between align-center mt-6">
          <p class="text-caption text-medium-emphasis">
            Showing {{ bookings.length }} of {{ meta.total }} bookings
            <v-btn v-if="meta.has_next" variant="text" size="small" @click="loadMore">
              Load more
            </v-btn>
          </p>
        </div>

        <!-- CHATBOT -->
        <Chatbot class="mt-8" />

      </v-col>
    </v-row>

    <!-- DELETE CONFIRM DIALOG -->
    <v-dialog v-model="deleteDialog.show" max-width="400" rounded="xl">
      <v-card rounded="xl" class="pa-4">
        <v-card-title class="d-flex align-center gap-2">
          <v-icon color="error">mdi-delete-alert-outline</v-icon>
          Delete Booking
        </v-card-title>
        <v-card-text class="text-medium-emphasis">
          Are you sure you want to delete this booking? This action cannot be undone.
        </v-card-text>
        <v-card-actions class="justify-end gap-2">
          <v-btn variant="text" rounded="lg" class="text-none"
            @click="deleteDialog.show = false">
            Cancel
          </v-btn>
          <v-btn color="error" variant="flat" rounded="lg" class="text-none font-weight-bold"
            :loading="deleteDialog.loading"
            @click="handleDelete">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- SNACKBAR -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" rounded="lg" timeout="3000" location="bottom right">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api/axios'
import Chatbot from '@/components/Chatbot.vue'

const router = useRouter()
const authStore = useAuthStore()

// State
const activeTab = ref('all')
const search = ref('')
const loading = ref(false)
const bookings = ref([])
const stats = ref({ total: 0, pending: 0, confirmed: 0, cancelled: 0, expired: 0 })
const snackbar = ref({ show: false, message: '', color: 'success' })
const deleteDialog = ref({ show: false, loading: false, bookingId: null })

// Pagination state
const meta = ref({ total: 0, has_next: false, page: 1, pages: 1 })
const currentPage = ref(1)

let searchTimeout = null

// Avatar letter
const avatarLetter = computed(() => {
  const name = authStore.user?.full_name
  const email = authStore.user?.email
  return (name || email || 'U').charAt(0).toUpperCase()
})

// Helpers
const showSnackbar = (message, color = 'success') => {
  snackbar.value = { show: true, message, color }
}

const getStatusColor = (status, date, time) => {
  if (status === 'pending') {
    const bookingDt = new Date(`${date}T${time}`)
    if (bookingDt < new Date()) return 'grey'
  }
  switch (status) {
    case 'confirmed': return 'success'
    case 'pending': return 'warning'
    case 'cancelled': return 'error'
    default: return 'grey'
  }
}

const getStatusLabel = (status, date, time) => {
  if (status === 'pending') {
    const bookingDt = new Date(`${date}T${time}`)
    if (bookingDt < new Date()) return 'expired'
  }
  return status
}

// API calls
const fetchStats = async () => {
  try {
    const res = await apiClient.get('/bookings/stats')
    stats.value = res.data
  } catch (err) {
    console.error('Stats error:', err)
  }
}

const fetchBookings = async (resetPage = true) => {
  if (resetPage) {
    currentPage.value = 1
    bookings.value = []
  }

  loading.value = true
  try {
    const params = { page: currentPage.value, limit: 10 }
    if (search.value.trim()) params.search = search.value.trim()
    if (activeTab.value !== 'all') params.status = activeTab.value

    const res = await apiClient.get('/bookings/me', { params })
    const newBookings = res.data.data || []
    const metaData = res.data.meta || { total: 0, has_next: false }

    if (resetPage) {
      bookings.value = newBookings
    } else {
      bookings.value = [...bookings.value, ...newBookings]
    }

    meta.value = metaData
  } catch (err) {
    showSnackbar('Failed to load bookings.', 'error')
    console.error('Fetch bookings error:', err)
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  if (meta.value.has_next && !loading.value) {
    currentPage.value++
    fetchBookings(false)
  }
}

const onSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => fetchBookings(true), 400)
}

const confirmDelete = (bookingId) => {
  deleteDialog.value = { show: true, loading: false, bookingId }
}

const handleDelete = async () => {
  deleteDialog.value.loading = true
  try {
    await apiClient.delete(`/bookings/${deleteDialog.value.bookingId}`)
    bookings.value = bookings.value.filter(b => b.id !== deleteDialog.value.bookingId)
    await fetchStats()
    showSnackbar('Booking deleted successfully.')
  } catch (err) {
    const errBody = err.response?.data?.error
    showSnackbar(errBody?.message || 'Failed to delete booking.', 'error')
  } finally {
    deleteDialog.value = { show: false, loading: false, bookingId: null }
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  await Promise.all([fetchStats(), fetchBookings(true)])
})
</script>

<style scoped>
.bg-background-light { background-color: #f8f7f6 !important; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
.tracking-tight { letter-spacing: -0.015em !important; }
.text-warning { color: #FB8C00 !important; }
</style>