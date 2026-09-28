"""Lifecycle phase derivation and role-scoped visibility.

Two rules live here, and nowhere else in the codebase.

**1. A phase is derived from records, never read from a stored label.**
``Asset.lifecycle_state`` is a convenience column, not an authority.  The phase a
bridge is actually in is computed from what has genuinely happened to it: has a
contract been awarded, and has it been completed.  A stored label can disagree
with the records behind it -- a bridge can be labelled ``POST_COMPLETION``
without a contract ever having been awarded.  A derivation cannot.  This is what
makes "post-construction applies only to a bridge that was actually constructed"
a structural property of the system rather than a promise made in a demo.

It also means a bridge cannot be *teleported* between phases by writing to a
column.  Phase changes because a fact changed: a gate passed, a tender was
awarded, a contract completed.

**2. Visibility is applied in SQL, from the caller's role, before any row is
read.**  A role is not a filter the frontend applies after the fact.  If a
contractor's query never returns another company's pre-tender pricing, then no
client-side mistake can leak it.  Defence in depth: the endpoints re-check on
write, and the UI hides what the API would not return anyway.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from .mvp_models import (
    Asset,
    CompanyUserMembership,
    ContractRecord,
    ContractorCompany,
    DefectRecord,
    GateEvaluation,
    ProjectRecord,
    TenderRecord,
    WorkOrderRecord,
)

# --------------------------------------------------------------------------
# Phase vocabulary
# --------------------------------------------------------------------------

PHASE_PRE = "SANCTION_AND_CLEARANCE"
PHASE_BUILD = "EXECUTION"
PHASE_POST = "POST_COMPLETION"

PHASE_ORDER = (PHASE_PRE, PHASE_BUILD, PHASE_POST)

PHASE_LABELS = {
    PHASE_PRE: "Sanction & Clearance",
    PHASE_BUILD: "Execution",
    PHASE_POST: "Post-Completion",
}

PHASE_PURPOSE = {
    PHASE_PRE: "Propose the bridge, clear the land and statutory approvals, fix the estimate, and award the works.",
    PHASE_BUILD: "Build it: measure, test, certify quality, and settle the running account and price variation.",
    PHASE_POST: "Operate it: inspect, record defects, get them rectified, and run out the defect liability period.",
}

# A tender is only *awarded* once it has actually been awarded.
TENDER_AWARDED = frozenset({"AWARDED", "ACCEPTED"})
# A contract only finishes when it is recorded as finished.
CONTRACT_FINISHED = frozenset({"COMPLETED", "CLOSED"})


def readable(value: str | None) -> str:
    return (value or "").replace("_", " ").lower()


# --------------------------------------------------------------------------
# Phase derivation
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class PhaseFacts:
    """What phase a bridge is in, why, and what stops it advancing."""

    phase: str
    basis: str
    blockers: tuple[str, ...] = ()
    next_phase: str | None = None

    def as_dict(self) -> dict:
        return {
            "phase": self.phase,
            "phase_label": PHASE_LABELS[self.phase],
            "basis": self.basis,
            "next_phase": self.next_phase,
            "next_phase_label": PHASE_LABELS.get(self.next_phase) if self.next_phase else None,
            "blockers": list(self.blockers),
        }


def _derive(contract: ContractRecord | None, tender: TenderRecord | None, gate: GateEvaluation | None) -> PhaseFacts:
    # Post-construction requires a *completed contract*. Nothing else qualifies.
    if contract is not None and contract.state in CONTRACT_FINISHED:
        return PhaseFacts(
            phase=PHASE_POST,
            basis=f"Contract {contract.contract_number} is recorded as {readable(contract.state)}.",
        )

    # Under construction requires a contract, or at minimum an awarded tender
    # whose contract is being appointed.
    if contract is not None:
        blockers = [f"The contract is {readable(contract.state)}, not completed."]
        if gate is not None and gate.status != "PASSED":
            blockers.append("The tender-readiness gate is not in a passed state.")
        return PhaseFacts(
            phase=PHASE_BUILD,
            basis=f"Contract {contract.contract_number} was awarded; the bridge is being built.",
            blockers=tuple(blockers),
            next_phase=PHASE_POST,
        )

    if tender is not None and tender.status in TENDER_AWARDED:
        return PhaseFacts(
            phase=PHASE_BUILD,
            basis=f"Tender {tender.tender_number} is {readable(tender.status)} and the contract is being appointed.",
            blockers=("No contract has been recorded yet.",),
            next_phase=PHASE_POST,
        )

    # Pre-construction. Note that a *published* tender is still pre-construction:
    # a bridge cannot be under construction without somebody being bound to build
    # it.
    blockers: list[str] = []
    if gate is not None and gate.status != "PASSED":
        blockers.append("The tender-readiness gate has not passed.")
    if tender is None:
        blockers.append("No tender has been raised.")
    elif tender.status not in TENDER_AWARDED:
        blockers.append(f"The tender is {readable(tender.status)}, not awarded.")
    return PhaseFacts(
        phase=PHASE_PRE,
        basis="No contract has been awarded, so nothing has been constructed.",
        blockers=tuple(blockers),
        next_phase=PHASE_BUILD,
    )


def phase_facts(session: Session, asset_ids: list[str]) -> dict[str, PhaseFacts]:
    """Derive the phase of many bridges in three queries, not three-per-bridge."""
    ids = list(dict.fromkeys(asset_ids))
    if not ids:
        return {}

    projects = {
        project.asset_id: project
        for project in session.scalars(select(ProjectRecord).where(ProjectRecord.asset_id.in_(ids))).all()
    }
    project_ids = [project.id for project in projects.values()]

    tenders: dict[str, TenderRecord] = {}
    contracts: dict[str, ContractRecord] = {}
    if project_ids:
        tenders = {
            tender.project_id: tender
            for tender in session.scalars(select(TenderRecord).where(TenderRecord.project_id.in_(project_ids))).all()
        }
        contracts = {
            contract.project_id: contract
            for contract in session.scalars(select(ContractRecord).where(ContractRecord.project_id.in_(project_ids))).all()
        }

    # Most recent gate evaluation per bridge decides the blocking state.
    gates: dict[str, GateEvaluation] = {}
    for gate in session.scalars(
        select(GateEvaluation)
        .where(GateEvaluation.asset_id.in_(ids))
        .order_by(GateEvaluation.evaluated_at.desc())
    ).all():
        gates.setdefault(gate.asset_id, gate)

    facts: dict[str, PhaseFacts] = {}
    for asset_id in ids:
        project = projects.get(asset_id)
        facts[asset_id] = _derive(
            contracts.get(project.id) if project else None,
            tenders.get(project.id) if project else None,
            gates.get(asset_id),
        )
    return facts


# --------------------------------------------------------------------------
# Phase gating: which phases are open, and why the others are not
# --------------------------------------------------------------------------


def _closed_reason(phase: str, facts: PhaseFacts) -> str:
    if phase == PHASE_BUILD:
        return (
            "This bridge has not been awarded yet, so there is nothing under construction. "
            "Blockers: " + (" ".join(facts.blockers) if facts.blockers else "none recorded")
        )
    if phase == PHASE_POST and facts.phase == PHASE_PRE:
        return (
            "Nothing has been constructed, so this bridge has no defect liability period, "
            "no service life and no condition to inspect."
        )
    if phase == PHASE_POST:
        return "The contract is not completed, so the bridge is not yet open to traffic."
    return "This phase has not been reached by this bridge."


def phase_gates(facts: PhaseFacts) -> dict:
    """Open and closed phases, each with the reason stated.

    Nothing is hidden silently.  A closed phase says why it is closed, which is
    the difference between a coherent register and a confusing one.
    """
    current = PHASE_ORDER.index(facts.phase)
    gates: dict[str, dict] = {}
    for index, phase in enumerate(PHASE_ORDER):
        if index < current:
            gates[phase] = {
                "available": True,
                "open_now": False,
                "reason": "Earlier phase, shown as recorded history.",
            }
        elif index == current:
            gates[phase] = {
                "available": True,
                "open_now": True,
                "reason": f"This is where the bridge is now. {facts.basis}",
            }
        else:
            gates[phase] = {
                "available": False,
                "open_now": False,
                "reason": _closed_reason(phase, facts),
            }
    return gates


# --------------------------------------------------------------------------
# Role-scoped visibility
# --------------------------------------------------------------------------

# Engineers and auditors need the whole register to do their job.
SEE_ALL_ROLES = frozenset({"STATE_ADMIN", "CHIEF_ENGINEER", "SUPERINTENDING_ENGINEER", "EXECUTIVE_ENGINEER", "AUDITOR"})

# These roles only ever act on a bridge that physically exists -- one that has
# been awarded and is either being built or is in service. They have no business
# seeing a proposal that has not been tendered.
BUILT_ONLY_ROLES = frozenset({"INSPECTOR", "QUALITY_ENGINEER", "FINANCE"})

# A contractor sees three things and nothing else: a tender it is entitled to bid
# on, a bridge it is bound to build, and a defect it has been told to repair.
CONTRACTOR_ROLES = frozenset({"CONTRACTOR"})

VISIBILITY_RULES = {
    "engineers_and_auditors": "See the whole register: they must be able to compare a proposal against a bridge already in service.",
    "inspectors_quality_finance": "See only bridges that have been awarded, because their work acts on a physical structure.",
    "contractors": (
        "See only bridges with a published tender open for bidding, bridges where their own company holds a "
        "contract, and bridges where their own company holds a work order. They never see another company's "
        "bids or commercial position."
    ),
}

# The criteria are stated to the user, not just to the reader of this file.
# A register that silently omits an asset is indistinguishable from a broken
# one, which is the same failure mode D-016 fixed for the register and D-019
# fixed for authorization. Publishing the rule is what makes an absence
# explicable without revealing what is being withheld: a contractor is told
# that a tender becomes visible when the department publishes it, and is never
# told that a particular internal draft exists.
SCOPE_CRITERIA: dict[str, list[str]] = {
    "engineers_and_auditors": [
        "You see the whole register, so a proposal can be judged against a bridge already in service.",
    ],
    "inspectors_quality_finance": [
        "You see bridges that have been awarded, because your work acts on a physical structure.",
        "A bridge enters your scope the moment a contract is awarded, not when it is proposed.",
    ],
    "contractors": [
        "You see a bridge when its tender is open for bidding, when your own company holds the contract, or when your own company holds a work order against a defect.",
        "A tender stays internal to the department until it is published. Creating or drafting a tender does not expose it to bidders, and that is deliberate: a draft carries the department's commercial position before it is released.",
        "You never see another company's contract, work order, bid price or commercial position.",
    ],
}

# A tender notice is published by design -- nProcure makes it public -- so a
# contractor must be able to see a tender it has not yet won. What stays private
# is the *bids*: the notice is public, the tender room is not. Omitting this
# clause is what made the bid button unreachable, because a not-yet-won contract
# is by definition not in the contractor's scope.
OPEN_FOR_BID = "PUBLISHED"


def contractor_company_ids(session: Session, user_id: str) -> set[str]:
    return set(
        session.scalars(
            select(ContractorCompany.id)
            .join(CompanyUserMembership, CompanyUserMembership.company_id == ContractorCompany.id)
            .where(CompanyUserMembership.user_id == user_id)
        ).all()
    )


def visible_asset_ids(session: Session, roles: set[str], user_id: str) -> set[str] | None:
    """Asset ids this caller may see. ``None`` means unrestricted."""
    if roles & SEE_ALL_ROLES:
        return None

    visible: set[str] = set()

    if roles & CONTRACTOR_ROLES:
        # Open tenders: the notice is public, so the tender is visible to any
        # authenticated contractor. The bids on it are not.
        visible.update(
            session.scalars(
                select(ProjectRecord.asset_id)
                .join(TenderRecord, TenderRecord.project_id == ProjectRecord.id)
                .where(TenderRecord.status == OPEN_FOR_BID)
            ).all()
        )
        companies = contractor_company_ids(session, user_id)
        if companies:
            visible.update(
                session.scalars(
                    select(ProjectRecord.asset_id)
                    .join(ContractRecord, ContractRecord.project_id == ProjectRecord.id)
                    .where(ContractRecord.company_id.in_(companies))
                ).all()
            )
            visible.update(
                session.scalars(
                    select(DefectRecord.asset_id)
                    .join(WorkOrderRecord, WorkOrderRecord.defect_id == DefectRecord.id)
                    .where(WorkOrderRecord.company_id.in_(companies))
                ).all()
            )

    if roles & BUILT_ONLY_ROLES:
        visible.update(
            session.scalars(
                select(ProjectRecord.asset_id)
                .join(ContractRecord, ContractRecord.project_id == ProjectRecord.id)
            ).all()
        )

    return visible


def scope_asset_query(query: Select, session: Session, user, roles: set[str]) -> Select:
    """Apply role scoping to an ``Asset`` query in SQL, before any row is read."""
    allowed = visible_asset_ids(session, roles, user.id)
    if allowed is None:
        return query
    if not allowed:
        # Explicitly match nothing, rather than accidentally returning everything.
        return query.where(Asset.id.is_(None))
    return query.where(Asset.id.in_(allowed))


def may_see(session: Session, user, roles: set[str], asset_id: str) -> bool:
    allowed = visible_asset_ids(session, roles, user.id)
    return allowed is None or asset_id in allowed


def scope_explanation(roles: set[str]) -> str:
    """Plain-language reason for what this caller is allowed to see."""
    if roles & SEE_ALL_ROLES:
        return VISIBILITY_RULES["engineers_and_auditors"]
    if roles & CONTRACTOR_ROLES:
        return VISIBILITY_RULES["contractors"]
    return VISIBILITY_RULES["inspectors_quality_finance"]


def scope_criteria(roles: set[str]) -> list[str]:
    """The same rule, broken into the clauses a user can act on.

    Returned alongside the register so that an asset which is absent is
    explicable. Without this, a contractor who watches a new bridge not appear
    has no way to tell a deliberate access boundary from a defect, and the
    correct behaviour reads as the broken one.
    """
    if roles & SEE_ALL_ROLES:
        return list(SCOPE_CRITERIA["engineers_and_auditors"])
    if roles & CONTRACTOR_ROLES:
        return list(SCOPE_CRITERIA["contractors"])
    return list(SCOPE_CRITERIA["inspectors_quality_finance"])
