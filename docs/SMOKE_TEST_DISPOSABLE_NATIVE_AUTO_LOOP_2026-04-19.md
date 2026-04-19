---
title: "arch_skill - Smoke test disposable native auto loop - Architecture Plan"
date: 2026-04-19
status: active
fallback_policy: forbidden
owners: [amir]
reviewers: [amir]
doc_type: new_system
related:
  - docs/NATIVE_AUTO_LOOPS_FOR_CODEX_AND_CLAUDE_2026-04-19.md
---

# TL;DR

- Outcome: verify that `miniarch-step auto-plan` and `miniarch-step auto-implement` drive the Claude Code Stop hook through research → deep-dive → phase-plan → implement → audit on a trivially disposable target.
- Problem: the native Claude Code auto-loop plumbing for `miniarch-step` has just been wired up and needs a safe end-to-end smoke test against a target that cannot damage live surfaces.
- Approach: pick a target that is obviously throwaway (a single marker file under a fresh `scratch/` directory) so the code-writing pass is trivial; keep the plan canonical enough that the controller actually exercises each stage.
- Plan: one single coherent phase that creates `scratch/hello_smoke_2026-04-19.txt` with a fixed line of text, and adds `scratch/` to `.gitignore` so nothing is committed by accident.
- Non-negotiables: no changes to any live skill, doc, or build surface; no new runtime code paths; only files under `scratch/` and a single `.gitignore` line may change; controller must actually move through every planning stage in separate turns via the installed Stop hook.

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-04-19
recommended_flow: research -> deep dive -> phase plan -> implement
note: This block tracks stage order only. It never overrides readiness blockers caused by unresolved decisions.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

Running `$miniarch-step auto-plan docs/SMOKE_TEST_DISPOSABLE_NATIVE_AUTO_LOOP_2026-04-19.md` followed by `$miniarch-step auto-implement docs/SMOKE_TEST_DISPOSABLE_NATIVE_AUTO_LOOP_2026-04-19.md` in Claude Code ends with:

- this doc fully populated through `# 7)` via the installed Claude Stop hook (one stage per turn).
- a new file `scratch/hello_smoke_2026-04-19.txt` containing exactly one line: `smoke test ok 2026-04-19`.
- one new line in `.gitignore` adding the `scratch/` pattern.
- a clean `audit-implementation` verdict authored by a fresh hook-launched auditor.

## 0.2 In scope

- Creating the disposable marker file under a new `scratch/` directory.
- Adding `scratch/` to `.gitignore`.
- Writing the canonical arch-plan blocks (`research_grounding`, `current_architecture`, `target_architecture`, `call_site_audit`, `phase_plan`) for this smoke target.
- Populating `planning_passes` correctly as stages complete.

## 0.3 Out of scope

- Any change to `skills/`, `Makefile`, `README.md`, or live docs.
- Any change to hook scripts or install behavior.
- Any persistence of the smoke-test marker file in git history.
- Any automation that fires when the smoke test runs.

## 0.4 Definition of done (acceptance evidence)

- `scratch/hello_smoke_2026-04-19.txt` exists and `cat` returns `smoke test ok 2026-04-19` plus a trailing newline.
- `.gitignore` contains a line equal to `scratch/`.
- `git status --short` shows only the expected changes: this doc, the `.gitignore` edit, and the worklog. `scratch/` itself should not appear because it is ignored.
- Section 3, 4, 5, 6, 7 are populated by the hook-driven auto-plan stages, not by a single parent turn.
- `arch_skill:block:implementation_audit` is written by a fresh hook-launched auditor with `Verdict (code): COMPLETE`.

## 0.5 Key invariants (fix immediately if violated)

- No fallbacks or runtime shims.
- Fail-loud boundaries: the controller must either actually advance stages via the Stop hook, or fail loud; no prompt-only same-turn chaining.
- No dual sources of truth: this doc is the only plan doc for the smoke test.
- No touching live skill surfaces; scratch-only file writes during implement.

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)

