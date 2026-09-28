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
  scope that it "does not cover Bridge Assets"**. Quotable as evidence of the
  exclusion. **Never** quotable as authority for a rule about bridge records —
  see the correction note under D-008 Amendment 1 and D-009.

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
| Sanctioned work with zero delivery | **33 CRIF road projects sanctioned at Rs. 904.54 cr, expenditure reported: Nil** | RS US Q 1057, 4 Dec 2024 |
| Irregularity in Gujarat R&B money, full audit period | **Rs. 8.75 cr across 5 paragraphs** — Rs. 4.74 cr price-variation overpayment, Rs. 2.40 cr bonus, Rs. 2.21 cr bid-validity overrun, Rs. 1.62 cr curve widening | CAG Gujarat Rep. 1 of 2026, paras 3.6-3.11 |
| Sanctioned repair not executed | Gambhira: **Rs. 212 cr replacement approved before the collapse**; sanctioned four days after it | State of Gujarat's own account |
| Wasteful expenditure | Rs. 1.35 cr avoidable; Rs. 73.04 lakh lease premium; Rs. 112.37 lakh unfruitful; **Rs. 2.78 cr idle or blocked** | CAG Gujarat Audit Report No. 4 of 2014 |
| Forward-looking record schema | Five-part maintenance record with estimated cost, recommended action date, and a 60-year plan **with assumptions recorded** | UK CG 302 |
| Valuation discipline | Four valuation approaches; investment-backlog estimation; network vs project decision levels | IRC:130-2020, **borrowed as method only** — it is a roads-only standard and its scope excludes bridge assets, so applying it to a bridge register is an extension, not a citation |

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
| C3 | **Deferred sanctioned work** | **MVP, highest value** | "Rs. 4.2 cr sanctioned 2024-03, not executed, 611 days overdue." The per-bridge answer to 33 CRIF projects sanctioned at Rs. 904.54 cr with Nil expenditure reported. |
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
prove a design life, and cannot answer a negligence claim.**

> **Corrected 28 Sep 2026.** An earlier draft of this paragraph attributed the
> liability-shielding argument to **IRC:130-2020**. That was a misattribution and
> it has been removed. IRC:130-2020 is *Guidelines for Road Asset Management
> System* and its scope clause states it **"does not cover Bridge Assets."** It
> cannot be cited as authority for anything about a bridge record. The
> prohibition is still quotable — as evidence that India's own road asset
> standard excludes bridges by name — but never as a positive rule.
>
> The correct authorities are **IRC:SP 35** (inspection and evaluation of
> bridges) and **IRC:SP 40** (testing), and the argument should be made from an
> adjudicated fact rather than from a design standard. See D-009.

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

#### The defect liability period — corrected 28 Sep 2026

**The 12-24 month range in the original draft was wrong, and it was wrong in
the direction that made the product look smaller.** It has been replaced by
evidence read out of an actual contract document.

| Item | Value | Source |
|---|---|---|
| DLP, stand-alone structures and **major bridges** | **10 years** from the Completion Certificate | NHAI/MoRTH Standard EPC **Art. 17.1(d)** |
| DLP, ROB / RUB / rail bridges | **4 years** maintenance period | Indian Railways Railway Board letter No. 20221 CE-II/Bridge, 29 Dec 2025 |
| DLP deemed extended | *"till the identified Defects under Clause 17.2 have been remedied"* | Art. **17.5** |
| DLP failure, remedy | cost of rectification **plus 20% damages**, deductible from monies due | Art. **17.4** |
| Cure period after notice | **15 days** | Art. 17 |
| Retention | 6% deduction, **capped at 5% of Contract Price**; alternatively omitted with performance security raised 7.5% → 10% | EPC / footnote 11 swap |
| **Retention money released** | **within 15 days of the Completion Certificate** | EPC |
| Performance security | **5%** within 30 days of the Letter of Award | Art. |
| Completion Certificate issued by | **the Authority's Engineer**, not the contractor | Schedule-L |

Two consequences that must survive into the schema.

**1. The DLP is not a date, it is a predicate.**
`DLP_active = (start + 10 years) AND (open_defects == 0)`. Art. 17.5 makes an
open defect block expiry automatically, so the "do defects actually get closed
or quietly lapse" question has a contractual answer — the clock does not run
out while a defect is open. Whether Gujarat enforces it is a separate and still
unknown question.

**2. Retention does not back the DLP.** The cash leaves *before* the DLP starts.
The only security standing behind a 10-year liability is the **performance
security**. Any model that treats retention as DLP cover is wrong, and this is
also the most defensible thing to say out loud in an interview: the money is
gone by day fifteen and the risk runs for a decade.

> **Scope limit — this is not Gujarat R&B's contract.** The figures above are
> NHAI/MoRTH Standard EPC. Gujarat R&B tenders on **SBD/B-1 percentage rate
> form**, and the operative text sits in **GR TNC-1088-D-347-7-C**, which could
> not be opened. Gujarat R&B's own DLP duration, security percentage and
> retention terms are therefore **NOT ESTABLISHED** and must not be modelled
> from these numbers. See D-010.

**Still unknown and still not to be assumed:** whether Gujarat R&B actually
closes DLP defects or lets them lapse. No CAG paragraph stating that retention
was released while defects remained open has been found. What has been found
instead is a Himachal Pradesh bridge whose defect was noticed only *after* DLP
expiry, alongside pervasive CAG coverage of DLP working. That is suggestive,
not proof, and the gap is recorded in `docs/known-issues.md`.

#### Updated reconsideration trigger

This amendment adds one: if the sponsor requires live e-tendering or payment
processing rather than a record of a tender that has already concluded, the
construction phase must be dropped back to provenance-only, because the
tendering system is not a ten-hour build and is not this product.

---

## D-009 — The three-phase split is the *missing* taxonomy, not the established one

### Context

The sponsor's brief is split into pre-construction, construction, and
post-construction. D-008 built the product on that split. Before that split
became the organising principle of the schema, it was tested against every
document that actually defines Indian road audit practice.

**It is not the established taxonomy.** That is the finding, and it is the most
useful thing the cross-phase pass produced.

| Source | What it actually uses |
|---|---|
| CAG *Manual of Civil Audit Procedure 2023* (Principal Director of Audit — Infrastructure, whose portfolio includes MoRTH) | **No** pre- / construction / post-construction definition anywhere |
| CAG Report No. 19 of 2023, MoRTH, Bharatmala Pariyojana | Functional chapters: Conceptualisation & Planning · Fund Management · Award of Projects · Execution · Monitoring & IT. **Stops at execution.** No O&M chapter |
| CAG Report No. 8 of 2022, Karnataka, PWD road works | Planning · Sanction · Tender · Variations/Advances · Quality Control. **Explicitly excludes O&M from scope** |
| CAG Report No. 5 of 2021 Sikkim; No. 11 of 2022 Tamil Nadu | The only two flagship roads audits that reach maintenance — both cover *two* phases, not three |
| MoRTH | Uses "pre-construction activities" as a formal **cost category** (LS US Q 1975, 31 Jul 2025), not a lifecycle |
| RS Standing Committee 296th Report, 28 Jul 2021 | Recommended fixing accountability *"from the stage of drafting the project report till complete project execution"* — the whole span, as a **recommendation**, not current practice |

