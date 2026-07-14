const CourseCard = ({ id, name, code, credits, grade, onEnroll, isEnrolled }) => {
  const handleClick = () => {
    onEnroll({ id, name, code, credits, grade })
  }
  return (
    <article className="course-card">
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
