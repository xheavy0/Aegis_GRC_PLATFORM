from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.finding import Finding
from app.core.deps import get_current_user, require_analyst_or_above, log_action
from app.schemas.finding import FindingCreate, FindingUpdate, FindingOut

router = APIRouter()


@router.get("", response_model=List[FindingOut])
def list_findings(
    skip: int = 0, limit: int = 100,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Finding)
    if severity:
        q = q.filter(Finding.severity == severity)
    if status:
        q = q.filter(Finding.status == status)
    return q.order_by(Finding.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=FindingOut, status_code=status.HTTP_201_CREATED)
def create_finding(payload: FindingCreate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    finding = Finding(**payload.model_dump(), created_by=current.id)
    db.add(finding)
    db.commit()
    db.refresh(finding)
    log_action(db, current.id, "CREATE", "finding", finding.id, f"Created finding: {finding.title}")
    return finding


@router.get("/{finding_id}", response_model=FindingOut)
def get_finding(finding_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return finding


@router.patch("/{finding_id}", response_model=FindingOut)
def update_finding(finding_id: UUID, payload: FindingUpdate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(finding, field, val)
    db.commit()
    db.refresh(finding)
    log_action(db, current.id, "UPDATE", "finding", finding.id)
    return finding


@router.delete("/{finding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_finding(finding_id: UUID, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    db.delete(finding)
    db.commit()
    log_action(db, current.id, "DELETE", "finding", finding_id)
