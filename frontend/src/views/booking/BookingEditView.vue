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
          <p class="text-body-1 text-medium-emphasis">Update your reservation information below.</p>
        </div>

        <!-- LOADING -->
        <div v-if="pageLoading" class="d-flex justify-center align-center py-16">
          <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
        </div>

        <!-- NOT FOUND -->
        <v-alert v-else-if="!booking" type="error" variant="tonal" rounded="lg">
          Booking not found.
          <v-btn variant="text" color="error" @click="router.push('/dashboard')">Back to Dashboard</v-btn>
        </v-alert>

        <template v-else>
          <!-- RESTAURANT INFO (readonly) -->
          <v-card variant="outlined" rounded="xl" class="bg-white border-subtle mb-6 overflow-hidden">
            <div class="pa-4 d-flex align-center gap-3" style="background-color: #ee7c2b;">
              <v-icon color="white" size="20">mdi-storefront-outline</v-icon>
              <span class="text-white font-weight-bold text-body-1">Reserved Restaurant</span>
              <v-spacer></v-spacer>
              <v-chip size="small" color="white" variant="tonal" class="text-white">Cannot be changed</v-chip>
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

          <!-- EDIT FORM -->
          <v-card variant="outlined" rounded="xl" class="bg-white border-subtle overflow-hidden">
            <v-alert v-if="errorMessage" type="error" variant="tonal" rounded="0" class="mb-0" closable
              @click:close="errorMessage = ''">
              {{ errorMessage }}
            </v-alert>

            <v-form ref="formRef" @submit.prevent="updateBooking" class="pa-8">

              <!-- DATE / TIME / GUESTS -->
              <div class="d-flex align-center gap-2 mb-6 border-b pb-2">
                <v-avatar color="orange-lighten-5" size="32" rounded="lg">
                  <v-icon color="primary" size="18">mdi-calendar-clock</v-icon>
                </v-avatar>
                <h2 class="text-h6 font-weight-bold">Date, Time & Guests</h2>
              </div>

              <v-row>
                <v-col cols="12" md="4">
                  <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Booking Date</label>
                  <v-text-field
                    v-model="form.booking_date"
                    type="date"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                    color="primary"
                    :min="today"
                    :rules="[rules.required]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                  <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Booking Time</label>
                  <v-text-field
                    v-model="form.booking_time"
                    type="time"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                    color="primary"
                    :rules="[rules.required]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                  <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Number of Guests</label>
                  <v-text-field
                    v-model.number="form.number_of_guests"
                    type="number"
                    min="1"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                    prepend-inner-icon="mdi-account-group-outline"
                    color="primary"
                    :rules="[rules.required, rules.minGuests]"
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- STATUS -->
              <div class="d-flex align-center gap-2 mb-6 border-b pb-2 mt-4">
                <v-avatar color="orange-lighten-5" size="32" rounded="lg">
                  <v-icon color="primary" size="18">mdi-list-status</v-icon>
                </v-avatar>
                <h2 class="text-h6 font-weight-bold">Status</h2>
              </div>

              <v-row>
                <v-col cols="12" md="6">
                  <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Update Status</label>
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
                    <span class="text-caption text-error font-weight-bold">Cancelling cannot be undone!</span>
                  </v-sheet>
                </v-col>
              </v-row>

              <!-- NOTES -->
              <div class="d-flex align-center gap-2 mb-6 border-b pb-2 mt-4">
                <v-avatar color="orange-lighten-5" size="32" rounded="lg">
                  <v-icon color="primary" size="18">mdi-note-text-outline</v-icon>
                </v-avatar>
                <h2 class="text-h6 font-weight-bold">Special Notes</h2>
              </div>

              <v-textarea
                v-model="form.special_notes"
                placeholder="Any special requests..."
                variant="outlined"
                rounded="lg"
                rows="3"
                color="primary"
                class="mb-6"
              ></v-textarea>

              <!-- ACTIONS -->
              <div class="d-flex flex-wrap align-center justify-space-between pt-6 border-t gap-4">
                <v-btn color="error" variant="tonal" prepend-icon="mdi-delete-outline"
                  size="large" rounded="lg" class="text-none" @click="deleteDialog = true">
                  Delete Booking
                </v-btn>
                <div class="d-flex gap-3">
                  <v-btn variant="outlined" size="large" rounded="lg" class="text-none"
                    @click="router.push('/dashboard')">Cancel</v-btn>
                  <v-btn color="primary" size="large" rounded="lg" class="text-none px-8"
                    type="submit" prepend-icon="mdi-content-save-outline" :loading="loading">
                    Save Changes
                  </v-btn>
                </div>
              </div>
            </v-form>
          </v-card>

          <!-- ACTIVITY TIMELINE -->
          <div class="mt-10">
            <h3 class="text-h6 font-weight-bold mb-4">Activity History</h3>
            <v-timeline side="end" align="start" density="compact">
              <v-timeline-item dot-color="primary" size="x-small">
                <div class="text-body-2 font-weight-bold">Last updated</div>
                <div class="text-caption text-medium-emphasis">{{ formatDate(booking.updated_at) }}</div>
              </v-timeline-item>
              <v-timeline-item dot-color="grey" size="x-small">
                <div class="text-body-2">Booking created</div>
                <div class="text-caption text-medium-emphasis">{{ formatDate(booking.created_at) }}</div>
              </v-timeline-item>
            </v-timeline>
          </div>
        </template>

      </v-col>
    </v-row>

    <!-- DELETE CONFIRM DIALOG -->
    <v-dialog v-model="deleteDialog" max-width="400" rounded="xl">
      <v-card rounded="xl" class="pa-4">
        <v-card-title class="d-flex align-center gap-2">
          <v-icon color="error">mdi-delete-alert-outline</v-icon>
          Delete Booking
        </v-card-title>
        <v-card-text class="text-medium-emphasis">
          Are you sure you want to delete this booking? This action cannot be undone.
        </v-card-text>
        <v-card-actions class="justify-end gap-2">
          <v-btn variant="text" rounded="lg" class="text-none" @click="deleteDialog = false">
            Cancel
          </v-btn>
          <v-btn color="error" variant="flat" rounded="lg" class="text-none font-weight-bold"
            :loading="deleteLoading" @click="handleDelete">
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/api/axios'

