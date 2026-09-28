import os
from contextlib import asynccontextmanager
from decimal import Decimal
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import SessionLocal
from .errors import DomainError, domain_error_handler
from .models import Bid, Bridge, LifecycleEvent, Project, Tender, User, WorkOrder
from .mvp_api import router as mvp_router
from .mvp_seed import seed_mvp_demo
from .security import create_access_token, get_current_user, require_roles, verify_password
from .seed import seed_demo_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    with SessionLocal() as session:
        seed_demo_data(session)
        seed_mvp_demo(session)
    yield


app = FastAPI(title="R&B Bridge Lifecycle API", version="0.4.0", lifespan=lifespan)

# Structured refusals. A DomainError carries a machine code, an explanation,
# remediation steps and the section of the research record that justifies the
# rule, and the client renders all four. Registered here rather than in the
# router so that every route inherits it, including ones added later.
app.add_exception_handler(DomainError, domain_error_handler)


def _cors_origins() -> list[str]:
    """Origins allowed to call this API from a browser.

    `CORS_ORIGINS` is a comma-separated list. It must be set on any deployed
    instance, because a hardcoded allowlist silently breaks the frontend the
    moment the deployment hostname changes.
    """
    configured = os.getenv("CORS_ORIGINS", "").strip()
    origins = [item.strip() for item in configured.split(",") if item.strip()]
    return origins or [
        "http://localhost:3000",
        "https://bridge-the-gap-dusky.vercel.app",
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(mvp_router)


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class ProjectCreate(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    division: str = Field(min_length=2, max_length=100)
    estimate: Decimal = Field(gt=0, max_digits=15, decimal_places=2)


class BidCreate(BaseModel):
    contractor: str = Field(min_length=2, max_length=160)
    amount: Decimal = Field(gt=0, max_digits=15, decimal_places=2)


class WorkCreate(BaseModel):
    description: str = Field(min_length=5, max_length=2000)
    contractor: str = Field(min_length=2, max_length=160)


def get_session():
    with SessionLocal() as session:
        yield session


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8].upper()}"


def not_found() -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")


def user_data(user: User) -> dict:
    return {"id": user.id, "email": user.email, "name": user.name, "role": user.role, "contractor_name": user.contractor_name}


def project_data(item: Project) -> dict:
    return {"id": item.id, "name": item.name, "division": item.division, "estimate": float(item.estimate), "status": item.status}


def bridge_data(item: Bridge) -> dict:
    return {"id": item.id, "name": item.name, "code": item.code, "service_status": item.service_status, "maintenance_status": item.maintenance_status, "next_inspection": item.next_inspection}


def work_data(item: WorkOrder) -> dict:
    return {"id": item.id, "bridge_id": item.bridge_id, "description": item.description, "contractor": item.contractor, "status": item.status}


def record_event(session: Session, bridge_id: str, actor: str, message: str) -> LifecycleEvent:
    event = LifecycleEvent(id=new_id("EVT"), bridge_id=bridge_id, actor=actor, message=message)
    session.add(event)
    return event


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "bridge-lifecycle-api"}


@app.post("/api/auth/login")
def login(payload: LoginRequest, session: Session = Depends(get_session)) -> dict:
    user = session.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    return {"access_token": create_access_token(user), "token_type": "bearer", "user": user_data(user)}


@app.get("/api/auth/me")
def me(user: User = Depends(get_current_user)) -> dict:
    return user_data(user)


@app.get("/api/dashboard/summary")
def dashboard_summary(_: User = Depends(get_current_user), session: Session = Depends(get_session)) -> dict:
    return {
        "projects": session.scalar(select(func.count()).select_from(Project)) or 0,
        "bridges": session.scalar(select(func.count()).select_from(Bridge)) or 0,
        "attention_required": session.scalar(select(func.count()).select_from(Bridge).where(Bridge.maintenance_status == "ACTION_REQUIRED")) or 0,
        "active_work_orders": session.scalar(select(func.count()).select_from(WorkOrder).where(WorkOrder.status != "VERIFIED")) or 0,
    }


