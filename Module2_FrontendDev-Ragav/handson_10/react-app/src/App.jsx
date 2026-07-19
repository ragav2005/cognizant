import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchCourses } from './store/coursesSlice'
import CourseList from './components/CourseList'

function App() {
  const dispatch = useDispatch()
  const { items, status, error } = useSelector((state) => state.courses)

  useEffect(() => {
    dispatch(fetchCourses())
  }, [dispatch])

  return (
    <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto' }}>
      <h1>Student Portal</h1>
      {status === 'loading' && <p>Loading courses…</p>}
      {status === 'failed' && <p style={{ color: 'red' }}>Error: {error}</p>}
      {status === 'succeeded' && <CourseList courses={items} />}
    </div>
  )
}

export default App
