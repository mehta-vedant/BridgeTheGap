# ruff: noqa: I001 - seed ordering mirrors the lifecycle narrative.
"""Seed a synthetic Gujarat R&B bridge portfolio.

The portfolio spans all three lifecycle phases the department itself uses
(Sanction & Clearance, Execution, Post-Completion) so the product is never
demonstrated as a single asset.

This seed is ADDITIVE and IDEMPOTENT per asset code.  It never deletes or
rewrites an existing row, so re-running it adds any missing portfolio asset and
leaves operator-created data untouched.
"""
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User
from .mvp_models import (
    ATR,
    Asset,
    AssetComponent,
    AuditEvent,
    BridgeProfile,
    CompanyUserMembership,
    ContractorClassHistory,
    ContractorCompany,
    ContractRecord,
    ClearanceRecord,
    DefectRecord,
    GateDefinition,
    GateEvaluation,
    InspectionRecord,
    Milestone,
    OrganisationUnit,
    PolicyVersion,
    PriceVariationClaim,
    ProjectRecord,
    ProjectReport,
    QualityTest,
    RectificationSubmission,
    RoleDefinition,
    SourceReference,
    TenderBidRecord,
    TenderRecord,
    TestEvaluation,
    TestSample,
    UserRoleAssignment,
    WorkOrderRecord,
    WorkVerification,
)

ROLE_CATALOGUE = [
    ("CHIEF_ENGINEER", "Chief Engineer"),
    ("SUPERINTENDING_ENGINEER", "Superintending Engineer"),
    ("EXECUTIVE_ENGINEER", "Executive Engineer"),
    ("INSPECTOR", "Inspector / Assistant or Deputy Engineer"),
    ("QUALITY_ENGINEER", "Quality Engineer"),
    ("FINANCE", "Divisional Accountant / Finance"),
    ("CONTRACTOR", "Contractor"),
    ("AUDITOR", "Auditor / Viewer"),
    ("STATE_ADMIN", "State Administrator"),
]

DIVISIONS = [
    ("1", "Vadodara Bridge Division", "VAD-BRD", "DIVISION"),
    ("3", "Bharuch Bridge Division", "BRC-BRD", "DIVISION"),
    ("4", "Surat Bridge Division", "SRT-BRD", "DIVISION"),
    ("5", "Navsari Bridge Division", "NAV-BRD", "DIVISION"),
    ("6", "Rajkot Bridge Division", "RAJ-BRD", "DIVISION"),
    ("7", "Bhavnagar Bridge Division", "BHV-BRD", "DIVISION"),
    ("2", "Vadodara Circle", "VAD-CIR", "CIRCLE"),
]

SANCTION = "SANCTION_AND_CLEARANCE"
EXECUTION = "EXECUTION"
POST = "POST_COMPLETION"

DIVISION_CODE_BY_ID = {raw_id: code for raw_id, _name, code, _kind in DIVISIONS}

SYNTHETIC = "Synthetic demonstration data. Not a Gujarat R&B record."


def mvp_id(value: str) -> str:
    return f"00000000-0000-0000-0000-{value:0>12}"[-36:]


