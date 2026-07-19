import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([])

  const totalCredits = computed(() =>
    enrolledCourses.value.reduce((total, course) => total + course.credits, 0),
  )

  function enroll(course) {
    const isAlreadyEnrolled = enrolledCourses.value.some((item) => item.id === course.id)

    if (!isAlreadyEnrolled) {
      enrolledCourses.value.push(course)
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter((course) => course.id !== courseId)
  }

  return { enrolledCourses, totalCredits, enroll, unenroll }
})
