<template>
  <v-app class="bg-background-light">

    <!-- NAVBAR -->
    <v-app-bar flat border class="px-md-10 px-4" color="white">
      <div class="d-flex align-center gap-3">
        <v-sheet width="32" height="32" color="primary" rounded="lg" class="d-flex align-center justify-center">
          <v-icon color="white" size="20">mdi-calendar-check</v-icon>
        </v-sheet>
        <v-app-bar-title class="text-h6 font-weight-bold tracking-tight">
          Booking Tracker
        </v-app-bar-title>
      </div>
      <v-spacer></v-spacer>
      <v-btn variant="text" class="text-none font-weight-bold mr-2" to="/login">Login</v-btn>
      <v-btn color="primary" variant="flat" rounded="lg" class="text-none font-weight-bold" to="/register">
        Get Started
      </v-btn>
    </v-app-bar>

    <v-main>

      <!-- HERO SECTION -->
      <v-container fluid class="pa-0">
        <v-row no-gutters justify="center" align="center"
          style="min-height: 88vh; background: linear-gradient(135deg, #fff8f4 0%, #fff3eb 50%, #f8f7f6 100%);">
          <v-col cols="12" md="8" lg="6" class="text-center px-6 py-16">

            <v-chip color="primary" variant="tonal" size="small" class="mb-6 font-weight-bold">
              <v-icon start size="14">mdi-star</v-icon>
              Restaurant Booking System
            </v-chip>

            <h1 class="text-h2 text-md-h1 font-weight-black tracking-tight mb-6 text-dark" style="line-height: 1.1;">
              Đặt bàn dễ dàng,<br>
              <span class="text-primary">không lo quên chỗ</span>
            </h1>

            <p class="text-body-1 text-medium-emphasis mb-10 mx-auto" style="max-width: 480px; line-height: 1.7;">
              Quản lý toàn bộ lịch đặt bàn nhà hàng của bạn tại một nơi.
              Tạo, theo dõi và cập nhật đơn đặt bàn chỉ trong vài giây.
            </p>

            <div class="d-flex justify-center gap-4 flex-wrap">
              <v-btn color="primary" size="x-large" rounded="lg"
                class="text-none font-weight-bold shadow-primary px-8" to="/register">
                <v-icon start>mdi-rocket-launch-outline</v-icon>
                Bắt đầu miễn phí
              </v-btn>
              <v-btn variant="outlined" color="grey-darken-2" size="x-large" rounded="lg"
                class="text-none font-weight-bold px-8" to="/login">
                Đăng nhập
              </v-btn>
            </div>

            <!-- STATS ROW -->
            <v-row justify="center" class="mt-16">
              <v-col cols="4" sm="3" v-for="stat in heroStats" :key="stat.label">
                <div class="text-h4 font-weight-black text-primary">{{ stat.value }}</div>
                <div class="text-caption text-medium-emphasis font-weight-bold mt-1">{{ stat.label }}</div>
              </v-col>
            </v-row>

          </v-col>
        </v-row>
      </v-container>

      <!-- FEATURES SECTION -->
      <v-container class="py-16">
        <div class="text-center mb-12">
          <h2 class="text-h4 font-weight-black text-dark mb-3">Tại sao chọn Booking Tracker?</h2>
          <p class="text-body-1 text-medium-emphasis">Mọi thứ bạn cần để quản lý đặt bàn hiệu quả</p>
        </div>

        <v-row justify="center">
          <v-col cols="12" sm="6" md="4" v-for="feature in features" :key="feature.title">
            <v-card variant="outlined" rounded="xl" class="pa-6 border-subtle bg-white h-100 text-center">
              <v-avatar :color="feature.color + '-lighten-5'" size="64" rounded="lg" class="mb-4">
                <v-icon :color="feature.color" size="32">{{ feature.icon }}</v-icon>
              </v-avatar>
              <h3 class="text-h6 font-weight-bold text-dark mb-2">{{ feature.title }}</h3>
              <p class="text-body-2 text-medium-emphasis">{{ feature.desc }}</p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <!-- HOW IT WORKS -->
      <v-container fluid class="py-16" style="background-color: #fff8f4;">
        <v-container>
          <div class="text-center mb-12">
            <h2 class="text-h4 font-weight-black text-dark mb-3">Chỉ 3 bước đơn giản</h2>
            <p class="text-body-1 text-medium-emphasis">Bắt đầu quản lý đặt bàn ngay hôm nay</p>
          </div>
          <v-row justify="center">
            <v-col cols="12" sm="4" v-for="(step, i) in steps" :key="i" class="text-center">
              <v-avatar color="primary" size="56" class="mb-4 elevation-2">
                <span class="text-h6 font-weight-black text-white">{{ i + 1 }}</span>
              </v-avatar>
              <h3 class="text-h6 font-weight-bold text-dark mb-2">{{ step.title }}</h3>
              <p class="text-body-2 text-medium-emphasis">{{ step.desc }}</p>
            </v-col>
          </v-row>
        </v-container>
      </v-container>

      <!-- CTA SECTION -->
      <v-container class="py-16 text-center">
        <v-sheet color="primary" rounded="xl" class="pa-12 shadow-primary mx-auto" style="max-width: 640px;">
          <v-icon color="white" size="48" class="mb-4">mdi-calendar-heart</v-icon>
          <h2 class="text-h4 font-weight-black text-white mb-3">Sẵn sàng bắt đầu?</h2>
          <p class="text-body-1 text-white mb-8" style="opacity: 0.85;">
            Tạo tài khoản miễn phí và đặt bàn đầu tiên của bạn ngay hôm nay.
          </p>
          <v-btn color="white" size="x-large" rounded="lg" class="text-none font-weight-bold text-primary px-10" to="/register">
            Đăng ký ngay
          </v-btn>
        </v-sheet>
      </v-container>

      <!-- FOOTER -->
      <v-footer color="white" border class="justify-center text-caption text-grey py-6">
        © 2025 Booking Tracker. All rights reserved.
      </v-footer>

    </v-main>
  </v-app>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Nếu đã login thì vào Dashboard luôn