def _portfolio() -> list[dict]:
    """The demo portfolio: nine bridges distributed across the three phases."""
    return [
        # ------------------------------------------------------------------
        # PHASE 1 - SANCTION AND CLEARANCE
        # ------------------------------------------------------------------
        {
            "id": "140", "code": "BRG-GJ-VAD-000142", "name": "Mahi River Bridge",
            "division": "1", "lifecycle": SANCTION, "service": "OPEN", "grade": None,
            "district": "Vadodara", "lat": 22.307000, "lng": 73.181000,
            "bridge_class": "MAJOR_BRIDGE", "route": "Vadodara - Dabhoi Road",
            "chainage": 42.6, "length": 184.0, "spans": 8,
            "project_type": "REHABILITATION", "title": "Mahi River Bridge Rehabilitation",
            "estimate": Decimal("12500000.00"),
            "reports": [("DPR", "DPR/BRG/2026/0142: rehabilitation design basis and estimate", "NATIONAL_REFERENCE")],
            "clearances": [("LAND", "PENDING", None), ("WATER", "PENDING", None)],
            "gate": ("FAILED", "Tender publication is blocked: land possession is 72%, below the configured 90% demonstration threshold.",
                     ["18% additional possession", "Handover memorandum reference"]),
        },
        {
            "id": "141", "code": "BRG-GJ-BRC-000311", "name": "Karkhana River Bridge",
            "division": "3", "lifecycle": SANCTION, "service": "OPEN", "grade": None,
            "district": "Bharuch", "lat": 21.703000, "lng": 72.996000,
            "bridge_class": "MAJOR_BRIDGE", "route": "Bharuch - Ankleshwar Road",
            "chainage": 18.4, "length": 156.0, "spans": 6,
            "project_type": "NEW_CONSTRUCTION", "title": "Karkhana River Bridge (New Construction)",
            "estimate": Decimal("24800000.00"),
            "reports": [
                ("PFR", "PFR/BRG/2026/0311: missing-link feasibility and need assessment", "NATIONAL_REFERENCE"),
                ("FSR", "FSR/BRG/2026/0311: options appraisal and cost basis", "NATIONAL_REFERENCE"),
                ("DPR", "DPR/BRG/2026/0311: sanction-ready design and tender package", "NATIONAL_REFERENCE"),
            ],
            "clearances": [
                ("LAND", "CLEARED", "SYN-LAND-MEMO-0311"),
                ("FOREST", "CLEARED", "SYN-FOREST-0311"),
                ("WATER", "PENDING", None),
                ("RAILWAY", "PENDING", None),
            ],
            "gate": ("FAILED", "Tender publication is blocked: water and railway crossing clearances are not recorded.",
                     ["Water authority NOC", "Railway crossing clearance"]),
            "tender": ("DRAFT", "SYN-BRC-2026-0311", Decimal("24800000.00")),
        },
        {
            "id": "142", "code": "BRG-GJ-SRT-000522", "name": "Bhogavo River Bridge",
            "division": "4", "lifecycle": SANCTION, "service": "OPEN", "grade": None,
            "district": "Surat", "lat": 21.170000, "lng": 72.831000,
            "bridge_class": "MAJOR_BRIDGE", "route": "Surat - Bardoli Road",
            "chainage": 9.8, "length": 212.0, "spans": 9,
            "project_type": "REPLACEMENT", "title": "Bhogavo River Bridge Replacement",
            "estimate": Decimal("38900000.00"),
            "reports": [
                ("PFR", "PFR/BRG/2026/0522: distress-driven replacement need", "NATIONAL_REFERENCE"),
                ("FSR", "FSR/BRG/2026/0522: replace versus strengthen options appraisal", "NATIONAL_REFERENCE"),
            ],
            "clearances": [("LAND", "PARTIAL", "SYN-LAND-MEMO-0522")],
            "gate": ("FAILED", "Tender publication is blocked: only 60% land possession is recorded for the replacement alignment.",
                     ["40% additional possession", "Rehabilitation option cost comparison"]),
        },
        # ------------------------------------------------------------------
        # PHASE 2 - EXECUTION
        # ------------------------------------------------------------------
        {
            "id": "150", "code": "BRG-GJ-NAV-000208", "name": "Alok Bridge",
            "division": "5", "lifecycle": EXECUTION, "service": "OPEN", "grade": None,
            "district": "Navsari", "lat": 20.948000, "lng": 72.932000,
            "bridge_class": "MAJOR_BRIDGE", "route": "Navsari - Vapi Road",
            "chainage": 27.1, "length": 98.0, "spans": 4,
            "project_type": "NEW_CONSTRUCTION", "title": "Alok Bridge (New Construction)",
            "estimate": Decimal("16200000.00"),
            "reports": [("DPR", "DPR/BRG/2026/0208: sanction-ready package", "NATIONAL_REFERENCE")],
            "clearances": [("LAND", "CLEARED", "SYN-LAND-MEMO-0208"), ("WATER", "CLEARED", "SYN-WATER-0208")],
            "gate": ("PASSED", "Land and water clearances recorded; tender publication is permitted.", []),
            "tender": ("PUBLISHED", "SYN-NAV-2026-0208", Decimal("16200000.00")),
            "bid": ("Saffron Infrastructure", Decimal("15740000.00"), "Controlled tender-room proposal with a documented execution approach."),
        },
        {
            "id": "151", "code": "BRG-GJ-VAD-000457", "name": "Tadaula Bridge",
            "division": "1", "lifecycle": EXECUTION, "service": "OPEN", "grade": None,
            "district": "Vadodara", "lat": 22.564000, "lng": 73.043000,
            "bridge_class": "MAJOR_BRIDGE", "route": "Vadodara - Tadaula Road",
            "chainage": 33.2, "length": 121.0, "spans": 5,
            "project_type": "NEW_CONSTRUCTION", "title": "Tadaula Bridge (New Construction)",
            "estimate": Decimal("19400000.00"),
            "reports": [("DPR", "DPR/BRG/2026/0457: sanction-ready package", "NATIONAL_REFERENCE")],
            "clearances": [("LAND", "CLEARED", "SYN-LAND-MEMO-0457"), ("WATER", "CLEARED", "SYN-WATER-0457")],
            "gate": ("PASSED", "Clearances recorded; tender published and evaluated.", []),
            "tender": ("AWARDED", "SYN-VAD-2026-0457", Decimal("19400000.00")),
            "contract": ("AWARDED", "SYN-CTR-2026-0457", Decimal("18830000.00"), date(2026, 3, 12), 62.5),
            "milestones": [("Foundation and substructure", 30.0, 31.5), ("Superstructure and bearings", 30.0, 24.0), ("Deck and wearing course", 25.0, 0.0), ("Finishes and approaches", 15.0, 0.0)],
            "quality": ("Concrete cube strength", Decimal("30"), [Decimal("32.4"), Decimal("31.1"), Decimal("33.0"), Decimal("29.6")]),
        },
        {
            "id": "152", "code": "BRG-GJ-RAJ-000633", "name": "Machhla Bridge",
            "division": "6", "lifecycle": EXECUTION, "service": "OPEN", "grade": None,
            "district": "Rajkot", "lat": 22.301000, "lng": 70.802000,
            "bridge_class": "MAJOR_BRIDGE", "route": "Rajkot - Gondal Road",
            "chainage": 51.7, "length": 143.0, "spans": 6,
            "project_type": "REHABILITATION", "title": "Machhla Bridge Strengthening",
            "estimate": Decimal("8700000.00"),
            "reports": [("DPR", "DPR/BRG/2026/0633: strengthening design basis", "NATIONAL_REFERENCE")],
            "clearances": [("LAND", "CLEARED", "SYN-LAND-MEMO-0633")],
            "gate": ("PASSED", "Clearances recorded; tender published and evaluated.", []),
            "tender": ("AWARDED", "SYN-RAJ-2026-0633", Decimal("8700000.00")),
            "contract": ("AWARDED", "SYN-CTR-2026-0633", Decimal("8412000.00"), date(2025, 11, 4), 88.0),
            "milestones": [("External post-tensioning", 45.0, 45.0), ("Deck and joint rehabilitation", 35.0, 35.0), ("Finishes and safety furniture", 20.0, 12.0)],
            "price_variation": (Decimal("1280000.00"), Decimal("1254500.00"), "SYN-PV-0633"),
        },
        # ------------------------------------------------------------------
        # PHASE 3 - POST-COMPLETION
        # ------------------------------------------------------------------
        {
            "id": "170", "code": "BRG-GJ-BRD-000174", "name": "Khan River Bridge",
            "division": "1", "lifecycle": POST, "service": "OPEN", "grade": "SRI",
            "district": "Vadodara", "lat": 22.718000, "lng": 73.144000,
            "bridge_class": "MAJOR_BRIDGE", "route": "Vadodara - Padra Road",
            "chainage": 24.5, "length": 167.0, "spans": 7,
            "commissioned_on": date(2019, 6, 20), "naming_finalised_on": date(2019, 7, 1),
            "project_type": "NEW_CONSTRUCTION", "title": "Khan River Bridge (New Construction)",
            "estimate": Decimal("22100000.00"),
            "reports": [("DPR", "DPR/BRG/2019/0174: as-built sanction package", "NATIONAL_REFERENCE")],
            "clearances": [("LAND", "CLEARED", "SYN-LAND-MEMO-0174")],
            "gate": ("PASSED", "All clearances recorded before tender publication.", []),
            "tender": ("AWARDED", "SYN-BRD-2019-0174", Decimal("22100000.00")),
            "contract": ("COMPLETED", "SYN-CTR-2019-0174", Decimal("21740000.00"), date(2019, 1, 22), 100.0),
            "inspection": ("PRE_MONSOON", "SRI", "Deck drainage joint deterioration and spalling at the pier-cap interface; accountable rectification required.", "SAFETY_REVIEW"),
            "defect": ("Deck drainage joint deterioration", "SAFETY_REVIEW", "OPEN", 30),
            "work_order": ("REPAIR", "APPROVED", "Repair the deck drainage joint and submit rectification evidence for independent verification."),
        },
        {
            "id": "171", "code": "BRG-GJ-SRT-000090", "name": "Gunga River Bridge",
            "division": "4", "lifecycle": POST, "service": "OPEN", "grade": "S",
            "district": "Surat", "lat": 21.245000, "lng": 72.789000,
            "bridge_class": "MAJOR_BRIDGE", "route": "Surat - Kamrej Road",
            "chainage": 6.3, "length": 134.0, "spans": 5,
            "commissioned_on": date(2016, 11, 8), "naming_finalised_on": date(2016, 12, 1),
            "project_type": "NEW_CONSTRUCTION", "title": "Gunga River Bridge (New Construction)",
            "estimate": Decimal("17800000.00"),
            "reports": [("DPR", "DPR/BRG/2016/0090: as-built sanction package", "NATIONAL_REFERENCE")],
            "clearances": [("LAND", "CLEARED", "SYN-LAND-MEMO-0090")],
            "gate": ("PASSED", "All clearances recorded before tender publication.", []),
            "tender": ("AWARDED", "SYN-SRT-2016-0090", Decimal("17800000.00")),
            "contract": ("COMPLETED", "SYN-CTR-2016-0090", Decimal("17420000.00"), date(2016, 4, 19), 100.0),
            "inspection": ("POST_MONSOON", "S", "Routine post-monsoon inspection completed; no distress requiring accountable rectification.", "NONE"),
            "defect_closed": ("Bearing seat seepage noted in 2023", "ROUTINE_MAINTENANCE", "CLOSED"),
        },
        {
            "id": "172", "code": "BRG-GJ-BRC-000745", "name": "Amika River Bridge",
            "division": "3", "lifecycle": POST, "service": "RESTRICTED", "grade": "U",
            "district": "Bharuch", "lat": 21.498000, "lng": 73.116000,
            "bridge_class": "MAJOR_BRIDGE", "route": "Bharuch - Netrang Road",
            "chainage": 39.9, "length": 176.0, "spans": 8,
            "commissioned_on": date(2004, 8, 12), "naming_finalised_on": date(2004, 9, 15),
            "project_type": "NEW_CONSTRUCTION", "title": "Amika River Bridge (New Construction)",
            "estimate": Decimal("9600000.00"),
            "reports": [("DPR", "DPR/BRG/2004/0745: as-built sanction package", "NATIONAL_REFERENCE")],
            "clearances": [("LAND", "CLEARED", "SYN-LAND-MEMO-0745")],
            "gate": ("PASSED", "All clearances recorded before tender publication.", []),
            "tender": ("AWARDED", "SYN-BRC-2004-0745", Decimal("9600000.00")),
            "contract": ("COMPLETED", "SYN-CTR-2004-0745", Decimal("9480000.00"), date(2004, 2, 10), 100.0),
            "inspection": ("SPECIAL", "U", "Pier-cap spalling and exposed reinforcement observed; load restriction applied pending engineering disposition.", "SAFETY_REVIEW"),
            "defect": ("Pier-cap spalling with exposed reinforcement", "SAFETY_REVIEW", "OPEN", 15),
        },
    ]


