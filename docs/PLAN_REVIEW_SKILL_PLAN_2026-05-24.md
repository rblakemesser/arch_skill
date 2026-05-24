# Plan Review Skill Plan

Status: planning document only. Do not treat this as implemented behavior.

Date: 2026-05-24

Working skill name: `plan-review`

## Doctrine-Only Build Constraint

This is a doctrine-only skill plan.

When this plan is implemented, the skill should be built as agent guidance:
`SKILL.md`, reference docs, trigger metadata, and examples. The workflow is
deliberately made of judgment, ordered reading, review lenses, audit-log
discipline, and output contracts.

Do not turn this plan into:

- a deterministic harness
- a runner
- a controller
- a rule engine
- a scorer
- a checklist executor
- a grep gate
- an automated architecture validator
- a script that decides whether a plan is elegant, ready, or complete

The checklists in this document are doctrine for human/agent judgment. They are
not specifications for a deterministic engine. The audit log is a durable
Markdown review ledger beside the plan, not a state machine that owns the
workflow. Scripts are out of scope unless a future user explicitly asks for a
narrow helper that handles only mechanical formatting or extraction and does
not own review judgment.

## 0. User Problem

The user wants a reusable skill that can be run during planning, before
implementation, to audit a plan against the actual codebase with an extremely
high architecture bar.

The target review is not "does this plan sound reasonable?" It is:

- Does the plan state the North Star outcome before it lists tasks?
- Does it define explicit done-state requirements: when this plan is complete,
  these concrete things will be true?
- Is this the most elegant credible architecture available from this repo?
- Does the plan route through the canonical owner path instead of creating a
  second way to do the same thing?
- Does it reduce bug vectors rather than move them around?
- Does it delete legacy paths, dead code, duplicate truth, stale docs, bad
  defaults, and side doors instead of retiring or archiving them?
- Does it close every adjacent surface that could let old behavior survive?
- Does it choose central clean abstractions only where they reduce real
  complexity?
- Does it avoid bloated infrastructure, speculative tooling, compatibility
  shims, and "cleanup later" placeholders?
- Does it build depth-first by proving one narrow integrated slice before
  widening, instead of discovering at the end that the architecture was broken
  from the start?
- Does it resolve real ambiguity where two reasonable implementers could build
  different outcomes, especially around requirements, constraints, compatibility,
  deletes, and proof?
- Can implementation and later audit prove completion without guessing?

Canonical user asks:

```text
Use plan-review on docs/FEATURE_PLAN.md. Audit it against the code and tell me
where the architecture is not elegant enough.
```

```text
Run the hardcore plan review skill before we implement this. I want parallel
agents looking for side doors, deletion gaps, duplicate truth, and simpler
architectures.
```

```text
Review this plan for whether it actually converges the codebase, deletes old
paths, and avoids new bug vectors.
```

Anti-cases:

- "Implement Phase 4 with parallel workers." Use `plan-swarm`.
- "Review this branch diff before merge." Use `code-review`, optionally with
  `thermo-nuclear-code-quality-review`.
- "Create the architecture plan from scratch." Use `arch-step`,
  `miniarch-step`, `arch-mini-plan`, or `lilarch` depending on size.
- "Clean up stale repo docs after code is stable." Use `arch-docs`.

## 1. North Star

Build a read-only planning-stage review skill that audits one existing plan doc
against repo truth, uses parallel independent review agents when available, and
returns evidence-backed findings about where the plan is not yet the cleanest,
simplest, most convergent architecture the codebase can support.

The skill's job is to raise the plan's architectural ceiling before code is
written. It should be severe about elegance, but not bloated. The winning plan
is the one that makes the correct implementation feel inevitable: fewer live
paths, fewer branches, clearer ownership, harder-to-misuse APIs, better
boundary types, explicit done-state truths, depth-first proof, and no leftover
wrong road.

The skill is review-first. It does not implement code. It does not create a
second plan. It does not silently rewrite scope. It returns a verdict, blocking
findings, optional plan repair guidance, exact evidence anchors, and a durable
audit log beside the plan so repeated review loops can converge instead of
starting over.

## 2. Mechanism Choice

This should be a skill, not just a one-shot prompt, because the workflow is
repeated, high judgment, repo-grounded, and easy to underdo. A useful run needs
the same recurring pieces:

- plan target resolution
- audit log resolution or creation
- local instruction and repo convention reading
- code-backed current architecture mapping
- adjacent-surface and call-site search
- exhaustive relevant-code coverage tracking
- parallel lens review
- parent synthesis
- severe architecture and elegance bar
- findings-first output with exact plan repair guidance

V1 should be prompt-first, not script-backed.

The top-level doctrine-only constraint controls this section. The references
and checklists are meant to sharpen agent judgment, not to become deterministic
implementation machinery.

The skill should use existing subprocess capabilities instead of inventing a
runner:

- Use `fresh-consult` for observation-only parallel cold reads when the host
  skill surface supports it and the user wants multiple model reads.
- Use `agent-delegate` only if a child must run local commands with a concrete
  read-only task and a clear write scope of `none`.
- Child agents are read-only. The parent may create or update only the plan
  review audit log sidecar unless the user explicitly asks for plan edits.
- Do not create a deterministic orchestrator, controller, or state machine in
  V1. The parent agent can coordinate a small set of read-only review prompts.

A future script may be justified only for narrow mechanics such as generating a
blank review artifact, extracting heading anchors from a Markdown plan, or
normalizing child output. The script must not own review judgment.

## 3. Reviewed Doctrine Inputs

This plan pulls architecture-quality doctrine from the repo's existing skills
and planning docs. The important source files inspected were:

| Source | Relevant doctrine pulled into `plan-review` |
| --- | --- |
| `skills/arch-step/references/shared-doctrine.md` | Code is ground truth; find the canonical path before designing; single source of truth by default; adjacent surfaces must be classified; prefer hard cutover, explicit deletes, and fail-loud boundaries; runtime shims need explicit approval and removal plans. |
| `skills/arch-step/references/section-quality.md` | Strong plans name current and target architecture, canonical owner path, call-site audit, delete list, compatibility posture, concrete phase exit criteria, and proof that later audit can validate. |
| `skills/arch-step/references/arch-review-gate.md` | Review asks whether the plan is idiomatic, convergent, decision-complete, routed through canonical paths, free of unnecessary new paths, and grounded in existing agent/model capabilities when relevant. |
| `skills/arch-step/references/arch-overbuild-protector.md` | Separate required convergence work from product creep and architecture theater; reject docs-audit scripts, stale-term greps, absence gates, repo-layout policing, and capability-replacing tooling unless explicitly required. |
| `skills/arch-step/references/arch-phase-plan.md` | Section 7 must be the one authoritative checklist; phases should be depth-first, prove the canonical owner path early, and make required deletes, cleanup, docs/comments, and proof visible in checklist or exit criteria. |
| `skills/arch-step/references/arch-consistency-pass.md` | Cold-read the whole plan for cross-section contradictions before implementation; unresolved decisions, unauthorized scope cuts, orphan obligations, and non-auditable exit criteria block readiness. |
| `skills/arch-step/references/arch-audit-implementation.md` | Audit must verify SSOT, required deletes, no forbidden shims, no parallel path, behavior preservation, call-site completeness, and plan promises against code reality. `plan-review` should catch these before implementation. |
| `vendor/cursor/plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md` | Look for code-judo moves that delete complexity; push for dramatically simpler structure; flag spaghetti conditionals, thin wrappers, wrong-layer logic, cast-heavy contracts, file sprawl, and missed decomposition. |
| `skills/code-review/SKILL.md` and `skills/code-review/references/reviewer-prompt.md` | Map before findings; derive local policy first; read changed or relevant code directly; use parallel lenses; emit sparse evidence-backed findings; reviewer summaries are evidence, not verdicts. |
| `skills/code-review/references/review-requirements.md` | Mandatory lenses include correctness, architecture, proof, docs drift, security when triggered, and agent-linter when instruction-bearing surfaces change. Also flags duplication, drift, shims, feature flags, test-only branches, and fallback paths not authorized by the plan. |
| `skills/audit-loop/SKILL.md` and `skills/audit-loop/references/shared-doctrine.md` | Exhaustive map before action; rank by consequence first; dead code is a bug waiting to happen; duplication is deferred breakage; every change needs post-change audit for safety, consequences, elegance, and duplication. |
| `skills/audit-loop/references/quality-bar.md` | Strong findings tie code anchors to consequence and fixable risk; strong stop decisions do not call work clean while major unresolved risks remain. |
| `skills/arch-docs/SKILL.md` | Stale docs and old point-in-time docs are wrong-path risks; durable truth should move to canonical homes and obsolete working docs should be deleted. Git is the archive. |
| `docs/coordination_kit_specialists/cleanup.md` | Cleanup exists because projects can pass feature tests while leaving future agents an easy wrong path; stale paths, bad defaults, duplicate truth, and side doors need explicit classification. |
| `docs/coordination_kit_specialists/code_quality_critic.md` | The honest review unit is the changed subsystem and affected call sites, not one isolated file; code can match spec and still be a bad path to inherit. |
| `docs/coordination_kit_specialists/spec_compliance_critic.md` | A reviewer reads the plan, requirements, diff, and evidence directly; it does not trust implementer summaries or invent new requirements. |
| `docs/coordination_kit_specialists/closure.md` | Completion must be reconstructable from disk through contracts, evidence, gate records, waivers, and residual risks, not chat memory. |
| `docs/coordination_kit_specialists/dual_witness.md` | Judgment-heavy decisions should use independent reads before convergence and must record rejected alternatives and plan amendment needs. |
| `skills/arch-mini-plan/references/quality-bar.md` | Strong plans name real files, symbols, ownership before/after, deletes, migrations, phase goals, verification, and done bars. Weak plans rely on vague "update all usages" language. |
| `skills/arch-mini-plan/references/shared-doctrine.md` | Plan compression must not lower the quality bar; code is ground truth; prompt/native capability options get first right of refusal for agent-backed systems. |
| `skills/lilarch/references/shared-doctrine.md` | Compact plans still need real current/target architecture, explicit defaults, hard cutover, deletes, and no "cleanup later" without ownership. |
| `skills/bugs-flow/references/fix.md` | Fixes should go to the one correct boundary; no silent fallbacks, stale-cache masks, old-API fallbacks, or false tests preserved as contracts. |
| `skills/plan-swarm/SKILL.md` and references | Parallel agents should receive a compact source-of-truth contract, work by owner/proof boundaries, and route review findings through triage rather than scope expansion. |
| `skills/fresh-consult/SKILL.md` | Clean read-only child agents are for second opinions, completion checks, consistency audits, and confusion checks; they do not edit. |
| `skills/agent-delegate/SKILL.md` | Delegated children need concrete task, success bar, work root, allowed write scope, constraints, and a report contract; parallel children must not revert unfamiliar work. |
| `skills/model-consensus/SKILL.md` | Agreement is not accumulation; in architecture mode, prefer one existing path over two new ones and force simpler converged plans. |
| `skills/skill-authoring/SKILL.md` | Skills are prompt contracts first; keep V1 lean, self-contained, peer-aware, and anti-heuristic; add scripts only when deterministic mechanics earn them. |
| `skills/prompt-authoring/SKILL.md` | Write mission-level intent, rich quality bars, evidence policy, completion rules, and recognition tests; avoid brittle keyword routers and giant checklists. |
| `skills/skill-flow/SKILL.md` | Keep jobs distinct, handoffs concrete, and peer boundaries clear; do not replace judgment with runner scaffolding. |

