import { useEffect, useState } from 'react'
import './App.css'
import Header from './components/Header'
import Footer from './components/Footer'
import CourseCard from './components/CourseCard'
import StudentProfile from './components/StudentProfile'

const App = () => {
  const [courses, setCourses] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [enrolledCourses, setEnrolledCourses] = useState([])
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

  const displayedCourses = courses.filter((course) => {
    const query = searchTerm.toLowerCase().trim()
    return (
      course.name.toLowerCase().includes(query) ||
      course.code.toLowerCase().includes(query)
    )
  })




  const handleEnroll = (courseToEnroll) => {
    setEnrolledCourses((currentEnrolledCourses) => {
      const enrolledIDs = currentEnrolledCourses.map((course) => course.id)
      if (enrolledIDs.includes(courseToEnroll.id)) {
        return currentEnrolledCourses
      }

      return [...currentEnrolledCourses, courseToEnroll]
    })
  }

  return (
    <div className="app">
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />
      <main className="content">
        <section className="course-list-section">
          <input
            type="text"
            className="search-input"
            placeholder="Search by course name or code"
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
          />
          <div className="course-list">
            {loading && <p className="status-text">Loading...</p>}
            {!loading && error && <p className="status-text error-text">{error}</p>}
            {!loading &&
              !error &&
              displayedCourses.map((course) => (
                <CourseCard
                  key={course.id}
                  {...course}
                  onEnroll={handleEnroll}
                  isEnrolled={enrolledCourses.some((enrolled) => enrolled.id === course.id)}
                />
              ))}
          </div>
          <StudentProfile />
        </section>
      </main>
      <Footer />
    </div>
  )
}

export default App
