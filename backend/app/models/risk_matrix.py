from sqlalchemy import Column, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from datetime import datetime, timezone
import uuid

from app.database import Base


DEFAULT_LIKELIHOOD_LABELS = ["Rare", "Unlikely", "Possible", "Likely", "Almost Certain"]
DEFAULT_IMPACT_LABELS = ["Negligible", "Minor", "Moderate", "Major", "Catastrophic"]

# cell_ratings[likelihood_index][impact_index]  (index 0 = level 1, index 4 = level 5)
DEFAULT_CELL_RATINGS = [
    ["low",    "low",    "low",    "medium",   "medium"],   # Likelihood 1
    ["low",    "low",    "medium", "medium",   "high"],     # Likelihood 2
    ["low",    "medium", "medium", "high",     "high"],     # Likelihood 3
    ["medium", "medium", "high",   "high",     "critical"], # Likelihood 4
    ["medium", "high",   "high",   "critical", "critical"], # Likelihood 5
]


class RiskMatrixConfig(Base):
    __tablename__ = "risk_matrix_config"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    likelihood_labels = Column(JSON, nullable=False, default=list(DEFAULT_LIKELIHOOD_LABELS))
    impact_labels = Column(JSON, nullable=False, default=list(DEFAULT_IMPACT_LABELS))
    # 5x5 nested list: cell_ratings[likelihood_index][impact_index] -> "low"|"medium"|"high"|"critical"
    cell_ratings = Column(JSON, nullable=False, default=lambda: [row[:] for row in DEFAULT_CELL_RATINGS])
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
