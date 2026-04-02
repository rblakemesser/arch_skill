# `plan-enhance` Command Contract

Use this reference when the user runs `arch-step plan-enhance`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for Sections `1`, `5`, `6`, `7`, and `8`.
- Use the highest bar in this package: best possible by our standards, simplest viable design, correct by construction, SSOT, and hard to drift.

## Artifact sections this command reads for alignment

- the full plan doc
- especially `# 0)`, `# 1)`, `# 5)`, `# 6)`, `# 7)`, and `# 8)`

## Artifact sections or blocks this command updates

- `arch_skill:block:plan_enhancer`
- when a better contract is obvious and low-risk to state, the relevant plan sections should be sharpened too

## Quality bar for what this command touches

- make SSOT explicit
- remove or reject parallel implementations
- make boundaries and invariants enforceable
- name required deletes and cleanup
- identify must-change call sites and drift-prone adopters
- keep the evidence plan common-sense and non-blocking

## Hard rules

- Docs-only. Do not modify code.
- Read `DOC_PATH` fully and enough code to make real architectural decisions.
- Treat code as ground truth.
- Do not design fallbacks or compatibility shims by default.
- Treat scope as authoritative. If consolidation expands scope, default to follow-up or ignore rather than asking for a new scope decision.
- Questions are only for true product, UX, or access gaps.

## Artifact preservation

- Preserve the canonical scaffold and append the helper block without degrading canonical Sections 0 through 10.
- Prefer inserting near the end before the Decision Log.
- If the doc is materially non-canonical, route to `reformat` before hardening the plan.

## Update rules

Write or update:

- `arch_skill:block:plan_enhancer`

The block should capture:

- concrete plan upgrades
- whether the architecture is now best possible by our standards
- drift-proofing rules
- must-change call sites
- deletes and cleanup
- consolidation sweep with include, follow-up, or ignore calls
- evidence plan
- questions only if truly needed

The helper block is not a sidecar plan. It exists to harden the main artifact.

## Console contract

- North Star reminder
- punchline
- what upgrades were made to the plan
- biggest remaining risks
- next action
