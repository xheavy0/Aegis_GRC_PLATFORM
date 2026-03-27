from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import os
import uuid as uuid_lib
import aiofiles

from app.database import get_db
from app.models.evidence import Evidence
from app.core.deps import get_current_user, require_analyst_or_above, log_action
from app.schemas.evidence import EvidenceCreate, EvidenceUpdate, EvidenceOut

router = APIRouter()

UPLOAD_DIR = "uploads/evidence"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_MIME_TYPES = {
    "application/pdf", "image/png", "image/jpeg", "image/gif",
    "text/plain", "text/csv",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@router.get("", response_model=List[EvidenceOut])
def list_evidence(
    skip: int = 0, limit: int = 100,
    control_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Evidence)
    if control_id:
        q = q.filter(Evidence.control_id == control_id)
    if status:
        q = q.filter(Evidence.status == status)
    return q.order_by(Evidence.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=EvidenceOut, status_code=status.HTTP_201_CREATED)
def create_evidence(payload: EvidenceCreate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    evidence = Evidence(**payload.model_dump(), created_by=current.id)
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    log_action(db, current.id, "CREATE", "evidence", evidence.id, f"Created evidence: {evidence.title}")
    return evidence


@router.post("/upload", response_model=EvidenceOut, status_code=status.HTTP_201_CREATED)
async def upload_evidence(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    control_id: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current=Depends(require_analyst_or_above),
):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"File type not allowed: {file.content_type}")

    file_id = str(uuid_lib.uuid4())
    ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")

    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    evidence = Evidence(
        title=title,
        description=description,
        control_id=UUID(control_id) if control_id else None,
        source="manual",
        file_path=file_path,
        file_name=file.filename,
        file_size=len(content),
        mime_type=file.content_type,
        created_by=current.id,
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    log_action(db, current.id, "UPLOAD", "evidence", evidence.id, f"Uploaded file: {file.filename}")
    return evidence


@router.get("/{evidence_id}", response_model=EvidenceOut)
def get_evidence(evidence_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    ev = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return ev


@router.patch("/{evidence_id}", response_model=EvidenceOut)
def update_evidence(evidence_id: UUID, payload: EvidenceUpdate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    ev = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence not found")
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(ev, field, val)
    db.commit()
    db.refresh(ev)
    log_action(db, current.id, "UPDATE", "evidence", ev.id)
    return ev


@router.delete("/{evidence_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evidence(evidence_id: UUID, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    ev = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence not found")
    if ev.file_path and os.path.exists(ev.file_path):
        os.remove(ev.file_path)
    db.delete(ev)
    db.commit()
    log_action(db, current.id, "DELETE", "evidence", evidence_id)
