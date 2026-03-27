from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
import enum

from app.database import Base


class AssetType(str, enum.Enum):
    SERVER = "server"
    WORKSTATION = "workstation"
    APPLICATION = "application"
    DATABASE = "database"
    NETWORK = "network"
    CLOUD = "cloud"
    OTHER = "other"


class AssetCriticality(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(500), nullable=False)
    asset_type = Column(Enum(AssetType), default=AssetType.OTHER)
    criticality = Column(Enum(AssetCriticality), default=AssetCriticality.MEDIUM)
    description = Column(Text, nullable=True)
    owner = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    tags = Column(String(500), nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
