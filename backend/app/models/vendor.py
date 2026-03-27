from sqlalchemy import Column, String, Text, DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
import enum

from app.database import Base


class VendorRisk(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class VendorStatus(str, enum.Enum):
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    INACTIVE = "inactive"
    TERMINATED = "terminated"


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(500), nullable=False)
    category = Column(String(100), nullable=True)
    risk_level = Column(Enum(VendorRisk), default=VendorRisk.MEDIUM)
    status = Column(Enum(VendorStatus), default=VendorStatus.ACTIVE)
    contact_name = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    contract_expiry = Column(DateTime(timezone=True), nullable=True)
    score = Column(Integer, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
