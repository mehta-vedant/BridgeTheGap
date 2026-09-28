# Decision Log

Durable architecture and product reasoning. One entry per meaningful
decision, newest last.

Each entry records: Context, Decision, Reason, Alternatives considered,
Trade-offs, Future reconsideration trigger.

---

## D-001 — Hackathon skills are project-scoped, not user-global

**Status:** accepted

### Context

Ten skills form the hackathon operating system:

```text
problem-analysis      research            architecture-design
database-design       api-design          frontend
production-review     demo-readiness      interview-defense
handoff               resume-work
```

These had to live somewhere. Two candidate locations existed: a
user-global skills directory on this machine, or this repository's
`.agents/skills/`.

### Decision

All ten live in `C:\pravi\.agents\skills\`, versioned with the repository.

The user-global skills directory is reserved for genuinely universal
utilities that carry no project context, for example:

```text
generic code review
generic commit-message helper
generic shell troubleshooting
```

### Reason

These skills are not tools that happen to be useful during a hackathon.
They *constitute* the hackathon operating system. They encode the
sequence in which work must happen, the documentation contract in
`AGENTS.md`, and the handoff protocol. That is project knowledge.

Three concrete consequences of project-scoping:

1. **They travel with the repo.** Clone the repository at hackathon start
   and the full operating system is present. Nothing to install, nothing
   to remember, no per-machine setup step.
2. **They stay versioned.** Skill changes are reviewable, diffable, and
   revertible like any other change. An operating system that lives in
   someone's home directory cannot be reviewed in a pull request.
3. **They stay consistent across agents and teammates.** Codex and
   OpenCode resolve the same files, so both agents enforce the same
   contracts. A user-global skill silently differs per machine, which
   defeats the purpose of a shared operating system.

### Alternatives considered

**User-global directory** — rejected. Works, but creates a hidden
dependency on one machine's configuration. A teammate or a fresh CI runner
would silently lose the entire operating system, with no error to signal
it. Also unversioned, so there is no way to know which version of a skill
produced a given piece of work.

**Duplicate into both locations** — rejected. Two copies drift, and the
drift is silent. A team member running a stale global copy would apply
different rules than the repo documents, which is worse than either
option alone.

### Trade-offs

Accepted costs:

- The skills only exist inside this repository. Working on an unrelated
  project does not inherit them. Accepted, because these skills are
  deliberately hackathon-specific and would be dead weight elsewhere.
- Adding a skill requires a commit rather than a local file drop. Slightly
  more friction, in exchange for reviewability. During a fast hackathon
  this is worth it: an unreviewed operating-system rule is a rule nobody
  can reason about under pressure.
- `AGENTS.md` and the skills can drift out of sync. Mitigated by having
  skills reference `AGENTS.md` sections rather than restate them.

### Future reconsideration trigger

Reconsider if either becomes true:

- The skills become generally useful for non-hackathon work, which would
  argue for a user-global copy of a trimmed subset.
- A second repository needs the same operating system. At that point
  extract the shared skills into their own versioned package or repo and
  consume them as a dependency from both, rather than copying.

---

## D-002 — One folder; no git repository until official kickoff

**Status:** accepted

### Context

This repository holds the pre-hackathon engineering toolkit. It will also be
the folder the hackathon product is built in.

An earlier draft of the design assumed two locations: a permanent toolkit at
`C:\pravi` that was versioned freely, and a copy into
`C:\hackathons\<project>` for the submission. Under that model, toolkit
history and submission history were cleanly separated.

A concern was then raised that a hackathon evaluator inspecting Git history
should not see commits made the night before. That is a real risk, but the
two-folder model was solving it with a procedural guarantee: the operator had
to remember to exclude `.git` when copying. A procedural guarantee fails at
3am, which is precisely when a hackathon copy is made.

### Decision

**There is one folder, and it is not a git repository until official
kickoff.**

```text
C:\pravi   toolkit files on disk, no .git, no commits
              |
          official start
              v
           scripts\kickoff.ps1  ->  git init, branch main, no commit
              v
           first commit, only once the problem statement is in hand
