import { createRouter, createWebHistory } from 'vue-router'
import ConfiguratorView from '../views/ConfiguratorView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
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
    meta: { title: 'Вход - Онлайн-конфигуратор ПК', guest: true, description: 'Войдите в свой аккаунт, чтобы сохранять сборки ПК и управлять ими.' },
  },
  { 
    path: '/register', 
    name: 'register',
    component: RegisterView, 
    meta: { title: 'Регистрация - Онлайн-конфигуратор ПК', guest: true, description: 'Создайте аккаунт, чтобы сохранять сборки ПК, делиться ими и возвращаться к ним позже.' } 
  },
  { 
    path: '/profile', 
    name: 'profile',
    component: ProfileView, 
    meta: { title: 'Личный кабинет - мои сборки ПК', auth: true, description: 'Ваши сохранённые сборки. Открывайте, редактируйте или делитесь ссылкой на конфигурацию.' } 
  },
  { 
    path: '/:pathMatch(.*)*', 
    name: 'NotFound',
    component: NotFoundView,
    meta: { title: '404 - Страница не найдена', description: 'Запрашиваемая страница не существует. Вернитесь на главную и попробуйте снова.' }
  }
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

router.beforeEach((to, from, next) => {
  const defaultTitle = 'Онлайн-конфигруатор ПК с проверкой совместимости и агрегатором цен'
  const defaultDescription = 'Выбирай комплектующие а конфигуратор ПК проверит их совместимость! Сравнивай цены в магазинах и выбирай наилучшее предложение!'
  
  document.title = to.meta.title || defaultTitle
  
  const description = to.meta.description || defaultDescription
  let descriptionTag = document.querySelector('meta[name="description"]')
  if (!descriptionTag) {
    descriptionTag = document.createElement('meta')
    descriptionTag.setAttribute('name', 'description')
    document.head.appendChild(descriptionTag)
  }
  descriptionTag.setAttribute('content', description)
  
  next()
})

export default router