The audit universe, structurally, **ends when the contractor is paid.** O&M was
so clearly a separate problem that Parliament had to go back for it: the
Committee took up *"Operation and Maintenance of National Highways and
Management of Toll Plazas"* as a **367th Report in February 2024**, three years
after telling MoRTH to fix accountability across the whole lifecycle.

### Decision

**Adopt the three-phase split as the product's organising principle, and state
in every document and every demo that it is a proposal to close a documented gap
— never a description of how the sector currently audits.**

The thesis is not "we organised things nicely." It is the sanction table.

**13 structural collapses during construction. 3 structural failures of
completed or in-service structures.** MoRTH's own annexure to **Lok Sabha
US Q 3054, 18 Dec 2025** — 72 projects and stretches, 11 officers removed from
service. The 13/3 split is **our own row-by-row tabulation** of that annexure
(71 of 72 rows legible in the extracted text), not a published statistic. Its
original citation could not be found and must not be attributed to MoRTH.

The sanction asymmetry that follows is the argument:

| | Under construction | Completed / in service |
|---|---|---|
| Debarment ≥ 12 months | 4 cases | **none** |
| Designer-team debarment | 2 cases | **none** |
| Government officer suspended / transferred | 3 cases + 11 removed | **none listed** |
| Contract termination / PBG forfeiture | 3 cases | 1 case |

