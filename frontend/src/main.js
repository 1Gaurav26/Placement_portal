import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:5000/api'

// Restore token header on load
const token = localStorage.getItem('token')
if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
