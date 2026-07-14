import { useDispatch, useSelector } from 'react-redux'
import StudentProfile from '../components/StudentProfile'
import { unenroll } from '../features/enrollmentSlice'

const ProfilePage = () => {
  const dispatch = useDispatch()
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses)

  return (
    <section className="profile-page">
      <StudentProfile />
      <section className="enrolled-courses">
        <h2>My Enrolled Courses</h2>
        {enrolledCourses.length === 0 ? (
          <p>You have not enrolled in any courses yet.</p>
        ) : (
          <ul>
            {enrolledCourses.map((course) => (
              <li key={course.id}>
                {course.name} ({course.code})
                <button type="button" className="unenroll-button" onClick={() => dispatch(unenroll(course.id))}>
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </section>
  )
}

export default ProfilePage
