<template>
  <div class="login-page">
    <h2>🔐 Đăng nhập hệ thống</h2>
    <form @submit.prevent="handleLogin">
      <input type="email" placeholder="Email" v-model="email" /><br>
      <input type="password" placeholder="Mật khẩu" v-model="password" /><br>
      <button type="submit">Vào thôi!</button>
    </form>
    <router-link to="/">Quay lại trang chủ</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const email = ref('')
const password = ref('')

const handleLogin = () => {
  alert(`Bạn đang thử đăng nhập với: ${email.value}. Bước tiếp theo chúng ta sẽ gửi cái này sang FastAPI!`)
}
</script>

<style scoped>
.login-page { text-align: center; margin-top: 100px; }
input { margin: 5px; padding: 8px; width: 250px; }
</style>