onMounted(() => {
  if (localStorage.getItem('user_token')) {
    router.push('/dashboard')
  }
})

const heroStats = [
  { value: '500+', label: 'Nhà hàng' },
  { value: '10K+', label: 'Đơn đặt bàn' },
  { value: '99%',  label: 'Hài lòng' },
]

const features = [
  {
    icon: 'mdi-calendar-check',
    color: 'primary',
    title: 'Đặt bàn nhanh chóng',
    desc: 'Chọn nhà hàng, ngày giờ và số khách chỉ trong vài giây. Giao diện đơn giản, dễ dùng.'
  },
  {
    icon: 'mdi-view-dashboard-outline',
    color: 'blue',
    title: 'Dashboard trực quan',
    desc: 'Xem toàn bộ lịch đặt bàn, lọc theo trạng thái và tìm kiếm dễ dàng.'
  },
  {
    icon: 'mdi-bell-outline',
    color: 'green',
    title: 'Theo dõi trạng thái',
    desc: 'Biết ngay đơn nào đang pending, confirmed hay cancelled. Không bao giờ bỏ lỡ.'
  },
  {
    icon: 'mdi-shield-check-outline',
    color: 'orange',
    title: 'Bảo mật tài khoản',
    desc: 'Xác thực JWT, mã hóa mật khẩu. Thông tin của bạn luôn được bảo vệ.'
  },
  {
    icon: 'mdi-pencil-outline',
    color: 'purple',
    title: 'Chỉnh sửa linh hoạt',
    desc: 'Cập nhật hoặc hủy đơn đặt bàn bất cứ lúc nào trước giờ đến.'
  },
  {
    icon: 'mdi-chart-bar',
    color: 'teal',
    title: 'Thống kê chi tiết',
    desc: 'Xem tổng số booking, đã xác nhận, đã hủy và hết hạn trên trang profile.'
  },
]

const steps = [
  {
    title: 'Tạo tài khoản',
    desc: 'Đăng ký miễn phí với email và mật khẩu. Chỉ mất 30 giây.'
  },
  {
    title: 'Chọn nhà hàng',
    desc: 'Duyệt danh sách nhà hàng và chọn nơi bạn muốn đến.'
  },
  {
    title: 'Xác nhận đặt bàn',
    desc: 'Điền ngày giờ, số khách và ghi chú đặc biệt nếu cần.'
  },
]
</script>

<style scoped>
.bg-background-light { background-color: #f8f7f6 !important; }
.text-dark { color: #1b130d !important; }
.tracking-tight { letter-spacing: -0.02em !important; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
.border-subtle { border: 1px solid #f3ece7 !important; }
.shadow-primary { box-shadow: 0 8px 32px 0 rgba(238, 124, 43, 0.25) !important; }
.h-100 { height: 100%; }
</style>