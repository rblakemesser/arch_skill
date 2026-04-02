# `audit-implementation` Command Contract

Use this reference when the user runs `arch-step audit-implementation`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for Sections `5`, `6`, `7`, `WORKLOG_PATH`, and `implementation_audit`.
- This is the highest-bar completeness check in the package. It exists to stop false-complete claims.

## Artifact sections this command reads for alignment

- the full plan doc
- target architecture contracts
- call-site audit and delete list
- phase plan and phase statuses
- definition of done and evidence expectations
- worklog when present

## Artifact sections or blocks this command updates

- `arch_skill:block:implementation_audit`
- reopened phase status lines and `Missing (code):` notes
- `Manual QA (non-blocking):` notes when needed

## Quality bar for what this command touches

- validate code completeness against plan reality
- distinguish missing code from missing manual QA
- reopen false-complete phases
- keep missing items evidence-anchored and concrete

## Hard rules

- Docs-only. Do not modify code.
- Resolve `DOC_PATH`.
- Code is ground truth.
- This is a code-completeness audit, not a bureaucracy audit.
- Missing manual QA evidence is non-blocking and should not by itself reopen phases.
- Do not "fix it while you are here." Record gaps instead.

## Highest-bar audit criteria

Check all of these:

- absolute completeness:
  - if the plan says something is done, it is actually built
- architecture compliance:
  - SSOT is real
  - boundaries and contracts match the plan
  - required deletes and cleanup actually happened
  - no forbidden fallbacks or shims slipped in
- idiomatic fit:
  - the implementation aligns with existing repo patterns unless the plan explicitly justified divergence
- call-site completeness:
  - every call site that should have migrated actually migrated

## Artifact preservation

- Preserve the canonical scaffold and record audit outcomes inside that artifact.
- Prefer updating the existing phase sections and implementation-audit block rather than creating parallel audit structure.
- If the doc is materially non-canonical, route to `reformat` before certifying completeness against it.

## Audit procedure

- read `DOC_PATH` fully
- extract target contracts, call-site audit items, phase plan, delete list, and done criteria
- split evidence expectations into:
  - code-verifiable evidence
  - manual non-blocking evidence
- validate each planned code change against repo reality
- search for missed call sites or lingering superseded patterns
- verify SSOT enforcement and cleanup
- reopen phases only for missing or incorrect code work

## Update rules

Write or update:

- `arch_skill:block:implementation_audit`

The block must capture:

- date
- code verdict: `COMPLETE` or `NOT COMPLETE`
- manual QA status as non-blocking
- code blockers
- reopened phases
- missing items with evidence anchors
- non-blocking follow-ups

If code work is missing, update the affected phase section in place with:

- `Status: REOPENED (audit found missing code work)`
- `Missing (code):`

If only manual QA is pending:

- do not reopen the phase
- update a `Manual QA (non-blocking):` note instead

## Console contract

- North Star reminder
- punchline
- what the audit found and what changed in the doc
- risks or blockers
- next action
