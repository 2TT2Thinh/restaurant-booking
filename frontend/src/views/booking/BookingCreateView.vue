<template>
  <v-container fluid class="bg-background-light min-h-screen pa-6 pa-md-10">
    <v-row justify="center">
      <v-col cols="12" xl="10">

        <!-- BREADCRUMB -->
        <div class="d-flex align-center gap-2 mb-4 text-body-2">
          <router-link to="/dashboard" class="text-decoration-none text-primary font-weight-medium">
            Bookings
          </router-link>
          <v-icon size="16" color="grey">mdi-chevron-right</v-icon>
          <span class="text-grey-darken-1">Create New</span>
        </div>

        <div class="mb-8">
          <h1 class="text-h3 font-weight-black tracking-tight mb-2">Create New Booking</h1>
          <p class="text-subtitle-1 text-brown">Select a restaurant and fill in your reservation details below.</p>
        </div>

        <v-alert v-if="errorMessage" type="error" variant="tonal" rounded="lg" class="mb-6" closable
          @click:close="errorMessage = ''">
          {{ errorMessage }}
        </v-alert>

        <v-row>
          <!-- LEFT: FORM -->
          <v-col cols="12" lg="7">
            <v-card variant="outlined" rounded="xl" class="pa-8 bg-white border-subtle">
              <v-form ref="formRef" @submit.prevent="handleCreate">

                <!-- SELECT RESTAURANT -->
                <div class="d-flex align-center gap-2 mb-5 pb-2 border-b">
                  <v-avatar color="orange-lighten-5" size="32" rounded="lg">
                    <v-icon color="primary" size="18">mdi-silverware-fork-knife</v-icon>
                  </v-avatar>
                  <h2 class="text-h6 font-weight-bold">Select Restaurant</h2>
                </div>

                <v-text-field
                  v-model="restaurantSearch"
                  placeholder="Search by name or cuisine type..."
                  variant="outlined"
                  rounded="lg"
                  prepend-inner-icon="mdi-magnify"
                  color="primary"
                  hide-details
                  class="mb-3"
                  @update:model-value="onRestaurantSearch"
                ></v-text-field>

                <v-progress-linear v-if="loadingRestaurants" indeterminate color="primary" rounded class="mb-2"></v-progress-linear>

                <!-- Hiện lỗi nếu chưa chọn nhà hàng khi submit -->
                <p v-if="restaurantError" class="text-caption text-error mb-2 ml-1">
                  <v-icon size="14" class="mr-1">mdi-alert-circle-outline</v-icon>
                  Please select a restaurant.
                </p>

                <v-sheet border rounded="lg" class="overflow-hidden mb-6" style="max-height: 260px; overflow-y: auto;">
                  <v-list density="compact" class="pa-0">
                    <v-list-item
                      v-for="r in restaurants"
                      :key="r.id"
                      :class="form.restaurant_id === r.id ? 'bg-orange-lighten-5 border-left-primary' : ''"
                      class="py-3"
                      @click="selectRestaurant(r)"
                    >
                      <template v-slot:prepend>
                        <v-avatar
                          :color="form.restaurant_id === r.id ? 'primary' : 'grey-lighten-3'"
                          size="36" rounded="lg" class="mr-3"
                        >
                          <v-icon :color="form.restaurant_id === r.id ? 'white' : 'grey'" size="18">
                            mdi-silverware-fork-knife
                          </v-icon>
                        </v-avatar>
                      </template>
                      <v-list-item-title class="font-weight-bold text-body-2">{{ r.name }}</v-list-item-title>
                      <v-list-item-subtitle class="text-caption mt-1">
                        <v-icon size="12" class="mr-1">mdi-map-marker-outline</v-icon>{{ r.address }}
                      </v-list-item-subtitle>
                      <template v-slot:append>
                        <div class="d-flex flex-column align-end gap-1">
                          <v-chip v-if="r.cuisine_type" size="x-small" color="primary" variant="tonal">{{ r.cuisine_type }}</v-chip>
                          <v-chip size="x-small" color="grey" variant="tonal">
                            <v-icon start size="10">mdi-account-group</v-icon>{{ r.max_capacity }}
                          </v-chip>
                        </div>
                      </template>
                    </v-list-item>

                    <v-list-item v-if="restaurants.length === 0 && !loadingRestaurants" class="py-6">
                      <v-list-item-title class="text-grey text-center text-body-2">
                        No restaurants found.
                      </v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-sheet>

                <v-divider class="mb-6"></v-divider>

                <!-- DATE / TIME / GUESTS -->
                <div class="d-flex align-center gap-2 mb-5 pb-2 border-b">
                  <v-avatar color="orange-lighten-5" size="32" rounded="lg">
                    <v-icon color="primary" size="18">mdi-calendar-clock</v-icon>
                  </v-avatar>
                  <h2 class="text-h6 font-weight-bold">Date, Time & Guests</h2>
                </div>

                <v-row>
                  <v-col cols="12" sm="4">
                    <label class="text-subtitle-2 font-weight-bold mb-2 d-block">
                      Booking Date <span class="text-error">*</span>
                    </label>
                    <v-text-field
                      v-model="form.booking_date"
                      type="date"
                      variant="outlined"
                      rounded="lg"
                      color="primary"
                      :min="today"
                      :rules="[rules.required]"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="4">
                    <label class="text-subtitle-2 font-weight-bold mb-2 d-block">
                      Booking Time <span class="text-error">*</span>
                    </label>
                    <v-text-field
                      v-model="form.booking_time"
                      type="time"
                      variant="outlined"
                      rounded="lg"
                      color="primary"
                      :rules="[rules.required]"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="4">
                    <label class="text-subtitle-2 font-weight-bold mb-2 d-block">
                      Guests <span class="text-error">*</span>
                    </label>
                    <v-text-field
                      v-model.number="form.number_of_guests"
                      type="number"
                      min="1"
                      :max="selectedRestaurant?.max_capacity || 999"
                      variant="outlined"
                      rounded="lg"
                      prepend-inner-icon="mdi-account-group"
                      color="primary"
                      :rules="[rules.required, rules.minGuests, rules.maxGuests]"
                    ></v-text-field>
                  </v-col>
                </v-row>

                <v-divider class="mb-6"></v-divider>

                <!-- SPECIAL NOTES -->
                <div class="d-flex align-center gap-2 mb-5 pb-2 border-b">
                  <v-avatar color="orange-lighten-5" size="32" rounded="lg">
                    <v-icon color="primary" size="18">mdi-note-text-outline</v-icon>
                  </v-avatar>
                  <h2 class="text-h6 font-weight-bold">Special Notes</h2>
                </div>

                <v-textarea
                  v-model="form.special_notes"
                  placeholder="e.g. Window seat, children attending, food allergies..."
                  variant="outlined"
                  rounded="lg"
                  rows="3"
                  color="primary"
                  class="mb-6"
                ></v-textarea>

                <div class="d-flex justify-end gap-4">
                  <v-btn variant="flat" color="grey-lighten-3" height="48" min-width="120"
                    class="text-none font-weight-bold" @click="router.push('/dashboard')">
                    Cancel
                  </v-btn>
                  <v-btn variant="flat" color="primary" height="48" min-width="160"
                    class="text-none font-weight-bold shadow-orange" type="submit" :loading="loading">
                    <v-icon start>mdi-calendar-plus</v-icon>Create Booking
                  </v-btn>
                </div>

              </v-form>
            </v-card>
          </v-col>

          <!-- RIGHT: INFO + SUMMARY -->
          <v-col cols="12" lg="5">

            <!-- RESTAURANT INFO -->
            <v-card variant="outlined" rounded="xl" class="bg-white border-subtle mb-4 overflow-hidden">
              <div class="pa-4 d-flex align-center gap-3" style="background-color: #ee7c2b;">
                <v-icon color="white" size="20">mdi-storefront-outline</v-icon>
                <span class="text-white font-weight-bold text-body-1">Restaurant Info</span>
              </div>

              <div v-if="!selectedRestaurant" class="pa-8 text-center">
                <v-icon size="56" color="grey-lighten-2" class="mb-3">mdi-silverware-fork-knife</v-icon>
                <p class="text-body-2 text-grey">Select a restaurant on the left to see its details.</p>
              </div>

              <div v-else class="pa-5">
                <div class="d-flex align-center gap-3 mb-4">
                  <v-avatar color="orange-lighten-5" size="52" rounded="lg">
                    <v-icon color="primary" size="28">mdi-silverware-fork-knife</v-icon>
                  </v-avatar>
                  <div>
                    <div class="font-weight-black text-body-1">{{ selectedRestaurant.name }}</div>
                    <v-chip v-if="selectedRestaurant.cuisine_type" size="x-small" color="primary" variant="tonal" class="mt-1">
                      {{ selectedRestaurant.cuisine_type }}
                    </v-chip>
                  </div>
                </div>
                <v-divider class="mb-4"></v-divider>
                <div class="d-flex flex-column gap-3">
                  <div class="d-flex align-center gap-3">
                    <v-icon color="primary" size="18">mdi-map-marker-outline</v-icon>
                    <span class="text-body-2">{{ selectedRestaurant.address }}</span>
                  </div>
                  <div v-if="selectedRestaurant.phone" class="d-flex align-center gap-3">
                    <v-icon color="primary" size="18">mdi-phone-outline</v-icon>
                    <span class="text-body-2">{{ selectedRestaurant.phone }}</span>
                  </div>
                  <div v-if="selectedRestaurant.opening_time" class="d-flex align-center gap-3">
                    <v-icon color="primary" size="18">mdi-clock-outline</v-icon>
                    <span class="text-body-2">{{ selectedRestaurant.opening_time }} – {{ selectedRestaurant.closing_time }}</span>
                  </div>
                  <div class="d-flex align-center gap-3">
                    <v-icon color="primary" size="18">mdi-account-group-outline</v-icon>
                    <span class="text-body-2">Max capacity: <strong>{{ selectedRestaurant.max_capacity }} guests</strong></span>
                  </div>
                </div>
              </div>
            </v-card>

            <!-- BOOKING SUMMARY -->
            <v-card variant="outlined" rounded="xl" class="bg-white border-subtle overflow-hidden">
              <div class="pa-4 bg-orange-lighten-5 d-flex align-center gap-3">
                <v-icon color="primary" size="20">mdi-clipboard-text-outline</v-icon>
                <span class="text-primary font-weight-bold text-body-1">Booking Summary</span>
              </div>
              <div class="pa-5">
                <div class="d-flex flex-column gap-3">
                  <div class="d-flex justify-space-between align-center">
                    <span class="text-caption text-medium-emphasis font-weight-bold text-uppercase">Restaurant</span>
                    <span class="text-body-2 font-weight-bold text-right" style="max-width:60%">
                      {{ selectedRestaurant?.name || '—' }}
                    </span>
                  </div>
                  <v-divider></v-divider>
                  <div class="d-flex justify-space-between align-center">
                    <span class="text-caption text-medium-emphasis font-weight-bold text-uppercase">Date</span>
                    <span class="text-body-2 font-weight-bold">{{ form.booking_date || '—' }}</span>
                  </div>
                  <v-divider></v-divider>
                  <div class="d-flex justify-space-between align-center">
                    <span class="text-caption text-medium-emphasis font-weight-bold text-uppercase">Time</span>
                    <span class="text-body-2 font-weight-bold">{{ form.booking_time || '—' }}</span>
                  </div>
                  <v-divider></v-divider>
                  <div class="d-flex justify-space-between align-center">
                    <span class="text-caption text-medium-emphasis font-weight-bold text-uppercase">Guests</span>
                    <v-chip size="small" color="primary" variant="tonal">
                      <v-icon start size="14">mdi-account-group</v-icon>{{ form.number_of_guests }}
                    </v-chip>
                  </div>
                  <template v-if="form.special_notes">
                    <v-divider></v-divider>
                    <div class="d-flex flex-column gap-1">
                      <span class="text-caption text-medium-emphasis font-weight-bold text-uppercase">Notes</span>
                      <span class="text-body-2 text-grey-darken-1 font-italic">{{ form.special_notes }}</span>
                    </div>
                  </template>
                </div>

                <v-sheet color="orange-lighten-5" rounded="lg" class="pa-3 mt-5 d-flex align-center gap-2">
                  <v-icon color="warning" size="18">mdi-clock-outline</v-icon>
                  <span class="text-caption font-weight-bold text-orange-darken-2">
                    Status will be <strong>PENDING</strong> after creation.
                  </span>
                </v-sheet>
              </div>
            </v-card>

          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" rounded="lg" timeout="3000" location="bottom right">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/axios'

