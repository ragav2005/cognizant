export default function CourseCard({ course }) {
  return (
    <article style={{ border: '1px solid #dbe3f0', borderRadius: '0.5rem', padding: '1rem', background: 'white' }}>
      <p style={{ color: '#334155', margin: '0 0 0.25rem', fontSize: '0.85rem' }}>{course.code}</p>
      <h3 style={{ margin: '0 0 0.5rem' }}>{course.name}</h3>
      <div>
        <span>{course.credits} credits</span> <br />
        <strong>Grade: {course.grade}</strong>
      </div>
    </article>
  )
}