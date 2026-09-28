from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="R&B Bridge Lifecycle API", version="0.1.0")

projects = [{"id": "PRJ-001", "name": "Mahi River Bridge Rehabilitation", "status": "TENDER_OPEN", "estimate": 12500000, "division": "Vadodara"}]
tenders = [{"id": "TEN-001", "project_id": "PRJ-001", "status": "OPEN", "bids": [{"id": "BID-001", "contractor": "Saffron Infrastructure", "amount": 11850000}, {"id": "BID-002", "contractor": "Narmada Works", "amount": 12100000}]}]
bridges = [{"id": "BRG-001", "name": "Mahi River Bridge", "code": "GJ-RB-042", "service_status": "IN_SERVICE", "maintenance_status": "NONE", "next_inspection": "2026-10-15", "contractor": "Saffron Infrastructure"}]
events = [{"id": "EVT-001", "bridge_id": "BRG-001", "at": "2026-09-28", "actor": "Executive Engineer", "message": "Demo bridge passport created from handover record."}]
work_orders: list[dict] = []

class ProjectCreate(BaseModel):
    name: str = Field(min_length=3)
    division: str = Field(min_length=2)
    estimate: int = Field(gt=0)

class BidCreate(BaseModel):
    contractor: str = Field(min_length=2)
    amount: int = Field(gt=0)

class WorkCreate(BaseModel):
    description: str = Field(min_length=5)
    contractor: str = Field(min_length=2)

def find(items: list[dict], item_id: str) -> dict:
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        raise HTTPException(404, "Resource not found")
    return item

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "bridge-lifecycle-api"}

@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict:
    return {"projects": len(projects), "bridges": len(bridges), "attention_required": sum(1 for bridge in bridges if bridge["maintenance_status"] == "ACTION_REQUIRED"), "active_work_orders": sum(1 for work in work_orders if work["status"] != "VERIFIED")}

@app.get("/api/projects")
def list_projects() -> list[dict]: return projects

@app.post("/api/projects", status_code=201)
def create_project(payload: ProjectCreate) -> dict:
    project = {"id": f"PRJ-{len(projects)+1:03}", **payload.model_dump(), "status": "NEED_IDENTIFIED"}
    projects.append(project)
    return project

@app.post("/api/projects/{project_id}/approvals")
def approve_project(project_id: str) -> dict:
    project = find(projects, project_id)
    if project["status"] == "TECHNICALLY_SANCTIONED": return project
    project["status"] = "TECHNICALLY_SANCTIONED"
    return project

@app.get("/api/tenders/{tender_id}")
def get_tender(tender_id: str) -> dict: return find(tenders, tender_id)

@app.post("/api/tenders/{tender_id}/bids", status_code=201)
def submit_bid(tender_id: str, payload: BidCreate) -> dict:
    tender = find(tenders, tender_id)
    if tender["status"] != "OPEN": raise HTTPException(409, "Tender is not open")
    bid = {"id": f"BID-{uuid4().hex[:6].upper()}", **payload.model_dump()}
    tender["bids"].append(bid)
    return bid

@app.post("/api/tenders/{tender_id}/award")
def award_tender(tender_id: str) -> dict:
    tender = find(tenders, tender_id)
    if tender["status"] == "AWARDED": return tender
    winner = min(tender["bids"], key=lambda bid: bid["amount"])
    tender.update({"status": "AWARDED", "awarded_bid": winner, "contract_id": f"CON-{tender_id[-3:]}"})
    project = find(projects, tender["project_id"]); project["status"] = "AWARDED"
    return tender

@app.get("/api/bridges")
def list_bridges() -> list[dict]: return bridges

@app.get("/api/bridges/{bridge_id}/timeline")
def timeline(bridge_id: str) -> list[dict]:
    find(bridges, bridge_id)
    return [event for event in events if event["bridge_id"] == bridge_id]

@app.post("/api/bridges/{bridge_id}/inspections")
def submit_inspection(bridge_id: str, requires_disposition: bool = True) -> dict:
    bridge = find(bridges, bridge_id)
    bridge["maintenance_status"] = "ACTION_REQUIRED" if requires_disposition else "NONE"
    event = {"id": f"EVT-{uuid4().hex[:6]}", "bridge_id": bridge_id, "at": str(datetime.now(UTC).date()), "actor": "Inspector", "message": "Inspection submitted; engineering disposition required." if requires_disposition else "Inspection submitted with no action required."}
    events.append(event)
    return {"bridge": bridge, "event": event}

@app.post("/api/bridges/{bridge_id}/work-orders", status_code=201)
def create_work_order(bridge_id: str, payload: WorkCreate) -> dict:
    bridge = find(bridges, bridge_id)
    if bridge["maintenance_status"] != "ACTION_REQUIRED": raise HTTPException(409, "No disposition-required finding")
    work = {"id": f"WO-{len(work_orders)+1:03}", "bridge_id": bridge_id, **payload.model_dump(), "status": "APPROVED"}
    work_orders.append(work); bridge["maintenance_status"] = "WORK_APPROVED"
    events.append({"id": f"EVT-{uuid4().hex[:6]}", "bridge_id": bridge_id, "at": str(datetime.now(UTC).date()), "actor": "Executive Engineer", "message": f"Work order {work['id']} approved."})
    return work

@app.post("/api/work-orders/{work_id}/complete")
def complete_work(work_id: str) -> dict:
    work = find(work_orders, work_id)
    if work["status"] == "VERIFIED": raise HTTPException(409, "Verified work cannot be completed again")
    work["status"] = "VERIFICATION_PENDING"; return work

@app.post("/api/work-orders/{work_id}/verify")
def verify_work(work_id: str) -> dict:
    work = find(work_orders, work_id)
    if work["status"] == "VERIFIED": return work
    if work["status"] != "VERIFICATION_PENDING": raise HTTPException(409, "Completion is required before verification")
    work["status"] = "VERIFIED"; bridge = find(bridges, work["bridge_id"]); bridge["maintenance_status"] = "NONE"
    events.append({"id": f"EVT-{uuid4().hex[:6]}", "bridge_id": bridge["id"], "at": str(datetime.now(UTC).date()), "actor": "Executive Engineer", "message": f"Work order {work_id} independently verified."})
    return work
