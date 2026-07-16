<script setup>
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()
</script>

<template>
  <section class="profile">
    <h2>Student Profile</h2>
    <p>Enrolled courses: {{ store.enrolledCourses.length }}</p>

    <ul v-if="store.enrolledCourses.length">
      <li v-for="course in store.enrolledCourses" :key="course.id">
        <strong>{{ course.name }}</strong> ({{ course.code }}) — {{ course.credits }} credits
        <button type="button" @click="store.unenroll(course.id)">Unenroll</button>
      </li>
    </ul>
    <p v-else class="empty">You have not enrolled in any courses yet.</p>

    <p class="summary">Total credits: {{ store.totalCredits }}</p>
    <RouterLink to="/courses">Back to courses</RouterLink>
  </section>
</template>

<style scoped>
.profile {
  max-width: 560px;
  padding: 1.5rem;
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

ul {
  padding: 0;
  list-style: none;
}

li {
  display: flex;
  align-items: center;
  gap: .5rem;
  padding: .75rem 0;
  border-bottom: 1px solid #dbe3f0;
}

.summary {
  font-weight: 600;
}

button {
  margin-left: auto;
  padding: .4rem .7rem;
  color: #b91c1c;
  background: white;
  border: 1px solid #b91c1c;
  border-radius: .3rem;
  cursor: pointer;
}
</style>
