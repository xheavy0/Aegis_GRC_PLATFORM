from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.framework import Framework
from app.core.deps import get_current_user, require_admin, log_action
from app.schemas.framework import FrameworkCreate, FrameworkUpdate, FrameworkOut

router = APIRouter()


@router.get("", response_model=List[FrameworkOut])
def list_frameworks(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Framework).order_by(Framework.name).all()


@router.post("", response_model=FrameworkOut, status_code=status.HTTP_201_CREATED)
def create_framework(payload: FrameworkCreate, db: Session = Depends(get_db), current=Depends(require_admin)):
    if db.query(Framework).filter(Framework.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Framework already exists")
    fw = Framework(**payload.model_dump())
    db.add(fw)
    db.commit()
    db.refresh(fw)
    log_action(db, current.id, "CREATE", "framework", fw.id, f"Created framework: {fw.name}")
    return fw


@router.get("/{framework_id}", response_model=FrameworkOut)
def get_framework(framework_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    fw = db.query(Framework).filter(Framework.id == framework_id).first()
    if not fw:
        raise HTTPException(status_code=404, detail="Framework not found")
    return fw


@router.patch("/{framework_id}", response_model=FrameworkOut)
def update_framework(framework_id: UUID, payload: FrameworkUpdate, db: Session = Depends(get_db), current=Depends(require_admin)):
    fw = db.query(Framework).filter(Framework.id == framework_id).first()
    if not fw:
        raise HTTPException(status_code=404, detail="Framework not found")
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(fw, field, val)
    db.commit()
    db.refresh(fw)
    log_action(db, current.id, "UPDATE", "framework", fw.id)
    return fw


@router.delete("/{framework_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_framework(framework_id: UUID, db: Session = Depends(get_db), current=Depends(require_admin)):
    fw = db.query(Framework).filter(Framework.id == framework_id).first()
    if not fw:
        raise HTTPException(status_code=404, detail="Framework not found")
    db.delete(fw)
    db.commit()
    log_action(db, current.id, "DELETE", "framework", framework_id)
