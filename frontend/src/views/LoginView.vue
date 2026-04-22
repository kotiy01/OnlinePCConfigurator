<template>
  <div class="form-container">
    <h2 class="form-container__title">Вход</h2>
    <form @submit.prevent="handleLogin" class="form-container__form form">
      <input class="form__input" type="text" v-model="username" placeholder="Имя пользователя" autocomplete="username" required>
      <input class="form__input" type="password" v-model="password" placeholder="Пароль" autocomplete="current-password" required>
      <button class="form__btn" type="submit">Войти</button>
      <p v-if="error" class="form__error">{{ error }}</p>
    </form>
    <p class="form__text">Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')

async function handleLogin() {
  const result = await authStore.login(username.value, password.value)
  if (result.success) {
    router.push('/profile')
  } else {
    error.value = result.error
  }
}
</script>