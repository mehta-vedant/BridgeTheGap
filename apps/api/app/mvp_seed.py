# ruff: noqa: I001 - seed ordering mirrors the lifecycle narrative.
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User
from .mvp_models import (
    Asset,
    AssetComponent,
    ATR,
    AuditEvent,
    BridgeProfile,
    CompanyUserMembership,
    ContractorCompany,
    ContractorClassHistory,
    DefectRecord,
    GateDefinition,
    GateEvaluation,
    InspectionRecord,
    OrganisationUnit,
    PolicyVersion,
    ProjectRecord,
    RoleDefinition,
    SourceReference,
    TenderRecord,
    UserRoleAssignment,
)


def mvp_id(value: str) -> str:
    return f"00000000-0000-0000-0000-{value:0>12}"[-36:]


def seed_mvp_demo(session: Session) -> None:
    """Seed a single synthetic end-to-end bridge story without external data claims."""
    if session.scalar(select(Asset.id).limit(1)):
        return

    division = OrganisationUnit(id=mvp_id("1"), name="Vadodara Bridge Division", kind="DIVISION", code="VAD-BRD")
    circle = OrganisationUnit(id=mvp_id("2"), name="Vadodara Circle", kind="CIRCLE", code="VAD-CIR")
    roles = [
        RoleDefinition(id=mvp_id("10"), code="STATE_ADMIN", name="State Administrator"),
        RoleDefinition(id=mvp_id("11"), code="EXECUTIVE_ENGINEER", name="Executive Engineer"),
        RoleDefinition(id=mvp_id("12"), code="SUPERINTENDING_ENGINEER", name="Superintending Engineer"),
        RoleDefinition(id=mvp_id("13"), code="INSPECTOR", name="Inspector"),
        RoleDefinition(id=mvp_id("14"), code="CONTRACTOR", name="Contractor"),
        RoleDefinition(id=mvp_id("15"), code="QUALITY_ENGINEER", name="Quality Engineer"),
        RoleDefinition(id=mvp_id("16"), code="FINANCE", name="Divisional Accountant"),
    ]
    users = {user.email: user for user in session.scalars(select(User)).all()}
    company = ContractorCompany(id=mvp_id("20"), legal_name="Saffron Infrastructure", registration_reference="SYNTHETIC-DEMO-001", registration_circle_id=division.id)
    source = SourceReference(id=mvp_id("30"), title="Synthetic demonstration policy", citation="Demo configuration; not a Gujarat R&B rule.", source_class="DEMO_CONFIGURABLE")
    land_policy = PolicyVersion(id=mvp_id("31"), policy_code="LAND_READINESS", version=1, name="Land readiness demonstration gate", source_reference_id=source.id, source_class="NATIONAL_REFERENCE", expression={"minimum_possession_percent": 90, "required_evidence": ["handover_memorandum"]}, effective_from=date(2026, 1, 1))
    pv_policy = PolicyVersion(id=mvp_id("32"), policy_code="PRICE_VARIATION", version=1, name="Gujarat price variation demonstrator", source_reference_id=source.id, source_class="GUJARAT_VERIFIED", expression={"eligible_estimate_min": 2500000, "minimum_duration_months": 12, "first_12_months_eligible": False}, effective_from=date(2026, 1, 1))
    gate = GateDefinition(id=mvp_id("33"), code="LAND_READINESS", name="Land / right-of-way readiness", applies_at="TENDER_PUBLICATION", blocking=True, responsible_role="EXECUTIVE_ENGINEER", approver_role="SUPERINTENDING_ENGINEER", policy_version_id=land_policy.id)
    asset = Asset(id=mvp_id("40"), asset_code="BRG-GJ-VAD-000142", asset_type="BRIDGE", canonical_name="Mahi River Bridge", owner_unit_id=division.id, lifecycle_state="SANCTION_AND_CLEARANCE", service_state="OPEN", condition_grade="S", district="Vadodara")
    profile = BridgeProfile(asset_id=asset.id, bridge_class="MAJOR_BRIDGE", route_name="Vadodara–Dabhoi Road", chainage_km=42.6, length_m=184, span_count=8, naming_finalised_on=date(2026, 1, 15))
    project = ProjectRecord(id=mvp_id("41"), asset_id=asset.id, owner_unit_id=division.id, project_type="REHABILITATION", title="Mahi River Bridge Rehabilitation", state="SANCTION_AND_CLEARANCE", estimate_amount=Decimal("12500000.00"), created_by_id=users["engineer@demo.local"].id)
    evaluation = GateEvaluation(id=mvp_id("42"), gate_id=gate.id, project_id=project.id, asset_id=asset.id, status="FAILED", explanation="Tender publication is blocked: land possession is 72%, below the configured 90% demonstration threshold.", missing_requirements=["18% additional possession", "Handover memorandum reference"], evaluated_by_id=users["engineer@demo.local"].id)
    tender = TenderRecord(id=mvp_id("43"), project_id=project.id, tender_number="SYN-VAD-2026-0142", status="DRAFT", estimated_cost=Decimal("12500000.00"), invited_by_id=users["engineer@demo.local"].id)
    inspection = InspectionRecord(id=mvp_id("50"), asset_id=asset.id, inspection_type="PRE_MONSOON", grade="SRI", submitted_by_id=users["inspector@demo.local"].id, notes="Synthetic demo finding: deck drainage joint requires rectification.")
    due_on = datetime.now(UTC).date() + timedelta(days=30)
    defect = DefectRecord(id=mvp_id("51"), asset_id=asset.id, inspection_id=inspection.id, description="Deck drainage joint deterioration", risk_level="SAFETY_REVIEW", status="OPEN", owner_user_id=users["engineer@demo.local"].id, due_on=due_on)
    atr = ATR(id=mvp_id("52"), defect_id=defect.id, due_on=due_on, status="OPEN")
    events = [
        AuditEvent(id=mvp_id("60"), asset_id=asset.id, entity_type="ASSET", entity_id=asset.id, event_type="ASSET_CREATED", actor_id=users["engineer@demo.local"].id, new_value={"asset_code": asset.asset_code}, reason="Synthetic lifecycle scenario initialized."),
        AuditEvent(id=mvp_id("61"), asset_id=asset.id, entity_type="GATE_EVALUATION", entity_id=evaluation.id, event_type="GATE_FAILED", actor_id=users["engineer@demo.local"].id, new_value={"status": evaluation.status}, reason=evaluation.explanation),
        AuditEvent(id=mvp_id("62"), asset_id=asset.id, entity_type="INSPECTION", entity_id=inspection.id, event_type="INSPECTION_SUBMITTED", actor_id=users["inspector@demo.local"].id, new_value={"grade": "SRI"}, reason=inspection.notes),
    ]
    role_by_code = {role.code: role for role in roles}
    assignments = [
        UserRoleAssignment(id=mvp_id("70"), user_id=users["manager@demo.local"].id, role_id=role_by_code["STATE_ADMIN"].id, organisation_unit_id=division.id),
        UserRoleAssignment(id=mvp_id("71"), user_id=users["engineer@demo.local"].id, role_id=role_by_code["EXECUTIVE_ENGINEER"].id, organisation_unit_id=division.id),
        UserRoleAssignment(id=mvp_id("72"), user_id=users["inspector@demo.local"].id, role_id=role_by_code["INSPECTOR"].id, organisation_unit_id=division.id),
        UserRoleAssignment(id=mvp_id("73"), user_id=users["contractor@demo.local"].id, role_id=role_by_code["CONTRACTOR"].id, organisation_unit_id=division.id),
        CompanyUserMembership(id=mvp_id("74"), company_id=company.id, user_id=users["contractor@demo.local"].id),
        ContractorClassHistory(id=mvp_id("75"), company_id=company.id, class_code="SPECIAL_CATEGORY_I_BRIDGES", effective_from=date(2025, 1, 1), source_reference="Synthetic demo registration history"),
    ]
    session.add_all([division, circle, *roles, company, source, land_policy, pv_policy, gate, asset, profile, AssetComponent(id=mvp_id("44"), asset_id=asset.id, component_type="DECK", component_label="Deck drainage joint"), project, evaluation, tender, inspection, defect, atr, *events, *assignments])
    session.commit()
