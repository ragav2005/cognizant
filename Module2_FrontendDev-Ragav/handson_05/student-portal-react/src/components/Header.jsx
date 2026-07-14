const Header = (props) => {
  return (
    <header className="header">
      <div>
        <h1>{props.siteName}</h1>
        <p className="enrolled-count">Enrolled Courses: {props.enrolledCount}</p>
      </div>
      <nav>
        <a href="#">Home</a>
        <a href="#">Courses</a>
        <a href="#">Profile</a>
      </nav>
    </header>
  )
}

export default Header;
