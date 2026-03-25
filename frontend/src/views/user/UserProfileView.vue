<template>
  <v-container fluid class="pa-0 bg-background-light min-h-screen">
    <v-row no-gutters>
      <v-col cols="12" class="pa-4 pa-md-8">
        <div class="max-w-5xl mx-auto">

          <div class="d-flex flex-column flex-md-row justify-space-between align-md-end mb-8 gap-4">
            <div>
              <h1 class="text-h3 font-weight-black tracking-tight mb-2 text-dark">User Profile</h1>
              <p class="text-subtitle-1 text-brown">Manage your identity and view your booking performance.</p>
            </div>
            <div class="d-flex gap-3">
              <v-btn prepend-icon="mdi-logout" variant="flat" color="grey-lighten-3" class="rounded-lg" height="44"
                @click="handleLogout">Sign Out</v-btn>
              <v-btn color="primary" variant="flat" class="rounded-lg shadow-btn" height="44"
                :loading="loading" @click="saveChanges">Save All Changes</v-btn>
            </div>
          </div>

          <v-row>
            <!-- LEFT: PERSONAL INFO + SECURITY -->
            <v-col cols="12" lg="8">
              <div class="d-flex flex-column gap-8">

                <!-- PERSONAL INFO -->
                <v-card variant="outlined" class="rounded-xl border-subtle bg-white pa-6 pa-md-8 shadow-sm">
                  <div class="d-flex align-center gap-6 mb-8">
                    <v-badge location="bottom right" offset-x="5" offset-y="5">
                      <template v-slot:badge>
                        <v-btn icon="mdi-camera" size="x-small" color="primary"></v-btn>
                      </template>
                      <v-avatar size="96" class="ring-avatar">
                        <v-img :src="'https://i.pravatar.cc/300'"></v-img>
                      </v-avatar>
                    </v-badge>
                    <div>
                      <h3 class="text-h6 font-weight-bold text-dark">Personal Information</h3>
                      <p class="text-caption text-brown">Member since {{ formatDate(user.joined_date) }}</p>
                    </div>
                  </div>

                  <v-alert v-if="profileError" type="error" variant="tonal" rounded="lg" class="mb-4" closable
                    @click:close="profileError = ''">
                    {{ profileError }}
                  </v-alert>

                  <v-form ref="profileFormRef">
                    <v-row>
                      <v-col cols="12" md="6">
                        <label class="text-sm font-weight-bold mb-1 d-block px-1">Full Name</label>
                        <v-text-field
                          v-model="user.full_name"
                          variant="solo-filled" flat rounded="lg" hide-details
                          bg-color="grey-lighten-4"
                          :rules="[rules.required]"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <label class="text-sm font-weight-bold mb-1 d-block px-1">Phone Number</label>
                        <v-text-field
                          v-model="user.phone"
                          variant="solo-filled" flat rounded="lg" hide-details
                          bg-color="grey-lighten-4"
                          :rules="[rules.phone]"
                          @keypress="allowOnlyDigits"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <div class="d-flex justify-space-between px-1 mb-1">
                          <label class="text-sm font-weight-bold">Email Address</label>
                          <span class="text-overline text-brown font-weight-black">Read Only</span>
                        </div>
                        <v-text-field
                          v-model="user.email"
                          variant="solo-filled" flat readonly rounded="lg"
                          append-inner-icon="mdi-lock" hide-details
                          bg-color="brown-lighten-5" class="readonly-field"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-form>
                </v-card>

                <!-- SECURITY -->
                <v-card variant="outlined" class="rounded-xl border-subtle bg-white pa-6 pa-md-8 shadow-sm">
                  <div class="d-flex align-center gap-3 mb-6">
                    <v-icon color="primary">mdi-shield-check</v-icon>
                    <h3 class="text-h6 font-weight-bold text-dark">Security Settings</h3>
                  </div>

                  <v-alert v-if="passwordError" type="error" variant="tonal" rounded="lg" class="mb-4" closable
                    @click:close="passwordError = ''">
                    {{ passwordError }}
                  </v-alert>

                  <v-form ref="passwordFormRef">
                    <v-row>
                      <v-col cols="12">
                        <label class="text-sm font-weight-bold mb-1 d-block px-1">Current Password</label>
                        <v-text-field
                          v-model="passwords.current"
                          type="password" variant="solo-filled" flat rounded="lg"
                          bg-color="grey-lighten-4" placeholder="Enter current password"
                          :rules="[rules.required]"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <label class="text-sm font-weight-bold mb-1 d-block px-1">New Password</label>
                        <v-text-field
                          v-model="passwords.new"
                          type="password" variant="solo-filled" flat rounded="lg"
                          bg-color="grey-lighten-4"
                          :rules="[rules.required, rules.minLength, rules.hasUppercase, rules.hasNumber, rules.hasSpecial]"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <label class="text-sm font-weight-bold mb-1 d-block px-1">Confirm New Password</label>
                        <v-text-field
                          v-model="passwords.confirm"
                          type="password" variant="solo-filled" flat rounded="lg"
                          bg-color="grey-lighten-4"
                          :rules="[rules.required, rules.confirmMatch]"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-form>

                  <div class="mt-6 d-flex justify-end">
                    <v-btn color="primary" variant="tonal" rounded="lg"
                      class="text-none font-weight-bold px-6" :loading="passwordLoading"
                      @click="updatePassword">
                      Update Password
                    </v-btn>
                  </div>
                </v-card>

              </div>
            </v-col>

            <!-- RIGHT: STATS -->
            <v-col cols="12" lg="4">
              <v-card variant="outlined" class="rounded-xl border-subtle bg-white pa-6 shadow-sm">
                <h4 class="text-overline font-weight-black text-brown mb-6">Booking Stats</h4>
                <div class="d-flex flex-column gap-4">

                  <div class="d-flex align-center justify-space-between pa-4 rounded-xl bg-stat-primary">
                    <div class="d-flex align-center gap-3">
                      <v-avatar color="primary" size="40" rounded="lg">
                        <v-icon color="white">mdi-calendar-check</v-icon>
                      </v-avatar>
                      <span class="text-sm font-weight-bold">Total Bookings</span>
                    </div>
                    <span class="text-h5 font-weight-black text-primary">{{ stats.total }}</span>
                  </div>

                  <div class="d-flex align-center justify-space-between pa-4 rounded-xl bg-stat-green">
                    <div class="d-flex align-center gap-3">
                      <v-avatar color="green" size="40" rounded="lg">
                        <v-icon color="white">mdi-check-decagram</v-icon>
                      </v-avatar>
                      <span class="text-sm font-weight-bold">Confirmed</span>
                    </div>
                    <span class="text-h5 font-weight-black text-green">{{ stats.confirmed }}</span>
                  </div>

                  <div class="d-flex align-center justify-space-between pa-4 rounded-xl bg-stat-orange">
                    <div class="d-flex align-center gap-3">
                      <v-avatar color="orange" size="40" rounded="lg">
                        <v-icon color="white">mdi-clock-outline</v-icon>
                      </v-avatar>
                      <span class="text-sm font-weight-bold">Pending</span>
                    </div>
                    <span class="text-h5 font-weight-black text-orange">{{ stats.pending }}</span>
                  </div>

                  <div class="d-flex align-center justify-space-between pa-4 rounded-xl bg-stat-red">
                    <div class="d-flex align-center gap-3">
                      <v-avatar color="red" size="40" rounded="lg">
                        <v-icon color="white">mdi-close-circle</v-icon>
                      </v-avatar>
                      <span class="text-sm font-weight-bold">Cancelled</span>
                    </div>
                    <span class="text-h5 font-weight-black text-red">{{ stats.cancelled }}</span>
                  </div>

                  <div class="d-flex align-center justify-space-between pa-4 rounded-xl bg-stat-grey">
                    <div class="d-flex align-center gap-3">
                      <v-avatar color="grey" size="40" rounded="lg">
                        <v-icon color="white">mdi-calendar-remove</v-icon>
                      </v-avatar>
                      <span class="text-sm font-weight-bold">Expired</span>
                    </div>
                    <span class="text-h5 font-weight-black text-grey">{{ stats.expired }}</span>
                  </div>

                </div>
                <v-divider class="my-6 border-subtle"></v-divider>
                <p class="text-caption text-brown text-center italic">Stats updated today</p>
              </v-card>
            </v-col>
          </v-row>
        </div>
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api/axios'

