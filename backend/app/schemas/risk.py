from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.risk import RiskLevel, RiskStatus


class RiskBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    level: RiskLevel = RiskLevel.MEDIUM
    status: RiskStatus = RiskStatus.OPEN
    likelihood: int = 3
    impact: int = 3
    owner: Optional[str] = None
    due_date: Optional[datetime] = None


class RiskCreate(RiskBase):
    pass


class RiskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[RiskLevel] = None
    status: Optional[RiskStatus] = None
    likelihood: Optional[int] = None
    impact: Optional[int] = None
    owner: Optional[str] = None
    due_date: Optional[datetime] = None


class RiskOut(RiskBase):
    id: UUID
    risk_score: float
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
