from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


def login(client: TestClient, email: str) -> dict[str, str]:
    response = client.post("/api/auth/login", json={"email": email, "password": "DemoPass123"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def new_passport_payload() -> dict:
    return {
        "asset_code": "BRG-GJ-VAD-009901",
        "canonical_name": "Orsang River Bridge",
        "district": "Vadodara",
        "bridge_class": "MINOR_BRIDGE",
        "route_name": "Dabhoi - Bodeli Road",
        "chainage_km": 18.4,
        "length_m": 62,
        "span_count": 3,
        "project_title": "Orsang River Bridge Renewal",
        "project_type": "NEW_CONSTRUCTION",
        "estimate_amount": 8500000,
    }


def test_executive_engineer_creates_permanent_passport_and_project() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestClient(app) as client:
        engineer = login(client, "engineer@demo.local")
        created = client.post("/api/mvp/assets", json=new_passport_payload(), headers=engineer)
        assert created.status_code == 201
        body = created.json()
        assert body["asset"]["asset_code"] == "BRG-GJ-VAD-009901"
        assert body["asset"]["lifecycle_state"] == "SANCTION_AND_CLEARANCE"
        passport = client.get(f"/api/mvp/assets/{body['asset']['id']}/passport", headers=engineer)
        assert passport.status_code == 200
        assert passport.json()["project"]["title"] == "Orsang River Bridge Renewal"
        assert passport.json()["tender"]["status"] == "DRAFT"
        project_id = body["project_id"]
        report = client.post(f"/api/mvp/projects/{project_id}/reports", json={"report_type": "DPR", "reference": "DPR-2026-001", "source_class": "NATIONAL_REFERENCE"}, headers=engineer)
        assert report.status_code == 201
        clearance = client.post(f"/api/mvp/projects/{project_id}/clearances", json={"clearance_type": "GAD", "status": "SUBMITTED", "reference": "GAD-2026-001", "source_class": "GUJARAT_VERIFIED"}, headers=engineer)
        assert clearance.status_code == 201


def test_contractor_cannot_create_bridge_passport() -> None:
    with TestClient(app) as client:
        contractor = login(client, "contractor@demo.local")
        response = client.post("/api/mvp/assets", json=new_passport_payload(), headers=contractor)
        assert response.status_code == 403


def test_blank_asset_code_is_generated() -> None:
    with TestClient(app) as client:
        engineer = login(client, "engineer@demo.local")
        payload = new_passport_payload()
        payload["asset_code"] = ""
        created = client.post("/api/mvp/assets", json=payload, headers=engineer)
        assert created.status_code == 201
        assert created.json()["asset"]["asset_code"].startswith("BRG-GJ-VAD-")
