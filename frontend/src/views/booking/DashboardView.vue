<template>
  <v-container fluid class="bg-background-light min-h-screen pa-6 pa-md-10">
    <v-row justify="center">
      <v-col cols="12" lg="10" xl="8">
        <header class="d-flex align-center justify-space-between mb-6 pb-4 border-b">
          <div class="d-flex align-center gap-4">
            <v-sheet width="48" height="48" color="orange-lighten-5" rounded="lg" class="d-flex align-center justify-center">
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
            size="large" rounded="lg" 
            class="text-none font-weight-bold d-none d-sm-flex" 
            style="margin-right: 45px;"
            @click="router.push('/bookings/new')"
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
                  <v-list-item prepend-icon="mdi-account-circle-outline" :title="userEmail" subtitle="Logged in" class="mb-2"></v-list-item>
                  <v-divider class="mb-2"></v-divider>
                  <v-list-item link prepend-icon="mdi-badge-account-outline" title="My Profile" @click="goToProfile"></v-list-item>
                  <v-list-item link prepend-icon="mdi-logout" title="Logout" color="error" @click="handleLogout"></v-list-item>
                </v-list>
              </v-card>
            </v-menu>
          </div>
        </header>

        <v-row class="mb-4 align-center">
          <v-col cols="12" md="6">
            <v-tabs v-model="activeTab" color="primary" align-tabs="start">
            <v-tab value="all" class="text-none font-weight-bold">
              All 
              <v-chip size="x-small" variant="tonal" class="ml-2">
                {{ bookings.length }}
              </v-chip>
            </v-tab>

            <v-tab value="pending" class="text-none font-weight-bold">
              Pending
              <v-chip size="x-small" color="warning" variant="flat" class="ml-2">
                {{ bookings.filter(b => b.status === 'pending').length }}
              </v-chip>
            </v-tab>

            <v-tab value="confirmed" class="text-none font-weight-bold">
              Confirmed
              <v-chip size="x-small" color="success" variant="flat" class="ml-2">
                {{ bookings.filter(b => b.status === 'confirmed').length }}
              </v-chip>
            </v-tab>

            <v-tab value="cancelled" class="text-none font-weight-bold">
              Cancelled
              <v-chip size="x-small" color="error" variant="flat" class="ml-2">
                {{ bookings.filter(b => b.status === 'cancelled').length }}
              </v-chip>
            </v-tab>
          </v-tabs>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="search" prepend-inner-icon="mdi-magnify" label="Search restaurant name..." variant="outlined" density="comfortable" rounded="lg" hide-details bg-color="white"></v-text-field>
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
              <tr v-for="booking in filteredBookings" :key="booking.id">
                <td class="font-weight-bold">{{ booking.restaurant_name }}</td>
                <td class="text-body-2 text-medium-emphasis">{{ booking.restaurant_address }}</td>
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
                    :color="getStatusColor(booking.status, `${booking.booking_date}T${booking.booking_time}`)"
                    size="small"
                    class="font-weight-bold text-uppercase"
                    label
                  >
                    {{ booking.status }}
                  </v-chip>
                </td>
                <td class="text-right">
                  <v-btn 
                  icon="mdi-pencil-outline" 
                  variant="text"
                   size="small" 
                   color="grey"
                   @click="router.push(`/bookings/edit/${booking.id}`)"
                  ></v-btn>
                  <v-btn icon="mdi-delete-outline" variant="text" size="small" color="red-lighten-1" @click="handleDelete(booking.id)"></v-btn>
                </td>
              </tr>
              <tr v-if="filteredBookings.length === 0">
                <td colspan="6" class="text-center py-4 text-grey">No bookings found.</td>
              </tr>
            </tbody>
          </v-table>
        </v-card>

        <div class="d-flex justify-space-between align-center mt-6">
          <p class="text-caption text-medium-emphasis">Showing {{ filteredBookings.length }} bookings</p>
          <v-pagination v-model="page" :length="3" density="comfortable" rounded="lg" active-color="primary"></v-pagination>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const userEmail = ref('');
