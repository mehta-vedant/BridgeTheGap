---
name: resume-work
description: >
  Resume interrupted work from HANDOFF.md and the repository state. Loads the shared agent context, reconciles the handoff's claims against actual git/filesystem truth, flags staleness or conflicts instead of silently trusting the document, and executes the documented Exact Next Action. Use at the start of any session continuing someone else's work, when told to "resume", "pick up where we left off", "continue the handoff", or after a context switch. Triggers on "resume", "resume work", "continue from handoff", "pick up where we left off", "read the handoff", "what was I doing", "continue the task", or /resume-work.
---

# Resume Work — Continue From Recorded State

Load prior context from disk, verify it is still true, then continue the
documented objective **without redesigning it**.

**Why this exists:** a handoff is a snapshot, and snapshots go stale. Between
writing and reading it, files may have been committed, a branch rebased, a
migration applied, or a person may have hand-edited things. Blindly trusting
`HANDOFF.md` is how an agent confidently resumes a state that no longer
exists. The filesystem always wins; the handoff is a *hypothesis to be
checked*, never an authority.

**The failure this prevents:** not "I forgot what we were doing" — you have
the file. It is "I obeyed a stale instruction, overwrote someone's committed
work, and reported success for a change that was never applied."

---

## Phase 0 — Pick your reading depth

Time pressure is normal. Read only what the next action needs.

| Ladder | Read | When |
|---|---|---|
| **Just-in-time** | `HANDOFF.md` + files named in Exact Next Action | Mid-crash, seconds left |
| **Normal** | + `AGENTS.md` + relevant `docs/*.md` + `git status` / `log` / `diff` | Default |
| **Deep** | + full `docs/` sweep + `git log -20` + every uncommitted diff | Starting a hard or unfamiliar area |

Never skip Phase 1, at any depth. It costs three commands and catches the one
error class that destroys work.

---

## Phase 1 — Reconcile the handoff against reality

**First, check whether this is even a git repository:**

```bash
git rev-parse --git-dir >/dev/null 2>&1 && echo "repo" || echo "no repo"
```

### Path A — inside a git repository

```bash
git status --short
git rev-list --all --count    # NOT `git log`: prints 0 and exits 0 when empty
git log --oneline -10
git diff --stat
git stash list
```

Compare to the `State Snapshot`, `Work Just Completed`, and `Uncommitted /
Risky State` sections. Check for drift:

| Drift | Meaning | Action |
|---|---|---|
| SHA in handoff is not in `git log` | rebased, reset, or branch switched | **Stop.** Report. Do not build on either branch until resolved. |
| Files listed dirty are now clean | someone committed them | Adopt the commit as truth; update `HANDOFF.md`. |
| New untracked files not in handoff | work happened outside the handoff | Inspect before touching; it may be newer than the packet. |
| Handoff says "implemented", code absent | handoff was aspirational | Trust the code. Report the gap. |
| A `docs/` file the handoff calls written is empty | the claim was false | Flag it loudly — it means other claims need auditing too. |
| Branch differs from handoff | wrong branch | Confirm intent with the human before writing anything. |
| `git log` says "does not have any commits yet" | unborn HEAD, not a fault | Expected on a fresh repo. Use `rev-list --all --count` to confirm it is 0. |

**If reality and handoff disagree, reality wins — and say so out loud before
continuing.** Correct `HANDOFF.md` as part of the work; never leave a known-false
packet in place for the agent after you.

### Path B — not a git repository

Legitimate, not a fault. The folder may be a pre-hackathon toolkit whose Git
history must begin only at official kickoff.

- **Do not run `git init`.** Creating a repository is a human decision, not
  part of resuming work.
- Skip the git rows of the drift table entirely.
- Verify claims against the filesystem instead: does the file named in
  `Work Just Completed` exist? Does the file named in `Exact Next Action`
  exist? Are the file contents consistent with the description?
- If the handoff claims a commit that cannot exist, flag it — that is a false
  claim worth reporting even though there is no repo to check it against.

If there is a genuine conflict you cannot resolve (ambiguous intent, two
plausible intents, missing access), **stop and ask one specific question.**
Do not pick an interpretation and build for forty tool calls.

---

## Phase 2 — Establish the working baseline

Before executing, confirm the things a handoff cannot carry:

- Are you on the intended branch, with the intended tree?
- Are required env vars present? (check names/existence, never print values)
- Does anything need to be running first — dev server, DB container, tunnel?
  If the handoff lists a port or service under Traps, start it now.
- Is the toolchain available (runtime, package manager, DB client)?

If a listed prerequisite is missing, resolve it or report it. Do not discover
it halfway through the next action.

---

## Phase 3 — Confirm understanding before executing

State back, in a few lines and without waiting for permission:

- the current objective,
- the state you verified,
- **the Exact Next Action you are about to run**,
- anything you are deliberately *not* doing.

This is ten seconds of insurance against inheriting a bad handoff. If your
understanding contradicts `HANDOFF.md`, that is the signal to stop and ask.

Then run the Exact Next Action **as written**. It was written to be executed
without a decision.

---

## Phase 4 — Execute, and stay in scope

- Continue the documented objective. Do not substitute a better one.
- Do not redesign working systems because a different design is possible
  (`AGENTS.md` §24). Note improvements in `docs/tasks.md` instead.
- Preserve the work you inherited. If you must deviate from the next action,
  say why in one line, then deviate.
- Match existing code style, naming, and file layout over your own preference.
- Do not add infrastructure the problem does not require (`AGENTS.md` §2).
- Clean up what you touch. Unrelated refactors mixed into a continuation are
  how a handoff chain turns into noise.

---

## Phase 5 — Maintain the packet

`HANDOFF.md` is now **yours** to keep true. A packet you inherited and
silently invalidated is worse than no packet.

Update it when — not only when you are finishing:

- you corrected a stale or false claim (Phase 1),
- the objective changed,
- you hit a blocker that changes the next step,
- a decision was made that the next agent must know.

When your own context runs low, or you must switch agents, invoke the
`handoff` skill. Read `HANDOFF.md`'s Traps section before you leave and add
whatever would have tripped *you* up.

---

## Anti-patterns

- **Trusting the document over the filesystem.** The handoff is a hypothesis.
- **Reading the entire repo "to be safe."** Read what the next action needs.
- **Rebuilding a plan the handoff already settled.** That is the cost you
  avoided by reading it.
- **Silently fixing drift.** Reconcile *and report* — a silent correction
  hides the fact that the packet was wrong.
- **Mixing opportunistic refactors into a continuation.** Separate commits,
  or not at all.
- **Continuing past a blocker without recording it.** The next agent inherits
  the same wall and no map of it.
- **Guessing intent when the handoff is ambiguous.** One question now beats
  forty tool calls of wrong work.

---

## Self-check before you finish

- [ ] Phase 1 drift check actually run, and any mismatch reported.
- [ ] `HANDOFF.md` corrected if it was stale or false.
- [ ] Objective and next action stated back before executing.
- [ ] Prerequisites (env, services, ports, toolchain) confirmed.
- [ ] Deviations from the documented next action were explicit.
- [ ] `docs/current-state.md` / `docs/tasks.md` reflect what actually happened.
- [ ] `HANDOFF.md` left true for the next agent.
