from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AttachmentOut(BaseModel):
    id: UUID
    entity_type: str
    entity_id: str
    title: str
    description: Optional[str] = None
    file_path: str
    file_name: str
    file_size: int
    mime_type: Optional[str] = None
    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
