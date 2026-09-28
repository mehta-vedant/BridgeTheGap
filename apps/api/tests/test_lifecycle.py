from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine
from app.main import app
from app.seed import seed_demo_data


def login(client: TestClient, email: str) -> dict[str, str]:
    response = client.post("/api/auth/login", json={"email": email, "password": "DemoPass123"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_bridge_inspection_to_verified_workflow() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        seed_demo_data(session)
    with TestClient(app) as client:
        inspector = login(client, "inspector@demo.local")
        engineer = login(client, "engineer@demo.local")
        contractor = login(client, "contractor@demo.local")
        inspection = client.post("/api/bridges/BRG-001/inspections", headers=inspector)
        assert inspection.status_code == 200
        work = client.post(
            "/api/bridges/BRG-001/work-orders",
            json={"description": "Repair deck drainage joint", "contractor": "Saffron Infrastructure"},
            headers=engineer,
        )
        assert work.status_code == 201
        work_id = work.json()["id"]
        assert client.post(f"/api/work-orders/{work_id}/complete", headers=contractor).status_code == 200
        assert client.post(f"/api/work-orders/{work_id}/verify", headers=engineer).json()["status"] == "VERIFIED"


def test_role_checks_are_enforced() -> None:
    with TestClient(app) as client:
        contractor = login(client, "contractor@demo.local")
        response = client.post("/api/projects", json={"name": "Unauthorised", "division": "Surat", "estimate": 1000000}, headers=contractor)
        assert response.status_code == 403
