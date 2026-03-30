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
                @click:close="errorMessage = ''"
              >
                {{ errorMessage }}
              </v-alert>

              <v-alert
                v-if="successMessage"
                type="success"
                variant="tonal"
                class="mb-6 rounded-lg"
              >
                {{ successMessage }}
              </v-alert>

              <v-form ref="formRef" @submit.prevent="handleRegister">
                <v-row dense>
                  <!-- Full Name -->
                  <v-col cols="12">
                    <label class="text-subtitle-2 font-weight-bold mb-1 d-block">Full Name</label>
                    <v-text-field
                      v-model="form.full_name"
                      placeholder="e.g., John Doe"
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      color="primary"
                      :rules="[rules.required]"
                    ></v-text-field>
                  </v-col>

                  <!-- Email -->
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
                      :rules="[rules.required, rules.email]"
                    ></v-text-field>
                  </v-col>

                  <!-- Phone -->
                  <v-col cols="12">
                    <label class="text-subtitle-2 font-weight-bold mb-1 d-block">Phone Number</label>
                    <v-text-field
                      v-model="form.phone"
                      placeholder="0912345678"
                      variant="outlined"
                      density="comfortable"
                      rounded="lg"
                      color="primary"
                      :rules="[rules.required, rules.phoneOnlyDigits, rules.phoneLength]"
                      @keypress="allowOnlyDigits"
                    ></v-text-field>
                  </v-col>

                  <!-- Password -->
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
                      :rules="[rules.required, rules.minLength, rules.hasUppercase, rules.hasNumber, rules.hasSpecial]"
                    ></v-text-field>
                  </v-col>

                  <!-- Confirm Password -->
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
                      :rules="[rules.required, rules.confirmMatch]"
                    ></v-text-field>
                  </v-col>
                </v-row>

                <!-- Password strength chips -->
                <div class="mb-4">
                  <div class="d-flex flex-wrap gap-2">
                    <v-chip
                      v-for="hint in passwordHints"
                      :key="hint.label"
                      size="x-small"
                      :color="hint.passed ? 'success' : 'grey-lighten-1'"
                      :variant="hint.passed ? 'tonal' : 'outlined'"
                    >
                      <v-icon start size="12">{{ hint.passed ? 'mdi-check' : 'mdi-close' }}</v-icon>
                      {{ hint.label }}
                    </v-chip>
                  </div>
                </div>

                <!-- Password match indicator -->
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
const formRef = ref(null);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const showPassword = ref(false);

const form = ref({
  full_name: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
});

// ── Validation rules ──────────────────────────────────────────────
const rules = {
  required:        (v) => !!v?.trim()                              || 'This field is required.',
  email:           (v) => /.+@.+\..+/.test(v)                     || 'Please enter a valid email.',
  phoneOnlyDigits: (v) => /^\d+$/.test(v)                         || 'Phone number must contain digits only.',
  phoneLength:     (v) => v?.length === 10                         || 'Phone number must be exactly 10 digits.',
  minLength:       (v) => v?.length >= 8                           || 'At least 8 characters.',
  hasUppercase:    (v) => /[A-Z]/.test(v)                          || 'At least one uppercase letter (A-Z).',
  hasNumber:       (v) => /[0-9]/.test(v)                          || 'At least one number (0-9).',
  // hasSpecial:      (v) => /[!@#$%^&*(),.?":{}|<>]/.test(v)        || 'At least one special character (!@#...).',
  confirmMatch:    (v) => v === form.value.password                || 'Passwords do not match.',
};

// ── Chặn nhập ký tự không phải số ở Phone ────────────────────────
const allowOnlyDigits = (e) => {
  if (!/[0-9]/.test(e.key)) e.preventDefault();
};

// ── Password strength chips ───────────────────────────────────────
const passwordHints = computed(() => [
  { label: '8+ characters',    passed: form.value.password.length >= 8 },
  { label: 'Uppercase (A-Z)', passed: /[A-Z]/.test(form.value.password) },
  { label: 'Number (0-9)',    passed: /[0-9]/.test(form.value.password) },
  
]);

// ── Password match ────────────────────────────────────────────────
const passwordMatch = computed(() =>
  form.value.password.length > 0 && form.value.password === form.value.confirmPassword
);

// ── Submit ────────────────────────────────────────────────────────
const handleRegister = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  loading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    await authService.register({
      full_name: form.value.full_name.trim(),
      email:     form.value.email.trim(),
      phone:     form.value.phone.trim(),
      password:  form.value.password,
    });

    successMessage.value = 'Account created successfully! Redirecting to login…';
    setTimeout(() => router.push('/login'), 1500);
  } catch (error) {
    errorMessage.value =
      error.response?.data?.detail || 'Registration failed. Please try again.';
    // Clear password khi lỗi
    form.value.password = '';
    form.value.confirmPassword = '';
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

:deep(.v-field__outline) {
  --v-field-border-opacity: 0.1;
}
</style>