def _ensure_reference_data(session: Session, users: dict[str, User]) -> dict:
    """Idempotently create org units, roles, policies, gate and the demo company."""
    existing_units = {unit.code: unit for unit in session.scalars(select(OrganisationUnit)).all()}
    units: dict[str, OrganisationUnit] = {}
    for raw_id, name, code, kind in DIVISIONS:
        if code not in existing_units:
            unit = OrganisationUnit(id=mvp_id(raw_id), name=name, kind=kind, code=code, active=True)
            session.add(unit)
            session.flush()
        units[code] = existing_units.get(code) or unit
    session.flush()

    existing_roles = {role.code: role for role in session.scalars(select(RoleDefinition)).all()}
    roles: dict[str, RoleDefinition] = {}
    for index, (code, name) in enumerate(ROLE_CATALOGUE, start=100):
        if code not in existing_roles:
            role = RoleDefinition(id=mvp_id(str(index)), code=code, name=name)
            session.add(role)
            session.flush()
        roles[code] = existing_roles.get(code) or role
    session.flush()

    company = session.scalar(select(ContractorCompany).where(ContractorCompany.legal_name == "Saffron Infrastructure"))
    if not company:
        company = ContractorCompany(id=mvp_id("20"), legal_name="Saffron Infrastructure",
                                    registration_reference="SYNTHETIC-DEMO-001",
                                    registration_circle_id=units["VAD-BRD"].id)
        session.add(company)
        session.flush()

    source = session.scalar(select(SourceReference).where(SourceReference.citation == SYNTHETIC))
    if not source:
        source = SourceReference(id=mvp_id("30"), title="Synthetic demonstration policy", citation=SYNTHETIC,
                                 source_class="DEMO_CONFIGURABLE")
        session.add(source)
        session.flush()

    policies: dict[str, PolicyVersion] = {}
    specs = [
        ("31", "LAND_READINESS", "Land readiness demonstration gate", "NATIONAL_REFERENCE",
         {"minimum_possession_percent": 90, "required_evidence": ["handover_memorandum"]}),
        ("32", "PRICE_VARIATION", "Gujarat price variation demonstrator", "GUJARAT_VERIFIED",
         {"eligible_estimate_min": 2500000, "minimum_duration_months": 12, "first_12_months_eligible": False}),
        ("35", "QUALITY_ACCEPTANCE", "Quality acceptance demonstration rule", "DEMO_CONFIGURABLE",
         {"method": "mean_of_specified_plus_or_minus_ten_percent", "absolute_minimum_percent": 90}),
    ]
    for raw_id, code, name, source_class, expression in specs:
        policy = session.scalar(select(PolicyVersion).where(PolicyVersion.policy_code == code, PolicyVersion.version == 1))
        if not policy:
            policy = PolicyVersion(id=mvp_id(raw_id), policy_code=code, version=1, name=name,
                                   source_reference_id=source.id, source_class=source_class,
                                   expression=expression, effective_from=date(2026, 1, 1), active=True)
            session.add(policy)
            session.flush()
        policies[code] = policy

    gate = session.scalar(select(GateDefinition).where(GateDefinition.code == "LAND_READINESS"))
    if not gate:
        gate = GateDefinition(id=mvp_id("33"), code="LAND_READINESS", name="Land / right-of-way readiness",
                              applies_at="TENDER_PUBLICATION", blocking=True,
                              responsible_role="EXECUTIVE_ENGINEER", approver_role="SUPERINTENDING_ENGINEER",
                              policy_version_id=policies["LAND_READINESS"].id)
        session.add(gate)
        session.flush()

    _ensure_assignments(session, users, roles, units, company)
    return {"units": units, "roles": roles, "policies": policies, "gate": gate, "company": company, "source": source}


