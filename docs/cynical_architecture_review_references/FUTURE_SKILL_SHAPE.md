# Future Skill Shape

Date: 2026-06-25

Parent brief:
[Cynical Architecture Review Intention](../CYNICAL_ARCHITECTURE_REVIEW_INTENTION_2026-06-25.md)

Research base:
[Simplicity and architecture research](SIMPLICITY_AND_ARCHITECTURE_RESEARCH.md)

Doctrine base:
[Doctrine notes](CYNICAL_ARCHITECTURE_REVIEW_DOCTRINE_NOTES.md)

Failure catalog:
[Architecture failure patterns](ARCHITECTURE_FAILURE_PATTERNS.md)

Status: proposal/source notes folded into the implemented
[`skills/cynical-architecture-review/`](../../skills/cynical-architecture-review/)
package on 2026-06-25. Do not install this document as runtime behavior; the
runtime contract lives in the skill package.

## Implemented Skill

```text
cynical-architecture-review
```

Subtitle:

```text
Subtraction-first review for accidental architecture.
```

## Repeated User Problem

The user has code, a branch, a plan-backed implementation, or an existing
subsystem that may technically work but has developed ugly architecture:
sprawl, split ownership, duplicate truth, wrappers, flags, registries, wrong
boundaries, and local patterns that spread because each iteration accepted the
previous accident.

The user wants a reviewer to distrust that architecture and find the simpler
structure that should exist underneath it.

## Canonical User Asks

```text
Run a cynical architecture review on this branch. Assume the architecture just
happened and find the sprawl, invalid ownership splits, and complexity we can
delete.
```

```text
Audit this subsystem for accidental architecture. Do not change the UX or
experiment requirements; tell me how to achieve the same behavior with half the
concepts.
```

```text
This plan was implemented, but I think the architecture got ugly. Find the
wrong owners, duplicate truths, wrappers, flags, and places where iteration
cemented bad structure.
```

## Anti-Cases

Do not use this skill when:

- The user wants ordinary bug-focused code review.
- The user wants exhaustive coverage accounting over every changed file and
  hunk. Use `exhaustive-code-review`.
- The user wants skeptical implementation completion review. Use
  `cynical-code-review`.
- The user wants harsh maintainability review without the accidental
  architecture and requirement-grounding posture. Use
  `thermo-nuclear-code-quality-review`.
- The user wants a plan audited before implementation against the repo quality
  canon. Use `plan-audit`.
- The user wants QA review, test coverage review, test cleanup, docs cleanup,
  README drift review, proof validation, or release-readiness checking. Use the
  relevant review or verification lane only if the user asks for it.
- The user wants implementation or repair work.

## Source Trigger Description

Source text that shaped the runtime trigger:

```yaml
description: "Run a prompt-only cynical architecture review over a branch, diff, subsystem, plan-backed implementation, or code area by assuming the architecture was not intentionally designed but emerged through iteration and got cemented. Hunt for sprawl, invalid split ownership, duplicate truth, accidental abstractions, compatibility shims, flags-as-architecture, registries, adapters, state spread, wrong decomposition, and complexity not forced by the intended user experience or hard experiment requirements. Push for subtraction-first architecture: delete, consolidate, move ownership, simplify boundaries, and preserve the same UX with fewer concepts and less code. Not for normal bug review, QA/test/doc review, exhaustive coverage review, completion-truth review, implementation, or proof harnesses."
```

This is intentionally posture-heavy. The implemented skill description was
checked against runtime metadata limits.

## Mission

Review current code architecture from a subtractive stance.

The reviewer should:

1. Name the intended user experience.
2. Name hard requirements and experiment constraints.
3. Trace current code ownership and behavior.
4. Identify architecture that appears to have emerged accidentally.
5. Separate essential complexity from accidental complexity.
6. Find deletion, consolidation, and owner-boundary repair opportunities.
7. Flag patterns likely to spread if left in place.
8. Return findings that preserve behavior while making the architecture
   smaller, clearer, and harder to misuse.

## Non-Negotiables

- Review only. Do not edit code.
- Doctrine only. Do not add a runner, harness, controller, scorer, or formal
  parameter interface.
- Current code is the authority for what exists.
- Intended UX and experiment requirements are the authority for what must keep
  existing.
- Existing architecture is not self-justifying.
- Every abstraction, layer, flag, wrapper, registry, adapter, state surface,
  compatibility path, and owner split must point to a real requirement or lose
  trust.
- Findings must propose simplification without changing the user-visible
  behavior or weakening experiment requirements.
