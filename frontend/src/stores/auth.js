import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
  }),
  getters: {
    isLoggedIn: (state) => state.isAuthenticated,
    currentUser: (state) => state.user,
  },
  actions: {
    async register(username, email, password, password2) {
      try {
        const response = await api.post('/auth/register/', { username, email, password, password2 })
        this.user = response.data.user
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        this.isAuthenticated = true
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data || 'Ошибка регистрации' }
      }
    },
    async login(username, password) {
      try {
        const response = await api.post('/auth/login/', { username, password })
        this.user = response.data.user
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        this.isAuthenticated = true
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || 'Ошибка входа' }
      }
    },
    async logout() {
      const refresh = localStorage.getItem('refresh_token')
      if (refresh) {
        try {
          await api.post('/auth/logout/', { refresh })
        } catch (e) {}
      }
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
    async fetchProfile() {
      try {
        const response = await api.get('/auth/profile/')
        this.user = response.data
        this.isAuthenticated = true
        return true
      } catch (error) {
        this.user = null
        this.isAuthenticated = false
        return false
      }
    },
  },
})