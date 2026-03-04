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
              <v-btn prepend-icon="mdi-logout" variant="flat" color="grey-lighten-3" class="rounded-lg" height="44" @click="handleLogout">Sign Out</v-btn>
              <v-btn color="primary" variant="flat" class="rounded-lg shadow-btn" height="44" :loading="loading" @click="saveChanges">Save All Changes</v-btn>
            </div>
          </div>

          <v-row>
            <v-col cols="12" lg="8">
              <div class="d-flex flex-column gap-8">
                <v-card variant="outlined" class="rounded-xl border-subtle bg-white pa-6 pa-md-8 shadow-sm">
                  <div class="d-flex align-center gap-6 mb-8">
                    <v-badge location="bottom right" offset-x="5" offset-y="5">
                      <template v-slot:badge><v-btn icon="mdi-camera" size="x-small" color="primary"></v-btn></template>
                      <v-avatar size="96" class="ring-avatar">
                        <v-img :src="user.avatar || 'https://i.pravatar.cc/300'"></v-img>
                      </v-avatar>
                    </v-badge>
                    <div>
                      <h3 class="text-h6 font-weight-bold text-dark">Personal Information</h3>
                      <p class="text-caption text-brown">Member since {{ formatDate(user.joined_date) }}</p>
                    </div>
                  </div>

                  <v-form>
                    <v-row>
                      <v-col cols="12" md="6">
                        <label class="text-sm font-weight-bold mb-1 d-block px-1">Full Name</label>
                        <v-text-field v-model="user.full_name" variant="solo-filled" flat rounded="lg" hide-details bg-color="grey-lighten-4"></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <label class="text-sm font-weight-bold mb-1 d-block px-1">Phone Number</label>
                        <v-text-field v-model="user.phone" variant="solo-filled" flat rounded="lg" hide-details bg-color="grey-lighten-4"></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <div class="d-flex justify-space-between px-1 mb-1">
                          <label class="text-sm font-weight-bold">Email Address</label>
                          <span class="text-overline text-brown font-weight-black">Read Only</span>
                        </div>
                        <v-text-field v-model="user.email" variant="solo-filled" flat readonly rounded="lg" append-inner-icon="mdi-lock" hide-details bg-color="brown-lighten-5" class="readonly-field"></v-text-field>
                      </v-col>
                    </v-row>
                  </v-form>
                </v-card>

               <v-card variant="outlined" class="rounded-xl border-subtle bg-white pa-6 pa-md-8 shadow-sm">
  <div class="d-flex align-center gap-3 mb-6">
    <v-icon color="primary">mdi-shield-check</v-icon>
    <h3 class="text-h6 font-weight-bold text-dark">Security Settings</h3>
  </div>
  <v-row>
    <v-col cols="12">
      <label class="text-sm font-weight-bold mb-1 d-block px-1">Current Password</label>
      <v-text-field v-model="passwords.current" type="password" variant="solo-filled" flat rounded="lg" hide-details bg-color="grey-lighten-4" placeholder="Enter current password"></v-text-field>
    </v-col>
    
    <v-col cols="12" md="6">
      <label class="text-sm font-weight-bold mb-1 d-block px-1">New Password</label>
      <v-text-field v-model="passwords.new" type="password" variant="solo-filled" flat rounded="lg" hide-details bg-color="grey-lighten-4"></v-text-field>
    </v-col>
    <v-col cols="12" md="6">
      <label class="text-sm font-weight-bold mb-1 d-block px-1">Confirm New Password</label>
      <v-text-field v-model="passwords.confirm" type="password" variant="solo-filled" flat rounded="lg" hide-details bg-color="grey-lighten-4"></v-text-field>
    </v-col>
  </v-row>
  <div class="mt-6 d-flex justify-end">
    <v-btn color="primary" variant="tonal" rounded="lg" class="text-none font-weight-bold px-6" @click="updatePassword">Update Password</v-btn>
  </div>
