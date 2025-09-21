from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    student_id: str = Field(..., description="Unique ID for the student")
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
    id: str = Field(..., description="MongoDB string id")
    created_at: datetime
    updated_at: datetime


class StudentPublic(StudentBase):
    id: str
    created_at: datetime
    updated_at: datetime


class AnalyticsResponse(BaseModel):
    total_students: int
    students_by_department: List[dict]
    recent_onboarded: List[StudentPublic]
    active_last_7_days: int


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class VoiceChatRequest(BaseModel):
    messages: List[ChatMessage]
    include_audio: bool = True  # Whether to include audio response


class VoiceUploadRequest(BaseModel):
    audio_data: str  # Base64 encoded audio data
    include_audio: bool = True


class ChatHistoryEntry(BaseModel):
    id: Optional[str] = None
    user_id: str
    session_id: str
    user_message: str
    ai_response: str
    timestamp: datetime
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    user_id: str
    total_chats: int
    chats: List[ChatHistoryEntry]


class UserChatRequest(BaseModel):
    user_id: str
    messages: List[ChatMessage]


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class SignupRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


