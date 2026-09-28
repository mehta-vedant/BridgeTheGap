# Bridge The Gap

**A bridge lifecycle management system for the Gujarat Roads & Buildings Department.**

Gujarat has 7,185 bridges — 1,596 major, 5,589 minor. The department already
mandates twice-yearly inspection, already maintains a bar-chart register, and
already names a Deputy Engineer *personally responsible* when inspections are
missed. The process exists. It failed anyway.

The World Bank's own evaluation of Gujarat's highway programme described its
bridge management in 2012 as *"presently in the form of a catalogue of bridge
condition with photographs."* CAG Report No. 1 of 2026 found the department has
**no works accounting and management system at all**, and recommended building
one — with an automated price-variation module — naming Odisha's WAMIS as the
model.

This is that substrate.

---

## What it does

One register. Every bridge. Three lifecycle phases derived from records.
Authority enforced in the query. Money computed, not accepted.

| | |
|---|---|
| **Sanction & Clearance** | Land readiness, sanctions, drawings, technical clearance, tendering |
| **Execution** | Award, milestones, quality testing, price variation, S/SRI/U → ATR escalation |
| **Post-Completion** | Inspections, defects, work orders, the 10-year defect liability period, retention release |

### The three ideas worth defending

**1. Phase is derived, never typed.**
`app/lifecycle.py` computes the phase from whether a contract has been awarded
and whether it is completed. You cannot put a bridge into post-construction by
writing a column, and a not-yet-built bridge is structurally incapable of
appearing there. A *published but unawarded* tender is still pre-construction —
you cannot be under construction without somebody being bound to build you.

**2. Scope is SQL, not the frontend.**
A contractor sees only bridges with a tender open for bidding, bridges their
company is bound to build, and defects they have been told to repair. That is
applied in the query, before a row is read — not by hiding cards in React. The
tender *notice* is public; the *tender room* is not. A contractor sees that a
competing bid exists and never sees its price.

**3. Every rule cites its source.**
`app/rules.py` holds ~20 predicates, each returning a verdict with a `basis`
naming the section of the research record that justifies it. Every error carries
a code, a message, remediation steps, and a reference. Where the record says
`NOT ESTABLISHED`, the system returns **501 rather than inventing a value**.

A plausible number nobody can defend is worse than no number.

---

## Quick start

Requires Python 3.11+ and Node 20+.

```bash
# API  -> http://localhost:8000  (docs at /docs)
cd apps/api
pip install -r requirements.txt
python serve.py            # migrates, then serves

# Web -> http://localhost:3000
cd apps/web
npm install
npm run dev
```

`serve.py` runs `alembic upgrade head` and then starts the server in one
process. Use it rather than invoking alembic and uvicorn separately — see
"Deployment" below for why.

The database seeds itself on first run: a nine-bridge portfolio, six divisions,
and nine demo accounts. Seeding is **additive and idempotent** per `asset_code`
— it never deletes or overwrites existing rows.

### Demo accounts

Password for all: `DemoPass123`

| Role | Email | Sees |
|---|---|---|
| Executive Engineer | `engineer@demo.local` | Everything; moves gates, awards work |
| Chief Engineer | `chiefengineer@demo.local` | Everything; statewide portfolio |
| Superintending Engineer | `superintendent@demo.local` | Everything; circle-level oversight |
| Bridge Inspector | `inspector@demo.local` | Awarded bridges only; records condition evidence |
| Quality Engineer | `quality@demo.local` | Awarded bridges only; validates test evidence |
| Divisional Accountant | `finance@demo.local` | Awarded bridges only; reviews PV and finance |
| Contractor | `contractor@demo.local` | Own tenders, contracts and work orders only |
| Manager | `manager@demo.local` | Everything; portfolio oversight |
| Auditor | `auditor@demo.local` | Everything, read-only |

Scope is enforced server-side. Signing in as different roles visibly changes
the register.

---

## The demo path

Nine bridges, three per phase, in one register with no pagination — a query
cannot hide an asset.

1. **Sign in as Executive Engineer.** The rail shows all nine, grouped by
   *derived* phase.
2. **Open a proposed bridge.** It is pre-construction, and the header says
   *why*. Post-Completion is **closed with a reason** — not hidden.
