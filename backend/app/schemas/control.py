from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.control import ControlStatus, ControlType


class ControlBase(BaseModel):
    title: str
    description: Optional[str] = None
    control_type: ControlType = ControlType.PREVENTIVE
    status: ControlStatus = ControlStatus.PLANNED
    framework: Optional[str] = None
    framework_ref: Optional[str] = None
    owner: Optional[str] = None
    effectiveness: Optional[str] = None


class ControlCreate(ControlBase):
    pass


class ControlUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    control_type: Optional[ControlType] = None
    status: Optional[ControlStatus] = None
    framework: Optional[str] = None
    framework_ref: Optional[str] = None
    owner: Optional[str] = None
    effectiveness: Optional[str] = None


class ControlOut(ControlBase):
    id: UUID
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
