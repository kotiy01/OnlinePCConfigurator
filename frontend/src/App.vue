<template>
  <div id="app">
    <header class="app-header">
      <p class="app-header__title">Онлайн-конфигуратор ПК</p>
    </header>
    <router-view />
    <footer class="app-footer">
      <p>© 2026 Онлайн-конфигуратор ПК.</p>
    </footer>
  </div>
</template>

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

.app-header {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80px;
  background: #4361ee;
  color: white;

  &__title {
    font-size: 30px;
    font-weight: bold;
  }
}

.app-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #333;
  color: white;
  font-size: 14px;
  height: 50px;
}
</style>