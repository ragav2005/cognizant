import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { enrollStudent } from '../api/courseApi'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([])
  const isEnrolling = ref(false)
  const error = ref(null)

  const totalCredits = computed(() =>
    enrolledCourses.value.reduce((total, course) => total + course.credits, 0),
  )

  const isEnrolled = (courseId) =>
    enrolledCourses.value.some((c) => c.id === courseId)

  function enroll(course) {
    const isAlreadyEnrolled = enrolledCourses.value.some((item) => item.id === course.id)

    if (!isAlreadyEnrolled) {
      enrolledCourses.value.push(course)
    }
  }

  async function fetchAndEnroll(courseId, studentId = 's123') {
    isEnrolling.value = true
    error.value = null
    try {

      const result = await enrollStudent(studentId, courseId)


      if (result?.success && !isEnrolled(courseId)) {
        enrolledCourses.value.push({
          id: courseId,

          name: `Course ${courseId}`,
          code: `CODE${courseId}`,
          credits: 3,
          grade: 'N/A',
        })
      }
      return true
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      isEnrolling.value = false
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter((course) => course.id !== courseId)
  }

  function $reset() {
    enrolledCourses.value = []
    isEnrolling.value = false
    error.value = null
  }

  return {
    // state
    enrolledCourses,
    isEnrolling,
    error,
    // getters
    totalCredits,
    isEnrolled,
    // actions
    enroll,
    fetchAndEnroll,
    unenroll,
    $reset,
  }
})
