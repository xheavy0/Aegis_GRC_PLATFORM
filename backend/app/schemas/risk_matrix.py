from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime
from uuid import UUID

VALID_RATINGS = {"low", "medium", "high", "critical"}


class RiskMatrixConfigUpdate(BaseModel):
    likelihood_labels: List[str]
    impact_labels: List[str]
    cell_ratings: List[List[str]]

    @field_validator("likelihood_labels", "impact_labels")
    @classmethod
    def must_have_five(cls, v: List[str]) -> List[str]:
        if len(v) != 5:
            raise ValueError("Must contain exactly 5 labels")
        return v

    @field_validator("cell_ratings")
    @classmethod
    def validate_grid(cls, v: List[List[str]]) -> List[List[str]]:
        if len(v) != 5 or any(len(row) != 5 for row in v):
            raise ValueError("cell_ratings must be a 5x5 grid")
        for row in v:
            for cell in row:
                if cell not in VALID_RATINGS:
                    raise ValueError(f"Invalid rating '{cell}'. Must be one of: {VALID_RATINGS}")
        return v


class RiskMatrixConfigOut(RiskMatrixConfigUpdate):
    id: UUID
    updated_at: datetime

    class Config:
        from_attributes = True
