# Hackathon Engineering Instructions

## 1. Purpose

This repository is a reusable engineering workspace for time-constrained
hackathons and hiring challenges.

The primary objectives are:

1. Understand the problem before implementation.
2. Research the existing solution landscape.
3. Build the smallest useful end-to-end product quickly.
4. Keep architecture simple and explainable.
5. Maintain enough engineering quality for the product to be defensible
   during a technical interview.
6. Preserve project context so multiple coding agents can safely continue
   each other's work.

The repository is the canonical source of project truth.

Do not rely on conversational history for architectural decisions,
requirements, implementation status, or unresolved issues.

If conversational instructions conflict with repository documentation,
identify the conflict before changing implementation.


### Pre-Hackathon Boundary

This repository is a reusable engineering toolkit that will become a
hackathon project repository.

Before the official hackathon begins:

- do not implement problem-specific product functionality
- do not pre-build likely hackathon solutions
- do not create domain-specific workflows based on guessed problem
  statements
- **do not create a git repository or any commit in this folder**

This folder is not a git repository before the official start of the event.
Its Git history must begin only after the event starts, so that the
submission history contains no prior work.

There is no second folder and no copy step. This directory *is* the
project directory. At kickoff, run:

```bash
scripts/kickoff.sh
```

or on Windows:

```powershell
.\scripts\kickoff.ps1
```

That initializes the repository on branch `main` and deliberately creates
**no commit** unless you explicitly ask for one. Make the first commit only
once the official problem statement is in hand.


## 2. Core Engineering Philosophy

## Simplicity first

Prefer the simplest architecture that satisfies the current requirements.

Do not introduce infrastructure simply because it is considered
"production-grade."

Examples:

- Do not introduce Redis without a caching/state-management requirement.
- Do not introduce Kafka/RabbitMQ without a meaningful asynchronous workflow.
- Do not introduce microservices unless independent scaling, ownership, or
  deployment provides a concrete benefit.
- Do not introduce Elasticsearch unless search requirements justify it.
- Do not introduce NoSQL merely for perceived scalability.

Complexity must be earned.


## Build vertical slices

Prefer:

User interaction
→ API
→ business logic
→ database
→ working result

before beginning another major feature.

Avoid implementing the complete database layer, then complete backend,
then complete frontend while leaving no demonstrable workflow.


## Working product before stretch features

Prioritize:

1. core workflow
2. correctness
3. demo reliability
4. important UX states
5. deployment
6. testing
7. polish
8. stretch features

AI functionality is not automatically higher priority than the core product.


## 3. Problem Analysis

Before substantial implementation begins, ensure the repository documents:

- target users / actors
- current workflow
- pain points
- functional requirements
- non-functional requirements
- assumptions
- constraints
- unresolved questions
- MVP scope
- stretch scope
- existing systems / competitors where relevant

Primary files:

- `docs/problem.md`
- `docs/requirements.md`
- `docs/research.md`

Do not silently invent requirements.

When ambiguity materially changes architecture or product behavior,
surface the ambiguity.


## 4. Technology Selection

The technology stack must be selected based on the problem.

Do not assume any particular framework merely because it has been used
previously.

Evaluate at minimum:

- product type
- implementation time
- team familiarity
- backend complexity
- database requirements
- realtime requirements
- AI/ML requirements
- file/storage requirements
- deployment constraints
- scalability requirements

Possible defaults may include:

- Next.js / TypeScript for full product UIs
- FastAPI / Python for API-heavy or AI-heavy backends
- PostgreSQL for relational transactional workflows

These are defaults, not mandatory choices.

Document important technology choices in:

`docs/decisions.md`


## 5. Architecture Rules

Prefer a modular monolith for early-stage hackathon applications unless
there is a concrete reason not to.

For each major component, be able to answer:

- Why does it exist?
- What responsibility does it own?
- What data does it consume?
- What data does it produce?
- Is communication synchronous or asynchronous?
- What happens if it fails?
- What would force it to scale independently?

Keep architecture documentation updated in:

`docs/architecture.md`


## 6. Database Rules

Choose the database based on access patterns and consistency requirements.

For relational systems:

