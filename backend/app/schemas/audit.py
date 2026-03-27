from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.audit import AuditStatus, AuditType


class AuditBase(BaseModel):
    title: str
    audit_type: AuditType = AuditType.INTERNAL
    status: AuditStatus = AuditStatus.PLANNED
    description: Optional[str] = None
    auditor: Optional[str] = None
    scope: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class AuditCreate(AuditBase):
    pass


class AuditUpdate(BaseModel):
    title: Optional[str] = None
    audit_type: Optional[AuditType] = None
    status: Optional[AuditStatus] = None
    description: Optional[str] = None
    auditor: Optional[str] = None
    scope: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    findings_count: Optional[int] = None


class AuditOut(AuditBase):
    id: UUID
    findings_count: int
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
