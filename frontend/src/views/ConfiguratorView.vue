<template>
  <div class="configurator configurator-block">
    <div class="left-column configurator-block__items">
      <CategoryItem
        v-for="cat in categories"
        :key="cat.key"
        :category="cat"
        :selectedComponent="buildStore.components[cat.key]"
        @select="openSelector(cat.key, cat.label)"
        @remove="buildStore.removeComponent(cat.key)"
      />
    </div>
    <div class="right-column configurator-block__info">
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBuildStore } from '../stores/build'
import api from '../api/index'
import CategoryItem from '../components/CategoryItem.vue'
import SelectedComponentsList from '../components/SelectedComponentsList.vue'
import ComponentSelectorModal from '../components/ComponentSelectorModal.vue'

const buildStore = useBuildStore()

const categories = [
  { key: 'cpu', label: 'Процессор', icon: 'cpu' },
  { key: 'motherboard', label: 'Материнская плата', icon: 'motherboard' },
  { key: 'ram', label: 'Оперативная память', icon: 'ram' },
  { key: 'gpu', label: 'Видеокарта', icon: 'gpu' },
  { key: 'cooler', label: 'Охлаждение процессора', icon: 'cooler' },
  { key: 'storage', label: 'Накопитель', icon: 'storage' },
  { key: 'psu', label: 'Блок питания', icon: 'psu' },
  { key: 'case', label: 'Корпус', icon: 'case' },
  { key: 'casefan', label: 'Корпусное охлаждение', icon: 'caseFan' },
]

const modalVisible = ref(false)
const currentCategory = ref('')
const currentCategoryLabel = ref('')

onMounted(() => {
  buildStore.loadFromLocalStorage()
})

function openSelector(categoryKey, categoryLabel) {
  currentCategory.value = categoryKey
  currentCategoryLabel.value = categoryLabel
  modalVisible.value = true
}

async function onComponentSelected(component) {
  // Формирование текущей сборки для проверки совместимости
  const buildPayload = {}
  for (const key in buildStore.components) {
    if (buildStore.components[key]) {
      buildPayload[key] = buildStore.components[key].id
    }
  }
  buildPayload[currentCategory.value] = component.id

  try {
    const response = await api.post('/check-compatibility/', { build: buildPayload })
    if (response.data.compatible) {
      buildStore.addComponent(currentCategory.value, component)
    } else {
      alert('Несовместимо:\n' + (response.data.messages || []).join('\n'))
    }
  } catch (error) {
    console.error('Ошибка проверки совместимости', error)
    // Без проверки, если API не работает
    buildStore.addComponent(currentCategory.value, component)
  }
  modalVisible.value = false
}
</script>

<style scoped>
.configurator {
  display: flex;
  justify-content: space-between;
  width: 1274px;
  margin: 0 auto;
  padding-top: 40px;
}
.left-column {
  flex: 2;
  min-width: 0;
}
.right-column {
  display: flex;
  width: 304px;
  height: auto;
}
@media (max-width: 768px) {
  .configurator {
    flex-direction: column;
    padding: 1rem;
  }
}
</style>