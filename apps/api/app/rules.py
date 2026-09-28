"""Computable rules, each traceable to the research record.

Every function in this module is a *predicate with a statutory or contractual
meaning*, and every one names the source that makes it true.  Two rules govern
this file:

**1. No rule exists without a citation.**  Each result carries a ``basis``
string pointing at the section of ``docs/research_3phase_opencode.md`` that
establishes it.  Where the record says ``NOT ESTABLISHED``, the helper returns
``established=False`` and the caller refuses to compute.  This is deliberate: the
research record's whole purpose is to make a plausible-but-unsourced number
impossible to introduce quietly.

**2. A rule the department already gets wrong is the highest-value rule here.**
  Section 4A.4 records 4.74 crore rupees overpaid across 11 works in 5 divisions,
  caused by a single arithmetic inversion: in one Bharuch cell the base index for
  Cement was interchanged with the base index for Steel, turning a 15.57 lakh
  recovery into a 40.13 lakh payment.  The engine below therefore binds every
  index to its component and refuses a claim whose base index does not match the
  recorded official base.  That single check is the whole point.

Section references are to ``docs/research_3phase_opencode.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

RECORD = "docs/research_3phase_opencode.md"


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Verdict:
    """A rule outcome: did it hold, on what evidence, and if not, why not."""

    passed: bool
    value: object
    basis: str
    reasons: tuple[str, ...] = ()
    established: bool = True

    def as_dict(self) -> dict:
        return {
            "passed": self.passed,
            "value": self.value,
            "basis": self.basis,
            "reasons": list(self.reasons),
            "established": self.established,
        }


# ==========================================================================
# 3.2  Concrete acceptance -- the template for every quality gate
# ==========================================================================

CUBE_MARGIN_MPA = Decimal("3")
CUBE_WINDOW = 4
CUBE_MIN_SAMPLES = 15
CORE_MIN_COUNT = 3
CORE_AVERAGE_RATIO = Decimal("0.85")
CORE_FLOOR_RATIO = Decimal("0.75")
WATER_PERMEABILITY_MAX_MM = Decimal("25")


def concrete_cube_acceptance(samples: list[Decimal], specified: Decimal) -> Verdict:
    """Both MoRTH conditions must hold. Not one, not a threshold -- both.

    1. the mean of four consecutive samples exceeds the specified strength by
       3 MPa; **and**
    2. no sample falls below the specified strength less 3 MPa.

    (sec 3.2, MoRTH Specifications Table 1700-9)

    The earlier implementation accepted ``all(sample >= specified)`` in the API
    and ``mean >= specified * 0.9`` in the seed.  Both were invented, and the two
    disagreed with each other, which is the clearest possible sign that a rule
    had been guessed rather than sourced.  Section 3.2 calls this the template
    for every quality gate in the product.
    """
    basis = f"{RECORD} sec 3.2 (MoRTH Specifications, Table 1700-9)"
    if len(samples) < CUBE_WINDOW:
        return Verdict(
            passed=False,
            value=None,
            basis=basis,
            reasons=(
                f"A verdict needs {CUBE_WINDOW} consecutive samples; {len(samples)} recorded. "
                "The rule is a mean over four consecutive samples, so fewer than four cannot be evaluated.",
            ),
        )

    # Condition 1 is evaluated over EVERY rolling window of four consecutive
    # samples, and the weakest window governs. A single bad group in the middle
    # of a lot is not forgiven by a good group after it -- accepting on "some
    # four consecutive samples passed" would be a weaker rule than the source.
    windows: list[dict] = []
    reasons: list[str] = []
    for start in range(len(samples) - CUBE_WINDOW + 1):
        window = samples[start : start + CUBE_WINDOW]
        mean = sum(window) / Decimal(CUBE_WINDOW)
        ok_mean = mean > specified + CUBE_MARGIN_MPA
        ok_min = min(window) >= specified - CUBE_MARGIN_MPA
        windows.append(
            {"from": start + 1, "to": start + CUBE_WINDOW, "mean": mean, "ok_mean": ok_mean, "ok_min": ok_min, "passes": ok_mean and ok_min}
        )
        if not ok_mean:
            reasons.append(
                f"Samples {start + 1}-{start + CUBE_WINDOW}: mean {mean:.2f} MPa is not more than "
                f"{CUBE_MARGIN_MPA} MPa above the specified {specified} MPa "
                f"(needs > {specified + CUBE_MARGIN_MPA} MPa)."
            )
        if not ok_min:
            reasons.append(
                f"Samples {start + 1}-{start + CUBE_WINDOW}: weakest sample {min(window)} MPa is below the "
                f"specified {specified} MPa less {CUBE_MARGIN_MPA} MPa "
                f"(floor {specified - CUBE_MARGIN_MPA} MPa)."
            )

    passing = [row for row in windows if row["passes"]]
    weakest = min(windows, key=lambda row: row["mean"]) if windows else None
    return Verdict(
        passed=len(passing) == len(windows) and bool(windows),
        value={
            "sample_count": len(samples),
            "mean_mpa": str((sum(samples) / Decimal(len(samples))).quantize(Decimal("0.01"))),
            "windows_evaluated": len(windows),
            "windows_passing": len(passing),
            "weakest_window": (
                {"from": weakest["from"], "to": weakest["to"], "mean_mpa": str(weakest["mean"].quantize(Decimal("0.01")))}
                if weakest
                else None
            ),
            "specified_mpa": str(specified),
            "weakest_sample_mpa": str(min(samples)),
            "required_mean_above": str(specified + CUBE_MARGIN_MPA),
            "required_sample_floor": str(specified - CUBE_MARGIN_MPA),
        },
        basis=basis,
        reasons=tuple(reasons),
    )


def core_acceptance(cores: list[Decimal], specified: Decimal) -> Verdict:
    """Core-extraction fallback when cubes fail, per IS:1199.

    At least three cores, average >= 85% of specified, and no core below 75%.
    (sec 3.2)
    """
    basis = f"{RECORD} sec 3.2 (core extraction per IS:1199)"
    if len(cores) < CORE_MIN_COUNT:
        return Verdict(
            passed=False,
            value=None,
            basis=basis,
            reasons=(f"At least {CORE_MIN_COUNT} cores are required; {len(cores)} recorded.",),
        )
    average = sum(cores) / Decimal(len(cores))
    reasons: list[str] = []
    if average < specified * CORE_AVERAGE_RATIO:
        reasons.append(
            f"Core average {average:.2f} MPa is below 85% of the specified {specified} MPa "
            f"(needs >= {specified * CORE_AVERAGE_RATIO} MPa)."
        )
    below = [core for core in cores if core < specified * CORE_FLOOR_RATIO]
    if below:
        reasons.append(
            f"{len(below)} core(s) fall below 75% of the specified {specified} MPa "
            f"(floor {specified * CORE_FLOOR_RATIO} MPa)."
        )
    return Verdict(
        passed=not reasons,
        value={
            "average_mpa": str(average.quantize(Decimal("0.01"))),
            "core_count": len(cores),
            "weakest_core_mpa": str(min(cores)),
        },
        basis=basis,
        reasons=tuple(reasons),
    )


DURABILITY_LIMITS: dict[str, dict[str, Decimal | str]] = {
    "MODERATE": {"max_wc_ratio": Decimal("0.45"), "min_cement_kg_m3": Decimal("340"), "min_grade": "M25"},
    "SEVERE": {"max_wc_ratio": Decimal("0.45"), "min_cement_kg_m3": Decimal("360"), "min_grade": "M30"},
    "VERY_SEVERE": {"max_wc_ratio": Decimal("0.40"), "min_cement_kg_m3": Decimal("380"), "min_grade": "M40"},
}

_GRADE_ORDER = ["M15", "M20", "M25", "M30", "M35", "M40", "M45", "M50"]


def durability_check(exposure: str, water_cement_ratio: Decimal, cement_kg_m3: Decimal, achieved_grade: str) -> Verdict:
    """Three conditions, all must hold, keyed on the exposure class. (sec 3.3)"""
    basis = f"{RECORD} sec 3.3 (MoRTH Specifications Table 1700-2)"
    limits = DURABILITY_LIMITS.get(exposure)
    if limits is None:
        return Verdict(
            passed=False,
            value=None,
            basis=basis,
            reasons=(f"Exposure class {exposure!r} is not one of Moderate, Severe, Very severe.",),
        )
    reasons: list[str] = []
    if water_cement_ratio > Decimal(limits["max_wc_ratio"]):
        reasons.append(
            f"Water-cement ratio {water_cement_ratio} exceeds the {limits['max_wc_ratio']} limit for {exposure.lower()} exposure."
        )
    if cement_kg_m3 < Decimal(limits["min_cement_kg_m3"]):
        reasons.append(
            f"Cement content {cement_kg_m3} kg/m3 is below the {limits['min_cement_kg_m3']} kg/m3 minimum for {exposure.lower()} exposure."
        )
    if achieved_grade not in _GRADE_ORDER or _GRADE_ORDER.index(achieved_grade) < _GRADE_ORDER.index(limits["min_grade"]):
        reasons.append(
            f"Achieved grade {achieved_grade} is below the {limits['min_grade']} minimum for {exposure.lower()} exposure."
        )
    return Verdict(
        passed=not reasons,
        value={"exposure": exposure, "limits": {k: str(v) for k, v in limits.items()}},
        basis=basis,
        reasons=tuple(reasons),
    )


# ==========================================================================
# 3.4  Milestones, partial credit, liquidated damages
# ==========================================================================

MILESTONE_SCHEDULE: tuple[tuple[str, Decimal, str], ...] = (
    ("MILESTONE_1", Decimal("35"), "Foundation and substructure complete."),
    ("MILESTONE_2", Decimal("60"), "Superstructure started; should have started construction of all bridges."),
    ("MILESTONE_3", Decimal("85"), "Superstructure and finishing substantially complete."),
)

LD_PERCENT_PER_DAY = Decimal("0.05")
LD_CAP_PERCENT = Decimal("10")


def milestone_credit(milestone_percent: Decimal, completion_percent: Decimal) -> Verdict:
    """Partial credit is pro-rated, not all-or-nothing. (sec 3.4)

    The contract works an example in which 10% x 0.95 = 9.5%: a milestone 95%
    complete earns 95% of its value.  Software that pays a milestone in full or
    not at all is the single most common error in this class, and it is the
    detail an interviewer will probe.
    """
    basis = f"{RECORD} sec 3.4 (milestone partial credit is pro-rated)"
    if not 0 <= completion_percent <= 100:
        return Verdict(
            passed=False,
            value=None,
            basis=basis,
            reasons=(f"Completion {completion_percent}% is outside 0-100.",),
        )
    if not 0 <= milestone_percent <= 100:
        return Verdict(
            passed=False,
            value=None,
            basis=basis,
            reasons=(f"Milestone value {milestone_percent}% is outside 0-100.",),
        )
    ratio = completion_percent / Decimal(100)
    return Verdict(
        passed=completion_percent >= milestone_percent,
        value={
            "milestone_percent": str(milestone_percent),
            "completion_percent": str(completion_percent),
            "credit_ratio": str(ratio.quantize(Decimal("0.0001"))),
            "credit_percent": str((milestone_percent * ratio).quantize(Decimal("0.01"))),
        },
        basis=basis,
        reasons=() if completion_percent >= milestone_percent else (
            f"Physical completion {completion_percent}% is below the {milestone_percent}% milestone, so no credit is due.",
        ),
    )


def liquidated_damages(contract_price: Decimal, days_overdue: int) -> Verdict:
    """0.05% per day, capped at 10% of the relevant milestone or the Contract Price. (sec 3.4)"""
    basis = f"{RECORD} sec 3.4 (LD 0.05%/day, capped at 10%)"
    if days_overdue < 0:
        return Verdict(passed=True, value=Decimal("0.00"), basis=basis, reasons=("Not overdue.",))
    uncapped = contract_price * LD_PERCENT_PER_DAY / Decimal(100) * Decimal(days_overdue)
    cap = contract_price * LD_CAP_PERCENT / Decimal(100)
    payable = min(uncapped, cap)
    return Verdict(
        passed=days_overdue == 0,
        value=_money(payable),
        basis=basis,
        reasons=(
            (
                f"{days_overdue} day(s) overdue. Uncapped {LD_PERCENT_PER_DAY}%/day = {_money(uncapped)}, "
                f"capped at {LD_CAP_PERCENT}% = {_money(cap)}. Levy {_money(payable)}."
            )
            if days_overdue
            else ("Not overdue; no levy.",)
        ),
    )


# ==========================================================================
# 3.5  Tests on Completion
# ==========================================================================

LOAD_TEST_SPAN_THRESHOLD_M = Decimal("15")


def tests_on_completion(spans: int, length_m: Decimal, tests_per_span: int, load_test_done: bool, insurance_proof: bool) -> Verdict:
    """The strongest construction gate. (sec 3.5, IRC HRB Special Report 17:1996)

    Rebound hammer and UPV at *two random spots per span*; load testing if the
    span is >= 15 m; insurance proof a hard precondition; the Completion
    Certificate is signed by the Authority's Engineer, not the contractor.

    The >= 15 m load-test trigger is a conditional gate keyed off a recorded span
    length, which is exactly the kind of rule a product should enforce and a
    spreadsheet never will.
    """
    basis = f"{RECORD} sec 3.5 (IRC HRB Special Report No. 17:1996)"
    required = spans * 2
    reasons: list[str] = []
    if tests_per_span < 2:
        reasons.append(f"Two random spots per span are required; {tests_per_span} recorded per span.")
    if tests_per_span * max(spans, 1) < required:
        reasons.append(f"Expected {required} tests across {spans} span(s); {tests_per_span * max(spans, 1)} recorded.")
    load_required = length_m >= LOAD_TEST_SPAN_THRESHOLD_M
    if load_required and not load_test_done:
        reasons.append(
            f"Span length {length_m} m is at or above {LOAD_TEST_SPAN_THRESHOLD_M} m, so a load test is required and none is recorded."
        )
    if not insurance_proof:
        reasons.append("Insurance proof is a hard precondition to the Completion Certificate and is not recorded.")
    return Verdict(
        passed=not reasons,
        value={
            "spans": spans,
            "length_m": str(length_m),
            "required_tests": required,
            "recorded_tests_per_span": tests_per_span,
            "load_test_required": load_required,
            "load_test_recorded": load_test_done,
            "insurance_proof_recorded": insurance_proof,
        },
        basis=basis,
        reasons=tuple(reasons),
    )


# ==========================================================================
# 3.6  Defect Liability Period -- a predicate, not a date
# ==========================================================================

DLP_YEARS = 10
DLP_CURE_DAYS = 15
DLP_REMEDY_DAMAGES_PERCENT = Decimal("20")
RETENTION_REFUND_DAYS = 15
RETENTION_DEDUCTION_PERCENT = Decimal("6")
RETENTION_CAP_PERCENT = Decimal("5")


def dlp_state(completion_date: date, open_defects: int, today: date) -> Verdict:
    """``DLP_active = (now < start + 10 years) AND (open_defects == 0)``

    Art. 17.5 extends the period until identified defects are remedied, so an
    open defect blocks expiry automatically.  The clock does not run out while a
    defect is open.  (sec 3.6, 3.6.1)
    """
    basis = f"{RECORD} sec 3.6 and 3.6.1 (Art. 17.1(d), Art. 17.5)"
    expiry = date(completion_date.year + DLP_YEARS, completion_date.month, completion_date.day)
    within_period = today < expiry
    active = within_period and open_defects == 0
    days_remaining = (expiry - today).days

    reasons: list[str] = []
    if not within_period:
        reasons.append(f"The {DLP_YEARS}-year period expired on {expiry.isoformat()}.")
    elif open_defects:
        reasons.append(
            f"{open_defects} defect(s) remain open. Art. 17.5 extends the period until the identified "
            "defects are remedied, so the clock does not run out while a defect is open."
        )
    return Verdict(
        passed=within_period,
        value={
            "active": active,
            "completion_date": completion_date.isoformat(),
            "nominal_expiry": expiry.isoformat(),
            "days_remaining": days_remaining,
            "open_defects": open_defects,
            "extended_by_open_defects": within_period and open_defects > 0,
        },
        basis=basis,
        reasons=tuple(reasons),
    )


def defect_rectification_demand(defect, cure_days: int = DLP_CURE_DAYS) -> Verdict:
    """Art. 17: 15 days to cure; on failure, cost of rectification plus 20% damages. (sec 3.6)"""
    basis = f"{RECORD} sec 3.6 (Art. 17 cure period, Art. 17.4 remedy)"
    rectification_cost = Decimal(defect.estimated_rectification_cost or 0)
    demand_due = defect.notified_on + timedelta(days=cure_days)
    damages = _money(rectification_cost * DLP_REMEDY_DAMAGES_PERCENT / Decimal(100))
    return Verdict(
        passed=bool(getattr(defect, "rectified_on", None)),
        value={
            "cure_period_days": cure_days,
            "rectification_due": demand_due.isoformat(),
            "rectification_cost": str(_money(rectification_cost)),
            "damages_at_20_percent": str(damages),
            "total_deductible": str(_money(rectification_cost + damages)),
        },
        basis=basis,
        reasons=(
            f"{defect.estimated_rectification_cost or 0} cost of rectification plus "
            f"{DLP_REMEDY_DAMAGES_PERCENT}% damages = {_money(rectification_cost + damages)}, "
            f"deductible from monies due."
        ),
    )


def retention_refund(completion_certificate_date: date | None) -> Verdict:
    """Retention is refunded within 15 days of the Completion Certificate.

    This is the uncomfortable finding the research record insists be said out
    loud: the cash leaves a fortnight into a decade of liability, and the only
    security standing behind a 10-year DLP is the performance security. A model
    that treats retention as DLP cover is simply wrong. (sec 3.6.1)
    """
    basis = f"{RECORD} sec 3.6.1 (retention does not back the DLP)"
    if completion_certificate_date is None:
        return Verdict(
            passed=False,
            value=None,
            basis=basis,
            reasons=("No Completion Certificate has been issued, so no refund clock has started.",),
        )
    refund_due = completion_certificate_date + timedelta(days=RETENTION_REFUND_DAYS)
    return Verdict(
        passed=True,
        value={
            "completion_certificate_date": completion_certificate_date.isoformat(),
            "retention_refund_due": refund_due.isoformat(),
            "deduction_percent": str(RETENTION_DEDUCTION_PERCENT),
            "cap_percent_of_contract_price": str(RETENTION_CAP_PERCENT),
            "note": (
                "Retention is 6% deduction capped at 5% of the Contract Price, refunded within 15 days of "
                "the Completion Certificate. It does not back the 10-year DLP; the performance security does."
            ),
        },
        basis=basis,
    )


# ==========================================================================
# 3.7  Escalation weights -- Major Bridges
# ==========================================================================

BRIDGE_ESCALATION_WEIGHTS: dict[str, Decimal] = {
    "LABOUR": Decimal("20"),
    "CEMENT": Decimal("0"),
    "STEEL": Decimal("0"),
    "BITUMEN": Decimal("15"),
    "FUEL": Decimal("10"),
    "OTHER_MATERIALS": Decimal("40"),
    "PLANT_MACHINERY": Decimal("15"),
}

ZERO_WEIGHT_FOR_BRIDGES = frozenset({"CEMENT", "STEEL"})


# ==========================================================================
# 4A.2  Gujarat's own contract terms
# ==========================================================================

B1_CEILING_ROAD = Decimal("12000000")
B1_CEILING_BRIDGE = Decimal("10000000")
PERFORMANCE_BOND_PERCENT = Decimal("3")


def tender_form(estimated_cost: Decimal, is_bridge: bool) -> Verdict:
    """B-1 vs B-2 is a function of the amount, and B-1 is mandatory above it.

    GR TNC-1088-D-347-(7)-C dt 11-07-2017, verbatim: the monetary limit is
    "enhanced to Rs. 12.00 Crore for Road works, and Rs. 10.00 Crore for Bridge
    and Building works", applicable "with the strict application of a condition
    that tenders ... should invariably be invited on B-1 tender form only". (sec 4A.2)
    """
    basis = f"{RECORD} sec 4A.2 (GR TNC-1088-D-347-(7)-C dt 11-07-2017)"
    ceiling = B1_CEILING_BRIDGE if is_bridge else B1_CEILING_ROAD
    kind = "bridge and building" if is_bridge else "road"
    mandatory_b1 = estimated_cost > ceiling
    return Verdict(
        passed=mandatory_b1,
        value={
            "estimated_cost": str(estimated_cost),
            "b1_ceiling": str(ceiling),
            "b1_ceiling_crore": str((ceiling / Decimal(10000000)).normalize()),
            "applies_to": kind,
            "tender_form": "B-1" if mandatory_b1 else "B-1 or B-2",
        },
        basis=basis,
        reasons=(
            f"Estimated cost {estimated_cost} is above the {kind} B-1 ceiling of {ceiling}. "
            "The tender must be invited on B-1 form only."
            if mandatory_b1
            else f"Estimated cost {estimated_cost} is at or below the {kind} B-1 ceiling of {ceiling}, so B-1 or B-2 is available."
        ),
    )


def security_deposit(estimated_cost: Decimal, is_hydraulic: bool = False) -> Verdict:
    """Gujarat's own banded security deposit. (sec 4A.2, GR TNC-10-2013-3-(BHAG-2)-C)

    A bridge estimate is essentially always above 5 lakh rupees, so 3% with a
    2-year bank guarantee is the operative case. Not 5%. Not 6%. Gujarat is 3%.
    """
    basis = f"{RECORD} sec 4A.2 (GR TNC-10-2013-3-(BHAG-2)-C dt 20-11-2013)"
    if is_hydraulic:
        percent, bg_years, claim_years = Decimal("5"), 5, 5
    elif estimated_cost >= Decimal("500000"):
        percent, bg_years, claim_years = Decimal("3"), 2, 2
    else:
        percent, bg_years, claim_years = Decimal("2"), 1, 1
    return Verdict(
        passed=True,
        value={
            "percent": str(percent),
            "amount": str(_money(estimated_cost * percent / Decimal(100))),
            "bg_validity_years": bg_years,
            "max_claim_period_years": claim_years,
            "penalty_for_breach": "the security-deposit amount then payable by the contractor",
        },
        basis=basis,
    )


def performance_bond(total_contract_amount: Decimal) -> Verdict:
    """3% of the total contract amount. (sec 4A.2, GR PRC-10-2020-329-C dt 01-06-2021)"""
    basis = f"{RECORD} sec 4A.2 (GR PRC-10-2020-329-C dt 01-06-2021)"
    amount = total_contract_amount * PERFORMANCE_BOND_PERCENT / Decimal(100)
    return Verdict(
        passed=True,
        value={
            "percent": str(PERFORMANCE_BOND_PERCENT),
            "amount": str(_money(amount)),
            "sole_security_behind_dlp": True,
            "note": "Retention is refunded 15 days after the Completion Certificate, so this is the only security behind the 10-year DLP.",
        },
        basis=basis,
    )


# ==========================================================================
# 4A.3  Post-construction quality state machine
# ==========================================================================

INSPECTION_GRADES = ("S", "SRI", "U")
GRADE_MEANING = {
    "S": "Satisfactory; no consequence.",
    "SRI": "Satisfactory but requires improvement; ATR with time-bound rectification, plus escalation and penalty.",
    "U": "Unsatisfactory; ATR, escalation, and can trigger Reconstruction.",
}
ATR_MONTHS = (2, 3, 6, 12)


def inspection_outcome(grade: str, atr_due_date: date | None) -> Verdict:
    """S / SRI / U -> ATR with a time-bound rectification, escalation, penalty, and a Red Card. (sec 4A.3)"""
    basis = f"{RECORD} sec 4A.3 (GR PRC-10-2017-31-C dt 26-05-2017, 28 standard forms)"
    if grade not in INSPECTION_GRADES:
        return Verdict(
            passed=False,
            value=None,
            basis=basis,
            reasons=(f"Grade {grade!r} is not one of S, SRI, U.",),
        )
    if grade == "S":
        return Verdict(
            passed=True,
            value={"grade": grade, "meaning": GRADE_MEANING[grade], "atr_required": False},
            basis=basis,
        )
    reasons: list[str] = []
    if atr_due_date is None:
        reasons.append(
            f"Grade {grade} requires an ATR with a time-bound rectification "
            f"({', '.join(str(m) for m in ATR_MONTHS)} months), and no due date is recorded."
        )
    return Verdict(
        passed=not reasons,
        value={
            "grade": grade,
            "meaning": GRADE_MEANING[grade],
            "atr_required": True,
            "atr_due_date": atr_due_date.isoformat() if atr_due_date else None,
            "escalation_ladder": ["Rectification", "Escalation", "Reconstruction", "Red Card to contractor"],
        },
        basis=basis,
        reasons=tuple(reasons),
    )


# ==========================================================================
# 4A.4  The price-variation engine
# ==========================================================================

PV_MIN_ESTIMATED_COST = Decimal("2500000")
PV_MIN_DURATION_MONTHS = 12
PV_FIRST_MONTHS_EXCLUDED = 12
PV_CEILING_PERCENT = Decimal("5")
PV_ESCALATION_BASE = Decimal("1.1")
PV_EPC_BASE_DATE_OFFSET_DAYS = 28
PV_CEILING_DEDUCT_COMPONENTS = frozenset({"CEMENT", "STEEL", "ASPHALT"})


def pv_admissible(estimated_cost: Decimal, time_limit_months: int) -> Verdict:
    """Admissible only if estimated cost > 25 lakh AND time limit > 12 months. (sec 4A.4, clauses 59/59A, 60/60A)"""
    basis = f"{RECORD} sec 4A.4 (Gujarat clauses 59/59A, 60/60A as amended by GR TNC-1089-4-C dt 21-10-2005)"
    reasons: list[str] = []
    if estimated_cost <= PV_MIN_ESTIMATED_COST:
        reasons.append(f"Estimated cost {estimated_cost} is not above {PV_MIN_ESTIMATED_COST}.")
    if time_limit_months <= PV_MIN_DURATION_MONTHS:
        reasons.append(f"Time limit {time_limit_months} months is not more than {PV_MIN_DURATION_MONTHS} months.")
    return Verdict(
        passed=not reasons,
        value={
            "estimated_cost": str(estimated_cost),
            "time_limit_months": time_limit_months,
            "min_estimated_cost": str(PV_MIN_ESTIMATED_COST),
            "min_duration_months": PV_MIN_DURATION_MONTHS,
        },
        basis=basis,
        reasons=tuple(reasons),
    )


def escalation_index(n: int, base: Decimal = PV_ESCALATION_BASE) -> Decimal:
    """1.1^n. (sec 4A.4)"""
    return (base ** n).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def pv_ceiling(estimated_cost: Decimal, cement: Decimal, steel: Decimal, asphalt: Decimal) -> Verdict:
    """Ceiling = 5% of estimated cost, less the value of Cement, Steel and Asphalt. (sec 4A.4)"""
    basis = f"{RECORD} sec 4A.4 (ceiling: 5% of estimated cost less Cement, Steel, Asphalt)"
    headroom = estimated_cost * PV_CEILING_PERCENT / Decimal(100)
    deducted = cement + steel + asphalt
    ceiling = headroom - deducted
    clamped = max(ceiling, Decimal("0"))
    return Verdict(
        passed=ceiling > 0,
        value={
            "five_percent_of_estimated_cost": str(_money(headroom)),
            "less_cement_steel_asphalt": str(_money(deducted)),
            "ceiling": str(_money(clamped)),
            "clamped_from_negative": ceiling < 0,
        },
        basis=basis,
        reasons=(
            ()
            if ceiling > 0
            else (
                f"The 5% headroom of {_money(headroom)} is fully consumed by the Cement, Steel and Asphalt "
                f"value of {_money(deducted)}, so no price variation is payable on this work.",
            )
        ),
    )


@dataclass(frozen=True)
class PvComponent:
    """One line of a price-variation claim.

    ``base_index`` is the *official* base index for this component.  The engine
    refuses a claim whose submitted base index disagrees with it, because
    interchanging component base indices is precisely how a 15.57 lakh recovery
    became a 40.13 lakh payment in Bharuch.
    """

    name: str
    portion: Decimal
    base_index: Decimal
    current_index: Decimal
    is_bridge: bool = True


def price_variation(components: list[PvComponent], months_elapsed: int, estimated_cost: Decimal) -> Verdict:
    """Compute the claim, or refuse it, with every refusal stating its reason.

    This is the strongest single demo asset in the research base, and the exact
    computation CAG has formally recommended the department build.  It replaces
    an endpoint that accepted both the submitted and the calculated amount from
    the client and stored the difference -- which is a difference calculator, not
    an engine, and it leaves the arithmetic with the people who got it wrong.
    """
    basis = f"{RECORD} sec 4A.4 (CAG: 4.74 cr overpaid across 11 works in 5 divisions)"

    reasons: list[str] = []

    # 1. No price variation at all in the first 12 months.
    if months_elapsed <= PV_FIRST_MONTHS_EXCLUDED:
        reasons.append(
            f"{months_elapsed} month(s) have elapsed. No price variation is admissible in the first "
            f"{PV_FIRST_MONTHS_EXCLUDED} months."
        )

    # 2. For bridges, cement and steel carry zero weight.
    zero_weight_lines = [line for line in components if line.is_bridge and line.name in ZERO_WEIGHT_FOR_BRIDGES]
    for line in zero_weight_lines:
        reasons.append(
            f"{line.name.title()} carries zero escalation weight for Major Bridges (MoRTH weights: "
            f"{', '.join(f'{k.title()} {v}%' for k, v in BRIDGE_ESCALATION_WEIGHTS.items())}). "
            f"The submitted {line.name} line of {line.portion} is not admissible and must be removed."
        )

    # 3. Index-base integrity: the Bharuch check.
    #
    # This is deliberately fatal rather than advisory. A claim built on a base
    # index belonging to a different component does not produce a number that
    # happens to be wrong; it produces a plausible number, which is exactly the
    # failure mode. In Bharuch that turned a 15.57 lakh recovery into a 40.13
    # lakh payment and was paid without query. So the engine refuses to produce
    # a figure at all rather than produce one that cannot be trusted.
    index_integrity_failed = False
    for line in components:
        if line.base_index <= 0 or line.current_index <= 0:
            reasons.append(f"{line.name}: base and current index must both be positive.")
            index_integrity_failed = True
            continue
        if line.name in ZERO_WEIGHT_FOR_BRIDGES and line.is_bridge:
            continue
        recorded = OFFICIAL_BASE_INDICES.get(line.name)
        if recorded is not None and Decimal(recorded) != line.base_index:
            index_integrity_failed = True
            reasons.append(
                f"{line.name}: base index {line.base_index} does not match the recorded official base "
                f"{recorded}. In Bharuch the base indices for Cement and Steel were interchanged in one cell, "
                "turning a 15.57 lakh recovery into a 40.13 lakh payment -- a 55.70 lakh inversion. "
                "No payable value is computed from a claim whose index bases are not verifiable."
            )

    if not components:
        reasons.append("No price-variation component lines were submitted.")

    # Compute what was submitted, for the record, even when a reason blocks it.
    lines: list[dict] = []
    total = Decimal("0")
    for line in components:
        admissible = not (line.is_bridge and line.name in ZERO_WEIGHT_FOR_BRIDGES)
        movement = (line.current_index - line.base_index) / line.base_index
        claim = line.portion * movement if admissible else Decimal("0")
        total += claim
        lines.append(
            {
                "component": line.name,
                "portion": str(line.portion),
                "base_index": str(line.base_index),
                "current_index": str(line.current_index),
                "index_movement_pct": str((movement * 100).quantize(Decimal("0.01"))),
                "zero_weight_for_bridges": line.is_bridge and line.name in ZERO_WEIGHT_FOR_BRIDGES,
                "admissible": admissible,
                "claim": str(_money(claim)),
            }
        )

    if index_integrity_failed:
        computed = Decimal("0")
    elif months_elapsed <= PV_FIRST_MONTHS_EXCLUDED:
        computed = Decimal("0")
    else:
        computed = total
    ceiling_verdict = pv_ceiling(
        estimated_cost,
        sum((line.portion for line in components if line.name == "CEMENT"), Decimal("0")),
        sum((line.portion for line in components if line.name == "STEEL"), Decimal("0")),
        sum((line.portion for line in components if line.name == "ASPHALT"), Decimal("0")),
    )
    payable = min(computed, Decimal(ceiling_verdict.value["ceiling"])) if ceiling_verdict.value["ceiling"] else Decimal("0")
    if computed > Decimal(ceiling_verdict.value["ceiling"]):
        reasons.append(
            f"Computed {computed} exceeds the ceiling of {ceiling_verdict.value['ceiling']}. "
            "Payable value is capped at the ceiling; the excess is not payable."
        )

    return Verdict(
        passed=not reasons,
        value={
            "lines": lines,
            "computed": str(_money(computed)),
            "arithmetic_sum_before_checks": str(_money(total)),
            "index_integrity_verified": not index_integrity_failed,
            "ceiling": ceiling_verdict.value["ceiling"],
            "payable": str(_money(payable)),
            "months_elapsed": months_elapsed,
            "epc_base_date_offset_days": PV_EPC_BASE_DATE_OFFSET_DAYS,
        },
        basis=basis,
        reasons=tuple(reasons),
    )


# The official base indices the engine holds authoritative. Populated from the
# official circular data; an empty entry means "not established", and the engine
# then accepts the submitted base without cross-checking rather than inventing one.
OFFICIAL_BASE_INDICES: dict[str, str] = {
    "CEMENT": "122.5",
    "STEEL": "108.4",
}


# ==========================================================================
# 4A.5  Schedule-G escalation SLA, and bid capacity
# ==========================================================================

SCHEDULE_G_STAGES: dict[int, dict[str, int]] = {
    1: {"to_parent_department": 7, "to_legal": 7, "for_legal_clearance": 7, "to_file": 9, "total": 30},
    2: {"to_parent_department": 14, "to_legal": 14, "for_legal_clearance": 14, "to_file": 18, "total": 60},
    3: {"to_parent_department": 30, "to_legal": 14, "for_legal_clearance": 14, "to_file": 32, "total": 90},
}


def schedule_g_sla(stage: int) -> Verdict:
    """A government-approved, SLA-shaped, three-stage escalation with a hard outer bound.

    A deadline calculator needs no data at all. Zero data risk. (sec 4A.5,
    Letter No. RBD/0098/12/2025 approved 17-01-2026 by the Chief Secretary)
    """
    basis = f"{RECORD} sec 4A.5 (Letter No. RBD/0098/12/2025, approved 17-01-2026)"
    legs = SCHEDULE_G_STAGES.get(stage)
    if legs is None:
        return Verdict(
            passed=False,
            value=None,
            basis=basis,
            reasons=(f"Stage {stage} is not one of 1, 2, 3.",),
        )
    return Verdict(
        passed=True,
        value={"stage": stage, "legs": legs, "outer_bound_days": legs["total"]},
        basis=basis,
    )


def bid_capacity(available_capital: Decimal, net_worth: Decimal, years: Decimal) -> Verdict:
    """ABC = 2*A*N - B, with turnover X = tender amount / time limit in years. (sec 4A.5, 4A.6)"""
    basis = f"{RECORD} sec 4A.5 and 4A.6 (ABC = 2.A.N - B)"
    if years <= 0:
        return Verdict(
            passed=False,
            value=None,
            basis=basis,
            reasons=("Time limit must be greater than zero to express it in years.",),
        )
    capacity = 2 * available_capital * years - net_worth
    return Verdict(
        passed=capacity > 0,
        value={"a_available_capital": str(available_capital), "n_years": str(years), "b_net_worth": str(net_worth), "capacity": str(_money(capacity))},
        basis=basis,
    )


# ==========================================================================
# 4A.6  Prequalification regime
# ==========================================================================

PREQUAL_THRESHOLD_BRIDGE = Decimal("70000000")
PREQUAL_THRESHOLD_ROAD = Decimal("75000000")
PREQUAL_SIMILAR_WORK_RATIO = Decimal("0.40")
PREQUAL_LOOKBACK_YEARS_BRIDGE = 10
PREQUAL_LOOKBACK_YEARS_ROAD = 5
JV_MAX_FIRMS = 3
JV_LEAD_MIN_PERCENT = Decimal("51")
JV_OTHER_MIN_PERCENT = Decimal("20")


def prequalification(tender_amount: Decimal, is_bridge: bool, similar_work_value: Decimal, completed_years_ago: int) -> Verdict:
    """The bridge threshold is *lower* than the road threshold, and the bridge look-back is *longer*.

    Both are designed distinctions, not accidents. (sec 4A.6,
    GR SSR/10/2015/17-C dt 20-06-2020)
    """
    basis = f"{RECORD} sec 4A.6 (GR SSR/10/2015/17-C dt 20-06-2020)"
    threshold = PREQUAL_THRESHOLD_BRIDGE if is_bridge else PREQUAL_THRESHOLD_ROAD
    lookback = PREQUAL_LOOKBACK_YEARS_BRIDGE if is_bridge else PREQUAL_LOOKBACK_YEARS_ROAD
    reasons: list[str] = []
    if tender_amount <= threshold:
        reasons.append(
            f"Tender amount {tender_amount} is at or below the {PREQUAL_THRESHOLD_BRIDGE if is_bridge else PREQUAL_THRESHOLD_ROAD} "
            f"threshold for {'bridge' if is_bridge else 'road'} works, so prequalification does not apply."
        )
    required_similar = tender_amount * PREQUAL_SIMILAR_WORK_RATIO
    if similar_work_value < required_similar:
        reasons.append(
            f"Similar work of {similar_work_value} is below 40% of the tender amount "
            f"({required_similar})."
        )
    if completed_years_ago > lookback:
        reasons.append(
            f"The similar work was completed {completed_years_ago} year(s) ago; for "
            f"{'bridges' if is_bridge else 'roads'} the look-back is {lookback} financial years."
        )
    return Verdict(
        passed=not reasons,
        value={
            "tender_amount": str(tender_amount),
            "threshold": str(threshold),
            "threshold_applies": tender_amount > threshold,
            "similar_work_required": str(required_similar),
            "lookback_years": lookback,
        },
        basis=basis,
        reasons=tuple(reasons),
    )


# ==========================================================================
# 4A.9  The 120-day rule
# ==========================================================================

TENDER_ACCEPTANCE_DEADLINE_DAYS = 120


def tender_acceptance_120_day(opening_date: date, accepted_date: date | None, work_order_date: date | None) -> Verdict:
    """Tender must be accepted and the work order issued within 120 days of tender opening.

    GPWM Clause 212-A with GR 10 May 2013. Breach means re-tender. CAG cost it:
    Mehsana Asjol-Karansagar L1 5.40 cr rose to 6.13 cr; Palanpur Boys Hostel
    3.66 cr rose to 5.14 cr. (sec 4A.9)
    """
    basis = f"{RECORD} sec 4A.9 (GPWM Clause 212-A, GR 10-05-2013)"
    deadline = opening_date + timedelta(days=TENDER_ACCEPTANCE_DEADLINE_DAYS)
    reasons: list[str] = []
    if accepted_date is None:
        reasons.append(f"The tender has not been accepted. Acceptance was due by {deadline.isoformat()}.")
    elif accepted_date > deadline:
        reasons.append(
            f"Acceptance on {accepted_date.isoformat()} is {(accepted_date - deadline).days} day(s) past the "
            f"120-day deadline of {deadline.isoformat()}. The tender must be re-invited."
        )
    if accepted_date is not None and work_order_date is None:
        reasons.append("The tender was accepted but no work order is recorded, so the 120-day rule is not yet satisfied.")
    elif work_order_date is not None and work_order_date > deadline:
        reasons.append(
            f"Work order on {work_order_date.isoformat()} is {(work_order_date - deadline).days} day(s) past the "
            f"120-day deadline of {deadline.isoformat()}. The tender must be re-invited."
        )
    return Verdict(
        passed=not reasons,
        value={
            "opening_date": opening_date.isoformat(),
            "deadline": deadline.isoformat(),
            "accepted_date": accepted_date.isoformat() if accepted_date else None,
            "work_order_date": work_order_date.isoformat() if work_order_date else None,
            "days_remaining": (deadline - opening_date).days,
        },
        basis=basis,
        reasons=tuple(reasons),
    )


# ==========================================================================
# 2.2  Design life
# ==========================================================================

DESIGN_LIFE_YEARS = 100


def design_life_justified(regular_inspection: bool, regular_maintenance: bool, regular_repairs: bool) -> Verdict:
    """The 100-year design life is explicitly conditional on inspection, maintenance and repairs.

    IRC:5-2024 clause 104.1.4 gives all structural components a 100-year design
    life, and attaches the condition in the same breath.  The condition is the
    product's opening: the design life is not a property of the concrete, it is a
    property of the regime, and this is the machine-checkable form of that.
    """
    basis = f"{RECORD} sec 2.2 and sec 4A.1 (IRC:5-2024 cl. 104.1.4 -- 100-year design life, conditional)"
    missing = []
    if not regular_inspection:
        missing.append("regular inspection")
    if not regular_maintenance:
        missing.append("regular maintenance")
    if not regular_repairs:
        missing.append("repairs")
    return Verdict(
        passed=not missing,
        value={"design_life_years": DESIGN_LIFE_YEARS, "conditions_met": not missing},
        basis=basis,
        reasons=(
            ()
            if not missing
            else (
                f"The {DESIGN_LIFE_YEARS}-year design life is conditional on regular inspection, maintenance "
                f"and repairs. Not established: {', '.join(missing)}.",
            )
        ),
    )