def _ensure_assignments(session: Session, users: dict[str, User], roles: dict[str, RoleDefinition],
                        units: dict[str, OrganisationUnit], company: ContractorCompany) -> None:
    """Grant every demo account a dated role assignment exactly once."""
    plan = [
        ("90", "manager@demo.local", "STATE_ADMIN", "VAD-BRD"),
        ("91", "engineer@demo.local", "EXECUTIVE_ENGINEER", "VAD-BRD"),
        ("92", "inspector@demo.local", "INSPECTOR", "VAD-BRD"),
        ("93", "contractor@demo.local", "CONTRACTOR", "VAD-BRD"),
        ("94", "chiefengineer@demo.local", "CHIEF_ENGINEER", "VAD-CIR"),
        ("95", "superintendent@demo.local", "SUPERINTENDING_ENGINEER", "VAD-CIR"),
        ("96", "quality@demo.local", "QUALITY_ENGINEER", "VAD-BRD"),
        ("97", "finance@demo.local", "FINANCE", "VAD-BRD"),
        ("98", "auditor@demo.local", "AUDITOR", "VAD-BRD"),
    ]
    existing = set(session.scalars(select(UserRoleAssignment.id)).all())
    for raw_id, email, role_code, unit_code in plan:
        user = users.get(email)
        if not user:
            continue
        assignment_id = mvp_id(raw_id)
        if assignment_id in existing:
            continue
        session.add(UserRoleAssignment(id=assignment_id, user_id=user.id, role_id=roles[role_code].id,
                                        organisation_unit_id=units[unit_code].id, effective_from=datetime.now(UTC)))
    if not session.scalar(select(CompanyUserMembership).limit(1)):
        session.add(CompanyUserMembership(id=mvp_id("99"), company_id=company.id, user_id=users["contractor@demo.local"].id))
    if not session.scalar(select(ContractorClassHistory).limit(1)):
        session.add(ContractorClassHistory(id=mvp_id("100"), company_id=company.id,
                                           class_code="SPECIAL_CATEGORY_I_BRIDGES", effective_from=date(2025, 1, 1),
                                           source_reference="Synthetic demo registration history"))
    session.flush()


