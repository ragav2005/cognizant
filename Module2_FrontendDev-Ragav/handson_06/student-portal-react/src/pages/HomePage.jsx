import { Link } from 'react-router-dom'

const HomePage = () => (
  <section className="home-page">
    <h2>Welcome to the Student Portal</h2>
    <p>Browse available courses, enroll in a course, and manage your profile.</p>
    <Link className="enroll-button home-cta" to="/courses">View courses</Link>
  </section>
)

export default HomePage
