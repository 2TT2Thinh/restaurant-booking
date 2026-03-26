<template>
  <div class="admin-bg min-h-screen pa-10">

    <!-- HEADER -->
    <div class="d-flex flex-column flex-md-row justify-space-between align-md-end mb-10 gap-4">
      <div>
        <div class="text-caption font-weight-black text-indigo mb-1"
          style="letter-spacing: 0.15em; text-transform: uppercase;">Curation Hub</div>
        <h1 class="text-h3 font-weight-black text-dark tracking-tight">Restaurants</h1>
        <p class="text-body-2 text-grey-darken-1 mt-1">Manage the portfolio of dining experiences.</p>
      </div>
      <v-btn color="indigo-darken-3" variant="flat" rounded="lg"
        class="text-none font-weight-bold shadow-indigo"
        prepend-icon="mdi-plus" @click="openCreateDialog">
        Add New Restaurant
      </v-btn>
    </div>

    <!-- STATS -->
    <v-row class="mb-8">
      <v-col cols="12" sm="4">
        <v-card variant="flat" rounded="xl" class="stat-card pa-6">
          <div class="text-caption font-weight-black text-grey mb-1"
            style="text-transform:uppercase; letter-spacing:0.1em;">Total Venues</div>
          <div class="text-h4 font-weight-black text-indigo-darken-3">{{ restaurants.length }}</div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card variant="flat" rounded="xl" class="stat-card pa-6">
          <div class="text-caption font-weight-black text-grey mb-1"
            style="text-transform:uppercase; letter-spacing:0.1em;">Avg Capacity</div>
          <div class="text-h4 font-weight-black text-indigo-darken-3">{{ avgCapacity }}</div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card variant="flat" rounded="xl" class="stat-card pa-6">
          <div class="text-caption font-weight-black text-grey mb-1"
            style="text-transform:uppercase; letter-spacing:0.1em;">Cuisine Types</div>
          <div class="text-h4 font-weight-black text-indigo-darken-3">{{ cuisineCount }}</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- FILTER + SEARCH -->
    <v-card variant="flat" rounded="xl" class="stat-card pa-4 mb-2 d-flex align-center justify-space-between flex-wrap gap-3">
      <div class="d-flex align-center gap-3">
        <v-text-field
          v-model="search"
          placeholder="Search restaurants..."
          variant="solo" flat density="compact"
          prepend-inner-icon="mdi-magnify"
          hide-details rounded="lg"
          bg-color="grey-lighten-4"
          style="min-width: 280px;"
          @update:model-value="onSearch"
        ></v-text-field>
        <v-select
          v-model="filterCuisine"
          :items="cuisineTypes"
          variant="solo" flat density="compact"
          hide-details rounded="lg"
          bg-color="grey-lighten-4"
          style="min-width: 160px;"
          @update:model-value="fetchRestaurants"
        ></v-select>
      </div>
      <p class="text-caption text-grey font-weight-medium">
        Showing {{ restaurants.length }} results
      </p>
    </v-card>

    <!-- TABLE -->
    <v-card variant="flat" rounded="xl" class="overflow-hidden stat-card">
      <v-table>
        <thead>
          <tr class="table-header">
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">ID</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Restaurant</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Address</th>
            <th class="text-caption font-weight-black text-grey" style="text-transform:uppercase; letter-spacing:0.1em;">Cuisine</th>
            <th class="text-caption font-weight-black text-grey text-center" style="text-transform:uppercase; letter-spacing:0.1em;">Capacity</th>
            <th class="text-caption font-weight-black text-grey text-center" style="text-transform:uppercase; letter-spacing:0.1em;">Hours</th>
            <th class="text-caption font-weight-black text-grey text-right" style="text-transform:uppercase; letter-spacing:0.1em;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="7" class="text-center py-8">
              <v-progress-circular indeterminate color="indigo" size="32"></v-progress-circular>
            </td>
          </tr>
          <tr v-else v-for="r in restaurants" :key="r.id" class="table-row">
            <td class="py-5">
              <span class="text-caption font-weight-medium text-grey" style="font-family: monospace;">
                #RES-{{ String(r.id).padStart(3, '0') }}
              </span>
            </td>
            <td class="py-5">
              <div class="d-flex align-center gap-3">
                <v-avatar color="indigo-lighten-5" size="40" rounded="lg">
                  <v-icon color="indigo-darken-3" size="20">mdi-silverware-fork-knife</v-icon>
                </v-avatar>
                <div>
                  <div class="text-body-2 font-weight-bold text-dark">{{ r.name }}</div>
                  <div class="text-caption text-grey" v-if="r.phone">{{ r.phone }}</div>
                </div>
              </div>
            </td>
            <td class="py-5">
              <p class="text-caption text-grey-darken-1" style="max-width: 200px; line-height: 1.5;">
                {{ r.address }}
              </p>
            </td>
            <td class="py-5">
              <v-chip v-if="r.cuisine_type" size="x-small" color="indigo" variant="tonal" class="font-weight-bold">
                {{ r.cuisine_type }}
              </v-chip>
              <span v-else class="text-caption text-grey">—</span>
            </td>
            <td class="py-5 text-center">
              <span class="text-body-2 font-weight-bold text-dark">{{ r.max_capacity }}</span>
            </td>
            <td class="py-5 text-center">
              <span class="text-caption text-grey-darken-1" v-if="r.opening_time">
                {{ r.opening_time?.slice(0,5) }} – {{ r.closing_time?.slice(0,5) }}
              </span>
              <span v-else class="text-caption text-grey">—</span>
            </td>
            <td class="py-5 text-right">
              <div class="d-flex justify-end gap-2 action-btns">
                <v-btn icon size="small" color="indigo" variant="tonal" @click="openEditDialog(r)">
                  <v-icon size="16">mdi-pencil-outline</v-icon>
                </v-btn>
                <v-btn icon size="small" color="error" variant="tonal" @click="confirmDelete(r)">
                  <v-icon size="16">mdi-delete-outline</v-icon>
                </v-btn>
              </div>
            </td>
          </tr>
          <tr v-if="!loading && restaurants.length === 0">
            <td colspan="7" class="text-center py-10 text-grey">
              <v-icon size="48" color="grey-lighten-2" class="mb-2">mdi-silverware-fork-knife</v-icon>
              <div>No restaurants found.</div>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <!-- DIALOG CREATE / EDIT -->
    <v-dialog v-model="dialog.show" max-width="600" persistent>
      <v-card rounded="xl">
        <div class="pa-6 d-flex align-center justify-space-between border-b">
          <h3 class="text-h6 font-weight-bold text-dark">
            {{ dialog.isEdit ? 'Edit Restaurant' : 'Add New Restaurant' }}
          </h3>
          <v-btn icon variant="text" @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <v-card-text class="pa-6">
          <v-alert v-if="dialog.error" type="error" variant="tonal" rounded="lg" class="mb-4" closable
            @click:close="dialog.error = ''">
            {{ dialog.error }}
          </v-alert>

          <v-form ref="dialogFormRef">
            <v-row>
              <v-col cols="12">
                <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Restaurant Name *</label>
                <v-text-field v-model="form.name" variant="outlined" rounded="lg" density="comfortable"
                  placeholder="The Golden Grill" color="indigo"
                  :rules="[rules.required]"></v-text-field>
              </v-col>
              <v-col cols="12">
                <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Address *</label>
                <v-textarea v-model="form.address" variant="outlined" rounded="lg" density="comfortable"
                  rows="2" placeholder="123 Main Street, District 1" color="indigo"
                  :rules="[rules.required]"></v-textarea>
              </v-col>
              <v-col cols="12" sm="6">
                <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Phone Number</label>
                <v-text-field v-model="form.phone" variant="outlined" rounded="lg" density="comfortable"
                  placeholder="028 1234 5678" color="indigo"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Cuisine Type</label>
                <v-text-field v-model="form.cuisine_type" variant="outlined" rounded="lg" density="comfortable"
                  placeholder="Italian, Japanese, Vietnamese..." color="indigo"></v-text-field>
              </v-col>
              <v-col cols="12" sm="4">
                <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Opening Time</label>
                <v-text-field v-model="form.opening_time" type="time" variant="outlined" rounded="lg"
                  density="comfortable" color="indigo"></v-text-field>
              </v-col>
              <v-col cols="12" sm="4">
                <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Closing Time</label>
                <v-text-field v-model="form.closing_time" type="time" variant="outlined" rounded="lg"
                  density="comfortable" color="indigo"></v-text-field>
              </v-col>
              <v-col cols="12" sm="4">
                <label class="text-subtitle-2 font-weight-bold mb-2 d-block">Max Capacity *</label>
                <v-text-field v-model.number="form.max_capacity" type="number" min="1"
                  variant="outlined" rounded="lg" density="comfortable" color="indigo"
                  :rules="[rules.required, rules.minCapacity]"></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-6 pt-0 d-flex justify-end gap-3">
          <v-btn variant="outlined" rounded="lg" class="text-none" @click="closeDialog">Cancel</v-btn>
          <v-btn color="indigo-darken-3" variant="flat" rounded="lg"
            class="text-none font-weight-bold px-6"
            :loading="dialog.loading" @click="submitForm">
            {{ dialog.isEdit ? 'Save Changes' : 'Create Restaurant' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- DIALOG DELETE -->
    <v-dialog v-model="deleteDialog.show" max-width="420">
      <v-card rounded="xl" class="pa-6">
        <div class="text-center mb-6">
          <v-avatar color="red-lighten-4" size="64" class="mb-4">
            <v-icon color="error" size="32">mdi-delete-outline</v-icon>
          </v-avatar>
          <h3 class="text-h6 font-weight-bold text-dark mb-2">Delete Restaurant?</h3>
          <p class="text-body-2 text-grey-darken-1">
            Are you sure you want to delete
            <strong>{{ deleteDialog.restaurant?.name }}</strong>?
            This action cannot be undone.
          </p>
        </div>
        <div class="d-flex gap-3">
          <v-btn variant="outlined" rounded="lg" class="text-none flex-grow-1"
            @click="deleteDialog.show = false">Cancel</v-btn>
          <v-btn color="error" variant="flat" rounded="lg"
            class="text-none font-weight-bold flex-grow-1"
            :loading="deleteDialog.loading" @click="deleteRestaurant">Delete</v-btn>
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

const restaurants  = ref([])
const loading      = ref(false)
const search       = ref('')
const filterCuisine = ref('All Cuisines')
const dialogFormRef = ref(null)
let searchTimeout  = null

const dialog = ref({ show: false, isEdit: false, loading: false, error: '', editId: null })
const deleteDialog = ref({ show: false, loading: false, restaurant: null })
const snackbar = ref({ show: false, message: '', color: 'success' })

const defaultForm = {
  name: '', address: '', phone: '', cuisine_type: '',
  opening_time: '', closing_time: '', max_capacity: 50
}
const form = ref({ ...defaultForm })

// ── Validation rules ──────────────────────────────────────────────
const rules = {
  required:    (v) => !!v || 'This field is required.',
  minCapacity: (v) => v >= 1 || 'Capacity must be at least 1.',
}

// ── Computed ──────────────────────────────────────────────────────
const avgCapacity = computed(() => {
  if (!restaurants.value.length) return 0
  const total = restaurants.value.reduce((sum, r) => sum + (r.max_capacity || 0), 0)
  return Math.round(total / restaurants.value.length)
})

const cuisineCount = computed(() => {
  const types = restaurants.value.map(r => r.cuisine_type).filter(Boolean)
  return new Set(types).size
})

const cuisineTypes = computed(() => {
  const types = restaurants.value.map(r => r.cuisine_type).filter(Boolean)
  return ['All Cuisines', ...new Set(types)]
})

// ── Helpers ───────────────────────────────────────────────────────
const showSnackbar = (message, color = 'success') => {
  snackbar.value = { show: true, message, color }
}

const openCreateDialog = () => {
  form.value = { ...defaultForm }
  dialog.value = { show: true, isEdit: false, loading: false, error: '', editId: null }
}

const openEditDialog = (r) => {
  form.value = {
    name:         r.name,
    address:      r.address,
    phone:        r.phone || '',
    cuisine_type: r.cuisine_type || '',
    opening_time: r.opening_time?.slice(0, 5) || '',
    closing_time: r.closing_time?.slice(0, 5) || '',
    max_capacity: r.max_capacity
  }
  dialog.value = { show: true, isEdit: true, loading: false, error: '', editId: r.id }
}

const closeDialog = () => { dialog.value.show = false }

const confirmDelete = (r) => {
  deleteDialog.value = { show: true, loading: false, restaurant: r }
}

const onSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => fetchRestaurants(), 400)
}

