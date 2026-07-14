import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { enroll } from '../features/enrollmentSlice'

const CourseDetailPage = ({ courses, loading, error }) => {
  const { courseId } = useParams()
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses)
  const course = courses.find((item) => String(item.id) === courseId)

  if (loading) return <p className="status-text">Loading course...</p>
  if (error) return <p className="status-text error-text">{error}</p>
  if (!course) {
    return (
      <section className="course-detail">
        <h2>Course not found</h2>
        <Link to="/courses">Back to courses</Link>
      </section>
    )
  }

  const isEnrolled = enrolledCourses.some((enrolled) => enrolled.id === course.id)
  const handleEnroll = () => {
    dispatch(enroll(course))
    navigate('/profile')
  }

  return (
    <section className="course-detail">
      <Link to="/courses">← Back to courses</Link>
      <h2>{course.name}</h2>
      <p><strong>Code:</strong> {course.code}</p>
      <p><strong>Credits:</strong> {course.credits}</p>
      <p><strong>Grade:</strong> {course.grade}</p>
      {isEnrolled ? <p className="enrolled-message">You are enrolled in this course.</p> : (
        <button type="button" className="enroll-button" onClick={handleEnroll}>Enroll</button>
      )}
    </section>
  )
}

export default CourseDetailPage
