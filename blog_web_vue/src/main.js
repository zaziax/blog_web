import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

axios.defaults.baseURL = 'http://127.0.0.1:5000'
axios.defaults.withCredentials = true


createApp(App).use(store).use(router).use(ElementPlus).mount('#app')
