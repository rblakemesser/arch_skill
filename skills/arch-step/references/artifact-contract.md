# Arch Step Artifact Contract

Use this file when `arch-step` needs the canonical full-arch plan artifact shape, ownership model, and cross-section consistency rules.

This file is the self-contained artifact contract for `arch-step`. When a command writes or updates the plan doc, preserve this artifact unless the owning command contract explicitly says otherwise.

The finished artifact is one coherent plan doc, not a menu of mostly-independent sections. The headings below exist so later commands keep sharpening the same plan instead of inventing parallel structures.

## DOC_PATH and WORKLOG_PATH

- `DOC_PATH` is the one canonical plan doc under `docs/`.
- New docs use:
  - `docs/<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`
- `WORKLOG_PATH` is:
  - `<DOC_DIR>/<DOC_BASENAME>_WORKLOG.md`
- Planning commands update `DOC_PATH` only.
- `implement` updates both `DOC_PATH` and `WORKLOG_PATH`.
- `audit-implementation` updates `DOC_PATH` only.

## Canonical plan doc shape

The canonical doc is not a loose outline. It is the specific full-arch plan artifact produced by `arch-new` and preserved by `arch-reformat`.

### Always-required frontmatter

- `title`
- `date`
- `status`
- `fallback_policy`
- `owners`
- `reviewers`
- `doc_type`
- `related`

### Always-required scaffold in a canonical doc

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 1) Key Design Considerations (what matters most)`
- `# 2) Problem Statement (existing architecture + why change)`
- `# 3) Research Grounding (external + internal “ground truth”)`
- `# 4) Current Architecture (as-is)`
- `# 5) Target Architecture (to-be)`
- `# 6) Call-Site Audit (exhaustive change inventory)`
- `# 7) Depth-First Phased Implementation Plan (authoritative)`
- `# 8) Verification Strategy (common-sense; non-blocking)`
- `# 9) Rollout / Ops / Telemetry`
- `# 10) Decision Log (append-only)`

Every `arch-step` command is trying to converge the doc toward this finished shape. A command is not successful if it writes its local block but leaves the overall artifact structurally drifted or obviously contradictory.

### Reformat-only appendices when needed

- `# Appendix A) Imported Notes (unplaced; do not delete)`
- `# Appendix B) Conversion Notes`

`arch-reformat` may preserve imported material via appendices, but it should still normalize the doc back to this shape.

## Presence is not enough

- A heading existing does not mean the section is good enough.
- Use `section-quality.md` to judge whether a section is concrete enough for downstream work.
- `advance` and `status` should treat weak sections as incomplete enough to matter.
- A canonical doc is only truly healthy when its sections agree with each other.

## Artifact-first execution rule

- `DOC_PATH` is the primary state of the workflow.
- Every command begins by checking whether `DOC_PATH` still matches the canonical scaffold closely enough to support ordinary `arch-step` updates.
- Local block ownership does not override global artifact preservation.
- Preserve the exact canonical headings when they already exist. Do not rename them to nearby equivalents.
- If a command can safely repair the portion of scaffold it owns, repair it.
- If the doc is materially non-canonical outside that safe repair boundary, stop and route to `reformat`.
- No command may delete or silently degrade unrelated canonical sections.

## Section roles and primary writers

The canonical sections are shared state, but primary ownership is still useful:

- `# TL;DR`, `# 0)`, `# 1)`, `# 2)`, `# 8)`, `# 9)`, `# 10)`:
  - role: shared plan spine for outcome, scope, priorities, problem framing, verification, rollout, and drift history
  - seeded by `new` and `reformat`
  - later commands preserve them and may update them only when their command contract requires it
- `# 3) Research Grounding`:
  - role: evidence anchors, reusable patterns, and open questions grounded in reality
  - primary writer: `research`
- `# 4) Current Architecture`, `# 5) Target Architecture`, `# 6) Call-Site Audit`:
  - role: make the current state, desired state, and completeness surface concrete enough to build and audit
  - primary writer: `deep-dive`
- `# 7) Depth-First Phased Implementation Plan`:
  - role: the single execution checklist
  - primary writer: `phase-plan`
