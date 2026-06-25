# Cynical Architecture Review Intention

Date: 2026-06-25

Status: intention and research brief. Runtime implementation landed as
[`skills/cynical-architecture-review/`](../skills/cynical-architecture-review/)
on 2026-06-25.

Implemented skill name: `cynical-architecture-review`

Reference pack:

- [Reference index](cynical_architecture_review_references/README.md)
- [Simplicity and architecture research](cynical_architecture_review_references/SIMPLICITY_AND_ARCHITECTURE_RESEARCH.md)
- [Doctrine notes](cynical_architecture_review_references/CYNICAL_ARCHITECTURE_REVIEW_DOCTRINE_NOTES.md)
- [Failure-pattern catalog](cynical_architecture_review_references/ARCHITECTURE_FAILURE_PATTERNS.md)
- [Future skill shape](cynical_architecture_review_references/FUTURE_SKILL_SHAPE.md)

## High-Level Intention

Build a review skill that hunts for accidental architecture before it spreads
further.

The posture is deliberately cynical:

- Assume the architecture was not designed with clear intention unless current
  code proves otherwise.
- Assume many structures "just happened" during iteration and then later work
  cemented them.
- Assume complexity got rationalized after the fact as architecture.
- Assume every new layer, owner split, wrapper, adapter, flag, queue, registry,
  helper, state surface, and abstraction must prove it exists because the user
  experience or a hard experiment constraint requires it.
- Assume the best architecture move is often deletion, consolidation, or a
  cleaner ownership boundary, not another abstraction.

The review does not try to change the intended product or experiment. It keeps
the required user experience and real constraints intact, then asks:

```text
What is the simplest robust architecture that achieves this same outcome with
fewer concepts, fewer files, fewer paths, fewer owners, fewer states, and less
code?
```

The target bar is aggressive: the reviewer should look for credible ways to
achieve the same user-visible behavior with roughly half the complexity and
half the code, without weakening experiment requirements.

## What This Review Is For

Use this concept for codebases or branches where the problem is not simply
"there may be a bug." The problem is that the architecture itself may have
emerged by accident:

- sprawl across files, services, helpers, prompts, configs, generated artifacts,
  tests, docs, or command surfaces
- invalid split ownership where two places partly own the same concept
- duplicate truth hidden behind friendly names
- layers that exist because earlier iterations needed a workaround
- compatibility paths that became permanent architecture
- abstractions that add vocabulary without removing complexity
- registries, dispatchers, adapters, feature flags, or orchestrators that make
  the system harder to understand than the user job requires
- patterns that should have been defused early but are now becoming examples
  for future code to copy

The review's job is to stop those patterns from becoming normalized.

## Explicit Scope Guard: Code Architecture First

This review should not spend its attention on QA, test coverage, test cleanup,
docs cleanup, README drift, proof freshness, CI hygiene, release readiness, or
generic "needs more tests/docs" commentary unless the user explicitly asks for
that lane.

Tests, docs, fixtures, examples, generated artifacts, comments, status text,
and proof claims are only evidence when they point back to code architecture:
a stale owner path, mocked boundary, side door, duplicate contract, generated
truth split, misleading future-copy surface, or other sign that the
architecture in code is heavier or less coherent than the real requirements
force it to be.

The default output should be about implemented code structure: owners,
boundaries, state, call paths, abstractions, shims, flags, adapters, duplicate
truth, and what can be deleted or consolidated while preserving the intended
UX and hard experiment requirements.

## Ground Truth Order

The reviewer should resolve truth in this order:

1. The intended user experience.
2. The actual experiment requirements and hard constraints.
3. Current code behavior and current ownership paths.
4. Existing repo patterns that already solve the same class of problem.
5. The smallest robust architecture that preserves items 1 and 2.
6. Only then, the implementation's current explanation for itself.

Docs, plans, status claims, names, comments, tests, and worklogs are useful
clues. They are not authority. A label like `canonical`, `shared`,
`orchestrator`, `registry`, `unified`, `v2`, `adapter`, `platform`, or `owner`
is only a claim.

## Core Review Question

The skill should repeatedly ask:

```text
If we started from the required user experience and constraints today, would we
choose this architecture again?
```

If the honest answer is no, the review should name:

- what requirement the current complexity claims to serve
- whether that requirement is real
- what concept, layer, owner, path, state, flag, or file can disappear
- what simpler owner boundary should replace it
- which existing pattern should absorb it
- what user-visible behavior must stay unchanged

## Source-Informed Doctrine

The research pack supports one main conclusion: strong architecture is
subtractive. It separates essential complexity from accidental complexity, then
removes accidental complexity instead of decorating it.

Important source-backed ideas:

- Elon Musk's engineering algorithm puts requirement challenge and deletion
  before simplification, speed, or automation. This maps directly to architecture
  review: do not optimize an architecture that should not exist.
- John Ousterhout frames complexity as what makes software hard to evolve.
  Dependencies and obscurity accumulate through many small choices, which
  matches the "just happened" failure mode.
- David Parnas argues that decomposition should hide design decisions likely
  to change, not mirror process steps. This is a direct test for invalid split
  ownership.
- Fred Brooks's conceptual integrity lens says one coherent design idea is
  better than many independent good ideas. Sprawl is often a loss of conceptual
  integrity, not a sign of power.
- Niklaus Wirth, Tony Hoare, Rich Hickey, Martin Fowler, Doug McIlroy, and John
  Gall all point toward the same review move: delete presumptive features,
  reduce intertwinement, prefer small composable units, and resist bloated
  systems that no one can fully understand.

Detailed source notes are in
[Simplicity and architecture research](cynical_architecture_review_references/SIMPLICITY_AND_ARCHITECTURE_RESEARCH.md).

## What The Future Skill Must Not Become

This should stay doctrine-first and review-only.

Do not turn it into:

- an implementation workflow
- a proof harness
- a visual verification ritual
- a deterministic architecture validator
- a grep gate
- a checklist executor
- a scoring engine
- a runner, controller, or orchestration layer
- a generic test/doc nit skill
- a UX redesign skill

It should explicitly not focus on QA, test coverage, test hygiene, docs
hygiene, README drift, or proof-chasing unless the user asks for that. Tests,
docs, fixtures, examples, generated artifacts, and status text are in scope
only when they reveal or preserve an architecture problem: a mocked boundary, a
stale generated truth, an old owner path, a misleading contract, or a side door
future work will copy. Otherwise, leave them alone.

The hard part is judgment: reading the code, understanding what the user
experience requires, and seeing where the architecture is heavier than the
problem.

## Relationship To Existing Review Skills

This review lane is related to existing skills, but it is not the same job.

- `cynical-code-review` distrusts implementation completion stories. It asks
  whether the code made a claimed outcome real.
- `thermo-nuclear-code-quality-review` attacks maintainability problems in
  implemented code.
- `exhaustive-code-review` owns coverage-ledger review over files, hunks, and
  abstractions.
- `plan-audit` and plan-backed implementation audit judge work against plan
  architecture and quality bars.

`cynical-architecture-review` should own accidental architecture detection and
subtraction-first architecture review. Its center is not "is this code complete?"
or "did we cover every file?" It is:

```text
What architecture happened by accident, what complexity is not forced by the
real requirements, and how do we defuse it before it becomes the next pattern?
```

## Future Work

The runtime package now lives at
[`skills/cynical-architecture-review/`](../skills/cynical-architecture-review/).
Keep it lean: `SKILL.md`, small references, and optional agent metadata only.
No scripts or harnesses are justified by this brief.
