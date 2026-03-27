from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.asset import AssetType, AssetCriticality


class AssetBase(BaseModel):
    name: str
    asset_type: AssetType = AssetType.OTHER
    criticality: AssetCriticality = AssetCriticality.MEDIUM
    description: Optional[str] = None
    owner: Optional[str] = None
    location: Optional[str] = None
    ip_address: Optional[str] = None
    tags: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    asset_type: Optional[AssetType] = None
    criticality: Optional[AssetCriticality] = None
    description: Optional[str] = None
    owner: Optional[str] = None
    location: Optional[str] = None
    ip_address: Optional[str] = None
    tags: Optional[str] = None


class AssetOut(AssetBase):
    id: UUID
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
