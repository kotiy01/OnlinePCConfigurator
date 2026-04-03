import { createRouter, createWebHistory } from 'vue-router'
import ConfiguratorView from '../views/ConfiguratorView.vue'

const routes = [
  {
    path: '/',
    name: 'configurator',
    component: ConfiguratorView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router