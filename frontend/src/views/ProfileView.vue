<template>
  <div class="profile-container" v-if="authStore.isAuthenticated">
    <h2 class="profile-container__title">Личный кабинет</h2>
    <div class="profile-container__info-block">
      <p class="profile-container__text"><strong>Имя пользователя:</strong> {{ authStore.currentUser?.username }}</p>
      <p class="profile-container__text"><strong>Email:</strong> {{ authStore.currentUser?.email }}</p>
      <p class="profile-container__text"><strong>Дата регистрации:</strong> {{ formatDate(authStore.currentUser?.date_joined) }}</p>
    </div>
    
    <div class="profile-container__saved-builds">
      <h3 class="profile-container__subtitle">Сохраненные сборки</h3>
      <div v-if="!savedBuildsList || savedBuildsList.length === 0" class="profile-container__empty">
        У вас пока нет сохраненных сборок
      </div>
      <div v-else class="profile-container__builds-list">
        <div v-for="build in savedBuildsList" :key="build.id" class="profile-container__build-item build-item">
          <div class="build-item__header" @click="toggleBuild(build.id)">
            <img src="../assets/icons/pc-icon.png" alt="Иконка конфигурации компьютера" class="build-item__icon">
            <span class="build-item__name">{{ build.name }}</span>
            <span class="build-item__price">{{ formatPrice(getBuildPrice(build)) }} ₽</span>
            <button class="build-item__share-btn" @click.stop="openShareModal(build)">Поделиться</button>
          </div>
          
          <div v-if="expandedBuildId === build.id" class="build-item__build-details">
            <div class="build-item__components-list">
              <div v-for="(component, category) in getBuildComponents(build)" :key="category" class="build-item__component-item">
                <img
                  class="build-item__comp-icon"
                  :src="getCategoryIcon(category)"
                  :alt="category.label"
                >
                <span class="build-item__comp-category">{{ getCategoryName(category) }}:</span>
                <span class="build-item__comp-name">{{ component?.name || 'Не выбран' }}</span>
                <span class="build-item__comp-price">{{ component?.price ? formatPrice(component.price) + ' ₽' : '—' }}</span>
                <span class="build-item__comp-shop">{{ component?.shop_name || '' }}</span>
              </div>
            </div>
            <div class="build-item__btns-block">
              <button class="build-item__open-build-btn" @click="openBuild(build)">Открыть сборку в конфигураторе</button>
              <button class="build-item__delete-btn" @click.stop="deleteBuild(build.id)">Удалить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="shareModalVisible" class="profile-container__modal-overlay" @click.self="closeShareModal">
      <div class="profile-container__modal-content">
        <div class="profile-container__modal-header">
          <h3 class="profile-container__modal-title">Поделиться сборкой</h3>
          <button @click="closeShareModal" class="profile-container__close-btn">✕</button>
        </div>
        <div class="profile-container__share-link">
          <input type="text" :value="shareUrl" readonly ref="shareInput" class="profile-container__input">
          <button @click="copyShareLink" class="profile-container__copy-btn">Копировать</button>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="profile-container">
    <p class="profile-container__login">Пожалуйста, <router-link to="/login">войдите</router-link> для просмотра профиля</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useBuildStore } from '../stores/build'
import { useRouter } from 'vue-router'
import api from '../api'

const authStore = useAuthStore()
const buildStore = useBuildStore()
const router = useRouter()
const expandedBuildId = ref(null)
const shareModalVisible = ref(false)
const shareUrl = ref('')
const shareInput = ref(null)
const avatarInput = ref('')

const avatarUrl = computed(() => authStore.currentUser?.avatar || null)

function getInitials() {
  const username = authStore.currentUser?.username || ''
  return username.charAt(0).toUpperCase()
}

function handleAvatarError(e) {
  e.target.style.display = 'none'
}

async function updateAvatar() {
  if (!avatarInput.value) return
  
  try {
    const response = await api.put('/auth/profile/', { avatar: avatarInput.value })
    authStore.user = response.data
    avatarInput.value = ''
    alert('Аватар обновлён')
  } catch (error) {
    console.error('Avatar update error:', error)
    alert('Ошибка обновления аватара')
  }
}

const savedBuildsList = computed(() => {
  if (buildStore.savedBuilds && Array.isArray(buildStore.savedBuilds)) {
    return buildStore.savedBuilds
  }
  return []
})

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await buildStore.loadSavedBuilds()
  }
})

function formatDate(date) {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ru-RU')
}

const formatPrice = (price) => {
  return price ? price.toLocaleString('ru-RU') : '0'
}

function getBuildPrice(build) {
  if (!build || !build.build_data) return 0
  if (build.build_data.totalPrice) return build.build_data.totalPrice
  let total = 0
  const components = build.build_data.components || {}
  for (const key in components) {
    if (components[key]?.price) {
      total += Number(components[key].price)
    }
  }
  return total
}

function getBuildComponents(build) {
  if (!build || !build.build_data || !build.build_data.components) {
    return {}
  }
  return build.build_data.components
}

