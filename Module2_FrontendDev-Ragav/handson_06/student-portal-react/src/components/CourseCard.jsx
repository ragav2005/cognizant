import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import { enroll } from '../features/enrollmentSlice'

const CourseCard = ({ id, name, code, credits, grade }) => {
  const dispatch = useDispatch()
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses)
  const navigate = useNavigate()
  const isEnrolled = enrolledCourses.some((course) => course.id === id)

  const handleClick = () => {
    dispatch(enroll({ id, name, code, credits, grade }))
    navigate('/profile')
  }
  return (
    <article className="course-card">
      <Link className="course-card-link" to={`/courses/${id}`}>
        <h2>{name}</h2>
        <p>
          <strong>Code:</strong> {code}
        </p>
        <p>
          <strong>Credits:</strong> {credits}
        </p>
        <p>
          <strong>Grade:</strong> {grade}
        </p>
      </Link>
      {!isEnrolled && <button
        type="button"
        className="enroll-button"
        onClick={handleClick}
      >
        Enroll
      </button>}
    </article>
  )
}

export default CourseCard
