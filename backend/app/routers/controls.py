from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.control import Control
from app.core.deps import get_current_user, require_analyst_or_above, log_action
from app.schemas.control import ControlCreate, ControlUpdate, ControlOut

router = APIRouter()


@router.get("", response_model=List[ControlOut])
def list_controls(
    skip: int = 0, limit: int = 100,
    status: Optional[str] = None,
    framework: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Control)
    if status:
        q = q.filter(Control.status == status)
    if framework:
        q = q.filter(Control.framework == framework)
    return q.order_by(Control.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=ControlOut, status_code=status.HTTP_201_CREATED)
def create_control(payload: ControlCreate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    control = Control(**payload.model_dump(), created_by=current.id)
    db.add(control)
    db.commit()
    db.refresh(control)
    log_action(db, current.id, "CREATE", "control", control.id, f"Created control: {control.title}")
    return control


@router.get("/{control_id}", response_model=ControlOut)
def get_control(control_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    control = db.query(Control).filter(Control.id == control_id).first()
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    return control


@router.patch("/{control_id}", response_model=ControlOut)
def update_control(control_id: UUID, payload: ControlUpdate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    control = db.query(Control).filter(Control.id == control_id).first()
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(control, field, val)
    db.commit()
    db.refresh(control)
    log_action(db, current.id, "UPDATE", "control", control.id)
    return control


@router.delete("/{control_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_control(control_id: UUID, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    control = db.query(Control).filter(Control.id == control_id).first()
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    db.delete(control)
    db.commit()
    log_action(db, current.id, "DELETE", "control", control_id)
