"""Normalized lifecycle domain for the BridgeTheGap MVP.

These tables are additive to the first prototype schema.  They deliberately keep
policy and evidence as first-class data so no Gujarat-specific unknown is baked
into application code.
"""
# ruff: noqa: I001 - SQLAlchemy types are kept together for readability.

from datetime import UTC, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def now() -> datetime:
    return datetime.now(UTC)


class OrganisationUnit(Base):
    __tablename__ = "organisation_units"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(180), unique=True)
    kind: Mapped[str] = mapped_column(String(40))  # DEPARTMENT, WING, CIRCLE, DIVISION, SUBDIVISION
    parent_id: Mapped[str | None] = mapped_column(ForeignKey("organisation_units.id"))
    code: Mapped[str | None] = mapped_column(String(40), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class RoleDefinition(Base):
    __tablename__ = "role_definitions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(60), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    permissions: Mapped[dict] = mapped_column(JSON, default=dict)


class UserRoleAssignment(Base):
    __tablename__ = "user_role_assignments"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    role_id: Mapped[str] = mapped_column(ForeignKey("role_definitions.id"), index=True)
    organisation_unit_id: Mapped[str | None] = mapped_column(ForeignKey("organisation_units.id"), index=True)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ContractorCompany(Base):
    __tablename__ = "contractor_companies"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    legal_name: Mapped[str] = mapped_column(String(180), unique=True)
    registration_reference: Mapped[str | None] = mapped_column(String(120))
    registration_circle_id: Mapped[str | None] = mapped_column(ForeignKey("organisation_units.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class CompanyUserMembership(Base):
    __tablename__ = "company_user_memberships"
    __table_args__ = (UniqueConstraint("company_id", "user_id", name="uq_company_user"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    company_id: Mapped[str] = mapped_column(ForeignKey("contractor_companies.id"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class ContractorClassHistory(Base):
    __tablename__ = "contractor_class_history"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    company_id: Mapped[str] = mapped_column(ForeignKey("contractor_companies.id"), index=True)
    class_code: Mapped[str] = mapped_column(String(40))
    effective_from: Mapped[Date] = mapped_column(Date)
    effective_to: Mapped[Date | None] = mapped_column(Date)
    source_reference: Mapped[str | None] = mapped_column(String(200))


class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    asset_type: Mapped[str] = mapped_column(String(40), index=True)
    canonical_name: Mapped[str] = mapped_column(String(240))
    owner_unit_id: Mapped[str] = mapped_column(ForeignKey("organisation_units.id"), index=True)
    lifecycle_state: Mapped[str] = mapped_column(String(50), default="PROPOSED", index=True)
    service_state: Mapped[str] = mapped_column(String(30), default="OPEN", index=True)
    condition_grade: Mapped[str | None] = mapped_column(String(20))
    risk_flag: Mapped[str | None] = mapped_column(String(40), index=True)
    district: Mapped[str | None] = mapped_column(String(100))
    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6))
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)


class BridgeProfile(Base):
    __tablename__ = "bridge_profiles"
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), primary_key=True)
    bridge_class: Mapped[str] = mapped_column(String(40))  # MAJOR_BRIDGE, MINOR_BRIDGE, ROB, RUB, CULVERT
    route_name: Mapped[str | None] = mapped_column(String(180))
    chainage_km: Mapped[float | None] = mapped_column(Numeric(12, 3))
    length_m: Mapped[float | None] = mapped_column(Numeric(12, 2))
    span_count: Mapped[int | None] = mapped_column(Integer)
    commissioned_on: Mapped[Date | None] = mapped_column(Date)
    naming_finalised_on: Mapped[Date | None] = mapped_column(Date)


class AssetComponent(Base):
    __tablename__ = "asset_components"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    component_type: Mapped[str] = mapped_column(String(80))
    component_label: Mapped[str] = mapped_column(String(160))


class AssetDesignBasis(Base):
    __tablename__ = "asset_design_basis"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), unique=True)
    design_life_years: Mapped[int | None] = mapped_column(Integer)
    discharge_return_period_years: Mapped[int | None] = mapped_column(Integer)
    qa_level: Mapped[str | None] = mapped_column(String(20))
    source_label: Mapped[str] = mapped_column(String(160))


