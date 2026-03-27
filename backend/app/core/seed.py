from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.framework import Framework
from app.core.security import hash_password
from app.config import settings


def seed_admin(db: Session):
    exists = db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first()
    if exists:
        return

    admin = User(
        email=settings.FIRST_ADMIN_EMAIL,
        full_name=settings.FIRST_ADMIN_NAME,
        hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
        role=UserRole.ADMIN,
        is_active=True,
    )
    db.add(admin)

    frameworks = [
        Framework(name="NIST CSF", full_name="NIST Cybersecurity Framework", version="2.0",
                  description="Framework for improving critical infrastructure cybersecurity.", total_controls=108),
        Framework(name="ISO 27001", full_name="ISO/IEC 27001:2022", version="2022",
                  description="Information security management systems standard.", total_controls=93),
        Framework(name="SOC 2", full_name="SOC 2 Type II", version="2017",
                  description="Service Organization Control 2 - Trust Services Criteria.", total_controls=64),
        Framework(name="PCI DSS", full_name="Payment Card Industry Data Security Standard", version="4.0",
                  description="Security standard for organizations handling payment cards.", total_controls=285),
        Framework(name="GDPR", full_name="General Data Protection Regulation", version="2018",
                  description="EU regulation on data protection and privacy.", total_controls=99),
    ]
    for fw in frameworks:
        if not db.query(Framework).filter(Framework.name == fw.name).first():
            db.add(fw)

    db.commit()
    print(f"[seed] Admin user created: {settings.FIRST_ADMIN_EMAIL}")
