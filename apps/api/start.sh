#!/bin/sh
set -eu

# Alembic records applied revisions, so this is safe on every container start.
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
