<template>
  <header class="header">
    <div class="header__logo">
      <router-link to="/" class="header__link">Конфигуратор ПК</router-link>
    </div>
    <div class="header__nav">
      <div v-if="authStore.isLoggedIn" class="header__user-menu">
        <router-link to="/profile" class="header__profile-link">
          <span class="header__username">{{ authStore.currentUser?.username }}</span>
        </router-link>
        <button @click="handleLogout" class="header__logout-btn">Выйти</button>
      </div>
      <div v-else class="header__btns-block">
        <router-link to="/login" class="header__btn">Войти</router-link>
        <router-link to="/register" class="header__btn">Регистрация</router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await authStore.logout()
  router.push('/')
}
</script>

<style lang="scss">
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 32px;
  background: #4361ee;
  color: white;

  &__link {
    color: white;
    text-decoration: none;
    font-size: 28px;
    font-weight: 700;
    line-height: 28px;
  }

  &__nav {
    display: block;
  }

  &__btns-block {
    display: flex;
    justify-content: space-between;
    width: 240px;
  }

  &__btn {
    font-size: 22px;
    font-weight: 500;
    padding: 8px;
    color: #fff;
  }
}
</style>