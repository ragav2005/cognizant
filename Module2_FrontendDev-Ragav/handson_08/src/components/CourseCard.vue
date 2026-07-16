<script setup>
defineProps({
  name: String,
  code: String,
  credits: Number,
  grade: String,
})
</script>

<template>
  <article class="course-card">
    <div>
      <p class="code">{{ code }}</p>
      <h3>{{ name }}</h3>
    </div>
    <div class="details">
      <span>{{ credits }} credits</span>
      <strong>Grade: {{ grade }}</strong>
    </div>
  </article>
</template>

<style scoped>
.course-card {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border: 1px solid #dbe3f0;
  border-radius: .5rem;
}

h3,
p {
  margin: 0;
}

.code {
  color: #526078;
  font-size: .85rem;
}

.details {
  display: grid;
  align-content: center;
  gap: .4rem;
  text-align: right;
}
</style>
