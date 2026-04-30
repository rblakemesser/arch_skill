# Figma Best Practices Fidelity Audit Upgrade Worklog

Plan doc: `docs/FIGMA_BEST_PRACTICES_FIDELITY_AUDIT_UPGRADE_2026-04-30.md`

## Implementation Pass 1

Date: 2026-04-30

Work completed:

- Kept the upgrade inside the existing prompt-only
  `skills/figma-best-practices` package.
- Added `references/figma-audit-toolkit.md`.
- Added `references/figma-visual-fidelity.md`.
- Reworked `references/figma-source-backed-parity.md` around source-truth
  discipline and bounded parity claims.
- Updated `references/figma-file-craft.md` and
  `references/figma-mcp-agent-gotchas.md` for `Index`, Figma cleanliness,
  audit write boundaries, and routing into the new references.
- Refactored `SKILL.md` and `agents/openai.yaml` to expose the expanded audit
  and fidelity lane without creating a new skill or fixed workflow.
- Added the requirements-doc status note that the durable content was folded
  into `figma-best-practices`.

Verification:

- `rtk proxy npx skills check` passed.
- Re-read edited runtime files after writing them.
- `rtk git diff --check -- skills/figma-best-practices/SKILL.md
  skills/figma-best-practices/agents/openai.yaml
  skills/figma-best-practices/references/figma-file-craft.md
  skills/figma-best-practices/references/figma-mcp-agent-gotchas.md` passed.
- `rtk rg -n "[ \t]+$" ...` found no trailing whitespace in edited runtime
  files and planning docs checked during this pass.
- Runtime leak review found no project-specific names or absolute local paths
  under `skills/figma-best-practices`.
- `SKILL.md` frontmatter description length is 527 characters.

Notes:

- The worktree already contained overlapping Figma best-practices edits before
  this implementation pass; this pass preserved and built on them.
- No branch was created. The current developer instruction requires respecting
  the existing branch.
- `make verify_install` was not run because install behavior did not change.
- App/device tests were not run because no app code or external audit tooling
  changed.

## Implementation Pass 2

Date: 2026-04-30

Fresh audit result addressed:

- Phase 2 was reopened because `figma-audit-toolkit.md` was missing required
  output-contract shapes for compliance checklist, authorship ledger,
  handoff-readiness ledger, and style-guide gap ledger.
- Phase 7 was reopened because the first verification pass did not catch that
  runtime doctrine gap.

Work completed:

- Added compliance checklist, authorship ledger, handoff-readiness ledger, and
  style-guide gap ledger contracts to
  `skills/figma-best-practices/references/figma-audit-toolkit.md`.
- Added a concise `SKILL.md` output-expectations pointer for compliance
  checklist and handoff-readiness language so the output set is discoverable
  from the entrypoint without bloating it.
- Updated Phase 2 and Phase 7 progress truth in the plan doc; the authoritative
  implementation audit block remains untouched for the next fresh audit.

Verification:

- `rtk proxy npx skills check` passed.
- Re-read `figma-audit-toolkit.md` and `SKILL.md` after the repair.
- Targeted `rtk rg` confirmed all required output contract names are present:
  findings, compliance checklist, coverage ledger, app-fidelity match ledger,
  authorship ledger, handoff-readiness ledger, style-guide gap ledger,
  duplicate/stale ledger, verification receipts, and repair plan.
- Runtime leak review found no project-specific names or absolute local paths
  under `skills/figma-best-practices`.
- Trailing-whitespace checks found no issues in the edited runtime files and
  planning docs checked during this pass.
- Tracked-file `rtk git diff --check` passed for `SKILL.md` and the plan/worklog
  docs checked during this pass.

Notes:

- `make verify_install` was not run because install behavior did not change.
- App/device tests were not run because no app code or external audit tooling
  changed.
