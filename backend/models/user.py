from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserInDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime


class UserPublic(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime


def serialize_user(doc: dict) -> UserPublic:
    return UserPublic(
        id=str(doc.get("_id")),
        email=doc.get("email"),
        username=doc.get("username"),
        full_name=doc.get("full_name"),
        is_active=doc.get("is_active", True),
        is_admin=doc.get("is_admin", False),
        created_at=doc.get("created_at"),
        updated_at=doc.get("updated_at"),
    )


def serialize_user_in_db(doc: dict) -> UserInDB:
    return UserInDB(
        id=str(doc.get("_id")),
        email=doc.get("email"),
        username=doc.get("username"),
        full_name=doc.get("full_name"),
        is_active=doc.get("is_active", True),
        is_admin=doc.get("is_admin", False),
        hashed_password=doc.get("hashed_password"),
        created_at=doc.get("created_at"),
        updated_at=doc.get("updated_at"),
    )
