# BridgeTheGap Handoff

## Current objective

Deliver a defensible, research-backed Gujarat R&B bridge lifecycle prototype.
The current active slice is a persistent, role-based inspection-to-maintenance
workflow, deployed as Next.js on Vercel, FastAPI on Render, and PostgreSQL on
Neon.

## Git truth

- Branch: `main`, tracking `origin/main`
- Latest merge: `90a7107 merge: persistent role-based lifecycle workflow`
- Deliberately uncommitted user/other-agent files:
  - `docs/current-state.md`
  - `docs/decisions.md`
  - `docs/research_3phase_opencode.md`

Do not stage, discard, or overwrite those files without reconciling their
author's work first.

## Completed

- Editorial landing page and separate operations workspace.
- Initial Alembic schema, compatible with Neon PostgreSQL.
- Seeded fictional bridge/project/tender data and four demo users.
- JWT login with server-enforced roles: Manager, Executive Engineer,
  Inspector, and Contractor.
- Persistent inspection → approved work → contractor completion → independent
  verification workflow, including audit timeline records.
- CI-relevant checks pass locally: API Ruff/tests, web lint/typecheck/build.

## Deployment action required

The Render web service was created manually, so the checked-in `render.yaml`
does not change its dashboard settings automatically. In Render, set:

```text
Build command: pip install -r requirements.txt && alembic upgrade head
Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set a long random `JWT_SECRET` in Render environment variables. `DATABASE_URL`
must remain the Neon connection string and must never be copied to Vercel.
Then manually deploy latest `main`. Vercel can auto-deploy from `main` with
only `NEXT_PUBLIC_API_URL=https://bridgethegap-q1ma.onrender.com`.

## Exact next action

After Render deploys, open `/workspace`, choose Inspector, record an
inspection; switch to Executive Engineer to approve work; switch to Contractor
to complete it; switch back to Engineer or Inspector to verify it. Confirm the
state remains after refresh. Then add the project-to-tender-to-award and
construction-to-handover workflow slices, using the research documentation as
the authority boundary.

## Verification last run

```text
apps/api: alembic upgrade head; python -m ruff check .; pytest  → pass
apps/web: npm run lint; npx tsc --noEmit; npm run build          → pass
```
