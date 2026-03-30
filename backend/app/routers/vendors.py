from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.vendor import Vendor
from app.core.deps import get_current_user, require_analyst_or_above, log_action
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorOut

router = APIRouter()


@router.get("", response_model=List[VendorOut])
def list_vendors(
    skip: int = 0, limit: int = 100,
    risk_level: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Vendor)
    if risk_level:
        q = q.filter(Vendor.risk_level == risk_level)
    if status:
        q = q.filter(Vendor.status == status)
    return q.order_by(Vendor.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=VendorOut, status_code=status.HTTP_201_CREATED)
def create_vendor(payload: VendorCreate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    vendor = Vendor(**payload.model_dump(), created_by=current.id)
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    log_action(db, current.id, "CREATE", "vendor", vendor.id, f"Created vendor: {vendor.name}")
    return vendor


@router.get("/{vendor_id}", response_model=VendorOut)
def get_vendor(vendor_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.patch("/{vendor_id}", response_model=VendorOut)
def update_vendor(vendor_id: UUID, payload: VendorUpdate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(vendor, field, val)
    db.commit()
    db.refresh(vendor)
    log_action(db, current.id, "UPDATE", "vendor", vendor.id)
    return vendor


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(vendor_id: UUID, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    db.delete(vendor)
    db.commit()
    log_action(db, current.id, "DELETE", "vendor", vendor_id)
