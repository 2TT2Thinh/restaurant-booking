<template>
  <v-app class="bg-background-light">
    <v-app-bar flat border class="px-md-10 px-4" color="surface">
      <div class="d-flex align-center gap-3">
        <v-sheet
          width="32"
          height="32"
          color="primary"
          rounded="lg"
          class="d-flex align-center justify-center"
        >
          <v-icon color="white" size="20">mdi-calendar-check</v-icon>
        </v-sheet>
        <v-app-bar-title class="text-h6 font-weight-bold tracking-tight">
          Booking Tracker
        </v-app-bar-title>
      </div>
      <v-spacer></v-spacer>
      <v-btn
        variant="flat"
        color="grey-lighten-4"
        class="text-none font-weight-bold text-grey-darken-3"
        rounded="lg"
      >
        Help
      </v-btn>
    </v-app-bar>

    <v-main class="d-flex align-center justify-center bg-background-light">
      <v-container fluid>
        <v-row justify="center">
          <v-col cols="12" sm="8" md="4" lg="3" class="max-width-card">
            <v-card variant="outlined" class="pa-8 pa-md-10 border-thin login-card" rounded="xl">
              <div class="text-center mb-8">
                <v-avatar color="orange-lighten-5" size="64" class="mb-4">
                  <v-icon color="primary" size="36">mdi-lock-outline</v-icon>
                </v-avatar>
                <h1 class="text-h4 font-weight-bold mb-2">Welcome Back</h1>
                <p class="text-body-2 text-medium-emphasis">
                  Enter your credentials to access your bookings
                </p>
              </div>

              <v-alert
                v-if="errorMessage"
                type="error"
                variant="tonal"
                density="compact"
                class="mb-4 rounded-lg text-caption"
                closable
              >
                {{ errorMessage }}
              </v-alert>

              <v-form @submit.prevent="handleLogin">
                <label class="text-subtitle-2 font-weight-bold d-block mb-2">Email</label>
                <v-text-field
                  v-model="email"
                  placeholder="name@example.com"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-email-outline"
                  rounded="lg"
                  color="primary"
                  class="mb-2"
                  :disabled="loading"
                ></v-text-field>

                <div class="d-flex justify-space-between align-center mb-2">
                  <label class="text-subtitle-2 font-weight-bold">Password</label>
                  <a href="#" class="text-caption font-weight-bold text-primary text-decoration-none">
                    Forgot password?
                  </a>
                </div>
                <v-text-field
                  v-model="password"
                  placeholder="Enter your password"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-key-outline"
                  type="password"
                  rounded="lg"
                  color="primary"
                  :disabled="loading"
                ></v-text-field>

                <v-checkbox
                  v-model="rememberMe"
                  label="Keep me logged in"
                  color="primary"
                  hide-details
                  density="compact"
                  class="mt-1"
                ></v-checkbox>

                <v-btn
                  block
                  color="primary"
                  size="large"
                  rounded="lg"
                  elevation="2"
                  class="mt-6 text-none font-weight-bold shadow-primary"
                  type="submit"
                  :loading="loading"
                  :disabled="loading"
                >
                  Login
                </v-btn>
              </v-form>

              <div class="mt-8 pt-6 border-t text-center">
                <p class="text-body-2 text-medium-emphasis">
                  Don't have an account?
                  <a href="#" class="text-primary font-weight-bold text-decoration-none ml-1">
                    Register Now
                  </a>
                </p>
              </div>

              <div class="mt-6 d-flex align-center gap-4">
                <v-divider></v-divider>
                <span class="text-overline text-grey-lighten-1" style="white-space: nowrap">
                  Secure Entry
                </span>
                <v-divider></v-divider>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-footer app color="transparent" class="justify-center text-caption text-grey-darken-1 py-6">
      © 2026 Booking Tracker. All rights reserved. Secure encrypted connection.
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { authService } from '@/services/auth.service';
import { useRouter } from 'vue-router';

// Các biến lưu trạng thái
const email = ref('');
const password = ref('');
const rememberMe = ref(false);
const loading = ref(false);
const errorMessage = ref('');
const router = useRouter();

// Tự động điền email nếu trước đó có chọn "Keep me logged in"
onMounted(() => {
  const savedEmail = localStorage.getItem('remembered_email');
  if (savedEmail) {
    email.value = savedEmail;
    rememberMe.value = true;
  }
});

// Hàm xử lý đăng nhập
const handleLogin = async () => {
  if (!email.value || !password.value) {
    errorMessage.value = "Vui lòng nhập đầy đủ email và mật khẩu!";
    return;
  }

  loading.value = true;
  errorMessage.value = '';

  try {
    const response = await authService.login(email.value, password.value);
    
    // Ghi nhớ email nếu cần
    if (rememberMe.value) {
      localStorage.setItem('remembered_email', email.value);
    } else {
      localStorage.removeItem('remembered_email');
    }

    console.log('Đăng nhập thành công:', response);
    // Chuyển hướng người dùng vào trang Dashboard/Home
    router.push('/'); 
    
  } catch (error) {
    // Lấy thông báo lỗi từ Backend gửi về
    errorMessage.value = error.response?.data?.detail || "Email hoặc mật khẩu không chính xác!";
    console.error("Lỗi:", error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.bg-background-light {
  background-color: #f8f7f6 !important;
}

.login-card {
  background-color: #ffffff !important;
  border-color: #f3f4f6 !important;
}

.max-width-card {
  max-width: 440px !important;
}

.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

.shadow-primary {
  box-shadow: 0 4px 14px 0 rgba(238, 124, 43, 0.3) !important;
}

.tracking-tight {
  letter-spacing: -0.015em !important;
}

:deep(.v-field__outline) {
  --v-field-border-opacity: 0.12;
}

:deep(.v-label) {
  font-size: 0.875rem;
}
</style>