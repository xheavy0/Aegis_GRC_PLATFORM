from sqlalchemy import Column, String, Text, DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
import enum

from app.database import Base


class AuditStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AuditType(str, enum.Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    REGULATORY = "regulatory"
    VENDOR = "vendor"


class Audit(Base):
    __tablename__ = "audits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    audit_type = Column(Enum(AuditType), default=AuditType.INTERNAL)
    status = Column(Enum(AuditStatus), default=AuditStatus.PLANNED)
    description = Column(Text, nullable=True)
    auditor = Column(String(255), nullable=True)
    scope = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    findings_count = Column(Integer, default=0)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
