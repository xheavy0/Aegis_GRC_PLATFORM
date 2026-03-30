from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.evidence import EvidenceStatus


class EvidenceBase(BaseModel):
    title: str
    description: Optional[str] = None
    control_id: Optional[UUID] = None
    status: EvidenceStatus = EvidenceStatus.PENDING
    source: Optional[str] = None
    collected_at: Optional[datetime] = None
    collected_by: Optional[str] = None


class EvidenceCreate(EvidenceBase):
    pass


class EvidenceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    control_id: Optional[UUID] = None
    status: Optional[EvidenceStatus] = None
    source: Optional[str] = None
    collected_at: Optional[datetime] = None
    collected_by: Optional[str] = None


class EvidenceOut(EvidenceBase):
    id: UUID
    file_path: Optional[str]
    file_name: Optional[str]
    file_size: Optional[int]
    mime_type: Optional[str]
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