@app.get("/api/projects")
def list_projects(_: User = Depends(get_current_user), session: Session = Depends(get_session)) -> list[dict]:
    return [project_data(item) for item in session.scalars(select(Project).order_by(Project.id)).all()]


@app.post("/api/projects", status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, _: User = Depends(require_roles("MANAGER", "EXECUTIVE_ENGINEER")), session: Session = Depends(get_session)) -> dict:
    project = Project(id=new_id("PRJ"), **payload.model_dump(), status="NEED_IDENTIFIED")
    session.add(project)
    session.commit()
    return project_data(project)


@app.post("/api/projects/{project_id}/approvals")
def approve_project(project_id: str, _: User = Depends(require_roles("MANAGER", "EXECUTIVE_ENGINEER")), session: Session = Depends(get_session)) -> dict:
    project = session.get(Project, project_id)
    if not project:
        raise not_found()
    if project.status == "TECHNICALLY_SANCTIONED":
        return project_data(project)
    if project.status not in {"NEED_IDENTIFIED", "ADMINISTRATIVELY_APPROVED"}:
        raise HTTPException(status.HTTP_409_CONFLICT, "Project cannot be sanctioned in its current state")
    project.status = "TECHNICALLY_SANCTIONED"
    session.commit()
    return project_data(project)


@app.get("/api/tenders/{tender_id}")
def get_tender(tender_id: str, _: User = Depends(get_current_user), session: Session = Depends(get_session)) -> dict:
    tender = session.get(Tender, tender_id)
    if not tender:
        raise not_found()
    bids = session.scalars(select(Bid).where(Bid.tender_id == tender.id).order_by(Bid.amount)).all()
    return {"id": tender.id, "project_id": tender.project_id, "status": tender.status, "contract_id": tender.contract_id, "bids": [{"id": bid.id, "contractor": bid.contractor, "amount": float(bid.amount)} for bid in bids]}


@app.post("/api/tenders/{tender_id}/bids", status_code=status.HTTP_201_CREATED)
def submit_bid(tender_id: str, payload: BidCreate, user: User = Depends(require_roles("CONTRACTOR")), session: Session = Depends(get_session)) -> dict:
    tender = session.get(Tender, tender_id)
    if not tender:
        raise not_found()
    if tender.status != "OPEN":
        raise HTTPException(status.HTTP_409_CONFLICT, "Tender is not open")
    if user.contractor_name and payload.contractor != user.contractor_name:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Contractors can submit bids only for their own organisation")
    bid = Bid(id=new_id("BID"), tender_id=tender.id, **payload.model_dump())
    session.add(bid)
    session.commit()
    return {"id": bid.id, "contractor": bid.contractor, "amount": float(bid.amount)}


@app.post("/api/tenders/{tender_id}/award")
def award_tender(tender_id: str, user: User = Depends(require_roles("MANAGER", "EXECUTIVE_ENGINEER")), session: Session = Depends(get_session)) -> dict:
    tender = session.get(Tender, tender_id)
    if not tender:
        raise not_found()
    if tender.status == "AWARDED":
        return get_tender(tender_id, user, session)
    if tender.status != "OPEN":
        raise HTTPException(status.HTTP_409_CONFLICT, "Tender cannot be awarded in its current state")
    winner = session.scalar(select(Bid).where(Bid.tender_id == tender.id).order_by(Bid.amount).limit(1))
    if not winner:
        raise HTTPException(status.HTTP_409_CONFLICT, "At least one bid is required before award")
    tender.status = "AWARDED"
    tender.contract_id = new_id("CON")
    project = session.get(Project, tender.project_id)
    if project:
        project.status = "AWARDED"
    session.commit()
    return get_tender(tender_id, user, session)


@app.get("/api/bridges")
def list_bridges(_: User = Depends(get_current_user), session: Session = Depends(get_session)) -> list[dict]:
    return [bridge_data(item) for item in session.scalars(select(Bridge).order_by(Bridge.code)).all()]


