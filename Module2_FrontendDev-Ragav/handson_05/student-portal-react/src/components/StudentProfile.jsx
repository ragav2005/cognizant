import { useState } from 'react'

const StudentProfile = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [semester, setSemester] = useState('')

  return (
    <section className="student-profile">
      <h2>Student Profile</h2>
      <form className="profile-form">
        <label htmlFor="name">Name</label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />

        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />

        <label htmlFor="semester">Semester</label>
        <input
          id="semester"
          type="text"
          value={semester}
          onChange={(event) => setSemester(event.target.value)}
        />
      </form>
    </section>
  )
}

export default StudentProfile
