from typing import Optional

from database import Base, engine, get_db
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Response, status
from models import Course, Enrollment, Student
from schemas import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    EnrollmentCreate,
    EnrollmentResponse,
    EnrollmentUpdate,
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(
    title="Course Management API",
    description=(
        """
        Course Management REST API built using FastAPI.

        Features:
        - Course CRUD
        - Student CRUD
        - Enrollment CRUD
        - Async SQLAlchemy
        - Background Tasks
        - OpenAPI Documentation
        """
    ),
    version="1.0.0",
    contact={
        "name": "Digital Nurture Team",
        "email": "support@example.com",
    },
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def home():
    return {"message": "Course Management API Running"}


def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}")


async def get_course_or_404(course_id: int, db: AsyncSession) -> Course:
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


async def get_student_or_404(student_id: int, db: AsyncSession) -> Student:
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


async def get_enrollment_or_404(enrollment_id: int, db: AsyncSession) -> Enrollment:
    result = await db.execute(select(Enrollment).where(Enrollment.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


@app.get("/api/courses/", response_model=list[CourseResponse], tags=["Courses"])
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):

    query = select(Course)

    if department_id is not None:
        query = query.where(Course.department_id == department_id)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)

    courses = result.scalars().all()

    return courses


@app.get("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):

    return await get_course_or_404(course_id, db)


@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
    response_description="Created course details",
)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):

    new_course = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id,
    )

    db.add(new_course)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Course code already exists")

    await db.refresh(new_course)

    return new_course


@app.put("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def update_course(
    course_id: int, update: CourseUpdate, db: AsyncSession = Depends(get_db)
):

    course = await get_course_or_404(course_id, db)

    data = update.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(course, key, value)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Course code already exists")

    await db.refresh(course)

    return course


@app.delete(
    "/api/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"],
)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):

    course = await get_course_or_404(course_id, db)

    await db.delete(course)

    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get(
    "/api/courses/{course_id}/students/",
    response_model=list[StudentResponse],
    tags=["Courses"],
)
async def get_course_students(
    course_id: int, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):

    await get_course_or_404(course_id, db)

    result = await db.execute(
        select(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .where(Enrollment.course_id == course_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@app.get("/api/students/", response_model=list[StudentResponse], tags=["Students"])
async def get_students(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).offset(skip).limit(limit))
    return result.scalars().all()


@app.get(
    "/api/students/{student_id}", response_model=StudentResponse, tags=["Students"]
)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    return await get_student_or_404(student_id, db)


@app.post(
    "/api/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    new_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        department_id=student.department_id,
    )
    db.add(new_student)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Student email already exists")

    await db.refresh(new_student)
    return new_student


@app.put(
    "/api/students/{student_id}", response_model=StudentResponse, tags=["Students"]
)
async def update_student(
    student_id: int, update: StudentUpdate, db: AsyncSession = Depends(get_db)
):
    student = await get_student_or_404(student_id, db)
    data = update.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(student, key, value)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Student email already exists")

    await db.refresh(student)
    return student


@app.delete(
    "/api/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"],
)
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await get_student_or_404(student_id, db)
    await db.delete(student)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get(
    "/api/enrollments/", response_model=list[EnrollmentResponse], tags=["Enrollments"]
)
async def get_enrollments(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Enrollment).offset(skip).limit(limit))
    return result.scalars().all()


@app.get(
    "/api/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    tags=["Enrollments"],
)
async def get_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    return await get_enrollment_or_404(enrollment_id, db)


@app.post(
    "/api/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    student = await get_student_or_404(enrollment.student_id, db)
    await get_course_or_404(enrollment.course_id, db)

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
    )
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    background_tasks.add_task(send_confirmation_email, student.email)
    return new_enrollment


@app.put(
    "/api/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    tags=["Enrollments"],
)
async def update_enrollment(
    enrollment_id: int, update: EnrollmentUpdate, db: AsyncSession = Depends(get_db)
):
    enrollment = await get_enrollment_or_404(enrollment_id, db)
    data = update.model_dump(exclude_unset=True)

    if "student_id" in data:
        await get_student_or_404(data["student_id"], db)
    if "course_id" in data:
        await get_course_or_404(data["course_id"], db)

    for key, value in data.items():
        setattr(enrollment, key, value)

    await db.commit()
    await db.refresh(enrollment)
    return enrollment


@app.delete(
    "/api/enrollments/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"],
)
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    enrollment = await get_enrollment_or_404(enrollment_id, db)
    await db.delete(enrollment)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
