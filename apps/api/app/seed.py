from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Bid, Bridge, LifecycleEvent, Project, Tender, User
from .security import hash_password


def seed_demo_data(session: Session) -> None:
    if not session.scalar(select(Project.id).limit(1)):
        project = Project(id="PRJ-001", name="Mahi River Bridge Rehabilitation", division="Vadodara", estimate=12500000, status="TENDER_OPEN")
        tender = Tender(id="TEN-001", project_id=project.id, status="OPEN")
        session.add_all([
            project,
            tender,
            Bid(id="BID-001", tender_id=tender.id, contractor="Saffron Infrastructure", amount=11850000),
            Bid(id="BID-002", tender_id=tender.id, contractor="Narmada Works", amount=12100000),
            Bridge(id="BRG-001", code="GJ-RB-042", name="Mahi River Bridge", next_inspection="2026-10-15"),
            LifecycleEvent(id="EVT-001", bridge_id="BRG-001", actor="Executive Engineer", message="Demo bridge passport created from handover record."),
        ])
    users = [
        User(id="USR-MANAGER", email="manager@demo.local", name="Project Manager", role="MANAGER", password_hash=hash_password("DemoPass123")),
        User(id="USR-ENGINEER", email="engineer@demo.local", name="Executive Engineer", role="EXECUTIVE_ENGINEER", password_hash=hash_password("DemoPass123")),
        User(id="USR-INSPECTOR", email="inspector@demo.local", name="Bridge Inspector", role="INSPECTOR", password_hash=hash_password("DemoPass123")),
        User(id="USR-CONTRACTOR", email="contractor@demo.local", name="Saffron Site Lead", role="CONTRACTOR", contractor_name="Saffron Infrastructure", password_hash=hash_password("DemoPass123")),
        User(id="USR-CHIEF", email="chiefengineer@demo.local", name="Chief Engineer", role="CHIEF_ENGINEER", password_hash=hash_password("DemoPass123")),
        User(id="USR-SUPERINTENDENT", email="superintendent@demo.local", name="Superintending Engineer", role="SUPERINTENDING_ENGINEER", password_hash=hash_password("DemoPass123")),
        User(id="USR-QUALITY", email="quality@demo.local", name="Quality Engineer", role="QUALITY_ENGINEER", password_hash=hash_password("DemoPass123")),
        User(id="USR-FINANCE", email="finance@demo.local", name="Divisional Accountant", role="FINANCE", password_hash=hash_password("DemoPass123")),
        User(id="USR-AUDITOR", email="auditor@demo.local", name="Audit Viewer", role="AUDITOR", password_hash=hash_password("DemoPass123")),
    ]
    existing_emails = set(session.scalars(select(User.email)).all())
    session.add_all([user for user in users if user.email not in existing_emails])
    session.commit()
