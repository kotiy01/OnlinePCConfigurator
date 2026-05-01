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
  if (component.release_year) specs['Год выпуска'] = component.release_year
  if (component.part_numbers_json) specs['Коды производителя'] = component.part_numbers_json

  // Для CPU
  if (props.categoryKey === 'cpu') {
    if (component.socket) specs['Сокет'] = component.socket
    if (component.cores_total) specs['Ядра'] = component.cores_total
    if (component.threads) specs['Потоки'] = component.threads
    if (component.base_clock) specs['Базовая частота'] = `${component.base_clock} ГГц`
    if (component.boost_clock) specs['Макс. частота'] = `${component.boost_clock} ГГц`
    if (component.tdp) specs['TDP'] = `${component.tdp} Вт`
    if (component.l2_cache) specs['L2 кэш'] = `${component.l2_cache} Мб`
    if (component.l3_cache) specs['L3 кэш'] = `${component.l3_cache} Мб`
    if (component.integrated_graphics) specs['Втроенная графика'] = component.integrated_graphics
    if (component.max_memory) specs['Макс. память'] = `${component.max_memory} Гб`
    if (component.memory_types) specs['Тип памяти'] = component.memory_types
  }

  // Для материнской платы
  if (props.categoryKey === 'motherboard') {
    if (component.socket) specs['Сокет'] = component.socket
    if (component.form_factor) specs['Форм-фактор'] = component.form_factor
    if (component.chipset) specs['Чипсет'] = component.chipset
    if (component.memory_type) specs['Тип памяти'] = component.memory_type
    if (component.memory_slots) specs['Слоты памяти'] = component.memory_slots
    if (component.memory_max) specs['Макс. память'] = `${component.memory_max} Гб`
    if (component.color) specs['Цвет(а)'] = component.color
    if (component.sata_6_gb_s) specs['Порты SATA'] = component.sata_6_gb_s
    if (component.m2_slots) specs['Слоты M.2'] = component.m2_slots
    if (component.raid_support) specs['Поддержка RAID'] = component.raid_support
    // if (component.onboard_ethernet) specs['Встроенный Ethernet'] = component.onboard_ethernet
    if (component.wireless) specs['Wi-Fi'] = component.wireless
    if (component.audio) specs['Аудиочип'] = component.audio
    // if (component.back_panel_ports) specs['Порты задней панели'] = component.back_panel_ports
    // if (component.power_connectors) specs['Разъемы питания'] = component.power_connectors
  }

  // Для видеокарты
  if (props.categoryKey === 'gpu') {
    if (component.chipset) specs['Чипсет'] = component.chipset
    if (component.memory) specs['Память'] = `${component.memory} ГБ`
    if (component.memory_type) specs['Тип памяти'] = component.memory_type
    if (component.tdp) specs['TDP'] = `${component.tdp} Вт`
    if (component.interface) specs['Интерфейс'] = component.interface
    if (component.core_base_clock) specs['Базовая частота ядра'] = `${component.core_base_clock} МГц`
    if (component.core_boost_clock) specs['Boost частота'] = `${component.core_boost_clock} МГц`
    if (component.memory_bus) specs['Шина памяти'] = component.memory_bus
    if (component.length) specs['Длина'] = `${component.length} мм`
    if (component.case_expansion_slot_width) specs['Занимает слоов расширения'] = component.case_expansion_slot_width
    if (component.power_connectors) specs['Разъемы питания'] = component.power_connectors
    if (component.video_outputs) specs['Видеовыходы'] = component.video_outputs
    if (component.core_count) specs['Видеовыходы'] = component.core_count
    if (component.color) specs['Цвет'] = component.color
  }

  // Для RAM
  if (props.categoryKey === 'ram') {
    if (component.ram_type) specs['Тип'] = component.ram_type
    if (component.modules_quantity) specs['Количество модулей'] = component.modules_quantity
    if (component.capacity_per_module) specs['Объем одного модуля'] = `${component.capacity_per_module} ГБ`
    if (component.total_capacity) specs['Общий объем'] = `${component.total_capacity} ГБ`
    if (component.ram_type) specs['Тип'] = component.ram_type
    if (component.speed) specs['Частота'] = `${component.speed} МГц`
    if (component.cas_latency) specs['CAS Latency'] = component.cas_latency
    if (component.timings) specs['Тайминги'] = component.timings
    // if (component.profile_support) specs['Поддерживаемые профили'] = component.profile_support
    if (component.color) specs['Цвет(а)'] = component.color
  }

  // Для охлаждения процессора
  if (props.categoryKey === 'cooler') {
    if (component.cpu_sockets) specs['Совместимые сокеты'] = component.cpu_sockets
    if (component.min_fan_rpm) specs['Мин. обороты вентилятора'] = component.min_fan_rpm
    if (component.max_fan_rpm) specs['Макс. обороты вентилятора'] = component.max_fan_rpm
    if (component.min_noise_level) specs['Мин. уровень шума'] = `${component.min_noise_level} Дб`
    if (component.max_noise_level) specs['Макс. уровень шума'] = `${component.max_noise_level} Дб`
    if (component.height) specs['Высота'] = `${component.height} мм`
    if (component.water_cooled) specs['Водяное охлаждение'] = component.water_cooled
    if (component.fan_quantity) specs['Количество вентиляторов'] = component.fan_quantity
    if (component.radiator_size) specs['Размер радиатора'] = `${component.radiator_size} мм`
    if (component.fan_size) specs['Размер вентилятора'] = `${component.fan_size} мм`
    if (component.color) specs['Цвет(а)'] = component.color
  }

  // Для накопителей
  if (props.categoryKey === 'storage') {
    if (component.type) specs['Тип'] = component.type
    if (component.capacity) specs['Объем'] = `${component.capacity} Гб`
    if (component.form_factor) specs['Форм-фактор'] = component.form_factor
    if (component.interface) specs['Интерфейс'] = component.interface
    if (component.rpm) specs['Скорость вращения'] = `${component.rpm} RPM`
  }

  // Для блоков питания
  if (props.categoryKey === 'psu') {
    if (component.type) specs['Тип'] = component.type
    if (component.wattage) specs['Мощность'] = `${component.wattage} Вт`
    if (component.form_factor) specs['Форм-фактор'] = component.form_factor
    if (component.efficiency_rating) specs['Сертификат эффективности'] = component.efficiency_rating
    if (component.modular) specs['Модульность'] = component.modular
    if (component.length) specs['Длина'] = `${component.length} мм`
    if (component.connectors) specs['Разъемы'] = component.connectors
  }

  // Для корпусов
  if (props.categoryKey === 'case') {
    if (component.case_type) specs['Тип корпуса'] = component.case_type
    if (component.supported_motherboard_form_factors) specs['Форм-факторы мат. плат'] = component.supported_motherboard_form_factors
    if (component.side_panel) specs['Боковая панель'] = component.side_panel
    if (component.front_panel_usb) specs['USB на передней панели'] = component.front_panel_usb
    if (component.max_video_card_length) specs['Макс. длина видеокарты'] = `${component.max_video_card_length} мм`
    if (component.max_cpu_cooler_height) specs['Макс. высота кулера CPU'] = `${component.max_cpu_cooler_height} мм`
    if (component.internal_3_5_bays) specs['Внутренних отсеков 3.5 дюйма'] = component.internal_3_5_bays
    if (component.internal_2_5_bays) specs['Внутренних отсеков 2.5 дюйма'] = component.internal_2_5_bays
    if (component.expansion_slots) specs['Слоты расширения'] = component.expansion_slots
    if (component.dimensions) specs['Габариты'] = `${component.dimensions} мм`
    if (component.weight) specs['Габариты'] = `${component.weight} кг`
    if (component.supported_power_supply_form_factors) specs['Форм-факторы БП'] = component.supported_power_supply_form_factors
    if (component.color) specs['Цвет(а)'] = component.color
  }

  // Для корпусных вентиляторов
  if (props.categoryKey === 'casefan') {
    if (component.size) specs['Размер'] = `${component.size} мм`
    if (component.quantity) specs['Штук в упаковке'] = component.quantity
    if (component.min_airflow) specs['Мин. воздушный поток'] = `${component.min_airflow} CFM`
    if (component.max_airflow) specs['Макс. воздушный поток'] = `${component.max_airflow} CFM`
    if (component.min_noise_level) specs['Мин. уровень шума'] = `${component.min_noise_level} Дб`
    if (component.max_noise_level) specs['Макс. уровень шума'] = `${component.max_noise_level} Дб`


    if (component.color) specs['Цвет(а)'] = component.color
  }

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
    flex-direction: column;
    padding: 16px;
    width: 100%;
    overflow-y: auto;
    flex: 1;
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
  margin-bottom: 16px;
  width: 950px;

  &__img-block {
    width: 80px;
    height: 80px;
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
    font-size: 24px;
    line-height: 24px;
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