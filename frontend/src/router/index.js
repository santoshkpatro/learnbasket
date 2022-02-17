import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import About from '../pages/About.vue'
import Auth from '../pages/Auth.vue'

const routes = [
  {
    name: 'Home',
    path: '/',
    component: Home,
  },
  {
    name: 'About',
    path: '/about',
    component: About,
  },
  {
    path: '/auth',
    component: Auth,
    children: [
      {
        name: 'Login',
        path: 'login',
        component: () => import('../pages/auth/Login.vue'),
      },
      {
        name: 'Register',
        path: 'register',
        component: () => import('../pages/auth/Register.vue'),
      },
      {
        name: 'Profile',
        path: 'profile',
        component: () => import('../pages/auth/Profile.vue'),
        meta: { requiresAuth: true },
      },
      {
        name: 'EmailVerify',
        path: 'email_verify',
        component: () => import('../pages/auth/EmailVerify.vue'),
      },
      {
        name: 'GoogleCallback',
        path: 'oauth/google/callback',
        component: () => import('../pages/auth/oauth/GoogleCallback.vue'),
      },
    ],
  },
  {
    path: '/dashboard',
    component: () => import('../pages/Dashboard.vue'),
    children: [
      {
        name: 'Overview',
        path: '',
        component: () => import('../pages/dashboard/Overview.vue'),
        meta: { requiresAuth: true },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('access_token')

  if (to.matched.some((record) => record.meta.requiresAuth && !loggedIn)) {
    next({
      path: '/auth/login',
      query: { redirect: to.fullPath },
    })
  } else {
    next()
  }
})

export default router
