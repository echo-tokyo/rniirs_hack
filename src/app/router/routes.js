import { Main, SignIn, NewsPage } from "@/pages";
import SignUp from '@/pages/signUp/SignUp.vue'

export const routes = [
  {
    path: '/signin',
    name: 'signin',
    component: SignIn,
  },
  {
    path: '/',
    name: 'main',
    component: Main,
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp,
  },
  {
    path: '/news/:id',
    name: 'news',
    component: NewsPage,
    props: true
  }
];