const router = useRouter()

const formRef            = ref(null)
const loading            = ref(false)
const loadingRestaurants = ref(false)
const errorMessage       = ref('')
const restaurantError    = ref(false)   // lỗi chưa chọn nhà hàng
const restaurants        = ref([])
const selectedRestaurant = ref(null)
const restaurantSearch   = ref('')
const snackbar           = ref({ show: false, message: '', color: 'success' })
const today              = new Date().toISOString().split('T')[0]

const form = ref({
  restaurant_id:    null,
  booking_date:     today,
  booking_time:     '19:00',
  number_of_guests: 2,
  special_notes:    ''
})

let searchTimeout = null

// ── Validation rules ──────────────────────────────────────────────
const rules = {
  required:  (v) => !!v || 'This field is required.',
  minGuests: (v) => v >= 1 || 'At least 1 guest required.',
  maxGuests: (v) => {
    const max = selectedRestaurant.value?.max_capacity
    if (!max) return true
    return v <= max || `Maximum capacity is ${max} guests.`
  },
}

// ── Helpers ───────────────────────────────────────────────────────
const showSnackbar = (message, color = 'success') => {
  snackbar.value = { show: true, message, color }
}

const selectRestaurant = (r) => {
  form.value.restaurant_id = r.id
  selectedRestaurant.value = r
  restaurantError.value = false  // xóa lỗi khi đã chọn
}