@app.get("/api/bridges/{bridge_id}/timeline")
def timeline(bridge_id: str, _: User = Depends(get_current_user), session: Session = Depends(get_session)) -> list[dict]:
    if not session.get(Bridge, bridge_id):
        raise not_found()
    events = session.scalars(select(LifecycleEvent).where(LifecycleEvent.bridge_id == bridge_id).order_by(LifecycleEvent.created_at)).all()
    return [{"id": event.id, "bridge_id": event.bridge_id, "at": event.created_at.date().isoformat(), "actor": event.actor, "message": event.message} for event in events]


@app.get("/api/bridges/{bridge_id}/work-orders")
def list_work_orders(bridge_id: str, _: User = Depends(get_current_user), session: Session = Depends(get_session)) -> list[dict]:
    if not session.get(Bridge, bridge_id):
        raise not_found()
    return [work_data(item) for item in session.scalars(select(WorkOrder).where(WorkOrder.bridge_id == bridge_id).order_by(WorkOrder.id)).all()]


@app.post("/api/bridges/{bridge_id}/inspections")
def submit_inspection(bridge_id: str, requires_disposition: bool = True, user: User = Depends(require_roles("INSPECTOR")), session: Session = Depends(get_session)) -> dict:
    bridge = session.get(Bridge, bridge_id)
    if not bridge:
        raise not_found()
    bridge.maintenance_status = "ACTION_REQUIRED" if requires_disposition else "NONE"
    event = record_event(session, bridge_id, user.name, "Inspection submitted; engineering disposition required." if requires_disposition else "Inspection submitted with no action required.")
    session.commit()
    return {"bridge": bridge_data(bridge), "event": {"id": event.id, "at": event.created_at.date().isoformat(), "actor": event.actor, "message": event.message}}


@app.post("/api/bridges/{bridge_id}/work-orders", status_code=status.HTTP_201_CREATED)
def create_work_order(bridge_id: str, payload: WorkCreate, user: User = Depends(require_roles("MANAGER", "EXECUTIVE_ENGINEER")), session: Session = Depends(get_session)) -> dict:
    bridge = session.get(Bridge, bridge_id)
    if not bridge:
        raise not_found()
    if bridge.maintenance_status != "ACTION_REQUIRED":
        raise HTTPException(status.HTTP_409_CONFLICT, "No disposition-required finding")
    work = WorkOrder(id=new_id("WO"), bridge_id=bridge_id, **payload.model_dump(), status="APPROVED")
    bridge.maintenance_status = "WORK_APPROVED"
    session.add(work)
    record_event(session, bridge_id, user.name, f"Work order {work.id} approved.")
    session.commit()
    return work_data(work)


@app.post("/api/work-orders/{work_id}/complete")
def complete_work(work_id: str, user: User = Depends(require_roles("CONTRACTOR")), session: Session = Depends(get_session)) -> dict:
    work = session.get(WorkOrder, work_id)
    if not work:
        raise not_found()
    if user.contractor_name != work.contractor:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Contractors can complete only their assigned work")
    if work.status == "VERIFIED":
        raise HTTPException(status.HTTP_409_CONFLICT, "Verified work cannot be completed again")
    if work.status == "VERIFICATION_PENDING":
        return work_data(work)
    work.status = "VERIFICATION_PENDING"
    session.commit()
    return work_data(work)


@app.post("/api/work-orders/{work_id}/verify")
def verify_work(work_id: str, user: User = Depends(require_roles("INSPECTOR", "EXECUTIVE_ENGINEER")), session: Session = Depends(get_session)) -> dict:
    work = session.get(WorkOrder, work_id)
    if not work:
        raise not_found()
    if work.status == "VERIFIED":
        return work_data(work)
    if work.status != "VERIFICATION_PENDING":
        raise HTTPException(status.HTTP_409_CONFLICT, "Completion is required before verification")
    work.status = "VERIFIED"
    bridge = session.get(Bridge, work.bridge_id)
    if bridge:
        bridge.maintenance_status = "NONE"
    record_event(session, work.bridge_id, user.name, f"Work order {work_id} independently verified.")
    session.commit()
    return work_data(work)