function getCategoryName(key) {
  const names = {
    cpu: 'Процессор',
    motherboard: 'Материнская плата',
    ram: 'ОЗУ',
    gpu: 'Видеокарта',
    cooler: 'Процессорное охлаждение',
    storage: 'Накопитель',
    psu: 'Блок питания',
    case: 'Корпус',
    casefan: 'Корпусные вентиляторы'
  }
  return names[key] || key
}

const getCategoryIcon = (category) => {
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
  return icons[category] || '/src/assets/logo.png'
}

function toggleBuild(id) {
  expandedBuildId.value = expandedBuildId.value === id ? null : id
}

async function openBuild(build) {
  if (build && build.build_data && build.build_data.components) {
    await buildStore.loadBuildToConfigurator(build)
    router.push('/')
  } else {
    alert('Ошибка: данные сборки повреждены')
  }
}

function openShareModal(build) {
  shareUrl.value = `${window.location.origin}/?build_id=${build.id}`
  shareModalVisible.value = true
}

function closeShareModal() {
  shareModalVisible.value = false
  shareUrl.value = ''
}

async function copyShareLink() {
  if (shareInput.value) {
    shareInput.value.select()
    shareInput.value.setSelectionRange(0, 99999)
    try {
      await navigator.clipboard.writeText(shareInput.value.value)
      alert('Ссылка скопирована!')
    } catch (err) {
      document.execCommand('copy')
      alert('Ссылка скопирована!')
    }
  }
}

async function deleteBuild(buildId) {
  if (confirm('Удалить эту сборку?')) {
    await buildStore.deleteSavedBuild(buildId)
  }
}
</script>

<style lang="scss">
.profile-container {
  max-width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  margin-top: 20px;
  margin-bottom: 16px;

  &__title {
    font-size: 28px;
    font-weight: 700;
  }

  &__info-block {
    display: flex;
    align-items: center;
    flex-direction: column;
    padding: 16px;
  }

  &__text {
    font-size: 16px;
    line-height: 16px;
    padding: 4px;
  }

  &__saved-builds {
    display: flex;
    align-items: center;
    flex-direction: column;
    width: 950px;
  }

  &__subtitle {
    font-size: 22px;
    margin-bottom: 16px;
  }

  &__builds-list {
    display: flex;
    align-items: center;
    flex-direction: column;
    width: 100%;    
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
    border-radius: 12px;
    width: 480px;
  }

  &__share-link {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__input {
    padding: 16px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    font-size: 16px;
    box-sizing: border-box;
    width: 320px;
  }

  &__modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  &__modal-title {
    font-size: 22px;
    font-weight: 700;
  }

  &__close-btn {
    background: none;
    border: none;
    font-size: 22px;
    font-weight: 700;
    cursor: pointer;
    color: #999;

    &:hover {
      color: red;
    }
  }

  &__copy-btn {
    padding: 16px;
    border: none;
    border-radius: 4px;
    background-color: #4361ee;
    color: #fff;
    font-size: 16px;
    font-weight: 500;
    transition: 0.2s;

    &:hover {
      background-color: #4895ef;
    }
  }
}


.build-item {
  width: 100%;
  display: flex;
  flex-direction: column;
  transition: 0.2s;
  margin-bottom: 16px;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;

  &:hover {
    box-shadow: 0 0 6px rgba(0,0,0,0.2);
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 16px;
    background: #fff;
    cursor: pointer;
  }

  &__comp-icon {
    width: 28px;
    height: 28px;
    margin-right: 8px;
  }

  &__name {
    font-size: 22px;
    font-weight: 700;
    width: 560px;
  }

  &__price {
    font-size: 22px;
    font-weight: 500;
    width: 120px;
    text-align: end;
  }

  &__share-btn {
    padding: 8px;
    background: #4361ee;
    color: white;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    font-size: 22px;
    font-weight: 500;
    transition: 0.2s;
    width: 138px;

    &:hover {
        background: #4895ef;
    }
  }

  &__build-details {
    padding: 16px;
    border-top: 1px solid #ddd;
  }

  &__components-list {
    margin-bottom: 16px;
    overflow-y: auto;
  }

  &__component-item {
    display: flex;
    align-items: center;
    padding: 8px 0;
    font-size: 16px;
    border-bottom: 1px solid #e0e0e0;
  }

  &__comp-category {
    font-weight: bold;
    line-height: 20px;
    width: 130px;
    flex-shrink: 0;
  }

  &__comp-name {
    flex: 2;
    word-break: break-word;
  }

  &__comp-price {
    width: 90px;
    flex-shrink: 0;
    color: #000;
  }

  &__comp-shop {
    width: 110px;
    flex-shrink: 0;
    color: #0000ff;
    text-decoration: underline;
  }

  &__btns-block {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__open-build-btn {
    width: 79%;
    padding: 8px;
    border: none;
    border-radius: 4px;
    background-color: #4361ee;
    color: #fff;
    font-size: 22px;
    font-weight: 500;
    transition: 0.2s;

    &:hover {
      background-color: #4895ef;
    }
  }

  &__delete-btn {
    width: 20%;
    padding: 8px;
    border: none;
    border-radius: 4px;
    background-color: #FF4444;
    color: #fff;
    font-size: 22px;
    font-weight: 500;
    transition: 0.2s;

    &:hover {
      opacity: 0.8;
    }
  }

  &__icon {
    width: 60px;
  }
}
</style>