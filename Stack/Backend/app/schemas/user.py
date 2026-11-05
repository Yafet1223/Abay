from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.user import UserRole


# Shared user fields
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: UserRole


# Employee registration
class UserCreate(UserBase):
    password: str


# Employee update
class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None


# User response
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)