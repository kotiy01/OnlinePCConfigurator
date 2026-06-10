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

    <div class="main__content-block content-block">
      <div class="content-block__main-text-container">
        <div class="content-block__main-text-img">
          <img class="content-block__main-img" src="../assets/main-img.png" alt="Комплектующие ПК">
        </div>
        <div class="content-block__main-text-block">
          <h2 class="content-block__main-text-title">Собери компьютер сам с помощью онлайн-конфигуратора ПК</h2>
          <p class="content-block__main-text">Сборка компьютера кажется сложной? Боишься купить процессор, который не подойдёт к материнской плате? Онлайн-конфигуратор ПК с проверкой совместимости решит эти проблемы. Выбирай комплектующие из списка, а система автоматически проверит, подходят ли они друг к другу – сокеты, чипсеты, форм-факторы, мощность блока питания и даже длина видеокарты.<br>Конфигуратор подскажет, если ты ошибёшься: например, процессор AMD не встанет в сокет Intel, а оперативная память DDR5 не заработает на плате с поддержкой только DDR4. Ты можешь быть уверен – собранная система запустится.</p>
        </div>
      </div>
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
  buildStore.loadFromLocalStorage()
  
  const buildId = route.query.build_id
 
  if (buildId) {
    try {
      const response = await api.get(`/public-build/${buildId}/`)
      if (response.data && response.data.build_data && response.data.build_data.components) {
        buildStore.clearBuild()
        const apiComponents = response.data.build_data.components
        let loadedCount = 0
        
        for (const [category, compData] of Object.entries(apiComponents)) {
          if (compData && compData.id) {
            buildStore.components[category] = compData
            loadedCount++
          }
        }
        
        buildStore.currentBuildId = response.data.id
        buildStore.saveToLocalStorage()
        
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
    text-align: center;
    width: 90%;
    line-height: 38px;

    @media screen and (max-width: 760px) {
      font-size: 28px;
      line-height: 26px;
    }

    @media screen and (max-width: 550px) {
      font-size: 22px;
      line-height: 24px;
    }
  }
}

.configurator-block {
  display: flex;
  justify-content: space-between;
  width: 1274px;
  margin: 0 auto;
  margin-top: 24px;

  @media screen and (max-width: 1300px) {
    width: 95%;
  }

  @media screen and (max-width: 1080px) {
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  &__items {
    flex: 2;
    min-width: 0;
  }
}

.content-block {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 80%;
  margin-top: 40px;

  &__main-text-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }

  &__main-text-img {
    width: 35%;
    height: auto;
  }

  &__main-img {
    width: 100%;
    height: auto;
  }

  &__main-text-block {
    width: 65%;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    flex-direction: column;
  }

  &__main-text-title {
    margin-bottom: 20px;
    font-size: 24px;
  }

  &__main-text {
    font-size: 18px;
    line-height: 28px;
  }
}
</style>