from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.asset import Asset
from app.core.deps import get_current_user, require_analyst_or_above, log_action
from app.schemas.asset import AssetCreate, AssetUpdate, AssetOut

router = APIRouter()


@router.get("", response_model=List[AssetOut])
def list_assets(
    skip: int = 0, limit: int = 100,
    criticality: Optional[str] = None,
    asset_type: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Asset)
    if criticality:
        q = q.filter(Asset.criticality == criticality)
    if asset_type:
        q = q.filter(Asset.asset_type == asset_type)
    return q.order_by(Asset.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    asset = Asset(**payload.model_dump(), created_by=current.id)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    log_action(db, current.id, "CREATE", "asset", asset.id, f"Created asset: {asset.name}")
    return asset


@router.get("/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.patch("/{asset_id}", response_model=AssetOut)
def update_asset(asset_id: UUID, payload: AssetUpdate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(asset, field, val)
    db.commit()
    db.refresh(asset)
    log_action(db, current.id, "UPDATE", "asset", asset.id)
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(asset_id: UUID, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(asset)
    db.commit()
    log_action(db, current.id, "DELETE", "asset", asset_id)
