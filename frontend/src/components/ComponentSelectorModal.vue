<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-overlay__container">
      <div class="modal-overlay__header">
        <h2 class="modal-overlay__title">{{ categoryLabel }}</h2>
        <button class="modal-overlay__close-btn" @click="$emit('close')">✕</button>
      </div>

      <div class="modal-overlay__content-block" ref="scrollContainer" @scroll="handleScroll">
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
                <input class="filter-group__input" type="checkbox" :id="'cpu_socket_' + socket" :value="socket" v-model="selectedSockets">
                <label :for="'cpu_socket_' + socket" class="filter-group__label">{{ socket }}</label>
              </div>
            </div>
            <div v-if="categoryKey === 'cpu'" class="filter-group">
              <h4 class="filter-group__title">Количество ядер</h4>
              <div v-for="core in filterOptions.cores" :key="core" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'core_' + core" :value="core" v-model="selectedCores">
                <label :for="'core_' + core" class="filter-group__label">{{ core }}</label>
              </div>
            </div>

            <div v-if="categoryKey === 'gpu'" class="filter-group">
              <h4 class="filter-group__title">Объём памяти (ГБ)</h4>
              <div v-for="mem in filterOptions.memorySizes" :key="mem" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'mem_' + mem" :value="mem" v-model="selectedMemorySizes">
                <label :for="'mem_' + mem" class="filter-group__label">{{ mem }} ГБ</label>
              </div>
            </div>

            <div v-if="categoryKey === 'motherboard'" class="filter-group">
              <h4 class="filter-group__title">Сокет</h4>
              <div v-for="socket in filterOptions.sockets" :key="socket" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'mb_socket_' + socket" :value="socket" v-model="selectedSockets">
                <label :for="'mb_socket_' + socket" class="filter-group__label">{{ socket }}</label>
              </div>
            </div>
            <div v-if="categoryKey === 'motherboard'" class="filter-group">
              <h4 class="filter-group__title">Форм-фактор</h4>
              <div v-for="ff in filterOptions.formFactors" :key="ff" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'ff_' + ff" :value="ff" v-model="selectedFormFactors">
                <label :for="'ff_' + ff" class="filter-group__label">{{ ff }}</label>
              </div>
            </div>

            <div v-if="categoryKey === 'ram'" class="filter-group">
              <h4 class="filter-group__title">Тип памяти</h4>
              <div v-for="type in filterOptions.ramTypes" :key="type" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'type_' + type" :value="type" v-model="selectedRamTypes">
                <label :for="'type_' + type" class="filter-group__label">{{ type }}</label>
              </div>
            </div>
            <div v-if="categoryKey === 'ram'" class="filter-group">
              <h4 class="filter-group__title">Объём (ГБ)</h4>
              <div v-for="cap in filterOptions.capacities" :key="cap" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'cap_' + cap" :value="cap" v-model="selectedCapacities">
                <label :for="'cap_' + cap" class="filter-group__label">{{ cap }} ГБ</label>
              </div>
            </div>

            <div v-if="categoryKey === 'cpucooler'" class="filter-group">
              <h4 class="filter-group__title">Тип охлаждения</h4>
              <div class="filter-group__option">
                <input class="filter-group__input" type="checkbox" id="cooler_air" value="air" v-model="selectedCoolerTypes">
                <label for="cooler_air" class="filter-group__label">Воздушное</label>
              </div>
              <div class="filter-group__option">
                <input class="filter-group__input" type="checkbox" id="cooler_water" value="water" v-model="selectedCoolerTypes">
                <label for="cooler_water" class="filter-group__label">Жидкостное</label>
              </div>
            </div>
            <div v-if="categoryKey === 'cpucooler'" class="filter-group">
              <h4 class="filter-group__title">Размер вентилятора (мм)</h4>
              <div v-for="size in filterOptions.fanSizes" :key="size" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'cooler_size_' + size" :value="size" v-model="selectedFanSizes">
                <label :for="'cooler_size_' + size" class="filter-group__label">{{ size }} мм</label>
              </div>
            </div>

            <div v-if="categoryKey === 'storage'" class="filter-group">
              <h4 class="filter-group__title">Тип накопителя</h4>
              <div class="filter-group__option">
                <input class="filter-group__input" type="checkbox" id="storage_ssd" value="SSD" v-model="selectedStorageTypes">
                <label for="storage_ssd" class="filter-group__label">SSD</label>
              </div>
              <div class="filter-group__option">
                <input class="filter-group__input" type="checkbox" id="storage_hdd" value="HDD" v-model="selectedStorageTypes">
                <label for="storage_hdd" class="filter-group__label">HDD</label>
              </div>
            </div>
            <div v-if="categoryKey === 'storage'" class="filter-group">
              <h4 class="filter-group__title">Интерфейс</h4>
              <div v-for="iface in filterOptions.interfaces" :key="iface" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'iface_' + iface" :value="iface" v-model="selectedInterfaces">
                <label :for="'iface_' + iface" class="filter-group__label">{{ iface }}</label>
              </div>
            </div>
            <div v-if="categoryKey === 'storage'" class="filter-group">
              <h4 class="filter-group__title">Объём (ГБ)</h4>
              <div v-for="cap in filterOptions.storageCapacities" :key="cap" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'scap_' + cap" :value="cap" v-model="selectedStorageCapacities">
                <label :for="'scap_' + cap" class="filter-group__label">{{ cap }} ГБ</label>
              </div>
            </div>

            <div v-if="categoryKey === 'psu'" class="filter-group">
              <h4 class="filter-group__title">Мощность (Вт)</h4>
              <div v-for="watts in filterOptions.wattages" :key="watts" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'watts_' + watts" :value="watts" v-model="selectedWattages">
                <label :for="'watts_' + watts" class="filter-group__label">{{ watts }} Вт</label>
              </div>
            </div>
            <div v-if="categoryKey === 'psu'" class="filter-group">
              <h4 class="filter-group__title">Сертификат</h4>
              <div v-for="cert in filterOptions.certifications" :key="cert" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'cert_' + cert" :value="cert" v-model="selectedCertifications">
                <label :for="'cert_' + cert" class="filter-group__label">{{ cert }}</label>
              </div>
            </div>

            <div v-if="categoryKey === 'case'" class="filter-group">
              <h4 class="filter-group__title">Тип корпуса</h4>
              <div v-for="type in filterOptions.caseTypes" :key="type" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'case_type_' + type" :value="type" v-model="selectedCaseTypes">
                <label :for="'case_type_' + type" class="filter-group__label">{{ type }}</label>
              </div>
            </div>

            <div v-if="categoryKey === 'casefan'" class="filter-group">
              <h4 class="filter-group__title">Размер (мм)</h4>
              <div v-for="size in filterOptions.fanSizes" :key="size" class="filter-group__option">
                <input class="filter-group__input" type="checkbox" :id="'fan_size_' + size" :value="size" v-model="selectedFanSizes">
                <label :for="'fan_size_' + size" class="filter-group__label">{{ size }} мм</label>
              </div>
            </div>
            <div v-if="categoryKey === 'casefan'" class="filter-group">
              <h4 class="filter-group__title">PWM</h4>
              <div class="filter-group__option">
                <input class="filter-group__input" type="checkbox" id="fan_pwm" value="true" v-model="selectedPwm">
                <label for="fan_pwm" class="filter-group__label">С регулировкой оборотов</label>
              </div>
            </div>
            <div v-if="categoryKey === 'casefan'" class="filter-group">
              <h4 class="filter-group__title">Подсветка</h4>
              <div class="filter-group__option">
                <input class="filter-group__input" type="checkbox" id="fan_rgb" value="RGB" v-model="selectedLed">
                <label for="fan_rgb" class="filter-group__label">RGB</label>
              </div>
              <div class="filter-group__option">
                <input class="filter-group__input" type="checkbox" id="fan_argb" value="ARGB" v-model="selectedLed">
                <label for="fan_argb" class="filter-group__label">ARGB</label>
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
            <div v-if="isLoadingMore" class="modal-overlay__loading-more">Загрузка...</div>
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
const componentsList = ref([])
const loading = ref(true)
const selectedComponent = ref(null)

