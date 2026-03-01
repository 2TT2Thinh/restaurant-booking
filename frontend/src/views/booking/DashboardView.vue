<template>
  <v-container fluid class="bg-background-light min-h-screen pa-6 pa-md-10">
    <v-row justify="center">
      <v-col cols="12" lg="10" xl="8">
        <header class="d-flex align-center justify-space-between mb-6 pb-4 border-b">
  <div class="d-flex align-center gap-4">
    <v-sheet
      width="48"
      height="48"
      color="orange-lighten-5"
      rounded="lg"
      class="d-flex align-center justify-center"
    >
      <v-icon color="primary" size="28">mdi-calendar-check</v-icon>
    </v-sheet>
    <div>
      <h1 class="text-h4 font-weight-bold tracking-tight">My Bookings</h1>
      <p class="text-body-2 text-medium-emphasis">
        Welcome back, <span class="font-weight-bold text-primary">{{ userEmail }}</span>
      </p>
    </div>
  </div>

  <div class="d-flex align-center gap-3">
    <v-btn
      color="primary"
      prepend-icon="mdi-plus"
      size="large"
      rounded="lg"
      class="text-none font-weight-bold d-none d-sm-flex"
      style="margin-right: 45px;"
    >
      Create New
    </v-btn>
    
    <v-btn color="primary" icon="mdi-plus" size="small" class="d-flex d-sm-none" rounded="lg"></v-btn>

    <v-menu min-width="220px" rounded="xl" transition="slide-y-transition">
      <template v-slot:activator="{ props }">
        <v-btn icon v-bind="props" variant="text">
          <v-avatar color="primary" size="44" class="elevation-2">
            <span class="text-white text-h6 font-weight-bold">
              {{ userEmail ? userEmail.charAt(0).toUpperCase() : 'U' }}
            </span>
          </v-avatar>
        </v-btn>
      </template>

      <v-card class="mt-2">
        <v-list class="pa-2">
          <v-list-item
            prepend-icon="mdi-account-circle-outline"
            :title="userEmail"
            subtitle="Logged in"
            class="mb-2"
          >
          </v-list-item>

          <v-divider class="mb-2"></v-divider>

          <v-list-item 
            link 
            prepend-icon="mdi-badge-account-outline" 
            title="My Profile"
            @click="console.log('Profile clicked')"
          ></v-list-item>

          <v-list-item 
            link 
            prepend-icon="mdi-logout" 
            title="Logout" 
            color="error"
            @click="handleLogout"
          ></v-list-item>
        </v-list>
      </v-card>
    </v-menu>
  </div>
</header>

        <v-row class="mb-4 align-center">
          <v-col cols="12" md="6">
            <v-tabs v-model="activeTab" color="primary" align-tabs="start">
              <v-tab value="all" class="text-none font-weight-bold">All</v-tab>
              <v-tab value="pending" class="text-none font-weight-bold">Pending</v-tab>
              <v-tab value="confirmed" class="text-none font-weight-bold">Confirmed</v-tab>
              <v-tab value="cancelled" class="text-none font-weight-bold">Cancelled</v-tab>
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
            ></v-text-field>
          </v-col>
        </v-row>

        <v-card variant="outlined" rounded="xl" class="border-thin overflow-hidden">
          <v-table>
            <thead class="bg-grey-lighten-5">
              <tr>
                <th class="text-uppercase text-caption font-weight-bold">Restaurant Name</th>
                <th class="text-uppercase text-caption font-weight-bold">Address</th>
                <th class="text-uppercase text-caption font-weight-bold">Date / Time</th>
                <th class="text-uppercase text-caption font-weight-bold">Guests</th>
                <th class="text-uppercase text-caption font-weight-bold">Status</th>
                <th class="text-uppercase text-caption font-weight-bold text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="booking in bookings" :key="booking.id">
                <td class="font-weight-bold">{{ booking.name }}</td>
                <td class="text-body-2 text-medium-emphasis">{{ booking.address }}</td>
                <td>
                  <div class="text-body-2">{{ booking.date }}</div>
                  <div class="text-caption text-grey">{{ booking.time }}</div>
                </td>
                <td>
                  <v-chip size="small" variant="text" prepend-icon="mdi-account-group">
                    {{ booking.guests }}
                  </v-chip>
                </td>
                <td>
                  <v-chip
                    :color="getStatusColor(booking.status)"
                    size="small"
                    class="font-weight-bold text-uppercase"
                    label
                  >
                    {{ booking.status }}
                  </v-chip>
                </td>
                <td class="text-right">
                  <v-btn icon="mdi-pencil-outline" variant="text" size="small" color="grey"></v-btn>
                  <v-btn icon="mdi-delete-outline" variant="text" size="small" color="red-lighten-1"></v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>

        <div class="d-flex justify-space-between align-center mt-6">
          <p class="text-caption text-medium-emphasis">Showing {{ bookings.length }} bookings</p>
          <v-pagination v-model="page" :length="3" density="comfortable" rounded="lg" active-color="primary"></v-pagination>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const userEmail = ref('');
const activeTab = ref('all');
const search = ref('');
const page = ref(1);

// Dữ liệu mẫu (sau này sẽ gọi API lấy từ Backend)
const bookings = ref([
  { id: 1, name: 'The Golden Grill', address: '123 Maple St, Downtown', date: 'Oct 24, 2026', time: '7:00 PM', guests: 4, status: 'confirmed' },
  { id: 2, name: 'Ocean Breeze', address: '456 Harbor Pier', date: 'Oct 26, 2026', time: '6:30 PM', guests: 2, status: 'pending' },
  { id: 3, name: 'Urban Bites', address: '789 City Plaza', date: 'Oct 20, 2026', time: '8:00 PM', guests: 3, status: 'cancelled' }
]);

const getStatusColor = (status) => {
  switch (status) {
    case 'confirmed': return 'success';
    case 'pending': return 'warning';
    case 'cancelled': return 'error';
    default: return 'grey';
  }
};

onMounted(() => {
  // LẤY DỮ LIỆU ĐĂNG NHẬP TỪ LOCAL STORAGE
  const token = localStorage.getItem('user_token');
  
  if (!token) {
    // Nếu chưa đăng nhập, đá về trang login ngay
    router.push('/login');
    return;
  }

  // Tạm thời lấy email từ một cái key khác hoặc giải mã JWT
  // Nếu bạn có lưu thông tin user khi login, hãy lấy nó ra ở đây
  userEmail.value = localStorage.getItem('user_email') || 'User';
});
const handleLogout = () => {
  // 1. Xóa sạch kho lưu trữ
  localStorage.removeItem('user_token');
  localStorage.removeItem('user_email');
  
  // 2. Thông báo (tùy chọn)
  alert("Bạn đã đăng xuất thành công!");
  
  // 3. Chuyển hướng về trang Login
  router.push('/login');
};

const goToProfile = () => {
  // Sau này bạn làm trang Profile thì điền vào đây
  console.log("Đi tới trang cá nhân");
};
</script>

<style scoped>
.bg-background-light {
  background-color: #f8f7f6 !important;
}
.gap-4 { gap: 16px; }
.tracking-tight { letter-spacing: -0.015em !important; }
</style>