const route = useRoute()
const router = useRouter()
const bookingId = route.params.id

const formRef = ref(null)
const loading = ref(false)
const deleteLoading = ref(false)
const pageLoading = ref(true)
const errorMessage = ref('')
const booking = ref(null)
const deleteDialog = ref(false)
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

// Validation rules
const rules = {
  required: (v) => !!v || 'This field is required.',
  minGuests: (v) => v >= 1 || 'At least 1 guest required.',
}

// Helpers
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
  return new Date(dateStr).toLocaleString('en-GB', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

// Load booking - FIXED: fetch all bookings and find by ID (since no GET /bookings/{id} endpoint)
onMounted(async () => {
  try {
    console.log('Fetching all bookings to find ID:', bookingId)
    const res = await apiClient.get('/bookings/me')
    
    // Unwrap envelope - res.data.data is the array
    const bookingsList = res.data.data || []
    console.log('Bookings list length:', bookingsList.length)
    
    const found = bookingsList.find(b => b.id == bookingId)
    
    if (found) {
      console.log('Booking found:', found)
      booking.value = found
      form.value = {
        booking_date: found.booking_date,
        booking_time: found.booking_time?.slice(0, 5), // HH:MM:SS → HH:MM
        number_of_guests: found.number_of_guests,
        special_notes: found.special_notes || '',
        status: found.status
      }
    } else {
      console.error('Booking not found with ID:', bookingId)
      errorMessage.value = 'Booking not found'
    }
  } catch (err) {
    console.error('Failed to load booking:', err)
    errorMessage.value = 'Failed to load booking details.'
  } finally {
    pageLoading.value = false
  }
})

// Update booking - FIXED error handling
const updateBooking = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  errorMessage.value = ''
  try {
    await apiClient.patch(`/bookings/${bookingId}`, {
      booking_date: form.value.booking_date,
      booking_time: form.value.booking_time + ':00',
      number_of_guests: form.value.number_of_guests,
      special_notes: form.value.special_notes || null,
      status: form.value.status
    })
    showSnackbar('Booking updated successfully.')
    setTimeout(() => router.push('/dashboard'), 1000)
  } catch (err) {
    // Phase 4 error format - read from error.error
    const errBody = err.response?.data?.error
    errorMessage.value = errBody?.message || 'Failed to update booking. Please try again.'
  } finally {
    loading.value = false
  }
}

// Delete booking - FIXED error handling
const handleDelete = async () => {
  deleteLoading.value = true
  try {
    await apiClient.delete(`/bookings/${bookingId}`)
    showSnackbar('Booking deleted successfully.')
    setTimeout(() => router.push('/dashboard'), 1000)
  } catch (err) {
    // Phase 4 error format
    const errBody = err.response?.data?.error
    showSnackbar(errBody?.message || 'Failed to delete booking.', 'error')
    deleteDialog.value = false
  } finally {
    deleteLoading.value = false
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