<template>
  <div class="admin-bg min-h-screen pa-10">

    <!-- HEADER -->
    <div class="d-flex flex-column flex-md-row justify-space-between align-md-end mb-10 gap-4">
      <div>
        <div class="text-caption font-weight-black text-indigo mb-1"
          style="letter-spacing: 0.15em; text-transform: uppercase;">Management</div>
        <h1 class="text-h3 font-weight-black text-dark tracking-tight">Bookings</h1>
        <p class="text-body-2 text-grey-darken-1 mt-1">Managing the pulse of your dining experiences.</p>
      </div>
    </div>

    <!-- STATS BENTO -->
    <v-row class="mb-10">
      <v-col cols="12" md="4">
        <v-card variant="flat" rounded="xl" class="stat-card pa-8 overflow-hidden">
          <div class="text-caption font-weight-black text-grey mb-2"
            style="text-transform:uppercase; letter-spacing:0.1em;">Total Bookings</div>
          <div class="text-h3 font-weight-black text-indigo-darken-3">{{ bookings.length }}</div>
          <v-icon class="sparkle-icon" color="indigo-lighten-4" size="80">mdi-trending-up</v-icon>
        </v-card>
      </v-col>
      <v-col cols="12" md="8">
        <v-card variant="flat" rounded="xl" color="indigo-darken-3" class="pa-8 shadow-indigo h-100">
          <div class="text-caption font-weight-black mb-2"
            style="color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:0.1em;">
            Status Breakdown
          </div>
          <v-row class="mt-2">
            <v-col cols="4" class="text-center">
              <div class="text-h4 font-weight-black text-white">{{ pendingCount }}</div>
              <div class="text-caption text-white" style="opacity:0.7;">Pending</div>
            </v-col>
            <v-col cols="4" class="text-center">
              <div class="text-h4 font-weight-black text-white">{{ confirmedCount }}</div>
              <div class="text-caption text-white" style="opacity:0.7;">Confirmed</div>
            </v-col>
            <v-col cols="4" class="text-center">
              <div class="text-h4 font-weight-black text-white">{{ cancelledCount }}</div>
              <div class="text-caption text-white" style="opacity:0.7;">Cancelled</div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- FILTER + SEARCH -->
    <v-card variant="flat" rounded="xl" class="stat-card overflow-hidden mb-1">
      <div class="px-6 py-4 d-flex align-center justify-space-between border-b flex-wrap gap-3">
        <div class="d-flex gap-2">
          <v-btn
            v-for="tab in statusTabs"
            :key="tab.value"
            :variant="activeStatus === tab.value ? 'flat' : 'text'"
            :color="activeStatus === tab.value ? 'indigo-darken-3' : 'grey'"
            rounded="lg" size="small"
            class="text-none font-weight-bold"
            @click="activeStatus = tab.value; fetchBookings()"
          >
            {{ tab.label }}
            <v-chip v-if="tab.count !== null" size="x-small" class="ml-1"
              :color="activeStatus === tab.value ? 'white' : 'grey-lighten-2'"
              :text-color="activeStatus === tab.value ? 'indigo-darken-3' : 'grey'">
              {{ tab.count }}
            </v-chip>
          </v-btn>
        </div>
        <v-text-field
          v-model="search"
          placeholder="Search bookings..."
          variant="solo" flat density="compact"
          prepend-inner-icon="mdi-magnify"
          hide-details rounded="lg"
          bg-color="grey-lighten-4"
          style="max-width: 280px;"
          @update:model-value="onSearch"
        ></v-text-field>
      </div>

      <!-- TABLE -->
      <v-table>
        <thead>
          <tr class="table-header">
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">ID</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Customer</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Restaurant</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Date & Time</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Guests</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Status</th>
            <th class="text-caption font-weight-black text-grey text-right" style="text-transform:uppercase; letter-spacing:0.1em;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="7" class="text-center py-8">
              <v-progress-circular indeterminate color="indigo" size="32"></v-progress-circular>
            </td>
          </tr>
          <tr v-else v-for="booking in bookings" :key="booking.id" class="table-row">
            <td class="py-5">
              <span class="text-caption font-weight-medium text-grey" style="font-family:monospace;">
                #BK-{{ String(booking.id).padStart(4, '0') }}
              </span>
            </td>
            <td class="py-5">
              <div class="d-flex align-center gap-3">
                <v-avatar color="indigo-lighten-4" size="32" rounded="lg">
                  <span class="text-indigo-darken-3 text-caption font-weight-black">
                    {{ booking.user?.full_name?.charAt(0) || 'U' }}
                  </span>
                </v-avatar>
                <span class="text-body-2 font-weight-bold">
                  {{ booking.user?.full_name || 'User #' + booking.user_id }}
                </span>
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
              <v-chip :color="getStatusColor(booking.status)" size="small"
                variant="flat" class="font-weight-bold text-uppercase" label>
                {{ booking.status }}
              </v-chip>
            </td>
            <td class="text-right">
              <div class="d-flex justify-end gap-2 action-btns">
                <v-tooltip text="Confirm" location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn v-if="booking.status === 'pending'"
                      v-bind="props" icon size="small" color="success" variant="tonal"
                      @click="updateStatus(booking.id, 'confirmed')">
                      <v-icon size="16">mdi-check</v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>
                <v-tooltip text="Cancel" location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn v-if="booking.status !== 'cancelled'"
                      v-bind="props" icon size="small" color="error" variant="tonal"
                      @click="updateStatus(booking.id, 'cancelled')">
                      <v-icon size="16">mdi-close</v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>
                <v-tooltip text="Delete" location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon size="small" color="grey" variant="tonal"
                      @click="confirmDelete(booking)">
                      <v-icon size="16">mdi-delete-outline</v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>
              </div>
            </td>
          </tr>
          <tr v-if="!loading && bookings.length === 0">
            <td colspan="7" class="text-center py-10 text-grey">
              <v-icon size="48" color="grey-lighten-2" class="mb-2">mdi-calendar-blank</v-icon>
              <div>No bookings found.</div>
            </td>
          </tr>
        </tbody>
      </v-table>

      <div class="px-6 py-4 bg-grey-lighten-5 d-flex align-center justify-space-between border-t">
        <span class="text-caption font-weight-bold text-grey"
          style="text-transform:uppercase; letter-spacing:0.1em;">
          Showing {{ bookings.length }} bookings
        </span>
      </div>
    </v-card>

    <!-- DELETE DIALOG -->
    <v-dialog v-model="deleteDialog.show" max-width="420">
      <v-card rounded="xl" class="pa-6">
        <div class="text-center mb-6">
          <v-avatar color="red-lighten-4" size="64" class="mb-4">
            <v-icon color="error" size="32">mdi-delete-outline</v-icon>
          </v-avatar>
          <h3 class="text-h6 font-weight-bold text-dark mb-2">Delete Booking?</h3>
          <p class="text-body-2 text-grey-darken-1">
            Delete booking
            <strong>#BK-{{ String(deleteDialog.booking?.id || 0).padStart(4, '0') }}</strong>
            from <strong>{{ deleteDialog.booking?.user?.full_name || 'this user' }}</strong>?
            This action cannot be undone.
          </p>
        </div>
        <div class="d-flex gap-3">
          <v-btn variant="outlined" rounded="lg" class="text-none flex-grow-1"
            @click="deleteDialog.show = false">Cancel</v-btn>
          <v-btn color="error" variant="flat" rounded="lg"
            class="text-none font-weight-bold flex-grow-1"
            :loading="deleteDialog.loading" @click="deleteBooking">Delete</v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- SNACKBAR -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" rounded="lg" timeout="3000" location="bottom right">
      {{ snackbar.message }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '@/api/axios'

const bookings     = ref([])
const loading      = ref(false)
const search       = ref('')
const activeStatus = ref('all')
const deleteDialog = ref({ show: false, loading: false, booking: null })
const snackbar     = ref({ show: false, message: '', color: 'success' })
let searchTimeout  = null

// ── Computed ──────────────────────────────────────────────────────
const pendingCount   = computed(() => bookings.value.filter(b => b.status === 'pending').length)
const confirmedCount = computed(() => bookings.value.filter(b => b.status === 'confirmed').length)
const cancelledCount = computed(() => bookings.value.filter(b => b.status === 'cancelled').length)

const statusTabs = computed(() => [
  { label: 'All',       value: 'all',       count: bookings.value.length },
  { label: 'Pending',   value: 'pending',   count: pendingCount.value },
  { label: 'Confirmed', value: 'confirmed', count: confirmedCount.value },
  { label: 'Cancelled', value: 'cancelled', count: cancelledCount.value },
])

// ── Helpers ───────────────────────────────────────────────────────
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

const confirmDelete = (booking) => {
  deleteDialog.value = { show: true, loading: false, booking }
}

const onSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => fetchBookings(), 400)
}