## 4. Architecture Quality Canon

`plan-review` should encode these repo-native architecture opinions as its
quality bar.

### 4.1 Code Truth Before Plan Confidence

A plan is not strong because it sounds complete. It is strong when its claims
survive contact with the files, symbols, tests, generated artifacts, runtime
config, prompts, docs, and local instructions that actually govern the system.

The review must read code before approving a plan. If the plan names a target
architecture without identifying current owner paths and affected call sites,
that is a blocking weakness.

The review must read all relevant code. "All relevant" means every code surface
needed to validate the plan's claims, not every file in the repository. At
minimum, that includes:

- files and symbols named by the plan
- current owner modules and likely target owner modules
- public callers and representative internal call sites
- alternate entrypoints, commands, routes, jobs, scripts, UI paths, prompts, or
  generated artifacts that can exercise the same behavior
- persistence, schema, config, fixture, adapter, and test surfaces that define
  or preserve the contract
- comparable existing patterns in the repo
- stale or legacy code paths the plan claims to delete, migrate, or supersede

If the reviewer cannot tell whether more relevant code exists, the next move is
repo search and code reading, not approval. Parallel read-only agents should be
used for broad code mapping when the surface is large, so exhaustive reading is
fast enough to be practical.

### 4.2 Architect For A Tiny Team

The target audience is a tiny developer team, not a large platform
organization. The code must be easy to inherit by three busy developers who do
not have spare staff for ceremony, framework maintenance, or long archaeology.

The best plan favors:

- self-documenting names, shapes, and boundaries over explanatory sprawl
- direct control flow over clever indirection
- fewer files and fewer moving parts when that does not muddy ownership
- well-debugged existing libraries for solved problems
- boring, familiar repo patterns over bespoke infrastructure
- one obvious debugging path when production behavior is wrong
- simple code that a tired developer can safely modify later

The plan should be blocked when it creates maintenance work the team cannot
afford: custom frameworks, unnecessary runners, home-grown parsers, broad
config systems, generic plugin layers, or abstractions that require a mental
model larger than the problem.

### 4.3 Outcome North Star And Inescapable Done State

A plan should not begin as a task list. It should begin with the world it is
trying to make true.

The North Star is the plain outcome:

```text
We are trying to make <this system/user/developer outcome> true.
```

The explicit requirements beneath it are the done-state truths:

```text
When this plan is done, these things will be true.
```

Those truths should be specific enough that a reviewer cannot hand-wave around
them. They should be outcome-facing or user-facing when possible, and code-
quality-facing when the plan is about architecture. A good done-state says what
will be impossible, deleted, simpler, centralized, or proven after the work
lands.

A strong plan names done-state requirements like:

- the user-visible behavior that must work
- the developer-facing path that must become the only obvious path
- the old path, side door, fallback, or duplicate truth that must be gone
- the complexity that must not be introduced
- the abstraction that is allowed, avoided, deleted, or required
- the integration proof that makes the outcome real
- the maintenance burden that must be lower after the change

Weak requirements are task-shaped:

- "update the service"
- "add support"
- "refactor the flow"
- "clean this up"

Strong requirements are truth-shaped:

- "all writes go through one owner"
- "callers cannot choose old versus new behavior"
- "there is no compatibility fallback after migration"
- "the real checkout path proves the write reaches persistence through the
  canonical service"
- "the abstraction count goes down unless a new abstraction deletes a larger
  caller burden"

The review must ask whether the plan's tasks actually produce the North Star
outcome. If the plan can complete every checkbox while the intended outcome is
still not true, the plan is not ready.

### 4.4 Requirements, Constraints, And Complexity Budget Up Front

Before reviewing architecture, the plan must state the inputs that control the
architecture:

- requirements
- non-requirements
- hard constraints
- non-constraints
- assumptions or beliefs
- complexity sources

A non-requirement is something the plan explicitly does not need to support. A
non-constraint is something that looks limiting but is not actually binding.

The review should ask:

- Which requirements are actually driving code shape?
- Which constraints are real, and where is the evidence?
- Which assumed constraints are making the plan more complex than necessary?
- What complexity exists only because the plan believed something that might
  not be true?
- Can any requirement be narrowed without cutting approved behavior?
- Can any constraint be removed, replaced, or made explicit so the architecture
  becomes simpler?

Every plan should have a complexity budget: name the few pieces of complexity
that are truly buying correctness, capability, or maintainability. Complexity
that cannot point back to a real requirement, hard constraint, or drift-proofing
need should be removed.

### 4.5 Real Ambiguity And Miscommunication Risk

A plan can be dangerous even when every sentence sounds reasonable. If an
outcome, requirement, constraint, or non-requirement can be read two different
ways, two implementers can build two different systems.

`plan-review` must identify real ambiguity that changes implementation. It
must not ask fake questions, restate obvious preferences, or make the user
resolve contrived wording issues. It should read the repo and local context
first, then only surface ambiguity that materially affects outcome, scope,
architecture, constraints, deletion, compatibility, proof, or phase order.

The ambiguity test is:

```text
Could two reasonable implementers read this plan and build meaningfully
different outcomes?
```

If yes, the review should name:

- the ambiguous phrase, requirement, constraint, or outcome
- the plausible interpretations
- why those interpretations produce different architecture or proof
- the decision that must be made before implementation
- whether repo truth already resolves it

Examples of real ambiguity:

- "replace the old path" could mean delete it, hide it behind a fallback, or
  keep it for one legacy entrypoint.
- "support existing users" could mean preserve behavior exactly, migrate data
  once, maintain two contracts, or provide a temporary bridge.
- "use the existing pattern" could mean extend the canonical owner, copy a
  nearby anti-pattern, or converge several similar flows.
- "add a shared abstraction" could mean one domain owner, one helper package,
  one adapter boundary, or a broad framework.
- "good test coverage" could mean one integration proof through the real seam
  or many low-value unit tests.

Examples of fake ambiguity:

- asking whether the code should be maintainable
- asking whether tests should run
- asking whether obvious repo conventions should be followed
- asking a question already answered by the plan, code, or local instructions

Outcome-changing ambiguity must be resolved definitively before the plan is
done. The reviewer should not turn that into a general question list; it should
return the smallest set of decisions that actually changes the plan.

Resolution is not just an answer in chat. After an audit finds real ambiguity,
constraint confusion, or non-constraint confusion, somebody with authority must
reconcile it: either the user, or an agent explicitly given permission to make
that decision from repo evidence and stated intent. Then the plan must be
updated so the decision carries through the rest of the artifact.

Carry-through means the resolved decision is reflected everywhere it changes
meaning:

- North Star and done-state requirements
- requirements, non-requirements, constraints, and non-constraints
- target architecture
- canonical owner path
- compatibility or bridge posture
- delete list and side-door closure
- phase order and phase exit criteria
- proof strategy
- docs, prompts, examples, or instructions touched by the decision

A plan cannot be marked done while ambiguity and constraint questions are only
listed in the audit log or answered in conversation. The plan itself must carry
the reconciled truth.

### 4.6 Simplicity Pressure Loop

`plan-review` should repeatedly ask one question:

```text
Can this be simpler without breaking the stated requirements?
```

Ask it against:

- the target architecture
- the state model
- the caller API
- the phase plan
- the proof strategy
- new abstractions
- new tooling
- compatibility or migration posture
- cleanup and delete work

This is not a request to underbuild. It is a pressure loop that strips away
imagined constraints, fake safety, unused extension points, and generalized
machinery until only required complexity remains.

### 4.7 Depth-First Implementation Risk

The plan must be depth-first unless there is a real reason it cannot be.
Depth-first means the first implementation slice proves one narrow end-to-end
path through the intended architecture and highest-risk integration seam before
the plan widens.

Breadth-first plans are risky because they build layers, variants, helpers, and
parallel workstreams that only meet at the end. That lets a broken assumption
hide until the project is expensive to unwind.

A strong phase sequence is:

