import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'

const Header = () => {
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses)

  return (
    <header className="header">
      <div>
        <h1>Student Portal</h1>
        <p className="enrolled-count">Enrolled Courses: {enrolledCourses.length}</p>
      </div>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/courses">Courses</Link>
        <Link to="/profile">Profile</Link>
      </nav>
    </header>
  )
}

export default Header;
