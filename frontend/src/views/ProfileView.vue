<template>
  <div class="profile-container" v-if="authStore.isAuthenticated">
    <h2 class="profile-container__title">Личный кабинет</h2>
    <div class="profile-container__info-block">
      <p class="profile-container__text"><strong>Имя пользователя:</strong> {{ authStore.currentUser?.username }}</p>
      <p class="profile-container__text"><strong>Email:</strong> {{ authStore.currentUser?.email }}</p>
      <p class="profile-container__text"><strong>Дата регистрации:</strong> {{ formatDate(authStore.currentUser?.created_at) }}</p>
    </div>
    <div class="profile-container__saved-builds">
      <h3>Сохраненные сборки</h3>
      <p class="placeholder">Сохраненные конфигурации</p>
    </div>
  </div>
  <div v-else class="profile-container">
    <p class="profile-container__login">Пожалуйста, <router-link to="/login">войдите</router-link> для просмотра профиля</p>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

function formatDate(date) {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ru-RU')
}
</script>