</v-card>
              </div>
            </v-col>

            <v-col cols="12" lg="4">
              <v-card variant="outlined" class="rounded-xl border-subtle bg-white pa-6 shadow-sm">
                <h4 class="text-overline font-weight-black text-brown mb-6">Booking Stats</h4>
                <div class="d-flex flex-column gap-4">
                  <div class="d-flex align-center justify-space-between pa-4 rounded-xl bg-stat-primary">
                    <div class="d-flex align-center gap-3">
                      <v-avatar color="primary" size="40" rounded="lg"><v-icon color="white">mdi-calendar-check</v-icon></v-avatar>
                      <span class="text-sm font-weight-bold">Total Bookings</span>
                    </div>
                    <span class="text-h5 font-weight-black text-primary">{{ stats.total }}</span>
                  </div>
                  <div class="d-flex align-center justify-space-between pa-4 rounded-xl bg-stat-green">
                    <div class="d-flex align-center gap-3">
                      <v-avatar color="green" size="40" rounded="lg"><v-icon color="white">mdi-check-decagram</v-icon></v-avatar>
                      <span class="text-sm font-weight-bold">Confirmed</span>
                    </div>
                    <span class="text-h5 font-weight-black text-green">{{ stats.confirmed }}</span>
                  </div>
                  <div class="d-flex align-center justify-space-between pa-4 rounded-xl bg-stat-red">
                    <div class="d-flex align-center gap-3">
                      <v-avatar color="red" size="40" rounded="lg"><v-icon color="white">mdi-close-circle</v-icon></v-avatar>
                      <span class="text-sm font-weight-bold">Cancelled</span>
                    </div>
                    <span class="text-h5 font-weight-black text-red">{{ stats.cancelled }}</span>
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
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)

const user = ref({ full_name: '', phone: '', email: '', avatar: '', joined_date: '' })
const stats = ref({ total: 0, confirmed: 0, cancelled: 0 })

// 1. Thêm trường current vào ref
const passwords = ref({ current: '', new: '', confirm: '' })
const api = axios.create({ baseURL: 'http://127.0.0.1:8000/api/v1' })

api.interceptors.request.use(config => {
  const token = localStorage.getItem('user_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

const fetchProfile = async () => {
  try {
    const res = await api.get('/users/me')
    user.value = {
      full_name: res.data.full_name,
      phone: res.data.phone,
      email: res.data.email,
      joined_date: res.data.created_at
    }
    fetchStats()
  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
  }
}

const fetchStats = async () => {
  try {
    const res = await api.get('/users/me/stats')
    // Khớp với return của hàm Backend bạn vừa đưa
    stats.value = {
      total: res.data.total,
      confirmed: res.data.confirmed,
      cancelled: res.data.cancelled
    }
  } catch (err) {
    console.error("Stats fail:", err)
  }
}

const saveChanges = async () => {
  loading.value = true
  try {
    await api.patch('/users/me', {
      full_name: user.value.full_name,
      phone: user.value.phone
    })
    alert('Profile updated!')
  } catch (err) {
    alert('Update error')
  } finally { loading.value = false }
}



// 2. Sửa lại hàm gọi API
const updatePassword = async () => {
  // Kiểm tra đầu vào
  if (!passwords.value.current) return alert('Vui lòng nhập mật khẩu hiện tại')
  if (!passwords.value.new) return alert('Vui lòng nhập mật khẩu mới')
  if (passwords.value.new !== passwords.value.confirm) {
    return alert('Mật khẩu mới không khớp')
  }

  try {
    await api.post('/users/me/change-password', { 
      current_password: passwords.value.current, // Gửi đúng tên field Schema yêu cầu
      new_password: passwords.value.new 
    })
    alert('Đổi mật khẩu thành công!')
    // Reset form
    passwords.value = { current: '', new: '', confirm: '' }
  } catch (err) {
    // Nếu vẫn lỗi, in ra để debug
    console.error("Dữ liệu gửi đi:", { 
      current_password: passwords.value.current, 
      new_password: passwords.value.new 
    })
    const errorMsg = err.response?.data?.detail?.[0]?.msg || 'Mật khẩu cũ không chính xác hoặc lỗi định dạng'
    alert('Lỗi: ' + errorMsg)
  }
}
const handleLogout = () => {
  localStorage.removeItem('user_token')
  router.push('/login')
}

const formatDate = (dateStr) => {
  if (!dateStr) return '...'
  return new Date(dateStr).toLocaleDateString('vi-VN', { month: 'long', year: 'numeric' })
}

onMounted(fetchProfile)
</script>

<style scoped>
/* GIỮ NGUYÊN CSS GỐC CỦA BẠN */
.bg-background-light { background-color: #f8f7f6 !important; }
.text-dark { color: #1b130d !important; }
.text-brown { color: #9a6c4c !important; }
.border-subtle { border-color: #f3ece7 !important; }
.gap-3 { gap: 12px; } .gap-4 { gap: 16px; } .gap-6 { gap: 24px; } .gap-8 { gap: 32px; }
.bg-stat-primary { background-color: rgba(238, 124, 43, 0.08); }
.bg-stat-green { background-color: rgba(76, 175, 80, 0.08); }
.bg-stat-red { background-color: rgba(244, 67, 54, 0.08); }
.ring-avatar { border: 4px solid rgba(238, 124, 43, 0.1); }
.readonly-field :deep(input) { color: #9a6c4c !important; cursor: not-allowed !important; }
.shadow-btn { box-shadow: 0 4px 14px 0 rgba(238, 124, 43, 0.39) !important; }
</style>