3. **Click "Publish tender"** while the land gate is unmet. It is refused, with
   a code, the missing requirement, remediation, and the clause.
4. **Record 95% possession + memo.** The gate passes; the tender publishes and
   the 120-day acceptance clock starts.
5. **Sign in as Contractor.** The published tender is visible. Submit a bid.
6. **Back as Executive Engineer.** Award. The derived phase moves to Execution
   with no column written, and the response carries the security deposit (3%),
   the performance bond (3%), the milestone schedule, and the three-layer
   approval chain.
7. **Sign in as Divisional Accountant.** Submit a price-variation claim as
   *measured facts only* — components, portions, indices, months elapsed. The
   server computes the entitlement. Swap the Cement and Steel base indices: it
   produces **nothing**, because a claim built on a swapped base does not produce
   a wrong number, it produces a plausible one.

That last step is the real Bharuch failure: Cement at 122.5 and Steel at 108.4
interchanged in one cell, a ₹15.57 lakh recovery became a ₹40.13 lakh payment, and
₹55.70 lakh inverted with a completely convincing answer.

---

## Architecture

```
apps/
  api/
    app/
      lifecycle.py     Phase derivation, phase gates, role visibility
      rules.py         ~20 sourced predicates, each citing the research record
      errors.py        DomainError — code, message, remediation, reference
      mvp_api.py       20 lifecycle routes
      mvp_models.py    The domain schema
      mvp_seed.py      Nine-bridge portfolio, additive and idempotent
      main.py          Auth, health, CORS, legacy routes
    alembic/versions/  0001 → 0004
    tests/             68 tests
  web/
    src/app/workspace/ The register, passport, gates, quality, finance
docs/
  research_3phase_opencode.md   The evidence record. Read this first.
  decisions.md                  D-001 … D-022
```

A modular monolith: FastAPI + SQLAlchemy on Postgres, Next.js on the front. No
queue, no cache, no microservices — none is earned by the current requirements.

### Four modules that carry the design

- **`lifecycle.py`** — the single source of truth for phase and visibility.
  `phase_facts` answers for a list of assets in three queries, not N.
- **`rules.py`** — no rule lives in a route handler. A route gathers facts and
  calls a rule; the rule returns a verdict with a `basis`.
- **`errors.py`** — `DomainError` subclasses `HTTPException` and carries
  `code` / `message` / `detail` / `remediation` / `reference`. The client renders
  all five.
- **`research_3phase_opencode.md`** — 1,644 lines, 22 source URLs, 36 explicit
  `NOT ESTABLISHED` markers. Every rule in the code traces to a section of it,
  and a test enforces that it does.

---

## Testing

```bash
cd apps/api
python -m pytest tests -q          # 68 passed
cd ../../apps/web
npx tsc --noEmit                  # clean
npm run build
```

Two suites matter more than the rest:

- **`test_rules.py`** — every predicate, and an assertion that *every* verdict
  cites the research record.
- **`test_phase_and_scope.py`** — the three regressions that broke the demo:
  a bridge could be labelled post-construction without being built, every
  authenticated user saw every bridge, and a contractor could not reach a tender
  they were entitled to bid on. All three are tested through the real HTTP
  surface, because each bug lived in the *interaction* between derivation,
  scoping and the endpoint.

---

## Deployment

The frontend is on Vercel. The API is on Render.

> **If you created the Render service by hand, `render.yaml` is ignored** —
> dashboard settings override the file completely. Set these in the dashboard.

**Settings → Build & Deploy**

