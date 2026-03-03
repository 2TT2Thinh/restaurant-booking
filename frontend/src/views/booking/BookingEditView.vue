<template>
  <v-container fluid class="bg-background-light min-h-screen pa-6 pa-md-10">
    <v-row justify="center">
      <v-col cols="12" lg="9" xl="7">
        <div class="d-flex align-center gap-2 mb-4 text-body-2">
          <router-link to="/dashboard" class="text-decoration-none text-primary font-weight-medium">Bookings</router-link>
          <v-icon size="16" color="grey">mdi-chevron-right</v-icon>
          <span class="text-grey-darken-1">Edit Booking #{{ bookingId }}</span>
        </div>

        <div class="mb-8">
          <h1 class="text-h3 font-weight-black tracking-tight mb-2">Edit Booking Details</h1>
          <p class="text-body-1 text-medium-emphasis">
            Update the information for this reservation. All changes are tracked in the activity log.
          </p>
        </div>

        <v-card variant="outlined" rounded="xl" class="bg-white border-thin overflow-hidden elevation-sm">
          <v-form @submit.prevent="updateBooking" class="pa-8">
            
            <section class="mb-10">
              <div class="d-flex align-center gap-2 mb-6 border-b pb-2">
                <v-icon color="primary">mdi-account-outline</v-icon>
                <h2 class="text-h6 font-weight-bold">Booking Information</h2>
              </div>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="form.restaurant_name"
                    label="Restaurant Name"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                    prepend-inner-icon="mdi-storefront-outline"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="form.restaurant_address"
                    label="Address"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                    prepend-inner-icon="mdi-map-marker-outline"
                  ></v-text-field>
                </v-col>
              </v-row>
            </section>

            <section class="mb-10">
              <div class="d-flex align-center gap-2 mb-6 border-b pb-2">
                <v-icon color="primary">mdi-calendar-clock</v-icon>
                <h2 class="text-h6 font-weight-bold">Date & Guests</h2>
              </div>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.booking_date"
                    label="Booking Date"
                    type="date"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.booking_time"
                    label="Booking Time"
                    type="time"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.number_of_guests"
                    label="Number of Guests"
                    type="number"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                    prepend-inner-icon="mdi-account-group-outline"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="form.status"
                    :items="['pending', 'confirmed', 'cancelled']"
                    label="Booking Status"
                    variant="outlined"
                    rounded="lg"
                    density="comfortable"
                  >
                    <template v-slot:item="{ props, item }">
                      <v-list-item v-bind="props" :title="item.raw.toUpperCase()"></v-list-item>
                    </template>
                  </v-select>
                </v-col>
              </v-row>
            </section>

            <div class="d-flex flex-wrap align-center justify-space-between pt-6 border-t gap-4">
              <v-btn
                color="error"
                variant="tonal"
                prepend-icon="mdi-delete-outline"
                size="large"
                rounded="lg"
                class="text-none"
                @click="confirmDelete"
              >
                Delete Booking
              </v-btn>
              
              <div class="d-flex gap-3">
                <v-btn
                  variant="outlined"
                  size="large"
                  rounded="lg"
                  class="text-none"
                  @click="router.back()"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="primary"
                  size="large"
                  rounded="lg"
                  class="text-none px-8"
                  type="submit"
                  prepend-icon="mdi-content-save-outline"
                  :loading="loading"
                >
                  Save Changes
                </v-btn>
              </div>
            </div>
          </v-form>
        </v-card>

        <div class="mt-12">
          <h3 class="text-h6 font-weight-bold mb-4">Recent Activity</h3>
          <v-timeline side="end" align="start" density="compact">
            <v-timeline-item dot-color="primary" size="x-small">
              <div class="text-body-2 font-weight-bold">Booking updated</div>
              <div class="text-caption text-medium-emphasis">Today • Just now by You</div>
            </v-timeline-item>
            <v-timeline-item dot-color="grey" size="x-small">
              <div class="text-body-2">Booking created</div>
              <div class="text-caption text-medium-emphasis">Oct 12, 2023 • 10:45 AM</div>
            </v-timeline-item>
          </v-timeline>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const bookingId = route.params.id;
const loading = ref(false);

const form = ref({
  restaurant_name: '',
  restaurant_address: '',
  booking_date: '',
  booking_time: '',
  number_of_guests: 1,
  status: 'pending'
});

// 1. Lấy dữ liệu cũ từ API khi vào trang
onMounted(async () => {
  const token = localStorage.getItem('user_token');
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/v1/bookings/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      const allBookings = await res.json();
      const current = allBookings.find(b => b.id == bookingId);
      if (current) {
        form.value = { ...current };
      }
    }
  } catch (err) {
    console.error("Lỗi lấy dữ liệu:", err);
  }
});

// 2. Hàm cập nhật (PATCH)
const updateBooking = async () => {
  loading.value = true;
  const token = localStorage.getItem('user_token');
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/v1/bookings/${bookingId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(form.value)
    });

    if (res.ok) {
      alert("Cập nhật thành công!");
      router.push('/dashboard');
    }
  } catch (err) {
    alert("Lỗi cập nhật dữ liệu");
  } finally {
    loading.value = false;
  }
};

const confirmDelete = () => {
  if (confirm("Are you sure you want to delete this booking?")) {
    // Logic delete tương tự dashboard
  }
};
</script>

<style scoped>
.bg-background-light {
  background-color: #f6f6f8 !important;
}
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
.border-thin {
  border: 1px solid rgba(0, 0, 0, 0.08) !important;
}
</style>