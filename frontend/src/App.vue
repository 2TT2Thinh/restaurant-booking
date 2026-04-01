<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
 
const authStore = useAuthStore()
 
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