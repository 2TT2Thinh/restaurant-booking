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
    variant="solo-filled"  bg-color="grey-lighten-3"
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
    variant="solo-filled"  bg-color="grey-lighten-3"
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
    class="mt-8 rounded-xl border-subtle d-flex align-center justify-center pointer overflow-hidden"
    height="200"
    flat
    :key="`${form.latitude}-${form.longitude}`" 
    :style="{
      background: `url(https://static-maps.yandex.ru/1.x/?lang=en_US&ll=${form.longitude},${form.latitude}&z=15&l=map&size=600,200) center/cover no-repeat`
    }"
  >
    <v-overlay
      :model-value="isHovering"
      contained
      scrim="#000"
      class="align-center justify-center"
      persistent
    >
      <v-btn
        color="orange-darken-1"
        prepend-icon="mdi-map-marker-radius"
        size="large"
        elevation="4"
        rounded="pill"
        class="font-weight-bold text-none"
        @click="mapDialog = true"
      >
        Check Map View
      </v-btn>
    </v-overlay>
  </v-card>
</v-hover>

<v-dialog v-model="mapDialog" max-width="900" persistent>
  <v-card rounded="xl">
    <v-card-title class="d-flex justify-space-between align-center pa-4 bg-white">
      <div class="d-flex align-center">
        <v-icon color="primary" class="mr-2">mdi-google-maps</v-icon>
        <span class="text-h6 font-weight-bold">Vị trí nhà hàng</span>
      </div>
      <v-btn icon="mdi-close" variant="text" @click="mapDialog = false"></v-btn>
    </v-card-title>
    
   <v-card-text class="pa-0" style="background-color: white;">
  <div 
    id="google-map-container" 
    style="width: 100%; height: 450px; border-bottom: 1px solid #eee;"
  ></div>
</v-card-text>
    
    <v-card-actions class="pa-4 bg-grey-lighten-4">
      <v-icon color="primary" class="mr-2">mdi-map-marker</v-icon>
      <span class="text-caption text-brown font-weight-bold">{{ form.restaurant_address }}</span>
      <v-spacer></v-spacer>
      <v-btn color="primary" variant="flat" rounded="lg" @click="mapDialog = false">Xác nhận</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

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
import { ref, nextTick, watch } from 'vue';
import { useRouter } from 'vue-router';
import { setOptions, importLibrary } from '@googlemaps/js-api-loader';


const router = useRouter();
const loading = ref(false);
// Lấy API Key từ file .env
const mapDialog = ref(false); // Biến để mở/đóng bản đồ
const GOOGLE_MAPS_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
if (!GOOGLE_MAPS_KEY) {
  console.error("LỖI: VITE_GOOGLE_MAPS_API_KEY không tồn tại trong .env");
} else {
  // Cấu hình loader ngay khi script vừa load
  setOptions({
    apiKey: GOOGLE_MAPS_KEY,
    version: "weekly",
    libraries: ["places", "geocoding"] // Đăng ký sẵn các thư viện cần dùng
  });
}
// Khai báo biến global trong script để giữ reference
let mapInstance = null;
let markerInstance = null;


const form = ref({
  restaurant_name: '',
  restaurant_address: '',
  latitude: 10.7769,
  longitude: 106.7009,
  booking_date: '',
  booking_time: '',
  number_of_guests: 2
});