1. Prove one real path.
2. Verify it in the real runtime, simulator, command path, integration test, or
   closest honest environment.
3. Widen to the next caller, variant, platform, or feature.
4. Verify again.
5. Add polish, optional modes, and extra coverage only after the core
   abstraction has survived integration.

The review must ask:

- What is the first narrow slice that proves the architecture works?
- Which highest-risk seam does that slice cross?
- What exact proof must pass before the plan widens?
- Does each later phase build on a proven integrated base?
- Is any complexity being added before the core path is proven?
- Can a phase be marked complete with only unit tests, mocks, typecheck, or
  "works in theory" proof?

Block plans that create a wide scaffold first and defer integration proof to
the end. The safest plan makes wrong architecture fail early, while the system
is still small enough to change.

### 4.8 Canonical Owner Path Or Bust

The plan should extend or simplify the existing canonical owner path whenever
that path can own the behavior cleanly.

Block the plan when it:

- creates a parallel implementation beside an extendable owner
- adds a duplicate writer, reader, command path, prompt truth, schema truth, or
  helper truth
- routes around the boundary that already owns the concept
- leaves a new abstraction without a real caller-driven reason to exist
- uses a wrapper mainly to hide an unresolved contract

### 4.9 Existing Pattern And Convergence Audit

Before a plan introduces a pattern, abstraction, service, state model, API
shape, event flow, hook, adapter, command path, or persistence path, it must
prove it inspected the repo's existing design language.

The review must ask:

- What else in this repo already solves this kind of problem?
- Which existing pattern is the best pattern to extend?
- Which similar pattern is local debt and should not be copied?
- Does the proposed design create a new pattern where an old one could have
  been made canonical?
- What existing code should move onto the chosen pattern now?
- What existing code should stay different because it has a real different
  reason?
- What old pattern, helper, API, or state shape becomes obsolete and should be
  deleted?

A strong plan includes a pattern inventory. It names comparable services,
adapters, handlers, state machines, validators, persistence flows, async
workflows, UI controllers, prompt/runtime patterns, generated artifacts, and
tests when they belong to the same family.

A strong plan also includes a convergence sweep:

- `move now`: related code that must migrate for the architecture to be honest
- `delete now`: old paths made obsolete by the new owner path
- `leave alone`: similar code with a real different contract
- `named follow-up`: real work outside current scope, with an owner or trigger
- `user decision`: scope or behavior choice the repo cannot answer

Do not let the plan add a shiny new pattern beside older live patterns without
classifying the old ones. That creates a better local implementation while the
repo as a whole gets worse.

### 4.10 Caller Shape And Misuse Resistance

The reviewer should inspect the architecture from the caller's side. The best
plans make correct usage obvious and incorrect usage hard.

Block the plan when callers must:

- know internal lifecycle rules that should belong to the owner module
- pass several flags, modes, nullable fields, or magic strings to get ordinary
  behavior
- repeat the same validation, fallback, cleanup, or edge-case handling
- choose between old and new APIs
- bypass the owner path to make common work possible

Good plans make the caller say the simple thing it wants and put the dangerous
details behind the boundary that owns them.

### 4.11 Drift-Proof Coupling

When components depend on each other, the plan must make the shared dependency
hard to drift.

The review should ask:

- Is shared behavior represented once, or copied into several places?
- Can one side change while the other silently keeps the old contract?
- Do generated artifacts, fixtures, schemas, prompts, examples, adapters, and
  tests all read the same source of truth where they should?
- Does the plan create a contract boundary that fails loudly when dependents
  drift?
- Are versioned bridges timeboxed with removal work, or are two contracts going
  to live forever?

Drift-proofing should come from structure: shared code, typed contracts,
generated artifacts, one writer, one validator, one schema, one adapter
boundary, or fail-loud runtime checks. It should not depend on everyone
remembering to update matching files by hand.

### 4.12 Invariants, State Model, And Atomicity

The plan must name the invariants that make the system safe. An invariant is a
rule that must always stay true, such as one active writer, one session owner,
one source of saved state, or one validation boundary.

The review should ask:

- Where does each invariant live in code?
- Can the type or state model represent impossible combinations?
- Are new booleans, modes, nullable fields, or partial states multiplying
  conditionals?
- Can a small state machine or typed model delete branches?
- Can related updates succeed or fail together, or can the system be left
  half-migrated?

Plans should be blocked when they rely on future developers remembering
invariants instead of making those invariants real in code, types, API shape,
runtime routing, or deletion.

### 4.13 Abstraction Earning Test

Every new abstraction must earn its keep.

A good abstraction:

- removes repeated logic
- gives one name to a real domain concept
- hides a dangerous boundary
- makes callers simpler
- makes invalid usage harder
- creates one place to change behavior later

A bad abstraction:

- wraps one function without simplifying anything
- passes parameters through unchanged
- hides a messy contract instead of fixing it
- introduces a framework before examples justify it
- makes readers learn a new concept while old concepts remain live

`plan-review` should be hostile to fake abstractions. New structure is good
only when the repo becomes simpler after it lands.

### 4.14 Layer Boundary And Refactor Radius

The plan must put logic in the layer that owns it and must name the natural
refactor radius.

The review should ask:

- Is product logic leaking into UI?
- Is persistence logic leaking into components?
- Is feature-specific logic leaking into shared code?
- Is orchestration mixed with business logic?
- Is a caller being asked to know details only the callee should know?
- How far must related code move for the architecture to be honest?

The refactor radius may be one function, one module, one feature, one contract
family, one call-site family, one generated artifact path, or one runtime
boundary. A plan is too small in a dangerous way when it changes the new path
but leaves the rest of the contract family split.

### 4.15 Concept Count Budget

The reviewer should ask whether the repo has fewer live concepts or more live
concepts after the plan lands.

A strong plan can add one concept if it deletes, merges, privatizes, or makes
unreachable several weaker concepts. A weak plan adds a new concept while all
old concepts remain available.

The review should track:

- concepts added
- concepts deleted
- concepts merged
- concepts made private
- concepts still exposed
- concepts deliberately left alone

Every live concept is a future bug surface. The best plans lower the number of
choices future developers can get wrong.

### 4.16 Elegance Means Fewer Live Concepts

Elegance is not more architecture. Elegance is fewer concepts needed to explain
the same behavior.

The reviewer should actively search for a simpler reframing:

- delete a whole branch instead of centralizing it
- make the state model remove conditionals
- route through one default flow instead of many exceptions
- use a typed contract so optionality and casts disappear
- place logic in the module that already owns the concept
- split a swollen file only when the split creates real ownership, not another
  maze

### 4.17 Delete Legacy Paths, Do Not Archive Them

Git is the archive. Plans should delete retired live truth surfaces when they
are in scope:

- old code paths
- stale feature flags
- compatibility shims
- duplicate APIs
- obsolete docs
- stale comments
- old prompts or instructions
- generated artifacts no longer consumed
- bad defaults and wrong examples

Keeping a wrong live path "just in case" is a bug vector. The plan must either
delete it, prove it is out of scope, or record a timeboxed bridge with a clear
removal checkpoint.

### 4.18 Close Side Doors

The plan must inspect and close side doors that can keep the old behavior alive:

- alternative entrypoints
- CLI commands, scripts, or UI affordances
- direct mutation paths
- fallback readers or writers
- fixtures and examples that teach old usage
- docs that point to old commands
- tests that encode the old contract
- prompt snippets and agent instructions that still route users or agents down
  the wrong path

If the plan only changes the happy path, it is not architecture-complete.

### 4.19 Boundaries Must Be Real

Boundaries belong in code, runtime routing, types, APIs, behavior, and shipped
contracts. They should not rely on:

- stale-term grep gates
- absence tests
- docs-audit scripts
- repo layout policing
- CI checks whose main purpose is taxonomy cleanliness
- comments that say "do not use" while the path remains callable

### 4.20 Proof Should Be Integration-First And Meaningful

Verification should prove behavior, preservation, or the actual contract. It
should not reward deletion trivia or bureaucracy.

Strong proof:

- targets the highest-risk seam
- favors integration tests when behavior crosses modules, persistence, runtime
  boundaries, commands, generated artifacts, UI state, or agent/tool contracts
- proves behavior preservation after refactor or convergence
- covers affected call-site families
- uses existing tests, typecheck, build, runtime assertions, instrumentation,
  or a short manual checklist when that is the honest signal

Unit tests are useful when they protect a tricky isolated rule. They are weak
when they only prove the compiler, mock a behavior that should be integrated,
or lock implementation details that a later refactor should be free to change.
For this team, a smaller number of behavior-level integration tests is usually
worth more than a large pile of shallow unit tests.

Weak proof:

- "run all tests" with no relation to the plan
- unit tests that only prove the compiler, framework, or mock setup works
- deleted-code proof tests
- visual constants
- brittle goldens
- mock-only interaction tests
- keyword absence gates
- coverage bumps without protected behavior

### 4.21 Plan Readiness Is Decision Completeness

The plan is not ready while unresolved decisions remain about:

- requested behavior scope
- allowed architectural convergence scope
- canonical owner path
- adjacent-surface disposition
- compatibility posture
- required deletes
- fallback or bridge policy
- behavior-preservation proof
- phase-exit evidence
- live docs, comments, prompts, or instruction cleanup

Uncertainty that changes architecture is not a follow-up. It is a blocker
question or a required plan repair.

## 5. Skill Lane And Peer Boundary

`plan-review` is a planning-stage architecture reviewer. It sits between plan
authoring and implementation.

