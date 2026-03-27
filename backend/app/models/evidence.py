from sqlalchemy import Column, String, Text, DateTime, Enum, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
import enum

from app.database import Base


class EvidenceStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    control_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(Enum(EvidenceStatus), default=EvidenceStatus.PENDING)
    source = Column(String(100), nullable=True)
    file_path = Column(String(1000), nullable=True)
    file_name = Column(String(500), nullable=True)
    file_size = Column(BigInteger, nullable=True)
    mime_type = Column(String(100), nullable=True)
    collected_at = Column(DateTime(timezone=True), nullable=True)
    collected_by = Column(String(255), nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
