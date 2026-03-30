from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.risk_matrix import RiskMatrixConfig, DEFAULT_LIKELIHOOD_LABELS, DEFAULT_IMPACT_LABELS, DEFAULT_CELL_RATINGS
from app.core.deps import get_current_user, require_admin, log_action
from app.schemas.risk_matrix import RiskMatrixConfigUpdate, RiskMatrixConfigOut

router = APIRouter()


def _get_or_create(db: Session) -> RiskMatrixConfig:
    cfg = db.query(RiskMatrixConfig).first()
    if not cfg:
        cfg = RiskMatrixConfig(
            likelihood_labels=list(DEFAULT_LIKELIHOOD_LABELS),
            impact_labels=list(DEFAULT_IMPACT_LABELS),
            cell_ratings=[row[:] for row in DEFAULT_CELL_RATINGS],
        )
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg


@router.get("", response_model=RiskMatrixConfigOut)
def get_matrix_config(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_or_create(db)


@router.put("", response_model=RiskMatrixConfigOut)
def update_matrix_config(
    payload: RiskMatrixConfigUpdate,
    db: Session = Depends(get_db),
    current=Depends(require_admin),
):
    cfg = _get_or_create(db)
    cfg.likelihood_labels = payload.likelihood_labels
    cfg.impact_labels = payload.impact_labels
    cfg.cell_ratings = payload.cell_ratings
    db.commit()
    db.refresh(cfg)
    log_action(db, current.id, "UPDATE", "risk_matrix_config", cfg.id, "Updated risk matrix configuration")
    return cfg
