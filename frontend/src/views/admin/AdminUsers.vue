<template>
  <div class="admin-bg min-h-screen pa-10">

    <!-- HEADER -->
    <div class="d-flex flex-column flex-md-row justify-space-between align-md-end mb-10 gap-4">
      <div>
        <div class="text-caption font-weight-black text-indigo mb-1"
          style="letter-spacing: 0.15em; text-transform: uppercase;">Directory</div>
        <h1 class="text-h3 font-weight-black text-dark tracking-tight">User Management</h1>
        <p class="text-body-2 text-grey-darken-1 mt-1">Oversee and curate platform access permissions.</p>
      </div>
    </div>

    <!-- STATS BENTO -->
    <v-row class="mb-10">
      <v-col cols="12" md="4">
        <v-card variant="flat" rounded="xl" class="stat-card pa-8 overflow-hidden">
          <div class="text-caption font-weight-black text-grey mb-2"
            style="text-transform:uppercase; letter-spacing:0.1em;">Total Users</div>
          <div class="text-h3 font-weight-black text-indigo-darken-3">{{ users.length }}</div>
          <div class="d-flex align-center gap-1 mt-3 text-success">
            <v-icon size="16" color="success">mdi-trending-up</v-icon>
            <span class="text-caption font-weight-bold">{{ activeCount }} active</span>
          </div>
          <v-icon class="sparkle-icon" color="indigo-lighten-4" size="80">mdi-account-group</v-icon>
        </v-card>
      </v-col>
      <v-col cols="12" md="8">
        <v-card variant="flat" rounded="xl" color="indigo-darken-3" class="pa-8 shadow-indigo h-100">
          <div class="text-caption font-weight-black mb-4"
            style="color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:0.1em;">
            User Breakdown
          </div>
          <v-row>
            <v-col cols="4" class="text-center">
              <div class="text-h4 font-weight-black text-white">{{ adminCount }}</div>
              <div class="text-caption text-white" style="opacity:0.7;">Admins</div>
            </v-col>
            <v-col cols="4" class="text-center">
              <div class="text-h4 font-weight-black text-white">{{ customerCount }}</div>
              <div class="text-caption text-white" style="opacity:0.7;">Customers</div>
            </v-col>
            <v-col cols="4" class="text-center">
              <div class="text-h4 font-weight-black text-white">{{ inactiveCount }}</div>
              <div class="text-caption text-white" style="opacity:0.7;">Deactivated</div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- TABLE CONTAINER -->
    <v-card variant="flat" rounded="xl" class="stat-card overflow-hidden">

      <!-- TABS + SEARCH -->
      <div class="px-6 py-4 d-flex align-center justify-space-between border-b flex-wrap gap-3">
        <div class="d-flex gap-2">
          <v-btn
            v-for="tab in userTabs"
            :key="tab.value"
            :variant="activeTab === tab.value ? 'flat' : 'text'"
            :color="activeTab === tab.value ? 'indigo-darken-3' : 'grey'"
            rounded="lg"
            size="small"
            class="text-none font-weight-bold"
            @click="activeTab = tab.value"
          >{{ tab.label }}</v-btn>
        </div>
        <v-text-field
          v-model="search"
          placeholder="Search users..."
          variant="solo"
          flat
          density="compact"
          prepend-inner-icon="mdi-magnify"
          hide-details
          rounded="lg"
          bg-color="grey-lighten-4"
          style="max-width: 280px;"
          @update:model-value="onSearch"
        ></v-text-field>
      </div>

      <!-- TABLE -->
      <v-table>
        <thead>
          <tr class="table-header">
            <th class="text-caption font-weight-black text-grey"
              style="text-transform:uppercase; letter-spacing:0.1em;">User Identity</th>
            <th class="text-caption font-weight-black text-grey"
              style="text-transform:uppercase; letter-spacing:0.1em;">Contact Info</th>
            <th class="text-caption font-weight-black text-grey"
              style="text-transform:uppercase; letter-spacing:0.1em;">System Role</th>
            <th class="text-caption font-weight-black text-grey"
              style="text-transform:uppercase; letter-spacing:0.1em;">Status</th>
            <th class="text-caption font-weight-black text-grey"
              style="text-transform:uppercase; letter-spacing:0.1em;">Joined</th>
            <th class="text-caption font-weight-black text-grey text-right"
              style="text-transform:uppercase; letter-spacing:0.1em;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="6" class="text-center py-8">
              <v-progress-circular indeterminate color="indigo" size="32"></v-progress-circular>
            </td>
          </tr>
          <tr
            v-else
            v-for="user in filteredUsers"
            :key="user.id"
            class="table-row"
            :class="{ 'deactivated-row': !user.is_active }"
          >
            <td class="py-5">
              <div class="d-flex align-center gap-4">
                <v-avatar
                  :color="user.is_active ? 'indigo-lighten-4' : 'grey-lighten-3'"
                  size="44" rounded="lg"
                >
                  <span
                    :class="user.is_active ? 'text-indigo-darken-3' : 'text-grey'"
                    class="text-body-2 font-weight-black"
                  >{{ user.full_name?.charAt(0)?.toUpperCase() || 'U' }}</span>
                </v-avatar>
                <div>
                  <div class="text-body-2 font-weight-bold"
                    :class="user.is_active ? 'text-dark' : 'text-grey'">
                    {{ user.full_name }}
                  </div>
                  <div class="text-caption text-grey">ID: #{{ String(user.id).padStart(4, '0') }}</div>
                </div>
              </div>
            </td>
            <td class="py-5">
              <div class="text-body-2 font-weight-medium"
                :class="user.is_active ? '' : 'text-grey'">{{ user.email }}</div>
              <div class="text-caption text-grey" v-if="user.phone">{{ user.phone }}</div>
            </td>
            <td class="py-5">
              <div class="d-flex align-center gap-2">
                <v-icon
                  size="8"
                  :color="user.role === 'admin' ? 'indigo-darken-3' : 'grey'"
                >mdi-circle</v-icon>
                <span
                  class="text-body-2 font-weight-bold"
                  :class="user.role === 'admin' ? 'text-indigo-darken-3' : 'text-grey-darken-1'"
                >{{ user.role === 'admin' ? 'Admin' : 'Customer' }}</span>
              </div>
            </td>
            <td class="py-5">
              <v-chip
                :color="user.is_active ? 'success' : 'grey'"
                size="small"
                variant="tonal"
                class="font-weight-bold"
              >{{ user.is_active ? 'Active' : 'Deactivated' }}</v-chip>
            </td>
            <td class="py-5">
              <span class="text-caption text-grey">{{ formatDate(user.created_at) }}</span>
            </td>
            <td class="py-5 text-right">
              <div class="d-flex justify-end gap-2 action-btns">
                <!-- Đổi role -->
                <v-tooltip
                  :text="user.role === 'admin' ? 'Set as Customer' : 'Set as Admin'"
                  location="top"
                >
                  <template v-slot:activator="{ props }">
                    <v-btn
                      v-bind="props"
                      icon size="small"
                      color="indigo"
                      variant="tonal"
                      @click="toggleRole(user)"
                    >
                      <v-icon size="16">mdi-shield-account-outline</v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>

                <!-- Kích hoạt / Vô hiệu hóa -->
                <v-tooltip
                  :text="user.is_active ? 'Deactivate' : 'Activate'"
                  location="top"
                >
                  <template v-slot:activator="{ props }">
                    <v-btn
                      v-bind="props"
                      icon size="small"
                      :color="user.is_active ? 'error' : 'success'"
                      variant="tonal"
                      @click="toggleActive(user)"
                    >
                      <v-icon size="16">
                        {{ user.is_active ? 'mdi-account-off-outline' : 'mdi-account-check-outline' }}
                      </v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>
              </div>
            </td>
          </tr>
          <tr v-if="!loading && filteredUsers.length === 0">
            <td colspan="6" class="text-center py-10 text-grey">
              <v-icon size="48" color="grey-lighten-2" class="mb-2">mdi-account-group</v-icon>
              <div>Không tìm thấy user nào</div>
            </td>
          </tr>
        </tbody>
      </v-table>

      <!-- PAGINATION INFO -->
      <div class="px-6 py-4 bg-grey-lighten-5 d-flex align-center justify-space-between border-t">
        <span class="text-caption font-weight-bold text-grey"
          style="text-transform:uppercase; letter-spacing:0.1em;">
          Showing {{ filteredUsers.length }} of {{ users.length }} users
        </span>
      </div>
    </v-card>

    <!-- DIALOG XÁC NHẬN ĐỔI ROLE -->
    <v-dialog v-model="confirmDialog.show" max-width="420">
      <v-card rounded="xl" class="pa-6">
        <div class="text-center mb-6">
          <v-avatar color="indigo-lighten-4" size="64" class="mb-4">
            <v-icon color="indigo-darken-3" size="32">mdi-shield-account-outline</v-icon>
          </v-avatar>
          <h3 class="text-h6 font-weight-bold text-dark mb-2">{{ confirmDialog.title }}</h3>
          <p class="text-body-2 text-grey-darken-1">{{ confirmDialog.message }}</p>
        </div>
        <div class="d-flex gap-3">
          <v-btn variant="outlined" rounded="lg" class="text-none flex-grow-1"
            @click="confirmDialog.show = false">Hủy</v-btn>
          <v-btn
            :color="confirmDialog.color"
            variant="flat" rounded="lg"
            class="text-none font-weight-bold flex-grow-1"
            :loading="confirmDialog.loading"
            @click="confirmDialog.action"
          >Xác nhận</v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- SNACKBAR -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" rounded="lg" timeout="3000" location="bottom right">
      {{ snackbar.message }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '@/api/axios'

const users = ref([])
const loading = ref(false)
const search = ref('')
const activeTab = ref('all')
const snackbar = ref({ show: false, message: '', color: 'success' })
const confirmDialog = ref({
  show: false, loading: false,
  title: '', message: '', color: 'indigo',
  action: () => {}
})
let searchTimeout = null

// ==================== COMPUTED ====================

const activeCount   = computed(() => users.value.filter(u => u.is_active).length)
const inactiveCount = computed(() => users.value.filter(u => !u.is_active).length)
const adminCount    = computed(() => users.value.filter(u => u.role === 'admin').length)
const customerCount = computed(() => users.value.filter(u => u.role === 'customer').length)

const userTabs = [
  { label: 'All Users',      value: 'all' },
  { label: 'Administrators', value: 'admin' },
  { label: 'Customers',      value: 'customer' },
]

const filteredUsers = computed(() => {
  return users.value.filter(u => {
    const tabMatch = activeTab.value === 'all' || u.role === activeTab.value
    const searchMatch = !search.value.trim() ||
      u.full_name?.toLowerCase().includes(search.value.toLowerCase()) ||
      u.email?.toLowerCase().includes(search.value.toLowerCase())
    return tabMatch && searchMatch
  })
})

// ==================== HELPERS ====================

const showSnackbar = (message, color = 'success') => {
  snackbar.value = { show: true, message, color }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('vi-VN', {
    day: '2-digit', month: '2-digit', year: 'numeric'
  })
}

const onSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => fetchUsers(), 400)
}

