<template>
  <v-container fluid class="bg-background-light min-h-screen pa-6 pa-md-10">
    <v-row justify="center">
      <v-col cols="12" lg="9" xl="7">

        <!-- BREADCRUMB -->
        <div class="d-flex align-center gap-2 mb-4 text-body-2">
          <router-link to="/dashboard" class="text-decoration-none text-primary font-weight-medium">Bookings</router-link>
          <v-icon size="16" color="grey">mdi-chevron-right</v-icon>
          <span class="text-grey-darken-1">Edit Booking #{{ bookingId }}</span>
        </div>

        <div class="mb-8">
          <h1 class="text-h3 font-weight-black tracking-tight mb-2">Edit Booking Details</h1>
          <p class="text-body-1 text-medium-emphasis">Cập nhật thông tin đặt bàn của bạn.</p>
        </div>

        <!-- LOADING -->
        <div v-if="pageLoading" class="d-flex justify-center align-center py-16">
          <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
        </div>

        <!-- NOT FOUND -->
        <v-alert v-else-if="!booking" type="error" variant="tonal" rounded="lg">
          Không tìm thấy đơn đặt bàn này.
          <v-btn variant="text" color="error" @click="router.push('/dashboard')">Quay lại Dashboard</v-btn>
        </v-alert>

        <template v-else>
          <!-- INFO NHÀ HÀNG (readonly) -->
          <v-card variant="outlined" rounded="xl" class="bg-white border-subtle mb-6 overflow-hidden">
            <div class="pa-4 d-flex align-center gap-3" style="background-color: #ee7c2b;">
              <v-icon color="white" size="20">mdi-storefront-outline</v-icon>
              <span class="text-white font-weight-bold text-body-1">Nhà Hàng Đã Đặt</span>
              <v-spacer></v-spacer>
              <v-chip size="small" color="white" variant="tonal" class="text-white">Không thể thay đổi</v-chip>
            </div>
            <div class="pa-5 d-flex align-center gap-4">
              <v-avatar color="orange-lighten-5" size="52" rounded="lg">
                <v-icon color="primary" size="28">mdi-silverware-fork-knife</v-icon>
              </v-avatar>
              <div class="flex-grow-1">
                <div class="font-weight-black text-body-1">{{ booking.restaurant?.name || '—' }}</div>
                <div class="text-caption text-medium-emphasis mt-1">
                  <v-icon size="12" class="mr-1">mdi-map-marker-outline</v-icon>
                  {{ booking.restaurant?.address || '—' }}
                </div>
                <v-chip v-if="booking.restaurant?.cuisine_type" size="x-small" color="primary" variant="tonal" class="mt-1">
                  {{ booking.restaurant.cuisine_type }}
                </v-chip>
              </div>
              <v-chip
                :color="getStatusColor(booking.status)"
                variant="flat"
                size="small"
                class="font-weight-bold text-uppercase"
                label
              >
                {{ booking.status }}
              </v-chip>
            </div>
          </v-card>

          <!-- FORM SỬA -->
          <v-card variant="outlined" rounded="xl" class="bg-white border-subtle overflow-hidden">
            <v-alert v-if="errorMessage" type="error" variant="tonal" rounded="0" class="mb-0" closable
              @click:close="errorMessage = ''">
              {{ errorMessage }}
            </v-alert>

            <v-form @submit.prevent="updateBooking" class="pa-8">

              <!-- NGÀY GIỜ KHÁCH -->
              <div class="d-flex align-center gap-2 mb-6 border-b pb-2">
                <v-avatar color="orange-lighten-5" size="32" rounded="lg">
                  <v-icon color="primary" size="18">mdi-calendar-clock</v-icon>
                </v-avatar>
                <h2 class="text-h6 font-weight-bold">Thời Gian & Số Khách</h2>
              </div>

              <v-row>
                <v-col cols="12" md="4">
                  <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Ngày đặt</label>
                  <v-text-field
                    v-model="form.booking_date"
                    type="date"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                    color="primary"
                    :min="today"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                  <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Giờ đặt</label>
                  <v-text-field
                    v-model="form.booking_time"
                    type="time"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                    color="primary"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                  <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Số khách</label>
                  <v-text-field
                    v-model.number="form.number_of_guests"
                    type="number"
                    min="1"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                    prepend-inner-icon="mdi-account-group-outline"
                    color="primary"
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- STATUS -->
              <div class="d-flex align-center gap-2 mb-6 border-b pb-2 mt-4">
                <v-avatar color="orange-lighten-5" size="32" rounded="lg">
                  <v-icon color="primary" size="18">mdi-list-status</v-icon>
                </v-avatar>
                <h2 class="text-h6 font-weight-bold">Trạng Thái</h2>
              </div>

              <v-row>
                <v-col cols="12" md="6">
                  <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Cập nhật trạng thái</label>
                  <v-select
                    v-model="form.status"
                    :items="statusItems"
                    item-title="label"
                    item-value="value"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                    color="primary"
                  >
                    <template v-slot:item="{ props, item }">
                      <v-list-item v-bind="props">
                        <template v-slot:prepend>
                          <v-icon :color="item.raw.color" size="18" class="mr-2">{{ item.raw.icon }}</v-icon>
                        </template>
                      </v-list-item>
                    </template>
                  </v-select>
                </v-col>
                <v-col cols="12" md="6" class="d-flex align-center">
                  <v-sheet
                    v-if="form.status === 'cancelled'"
                    color="red-lighten-5" rounded="lg" class="pa-3 d-flex align-center gap-2 w-100"
                  >
                    <v-icon color="error" size="18">mdi-alert-circle-outline</v-icon>
                    <span class="text-caption text-error font-weight-bold">Hủy đơn sẽ không thể hoàn tác!</span>
                  </v-sheet>
                </v-col>
              </v-row>

              <!-- GHI CHÚ -->
              <div class="d-flex align-center gap-2 mb-6 border-b pb-2 mt-4">
                <v-avatar color="orange-lighten-5" size="32" rounded="lg">
                  <v-icon color="primary" size="18">mdi-note-text-outline</v-icon>
                </v-avatar>
                <h2 class="text-h6 font-weight-bold">Ghi Chú</h2>
              </div>

              <v-textarea
                v-model="form.special_notes"
                placeholder="Ghi chú đặc biệt..."
                variant="outlined"
                rounded="lg"
                rows="3"
                color="primary"
                class="mb-6"
              ></v-textarea>

              <!-- ACTIONS -->
              <div class="d-flex flex-wrap align-center justify-space-between pt-6 border-t gap-4">
                <v-btn color="error" variant="tonal" prepend-icon="mdi-delete-outline"
                  size="large" rounded="lg" class="text-none" @click="confirmDelete">
                  Xóa Booking
                </v-btn>
                <div class="d-flex gap-3">
                  <v-btn variant="outlined" size="large" rounded="lg" class="text-none"
                    @click="router.push('/dashboard')">Hủy</v-btn>
                  <v-btn color="primary" size="large" rounded="lg" class="text-none px-8"
                    type="submit" prepend-icon="mdi-content-save-outline" :loading="loading">
                    Lưu Thay Đổi
                  </v-btn>
                </div>
              </div>
            </v-form>
          </v-card>

          <!-- ACTIVITY TIMELINE -->
          <div class="mt-10">
            <h3 class="text-h6 font-weight-bold mb-4">Lịch Sử Hoạt Động</h3>
            <v-timeline side="end" align="start" density="compact">
              <v-timeline-item dot-color="primary" size="x-small">
                <div class="text-body-2 font-weight-bold">Booking được cập nhật lần cuối</div>
                <div class="text-caption text-medium-emphasis">{{ formatDate(booking.updated_at) }}</div>
              </v-timeline-item>
              <v-timeline-item dot-color="grey" size="x-small">
                <div class="text-body-2">Booking được tạo</div>
                <div class="text-caption text-medium-emphasis">{{ formatDate(booking.created_at) }}</div>
              </v-timeline-item>
            </v-timeline>
          </div>
        </template>

      </v-col>
    </v-row>

    <!-- SNACKBAR -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" rounded="lg" timeout="3000" location="bottom right">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/api/axios'

