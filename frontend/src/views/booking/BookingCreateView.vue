<template>
  <v-layout>
    <v-app-bar flat border class="px-md-10 bg-white">
      <div class="d-flex align-center gap-2 text-primary">
        <v-icon size="32">mdi-rhombus-split</v-icon>
        <v-toolbar-title class="font-weight-black text-black">BookingTracker</v-toolbar-title>
      </div>
      <v-spacer></v-spacer>
      <v-btn variant="text" class="text-none font-weight-bold" to="/dashboard">Dashboard</v-btn>
      <v-btn variant="text" class="text-none font-weight-bold">My Bookings</v-btn>
      <v-avatar size="40" class="ml-4 border">
        <v-img src="https://randomuser.me/api/portraits/men/1.jpg"></v-img>
      </v-avatar>
    </v-app-bar>

    <v-main class="bg-background-light min-h-screen">
      <v-container fluid class="pa-0 py-10">
        <v-row justify="center" class="ma-0">
          <v-col cols="12" md="8" lg="6">
            
            <div class="mb-8 px-4">
              <h1 class="text-h3 font-weight-black mb-2">Create New Booking</h1>
              <p class="text-subtitle-1 text-brown">Enter the details of your upcoming visit below.</p>
            </div>

            <v-card variant="outlined" rounded="xl" class="pa-8 bg-white border-subtle shadow-sm">
              <v-form @submit.prevent="handleCreate">
                
                <div class="mb-6">
                  <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Restaurant Name (required)</label>
                  <v-text-field
                    v-model="form.restaurant_name"
                    placeholder="e.g. The Golden Grill"
                    variant="outlined"
                    rounded="lg"
                    prepend-inner-icon="mdi-silverware-fork-knife"
                    color="primary"
                    required
                  ></v-text-field>
                </div>

                <v-sheet border rounded="lg" class="pa-5 mb-6 bg-grey-lighten-5">
                  <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Restaurant Address</label>
                  <v-textarea
                    v-model="form.restaurant_address"
                    placeholder="Enter the full street address..."
                    variant="outlined"
                    rounded="lg"
                    bg-color="white"
                    rows="3"
                  ></v-textarea>

                  <v-row align="end" class="mt-2">
                    <v-col cols="12" sm="4">
                      <v-btn
                        variant="outlined"
                        color="primary"
                        prepend-icon="mdi-map-marker"
                        block
                        height="48"
                        class="text-none font-weight-bold"
                        @click="getCoordinates"
                      >
                        Get Coordinates
                      </v-btn>
                    </v-col>
                    <v-col cols="6" sm="4">
                      <label class="text-caption font-weight-bold text-uppercase text-brown">Latitude</label>
                      <v-text-field
                        v-model="form.latitude"
                        readonly
                        density="compact"
                        variant="flat"
                        bg-color="grey-lighten-3"
                        rounded="lg"
                        hide-details
                      ></v-text-field>
                    </v-col>
                    <v-col cols="6" sm="4">
                      <label class="text-caption font-weight-bold text-uppercase text-brown">Longitude</label>
                      <v-text-field
                        v-model="form.longitude"
                        readonly
                        density="compact"
                        variant="flat"
                        bg-color="grey-lighten-3"
                        rounded="lg"
                        hide-details
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-sheet>

                <v-row>
                  <v-col cols="12" sm="4">
                    <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Date</label>
                    <v-text-field
                      v-model="form.booking_date"
                      type="date"
                      variant="outlined"
                      rounded="lg"
                      prepend-inner-icon="mdi-calendar"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="4">
                    <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Time</label>
                    <v-text-field
                      v-model="form.booking_time"
                      type="time"
                      variant="outlined"
                      rounded="lg"
                      prepend-inner-icon="mdi-clock-outline"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="4">
                    <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Guests</label>
                    <v-text-field
                      v-model="form.number_of_guests"
                      type="number"
                      min="1"
                      variant="outlined"
                      rounded="lg"
                      prepend-inner-icon="mdi-account-group"
                    ></v-text-field>
                  </v-col>
                </v-row>

                <v-divider class="my-6"></v-divider>
                <div class="d-flex justify-end gap-4">
                  <v-btn
                    variant="flat"
                    color="grey-lighten-3"
                    height="48"
                    min-width="120"
                    class="text-none font-weight-bold"
                    @click="router.push('/dashboard')"
                  >
                    Cancel
                  </v-btn>
                  <v-btn
                    variant="flat"
                    color="primary"
                    height="48"
                    min-width="160"
                    class="text-none font-weight-bold shadow-orange"
                    type="submit"
                    :loading="loading"
                  >
                    Create Booking
                  </v-btn>
                </div>
              </v-form>
            </v-card>

            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                class="mt-8 rounded-xl border-subtle d-flex align-center justify-center pointer"
                height="200"
                flat
                img="https://api.mapbox.com/styles/v1/mapbox/light-v10/static/-74.006,40.7128,12/800x200?access_token=YOUR_TOKEN"
              >
                <v-overlay
                  :model-value="isHovering"
                  contained
                  scrim="#000"
                  class="align-center justify-center"
                >
                  <v-btn color="white" rounded="pill" prepend-icon="mdi-map" class="text-none font-weight-bold">
                    Check Map View
                  </v-btn>
                </v-overlay>
              </v-card>
            </v-hover>

          </v-col>
        </v-row>
        
        <footer class="text-center pa-8 text-brown opacity-70">
          <p>© 2024 BookingTracker. All rights reserved.</p>
        </footer>
      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(false);

const form = ref({
  restaurant_name: '',
  restaurant_address: '',
  latitude: '40.7128',
  longitude: '-74.0060',
  booking_date: '',
  booking_time: '',
  number_of_guests: 2
});

const getCoordinates = () => {
  alert("Geocoding address...");
};

const handleCreate = async () => {
  loading.value = true;
  const token = localStorage.getItem('user_token');
  
  try {
    const res = await fetch('http://127.0.0.1:8000/api/v1/bookings/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(form.value)
    });

    if (res.ok) {
      alert("Tạo đơn đặt bàn thành công!");
      router.push('/dashboard');
    } else {
      // Logic dự phòng khi không có backend để bạn vẫn test được dashboard
      console.warn("Backend lỗi, chuyển hướng về dashboard để demo...");
      router.push('/dashboard');
    }
  } catch (err) {
    console.error("Lỗi kết nối:", err);
    // Nếu lỗi kết nối (không chạy backend), vẫn cho quay về dashboard
    router.push('/dashboard');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.text-primary { color: #ee7c2b !important; }
.bg-primary { background-color: #ee7c2b !important; }
.bg-background-light { background-color: #f8f7f6 !important; }
.text-brown { color: #9a6c4c !important; }
.border-subtle { border: 1px solid #e7d9cf !important; }

.shadow-orange {
  box-shadow: 0 4px 14px 0 rgba(238, 124, 43, 0.39) !important;
}

.gap-2 { gap: 8px; }
.gap-4 { gap: 16px; }
.pointer { cursor: pointer; }
</style>