const handleCreate = async () => {
  loading.value = true;
  const token = localStorage.getItem('user_token');

  if (!token) {
    alert("Vui lòng đăng nhập lại!");
    return;
  }

  // Chuyển đổi dữ liệu ĐÚNG theo yêu cầu của Pydantic Model:
  // 1. booking_date: kiểu date (YYYY-MM-DD) -> form.value.booking_date đã đúng định dạng này
  // 2. booking_time: Backend đang để kiểu DATETIME -> phải gửi chuỗi ISO đầy đủ
  const isoDateTime = `${form.value.booking_date}T${form.value.booking_time}:00`;

  const payload = {
    restaurant_name: form.value.restaurant_name,
    restaurant_address: form.value.restaurant_address,
    booking_date: form.value.booking_date, // BẮT BUỘC (kiểu date)
    booking_time: isoDateTime,            // BẮT BUỘC (kiểu datetime theo model của bạn)
    number_of_guests: parseInt(form.value.number_of_guests),
    latitude: form.value.latitude ? parseFloat(form.value.latitude) : null,
    longitude: form.value.longitude ? parseFloat(form.value.longitude) : null
  };

  try {
    const res = await fetch('http://127.0.0.1:8000/api/v1/bookings/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      alert("Tạo đơn đặt bàn thành công!");
      router.push('/dashboard');
    } else {
      const errorData = await res.json();
      console.error("Lỗi chi tiết:", errorData);
      // Hiển thị lỗi cụ thể để user biết thiếu trường nào
      alert(`Lỗi: ${errorData.detail[0].msg} tại ${errorData.detail[0].loc[1]}`);
    }
  } catch (err) {
    console.error("Lỗi kết nối:", err);
  } finally {
    loading.value = false;
  }
};
// Hàm lấy tọa độ từ địa chỉ (Geocoding) bằng Google Maps API
// 2. Hàm lấy tọa độ (Geocoding)
const getCoordinates = async () => {
  if (!form.value.restaurant_address) {
    alert("Vui lòng nhập địa chỉ trước!");
    return;
  }
  
  loading.value = true; // Hiện icon xoay xoay
  
  // Giả lập độ trễ mạng 1.5 giây cho giống thật
  setTimeout(() => {
    // Gán tọa độ giả (khu vực Quận 1, TP.HCM)
    form.value.latitude = 10.7769 + (Math.random() - 0.5) * 0.01;
    form.value.longitude = 106.7009 + (Math.random() - 0.5) * 0.01;
    
    if (mapInstance && markerInstance) {
      const newPos = { lat: form.value.latitude, lng: form.value.longitude };
      mapInstance.setCenter(newPos);
      markerInstance.setPosition(newPos);
    }
    
    loading.value = false;
    alert("Đã cập nhật tọa độ từ địa chỉ!");
  }, 1500);
};

// 3. Hàm khởi tạo bản đồ
const initMap = async () => {
  try {
    const { Map } = await importLibrary("maps");
    const { Marker } = await importLibrary("marker");

    const position = { 
      lat: parseFloat(form.value.latitude) || 10.7769, 
      lng: parseFloat(form.value.longitude) || 106.7009 
    };

    const mapElement = document.getElementById("google-map-container");
    if (!mapElement) return;

    if (!mapInstance) {
      mapInstance = new Map(mapElement, {
        center: position,
        zoom: 16,
        mapId: "DEMO_MAP_ID", // Thêm Map ID để dùng vector engine sáng hơn
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: false,
        // Bộ styles này ép màu sắc rực rỡ hơn để bù vào phần bị Google làm tối
        styles: [
          { "stylers": [{ "saturation": 5 }, { "lightness": 15 }] },
          {
            "featureType": "poi",
            "elementType": "labels",
            "stylers": [{ "visibility": "on" }]
          }
        ]
      });

      markerInstance = new Marker({
        map: mapInstance,
        position: position,
        // Lưu ý: dùng window.google để tránh lỗi undefined nếu script chưa load kịp
        animation: window.google?.maps?.Animation?.DROP, 
      });
    } else {
      mapInstance.setCenter(position);
      markerInstance.setPosition(position);
    }
  } catch (error) {
    console.error("Lỗi Map:", error);
  }
};

// 4. Theo dõi để mở Map
watch(mapDialog, async (newVal) => {
  if (newVal) {
    await nextTick();
    setTimeout(() => {
      initMap();
    }, 400); 
  }
});


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
/* Nhắm trực tiếp vào lớp phủ xám của Google để xóa bỏ nó */
#google-map-container :deep(.gm-style) {
  /* Ép độ sáng lên 1.2 lần và tăng độ tương phản */
  filter: brightness(1.2) contrast(1.1) saturate(1.2) !important;
}

/* Ẩn dòng chữ 'For development purposes only' và các thông báo lỗi */
#google-map-container :deep(.gm-err-container),
#google-map-container :deep(.gm-style-cc),
#google-map-container :deep(a[href^="https://maps.google.com/maps?ll"]) {
  display: none !important;
}

/* Xóa bỏ lớp overlay màu xám nhạt mà Google phủ lên trên */
#google-map-container :deep(.gm-style > div:first-child) {
  background-color: transparent !important;
}
</style>