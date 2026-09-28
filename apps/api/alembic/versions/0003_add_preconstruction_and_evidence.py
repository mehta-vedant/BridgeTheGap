"""add pre-construction records and evidence metadata

Revision ID: 0003_preconstruction_evidence
Revises: 0002_mvp_domain
Create Date: 2026-09-28
"""

# ruff: noqa: F401, I001 - import registers model metadata before create_all.
import app.mvp_models
from alembic import op

from app.database import Base

revision = "0003_preconstruction_evidence"
down_revision = "0002_mvp_domain"
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    for name in ("evidence_records", "clearance_records", "project_reports"):
        Base.metadata.tables[name].drop(bind=op.get_bind(), checkfirst=True)
