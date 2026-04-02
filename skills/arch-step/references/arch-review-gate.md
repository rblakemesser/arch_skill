# `review-gate` Command Contract

Use this reference when the user runs `arch-step review-gate`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for the sections most central to the current plan.
- Keep this local. Do not turn it into external reviewer orchestration.

## Artifact sections this command reads for alignment

- the full plan doc
- the key code anchors relevant to the plan

## Artifact sections or blocks this command updates

- `arch_skill:block:review_gate`
- any plan sections that should change after accepted review feedback

## Quality bar for what this command touches

- ask whether the plan is idiomatic and complete relative to the code and its own claims
- identify plan drift, SSOT or contract violations, and missing work
- recommend only high-signal verification, not negative-value tests
- check whether sharp edges or new SSOTs need boundary comments

## Hard rules

- Docs-only. Do not modify code.
- Do the review locally. Do not use external reviewer CLIs or other-model consultations from this command.
- Read `DOC_PATH` plus the key repo anchors needed to answer the review question.
- If North Star or UX scope is contradictory, pause for a quick doc edit first.

## Artifact preservation

- Preserve the canonical scaffold and record review outcomes inside that artifact.
- Prefer inserting the helper block near the end before the Decision Log.
- If the doc is materially non-canonical, route to `reformat` before recording review guidance.

## Core review question

- `Is this idiomatic and complete relative to the plan? What is missing? Where does the code or plan drift? Are there any SSOT or contract violations?`

Integrate the feedback you agree with by updating the real plan sections first. The helper block records what changed and why.

## Update rules

Write or update:

- `arch_skill:block:review_gate`

Capture:

- reviewers: self
- question asked
- feedback summary
- integrated changes
- proceed decision

## Console contract

- North Star reminder
- punchline
- what the review changed
- remaining risks
- next action
