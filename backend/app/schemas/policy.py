from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.policy import PolicyStatus


class PolicyBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    status: PolicyStatus = PolicyStatus.DRAFT
    owner: Optional[str] = None
    version: str = "1.0"
    review_date: Optional[datetime] = None
    approved_by: Optional[str] = None


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    status: Optional[PolicyStatus] = None
    owner: Optional[str] = None
    version: Optional[str] = None
    review_date: Optional[datetime] = None
    approved_by: Optional[str] = None


class PolicyOut(PolicyBase):
    id: UUID
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