def _seed_asset(session: Session, spec: dict, users: dict[str, User], ref: dict, slot: int) -> None:
    """Create one portfolio bridge and whichever lifecycle layers it has reached.

    Every asset owns a dedicated 100-ID block so no two assets can ever collide
    on a primary key, regardless of how many layers each one carries.
    """
    base = 1000 + slot * 100
    engineer = users["engineer@demo.local"]
    inspector = users["inspector@demo.local"]
    quality = users["quality@demo.local"]
    contractor = users["contractor@demo.local"]

    unit = ref["units"][DIVISION_CODE_BY_ID[spec["division"]]]
    asset_id = mvp_id(str(base))
    project_id = mvp_id(str(base + 1))

    asset = Asset(
        id=asset_id, asset_code=spec["code"], asset_type="BRIDGE", canonical_name=spec["name"],
        owner_unit_id=unit.id, lifecycle_state=spec["lifecycle"], service_state=spec["service"],
        condition_grade=spec.get("grade"), risk_flag="SERVICE_RESTRICTED" if spec["service"] == "RESTRICTED" else None,
        district=spec["district"], latitude=spec["lat"], longitude=spec["lng"],
    )
    profile = BridgeProfile(
        asset_id=asset_id, bridge_class=spec["bridge_class"], route_name=spec["route"],
        chainage_km=spec["chainage"], length_m=spec["length"], span_count=spec["spans"],
        commissioned_on=spec.get("commissioned_on"), naming_finalised_on=spec.get("naming_finalised_on"),
    )
    project = ProjectRecord(
        id=project_id, asset_id=asset_id, owner_unit_id=unit.id, project_type=spec["project_type"],
        title=spec["title"], state=spec["lifecycle"], estimate_amount=spec["estimate"], created_by_id=engineer.id,
    )
    session.add_all([asset, profile, project])
    session.flush()

    for offset, (report_type, reference, source_class) in enumerate(spec.get("reports", []), start=2):
        session.add(ProjectReport(id=mvp_id(str(base + offset)), project_id=project_id, report_type=report_type,
                                  status="SUBMITTED", reference=reference, source_class=source_class,
                                  prepared_by_id=engineer.id))
    for offset, (clearance_type, status_value, reference) in enumerate(spec.get("clearances", []), start=10):
        session.add(ClearanceRecord(id=mvp_id(str(base + offset)), project_id=project_id, clearance_type=clearance_type,
                                    status=status_value, reference=reference,
                                    source_class="NATIONAL_REFERENCE" if reference else "DEMO_CONFIGURABLE",
                                    recorded_by_id=engineer.id))
    session.flush()

    session.add(AssetComponent(id=mvp_id(str(base + 20)), asset_id=asset_id, component_type="DECK",
                               component_label="Deck and expansion joint"))

    if spec.get("gate"):
        status_value, explanation, missing = spec["gate"]
        session.add(GateEvaluation(id=mvp_id(str(base + 21)), gate_id=ref["gate"].id, project_id=project_id,
                                   asset_id=asset_id, status=status_value, explanation=explanation,
                                   missing_requirements=missing, evaluated_by_id=engineer.id))
    session.flush()

    tender = spec.get("tender")
    tender_id = None
    if tender:
        tender_status, number, cost = tender
        tender_id = mvp_id(str(base + 22))
        # B-1 is the default form because it is mandatory above the ceiling, and
        # the work-order date is recorded so the 120-day rule is evaluable.
        opened = tender_status != "DRAFT"
        session.add(TenderRecord(id=tender_id, project_id=project_id, tender_number=number, status=tender_status,
                                 estimated_cost=cost, invited_by_id=engineer.id, tender_form="B-1",
                                 opened_by_id=engineer.id if opened else None,
                                 opening_on=date(2026, 1, 20) if opened else None,
                                 work_order_issued_on=date(2026, 2, 15) if opened else None))
        session.flush()

    if spec.get("bid"):
        session.add(TenderBidRecord(id=mvp_id(str(base + 23)), tender_id=tender_id, company_id=ref["company"].id,
                                    technical_status="SUBMITTED", price_amount=spec["bid"][1], submitted_by_id=contractor.id))
        session.flush()

    contract = spec.get("contract")
    contract_id = None
    if contract:
        state, number, amount, appointed, _progress = contract
        contract_id = mvp_id(str(base + 24))
        # Physical progress and the completion date are recorded facts, not
        # derived ones. A completed contract carries a Completion Certificate
        # date because the 10-year defect liability period runs from it, and
        # retention is refunded 15 days after it -- so a completed contract
        # without one has no computable liability period at all.
        completion = appointed if state == "COMPLETED" else None
        session.add(ContractRecord(id=contract_id, project_id=project_id, tender_id=tender_id,
                                   company_id=ref["company"].id, contract_number=number, awarded_amount=amount,
                                   state=state, appointed_date=appointed, completion_date=completion,
                                   physical_progress=Decimal("100") if state == "COMPLETED" else Decimal(str(_progress))))
        session.flush()
        for offset, (name, planned, actual) in enumerate(spec.get("milestones", []), start=25):
            session.add(Milestone(id=mvp_id(str(base + offset)), contract_id=contract_id, name=name,
                                  planned_percent=planned, actual_percent=actual,
                                  status="COMPLETE" if actual >= planned else "IN_PROGRESS"))
        session.flush()

    if spec.get("quality"):
        test_type, specified, samples = spec["quality"]
        test_id = mvp_id(str(base + 31))
        session.add(QualityTest(id=test_id, contract_id=contract_id, test_type=test_type, specified_value=specified,
                                rule_policy_version_id=ref["policies"]["QUALITY_ACCEPTANCE"].id, status="EVALUATED"))
        for number, value in enumerate(samples, start=1):
            session.add(TestSample(id=mvp_id(str(base + 31 + number)), test_id=test_id, sample_number=number,
                                   measured_value=value, recorded_by_id=quality.id))
        mean = sum(samples) / len(samples)
        calculated = "PASS" if mean >= specified * Decimal("0.9") else "FAIL"
        session.add(TestEvaluation(id=mvp_id(str(base + 36)), test_id=test_id, calculated_status=calculated,
                                   calculation={"mean": str(mean), "specified": str(specified),
                                                "rule": "mean of specified value minus ten percent",
                                                "sample_count": len(samples)},
                                   reviewer_id=quality.id, reviewed_at=datetime.now(UTC)))
        session.flush()

    if spec.get("price_variation"):
        submitted, calculated_amount, reference = spec["price_variation"]
        session.add(PriceVariationClaim(id=mvp_id(str(base + 37)), contract_id=contract_id, submitted_amount=submitted,
                                        calculated_amount=calculated_amount,
                                        variance_amount=calculated_amount - submitted,
                                        status="UNDER_FINANCE_REVIEW",
                                        policy_version_id=ref["policies"]["PRICE_VARIATION"].id,
                                        explanation=f"{reference}: submitted claim preserved; calculated entitlement differs and awaits Divisional Accountant review."))
        session.flush()

    inspection = spec.get("inspection")
    defect = spec.get("defect")
    defect_closed = spec.get("defect_closed")
    if inspection or defect or defect_closed:
        inspection_id = mvp_id(str(base + 40)) if inspection else None
        if inspection:
            itype, grade, notes, _risk = inspection
            session.add(InspectionRecord(id=inspection_id, asset_id=asset_id, inspection_type=itype, grade=grade,
                                         submitted_by_id=inspector.id, notes=notes))
        session.flush()

        if defect:
            description, risk, defect_status, days = defect
            defect_id = mvp_id(str(base + 41))
            due = datetime.now(UTC).date() + timedelta(days=days)
            session.add(DefectRecord(id=defect_id, asset_id=asset_id, inspection_id=inspection_id,
                                     description=description, risk_level=risk, status=defect_status,
                                     owner_user_id=engineer.id, due_on=due))
            session.add(ATR(id=mvp_id(str(base + 42)), defect_id=defect_id, due_on=due, status="OPEN"))
            session.flush()
            work_order = spec.get("work_order")
            if work_order:
                decision, work_status, work_description = work_order
                work_id = mvp_id(str(base + 43))
                session.add(WorkOrderRecord(id=work_id, defect_id=defect_id, company_id=ref["company"].id,
                                            status=work_status, decision_type=decision, description=work_description,
                                            approved_by_id=engineer.id))
                session.flush()
                if work_status == "VERIFICATION_PENDING":
                    session.add(RectificationSubmission(id=mvp_id(str(base + 44)), work_id=work_id,
                                                       submitted_by_id=contractor.id,
                                                       notes="Rectification completed and submitted for independent verification."))
                    session.flush()

        if defect_closed:
            description, decision, defect_status = defect_closed
            closed_defect_id = mvp_id(str(base + 45))
            closed_work_id = mvp_id(str(base + 47))
            session.add(DefectRecord(id=closed_defect_id, asset_id=asset_id, status=defect_status,
                                     description=description, risk_level="ROUTINE", owner_user_id=engineer.id))
            session.add(ATR(id=mvp_id(str(base + 46)), defect_id=closed_defect_id,
                            due_on=datetime.now(UTC).date(), status="CLOSED",
                            response="Attended during the scheduled maintenance cycle."))
            session.add(WorkOrderRecord(id=closed_work_id, defect_id=closed_defect_id, company_id=ref["company"].id,
                                        status="VERIFIED", decision_type=decision,
                                        description="Routine maintenance executed and independently verified.",
                                        approved_by_id=engineer.id))
            session.add(WorkVerification(id=mvp_id(str(base + 48)), work_order_id=closed_work_id, verifier_id=inspector.id,
                                         decision="ACCEPTED", notes="Closed defect independently verified on site.",
                                         verified_at=datetime.now(UTC)))
            session.flush()

    events = [(base + 50, "ASSET", asset_id, "ASSET_CREATED",
               {"asset_code": spec["code"], "lifecycle_state": spec["lifecycle"]},
               f"Synthetic portfolio asset registered in {spec['lifecycle']}.")]
    if inspection:
        events.append((base + 51, "INSPECTION", mvp_id(str(base + 40)), "INSPECTION_SUBMITTED",
                       {"grade": inspection[1]}, inspection[2]))
    if spec.get("gate") and spec["gate"][0] == "FAILED":
        events.append((base + 52, "GATE_EVALUATION", mvp_id(str(base + 21)), "GATE_FAILED",
                       {"status": "FAILED"}, spec["gate"][1]))
    if contract:
        events.append((base + 53, "CONTRACT", mvp_id(str(base + 24)), "CONTRACT_AWARDED",
                       {"state": contract[0], "amount": str(contract[2])}, f"Contract {contract[1]} recorded."))
    if defect and spec.get("work_order"):
        events.append((base + 54, "WORK_ORDER", mvp_id(str(base + 43)), "WORK_ORDER_APPROVED",
                       {"decision_type": spec["work_order"][0]}, spec["work_order"][2]))
    for raw, entity_type, entity_id, event_type, value, reason in events:
        session.add(AuditEvent(id=mvp_id(str(raw)), asset_id=asset_id, entity_type=entity_type,
                               entity_id=entity_id, event_type=event_type, actor_id=engineer.id,
                               new_value=value, reason=reason))
    session.flush()


def seed_mvp_demo(session: Session) -> None:
    """Seed the synthetic portfolio. Additive, idempotent, and never destructive."""
    users = {user.email: user for user in session.scalars(select(User)).all()}
    if not users:
        return
    required = {"engineer@demo.local", "inspector@demo.local", "contractor@demo.local",
                "quality@demo.local", "finance@demo.local"}
    if not required.issubset(users):
        return

    ref = _ensure_reference_data(session, users)
    existing_codes = set(session.scalars(select(Asset.asset_code)).all())
    for slot, spec in enumerate(_portfolio()):
        if spec["code"] in existing_codes:
            continue
        _seed_asset(session, spec, users, ref, slot)
        existing_codes.add(spec["code"])
    session.commit()
