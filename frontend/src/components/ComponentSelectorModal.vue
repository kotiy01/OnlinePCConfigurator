<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-overlay__container">
      <div class="modal-overlay__header">
        <h2 class="modal-overlay__title">{{ categoryLabel }}</h2>
        <button class="modal-overlay__close-btn" @click="$emit('close')">✕</button>
      </div>
      <div class="modal-overlay__content-block">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Поиск по названию..."
          class="modal-overlay__search-input"
        />
        <div v-if="loading" class="modal-overlay__loading">Загрузка...</div>
        <div v-else class="modal-overlay__components-list">
          <div
            v-for="comp in filteredComponents"
            :key="comp.id"
            class="component-card modal-overlay__component-card"
            @click="openDetail(comp)"
          >
            <h3 class="component-card__name">{{ comp.name }}</h3>
            <p class="component-card__specs">{{ shortSpecs(comp) }}</p>
            <p class="component-card__price">Выбрать от {{ comp.min_price }} ₽</p>
          </div>
        </div>
      </div>
    </div>
    <ComponentDetailModal
      v-if="selectedComponent"
      :component="selectedComponent"
      :category-key="categoryKey"
      @close="selectedComponent = null"
      @select="onSelectFromDetail"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api/index'
import ComponentDetailModal from './ComponentDetailModal.vue'

const props = defineProps({
  categoryKey: String,
  categoryLabel: String,
})

const emit = defineEmits(['close', 'select'])

const searchQuery = ref('')
const components = ref([])
const loading = ref(true)
const selectedComponent = ref(null)

const filteredComponents = computed(() => {
  if (!searchQuery.value) return components.value
  const q = searchQuery.value.toLowerCase()
  return components.value.filter(c => c.name.toLowerCase().includes(q))
})

onMounted(async () => {
  try {
    const response = await api.get(`/${props.categoryKey}/`, {
      params: { has_prices: true }
    })
    components.value = response.data.results || response.data
  } catch (error) {
    console.error('Ошибка загрузки компонентов', error)
  } finally {
    loading.value = false
  }
})

function shortSpecs(comp) {
  if (props.categoryKey === 'cpu') {
    return `${comp.cores_total || '?'} ядер, ${comp.socket || '?'}`
  }
  if (props.categoryKey === 'motherboard') {
    return `${comp.socket || '?'}, ${comp.form_factor || '?'}, ${comp.memory_type || '?'}`
  }
  if (props.categoryKey === 'gpu') {
    return `${comp.memory || '?'} ГБ`
  }
  if (props.categoryKey === 'ram') {
    return `${comp.total_capacity || '?'} ГБ, ${comp.ram_type || '?'}`
  }
  if (props.categoryKey === 'storage') {
    return `${comp.capacity || '?'} ГБ, ${comp.interface || '?'}`
  }
  if (props.categoryKey === 'psu') {
    return `${comp.wattage || '?'} Вт`
  }
  if (props.categoryKey === 'case') {
    return `${comp.case_type || '?'}`
  }
  if (props.categoryKey === 'casefan') {
    return `${comp.size || '?'} мм, ${comp.quantity || '?'} шт.`
  }
  return ''
}

function openDetail(comp) {
  selectedComponent.value = comp
}

function onSelectFromDetail(shopItem) {
  emit('select', shopItem)
  selectedComponent.value = null
  emit('close')
}
</script>

<style lang="scss">
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;

  &__container {
    background: white;
    width: 90%;
    max-width: 1200px;
    max-height: 85vh;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #e0e0e0;
    background: #f8f9fa;
  }

  &__title {
    font-size: 28px;
    font-weight: 700;
  }

  &__close-btn {
    background: none;
    border: none;
    font-size: 28px;
    font-weight: 700;
    cursor: pointer;
    color: #999;
    transition: 0.2s;

    &:hover {
      color: red;
    }
  }

  &__content-block {
    padding: 16px;
    overflow-y: auto;
    flex: 1;
  }

  &__search-input {
    width: 100%;
    padding: 16px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    font-size: 18px;
    margin-bottom: 16px;
    box-sizing: border-box;
  }

  &__loading {
    text-align: center;
    padding: 32px;
    color: #999;
  }

  &__components-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
    gap: 16px;
  }
}

.component-card {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  flex-direction: column;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: 0.2s;

  &:hover {
    box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);
  }

  &__name {
    font-weight: 700;
    margin-bottom: 8px;
    font-size: 22px;
  }

  &__specs {
    font-size: 16px;
    font-weight: 400;
    margin-bottom: 8px;
    color: #666;
  }

  &__price {
    font-size: 18px;
    font-weight: 500;
    padding: 8px;
    color: white;
    background-color: #4361ee;
    border-radius: 4px;
    
    &:hover {
      background-color: #4895ef;
    }
  }
}
</style>