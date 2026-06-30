from typing import Optional

from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from models import Course
from schemas import CourseCreate, CourseResponse, CourseUpdate
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title="Course Management API")


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def home():
    return {"message": "Course Management API Running"}


@app.get("/api/courses/", response_model=list[CourseResponse])
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


@app.get("/api/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Course).where(Course.id == course_id))

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@app.post("/api/courses/", response_model=CourseResponse, status_code=201)
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


@app.put("/api/courses/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int, update: CourseUpdate, db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(Course).where(Course.id == course_id))

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

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


@app.delete("/api/courses/{course_id}")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Course).where(Course.id == course_id))

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    await db.delete(course)

    await db.commit()

    return {"message": "Course deleted successfully"}
