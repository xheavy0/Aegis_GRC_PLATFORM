from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.policy import Policy
from app.core.deps import get_current_user, require_analyst_or_above, log_action
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyOut

router = APIRouter()


@router.get("", response_model=List[PolicyOut])
def list_policies(
    skip: int = 0, limit: int = 100,
    status: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(Policy)
    if status:
        q = q.filter(Policy.status == status)
    if category:
        q = q.filter(Policy.category == category)
    return q.order_by(Policy.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=PolicyOut, status_code=status.HTTP_201_CREATED)
def create_policy(payload: PolicyCreate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    policy = Policy(**payload.model_dump(), created_by=current.id)
    db.add(policy)
    db.commit()
    db.refresh(policy)
    log_action(db, current.id, "CREATE", "policy", policy.id, f"Created policy: {policy.title}")
    return policy


@router.get("/{policy_id}", response_model=PolicyOut)
def get_policy(policy_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@router.patch("/{policy_id}", response_model=PolicyOut)
def update_policy(policy_id: UUID, payload: PolicyUpdate, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    for field, val in payload.model_dump(exclude_none=True).items():
        setattr(policy, field, val)
    db.commit()
    db.refresh(policy)
    log_action(db, current.id, "UPDATE", "policy", policy.id)
    return policy


@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_policy(policy_id: UUID, db: Session = Depends(get_db), current=Depends(require_analyst_or_above)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    db.delete(policy)
    db.commit()
    log_action(db, current.id, "DELETE", "policy", policy_id)
