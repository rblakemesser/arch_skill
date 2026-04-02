# `fold-in` Command Contract

Use this reference when the user runs `arch-step fold-in`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for Section `7` and the helper-block expectations.
- The goal is to make implementation unable to miss important reference material by folding it into the plan itself.

## Artifact sections this command reads for alignment

- the full plan doc
- `related:` frontmatter when present
- the phase plan when present

## Artifact sections or blocks this command updates

- `arch_skill:block:reference_pack`
- `related:` frontmatter when relevant
- phase-plan `Reference obligations (must satisfy)` bullets when phases exist

## Quality bar for what this command touches

- resolve one `DOC_PATH` and the true set of reference materials
- read every reference fully
- distill binding obligations rather than vague summaries
- phase-align those obligations so implementation sees them where they matter
- fold the source material into the main artifact instead of leaving it out of line

## Hard rules

- Docs-only. Do not modify code.
- Resolve one `DOC_PATH` and the set of REFS from the user blurb and obvious plan references.
- Read every reference fully rather than hand-waving it.
- Preserve the single-document rule.
- Do not create a second execution checklist.

## Artifact preservation

- Preserve the canonical scaffold and fold references into it rather than creating parallel plan structure.
- If a phase plan exists, wire obligations into that authoritative section instead of inventing another checklist surface.
- If the doc is materially non-canonical, route to `reformat` before folding references in.

## Resolution and folding rules

- Prefer the most credible plan doc when multiple doc candidates exist.
- Never choose `*_WORKLOG.md` as `DOC_PATH`.
- Treat every other provided doc or URL as a candidate reference unless it is clearly just a code anchor.
- For each reference:
  - extract binding obligations
  - keep a stable `R#` identifier
  - inline the source or extracted text into the reference pack
- If phase alignment is uncertain, treat the obligation as global rather than asking a low-value question.

## Update rules

Write or update:

- `arch_skill:block:reference_pack`

If a phase plan exists, wire each phase with:

- `* Reference obligations (must satisfy):`

Populate those bullets with the phase-aligned obligations and `R#` references.

## Console contract

- North Star reminder
- punchline
- chosen `DOC_PATH` and how many refs were folded
- what changed in the reference pack and phase alignment
- next action
