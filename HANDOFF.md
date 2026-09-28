# Toolkit Handoff

## Repository Purpose

This folder is a **pre-hackathon engineering toolkit** that will become the
hackathon project repository.

There is **no second folder and no copy step**. This directory *is* the
project directory.

It is deliberately **not a git repository** before the official start of the
event, so the submission history contains no prior work:

```text
now          C:\pravi   toolkit files on disk, no .git, no commits
                            |
                        official start
                            v
kickoff      scripts\kickoff.ps1  ->  git init, branch main, no commit
first commit only after the problem statement is in hand
```

Before that point, do not implement problem-specific functionality and do
not run `git init`. See `AGENTS.md` section 1, "Pre-Hackathon Boundary".

This file contains the immediate continuation state for another engineering
agent.

Keep it concise and current.

<!-- Last Updated: 2026-09-28 | Agent: OpenCode -->

---

## Current Objective

No product problem has been assigned yet.

Current objective:
Close the remaining open skill-layer defects listed under Known Issues. The
MCP and tool-integration question is settled (`docs/decisions.md` D-005) and the
starter-template question is settled (D-006).

---

## Current Phase

Pre-kickoff toolkit construction. No product code exists.

---

## Completed

- Windows development environment selected as canonical environment.
- Git, GitHub CLI, Node.js, npm, Python, Docker Desktop installed.
- OpenAI Codex CLI and OpenCode installed.
- Shared repository documentation structure created.
- `AGENTS.md` constitution in place (28 sections, plus the Pre-Hackathon
  Boundary rule).
- `docs/agent-start.md` startup procedure written.
- `handoff` and `resume-work` skills designed, installed, and verified
  registered by the agent harness.
- Both skills patched to operate with or without a git repository.
- `.gitignore` written and empirically validated.
- `.gitattributes` written for cross-platform line endings.
- `scripts/kickoff.ps1` and `scripts/kickoff.sh` written and tested.
- Stale `config/` folder (unrelated `codex` PyPI package) removed.
- Decisions D-001 through D-004 recorded in `docs/decisions.md`.
- **All 12 `SKILL.md` files written.** Every skill is registered by the
  harness. `research-brief` was renamed to `research` and written; it is no
  longer a placeholder.
- `AGENTS.md` section 28 "Skill Routing" added, recording the recommended
  skill order and the rule that skills are a toolbox, not a waterfall.
- OpenCode MCP surface reduced to four connected servers. See `docs/decisions.md`
  D-005.
- **D-006 recorded: no pre-built starter templates before the problem
  statement.** A working Next.js + FastAPI template set was built, verified and
  then deleted. Do not rebuild it. The reusable findings were kept in
  `docs/known-issues.md`.
- MCP tool layer validated live: Playwright navigated and interacted with a
  local app, `shadcn` returned a registry response, Context7 resolved and
  fetched FastAPI documentation.
- `docs/known-issues.md` rewritten with six stack-independent landmines, each
  with symptom, cause and fix.
- `.gitignore` extended to cover `.playwright-mcp/`, which the Playwright MCP
  server was writing into the working tree on every run.

---

## State Snapshot

- Git repository: **none**. Deliberate, per `AGENTS.md` section 1. Do not run
  `git init` before official kickoff.
- Files: toolkit only, no product code
- History: none. The first commit belongs at kickoff.
- Running processes: none
- Kickoff command: `.\scripts\kickoff.ps1`
- Line endings: UTF-8, LF, enforced by `.gitattributes` once git exists

---

## Work Just Completed

- Removed the temporary git repository. Two commits existed (`cc93dac`,
  `380baaa`) and both are now **permanently unrecoverable**. The toolkit has
  no version-control history until kickoff. This was a deliberate decision,
  not data loss.
- `AGENTS.md` — added the "Pre-Hackathon Boundary" rule as a subsection of
  section 1 rather than a new numbered section, so existing cross-references
  such as "AGENTS.md section 15" stay valid.
- `AGENTS.md` — corrected heading levels on sections 2 through 27, which had
  been written as `#` (h1) instead of `##` (h2). All 27 sections are now
  properly nested under the single h1 title.
