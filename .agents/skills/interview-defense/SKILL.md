---
name: interview-defense
description: Prepare the team to deeply defend its hackathon project in technical interviews by generating architecture, stack, database, API, scaling, optimization, security, failure, and ownership questions grounded in the actual repository.
---

# Interview Defense Skill

## Purpose

Use after the product is substantially complete.

This skill does not produce generic interview questions.

It must inspect the ACTUAL repository and challenge the ACTUAL decisions.

Primary goals:

1. Prepare Round 1 project defence.
2. Prepare Round 2 optimization/system-design extensions.

---

# Inputs

Read:

- `AGENTS.md`
- `HANDOFF.md`
- `docs/problem.md`
- `docs/requirements.md`
- `docs/research.md`
- `docs/architecture.md`
- `docs/database.md`
- `docs/api.md`
- `docs/decisions.md`
- `docs/current-state.md`
- `docs/scale-plan.md`
- relevant code

Inspect actual implementation before generating questions.

---

# Part A — Problem Defense

Ask:

- What problem are you solving?
- Who exactly has this problem?
- How is it solved today?
- What evidence supports the pain point?
- What existing systems did you research?
- What gap remains?
- Why does our product need to exist?
- What did you intentionally NOT solve?

Answers must distinguish research from assumptions.

---

# Part B — Product Defense

Ask:

- What is the primary workflow?
- Why is this the MVP?
- Why were these features prioritized?
- What is the most important user outcome?
- What feature would you remove first if time was shorter?
- What would you build next?

---

# Part C — Tech Stack Defense

For EVERY major technology ask:

- Why this technology?
- What alternative did you consider?
- What advantage mattered here?
- What disadvantage did you accept?
- What would make you replace it?

Examples:

Why Next.js?

Why FastAPI?

Why PostgreSQL?

Why Supabase?

Why Redis?

Why no Redis?

Why modular monolith?

Why not microservices?

Answers must reference actual project requirements.

---

# Part D — Architecture Walkthrough

Require candidate to explain:

User
→ frontend
→ backend
→ authorization
→ service
→ database
→ response

Then challenge:

- Where is state stored?
- Which component owns what?
- Which calls are synchronous?
- What is asynchronous?
- What happens when each dependency fails?

---

# Part E — Request Walkthrough

Select one important operation from code.

Example:

"Contractor submits milestone."

Ask candidate to trace:

1. frontend event
2. API call
3. validation
4. authentication
5. authorization
6. business logic
7. DB operations
8. side effects
9. response
10. frontend update

Candidate should know actual files/components involved.

---

# Part F — Database Defense

Ask:

- Why relational / document / other?
- What are the important entities?
- Why these relationships?
- Which constraints matter?
- Which indexes exist?
- What query does each index optimize?
- What requires a transaction?
- What happens with concurrent updates?
- What happens with duplicate requests?

Challenge unnecessary schema choices.

---

# Part G — API Defense

Ask:

- Why this route?
- Why this HTTP method?
- Who can call it?
- How is ownership checked?
- What happens when called twice?
- What status codes can it return?
- What side effects occur?
- What happens under concurrent calls?

---

# Part H — Security

Ask:

- How does authentication work?
- How is authorization different?
- Where is authorization enforced?
- Can one user access another user's resource?
- Where are secrets stored?
- How are uploads protected?
- What sensitive data exists?
- What would you improve for production?

---

# Part I — AI Defense

If AI exists ask:

- Why is AI necessary?
- Could deterministic logic solve this?
- What model/provider?
- Why that provider?
- What happens if output is wrong?
- Is output structured?
- Is it validated?
- What happens if provider is down?
- What is the latency/cost implication?
- Is there human review?

Attack "AI for AI's sake."

---

# Part J — Scaling

Start with:

"Your prototype works. Now 10 million users use it."

Force stepwise reasoning.

Ask:

- What breaks first?
- How do you know?
- What metrics would you inspect?
- What query becomes hot?
- What would you cache?
- What would not be safe to cache?
- Where would read replicas help?
- When would partitioning help?
- When would sharding actually be justified?

Do not accept "add microservices" as a complete answer.

---

# Part K — Caching

If caching is proposed ask:

