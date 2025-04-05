import { Main, SignIn } from "@/pages";

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
];
