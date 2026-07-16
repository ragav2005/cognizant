<script setup>
import { computed, onMounted, ref } from 'vue'
import CourseCard from '../components/CourseCard.vue'
import { courseCatalog } from '../data/courses'
import { useEnrollmentStore } from '../stores/enrollment'

const courses = ref([])
const searchTerm = ref('')
const store = useEnrollmentStore()

onMounted(() => {
  courses.value = courseCatalog
})

const filteredCourses = computed(() => {
  const query = searchTerm.value.trim().toLowerCase()

  if (!query) {
    return courses.value
  }

  return courses.value.filter((course) =>
    course.name.toLowerCase().includes(query) ||
    course.code.toLowerCase().includes(query),
  )
})
</script>

<template>
  <section class="courses">
    <div class="heading">
      <h2>My Courses</h2>
      <input
        v-model="searchTerm"
        type="search"
        placeholder="Search by course or code"
        aria-label="Search courses"
      />
    </div>

    <div v-if="filteredCourses.length" class="course-grid">
      <div
        v-for="course in filteredCourses"
        :key="course.id"
        class="course-item"
      >
        <RouterLink :to="`/courses/${course.id}`" class="course-link">
          <CourseCard
            :name="course.name"
            :code="course.code"
            :credits="course.credits"
            :grade="course.grade"
          />
        </RouterLink>
        <button type="button" :disabled="store.enrolledCourses.some((item) => item.id === course.id)" @click="store.enroll(course)">
          {{ store.enrolledCourses.some((item) => item.id === course.id) ? 'Enrolled' : 'Enroll' }}
        </button>
      </div>
    </div>

    <p v-else class="empty">No courses found.</p>
  </section>
</template>

<style scoped>
.courses {
  padding: 1.25rem;
  background: #eef3ff;
  border-radius: .75rem;
}

.heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

h2 {
  margin: 0;
}

input {
  min-width: 250px;
  padding: .7rem .8rem;
  border: 1px solid #9fb0ca;
  border-radius: .35rem;
}

.course-grid {
  display: grid;
  gap: .75rem;
}

.course-item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: .75rem;
  align-items: center;
}

.course-link {
  color: inherit;
  text-decoration: none;
}

button {
  padding: .7rem 1rem;
  color: white;
  background: #1e40af;
  border: 0;
  border-radius: .35rem;
  cursor: pointer;
}

button:disabled {
  cursor: default;
  opacity: .55;
}

.empty {
  margin: 0;
  padding: 1rem;
  color: #526078;
  background: white;
  border-radius: .5rem;
}

@media (max-width: 550px) {
  .heading {
    flex-direction: column;
    align-items: stretch;
  }

  input {
    min-width: 0;
  }

  .course-item {
    grid-template-columns: 1fr;
  }
}
</style>
