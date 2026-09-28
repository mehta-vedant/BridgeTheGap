# ruff: noqa: I001 - domain imports are grouped for readability.
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .mvp_models import (
    Asset, ATR, AuditEvent, BridgeProfile, CompanyUserMembership, ContractRecord,
    DefectRecord, GateDefinition, GateEvaluation, InspectionRecord, Milestone,
    OrganisationUnit, PolicyVersion, PriceVariationClaim, ProjectRecord,
    RoleDefinition, ServiceStateRequest, TenderBidRecord, TenderRecord, TestEvaluation,
    TestSample, QualityTest, UserRoleAssignment, WorkOrderRecord, RectificationSubmission,
    WorkVerification,
)
from .security import get_current_user

router = APIRouter(prefix="/api/mvp", tags=["Lifecycle MVP"])

ROLE_FALLBACKS = {
    "MANAGER": "STATE_ADMIN", "EXECUTIVE_ENGINEER": "EXECUTIVE_ENGINEER",
    "INSPECTOR": "INSPECTOR", "CONTRACTOR": "CONTRACTOR",
    "CHIEF_ENGINEER": "STATE_ADMIN", "SUPERINTENDING_ENGINEER": "SUPERINTENDING_ENGINEER",
    "QUALITY_ENGINEER": "QUALITY_ENGINEER", "FINANCE": "FINANCE", "AUDITOR": "AUDITOR",
}


class LandReadinessInput(BaseModel):
    possession_percent: Decimal = Field(ge=0, le=100)
    handover_reference: str | None = Field(default=None, max_length=240)


class BidInput(BaseModel):
    technical_summary: str = Field(min_length=10, max_length=2000)
    price_amount: Decimal = Field(gt=0, max_digits=15, decimal_places=2)


class InspectionInput(BaseModel):
    grade: str = Field(pattern="^(S|SRI|U)$")
    notes: str = Field(min_length=10, max_length=3000)
    risk_level: str = Field(default="NONE", pattern="^(NONE|SAFETY_REVIEW)$")
    atr_months: int = Field(default=3, ge=2, le=12)


class WorkOrderInput(BaseModel):
    decision_type: str = Field(pattern="^(ROUTINE_MAINTENANCE|REPAIR|REHABILITATION|STRENGTHENING|REPLACEMENT)$")
    description: str = Field(min_length=10, max_length=3000)
    company_id: str


class RectificationInput(BaseModel):
    notes: str = Field(min_length=10, max_length=3000)


class ServiceRequestInput(BaseModel):
    requested_state: str = Field(pattern="^(OPEN|RESTRICTED|CLOSED)$")
    reason: str = Field(min_length=10, max_length=1000)


class PVClaimInput(BaseModel):
    submitted_amount: Decimal = Field(gt=0, max_digits=15, decimal_places=2)
    calculated_amount: Decimal = Field(gt=0, max_digits=15, decimal_places=2)


class TestInput(BaseModel):
    test_type: str = Field(min_length=3, max_length=80)
    specified_value: Decimal = Field(gt=0)
    samples: list[Decimal] = Field(min_length=1, max_length=20)


class PassportCreateInput(BaseModel):
    asset_code: str = Field(pattern=r"^[A-Z0-9-]{6,64}$")
    canonical_name: str = Field(min_length=5, max_length=240)
    district: str = Field(min_length=2, max_length=100)
    bridge_class: str = Field(pattern=r"^(MAJOR_BRIDGE|MINOR_BRIDGE|ROB|RUB|CULVERT)$")
    route_name: str = Field(min_length=3, max_length=180)
    chainage_km: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=3)
    length_m: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    span_count: int | None = Field(default=None, ge=1, le=100)
    project_title: str = Field(min_length=5, max_length=240)
    project_type: str = Field(default="NEW_CONSTRUCTION", pattern=r"^(NEW_CONSTRUCTION|REHABILITATION|REPLACEMENT)$")
    estimate_amount: Decimal = Field(gt=0, max_digits=15, decimal_places=2)


def session_dependency():
    with SessionLocal() as session:
        yield session


def uid(prefix: str) -> str:
    return f"{prefix}-{uuid4()}"


