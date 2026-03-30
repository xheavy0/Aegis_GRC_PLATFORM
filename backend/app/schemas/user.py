from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.VIEWER
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserOut(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class LoginRequest(BaseModel):
    email: str
    password: str


class AuditLogOut(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    action: str
    resource: str
    resource_id: Optional[str]
    detail: Optional[str]
    ip_address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
