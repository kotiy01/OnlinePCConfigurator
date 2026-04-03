import { defineStore } from 'pinia'

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
    },

    isComplete: (state) => {
      return state.components.cpu && 
             state.components.motherboard && 
             state.components.ram && 
             state.components.psu
    },
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
  },
})