```

Supporting decisions:

- **No copy step, and no second location.** The copy was the weak link. With
  no `.git` present, even a naive folder copy is safe, because there is
  nothing to leak.
- **The `handoff` and `resume-work` skills were patched** to detect a
  missing repository and fall back to filesystem-only state capture. Both
  previously assumed `git status` and `git log` would work.
- **`scripts/kickoff.ps1` / `scripts/kickoff.sh` initialize the repository
  but create no commit by default.** Making the commit opt-in means the
  default action at kickoff cannot contaminate the history.
- **`AGENTS.md` section 1 carries a "Pre-Hackathon Boundary" rule** stating
  that no git repository and no problem-specific implementation may be
  created before the official start. It is a subsection of section 1 rather
  than a new numbered section, so the existing cross-references to sections
  15, 20, 23, and 24 remain valid.

### Reason

The guarantee becomes structural instead of procedural. There is no
contamination *possible* rather than contamination *avoided*, which is the
right trade when the cost of being wrong is a poor impression with the people
evaluating the work.

It also collapses one moving part. Two folders meant a copy step, a naming
convention, a second location to remember, and a class of mistakes where the
wrong folder gets submitted. One folder with a delayed `git init` is the
same outcome with fewer ways to fail.

### Alternatives considered

**Two folders, toolkit versioned, copy excluding `.git`** — rejected. It
works, and it was the previous design, but it depends on remembering an
exclude flag. The whole point of this decision is to remove that dependency.

**Keep `.git` in the toolkit and rely on `new-project` scripts to exclude
it** — rejected for the same reason. The script reduces the risk but does not
eliminate it: a manual copy, a drag-and-drop, or a zip of the folder all
bypass it. Making the risky state unrepresentable beats making it unlikely.

**Keep `.git` and never create a remote** — rejected. An unused repository
still carries real costs (the two continuation skills break, and every future
editor assumes a repo exists). Removing it makes the state honest: this
folder genuinely has no history yet.

### Trade-offs

Accepted costs, stated plainly:

- **No version control on the toolkit during preparation.** The twelve
  skills, `AGENTS.md`, and the docs are being actively edited with no diff,
  no revert, and no history. An accidental overwrite is unrecoverable except
  through editor history. This is the real price of the decision, and it is
  the main argument against it.
- **Two commits were permanently lost.** `cc93dac` and `380baaa` were deleted
  when the repository was removed. Their content survives on disk, but the
  history does not.
- **The continuation skills run in their fallback path**, not their primary
  path, for the entire pre-kickathon period. They are correct in both modes
  but are less exercised in the fallback one.
- **`.gitignore` and `.gitattributes` cannot be validated** by git until the
  repository exists at kickoff. They were validated earlier while a
  repository was temporarily present, but should be re-checked at kickoff.

### Future reconsideration trigger

Reconsider if any becomes true:

- The toolkit grows large enough that losing an edit becomes a real and
  likely cost. At that point the better answer is to version the toolkit in
  a **separate private repository elsewhere on disk**, not to reintroduce
  `.git` here.
- Two or more hackathons need the same toolkit, which argues for extracting
  it into its own versioned package consumed by each submission repo.
- A submission ever requires demonstrating prior work, which would reverse
  the rationale entirely.

---

## D-003 — A dedicated research skill is required; no existing research skill could be reused

**Status:** accepted

> **Naming note, 2026-09-28.** The skill was ultimately written and shipped as
> `.agents/skills/research/SKILL.md`, not `research-brief`. The reasoning
> below still stands: no pre-existing research skill was available to reuse.
> `AGENTS.md` section 28 routes to `research`.

### Context

The original skill plan included `research-brief`. It was later proposed for
deletion on the grounds that a research skill already exists and reusing it
would be better than duplicating functionality, since duplicate skills drift
and conflict.

All four skills directories were searched:

```text
C:\pravi\.agents\skills
~\.agents\skills
~\.config\opencode\skills
~\.codex\skills
```

No `research` skill exists in any of them.

### Decision

Create `.agents/skills/research/SKILL.md`, project-scoped per D-001.

The skill will **delegate** to existing research tooling rather than
reimplement it. Available capabilities: `firecrawl_search` and
`firecrawl_scrape` for web research, and `context7` for library
documentation. The skill's job is to decide *what* to search, *when* the
search is worth the time, and *what to record*; the tools already know *how*
to fetch.

### Reason

The anti-duplication argument was sound in principle but rested on a false
premise. Nothing was available to reuse, so the choice was never "duplicate"
versus "reuse" but "cover the phase" versus "leave a hole".

The gap matters more than usual here. `AGENTS.md` section 3 names
`docs/research.md` as one of three primary problem-analysis documents, and
`problem-analysis` is the first workflow run once the problem statement
lands. Skipping research would leave the first 30 to 45 minutes of the
hackathon without a documented method, at exactly the point where momentum
matters most.

Delegating to `firecrawl` and `context7` honours the original intent of the
proposal: no duplicated capability, only a documented workflow around tools
that already exist.

### Alternatives considered

**Skip it and rely on ad hoc `firecrawl_search`** — rejected. It leaves
`docs/research.md` an empty placeholder, leaves `AGENTS.md` section 3
pointing at a document nobody writes, and puts the quality of the opening
phase at the mercy of whichever agent happens to be running.

**Merge research into `problem-analysis`** — rejected for now. They answer
different questions: problem analysis is about *this* problem's actors and
scope, research is about *the existing solution landscape*. Splitting them
keeps each workflow focused. Worth revisiting if time pressure proves the
extra skill invocation is not worth it.

### Trade-offs

- Two skills to read instead of one at the start of the event. Minor, since
  both are short and the first agent reads them once.
- A small risk of duplicating `firecrawl` usage patterns. Mitigated by
  writing the skill as a decision procedure, not a tool tutorial.

### Future reconsideration trigger

Reconsider if a genuine general-purpose research skill is later installed
user-globally. At that point, either delete `research` in favour of it,
or narrow `research` to be purely about *competitive and technical
landscape* research specific to hackathon problem framing.

---

## D-004 — Database design and API design are separate skills

**Status:** accepted

### Context

The original plan had a single combined `database-api` skill. The split into
`database-design` and `api-design` was proposed because they answer
substantially different questions.

### Decision

Two separate skills.

**`database-design` answers:**

```text
What entities?
What relationships?
What constraints protect the invariants?
What indexes, and which access pattern does each one serve?
Where are transactions required, and what must be atomic?
```

**`api-design` answers:**

```text
Which endpoints?
What method and payload shape?
What authentication and authorization?
What is idempotent, and what are the side effects?
How are errors shaped?
```

### Reason

They interact, but they are not the same activity. A schema decision is
usually driven by invariants and access patterns; an endpoint decision is
usually driven by a client workflow and an authorization boundary. Merging
them produces a skill that is long, has two distinct outputs, and gives an
agent no clear signal about which half it is currently doing.

Separate skills also produce separate documents. `AGENTS.md` section 20
already requires both `docs/database.md` and `docs/api.md`, and section 6 and
section 7 treat them as distinct concerns. One skill writing two unrelated
documents invites a shallow job in both.

### Trade-offs

- An extra skill invocation between the two.
- A risk of drift between them: the schema and the endpoints must agree. This
  is handled by having both reference `docs/architecture.md` for the shared
  component boundaries, and by `api-design` explicitly reading the schema
  before finalising payloads.

### Future reconsideration trigger

Reconsider if, in practice, the data model is small and entirely
deterministic given the endpoints, making the separate schema pass
ceremonial. In that case a combined skill with two short phases would be
faster.

---

## D-005 — OpenCode MCP surface: four connected servers, everything else disabled

**Status:** accepted

### Context

The OpenCode global configuration at
`~/.config/opencode/opencode.jsonc` had accumulated nine MCP servers, most of
which were failing or unused:

```text
✓ context7  ✓ firecrawl  ✓ github  ✓ notion  ✓ playwright
✗ jira      ✗ postgres   ✗ shadcn (Request timed out)
```

Three further problems were found by reading the file against the OpenCode
V2 documentation:

1. Seven of the nine servers sat **directly under `mcp`** rather than under
   `mcp.servers`. V1 compatibility kept them working, but it is the wrong
   shape and it hid a duplicate: `playwright` was defined twice, and the
   `mcp.servers` copy ran `npx @playwright/mcp@latest` **without `-y`**.
2. `"enabled": true` was set on seven servers. V2 has no `enabled` field; it
   uses `disabled`. The field was a silent no-op.
3. `"plugin"` was written instead of `"plugins"`, so
   `@techdivision/opencode-plugin-shell-env` was very likely never loading.

A Context7 API key was also hardcoded in plaintext in an `Authorization`
header, which contradicts `AGENTS.md` section 15.

The same defect explains the shadcn timeout. `npx shadcn@latest mcp` without
`-y` prompts for install consent, and a prompt inside a non-TTY stdio server
hangs until the startup timeout expires rather than returning an error.

### Decision

Connect four servers. Disable, do not delete, the rest.

```text
✓ context7    connected   remote, OAuth
✓ github      connected   local, token from {env:GITHUB_TOKEN}
✓ playwright  connected   local, single definition, -y
✓ shadcn      connected   local, -y, timeout.startup 60000
○ firecrawl   disabled    enable when the research skill needs it
○ notion      disabled
○ jira        disabled
○ postgres    disabled
```

Supporting changes:

- All servers moved under `mcp.servers`.
- Duplicate `playwright` removed; every `npx` invocation gained `-y`.
- `enabled` removed; `disabled: true` used where a server should stay dark.
- `plugin` corrected to `plugins`.
- The hardcoded Context7 bearer token deleted. Context7 is a remote server,
  so OAuth applies and no key needs to be stored in configuration.
- `.env`, `.env.*` and `opencode.jsonc.bak-*` added to the config
  directory's `.gitignore`, which previously did not ignore `.env`.

### Reason

MCP tools consume model context, and every connected server is reachable by
the agent whether or not the current task needs it. During a
time-constrained hackathon that is a real tax. A failing server also costs
startup time and emits a misleading error on every launch.

`disabled` rather than deletion because each of these is one flag away from
use, and because a disabled server connects nothing and therefore costs no
context. Deleting would make re-enabling a rewrite rather than an edit.

`firecrawl` is disabled rather than enabled because the rule for keeping it
was "only if the research skill uses it", and the research skill was still
unwritten. The condition was evaluated rather than assumed.

### Alternatives considered

**Delete `jira`, `postgres`, `notion` outright.** Rejected as irreversible
during the event for no gain. The problem was connection and context cost,
which `disabled` already solves.

**Keep `firecrawl` connected on the assumption that research will need
it.** Rejected. Enabling on an unmet condition spends context on a guess.

**Keep the Context7 key, just move it to `.env`.** Rejected. Context7 is a
remote server and OAuth is on by default, so a key is not required at all.
Verified after the change: `context7` reconnected without the header.

**Configure a second GitHub integration for Codex.** Rejected. GitHub MCP
was already connected in both agents.

### Trade-offs

- Disabling `notion` breaks any workflow that had come to depend on it. It
  was not part of the hackathon toolkit, so nothing referenced it.
- The Context7 key was stored in plaintext and, during diagnosis, printed
  into an agent transcript. It must be rotated at the provider regardless of
  this config change.
- `disabled: true` entries still sit in the file. A future reader must
  understand that disabled means configured-but-dark, not absent.

### Future reconsideration trigger

Enable `firecrawl` as soon as the research skill is written, since D-003
already commits the team to delegating research to `firecrawl_search` and
`firecrawl_scrape`.

Reconsider the whole set if the problem statement turns out to require a
live database, issue tracker, or document store. Enable that one server at
that point rather than pre-emptively.

Reconsider `shadcn` if the team does not commit to Tailwind. It contributes
7 tools and little value without a `components.json`.

---

## D-006 — No pre-built starter templates before the problem statement

### Context

An attempt was made to build reusable `templates/frontend` (Next.js 16,
React 19, Tailwind v4) and `templates/backend` (FastAPI, SQLAlchemy 2, Alembic)
starters ahead of the event, on the reasoning that they would save setup time
at hour zero.

Both were built and verified working: the backend passed 9 tests and a clean
Ruff run, the frontend passed install, typecheck, lint and build. They were then
deleted.

The original motivation had a flaw. It was presented as resolving the open gap
in `problem-analysis` Phase 12, which evaluates a "default stack" that is
defined nowhere. Building a pinned Next.js and FastAPI starter does not resolve
that gap. It pre-commits to an answer, which is the opposite of resolving it.

### Decision

No starter templates, project templates, or CI workflow templates are committed
before the official problem statement is in hand.

The technology findings that came out of building them are preserved in
`docs/known-issues.md` as stack-independent landmines: the ESLint 10 crash, the
psycopg 2 and 3 mismatch, Playwright artifact pollution, and the rest.

The undefined "default stack" in `problem-analysis` Phase 12 is closed by
writing down a selection *procedure*, not by shipping a stack.

### Reason

`AGENTS.md` section 4 requires the technology stack to be selected from the
problem, and states that Next.js, FastAPI and PostgreSQL are "defaults, not
mandatory choices". Shipping pinned versions of exactly those three converts a
stated default into a de facto mandate, and does so before anyone has read the
problem. A team that copies the template has not evaluated a stack; it has
inherited one.

The templates also fail the "smallest useful" test. A problem needing only a
server, or only a single-page app, or no web frontend at all, would find roughly
thirty files of deliberate non-use. A generator run at hour zero costs a couple
of minutes. The asymmetry is not close.

The pre-hackathon boundary in `AGENTS.md` prohibits pre-building likely
solutions. Generic infrastructure was judged permissible on the grounds that it
encodes no domain logic. That judgement was too generous: a pinned stack is a
solution to a problem not yet chosen.

### Alternatives considered

**Ship the templates and document when to discard them.** Rejected. The cost of
a wrong pre-commitment is a slow, guilt-laden decision during the event, which
is worse than a two-minute setup.

**Ship a neutral "pick a stack" decision record and templates later.** Rejected
only in the sense that it is the actual plan; the procedure is written during
problem analysis, against the real problem.

**Keep only the backend, or only the frontend.** Rejected as a distinction
without a difference. The objection is the stack pre-commitment, which applies
equally to either half.

### Trade-offs

- Setup work is repeated at hour zero. Accepted: minutes, against the risk of a
  team building against a stack nobody chose.
- The verified dependency versions in the deleted templates are gone. The
  relevant ones are recorded in `docs/known-issues.md`; the rest are recoverable
  from the generators, which is where they should have come from anyway.
- Templates remain worth building *after* the stack is chosen, at which point
  they encode a decision rather than predating one.

### Future reconsideration trigger

Once `docs/architecture.md` records a chosen stack, build templates for that
stack and only that stack. Revisit this decision if two consecutive hackathons
on this workspace converge on the same stack, which would make the template
reusable rather than speculative.

---

## D-007 — Asset class is bridges

**Status:** accepted by the team, 2026-09-28

### Context

The brief asked for an end-to-end physical asset inventory. Four rounds of
research narrowed the scope as follows.

| Round | Question | Outcome |
|---|---|---|
| 1 | Which of 8 generic infrastructure classes? | DC hardware and end-user devices tied at 7.44 |
| 2 | Sponsor clarification: government assets | Cloud and SaaS eliminated *on definition* — they are intangible under IPSAS 31 and cannot be the subject of a physical register |
| 3 | Which government class? | Vehicles & fleet led — deepest statute-traceable process, 5–7 approvals per asset |
| 4 | Sponsor clarification: Gujarat R&B Department | Vehicles out of remit as a centrepiece. Construction plant & machinery led on score. |

In round 4, research on the R&B estate produced two findings that reshaped
the field entirely:

- **Roads and bridges are not depreciable.** CAG's own guidance is that
  *physical assets are not depreciated and losses at end of life are not
  expensed.* A product built on book value and end-of-life loss has **no
  accounting substrate on roads.** The lifecycle framing is actively
  contradicted by the accounting.
- **Gujarat has a mandated, written, cited bridge inspection process that
  demonstrably failed.** The R&B Department's own 1990 circular requires
  district engineers to inspect bridges twice yearly, and makes the signing
  engineer **personally liable**. That process did not prevent the 9 July 2025
  Gambhira collapse, in which an inspection **two months prior documented the
  damage and triggered no closure.**

### Decision

**Single asset class: bridges owned by a Gujarat R&B division.**

Not roads. Not buildings. Not construction plant and machinery. One class,
implemented end to end.

### Reason

The selection was made on a published 10-criterion rubric, recorded in
`docs/research-bridges.md` section 1. Bridges win on the three criteria that
the scoring axis actually rewards:

1. **Depth of process.** A mandated two-a-year inspection cycle with a
   personally-liable signatory, a condition grade, a defect classification,
   and a sanctioned work decision with a cost. This is a *process*, not a
   data-entry exercise, and it is written down in a circular that can be cited
   in the judging room.
2. **Explainability.** *"The inspection found the crack in May. The bridge
   collapsed in July. Nobody closed it."* A judge with zero domain knowledge
   understands that in one sentence, and it is true.
3. **Auditability of the failure.** The causal chain from missing inspection
   data to collapse is documented end to end by a state legislature, a
   High Court, a Public Accounts Committee, and a Supreme Judicial
   Committee. We are not inferring a problem; we are citing one.

### Alternatives considered

| Alternative | Why not |
|---|---|
| **Construction plant & machinery** | Scored marginally higher. Rejected in favour of bridges for a reason worth stating: machinery's evidence base is thin and almost entirely non-Gujarat, while bridges has a *Gujarat-specific mandated process and a Gujarat-specific documented failure.* Scored against the sponsor's actual institution, bridges is stronger. |
| **Vehicles & fleet** | Strongest statutory depth, but off-message for a Roads & Buildings Department. Recommending a fleet product to a roads department reads as not having read the department. |
| **Roads** | Rejected on the accounting finding above. No serials, no individual condition grade, no lifecycle state. A road is a network segment, not an asset. |
| **Government buildings** | A building is closer to a *location* than a unit. Far weaker unit identity, and far fewer per-unit process gates. |
| **All four classes** | Would produce the lowest common denominator: a table with a status column. Unifying immovable and movable holdings deletes the process, because the process only exists in the gaps. Explicitly rejected. |

### Trade-offs

- **Genuine incumbent risk.** MoRTH's **IBMS** already owns bridge inventory,
  condition assessment, and prioritisation nationally. The prototype must be
  explicit that it is not IBMS. See the known-risk note below.
- **Data must be synthesised.** No open unit-level government asset register
  exists for any class. Real data is available for *locations and network
  statistics only*. The demo must be transparent about which fields are real
  and which are simulated — see `docs/research-bridges.md` section 8.
- **We are building after the fact.** The Gambhira collapse is July 2025. A
  prototype appearing afterwards must be framed as addressing a *standing*
  failure, not reacting to a news event. Phase 3 in `docs/problem.md`
  records that the process failure predates it by decades.

### Known risk, and its resolution

**IBMS is a real national incumbent and our asset class overlaps it.** The
defensibility of this decision rests entirely on the layer IBMS does not own.

When this decision was taken, the gap was an unverified assertion and was
recorded as a **P0 verification item**: confirm that IBMS covers inventory and
condition and does **not** block an unsafe structure from remaining in service.
"If IBMS already enforces that, this decision is wrong and the class changes
before implementation."

**Research has since resolved it, in the incumbent's favour but not fatally.**

- IBMS does national inventory, condition assessment, health indexing, and
  maintenance prioritisation across roughly 1.62 lakh structures. It is good.
- RAMS describes its Bridge Information System as a *"data repository for
  bridge and culvert inventory and condition including brief details on
  maintenance and priorities."* Repository language, not decision-record
  language.
- The MoRTH circular of 25 June 2026 adds as-built drawings, mandates DPR
  consultants to input data, and introduces a mobile app. **More data, still no
  gate.**
- **The seam is measurable.** IBMS inherits the 1987 MoRTH inspection proforma,
  whose **Item 23 — "position of recommendations of previous inspection" — is
  reported by a field practitioner to be the field most often left blank.** That
  is precisely the field an inquiry would need to establish whether a known
  defect was carried forward.
- India's own road asset management standard, **IRC:130-2020, states in its
  scope that it "does not cover Bridge Assets"**.

**Conclusion: the risk is downgraded, not dismissed.** The class stands. What
must not be claimed is that IBMS is absent or poor. The demo must open by
naming it, and then show the gate it does not have.

Full evidence and the complete borrowings ledger are in
`docs/research-bridges.md` §1.4 and §11.

### Consequential decisions taken at the same time

- **Borrow, do not reinvent.** The identity model, component ratings, and
  validation hierarchy are IBMS's, because the Gujarat field engineers already
  speak them and a prototype that invents a new vocabulary is a prototype
  nobody uses.
- **The product is a decision chain, not an inventory.** Structure →
  inspection → finding → need → scheme → work order → acceptance, with a
  mandatory recorded rationale on every decision. CG 302 in the UK comes
  closest to this and still has no `rationale` field. It is genuine white
  space, not a feature nobody wanted.
- **The enforcement layer is the deliverable.** Second-person QC on every
  inspection, computed inspection intervals, a critical-finding escalation
  clock, and a hard gate preventing a critical structure returning to service
  without a recorded, reasoned, approved decision.

### Future reconsideration trigger

The first trigger has been tested and did not fire: IBMS was found to be a
data and prioritisation system without a service-blocking gate, so the class
stands.

Revisit this decision if:

- Gujarat R&B is found to operate a bridge management system that already
  captures the full lifecycle history **and** decision rationale with an
  enforcement gate, closing the gap this project intends to occupy. This is
  the live trigger. **Gujarat R&B's own systems could not be verified during
  research** — the department's domains failed TLS validation and one did not
  resolve. Check this by hand before the deck is written.
- The lifecycle research pass establishes a mandated state or decision model
  that is materially incompatible with the provisional state machine in
  `docs/research-bridges.md` §4.7.

---

## D-008 — Lifecycle scope boundary, and the cost model

**Status:** accepted, 2026-09-28
**Amended:** 2026-09-28, same session. The original boundary excluded
construction and tendering entirely. That was too aggressive and was
corrected — see *Amendment 1* at the foot of this entry, which supersedes
*Decision part 1* only. Parts 2 and 3 stand unchanged.

### Context

The brief asks for assets tracked "across their entire lifecycle." Research
had converged on bridges with a deep inspection-and-enforcement process, and
there was a real risk of having quietly narrowed the product to inspections in
order to make a ten-hour build comfortable.

That would have been a mistake. **Cost is the best-evidenced part of this
entire research base**, and every major Gujarat audit finding already has a
rupee figure in it:

| Finding | Figure | Source |
|---|---|---|
| Maintenance norms flouted | **199%-346% above** norms; 161 works granted time extension with no liquidated damages recovered | CAG Gujarat Civil Report 2001, Ch. IV |
| Capital blocked in stalled projects | R&B **Rs. 11,146 cr** capex; **168 projects >= Rs. 10 cr incomplete**; Rs. 5,194 cr spent against Rs. 7,353 cr estimated | CAG SFAR 2023-24 |
| Sanctioned repair not executed | Gambhira: **Rs. 212 cr replacement approved before the collapse**; sanctioned four days after it | State of Gujarat's own account |
| Wasteful expenditure | Rs. 1.35 cr avoidable; Rs. 73.04 lakh lease premium; Rs. 112.37 lakh unfruitful; **Rs. 2.78 cr idle or blocked** | CAG Gujarat Audit Report No. 4 of 2014 |
| Forward-looking record schema | Five-part maintenance record with estimated cost, recommended action date, and a 60-year plan **with assumptions recorded** | UK CG 302 |
| Valuation discipline | Four valuation approaches; investment-backlog estimation; network vs project decision levels | IRC:130-2020 |

A product that cannot produce these numbers per asset is leaving the strongest
available evidence on the table.

### Decision

Three parts.

**1. The lifecycle boundary is explicit.** The register begins at
**OPENED TO TRAFFIC**. Construction is an **immutable provenance block** —
contract cost, year, contractor, design code, design life, as-built drawing
reference — captured once at entry and never managed as a phase.

> **Superseded in part by Amendment 1 below.** Construction and tendering are
> now in scope as provenance *plus one live gate*. The "captured once, never
> managed" rule still holds for everything except the defect liability period.

**2. Five cost ledgers, not "cost as a field".**

| | Ledger | Priority | Produces |
|---|---|---|---|
| C1 | Capital, read-only provenance | MVP | Contract cost, year, design life, as-built reference. Immutable. |
| C2 | Maintenance spend, accrued | MVP | Cost to date, cost per service-year, cost trend. Makes the 199%-346% finding per-asset. |
| C3 | **Deferred sanctioned work** | **MVP, highest value** | "Rs. 4.2 cr sanctioned 2024-03, not executed, 611 days overdue." The direct per-bridge answer to the PAC's 168 stalled projects. |
| C4 | Lifecycle projection, 60-year | Stretch | Next intervention and cost from condition trend and component lives, assumptions recorded. |
| C5 | Exposure at risk | MVP, **as a refusal** | Capital at risk, days critical, vehicles per day over an unsafe structure, district. |

**3. C5 reports three columns and refuses to collapse them into a rupee
figure.** No expected-value-of-a-life arithmetic, at any point, in any screen.

### Reason

**On the boundary.** In Gujarat R&B's own estate a bridge is usually handed
over already built, the construction agency is a separate entity, and
construction supervision is already covered by MoRTH's e-construction
machinery. Tracking construction properly would double the actor model, and the
actor model is where the demo time actually goes.

More decisively, the accountability asymmetry points the same way: MoRTH took
action against contractors in **13** under-construction failures and against
concessionaires in only **3** completed ones. *The spend and the punishment are
both at the front of the asset's life; the risk is in the middle and the
back.* A product that stops at handover is aimed at the part of the lifecycle
that is already supervised.

As-built provenance is still mandatory because CG 302 requires as-built
drawings, MoRTH's own 25 June 2026 circular now mandates them, design life and
design cost are inputs to every downstream calculation, and Gambhira's *1985*
is the first fact in the story.

**On C3.** It is the strongest cost feature in the product because it is pure
arithmetic on facts a government already holds. No estimation, no modelling, no
disputed assumption. A sanctioned scheme that has not been executed accrues
overdue days against its sanctioned value, and the sum over a division is the
blocked-capital figure the CAG reports in aggregate.

**On the C5 refusal.** A death has no defensible price. A government system
that publishes one is laundering a value judgement through arithmetic, and it
is the kind of thing that fails an interview on ethics rather than engineering.
Reporting rupees, days, and traffic as three separate columns, and declining to
multiply them, is both more honest and a stronger answer than the formula
would be.

**On retirement.** Decommissioning is a record, not a disposal workflow. The
auction is a commodity: GeM Forward Auctions has run Rs. 2,200 cr across 13,000+
auctions since December 2021, and MSTC operates the mandated e-auction service.
We reference the external process. We do not rebuild it.

### Trade-offs

- C4 is the only genuinely expensive item, because a defensible forward
  projection needs a deterioration model. It is deferred to stretch. **A
  projection without recorded assumptions is worse than no projection**, so if
  it is cut it is cut entirely rather than shipped as a guess.
- Funding C2-C5 means dropping the separate network-level and project-level
  decision screens from the MVP; the cost dashboard covers the aggregate view.
  The routine-maintenance task list simplifies to the tasks that generate costs.
- Provenance captured at entry cannot be corrected later without an audit
  trail. That is intentional.

### Future reconsideration trigger

Revisit if the sponsor states that construction-phase or land-acquisition cost
data must be in scope, since that would move the register boundary upstream and
require modelling the contractor and PMC as first-class actors. Also revisit if
a Gujarat R&B division can supply real sanctioned-versus-executed cost data,
which would convert C3 from a synthesised arithmetic demo into a genuine
finding.

---

### Amendment 1 — Construction and tendering are in scope, with one gate

**Recorded 2026-09-28, same session. Supersedes *Decision part 1* only.**

#### What changed and why

The team read *Decision part 1* as excluding construction and tendering from
the product, on the reasoning that a full construction management system is a
different product. That reading was wrong on the merits, for two reasons.

**First, the brief says "entire lifecycle," and a register that starts at
handover cannot honestly claim that.** A judge asking "you did the maintenance
half and called it a lifecycle product" would be right, and the answer would be
defensive.

**Second, the evidence is on the other side of the handover.** A bridge's
service-life condition is frequently *caused* by its construction:

| Case | Finding | Source |
|---|---|---|
| Karmanasa river bridge, NH-2, UP | Pier cap bracket failed 28 Dec 2019, **16 years after construction**; attributed to inadequate reinforcement, unregulated overloading and poor maintenance; **Rs. 41.52 cr** additional expenditure | CAG audit; CECR forensic review |
| Suktel high-level bridge, Odisha | Cracks from *"very poor and porous concrete"*; **collapsed April 2020 during dismantling**; Rs. 7.58 cr | CAG, Biju Setu Yojana |
| Odisha bridge works generally | **State Quality Monitors did not inspect 96% of bridge works; Third-Party Quality Monitors 80%**; 38% of UPV-tested locations doubtful; **25% below required compressive strength** | CAG |
| Rapar, Kachchh (2022-23) | *"Scouring in pier foundation… pier settled down"* | MoRTH PIB annexure, Aug 2024 |

The accountability asymmetry noted in D-007 cuts **for** including
construction as well as against it: MoRTH acts on under-construction failures
(13 instances) far more than on completed ones (3). A product that shows both
is more complete, because it demonstrates where accountability works as well as
where it does not.

#### The decision

**Record construction. Do not manage construction.**

Construction and tendering are in scope as **rich immutable provenance, plus
exactly one live gate**. The gate is the **Defect Liability Period**.

In a standard Indian road and bridge contract, construction ends at the
completion certificate, but the contractor remains liable for defects for a
further period. During it, a defect raised by the engineer must be rectified at
the **contractor's** cost, the contractor's **security deposit is at risk**,
and liability **expires on a date**, after which the department owns
everything.

**The DLP is where the two halves of the lifecycle overlap** — construction
liability still live while maintenance responsibility has already begun. It is
a real seam in the actual process, not one invented for this product.

#### The lifecycle as scoped

```text
 [P0] SANCTION       estimate, sanction note, budget head
     |
 [P1] TENDER         NIT -> tender -> L1 -> LOA        (closed, read-only)
     |
 [P2] CONTRACT       contractor, PMC, value, guarantees, security deposit
     |
 [P3] CONSTRUCTION  start -> milestones -> completion certificate
     |               QC summary, design code, as-built reference
     |
 [P4] DLP  <-- THE SEAM.  liability sits with the CONTRACTOR.
     |     defects must close at contractor cost.  security deposit at risk.
     |     DLP expires -> final completion certificate
     |
 [P5] HANDOVER       transferred to the maintenance wing.  Register opens.
     |
 [P6] IN SERVICE    ~~~ the twice-yearly inspection cycle begins ~~~
     |
     +--> CRITICAL ---> [GATE] --> CLOSED / LOAD RESTRICTED
     |
 [P7] WORK           maintenance / rehabilitation / strengthening, with cost
     |
 [P8] RETIREMENT     decommissioning record; disposal referenced externally
