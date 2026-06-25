# Cynical Architecture Review Doctrine Notes

Date: 2026-06-25

Parent brief:
[Cynical Architecture Review Intention](../CYNICAL_ARCHITECTURE_REVIEW_INTENTION_2026-06-25.md)

Research base:
[Simplicity and architecture research](SIMPLICITY_AND_ARCHITECTURE_RESEARCH.md)

Sibling references:

- [Failure-pattern catalog](ARCHITECTURE_FAILURE_PATTERNS.md)
- [Future skill shape](FUTURE_SKILL_SHAPE.md)

## Mission

The review should find architecture that emerged accidentally and stop it
from becoming the next copied pattern.

It should not merely say "this is complex." It should explain:

- what real requirement the complexity claims to serve
- whether that requirement is actually real
- which ownership boundary is wrong
- which concepts are accidental
- which code paths can disappear
- what smaller architecture would preserve the same user experience and
  experiment constraints

## Required Posture

Start from these assumptions:

- The architecture was probably not built from a clean first-principles design.
- The current shape probably reflects a sequence of local iterations.
- Each iteration probably made the previous compromise look more permanent.
- Names probably overstate intention.
- Existing patterns may be accidents that happened often enough to look normal.
- If the codebase offers two ways to do the same thing, future agents will copy
  both unless the review defuses one.

This is not cynicism for tone. It is a way to counter the default agent failure:
assuming that existing structure exists for a good reason.

## Ground Truth

The reviewer should identify ground truth in this order:

1. Intended user experience: what the user should actually see, do, or rely on.
2. Experiment requirements: what must stay measurable, switchable, reversible,
   comparable, or stable for the experiment to remain valid.
3. Hard constraints: platform, runtime, data, security, performance, model,
   framework, or migration constraints that cannot be wished away.
4. Existing canonical patterns: the repo's current best path, if one exists.
5. Current architecture: actual owners, call paths, state, storage, APIs,
   generated artifacts, prompts, docs, tests, and commands.
6. Implementation story: what the code claims about itself through names,
   comments, plans, status, and helper structure.

The implementation story is last because it is often the lie.

## Core Review Loop

For each major architecture surface:

1. Name the user job.
2. Name the real requirements and non-requirements.
3. Name the required experiment constraints.
4. Trace the current code path that delivers the job.
5. List the live concepts a maintainer must understand.
6. Identify the owner of each concept.
7. Ask which concepts are essential and which are accidental.
8. Ask what can be deleted, merged, moved, or made impossible.
9. Sketch the smaller architecture that preserves the same behavior.
10. Write only findings that materially reduce sprawl, split ownership,
    bug-vector count, or future-copy risk.

## Subtraction Questions

Use these questions aggressively:

- What would disappear if we rebuilt this from the required user experience?
- Which requirement forces this layer to exist?
- Which user-visible behavior would break if this abstraction were deleted?
- Which experiment requirement would be weakened if this path were removed?
- Why is this not just a compatibility shim that became architecture?
- Why is this not just a local workaround copied into a pattern?
- What code would a future agent copy from this, and would that make the repo
  worse?
- What invariant is split across multiple places?
- What state can be represented once instead of synchronized?
- What branching can be turned into a simpler model?
- What optionality exists only because ownership is unclear?
- What does this layer know that it should not know?
- What does the caller have to remember that the architecture should enforce?

## Complexity Tax Ledger

When reviewing a suspect structure, account for its tax:

- files added
- concepts added
- APIs added
- flags or modes added
- states added
- owner boundaries added
- generated artifacts added
- call paths added
- sync points added
- places future edits must remember to touch
- ways a future agent can choose the wrong path

Then compare that tax to the requirement it claims to serve.

If the tax is real and the requirement is vague, imagined, or avoidable, the
architecture should be challenged.

## Valid Reasons For Complexity

The review should hate complexity for no reason, not complexity itself.

Complexity can be justified when it directly preserves:

- a required user experience
- a real experiment requirement
- a hard runtime or platform constraint
- a security boundary
- a reliability or recovery requirement
- a performance requirement measured in the actual system
- a compatibility constraint with an explicit sunset path
- a domain concept that would otherwise leak everywhere
- an invariant that becomes safer because the abstraction exists

Even then, the reviewer should ask whether the same requirement can be met with
fewer live concepts.

## Invalid Reasons For Complexity

These should be treated as suspect by default:

- "We might need it later."
- "This is how the previous iteration did it."
- "It was easier to add a wrapper."
- "The docs explain the contract."
- "The test covers it."
- "The plan said to add a layer."
- "This gives us flexibility" without a concrete current variation.
- "This keeps old behavior working" without a real compatibility requirement
  and removal path.
- "This pattern already exists elsewhere" when the existing pattern may itself
  be accidental.
- "This is cleaner" when the concept count increased.

## Findings Bar

A good finding should have this shape:

```text
This structure is accidental because <evidence from current code>. It claims to
serve <requirement>, but the real requirement is <smaller truth>. The current
shape adds <complexity tax> and creates <future spread or bug risk>. A smaller
architecture would <delete/consolidate/move/make impossible> while preserving
<user behavior and experiment constraint>.
```

A weak finding is:

- cosmetic
- style-only
- test-only
- doc-only
- QA-focused unless the user requested QA
- proof-focused unless the user requested proof validation
- a vague "too complex" complaint
- a preference for a different pattern without showing a smaller architecture
- an attempt to change the product or experiment rather than simplify the
  architecture that serves it

## QA, Tests, And Docs Boundary

This review should not drift into pedantic QA, test, or docs review.

Do not focus on:

- test coverage gaps
- test naming or fixture polish
- missing test cases
- README or docs drift
- doc wording cleanup
- proof freshness
- release-readiness checklists
- CI hygiene

unless the user explicitly asks for that lane.

Tests and docs are only relevant when they are architecture evidence. Examples:

- a test mocks the boundary that should be the real owner
- a fixture preserves an obsolete contract
- generated docs or schemas still teach the old authority path
- examples route future work through the wrong owner
- status text says a path is deleted while code still routes through it
- a doc is the only thing preventing misuse that the API should make impossible

If tests or docs do not expose an architecture ownership, complexity, or
future-copy problem, ignore them.

## Protection Against Overreach

The reviewer must not use simplicity as an excuse to damage the product.

Do not recommend removing:

- user-visible behavior that is part of the requested experience
- experiment branches needed for measurement
- compatibility code that has a real active consumer and no approved cutover
- safety checks that enforce an invariant
- domain concepts that are irreducible
- necessary adapters around external systems

Instead, ask whether those realities can be represented with clearer ownership
and fewer live concepts.

## Output Philosophy

The skill should produce findings, not a giant essay.

The saved artifact can contain maps and reasoning. The final response should
lead with blockers:

- accidental architecture that should be defused now
- invalid owner splits
- structures likely to spread if left in place
- deletion or consolidation moves with the highest leverage
- residual uncertainties where the reviewer could not determine the true
  requirement or owner

The tone should be blunt but useful. The goal is not to shame the previous
iteration. The goal is to prevent local accidents from becoming permanent
architecture.
