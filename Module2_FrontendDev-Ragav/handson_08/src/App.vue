<script setup>
import Header from './components/Header.vue'
</script>

<template>
  <Header />
  <main class="portal-content">
    <RouterView />
  </main>
</template>

<style scoped>
.portal-content {
  max-width: 1040px;
  margin: 0 auto;
  padding: 2rem 1rem;
}
</style>
