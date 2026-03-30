from sqlalchemy import Column, String, Integer, Text, DateTime, Enum, Float
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
import enum

from app.database import Base


class RiskStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    MITIGATED = "mitigated"
    ACCEPTED = "accepted"
    CLOSED = "closed"


class RiskLevel(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Risk(Base):
    __tablename__ = "risks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    level = Column(Enum(RiskLevel), default=RiskLevel.MEDIUM, nullable=False)
    status = Column(Enum(RiskStatus), default=RiskStatus.OPEN, nullable=False)
    likelihood = Column(Integer, default=3)   # 1-5
    impact = Column(Integer, default=3)       # 1-5
    risk_score = Column(Float, default=9.0)   # likelihood * impact
    owner = Column(String(255), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
