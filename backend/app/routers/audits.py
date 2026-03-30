from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.audit import Audit
from app.core.deps import get_current_user, require_analyst_or_above, log_action
from app.schemas.audit import AuditCreate, AuditUpdate, AuditOut

router = APIRouter()


@router.get("", response_model=List[AuditOut])
def list_audits(
    skip: int = 0, limit: int = 100,
    status: Optional[str] = None,
    audit_type: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Audit)
    if status:
        q = q.filter(Audit.status == status)
    if audit_type:
        q = q.filter(Audit.audit_type == audit_type)
    return q.order_by(Audit.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=AuditOut, status_code=status.HTTP_201_CREATED)
def create_audit(payload: AuditCreate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    audit = Audit(**payload.model_dump(), created_by=current.id)
    db.add(audit)
    db.commit()
    db.refresh(audit)
    log_action(db, current.id, "CREATE", "audit", audit.id, f"Created audit: {audit.title}")
    return audit


@router.get("/{audit_id}", response_model=AuditOut)
def get_audit(audit_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit


@router.patch("/{audit_id}", response_model=AuditOut)
def update_audit(audit_id: UUID, payload: AuditUpdate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(audit, field, val)
    db.commit()
    db.refresh(audit)
    log_action(db, current.id, "UPDATE", "audit", audit.id)
    return audit


@router.delete("/{audit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit(audit_id: UUID, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    db.delete(audit)
    db.commit()
    log_action(db, current.id, "DELETE", "audit", audit_id)
