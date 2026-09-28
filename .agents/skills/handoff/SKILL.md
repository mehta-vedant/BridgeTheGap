---
name: handoff
description: >
  Write a durable continuation packet into HANDOFF.md so another coding agent (Codex, OpenCode, or a fresh session) can resume from the exact state: objective, git truth, dirty-file conditions, and one unambiguous next action. Use when context is running low, when you are stuck, before switching agents, before a long break, or when the work must be transferred. Triggers on "handoff", "hand off", "hand this over", "I'm low on context", "context running out", "switching to Codex", "wrap up and pass this on", "save my progress", "save my work", or /handoff.
---

# Handoff — Leave the Work Resumable

Write `HANDOFF.md` so an agent with **zero conversation history** can continue
the work correctly on its very next action.

**Why this exists:** agent context is volatile and unrecoverable; a file on
disk is not. The expensive failure is not "the next agent has less context" —
it is "the next agent confidently resumes a *different* task than the one in
progress, or re-derives the five things you already spent forty tool calls
learning." A handoff is a cache of expensive-won knowledge.

**The test:** a stranger agent reads only `HANDOFF.md` plus the repo. If it
can state your objective and execute your next action without asking a
question, the handoff is good. If it has to ask *"what were we doing?"* — or
worse, guesses and starts refactoring — the handoff failed.

---

## When to use

- Context is running low and you cannot realistically finish.
- You are stuck, and a fresh context is cheaper than a fourth attempt.
- You are about to hand the machine to a different agent or human.
- A real pause is coming (meeting, sleep) and state would be lost.
- **Instead of** declaring a blocker you have not actually investigated.

Do **not** use handoff for routine mid-task commits, or for restating work
that is already documented and cleanly committed.

---

## Phase 0 — Choose your depth

Assess how much context you have left and pick a lane.

**Full handoff** (normal case). Do all of Phase 1–5.

**Panic handoff** (context nearly gone, or you are mid-crash). Write only the
3-line minimum, then stop. Do not spend your last tokens on prose.

```md
# Agent Handoff

## Current Objective
<one sentence>

## Exact Next Action
1. <one concrete step: file, command, or edit>

## Uncommitted / Risky State
- <path> — <half-written | untested | known-broken>
```

Then immediately update `HANDOFF.md`'s `Last Updated` and stop. A 3-line
handoff beats a beautiful one you never finish writing.

---

## Phase 1 — Capture git truth, do not recall it

**First, check whether this is even a git repository:**

```bash
git rev-parse --git-dir >/dev/null 2>&1 && echo "repo" || echo "no repo"
```

Then follow the matching path.

### Path A — inside a git repository

Never write state from memory. Run these and copy the real output:

```bash
git status --short          # what is dirty, untracked, staged
git log --oneline -10       # where we are in history
git diff --stat             # size and shape of uncommitted work
git stash list              # is work parked in a stash? (silent killer)
git rev-parse --abbrev-ref HEAD
```

**Unborn HEAD edge case:** a freshly `git init`-ed repository has zero
commits, and `git log` then exits non-zero with
`does not have any commits yet`. That is not an error state — it simply
means there is no history yet. To count commits safely on any repo:

```bash
git rev-list --all --count    # prints 0 and exits 0
```

Prefer it over `git log` whenever you only need the count. In PowerShell,
`$ErrorActionPreference = 'Stop'` will turn git's stderr into a *terminating*
error, so `2>$null` will not suppress it — use `rev-list --count`.

### Path B — not a git repository

Expected during pre-hackathon toolkit work, and immediately after
`git init` but before the first commit in some setups. Do **not** treat it as
a problem to fix, and do **not** run `git init` uninvited.

Record the state from the filesystem instead:

```bash
find . -type f -not -path './.git/*' | sort   # or: ls -R
```

- `State Snapshot` must say `Tree: no git repository` and give the file
  count.
- `Uncommitted / Risky State` becomes a plain list of half-written or
  untested files.
- Phase 4 is skipped, with the reason noted.

The important rule is unchanged: **measure, do not recall.** "I think these
files are fine" is not a state snapshot.

---

## Phase 2 — Verify, or explicitly declare unverified

Run the cheapest check that proves the current state:

1. tests for the touched area
2. type check / lint
3. build, only if the task is at a build boundary

Then record the **actual** result. If you could not run it, write `NOT RUN`
and say why. Never let a later agent infer "tests pass" from silence —
an unverified handoff read as a verified one is how false confidence
propagates across sessions.

---

## Phase 3 — Write `HANDOFF.md`

