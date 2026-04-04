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
            <a
                v-if="selectedComponent.url"
                :href="selectedComponent.url"
                target="_blank"
                rel="noopener noreferrer"
                class="category-item__shop-name"
            >
                {{ selectedComponent.shop_name }}
            </a>
        </div>
        <div class="category-item__order-block">
            <span class="category-item__price">{{ formatPrice(selectedComponent.price) }} ₽</span>
            <span class="category-item__compatibility">Совместимость</span>
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
        line-height: 28px;
    }

    &__name, &__price {
        font-weight: 500;
    }

    &__shop-name, &__empty-text, &__compatibility {
        font-size: 22px;
        line-height: 22px;
        margin-top: 8px;
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
        font-size: 24px;
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
        }
    }
}
</style>