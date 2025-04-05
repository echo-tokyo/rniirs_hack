import App from './App.vue';
import '../assets/global.scss'
import '../assets/reset.scss'
import { router } from './router/index';
import { createApp } from 'vue'

// const pinia = createPinia();

export const app = createApp(App)
  // .use(pinia)
  .use(router);