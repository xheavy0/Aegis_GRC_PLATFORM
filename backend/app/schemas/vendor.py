from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.vendor import VendorRisk, VendorStatus


class VendorBase(BaseModel):
    name: str
    category: Optional[str] = None
    risk_level: VendorRisk = VendorRisk.MEDIUM
    status: VendorStatus = VendorStatus.ACTIVE
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    contract_expiry: Optional[datetime] = None
    score: Optional[int] = None


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    risk_level: Optional[VendorRisk] = None
    status: Optional[VendorStatus] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    contract_expiry: Optional[datetime] = None
    score: Optional[int] = None


class VendorOut(VendorBase):
    id: UUID
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
