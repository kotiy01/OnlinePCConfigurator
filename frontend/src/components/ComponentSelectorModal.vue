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

        <div class="modal-overlay__content">
          <div class="modal-overlay__filters-sidebar">
            <div class="modal-overlay__filter-group filter-group">
              <h4 class="filter-group__title">Сортировка</h4>
              <select v-model="sortBy" class="filter-group__select">
                <option value="price_asc">От дешевых к дорогим</option>
                <option value="price_desc">От дорогих к дешевым</option>
                <option value="name_asc">По названию (А-Я)</option>
                <option value="name_desc">По названию (Я-А)</option>
              </select>
            </div>

            <div class="filter-group">
              <h4 class="filter-group__title">Макс. цена</h4>
              <input class="filter-group__range" type="range" v-model="maxPrice" :min="priceRange.min" :max="priceRange.max" step="100">
              <div class="filter-group__price-range">до {{ maxPrice }} ₽</div>
            </div>

            <div class="filter-group">
              <h4 class="filter-group__title">Производитель</h4>
              <div v-for="brand in filterOptions.brands" :key="brand" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'brand_' + brand" :value="brand" v-model="selectedBrands">
                <label :for="'brand_' + brand" class="filter-group__label">{{ brand }}</label>
              </div>
            </div>

            <div v-if="categoryKey === 'cpu'" class="filter-group">
              <h4 class="filter-group__title">Сокет</h4>
              <div v-for="socket in filterOptions.sockets" :key="socket" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="socket" :value="socket" v-model="selectedSockets">
                <label :for="socket" class="filter-group__label">{{ socket }}</label>
              </div>
            </div>

            <div v-if="categoryKey === 'cpu'" class="filter-group">
              <h4 class="filter-group__title">Количество ядер</h4>
              <div v-for="core in filterOptions.cores" :key="core" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="`core_${core}`" :value="core" v-model="selectedCores">
                <label :for="`core_${core}`" class="filter-group__label">{{ core }}</label>
              </div>
            </div>

            <!-- Фильтры для видеокарты -->
            <div v-if="categoryKey === 'gpu'" class="filter-group">
              <h4 class="filter-group__title">Объем памяти (ГБ)</h4>
              <div v-for="mem in filterOptions.memorySizes" :key="mem" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="`mem_${mem}`" :value="mem" v-model="selectedMemorySizes">
                <label :for="`mem_${mem}`" class="filter-group__label">{{ mem }} ГБ</label>
              </div>
            </div>

            <!-- Фильтры для материнской платы -->
            <div v-if="categoryKey === 'motherboard'" class="filter-group">
              <h4 class="filter-group__title">Сокет</h4>
              <div v-for="socket in filterOptions.sockets" :key="socket" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="socket" :value="socket" v-model="selectedSockets">
                <label :for="socket" class="filter-group__label">{{ socket }}</label>
              </div>
            </div>

            <div v-if="categoryKey === 'motherboard'" class="filter-group">
              <h4 class="filter-group__title">Форм-фактор</h4>
              <div v-for="ff in filterOptions.formFactors" :key="ff" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="ff" :value="ff" v-model="selectedFormFactors">
                <label :for="ff" class="filter-group__label">{{ ff }}</label>
              </div>
            </div>

            <!-- Фильтры для оперативной памяти -->
            <div v-if="categoryKey === 'ram'" class="filter-group">
              <h4 class="filter-group__title">Тип памяти</h4>
              <div v-for="type in filterOptions.ramTypes" :key="type" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="type" :value="type" v-model="selectedRamTypes">
                <label :for="type" class="filter-group__label">{{ type }}</label>
              </div>
            </div>

            <div v-if="categoryKey === 'ram'" class="filter-group">
              <h4 class="filter-group__title">Объем (ГБ)</h4>
              <div v-for="cap in filterOptions.capacities" :key="cap" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="`cap_${cap}`" :value="cap" v-model="selectedCapacities">
                <label :for="`cap_${cap}`" class="filter-group__label">{{ cap }} ГБ</label>
              </div>
            </div>

            <!-- Фильтры для оперативной памяти -->
            <div v-if="categoryKey === 'cpucooler'" class="filter-group">
              <h4 class="filter-group__title">Тип охлаждения</h4>
              <div v-for="type in filterOptions.ramTypes" :key="type" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="type" :value="type" v-model="selectedRamTypes">
                <label :for="type" class="filter-group__label">{{ type }}</label>
              </div>
            </div>

            <button class="modal-overlay__reset-btn" @click="resetFilters">Сбросить все</button>
          </div>

          <div v-if="loading" class="modal-overlay__loading">Загрузка...</div>
          <div v-else class="modal-overlay__components-list">
            <div
              v-for="comp in filteredAndSortedComponents"
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
import { ref, computed, onMounted, watch } from 'vue'
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

