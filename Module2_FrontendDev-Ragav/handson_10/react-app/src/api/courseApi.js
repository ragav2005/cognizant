import apiClient from './apiClient'

const delay = (ms) => new Promise((r) => setTimeout(r, ms))

const mockCourses = [
  { id: '1', name: 'Mathematics', code: 'MTH101', credits: 3, grade: 'A' },
  { id: '2', name: 'Physics', code: 'PHY101', credits: 4, grade: 'B' },
  { id: '3', name: 'Chemistry', code: 'CHM101', credits: 3, grade: 'A-' },
]

export async function getAllCourses() {
  await delay(300)

  const data = await apiClient.get('/posts')

  return data.slice(0, 5).map((item, idx) => ({
    id: String(item.id),
    name: item.title,
    code: `POST${String(idx + 1).padStart(3, '0')}`,
    credits: 3,
    grade: 'A',
  }))
}

export async function getCourseById(id) {
  await delay(200)
  const course = mockCourses.find((c) => c.id === id)
  if (!course) {
    const err = new Error('Course not found')
    err.statusCode = 404
    throw err
  }
  return course
}

export async function enrollStudent(studentId, courseId) {
  await delay(400)

  return { success: true, studentId, courseId }
}