| Nearby skill | Boundary |
| --- | --- |
| `arch-step`, `miniarch-step`, `arch-mini-plan`, `lilarch` | These create, repair, or execute architecture plans. `plan-review` audits an existing plan for maximum elegance and convergence. It does not own the full planning workflow. |
| `arch-step review-gate` | `review-gate` is local and integrates feedback into one arch artifact. `plan-review` is a reusable, standalone hardcore review skill with parallel independent agents and a broader architecture-quality canon. |
| `arch-step consistency-pass` | `consistency-pass` checks cross-section agreement inside one canonical full-arch doc. `plan-review` checks the plan against code truth, canonical architecture, side doors, delete obligations, and more elegant alternatives. |
| `code-review` | `code-review` reviews code diffs or completion claims after code exists. `plan-review` reviews plans before implementation. |
| `thermo-nuclear-code-quality-review` | Thermo reviews implementation maintainability. `plan-review` imports that severity into pre-implementation plan review. |
| `fresh-consult` | `fresh-consult` is the generic read-only second-opinion primitive. `plan-review` shapes the specific plan-audit question and synthesizes findings. |
| `agent-delegate` | `agent-delegate` is an operational child-worker primitive. `plan-review` may use it read-only for concrete lens tasks, but does not become implementation delegation. |
| `model-consensus` | `model-consensus` converges two models on a plan or concept. `plan-review` is findings-first audit. Use `model-consensus` only when the user wants model dialogue or adversarial convergence rather than a review verdict. |
| `plan-swarm` | `plan-swarm` implements approved plan phases with parallel workers. `plan-review` can run before `plan-swarm` to harden the plan. |
| `audit-loop` | `audit-loop` audits and fixes repo risks. `plan-review` audits one plan's architecture and does not edit code. |
| `arch-docs` | `arch-docs` cleans repo docs after code truth is stable. `plan-review` flags doc/comment/instruction cleanup required by the plan's architecture. |

The proposed trigger should reject generic "review this code" and generic
"write a plan" asks. It should fire for plan-audit language where the target
artifact is a plan, strategy, architecture proposal, phase plan, implementation
plan, migration plan, or design doc and the user wants architectural severity.

## 6. V1 Workflow

### 6.1 Intake

Resolve:

- `PLAN_PATH`
- audit log path, defaulting to `<PLAN_STEM>_PLAN_REVIEW_AUDIT.md` beside the
  plan
- review scope: whole plan, named phase, or named section
- code root
- whether parallel agents are requested, available, or implied by the skill
- model/runtime policy if the user pins it
- whether the user explicitly asked for plan edits; otherwise only the audit
  log sidecar may be written

Do not ask about anything discoverable from the repo. Read local instructions,
the plan, and repo conventions first.

### 6.2 Parent Grounding Pass

The parent agent must read enough code before launching child review prompts to
shape useful lenses. Minimum parent read:

- local `AGENTS.md`, `CLAUDE.md`, `README.md`, and relevant build/test config
- the full plan or requested scope
- existing plan review audit log if present
- North Star outcome and explicit done-state requirements
- requirements, non-requirements, constraints, non-constraints, assumptions,
  and complexity sources stated by the plan
- ambiguous outcome, constraint, compatibility, deletion, proof, or phase
  language that could change implementation
- target architecture sections
- call-site audit or equivalent inventory
- phase plan and exit criteria
- first planned implementation slice, widening sequence, and proof required
  before each phase expands scope
- plan-defined deletes, cleanup, compatibility, fallback, and verification
- files and symbols the plan names
- quick repo search for the old and new concepts
- all relevant code needed to validate the plan's claims, with parallel
  read-only agents encouraged for broad surfaces
- search for similar existing patterns before accepting new services,
  adapters, handlers, state models, APIs, command paths, generated artifacts,
  or persistence flows
- caller-side shape of the proposed API or boundary
- likely invariants, partial-state risks, and misuse paths
- shared dependencies or contract families that could drift
- proof strategy, with special attention to integration coverage versus
  low-value unit tests

The parent records a compact review brief:

- plan path and requested scope
- audit log path and prior unresolved findings
- user intent and stop boundary
- North Star outcome and done-state requirements
- stated requirements, non-requirements, constraints, non-constraints, and
  assumptions
- real ambiguity or miscommunication risks that repo truth does not resolve
- complexity sources and the requirements or constraints that justify them
- current architecture anchors
- target architecture claims
- relevant code read and relevant code still unknown
- likely canonical owner paths
- comparable existing patterns and the candidate canonical pattern
- nearby old patterns that may need migration, deletion, or explicit exclusion
- first narrow slice, highest-risk seam, and whether the sequence is
  depth-first or breadth-first
- likely old paths and side doors
- likely drift-prone shared dependencies
- likely integration proof needed
- proof gates that must pass before later phases widen the implementation
- likely adjacent surfaces
- review lenses to launch

This brief is not a new plan. It is a child-agent briefing and synthesis aid.

### 6.3 Parallel Lens Fanout

When parallel agents are available, launch independent read-only lenses. For a
small plan, combine adjacent lenses in one reviewer prompt. For a substantial
plan, split the required lenses below into distinct reviewers or tightly paired
reviewer prompts. Do not spawn more agents than the plan can feed with distinct
work.

Use parallel agents aggressively for code reading when the relevant surface is
large. The parent should split by owner path, caller family, legacy path,
generated/contract surface, tests/proof surface, or comparable pattern family.
The point is not parallel theater; the point is to make "read all relevant
code" practical and repeatable during a plan-refinement loop.

Required lenses for substantial plans:

1. `outcome-north-star`
   - Check whether the plan states the North Star outcome before task detail.
   - Verify that done-state requirements say what will be true when the plan is
     complete.
   - Require outcome-facing or user-facing requirements where possible, and
     code-quality requirements for complexity, abstraction, deletion,
     centralization, drift-proofing, and proof where architecture is the work.
   - Block plans whose checklists can complete while the stated outcome remains
     false.

2. `ambiguity-and-miscommunication`
   - Find real ambiguity where two reasonable implementers could build
     different outcomes.
   - Focus on outcome, requirements, constraints, non-constraints,
     compatibility, deletion, proof, and phase sequencing.
   - Ignore fake ambiguity and questions already answered by repo truth.
   - Return the smallest set of decisions that must be resolved before
     implementation.

3. `requirements-constraints-simplicity`
   - Check whether the plan states real requirements, non-requirements, hard
     constraints, non-constraints, assumptions, and complexity sources up
     front.
   - Challenge every complexity source with: can this be simpler without
     breaking the stated requirements?

4. `tiny-team-maintainability`
   - Judge whether the design fits a three-developer team.
   - Prefer self-documenting code, simple control flow, well-debugged existing
     libraries for solved problems, and minimal custom infrastructure.
   - Block architecture that creates ongoing maintenance burden without clear
     payoff.

5. `depth-first-risk`
   - Check whether the phase plan proves a narrow end-to-end path before it
     widens.
   - Identify the first integrated slice, highest-risk seam, and exact proof
     required before adding callers, variants, platforms, or features.
   - Block breadth-first layer scaffolding, parallel disconnected workstreams,
     and phase exits that rely on unit-only, mock-only, or "works in theory"
     proof where integration is the real risk.

6. `code-truth-map`
   - Verify that the plan's current architecture, target architecture, and
     call-site inventory match repo reality.
   - Find unnamed owner paths, callers, generated artifacts, tests, docs,
     prompts, or config that the plan should account for.

7. `canonical-owner-and-ssot`
   - Ask whether the plan extends the correct central path.
   - Find duplicate truth, parallel implementations, shadow contracts,
     alternate writers/readers, or wrong-layer logic.

8. `existing-pattern-and-convergence`
   - Find every existing repo pattern similar to the proposed architecture.
   - Decide which pattern is canonical, which patterns are debt, and which
     related code should migrate, delete, stay different, or become a named
     follow-up.
   - Block new patterns that are not justified against existing conventions.

9. `caller-invariant-state`
   - Review the proposed API or boundary from the caller's side.
   - Check misuse resistance, invariant ownership, state-model simplicity,
     partial-update risks, and whether callers must know internals.

10. `drift-proof-coupling`
   - Inspect shared dependencies, schemas, generated artifacts, adapters,
     fixtures, prompts, tests, and contract families for drift risk.
   - Check whether dependent pieces share one source of truth or can silently
     diverge.

11. `elegance-and-code-judo`
   - Search for a simpler architecture that deletes concepts.
   - Challenge bloated abstractions, wrappers, conditionals, compatibility
     layers, overbroad scaffolding, and unnecessary tools.
   - Track concept count: what is added, deleted, merged, made private, or left
     exposed.

12. `deletion-and-side-door`
   - Search for legacy paths, stale flags, direct mutation paths, old commands,
     bad defaults, docs, examples, comments, prompts, tests, or fixtures that
     would keep the old behavior discoverable or callable.

13. `proof-and-phase-exit`
   - Check whether the plan's phases, checklists, exit criteria, rollback, and
     verification actually prove the architecture and behavior-preservation
     claims without bureaucracy.
   - Prefer behavior-level integration proof when the risk crosses modules or
     runtime boundaries. Reject tests that only prove the compiler, framework,
     or mock setup works.

Conditional lenses:

- `agent-capability`
  - Required when the plan changes prompts, agents, skills, LLM workflows, MCP,
    or model-facing behavior. Checks prompt-first and native-capability-first
    options before custom tooling.
- `docs-contract-drift`
  - Required when the plan changes public commands, APIs, docs, prompts,
    user-facing contracts, telemetry names, stable IDs, or install behavior.
- `security-boundary`
  - Required when the plan touches auth, permissions, secrets, command
    execution, input validation, privacy, filesystem, process, or network
    boundaries.

Every child must be told:

```text
Read repo truth directly. This is read-only. Do not edit files. Do not invent
scope. Return only findings your lens owns, with file/symbol/line evidence and
the concrete plan repair needed. If the plan is clean for your lens, say so
plainly. Do not produce a second plan.
```

