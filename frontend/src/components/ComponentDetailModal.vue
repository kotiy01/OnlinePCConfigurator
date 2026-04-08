<template>
  <div class="detail-modal" @click.self="$emit('close')">
    <div class="detail-modal__container">
      <div class="detail-modal__header">
        <h2 class="detail-modal__title">{{ component.name }}</h2>
        <button @click="$emit('close')" class="detail-modal__close-btn">✕</button>
      </div>
      <div class="detail-modal__main-section">
        <h3 class="detail-modal__specs-title">Характеристики</h3>
        <table class="detail-modal__specs-table">
          <tr v-for="(value, key) in displaySpecs" :key="key" class="detail-modal__spec">
            <td class="detail-modal__spec-label">{{ key }}</td>
            <td class="detail-modal__spec-value">{{ value }}</td>
          </tr>
        </table>

        <div class="detail-modal__shops-section">
          <h3 class="detail-modal__shops-title">Где купить</h3>
          <div v-if="shopItems.length === 0" class="detail-modal__empty">
            Нет в наличии
          </div>
          <div
            v-for="shop in shopItems"
            :key="shop.id"
            class="detail-modal__shop-card shop-card"
            @click="selectShop(shop)"
          >
            <div class="shop-card__img-block">
              <img
                class="shop-card__img"
                :src="shop.image_url"
                :alt="shop.name"
              >
            </div>
            <div class="shop-card__content-block">
              <h4 class="shop-card__item-name">{{ shop.name }}</h4>
              <div class="shop-card__info-block">
                <a :href="shop.url" target="_blank" class="shop-card__link" @click.stop>В магазине {{ shop.shop_name }}</a>
                <p class="shop-card__in-stock" :class="{ 'out-of-stock shop-card__out-of-stock': !shop.in_stock }">
                  {{ shop.in_stock ? 'В наличии' : 'Нет в наличии' }}
                </p>
                <p class="shop-card__price">{{ shop.price }} ₽</p>
                <button class="shop-card__select-btn" @click.stop="selectShop(shop)">Добавить в сборку</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import api from '../api'

const props = defineProps(['component', 'categoryKey'])
const emit = defineEmits(['close', 'select'])

const shopItems = ref(props.component.shop_items || [])

onMounted(async () => {
  try {
    const response = await api.get(`/${props.categoryKey}/${props.component.id}/`)
    shopItems.value = response.data.shop_items || []
  } catch (error) {
    console.error('Ошибка загрузки магазинов', error)
  }
})

// Формирование списка характеристик для отображения
const displaySpecs = computed(() => {
  const specs = {}
  const component = props.component

  // Общие для всех категорий
  if (component.brand) specs['Бренд'] = component.brand
  if (component.name) specs['Модель'] = component.name

  // Для CPU
  if (props.categoryKey === 'cpu') {
    if (component.socket) specs['Сокет'] = component.socket
    if (component.cores_total) specs['Ядра'] = component.cores_total
    if (component.threads) specs['Потоки'] = component.threads
    if (component.base_clock) specs['Базовая частота'] = `${component.base_clock} ГГц`
    if (component.boost_clock) specs['Макс. частота'] = `${component.boost_clock} ГГц`
    if (component.tdp) specs['TDP'] = `${component.tdp} Вт`
  }

  // Для материнской платы
  if (props.categoryKey === 'motherboard') {
    if (component.socket) specs['Сокет'] = component.socket
    if (component.form_factor) specs['Форм-фактор'] = component.form_factor
    if (component.memory_type) specs['Тип памяти'] = component.memory_type
    if (component.memory_slots) specs['Слоты памяти'] = component.memory_slots
  }

  // Для видеокарты
  if (props.categoryKey === 'gpu') {
    if (component.chipset) specs['Чипсет'] = component.chipset
    if (component.memory) specs['Память'] = `${component.memory} ГБ`
    if (component.memory_type) specs['Тип памяти'] = component.memory_type
    if (component.tdp) specs['TDP'] = `${component.tdp} Вт`
  }

  // Для RAM
  if (props.categoryKey === 'ram') {
    if (component.ram_type) specs['Тип'] = component.ram_type
    if (component.total_capacity) specs['Объём'] = `${component.total_capacity} ГБ`
    if (component.speed) specs['Частота'] = `${component.speed} МГц`
    if (component.cas_latency) specs['CAS Latency'] = component.cas_latency
  }

  // Другие категории ...

  return specs
})

function selectShop(shop) {
  const selectedItem = {
    ...props.component,
    name: shop.name,
    shop_name: shop.shop_name,
    price: shop.price,
    url: shop.url,
    image_url: shop.image_url,
    in_stock: shop.in_stock,
    shop_item_id: shop.id,
  }
  emit('select', selectedItem)
  emit('close')
}
</script>

<style lang="scss">
.detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;

  &__container {
    display: flex;
    // justify-content: flex-start;
    // align-items: flex-start;
    flex-direction: column;
    background-color: #fff;
    width: 90%;
    max-height: 85vh;
    max-width: 982px;
    border-radius: 12px;
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid #ddd;
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

    &:hover {
      color: red;
    }
  }

  &__main-section, &__shop-section {
    display: flex;
    // justify-content: flex-start;
    // align-items: flex-start;
    flex-direction: column;
    padding: 16px;
    width: 100%;
  }

  &__specs-title, &__shops-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 8px;
  }

  &__specs-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 16px;
  }

  &__spec {
    width: 100%;
    border-bottom: 1px solid #e0e0e0;
  }

  &__spec-label {
    font-size: 18px;
    font-weight: 700;
    padding: 4px 0 4px 0;
  }

  &__spec-label {
    font-size: 18px;
    font-weight: 500;
    padding: 4px 0 4px 0;
  }
}

.shop-card {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
  width: 950px;

  &__img-block {
    width: 80px;
    height: 80px;
    // margin-right: 16px;
  }

  &__img {
    width: 80px;
    height: auto;
  }

  &__content-block {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    flex-direction: column;
    width: 830px;
  }

  &__info-block {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }

  &__item-name {
    font-size: 28px;
    line-height: 28px;
    font-weight: 700;
    margin-bottom: 8px;
  }

  &__link, &__in-stock, &__out-of-stock, &__price {
    font-size: 22px;
    padding: 8px 0 8px 0;
  }

  &__link {
    color: #4361ee;
    text-decoration: underline;
    font-weight: 500;
    width: 360px;
  }

  &__in-stock {
    color: green;
  }

  &__out-of-stock {
    color: red;
  }

  &__price {
    font-weight: 700;
  }

  &__select-btn {
    padding: 8px;
    font-size: 22px;
    font-weight: 500;
    color: white;
    background-color: #4361ee;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    transition: 0.2s;

    &:hover {
      background: #4895ef;
    }
  }
}
</style>