// ── API ───────────────────────────────────────────────────────────
const fetchRestaurants = async () => {
  loading.value = true
  try {
    const params = {}
    if (search.value.trim()) params.search = search.value.trim()
    const res = await apiClient.get('/restaurants/', { params })
    let data = res.data
    if (filterCuisine.value && filterCuisine.value !== 'All Cuisines') {
      data = data.filter(r => r.cuisine_type === filterCuisine.value)
    }
    restaurants.value = data
  } catch (err) {
    showSnackbar('Failed to load restaurants.', 'error')
  } finally {
    loading.value = false
  }
}

const submitForm = async () => {
  const { valid } = await dialogFormRef.value.validate()
  if (!valid) return

  dialog.value.loading = true
  dialog.value.error = ''

  const payload = {
    name:         form.value.name,
    address:      form.value.address,
    phone:        form.value.phone || null,
    cuisine_type: form.value.cuisine_type || null,
    opening_time: form.value.opening_time ? form.value.opening_time + ':00' : null,
    closing_time: form.value.closing_time ? form.value.closing_time + ':00' : null,
    max_capacity: form.value.max_capacity
  }

  try {
    if (dialog.value.isEdit) {
      await apiClient.patch(`/restaurants/${dialog.value.editId}`, payload)
      showSnackbar('Restaurant updated successfully.')
    } else {
      await apiClient.post('/restaurants/', payload)
      showSnackbar('Restaurant created successfully.')
    }
    closeDialog()
    await fetchRestaurants()
  } catch (err) {
    const detail = err.response?.data?.detail
    dialog.value.error = typeof detail === 'string' ? detail : 'Something went wrong. Please try again.'
  } finally {
    dialog.value.loading = false
  }
}

