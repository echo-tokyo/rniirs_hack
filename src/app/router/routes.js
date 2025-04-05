import { Main, SignIn } from "@/pages";
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
    path: '/signUp',
    name: 'signup',
    component: SignUp,
  }
];
