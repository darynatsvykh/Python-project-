import { createApp } from 'vue'
import { createPinia } from 'pinia';
import App from './App.vue'
import router from './router'
import axios from 'axios';


import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://127.0.0.1:8000";

const app = createApp(App)
const pinia = createPinia()

app.use(router)

app.use(router)
app.use(pinia)

app.mount('#app')
console.log('App created:', app);
console.log('Router used:', router);