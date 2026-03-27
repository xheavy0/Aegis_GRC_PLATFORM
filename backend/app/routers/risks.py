from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.risk import Risk
from app.core.deps import get_current_user, require_analyst_or_above, log_action
from app.schemas.risk import RiskCreate, RiskUpdate, RiskOut

router = APIRouter()


@router.get("", response_model=List[RiskOut])
def list_risks(
    skip: int = 0, limit: int = 100,
    status: Optional[str] = None,
    level: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Risk)
    if status:
        q = q.filter(Risk.status == status)
    if level:
        q = q.filter(Risk.level == level)
    return q.order_by(Risk.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=RiskOut, status_code=status.HTTP_201_CREATED)
def create_risk(payload: RiskCreate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    risk = Risk(**payload.model_dump(), created_by=current.id)
    risk.risk_score = float(risk.likelihood * risk.impact)
    db.add(risk)
    db.commit()
    db.refresh(risk)
    log_action(db, current.id, "CREATE", "risk", risk.id, f"Created risk: {risk.title}")
    return risk


@router.get("/{risk_id}", response_model=RiskOut)
def get_risk(risk_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    return risk


@router.patch("/{risk_id}", response_model=RiskOut)
def update_risk(risk_id: UUID, payload: RiskUpdate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(risk, field, val)
    risk.risk_score = float(risk.likelihood * risk.impact)
    db.commit()
    db.refresh(risk)
    log_action(db, current.id, "UPDATE", "risk", risk.id, f"Updated risk: {risk.title}")
    return risk


@router.delete("/{risk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_risk(risk_id: UUID, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    db.delete(risk)
    db.commit()
    log_action(db, current.id, "DELETE", "risk", risk_id, f"Deleted risk: {risk.title}")
