<template>
  <section class="home">
    <h2>Welcome to the Student Portal</h2>
    <p>Browse your enrolled courses, review grades, and manage your profile.</p>
    <RouterLink to="/courses">View my courses</RouterLink>
  </section>
</template>

<style scoped>
.home {
  padding: 2rem;
  background: white;
  border: 1px solid #dbe3f0;
  border-radius: .75rem;
}

h2 {
  margin-top: 0;
}

p {
  color: #526078;
}

a {
  display: inline-block;
  padding: .7rem 1rem;
  color: white;
  text-decoration: none;
  background: #1e40af;
  border-radius: .35rem;
}
</style>
