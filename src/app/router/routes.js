import { Main, SignIn, NewsPage } from "@/pages";

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
    path: '/news/:id',
    name: 'news',
    component: NewsPage,
    props: true
  }
];
