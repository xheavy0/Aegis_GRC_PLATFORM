from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class FrameworkControlOut(BaseModel):
    id: UUID
    ref: str
    title: str
    description: Optional[str]
    status: str

    class Config:
        from_attributes = True


class FrameworkBase(BaseModel):
    name: str
    full_name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    is_active: bool = True


class FrameworkCreate(FrameworkBase):
    pass


class FrameworkUpdate(BaseModel):
    full_name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None


class FrameworkOut(FrameworkBase):
    id: UUID
    total_controls: int
    implemented_controls: int
    created_at: datetime
    controls: List[FrameworkControlOut] = []

    class Config:
        from_attributes = True
