<script setup>
// Ở đây chúng ta không cần import HelloWorld nữa
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