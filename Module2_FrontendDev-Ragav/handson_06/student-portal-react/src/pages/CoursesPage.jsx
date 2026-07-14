import CourseCard from '../components/CourseCard'

const CoursesPage = ({ courses, searchTerm, setSearchTerm, loading, error }) => {
  const displayedCourses = courses.filter((course) => {
    const query = searchTerm.toLowerCase().trim()
    return course.name.toLowerCase().includes(query) || course.code.toLowerCase().includes(query)
  })

  return (
    <section className="course-list-section">
      <h2>Courses</h2>
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
        {!loading && !error && displayedCourses.map((course) => (
          <CourseCard
            key={course.id}
            {...course}
          />
        ))}
      </div>
    </section>
  )
}

export default CoursesPage