const nextPageUrl = ref(null)
const isLoadingMore = ref(false)
const scrollContainer = ref(null)
let currentPage = 1

// Состояние фильтров
const sortBy = ref('price_asc')
const selectedBrands = ref([])
const selectedSockets = ref([])
const maxPrice = ref(500000)
const priceRange = ref({ min: 0, max: 500000 })

const selectedCores = ref([])
const selectedMemorySizes = ref([])
const selectedFormFactors = ref([])
const selectedRamTypes = ref([])
const selectedCapacities = ref([])
const selectedCoolerTypes = ref([])
const selectedFanSizes = ref([])
const selectedStorageTypes = ref([])
const selectedInterfaces = ref([])
const selectedStorageCapacities = ref([])
const selectedWattages = ref([])
const selectedCertifications = ref([])
const selectedCaseTypes = ref([])
const selectedPwm = ref([])
const selectedLed = ref([])

// Доступные опции для фильтров
const filterOptions = ref({
  brands: [],
  sockets: [],
  cores: [],
  memorySizes: [],
  formFactors: [],
  ramTypes: [],
  capacities: [],
  fanSizes: [],
  interfaces: [],
  wattages: [],
  certifications: [],
  caseTypes: [],
  storageCapacities: [],
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

async function loadComponents(reset = true) {
  if (reset) {
    loading.value = true
    componentsList.value = []
    currentPage = 1
  }
  
  try {
    const response = await api.get(`/${props.categoryKey}/`, {
      params: { has_prices: true, page: currentPage, page_size: 20 }
    })
    const newItems = response.data.results || response.data
    
    if (reset) {
      componentsList.value = newItems
    } else {
      componentsList.value = [...componentsList.value, ...newItems]
    }

    nextPageUrl.value = newItems.length === 20 ? 'has_more' : null
    
    if (reset && componentsList.value.length) {
      calculatePriceRange()
      await loadFilterOptions()
    }
  } catch (error) {
    console.error('Ошибка загрузки компонентов', error)
  } finally {
    loading.value = false
  }
}

async function loadFilterOptions() {
  const items = componentsList.value
  
  const brands = [...new Set(items.map(c => c.brand).filter(b => b && b !== 'null' && b !== ''))]
  const sockets = [...new Set(items.map(c => c.socket).filter(Boolean))]
  const cores = [...new Set(items.map(c => c.cores_total).filter(Boolean))].sort((a, b) => a - b)
  const memorySizes = [...new Set(items.map(c => c.memory).filter(Boolean))].sort((a, b) => a - b)
  const formFactors = [...new Set(items.map(c => c.form_factor).filter(Boolean))]
  const ramTypes = [...new Set(items.map(c => c.ram_type).filter(Boolean))]
  const capacities = [...new Set(items.map(c => c.total_capacity).filter(Boolean))].sort((a, b) => a - b)
  const fanSizes = [...new Set(items.map(c => c.size).filter(Boolean))].sort((a, b) => a - b)
  const interfaces = [...new Set(items.map(c => c.interface).filter(Boolean))]
  const storageCapacities = [...new Set(items.map(c => c.capacity).filter(Boolean))].sort((a, b) => a - b)
  const wattages = [...new Set(items.map(c => c.wattage).filter(Boolean))].sort((a, b) => a - b)
  const certifications = [...new Set(items.map(c => c.efficiency_rating).filter(Boolean))]
  const caseTypes = [...new Set(items.map(c => c.case_type).filter(Boolean))]
  const caseFormFactors = [...new Set(items.map(c => c.form_factor).filter(Boolean))]
  
  filterOptions.value = { brands, sockets, cores, memorySizes, formFactors, ramTypes, capacities, interfaces, wattages, certifications, caseTypes, fanSizes, storageCapacities, caseFormFactors }
}

function calculatePriceRange() {
  const prices = componentsList.value.map(c => c.min_price).filter(p => p)
  if (prices.length) {
    priceRange.value.min = Math.min(...prices)
    priceRange.value.max = Math.max(...prices)
    maxPrice.value = priceRange.value.max
  }
}

async function loadMore() {
  if (!nextPageUrl.value || isLoadingMore.value || loading.value) return
  isLoadingMore.value = true
  currentPage++
  await loadComponents(false)
  isLoadingMore.value = false
  calculatePriceRange()
  loadFilterOptions()
}

function handleScroll(e) {
  const container = e.target
  const scrollBottom = container.scrollHeight - container.scrollTop - container.clientHeight
  
  if (scrollBottom < 200 && nextPageUrl.value && !isLoadingMore.value && !loading.value) {
    loadMore()
  }
}

const filteredAndSortedComponents = computed(() => {
  let result = [...componentsList.value]
  
  // Поиск
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(c => c.name.toLowerCase().includes(q))
  }

  if (selectedBrands.value.length) {
    result = result.filter(c => selectedBrands.value.includes(c.brand))
  }
  
  // Сокет (CPU, Motherboard)
  if (selectedSockets.value.length) {
    result = result.filter(c => selectedSockets.value.includes(c.socket))
  }

  // CPU
  if (props.categoryKey === 'cpu') {
    if (selectedCores.value.length) {
      result = result.filter(c => selectedCores.value.includes(c.cores_total))
    }
  }

  // GPU
  if (props.categoryKey === 'gpu') {
    if (selectedMemorySizes.value.length) {
      result = result.filter(c => selectedMemorySizes.value.includes(c.memory))
    }
  }

  // Motherboard
  if (props.categoryKey === 'motherboard') {
    if (selectedFormFactors.value.length) {
      result = result.filter(c => selectedFormFactors.value.includes(c.form_factor))
    }
  }

  // RAM
  if (props.categoryKey === 'ram') {
    if (selectedRamTypes.value.length) {
      result = result.filter(c => selectedRamTypes.value.includes(c.ram_type))
    }
    if (selectedCapacities.value.length) {
      result = result.filter(c => selectedCapacities.value.includes(c.total_capacity))
    }
  }

  // CPU Cooler
  if (props.categoryKey === 'cpucooler') {
    if (selectedCoolerTypes.value.length) {
      result = result.filter(c => {
        if (selectedCoolerTypes.value.includes('air') && c.water_cooled === false) return true
        if (selectedCoolerTypes.value.includes('water') && c.water_cooled === true) return true
        return false
      })
    }
    if (selectedFanSizes.value.length) {
      result = result.filter(c => selectedFanSizes.value.includes(c.size))
    }
  }

  // Storage
  if (props.categoryKey === 'storage') {
    if (selectedStorageTypes.value.length) {
      result = result.filter(c => selectedStorageTypes.value.includes(c.type))
    }
    if (selectedInterfaces.value.length) {
      result = result.filter(c => selectedInterfaces.value.includes(c.interface))
    }
    if (selectedStorageCapacities.value.length) {
      result = result.filter(c => selectedStorageCapacities.value.includes(c.capacity))
    }
  }

  // PSU
  if (props.categoryKey === 'psu') {
    if (selectedWattages.value.length) {
      result = result.filter(c => selectedWattages.value.includes(c.wattage))
    }
    if (selectedCertifications.value.length) {
      result = result.filter(c => selectedCertifications.value.includes(c.efficiency_rating))
    }
  }

  // Case
  if (props.categoryKey === 'case') {
    if (selectedCaseTypes.value.length) {
      result = result.filter(c => selectedCaseTypes.value.includes(c.case_type))
    }
    if (selectedFormFactors.value.length) {
      result = result.filter(c => selectedFormFactors.value.includes(c.supported_motherboard_form_factors))
    }
  }

  if (props.categoryKey === 'casefan') {
    if (selectedFanSizes.value.length) {
      result = result.filter(c => selectedFanSizes.value.includes(c.size))
    }
    if (selectedPwm.value.length) {
      result = result.filter(c => c.pwm === true)
    }
    if (selectedLed.value.length) {
      result = result.filter(c => selectedLed.value.includes(c.led))
    }
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
  selectedCoolerTypes.value = []
  selectedFanSizes.value = []
  selectedStorageTypes.value = []
  selectedInterfaces.value = []
  selectedStorageCapacities.value = []
  selectedWattages.value = []
  selectedCertifications.value = []
  selectedCaseTypes.value = []
  selectedPwm.value = []
  selectedLed.value = []
  selectedStorageCapacities.value = []
  maxPrice.value = priceRange.value.max
  searchQuery.value = ''
  sortBy.value = 'price_asc'
  currentPage = 1
  nextPageUrl.value = null
  loadComponents(true)
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

    @media screen and (max-width: 760px) {
      width: 95%;
    }
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid #e0e0e0;
    background: #f5f5f5;

    @media screen and (max-width: 760px) {
      padding: 12px;
    }

    @media screen and (max-width: 460px) {
      padding: 8px;
    }
  }

  &__title {
    font-size: 28px;
    font-weight: 700;

    @media screen and (max-width: 760px) {
      font-size: 22px;
    }

    @media screen and (max-width: 460px) {
      font-size: 18px;
    }
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

    @media screen and (max-width: 760px) {
      font-size: 22px;
    }

    @media screen and (max-width: 460px) {
      font-size: 18px;
    }
  }

  &__content-block {
    padding: 16px;
    overflow-y: auto;
    flex: 1;
    max-height: 85vh;

    @media screen and (max-width: 760px) {
      padding: 12px;
    }

    @media screen and (max-width: 760px) {
      padding: 8px;
    }
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

    @media screen and (max-width: 760px) {
      padding: 8px;
      font-size: 16px;
    }

    @media screen and (max-width: 460px) {
      font-size: 14px;
    }
  }

  &__loading {
    text-align: center;
    padding: 32px;
    color: #999;

    @media screen and (max-width: 760px) {
      padding: 12px;
    }
  }

  &__loading-more {
    text-align: center;
    padding: 16px;
    color: #999;
  }

  &__components-list {
    width: 100%;
    margin-left: 16px;
    display: flex;
    flex-direction: column;

    @media screen and (max-width: 760px) {
      margin-left: 12px;
    }

    @media screen and (max-width: 460px) {
      margin-left: 8px;
    }
  }

  &__filters-sidebar {
    width: 260px;
    padding: 0;

    @media screen and (max-width: 760px) {
      width: 200px;
    }

    @media screen and (max-width: 460px) {
      width: 120px;
    }
  }

  &__reset-btn {
    color: #fff;
    font-size: 16px;
    border: none;
    background-color: #FF4444;
    border-radius: 6px;
    padding: 6px;
    transition: 0.2s;

    &:hover {
      opacity: 0.8;
    }

    @media screen and (max-width: 460px) {
      font-size: 14px;
    }
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

  @media screen and (max-width: 760px) {
    padding: 12px;
  }

  @media screen and (max-width: 460px) {
    padding: 8px;
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

    @media screen and (max-width: 760px) {
      font-size: 20px;
    }

    @media screen and (max-width: 460px) {
      font-size: 18px;
      line-height: 20px;
    }
  }

  &__specs {
    font-size: 16px;
    font-weight: 400;
    margin-bottom: 8px;
    color: #666;

    @media screen and (max-width: 460px) {
      font-size: 14px;
    }
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

    @media screen and (max-width: 460px) {
      font-size: 14px;
    }
  }
}

.filter-group {
  width: 100%;
  margin-bottom: 8px;
  
  &__title {
    font-size: 16px;
    font-weight: 700;

    @media screen and (max-width: 460px) {
      font-size: 14px;
    }
  }

  &__select {
    width: 100%;
    font-size: 16px;
    font-weight: 500;
    border-radius: 4px;
    margin-top: 4px;

    @media screen and (max-width: 460px) {
      font-size: 14px;
    }
  }

  &__input {
    margin-right: 4px;
  }

  &__range {
    width: 100%;
  }

  &__label {
    font-size: 16px;

    @media screen and (max-width: 460px) {
      font-size: 14px;
    }
  }
}
</style>