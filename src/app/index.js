import App from './App.vue';
import '../assets/reset.scss'
import '../assets/global.scss'
import { router } from './router/index';
import { createApp } from 'vue'
import { createPinia } from 'pinia'

const pinia = createPinia();

export const app = createApp(App)
  .use(pinia)
  .use(router);