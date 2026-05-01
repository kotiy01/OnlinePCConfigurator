<template>
  <div class="main">
    <h1 class="main__title">Онлайн-конфигуратор ПК с проверкой cовместимости и агрегатором цен</h1>
    <div class="main__configurator-block configurator-block">
      <div class="configurator-block__items">
        <CategoryItem
          v-for="cat in categories"
          :key="cat.key"
          :category="cat"
          :selectedComponent="buildStore.components[cat.key]"
          @select="openSelector(cat.key, cat.label)"
          @remove="buildStore.removeComponent(cat.key)"
        />
      </div>
      <div class="configurator-block__info">
        <SelectedComponentsList />
      </div>

      <ComponentSelectorModal
        v-if="modalVisible"
        :categoryKey="currentCategory"
        :categoryLabel="currentCategoryLabel"
        @close="modalVisible = false"
        @select="onComponentSelected"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBuildStore } from '../stores/build'
import api from '../api/index'
import CategoryItem from '../components/CategoryItem.vue'
import SelectedComponentsList from '../components/SelectedComponentsList.vue'
import ComponentSelectorModal from '../components/ComponentSelectorModal.vue'

const buildStore = useBuildStore()
const route = useRoute()

const categories = [
  { key: 'cpu', label: 'Процессор', emptytext: 'Не выбран' },
  { key: 'motherboard', label: 'Материнская плата', emptytext: 'Не выбрана' },
  { key: 'ram', label: 'Оперативная память', emptytext: 'Не выбрана' },
  { key: 'gpu', label: 'Видеокарта', emptytext: 'Не выбрана' },
  { key: 'cooler', label: 'Охлаждение процессора', emptytext: 'Не выбрано' },
  { key: 'storage', label: 'Накопитель', emptytext: 'Не выбран' },
  { key: 'psu', label: 'Блок питания', emptytext: 'Не выбран' },
  { key: 'case', label: 'Корпус', emptytext: 'Не выбран' },
  { key: 'casefan', label: 'Корпусное охлаждение', emptytext: 'Не выбрано' },
]

const modalVisible = ref(false)
const currentCategory = ref('')
const currentCategoryLabel = ref('')

onMounted(async () => {
  // console.log('=== ConfiguratorView mounted ===')
  
  // Загрузка из localStorage
  buildStore.loadFromLocalStorage()
  // console.log('After localStorage load, components:', JSON.parse(JSON.stringify(buildStore.components)))
  
  const buildId = route.query.build_id
  // console.log('build_id from URL:', buildId)
  
  if (buildId) {
    // console.log('Loading build from API...')
    try {
      const response = await api.get(`/public-build/${buildId}/`)
      // console.log('API response status:', response.status)
      // console.log('API response data:', response.data)
      
      if (response.data && response.data.build_data && response.data.build_data.components) {
        // console.log('Components from API:', Object.keys(response.data.build_data.components))
        
        // Очистка текущей сборки
        buildStore.clearBuild()
        // console.log('After clearBuild, components:', buildStore.components)
        
        // Загрузка компоненты
        const apiComponents = response.data.build_data.components
        let loadedCount = 0
        
        for (const [category, compData] of Object.entries(apiComponents)) {
          if (compData && compData.id) {
            // console.log(`Loading ${category}:`, compData.name)
            buildStore.components[category] = compData
            loadedCount++
          }
        }
        
        buildStore.currentBuildId = response.data.id
        buildStore.saveToLocalStorage()
        
        // console.log(`Loaded ${loadedCount} components`)
        // console.log('Final components:', JSON.parse(JSON.stringify(buildStore.components)))
        
        // Принудительное обновление UI
        window.dispatchEvent(new Event('storage'))
      } else {
        console.warn('Invalid build data structure:', response.data)
      }
    } catch (error) {
      console.error('Error loading build:', error)
      if (error.response) {
        console.error('Error response:', error.response.status, error.response.data)
      }
      alert('Сборка не найдена или удалена')
    }
  }
})

function openSelector(categoryKey, categoryLabel) {
  currentCategory.value = categoryKey
  currentCategoryLabel.value = categoryLabel
  modalVisible.value = true
}

function onComponentSelected(selectedItem) {
  buildStore.addComponent(currentCategory.value, selectedItem)
  modalVisible.value = false
}
</script>

<style lang="scss">
.main {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  flex-direction: column;

  &__title {
    font-size: 36px;
    font-weight: 700;
    margin-top: 24px;
  }

  &__info {
    display: flex;
    width: 304px;
    height: auto;
  }
}

.configurator-block {
  display: flex;
  justify-content: space-between;
  width: 1274px;
  margin: 0 auto;
  margin-top: 24px;

  &__items {
    flex: 2;
    min-width: 0;
  }
}
</style>