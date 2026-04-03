import api from './index'

export const componentApi = {
  // Получение списка комплектующих по категории
  getCPU(params = {}) {
    return api.get('/cpu/', { params })
  },
  getMotherboard(params = {}) {
    return api.get('/motherboard/', { params })
  },
  getGPU(params = {}) {
    return api.get('/gpu/', { params })
  },
  getRAM(params = {}) {
    return api.get('/ram/', { params })
  },
  getStorage(params = {}) {
    return api.get('/storage/', { params })
  },
  getPSU(params = {}) {
    return api.get('/psu/', { params })
  },
  getCase(params = {}) {
    return api.get('/case/', { params })
  },
  getCooler(params = {}) {
    return api.get('/cooler/', { params })
  },
  getCaseFan(params = {}) {
    return api.get('/casefan/', { params })
  },
  // Проверка совместимости
  checkCompatibility(build) {
    return api.post('/check-compatibility/', { build })
  },
}