- `External Research` block:
  - role: narrow external best-practice synthesis that materially affects this plan
  - primary writer: `external-research`
- helper blocks:
  - role: sharpen the main artifact without creating competing execution surfaces
  - primary writers are their matching helper commands
- `WORKLOG_PATH`:
  - role: execution truth and progress evidence
  - primary writer: `implement`
- `implementation_audit` block and phase reopening:
  - role: false-complete prevention and final completeness accounting
  - primary writer: `audit-implementation`

Primary ownership does not override global artifact preservation.

## Cross-section consistency rules

Treat these as hard consistency checks:

- TL;DR, Section 0, and Section 7 may not disagree on the goal, scope, or plan shape.
- Section 1 should explain the bias behind Section 5, not contradict it.
- Section 2 should explain the current reality that Sections 4 and 6 make concrete.
- Section 3 and External Research should sharpen Section 5 and Section 8, not float independently.
- Section 5 and Section 6 must agree on contracts, migrations, and deletes.
- Section 7 must be implementable from Sections 5 and 6 and must remain the single authoritative execution checklist.
- Section 8 must match the evidence philosophy in Section 0 and the verification load implied by Section 7.
- Section 9 should stay proportional to the actual rollout or telemetry needs.
- Section 10 records real drift, approvals, and plan changes instead of silently rewriting history.

## Full-consistency repair rule

- When a command materially changes architecture, scope, sequencing, verification, rollout, or accepted constraints, it must repair any now-obvious contradictions in adjacent canonical sections before exiting.
- Prefer minimal cross-section repairs over leaving stale claims behind.
- Use the Decision Log when a previously recorded decision changed in a meaningful way.
- If the command cannot safely repair the inconsistency without leaving its scope, it should say so plainly and point to the next command that must run.

## Minimum structural health checks

Before a command treats a doc as healthy enough for ordinary stage work, inspect:

- required frontmatter keys are present
- `# TL;DR` exists and still carries outcome, problem, approach, plan, and non-negotiables
- the `planning_passes` block exists near the top of the doc
- `# 0) Holistic North Star` exists
- sections `# 1)` through `# 10)` exist with the exact canonical headings when the doc is canonical
- command-owned blocks are present or can be inserted without renaming the surrounding canonical scaffold
- the sections this command depends on are strong enough for their job, not merely present

## North Star confirmation rule

- New or reformatted docs begin as `status: draft`.
- `new` and `reformat` must draft TL;DR + Section 0 without placeholders when source material allows.
- After drafting, stop and ask for explicit North Star confirmation.
- Once the user confirms, update `status:` from `draft` to `active`.
- Do not continue deeper into the flow until the North Star is confirmed.

## Stable block inventory

Keep these markers stable when present:

- `arch_skill:block:planning_passes`
- `arch_skill:block:research_grounding`
- `arch_skill:block:external_research`
- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `arch_skill:block:phase_plan`
- `arch_skill:block:reference_pack`
- `arch_skill:block:plan_enhancer`
- `arch_skill:block:overbuild_protector`
- `arch_skill:block:review_gate`
- `arch_skill:block:gaps_concerns`
- `arch_skill:block:implementation_audit`

If a matching semantic section exists without the marker, update it in place rather than duplicating it.

## Planning-passes block

`new` and `reformat` should preserve or insert this warn-first bookkeeping block near the top of the doc:

```text
<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: not started
external_research_grounding: not started
deep_dive_pass_2: not started
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
note: This is a warn-first checklist only. It should not hard-block execution.
-->
<!-- arch_skill:block:planning_passes:end -->
```

Update rules:

- `deep-dive` marks pass 1 or pass 2 depending on whether external research already exists
- `external-research` marks `external_research_grounding`
- preserve existing timestamps and never wipe completed fields

## Single-document rule

- All planning and decisions live in `DOC_PATH`.
- `WORKLOG_PATH` is progress evidence, not a second plan doc.
- Do not create sidecar planning docs.

## Write-boundary rule

- `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `review-gate`, and `audit-implementation` are docs-only.
- `implement` is the only code-writing command in this skill.
