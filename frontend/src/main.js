import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 1. Import Vuetify và CSS
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// 2. Import Icons (Để hiển thị mdi-calendar, mdi-lock...)
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css' 

// 3. Cấu hình Theme (Màu sắc theo đúng thiết kế StichAI)
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#ee7c2b',       // Màu cam đặc trưng của bạn
          surface: '#ffffff',       // Màu nền trắng của card
          'background-light': '#f8f7f6', // Màu nền nhạt phía sau
        },
      },
    },
  },
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify) // 4. Kích hoạt Vuetify

app.mount('#app')