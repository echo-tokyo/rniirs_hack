import { Main, SignIn, NewsPage, Requests } from "@/pages";
import SignUp from '@/pages/signUp/SignUp.vue'
import RequestPreview from '@/pages/requestPreview/RequestPreview.vue'

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
  },
  {
    path: '/requests',
    name: 'requests',
    component: Requests,
  },
  {
    path: '/requests/:id',
    name: 'request-preview',
    component: RequestPreview,
    props: true
  }
];