const route = useRoute()
const router = useRouter()
const bookingId = route.params.id
const loading = ref(false)
const pageLoading = ref(true)
const errorMessage = ref('')
const booking = ref(null)
const snackbar = ref({ show: false, message: '', color: 'success' })
const today = new Date().toISOString().split('T')[0]

const form = ref({
  booking_date: '',
  booking_time: '',
  number_of_guests: 1,
  special_notes: '',
  status: 'pending'
})

const statusItems = [
  { label: 'Pending',   value: 'pending',   color: 'warning', icon: 'mdi-clock-outline' },
  { label: 'Confirmed', value: 'confirmed', color: 'success', icon: 'mdi-check-circle-outline' },
  { label: 'Cancelled', value: 'cancelled', color: 'error',   icon: 'mdi-close-circle-outline' },
]

// ==================== HELPERS ====================

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

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleString('vi-VN', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

// ==================== API ====================

onMounted(async () => {
  if (!localStorage.getItem('user_token')) return router.push('/login')
  try {
    // Lấy danh sách rồi tìm booking theo ID
    const res = await apiClient.get('/bookings/me')
    const found = res.data.find(b => b.id == bookingId)
    if (found) {
      booking.value = found
      form.value = {
        booking_date:     found.booking_date,
        booking_time:     found.booking_time?.slice(0, 5), // HH:MM:SS → HH:MM
        number_of_guests: found.number_of_guests,
        special_notes:    found.special_notes || '',
        status:           found.status
      }
    }
  } catch (err) {
    console.error('Lỗi lấy dữ liệu:', err)
  } finally {
    pageLoading.value = false
  }
})

const updateBooking = async () => {
  if (form.value.number_of_guests < 1) {
    errorMessage.value = 'Số khách phải lớn hơn 0!'
    return
  }
  loading.value = true
  errorMessage.value = ''
  try {
    await apiClient.patch(`/bookings/${bookingId}`, {
      booking_date:     form.value.booking_date,
      booking_time:     form.value.booking_time + ':00',
      number_of_guests: form.value.number_of_guests,
      special_notes:    form.value.special_notes || null,
      status:           form.value.status
    })
    showSnackbar('Cập nhật thành công!')
    setTimeout(() => router.push('/dashboard'), 1000)
  } catch (err) {
    const detail = err.response?.data?.detail
    errorMessage.value = typeof detail === 'string' ? detail : 'Lỗi cập nhật, vui lòng thử lại!'
  } finally {
    loading.value = false
  }
}

const confirmDelete = async () => {
  if (!confirm('Bạn có chắc chắn muốn xóa đơn đặt bàn này?')) return
  try {
    await apiClient.delete(`/bookings/${bookingId}`)
    showSnackbar('Đã xóa đơn đặt bàn!')
    setTimeout(() => router.push('/dashboard'), 1000)
  } catch (err) {
    showSnackbar(err.response?.data?.detail || 'Lỗi khi xóa!', 'error')
  }
}
</script>

<style scoped>
.bg-background-light { background-color: #f6f6f8 !important; }
.border-subtle { border: 1px solid #e7d9cf !important; }
.tracking-tight { letter-spacing: -0.015em !important; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
</style>