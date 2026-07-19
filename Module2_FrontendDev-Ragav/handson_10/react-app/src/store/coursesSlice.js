import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { getAllCourses, getCourseById, enrollStudent } from '../api/courseApi'

export const fetchCourses = createAsyncThunk('courses/fetchAll', async () => {
  const data = await getAllCourses()
  return data
})

export const fetchCourseById = createAsyncThunk('courses/fetchById', async (id) => {
  const data = await getCourseById(id)
  return data
})

export const enrollInCourse = createAsyncThunk(
  'courses/enroll',
  async ({ studentId, courseId }) => {
    const data = await enrollStudent(studentId, courseId)
    return { ...data, courseId }
  }
)

const coursesSlice = createSlice({
  name: 'courses',
  initialState: {
    items: [],
    status: 'idle',
    error: null,
    currentCourse: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchCourses.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(fetchCourses.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.items = action.payload
      })
      .addCase(fetchCourses.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message
      })
      .addCase(fetchCourseById.fulfilled, (state, action) => {
        state.currentCourse = action.payload
      })
      .addCase(enrollInCourse.fulfilled, (state, action) => {
        // could update enrollment status in items
      })
  },
})

export default coursesSlice.reducer