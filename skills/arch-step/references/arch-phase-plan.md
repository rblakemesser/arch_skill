# `phase-plan` Command Contract

Use this reference when the user runs `arch-step phase-plan`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for Sections `5`, `6`, `7`, and `8`.
- Carry forward the warn-first sequencing and anti-bureaucratic verification doctrine from the bundled doctrine.

## Artifact sections this command reads for alignment

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 5) Target Architecture`
- `# 6) Call-Site Audit`
- `planning_passes`

## Artifact sections or blocks this command updates

- `# 7) Depth-First Phased Implementation Plan (authoritative)`
- `arch_skill:block:phase_plan`

## Quality bar for what this command touches

- Section 7 is the single authoritative execution checklist.
- The plan should be foundational-first.
- Each phase should have goal, work, verification, docs or comments when needed, exit criteria, and rollback.
- Verification should be small, credible, and non-bureaucratic.
- Helper blocks may constrain the phase plan, but they must not compete with it.

## Consistency duties beyond local ownership

- If the phase plan changes sequencing, scope shape, or verification expectations, repair the smallest stale claims in TL;DR, Section 0, and Section 8.
- If new sequencing or scope decisions replace an earlier assumption, append or update Section 10 rather than silently rewriting history.
- Section 7 must remain the one execution checklist even after helper blocks exist.

## Hard rules

- Docs-only. Do not modify code.
- Resolve `DOC_PATH`.
- If North Star or UX scope is contradictory, pause for a quick doc edit first.
- Do not hard-block if planning passes are incomplete; warn and continue.
- If you discover missing work while planning, add it to the phase plan rather than leaving it implicit.

## Artifact preservation

- Preserve the canonical scaffold when it already exists.
- Preserve the exact canonical heading and numbering for Section 7 in canonical docs.
- If this command inserts the phase-plan section into a canonical doc, use the exact Section 7 heading from `artifact-contract.md`.
- If the doc is materially non-canonical outside this command's safe repair boundary, stop and route to `reformat`.

## Preflight

Before writing the phase plan:

- inspect `planning_passes`
- or infer from doc contents if the block is missing
- if recommended sequencing is incomplete or unknown, warn but still write the phase plan

## Update rules

Write or update:

- `arch_skill:block:phase_plan`

If `DOC_PATH` is already canonical, preserve or insert the section as:

- `# 7) Depth-First Phased Implementation Plan (authoritative)`

Use this canonical block shape:

```text
<!-- arch_skill:block:phase_plan:start -->
# Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; every phase has exit criteria + explicit verification plan (tests optional). No fallbacks/runtime shims — the system must work correctly or fail loudly (delete legacy paths). Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests (deletion checks, visual constants, doc-driven gates). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).

## Phase 1 — <foundation>

* Goal:
* Work:
* Verification (smallest signal):
* Docs/comments (propagation; only if needed):
* Exit criteria:
* Rollback:

## Phase N — <end state + cleanup>

* Goal:
* Work:
* Verification (smallest signal):
* Docs/comments (propagation; only if needed):
* Exit criteria:
* Rollback:
<!-- arch_skill:block:phase_plan:end -->
```

## Console contract

- North Star reminder
- punchline
- what changed in the phase plan
- warn about missing prior passes when relevant
- next action
