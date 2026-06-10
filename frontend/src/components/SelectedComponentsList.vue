<template>
  <div class="selected-list">
    <h3 class="selected-list__title">Ваша сборка</h3>
    <div v-for="cat in categories" :key="cat.key" class="selected-item selected-list__item">
      <div v-if="buildStore.components[cat.key]" class="item-detail selected-list__item-detail">
        <p class="selected-list__name">{{ buildStore.components[cat.key].name }}</p>
        <div class="selected-list__info-block">
          <p class="selected-list__shop-name">Цена в {{ buildStore.components[cat.key].shop_name }}</p>
          <p class="selected-list__price">{{ formatPrice(buildStore.components[cat.key].min_price) }} ₽</p>
        </div>
      </div>
      <div v-else class="selected-list__empty">{{ cat.label }} {{cat.emptytext }}</div>
    </div>
    <div class="selected-list__total">
      <strong class="selected-list__total-price">Итого:</strong> {{ formatPrice(buildStore.totalPrice) }} ₽
    </div>
    <button class="selected-list__save-build-btn" @click="openSaveModal">Сохранить сборку</button>
    <div v-if="showSaveModal" class="selected-list__modal-overlay" @click.self="closeSaveModal">
      <div class="selected-list__modal-content">
        <h3 class="selected-list__modal-title">Сохранить сборку</h3>
        <input 
          type="text" 
          v-model="buildName" 
          placeholder="Название сборки"
          class="selected-list__build-name-input"
        >
        <div class="selected-list__modal-buttons">
          <button @click="saveBuild" class="selected-list__save-btn">Сохранить</button>
          <button @click="closeSaveModal" class="selected-list__cancel-btn">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useBuildStore } from '../stores/build'
import { useAuthStore } from '../stores/auth'

const buildStore = useBuildStore()
const authStore = useAuthStore()
const showSaveModal = ref(false)
const buildName = ref('')

const categories = [
  { key: 'cpu', label: 'Процессор', emptytext: 'не выбран' },
  { key: 'motherboard', label: 'Материнская плата', emptytext: 'не выбрана' },
  { key: 'ram', label: 'Оперативная память', emptytext: 'не выбрана' },
  { key: 'gpu', label: 'Видеокарта', emptytext: 'не выбрана' },
  { key: 'cooler', label: 'Охлаждение процессора', emptytext: 'не выбрано' },
  { key: 'storage', label: 'Накопитель', emptytext: 'не выбран' },
  { key: 'psu', label: 'Блок питания', emptytext: 'не выбран' },
  { key: 'case', label: 'Корпус', emptytext: 'не выбран' },
  { key: 'casefan', label: 'Корпусное охлаждение', emptytext: 'не выбрано' },
]

const formatPrice = (price) => {
  return price ? price.toLocaleString('ru-RU') : '0'
}

const openSaveModal = () => {
  if (!authStore.isAuthenticated) {
    alert('Войдите в аккаунт, чтобы сохранить сборку')
    return
  }
  buildName.value = `Сборка от ${new Date().toLocaleDateString('ru-RU')}`
  showSaveModal.value = true
}

const closeSaveModal = () => {
  showSaveModal.value = false
  buildName.value = ''
}

const saveBuild = async () => {
  if (!buildName.value.trim()) {
    alert('Введите название сборки')
    return
  }
  const result = await buildStore.saveCurrentBuild(buildName.value)
  if (result.success) {
    alert('Сборка сохранена!')
    closeSaveModal()
  } else {
    alert('Ошибка при сохранении')
  }
}
</script>

<style lang="scss">
.selected-list {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background: white;
  position: sticky;
  top: 16px;
  width: 304px;
  height: fit-content;

  @media screen and (max-width: 1080px) {
    width: 600px;
  }

  @media screen and (max-width: 760px) {
    width: 100%;
  }

  &__title {
    font-size: 28px;
    font-weight: 700;

    @media screen and (max-width: 760px) {
      font-size: 24px;
    }
  }

  &__item {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    flex-direction: column;
    margin: 6px 0 6px 0;
    width: 100%;
  }

  &__item_detail {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    flex-direction: column;
    width: 268px;

    @media screen and (max-width: 1080px) {
      width: 100%;
    }
  }

  &__name {
    width: 268px;
    display: block;
    font-size: 16px;
    font-weight: 500;
    overflow-x: hidden;
    overflow-y: clip;
    white-space: nowrap;
    text-overflow: ellipsis;

    @media screen and (max-width: 1080px) {
      width: 568px;
    }

    @media screen and (max-width: 760px) {
      max-width: 500px;
    }

    @media screen and (max-width: 600px) {
      max-width: 400px;
    }

    @media screen and (max-width: 490px) {
      max-width: 300px;
    }

    @media screen and (max-width: 400px) {
      max-width: 280px;
    }
  }

  &__info-block {
    display: flex;
    justify-content: space-between;
    width: 100%;
    padding-bottom: 8px;
    border-bottom: 1px solid #e0e0e0;
  }

  &__shop-name {
    font-size: 16px;
  }

  &__price {
    font-size: 16px;
    font-weight: 500;
  }

  &__empty {
    width: 100%;
    padding-bottom: 8px;
    color: #666;
    border-bottom: 1px solid #e0e0e0;
  }

  &__save-build-btn {
    width: 100%;
    padding: 8px;
    margin-top: 8px;
    background: #00dc33;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 500;
    transition: .2s;

    &:hover {
      background: #09bf09;
    }
  }

  &__modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  &__modal-content {
    background: white;
    padding: 16px;
    border-radius: 8px;
    width: 300px;
  }

  &__build-name-input {
    width: 100%;
    padding: 8px;
    margin: 16px 0;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  &__modal-buttons {
    display: flex;
    gap: 16px;
    justify-content: space-between;
    width: 100%;
  }

  &__save-btn {
    background: #00dc33;
    color: white;
    border: none;
    padding: 8px;
    border-radius: 4px;
    cursor: pointer;
    width: 66%;
    transition: .2s;

    &:hover {
      background: #09bf09;
    }
  }

  &__cancel-btn {
    background: #e74c3c;
    color: white;
    border: none;
    padding: 8px;
    border-radius: 4px;
    cursor: pointer;
    width: 30%;
    transition: .2s;

    &:hover {
      opacity: 0.7;
    }
  }
}
</style>