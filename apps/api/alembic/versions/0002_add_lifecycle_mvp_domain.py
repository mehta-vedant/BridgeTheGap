"""add normalized lifecycle MVP domain

Revision ID: 0002_mvp_domain
Revises: 0001_initial
Create Date: 2026-09-28
"""
# ruff: noqa: I001 - mapping import registers metadata for the additive initial domain.

import app.mvp_models
from alembic import op

from app.database import Base

revision = "0002_mvp_domain"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    for table in reversed(list(app.mvp_models.Base.metadata.sorted_tables)):
        if table.name not in {"bridge_projects", "tenders", "tender_bids", "bridges", "work_orders", "lifecycle_events", "users"}:
            table.drop(bind=op.get_bind(), checkfirst=True)
