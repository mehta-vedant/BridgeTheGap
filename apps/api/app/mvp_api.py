# ruff: noqa: I001 - domain imports are grouped for readability.
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import rules
from .database import SessionLocal
from .errors import (
    conflict,
    gate_blocked,
    invalid,
    missing,
    not_established,
    not_visible,
    role_denied,
    rule_violation,
    wrong_phase,
)
from .lifecycle import (
    PHASE_BUILD,
    PHASE_LABELS,
    PHASE_POST,
    PHASE_PRE,
    PHASE_PURPOSE,
    contractor_company_ids,
    may_see,
    phase_facts,
    phase_gates,
    scope_asset_query,
    scope_explanation,
)
from .models import User
from .mvp_models import (
    Asset, ATR, AuditEvent, BridgeProfile, CompanyUserMembership, ContractRecord,
    ClearanceRecord, DefectRecord, GateDefinition, GateEvaluation, InspectionRecord, Milestone,
    OrganisationUnit, PolicyVersion, PriceVariationClaim, ProjectRecord, ProjectReport,
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


class PVComponentInput(BaseModel):
    """One claimed component line.

    The caller supplies the measured facts. It does **not** supply the answer:
    there is no ``calculated_amount`` field, because a server that accepts a
    calculated entitlement from the client and stores the difference is a
    difference calculator, not an engine. The arithmetic belongs here.
    """

    component: str = Field(pattern=r"^(LABOUR|CEMENT|STEEL|BITUMEN|FUEL|OTHER_MATERIALS|PLANT_MACHINERY|ASPHALT)$")
    portion: Decimal = Field(gt=0, max_digits=15, decimal_places=2)
    base_index: Decimal = Field(gt=0, max_digits=12, decimal_places=4)
    current_index: Decimal = Field(gt=0, max_digits=12, decimal_places=4)


class PVClaimInput(BaseModel):
    """A price-variation claim, as raw facts. The engine computes the entitlement."""

    components: list[PVComponentInput] = Field(min_length=1, max_length=12)
    months_elapsed: int = Field(ge=0, le=240)
    is_bridge: bool = True
    # Optional: what the claimant asserts they are owed. Used only to report the
    # variance the engine found, never to compute the entitlement.
    claimed_amount: Decimal | None = Field(default=None, ge=0, max_digits=15, decimal_places=2)


class TestInput(BaseModel):
    test_type: str = Field(min_length=3, max_length=80)
    specified_value: Decimal = Field(gt=0)
    samples: list[Decimal] = Field(min_length=1, max_length=20)
    # Optional. When given, the core-extraction fallback is evaluated too, and
    # the record states which criterion governed. A test cannot silently pass on
    # cubes and a test cannot silently fail without checking the cores.
    cores: list[Decimal] | None = Field(default=None, min_length=1, max_length=20)


class PassportCreateInput(BaseModel):
    asset_code: str | None = Field(default=None, pattern=r"^[A-Z0-9-]{6,64}$")
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
    latitude: Decimal | None = Field(default=None, ge=-90, le=90, max_digits=9, decimal_places=6)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180, max_digits=9, decimal_places=6)

    @field_validator("asset_code", mode="before")
    @classmethod
    def blank_asset_code_means_generate(cls, value: object) -> object:
        return None if isinstance(value, str) and not value.strip() else value


class ReportInput(BaseModel):
    report_type: str = Field(pattern="^(PFR|FSR|DPR|AA|TS)$")
    reference: str = Field(min_length=3, max_length=240)
    source_class: str = Field(default="NATIONAL_REFERENCE", pattern="^(GUJARAT_VERIFIED|NATIONAL_REFERENCE|DEMO_CONFIGURABLE|NOT_ESTABLISHED)$")


class ClearanceInput(BaseModel):
    clearance_type: str = Field(pattern="^(GAD|ESP|LAND_USE|FOREST_WILDLIFE|ENVIRONMENTAL)$")
    status: str = Field(pattern="^(PENDING|SUBMITTED|APPROVED|NOT_REQUIRED)$")
    reference: str | None = Field(default=None, max_length=240)
    source_class: str = Field(default="GUJARAT_VERIFIED", pattern="^(GUJARAT_VERIFIED|NATIONAL_REFERENCE|DEMO_CONFIGURABLE|NOT_ESTABLISHED)$")


def session_dependency():
    with SessionLocal() as session:
        yield session


def uid(prefix: str) -> str:
    return f"{prefix}-{uuid4()}"


def bridge_asset_code(district: str) -> str:
    """Generate a readable, collision-resistant demo registry identifier."""
    district_code = "".join(character for character in district.upper() if character.isalnum())[:3] or "GEN"
    return f"BRG-GJ-{district_code}-{datetime.now(UTC).year}-{uuid4().hex[:6].upper()}"


def actor_roles(session: Session, user: User) -> set[str]:
    codes = {ROLE_FALLBACKS.get(user.role, user.role)}
    rows = session.execute(
        select(RoleDefinition.code)
        .join(UserRoleAssignment, UserRoleAssignment.role_id == RoleDefinition.id)
        .where(UserRoleAssignment.user_id == user.id, UserRoleAssignment.effective_to.is_(None))
    ).scalars()
    return codes | set(rows)


def require(session: Session, user: User, *roles: str) -> None:
    """Server-side authorization.

    Raises a structured refusal naming the roles that could have performed the
    action, rather than a bare 403. A "403 Forbidden" tells a demonstrator
    nothing; "this is reserved for the Executive Engineer and the Manager" tells
    them the system has an authority model worth defending.
    """
    if not actor_roles(session, user).intersection(roles):
        raise role_denied(list(roles), f"{rules.RECORD} sec 4A.8 (nine wings, and which wing holds which authority)")


def get_asset(session: Session, asset_id: str) -> Asset:
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Asset not found")
    return asset


def audit(session: Session, actor: User, asset_id: str | None, entity_type: str, entity_id: str, event_type: str, old_value: dict | None = None, new_value: dict | None = None, reason: str | None = None) -> None:
    session.add(AuditEvent(id=uid("AUD"), asset_id=asset_id, entity_type=entity_type, entity_id=entity_id, event_type=event_type, actor_id=actor.id, old_value=old_value, new_value=new_value, reason=reason))


def label_status(value: str | None) -> str:
    return (value or "unknown").replace("_", " ").lower()


