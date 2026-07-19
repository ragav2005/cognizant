<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { courseCatalog } from '../data/courses'
import { useEnrollmentStore } from '../stores/enrollment'

const route = useRoute()
const router = useRouter()
const store = useEnrollmentStore()

const course = computed(() =>
  courseCatalog.find((item) => item.id === Number(route.params.id)),
)

function enroll() {
  if (course.value) {
    store.enroll(course.value)
  }
  router.push('/profile')
}
</script>

<template>
  <section v-if="course" class="course-detail">
    <p class="code">{{ course.code }}</p>
    <h2>{{ course.name }}</h2>
    <dl>
      <div>
        <dt>Credits</dt>
        <dd>{{ course.credits }}</dd>
      </div>
      <div>
        <dt>Current grade</dt>
        <dd>{{ course.grade }}</dd>
      </div>
    </dl>
    <button type="button" @click="enroll">Enroll</button>
  </section>

  <section v-else class="not-found">
    <h2>Course not found</h2>
    <RouterLink to="/courses">Back to courses</RouterLink>
  </section>
</template>

<style scoped>
.course-detail,
.not-found {
  max-width: 560px;
  padding: 1.5rem;
  background: white;
  border: 1px solid #dbe3f0;
  border-radius: .75rem;
}

.code {
  margin: 0;
  color: #526078;
}

h2 {
  margin-top: .4rem;
}

dl {
  display: grid;
  gap: .75rem;
}

dl div {
  display: flex;
  justify-content: space-between;
}

dt {
  font-weight: 600;
}

dd {
  margin: 0;
}

button {
  margin-top: 1rem;
  padding: .7rem 1rem;
  color: white;
  background: #1e40af;
  border: 0;
  border-radius: .35rem;
  cursor: pointer;
}
</style>