- use foreign keys where appropriate
- use constraints to protect invariants
- use transactions where multiple changes must remain consistent
- avoid storing large binary objects directly in relational tables
- use schema migrations for schema changes

For every important index, document:

- indexed columns
- query/access pattern it accelerates
- expected reason for the index

Do not add indexes blindly.

Keep database documentation in:

`docs/database.md`


## 7. API Rules

For important endpoints document:

- HTTP method
- route
- purpose
- request
- response
- authentication
- authorization
- failure cases
- idempotency requirements
- side effects

Keep API documentation in:

`docs/api.md`

Do not change established API contracts silently.


## 8. Backend Guidelines

Regardless of backend framework:

- keep transport/route logic small
- isolate business logic
- isolate persistence logic where practical
- validate untrusted input
- return structured errors
- enforce authorization server-side
- avoid leaking secrets or internal traces to clients
- avoid unnecessary dependencies
- make critical operations safe against duplicate requests where relevant


## 9. Frontend Guidelines

Prioritize usable workflows over visual experimentation.

Prefer reusable components.

Critical screens should account for:

- loading state
- empty state
- error state
- success feedback
- disabled/submitting state

Use a consistent visual language.

Avoid adding multiple UI libraries without justification.

Do not spend disproportionate hackathon time on animations,
complex theme systems, or cosmetic effects while core workflows are incomplete.


## 10. AI / LLM Features

AI must solve a concrete product problem.

Do not add a generic chatbot merely to claim AI functionality.

Where AI output affects structured workflows:

- prefer structured output
- validate returned data
- handle malformed responses
- provide fallbacks
- avoid making irreversible critical decisions solely from model output

Keep AI-provider integration isolated enough that providers can be changed
without rewriting unrelated application logic.


## 11. Authentication and Authorization

Authentication answers:

"Who is this user?"

Authorization answers:

"What is this user allowed to do?"

Do not confuse the two.

Authorization must be enforced by trusted backend logic, not only hidden
frontend controls.

For role-based systems, document roles and permissions.


## 12. Files and Object Storage

For large files such as:

- images
- videos
- PDFs
- reports

prefer object storage or an appropriate file service.

Store metadata/references in the primary database where appropriate.


## 13. Performance and Scaling

Do not prematurely optimize.

When reviewing performance, think in this order:

1. measure / identify bottleneck
2. inefficient application logic
3. inefficient queries
4. indexes
5. unnecessary network/database calls
6. caching
7. background processing
8. read replicas
9. partitioning
10. sharding / architectural decomposition

Do not jump directly to distributed architecture.


## 14. Reliability

For important operations consider:

- retries
- timeouts
- idempotency
- duplicate events
- partial failure
- graceful degradation

External providers should not unnecessarily make the entire application
unusable when they fail.


## 15. Security

Never:

- commit secrets
- print secrets
- expose private tokens
- hard-code credentials
- place production secrets in documentation

Use environment variables.

Commit `.env.example`, never real `.env` files.

Validate untrusted input.

Use least privilege for external tools and MCP integrations.


## 16. Git Practices

Prefer small, coherent commits.

Use descriptive commit messages such as:

- `feat: add milestone submission workflow`
- `fix: prevent duplicate approval`
- `perf: index project status query`
- `docs: record database decision`
- `test: cover inspector authorization`

Avoid meaningless messages such as:

- update
- changes
- final
- final2
- working

Do not include dates in commit messages.

Do not rewrite large working portions of the project unless there is a
concrete reason.

Before large changes, inspect the current diff and repository state.


## 17. Dependencies

Before adding a significant dependency, determine whether:

- an existing dependency already solves the problem
- the standard library is sufficient
- the added complexity is justified

Avoid unnecessary dependency growth.


## 18. Testing

Prioritize tests around:

- critical workflows
- authorization boundaries
- state transitions
- important business rules
- regression-prone functionality

Do not optimize for arbitrary coverage percentages during a hackathon.


## 19. Verification

Before declaring substantial work complete:

1. run relevant tests
2. run relevant linting
3. run type checking where applicable
4. build where appropriate
5. inspect the diff
6. verify the main affected workflow
7. update documentation if behavior or architecture changed