class ProjectRecord(Base):
    __tablename__ = "lifecycle_projects"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), unique=True)
    owner_unit_id: Mapped[str] = mapped_column(ForeignKey("organisation_units.id"), index=True)
    project_type: Mapped[str] = mapped_column(String(40))
    title: Mapped[str] = mapped_column(String(240))
    state: Mapped[str] = mapped_column(String(50), default="SANCTION_AND_CLEARANCE", index=True)
    estimate_amount: Mapped[float | None] = mapped_column(Numeric(15, 2))
    created_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ProjectReport(Base):
    __tablename__ = "project_reports"
    __table_args__ = (UniqueConstraint("project_id", "report_type", name="uq_project_report_type"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_projects.id"), index=True)
    report_type: Mapped[str] = mapped_column(String(20))  # PFR, FSR, DPR, AA, TS
    status: Mapped[str] = mapped_column(String(30), default="DRAFT", index=True)
    reference: Mapped[str] = mapped_column(String(240))
    source_class: Mapped[str] = mapped_column(String(40))
    prepared_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    reviewed_by_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ClearanceRecord(Base):
    __tablename__ = "clearance_records"
    __table_args__ = (UniqueConstraint("project_id", "clearance_type", name="uq_project_clearance_type"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_projects.id"), index=True)
    clearance_type: Mapped[str] = mapped_column(String(60))
    status: Mapped[str] = mapped_column(String(30), default="PENDING", index=True)
    reference: Mapped[str | None] = mapped_column(String(240))
    source_class: Mapped[str] = mapped_column(String(40))
    recorded_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class SourceReference(Base):
    __tablename__ = "source_references"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(240))
    citation: Mapped[str] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(Text)
    source_class: Mapped[str] = mapped_column(String(40))


class PolicyVersion(Base):
    __tablename__ = "policy_versions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    policy_code: Mapped[str] = mapped_column(String(80), index=True)
    version: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(180))
    source_reference_id: Mapped[str | None] = mapped_column(ForeignKey("source_references.id"))
    source_class: Mapped[str] = mapped_column(String(40))
    expression: Mapped[dict] = mapped_column(JSON, default=dict)
    effective_from: Mapped[Date] = mapped_column(Date)
    effective_to: Mapped[Date | None] = mapped_column(Date)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    __table_args__ = (UniqueConstraint("policy_code", "version", name="uq_policy_version"),)


class GateDefinition(Base):
    __tablename__ = "gate_definitions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(80), unique=True)
    name: Mapped[str] = mapped_column(String(180))
    applies_at: Mapped[str] = mapped_column(String(50))
    blocking: Mapped[bool] = mapped_column(Boolean, default=True)
    responsible_role: Mapped[str] = mapped_column(String(60))
    approver_role: Mapped[str | None] = mapped_column(String(60))
    policy_version_id: Mapped[str] = mapped_column(ForeignKey("policy_versions.id"))


class GateEvaluation(Base):
    __tablename__ = "gate_evaluations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    gate_id: Mapped[str] = mapped_column(ForeignKey("gate_definitions.id"), index=True)
    project_id: Mapped[str | None] = mapped_column(ForeignKey("lifecycle_projects.id"), index=True)
    asset_id: Mapped[str | None] = mapped_column(ForeignKey("assets.id"), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True)
    explanation: Mapped[str] = mapped_column(Text)
    missing_requirements: Mapped[dict] = mapped_column(JSON, default=list)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    evaluated_by_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))


class DocumentRecord(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    document_type: Mapped[str] = mapped_column(String(80))
    title: Mapped[str] = mapped_column(String(240))
    reference_url: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(160))
    verification_state: Mapped[str] = mapped_column(String(40), default="UNVERIFIED")
    checksum: Mapped[str | None] = mapped_column(String(128))
    issued_on: Mapped[Date | None] = mapped_column(Date)
    uploaded_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class DocumentLink(Base):
    __tablename__ = "document_links"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), index=True)
    entity_type: Mapped[str] = mapped_column(String(60), index=True)
    entity_id: Mapped[str] = mapped_column(String(36), index=True)


