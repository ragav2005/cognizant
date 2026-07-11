from models import Course, Department, Enrollment, Student
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:p%40ssw0rd@localhost/college_db_orm"

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)

session = Session()

cs = Department(dept_name="Computer Science")
it = Department(dept_name="Information Technology")
ece = Department(dept_name="Electronics")

session.add_all([cs, it, ece])
session.commit()

students = [
    Student(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        enrollment_year=2022,
        department=cs,
    ),
    Student(
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        enrollment_year=2022,
        department=cs,
    ),
    Student(
        first_name="Bob",
        last_name="Brown",
        email="bob@example.com",
        enrollment_year=2023,
        department=it,
    ),
    Student(
        first_name="David",
        last_name="Lee",
        email="david@example.com",
        enrollment_year=2023,
        department=ece,
    ),
    Student(
        first_name="Emma",
        last_name="White",
        email="emma@example.com",
        enrollment_year=2024,
        department=cs,
    ),
]

session.add_all(students)
session.commit()

courses = [
    Course(course_name="Database Systems", course_code="CS301", credits=4),
    Course(course_name="Operating Systems", course_code="CS302", credits=4),
    Course(course_name="Computer Networks", course_code="CS303", credits=3),
]

session.add_all(courses)
session.commit()

enrollments = [
    Enrollment(student_id=1, course_id=1, grade="A"),
    Enrollment(student_id=2, course_id=1, grade="B"),
    Enrollment(student_id=3, course_id=2, grade="A"),
    Enrollment(student_id=4, course_id=3, grade="C"),
]

session.add_all(enrollments)
session.commit()

students = (
    session.query(Student)
    .join(Department)
    .filter(Department.dept_name == "Computer Science")
    .all()
)

for s in students:
    print(s.first_name, s.last_name)