If the child runtime supports native parallelism, include:

```text
Maximize parallelism by using parallel agents. Do not invoke skills that spawn
subagents.
```

### 6.4 Parent Synthesis

The parent must not concatenate child results. It must read repo evidence,
dedupe, validate, and classify findings.

For each child finding:

- spot-check the cited file or plan section
- decide whether the finding is blocking, non-blocking, wrong, or out of scope
- merge duplicates across lenses
- preserve disagreements when the right architecture is genuinely unresolved
- cite direct plan/code evidence in the final output

The parent may add findings the children missed.

The final verdict should not be softer than the evidence. A plan that lacks a
clear North Star, lacks explicit done-state requirements, leaves real
outcome-changing ambiguity, leaves side doors, duplicate truth, unresolved
architecture choices, breadth-first implementation risk, or fake proof is not
ready.

### 6.5 Progressive Audit Order

`plan-review` should audit in a fixed order so it does not jump straight to
taste comments or local code smells before proving the plan's target and code
truth.

The ordered audit is:

1. Resolve artifacts.
   - Resolve `PLAN_PATH`.
   - Resolve `AUDIT_LOG_PATH`, defaulting to
     `<PLAN_STEM>_PLAN_REVIEW_AUDIT.md` beside the plan.
   - Read local instructions and repo verification rules.
   - If the audit log exists, read it before starting. If it does not exist,
     create it before final output.

2. Read the plan as written.
   - Identify scope, requested behavior, stop boundary, phase boundaries, and
     claimed verification.
   - Do not repair the plan mentally. Audit the plan on disk.

3. Extract the outcome contract.
   - Find the North Star.
   - Find explicit done-state requirements.
   - Find requirements, non-requirements, constraints, non-constraints,
     assumptions, and complexity sources.
   - Mark missing outcome contract pieces before judging detailed
     architecture.

4. Identify real ambiguity.
   - Name wording that can produce different outcomes.
   - Check whether repo truth resolves it.
   - Keep only ambiguity that changes requirements, constraints,
     compatibility, deletion, proof, or phase order.
   - Mark each unresolved ambiguity or constraint question as requiring
     reconciliation before the plan can be ready.

5. Build the relevant-code map.
   - List every named file, symbol, module, command, route, prompt, generated
     artifact, fixture, schema, config, test surface, and doc/instruction
     surface the plan depends on.
   - Search for old and new concepts.
   - Search for comparable existing patterns.
   - Search for side doors and alternate entrypoints.
   - Split broad code reading across parallel read-only agents when useful.

6. Read all relevant code.
   - Read the canonical owner path.
   - Read representative and public callers.
   - Read legacy paths that should delete or converge.
   - Read comparable pattern families.
   - Read contract surfaces that can drift.
   - Read tests and proof surfaces.
   - Read touched docs, prompts, examples, and instructions that can route
     humans or agents to the wrong path.
   - Record every code area read in the audit log coverage ledger.

7. Synthesize code truth.
   - Write down current architecture anchors.
   - Write down target architecture claims.
   - Identify where the plan matches code, where it is stale, and where the
     plan is guessing.
   - Do not move to approval while relevant-code coverage is unknown.

8. Run required lenses in order.
   - Outcome North Star.
   - Ambiguity and miscommunication.
   - Requirements, constraints, and simplicity pressure.
   - Tiny-team maintainability.
   - Depth-first implementation risk.
   - Code-truth map.
   - Canonical owner and SSOT.
   - Existing pattern and convergence.
   - Caller, invariant, and state model.
   - Drift-proof coupling.
   - Elegance and code-judo.
   - Deletion and side-door closure.
   - Proof and phase exit.
   - Conditional lenses for agent capability, docs/contract drift, and security
     boundary when triggered.

9. Challenge the architecture.
   - Ask whether this can be simpler without breaking stated requirements.
   - Ask whether the same outcome can be achieved with fewer live concepts.
   - Ask whether an existing pattern should be extended or made canonical.
   - Ask what can be deleted, privatized, merged, or made unreachable.

10. Verify phase risk.
    - Confirm Phase 1 proves a real narrow integrated path.
    - Confirm each later phase widens from a proven base.
    - Confirm proof gates are integration-level where integration is the risk.
    - Block plans that build broad scaffolding and only integrate at the end.

11. Classify findings.
    - Blocking: plan is unsafe, ambiguous, under-read, overbuilt, not
      convergent, not provable, or not ready to implement.
    - Non-blocking: improvement that does not change implementation safety,
      architecture, proof, drift, or completion.
    - Wrong or out of scope: rejected with a short reason in the audit log.

12. Update the audit log.
    - Add a new pass entry.
    - Update current verdict.
    - Check off resolved findings only when the plan or repo evidence proves
      they are resolved.
    - Check off ambiguity or constraint decisions only when the decision was
      made by the user or an authorized agent and carried through into the
      plan.
    - Add new findings with stable IDs.
    - Update relevant-code coverage.
    - Carry unresolved findings forward.

13. Return the verdict.
    - Report the audit log path.
    - Lead with blocking findings.
    - Name the smallest next plan repair.
    - Do not call the plan ready until the proper-audit checklist is complete
      and all blocking findings are resolved.

### 6.6 Audit Log Contract

Every non-trivial `plan-review` run should maintain an audit log beside the
plan. Default path:

```text
<PLAN_STEM>_PLAN_REVIEW_AUDIT.md
```

For example:

```text
docs/PAYMENTS_MIGRATION_PLAN.md
docs/PAYMENTS_MIGRATION_PLAN_REVIEW_AUDIT.md
```

The audit log is not a second plan. It is the durable review ledger used across
the loop while the plan is refined. The plan remains the artifact under review.

The audit log should contain:

```markdown
# Plan Review Audit Log

Plan: <path>
Audit log: <path>
Current verdict: ready | not-ready | blocked-on-decision | inconclusive
Last reviewed: <date/time>
Scope: <whole plan | phase | section>

## Current Blocking Findings

- [ ] PRV-001 - <title>
  - Lens:
  - Evidence:
  - Required plan repair:
  - Status: open | resolved | accepted-risk | out-of-scope | wrong
  - Resolution evidence:

## Current Non-Blocking Findings

<same shape, shorter>

## Relevant Code Coverage Ledger

| Area | Files/symbols read | Why relevant | Reader | Status |
| --- | --- | --- | --- | --- |
| Canonical owner path |  |  |  | read/unknown |
| Caller families |  |  |  | read/unknown |
| Legacy and side-door paths |  |  |  | read/unknown |
| Comparable patterns |  |  |  | read/unknown |
| Contract/proof surfaces |  |  |  | read/unknown |

## Required Lens Checklist

- [ ] Outcome North Star
- [ ] Ambiguity and miscommunication
- [ ] Requirements, constraints, and simplicity
- [ ] Tiny-team maintainability
- [ ] Depth-first implementation risk
- [ ] Code-truth map
- [ ] Canonical owner and SSOT
- [ ] Existing pattern and convergence
- [ ] Caller, invariant, and state model
- [ ] Drift-proof coupling
- [ ] Elegance and code-judo
- [ ] Deletion and side-door closure
- [ ] Proof and phase exit
- [ ] Conditional lenses, if triggered

## Ambiguity And Decision Ledger

| ID | Ambiguity/constraint question | Interpretations | Impact | Required decision | Decision owner | Plan carry-through evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Pass History

### Pass <n> - <date/time>

- Scope:
- Agents/lenses run:
- Code areas read:
- Findings added:
- Findings resolved:
- Findings carried forward:
- Verdict:
- Next audit focus:
```

Audit log rules:

- Read the latest audit log before every repeat audit.
- Keep stable finding IDs so plan repairs can be checked off instead of
  rediscovered.
- Check off an item only when the plan changed or repo evidence proves the
  finding no longer applies.
- Check off an ambiguity or constraint decision only when a real decision owner
  resolved it and the plan now carries that decision through every affected
  section.
- Do not erase old findings. Mark them resolved, wrong, out of scope, or
  accepted-risk with evidence.
- Do not let the audit log become a second implementation checklist. It tracks
  review evidence and plan-readiness state.
- Keep child transcripts out of the main log unless they are short. Link or
  summarize child artifacts.
- If a repeat audit finds the same issue again, keep the original ID and add
  new evidence rather than creating a duplicate.
- If the plan changes scope, add a pass entry explaining whether old findings
  still apply.

### 6.7 Proper-Audit Checklist

A `plan-review` run has not audited the plan properly unless all applicable
items below are true.

Artifact setup:

- [ ] The plan path is resolved.
- [ ] The audit log path is resolved or created beside the plan.
- [ ] Existing audit log entries were read before the new pass.
- [ ] Local instructions and repo verification rules were read.
- [ ] The reviewed scope is explicit.
- [ ] The output names what was not checked, if anything.

Outcome contract:

- [ ] The North Star outcome is identified or marked missing.
- [ ] Done-state requirements are identified or marked missing.
- [ ] Requirements are separated from tasks.
- [ ] Non-requirements are identified or marked missing.
- [ ] Hard constraints are identified and evidence-checked.
- [ ] Non-constraints are identified where they remove fake complexity.
- [ ] Assumptions and beliefs creating complexity are named.
- [ ] Code-quality requirements around complexity, abstraction, deletion,
  centralization, drift-proofing, and proof are checked.

Ambiguity:

- [ ] Real outcome-changing ambiguity is listed.
- [ ] Plausible interpretations are named.
- [ ] Architecture impact is explained.
- [ ] Repo truth was checked before asking the user.
- [ ] Fake ambiguity was ignored.
- [ ] Required decisions are stated in the smallest possible set.

Relevant-code coverage:

