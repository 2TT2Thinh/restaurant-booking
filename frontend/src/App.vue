<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
 
const authStore = useAuthStore()
 
/**
 * Khi app khởi động:
 * Nếu user còn token trong localStorage → tự động fetch lại user info
 * Nhờ vậy user không bị mất đăng nhập khi F5
 */
onMounted(async () => {
  await authStore.init()
})
</script>

<template>
  <div id="app-container">
    <router-view />
  </div>
</template>

<style>
/* Reset CSS cơ bản để giao diện trông sạch sẽ hơn */
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
  color: #333;
}

#app-container {
  min-height: 100vh;
}
</style>