| Field | Value |
|---|---|
| Root Directory | `apps/api` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python serve.py` |
| Health Check Path | `/health` |

That is the whole configuration. Migrations are not in either field, on
purpose.

### Why there is no `&&` and no alembic in the dashboard

This is worth understanding, because both obvious approaches have already
failed on this project and both fail *quietly*.

**Putting `alembic upgrade head` in the build step** is Render's own documented
pattern, and it is right in general. Here it was missed, `pip install` alone
succeeded, the deploy reported success, and the application then died at
startup on `relation "clearance_records" does not exist` — a table migration
0003 creates. The worst part was not the crash: it was that the deploy looked
fine.

**Putting it in the start step as `alembic upgrade head && uvicorn ...`**
cannot work. Render passes the entire field to a single process, so alembic
receives `&& uvicorn app.main:app --host 0.0.0.0 --port $PORT` as literal
arguments and exits 2.

So `serve.py` does both, in one process, and the Start Command is a single
argument-free command. Three consequences:

- `&&` cannot be fat-fingered, because there is nowhere to put it.
- An unmigrated database **cannot start**, so the failure is a short message at
  deploy time instead of a 200-frame SQLAlchemy traceback during your demo.
- The build step is only `pip install`, so there is nothing to remember.

`serve.py` also prints `Database is at head.` before binding, which is the line
to look for in the Render log when a deploy misbehaves.

**Environment**

| Key | Value |
|---|---|
| `DATABASE_URL` | `postgresql://…` — SQLite will not survive a redeploy |
| `JWT_SECRET` | Generate; Render fills it |
| `CORS_ORIGINS` | Your Vercel origin, e.g. `https://your-app.vercel.app` |

Two traps that cost real time:

- **Never hardcode `--port`.** Render injects `$PORT` per service. A hardcoded
  10000 or 8000 binds the wrong socket and the health check never passes.
  `serve.py` reads `PORT` for you.
- **Never put `&&` in a Start Command.** Covered above.

`JWT_SECRET` falls back to a development key when unset so the local demo works
with no setup, and logs a loud `WARNING` when it does. On a deployed instance,
set it.

---

## What is not built

Honesty is more useful than a full feature list.

- **The research record has 36 open source gaps.** Retention and defect-liability
  percentages, the Gujarat Delegation of Powers, the Public Works Manual
  (557pp + 735pp annexures, corrupt text layer), 28 QC form names, the
  per-component defect taxonomy and service life. These are marked
  `NOT ESTABLISHED` and the system returns 501 rather than guessing. Some are
  permanently unobtainable.
- **No defect taxonomy.** IRC:SP:35-2024 defines 62+ distress types and a
  weighted Bridge Health Index, but no Gujarat document references any SP:35
  edition. Adopting a score Gujarat has never adopted would be the exact
  fabrication this project exists to avoid.
- **Closure is load-capacity-conditional, never score-conditional.** Pocket Book
  §10.8.3: restrict to assessed capacity with 6-monthly special inspection, close
  where rated capacity is below expected traffic load, or strengthen. Never
  auto-close on a BHI.
- **No photo upload.** The World Bank's criticism of the existing system is that
  it is *a catalogue of photographs*. This system is deliberately the data layer
  beneath that, not the catalogue.
- **The two `Orsang River Bridge` rows are intentional.** Two bridges, same name,
  different codes, different districts. A real register has those.

### Claims that are barred

Do not put these on a slide or in an interview:

- **1,441 and 6,768 bridge counts.** Unsourceable. Only 7,185 holds.
- **"34.5 years average bridge age."** Fabricated across all 65 IRC documents
  reviewed. The sourced substitute is IRC:SP:35-2024 §1.1's own hedged *"about
  25% of the bridge stock is in some form of distress"* — quote the hedge.
- **Cement and Steel carrying weight in Major Bridge price variation.** For
  Major Bridges they carry **zero**; the weights are Labour 20%, Bitumen 15%,
  Fuel 10%, Other materials 40%, Plant 15%. Counter-intuitive, and the detail
  that distinguishes research from assumption.

---

## Further reading

| Document | What it settles |
|---|---|
| [`docs/research_3phase_opencode.md`](docs/research_3phase_opencode.md) | The evidence record. Every rule traces here. |
| [`docs/decisions.md`](docs/decisions.md) | D-001 … D-022, with alternatives and trade-offs |
| [`docs/architecture.md`](docs/architecture.md) | Components, data flow, failure boundaries |
| [`docs/database.md`](docs/database.md) | Entities, constraints, indexes and why each exists |
| [`docs/api.md`](docs/api.md) | Endpoints, authorization, failure cases |
| [`docs/demo-script.md`](docs/demo-script.md) | The 3m30s demo, with a "do not say" list |
| [`HANDOFF.md`](HANDOFF.md) | Current state and the exact next action |

Interactive API docs run at `/docs` on a live instance.
