<template>
  <v-app>
    <!-- ==================== SIDEBAR ==================== -->
    <v-navigation-drawer
      v-model="drawer"
      permanent
      width="256"
      color="white"
      border="right"
      class="admin-sidebar"
    >
      <!-- LOGO -->
      <div class="px-8 py-6 d-flex align-center gap-3">
        <v-sheet
          width="36" height="36"
          color="indigo-darken-3"
          rounded="lg"
          class="d-flex align-center justify-center flex-shrink-0"
        >
          <v-icon color="white" size="20">mdi-silverware-fork-knife</v-icon>
        </v-sheet>
        <div>
          <div class="text-subtitle-1 font-weight-black text-indigo-darken-4 leading-tight">Architect</div>
          <div class="text-caption text-grey tracking-widest" style="font-size: 9px; text-transform: uppercase;">
            Premium Management
          </div>
        </div>
      </div>

      <v-divider></v-divider>

      <!-- NAV ITEMS -->
      <v-list nav density="compact" class="px-4 py-4">
        <v-list-item
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
          rounded="lg"
          class="mb-1 nav-item"
          active-class="nav-item-active"
        ></v-list-item>
      </v-list>

      <!-- BOTTOM ACTIONS -->
      <template v-slot:append>
        <v-divider></v-divider>
        <v-list nav density="compact" class="px-4 py-4">
          <v-list-item
            prepend-icon="mdi-view-dashboard-outline"
            title="Back to App"
            rounded="lg"
            class="nav-item mb-1"
            to="/dashboard"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-logout"
            title="Logout"
            rounded="lg"
            class="nav-item-logout"
            @click="handleLogout"
          ></v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>

    <!-- ==================== TOPBAR ==================== -->
    <v-app-bar
      flat
      height="64"
      class="admin-topbar"
      style="left: 256px !important;"
    >
      <div class="d-flex align-center px-6 w-100">
        <!-- SEARCH -->
        <v-text-field
          v-model="searchQuery"
          placeholder="Search..."
          variant="solo"
          flat
          density="compact"
          prepend-inner-icon="mdi-magnify"
          hide-details
          rounded="lg"
          bg-color="grey-lighten-4"
          style="max-width: 360px;"
          @keyup.enter="handleSearch"
        ></v-text-field>

        <v-spacer></v-spacer>

        <!-- ACTIONS -->
        <v-btn icon variant="text" color="grey-darken-1" class="mr-1">
          <v-icon>mdi-bell-outline</v-icon>
        </v-btn>
        <v-btn icon variant="text" color="grey-darken-1" class="mr-3">
          <v-icon>mdi-cog-outline</v-icon>
        </v-btn>

        <v-divider vertical class="mr-4" style="height: 32px;"></v-divider>

        <!-- ADMIN PROFILE -->
        <div class="d-flex align-center gap-3">
          <div class="text-right">
            <div class="text-caption font-weight-bold text-indigo-darken-3 leading-tight">{{ adminEmail }}</div>
            <div class="text-caption text-grey" style="font-size: 10px;">Super Admin</div>
          </div>
          <v-avatar color="indigo-darken-3" size="36">
            <span class="text-white text-body-2 font-weight-bold">
              {{ adminEmail ? adminEmail.charAt(0).toUpperCase() : 'A' }}
            </span>
          </v-avatar>
        </div>
      </div>
    </v-app-bar>

    <!-- ==================== MAIN CONTENT ==================== -->
    <v-main style="margin-left: 0;">
      <router-view></router-view>
    </v-main>

  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const drawer = ref(true)
const searchQuery = ref('')
const adminEmail = ref('')

const navItems = [
  { title: 'Dashboard',    icon: 'mdi-view-dashboard-outline', to: '/admin' },
  { title: 'Restaurants',  icon: 'mdi-silverware-fork-knife',  to: '/admin/restaurants' },
  { title: 'Bookings',     icon: 'mdi-calendar-check-outline', to: '/admin/bookings' },
  { title: 'Users',        icon: 'mdi-account-group-outline',  to: '/admin/users' },
]

const handleLogout = () => {
  localStorage.removeItem('user_token')
  localStorage.removeItem('user_email')
  router.push('/login')
}

const handleSearch = () => {
  // Search toàn cục nếu cần sau này
}

onMounted(() => {
  adminEmail.value = localStorage.getItem('user_email') || 'Admin'
})
</script>

<style scoped>
.admin-sidebar {
  border-right: 1px solid #f1f1f1 !important;
}

.admin-topbar {
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(12px) !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06) !important;
  box-shadow: 0 4px 24px rgba(36, 56, 156, 0.04) !important;
}

.nav-item {
  color: #64748b !important;
  font-weight: 500 !important;
}

.nav-item:hover {
  color: #1e293b !important;
  background-color: #f8fafc !important;
}

.nav-item-active {
  color: #3730a3 !important;
  background-color: #eef2ff !important;
  font-weight: 700 !important;
  border-left: 3px solid #3730a3 !important;
}

:deep(.nav-item-active .v-list-item__prepend .v-icon) {
  color: #3730a3 !important;
}

.nav-item-logout {
  color: #ef4444 !important;
  font-weight: 500 !important;
}

.nav-item-logout:hover {
  background-color: #fef2f2 !important;
}

.gap-3 { gap: 12px; }
</style>