```

**The gate at P4 and the gate at P6 are the same gate** — different assignee,
different money, different end date. One piece of machinery, used at both ends
of the handover. This is what makes the lifecycle claim honest without
doubling the build.

#### What this does to the anchor case

Gambhira currently starts in 2025 with an inspection. In scope, it starts in
**1985**: who built it, under which contract, to which design code, with what
design life, **when the contractor's defect liability expired, and whether
anyone has looked at that record in forty years.** The bridge is now critical,
and the department has carried it alone since 1986.

That is something a condition register cannot do. It also sharpens the
register thesis: the 1,441 vs 6,768 discrepancy is not only about current
structures, it is about provenance back to construction. **A register that
cannot say when a bridge entered service cannot enforce a warranty, cannot
prove a design life, and cannot answer a negligence claim** — and IRC:130-2020
states that the record is the defence against exactly that claim.

#### Explicitly not built

e-tendering · bid comparison and evaluation · running-bill and payment
processing · contractor resource management · the full quality-control test
register · change orders and variations · PMC certification workflow ·
e-construction compliance · land acquisition · the auction itself.

Each is either already a government system or a product in its own right. This
list is the boundary, and it is not to be eroded.

#### Build cost and funding

| Item | Cost | Note |
|---|---|---|
| Tender and contract provenance | ~0 | Read-only fields, written once |
| QC summary, design code, as-built reference | S | A handful of fields |
| DLP defect flow and gate | M | **Reuses** the inspection-finding and work-order machinery, with a different assignee and a different closure rule |
| Construction-phase actor roles | S | Two role labels on the existing actor table: contractor, PMC |

**S + M total**, funded by the cuts already named above: the separate
network-level and project-level decision screens, and the routine-maintenance
task list.

#### The verification item this creates

**The defect liability period was not researched in the earlier passes.** The
12-24 month range and the security-deposit mechanics come from general Indian
construction-contract practice, not from a Gujarat R&B or MoRTH contract
document that has actually been read.

Before this reaches the schema, confirm against the actual Gujarat R&B works
contract: the DLP duration, what security is held and at what percentage, and
**whether DLP defects actually get closed or quietly lapse.**

That last question is the one that matters. If DLP defects routinely expire
unclosed in Gujarat, this is a second Gambhira. If they never lapse, the gate
is a formality. Either answer is useful. Neither is currently known, and
neither may be assumed.

#### Updated reconsideration trigger

This amendment adds one: if the sponsor requires live e-tendering or payment
processing rather than a record of a tender that has already concluded, the
construction phase must be dropped back to provenance-only, because the
tendering system is not a ten-hour build and is not this product.
