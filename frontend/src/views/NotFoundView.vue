<template>
  <div class="not-found">
    <div class="not-found__content">
      <h1 class="not-found__code">404</h1>
      <h2 class="not-found__title">Страница не найдена</h2>
      <p class="not-found__text">К сожалению, страница, которую вы ищете, не существует :(</p>
      <p class="not-found__text">Возможно, вы хотели собрать компьютер? Попробуйте начать с главной страницы.</p>
      <router-link to="/" class="not-found__btn">На главную</router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  document.title = '404 — Страница не найдена | PC Configurator'
})
</script>

<style lang="scss">
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;

  &__content {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    max-width: 600px;
  }

  &__code {
    font-size: 62px;
    font-weight: 700;
    text-shadow: 0px 0px 8px rgba(0, 0, 0, 0.1);
  }

  &__title {
    font-size: 32px;
    margin-bottom: 20px;
  }

  &__text {
    color: #333;
    font-size: 18px;
    line-height: 28px;
  }

  &__btn {
    padding: 8px;
    background: #4361ee;
    color: white;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    font-size: 18px;
    font-weight: 500;
    transition: 0.2s;
    margin-top: 10px;
    width: 280px;
    text-decoration: none;

    &:hover {
      background: #4895ef;
    }
  }
}
</style>