<template>
  <div class="form-container">
    <h2 class="form-container__title">Регистрация</h2>
    <form @submit.prevent="handleRegister" class="form-container__form form">
      <input class="form__input" type="text" v-model="username" placeholder="Имя пользователя" autocomplete="username" required>
      <input class="form__input" type="email" v-model="email" placeholder="Email" autocomplete="email" required>
      <input class="form__input" type="password" v-model="password" placeholder="Пароль" autocomplete="new-password" required>
      <input class="form__input" type="password" v-model="password2" placeholder="Подтверждение пароля" autocomplete="new-password" required>
      <button class="form__btn" type="submit">Зарегистрироваться</button>
      <p v-if="error" class="form__error">{{ error }}</p>
    </form>
    <p class="form__text">Уже есть аккаунт? <router-link to="/login" class="form__link">Войти</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const error = ref('')

async function handleRegister() {
  const result = await authStore.register(
    username.value, 
    email.value, 
    password.value, 
    password2.value
  )
  if (result.success) {
    await authStore.fetchProfile()
    router.push('/profile')
  } else {
    // Проверка на разные варианты ошибок
    if (result.error?.non_field_errors) {
      error.value = result.error.non_field_errors[0]
    } else if (result.error?.password2) {
      error.value = result.error.password2[0]
    } else if (result.error?.password) {
      error.value = result.error.password[0]
    } else if (result.error?.username) {
      error.value = result.error.username[0]
    } else if (result.error?.email) {
      error.value = result.error.email[0]
    } else if (typeof result.error === 'string') {
      error.value = result.error
    } else {
      error.value = 'Ошибка регистрации'
    }
  }
}
</script>

<style lang="scss">
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  height: 80vh;

  &__title {
    font-size: 28px;
    font-weight: 700;
  }
}

.form {
  display: flex;
  flex-direction: column;
  width: 360px;
  padding: 16px 0 16px 0;

  &__input {
    padding: 8px;
    font-size: 22px;
    font-weight: 400;
    margin: 8px 0 8px 0;
    border-radius: 8px;
    border: 1px solid #666;
    transition: 0.2s;

    &:hover {
      box-shadow: 0 0 6px rgba(0,0,0,0.2);
    }
  }

  &__btn {
    padding: 8px;
    background-color: #4361ee;
    border: none;
    border-radius: 8px;
    font-size: 22px;
    color: #fff;
    font-weight: 500;
    margin-top: 8px;
    transition: 0.2s;

    &:hover {
      background-color: #4895ef;
    }
  }

  &__text {
    font-size: 16px;
    font-weight: 400;
  }

  &__link {
    font-size: 16px;
    font-weight: 400;
    color: #4361ee;
    text-decoration: underline;
  }

  &__error {
    font-size: 16px;
    font-weight: 500;
    color: red;
    margin-top: 16px;
  }
}
</style>