def actor_roles(session: Session, user: User) -> set[str]:
    codes = {ROLE_FALLBACKS.get(user.role, user.role)}
    rows = session.execute(
        select(RoleDefinition.code)
        .join(UserRoleAssignment, UserRoleAssignment.role_id == RoleDefinition.id)
        .where(UserRoleAssignment.user_id == user.id, UserRoleAssignment.effective_to.is_(None))
    ).scalars()
    return codes | set(rows)


def require(session: Session, user: User, *roles: str) -> None:
    if not actor_roles(session, user).intersection(roles):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Your assigned role cannot perform this action")


def get_asset(session: Session, asset_id: str) -> Asset:
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Asset not found")
    return asset


def audit(session: Session, actor: User, asset_id: str | None, entity_type: str, entity_id: str, event_type: str, old_value: dict | None = None, new_value: dict | None = None, reason: str | None = None) -> None:
    session.add(AuditEvent(id=uid("AUD"), asset_id=asset_id, entity_type=entity_type, entity_id=entity_id, event_type=event_type, actor_id=actor.id, old_value=old_value, new_value=new_value, reason=reason))


def asset_view(asset: Asset, profile: BridgeProfile | None = None) -> dict:
    return {
        "id": asset.id, "asset_code": asset.asset_code, "name": asset.canonical_name,
        "asset_type": asset.asset_type, "lifecycle_state": asset.lifecycle_state,
        "service_state": asset.service_state, "condition_grade": asset.condition_grade,
        "risk_flag": asset.risk_flag, "district": asset.district,
        "bridge": None if not profile else {"class": profile.bridge_class, "route": profile.route_name, "chainage_km": float(profile.chainage_km) if profile.chainage_km is not None else None, "length_m": float(profile.length_m) if profile.length_m is not None else None, "span_count": profile.span_count},
    }


