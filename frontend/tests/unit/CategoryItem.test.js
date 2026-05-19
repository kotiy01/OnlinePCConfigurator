import { mount } from '@vue/test-utils'
import { setActivePinia, createPinia } from 'pinia'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import CategoryItem from '../../src/components/CategoryItem.vue'

vi.mock('../../src/stores/build', () => ({
  useBuildStore: vi.fn(() => ({
    components: { cpu: null, motherboard: null },
    totalPrice: 0,
    addComponent: vi.fn(),
    removeComponent: vi.fn(),
  })),
}))

describe('CategoryItem', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  const mockCategory = {
    key: 'cpu',
    label: 'Процессор',
    icon: 'cpu',
    emptytext: 'Не выбран',
  }

  it('отображает кнопку "Выбрать", когда компонент не выбран', () => {
    const wrapper = mount(CategoryItem, {
      props: {
        category: mockCategory,
        selectedComponent: null,
      },
    })
    expect(wrapper.text()).toContain('Выбрать')
    expect(wrapper.find('.category-item__price').exists()).toBe(false)
  })

  it('эмитит событие select при нажатии на кнопку "Выбрать"', async () => {
    const wrapper = mount(CategoryItem, {
      props: {
        category: mockCategory,
        selectedComponent: null,
      },
    })
    await wrapper.find('.category-item__btn').trigger('click')
    expect(wrapper.emitted('select')).toBeTruthy()
  })

  it('эмитит событие remove при нажатии на кнопку "Удалить"', async () => {
    const selectedComponent = {
      name: 'AMD Ryzen 7 7800X3D',
      price: 35000,
      shop_name: 'Regard.ru',
    }
    const wrapper = mount(CategoryItem, {
      props: {
        category: mockCategory,
        selectedComponent,
      },
    })
    await wrapper.find('.category-item__btn_red').trigger('click')
    expect(wrapper.emitted('remove')).toBeTruthy()
  })
})