const activeTab = ref('all');
const search = ref('');
const page = ref(1);

// 1. Khai báo stats và bookings (khởi tạo rỗng để chờ dữ liệu từ API)
const stats = ref({ total: 0, pending: 0, confirmed: 0, cancelled: 0, expired: 0 });
const bookings = ref([]);
// 2. Hàm định dạng màu sắc dựa trên trạng thái VÀ thời gian (Expired)
const getStatusColor = (status, bookingTime) => {
  // Logic: Nếu đang chờ nhưng giờ hiện tại đã vượt quá giờ đặt bàn
  if (status === 'pending' && new Date(bookingTime) < new Date()) {
    return 'grey'; // Hiển thị màu xám cho đơn quá hạn
  }
  
  switch (status) {
    case 'confirmed': return 'success';
    case 'pending': return 'warning';
    case 'cancelled': return 'error';
    default: return 'grey';
  }
};

// 3. Xử lý khi trang được load
onMounted(async () => {
  // Lấy token từ localStorage (phải khớp với key 'user_token' ở authService)
  const token = localStorage.getItem('user_token');
  userEmail.value = localStorage.getItem('user_email') || 'User';

  if (!token) {
    router.push('/login');
    return;
  }

  try {
    // GỌI API THỐNG KÊ (Hàm CASE WHEN ở Backend)
    const statsRes = await fetch('http://127.0.0.1:8000/api/v1/bookings/stats', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (statsRes.ok) {
      stats.value = await statsRes.json();
    }

    // GỌI API DANH SÁCH BOOKING THỰC TẾ
    const bookingsRes = await fetch('http://127.0.0.1:8000/api/v1/bookings/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (bookingsRes.ok) {
      bookings.value = await bookingsRes.json();
    }
  } catch (error) {
    console.error("Lỗi kết nối API:", error);
  }
});

// 4. Các hàm điều hướng
const handleLogout = () => {
  localStorage.removeItem('user_token');
  localStorage.removeItem('user_email');
  router.push('/login');
};

const goToProfile = () => {
  router.push('/profile');
};

const handleDelete = async (bookingId) => {
  // 1. Xác nhận với người dùng
  if (!confirm("Bạn có chắc chắn muốn xóa đơn đặt bàn này?")) return;

  try {
    const token = localStorage.getItem('user_token');
    
    // 2. Gọi API Delete đến Backend
    const response = await fetch(`http://127.0.0.1:8000/api/v1/bookings/${bookingId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      // 3. Nếu xóa thành công ở Backend, xóa dòng đó ở Frontend (Local State)
      bookings.value = bookings.value.filter(b => b.id !== bookingId);
      
      // Có thể thêm thông báo nhỏ (tùy chọn)
      console.log("Xóa thành công đơn hàng:", bookingId);
    } else {
      const errorData = await response.json();
      alert("Lỗi khi xóa: " + (errorData.detail || "Không rõ nguyên nhân"));
    }
  } catch (error) {
    console.error("Lỗi kết nối khi xóa:", error);
    alert("Không thể kết nối tới server.");
  }
};

// LOGIC LỌC DỮ LIỆU
const filteredBookings = computed(() => {
  return bookings.value.filter(booking => {
    // 1. Lọc theo trạng thái (Tab)
    // Lưu ý: booking.status phải khớp với các giá trị: 'pending', 'confirmed', 'cancelled'
    const statusMatch = activeTab.value === 'all' || 
                        booking.status.toLowerCase() === activeTab.value.toLowerCase();

    // 2. Lọc theo tên nhà hàng (Search)
    const searchMatch = booking.restaurant_name
      .toLowerCase()
      .includes(search.value.toLowerCase());

    return statusMatch && searchMatch;
  });
});
</script>

<style scoped>
.bg-background-light {
  background-color: #f8f7f6 !important;
}
.gap-4 { gap: 16px; }
.tracking-tight { letter-spacing: -0.015em !important; }
</style>