- [ ] Every file and symbol named by the plan was read.
- [ ] The current canonical owner path was read.
- [ ] The proposed target owner path was read.
- [ ] Public caller families were read.
- [ ] Representative internal call sites were read.
- [ ] Legacy paths, old APIs, fallbacks, flags, scripts, commands, jobs, UI
  affordances, prompts, or generated artifacts that can preserve old behavior
  were searched and read when found.
- [ ] Comparable existing patterns were searched and read.
- [ ] Persistence, schema, config, fixture, adapter, and generated contract
  surfaces were read when relevant.
- [ ] Existing tests, integration tests, manual proof surfaces, and low-value
  test risks were read.
- [ ] Touched docs, examples, comments, prompts, and instructions were read
  when they can affect behavior or future routing.
- [ ] Unknown relevant-code areas are named explicitly; the review does not
  approve while relevant coverage is unknown.

Parallel read quality:

- [ ] Parallel agents were considered for broad code reading.
- [ ] Parallel agents, when used, had non-overlapping read-only scopes.
- [ ] Child reports included exact files, symbols, and evidence.
- [ ] Parent synthesis spot-checked child evidence before trusting findings.
- [ ] Child output did not become the verdict by itself.

Architecture quality:

- [ ] The canonical owner path is named.
- [ ] Duplicate truth and parallel implementation paths are identified.
- [ ] Existing patterns are inventoried before approving a new one.
- [ ] Related code is classified as move now, delete now, leave different,
  named follow-up, or user decision.
- [ ] Caller API shape is checked for misuse resistance.
- [ ] Invariants are named and located in code or target code shape.
- [ ] State model and partial-state risks are checked.
- [ ] Drift-proof coupling is checked across shared dependencies.
- [ ] Abstractions are checked for real complexity reduction.
- [ ] Layer boundaries and refactor radius are checked.
- [ ] Live concept count is checked.
- [ ] Legacy paths and side doors are checked for deletion or closure.

Implementation-risk quality:

- [ ] The phase plan is depth-first or has a real reason it cannot be.
- [ ] Phase 1 proves a narrow integrated path.
- [ ] The highest-risk seam is crossed early.
- [ ] Each phase has a proof gate before widening.
- [ ] Bells, optional modes, and polish are deferred until the core path works.
- [ ] Integration proof is required where integration is the real risk.
- [ ] Low-value unit-only or mock-only proof is rejected where it would miss
  actual bugs.

Finding quality:

- [ ] Every blocking finding includes consequence, evidence, and required plan
  repair.
- [ ] Evidence cites plan and code anchors where possible.
- [ ] Findings are deduped across lenses.
- [ ] Non-blocking findings are clearly separated from blockers.
- [ ] Wrong, resolved, accepted-risk, or out-of-scope findings are labeled with
  a reason.
- [ ] The final verdict is not softer than the worst unresolved blocker.

Loop readiness:

- [ ] The audit log current checklist was updated.
- [ ] Stable finding IDs were used.
- [ ] Resolved findings were checked off only with evidence.
- [ ] Unresolved findings were carried forward.
- [ ] Relevant-code coverage was updated.
- [ ] The next audit focus is named.
- [ ] The final response points to the audit log path.

Reconciliation gate:

- [ ] Every real ambiguity question has a decision owner.
- [ ] Every real constraint or non-constraint question has a decision owner.
- [ ] User-owned decisions were answered by the user.
- [ ] Agent-owned decisions were made only when the agent had explicit
  permission and enough repo evidence.
- [ ] Each resolved decision is written back into the plan.
- [ ] The plan carry-through was checked across requirements, constraints,
  target architecture, phase order, delete list, compatibility posture, and
  proof strategy.
- [ ] No ambiguity or constraint item is marked resolved solely because it was
  discussed in chat or listed in the audit log.
- [ ] The plan is not marked ready while any outcome-changing decision remains
  open or uncaptured in the plan.

### 6.8 Post-Audit Reconciliation Gate

After an audit, the plan can move toward `ready` only through reconciliation.
The loop is:

1. Audit finds ambiguity, constraint confusion, non-constraint confusion, or a
   decision gap.
2. The audit log records the question, plausible interpretations, impact,
   required decision, and decision owner.
3. The user or an explicitly authorized agent resolves the question.
4. The plan is edited so the decision is carried through every affected
   section.
5. The next audit rereads the plan and audit log, verifies the carry-through,
   and only then marks the item resolved.

This gate matters because a resolved chat question that never reaches the plan
still lets implementers build the wrong thing later. The artifact of truth is
the plan on disk, not memory and not the audit log.

The reviewer should block readiness when:

- the decision owner is unclear
- the user has not answered a user-owned decision
- an agent made a decision without explicit permission
- the plan was not updated after the decision
- the plan updated one section but left contradictory old wording elsewhere
- the phase plan, delete list, compatibility posture, or proof strategy did
  not change even though the decision requires it

## 7. Blocking Finding Standards

Findings are blocking when they mean the plan is not safe or elegant enough to
implement yet.

Presumptive blockers:

- The plan does not state a North Star outcome before task detail.
- The plan lacks explicit done-state requirements: concrete truths that will
  hold when the plan is complete.
- The plan's requirements are task-shaped instead of truth-shaped, so the
  checklist can complete while the desired outcome remains false.
- The plan's architecture requirements do not name complexity, abstraction,
  deletion, centralization, drift-proofing, or proof outcomes where those are
  core to the work.
- Two reasonable implementers could read the plan and build meaningfully
  different outcomes because a requirement, constraint, compatibility posture,
  delete obligation, proof bar, or phase sequence is ambiguous.
- The plan has real outcome-changing ambiguity that repo truth does not
  resolve and the plan has not made a definitive decision.
- A real ambiguity, constraint, or non-constraint question has been identified
  but no decision owner is named.
- A user-owned ambiguity or constraint question has not been answered by the
  user.
- An agent-owned ambiguity or constraint decision was made without explicit
  permission or enough repo evidence.
- A resolved ambiguity or constraint decision was not written back into the
  plan.
- A resolved decision was written into one plan section but not carried through
  affected requirements, constraints, target architecture, phase order, delete
  list, compatibility posture, or proof strategy.
- The plan asks the user fake questions or treats obvious repo-discoverable
  facts as ambiguity instead of reading the code and local instructions.
- The review has not read all relevant code needed to validate the plan's
  claims.
- Relevant code coverage is unknown, vague, or based on implementer summaries
  instead of direct file/symbol reads.
- The review did not create or update the plan review audit log for a
  non-trivial audit.
- The audit log does not carry unresolved prior findings forward.
- A repeat audit marks findings resolved without plan changes or repo evidence.
- The plan does not state requirements, non-requirements, hard constraints,
  non-constraints, assumptions, and complexity sources before architecture
  decisions depend on them.
- The plan treats an assumed constraint as real without evidence, and that
  belief makes the architecture more complex.
- The plan cannot explain which requirement or constraint justifies a major
  piece of complexity.
- The plan has not repeatedly pressure-tested whether the architecture can be
  simpler without breaking stated requirements.
- The plan designs for a large platform team instead of a tiny team that needs
  self-documenting, direct, easy-to-debug code.
- The plan builds custom infrastructure, parsers, runners, frameworks, plugin
  systems, or config surfaces where a proven library, existing repo pattern, or
  simpler direct implementation would do.
- The phase plan is breadth-first: it builds many layers, variants, helpers,
  or workstreams before proving one narrow integrated path.
- The first phase does not cross the highest-risk integration seam.
- The first phase builds foundation or scaffolding but cannot show the desired
  behavior working in a real runtime, simulator, command path, integration
  test, or closest honest environment.
- Later phases widen the implementation before the previous phase has passed
  meaningful integration proof.
- The plan treats unit tests, mocks, typecheck, or "works in theory" as enough
  proof when the actual risk is whether integrated pieces produce the desired
  behavior.
- Bells, variants, optional modes, or polish are scheduled before the core
  abstraction and owner path have been proven end-to-end.
- The canonical owner path is missing, wrong, or bypassed.
- The plan did not audit similar existing repo patterns before proposing a new
  pattern, service, abstraction, state model, API, event flow, adapter, or
  command path.
- The plan proposes a new pattern without proving existing patterns are wrong,
  insufficient, or debt that should not be copied.
- The plan copies a local anti-pattern without naming why that precedent is
  safe to use.
- The plan creates a new good path but leaves related old paths live.
- The plan fails to identify which nearby code should converge onto the chosen
  pattern now, which code should be deleted, and which code is intentionally
  different.
- The plan creates or preserves a parallel implementation path.
- Old and new writers/readers remain live without an approved bridge.
- Legacy path deletion is missing, vague, or postponed to "cleanup later."
- A side door remains discoverable or callable.
- The plan's target architecture adds special-case conditionals where a better
  state model or owner boundary should delete them.
- A new abstraction is a thin wrapper, identity pass-through, or framework
  without real complexity reduction.
- The proposed API makes callers understand internal lifecycle, state, flags,
  modes, or cleanup rules that should belong behind the owner boundary.
- The plan does not say where key invariants live in code, types, API shape, or
  runtime routing.
- The plan adds state flags, nullable fields, or modes that allow impossible or
  half-migrated states when a simpler typed model or state machine could remove
  branches.
- The plan leaves common developer misuse possible through public APIs,
  exports, commands, fixtures, or examples.
- Shared dependencies, generated artifacts, schemas, fixtures, tests, prompts,
  adapters, or contract-family surfaces can drift because they are not tied to
  one source of truth or fail-loud boundary.
- The plan makes the repo's live concept count go up without deleting,
  merging, privatizing, or making obsolete concepts unreachable.
- The plan relies on silent fallback, compatibility shim, stale cache, old API
  retry, or dev-only bypass without explicit approval and removal plan.
