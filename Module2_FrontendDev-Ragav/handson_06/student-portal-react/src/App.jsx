import { useEffect, useState } from 'react'
import { Route, Routes } from 'react-router-dom'
import './App.css'
import Header from './components/Header'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import CoursesPage from './pages/CoursesPage'
import ProfilePage from './pages/ProfilePage'
import CourseDetailPage from './pages/CourseDetailPage'

const App = () => {
  const [courses, setCourses] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true)
        setError('')

        const response = await fetch('/api/posts')
        if (!response.ok) {
          throw new Error('Failed to load courses.')
        }

        const posts = await response.json()
        const mappedCourses = posts.slice(0, 5).map((post) => ({
          id: post.id,
          name: post.title,
          code: `COURSE-${String(post.id).padStart(3, '0')}`,
          credits: (post.id % 3) + 2,
          grade: 'N/A',
        }))

        setCourses(mappedCourses)
      } catch (fetchError) {
        setError(fetchError.message)
      } finally {
        setLoading(false)
      }
    }

    fetchCourses()
  }, [])

  useEffect(() => {
    // dependency array makes sures this part is re-rendered
    if (!loading && !error) {
      console.log('Courses updated')
    }
  }, [courses, loading, error])

  return (
    <div className="app">
      <Header />
      <main className="content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route
            path="/courses"
            element={
              <CoursesPage
                courses={courses}
                searchTerm={searchTerm}
                setSearchTerm={setSearchTerm}
                loading={loading}
                error={error}
              />
            }
          />
          <Route path="/profile" element={<ProfilePage />} />
          <Route
            path="/courses/:courseId"
            element={
              <CourseDetailPage
                courses={courses}
                loading={loading}
                error={error}
              />
            }
          />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}

export default App