- `HANDOFF.md` — rewritten as "Toolkit Handoff" with a Repository Purpose
  section, so no agent mistakes this folder for a finished submission.
- `.agents/skills/handoff/SKILL.md` — Phase 1 and Phase 4 now branch on
  whether a git repository exists, and document the unborn-HEAD case.
- `.agents/skills/resume-work/SKILL.md` — Phase 1 now branches on whether a
  git repository exists, with a filesystem-based verification path.
- `scripts/kickoff.ps1` / `scripts/kickoff.sh` — replaced the earlier
  copy-to-new-folder scripts, which described a two-folder model that is no
  longer in use. These initialize the repository but deliberately create no
  commit unless explicitly asked.
- `docs/decisions.md` — D-002 records the single-folder architecture.
- `AGENTS.md` — appended section 28 "Skill Routing". Appended rather than
  inserted so that the existing "section 15 / 20 / 23 / 24" cross-references
  stay valid. All 28 sections verified at h2.
- Eight skills written verbatim from user-supplied content:
  `architecture-design`, `database-design`, `api-design`,
  `implementation-plan`, `frontend-build`, `production-review`,
  `demo-readiness`, `interview-defense`. All eight were confirmed registered
  by the harness after writing.
- Mojibake scan re-run across all 12 skills and `AGENTS.md` after every
  write: 0 suspect characters.

---

## Exact Next Action

Close the two remaining skill-layer defects, in this order.

1. **Bind the `research` skill to actual tools.** The skill was written and
   registered, but it names no mechanism at all — no `firecrawl`, no
   `context7`, no search mechanism. An agent executing it during the event
   has to improvise. D-003 already commits the team to delegating research
   to `firecrawl_search` / `firecrawl_scrape` / `context7`; the shipped text
   does not. Either add a short "Tooling" section naming them, or accept
   that the skill is deliberately tool-agnostic and record that in D-003.
2. **Resolve the `problem-analysis` "default stack"** (Known Issue 5). D-006
   settled *how* to resolve it: write down a selection procedure during problem
   analysis, against the real problem. Do not resolve it by shipping a stack.

Both are documentation edits. Do not create a git repository or any commit
while doing them.

Do **not** build CI/CD workflows, deployment config, or project templates
before the problem statement is in hand. D-006 covers this.

---

## Current Architecture

No product architecture has been selected yet.

Do not assume a framework or database until the hackathon problem is known.

Toolkit-level structure only:

```text
AGENTS.md              constitution and hard rules
HANDOFF.md             this file, current agent state
.agents/skills/        the hackathon operating system
docs/                  one document per concern, per AGENTS.md section 20
scripts/               kickoff bootstrap
.gitignore             secrets, deps, build output
.gitattributes         line-ending normalization
```

---

## Current Stack

No product stack selected yet. Tooling only:

- Node.js, Python, Docker (available, unchosen)
- Git, GitHub CLI
- Codex, OpenCode

---

## Current Branch

Not applicable. No git repository exists. See State Snapshot.

---

## Known Issues

1. **No version control on the toolkit.** With `.git` removed there is no
   diff, no revert, and no history for the 12 skills, `AGENTS.md`, and docs
   being actively edited. An accidental overwrite is unrecoverable except
   through editor history. Accepted deliberately to keep the submission
   history clean. Reconsider if the toolkit grows large enough that losing
   work becomes a real risk.
2. **`.env.example` is empty (0 bytes).** Required by `AGENTS.md` section 15,
   but there is no product yet, so there are no variables to declare.
   Populate it as soon as the first environment variable exists.
3. **11 of 13 `docs/` files are empty placeholders.** Intentional
   (`AGENTS.md` section 20), but a resuming agent should not mistake them for
   finished analysis. Only `agent-start.md` and `decisions.md` have content.
4. **The `research` skill names no research tool.** It is 12180 bytes across
   17 phases and never mentions `firecrawl`, `context7`, or any other
   mechanism. A grep for tool names returns nothing but the words "Research"
   in headings. During a time-boxed event an agent following it literally has
   no instruction on *how* to gather evidence, which is the one thing it
   cannot improvise safely. Note that the `firecrawl` MCP server is currently
   **disabled** (D-005), so the tool the skill would need is not even
   connected.