// Состояние фильтров
const sortBy = ref('price_asc')
const selectedBrands = ref([])
const selectedSockets = ref([])
const selectedCores = ref([])
const selectedMemorySizes = ref([])
const selectedFormFactors = ref([])
const selectedRamTypes = ref([])
const selectedCapacities = ref([])
const maxPrice = ref(500000)
const priceRange = ref({ min: 0, max: 500000 })

// Доступные опции для фильтров
const filterOptions = ref({
  brands: [],
  sockets: [],
  cores: [],
  memorySizes: [],
  formFactors: [],
  ramTypes: [],
  capacities: [],
})


// const filteredComponents = computed(() => {
//   if (!searchQuery.value) return components.value
//   const q = searchQuery.value.toLowerCase()
//   return components.value.filter(c => c.name.toLowerCase().includes(q))
// })

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
    return `${comp.cores_total || '?'} ядер, ${comp.threads || '?'} потоков, ${comp.socket || '?'}`
  }
  if (props.categoryKey === 'motherboard') {
    return `${comp.socket || '?'}, ${comp.form_factor || '?'}, ${comp.memory_type || '?'}`
  }
  if (props.categoryKey === 'gpu') {
    return `${comp.memory || '?'} ГБ, ${comp.memory_type || '?'}, ${comp.interface || '?'}`
  }
  if (props.categoryKey === 'ram') {
    return `${comp.ram_type || '?'}, ${comp.total_capacity || '?'} ГБ, ${comp.speed || '?'} МГц`
  }
  if (props.categoryKey === 'storage') {
    return `${comp.interface || '?'}, ${comp.capacity || '?'} ГБ,`
  }
  if (props.categoryKey === 'cooler') {
    return `${comp.cpu_sockets || '?'}, высота ${comp.height || '?'} мм`
  }
  if (props.categoryKey === 'psu') {
    return `${comp.wattage || '?'} Вт, ${comp.form_factor || '?'}, ${comp.efficiency_rating || '?'}`
  }
  if (props.categoryKey === 'case') {
    return `${comp.case_type || '?'}, ${comp.supported_motherboard_form_factors || '?'}`
  }
  if (props.categoryKey === 'casefan') {
    return `${comp.size || '?'} мм, ${comp.quantity || '?'} шт.`
  }
  return ''
}

// Загрузка компонентов
onMounted(async () => {
  await loadComponents()
  await loadFilterOptions()
})

async function loadComponents() {
  try {
    const response = await api.get(`/${props.categoryKey}/?has_prices=true`)
    components.value = response.data.results || response.data
    calculatePriceRange()
  } catch (error) {
    console.error('Ошибка загрузки компонентов', error)
  }
}

async function loadFilterOptions() {
  try {
    const response = await api.get(`/${props.categoryKey}/`)

    const items = components.value
    
    // Уникальные значения для фильтров из данных
    const brands = [...new Set(items.map(c => c.brand).filter(b => b && b !== 'null' && b !== ''))]
    const sockets = [...new Set(items.map(c => c.socket).filter(Boolean))]
    const cores = [...new Set(items.map(c => c.cores_total).filter(Boolean))].sort((a, b) => a - b)
    const memorySizes = [...new Set(items.map(c => c.memory).filter(Boolean))].sort((a, b) => a - b)
    const formFactors = [...new Set(items.map(c => c.form_factor).filter(Boolean))]
    const ramTypes = [...new Set(items.map(c => c.ram_type).filter(Boolean))]
    const capacities = [...new Set(items.map(c => c.total_capacity).filter(Boolean))].sort((a, b) => a - b)
    
    filterOptions.value = { brands, sockets, cores, memorySizes, formFactors, ramTypes, capacities }
  } catch (error) {
    console.error('Ошибка загрузки фильтров', error)
  }
}