// ==================== API ====================

const fetchUsers = async () => {
  loading.value = true
  try {
    const params = { limit: 200 }
    if (search.value.trim()) params.search = search.value.trim()
    const res = await apiClient.get('/admin/users', { params })
    users.value = res.data
  } catch (err) {
    showSnackbar('Lỗi tải danh sách user!', 'error')
  } finally {
    loading.value = false
  }
}

const toggleRole = (user) => {
  const newRole = user.role === 'admin' ? 'customer' : 'admin'
  confirmDialog.value = {
    show: true,
    loading: false,
    title: `Đổi role thành ${newRole}?`,
    message: `Bạn có chắc muốn đổi role của ${user.full_name} thành ${newRole.toUpperCase()}?`,
    color: 'indigo-darken-3',
    action: async () => {
      confirmDialog.value.loading = true
      try {
        await apiClient.patch(`/admin/users/${user.id}`, { role: newRole })
        showSnackbar(`Đã đổi role thành ${newRole}!`)
        confirmDialog.value.show = false
        await fetchUsers()
      } catch (err) {
        showSnackbar(err.response?.data?.detail || 'Lỗi đổi role!', 'error')
      } finally {
        confirmDialog.value.loading = false
      }
    }
  }
}

const toggleActive = (user) => {
  const newActive = !user.is_active
  confirmDialog.value = {
    show: true,
    loading: false,
    title: newActive ? 'Kích hoạt tài khoản?' : 'Vô hiệu hóa tài khoản?',
    message: newActive
      ? `Kích hoạt lại tài khoản của ${user.full_name}?`
      : `Vô hiệu hóa tài khoản của ${user.full_name}? User sẽ không thể đăng nhập.`,
    color: newActive ? 'success' : 'error',
    action: async () => {
      confirmDialog.value.loading = true
      try {
        await apiClient.patch(`/admin/users/${user.id}`, { is_active: newActive })
        showSnackbar(newActive ? 'Đã kích hoạt tài khoản!' : 'Đã vô hiệu hóa tài khoản!')
        confirmDialog.value.show = false
        await fetchUsers()
      } catch (err) {
        showSnackbar(err.response?.data?.detail || 'Lỗi cập nhật!', 'error')
      } finally {
        confirmDialog.value.loading = false
      }
    }
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.admin-bg { background-color: #f8f9fc !important; }
.text-dark { color: #1a1c1c !important; }
.text-indigo { color: #3730a3 !important; }
.tracking-tight { letter-spacing: -0.02em !important; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }

.stat-card {
  background: #fff !important;
  border: 1px solid #f1f5f9 !important;
}
.shadow-indigo { box-shadow: 0 8px 24px rgba(55, 48, 163, 0.25) !important; }
.h-100 { height: 100%; }

.sparkle-icon {
  position: absolute;
  bottom: -10px;
  right: -10px;
  opacity: 0.06;
}

.table-header th {
  background-color: #f8fafc !important;
  padding: 16px 20px !important;
}
.table-row td {
  padding: 0 20px !important;
  border-bottom: 1px solid #f1f5f9 !important;
}
.table-row:hover { background-color: #f8fafc !important; }
.deactivated-row { opacity: 0.6; }
.action-btns { opacity: 0; transition: opacity 0.2s; }
.table-row:hover .action-btns { opacity: 1; }
</style>