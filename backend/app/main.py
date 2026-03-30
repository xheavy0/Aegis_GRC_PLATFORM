from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.routers import auth, users, risks, controls, assets, findings, vendors, audits, policies, evidence, frameworks, reports
from app.routers import risk_matrix
import app.models  # noqa: F401 - registers all models with SQLAlchemy

# Create all tables
Base.metadata.create_all(bind=engine)

# Seed initial data
from app.core.seed import seed_admin
with SessionLocal() as db:
    seed_admin(db)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for uploads
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# API routes
app.include_router(auth.router,       prefix="/api/auth",       tags=["Auth"])
app.include_router(users.router,      prefix="/api/users",      tags=["Users"])
app.include_router(risks.router,      prefix="/api/risks",      tags=["Risks"])
app.include_router(controls.router,   prefix="/api/controls",   tags=["Controls"])
app.include_router(assets.router,     prefix="/api/assets",     tags=["Assets"])
app.include_router(findings.router,   prefix="/api/findings",   tags=["Findings"])
app.include_router(vendors.router,    prefix="/api/vendors",    tags=["Vendors"])
app.include_router(audits.router,     prefix="/api/audits",     tags=["Audits"])
app.include_router(policies.router,   prefix="/api/policies",   tags=["Policies"])
app.include_router(evidence.router,   prefix="/api/evidence",   tags=["Evidence"])
app.include_router(frameworks.router, prefix="/api/frameworks", tags=["Frameworks"])
app.include_router(reports.router,    prefix="/api/reports",    tags=["Reports"])
app.include_router(risk_matrix.router, prefix="/api/risk-matrix", tags=["Risk Matrix"])


@app.get("/api/health")
def health():
    return {"status": "ok", "version": settings.APP_VERSION, "app": settings.APP_NAME}