1. Exercise the full native Claude auto-loop plumbing honestly.
2. Keep blast radius essentially zero (single marker file, one ignored dir).
3. Keep the plan canonical enough that the hook actually has real work to do at each stage.

## 1.2 Constraints

- Target runtime is Claude Code only; Codex path is not in scope for this smoke test.
- Must respect `miniarch-step`'s fresh-audit requirement: the authoritative audit must come from the hook-launched child, not from the parent implementation pass.

## 1.3 Architectural principles (rules we will enforce)

- One canonical plan doc; no sidecars.
- Scratch files live only under `scratch/` which must be gitignored.
- Implementation pass must leave the repo buildable and test-clean (no live surface changes means this is trivially true).

## 1.4 Known tradeoffs (explicit)

- A smoke test with a trivial target under-exercises the deep-dive call-site audit. That is acceptable: the point is plumbing, not planning depth.

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today

- `miniarch-step` auto-plan and auto-implement controllers exist and write state under `.claude/arch_skill/`.
- The Claude Stop hook is installed in `~/.claude/settings.json` and points at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime claude`.

## 2.2 What's broken / missing (concrete)

- Nothing is known to be broken. We simply have no end-to-end smoke-test evidence that the installed Claude auto-loop actually advances stages in practice.

## 2.3 Constraints implied by the problem

- Must run in the live repo without risking live skill/doc surfaces.
- Must be easy to clean up afterwards.

<!-- arch_skill:block:research_grounding:start -->
# 3) Research Grounding (external + internal "ground truth")

## 3.1 External anchors (papers, systems, prior art)

- None required. This is a disposable smoke test against already-installed native auto-loop plumbing; no external system or paper shapes the decision.

## 3.2 Internal ground truth (code as spec)

- Authoritative behavior anchors (do not reinvent):
  - `~/.claude/skills/miniarch-step/references/arch-auto-plan.md` — defines the `auto-plan` controller contract (arm state, run `research` only, hand off to Stop hook).
  - `~/.claude/skills/miniarch-step/references/arch-implement-loop.md` — defines the `implement-loop`/`auto-implement` controller contract (arm state, run implement through the full ordered frontier, hand off to fresh hook-launched audit).
  - `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py` — installed shared Stop-hook runner used by both Codex and Claude Code to read doc truth and feed the next literal command.
  - `~/.claude/settings.json` — repo-managed `Stop` hook entry pointing at the installed runner with `--runtime claude`.
- Canonical path / owner to reuse:
  - `docs/SMOKE_TEST_DISPOSABLE_NATIVE_AUTO_LOOP_2026-04-19.md` — this file is the single canonical plan doc for the smoke test; there is no pre-existing canonical path because the target is disposable.
- Adjacent surfaces tied to the same contract family:
  - `.claude/arch_skill/` — runtime-local armed controller state lives here; must be armed before turn-end for the Stop hook to continue.
  - `.gitignore` — adjacent surface because the scratch directory must be ignored to preserve "disposable" semantics.
- Compatibility posture (separate from `fallback_policy`):
  - Clean cutover. Nothing pre-existing is being preserved because the target (`scratch/hello_smoke_2026-04-19.txt` and the `scratch/` ignore line) does not yet exist.
- Existing patterns to reuse:
  - `skills/miniarch-step/references/arch-auto-plan.md` controller procedure — reuse exactly; do not invent a second planning controller.
  - Canonical full-arch doc shape from `skills/miniarch-step/references/artifact-contract.md` — reuse in full.
- Prompt surfaces / agent contract to reuse:
  - The `miniarch-step` SKILL.md and reference files are the governing prompts; no new prompt engineering is needed for a smoke test.
- Native model or agent capabilities to lean on:
  - Claude Code Stop hook — primary capability under test; this is exactly what the smoke test is validating.
- Existing grounding / tool / file exposure:
  - Claude Code CLI already has Read/Edit/Write/Bash tool access to this repo.
- Duplicate or drifting paths relevant to this change:
  - None. Target is new and disposable.
- Capability-first opportunities before new tooling:
  - None. No new tooling is proposed; the smoke test consumes existing capability.
- Behavior-preservation signals already available:
  - Not applicable; nothing is being refactored.

## 3.3 Decision gaps that must be resolved before implementation

- None. The North Star in Section 0 already fixes the exact file path, the exact line of text, the `.gitignore` entry, and the acceptance evidence. Repo evidence settles every plan-shaping decision for this disposable target.
<!-- arch_skill:block:research_grounding:end -->

# 4) Current Architecture (as-is)

## 4.1 On-disk structure

- _To be filled by `deep-dive`._

## 4.2 Control paths (runtime)

- _To be filled by `deep-dive`._

## 4.3 Object model + key abstractions

- _To be filled by `deep-dive`._

## 4.4 Observability + failure behavior today

- _To be filled by `deep-dive`._

## 4.5 UI surfaces (ASCII mockups, if UI work)

- Not applicable; no UI.

# 5) Target Architecture (to-be)

## 5.1 On-disk structure (future)

- _To be filled by `deep-dive`._

## 5.2 Control paths (future)

- _To be filled by `deep-dive`._

## 5.3 Object model + abstractions (future)

- _To be filled by `deep-dive`._

## 5.4 Invariants and boundaries

- _To be filled by `deep-dive`._

## 5.5 UI surfaces (ASCII mockups, if UI work)

- Not applicable; no UI.

# 6) Call-Site Audit (exhaustive change inventory)

## 6.1 Change map (table)

_To be filled by `deep-dive`._

## 6.2 Migration notes

_To be filled by `deep-dive`._

# 7) Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; split Section 7 into the best sequence of coherent self-contained units, optimizing for phases that are fully understood, credibly testable, compliance-complete, and safe to build on later. If two decompositions are both valid, bias toward more phases than fewer. `Work` explains the unit and is explanatory only for modern docs. `Checklist (must all be done)` is the authoritative must-do list inside the phase. `Exit criteria (all required)` names the exhaustive concrete done conditions the audit must validate. Resolve adjacent-surface dispositions and compatibility posture before writing the checklist. Before a phase is valid, run an obligation sweep and move every required promise from architecture, call-site audit, migration notes, delete lists, verification commitments, docs/comments propagation, approved bridges, and required helper follow-through into `Checklist` or `Exit criteria`. Refactors, consolidations, and shared-path extractions must preserve existing behavior with credible evidence proportional to the risk. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly (delete superseded paths). If a bridge is explicitly approved, timebox it and include removal work; otherwise plan either clean cutover or preservation work directly. Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests and heuristic gates (deletion checks, visual constants, doc-driven gates, keyword or absence gates, repo-shape policing). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).

_To be filled by `phase-plan`._

# 8) Verification Strategy (common-sense; non-blocking)

## 8.1 Unit tests (contracts)

- Not applicable; no runtime code.

## 8.2 Integration tests (flows)

- `cat scratch/hello_smoke_2026-04-19.txt` returns the expected line.
- `grep -Fx 'scratch/' .gitignore` exits 0.

## 8.3 E2E / device tests (realistic)

- Not applicable.

# 9) Rollout / Ops / Telemetry

## 9.1 Rollout plan

- Not applicable; disposable smoke test artifact only.

## 9.2 Telemetry changes

- None.

## 9.3 Operational runbook

- After the smoke test completes, optionally clean up by deleting `scratch/`, removing the added `.gitignore` line, and deleting this doc plus its worklog.

# 10) Decision Log (append-only)

## 2026-04-19 - Use a scratch-only disposable target

- Context: need to smoke-test `miniarch-step auto-plan` and `auto-implement` in Claude Code without risking live surfaces.
- Options:
  - A) Write into an existing skill as a dry-run. Risky, easy to drift live surfaces.
  - B) Write a dedicated scratch file under a gitignored `scratch/` directory. Disposable, zero blast radius.
- Decision: B.
- Consequences: plumbing is exercised end-to-end; the only cleanup is `git clean` + reverting the `.gitignore` line + deleting the plan doc.
- Follow-ups: if this smoke test ends `clean`, we have positive evidence the Claude Stop hook actually drives `miniarch-step` stage-to-stage.
