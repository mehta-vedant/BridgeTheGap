from fastapi import FastAPI

app = FastAPI(title="R&B Bridge Lifecycle API", version="0.1.0")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "bridge-lifecycle-api"}

@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict[str, int]:
    return {"projects": 0, "bridges": 0, "attention_required": 0, "active_work_orders": 0}
