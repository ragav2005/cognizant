from typing import Optional
from models import User
from database import Base, engine, get_db
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Request,
    Response,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from datetime import datetime, timedelta
from models import Course, Enrollment, Student, User
from schemas import (
    CourseCreate,
    CourseListResponse,
    CourseResponse,
    CourseUpdate,
    EnrollmentCreate,
    EnrollmentResponse,
    ErrorResponse,
    StudentCreate,
    StudentResponse,
    UserRegister,
    UserResponse,
    LoginRequest,
    Token,
)
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException as StarletteHTTPException
from security import (
    get_password_hash,
    verify_password,
)

app = FastAPI(
    title="Course Management API",
    description="REST API for managing courses, students, and enrollments.",
    version="1.0.0",
)

API_PREFIX = "/api/v1"

# JWT settings
SECRET_KEY = "change-me-please-use-env-variable"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/auth/login/")

# Configure CORS to allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def error_payload(code: str, message: str, field: Optional[str] = None) -> dict:
    return {"error": {"code": code, "message": message, "field": field}}


def map_status_to_code(status_code: int) -> str:
    status_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        404: "NOT_FOUND",
        422: "UNPROCESSABLE_ENTITY",
    }
    return status_map.get(status_code, "HTTP_ERROR")


async def require_auth(authorization: Optional[str] = None) -> None:
    # Authentication removed per request — this function is a no-op.
    return None


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict):
        code = detail.get("code", map_status_to_code(exc.status_code))
        message = detail.get("message", "Request failed")
        field = detail.get("field")
    else:
        code = map_status_to_code(exc.status_code)
        message = str(detail)
        field = None
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(code, message, field),
    )


@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(_: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(map_status_to_code(exc.status_code), str(exc.detail)),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    field = (
        str(first_error.get("loc")[-1])
        if isinstance(first_error.get("loc"), tuple) and first_error.get("loc")
        else None
    )
    message = first_error.get("msg", "Schema validation failed")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_payload("UNPROCESSABLE_ENTITY", message, field),
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
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": f"Course with id {course_id} does not exist",
            },
        )
    return course


async def get_student_or_404(student_id: int, db: AsyncSession) -> Student:
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": f"Student with id {student_id} does not exist",
            },
        )
    return student


async def get_enrollment_or_404(enrollment_id: int, db: AsyncSession) -> Enrollment:
    result = await db.execute(select(Enrollment).where(Enrollment.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": f"Enrollment with id {enrollment_id} does not exist",
            },
        )
    return enrollment


def set_location_header(response: Response, path: str) -> None:
    response.headers["Location"] = path