**Overwrite. Do not append.** `HANDOFF.md` is current state, not a history
log (`AGENTS.md` §23). If you want history, commit the old version in the same
commit that replaces it, or drop a dated note in `docs/decisions.md`.

Keep the required section names from `AGENTS.md` §23 so tooling and humans
find what they expect. Fill **Tier 1 always**; include **Tier 2 only when it
is true** (`AGENTS.md` §20: only document what is known).

### Tier 1 — never skip

```md
# Agent Handoff

<!-- Last Updated: <YYYY-MM-DD HH:MM> | Agent: <Codex|OpenCode|human> -->

## Current Objective

One sentence. The single active goal, in the present tense.
Not a goal history. Not a list of sub-tasks. One goal.

## State Snapshot

- Branch: <branch> @ <short-sha>
- Tree: clean | <n> modified, <n> untracked
- Last commit: <sha> <subject>
- Running processes: <dev server / tunnel / watcher — or "none">

## Work Just Completed

Concrete changes, each with a path. Say what now works that did not before.
3–8 bullets. Name files — do not write "refactored the API layer".

## Exact Next Action

1. A single numbered step, specific enough to execute without a decision.
   Prefer an exact command or an exact file + edit.

This is the highest-value field in the file. "Continue the auth work" is not
a next action. "Run `npm test -- auth`, then fix the failing refresh-token
case in `src/lib/auth.ts:88`" is.

## Verification Status

| Check | Command | Result |
|---|---|---|
| <name> | `<cmd>` | PASS / FAIL / NOT RUN (<why>) |
```

### Tier 2 — include when true

- **Current Phase** — `setup | analysis | build | verify | demo | blocked`
- **Uncommitted / Risky State** — every dirty path, each labelled
  `half-written`, `untested`, `known-broken`, or `unverified`. This is what
  stops the next agent from trusting a file you were midway through editing.
- **Traps for Next Agent** — non-obvious things that will otherwise waste
  time. Seed it with: running servers and ports, pending migrations, required
  env vars, known-flaky tests, external services that are down or rate-limited,
  credentials that exist but were not checked, and anything that looks like a
  bug but is intentional.
- **Known Blockers** — what is actually stopping progress.
- **Open Questions** — decisions you are deliberately deferring.
- **Next Recommended Work** — the ordered backlog after the next action.
- **Important Constraints** — only what is not already obvious from `AGENTS.md`.
- **Current Architecture / Current Stack** — only if a real product exists.

---

## Phase 4 — Anchor the state in git

**If this is not a git repository, skip this phase entirely** and note in the
handoff that no commit was made because no repository exists. Do not
initialize one to satisfy this phase. Some contexts deliberately have no
repository yet — for example a pre-hackathon toolkit whose Git history must
begin only at official kickoff.

Otherwise, default rule: **commit only what is known-good and needed for
continuity.**

- Clean, green tree → commit as `chore: handoff at <milestone>`.
- Dirty or failing tree → **do not** commit broken work just to have an anchor.
  Leave it dirty, list every path under Uncommitted / Risky State, and say
  plainly that the next agent inherits a dirty tree.
- Untracked files that represent real work → flag them loudly. Untracked work
  is one `git clean` away from gone.

A handoff commit is a landmark, not a squash of unfinished work.

---

## Phase 5 — Close with a resume line

End your turn with one line the human can act on:

```text
HANDOFF.md written. Resume with: /resume-work
```

Then stop. Do not "just one more quick fix" after a handoff — that is how
context runs out mid-handoff and the packet ends up describing a state you
already changed.

---

## Anti-patterns

- **Narrating instead of measuring.** "Tests were passing earlier" is not a
  status. Run them or write `NOT RUN`.
- **Vague next action.** The whole point is removing the next agent's first
  decision.
- **Handoff as diary.** Long prose about your reasoning buries the two facts
  that matter. Reasoning belongs in `docs/decisions.md`.
- **Committing broken work** to look tidy.
- **Leaving secrets in the packet.** Reference env var names, never values.
- **Duplicating `AGENTS.md`.** Constraints already written there do not need
  repeating; reference the section instead.

---

## Self-check before you finish

- [ ] Objective is one sentence, present tense.
- [ ] State Snapshot matches real `git` output from this session.
- [ ] Every dirty file is listed and labelled.
- [ ] Next Action is executable without a judgement call.
- [ ] Verification rows are real results, not assumptions.
- [ ] Traps include the running-server / missing-env-var / pending-migration
      items you would otherwise have to rediscover.
- [ ] `HANDOFF.md` was overwritten, not appended.
- [ ] No secrets.
- [ ] Resume line printed.