- Behavior preservation for a refactor or migration is not provable.
- The proof strategy rewards shallow unit tests over the integration behavior
  that can actually break.
- Tests mostly prove the compiler, framework, mocks, or implementation details
  instead of user-visible behavior, cross-module behavior, persistence, command
  routing, generated contracts, or runtime boundaries.
- Phases can be marked complete while required work remains outside checklist
  or exit criteria.
- The call-site audit says "all usages" without concrete call-site families,
  counts, or representative anchors.
- The plan changes instruction-bearing content while silently summarizing away
  operational structure.
- Agent-backed plans jump to wrappers, parsers, OCR, fuzzy retrieval, or
  harnesses before proving prompt, grounding, tool, context, or native model
  capability is insufficient.
- Touched live docs, comments, examples, prompts, or instructions would become
  stale and the plan does not update or delete them.
- The plan depends on repo-policing tests or doc-audit scripts instead of real
  runtime boundaries.
- A real user/product/architecture decision remains branchy in the plan.

Non-blocking findings:

- Local naming or prose could be clearer but does not affect implementation
  correctness, architecture, proof, or drift.
- A possible future cleanup is real but not part of the requested behavior,
  convergence scope, or adjacent surfaces.
- A broader redesign might be nice but would add product scope or delay without
  reducing current bug vectors.

## 8. Output Contract

The final review should be findings-first and sparse enough to act on. For
non-trivial audits, it should also create or update the audit log beside the
plan before returning the verdict.

Recommended shape:

```markdown
# Plan Review Verdict

VERDICT: ready | not-ready | blocked-on-decision | inconclusive
Confidence: high | medium | low
Scope reviewed: <whole plan | phase | section>
Plan: <path>
Audit log: <path>

## Blocking Findings

1. <finding title>
   - Problem:
   - Why it matters:
   - Evidence:
     - <plan path:line or heading>
     - <code path:line or symbol>
   - Required plan repair:
   - Review lens:

## Non-Blocking Findings

<same shape, shorter>

## Stronger Architecture Move

<when applicable: the simpler/elegant reframing, with evidence and tradeoff>

## North Star And Done-State Requirements

- North Star outcome:
- Done-state truths:
- User-facing or outcome-facing requirements:
- Code-quality requirements:
- Task-shaped requirements to rewrite:
- Outcome that remains unproven:

## Requirements, Constraints, And Simplicity Pressure

- Requirements driving architecture:
- Non-requirements:
- Hard constraints:
- Non-constraints:
- Assumptions or beliefs creating complexity:
- Complexity that earns its keep:
- Complexity to remove:
- Simpler viable architecture:

## Real Ambiguity And Required Decisions

- Ambiguous outcome, requirement, or constraint:
- Plausible interpretations:
- Architecture impact:
- Repo truth that resolves it:
- Decision owner:
- Required decision:
- Plan carry-through required:
- Plan carry-through evidence:
- Fake ambiguity ignored:

## Depth-First Implementation Risk

- First integrated slice:
- Highest-risk seam:
- Proof required before widening:
- Breadth-first scaffolding risks:
- Widening sequence:
- Complexity deferred until core proof:

## Tiny-Team Maintainability

- Self-documenting code risks:
- Custom infrastructure to avoid:
- Proven libraries or existing repo patterns to use:
- Debugging path:
- Ongoing maintenance burden:

## Existing Pattern And Convergence Audit

- Similar patterns found:
- Canonical pattern to extend:
- Anti-patterns not to copy:
- Move now:
- Delete now:
- Leave different:
- Named follow-up:
- User decision:

## Caller, Invariant, And State-Model Risks

- Caller misuse risk:
- Invariants and where they live:
- Impossible or partial states:
- Atomicity risks:
- Layer-boundary leaks:
- Drift-proof coupling risks:
- Concept count impact:

## Deletion And Side-Door Checklist

- Delete now:
- Close or migrate:
- Explicitly out of scope:
- Needs user decision:

## Proof And Phase-Exit Gaps

- Integration proof needed:
- Low-value tests to avoid:
- Behavior-preservation proof:
- Phase-exit gap:

## Coverage Notes

- Code areas read:
- Relevant code not yet read:
- Lenses run:
- Lenses not run:
- Audit log updated:
- Proper-audit checklist status:
- What was not checked:

## Recommended Next Move

<one exact next action>
```

Rules:

- Do not include placeholder sections with filler.
- Do not invent findings because the skill was invoked.
- Do not approve if a required lens could not inspect its scope.
- Do not approve if all relevant code has not been read or explicitly ruled
  irrelevant.
- Do not approve if the audit log is missing, stale, or not updated for the
  current pass.
- Do not use `optional`, `nice-to-have`, or `deferred` to soften
  ship-blocking convergence work.
- Do not paste long child transcripts. Link or name their artifact paths when
  they exist.

## 9. Planned Skill Package Shape

Target package:

```text
skills/plan-review/
  SKILL.md
  agents/
    openai.yaml
  references/
    architecture-quality-canon.md
    review-lenses.md
    progressive-audit-order.md
    audit-log-contract.md
    proper-audit-checklist.md
    child-prompt-contract.md
    output-contract.md
    examples.md
```

### `SKILL.md`

Owns:

- trigger and peer boundary
- read-only posture
- first move
- parent workflow
- when to use parallel agents
- synthesis rules
- audit log expectations
- output expectations
- reference map

It should stay lean. It should not copy the entire quality canon into the
entrypoint.

### `references/architecture-quality-canon.md`

Owns the strict architecture opinions:

- code truth first
- tiny-team architecture fit
- North Star outcome before task detail
- explicit done-state requirements
- outcome-facing and code-quality requirements
- requirements and non-requirements up front
- constraints and non-constraints up front
- real ambiguity and miscommunication risk
- post-audit reconciliation gate
- decision-owner and plan carry-through requirements
- complexity-source accounting
- repeated simplicity pressure
- depth-first phase sequencing
- first integrated slice through the highest-risk seam
- proven-before-widening implementation gates
- existing pattern inventory
- convergence onto the best local pattern
- canonical owner path
- SSOT
- caller-side simplicity and misuse resistance
- drift-proof shared dependencies
- invariant ownership
- state-model simplicity
- abstraction earning tests
- layer boundaries and refactor radius
- concept count reduction
- delete legacy paths
- side-door closure
- hard cutover and fail-loud boundaries
- no unauthorized shims
- code-judo simplification
- no thin abstractions
- real boundaries over repo-policing heuristics
- integration-first meaningful proof

### `references/review-lenses.md`

Owns:

- required and conditional lenses
- what each lens must inspect
- what each lens must ignore
- how to avoid overlap
- outcome North Star and done-state requirement review behavior
- ambiguity and miscommunication risk review behavior
- existing-pattern and convergence-sweep review behavior
- caller/invariant/state-model review behavior
- tiny-team maintainability review behavior
- depth-first implementation risk review behavior
- drift-proof coupling review behavior
- integration-first proof review behavior
- how parent synthesis should treat lens disagreement

### `references/progressive-audit-order.md`

Owns:

- the ordered audit pass
- when to read the audit log
- when to launch parallel code-reading agents
- how to move from plan reading to code truth to lenses to verdict
- how to avoid approving before relevant-code coverage is complete

### `references/audit-log-contract.md`

Owns:

- sidecar path convention
- audit log template
- stable finding IDs
- pass history
- relevant-code coverage ledger
- finding status rules
- loop behavior for repeat audits

### `references/proper-audit-checklist.md`

Owns:

- the exhaustive "was this plan audited properly?" checklist
- required artifact setup checks
- outcome, ambiguity, code coverage, parallel-read, architecture, proof,
  finding-quality, loop-readiness, and reconciliation-gate checks
- checklist status language for final output

### `references/child-prompt-contract.md`

Owns reusable prompt skeletons for:

- read-only child reviewer
- read-only code-coverage mapper
- specific lens prompts
- severe elegance/adversarial simplification prompt
- child output footer

These prompts should be designed for `fresh-consult` or read-only
`agent-delegate`, not for a new runner.

### `references/output-contract.md`

Owns:

- verdict vocabulary
- finding shape
- coverage notes
- malformed child output handling
- what `ready`, `not-ready`, `blocked-on-decision`, and `inconclusive` mean

### `references/examples.md`

Owns:

- one strong example of a blocking architecture finding
- one strong example of a side-door deletion finding
- one example where the plan is clean
- one anti-example of over-reviewing or inventing scope

Examples must teach judgment, not become a lookup table.

## 10. Draft Trigger Metadata

Candidate frontmatter:

```yaml
---
name: plan-review
description: "Run a severe audit-log-backed planning-stage architecture review of an existing plan document against all relevant repo code. Use when the user wants a plan, phase plan, migration plan, or design doc audited before implementation for North Star outcome clarity, explicit done-state requirements, real ambiguity, stated requirements/constraints, tiny-team simplicity, depth-first phase risk, elegance, canonical owner paths, existing-pattern convergence, drift-proof dependencies, duplicate truth, side doors, required deletes, integration-proof gaps, overbuild, and bug-vector reduction, optionally with parallel read-only agents. Not for creating the plan, implementing a phase, or reviewing an already-written code diff."
metadata:
  short-description: "Hardcore architecture review for existing plans"
---
```

This description is under the standard 1024-character runtime cap and names the
nearest wrong lanes.

## 11. Example Skill Invocation Behavior

User:

```text
Use plan-review on docs/PAYMENTS_MIGRATION_PLAN.md. I want the most elegant
possible architecture, not a rubber stamp.
```

Expected behavior:

1. Resolve `PLAN_PATH`.
2. Resolve or create
   `docs/PAYMENTS_MIGRATION_PLAN_REVIEW_AUDIT.md`.