- Do not focus on QA, test coverage, test hygiene, docs hygiene, README drift,
  proof validation, or release-readiness checks unless the user explicitly asks
  for that lane.
- Tests, docs, fixtures, examples, generated artifacts, and status text are
  evidence only when they reveal an architecture problem: a stale generated
  truth, mocked boundary, duplicate contract, side door, old owner path, or
  misleading contract future work will copy.
- Do not flood the user with style nits, test nits, doc hygiene, or generic
  "clean code" advice.

## First Move

1. Resolve review target from the user's natural language: current branch,
   diff, path set, subsystem, plan-backed implementation, or named architecture
   area.
2. Read local instructions and relevant repo conventions.
3. Read the smallest amount of code needed to map the user job, current owners,
   current behavior, and adjacent paths.
4. If a plan or completion claim exists, treat it as a claim to test against
   code, not as authority.
5. Build a short architecture suspicion map before writing findings.

## Review Lenses

The skill should use these lenses:

- user-experience preservation
- experiment requirement preservation
- essential versus accidental complexity
- owner and invariant mapping
- Parnas-style information hiding
- Brooks-style conceptual integrity
- Ousterhout-style dependency and obscurity accumulation
- Musk-style delete-before-optimize sequence
- Wirth/Hoare/Hickey/Fowler-style resistance to bloat, hidden cleverness,
  intertwinement, and presumptive features
- repo-local canonical path and convergence doctrine
- future-agent copy risk

## Suggested Saved Artifact

The implemented skill saves review artifacts under:

```text
/tmp/cynical-architecture-review/<scope-slug>-<timestamp>/
```

Suggested files:

- `target.md`
  - review target, user job, constraints, and plan/claim sources if any
- `architecture-map.md`
  - current owners, call paths, states, flags, configs, generated artifacts,
    docs/prompts/tests only when they affect architecture ownership or preserve
    a misleading path
- `complexity-ledger.md`
  - live concepts, files, APIs, states, flags, adapters, registries, wrappers,
    compatibility paths, and sync points
- `subtraction-map.md`
  - what can be deleted, consolidated, moved, inlined, made impossible, or
    represented once
- `coverage.md`
  - inspected files, traced paths, architecture surfaces, native agent lanes
    if used, and honest coverage gaps
- `findings.md`
  - findings-first review with concrete evidence and simplification direction
- `verdict.md`
  - approval state and top architecture risks

This artifact is a Markdown review ledger, not a proof harness.

## Verdicts

Possible verdicts:

- `approve`
  - No material accidental architecture issue was found in the requested scope.
- `not-approved`
  - At least one architecture issue should be repaired before the pattern
    spreads further.
- `scope-incomplete`
  - The reviewer could not inspect enough code to determine the architecture
    truth honestly.

## Finding Shape

Use this structure:

```text
Finding: <short title>
Evidence: <file/path/code behavior anchor>
Accidental architecture: <what appears to have emerged rather than been designed>
Requirement check: <real UX/experiment/constraint truth>
Complexity tax: <concepts/files/paths/states/owners added>
Spread risk: <how future work will copy or cement it>
Simpler architecture: <delete/consolidate/move ownership/reduce state/make impossible>
Behavior preserved: <what user-visible behavior or experiment requirement remains intact>
```

## Peer Boundary

### Versus `cynical-code-review`

`cynical-code-review` asks whether an implementation story is truthful in code.

`cynical-architecture-review` asks whether the architecture itself is accidental
and unnecessarily complex, even if the implementation story is mostly true.

### Versus `thermo-nuclear-code-quality-review`

`thermo-nuclear-code-quality-review` is a broad harsh maintainability review.

`cynical-architecture-review` is narrower and more requirement-grounded. It is
not simply "make code prettier." It asks what architecture can be removed while
preserving the intended UX and hard constraints.

### Versus `exhaustive-code-review`

`exhaustive-code-review` owns coverage discipline.

`cynical-architecture-review` owns architectural suspicion and subtraction.
Coverage matters only to the extent needed to make the architectural judgment
honest.

### Versus `plan-audit`

`plan-audit` owns plan-readiness and plan-backed implementation audit.

`cynical-architecture-review` can use a plan as context, but it is code-first
and can run without a plan.

## Implementation Constraint For Later

If this becomes a skill, start with:

```text
skills/cynical-architecture-review/
  SKILL.md
  agents/openai.yaml
  references/review-lenses.md
  references/failure-patterns.md
  references/output-contract.md
```

Do not add scripts unless a future user explicitly asks for a narrow
mechanical helper and prompt-only use has proven insufficient. The current
brief does not justify scripts.