Never claim verification succeeded unless the commands were actually run.


## 20. Documentation Responsibilities

Maintain these documents:

- `docs/problem.md`
- `docs/requirements.md`
- `docs/research.md`
- `docs/architecture.md`
- `docs/database.md`
- `docs/api.md`
- `docs/decisions.md`
- `docs/current-state.md`
- `docs/tasks.md`
- `docs/known-issues.md`
- `docs/scale-plan.md`
- `docs/demo-script.md`

Not every file must contain extensive content from the beginning.

Only document what is known.


## 21. Decision Log

Important architecture/product decisions should be recorded in:

`docs/decisions.md`

For meaningful decisions record:

- Context
- Decision
- Reason
- Alternatives considered
- Trade-offs
- Future reconsideration trigger


## 22. Shared Agent Context

Codex, OpenCode, and any other engineering agent must treat the repository
as shared persistent memory.

Primary context files:

`AGENTS.md`
- stable operating rules

`HANDOFF.md`
- immediate agent-to-agent continuation state

`docs/current-state.md`
- current implementation state

`docs/tasks.md`
- outstanding work

`docs/decisions.md`
- durable architectural/product reasoning

Detailed technical truth belongs in the corresponding documentation file.


## 23. Handoff Protocol

After completing a substantial unit of work or before switching agents:

1. inspect `git status`
2. inspect relevant diff
3. update `docs/current-state.md`
4. update `docs/tasks.md`
5. update `docs/known-issues.md` when necessary
6. record new major decisions in `docs/decisions.md`
7. update `HANDOFF.md`
8. record verification actually performed

`HANDOFF.md` should state:

- current objective
- work just completed
- relevant changed files
- current branch
- known blockers
- unresolved questions
- next recommended task
- verification status

Do not use `HANDOFF.md` as a giant project history.


## 24. Agent Resume Protocol

When beginning work from a previous agent:

1. read `AGENTS.md`
2. read `HANDOFF.md`
3. read `docs/current-state.md`
4. read `docs/tasks.md`
5. inspect relevant architecture/API/database documentation
6. inspect `git status`
7. inspect recent commits
8. inspect uncommitted diff if one exists
9. summarize current understanding before large changes
10. continue the documented objective rather than redesigning working systems


## 25. Architecture Change Rule

Do not silently introduce:

- another database
- another queue
- another storage system
- another cloud provider
- another deployment component
- microservices
- a major framework
- a new authentication system

Document the motivation first.


## 26. Hackathon Time Awareness

Always distinguish between:

MUST FIX NOW

SHOULD FIX BEFORE DEMO

CAN EXPLAIN AS PRODUCTION EVOLUTION

DO NOT NEED

A theoretically better architecture is not automatically the best
hackathon decision.


## 27. Interview Defensibility

Implementation decisions should remain explainable.

For meaningful choices, be prepared to answer:

- Why was this chosen?
- What alternatives existed?
- What trade-off was accepted?
- What breaks first at scale?
- How would it evolve?
- What failure modes exist?
- What was intentionally deferred?

The goal is not only to generate code.

The goal is to build a product the team understands well enough to defend.


## 28. Skill Routing

Use the repository skills in `.agents/skills/` for specialized workflows.

Recommended sequence after receiving a problem:

1. `problem-analysis`
2. `research` when external research is required
3. `architecture-design`
4. `database-design` when persistent domain data exists
5. `api-design` when an API boundary exists
6. `implementation-plan`
7. implementation using normal coding capabilities
8. `frontend-build` for frontend workflows
9. `production-review`
10. `demo-readiness`
11. `interview-defense`

Use `handoff` before changing agents or when context is running low.

Use `resume-work` when continuing work created by another agent.

Do not invoke every skill mechanically.

Only invoke a skill when its workflow is relevant.

The skills are a toolbox, not a mandatory waterfall.

Typical routing:

```text
Simple problem
→ problem-analysis
→ architecture-design
→ implementation-plan
```

```text
Complex data problem
→ problem-analysis
→ research
→ architecture-design
→ database-design
→ api-design
→ implementation-plan
```