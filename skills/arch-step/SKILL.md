---
name: arch-step
description: "Operate the explicit full-arch workflow one command at a time while preserving the canonical plan artifact and its bundled quality doctrine: `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `review-gate`, `implement`, `audit-implementation`, `status`, or `advance`. Use when the user wants a literal full-arch command surface with one specific plan-doc shape. Not for broader phase-family execution (`arch-plan`), read-only checklist routing (`arch-flow`), mini plans, lilarch, bugs, or open-ended loops."
metadata:
  short-description: "Explicit full-arch operator"
---

# Arch Step

Use this skill when the user wants a literal explicit full-arch command surface, not a loose approximation.

`arch-step` is self-contained. Its bundled references are the source of truth for artifact shape, block placement, stage ownership, and quality doctrine.

The primary object is not the selected command. The primary object is the one canonical full-arch plan doc plus the quality doctrine that makes that doc useful. Commands are controlled ways of advancing that doc toward the exact output shape defined inside this skill.

`arch-step` is a convergence skill. Every invocation should leave the plan doc closer to one finished artifact:

- required frontmatter
- `# TL;DR`
- `planning_passes`
- `# 0)` through `# 10)` with exact canonical headings
- optional helper blocks folded into the same doc
- `WORKLOG_PATH` once implementation begins

A command that updates its local block but leaves the overall artifact less coherent is wrong.

## When to use

- The user wants literal explicit full-arch control.
- The ask is command-shaped: `new`, `reformat`, `research`, `deep-dive`, `external-research`, `phase-plan`, `plan-enhance`, `fold-in`, `overbuild-protector`, `review-gate`, `implement`, `audit-implementation`, `status`, or `advance`.
- The user wants the same canonical plan artifact this skill defines.
- The user wants `advance` to choose exactly one best next full-arch command and then stop.
- The user wants a concise status readout based on the actual plan artifact, not a generic checklist.

## When not to use

- The user wants the broader intent-driven full-arch workflow handled more holistically or by phase family rather than by literal explicit commands. Use `arch-plan`.
- The user wants a read-only checklist or "what's next?" router. Use `arch-flow`.
- The task is a one-pass mini plan, a 1-3 phase small-feature flow, a bug flow, or an open-ended loop. Use `arch-mini-plan`, `lilarch`, `bugs-flow`, `goal-loop`, or `north-star-investigation`.
- The user is asking which arch skill to use. Use `arch-skills-guide`.

## Non-negotiables

- The canonical full-arch plan doc is the primary artifact. Commands are subordinate to it.
- The bundled `arch-step` contract files are the source of truth for stage behavior and quality bars.
- Do not paraphrase away concrete artifact rules that the bundled references already define.
- Every invocation must assess the current doc against both canonical structure and section quality before doing command-local work.
- No command may leave the doc less canonical than it found it.
- No command may treat a weak section as "done" merely because a heading or block exists.
- If a command materially changes scope, architecture, sequencing, verification, or rollout implications, it must repair any obvious contradictions it creates elsewhere in the canonical artifact before exiting.
- If the doc is malformed or materially non-canonical, repair it first when safe or route to `reformat`.
- Use repo evidence first. Ask only for true product, UX, external-constraint, access, or doc-path gaps.
- Keep one planning SSOT and one execution checklist. Do not create sidecar plan docs or competing checklists.
- Run exactly one command per invocation.
- `advance` chooses the next move from structural gaps first, quality gaps second, and stage order third. Helper commands stay explicit.
- `status` is read-only, compact, and based on the actual artifact.
- Keep one canonical `DOC_PATH` under `docs/` and derive `WORKLOG_PATH` from it.
- All planning commands are docs-only. Only `implement` may change code.
- Default to local implementation. Do not delegate implementation.

## First move

1. Read `references/artifact-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Resolve the requested command and `DOC_PATH` when the command needs an existing doc.
4. Assess the current doc against canonical structure and relevant section quality:
   - frontmatter
   - `# TL;DR`
   - `planning_passes`
   - exact top-level sections
   - command-owned blocks
   - contradictions across TL;DR, North Star, target architecture, phase plan, verification, rollout, and decision log
5. If the doc is missing essential scaffold:
   - repair the owned portion with the current command when safe
   - otherwise route to `reformat` instead of continuing on a malformed artifact
6. Read `references/section-quality.md` for the sections this command reads or writes.
7. Read the matching command reference:
   - `new` -> `references/arch-new.md`
   - `reformat` -> `references/arch-reformat.md`
   - `research` -> `references/arch-research.md`
   - `deep-dive` -> `references/arch-deep-dive.md`
   - `external-research` -> `references/arch-external-research.md`
   - `phase-plan` -> `references/arch-phase-plan.md`
   - `plan-enhance` -> `references/arch-plan-enhance.md`
   - `fold-in` -> `references/arch-fold-in.md`
   - `overbuild-protector` -> `references/arch-overbuild-protector.md`
   - `review-gate` -> `references/arch-review-gate.md`
   - `implement` -> `references/arch-implement.md`
   - `audit-implementation` -> `references/arch-audit-implementation.md`
   - `status` -> `references/status.md`