// ── API ───────────────────────────────────────────────────────────
const fetchBookings = async () => {
  loading.value = true
  try {
    const params = { limit: 100 }
    if (search.value.trim())       params.search = search.value.trim()
    if (activeStatus.value !== 'all') params.status = activeStatus.value
    const res = await apiClient.get('/admin/bookings', { params })
    bookings.value = res.data
  } catch (err) {
    showSnackbar('Failed to load bookings.', 'error')
  } finally {
    loading.value = false
  }
}

const updateStatus = async (bookingId, status) => {
  try {
    await apiClient.patch(`/admin/bookings/${bookingId}`, { status })
    showSnackbar(status === 'confirmed' ? 'Booking confirmed.' : 'Booking cancelled.')
    // Cập nhật local state — không fetch lại toàn bộ
    const booking = bookings.value.find(b => b.id === bookingId)
    if (booking) booking.status = status
  } catch (err) {
    showSnackbar(err.response?.data?.detail || 'Failed to update status.', 'error')
  }
}

const deleteBooking = async () => {
  deleteDialog.value.loading = true
  try {
    await apiClient.delete(`/admin/bookings/${deleteDialog.value.booking.id}`)
    showSnackbar('Booking deleted successfully.')
    deleteDialog.value.show = false
    await fetchBookings()
  } catch (err) {
    showSnackbar(err.response?.data?.detail || 'Failed to delete booking.', 'error')
  } finally {
    deleteDialog.value.loading = false
  }
}

onMounted(fetchBookings)
</script>

<style scoped>
.admin-bg { background-color: #f8f9fc !important; }
.text-dark { color: #1a1c1c !important; }
.text-indigo { color: #3730a3 !important; }
.tracking-tight { letter-spacing: -0.02em !important; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
.stat-card { background: #fff !important; border: 1px solid #f1f5f9 !important; }
.shadow-indigo { box-shadow: 0 8px 24px rgba(55, 48, 163, 0.25) !important; }
.h-100 { height: 100%; }
.sparkle-icon { position: absolute; bottom: -10px; right: -10px; opacity: 0.08; }
.table-header th { background-color: #f8fafc !important; padding: 16px 20px !important; }
.table-row td { padding: 0 20px !important; border-bottom: 1px solid #f1f5f9 !important; }
.table-row:hover { background-color: #f8fafc !important; }
.action-btns { opacity: 0; transition: opacity 0.2s; }
.table-row:hover .action-btns { opacity: 1; }
</style>