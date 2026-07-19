<script setup>
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()
</script>

<template>
  <header class="site-header">
    <div class="header-content">
      <div>
        <h1>Student Portal</h1>
        <p>Track your enrolled courses and grades</p>
      </div>
      <nav aria-label="Main navigation">
        <RouterLink to="/" aria-current="page">Home</RouterLink>
        <RouterLink to="/courses" aria-current="page">Courses</RouterLink>
        <RouterLink to="/profile" aria-current="page">Profile ({{ store.enrolledCourses.length }})</RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  padding: 1.25rem max(1rem, calc((100% - 1000px) / 2));
  color: white;
  background: #1e40af;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

h1,
p {
  margin: 0;
}

p {
  margin-top: .35rem;
  opacity: .85;
}

a {
  color: white;
  text-decoration: none;
}

nav {
  display: flex;
  gap: 1rem;
}

a.router-link-active {
  text-decoration: underline;
}
</style>