- what key?
- what value?
- TTL?
- invalidation?
- stale-data tolerance?
- source of truth?
- what happens if Redis is down?

Expected principle:

cache failure should not normally destroy source-of-truth correctness.

---

# Part L — Message Queue

Ask:

- Why a queue?
- What work is asynchronous?
- What happens if worker crashes?
- What happens if message is delivered twice?
- How do you retry?
- Dead-letter queue?
- Ordering requirement?
- Kafka vs RabbitMQ vs simpler background job?

Do not assume Kafka is automatically the answer.

---

# Part M — Consistency

Ask:

- Which operations require strong consistency?
- Which can tolerate eventual consistency?
- What happens when distributed components partially fail?
- Could duplicate processing occur?
- How is idempotency maintained?

---

# Part N — Availability / Failure

Ask scenarios:

- database unavailable
- cache unavailable
- AI provider unavailable
- object storage unavailable
- notification provider unavailable
- worker crashes
- frontend deployment fails

Candidate should classify:

core failure

degraded mode

optional feature failure

---

# Part O — Optimization Round

Ask:

"The dashboard takes 4 seconds. Diagnose it."

Expected progression:

measure
→ identify expensive request/query
→ inspect query plan
→ reduce unnecessary calls
→ index
→ cache if justified

Not:

"Use Redis immediately."

Another:

"Database has 100M rows."

Ask:

- query patterns
- indexes
- partitioning
- replicas
- archive strategy
- shard only if justified

---

# Part P — Deployment / CI-CD

Ask:

- how is application deployed?
- what happens after push?
- which CI checks run?
- what happens when CI fails?
- when do migrations run?
- what is the health endpoint?
- how are env vars managed?
- how would you roll back?

Candidate should understand actual deployment.

---

# Part Q — Observability

Ask:

How do you know the system is failing?

Expected:

- logs
- metrics
- error tracking
- health checks
- traces if justified

Potential metrics:

- request latency
- error rate
- DB latency
- queue lag
- cache hit ratio

---

# Part R — Ownership

Very important.

Ask each team member:

- What did you personally implement?
- Which files did you own?
- Which architecture decision did you influence?
- What bug did you solve?
- What trade-off did you personally make?

Avoid claiming teammates' work.

---

# Part S — Research Attack

Act skeptical:

"Something like this already exists."

Require candidate to explain:

- researched systems
- overlap
- limitations
- actual differentiation

Do not accept unsupported claims such as:

"No product in the world does this."

---

# Part T — Red-Team Questions

Generate at least 10 project-specific adversarial questions.

Examples:

- Why isn't this just a feature of an existing platform?
- Why does this require AI?
- Your architecture is overengineered. Defend it.
- Your architecture is under-scaled. What breaks?
- Why should this data be trusted?
- What if the user lies?
- What if two approvals happen simultaneously?
- Why are you storing this data?
- Why not use a managed service?
- What did your team actually build versus mock?

---

# Mock Interview Mode

Conduct interview in rounds.

## Round 1 — Explanation

Candidate explains project without interruption.

Then critique:

- unclear points
- unsupported claims
- weak architecture knowledge
- missing trade-offs

## Round 2 — Deep Dive

Ask stack/schema/API questions.

## Round 3 — Scale

Increase traffic dramatically.

## Round 4 — Failure

Break dependencies.

## Round 5 — Optimization

Give latency/DB bottlenecks.

## Round 6 — Ownership

Ask what candidate personally built.

---

# Answer Evaluation

For each answer classify:

STRONG

ACCEPTABLE

WEAK

DANGEROUS

Explain why.

Do not manufacture implementation details.

If candidate claims something not present in repository/documentation,
flag the discrepancy.

---

# Required Output

Produce:

## 30 Most Likely Questions

## 15 Architecture Questions

## 10 Database Questions

## 10 API Questions

## 10 Scaling Questions

## 10 Failure Questions

## 10 Security Questions

## 10 Project-Specific Adversarial Questions

## Weak Areas Found in Current Repository

## Claims Candidate Must Avoid

## Best Architecture Walkthrough

## Best 2-Minute Tech Stack Explanation

## Production Evolution Narrative

Do not fabricate facts about the project.
