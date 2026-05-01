import { defineStore } from 'pinia'
import api from '../api'

export const useBuildStore = defineStore('build', {
  state: () => ({
    components: {
      cpu: null,
      motherboard: null,
      ram: null,
      gpu: null,
      cooler: null,
      storage: null,
      psu: null,
      case: null,
      casefan: null,
    },
    savedBuilds: [],
    currentBuildId: null,
  }),

  getters: {
    totalPrice: (state) => {
      let sum = 0
      for (const key in state.components) {
        const comp = state.components[key]
        if (comp && comp.min_price) {
          sum += comp.min_price
        }
      }
      return sum
    }
  },

  actions: {
    addComponent(category, component) {
      this.components[category] = component
      this.saveToLocalStorage()
    },

    removeComponent(category) {
      this.components[category] = null
      this.saveToLocalStorage()
    },

    clearBuild() {
      for (const key in this.components) {
        this.components[key] = null
      }
      this.saveToLocalStorage()
    },

    saveToLocalStorage() {
      const toSave = {}
      for (const key in this.components) {
        if (this.components[key]) {
          toSave[key] = this.components[key]
        }
      }
      localStorage.setItem('pc_build', JSON.stringify(toSave))
    },

    loadFromLocalStorage() {
      const saved = localStorage.getItem('pc_build')
      if (saved) {
        try {
          const parsed = JSON.parse(saved)
          for (const key in parsed) {
            this.components[key] = parsed[key]
          }
        } catch (e) {
          console.error('Ошибка загрузки сохраненной сборки', e)
        }
      }
    },

    async saveCurrentBuild(name) {
      const buildData = {
        components: this.components,
        totalPrice: this.totalPrice,
      }
      
      try {
        // Всегда создается новая сборка, не обновляются старые
        const response = await api.post('/saved-builds/', {
          name,
          build_data: buildData
        })
        
        this.currentBuildId = response.data.id
        await this.loadSavedBuilds()
        
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Error saving build:', error)
        return { success: false, error: error.response?.data }
      }
    },
    
    async loadSavedBuilds() {
      try {
        const response = await api.get('/saved-builds/')
        if (response.data.results) {
          this.savedBuilds = response.data.results
        } else if (Array.isArray(response.data)) {
          this.savedBuilds = response.data
        } else {
          this.savedBuilds = []
        }
        // console.log('Loaded builds:', this.savedBuilds) // отладка
        return { success: true, data: this.savedBuilds }
      } catch (error) {
        console.error('Error loading builds:', error)
        this.savedBuilds = []
        return { success: false, error: error.response?.data }
      }
    },
    
    async deleteSavedBuild(buildId) {
      try {
        await api.delete(`/saved-builds/${buildId}/`)
        this.savedBuilds = this.savedBuilds.filter(b => b.id !== buildId)
        
        // Если удаляется текущая сборка, сбрасывается currentBuildId
        if (this.currentBuildId === buildId) {
          this.currentBuildId = null
          this.isNewBuild = true
        }
        
        return { success: true }
      } catch (error) {
        console.error('Error deleting build:', error)
        return { success: false, error: error.response?.data }
      }
    },
    
    async loadBuildToConfigurator(build) {
      if (build && build.build_data && build.build_data.components) {
        this.clearBuild() // очистка конфигурации перед загрузкой новой
        this.components = build.build_data.components
        this.currentBuildId = build.id
        return { success: true }
      }
      return { success: false, error: 'Некорректные данные сборки' }
    }
  }
})