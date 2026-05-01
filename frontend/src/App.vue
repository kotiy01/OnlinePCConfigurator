<template>
  <div id="app">
    <HeaderComponent />
    <router-view />
    <footer class="app__footer footer">
      <p>© 2026 Онлайн-конфигуратор ПК.</p>
    </footer>
  </div>
</template>

<script setup>
import HeaderComponent from './components/HeaderComponent.vue'
import { watch } from 'vue'
import { useAuthStore } from './stores/auth'
import { useBuildStore } from './stores/build'

const authStore = useAuthStore()
const buildStore = useBuildStore()

watch(() => authStore.isAuthenticated, async (isAuth) => {
  if (isAuth) {
    await buildStore.loadSavedBuilds()
  }
}, { immediate: true })
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f5f5f5;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.footer {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #333;
  color: white;
  font-size: 14px;
  height: 50px;
  bottom: 0;
  margin-top: auto;
}
</style>