class EvidenceRecord(Base):
    __tablename__ = "evidence_records"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    defect_id: Mapped[str | None] = mapped_column(ForeignKey("lifecycle_defects.id"), index=True)
    work_order_id: Mapped[str | None] = mapped_column(ForeignKey("lifecycle_work_orders.id"), index=True)
    evidence_type: Mapped[str] = mapped_column(String(30))  # BEFORE_PHOTO, AFTER_PHOTO, SITE_NOTE, AS_BUILT_REF
    reference_url: Mapped[str] = mapped_column(Text)
    caption: Mapped[str] = mapped_column(Text)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6))
    submitted_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    verification_state: Mapped[str] = mapped_column(String(30), default="SUBMITTED")


class TenderRecord(Base):
    __tablename__ = "lifecycle_tenders"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_projects.id"), unique=True)
    tender_number: Mapped[str] = mapped_column(String(80), unique=True)
    status: Mapped[str] = mapped_column(String(40), default="DRAFT", index=True)
    estimated_cost: Mapped[float] = mapped_column(Numeric(15, 2))
    invited_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    opened_by_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    opening_on: Mapped[Date | None] = mapped_column(Date)
    bid_valid_until: Mapped[Date | None] = mapped_column(Date)
    # Which bidding form the tender was invited on. B-1 is mandatory above the
    # sourced ceiling, and the ceiling differs for a bridge than for a road, so
    # the form is a fact about the tender rather than a label.
    tender_form: Mapped[str] = mapped_column(String(4), default="B-1")
    work_order_issued_on: Mapped[Date | None] = mapped_column(Date)


class TenderBidRecord(Base):
    __tablename__ = "lifecycle_tender_bids"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    tender_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_tenders.id"), index=True)
    company_id: Mapped[str] = mapped_column(ForeignKey("contractor_companies.id"), index=True)
    technical_status: Mapped[str] = mapped_column(String(40), default="SUBMITTED")
    price_amount: Mapped[float] = mapped_column(Numeric(15, 2))
    submitted_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    __table_args__ = (UniqueConstraint("tender_id", "company_id", name="uq_tender_company_bid"),)


class ContractRecord(Base):
    __tablename__ = "lifecycle_contracts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_projects.id"), unique=True)
    tender_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_tenders.id"), unique=True)
    company_id: Mapped[str] = mapped_column(ForeignKey("contractor_companies.id"))
    contract_number: Mapped[str] = mapped_column(String(80), unique=True)
    awarded_amount: Mapped[float] = mapped_column(Numeric(15, 2))
    state: Mapped[str] = mapped_column(String(40), default="AWARDED")
    appointed_date: Mapped[Date | None] = mapped_column(Date)
    # The Completion Certificate date. The 10-year defect liability period runs
    # from this date, and retention is refunded within 15 days of it, so a
    # contract that has been completed without recording this date cannot have
    # its liability period computed at all.
    completion_date: Mapped[Date | None] = mapped_column(Date)
    # Physical progress, 0-100. Milestone credit is pro-rated against this, and
    # it is the recorded fact that says whether a bridge has actually been built.
    physical_progress: Mapped[float | None] = mapped_column(Numeric(5, 2))
    dlp_policy_version_id: Mapped[str | None] = mapped_column(ForeignKey("policy_versions.id"))


class Milestone(Base):
    __tablename__ = "milestones"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    contract_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_contracts.id"), index=True)
    name: Mapped[str] = mapped_column(String(180))
    planned_percent: Mapped[float] = mapped_column(Numeric(5, 2))
    actual_percent: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    due_on: Mapped[Date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(40), default="PENDING")


class QualityTest(Base):
    __tablename__ = "quality_tests"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    contract_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_contracts.id"), index=True)
    test_type: Mapped[str] = mapped_column(String(80))
    specified_value: Mapped[float] = mapped_column(Numeric(12, 3))
    rule_policy_version_id: Mapped[str] = mapped_column(ForeignKey("policy_versions.id"))
    status: Mapped[str] = mapped_column(String(40), default="DRAFT")