function calculatePriceRange() {
  const prices = components.value.map(c => c.min_price).filter(p => p)
  if (prices.length) {
    priceRange.value.min = Math.min(...prices)
    priceRange.value.max = Math.max(...prices)
    maxPrice.value = priceRange.value.max
  }
}

const filteredAndSortedComponents = computed(() => {
  let result = [...components.value]
  
  // Поиск
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(c => c.name.toLowerCase().includes(q))
  }
  
  // Фильтры по категориям
  if (selectedBrands.value.length) {
    result = result.filter(c => selectedBrands.value.includes(c.brand))
  }
  
  if (selectedSockets.value.length) {
    result = result.filter(c => selectedSockets.value.includes(c.socket))
  }
  
  if (selectedCores.value.length && props.categoryKey === 'cpu') {
    result = result.filter(c => selectedCores.value.includes(c.cores_total))
  }
  
  if (selectedMemorySizes.value.length && props.categoryKey === 'gpu') {
    result = result.filter(c => selectedMemorySizes.value.includes(c.memory))
  }
  
  if (selectedFormFactors.value.length && props.categoryKey === 'motherboard') {
    result = result.filter(c => selectedFormFactors.value.includes(c.form_factor))
  }
  
  if (selectedRamTypes.value.length && props.categoryKey === 'ram') {
    result = result.filter(c => selectedRamTypes.value.includes(c.ram_type))
  }
  
  if (selectedCapacities.value.length && props.categoryKey === 'ram') {
    result = result.filter(c => selectedCapacities.value.includes(c.total_capacity))
  }
  
  // Фильтр по цене
  result = result.filter(c => (c.min_price || 0) <= maxPrice.value)
  
  // Сортировка
  if (sortBy.value === 'price_asc') {
    result.sort((a, b) => (a.min_price || 0) - (b.min_price || 0))
  } else if (sortBy.value === 'price_desc') {
    result.sort((a, b) => (b.min_price || 0) - (a.min_price || 0))
  } else if (sortBy.value === 'name_asc') {
    result.sort((a, b) => (a.name || '').localeCompare(b.name || ''))
  } else if (sortBy.value === 'name_desc') {
    result.sort((a, b) => (b.name || '').localeCompare(a.name || ''))
  }
  
  return result
})

function resetFilters() {
  selectedBrands.value = []
  selectedSockets.value = []
  selectedCores.value = []
  selectedMemorySizes.value = []
  selectedFormFactors.value = []
  selectedRamTypes.value = []
  selectedCapacities.value = []
  maxPrice.value = priceRange.value.max
  searchQuery.value = ''
  sortBy.value = 'price_asc'
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
    background: #f5f5f5;
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
    padding: 16px;
    border-bottom: 1px solid #e0e0e0;
    background: #f5f5f5;
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

  &__content {
    display: flex;
    flex-direction: row;
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
    width: 100%;
    margin-left: 16px;
    display: flex;
    flex-direction: column;
    // grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
    // gap: 16px;
  }

  &__filters-sidebar {
    width: 260px;
    padding: 0;
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
  background-color: #fff;
  max-height: 190px;
  height: fit-content;
  margin-bottom: 16px;

  &:hover {
    box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);
  }

  &__name {
    font-weight: 700;
    min-height: 28px;
    max-height: 56px;
    width: 100%;
    margin-bottom: 4px;
    font-size: 22px;
    line-height: 28px;
    overflow-x: clip;
    overflow-y: clip;
    // white-space: nowrap;
    text-overflow: ellipsis;
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
    transition: 0.2s;
    
    &:hover {
      background-color: #4895ef;
    }
  }
}

.filter-group {
  width: 100%;
  margin-bottom: 8px;
  
  &__title {
    font-size: 16px;
    font-weight: 700;
  }

  &__select {
    width: 100%;
    font-size: 16px;
    font-weight: 500;
    border-radius: 4px;
    margin-top: 4px;
  }

  &__input {
    margin-right: 4px;
  }

  &__range {
    width: 100%;
  }

  &__label {
    font-size: 16px;
  }
}
</style>