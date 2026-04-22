import { createRouter, createWebHistory } from 'vue-router'
import ConfiguratorView from '../views/ConfiguratorView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'configurator',
    component: ConfiguratorView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { title: 'Вход', guest: true },
  },
  { 
    path: '/register', 
    name: 'register',
    component: RegisterView, 
    meta: { title: 'Регистрация', guest: true } 
  },
  { 
    path: '/profile', 
    name: 'profile',
    component: ProfileView, 
    meta: { title: 'Профиль', auth: true } 
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Проверка токена при загрузке
  if (!authStore.isAuthenticated && localStorage.getItem('access_token')) {
    await authStore.fetchProfile()
  }
  
  if (to.meta.auth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next('/profile')
  } else {
    next()
  }
})

export default router