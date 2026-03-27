from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.risk import Risk, RiskStatus, RiskLevel
from app.models.control import Control, ControlStatus
from app.models.finding import Finding, FindingSeverity, FindingStatus
from app.models.asset import Asset
from app.models.vendor import Vendor
from app.models.audit import Audit
from app.models.policy import Policy
from app.models.evidence import Evidence
from app.core.deps import get_current_user

router = APIRouter()


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _=Depends(get_current_user)):
    risks_total = db.query(func.count(Risk.id)).scalar()
    risks_open = db.query(func.count(Risk.id)).filter(Risk.status == RiskStatus.OPEN).scalar()
    risks_critical = db.query(func.count(Risk.id)).filter(Risk.level == RiskLevel.CRITICAL).scalar()

    controls_total = db.query(func.count(Control.id)).scalar()
    controls_implemented = db.query(func.count(Control.id)).filter(Control.status == ControlStatus.IMPLEMENTED).scalar()

    findings_total = db.query(func.count(Finding.id)).scalar()
    findings_open = db.query(func.count(Finding.id)).filter(Finding.status == FindingStatus.OPEN).scalar()
    findings_critical = db.query(func.count(Finding.id)).filter(Finding.severity == FindingSeverity.CRITICAL).scalar()

    assets_total = db.query(func.count(Asset.id)).scalar()
    vendors_total = db.query(func.count(Vendor.id)).scalar()
    audits_total = db.query(func.count(Audit.id)).scalar()
    policies_total = db.query(func.count(Policy.id)).scalar()
    evidence_total = db.query(func.count(Evidence.id)).scalar()

    compliance_score = 0
    if controls_total > 0:
        compliance_score = round((controls_implemented / controls_total) * 100, 1)

    return {
        "risks": {
            "total": risks_total,
            "open": risks_open,
            "critical": risks_critical,
        },
        "controls": {
            "total": controls_total,
            "implemented": controls_implemented,
            "compliance_score": compliance_score,
        },
        "findings": {
            "total": findings_total,
            "open": findings_open,
            "critical": findings_critical,
        },
        "assets": {"total": assets_total},
        "vendors": {"total": vendors_total},
        "audits": {"total": audits_total},
        "policies": {"total": policies_total},
        "evidence": {"total": evidence_total},
    }
