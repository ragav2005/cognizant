import apiClient from './apiClient'

export async function getAllCourses() {
  const response = await apiClient.get('/courses')
  return response.data
}

export async function enrollStudent(studentId, courseId) {
  const response = await apiClient.post('/enrollments', { studentId, courseId })
  return response.data
}