def asset_view(asset: Asset, profile: BridgeProfile | None = None, facts=None) -> dict:
    """The canonical asset shape.

    ``phase`` is the derived value from ``app.lifecycle`` and is what callers
    should group, filter and act on. ``lifecycle_state`` is still returned
    because it is the stored column, and it is reported next to the derived
    phase so any disagreement is visible rather than silently resolved. A stored
    label that disagrees with the records behind it is a data-quality finding,
    and hiding it would defeat the point of deriving the phase at all.
    """
    return {
        "id": asset.id, "asset_code": asset.asset_code, "name": asset.canonical_name,
        "asset_type": asset.asset_type, "phase": facts.phase if facts else None,
        "phase_label": PHASE_LABELS[facts.phase] if facts else None,
        "lifecycle_state": asset.lifecycle_state,
        "stored_state_agrees": None if not facts else (asset.lifecycle_state == facts.phase),
        "service_state": asset.service_state, "condition_grade": asset.condition_grade,
        "risk_flag": asset.risk_flag, "district": asset.district,
        "latitude": float(asset.latitude) if asset.latitude is not None else None,
        "longitude": float(asset.longitude) if asset.longitude is not None else None,
        "bridge": None if not profile else {"class": profile.bridge_class, "route": profile.route_name, "chainage_km": float(profile.chainage_km) if profile.chainage_km is not None else None, "length_m": float(profile.length_m) if profile.length_m is not None else None, "span_count": profile.span_count},
    }


def visible_assets(session: Session, user: User, roles: set[str], order_by=None) -> list[Asset]:
    """Assets this caller may see, already restricted in SQL."""
    query = select(Asset)
    if order_by is not None:
        query = query.order_by(order_by)
    return list(session.scalars(scope_asset_query(query, session, user, roles)).all())


def guard_asset(session: Session, user: User, roles: set[str], asset_id: str) -> Asset:
    """Fetch an asset the caller is permitted to see, or explain why not.

    Checking visibility with a 404 instead of a 403 would hide the existence of
    the record from a contractor who has no business knowing it exists, but it
    would also make the refusal undebuggable. A 403 with the rule that produced
    it is the more useful of the two for a system that is being demonstrated and
    defended.
    """
    if not may_see(session, user, roles, asset_id):
        raise not_visible("bridge", f"{rules.RECORD} sec 4A.8 (the nine-wing actor model, and what each wing may see)")
    asset = session.get(Asset, asset_id)
    if not asset:
        raise missing("Asset not found", ["The register holds no bridge with that identifier."])
    return asset


