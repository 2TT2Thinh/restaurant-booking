<script setup>
// Sau này mình sẽ import API vào đây để lấy danh sách bàn từ Backend
const apiUrl = import.meta.env.VITE_API_BASE_URL
</script>

<template>
  <div class="home-container">
    <header>
      <h1>🏠 Restaurant Booking</h1>
      <nav>
        <router-link to="/login">Đăng nhập</router-link> |
        <router-link to="/booking">Đặt bàn ngay</router-link>
      </nav>
    </header>

    <main>
      <section class="hero">
        <h2>Chào mừng bạn đến với không gian ẩm thực tinh tế</h2>
        <p>Hệ thống đang kết nối với Backend tại: <code>{{ apiUrl }}</code></p>
        <button @click="$router.push('/booking')">Khám phá thực đơn & Đặt chỗ</button>
      </section>
    </main>
  </div>
</template>

<style scoped>
.home-container { text-align: center; font-family: sans-serif; }
header { background: #333; color: white; padding: 1rem; }
header a { color: #42b983; text-decoration: none; margin: 0 10px; }
.hero { margin-top: 50px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; display: inline-block; }
button { background: #42b983; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 15px; }
</style>

