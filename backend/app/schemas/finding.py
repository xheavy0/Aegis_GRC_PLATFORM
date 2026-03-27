from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.finding import FindingSeverity, FindingStatus


class FindingBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: FindingSeverity = FindingSeverity.MEDIUM
    status: FindingStatus = FindingStatus.OPEN
    source: Optional[str] = None
    asset_id: Optional[UUID] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    remediation: Optional[str] = None


class FindingCreate(FindingBase):
    pass


class FindingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[FindingSeverity] = None
    status: Optional[FindingStatus] = None
    source: Optional[str] = None
    asset_id: Optional[UUID] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    remediation: Optional[str] = None


class FindingOut(FindingBase):
    id: UUID
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
