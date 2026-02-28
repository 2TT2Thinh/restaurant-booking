<template>
  <v-app class="bg-background-light">
    <v-app-bar flat border class="px-md-10 px-4" color="white">
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
      <v-btn variant="text" color="grey-darken-1" to="/login" class="text-none">Login</v-btn>
    </v-app-bar>

    <v-main class="d-flex align-center justify-center py-12">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6" lg="5">
            <v-card variant="flat" border class="pa-8 rounded-xl shadow-card">
              <div class="text-center mb-8">
                <h1 class="text-h4 font-weight-bold mb-2">Join Booking Tracker</h1>
                <p class="text-body-2 text-grey-darken-1">Manage your schedule effortlessly in one place.</p>
              </div>

              <v-alert
                v-if="errorMessage"
                type="error"
                variant="tonal"
                closable
                class="mb-6 rounded-lg"
              >
                {{ errorMessage }}
              </v-alert>

              <v-form @submit.prevent="handleRegister">
                <v-row dense>
                  <v-col cols="12">
                    <label class="text-subtitle-2 font-weight-bold mb-1 d-block">Full Name</label>
                    <v-text-field
                      v-model="form.full_name"
                      placeholder="e.g., John Doe"
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      color="primary"
                      required
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12">
                    <label class="text-subtitle-2 font-weight-bold mb-1 d-block">Email Address</label>
                    <v-text-field
                      v-model="form.email"
                      placeholder="name@example.com"
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      color="primary"
                      type="email"
                      required
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12">
                    <label class="text-subtitle-2 font-weight-bold mb-1 d-block">Phone Number</label>
                    <v-text-field
                      v-model="form.phone"
                      placeholder="+1 (555) 000-0000"
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      color="primary"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <label class="text-subtitle-2 font-weight-bold mb-1 d-block">Password</label>
                    <v-text-field
                      v-model="form.password"
                      :type="showPassword ? 'text' : 'password'"
                      placeholder="••••••••"
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      color="primary"
                      :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                      @click:append-inner="showPassword = !showPassword"
                      required
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <label class="text-subtitle-2 font-weight-bold mb-1 d-block">Confirm</label>
                    <v-text-field
                      v-model="form.confirmPassword"
                      type="password"
                      placeholder="••••••••"
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      color="primary"
                      :error="form.password !== form.confirmPassword && form.confirmPassword !== ''"
                      required
                    ></v-text-field>
                  </v-col>
                </v-row>

                <div class="d-flex align-center gap-2 mb-6">
                  <v-icon :color="passwordMatch ? 'success' : 'grey-lighten-1'" size="18">
                    {{ passwordMatch ? 'mdi-check-circle' : 'mdi-information-outline' }}
                  </v-icon>
                  <span class="text-caption" :class="passwordMatch ? 'text-success' : 'text-grey'">
                    {{ passwordMatch ? 'Passwords match' : 'Passwords must match' }}
                  </span>
                </div>

                <v-btn
                  block
                  color="primary"
                  size="x-large"
                  rounded="lg"
                  type="submit"
                  class="text-none font-weight-bold shadow-primary"
                  :loading="loading"
                >
                  Register Account
                </v-btn>

                <p class="text-center text-body-2 mt-6 text-grey-darken-1">
                  Already have an account? 
                  <router-link to="/login" class="text-primary font-weight-bold text-decoration-none">Log in</router-link>
                </p>
              </v-form>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '@/services/auth.service';

const router = useRouter();
const loading = ref(false);
const errorMessage = ref('');
const showPassword = ref(false);

const form = ref({
  full_name: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
});

const passwordMatch = computed(() => {
  return form.value.password.length > 0 && form.value.password === form.value.confirmPassword;
});

const handleRegister = async () => {
  if (!passwordMatch.value) {
    errorMessage.value = "Mật khẩu xác nhận không khớp!";
    return;
  }

  loading.value = true;
  errorMessage.value = '';

  try {
    await authService.register({
      full_name: form.value.full_name,
      email: form.value.email,
      phone: form.value.phone,
      password: form.value.password
    });

    alert("Đăng ký thành công! Hãy đăng nhập.");
    router.push('/login');
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "Đăng ký thất bại. Vui lòng thử lại!";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700&display=swap');

.v-application {
  font-family: 'Work Sans', sans-serif !important;
}

.bg-background-light {
  background-color: #f8f7f6 !important;
}

.shadow-card {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05) !important;
}

.shadow-primary {
  box-shadow: 0 4px 14px 0 rgba(238, 124, 43, 0.3) !important;
}

.gap-3 { gap: 12px; }
.gap-2 { gap: 8px; }

/* Custom lại border cho đẹp giống mẫu HTML */
:deep(.v-field__outline) {
  --v-field-border-opacity: 0.1;
}
</style>