// ── Fetch restaurants ─────────────────────────────────────────────
const fetchRestaurants = async (search = '') => {
  loadingRestaurants.value = true
  try {
    const params = {}
    if (search.trim()) params.search = search.trim()
    const res = await apiClient.get('/restaurants/', { params })
    restaurants.value = res.data
  } catch (err) {
    console.error('Failed to load restaurants:', err)
  } finally {
    loadingRestaurants.value = false
  }
}

const onRestaurantSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => fetchRestaurants(restaurantSearch.value), 400)
}

// ── Create booking ────────────────────────────────────────────────
const handleCreate = async () => {
  // Kiểm tra nhà hàng (không dùng được v-rules vì là list item)
  if (!form.value.restaurant_id) {
    restaurantError.value = true
    return
  }

  // Validate các field còn lại
  const { valid } = await formRef.value.validate()
  if (!valid) return

  loading.value = true
  errorMessage.value = ''
  try {
    await apiClient.post('/bookings/', {
      restaurant_id:    form.value.restaurant_id,
      booking_date:     form.value.booking_date,
      booking_time:     form.value.booking_time + ':00',
      number_of_guests: form.value.number_of_guests,
      special_notes:    form.value.special_notes || null,
    })
    showSnackbar('Booking created successfully!')
    setTimeout(() => router.push('/dashboard'), 1000)
  } catch (err) {
    const detail = err.response?.data?.detail
    errorMessage.value = typeof detail === 'string' ? detail : 'Failed to create booking. Please try again.'
  } finally {
    loading.value = false
  }
}

// ── Lifecycle ─────────────────────────────────────────────────────
onMounted(async () => {
  // Không cần check token — router guard đã lo
  await fetchRestaurants()
})
</script>

<style scoped>
.bg-background-light { background-color: #f8f7f6 !important; }
.text-brown { color: #9a6c4c !important; }
.border-subtle { border: 1px solid #e7d9cf !important; }
.tracking-tight { letter-spacing: -0.015em !important; }
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
.border-left-primary { border-left: 3px solid #ee7c2b !important; }
.shadow-orange { box-shadow: 0 4px 14px 0 rgba(238, 124, 43, 0.39) !important; }
</style>