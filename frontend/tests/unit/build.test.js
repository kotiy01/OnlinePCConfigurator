// frontend/tests/unit/stores/build.test.js
import { setActivePinia, createPinia } from 'pinia'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useBuildStore } from '../../src/stores/build'

describe('Build Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('добавляет компонент в сборку', () => {
    const store = useBuildStore()
    const cpu = { id: 1, name: 'Ryzen 7', price: 35000, shop_name: 'Regard.ru' }
    store.addComponent('cpu', cpu)
    expect(store.components.cpu).toEqual(cpu)
  })

  it('удаляет компонент из сборки', () => {
    const store = useBuildStore()
    store.addComponent('cpu', { id: 1, name: 'Ryzen 7', price: 35000 })
    store.removeComponent('cpu')
    expect(store.components.cpu).toBeNull()
  })

  it('очищает всю сборку', () => {
    const store = useBuildStore()
    store.addComponent('cpu', { price: 35000 })
    store.addComponent('gpu', { price: 60000 })
    store.clearBuild()
    expect(store.components.cpu).toBeNull()
    expect(store.components.gpu).toBeNull()
    expect(store.currentBuildId).toBeNull()
  })
})