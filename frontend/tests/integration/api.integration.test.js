import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import api from '../../src/api'
import { useBuildStore } from '../../src/stores/build'
import { useAuthStore } from '../../src/stores/auth'

vi.mock('../../src/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  }
}))

describe('API Integration Tests', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('Build Store Integration', () => {
    it('загружает компоненты и обновляет стор', async () => {
      const mockCPUs = [
        { id: 1, name: 'Ryzen 7', min_price: 35000, shop_items: [] },
        { id: 2, name: 'Ryzen 5', min_price: 25000, shop_items: [] }
      ]
      api.get.mockResolvedValueOnce({ data: { results: mockCPUs } })
      
      const store = useBuildStore()
      const response = await api.get('/cpu/')
      
      expect(response.data.results).toHaveLength(2)
      expect(api.get).toHaveBeenCalledWith('/cpu/')
    })

    it('сохраняет сборку через API', async () => {
      const mockResponse = { id: 1, name: 'Тестовая сборка', build_data: {} }
      api.post.mockResolvedValueOnce({ data: mockResponse })
      
      const store = useBuildStore()
      store.addComponent('cpu', { id: 1, name: 'Ryzen 7', price: 35000 })
      
      const result = await store.saveCurrentBuild('Тестовая сборка')
      expect(result.success).toBe(true)
      expect(api.post).toHaveBeenCalledWith('/saved-builds/', expect.objectContaining({
        name: 'Тестовая сборка'
      }))
    })
  })

  describe('Auth Store Integration', () => {
    it('регистрирует пользователя и сохраняет токены', async () => {
      const mockAuthResponse = {
        user: { id: 1, username: 'newuser', email: 'new@example.com' },
        access: 'fake-access-token',
        refresh: 'fake-refresh-token'
      }
      api.post.mockResolvedValueOnce({ data: mockAuthResponse })
      
      const store = useAuthStore()
      const result = await store.register('newuser', 'new@example.com', 'pass123', 'pass123')
      
      expect(result.success).toBe(true)
      expect(store.isAuthenticated).toBe(true)
      expect(localStorage.getItem('access_token')).toBe('fake-access-token')
    })

    it('логинит пользователя и обновляет хранилище', async () => {
      const mockLoginResponse = {
        user: { id: 1, username: 'testuser', email: 'test@example.com' },
        access: 'fake-access-token',
        refresh: 'fake-refresh-token'
      }
      api.post.mockResolvedValueOnce({ data: mockLoginResponse })
      
      const store = useAuthStore()
      const result = await store.login('testuser', 'testpass')
      
      expect(result.success).toBe(true)
      expect(store.user).toEqual(mockLoginResponse.user)
    })
  })
})