class TestSample(Base):
    __tablename__ = "test_samples"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    test_id: Mapped[str] = mapped_column(ForeignKey("quality_tests.id"), index=True)
    sample_number: Mapped[int] = mapped_column(Integer)
    measured_value: Mapped[float] = mapped_column(Numeric(12, 3))
    recorded_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    __table_args__ = (UniqueConstraint("test_id", "sample_number", name="uq_test_sample_number"),)


class TestEvaluation(Base):
    __tablename__ = "test_evaluations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    test_id: Mapped[str] = mapped_column(ForeignKey("quality_tests.id"), unique=True)
    calculated_status: Mapped[str] = mapped_column(String(20))
    calculation: Mapped[dict] = mapped_column(JSON)
    reviewer_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class InspectionRecord(Base):
    __tablename__ = "lifecycle_inspections"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    inspection_type: Mapped[str] = mapped_column(String(40))
    grade: Mapped[str] = mapped_column(String(20))
    submitted_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    notes: Mapped[str | None] = mapped_column(Text)


class DefectRecord(Base):
    __tablename__ = "lifecycle_defects"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    inspection_id: Mapped[str | None] = mapped_column(ForeignKey("lifecycle_inspections.id"))
    component_id: Mapped[str | None] = mapped_column(ForeignKey("asset_components.id"))
    description: Mapped[str] = mapped_column(Text)
    risk_level: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(40), default="OPEN", index=True)
    owner_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    due_on: Mapped[Date | None] = mapped_column(Date)


class ATR(Base):
    __tablename__ = "atrs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    defect_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_defects.id"), unique=True)
    due_on: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(40), default="OPEN")
    response: Mapped[str | None] = mapped_column(Text)


class WorkOrderRecord(Base):
    __tablename__ = "lifecycle_work_orders"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    defect_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_defects.id"), index=True)
    company_id: Mapped[str] = mapped_column(ForeignKey("contractor_companies.id"))
    status: Mapped[str] = mapped_column(String(40), default="DRAFT")
    decision_type: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    approved_by_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))


class RectificationSubmission(Base):
    __tablename__ = "rectification_submissions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    work_order_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_work_orders.id"), unique=True)
    submitted_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    notes: Mapped[str] = mapped_column(Text)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class WorkVerification(Base):
    __tablename__ = "work_verifications"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    work_order_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_work_orders.id"), unique=True)
    verifier_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    decision: Mapped[str] = mapped_column(String(30))
    notes: Mapped[str | None] = mapped_column(Text)
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ServiceStateRequest(Base):
    __tablename__ = "service_state_requests"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    requested_state: Mapped[str] = mapped_column(String(30))
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="PENDING")
    requested_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    approved_by_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))


class PriceVariationClaim(Base):
    __tablename__ = "price_variation_claims"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    contract_id: Mapped[str] = mapped_column(ForeignKey("lifecycle_contracts.id"), index=True)
    submitted_amount: Mapped[float] = mapped_column(Numeric(15, 2))
    calculated_amount: Mapped[float | None] = mapped_column(Numeric(15, 2))
    variance_amount: Mapped[float | None] = mapped_column(Numeric(15, 2))
    status: Mapped[str] = mapped_column(String(40), default="SUBMITTED")
    policy_version_id: Mapped[str] = mapped_column(ForeignKey("policy_versions.id"))
    explanation: Mapped[str | None] = mapped_column(Text)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str | None] = mapped_column(ForeignKey("assets.id"), index=True)
    entity_type: Mapped[str] = mapped_column(String(60), index=True)
    entity_id: Mapped[str] = mapped_column(String(36), index=True)
    event_type: Mapped[str] = mapped_column(String(80))
    actor_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    old_value: Mapped[dict | None] = mapped_column(JSON)
    new_value: Mapped[dict | None] = mapped_column(JSON)
    reason: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, index=True)


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    kind: Mapped[str] = mapped_column(String(60))
    message: Mapped[str] = mapped_column(Text)
    entity_type: Mapped[str] = mapped_column(String(60))
    entity_id: Mapped[str] = mapped_column(String(36))
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
