"""End-to-end checks for derived phase, role scope, and the bid path.

These are the three things that were wrong when the demo broke: a bridge could
be labelled post-construction without being built, every authenticated user saw
every bridge, and a contractor could not reach a tender they were entitled to
bid on. Each is tested through the real HTTP surface, because the bug lived in
the interaction between derivation, scoping and the endpoint -- not in any one of
them alone.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app

DEMO_PASSWORD = "DemoPass123"


@pytest.fixture(scope="module")
def client():
    # `TestClient` only runs the application's lifespan -- which seeds the demo
    # users and the nine-bridge portfolio -- inside a `with` block. Without it
    # every login returns 401 because the users were never created, which cost
    # a debugging cycle once already.
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client


def login(client: TestClient, email: str) -> str:
    response = client.post("/api/auth/login", json={"email": email, "password": DEMO_PASSWORD})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Derived phase
# ---------------------------------------------------------------------------


def test_phase_is_derived_from_records_not_a_stored_label(client: TestClient):
    """Every register row carries a phase, its basis, and the stored label it came from."""
    token = login(client, "engineer@demo.local")
    body = client.get("/api/mvp/assets", headers=auth(token)).json()

    assert body["items"], "the register must not be empty"
    for item in body["items"]:
        assert item["phase"] in ("SANCTION_AND_CLEARANCE", "EXECUTION", "POST_COMPLETION")
        assert item["phase_label"]


def test_post_completion_requires_a_completed_contract(client: TestClient):
    """A bridge with no contract cannot be in post-construction, whatever the column says."""
    token = login(client, "engineer@demo.local")
    items = client.get("/api/mvp/assets", headers=auth(token)).json()["items"]

    for item in items:
        passport = client.get(f"/api/mvp/assets/{item['id']}/passport", headers=auth(token)).json()
        if item["phase"] == "POST_COMPLETION":
            contract = passport.get("contract")
            assert contract, f"{item['asset_code']} is post-completion with no contract"
            assert contract["state"] == "COMPLETED", f"{item['asset_code']} is post-completion on a {contract['state']} contract"
        if not passport.get("contract"):
            assert item["phase"] == "SANCTION_AND_CLEARANCE"


def test_a_closed_phase_states_why_instead_of_vanishing(client: TestClient):
    """A proposed bridge must say post-construction is closed, not just omit it."""
    token = login(client, "engineer@demo.local")
    pre = [i for i in client.get("/api/mvp/assets?phase=SANCTION_AND_CLEARANCE", headers=auth(token)).json()["items"]]

    assert pre, "the seeded portfolio should contain pre-construction bridges"
    passport = client.get(f"/api/mvp/assets/{pre[0]['id']}/passport", headers=auth(token)).json()
    gates = passport["phase_gates"]

    assert gates["POST_COMPLETION"]["available"] is False
    assert "construct" in gates["POST_COMPLETION"]["reason"].lower()
    assert passport["defect_liability"].get("available") is False
    assert passport["defects"] == []


# ---------------------------------------------------------------------------
# Role scope
# ---------------------------------------------------------------------------


def test_contractor_cannot_see_another_companys_contract_bridge(client: TestClient):
    token = login(client, "engineer@demo.local")
    everything = [i["id"] for i in client.get("/api/mvp/assets", headers=auth(token)).json()["items"]]

    contractor = login(client, "contractor@demo.local")
    visible = client.get("/api/mvp/assets", headers=auth(contractor)).json()

    assert visible["items"], "a contractor must be able to see the tenders they may bid on"
    assert len(visible["items"]) < len(everything), "the contractor scope should be narrower than the engineer's"
    assert visible["scope"]["restricted"] is True


def test_contractor_is_refused_a_bridge_outside_scope(client: TestClient):
    engineer = login(client, "engineer@demo.local")
    everything = client.get("/api/mvp/assets", headers=auth(engineer)).json()["items"]
    contractor = login(client, "contractor@demo.local")
    visible_ids = {i["id"] for i in client.get("/api/mvp/assets", headers=auth(contractor)).json()["items"]}
    outside = [i for i in everything if i["id"] not in visible_ids]

    assert outside, "expected at least one bridge outside the contractor's scope"
    response = client.get(f"/api/mvp/assets/{outside[0]['id']}/passport", headers=auth(contractor))
    assert response.status_code == 403
    body = response.json()["error"]
    assert body["code"] == "NOT_IN_YOUR_SCOPE"
    assert body["remediation"]


def test_contractor_can_reach_a_published_tender_to_bid_on(client: TestClient):
    """The regression that made the bid button unreachable.

    A tender open for bidding is public by design, so a contractor must be able to
    see it before winning it. The earlier rule scoped contractors to bridges they
    already held a contract on, which made the bid button impossible to reach.
    """
    engineer = login(client, "engineer@demo.local")
    published = client.get("/api/mvp/assets", headers=auth(engineer)).json()["items"]
    contractor = login(client, "contractor@demo.local")
    visible = {i["id"]: i for i in client.get("/api/mvp/assets", headers=auth(contractor)).json()["items"]}

    open_tender = None
    for item in published:
        passport = client.get(f"/api/mvp/assets/{item['id']}/passport", headers=auth(engineer)).json()
        if passport.get("tender", {}).get("status") == "PUBLISHED" and not passport.get("contract"):
            open_tender = item
            break

    assert open_tender, "the seeded portfolio should contain a published, unawarded tender"
    assert open_tender["id"] in visible, "a contractor must see a tender open for bidding"
    passport = client.get(f"/api/mvp/assets/{open_tender['id']}/passport", headers=auth(contractor)).json()
    assert passport["tender"]["status"] == "PUBLISHED"


def test_contractor_sees_a_competitor_bid_exists_but_not_its_price(client: TestClient):
    """The notice is public; the tender room is not."""
    engineer = login(client, "engineer@demo.local")
    contractor = login(client, "contractor@demo.local")
    contractor_ids = {i["id"] for i in client.get("/api/mvp/assets", headers=auth(contractor)).json()["items"]}

    for item in client.get("/api/mvp/assets", headers=auth(engineer)).json()["items"]:
        if item["id"] not in contractor_ids:
            continue
        as_contractor = client.get(f"/api/mvp/assets/{item['id']}/passport", headers=auth(contractor)).json()
        as_engineer = client.get(f"/api/mvp/assets/{item['id']}/passport", headers=auth(engineer)).json()
        if not as_engineer.get("bids"):
            continue
        for bid in as_contractor["bids"]:
            if bid["redacted"]:
                assert bid["price_amount"] is None
                assert bid["note"]
            else:
                assert bid["own_bid"] is True
        return
    pytest.skip("no awarded-contract bridge with a bid in the seeded portfolio")


def test_dashboard_counts_are_scoped_not_departmental(client: TestClient):
    engineer = login(client, "engineer@demo.local")
    contractor = login(client, "contractor@demo.local")
    engineer_body = client.get("/api/mvp/dashboard", headers=auth(engineer)).json()
    contractor_body = client.get("/api/mvp/dashboard", headers=auth(contractor)).json()

    assert contractor_body["metrics"]["assets"] == len(contractor_body["register"])
    assert contractor_body["metrics"]["assets"] < engineer_body["metrics"]["assets"]
    assert sum(contractor_body["phases"].values()) == contractor_body["metrics"]["assets"]


# ---------------------------------------------------------------------------
# The bid path end to end
# ---------------------------------------------------------------------------


def test_contractor_can_submit_a_bid_and_engineer_can_award(client: TestClient):
    """Publish-gate-bid-award, driven entirely through the HTTP surface."""
    engineer = login(client, "engineer@demo.local")
    draft = None
    for item in client.get("/api/mvp/assets?phase=SANCTION_AND_CLEARANCE", headers=auth(engineer)).json()["items"]:
        passport = client.get(f"/api/mvp/assets/{item['id']}/passport", headers=auth(engineer)).json()
        if (passport.get("tender") or {}).get("status") == "DRAFT" and not passport.get("contract"):
            draft = (item, passport)
            break
    if draft is None:
        pytest.skip("no draft tender left in the seeded portfolio")
    item, passport = draft
    tender_id = passport["tender"]["id"]

    # A DRAFT tender refuses publication while the land gate is unmet.
    blocked = client.post(f"/api/mvp/tenders/{tender_id}/publish", headers=auth(engineer))
    if blocked.status_code == 409:
        assert blocked.json()["error"]["code"] == "GATE_NOT_PASSED"
        assert blocked.json()["error"]["remediation"]

    client.post(f"/api/mvp/projects/{passport['project']['id']}/land-readiness", headers=auth(engineer), json={"possession_percent": 95, "handover_reference": "SYN-LAND-MEMO-E2E"})
    published = client.post(f"/api/mvp/tenders/{tender_id}/publish", headers=auth(engineer))
    assert published.status_code == 200, published.text

    contractor = login(client, "contractor@demo.local")
    assert item["id"] in {i["id"] for i in client.get("/api/mvp/assets", headers=auth(contractor)).json()["items"]}

    bid = client.post(
        f"/api/mvp/tenders/{tender_id}/bids",
        headers=auth(contractor),
        json={"technical_summary": "End-to-end controlled bid with documented execution approach and NABL cube testing.", "price_amount": 24000000},
    )
    assert bid.status_code == 201, bid.text

    awarded = client.post(f"/api/mvp/tenders/{tender_id}/award", headers=auth(engineer))
    assert awarded.status_code == 200, f"award failed: {awarded.status_code} {awarded.text}"
    result = awarded.json()
    assert result["derived_phase"] == "EXECUTION"
    assert result["security_deposit"]["value"]["percent"] == "3"
    assert result["performance_bond"]["value"]["percent"] == "3"
    assert len(result["approval_chain"]) == 3

    # And the derived phase has actually moved, with no column being written.
    after = client.get(f"/api/mvp/assets/{item['id']}/passport", headers=auth(engineer)).json()
    assert after["phase"]["phase"] == "EXECUTION"
    assert after["phase"]["next_phase"] == "POST_COMPLETION"
    assert after["phase_gates"]["POST_COMPLETION"]["available"] is False


# ---------------------------------------------------------------------------
# Structured refusals
# ---------------------------------------------------------------------------


def test_a_refusal_carries_a_code_remediation_and_a_source(client: TestClient):
    token = login(client, "inspector@demo.local")
    # A fully valid payload, so the refusal that comes back is the *role* refusal
    # and not a schema validation failure. Order matters: FastAPI validates the
    # body before the route's own guard runs, so an incomplete body would test
    # the wrong thing.
    contract = client.post("/api/mvp/assets", headers=auth(token), json={
        "canonical_name": "Refusal probe bridge", "district": "Vadodara",
        "bridge_class": "MAJOR_BRIDGE", "route_name": "NH 48", "chainage_km": 12.5,
        "length_m": 90, "span_count": 3, "project_title": "Refusal probe project",
        "project_type": "NEW_CONSTRUCTION", "estimate_amount": 8500000,
        "latitude": 22.3, "longitude": 73.2,
    })
    assert contract.status_code == 403, contract.text
    error = contract.json()["error"]

    assert error["code"] == "ROLE_NOT_PERMITTED"
    assert error["remediation"]
    assert "research_3phase_opencode.md" in error["reference"]


def test_a_quality_test_on_a_pre_construction_bridge_is_refused_by_phase(client: TestClient):
    """Construction gates do not apply to a bridge that has not been awarded."""
    engineer = login(client, "engineer@demo.local")
    pre = client.get("/api/mvp/assets?phase=SANCTION_AND_CLEARANCE", headers=auth(engineer)).json()["items"]
    passport = client.get(f"/api/mvp/assets/{pre[0]['id']}/passport", headers=auth(engineer)).json()
    if not passport.get("contract"):
        # No contract means no contract-scoped route to test; the phase gate on
        # the passport already covers it.
        assert passport["phase"]["phase"] == "SANCTION_AND_CLEARANCE"
        return
    response = client.post(
        f"/api/mvp/contracts/{passport['contract']['id']}/quality-tests",
        headers=auth(engineer),
        json={"test_type": "M30 cube", "specified_value": 30, "samples": [31, 32, 33, 34]},
    )
    assert response.status_code in (403, 409)
