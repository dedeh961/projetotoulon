import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';

const app = createApp(App);

axios.defaults.baseURL = 'http://localhost:8000';  // FastAPI

app.mount('#app');
