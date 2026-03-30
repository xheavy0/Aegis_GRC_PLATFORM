from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.framework import Framework
from app.core.security import hash_password
from app.config import settings


def seed_admin(db: Session):
    admin = db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first()
    if not admin:
        db.add(
            User(
                email=settings.FIRST_ADMIN_EMAIL,
                full_name=settings.FIRST_ADMIN_NAME,
                hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
                role=UserRole.ADMIN,
                is_active=True,
            )
        )

    frameworks = [
        {
            "name": "NIST CSF 2.0",
            "legacy_names": ["NIST CSF"],
            "full_name": "NIST Cybersecurity Framework",
            "version": "2.0",
            "description": "Framework for improving critical infrastructure cybersecurity.",
            "total_controls": 108,
        },
        {
            "name": "ISO 27001",
            "legacy_names": [],
            "full_name": "ISO/IEC 27001:2022",
            "version": "2022",
            "description": "Information security management systems standard.",
            "total_controls": 93,
        },
        {
            "name": "SOC 2",
            "legacy_names": [],
            "full_name": "SOC 2 Type II",
            "version": "2017",
            "description": "Service Organization Control 2 - Trust Services Criteria.",
            "total_controls": 64,
        },
        {
            "name": "PCI DSS",
            "legacy_names": [],
            "full_name": "Payment Card Industry Data Security Standard",
            "version": "4.0",
            "description": "Security standard for organizations handling payment cards.",
            "total_controls": 285,
        },
        {
            "name": "GDPR",
            "legacy_names": [],
            "full_name": "General Data Protection Regulation",
            "version": "2018",
            "description": "EU regulation on data protection and privacy.",
            "total_controls": 99,
        },
        {
            "name": "CIS Controls v8",
            "legacy_names": ["CIS Controls"],
            "full_name": "Center for Internet Security Controls v8",
            "version": "8",
            "description": "Prioritized cybersecurity safeguards to reduce common attack paths.",
            "total_controls": 153,
        },
    ]
    for item in frameworks:
        existing = db.query(Framework).filter(
            Framework.name.in_([item["name"], *item["legacy_names"]])
        ).first()
        if existing:
            existing.name = item["name"]
            existing.full_name = item["full_name"]
            existing.version = item["version"]
            existing.description = item["description"]
            existing.total_controls = item["total_controls"]
        else:
            db.add(
                Framework(
                    name=item["name"],
                    full_name=item["full_name"],
                    version=item["version"],
                    description=item["description"],
                    total_controls=item["total_controls"],
                )
            )

    db.commit()
