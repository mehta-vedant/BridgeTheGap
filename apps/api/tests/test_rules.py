"""Tests for the sourced rules.

Each test names the rule it defends and the record section that establishes it.
If a test is deleted the corresponding claim is no longer being defended, so a
deletion should be a deliberate act with a note, not a tidy-up.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from app import rules

# ---------------------------------------------------------------------------
# sec 3.2  concrete acceptance -- the two-condition rule
# ---------------------------------------------------------------------------


def test_cube_acceptance_requires_both_conditions():
    """A high mean alone is not enough; a single weak sample fails it."""
    specified = Decimal("30")

    # Mean is 33.75 (> 33 required) but one sample is 26, below the 27 floor.
    verdict = rules.concrete_cube_acceptance([Decimal("26"), Decimal("35"), Decimal("35"), Decimal("39")], specified)
    assert not verdict.passed
    assert any("weakest sample" in reason for reason in verdict.reasons)


def test_cube_acceptance_passes_only_when_both_hold():
    verdict = rules.concrete_cube_acceptance([Decimal("27"), Decimal("34"), Decimal("35"), Decimal("39")], Decimal("30"))
    assert verdict.passed
    assert verdict.reasons == ()


def test_cube_acceptance_needs_four_samples():
    verdict = rules.concrete_cube_acceptance([Decimal("40"), Decimal("40"), Decimal("40")], Decimal("30"))
    assert not verdict.passed
    assert "4 consecutive samples" in verdict.reasons[0]


def test_cube_acceptance_checks_every_window_not_just_the_last():
    """Four consecutive samples is a rolling window, so an early failure is not forgiven."""
    samples = [Decimal("20"), Decimal("20"), Decimal("20"), Decimal("20"), Decimal("40"), Decimal("40"), Decimal("40"), Decimal("40")]
    verdict = rules.concrete_cube_acceptance(samples, Decimal("30"))
    assert not verdict.passed
    # Four of the five rolling windows fail; only the final one passes.
    assert verdict.value["windows_evaluated"] == 5
    assert verdict.value["windows_passing"] == 1
    assert verdict.value["weakest_window"]["from"] == 1


def test_core_acceptance_fallback():
    specified = Decimal("30")
    assert rules.core_acceptance([Decimal("26"), Decimal("27"), Decimal("25.5")], specified).passed
    assert not rules.core_acceptance([Decimal("26"), Decimal("27"), Decimal("10")], specified).passed
    assert not rules.core_acceptance([Decimal("30")], specified).passed


def test_durability_is_a_three_way_and():
    assert rules.durability_check("SEVERE", Decimal("0.45"), Decimal("360"), "M30").passed
    # Ratio OK, cement OK, grade one step short.
    assert not rules.durability_check("SEVERE", Decimal("0.45"), Decimal("360"), "M25").passed
    assert not rules.durability_check("VERY_SEVERE", Decimal("0.45"), Decimal("380"), "M40").passed


# ---------------------------------------------------------------------------
# sec 3.4  partial credit is pro-rated, and LD is capped
# ---------------------------------------------------------------------------


def test_milestone_credit_is_prorated_not_all_or_nothing():
    """10% x 0.95 = 9.5% is the worked example in the contract."""
    verdict = rules.milestone_credit(Decimal("10"), Decimal("95"))
    assert verdict.passed
    assert verdict.value["credit_percent"] == "9.50"


def test_milestone_credit_denies_when_physical_completion_is_short():
    verdict = rules.milestone_credit(Decimal("35"), Decimal("20"))
    assert not verdict.passed
    assert verdict.value["credit_percent"] == "7.00"


def test_liquidated_damages_accumulate_then_cap_at_ten_percent():
    price = Decimal("10000000")
    cap = Decimal("1000000.00")  # 10% of 1 crore
    # 0.05% of 1 crore is 5,000 per day.
    assert rules.liquidated_damages(price, 10).value == Decimal("50000.00")
    # The cap binds at day 200 (200 x 5,000 = 1,000,000) and never moves again.
    assert rules.liquidated_damages(price, 200).value == cap
    assert rules.liquidated_damages(price, 5000).value == cap
    assert not rules.liquidated_damages(price, 1).passed


# ---------------------------------------------------------------------------
# sec 3.5  Tests on Completion
# ---------------------------------------------------------------------------


def test_load_test_is_triggered_by_a_recorded_span_length():
    """The >= 15 m trigger is a conditional gate keyed off a recorded span."""
    short_span = rules.tests_on_completion(spans=2, length_m=Decimal("12"), tests_per_span=2, load_test_done=False, insurance_proof=True)
    long_span = rules.tests_on_completion(spans=2, length_m=Decimal("15"), tests_per_span=2, load_test_done=False, insurance_proof=True)

    assert short_span.passed
    assert not long_span.passed
    assert any("load test" in reason for reason in long_span.reasons)


def test_tests_on_completion_requires_two_spots_per_span_and_insurance():
    verdict = rules.tests_on_completion(spans=3, length_m=Decimal("10"), tests_per_span=1, load_test_done=False, insurance_proof=False)
    assert not verdict.passed
    assert verdict.value["required_tests"] == 6
    assert any("Insurance proof" in reason for reason in verdict.reasons)


# ---------------------------------------------------------------------------
# sec 3.6  the DLP is a predicate, not a date
# ---------------------------------------------------------------------------


def test_dlp_is_active_inside_ten_years_with_no_open_defects():
    verdict = rules.dlp_state(completion_date=date(2020, 1, 1), open_defects=0, today=date(2025, 1, 1))
    assert verdict.value["active"] is True
    assert verdict.value["nominal_expiry"] == "2030-01-01"


def test_dlp_is_extended_while_a_defect_is_open():
    """Art. 17.5: the clock does not run out while a defect is open."""
    verdict = rules.dlp_state(completion_date=date(2020, 1, 1), open_defects=2, today=date(2035, 1, 1))
    assert verdict.value["active"] is False
    assert verdict.value["extended_by_open_defects"] is False
    assert any("expired" in reason for reason in verdict.reasons)

    inside = rules.dlp_state(completion_date=date(2020, 1, 1), open_defects=1, today=date(2025, 1, 1))
    assert inside.value["extended_by_open_defects"] is True


def test_defect_remedy_is_rectification_plus_twenty_percent():
    class _Defect:
        notified_on = date(2025, 3, 1)
        estimated_rectification_cost = Decimal("100000")
        rectified_on = None

    verdict = rules.defect_rectification_demand(_Defect())
    assert verdict.value["rectification_due"] == "2025-03-16"
    assert verdict.value["damages_at_20_percent"] == "20000.00"
    assert verdict.value["total_deductible"] == "120000.00"


def test_retention_is_refunded_in_fifteen_days_and_does_not_back_the_dlp():
    verdict = rules.retention_refund(date(2025, 6, 30))
    assert verdict.value["retention_refund_due"] == "2025-07-15"
    assert "does not back the 10-year DLP" in verdict.value["note"]


# ---------------------------------------------------------------------------
# sec 4A.2  Gujarat's own contract terms
# ---------------------------------------------------------------------------


def test_bridge_tender_above_ten_crore_must_be_b1():
    assert rules.tender_form(Decimal("12000000"), is_bridge=True).value["tender_form"] == "B-1"
    assert rules.tender_form(Decimal("9000000"), is_bridge=True).value["tender_form"] == "B-1 or B-2"


def test_bridge_ceiling_is_lower_than_road_ceiling():
    # 1.1 crore is above the 1.0 crore bridge ceiling but below the 1.2 crore road
    # ceiling, so the same amount attracts B-1 for a bridge and not for a road.
    assert rules.tender_form(Decimal("11000000"), is_bridge=True).value["tender_form"] == "B-1"
    assert rules.tender_form(Decimal("11000000"), is_bridge=False).value["tender_form"] == "B-1 or B-2"
    assert rules.B1_CEILING_ROAD > rules.B1_CEILING_BRIDGE


def test_security_deposit_is_three_percent_above_five_lakh():
    assert rules.security_deposit(Decimal("8500000")).value["percent"] == "3"
    assert rules.security_deposit(Decimal("300000")).value["percent"] == "2"
    assert rules.security_deposit(Decimal("3000000"), is_hydraulic=True).value["percent"] == "5"


def test_performance_bond_is_three_percent():
    verdict = rules.performance_bond(Decimal("10000000"))
    assert verdict.value["amount"] == "300000.00"
    assert verdict.value["sole_security_behind_dlp"] is True


# ---------------------------------------------------------------------------
# sec 4A.3  S / SRI / U
# ---------------------------------------------------------------------------


def test_only_unsatisfactory_grades_require_an_atr():
    assert not rules.inspection_outcome("S", None).value["atr_required"]
    assert rules.inspection_outcome("SRI", date(2025, 8, 1)).passed
    assert not rules.inspection_outcome("U", None).passed


# ---------------------------------------------------------------------------
# sec 4A.4  the price-variation engine
# ---------------------------------------------------------------------------


def test_pv_requires_above_twenty_five_lakh_and_above_twelve_months():
    assert not rules.pv_admissible(Decimal("2000000"), 24).passed
    assert not rules.pv_admissible(Decimal("5000000"), 12).passed
    assert rules.pv_admissible(Decimal("5000000"), 24).passed


def test_no_price_variation_in_the_first_twelve_months():
    components = [rules.PvComponent("LABOUR", Decimal("1000000"), Decimal("100"), Decimal("110"), is_bridge=False)]
    verdict = rules.price_variation(components, months_elapsed=6, estimated_cost=Decimal("5000000"))
    assert not verdict.passed
    assert verdict.value["computed"] == "0.00"
    assert any("first 12 months" in reason for reason in verdict.reasons)


def test_cement_and_steel_carry_zero_weight_for_bridges():
    """The counter-intuitive detail that distinguishes research from assumption."""
    components = [
        rules.PvComponent("CEMENT", Decimal("1000000"), rules.Decimal("122.5"), rules.Decimal("130"), is_bridge=True),
        rules.PvComponent("LABOUR", Decimal("2000000"), Decimal("100"), Decimal("110"), is_bridge=True),
    ]
    verdict = rules.price_variation(components, months_elapsed=18, estimated_cost=Decimal("5000000"))
    assert not verdict.passed
    cement = next(line for line in verdict.value["lines"] if line["component"] == "CEMENT")
    assert cement["zero_weight_for_bridges"] is True
    assert cement["admissible"] is False
    assert any("zero escalation weight" in reason for reason in verdict.reasons)


def test_interchanged_index_base_is_refused_with_the_bharuch_case_cited():
    """The exact error that cost 4.74 crore: Cement and Steel bases swapped."""
    components = [
        # Correct bases are Cement 122.5 and Steel 108.4. These are swapped.
        rules.PvComponent("CEMENT", Decimal("1000000"), rules.Decimal("108.4"), Decimal("130"), is_bridge=False),
        rules.PvComponent("STEEL", Decimal("1000000"), rules.Decimal("122.5"), Decimal("112"), is_bridge=False),
    ]
    verdict = rules.price_variation(components, months_elapsed=18, estimated_cost=Decimal("5000000"))
    assert not verdict.passed
    assert any("Bharuch" in reason for reason in verdict.reasons)
    # CEMENT's submitted base is 108.4, which is Steel's official base.
    cement_reason = next(reason for reason in verdict.reasons if "CEMENT: base index" in reason)
    assert "122.5" in cement_reason
    assert "108.4" in cement_reason
    assert verdict.value["computed"] == "0.00"


def test_computed_price_variation_is_capped_at_the_ceiling():
    components = [
        rules.PvComponent("LABOUR", Decimal("3000000"), Decimal("100"), Decimal("130"), is_bridge=False),
    ]
    verdict = rules.price_variation(components, months_elapsed=18, estimated_cost=Decimal("6000000"))
    # 5% of 60 lakh = 3 lakh ceiling, so a 90 lakh computed claim is cut to 3 lakh.
    assert verdict.value["computed"] == "900000.00"
    assert verdict.value["payable"] == "300000.00"
    assert any("exceeds the ceiling" in reason for reason in verdict.reasons)


def test_escalation_index_is_one_point_one_to_the_n():
    assert rules.escalation_index(0) == rules.Decimal("1.0000")
    assert rules.escalation_index(2) == rules.Decimal("1.2100")


# ---------------------------------------------------------------------------
# sec 4A.5 / 4A.6  Schedule-G, bid capacity, prequalification
# ---------------------------------------------------------------------------


def test_schedule_g_has_three_stages_with_hard_bounds():
    assert rules.schedule_g_sla(1).value["outer_bound_days"] == 30
    assert rules.schedule_g_sla(2).value["outer_bound_days"] == 60
    assert rules.schedule_g_sla(3).value["outer_bound_days"] == 90
    assert not rules.schedule_g_sla(4).passed


def test_bid_capacity_formula():
    verdict = rules.bid_capacity(Decimal("10000000"), Decimal("5000000"), Decimal("2"))
    assert verdict.value["capacity"] == "35000000.00"


def test_bridge_prequalification_uses_a_ten_year_lookback():
    verdict = rules.prequalification(
        tender_amount=Decimal("90000000"),
        is_bridge=True,
        similar_work_value=Decimal("40000000"),
        completed_years_ago=8,
    )
    assert verdict.passed
    verdict_road = rules.prequalification(
        tender_amount=Decimal("90000000"),
        is_bridge=False,
        similar_work_value=Decimal("40000000"),
        completed_years_ago=8,
    )
    assert not verdict_road.passed


# ---------------------------------------------------------------------------
# sec 4A.9  the 120-day rule
# ---------------------------------------------------------------------------


def test_120_day_rule_breach_is_reported():
    opening = date(2025, 1, 1)
    breach = rules.tender_acceptance_120_day(opening, date(2025, 6, 1), date(2025, 6, 15))
    assert not breach.passed
    # 1 Jan + 120 days is 1 May, so a 1 June acceptance is 31 days late.
    assert breach.value["deadline"] == "2025-05-01"
    assert any("31 day(s) past" in reason for reason in breach.reasons)
    assert any("re-invited" in reason for reason in breach.reasons)


def test_120_day_rule_passes_within_the_window():
    verdict = rules.tender_acceptance_120_day(date(2025, 1, 1), date(2025, 3, 1), date(2025, 3, 15))
    assert verdict.passed


# ---------------------------------------------------------------------------
# sec 2.2  the conditional design life
# ---------------------------------------------------------------------------


def test_design_life_is_conditional_on_the_regime_not_the_concrete():
    assert rules.design_life_justified(True, True, True).passed
    verdict = rules.design_life_justified(True, False, True)
    assert not verdict.passed
    assert any("maintenance" in reason for reason in verdict.reasons)


# ---------------------------------------------------------------------------
# Every rule must cite the record
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "call",
    [
        lambda: rules.concrete_cube_acceptance([Decimal("40")] * 4, Decimal("30")),
        lambda: rules.core_acceptance([Decimal("30")] * 3, Decimal("30")),
        lambda: rules.durability_check("SEVERE", Decimal("0.4"), Decimal("400"), "M35"),
        lambda: rules.milestone_credit(Decimal("35"), Decimal("100")),
        lambda: rules.liquidated_damages(Decimal("100"), 1),
        lambda: rules.tests_on_completion(1, Decimal("10"), 2, True, True),
        lambda: rules.dlp_state(date(2020, 1, 1), 0, date(2021, 1, 1)),
        lambda: rules.retention_refund(date(2021, 1, 1)),
        lambda: rules.tender_form(Decimal("20000000"), True),
        lambda: rules.security_deposit(Decimal("9000000")),
        lambda: rules.performance_bond(Decimal("9000000")),
        lambda: rules.inspection_outcome("S", None),
        lambda: rules.pv_admissible(Decimal("9000000"), 24),
        lambda: rules.price_variation([], 24, Decimal("9000000")),
        lambda: rules.schedule_g_sla(1),
        lambda: rules.bid_capacity(Decimal("1"), Decimal("1"), Decimal("1")),
        lambda: rules.prequalification(Decimal("90000000"), True, Decimal("40000000"), 1),
        lambda: rules.tender_acceptance_120_day(date(2025, 1, 1), date(2025, 2, 1), date(2025, 2, 5)),
        lambda: rules.design_life_justified(True, True, True),
    ],
)
def test_every_verdict_cites_the_research_record(call):
    """A rule with no citation is a guess, and a guess must fail this test."""
    verdict = call()
    assert "research_3phase_opencode.md" in verdict.basis
    assert verdict.as_dict()["basis"] == verdict.basis
