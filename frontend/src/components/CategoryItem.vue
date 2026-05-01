<template>
    <div v-if="selectedComponent" class="category-item">
        <div class="category-item__img-block">
            <img
                v-if="selectedComponent"
                class="category-item__img"
                :src="selectedComponent.image_url"
                :alt="selectedComponent.name"
            >
            <img
                v-else
                class="category-item__img"
                :src="getCategoryIcon(category.key)"
                :alt="category.label"
            >
        </div>
        <div class="category-item__info-block">
            <h3 class="category-item__name">{{ selectedComponent.name }}</h3>
            <p class="category-item__specs"></p>
            <a
                v-if="selectedComponent.url"
                :href="selectedComponent.url"
                target="_blank"
                rel="noopener noreferrer"
                class="category-item__shop-name"
            >
                В магазине {{ selectedComponent.shop_name }}
            </a>
        </div>
        <div class="category-item__order-block">
            <span class="category-item__price">{{ formatPrice(selectedComponent.price) }} ₽</span>
            <div 
                class="category-item__compatibility-wrapper"
                :class="{ 'incompatible': !isCompatible, 'compatible': isCompatible }"
            >
                <span 
                    class="category-item__compatibility"
                    :data-tooltip="compatibilityMessage"
                    @mouseenter="showTooltip = true"
                    @mouseleave="showTooltip = false"
                >
                    {{ compatibilityText }}
                </span>
                <div 
                    v-if="showTooltip && !isCompatible && compatibilityMessage"
                    class="category-item__tooltip"
                >
                    {{ compatibilityMessage }}
                </div>
            </div>
            <button class="category-item__btn_red" @click="$emit('remove')">Удалить</button>
        </div>
    </div>
    <div v-else class="category-item">
        <div class="category-item__img-block">
            <img
                class="category-item__img"
                :src="getCategoryIcon(category.key)"
                :alt="category.label"
            />
        </div>
        <div class="category-item__empty-block">
            <h3 class="category-item__title">{{ category.label }}</h3>
            <p class="category-item__empty-text">{{ category.emptytext }}</p>
        </div>
        <div class="category-item__order-block">
            <button class="category-item__btn" @click="$emit('select')">Выбрать</button>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useBuildStore } from '../stores/build'
import api from '../api'

const props = defineProps({
  category: {
    type: Object,
    required: true,
  },
  selectedComponent: {
    type: Object,
    default: null,
  },
})

defineEmits(['select', 'remove'])

const buildStore = useBuildStore()
const showTooltip = ref(false)
const compatibilityInfo = ref({ compatible: true, message: '' })

watch(
  () => [props.selectedComponent, buildStore.components],
  async () => {
    if (props.selectedComponent) {
      await checkCompatibility()
    }
  },
  { deep: true }
)

async function checkCompatibility() {
  if (!props.selectedComponent) return
  
  const buildPayload = {}
  for (const [key, component] of Object.entries(buildStore.components)) {
    if (component && component.id && key !== props.category.key) {
      buildPayload[key] = component.id
    }
  }
  
  try {
    const response = await api.post('/check-compatibility/', {
      build: buildPayload,
      component_key: props.category.key,
      component_id: props.selectedComponent.id
    })
    compatibilityInfo.value = {
      compatible: response.data.compatible,
      message: response.data.messages?.join(' ') || ''
    }
  } catch (error) {
    console.error('Ошибка проверки совместимости:', error)
    compatibilityInfo.value = {
      compatible: true,
      message: 'Не удалось проверить совместимость'
    }
  }
}

const isCompatible = computed(() => compatibilityInfo.value.compatible)
const compatibilityText = computed(() => isCompatible.value ? 'Совместимо' : 'Не совместимо')
const compatibilityMessage = computed(() => compatibilityInfo.value.message)

const formatPrice = (price) => {
  return price ? price.toLocaleString('ru-RU') : '0'
}

const getCategoryIcon = (key) => {
  // Получение путей к иконкам нужной категории 
  const icons = {
    cpu: '/src/assets/icons/cpu-icon.png',
    motherboard: '/src/assets/icons/motherboard-icon.png',
    ram: '/src/assets/icons/ram-icon.png',
    gpu: '/src/assets/icons/gpu-icon.png',
    cooler: '/src/assets/icons/cooler-icon.png',
    storage: '/src/assets/icons/storage-icon.png',
    psu: '/src/assets/icons/psu-icon.png',
    case: '/src/assets/icons/case-icon.png',
    casefan: '/src/assets/icons/casefan-icon.png',
  }
  return icons[key] || '/src/assets/logo.png'
}
</script>

<style lang="scss">
.category-item {
    display: flex;
    justify-content: space-between;
    align-items: space-between;
    flex-direction: row;
    width: 950px;
    height: auto;
    padding: 16px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin-bottom: 20px;
    background: white;
    transition: 0.2s;

    &:hover {
        box-shadow: 0 0 6px rgba(0,0,0,0.2);
    }
    
    &__img-block, &__img {
        width: 80px;
        height: 80px;
    }

    &__info-block, &__empty-block {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        flex-direction: column;
        width: 596px;
    }

    &__name, &__title, &__price {
        font-size: 28px;
        // line-height: 28px;
    }

    &__name, &__price {
        font-weight: 700;
    }

    &__name {
        width: 100%;
        // height: 28px;
        overflow-x: hidden;
        overflow-y: clip;
        // white-space: nowrap;
        text-overflow: ellipsis;
    }

    &__shop-name, &__empty-text, &__compatibility {
        font-size: 22px;
        line-height: 22px;
        // padding-top: 4px;
        // padding-bottom: 4px;
        margin-bottom: 8px;
    }

    &__compatibility-wrapper {
        height: 22px;
        padding-top: 4px;
        padding-bottom: 4px;
        // cursor: pointer;

        &.compatible {
            color: #00bb00;
        }

        &.incompatible {
            color: red;
            cursor: help;
        }
    }

    &__tooltip {
        position: absolute;
        transform: translateX(-35%);
        background-color: #333;
        color: #fff;
        max-width: 600px;
        padding: 8px;
        border-radius: 4px;
        z-index: 1000;
    }

    &__empty-text {
        font-size: 18px;
        color: #666;
    }

    &__order-block {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        flex-direction: column;
        width: 212px;
    }

    &__btn {
        padding: 8px;
        background: #4361ee;
        color: white;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        font-size: 22px;
        font-weight: 500;
        transition: 0.2s;

        &:hover {
            background: #4895ef;
        }

        &_red {
            background: none;
            border: none;
            cursor: pointer;
            color: red;
            margin-top: 8px;
            padding-top: 4px;
            padding-bottom: 4px;
        }
    }
}
</style>