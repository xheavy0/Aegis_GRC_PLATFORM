from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.database import Base


class Framework(Base):
    __tablename__ = "frameworks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    full_name = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    version = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    total_controls = Column(Integer, default=0)
    implemented_controls = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    controls = relationship("FrameworkControl", back_populates="framework", cascade="all, delete-orphan")


class FrameworkControl(Base):
    __tablename__ = "framework_controls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    framework_id = Column(UUID(as_uuid=True), ForeignKey("frameworks.id", ondelete="CASCADE"), nullable=False)
    ref = Column(String(100), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="not_implemented")

    framework = relationship("Framework", back_populates="controls")