3. Read local instructions.
4. Read the plan and any existing audit log.
5. Confirm the plan states the North Star outcome and explicit done-state
   truths before accepting its tasks.
6. Find any real ambiguity where two implementers could build different
   payment outcomes, especially around compatibility, old writer deletion,
   and proof.
   Name the decision owner and require the resolved answer to be carried back
   into the plan before the item can be checked off.
7. Confirm the plan states requirements, non-requirements, constraints,
   non-constraints, assumptions, and complexity sources before accepting its
   architecture.
8. Check whether the phase plan is depth-first: Phase 1 should prove one
   narrow payment path through the highest-risk integration seam before the
   plan widens.
9. Search the repo for named old/new concepts, owner modules, comparable
   existing patterns, call sites, caller API shapes, invariants, state models,
   shared dependency drift risks, tests, docs, prompts, examples, generated
   artifacts, and old side doors.
10. Launch parallel read-only code-reading and lens agents if subprocess
   skills are available and the relevant payment surface is large enough.
11. Synthesize findings and update the audit log coverage ledger, finding
   statuses, and pass history.
12. Return `VERDICT: not-ready` if the plan lacks an explicit payment outcome,
   has task-shaped requirements, leaves ambiguous compatibility behavior,
   duplicate payment writers, unjustified constraints, unjustified new service
   patterns, compatibility fallback, breadth-first scaffolding, caller-side
   misuse risk, drift-prone contracts, low-value test proof, old docs, or proof
   gaps.
13. Recommend the exact plan repair: state the payment North Star and done-state
   truths, resolve compatibility ambiguity, make Phase 1 prove a narrow payment
   write through the existing canonical service to persistence, then widen to
   other callers; migrate any same-family direct writers that must converge now,
   delete the old direct writer after migration, update examples, and add
   integration-level behavior-preservation proof at the service boundary. Do
   not mark the compatibility decision resolved until the plan carries that
   decision through requirements, architecture, phase order, delete list, and
   proof.

## 12. Implementation Plan For The Skill

### Phase 1 - Prompt-First Package

Goal: ship the lean v1 skill package.

Work:

- Add `skills/plan-review/SKILL.md`.
- Add the eight references listed in Section 9.
- Add `skills/plan-review/agents/openai.yaml` with concise runtime metadata.
- Add `plan-review` to the local install matrices in `Makefile`:
  `SKILLS`, `CLAUDE_SKILLS`, and `GEMINI_SKILLS`.
- Update `README.md` skill inventory.
- Update `AGENTS.md` skill routing:
  - use `$plan-review` when the user wants a severe pre-implementation plan
    audit against code truth, with parallel reviewers when useful.
- Do not add scripts in Phase 1.

Verification:

- Run `npx skills check`.
- Re-read new docs and skill package files.
- Use `rg` to confirm `plan-review` is named consistently in `README.md`,
  `AGENTS.md`, `Makefile`, and package paths.
- Use `rg` to confirm audit log path language and proper-audit checklist
  language are consistent across the package.

Done bar:

- The package is self-contained.
- Trigger boundary is clear next to `arch-step`, `code-review`,
  `fresh-consult`, `agent-delegate`, `model-consensus`, `plan-swarm`, and
  `thermo-nuclear-code-quality-review`.
- The skill preserves agent judgment and does not become a checklist runner.

### Phase 2 - Representative Dry Run

Goal: validate the skill on one existing plan without editing code.

Work:

- Pick one real plan doc in `docs/`.
- Run the skill manually against it.
- Confirm it reads repo truth before findings.
- Confirm it creates or updates `<PLAN_STEM>_PLAN_REVIEW_AUDIT.md` beside the
  plan.
- Confirm it tracks relevant-code coverage and carries unresolved findings
  forward across a repeat audit.
- Confirm ambiguity and constraint questions cannot be marked resolved until a
  decision owner resolves them and the plan carries the decision through.
- Confirm it flags breadth-first plans that defer end-to-end proof until late.
- Confirm it can produce zero findings when the plan is clean, and strong
  findings when the plan has real architecture gaps.
- Adjust prompt wording only where execution quality fails.

Verification:

- Compare findings against cited code anchors.
- Confirm it does not generate a second plan.
- Confirm it does not ask silly questions that repo reading can answer.

### Phase 3 - Optional Mechanics Only If Needed

Goal: add narrow helpers only if repeated manual runs prove prompt-only V1 is
too fragile.

Allowed helpers:

- blank review artifact template
- Markdown heading extractor
- child-output normalizer

Forbidden helpers:

- deterministic reviewer scorer
- architecture rule engine
- runner/controller/state machine
- grep-based absence gate treated as proof
- script that decides whether a plan is elegant

Verification:

- Helper stdout must be compact and agent-readable.
- `npx skills check`.
- Manual dry run still shows parent-agent judgment owns the verdict.

## 13. Risks And Anti-Patterns

Avoid these while building `plan-review`:

- Turning "elegance" into generic taste comments.
- Making the skill a duplicate of `code-review` before implementation exists.
- Letting child agents invent product scope.
- Treating every possible improvement as a blocker.
- Creating a second plan instead of findings and plan repairs.
- Writing a giant checklist that replaces human architecture judgment.
- Letting a plan begin as tasks without first stating the North Star outcome.
- Accepting vague task-shaped requirements when the plan needs explicit
  done-state truths.
- Missing real ambiguity where two implementers could build different
  outcomes.
- Creating noisy fake ambiguity lists instead of reading the repo and naming
  only decisions that change implementation.
- Treating ambiguity or constraint answers in chat as enough when the plan
  itself was not updated.
- Letting an unauthorized agent silently decide a user-owned ambiguity or
  constraint.
- Marking a decision resolved without checking carry-through across the plan.
- Approving a plan without reading all relevant code.
- Treating a few grep hits as a relevant-code audit.
- Running parallel agents as theater instead of giving them concrete
  non-overlapping code-reading scopes.
- Starting each repeat audit from scratch instead of reading and extending the
  existing audit log.
- Letting the audit log become a second plan instead of a review evidence
  ledger.
- Reviewing architecture before the plan states requirements, non-requirements,
  constraints, non-constraints, assumptions, and complexity sources.
- Accepting complexity caused by imagined constraints.
- Designing for a large staff instead of a tiny team that needs the simplest
  self-documenting code that can satisfy the requirements.
- Building custom infrastructure where a proven library, existing repo pattern,
  or direct implementation would be safer.
- Accepting breadth-first phase plans that defer integration proof to the end.
- Letting parallel work build disconnected layers before the core path works.
- Adding variants, optional modes, polish, or extra tooling before the base
  path is proven in the real runtime or closest honest integration
  environment.
- Accepting a new abstraction before the plan inventories existing repo
  patterns.
- Letting "follow the repo convention" mean copying a local anti-pattern.
- Approving a locally good pattern while related old patterns stay live and
  unclassified.
- Ignoring caller-side API shape, invariants, state modeling, atomicity, or
  common misuse paths.
- Ignoring shared dependency drift between coupled components, schemas,
  generated artifacts, adapters, fixtures, prompts, or tests.
- Adding concepts faster than the plan deletes, merges, privatizes, or makes
  obsolete concepts unreachable.
- Rewarding lots of shallow unit tests when integration tests would catch the
  actual bugs.
- Letting tests lock implementation details instead of behavior.
- Using deletion-proof tests or stale-term greps as substitutes for real
  side-door closure.
- Asking the user to answer questions the code already answers.
- Making "parallel agents" mandatory for tiny plans where one focused read is
  clearer.
- Letting `fresh-consult` or child model output become authority without parent
  evidence checks.
- Letting the skill soften hard cleanup into archive, retire, comment out, or
  "document as legacy."

## 14. Definition Of Done For This Planning Doc

This planning document is good enough to build from when:

- it names the repeated user problem and anti-cases
- it states up front that the future skill is doctrine-only and must not become
  a deterministic harness, runner, controller, scorer, or checklist executor
- it captures the repo's existing code-quality opinions
- it defines the plan-review lane relative to peer skills
- it specifies the strict architecture quality bar
- it requires a North Star outcome and explicit done-state truths before task
  detail
- it requires real ambiguity around outcomes, constraints, compatibility,
  deletes, proof, and phase order to be resolved before implementation
- it requires ambiguity and constraint questions to have decision owners, be
  reconciled by the user or an authorized agent, and then be carried through
  the plan before they can be marked resolved
- it tells the skill to ignore fake ambiguity and answer repo-discoverable
  questions by reading the repo
- it defines the progressive audit order from artifact resolution through code
  truth, lenses, synthesis, audit log update, and verdict
- it requires all relevant code to be read before approval
- it encourages parallel read-only agents for broad code-reading surfaces
- it requires a durable audit log beside the plan for repeat audit loops
- it defines the proper-audit checklist for deciding whether the plan was
  actually audited well enough
- it requires requirements, non-requirements, constraints, non-constraints,
  assumptions, and complexity sources to be stated before architecture review
- it encodes tiny-team maintainability: self-documenting, simple,
  easy-to-debug code with proven libraries or existing patterns where possible
- it requires depth-first sequencing: a first integrated slice through the
  highest-risk seam, real proof before widening, and no late "hope it works"
  integration phase
- it requires existing pattern inventory and convergence before new patterns
  are accepted
- it reviews caller-side API shape, invariants, state model, atomicity,
  abstraction value, refactor radius, drift-proof coupling, and live concept
  count
- it prefers meaningful integration proof over low-value tests that mostly
  prove compiler, framework, mocks, or implementation details
- it defines a parallel-agent review workflow without adding unnecessary
  deterministic machinery
- it gives a concrete package shape
- it gives a phased implementation plan and verification commands

The skill itself is not built yet.