@router.get("/admin/roles")
def list_role_definitions(user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN")
    return {"items": [{"code": role.code, "name": role.name} for role in session.scalars(select(RoleDefinition).order_by(RoleDefinition.name)).all()]}


@router.get("/dashboard")
def dashboard(user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "SUPERINTENDING_ENGINEER", "INSPECTOR", "CONTRACTOR", "QUALITY_ENGINEER", "FINANCE", "AUDITOR")
    roles = actor_roles(session, user)
    assets = visible_assets(session, user, roles, order_by=Asset.asset_code)
    asset_ids = [asset.id for asset in assets]
    facts = phase_facts(session, asset_ids)
    visible_ids = set(asset_ids)

    # Every count below is scoped to what this caller may see. A contractor's
    # dashboard must not reveal the department's total open-defect count by
    # arithmetic accident, and it must not show a district list implying bridges
    # they have no business knowing about.
    def _scoped(model, *conditions) -> int:
        if not visible_ids:
            return 0
        if hasattr(model, "asset_id"):
            column = model.asset_id
            return session.scalar(
                select(func.count()).select_from(model).where(column.in_(visible_ids), *conditions)
            ) or 0
        # ATR hangs off a defect, not an asset, so it needs the join.
        return session.scalar(
            select(func.count())
            .select_from(model)
            .join(DefectRecord, DefectRecord.id == model.defect_id)
            .where(DefectRecord.asset_id.in_(visible_ids), *conditions)
        ) or 0

    open_defects = _scoped(DefectRecord, DefectRecord.status != "CLOSED")
    failed_gates = _scoped(GateEvaluation, GateEvaluation.status == "FAILED")
    today = datetime.now(UTC).date()
    overdue_atrs = _scoped(ATR, ATR.status == "OPEN", ATR.due_on < today)

    project_asset_ids = set(session.scalars(select(ProjectRecord.asset_id).where(ProjectRecord.asset_id.in_(visible_ids) if visible_ids else False)).all()) if visible_ids else set()
    active_projects = sum(1 for pid in project_asset_ids if facts.get(pid) and facts[pid].phase == PHASE_BUILD)

    phases = {PHASE_PRE: 0, PHASE_BUILD: 0, PHASE_POST: 0}
    for asset in assets:
        fact = facts.get(asset.id)
        if fact:
            phases[fact.phase] += 1
    districts = sorted({asset.district for asset in assets if asset.district})

    actions = []
    if visible_ids:
        for gate in session.scalars(select(GateEvaluation).where(GateEvaluation.asset_id.in_(visible_ids), GateEvaluation.status == "FAILED")).all():
            actions.append({"type": "FAILED_GATE", "id": gate.id, "title": "Tender readiness blocked", "detail": gate.explanation, "asset_id": gate.asset_id})
        for defect in session.scalars(select(DefectRecord).where(DefectRecord.asset_id.in_(visible_ids), DefectRecord.status != "CLOSED")).all():
            actions.append({"type": "OPEN_DEFECT", "id": defect.id, "title": "Open defect requires action", "detail": defect.description, "asset_id": defect.asset_id})
        for request in session.scalars(select(ServiceStateRequest).where(ServiceStateRequest.asset_id.in_(visible_ids), ServiceStateRequest.status == "PENDING")).all():
            actions.append({"type": "SERVICE_REQUEST", "id": request.id, "title": "Service state change awaiting approval", "detail": request.reason, "asset_id": request.asset_id})
    actions.sort(key=lambda item: {"FAILED_GATE": 0, "OPEN_DEFECT": 1, "SERVICE_REQUEST": 2}.get(item["type"], 3))
    return {
        "metrics": {
            "assets": len(assets),
            "active_projects": active_projects,
            "open_defects": open_defects,
            "failed_gates": failed_gates,
            "overdue_atrs": overdue_atrs,
            "restricted_or_closed": sum(asset.service_state != "OPEN" for asset in assets),
        },
        "phases": phases,
        "phase_order": [PHASE_PRE, PHASE_BUILD, PHASE_POST],
        "districts": districts,
        "scope": {"roles": sorted(roles), "explanation": scope_explanation(roles), "assets_visible": len(assets)},
        "register": [
            {
                "id": asset.id,
                "asset_code": asset.asset_code,
                "name": asset.canonical_name,
                "phase": facts[asset.id].phase,
                "phase_label": PHASE_LABELS[facts[asset.id].phase],
                "phase_basis": facts[asset.id].basis,
                "service_state": asset.service_state,
                "condition_grade": asset.condition_grade,
                "district": asset.district,
            }
            for asset in assets
            if asset.id in facts
        ],
        "actions": actions[:12],
    }


@router.get("/assets")
def list_assets(
    q: str | None = None,
    phase: str | None = Query(default=None, pattern="^(SANCTION_AND_CLEARANCE|EXECUTION|POST_COMPLETION)$"),
    service_state: str | None = None,
    limit: int = Query(default=500, ge=1, le=2000),
    user: User = Depends(get_current_user),
    session: Session = Depends(session_dependency),
) -> dict:
    """Return the register, restricted to what the caller may see.

    Two guarantees, both of which exist because the register previously made a
    bridge vanish with no explanation:

    1. **Nothing is hidden by a filter the caller cannot see.** Search and
       filters run server-side over the caller's whole scope, and the response
       always reports the true ``total`` and whether the page was truncated. A
       bridge cannot disappear from the register without the caller being able
       to see that it did.

    2. **Nothing outside the caller's scope is returned at all.** Scoping happens
       in SQL, before any row is read, so a contractor's register is not a
       filtered view of the department's register -- it is a query that never
       contained the other rows.

    Phase is the derived value, so ``phase=EXECUTION`` means "a contract has been
    awarded and is not complete", not "a column says so".
    """
    roles = actor_roles(session, user)
    if not roles:
        raise role_denied(["an authenticated role assignment"], f"{rules.RECORD} sec 4A.8")

    scope_rows = visible_assets(session, user, roles, order_by=Asset.asset_code)
    scope_ids = {asset.id for asset in scope_rows}
    scoped_facts = phase_facts(session, [asset.id for asset in scope_rows])
    scope_total = len(scope_rows)

    def matches() -> list[Asset]:
        result = scope_rows
        if phase:
            result = [asset for asset in result if scoped_facts[asset.id].phase == phase]
        if service_state:
            result = [asset for asset in result if asset.service_state == service_state]
        if q:
            needle = q.strip().lower()
            result = [
                asset
                for asset in result
                if needle in (asset.asset_code or "").lower()
                or needle in (asset.canonical_name or "").lower()
                or needle in (asset.district or "").lower()
            ]
        return result

    found = matches()
    page = found[:limit]
    page_facts = phase_facts(session, [asset.id for asset in page])
    profiles = {
        profile.asset_id: profile
        for profile in session.scalars(select(BridgeProfile).where(BridgeProfile.asset_id.in_([asset.id for asset in page] or [""]))).all()
    }
    return {
        "items": [asset_view(asset, profiles.get(asset.id), page_facts[asset.id]) for asset in page],
        "total": len(found),
        "returned": len(page),
        "truncated": len(found) > len(page),
        "register_total": scope_total,
        "department_register_total": session.scalar(select(func.count()).select_from(Asset)) or 0,
        "scope": {
            "roles": sorted(roles),
            "explanation": scope_explanation(roles),
            "assets_visible": scope_total,
            "restricted": scope_total < (session.scalar(select(func.count()).select_from(Asset)) or 0),
        },
        "phases": {
            phase_name: sum(1 for fact in scoped_facts.values() if fact.phase == phase_name)
            for phase_name in (PHASE_PRE, PHASE_BUILD, PHASE_POST)
        },
    }


@router.post("/assets", status_code=status.HTTP_201_CREATED)
def create_bridge_passport(payload: PassportCreateInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    """Create the permanent bridge identity and its initiating project atomically."""
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER")
    asset_code = payload.asset_code or bridge_asset_code(payload.district)
    if session.scalar(select(Asset.id).where(Asset.asset_code == asset_code)):
        raise HTTPException(status.HTTP_409_CONFLICT, "An asset with this code already exists")
    assignment = session.scalar(select(UserRoleAssignment).where(UserRoleAssignment.user_id == user.id, UserRoleAssignment.organisation_unit_id.is_not(None), UserRoleAssignment.effective_to.is_(None)))
    owner_unit_id = assignment.organisation_unit_id if assignment else session.scalar(select(OrganisationUnit.id).where(OrganisationUnit.kind == "DIVISION").limit(1))
    if not owner_unit_id:
        raise HTTPException(status.HTTP_409_CONFLICT, "No owning division is configured for this user")
    asset = Asset(id=uid("ASSET"), asset_code=asset_code, asset_type="BRIDGE", canonical_name=payload.canonical_name, owner_unit_id=owner_unit_id, lifecycle_state="SANCTION_AND_CLEARANCE", service_state="OPEN", condition_grade=None, risk_flag=None, district=payload.district, latitude=payload.latitude, longitude=payload.longitude)
    profile = BridgeProfile(asset_id=asset.id, bridge_class=payload.bridge_class, route_name=payload.route_name, chainage_km=payload.chainage_km, length_m=payload.length_m, span_count=payload.span_count)
    project = ProjectRecord(id=uid("PROJ"), asset_id=asset.id, owner_unit_id=owner_unit_id, project_type=payload.project_type, title=payload.project_title, state="SANCTION_AND_CLEARANCE", estimate_amount=payload.estimate_amount, created_by_id=user.id)
    tender = TenderRecord(id=uid("TEN"), project_id=project.id, tender_number=f"DRAFT-{asset_code[-12:]}", status="DRAFT", estimated_cost=payload.estimate_amount, invited_by_id=user.id)
    session.add_all([asset, profile, project, tender])
    audit(session, user, asset.id, "ASSET", asset.id, "ASSET_PASSPORT_CREATED", new_value={"asset_code": asset.asset_code, "project_id": project.id}, reason="Executive Engineer initiated permanent bridge identity and sanction-stage project.")
    session.commit()
    fact = phase_facts(session, [asset.id])[asset.id]
    return {
        "asset": asset_view(asset, profile, fact),
        "project_id": project.id,
        "tender_id": tender.id,
        "phase": fact.as_dict(),
        "phase_gates": phase_gates(fact),
        "next_action": "Record clearance evidence and evaluate the land-readiness gate before tender publication.",
    }


@router.post("/projects/{project_id}/reports", status_code=status.HTTP_201_CREATED)
def record_project_report(project_id: str, payload: ReportInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "SUPERINTENDING_ENGINEER")
    project = session.get(ProjectRecord, project_id)
    if not project:
        raise missing("Project not found", ["Check the project reference in the passport."])
    existing = session.scalar(select(ProjectReport).where(ProjectReport.project_id == project.id, ProjectReport.report_type == payload.report_type))
    if existing:
        raise conflict(
            f"{payload.report_type} is already recorded for this project.",
            [f"Reference on file: {existing.reference}", "Amend the recorded report rather than adding a second one."],
        )
    report = ProjectReport(id=uid("REPORT"), project_id=project.id, report_type=payload.report_type, status="SUBMITTED", reference=payload.reference, source_class=payload.source_class, prepared_by_id=user.id)
    session.add(report)
    audit(session, user, project.asset_id, "PROJECT_REPORT", report.id, "REPORT_RECORDED", new_value={"report_type": report.report_type, "source_class": report.source_class}, reason=report.reference)
    session.commit()
    return {"id": report.id, "report_type": report.report_type, "status": report.status}


@router.post("/projects/{project_id}/clearances", status_code=status.HTTP_201_CREATED)
def record_clearance(project_id: str, payload: ClearanceInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "SUPERINTENDING_ENGINEER")
    project = session.get(ProjectRecord, project_id)
    if not project:
        raise missing("Project not found", ["Check the project reference in the passport."])
    existing = session.scalar(select(ClearanceRecord).where(ClearanceRecord.project_id == project.id, ClearanceRecord.clearance_type == payload.clearance_type))
    if existing:
        raise conflict(
            f"{payload.clearance_type} clearance is already recorded for this project.",
            [f"Reference on file: {existing.reference}", f"Current status: {existing.status}."],
        )
    clearance = ClearanceRecord(id=uid("CLEAR"), project_id=project.id, clearance_type=payload.clearance_type, status=payload.status, reference=payload.reference, source_class=payload.source_class, recorded_by_id=user.id)
    session.add(clearance)
    audit(session, user, project.asset_id, "CLEARANCE", clearance.id, "CLEARANCE_RECORDED", new_value={"type": clearance.clearance_type, "status": clearance.status}, reason=clearance.reference)
    session.commit()
    return {"id": clearance.id, "clearance_type": clearance.clearance_type, "status": clearance.status}


@router.get("/assets/{asset_id}/passport")
def asset_passport(asset_id: str, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    """The bridge passport, scoped to the caller's role and gated by derived phase.

    Two things this refuses to do:

    **It does not show a phase the bridge has not reached.** A proposed bridge
    carries no defect liability, no service life and no condition, so the
    post-construction sections are reported as closed *with the reason*, rather
    than being absent. A silently missing section reads as a broken system; a
    section that says "nothing has been constructed, so there is no defect
    liability period" reads as a system that knows what it is doing.

    **It does not show another company's commercial position to a contractor.**
    Bid prices and technical summaries are department-internal until award.
    """
    roles = actor_roles(session, user)
    if not roles:
        raise role_denied(["an authenticated role assignment"], f"{rules.RECORD} sec 4A.8")
    asset = guard_asset(session, user, roles, asset_id)
    fact = phase_facts(session, [asset.id])[asset.id]
    gates_by_phase = phase_gates(fact)

    project = session.scalar(select(ProjectRecord).where(ProjectRecord.asset_id == asset.id))
    tender = session.scalar(select(TenderRecord).where(TenderRecord.project_id == project.id)) if project else None
    contract = session.scalar(select(ContractRecord).where(ContractRecord.project_id == project.id)) if project else None
    defects = session.scalars(select(DefectRecord).where(DefectRecord.asset_id == asset.id).order_by(DefectRecord.status)).all()
    reports = session.scalars(select(ProjectReport).where(ProjectReport.project_id == project.id).order_by(ProjectReport.report_type)).all() if project else []
    clearances = session.scalars(select(ClearanceRecord).where(ClearanceRecord.project_id == project.id).order_by(ClearanceRecord.clearance_type)).all() if project else []
    defect_ids = [defect.id for defect in defects]
    work_orders = session.scalars(select(WorkOrderRecord).where(WorkOrderRecord.defect_id.in_(defect_ids or [""]))).all() if defect_ids else []
    gates = session.scalars(select(GateEvaluation).where(GateEvaluation.asset_id == asset.id).order_by(GateEvaluation.evaluated_at.desc())).all()
    events = session.scalars(select(AuditEvent).where(AuditEvent.asset_id == asset.id).order_by(AuditEvent.created_at.desc()).limit(40)).all()

    # A contractor sees only their own company's work orders, never another
    # contractor's, and never a bid table they are not a party to.
    own_company_ids: set[str] = contractor_company_ids(session, user.id) if "CONTRACTOR" in roles else set()
    if "CONTRACTOR" in roles:
        work_orders = [work for work in work_orders if work.company_id in own_company_ids]

    # Bid visibility. The tender notice is public; the tender room is not. A
    # contractor sees their own bid and whether they have been awarded, plus the
    # fact that competing bids exist. They never see a competitor's price, and
    # only the awarding authority sees the full table.
    bids_payload: list[dict] = []
    if tender is not None:
        all_bids = session.scalars(select(TenderBidRecord).where(TenderBidRecord.tender_id == tender.id).order_by(TenderBidRecord.price_amount)).all()
        can_see_prices = "CONTRACTOR" not in roles
        for bid in all_bids:
            if "CONTRACTOR" in roles and bid.company_id not in own_company_ids:
                bids_payload.append(
                    {
                        "id": bid.id,
                        "company_id": bid.company_id,
                        "own_bid": False,
                        "price_amount": None if not can_see_prices else float(bid.price_amount),
                        "technical_status": bid.technical_status,
                        "redacted": True,
                        "note": "A competing bid exists. Prices are visible to the department, not to other bidders.",
                    }
                )
            else:
                bids_payload.append(
                    {
                        "id": bid.id,
                        "company_id": bid.company_id,
                        "own_bid": "CONTRACTOR" in roles,
                        "price_amount": float(bid.price_amount) if can_see_prices else float(bid.price_amount),
                        "technical_status": bid.technical_status,
                        "redacted": False,
                    }
                )

    pre_open = gates_by_phase[PHASE_PRE]["available"]
    build_open = gates_by_phase[PHASE_BUILD]["available"]
    post_open = gates_by_phase[PHASE_POST]["available"]

    payload: dict = {
        "asset": asset_view(asset, session.get(BridgeProfile, asset.id), fact),
        "phase": fact.as_dict(),
        "phase_purpose": dict(PHASE_PURPOSE),
        "phase_gates": gates_by_phase,
        "scope": {"roles": sorted(roles), "explanation": scope_explanation(roles)},
        "project": None if not project else {
            "id": project.id, "title": project.title, "state": project.state, "type": project.project_type,
            "estimate_amount": float(project.estimate_amount) if project.estimate_amount else None,
        },
        "tender": None if not tender else {
            "id": tender.id, "number": tender.tender_number, "status": tender.status,
            "tender_form": tender.tender_form,
            "opening_on": tender.opening_on.isoformat() if tender.opening_on else None,
        },
        "contract": None if not contract else {
            "id": contract.id, "number": contract.contract_number, "state": contract.state,
            "awarded_amount": float(contract.awarded_amount),
        },
        "bids": bids_payload,
        "reports": [
            {"id": report.id, "type": report.report_type, "status": report.status, "reference": report.reference, "source_class": report.source_class}
            for report in reports
        ] if pre_open else [],
        "clearances": [
            {"id": clearance.id, "type": clearance.clearance_type, "status": clearance.status, "reference": clearance.reference, "source_class": clearance.source_class}
            for clearance in clearances
        ] if pre_open else [],
        "gates": [
            {"id": gate.id, "status": gate.status, "explanation": gate.explanation, "missing_requirements": gate.missing_requirements}
            for gate in gates
        ] if pre_open else [],
        "defects": [
            {"id": defect.id, "description": defect.description, "risk_level": defect.risk_level, "status": defect.status, "due_on": defect.due_on}
            for defect in defects
        ] if post_open else [],
        "work_orders": [
            {"id": work.id, "defect_id": work.defect_id, "status": work.status, "description": work.description, "company_id": work.company_id}
            for work in work_orders
        ] if post_open else [],
        "timeline": [
            {"id": event.id, "at": event.created_at.isoformat(), "event_type": event.event_type, "reason": event.reason, "new_value": event.new_value}
            for event in events
        ],
    }

    if build_open and contract is not None:
        milestones = session.scalars(select(Milestone).where(Milestone.contract_id == contract.id).order_by(Milestone.planned_percent)).all()
        payload["milestones"] = [
            {
                "id": milestone.id,
                "name": milestone.name,
                "planned_percent": str(milestone.planned_percent),
                "actual_percent": str(milestone.actual_percent),
                "credit": rules.milestone_credit(Decimal(milestone.planned_percent), Decimal(milestone.actual_percent)).as_dict(),
            }
            for milestone in milestones
        ]
    else:
        payload["milestones"] = []

    if post_open:
        completion_date = getattr(contract, "completion_date", None) if contract else None
        open_defects = sum(1 for defect in defects if defect.status != "CLOSED")
        payload["defect_liability"] = (
            rules.dlp_state(completion_date, open_defects, datetime.now(UTC).date()).as_dict()
            if completion_date
            else {
                "active": False,
                "established": False,
                "basis": f"{rules.RECORD} sec 3.6 and 3.6.1 (Art. 17.1(d), Art. 17.5)",
                "reasons": ("No Completion Certificate date is recorded, so the 10-year period has not started.",),
            }
        )
        payload["retention"] = rules.retention_refund(completion_date).as_dict()
    else:
        payload["defect_liability"] = {"available": False, "reason": gates_by_phase[PHASE_POST]["reason"]}
        payload["retention"] = {"available": False, "reason": gates_by_phase[PHASE_POST]["reason"]}

    payload["closed_sections"] = [
        {"phase": name, "reason": gates_by_phase[name]["reason"]}
        for name in (PHASE_PRE, PHASE_BUILD, PHASE_POST)
        if not gates_by_phase[name]["available"]
    ]
    return payload


@router.get("/assets/{asset_id}/defect-liability")
def defect_liability(asset_id: str, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    """The DLP as a predicate, not a date.

    ``DLP_active = (now < completion + 10 years) AND (open_defects == 0)``.

    Art. 17.5 extends the period until identified defects are remedied, so the
    clock does not run out while a defect is open. This is the calculation the
    research record calls the product's reason for existing, and it is
    meaningless without the second term: a date alone would let defects quietly
    lapse, which is precisely the failure the second term forecloses.
    """
    roles = actor_roles(session, user)
    if not roles:
        raise role_denied(["an authenticated role assignment"], f"{rules.RECORD} sec 4A.8")
    asset = guard_asset(session, user, roles, asset_id)
    fact = phase_facts(session, [asset.id])[asset.id]
    if fact.phase != PHASE_POST:
        raise wrong_phase(
            PHASE_LABELS[fact.phase],
            "a defect liability period",
            list(fact.blockers) or [phase_gates(fact)[PHASE_POST]["reason"]],
            f"{rules.RECORD} sec 3.6 (a defect liability period runs from the Completion Certificate of a constructed bridge)",
        )
    project = session.scalar(select(ProjectRecord).where(ProjectRecord.asset_id == asset.id))
    contract = session.scalar(select(ContractRecord).where(ContractRecord.project_id == project.id)) if project else None
    completion_date = getattr(contract, "completion_date", None) if contract else None
    if completion_date is None:
        raise not_established(
            "The defect liability period for this bridge",
            "the Completion Certificate date, which no record in this system holds",
        )
    defects = session.scalars(select(DefectRecord).where(DefectRecord.asset_id == asset.id)).all()
    open_defects = [defect for defect in defects if defect.status != "CLOSED"]
    dlp = rules.dlp_state(completion_date, len(open_defects), datetime.now(UTC).date())
    return {
        "asset_id": asset.id,
        "dlp": dlp.as_dict(),
        "retention": rules.retention_refund(completion_date).as_dict(),
        "open_defects": [
            {"id": defect.id, "description": defect.description, "risk_level": defect.risk_level, "due_on": defect.due_on}
            for defect in open_defects
        ],
        "note": (
            "Retention is refunded within 15 days of the Completion Certificate, so the cash leaves a "
            "fortnight into a decade of liability. The performance security is the only security behind "
            "the DLP."
        ),
    }


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
    """Publish a tender, subject to the land-readiness gate and the B-1 form rule."""
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER")
    tender = session.get(TenderRecord, tender_id)
    if not tender:
        raise missing("Tender not found", ["Check the tender reference in the passport."])
    project = session.get(ProjectRecord, tender.project_id)
    if not project:
        raise missing("Project not found", ["The tender is not linked to a project."])
    roles = actor_roles(session, user)
    asset = guard_asset(session, user, roles, project.asset_id)

    evaluation = session.scalar(select(GateEvaluation).where(GateEvaluation.project_id == project.id).order_by(GateEvaluation.evaluated_at.desc()))
    if not evaluation or evaluation.status != "PASSED":
        raise gate_blocked(
            "Tender publication requires a passed land-readiness gate: 90% possession with a handover memorandum.",
            list(evaluation.missing_requirements) if evaluation else ["No land-readiness evaluation has been recorded for this project."],
            f"{rules.RECORD} sec 2.5 and 2.5.2 (90% possession and the handover memorandum; the evaluation is machine-checkable, which is what makes it a gate)",
        )

    # B-1 is mandatory above the sourced ceiling, and the ceiling differs for a
    # bridge than for a road. Publishing above it on a B-2 form is the branch the
    # rule exists to prevent.
    profile = session.get(BridgeProfile, asset.id)
    is_bridge = bool(profile) and profile.bridge_class in ("MAJOR_BRIDGE", "MINOR_BRIDGE", "ROB", "RUB")
    form = rules.tender_form(Decimal(tender.estimated_cost or 0), is_bridge)
    tender_recorded_form = (tender.tender_form or "B-1").upper()
    if form.passed and tender_recorded_form != "B-1":
        raise gate_blocked(
            f"The estimated cost is above the B-1 ceiling of {form.value['b1_ceiling_crore']} crore for "
            f"{form.value['applies_to']} works, so the tender must be invited on B-1 form only. "
            f"This tender is recorded on {tender_recorded_form}.",
            [f"Re-invite on B-1, or reduce the scope to below {form.value['b1_ceiling']}."],
            f"{rules.RECORD} sec 4A.2 (GR TNC-1088-D-347-(7)-C dt 11-07-2017: B-1 invariably above the ceiling)",
        )

    tender.status = "PUBLISHED"
    project.state = "TENDERED"
    # Publishing is the moment bids can be submitted, so it is the moment the
    # 120-day clock starts. Recording it here rather than at award is what makes
    # the rule evaluable: an award-time-only record could always be backdated to
    # look compliant, which is exactly the failure the rule exists to catch.
    if tender.opening_on is None:
        tender.opening_on = datetime.now(UTC).date()
    if tender.opened_by_id is None:
        tender.opened_by_id = user.id
    audit(session, user, asset.id, "TENDER", tender.id, "TENDER_PUBLISHED", new_value={"status": tender.status, "form": tender_recorded_form, "opening_on": tender.opening_on.isoformat()}, reason=f"Gate passed; 120-day acceptance clock starts {tender.opening_on.isoformat()}. {form.reasons[0]}")
    session.commit()
    return {
        "id": tender.id,
        "status": tender.status,
        "tender_form": tender_recorded_form,
        "opening_on": tender.opening_on.isoformat(),
        "form_rule": form.as_dict(),
        "acceptance_deadline": rules.tender_acceptance_120_day(tender.opening_on, None, None).as_dict(),
    }


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
    """Award to the lowest evaluated bid, inside the three-layer approval chain.

    Research record section 2.7: the chain is EE invites, SE of the circle opens,
    the Department approves. CAG found a miscalculation that passed all three
    layers uncaught, which is the empirical case for making each layer a real
    recorded step rather than a status change. Each layer below records who acted
    and when, so the chain is auditable and not merely described.
    """
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "SUPERINTENDING_ENGINEER")
    tender = session.get(TenderRecord, tender_id)
    if not tender:
        raise missing("Tender not found", ["Check the tender reference in the passport."])
    if tender.status != "PUBLISHED":
        raise conflict(
            f"This tender is {label_status(tender.status)}, so it cannot be awarded.",
            ["Publish the tender before evaluating bids."],
        )
    winner = session.scalar(select(TenderBidRecord).where(TenderBidRecord.tender_id == tender.id).order_by(TenderBidRecord.price_amount).limit(1))
    if not winner:
        raise HTTPException(409, "At least one controlled tender-room bid is required")
    contract = session.scalar(select(ContractRecord).where(ContractRecord.tender_id == tender.id))
    if contract:
        return {"id": contract.id, "state": contract.state, "company_id": contract.company_id}
    project = session.get(ProjectRecord, tender.project_id)
    # The 120-day rule. Accepted and work-ordered within 120 days of opening, or
    # the tender is re-invited. CAG cost the department 5.40 to 6.13 crore on one
    # Mehsana re-tender, so this is a real rule with a real price tag, and it is
    # checkable from three dates that are all already recorded.
    opening_date = tender.opening_on
    if opening_date is None:
        raise invalid(
            "The tender has no recorded opening date, so the 120-day acceptance rule cannot be evaluated.",
            remediation=["Record the tender opening date before awarding."],
        )
    # The third approval layer -- the Department's approval -- is also the point
    # the work order issues. Recording it here is deliberate: the 120-day rule
    # requires *both* acceptance and the work order inside the window, so an
    # engine that only recorded acceptance would evaluate a weaker rule than the
    # one the clause actually states.
    today = datetime.now(UTC).date()
    tender.work_order_issued_on = today
    window = rules.tender_acceptance_120_day(
        opening_date,
        accepted_date=today,
        work_order_date=tender.work_order_issued_on,
    )
    if not window.passed:
        raise gate_blocked(
            "The 120-day acceptance rule is not satisfied, so this tender must be re-invited.",
            list(window.reasons),
            f"{rules.RECORD} sec 4A.9 (GPWM Clause 212-A, GR 10-05-2013; breach means re-tender, which cost 5.40 to 6.13 crore in Mehsana)",
        )
    if not (tender.tender_form or "B-1").upper() == "B-1" and Decimal(winner.price_amount) > Decimal(tender.estimated_cost or 0) * Decimal("1.2"):
        raise gate_blocked(
            f"The winning price is materially above the estimate of {tender.estimated_cost}. An award at this "
            "level on a B-2 form is not available above the B-1 ceiling.",
            [f"Re-invite on B-1, or record the revised estimate and its sanction."],
            f"{rules.RECORD} sec 4A.2 (B-1 is mandatory above the ceiling)",
        )

    contract = ContractRecord(
        id=uid("CON"),
        project_id=project.id,
        tender_id=tender.id,
        company_id=winner.company_id,
        contract_number=f"SYN-CON-{tender.tender_number[-4:]}",
        awarded_amount=winner.price_amount,
        state="AWARDED",
        appointed_date=tender.work_order_issued_on,
        physical_progress=Decimal("0"),
    )
    tender.status, project.state = "AWARDED", "AWARDED"
    asset = get_asset(session, project.asset_id)
    session.add_all([
        contract,
        Milestone(id=uid("MS"), contract_id=contract.id, name="Mobilisation and quality plan", planned_percent=35, actual_percent=0),
        Milestone(id=uid("MS"), contract_id=contract.id, name="Substructure complete; construction of all bridges started", planned_percent=60, actual_percent=0),
        Milestone(id=uid("MS"), contract_id=contract.id, name="Superstructure and finishing substantially complete", planned_percent=85, actual_percent=0),
    ])
    security = rules.security_deposit(Decimal(tender.estimated_cost or 0))
    bond = rules.performance_bond(winner.price_amount)
    audit(session, user, asset.id, "CONTRACT", contract.id, "CONTRACT_AWARDED", new_value={"company_id": winner.company_id, "amount": float(winner.price_amount), "security_deposit": security.value["amount"], "performance_bond": bond.value["amount"]}, reason=f"Security deposit {security.value['percent']}% and performance bond {bond.value['percent']}% of contract amount. 120-day rule satisfied by {window.value['deadline']}.")
    session.commit()
    return {
        "id": contract.id,
        "state": contract.state,
        "company_id": contract.company_id,
        "awarded_amount": float(contract.awarded_amount),
        "derived_phase": PHASE_BUILD,
        "phase_basis": "A contract has been awarded, so the bridge is under construction.",
        "security_deposit": security.as_dict(),
        "performance_bond": bond.as_dict(),
        "tender_acceptance_rule": window.as_dict(),
        "approval_chain": [
            {"layer": 1, "authority": "Executive Engineer", "action": "Invited the tender", "by": tender.invited_by_id, "at": tender.invited_at.isoformat() if getattr(tender, "invited_at", None) else None},
            {"layer": 2, "authority": "Superintending Engineer of the Circle", "action": "Opened the tender", "by": tender.opened_by_id, "at": tender.opening_on.isoformat() if tender.opening_on else None},
            {"layer": 3, "authority": "The Department", "action": "Approved the award and the contract", "by": user.id, "at": today.isoformat()},
        ],
    }


@router.post("/contracts/{contract_id}/quality-tests", status_code=status.HTTP_201_CREATED)
def submit_quality_test(contract_id: str, payload: TestInput, user: User = Depends(get_current_user), session: Session = Depends(session_dependency)) -> dict:
    """Evaluate cube samples against the two-condition MoRTH acceptance rule.

    The previous implementation compared every sample to the specified value and
    then described itself in the audit trail as "not a Gujarat R&B acceptance
    rule". That was at least honest, but it meant the product's headline quality
    gate was a guess. Section 3.2 of the research record calls the real rule "the
    template for every quality gate in the product", so it is implemented exactly
    as written, and the record states which criterion governed.
    """
    require(session, user, "STATE_ADMIN", "QUALITY_ENGINEER", "EXECUTIVE_ENGINEER")
    contract = session.get(ContractRecord, contract_id)
    if not contract:
        raise missing("Contract not found", ["Check the contract reference in the passport."])
    project = session.get(ProjectRecord, contract.project_id)
    if not project:
        raise missing("Project not found", ["The contract is not linked to a project."])

    facts = phase_facts(session, [project.asset_id])[project.asset_id]
    if facts.phase != PHASE_BUILD:
        raise wrong_phase(
            PHASE_LABELS[facts.phase],
            "a construction quality test",
            list(facts.blockers),
            f"{rules.RECORD} sec 3.2 (quality acceptance applies to concrete placed under an awarded contract)",
        )

    policy = session.scalar(select(PolicyVersion).where(PolicyVersion.policy_code == "CONCRETE_ACCEPTANCE"))
    test = QualityTest(
        id=uid("TEST"),
        contract_id=contract.id,
        test_type=payload.test_type,
        specified_value=payload.specified_value,
        rule_policy_version_id=policy.id if policy else None,
        status="SUBMITTED",
    )
    session.add(test)
    session.flush()
    for number, value in enumerate(payload.samples, start=1):
        session.add(TestSample(id=uid("SAMPLE"), test_id=test.id, sample_number=number, measured_value=value, recorded_by_id=user.id))

    cube = rules.concrete_cube_acceptance(payload.samples, payload.specified_value)
    core = rules.core_acceptance(payload.cores, payload.specified_value) if payload.cores else None

    # Cubes govern. Cores are the documented fallback when cubes fail, so a
    # failure on cubes with passing cores is recorded as the fallback having
    # saved the result -- not as a pass, and not as an unexamined failure.
    if cube.passed:
        calculated = "PASS"
        criterion = "cubes"
        reasons: tuple[str, ...] = ()
    elif core is not None and core.passed:
        calculated = "PASS_ON_CORES"
        criterion = "cores_fallback"
        reasons = ()
    else:
        calculated = "FAIL"
        criterion = "cubes_and_cores"
        reasons = tuple(cube.reasons) + (tuple(core.reasons) if core else ())

    calculation: dict = {
        "criterion_applied": criterion,
        "rule": "MoRTH cube acceptance: mean of four consecutive samples above specified + 3 MPa, and no sample below specified - 3 MPa",
        "basis": cube.basis,
        "cube_result": cube.as_dict(),
        "core_result": core.as_dict() if core else None,
        "specified_value": float(payload.specified_value),
    }
    session.add(
        TestEvaluation(
            id=uid("EVAL"),
            test_id=test.id,
            calculated_status=calculated,
            calculation=calculation,
        )
    )

    if not cube.passed and (core is None or not core.passed):
        # The test is recorded, because the record of a failure is the evidence.
        test.status = "FAILED"
        audit(
            session,
            user,
            project.asset_id,
            "QUALITY_TEST",
            test.id,
            "QUALITY_TEST_FAILED",
            new_value={"calculated_status": calculated},
            reason="; ".join(reasons) or "Acceptance criteria not met.",
        )
        session.commit()
        raise rule_violation(
            "CONCRETE_ACCEPTANCE_FAILED",
            f"{payload.test_type} does not meet the concrete acceptance criteria.",
            detail=calculation["rule"] + f". Specified {payload.specified_value}.",
            remediation=list(reasons),
            reference=cube.basis,
        )

    test.status = "PASSED"
    audit(
        session,
        user,
        project.asset_id,
        "QUALITY_TEST",
        test.id,
        "QUALITY_TEST_EVALUATED",
        new_value={"calculated_status": calculated, "criterion": criterion},
        reason=f"Evaluated against the sourced acceptance rule; {criterion} governed.",
    )
    session.commit()
    return {
        "test_id": test.id,
        "calculated_status": calculated,
        "criterion_applied": criterion,
        "calculation": calculation,
    }


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
    """Compute the price-variation entitlement. The client does not.

    This replaces an endpoint that accepted both ``submitted_amount`` and
    ``calculated_amount`` from the caller and stored the difference. That is a
    difference calculator, not an engine, and it leaves the arithmetic with the
    people who got it wrong: CAG recorded 4.74 crore rupees overpaid across 11
    works in 5 divisions, and in Bharuch a single interchange of the Cement and
    Steel base indices turned a 15.57 lakh recovery into a 40.13 lakh payment.

    The caller now supplies measured facts only. The entitlement is computed here
    against Gujarat's own clauses 59/59A and 60/60A, capped at the sourced
    ceiling, and refused outright if the index bases cannot be verified.
    """
    require(session, user, "STATE_ADMIN", "EXECUTIVE_ENGINEER", "FINANCE")
    contract = session.get(ContractRecord, contract_id)
    if not contract:
        raise missing("Contract not found", ["Check the contract reference in the passport."])
    project = session.get(ProjectRecord, contract.project_id)
    if not project:
        raise missing("Project not found", ["The contract is not linked to a project."])

    facts = phase_facts(session, [project.asset_id])[project.asset_id]
    if facts.phase != PHASE_BUILD:
        raise wrong_phase(
            PHASE_LABELS[facts.phase],
            "a running-account price variation",
            list(facts.blockers),
            f"{rules.RECORD} sec 4A.4 (price variation arises on an executing contract)",
        )

    policy = session.scalar(select(PolicyVersion).where(PolicyVersion.policy_code == "PRICE_VARIATION", PolicyVersion.active.is_(True)))
    asset = get_asset(session, project.asset_id)
    profile = session.scalar(select(BridgeProfile).where(BridgeProfile.asset_id == asset.id))
    is_bridge = profile.bridge_class in ("MAJOR_BRIDGE", "MINOR_BRIDGE", "ROB", "RUB") if profile else payload.is_bridge
    estimated_cost = Decimal(project.estimate_amount) if project.estimate_amount is not None else contract.awarded_amount

    components = [
        rules.PvComponent(
            name=line.component,
            portion=line.portion,
            base_index=line.base_index,
            current_index=line.current_index,
            is_bridge=is_bridge,
        )
        for line in payload.components
    ]
    engine = rules.price_variation(components, months_elapsed=payload.months_elapsed, estimated_cost=estimated_cost)
    admissibility = rules.pv_admissible(estimated_cost, time_limit_months=payload.months_elapsed if payload.months_elapsed else 0)
    if not admissibility.passed:
        engine = rules.Verdict(
            passed=False,
            value=engine.value,
            basis=engine.basis,
            reasons=admissibility.reasons + engine.reasons,
        )

    payable = Decimal(engine.value["payable"])
    claimed = payload.claimed_amount
    variance = (claimed - payable) if claimed is not None else None

    if not engine.passed:
        # A refused claim is still recorded. The refusal is the evidence.
        claim = PriceVariationClaim(
            id=uid("PV"),
            contract_id=contract.id,
            submitted_amount=claimed or payable,
            calculated_amount=payable,
            variance_amount=variance if variance is not None else Decimal("0.00"),
            status="REFUSED",
            policy_version_id=policy.id,
            explanation="; ".join(engine.reasons),
        )
        session.add(claim)
        audit(
            session,
            user,
            project.asset_id,
            "PRICE_VARIATION_CLAIM",
            claim.id,
            "PRICE_VARIATION_REFUSED",
            new_value={"computed": float(payable), "claimed": float(claimed) if claimed is not None else None},
            reason="; ".join(engine.reasons),
        )
        session.commit()
        raise rule_violation(
            "PRICE_VARIATION_REFUSED",
            "This price-variation claim does not qualify.",
            detail=engine.basis,
            remediation=list(engine.reasons),
            reference=engine.basis,
        )

    status_value = "VALIDATED" if variance is None or abs(variance) <= Decimal("1.00") else "VARIANCE_REQUIRES_REVIEW"
    explanation = (
        "The engine's computed entitlement matches the amount claimed."
        if status_value == "VALIDATED"
        else (
            f"The engine computes {payable} against the amount claimed, a variance of {variance}. "
            "The claim is preserved and routed for finance review rather than rejected, because a "
            "variance can also mean the claimant holds a document the engine has not seen."
        )
    )
    claim = PriceVariationClaim(
        id=uid("PV"),
        contract_id=contract.id,
        submitted_amount=claimed or payable,
        calculated_amount=payable,
        variance_amount=variance if variance is not None else Decimal("0.00"),
        status=status_value,
        policy_version_id=policy.id,
        explanation=explanation,
    )
    session.add(claim)
    audit(
        session,
        user,
        project.asset_id,
        "PRICE_VARIATION_CLAIM",
        claim.id,
        "PRICE_VARIATION_COMPUTED",
        new_value={
            "computed": float(payable),
            "claimed": float(claimed) if claimed is not None else None,
            "variance": float(variance) if variance is not None else None,
            "status": status_value,
        },
        reason=f"Computed by the sourced price-variation engine. {engine.basis}",
    )
    session.commit()
    return {
        "id": claim.id,
        "status": claim.status,
        "computed_amount": float(payable),
        "claimed_amount": float(claimed) if claimed is not None else None,
        "variance_amount": float(claim.variance_amount),
        "explanation": claim.explanation,
        "engine": engine.as_dict(),
        "admissibility": admissibility.as_dict(),
    }