A girder that topples while being launched gets a **two-year debarment of the
designer team and the senior bridge engineer plus ₹1 crore** (#51,
Sangariya–Rasisar). A bridge that **falls in operation** gets **one month**
(#19, Kaali Bridge) — from the regulator's *own* expert committee, which found
the Independent Engineer's failure to run the mandated IRC SP 35 biannual
survey was a *"gross failure,"* that the collapse *"could have been averted,"*
and that the pre-event signature, **cantilever-tip droop at the central hinges,
was visible.**

Same agency. Same year. Same instrument.

> The Indian system knows exactly who to punish for a bridge that breaks while
> they are building it, and has no idea who to punish for one that breaks after
> they have finished.

### Reason

**The gap in the audit taxonomy and the gap in the sanction table are the same
gap**, and a three-phase view is the only structure under which a design
decision, a construction defect and an operational collapse can be traced to
one asset and one decision chain. If the taxonomy already existed, this would be
a feature request. It does not exist, which is what makes it a product.

It is also already conceded, twice, in fragments:

- The **Rajya Sabha Standing Committee (2021)** asked for accountability from DPR
  drafting through complete execution.
- **MoRTH's circular of 25 June 2026** did, by circular and without naming it,
  exactly what this product proposes: made **DPR consultants** mandatorily
  responsible for existing-asset condition data, made **condition data a
  precondition of as-built drawing submission and of payment**, and attached a
  **suspension of monthly payment** to both.

We are not arguing with the ministry. We are naming what it already did.

### Alternatives considered

- **Organise by asset class** — the obvious default, and what every existing
  BMS does. Rejected: it is the shape of the incumbent, and it cannot express
  accountability at all.
- **Organise by function or department** — matches how CAG actually writes.
  Rejected: it reproduces the boundary that is the problem.
- **Organise by audit chapter** — maximally defensible, and it stops at
  execution by construction.
- **Keep the split but describe it as current practice.** Rejected outright. It
  is false, it is checkable in an afternoon by anyone with CAG's site, and it
  would cost the entire interview.

### Trade-offs

- We give up the comfort of "everyone already does this." Every claim needs the
  taxonomy's absence argued alongside it.
- The 13/3 figure carries the weight of the argument and is **our
  recomputation**. It reproduces exactly, and it must always be presented as
  our tabulation of a parliamentary annexure — never as a government statistic.
- A Gujarat-only story is weaker: CAG found **₹8.75 cr** of money
  irregularity across 5 paragraphs in Gujarat R&B for an entire audit period,
  plus 21.43 ha of forest land diverted without permission. The department is
  low-value and low-publication. That is strategic, not a weakness — **the
  accountability layer we are adding does not exist today, in any form, so there
  is nothing to displace.**

### Future reconsideration trigger

If the sponsor's actual requirement turns out to be a single-phase maintenance
or inspection tool, the three-phase framing is overhead and must be dropped
back to provenance-only. If **CAG Gujarat Report No. 2 of 2026** (SFAR
2024-25, tabled 25 Mar 2026) turns out to contain a lifecycle or O&M chapter
for R&B, this decision is superseded on the spot — that report has been listed
but never opened.

---

## D-010 — Contract regime of record is NHAI/MoRTH Standard EPC, explicitly labelled as a substitute

> ## ⚠ AMENDED — see D-011. The GR was opened; the trigger at the foot of this
> ### decision has fired. Read D-010 and D-011 together. D-010 remains the record
> ### of what was known and believed *at the time*, and is not to be deleted.
>
> **Summary of the change:** Gujarat's own **security deposit (3%, banded)** and
> **performance bond (3%)** are now established and **override** the NHAI figures.
> The NHAI substitute survives only for the **escalation weights, milestone
> schedule, LD rate, Tests on Completion, DLP duration and retention %**.

### Context

D-008's DLP gate needs contract numbers. Gujarat R&B's own works contract
could not be opened: tenders issue on **SBD/B-1 percentage rate form** under
**GR TNC-1088-D-347-7-C**, and that document is not retrievable. Gujarat R&B's
own DLP duration, security percentage and retention terms are therefore
**NOT ESTABLISHED**.

Every figure in circulation — 5% performance security, 6% retention capped at
5%, 10-year DLP — is **NHAI/MoRTH Standard EPC**. Using them for Gujarat R&B
without saying so is the exact failure mode this repository exists to prevent.

### Decision

**Model contract mechanics on NHAI/MoRTH Standard EPC and MoRTH
Specifications. Label every derived figure, everywhere — schema comments, docs,
demo narration — as "NHAI/MoRTH; Gujarat NOT ESTABLISHED."**

Precedence where Gujarat-specific fact *is* established:

| Established for Gujarat R&B | Source | Overrides NHAI? |
|---|---|---|
| Two-cover (Technical & Price) tender, SBD/B-1 | live NIT | yes — tender structure |
| EE invites, **SE of the Circle opens** | live NIT | yes — approval chain |
| EMD = 0.1% of ECPT; tender fee ₹18,000 | live NIT | yes |
| Tendering via nCode / `tender.nprocure.com`, mirrored on `statetenders.gujarat.gov.in` | live NIT | yes |
| Contract form B-1 percentage rate | GR TNC-1088-D-347-7-C | yes |
| DLP duration, security %, retention % | — | **nothing. NHAI used as labelled substitute** |

> **The last row is now superseded by D-011.** Security % and the B-1 ceiling
> *are* established. **Only the DLP duration and the retention % remain
> substituted.**

The **three-layer approval chain** is Gujarat-established and is worth keeping
as a structural fact: **EE invites → SE of the Circle opens → Department
approves.** CAG Gujarat Rep. 1 of 2026 para 3.8 is the proof that it is three
layers and not two: a bid-validity miscalculation passed through Division,
Circle and Department uncaught, producing a ₹72.53 lakh cost overrun on two
works. The Division's reply was *"an oversight error due to workload."*

### Reason

The alternative is not modelling the DLP at all, and that deletes the **only**
mechanism connecting construction to post-construction — the seam the entire
product rests on. A labelled substitute is defensible in an interview. A silent
substitution is not, and an invented Gujarat number would be worse than both.

### Alternatives considered

- **Leave the DLP unmodelled.** Rejected: removes the seam, and with it the
  justification for treating construction as a phase at all.
- **Use CPWD GCC 2023** (5% PS within 7 days of LOI, <80%-of-ECPT treated as
  abnormally low). Rejected: wrong department, and Gujarat R&B does not use
  CPWD forms.
- **Infer Gujarat numbers from NHAI figures and present them as Gujarat.**
  Rejected — this decision exists specifically to forbid it.

### Trade-offs

An audience that knows Gujarat R&B contracts will recognise the substitution.
That is acceptable **provided we disclose it first.** Volunteering it converts
a vulnerability into the strongest available evidence that the rest of the
research was read rather than assumed.

### Future reconsideration trigger

Any successful opening of **GR TNC-1088-D-347-7-C**, or a sponsor-supplied copy
of the Gujarat R&B works contract, **immediately replaces this decision** and
every figure derived under it.

> ### 🔺 TRIGGER FIRED. GR TNC-1088-D-347-7-C was recovered in full, verbatim, by
> ### OCR from the official scan on 11-07-2017. See D-011 for the replacement
> ### decision and the amended precedence table.

---

## D-011 — Gujarat's own contract terms now override NHAI where established; the substitute narrows, it does not vanish

### Context

D-010 recorded that **GR TNC-1088-D-347-7-C could not be opened** and that Gujarat
R&B's DLP, security and retention terms were therefore `NOT ESTABLISHED`, with
NHAI/MoRTH Standard EPC substituted. Its reconsideration trigger has fired.

The departmental site `rnb.gujarat.gov.in` was reached directly. **Every resolution
on it is an image-only scan**; operative text was recovered by rendering at
300–450 dpi and OCR'ing. The four-resolution B-1 chain was recovered, the 2017
link of it in English and cleanly.

> **Method caveat, carried forward everywhere:** "recovered by OCR from the
> official scan" is **not** "verified against a certified copy." Gujarati
> instruments were **not** recoverable — no Gujarati OCR model was available —
> so those are reported as *letter located, operative text not recovered*.

### Decision

**Gujarat-established figures now override NHAI. The NHAI substitute survives only
where Gujarat remains unestablished. Both tracks are labelled, per figure, in
schema comments, docs and demo narration.**

**The amended precedence table — this supersedes D-010's table:**

| Contract term | Gujarat R&B value | Source | Status |
|---|---|---|---|
| Tender form | **B-1 percentage rate**; **B-2 item rate** | GR TNC-1088-D-347-7-C chain | **[V] established** |
| **B-1 monetary ceiling** | **₹12.00 cr road · ₹10.00 cr bridge & building**, "invariably on B-1 tender form only" | **GR TNC-1088-D-347-(7)-C dt 11-07-2017**, verbatim; Finance Dept concurrence 27-06-2017; signed N.G. Parmar, OSD (S.P) | **[V] established** |
| **Security deposit** | **2%** ≤₹2L · **2%** ₹2–5L · **3% ≥₹5L (2-yr BG)** · **5%** hydraulic/bund (5-yr BG). Penalty = the deposit then payable | **GR TNC-10-2013-3-(BHAG-2)-C dt 20-11-2013**, table recovered verbatim | **[V] established.** A bridge estimate is essentially always >₹5L, so **3%** is the operative case |
| **Performance bond** | **3%** of total contract amount | **GR PRC-10-2020-329-C dt 01-06-2021** — figure appears in title, subject and body | **[V] established** |
| **DLP location** | **SBD clause 33, "Identifying Defects / Defect liability period"** | **CIRCULAR C dt 11-12-2025**, file `RBD/OAS/e-file/16/2022/0002/Section C`; refs GR 30-04-2020 and 19-08-2024; બ્રિજ in scope | **[V] established** |
| **DLP duration** | — | SBD not published | **`NOT ESTABLISHED` → NHAI substitute (10 yr) stands, labelled** |
| **FMGP location** | **SBD sub-clause 17(B)(3)**, road work only | GR TNC-10-2013-3-BHAG-3-C dt 13-12-2013 | **[V] established** |
| **Retention %** | — | lives inside the unpublished B-1/SBD | **`NOT ESTABLISHED` → NHAI substitute stands, labelled** |
| Escalation weights, milestone schedule, LD rate, Tests on Completion | — | NHAI EPC / MoRTH specs | **`NOT ESTABLISHED` → NHAI substitute, labelled** |
| 120-day tender acceptance | GPWM cl. 212-A + GR 10-05-2013 | GR TNC-10-2013-02-C | **[V] established — and double-grounded, since CAG cites the same resolution** |
| **Price variation** | clauses 59/59A (B-2), 60/60A (B-1) | GR TNC-1089-4-C dt 21-10-2005; GR 24-03-2022 COVID relief | **[V] established — see D-013** |

> ### ⚠ The single most important correction in this decision:
> ### **Gujarat's security deposit is 3% and its performance bond is 3%.**
> ### NHAI's figures are 5% and 6%. **Using NHAI's numbers for a Gujarat bridge
> ### was wrong, and had it shipped, a Gujarat engineer would have known in
> ### one question.** This is precisely the failure D-010 was written to
> ### prevent, and it is the argument for the discipline.

### Reason

Two of the three contract figures that mattered most are now the department's
own, recovered verbatim from the operative instrument. The substitution was
correct as a method and wrong as an outcome — which is the correct outcome for
a method, since it is falsifiable and was falsified. What remains substituted is
narrow, specific and enumerable, and is labelled everywhere it appears.

### Alternatives considered

- **Retire the NHAI substitute entirely now that the B-1 chain is open.**
  Rejected: the chain touched **only the monetary ceiling**. The DLP duration,
  the retention % and the clause percentages live inside the unpublished SBD
  and B-1 form. Retiring the substitute would mean *inventing* Gujarat numbers —
  strictly worse than a labelled borrow.
- **Treat the OCR'd figures as certified.** Rejected. Image-only scans OCR'd at
  300–450 dpi are good evidence, not certified copies, and the record must say so.
- **Assume the NHAI retention of 6%-capped-at-5% carries over.** Rejected —
  §4A.3 shows Gujarat runs a **banded** security regime, so its retention rules
  may well differ. **Do not assume.**

### Trade-offs

The schema now carries **two labelled provenance tracks** rather than one. That
is more work and it is worth it: a single figure now always answers *"whose
number is this, and why?"*

### Future reconsideration trigger

A **photocopy or PDF of Tender Form B-1 / B-2, or the Standard Bidding Document**
— physically issued to every tendering contractor, and the single document that
closes the largest remaining gap. **Second trigger:** a readable copy of
**GR SSR-10-2017-50-C**, the GST clause-amendment tables, whose OCR failed at
every setting and which is the likeliest published home of the clause
percentages.

---

## D-012 — The frame we present is Gujarat's own `Sanction → Execution → Post-Completion`, not the American triad

### Context

D-009 established that the pre-/construction/post-construction split is **not** a
recognised Indian taxonomy and must never be described as current practice. That
left the product defending an imported vocabulary against an audience that uses
a different one.

A second, independent search has now run against Gujarat's own records: the
**full text** of the Gujarat SFAR 2024-25 (739 KB), **CAG Report No. 1 of 2026**
including its entire R&B chapter (701 KB), a CAG AAG report, **CAG G2012
chapters 2 and 3 (PWD)**, and the Karnataka PWD and Roads chapters.

> **Zero hits. In the department's own audit record, its own audit manual, and
> the national PWD audit guidance.**

One real qualification: **Karnataka's PWD/Roads chapter does contain a formal
"Defect Liability Period" concept.** The *vocabulary* exists in Indian practice.
The *phase split* does not. The only confirmed user of the exact triad anywhere
is **US FHWA Road Safety Audit guidelines** — **not Indian precedent.**

### Decision

**Adopt `Sanction & Clearance` → `Execution` → `Post-Completion` as the frame we
present, anchored to the budget's own 051/053 minor-head split, and hang our
three stages inside it. Never present the American triad as Indian practice.**

CAG does not audit by lifecycle phase. It audits by: (i) **sanction-to-order
timeliness** (the 120-day rule), (ii) **completion** (the ≥₹10 cr cohort),
(iii) **cost control** (PV, EPC bonus, avoidable over-widening), (iv)
**environmental compliance**, (v) **asset and fund accounting**. That is a
five-part audit frame our three stages map onto cleanly.

Gujarat's own budget already splits the lifecycle into **051 Construction** and
**053 Maintenance & Repairs**, and there is **no budget line for a
pre-construction phase** — it is capitalised inside 051.

### Reason

This is strictly stronger than defending the triad. It is a *refinement* of a
split the department already uses in its accounts rather than an import, and it
converts a liability into an asset: the same evidence that would have
falsified us now makes us look like we'd read the accounts.

The **051 finding is the sharpest version of the argument in the entire
research base**: the department's own accounting **cannot separate the phase our
product exists to manage.** Pre-construction cost is obtainable only from the
Administrative Approval and its sub-estimates, never from the accounts. That is
not a gap in the data — it is a gap in the *category*.

### Alternatives considered

- **Continue presenting the triad, with a footnote.** Rejected: the footnote
  does the apologising and the interviewer does the remembering.
- **Use CAG's five-part audit frame as our product frame.** Rejected: it is an
  auditor's frame, not a lifecycle, and "cost control" is not a phase.
- **Drop the phase split and ship a single works register.** Rejected: this
  deletes the seam the entire product rests on (D-008, D-009).

### Trade-offs

A reviewer who knows the American literature may find our labels
unfamiliar. Mitigation: the labels are Gujarat's, and we can show the 051/053
mapping. The framing also **narrows our claim**, which makes it easier to
defend — a smaller true claim beats a larger borrowed one.

### Future reconsideration trigger

Any CAG or MoRTH document defining a formal three-phase lifecycle taxonomy.
**Note that MoRTH's circular of 25 Jun 2026 already builds the phase seam by
circular and attaches a payment sanction to it** — if it acquires the word
"phase", this decision must be revisited.

---

## D-013 — The price-variation engine is the primary demonstration, because CAG asked the department to build it

### Context

CAG Report No. 1 of 2026 found that **Gujarat R&B has no works accounting and
management system**, and recommended the Department build one, integrated with
IFMS, with an automated PV Calculation Module pre-loaded with correct indices,
ceilings and data-range logic — naming **Odisha's WAMIS** as good practice.

Corroborating findings in the same report set: a **statutory** asset register
does not exist as a database, only the Gujarat Highways Act 1955 **s.8** paper
map in the Highway Authority office; the 2008 monthly-monitoring `.xls` files
**404**; and **₹71.07 cr of ₹71.96 cr (98.76%)** of Roads and Bridges receipts
under MH 1054 were **wrongly booked under MH 800 (Stock)**.

Gujarat's own PV rules are recovered verbatim and fully computable: admissible
only where **estimated cost > ₹25 lakh and time limit > 12 months**; **no PV in
the first 12 months**; **ceiling 5% of estimated cost less the value of Cement,
Steel and Asphalt**; escalation **`1.1^n`**; EPC variant **WPI/CPI + IOCL HSD +
refinery bitumen, Base Date = bid due date − 28 days**, claimed against the
Interim Payment Certificate.

And the department demonstrably gets it wrong: **₹4.74 cr overpaid across 11
works in 5 divisions** (Bharuch, Godhra, Kheda-Nadiad, Palanpur, Surat). The
Bharuch case interchanged the **Cement (122.5)** and **Steel (108.4)** index
bases — instead of recovering ₹15.57 lakh the Division **paid ₹40.13 lakh**, a
**₹55.70 lakh** arithmetic inversion in one cell of a formula. NH Division
Gandhidham paid **₹7.35 cr PV with ₹78.30 lakh excess**.

### Decision

**Build the price-variation engine first. Lead the demonstration with it. It is
the feature an auditor has already recommended in writing, against a failure
CAG has already quantified.**

Two supporting engines follow, both computable from rules rather than recovered
from a dead system, so neither carries legacy-data risk:

- **The Schedule-G dispute clock** — three stages, 7/7/7/9 = **30 days**,
  14/14/14/18 = **60**, 30/14/14/32 = **90**, escalating into the Legal arm.
  **Approved by the Chief Secretary on 17-01-2026.** Needs no data at all.
- **The QC/ATR engine** — **`S` / `SRI` / `U`** → ATR at **2 / 3 / 6 / 12
  months** → escalation → **Reconstruction** → **Red Card** to the contractor.
  Gujarat's own, verbatim (GR PRC-10-2017-31-C dt 26-05-2017, 28 standard forms).

### Reason

No demo beat in this project is better matched to a documented recommendation
from the auditor who audits the client. We are not asserting a gap; we are
filling one that was written down, and we can price the failure we prevent.

The Schedule-G clock and the QC/ATR engine earn their place for a different
reason: **both are computable from published rules, so neither depends on data
we do not have.** In a hackathon with no access to a client's systems, that is
worth more than feature breadth.

### Alternatives considered

- **Lead with the three-phase narrative.** Rejected as the *lead*: it is
  abstract, and the interviewer will ask what we actually built.
- **Lead with the register that lies.** Retained, demoted: it is the best
  *problem* slide but the fix is data entry, not a product.
- **Lead with the Karwar refusal.** Retained — it requires zero domain
  knowledge and lands in ten seconds, which makes it the right *opener*.

### Trade-offs

The PV engine is the most technically demanding item in the plan. If the clock
runs short it is the correct thing to cut, because it carries the most
implementation risk. But **cutting it first and keeping the narrative would
cost us the strongest single asset we have**, so the sequencing is: opener =
Karwar, lead = PV, problem slide = the register.

### Future reconsideration trigger

Publication of a Gujarat R&B works accounting or PV module. If one ships, our
contribution narrows to the per-asset layer CAG also found missing, and the
framing must change from *build the module* to *the register the module has
nothing to read*.

---

## D-014 — The actor model is nine wings and a real post chain, not three roles

### Context

D-009 and the earlier actor work assumed a small, readable set of roles. Gujarat
R&B publishes its organisation, and the published structure does not support a
three-wing model.

**Nine CE&AS-level wings**, each headed by a **Chief Engineer & Additional
Secretary** — one officer holding an engineering post in Additional Secretary
capacity. Plus **Expressway** and **SHDP-PIU**, revealed by the 2022
distribution list and **absent from the CE roster**.

**Published sanctioned posts:** CE 14 · SE(Civil) 35 · EE(Civil) 167 ·
EE(Elec) 15 · DyEE(Civil) 587 · DyEE(Elec) 40 · AE(Civil) 839 · AE(Elec) 53 ·
AAE(Civil) 538 · AAE(Elec) 48 · **Class III 6,709**.

**Non-technical actors that real resolutions name, and which are therefore real:**
**Divisional Accountant** (required member of evaluation **Committee A**),
**Financial Advisor** (required member of **Committee B**, **appointed by the
Finance Department**), Sectional Officer, Legal Executive, Additional Secretary
(Budget), Chief Secretary.

### Decision

**Model `person` separately from `post`; model `org_unit` as a tree with a dated
parent; model the real post chain; and treat non-technical actors as
first-class.**

Specific commitments, each earned from a source rather than invented:

- **CE&AS is one person holding two capacities.** The dual charge is real and
  published. Do not model it as two people.
- **`unit_kind` must separate works-administration circles from
  contractor-registration circles.** The 7 circles on the Contractor List page are
  evidenced as *registration* circles, because the 8,113-contractor register is
  partitioned by them. **Which registration circle maps to which CE is `NOT
  ESTABLISHED`. Do not collapse the two.**
- **`committee_member` is a dated association** with `from_date`/`to_date`, not
  a static array. GR dt 17-10-2022 substitutes *"any other Chief Engineer
  available in the Headquarter"* when the chair is unavailable — the committee is
  **bench-based** and resilient to absence.
- **A contractor's class is a dated history, not an attribute.** *Demotion to
  lower class* is an enforceable sanction (GR 13-02-1976).
- **A bridge's canonical name is human-authored and once-finalised, not
  auto-derived**, with a `naming_finalised_on` date. This is a real requirement
  extracted from a circular about **nameplate spelling** (PWM-2105-MP-219-(3)-C
  dt 17-10-1985, finalise within 15 days) — trivial on its face, and a genuine
  schema consequence.
- **≈9,045 total staff is our arithmetic** from the published post table, not a
  published figure. **No published rows exist for Civil Engineer, Supervisor,
  Draughtsman, Chainman, Mate or Labourer** — they sit inside the Class III
  6,709 bucket. **Flag, do not fill.**

### Reason

A three-wing actor model would not survive contact with a Gujarat division. And
the second-person verification gate — the thing the entire product thesis rests
on — only means something if the posts that perform it actually exist. **They do**,
and they are numerous, and several of them are non-technical.

**Financial Advisor and Divisional Accountant being mandatory committee members
is the single most useful fact here.** It proves the department does not confine
approval to engineers, which is what makes an independent-verification gate
institutionally plausible rather than invented.

### Alternatives considered

- **Model the three wings the sponsor's brief implied.** Rejected: contradicted
  by the department's own published hierarchy.
- **Flatten posts to a single `role` string.** Rejected: destroys the dated
  history that demotion and bench-based committees both require.
- **Infer the Class III sub-roles.** Rejected: not published. Filling them is
  exactly the confident invention this repository forbids.

### Trade-offs

Nine wings, eleven posts and a dual-charge convention is more schema than a
three-wing model. Accepted: an interviewer from the department will check the
org chart, and a model that survives that check is worth the extra entities.

**A `UNKNOWN_CE` placeholder is required for Expressway and SHDP-PIU.** Showing
a gap honestly is better than omitting the wings.

### Future reconsideration trigger

A readable copy of **GR PDW-3079-D-2959-BHAG-1-136-C** (Delegation of Powers to
Technical Officers, 17-04-2002, extended annually) — the Gujarati operative text
did not OCR, and it is **the authority table for the approval model.** Until
then, every `approval_matrix` row carries an explicit *"limit unknown — pending
GR text"* marker, and **no monetary threshold is invented.**

---

## D-015 — Schema traps we will not walk into

### Context

The Gujarat pass recovered enough of the department's real vocabulary to make
several confident-sounding schema choices *wrong*. Each of these is a plausible
detail that a Gujarat engineer would catch immediately, and each was a live
risk before the instruments were read.

### Decision

**The following are excluded or constrained, with reasons recorded so no later
agent reinvents them:**

| Item | Ruling | Why |
|---|---|---|
| **`eMD`** | **EXCLUDE** | **MGNREGA / Shram Sudhi vocabulary, not R&B.** Gujarat R&B says **EMD** — GR SSR/10/2015/17/C uses "EMD forfeited". An *electronic* MGNREGA-style eMD is not an R&B concept |
| **`challan`** | **EXCLUDE** | A tax/receipt instrument, not tender vocabulary. **R&B contractor receipts run through e-payment** (GR SSR-102017-57-C dt 30-04-2018, RTGS/NEFT) |
| **Measurement book, cash book, muster roll, stock register, works register, estimate register, correspondence register** | **MODEL, but label** | Canonical PWD/GPWM office procedure across essentially every Indian state, and CAG itself cites GPWM in its Gujarat findings. **Right to model; wrong to attribute to Gujarat R&B.** Mark each *"modelled from standard GPWM practice, not from a published Gujarat R&B source"* |
| **"TRA"** | **CLARIFY before building** | Ambiguous. If **ATR** (Action Taken Report, GR PRC-10-2017-31-C) is meant, it is real and established. Anything else must be confirmed |
| **Arrear register** | **DO NOT MODEL** | `NOT ESTABLISHED` for Gujarat R&B. Standard public-works concept, but no instrument found |
| **A "Technical Note Committee" as a standing approving forum** | **DO NOT MODEL** | Subject search returns **zero hits**. The file-number prefixes `TNC-`, `PWM-`, `PRC-`, `SSR-`, `RGN-`, `RBD-`, `BKL-`, `LAB-`, `LCS-`, `DCB/CON-`, `B&L-` are **at least eleven distinct internal section codes**, so `TNC-` reads as a **file namespace, not a committee**. **This is an inference from file-number structure, not a sourced fact — record it as unconfirmed in both directions.** What *is* established as a per-work approving forum is the **evaluation committee** (A/B) and the **Administrative Approval** chain |
| **A standalone R&B "Rules of Business" or "Manual of Instructions"** | **DO NOT CITE** | **Both NOT FOUND.** The functional equivalents are the **Gujarat Public Works Manual**, **GPWM**, and the **General Rules and Instructions for Guidance of Contractors** (B-2), whose **Suggestion No. 18** is real but whose content did not OCR |
| **The department Budget page total (₹29,709.62 lakh / ₹296.97 cr for 2026-27)** | **NEVER as the department budget** | It is an office/sub-head-level schematic and is **~2 orders of magnitude below** CAG's MH 5054 capital outlay of ₹16,513.22 cr. **Putting the two in one slide is the easiest way to lose the room.** Use the Budget page for the *head and scheme-code taxonomy*; use CAG for *magnitudes* |
| **CAG report URLs** | **CITE BY NUMBER AND TITLE ONLY** | All plausible CAG Gujarat URLs **return 404**. An interviewer will click a fabricated link |

### Reason

Each ruling is a case where a plausible invention would have been *defensible to
us and wrong in fact*. The register exists so the next agent inherits the
reasoning, not just the conclusion — and so a rejected option is not silently
retried.

### Trade-offs

Some exclusions leave the model thinner than a general-practice reading would.
Accepted. **A gap labelled is defensible; a plausible invention discovered in the
room is terminal.**

### Future reconsideration trigger

A readable copy of the **Gujarat Public Works Manual** (557 pp + 735 pp
annexures) or the **B-1/B-2 tender forms**. One unexplored lead worth a single
request: **`/Pages/Contents/ACT`** on the departmental site, which may carry
departmental rules the search did not surface.

---

## D-016 — The register is the product, and no query may hide an asset

- **Status:** accepted
- **Date:** 2026-09-28
- **Trigger:** operator report that adding a new bridge made the previous one
  disappear from the workspace.

### Context

The MVP demonstrated a lifecycle by holding exactly one asset in view. The
operator's complaint was that creating a bridge appeared to remove the old one.

**The backend was never at fault.** A direct probe created two assets against a
seeded register of four and returned six, with every original code intact. The
defect was entirely in presentation, and it was a *design* defect rather than a
cosmetic one, for three reasons.

1. **The register was behind a navigation click.** The portfolio list lived on
   its own page, while every workflow page rendered a single selected asset. An
   operator working inside a lifecycle had no evidence that any other asset
   existed. Absence of evidence was being read as absence of the asset.
2. **The query silently truncated.** `list_assets` applied
   `.limit(min(limit, 100))` with a default of 50 and returned no total. Past
   fifty assets a bridge would vanish from the register with nothing in the
   response to indicate it. This is not a demo-only concern: the department's
   own Achievements page publishes **7,185** bridges, so that threshold sits at
   well under one percent of the real register.
3. **The seed created one bridge.** A lifecycle-management product whose
   register holds a single asset cannot demonstrate the thing it exists to
   manage, and a judge sees that in one glance.

### Decision

**a. The register is permanently visible.** An `AssetRail` renders every asset
on every authenticated page, grouped by lifecycle phase, with search. It is not
a navigation destination. Selection changes the asset under inspection and
nothing else; the surrounding register never unmounts.

**b. No endpoint may hide an asset silently.** `list_assets` now returns
`items`, `total` (post-filter), `returned`, `truncated`, and `register_total`.
Filtering and search run server-side against the whole register, so a search
term reaches assets beyond any page boundary. The client renders an explicit
warning when `truncated` is true rather than presenting a short list as though
it were complete.

**c. The seed is a nine-asset portfolio across the three phases.** Three
bridges each in Sanction & Clearance, Execution, and Post-Completion, with
varied service states: one `RESTRICTED`, one `SRI` carrying an open defect and
an approved work order, one clean `S` post-completion bridge, three blocked
gates, and two active contracts carrying different downstream layers
(milestones plus an evaluated quality test; a price-variation claim under
finance review).

**d. The seed is additive and idempotent per asset code.** It checks existence
by `asset_code` and creates only what is missing. It never deletes or rewrites
an existing row. Re-running it after an operator has created bridges leaves
those bridges untouched — verified directly, not assumed.

### Reason

An asset register whose contents can change without the operator being told is
not a register. This is the same failure the research record identifies in the
domain: CAG found Gujarat's receipts and asset records booked and maintained in
ways the department could not itself reconcile, and the department publishes
**three mutually inconsistent official bridge counts** (1,441 / 6,768 / 7,185).
A product arguing that the missing artefact is *a trustworthy register* cannot
ship a register that quietly drops rows.

The decision is also cheaper than the alternative. Making the register permanent
required no schema change and no new endpoint, because the data was already
correct; only its presentation was wrong.

### Alternatives considered

- **Paginate the register into a dedicated page.** Rejected: it reproduces the
  original defect, because the register is again absent from the workflow
  screen. Pagination stays a legitimate future addition once the register
  genuinely exceeds a few hundred assets, and the response shape added here
  (`total`, `truncated`) already supports it.
- **Show only the most recent N assets.** Rejected outright. A recency-ordered
  list makes a stable asset appear to vanish when a newer one is added, which is
  precisely the reported symptom.
- **Deduplicate by bridge name.** Rejected. Identity is the asset code, not the
  name. D-014 already settled that the canonical name is human-authored with a
  `naming_finalised_on` date, so two distinct bridges may legitimately share a
  name, and the register must show both.
- **Reset the database on seed.** Rejected: it would discard operator-created
  data, which is the same class of silent loss the change exists to prevent.

### Trade-offs

The rail consumes horizontal space, so the workspace grid widened from 1240px to
1500px and collapses to one column below 900px. A register growing to thousands
of assets will need windowing inside the rail; the `truncated` flag already
reports honestly in the meantime, and the API accepts a `limit` up to 2000.

Seeding nine bridges instead of one made the seed considerably longer and
required a dedicated 100-id block per asset, because the original single-asset
id arithmetic silently overlapped between assets and violated a primary key on
`clearance_records.id`. The block discipline is the cost.

### Future reconsideration trigger

A real register import. Once genuine Gujarat bridge data replaces the synthetic
portfolio, phase grouping in the rail should be driven by the department's own
recorded lifecycle state rather than a hardcoded constant, and the rail should
gain district and class filters. The `PHASES` constant in
`apps/web/src/app/workspace/page.tsx` is the single place that assumption lives.

---

## D-017 — Deployment configuration is read from the environment, never hardcoded

- **Status:** accepted
- **Date:** 2026-09-28
- **Trigger:** a failed Render deployment, followed by the discovery that the
  CORS allowlist and the deploy trigger were both hardcoded to values correct
  only for one specific deployment.

### Context

Three configuration faults, all of the same kind: a value that must change per
environment was frozen into the code or the manifest.

1. **CORS allowlist.** `main.py` hardcoded exactly two origins, one being a
   specific Vercel hostname. Any other deployment hostname would pass health
   checks and then fail every browser request, which reads as "the backend is
   down" during a demo.
2. **`autoDeployTrigger: checksPass`.** Render would deploy only once its health
   check passed, but the check could not pass until the service was running.
   This deadlocks the first deploy of a new service.
3. **Silent JWT fallback.** `security.py` fell back to a publicly known signing
   key when `JWT_SECRET` was unset, with no signal at any level. A deployment
   missing its secret would issue validly signed tokens under a key that is
   present in the repository.

### Decision

- CORS origins come from `CORS_ORIGINS`, a comma-separated environment
  variable. The two known-good origins remain as the default so local work is
  unaffected, and the default is now explicitly a fallback rather than the
  configuration.
- `autoDeployTrigger` is `commit`, with `autoDeploy: true`.
- `render.yaml` declares `DATABASE_URL`, `JWT_SECRET` and `CORS_ORIGINS` as
  `envVars`, so a missing secret is visible in the Render dashboard rather than
  inferred from a failure.
- The JWT fallback is retained for the local seeded demo, but emits a `WARNING`
  naming the risk at import time. Verified in both directions: with
  `JWT_SECRET` set the fallback is not used, and without it the warning fires.
- `.env.example` documents all four variables, marks which are mandatory on a
  deployed instance, and states the `postgresql://` to `postgresql+psycopg://`
  rewrite so a working connection string is not misdiagnosed as broken.

### Reason

A configuration fault that only manifests after deployment, and only in a
browser, is the most expensive class of bug available during a live demo. Every
value in this list is per-environment by definition, so none belongs in source.

The JWT fallback was deliberately **not** converted into a hard startup failure.
That would be the stricter engineering choice and is the right one for a system
handling real credentials. Here it would trade a security nicety for a demo that
cannot start on a forgotten environment variable. The compromise chosen keeps
the demo alive and makes the risk unmissable in the logs, which is the honest
version of that trade.

### Alternatives considered

- **Refuse to start without `JWT_SECRET` when not on localhost.** Rejected for
  now, for the reason above. Revisit the moment real user credentials exist.
- **Allow all origins.** Rejected outright. It would have hidden this fault
  rather than fixed it.

### Trade-offs

The CORS default is still a guess about the current deployment. Setting
`CORS_ORIGINS` remains a required deployment step, now documented in three
places: `render.yaml`, `.env.example`, and the `_cors_origins` docstring.

### Future reconsideration trigger

Real authentication. When genuine accounts exist, the JWT fallback must become a
startup failure, `TOKEN_TTL_HOURS` should move to configuration, and refresh
tokens should replace the single 8-hour access token.

---

## D-018 - Phase is derived from records, never read from a stored label

**Context.** `Asset.lifecycle_state` was a hand-maintained column. The audit
against `research_3phase_opencode.md` found the reported failure: a not-yet-built
bridge could be shown in Post-Completion, because "Post-Completion" was a value
someone typed rather than a fact the system could check. The seeded portfolio
was hand-tuned to a tidy 3/3/3 split across the three phases.

**Decision.** `Asset.lifecycle_state` remains as a convenience column, but the
authoritative phase is computed by `app/lifecycle.py:phase_facts` from two
recorded facts: whether a contract has been awarded, and whether it is
completed. `phase_facts` answers for a whole list of assets in three queries
rather than N. The passport reports `stored_state_agrees` so a divergence
between the two is visible rather than silent.

**Reason.** "Post-construction applies only to a constructed bridge" is now a
structural property of the system rather than a promise in a document. A bridge
cannot be teleported between phases by writing a column, because no code path
reads the column to decide anything.

A *published but unawarded* tender derives to Sanction & Clearance, not
Execution. This is correct: you cannot be under construction without somebody
being bound to build you. It reclassified the seeded Alok bridge and produced a
derived split of 5 pre / 2 execution / 3 post rather than the hand-set 3/3/3.

**Alternatives considered.** Keeping the column as the source of truth and
validating it — rejected, because validation can be skipped and does not prevent
a bad write. Deriving phase on the client — rejected for the same reason
`lifecycle_state` was unsafe: a presentation-layer derivation is not a fact.

**Trade-offs.** A stale column can disagree with the derived value, which is why
`stored_state_agrees` is surfaced. The hand-set seed values no longer need to be
maintained, which removes a whole class of demo breakage.

**Future reconsideration trigger.** If the department adopts a formal lifecycle
state machine with named transitions, the column becomes a cache of a real
state machine and can be trusted again. Until then it is a label.

---

## D-019 - Visibility is applied in SQL from the caller's role, before any row is read

**Context.** Every authenticated user saw every bridge. Role differences were
cosmetic: the frontend rendered different panels for different roles, but the
API returned the same data. A contractor could read another company's contract
terms and award amount.

**Decision.** A single function, `lifecycle.scope_asset_query`, applies
`Asset.id.in_(allowed)` inside the query. Three role groups:

- `SEE_ALL_ROLES` — State Admin, Chief Engineer, Superintending Engineer,
  Executive Engineer, Auditor.
- `BUILT_ONLY_ROLES` — Inspector, Quality Engineer, Finance. These see only
  awarded bridges, because their work acts on a physical structure.
- `CONTRACTOR_ROLES` — Contractor, and only what binds them.

An empty allow-set is compiled to `Asset.id.is_(None)`, so a role that can see
nothing receives nothing rather than everything.

A contractor is refused a bridge outside scope with **403 naming the rule that
produced it**, not a hiding 404. A 404 would make an authorization boundary
indistinguishable from a missing record.

**The contractor clause was corrected after the bid button proved unreachable.**
The first version scoped contractors to bridges where their company *already*
held a contract. That made a published tender they had not yet won invisible,
so "Submit controlled bid" could never render. A tender notice is public by
design — nProcure publishes it. A contractor now sees three things: a tender
open for bidding, a bridge they are bound to build, and a defect they have been
told to repair. Competing bids are shown to exist; their prices are not.

**Alternatives considered.** Filtering in the frontend — rejected, it is the
thing that was already broken. A permission table joining users to assets —
rejected as premature; the three role groups are derivable from what a role
does, and a join table would be a second source of truth for a decision that
lives in one function today.

**Trade-offs.** A role change is a code change, not a configuration change. That
is a real cost, and acceptable while the actor model is still being confirmed
with the sponsor. It also means the rules must be defensible, because they are
visible in a diff.

**Future reconsideration trigger.** Real accounts, or a sponsor decision to
delegate visibility to a division rather than a role. Either makes a persistent
grant table the right answer.

---

## D-020 - Every error cites the record that justifies it

**Context.** Refusals were bare `HTTPException`s. "403 Forbidden" and
"GATE_NOT_PASSED" tell a demonstrator nothing and cannot be defended in an
interview. Worse, nothing stopped a plausible-but-wrong rule from being written
into a message and shipped — the audit found two different invented quality rules
that contradicted each other, one in the API and one in the seed.

**Decision.** `app/errors.py` defines `DomainError(HTTPException)` carrying
`code`, `message`, `detail`, `remediation: list[str]`, and `reference`. Helpers:
`gate_blocked`, `role_denied`, `not_visible`, `wrong_phase`, `rule_violation`,
`not_established`, `conflict`, `invalid`, `missing`. Registered once in
`main.py` so every route inherits it, including routes added later.

`reference` names a section of `research_3phase_opencode.md`. Where the record
says `NOT ESTABLISHED`, `errors.not_established` returns **501**, not an
invented value.

**Reason.** A citation in the error is what makes the refusal a fact rather than
an assertion. It also means the research record and the running system cannot
silently drift apart: a rule with no source cannot produce a message.

**Alternatives considered.** Logging the basis server-side and showing a short
message — rejected, the audience for the basis is the person being refused and
the interviewer. Bare HTTPExceptions — rejected, that is the status quo this
replaces.

**Trade-offs.** Error bodies are larger. The frontend renders all five fields
deliberately; a bare message would have been less work and would have thrown
away the point.

**Future reconsideration trigger.** An i18n layer. `reference` and `remediation`
are currently English prose and would need to move to message catalogues, while
`code` stays stable as the machine-readable key.

---

## D-021 - The price-variation engine computes server-side or it does not exist

**Context.** `PVClaimInput` accepted both `submitted_amount` and
`calculated_amount`, computed their difference, and stored it. That is a
difference calculator, not an engine — and it left the arithmetic with the
people who got it wrong last time.

**Decision.** The input carries only measured facts: `components[]` with
`portion`, `base_index`, `current_index`; plus `months_elapsed` and `is_bridge`.
`claimed_amount` is optional and used **only** to report the variance the engine
found, never to compute the entitlement.

Index-base mismatch is **fatal**. On mismatch `computed` is forced to `0.00` and
no payable figure is produced at all, with `arithmetic_sum_before_checks` and
`index_integrity_verified` retained for audit.

**Reason.** The Bharuch failure was Cement (122.5) and Steel (108.4)
interchanged in one cell: a ₹15.57 lakh recovery became a ₹40.13 lakh payment, a
₹55.70 lakh inversion. The wrong answer was entirely plausible. An index-base
mismatch does not produce a wrong number, it produces a convincing one, so an
advisory warning would have been worse than useless — it would have let the
figure through with a note attached.

The full rule set is computable from Gujarat's own documents: admissible only if
EC > ₹25 lakh **and** time limit > 12 months; no price variation in the first 12
months; ceiling 5% of EC less Cement/Steel/Asphalt; escalation `1.1^n`; EPC base
date = bid due date − 28 days.

**Counter-intuitive detail that must survive.** For **Major Bridges, Cement and
Steel carry zero weight** — Labour 20%, Bitumen 15%, Fuel 10%, Other materials
40%, Plant 15%. Assuming they carry weight, as they do for roads, silently
inflates every Major Bridge claim.

**Alternatives considered.** Recompute on the client and compare — rejected, the
server must be the only place an entitlement is produced. Warn and let the
claimant proceed — rejected for the reason above.

**Trade-offs.** A legitimate claim with a genuinely revised base cannot proceed
without a route to record the new base. That is intentional: the route should be
an amendment with an audit trail, not an override.

**Future reconsideration trigger.** A department-issued base-date amendment
table. Today the base indices are constants in `rules.OFFICIAL_BASE_INDICES`,
which is honest but not maintainable.

---

## D-022 - Refusals are recorded, not discarded

**Context.** A refused price-variation claim and a failed quality test were
returned as 4xx and dropped. The client saw an error; the department kept no
record that anyone had tried.

**Decision.** Both are persisted with their reasons before the 4xx is raised. A
refused claim is evidence. A failed cube test is evidence. Neither is a
non-event.

**Reason.** In an audit, the record of a failure is the evidence. A system that
keeps only approvals cannot answer "was this tested and rejected, or never
tested?" — which is exactly the question that made Gujarat's bar-chart register
unable to support a condition-based decision.

**Alternatives considered.** Logging only — rejected, a log line is not a
durable record and cannot be reported on. Raising without persisting — rejected,
that is the current behaviour.

**Trade-offs.** Table growth on refused records. Bounded in practice, and worth
more than it costs.

**Future reconsideration trigger.** Volume. If refused claims become numerous
enough to matter, they need their own status lifecycle and a reporting view
rather than sharing the claims table.