5. **`problem-analysis` Phase 12 evaluates a "default stack" that is defined
   nowhere.** A grep for `default stack` / `DEFAULT STACK` across the
   repository returns nothing outside that skill. `AGENTS.md` section 4 lists
   Next.js / FastAPI / PostgreSQL as *defaults, not mandatory choices*, which
   is not a concrete baseline. Either define the default stack in
   `docs/decisions.md` or rewrite the phase to not depend on it.
6. **Context7 API key must be rotated.** A Context7 bearer token was found
   hardcoded in plaintext in the global `opencode.jsonc` and was printed into
   an agent transcript during diagnosis. The key has been removed from the
   config and `context7` reconnected via OAuth, but the old key is still
   valid at the provider until the user revokes it. This is a user action.
7. **None of the 10 problem/workflow skills declare trigger phrases.**
   `handoff` and `resume-work` do (for example: "Triggers on `handoff`,
   `hand off`, `switching to Codex`"). The other 10 are registered and their
   descriptions are informative, but they carry no explicit "Triggers on ..."
   list, so auto-invocation will be weaker than intended.
8. **Heading style is inconsistent between skills.** `handoff` and
   `resume-work` use `## Phase`. The 10 user-authored workflow skills use
   `#` for every phase, producing 15 to 25 h1 headings per file. Rendering is
   still correct because all files open with `#`, but the structures differ.
   Cosmetic. Do not normalise without asking: the `#` style was supplied
   deliberately and consistently across those files.
9. **Never run PowerShell `Get-Content` / `Set-Content` round-trips on these
   files.** Doing so read UTF-8 as Windows-1252 and double-encoded every
   em-dash and section sign, corrupting `HANDOFF.md`. If a scripted edit is
   unavoidable, read and write with explicit UTF-8 encoding, or use the agent
   file-edit tools instead.

---

## Open Questions

- Actual hackathon problem statement
- Product requirements
- Final technology stack
- Deployment architecture
- Required integrations
- Whether the kickoff commit should include the pre-seeded toolkit files or
  stage product paths only. `scripts/kickoff.ps1 -OnlyProduct` implements the
  second option; the default stages everything. Decide on the day.
- Whether the `research` skill should name its tooling explicitly or stay
  tool-agnostic. If it names tools, decide whether `firecrawl` is re-enabled.
- Whether to normalise heading levels across the 10 user-authored skills, and
  whether to add trigger phrases to them.
- What the "default stack" for `problem-analysis` Phase 12 should be, or
  whether that phase should stop assuming one.
- Whether Codex should receive the same MCP set as OpenCode. Codex currently
  has Playwright and shadcn enabled; GitHub was deliberately not duplicated.

Resolved:

- Architecture: one folder, `git init` at kickoff. See D-002.
- Research phase: a dedicated research skill is required, because none
  existed in any of the four skills directories. Now written as `research`.
  See D-003.
- Skill scope: project-scoped in `.agents/skills/`. See D-001.
- Database and API: two separate skills, not one. See D-004.
- Skill order and invocation: all 12 skills written, order recorded in
  `AGENTS.md` section 28, invoked selectively rather than as a waterfall.
- OpenCode MCP surface: four connected, four disabled rather than deleted.
  See D-005.

---

## Next Recommended Work

1. Close Known Issues 4 and 5: bind the `research` skill to a tool, and
   resolve the `problem-analysis` default stack. See Exact Next Action.
2. Create CI templates under `ci/`.
3. Create deployment templates under `deployment/`.
4. Create product starter templates under `templates/`.
5. Rehearse kickoff end to end in a throwaway copy, then discard it.

Do not initialize git in this folder. Item 5 must be rehearsed in a copy.

---

## Important Constraints

- Windows is the canonical development environment for this project.
- Project location is `C:\pravi`.
- **Do not create a git repository or commit in this folder before official
  kickoff.** See `AGENTS.md` section 1.
- Do not implement problem-specific functionality before the problem
  statement is received.
- Do not recreate the WSL/Ubuntu development environment.
- Do not select the product technology stack before problem analysis.
- Do not add unnecessary infrastructure.

---

## Verification Status

| Check | Command | Result |
|---|---|---|
| Config cleanup | `Test-Path config` | PASS - absent |
| Skill frontmatter | parsed by harness | PASS - both `name:` keys valid |
| Skills registered | harness reload mid-session | PASS - both loaded |
| `AGENTS.md` headings | `^## \d+\.` match | PASS - 28 of 28 at h2 |
| `AGENTS.md` cross-refs | sections 15, 20, 23, 24 still valid | PASS - no renumbering, section 28 appended |
| `AGENTS.md` skill routing | section 28 present | PASS - order recorded, waterfall explicitly discouraged |
| `opencode.jsonc` parse | `ConvertFrom-Json` | PASS - valid, all 8 servers under `mcp.servers` |
| `opencode.jsonc` credentials | grep for bearer/ctx7sk | PASS - 0 matches, plaintext key removed |
| `opencode.jsonc` schema | grep for `enabled` | PASS - 0 servers using the invalid V1 field |
| MCP final state | `opencode mcp list` | PASS - context7, github, playwright, shadcn connected; firecrawl, jira, notion, postgres disabled |
| shadcn startup fix | `opencode mcp list` | PASS - was `Request timed out`, now `connected` with `-y` + 60s startup timeout |
| Context7 after key removal | `opencode mcp list` | PASS - still connected, no OAuth re-auth needed |
| `docs/agent-start.md` | non-empty | PASS |
| `.gitignore` secrets | `git check-ignore .env .env.local` | PASS - both ignored |
| `.gitignore` example | `git check-ignore .env.example` | PASS - **not** ignored |
| `.gitignore` artifacts | node_modules, dist, venv, log, sqlite, pyc, tmp, test-results | PASS - all ignored |
| `.gitattributes` | written | PASS - not yet exercised, no repo |
| `scripts/kickoff.ps1` default | run in a throwaway copy | PASS - 0 commits, branch main, no commit made |
| `scripts/kickoff.ps1` re-run guard | run again after init | PASS - refuses, exits 1 |
| `scripts/kickoff.ps1 -Commit -OnlyProduct | run in a throwaway copy | PASS - commit contains only `src/main.ts`, toolkit untracked |
| `scripts/kickoff.sh` all three modes | run via Git Bash | PASS - identical behaviour to the .ps1 |
| `.gitignore` in a fresh repo | `git check-ignore` | PASS - `.env` ignored, `.env.example` tracked |
| `.gitattributes` in a fresh repo | observed git output | PASS - `CRLF will be replaced by LF`, correct direction |
| Mojibake scan | char-code scan, all skills + `AGENTS.md` | PASS - 0 suspect characters |
| Skill file sizes | byte count, 12 skills | PASS - all 12 non-empty, smallest 3516 b |
| 8 new skills registered | harness reload mid-session | PASS - all 8 loaded |
| `research` skill registered | harness reload mid-session | PASS - loaded, 12180 b |
| `.git` absent | `Test-Path .git` | PASS - no repository, by design |
| Tests | - | NOT RUN - no product code exists |
| Lint / typecheck | - | NOT RUN - no product code exists |

### Bugs found by actually running the scripts

Recorded because both would have failed at kickoff:

1. `git log` on a repository with no commits exits non-zero and writes to
   stderr. Under `$ErrorActionPreference = 'Stop'` that became a
   *terminating* PowerShell error, so the original state check failed on a
   perfectly healthy empty repository. Fixed by using
   `git rev-list --all --count`, which prints `0` and exits `0`.
2. The `.gitattributes` line-ending notice is a **warning on stderr**, and
   `Stop` escalated it too. This broke `kickoff.ps1 -OnlyProduct` on every
   Windows kickoff. Fixed by setting `$ErrorActionPreference = 'Continue'`
   and checking `$LASTEXITCODE` explicitly after each git call.

Lesson for later scripts: on Windows, never combine
`$ErrorActionPreference = 'Stop'` with native `git` calls that are expected
to warn.
