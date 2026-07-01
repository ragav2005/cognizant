from typing import Optional

from pydantic import BaseModel, ConfigDict


class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department_id: int


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    department_id: Optional[int] = None


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department_id: int

    model_config = ConfigDict(from_attributes=True)


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int

    model_config = ConfigDict(from_attributes=True)
