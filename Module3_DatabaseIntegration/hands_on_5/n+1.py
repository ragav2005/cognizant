from models import Course, Department, Enrollment, Student
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:p%40ssw0rd@localhost/college_db_orm"

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)

session = Session()

enrollments = session.query(Enrollment).all()

for e in enrollments:
    print(e.student.first_name, e.course.course_name)

student = session.query(Student).filter(Student.email == "john@example.com").first()

student.enrollment_year = 2024

session.commit()

print("Updated")

enrollment = session.query(Enrollment).first()

session.delete(enrollment)

session.commit()

print("Deleted")

enrollments = session.query(Enrollment).all()

enrollments = (
    session.query(Enrollment)
    .options(joinedload(Enrollment.student), joinedload(Enrollment.course))
    .all()
)

for e in enrollments:
    print(e.student.first_name, e.course.course_name)

"""
N+1 ANALYSIS

Before joinedload:
1 query for enrollments
N queries for students
N queries for courses

For 6 enrollments:
1 + 6 + 6 = 13 queries

For 10,000 enrollments:
1 + 10,000 + 10,000
= 20,001 queries

After joinedload:

session.query(Enrollment)
.options(
    joinedload(Enrollment.student),
    joinedload(Enrollment.course)
)

Only 1 SQL query is executed.

This eliminates the N+1 problem and greatly improves performance.
"""