@router.get("/admin/roles")
def list_role_definitions(user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN")
    return {"items": [{"code": role.code, "name": role.name} for role in session.scalars(select(RoleDefinition).order_by(RoleDefinition.name)).all()]}


@router.get("/dashboard")
def dashboard(user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "SUPERINTENDING_ENGINEER", "INSPECTOR", "CONTRACTOR", "QUALITY_ENGINEER", "FINANCE", "AUDITOR")
    open_defects = session.scalar(select(func.count()).select_from(DefectRecord).where(DefectRecord.status != "CLOSED")) or 0
    failed_gates = session.scalar(select(func.count()).select_from(GateEvaluation).where(GateEvaluation.status == "FAILED")) or 0
    today = datetime.now(UTC).date()
    overdue_atrs = session.scalar(select(func.count()).select_from(ATR).where(ATR.status == "OPEN", ATR.due_on < today)) or 0
    assets = session.scalars(select(Asset).order_by(Asset.asset_code)).all()
    actions = []
    for gate in session.scalars(select(GateEvaluation).where(GateEvaluation.status == "FAILED")).all():
        actions.append({"type": "FAILED_GATE", "id": gate.id, "title": "Tender readiness blocked", "detail": gate.explanation, "asset_id": gate.asset_id})
    for defect in session.scalars(select(DefectRecord).where(DefectRecord.status != "CLOSED")).all():
        actions.append({"type": "OPEN_DEFECT", "id": defect.id, "title": "Open defect requires action", "detail": defect.description, "asset_id": defect.asset_id})
    return {"metrics": {"assets": len(assets), "active_projects": session.scalar(select(func.count()).select_from(ProjectRecord)) or 0, "open_defects": open_defects, "failed_gates": failed_gates, "overdue_atrs": overdue_atrs, "restricted_or_closed": sum(asset.service_state != "OPEN" for asset in assets)}, "actions": actions[:12]}


@router.get("/assets")
def list_assets(q: str | None = None, lifecycle_state: str | None = None, service_state: str | None = None, limit: int = 50, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "SUPERINTENDING_ENGINEER", "INSPECTOR", "CONTRACTOR", "QUALITY_ENGINEER", "FINANCE", "AUDITOR")
    query = select(Asset).order_by(Asset.asset_code).limit(min(limit, 100))
    if lifecycle_state:
        query = query.where(Asset.lifecycle_state == lifecycle_state)
    if service_state:
        query = query.where(Asset.service_state == service_state)
    if q:
        query = query.where((Asset.asset_code.ilike(f"%{q}%")) | (Asset.canonical_name.ilike(f"%{q}%")))
    result = []
    for asset in session.scalars(query).all():
        result.append(asset_view(asset, session.get(BridgeProfile, asset.id)))
    return {"items": result, "limit": min(limit, 100)}


@router.post("/assets", status_code=status.HTTP_201_CREATED)
def create_bridge_passport(payload: PassportCreateInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    """Create the permanent bridge identity and its initiating project atomically."""
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER")
    if session.scalar(select(Asset.id).where(Asset.asset_code == payload.asset_code)):
        raise HTTPException(status.HTTP_409_CONFLICT, "An asset with this code already exists")
    assignment = session.scalar(select(UserRoleAssignment).where(UserRoleAssignment.user_id == user.id, UserRoleAssignment.organisation_unit_id.is_not(None), UserRoleAssignment.effective_to.is_(None)))
    owner_unit_id = assignment.organisation_unit_id if assignment else session.scalar(select(OrganisationUnit.id).where(OrganisationUnit.kind == "DIVISION").limit(1))
    if not owner_unit_id:
        raise HTTPException(status.HTTP_409_CONFLICT, "No owning division is configured for this user")
    asset = Asset(id=uid("ASSET"), asset_code=payload.asset_code, asset_type="BRIDGE", canonical_name=payload.canonical_name, owner_unit_id=owner_unit_id, lifecycle_state="SANCTION_AND_CLEARANCE", service_state="OPEN", condition_grade=None, risk_flag=None, district=payload.district)
    profile = BridgeProfile(asset_id=asset.id, bridge_class=payload.bridge_class, route_name=payload.route_name, chainage_km=payload.chainage_km, length_m=payload.length_m, span_count=payload.span_count)
    project = ProjectRecord(id=uid("PROJ"), asset_id=asset.id, owner_unit_id=owner_unit_id, project_type=payload.project_type, title=payload.project_title, state="SANCTION_AND_CLEARANCE", estimate_amount=payload.estimate_amount, created_by_id=user.id)
    tender = TenderRecord(id=uid("TEN"), project_id=project.id, tender_number=f"DRAFT-{payload.asset_code[-12:]}", status="DRAFT", estimated_cost=payload.estimate_amount, invited_by_id=user.id)
    session.add_all([asset, profile, project, tender])
    audit(session, user, asset.id, "ASSET", asset.id, "ASSET_PASSPORT_CREATED", new_value={"asset_code": asset.asset_code, "project_id": project.id, "lifecycle_state": asset.lifecycle_state}, reason="Executive Engineer initiated permanent bridge identity and sanction-stage project.")
    session.commit()
    return {"asset": asset_view(asset, profile), "project_id": project.id, "tender_id": tender.id, "next_action": "Record clearance evidence and evaluate the land-readiness gate before tender publication."}


@router.get("/assets/{asset_id}/passport")
def asset_passport(asset_id: str, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "SUPERINTENDING_ENGINEER", "INSPECTOR", "CONTRACTOR", "QUALITY_ENGINEER", "FINANCE", "AUDITOR")
    asset = get_asset(session, asset_id)
    project = session.scalar(select(ProjectRecord).where(ProjectRecord.asset_id == asset.id))
    tender = session.scalar(select(TenderRecord).where(TenderRecord.project_id == project.id)) if project else None
    contract = session.scalar(select(ContractRecord).where(ContractRecord.project_id == project.id)) if project else None
    defects = session.scalars(select(DefectRecord).where(DefectRecord.asset_id == asset.id).order_by(DefectRecord.status)).all()
    work_orders = []
    for defect in defects:
        work_orders.extend(session.scalars(select(WorkOrderRecord).where(WorkOrderRecord.defect_id == defect.id)).all())
    gates = session.scalars(select(GateEvaluation).where(GateEvaluation.asset_id == asset.id).order_by(GateEvaluation.evaluated_at.desc())).all()
    events = session.scalars(select(AuditEvent).where(AuditEvent.asset_id == asset.id).order_by(AuditEvent.created_at.desc()).limit(40)).all()
    return {"asset": asset_view(asset, session.get(BridgeProfile, asset.id)), "project": None if not project else {"id": project.id, "title": project.title, "state": project.state, "type": project.project_type, "estimate_amount": float(project.estimate_amount) if project.estimate_amount else None}, "tender": None if not tender else {"id": tender.id, "number": tender.tender_number, "status": tender.status}, "contract": None if not contract else {"id": contract.id, "number": contract.contract_number, "state": contract.state, "awarded_amount": float(contract.awarded_amount)}, "gates": [{"id": gate.id, "status": gate.status, "explanation": gate.explanation, "missing_requirements": gate.missing_requirements} for gate in gates], "defects": [{"id": defect.id, "description": defect.description, "risk_level": defect.risk_level, "status": defect.status, "due_on": defect.due_on} for defect in defects], "work_orders": [{"id": work.id, "defect_id": work.defect_id, "status": work.status, "description": work.description, "company_id": work.company_id} for work in work_orders], "timeline": [{"id": event.id, "at": event.created_at.isoformat(), "event_type": event.event_type, "reason": event.reason, "new_value": event.new_value} for event in events]}


@router.post("/projects/{project_id}/land-readiness")
def evaluate_land_readiness(project_id: str, payload: LandReadinessInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER")
    project = session.get(ProjectRecord, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    gate = session.scalar(select(GateDefinition).where(GateDefinition.code == "LAND_READINESS"))
    policy = session.get(PolicyVersion, gate.policy_version_id) if gate else None
    required = Decimal(str((policy.expression if policy else {}).get("minimum_possession_percent", 90)))
    passed = payload.possession_percent >= required and bool(payload.handover_reference)
    missing = []
    if payload.possession_percent < required:
        missing.append(f"Possession is {payload.possession_percent}%; configured demonstration threshold is {required}%.")
    if not payload.handover_reference:
        missing.append("Handover memorandum reference is required.")
    evaluation = GateEvaluation(id=uid("GATE"), gate_id=gate.id, project_id=project.id, asset_id=project.asset_id, status="PASSED" if passed else "FAILED", explanation="Land readiness gate passed." if passed else "Tender progression blocked by the configured land-readiness demonstration policy.", missing_requirements=missing, evaluated_by_id=user.id)
    session.add(evaluation)
    audit(session, user, project.asset_id, "GATE_EVALUATION", evaluation.id, "GATE_PASSED" if passed else "GATE_FAILED", new_value={"possession_percent": float(payload.possession_percent), "handover_reference": payload.handover_reference}, reason=evaluation.explanation)
    session.commit()
    return {"id": evaluation.id, "status": evaluation.status, "required_percent": float(required), "current_percent": float(payload.possession_percent), "missing_requirements": missing}


@router.post("/tenders/{tender_id}/publish")
def publish_tender(tender_id: str, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER")
    tender = session.get(TenderRecord, tender_id)
    if not tender:
        raise HTTPException(404, "Tender not found")
    project = session.get(ProjectRecord, tender.project_id)
    evaluation = session.scalar(select(GateEvaluation).where(GateEvaluation.project_id == project.id).order_by(GateEvaluation.evaluated_at.desc()))
    if not evaluation or evaluation.status != "PASSED":
        raise HTTPException(status.HTTP_409_CONFLICT, {"message": "Tender publication is blocked by the land-readiness gate.", "gate": None if not evaluation else {"status": evaluation.status, "missing": evaluation.missing_requirements}})
    tender.status = "PUBLISHED"
    project.state = "TENDERED"
    asset = get_asset(session, project.asset_id)
    asset.lifecycle_state = "TENDERED"
    audit(session, user, asset.id, "TENDER", tender.id, "TENDER_PUBLISHED", new_value={"status": tender.status})
    session.commit()
    return {"id": tender.id, "status": tender.status}


@router.post("/tenders/{tender_id}/bids", status_code=status.HTTP_201_CREATED)
def submit_bid(tender_id: str, payload: BidInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "CONTRACTOR")
    tender = session.get(TenderRecord, tender_id)
    if not tender or tender.status != "PUBLISHED":
        raise HTTPException(status.HTTP_409_CONFLICT, "Tender is not open for submissions")
    membership = session.scalar(select(CompanyUserMembership).where(CompanyUserMembership.user_id == user.id, CompanyUserMembership.active.is_(True)))
    if not membership:
        raise HTTPException(403, "No active contractor-company membership")
    bid = TenderBidRecord(id=uid("BID"), tender_id=tender.id, company_id=membership.company_id, technical_status="SUBMITTED", price_amount=payload.price_amount, submitted_by_id=user.id)
    session.add(bid)
    session.commit()
    return {"id": bid.id, "technical_status": bid.technical_status, "price_amount": float(bid.price_amount)}


@router.post("/tenders/{tender_id}/award")
def award_tender(tender_id: str, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "SUPERINTENDING_ENGINEER")
    tender = session.get(TenderRecord, tender_id)
    if not tender:
        raise HTTPException(404, "Tender not found")
    winner = session.scalar(select(TenderBidRecord).where(TenderBidRecord.tender_id == tender.id).order_by(TenderBidRecord.price_amount).limit(1))
    if not winner:
        raise HTTPException(409, "At least one controlled tender-room bid is required")
    contract = session.scalar(select(ContractRecord).where(ContractRecord.tender_id == tender.id))
    if contract:
        return {"id": contract.id, "state": contract.state, "company_id": contract.company_id}
    project = session.get(ProjectRecord, tender.project_id)
    contract = ContractRecord(id=uid("CON"), project_id=project.id, tender_id=tender.id, company_id=winner.company_id, contract_number=f"SYN-CON-{tender.tender_number[-4:]}", awarded_amount=winner.price_amount, state="AWARDED")
    tender.status, project.state = "AWARDED", "AWARDED"
    asset = get_asset(session, project.asset_id)
    asset.lifecycle_state = "AWARDED"
    session.add_all([contract, Milestone(id=uid("MS"), contract_id=contract.id, name="Mobilisation and quality plan", planned_percent=35, actual_percent=0)])
    audit(session, user, asset.id, "CONTRACT", contract.id, "CONTRACT_AWARDED", new_value={"company_id": winner.company_id, "amount": float(winner.price_amount)})
    session.commit()
    return {"id": contract.id, "state": contract.state, "company_id": contract.company_id, "awarded_amount": float(contract.awarded_amount)}


@router.post("/contracts/{contract_id}/quality-tests", status_code=status.HTTP_201_CREATED)
def submit_quality_test(contract_id: str, payload: TestInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "QUALITY_ENGINEER", "EXECUTIVE_ENGINEER")
    contract = session.get(ContractRecord, contract_id)
    if not contract:
        raise HTTPException(404, "Contract not found")
    policy = session.scalar(select(PolicyVersion).where(PolicyVersion.policy_code == "LAND_READINESS"))
    test = QualityTest(id=uid("TEST"), contract_id=contract.id, test_type=payload.test_type, specified_value=payload.specified_value, rule_policy_version_id=policy.id, status="SUBMITTED")
    session.add(test)
    session.flush()
    for number, value in enumerate(payload.samples, start=1):
        session.add(TestSample(id=uid("SAMPLE"), test_id=test.id, sample_number=number, measured_value=value, recorded_by_id=user.id))
    mean = sum(payload.samples) / len(payload.samples)
    calculated = "PASS" if all(sample >= payload.specified_value for sample in payload.samples) else "FAIL"
    evaluation = TestEvaluation(id=uid("EVAL"), test_id=test.id, calculated_status=calculated, calculation={"mean": float(mean), "minimum": float(min(payload.samples)), "specified_value": float(payload.specified_value), "method": "Synthetic threshold demonstration; not a Gujarat R&B acceptance rule."})
    session.add(evaluation)
    project = session.get(ProjectRecord, contract.project_id)
    audit(session, user, project.asset_id, "QUALITY_TEST", test.id, "QUALITY_TEST_EVALUATED", new_value={"calculated_status": calculated}, reason="Raw measurements evaluated by policy-backed demonstrator.")
    session.commit()
    return {"test_id": test.id, "calculated_status": calculated, "calculation": evaluation.calculation}


@router.post("/assets/{asset_id}/inspections", status_code=status.HTTP_201_CREATED)
def submit_inspection(asset_id: str, payload: InspectionInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "INSPECTOR", "EXECUTIVE_ENGINEER")
    asset = get_asset(session, asset_id)
    inspection = InspectionRecord(id=uid("INSP"), asset_id=asset.id, inspection_type="ROUTINE", grade=payload.grade, submitted_by_id=user.id, notes=payload.notes)
    session.add(inspection)
    response: dict = {"inspection_id": inspection.id, "grade": payload.grade}
    if payload.grade in {"SRI", "U"}:
        due_on = datetime.now(UTC).date() + timedelta(days=30 * payload.atr_months)
        defect = DefectRecord(id=uid("DEF"), asset_id=asset.id, inspection_id=inspection.id, description=payload.notes, risk_level=payload.risk_level, status="OPEN", owner_user_id=None, due_on=due_on)
        atr = ATR(id=uid("ATR"), defect_id=defect.id, due_on=defect.due_on, status="OPEN")
        session.add_all([defect, atr])
        response.update({"defect_id": defect.id, "atr_id": atr.id, "atr_due_on": atr.due_on})
        if payload.risk_level == "SAFETY_REVIEW":
            asset.risk_flag = "SAFETY_REVIEW"
    asset.condition_grade = payload.grade
    audit(session, user, asset.id, "INSPECTION", inspection.id, "INSPECTION_SUBMITTED", new_value={"grade": payload.grade, "risk_level": payload.risk_level}, reason=payload.notes)
    session.commit()
    return response


@router.post("/defects/{defect_id}/work-orders", status_code=status.HTTP_201_CREATED)
def create_work_order(defect_id: str, payload: WorkOrderInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER")
    defect = session.get(DefectRecord, defect_id)
    if not defect or defect.status == "CLOSED":
        raise HTTPException(409, "An open defect is required")
    work = WorkOrderRecord(id=uid("WO"), defect_id=defect.id, company_id=payload.company_id, status="APPROVED", decision_type=payload.decision_type, description=payload.description, approved_by_id=user.id)
    defect.status = "IN_WORK"
    session.add(work)
    audit(session, user, defect.asset_id, "WORK_ORDER", work.id, "WORK_ORDER_APPROVED", new_value={"decision_type": work.decision_type}, reason=work.description)
    session.commit()
    return {"id": work.id, "status": work.status, "defect_id": work.defect_id}


@router.post("/work-orders/{work_order_id}/rectification")
def submit_rectification(work_order_id: str, payload: RectificationInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "CONTRACTOR")
    work = session.get(WorkOrderRecord, work_order_id)
    membership = session.scalar(select(CompanyUserMembership).where(CompanyUserMembership.user_id == user.id, CompanyUserMembership.active.is_(True)))
    if not work or not membership or work.company_id != membership.company_id:
        raise HTTPException(403, "Contractors may submit rectification only for assigned work")
    if work.status not in {"APPROVED", "IN_PROGRESS"}:
        raise HTTPException(409, "Work cannot be rectified in its current state")
    work.status = "VERIFICATION_PENDING"
    submission = RectificationSubmission(id=uid("RECT"), work_order_id=work.id, submitted_by_id=user.id, notes=payload.notes)
    session.add(submission)
    defect = session.get(DefectRecord, work.defect_id)
    audit(session, user, defect.asset_id, "WORK_ORDER", work.id, "RECTIFICATION_SUBMITTED", new_value={"status": work.status}, reason=payload.notes)
    session.commit()
    return {"id": submission.id, "work_order_status": work.status}


@router.post("/work-orders/{work_order_id}/verify")
def verify_work(work_order_id: str, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "INSPECTOR", "EXECUTIVE_ENGINEER")
    work = session.get(WorkOrderRecord, work_order_id)
    rectification = session.scalar(select(RectificationSubmission).where(RectificationSubmission.work_order_id == work_order_id))
    if not work or work.status != "VERIFICATION_PENDING" or not rectification:
        raise HTTPException(409, "A submitted rectification is required before independent verification")
    if rectification.submitted_by_id == user.id:
        raise HTTPException(403, "The rectification submitter cannot independently verify closure")
    work.status = "VERIFIED"
    defect = session.get(DefectRecord, work.defect_id)
    defect.status = "CLOSED"
    session.add(WorkVerification(id=uid("VERIFY"), work_order_id=work.id, verifier_id=user.id, decision="VERIFIED"))
    audit(session, user, defect.asset_id, "WORK_ORDER", work.id, "WORK_VERIFIED", new_value={"status": "VERIFIED"}, reason="Independent maker-checker closure.")
    session.commit()
    return {"id": work.id, "status": work.status, "defect_status": defect.status}


@router.post("/assets/{asset_id}/service-state-requests", status_code=status.HTTP_201_CREATED)
def request_service_state(asset_id: str, payload: ServiceRequestInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "INSPECTOR", "EXECUTIVE_ENGINEER")
    asset = get_asset(session, asset_id)
    request = ServiceStateRequest(id=uid("SERVICE"), asset_id=asset.id, requested_state=payload.requested_state, reason=payload.reason, requested_by_id=user.id)
    session.add(request)
    audit(session, user, asset.id, "SERVICE_STATE_REQUEST", request.id, "SERVICE_STATE_REQUESTED", old_value={"service_state": asset.service_state}, new_value={"requested_state": request.requested_state}, reason=payload.reason)
    session.commit()
    return {"id": request.id, "status": request.status, "requested_state": request.requested_state}


@router.post("/service-state-requests/{request_id}/approve")
def approve_service_state(request_id: str, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "SUPERINTENDING_ENGINEER")
    request = session.get(ServiceStateRequest, request_id)
    if not request or request.status != "PENDING":
        raise HTTPException(409, "A pending service-state request is required")
    asset = get_asset(session, request.asset_id)
    if request.requested_state == "OPEN":
        unresolved = session.scalar(select(func.count()).select_from(DefectRecord).where(DefectRecord.asset_id == asset.id, DefectRecord.status != "CLOSED")) or 0
        if unresolved:
            raise HTTPException(status.HTTP_409_CONFLICT, {"message": "Reopening is blocked by unresolved defects.", "open_defects": unresolved})
    old = asset.service_state
    asset.service_state = request.requested_state
    request.status, request.approved_by_id = "APPROVED", user.id
    audit(session, user, asset.id, "ASSET", asset.id, "SERVICE_STATE_CHANGED", old_value={"service_state": old}, new_value={"service_state": asset.service_state}, reason=request.reason)
    session.commit()
    return {"asset_id": asset.id, "service_state": asset.service_state}


@router.post("/contracts/{contract_id}/price-variation", status_code=status.HTTP_201_CREATED)
def validate_price_variation(contract_id: str, payload: PVClaimInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "FINANCE")
    contract = session.get(ContractRecord, contract_id)
    if not contract:
        raise HTTPException(404, "Contract not found")
    policy = session.scalar(select(PolicyVersion).where(PolicyVersion.policy_code == "PRICE_VARIATION", PolicyVersion.active.is_(True)))
    variance = payload.submitted_amount - payload.calculated_amount
    status_value = "VALIDATED" if abs(variance) <= Decimal("1.00") else "VARIANCE_REQUIRES_REVIEW"
    explanation = "Submitted amount matches the policy calculation." if status_value == "VALIDATED" else "Submitted and calculated values differ; the claim is preserved and routed for finance review."
    claim = PriceVariationClaim(id=uid("PV"), contract_id=contract.id, submitted_amount=payload.submitted_amount, calculated_amount=payload.calculated_amount, variance_amount=variance, status=status_value, policy_version_id=policy.id, explanation=explanation)
    session.add(claim)
    project = session.get(ProjectRecord, contract.project_id)
    audit(session, user, project.asset_id, "PRICE_VARIATION_CLAIM", claim.id, "PRICE_VARIATION_VALIDATED", new_value={"submitted": float(payload.submitted_amount), "calculated": float(payload.calculated_amount), "variance": float(variance), "status": status_value}, reason=explanation)
    session.commit()
    return {"id": claim.id, "status": claim.status, "submitted_amount": float(claim.submitted_amount), "calculated_amount": float(claim.calculated_amount), "variance_amount": float(claim.variance_amount), "explanation": claim.explanation}
