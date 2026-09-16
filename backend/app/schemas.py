from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class APIMessage(BaseModel):
    success: bool = True
    message: str
    code: str = "OK"


class RegisterStart(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def gmail_only(cls, value: str) -> str:
        value = value.lower()
        if not value.endswith("@gmail.com"):
            raise ValueError("Only Gmail addresses can register.")
        return value


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
    purpose: str = "register"


class CompleteRegistration(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)
    name: str = Field(min_length=2, max_length=120)
    username: str = Field(min_length=3, max_length=80)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ResetPassword(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    username: str = Field(min_length=3, max_length=80)
    bio: str = Field(default="", max_length=600)
    location: str = Field(default="", max_length=120)
    availability: str = Field(default="Available", max_length=40)
    skills: list[str] = Field(default_factory=list, max_length=12)


class PostCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
    media_url: str = ""
    media_type: str = ""


class WorkCreate(BaseModel):
    title: str = Field(min_length=3, max_length=180)
    description: str = Field(min_length=10, max_length=5000)
    budget: float = Field(ge=0)
    deadline_duration_days: int = Field(ge=1, le=365)
    application_deadline: datetime | None = None
    location: str = Field(default="Remote", max_length=120)
    work_mode: str = Field(default="Remote", max_length=30)


class ApplicationCreate(BaseModel):
    message: str = Field(default="", max_length=1000)


class WorkAction(BaseModel):
    note: str = Field(default="", max_length=2000)


class ExtendWork(BaseModel):
    days: int = Field(ge=1, le=90)
    reason: str = Field(default="", max_length=500)


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=1000)


class WalletTopUp(BaseModel):
    amount: float = Field(gt=0, le=100000)


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class AIQuery(BaseModel):
    query: str = Field(min_length=1, max_length=500)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    username: str
    email: str
    bio: str
    location: str
    availability: str
    profile_image: str
    skills: list[str] = []
    rating: float = 0
    completed_works: int = 0


class WorkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    requester_id: int
    assignee_id: int | None
    title: str
    description: str
    status: str
    budget: float
    deadline_duration_days: int
    application_deadline: datetime | None
    accepted_at: datetime | None
    due_at: datetime | None
    submitted_at: datetime | None
    completed_at: datetime | None
    is_overdue: bool
    was_submitted_late: bool
    location: str
    work_mode: str
    progress: int
    requester_name: str = ""
    assignee_name: str = ""


class PostOut(BaseModel):
    id: int
    content: str
    media_url: str
    media_type: str
    likes_count: int
    comments_count: int
    created_at: datetime
    author: UserOut


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type: str
    title: str
    body: str
    is_read: bool
    created_at: datetime