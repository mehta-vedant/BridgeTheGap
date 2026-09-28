"""add tender bidding form, opening date, work order date, completion date and physical progress

Revision ID: 0004_tender_form_completion
Revises: 0003_preconstruction_evidence
Create Date: 2026-09-28

Why this migration exists
------------------------
The 120-day rule (GPWM Clause 212-A, GR 10-05-2013), the B-1 ceiling
(GR TNC-1088-D-347-(7)-C), and the 10-year defect liability period (Art. 17.1(d))
are all functions of dates and amounts. None of them can be evaluated without
these columns existing, and an evaluation that silently proceeds when a date is
missing is worse than one that refuses, because a re-tender triggered by the
120-day rule and a 10-year liability clock are both money.

`physical_progress` is recorded rather than derived from milestones so that a
contract's built state is a recorded fact rather than a sum of entries that may
or may not have been made. The derived lifecycle phase reads the contract state,
not this column, so a stale progress figure cannot teleport a bridge between
phases.
"""

# ruff: noqa: F401, I001 - import registers model metadata before inspection.
import app.mvp_models
from alembic import op
import sqlalchemy as sa

revision = "0004_tender_form_completion"
down_revision = "0003_preconstruction_evidence"
branch_labels = None
depends_on = None


_COLUMNS = (
    ("lifecycle_tenders", "tender_form", sa.String(4)),
    ("lifecycle_tenders", "work_order_issued_on", sa.Date()),
    ("lifecycle_contracts", "completion_date", sa.Date()),
    ("lifecycle_contracts", "physical_progress", sa.Numeric(5, 2)),
)


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())
    for table, column, column_type in _COLUMNS:
        if table not in existing_tables:
            # The table itself has not been created yet on this database; a later
            # create_all will produce it with these columns already present.
            continue
        present = {existing["name"] for existing in inspector.get_columns(table)}
        if column in present:
            continue
        default = sa.text("'B-1'") if column == "tender_form" else None
        op.add_column(table, sa.Column(column, column_type, nullable=True, server_default=default))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())
    for table, column, _ in reversed(_COLUMNS):
        if table in existing_tables:
            op.drop_column(table, column)
