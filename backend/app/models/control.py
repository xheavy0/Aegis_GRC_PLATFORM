from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
import enum

from app.database import Base


class ControlStatus(str, enum.Enum):
    IMPLEMENTED = "implemented"
    PARTIAL = "partial"
    PLANNED = "planned"
    NOT_IMPLEMENTED = "not_implemented"


class ControlType(str, enum.Enum):
    PREVENTIVE = "preventive"
    DETECTIVE = "detective"
    CORRECTIVE = "corrective"
    COMPENSATING = "compensating"


class Control(Base):
    __tablename__ = "controls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    control_type = Column(Enum(ControlType), default=ControlType.PREVENTIVE)
    status = Column(Enum(ControlStatus), default=ControlStatus.PLANNED)
    framework = Column(String(100), nullable=True)
    framework_ref = Column(String(100), nullable=True)
    owner = Column(String(255), nullable=True)
    effectiveness = Column(String(50), nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
