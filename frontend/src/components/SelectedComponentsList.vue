<template>
  <div class="selected-list">
    <h3 class="selected-list__title">Ваша сборка</h3>
    <div v-for="cat in categories" :key="cat.key" class="selected-item selected-list__item">
      <div v-if="buildStore.components[cat.key]" class="item-detail selected-list__item-detail">
        <div class="selected-list__name">{{ buildStore.components[cat.key].name }}</div>
        <div class="selected-list__info-block">
          <div class="name selected-list__shop-name">Цена в {{ buildStore.components[cat.key].shop_name }}</div>
          <div class="price selected-list__price">{{ formatPrice(buildStore.components[cat.key].min_price) }} ₽</div>
        </div>
      </div>
      <div v-else class="empty selected-list__empty">{{ cat.label }} {{cat.emptytext }}</div>
    </div>
    <div class="total selected-list__total">
      <strong class="selected-list__total-price">Итого:</strong> {{ formatPrice(buildStore.totalPrice) }} ₽
    </div>
  </div>
</template>

<script setup>
import { useBuildStore } from '../stores/build'

const buildStore = useBuildStore()

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
  height: auto;

  &__title {
    font-size: 24px;
    font-weight: 700;
  }

  &__item {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    flex-direction: column;
    margin: 6px 0 6px 0;
  }

  &__item_detail {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    flex-direction: column;
    margin: 6px 0 6px 0;
  }

  &__name {
    display: block;
    font-size: 16px;
    font-weight: 500;
    text-overflow: ellipsis;
    overflow: hidden;
    text-overflow: ellipsis;
    word-break: break-word;
    line-clamp: 1;
    box-orient: vertical;
  }

  &__info-block {
    display: flex;
    justify-content: space-between;
    width: 100%;
  }

  &__shop-name {
    font-size: 16px;
  }

  &__price {
    font-size: 16px;
    font-weight: 500;
  }

  &__empty {
    color: #666;
  }
}
</style>