const router    = useRouter()
const authStore = useAuthStore()

const profileFormRef  = ref(null)
const passwordFormRef = ref(null)
const loading         = ref(false)
const passwordLoading = ref(false)
const profileError    = ref('')
const passwordError   = ref('')
const snackbar        = ref({ show: false, message: '', color: 'success' })

// Lấy dữ liệu từ Store — không cần gọi API lại
const user = ref({
  full_name:   authStore.user?.full_name  || '',
  phone:       authStore.user?.phone      || '',
  email:       authStore.user?.email      || '',
  joined_date: authStore.user?.created_at || '',
})

const stats = ref({ total: 0, confirmed: 0, cancelled: 0, pending: 0, expired: 0 })
const passwords = ref({ current: '', new: '', confirm: '' })

// ── Validation rules ──────────────────────────────────────────────
const rules = {
  required:    (v) => !!v?.trim()                             || 'This field is required.',
  phone:       (v) => !v || /^\d{10}$/.test(v)               || 'Phone must be exactly 10 digits.',
  minLength:   (v) => v?.length >= 8                          || 'At least 8 characters.',
  hasUppercase:(v) => /[A-Z]/.test(v)                         || 'At least one uppercase letter.',
  hasNumber:   (v) => /[0-9]/.test(v)                         || 'At least one number.',
  hasSpecial:  (v) => /[!@#$%^&*(),.?":{}|<>]/.test(v)       || 'At least one special character.',
  confirmMatch:(v) => v === passwords.value.new               || 'Passwords do not match.',
}

// Phone chỉ cho nhập số
const allowOnlyDigits = (e) => {
  if (!/[0-9]/.test(e.key)) e.preventDefault()
}

// ── Helpers ───────────────────────────────────────────────────────
const showSnackbar = (message, color = 'success') => {
  snackbar.value = { show: true, message, color }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '...'
  return new Date(dateStr).toLocaleDateString('en-GB', { month: 'long', year: 'numeric' })
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// ── Fetch stats ───────────────────────────────────────────────────
const fetchStats = async () => {
  try {
    const res = await apiClient.get('/users/me/stats')
    stats.value = {
      total:     res.data.total     || 0,
      confirmed: res.data.confirmed || 0,
      cancelled: res.data.cancelled || 0,
      pending:   res.data.pending   || 0,
      expired:   res.data.expired   || 0,
    }
  } catch (err) {
    console.error('Stats error:', err)
  }
}

// ── Save profile ──────────────────────────────────────────────────
const saveChanges = async () => {
  const { valid } = await profileFormRef.value.validate()
  if (!valid) return

  loading.value = true
  profileError.value = ''
  try {
    await apiClient.patch('/users/me', {
      full_name: user.value.full_name.trim(),
      phone:     user.value.phone.trim(),
    })

    // Sync lại Store để navbar và các nơi khác cập nhật tên mới
    await authStore.fetchUser()

    showSnackbar('Profile updated successfully.')
  } catch (err) {
    profileError.value = err.response?.data?.detail || 'Failed to update profile.'
  } finally {
    loading.value = false
  }
}

// ── Change password ───────────────────────────────────────────────
const updatePassword = async () => {
  const { valid } = await passwordFormRef.value.validate()
  if (!valid) return

  passwordLoading.value = true
  passwordError.value = ''
  try {
    await apiClient.post('/users/me/change-password', {
      current_password: passwords.value.current,
      new_password:     passwords.value.new,
    })
    showSnackbar('Password updated successfully.')
    passwords.value = { current: '', new: '', confirm: '' }
    passwordFormRef.value.reset()
  } catch (err) {
    const msg = err.response?.data?.detail
    passwordError.value = typeof msg === 'string' ? msg : 'Incorrect current password.'
  } finally {
    passwordLoading.value = false
  }
}

// ── Lifecycle ─────────────────────────────────────────────────────
onMounted(async () => {
  // Không cần fetch /users/me lại — Store đã có
  // Chỉ fetch stats
  await fetchStats()
})
</script>

<style scoped>
.bg-background-light { background-color: #f8f7f6 !important; }
.text-dark   { color: #1b130d !important; }
.text-brown  { color: #9a6c4c !important; }
.text-orange { color: #FB8C00 !important; }
.border-subtle { border-color: #f3ece7 !important; }
.gap-3 { gap: 12px; } .gap-4 { gap: 16px; } .gap-6 { gap: 24px; } .gap-8 { gap: 32px; }
.bg-stat-primary { background-color: rgba(238, 124, 43, 0.08); }
.bg-stat-green   { background-color: rgba(76, 175, 80, 0.08); }
.bg-stat-orange  { background-color: rgba(251, 140, 0, 0.08); }
.bg-stat-red     { background-color: rgba(244, 67, 54, 0.08); }
.bg-stat-grey    { background-color: rgba(158, 158, 158, 0.08); }
.ring-avatar { border: 4px solid rgba(238, 124, 43, 0.1); }
.readonly-field :deep(input) { color: #9a6c4c !important; cursor: not-allowed !important; }
.shadow-btn  { box-shadow: 0 4px 14px 0 rgba(238, 124, 43, 0.39) !important; }
.shadow-sm   { box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important; }
</style>