8. For `advance`, choose the one command that most improves artifact completeness or core-flow progress, then run only that command.

## Workflow

### 1) Public command surface

- `new`
- `reformat`
- `research`
- `deep-dive`
- `external-research`
- `phase-plan`
- `plan-enhance`
- `fold-in`
- `overbuild-protector`
- `review-gate`
- `implement`
- `audit-implementation`
- `status`
- `advance`

### 2) Top-level model

`arch-step` always reasons about one canonical full-arch artifact with this bundled canonical shape:

- frontmatter
- `# TL;DR`
- `planning_passes`
- `# 0) Holistic North Star`
- `# 1)` through `# 10)` with the exact canonical headings from `artifact-contract.md`
- optional helper or audit blocks folded into that same doc

Each command owns only part of that artifact, but every command must preserve the whole and respect the shared doctrine that keeps sections coherent. The finished artifact is not just a heading set. It is one internally consistent plan that says the same thing about outcome, scope, architecture, verification, rollout, and drift history from multiple angles.

### 3) `advance` selection rule

Choose exactly one next command using this precedence:

1. If no plan doc exists yet, run `new`.
2. If a doc exists but is not in the canonical `arch-step` shape, run `reformat`.
3. If the doc is still `status: draft`, stop at North Star confirmation.
4. If the canonical scaffold is missing required sections or required command-owned blocks, choose the command that repairs the earliest missing core portion of the artifact.
5. If the structure exists but the relevant sections are still too weak for the next phase, choose the command that hardens those sections.
6. Otherwise follow the canonical core arc below.

The core arc is canonical and ordered:

- `new` or `reformat`
- North Star confirmation if the doc is still `status: draft`
- `research`
- `deep-dive`
- `external-research` when warranted
- `deep-dive` again when external research materially changed the plan
- `phase-plan`
- `implement`
- `audit-implementation`

Do not auto-run more than one command.

### 4) Helper commands

These stay explicit and do not auto-run from `advance`:

- `plan-enhance`
- `fold-in`
- `overbuild-protector`
- `review-gate`

Default placement in the flow:

- after `phase-plan` and before `implement`, unless the user explicitly asks otherwise

### 5) Decision boundaries

- If the bundled contract already defines the block shape, placement rule, or output contract, preserve it.
- If the canonical doc already uses the exact canonical headings, preserve that wording and numbering.
- If a command snippet shows an unnumbered heading, treat it as a content skeleton, not permission to rename an already-canonical section.
- If a section is present but low quality, treat it as incomplete for `advance` and `status`.
- If a doc is actually mini-plan, lilarch, bug-flow, or investigation-shaped, stop and route to the correct skill instead of forcing it through this surface.
- If the user wants the broader full-arch skill rather than explicit command control, hand off to `arch-plan`.

## Output expectations

- Keep console output high-signal and natural:
  - North Star reminder
  - punchline
  - what changed
  - issues or risks
  - next action
  - need from the user only when truly required
  - pointers to `DOC_PATH` and `WORKLOG_PATH`
- For `status`, keep it compact:
  - one short structural line for the canonical artifact
  - one short line per core arc stage
  - one short helper summary line
  - one short best-next-move line

## Reference map

- `references/artifact-contract.md` - canonical full-arch plan artifact, block inventory, and worklog contract
- `references/shared-doctrine.md` - repo-evidence-first, alignment, evidence, SSOT, anti-drift, and scope doctrine shared across commands
- `references/section-quality.md` - why each artifact section exists, what good looks like, what weak looks like, and consistency checks
- `references/arch-new.md` - create canonical doc and stop for North Star confirmation
- `references/arch-reformat.md` - convert an existing doc into the canonical artifact without losing content
- `references/arch-research.md` - research grounding block contract
- `references/arch-deep-dive.md` - current architecture, target architecture, call-site audit, and planning-pass updates
- `references/arch-external-research.md` - external research block and planning-pass rules
- `references/arch-phase-plan.md` - authoritative phase-plan block contract
- `references/arch-plan-enhance.md` - plan-enhancer helper contract
- `references/arch-fold-in.md` - reference-pack helper contract
- `references/arch-overbuild-protector.md` - scope-triage helper contract
- `references/arch-review-gate.md` - review-gate helper contract
- `references/arch-implement.md` - implementation, worklog, and completion-discipline contract
- `references/arch-audit-implementation.md` - implementation audit and phase-reopen contract
- `references/status.md` - compact status rules grounded in the exact artifact
