from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    student_id: str = Field(..., description="Unique student identifier")
    name: str
    department: str
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    email: Optional[EmailStr] = None


class StudentInDB(StudentBase):
    id: str
    created_at: datetime
    updated_at: datetime


class StudentPublic(StudentInDB):
    pass


def serialize_student(doc: dict) -> StudentPublic:
    return StudentPublic(
        id=str(doc.get("_id")),
        student_id=doc.get("student_id"),
        name=doc.get("name"),
        department=doc.get("department"),
        email=doc.get("email"),
        created_at=doc.get("created_at"),
        updated_at=doc.get("updated_at"),
    )


