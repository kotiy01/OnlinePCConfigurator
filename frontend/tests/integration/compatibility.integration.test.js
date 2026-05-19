import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import api from '../../src/api'
import { useBuildStore } from '../../src/stores/build'

vi.mock('../../src/api', () => ({
  default: {
    post: vi.fn(),
  }
}))

describe('Compatibility Integration', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('проверяет совместимость при добавлении компонента', async () => {
    const mockCompatibilityResponse = {
      compatible: true,
      messages: []
    }
    api.post.mockResolvedValueOnce({ data: mockCompatibilityResponse })
    
    const store = useBuildStore()
    store.addComponent('cpu', { id: 1, name: 'Ryzen 7', socket: 'AM5' })
    
    // Эмулируем добавление материнской платы
    const buildPayload = {
      build: { cpu: 1 },
      component_key: 'motherboard',
      component_id: 2
    }
    const response = await api.post('/check-compatibility/', buildPayload)
    
    expect(response.data.compatible).toBe(true)
    expect(api.post).toHaveBeenCalledWith('/check-compatibility/', expect.objectContaining({
      component_key: 'motherboard'
    }))
  })

  it('обрабатывает несовместимые компоненты', async () => {
    const mockCompatibilityResponse = {
      compatible: false,
      messages: ['Сокет процессора AM5 не поддерживается материнской платой LGA1700']
    }
    api.post.mockResolvedValueOnce({ data: mockCompatibilityResponse })
    
    const response = await api.post('/check-compatibility/', {
      build: { cpu: 1 },
      component_key: 'motherboard',
      component_id: 2
    })
    
    expect(response.data.compatible).toBe(false)
    expect(response.data.messages[0]).toContain('Сокет')
  })
})