def pagination_links(
    request: Request,
    page: int,
    page_size: int,
    total: int,
    search: Optional[str],
    department_id: Optional[int],
) -> tuple[Optional[str], Optional[str]]:
    query_params = {"page_size": page_size}
    if search:
        query_params["search"] = search
    if department_id is not None:
        query_params["department_id"] = department_id

    next_url = None
    previous_url = None
    if page * page_size < total:
        next_url = str(request.url.include_query_params(page=page + 1, **query_params))
    if page > 1:
        previous_url = str(
            request.url.include_query_params(page=page - 1, **query_params)
        )
    return next_url, previous_url


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail={"code": "UNAUTHORIZED", "message": "Could not validate credentials"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

router = APIRouter(prefix=API_PREFIX)


@router.get(
    "/courses/",
    response_model=CourseListResponse,
    tags=["Courses"],
    responses={
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def get_courses(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    department_id: Optional[int] = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    filters = []
    if department_id is not None:
        filters.append(Course.department_id == department_id)
    if search:
        pattern = f"%{search}%"
        filters.append(or_(Course.name.ilike(pattern), Course.code.ilike(pattern)))

    count_query = select(func.count()).select_from(Course)
    data_query = select(Course)
    for filter_expr in filters:
        count_query = count_query.where(filter_expr)
        data_query = data_query.where(filter_expr)

    total = await db.scalar(count_query)
    offset = (page - 1) * page_size
    result = await db.execute(data_query.offset(offset).limit(page_size))
    courses = result.scalars().all()

    next_url, previous_url = pagination_links(
        request=request,
        page=page,
        page_size=page_size,
        total=total or 0,
        search=search,
        department_id=department_id,
    )

    return {
        "count": total or 0,
        "next": next_url,
        "previous": previous_url,
        "results": courses,
    }


@router.get(
    "/courses/{course_id}/",
    response_model=CourseResponse,
    tags=["Courses"],
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    return await get_course_or_404(course_id, db)


@router.post(
    "/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
    response_description="Created course details",
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def create_course(
    course: CourseCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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
        raise HTTPException(
            status_code=400,
            detail={
                "code": "BAD_REQUEST",
                "message": "Course code already exists",
                "field": "code",
            },
        )
    await db.refresh(new_course)
    set_location_header(response, f"{API_PREFIX}/courses/{new_course.id}/")
    return new_course


@router.put(
    "/courses/{course_id}/",
    response_model=CourseResponse,
    tags=["Courses"],
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
    },
)
async def replace_course(
    course_id: int,
    payload: CourseCreate,
    db: AsyncSession = Depends(get_db),
):
    course = await get_course_or_404(course_id, db)
    course.name = payload.name
    course.code = payload.code
    course.credits = payload.credits
    course.department_id = payload.department_id
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail={
                "code": "BAD_REQUEST",
                "message": "Course code already exists",
                "field": "code",
            },
        )
    await db.refresh(course)
    return course


@router.patch(
    "/courses/{course_id}/",
    response_model=CourseResponse,
    tags=["Courses"],
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
    },
)
async def patch_course(
    course_id: int,
    update: CourseUpdate,
    db: AsyncSession = Depends(get_db),
):
    course = await get_course_or_404(course_id, db)
    data = update.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(course, key, value)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail={
                "code": "BAD_REQUEST",
                "message": "Course code already exists",
                "field": "code",
            },
        )
    await db.refresh(course)
    return course


@router.delete(
    "/courses/{course_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"],
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = await get_course_or_404(course_id, db)
    await db.delete(course)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/courses/{course_id}/students/",
    response_model=list[StudentResponse],
    tags=["Courses"],
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
)
async def get_course_students(
    course_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    await get_course_or_404(course_id, db)
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .where(Enrollment.course_id == course_id)
        .offset(offset)
        .limit(page_size)
    )
    return result.scalars().all()


@router.get("/students/", response_model=list[StudentResponse], tags=["Students"])
async def get_students(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * page_size
    result = await db.execute(select(Student).offset(offset).limit(page_size))
    return result.scalars().all()


@router.get(
    "/students/{student_id}/",
    response_model=StudentResponse,
    tags=["Students"],
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    return await get_student_or_404(student_id, db)


@router.post(
    "/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
)
async def create_student(
    student: StudentCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
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
        raise HTTPException(
            status_code=400,
            detail={
                "code": "BAD_REQUEST",
                "message": "Student email already exists",
                "field": "email",
            },
        )
    await db.refresh(new_student)
    set_location_header(response, f"{API_PREFIX}/students/{new_student.id}/")
    return new_student


@router.put(
    "/students/{student_id}/",
    response_model=StudentResponse,
    tags=["Students"],
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
    },
)
async def replace_student(
    student_id: int,
    payload: StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    student = await get_student_or_404(student_id, db)
    student.first_name = payload.first_name
    student.last_name = payload.last_name
    student.email = payload.email
    student.department_id = payload.department_id
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail={
                "code": "BAD_REQUEST",
                "message": "Student email already exists",
                "field": "email",
            },
        )
    await db.refresh(student)
    return student


@router.delete(
    "/students/{student_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"],
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
)
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await get_student_or_404(student_id, db)
    await db.delete(student)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/enrollments/",
    response_model=list[EnrollmentResponse],
    tags=["Enrollments"],
)
async def get_enrollments(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * page_size
    result = await db.execute(select(Enrollment).offset(offset).limit(page_size))
    return result.scalars().all()


@router.get(
    "/enrollments/{enrollment_id}/",
    response_model=EnrollmentResponse,
    tags=["Enrollments"],
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
)
async def get_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    return await get_enrollment_or_404(enrollment_id, db)


@router.post(
    "/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    response: Response,
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
    set_location_header(response, f"{API_PREFIX}/enrollments/{new_enrollment.id}/")
    return new_enrollment


@router.put(
    "/enrollments/{enrollment_id}/",
    response_model=EnrollmentResponse,
    tags=["Enrollments"],
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
)
async def replace_enrollment(
    enrollment_id: int,
    payload: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
):
    enrollment = await get_enrollment_or_404(enrollment_id, db)
    await get_student_or_404(payload.student_id, db)
    await get_course_or_404(payload.course_id, db)
    enrollment.student_id = payload.student_id
    enrollment.course_id = payload.course_id
    await db.commit()
    await db.refresh(enrollment)
    return enrollment


@router.delete(
    "/enrollments/{enrollment_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"],
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
)
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    enrollment = await get_enrollment_or_404(enrollment_id, db)
    await db.delete(enrollment)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail={"code": "UNAUTHORIZED", "message": "Could not validate credentials"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


@app.post(
    "/api/v1/auth/login/",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
)
async def login(
    creds: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == creds.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(creds.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail={"code": "UNAUTHORIZED", "message": "Incorrect email or password"},
        )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post(
    "/api/v1/auth/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
)
async def register(
    user: UserRegister,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(User).where(
            User.email == user.email
        )
    )

    existing = result.scalar_one_or_none()

    if existing:

        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(
            user.password
        ),
    )

    db.add(new_user)

    await db.commit()

    await db.refresh(new_user)

    return new_user


app.include_router(router)