const deleteRestaurant = async () => {
  deleteDialog.value.loading = true
  try {
    await apiClient.delete(`/restaurants/${deleteDialog.value.restaurant.id}`)
    showSnackbar('Restaurant deleted successfully.')
    deleteDialog.value.show = false
    await fetchRestaurants()
  } catch (err) {
    showSnackbar(err.response?.data?.detail || 'Failed to delete restaurant.', 'error')
  } finally {
    deleteDialog.value.loading = false
  }
}

onMounted(fetchRestaurants)
</script>

<style scoped>
.admin-bg { background-color: #f8f9fc !important; }
.text-dark { color: #1a1c1c !important; }
.text-indigo { color: #3730a3 !important; }
.tracking-tight { letter-spacing: -0.02em !important; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
.stat-card { background: #fff !important; border: 1px solid #f1f5f9 !important; transition: box-shadow 0.2s; }
.stat-card:hover { box-shadow: 0 8px 24px rgba(36, 56, 156, 0.06) !important; }
.shadow-indigo { box-shadow: 0 8px 24px rgba(55, 48, 163, 0.25) !important; }
.table-header th { background-color: #f8fafc !important; padding: 16px 20px !important; }
.table-row td { padding: 0 20px !important; border-bottom: 1px solid #f1f5f9 !important; }
.table-row:hover { background-color: #f8fafc !important; }
.action-btns { opacity: 0; transition: opacity 0.2s; }
.table-row:hover .action-btns { opacity: 1; }
</style>