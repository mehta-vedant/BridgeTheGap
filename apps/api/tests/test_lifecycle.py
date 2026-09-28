from fastapi.testclient import TestClient

from app.main import app


def test_bridge_inspection_to_verified_workflow() -> None:
    client = TestClient(app)
    inspection = client.post("/api/bridges/BRG-001/inspections")
    assert inspection.status_code == 200
    work = client.post(
        "/api/bridges/BRG-001/work-orders",
        json={"description": "Repair deck drainage joint", "contractor": "Saffron Infrastructure"},
    )
    assert work.status_code == 201
    work_id = work.json()["id"]
    assert client.post(f"/api/work-orders/{work_id}/complete").status_code == 200
    assert client.post(f"/api/work-orders/{work_id}/verify").json()["status"] == "VERIFIED"
