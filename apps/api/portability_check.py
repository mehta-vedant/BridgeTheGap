"""Compile the schema against the PostgreSQL dialect.

The app has only ever run on SQLite locally, so "it should work on Postgres" is
a claim, not a fact. This renders every table, index and constraint in the
PostgreSQL dialect, which is what Alembic will actually emit on Render, and
reports anything that will not compile. It catches the portability failures
that would otherwise surface as a failed deploy: JSONB-only defaults, SQLite
type affinity, dialect-specific DDL.

Run: python portability_check.py
"""

from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateIndex, CreateTable

import app.models
import app.mvp_models  # noqa: F401  - registers every table on Base.metadata
from app.database import Base

dialect = postgresql.dialect()
problems: list[str] = []
statements: list[str] = []

for table in Base.metadata.sorted_tables:
    try:
        ddl = str(CreateTable(table).compile(dialect=dialect))
        statements.append(ddl)
    except Exception as exc:  # noqa: BLE001 - the point is to report, not raise
        problems.append(f"TABLE {table.name}: {type(exc).__name__}: {exc}")
        continue
    for index in table.indexes:
        try:
            statements.append(str(CreateIndex(index).compile(dialect=dialect)))
        except Exception as exc:  # noqa: BLE001
            problems.append(f"INDEX {table.name}.{index.name}: {type(exc).__name__}: {exc}")

print(f"tables={len(Base.metadata.sorted_tables)} ddl_statements={len(statements)}")

# A real Postgres server rejects these; SQLite accepts them silently, so they
# are the failures most likely to be hiding in a SQLite-only development cycle.
banned = ("AUTOINCREMENT", "WITHOUT ROWID", "PRAGMA", "sqlite_")
for sql in statements:
    for token in banned:
        if token in sql.upper():
            problems.append(f"SQLITE-ONLY token {token} in: {sql[:90]}")

if problems:
    print("\nPROBLEMS")
    for problem in problems:
        print(" -", problem)
    raise SystemExit(1)

print("OK - every table, index and constraint compiles to PostgreSQL")

engine = create_engine("postgresql+psycopg://", strategy=None) if False else None
print("\nSample DDL (lifecycle_contracts):")
for sql in statements:
    if "CREATE TABLE lifecycle_contracts" in sql:
        print(sql)
        break
