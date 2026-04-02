# `deep-dive` Command Contract

Use this reference when the user runs `arch-step deep-dive`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for Sections `4`, `5`, and `6`, plus `planning_passes`.
- Carry forward the drift-proof rules from `shared-doctrine.md`: code is ground truth, no competing sources of truth, no fallback by default, idiomatic defaults, and scoped consolidation.

## Artifact sections this command reads for alignment

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 1) Key Design Considerations`
- `# 2) Problem Statement`
- `# 3) Research Grounding`
- any existing `External Research`

## Artifact sections or blocks this command updates

- `planning_passes`
- `# 4) Current Architecture (as-is)`
- `# 5) Target Architecture (to-be)`
- `# 6) Call-Site Audit (exhaustive change inventory)`
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`

## Quality bar for what this command touches

- Section 4 should describe the current structure, flows, ownership, and failure behavior concretely enough to plan against.
- Section 5 should fully specify the target architecture: future structure, contracts, boundaries, SSOT, and no parallel paths.
- Section 6 should be exhaustive enough to drive implementation and later audit.
- If the plan introduces a central pattern, the consolidation sweep should capture include, defer, or exclude candidates rather than ignoring drift risk.

## Consistency duties beyond local ownership

- If Sections 4 through 6 materially sharpen the design, repair any clearly stale TL;DR, Section 0, or Section 1 claims that are now wrong.
- If the architecture choice changed in a meaningful way, append or update a Decision Log entry instead of silently replacing history.
- If the new target architecture invalidates the current phase plan, say so plainly and point the next move to `phase-plan`.

## Hard rules

- Docs-only. Do not modify code.
- Resolve `DOC_PATH`.
- Read code and run read-only searches as needed.
- If the North Star or UX scope is contradictory, pause for a quick doc edit.
- Code is ground truth.
- No fallback or shim design unless explicitly approved in the plan doc.
- If multiple viable technical approaches exist, choose the most idiomatic default and note alternatives in the doc instead of punting the decision back to the user.

## Artifact preservation

- Preserve the canonical scaffold when it already exists.
- Preserve exact canonical headings and numbering for Sections 4, 5, and 6 in canonical docs.
- If this command inserts missing sections into a canonical doc, use the exact headings from `artifact-contract.md`.
- If the doc is materially non-canonical outside this command's safe repair boundary, stop and route to `reformat`.

## Planning-passes update rule

- Ensure the `planning_passes` block exists.
- If external research already exists in the doc, mark:
  - `deep_dive_pass_2: done <YYYY-MM-DD>`
- Otherwise mark:
  - `deep_dive_pass_1: done <YYYY-MM-DD>`
- Preserve existing timestamps and never wipe completed fields.

## Pattern consolidation sweep

- If this design introduces or sharpens a central pattern, look for other places that should adopt it.
- Default dispositions:
  - clearly in scope -> include
  - meaningful scope expansion -> defer or exclude and continue
  - stop only if the plan is internally contradictory

## Update rules

This command writes or updates:

- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`

Use semantic section replacement if blocks do not exist yet. Otherwise insert missing top-level sections in canonical order without degrading the surrounding canonical scaffold.

## Console contract

- North Star reminder
- punchline
- what changed in current architecture, target architecture, and call-site audit
- issues or risks if real
- next action
