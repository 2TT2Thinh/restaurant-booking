import { createApp } from 'vue'
import { createPinia } from 'pinia' // Import Pinia
import App from './App.vue'
import router from './router' // Import Router (lát nữa mình sẽ viết file này)

const app = createApp(App)

app.use(createPinia()) // Kích hoạt Pinia
app.use(router)        // Kích hoạt Router

app.mount('#app')