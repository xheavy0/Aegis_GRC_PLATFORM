import os
import uuid as uuid_lib
from typing import List

import aiofiles
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.deps import get_current_user, log_action, require_analyst_or_above
from app.database import get_db
from app.models.attachment import Attachment
from app.schemas.attachment import AttachmentOut

router = APIRouter()

UPLOAD_DIR = "uploads/attachments"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_ENTITY_TYPES = {"vendor", "policy", "audit", "asset", "evidence", "gap", "risk"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/gif",
    "text/plain",
    "text/csv",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
MAX_UPLOAD_SIZE = 10 * 1024 * 1024


@router.get("", response_model=List[AttachmentOut])
def list_attachments(
    entity_type: str,
    entity_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return (
        db.query(Attachment)
        .filter(Attachment.entity_type == entity_type, Attachment.entity_id == entity_id)
        .order_by(Attachment.created_at.desc())
        .all()
    )


@router.post("/upload", response_model=AttachmentOut, status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    entity_type: str = Form(...),
    entity_id: str = Form(...),
    title: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current=Depends(require_analyst_or_above),
):
    if entity_type not in ALLOWED_ENTITY_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported entity_type")
    if not entity_id.strip():
        raise HTTPException(status_code=400, detail="entity_id is required")
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"File type not allowed: {file.content_type}")

    file_id = str(uuid_lib.uuid4())
    ext = os.path.splitext(file.filename or "")[1].lower()
    safe_filename = f"{file_id}{ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10 MB.")

    async with aiofiles.open(file_path, "wb") as handle:
        await handle.write(content)

    attachment = Attachment(
        entity_type=entity_type,
        entity_id=entity_id.strip(),
        title=title,
        description=description,
        file_path=file_path,
        file_name=file.filename or safe_filename,
        file_size=len(content),
        mime_type=file.content_type,
        created_by=current.id,
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    log_action(
        db,
        current.id,
        "UPLOAD",
        f"{entity_type}_attachment",
        attachment.id,
        f"Uploaded attachment for {entity_type}:{entity_id}",
    )
    return attachment


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attachment(
    attachment_id: UUID,
    db: Session = Depends(get_db),
    current=Depends(require_analyst_or_above),
):
    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    if attachment.file_path and os.path.exists(attachment.file_path):
        os.remove(attachment.file_path)
    db.delete(attachment)
    db.commit()
    log_action(db, current.id, "DELETE", "attachment", attachment_id, f"Deleted {attachment.file_name}")
