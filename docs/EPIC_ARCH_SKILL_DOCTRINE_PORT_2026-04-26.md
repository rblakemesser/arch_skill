---
title: Epic - Arch skill Doctrine port and consistency cleanup
date: 2026-04-26
doc_type: epic
status: active
raw_goal: |-
  $arch-epic  new I want a plan to make our entire arch skill directory a) consistent in the way it is installed, references shared files, etc b) uses ../doctrine $doctrine-learn best practices similar to ../lessons_studio and is fully written in doctrine with shared/linked components where we can re-use so everything is consistent and clean (fully written in doctrine not half markdown half doctrine) and c) All redundancy is folded into shaerd components and d) Everything is written per $prompt-authoring and $skill-authoring best practices and e) No nuance is lost, no meaning is lost and the skills all work the same way they are intended to work today. This is a big port, clean up, make consistent, etc. job also our AGENTS.md should explain how we're architedted and require the use of $doctrine-learn $skill-authoring and $prompt-authoring going forward rewritten per $agents-md-authoring before we're done.
raw_goal_sha256: f09079c5fa7fd48cc73d8440c181cd8599edc704f45271a31b2d19b6a3ee0275
sub_plans_approved: true
critic_runtime: codex
critic_model: gpt-5.4
critic_effort: xhigh
models_sha256: f640e873aef32d5c044fc09b3a20c7707736b768875ba4f26bfa364017f733b3
---

# TL;DR

Port the live `arch_skill` skill surface to a Doctrine-authored source model without changing what the installed skills do. The work is split into six sub-plans: first freeze the current behavior and target architecture, then add the Doctrine build/install scaffold, then create shared Doctrine components, then port the skill packages in groups, then rewrite the repo instructions and public install docs around the new architecture, and finally run parity, redundancy, and install verification. This order protects the "no nuance lost" requirement by making the current behavior auditable before the port and by checking emitted/runtime surfaces after each major move. Future fresh-consults, spawned checks, and the epic scope-drift critic all use Codex `gpt-5.4` at `xhigh` per the active arch-loop requirements.

# Decomposition

1. **Freeze current behavior and choose the Doctrine architecture**: Audit the current `skills/`, `Makefile`, `README.md`, `AGENTS.md`, shared references, scripts, and adjacent `../doctrine` plus `../lessons_studio` patterns, then write the canonical target architecture for source prompts, emitted skill packages, shared components, install targets, and parity checks.
   - DOC_PATH: docs/FREEZE_CURRENT_BEHAVIOR_AND_CHOOSE_DOCTRINE_ARCHITECTURE_2026-04-26.md
   - Gate to next: A canonical architecture doc exists that maps every live skill, shared file, script, runtime metadata file, install target, and verification command to its current owner and target Doctrine source owner, with explicit parity requirements for preserving behavior.
   - Status: complete
   - Epic-critic verdict: pass-with-notes via Codex `gpt-5.4` `xhigh` completion consult at `/tmp/fresh-consult/arch-epic-subplan1-completion-rerun2-20260426T132653Z-9g0nR0/`

2. **Add the Doctrine source and emit scaffold without porting the whole suite**: Introduce the repo-level Doctrine dependency/configuration, source tree convention, emit targets, shared prompt-root wiring, lock/source receipt policy, and Makefile commands needed to build Doctrine-authored skills into the existing live `skills/` install surface.
   - DOC_PATH: docs/ADD_DOCTRINE_SOURCE_AND_EMIT_SCAFFOLD_2026-04-26.md
   - Gate to next: A representative Doctrine-authored package and any shared source module compile into the existing runtime layout, install commands still target the live `skills/` surface, and the scaffold has a documented narrow verification path.
   - Status: consistency-pass-complete-awaiting-implementation-authorization
   - Epic-critic verdict: North Star pass-with-notes via Codex `gpt-5.4` `xhigh` fresh consult at `/tmp/fresh-consult/arch-epic-subplan2-north-star-20260426T133843Z-ZM7UJh/`

3. **Create shared Doctrine components for repeated arch-skill law**: Move reusable cross-skill doctrine into shared Doctrine modules and emitted references, including controller lifecycle rules, model/runtime conventions, prompt-authoring quality bars, skill-authoring package rules, install-surface invariants, and any shared AGENTS-facing architecture rules that multiple skills need.
   - DOC_PATH: (not yet set)
   - Gate to next: The shared Doctrine modules compile, are imported by at least one representative skill package, emit self-contained runtime references, and no shipped skill depends on hidden repo docs or archived command files for runtime behavior.
   - Status: pending
   - Epic-critic verdict: -

4. **Port the live skill packages to Doctrine in behavior-preserving groups**: Convert every shipped `skills/<slug>/SKILL.md` package into Doctrine source, keep scripts/assets/runtime metadata intact, re-home duplicated prose into shared components, and verify each emitted package against the pre-port behavior inventory before moving to the next group.
   - DOC_PATH: (not yet set)
   - Gate to next: Every live skill installed from this repo has a Doctrine source owner, every emitted `SKILL.md` and bundled reference is self-contained, duplicated doctrine has a named shared home or an explicit local reason, and parity review finds no lost trigger, workflow, non-negotiable, output, script, or runtime-metadata meaning.
   - Status: pending
   - Epic-critic verdict: -

5. **Rewrite repo instructions and public docs around the new architecture**: Rework `AGENTS.md`, the Claude shim, `README.md`, and related install/usage docs so they explain the Doctrine source architecture, live emitted/runtime surface, install commands, verification commands, and required use of `$doctrine-learn`, `$skill-authoring`, `$prompt-authoring`, and `$agents-md-authoring` for future instruction-bearing work.
   - DOC_PATH: (not yet set)
   - Gate to next: A fresh agent can tell where to edit source, where emitted runtime files land, how to install and verify each supported runtime, and which authoring skills must load for Doctrine, skill, prompt, or AGENTS changes without reading historical backstory.
   - Status: pending
   - Epic-critic verdict: -

6. **Run suite-wide parity, redundancy, and install verification**: Check the full Doctrine-emitted skill tree, shared-component usage, source-to-runtime consistency, install behavior for agents/Codex, Claude Code, and Gemini, and final docs alignment; fix any drift before declaring the port complete.
   - DOC_PATH: (not yet set)
   - Gate to next: (last sub-plan)
   - Status: pending
   - Epic-critic verdict: -

# Orchestration Log

- 2026-04-26 Goal captured. Critic settings resolved from `opus 4.7 xhigh` to `runtime=claude`, `model=claude-opus-4-7`, `effort=xhigh`; sub-plan worker/reviewer preference recorded as Codex `gpt-5.4` `xhigh`. Decomposition drafted (6 sub-plans). Awaiting user approval.
- 2026-04-26 User approved autonomous operation of this epic through `$arch-loop`, `$arch-epic`, `$arch-step`, and `$fresh-consult`. Decomposition approved without changes; epic status set to active.
- 2026-04-26 Sub-plan 1 invoked: `$arch-step new docs/FREEZE_CURRENT_BEHAVIOR_AND_CHOOSE_DOCTRINE_ARCHITECTURE_2026-04-26.md`. Created the canonical draft plan doc and launched Codex `gpt-5.4` `xhigh` fresh consult support at `/tmp/fresh-consult/arch-epic-subplan1-20260426T121854Z/`.
- 2026-04-26 Sub-plan 1 fresh consult returned `pass-with-notes` with no blocking findings; folded no-loss notes into the draft North Star.
- 2026-04-26 Sub-plan 1 North Star approved under the autonomous epic gate. `docs/FREEZE_CURRENT_BEHAVIOR_AND_CHOOSE_DOCTRINE_ARCHITECTURE_2026-04-26.md` is now `status: active`; sub-plan 1 status is `north-star-approved`.
- 2026-04-26 User approved continuing without further pauses. Because `$arch-loop` already occupies the only session controller slot, sub-plan 1 planning is proceeding as arch-loop-managed one-stage-per-pass `$arch-step` work instead of arming a nested `auto-plan` state. Initial research pass completed in the sub-plan DOC_PATH.
- 2026-04-26 Repaired model/runtime drift for future orchestration: fresh-consults, spawned Codex checks, and the epic scope-drift critic now use Codex `gpt-5.4` at `xhigh` per the active arch-loop raw requirements. Historical `raw_goal` text and the initial raw-goal log entry remain unchanged for auditability; `models_sha256` now records `codex|gpt-5.4|xhigh`.
- 2026-04-26 Sub-plan 1 deep-dive pass 1 completed. `docs/FREEZE_CURRENT_BEHAVIOR_AND_CHOOSE_DOCTRINE_ARCHITECTURE_2026-04-26.md` now fills current architecture, runtime control paths, object model, and observability/failure behavior from `skills/`, `Makefile`, `README.md`, `docs/arch_skill_usage_guide.md`, and `skills/arch-step/scripts/arch_controller_stop_hook.py` evidence.
- 2026-04-26 Sub-plan 1 external-research grounding completed. The plan now records Doctrine and `lessons_studio` source evidence for skill-package emits, shared prompt roots, generated root instructions, receipts/locks, verification, and build wiring; Section 3.3 now gives concrete inputs for `deep_dive_pass_2` instead of open-ended decision-gap questions.
- 2026-04-26 Sub-plan 1 deep-dive pass 2 completed. Sections 5 and 6 now choose the Doctrine source/output architecture, root-instruction owner, shared-component boundaries, receipt/lock policy, runtime-matrix preservation, and call-site inventory while leaving Section 7 for the later `phase-plan` pass.
- 2026-04-26 Sub-plan 1 phase-plan completed. Section 7 now gives an eight-phase authoritative depth-first plan covering install-surface guardrails, Doctrine scaffold prerequisites, parity/no-loss transfer, shared components, two package-port groups, root/public docs ownership, and suite-wide receipt/parity/install verification. This was a planning-only pass; no scaffold or package port was implemented.
- 2026-04-26 Sub-plan 1 consistency-pass equivalent completed with repairs. Two Codex `gpt-5.4` `xhigh` explorers found stale planning truth and one real gate gap; the parent pass repaired the `planning_passes` marker, Section 3.3/external-research wording, the missing live package/source-owner matrix, the shared/support surface matrix, concrete Phase 2 representative/helper choices, no-lock and remote-install proof obligations, and the stale Section 7 decision-log consequence. Sub-plan 1 is now awaiting the Codex `gpt-5.4` `xhigh` completion consult or epic critic; sub-plan 2 has not started.
- 2026-04-26 Sub-plan 1 Codex `gpt-5.4` `xhigh` completion consult run `/tmp/fresh-consult/arch-epic-subplan1-completion-20260426T131145Z-pwMkGt/` returned `fail`. Blocking findings were stale current-state truth in Section 4.2: `remote_install` was overstated as remote-checkout plus remote verification, and Gemini was overstated as excluding all hook-backed controller packages. Repaired both baseline-truth errors in the sub-plan doc; rerun required before sub-plan 1 can complete.
- 2026-04-26 Sub-plan 1 Codex `gpt-5.4` `xhigh` completion consult rerun `/tmp/fresh-consult/arch-epic-subplan1-completion-rerun-20260426T131907Z-3fDeiW/` returned `fail`. The original blockers were repaired, but the rerun found stale Gemini shorthand in Section 7 and stale current-state truth about `AGENTS.md` already requiring `$doctrine-learn`/`$prompt-authoring`. Repaired those statements; another rerun is required before sub-plan 1 can complete.
- 2026-04-26 Sub-plan 1 Codex `gpt-5.4` `xhigh` completion consult rerun `/tmp/fresh-consult/arch-epic-subplan1-completion-rerun2-20260426T132653Z-9g0nR0/` returned `pass-with-notes` with no blocking findings. The remaining notes are deferred docs-inventory drift in `docs/arch_skill_usage_guide.md` and the already-repaired Doctrine reference shorthand. Sub-plan 1 is complete.
- 2026-04-26 Sub-plan 2 began with canonical arch-step DOC_PATH `docs/ADD_DOCTRINE_SOURCE_AND_EMIT_SCAFFOLD_2026-04-26.md`. The new doc is a draft North Star seed only; later arch-loop passes must handle the North Star gate and planning passes before implementation.
- 2026-04-26 Sub-plan 2 North Star gate ran through Codex `gpt-5.4` `xhigh` fresh consult at `/tmp/fresh-consult/arch-epic-subplan2-north-star-20260426T133843Z-ZM7UJh/` and returned `pass-with-notes` with no blockers. The parent pass activated the DOC_PATH, folded both notes, and completed deep-dive pass 1 by filling current architecture from `Makefile`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `skills/`, `../doctrine`, and `../lessons_studio`.
- 2026-04-26 Sub-plan 2 external-research grounding and deep-dive pass 2 completed. `docs/ADD_DOCTRINE_SOURCE_AND_EMIT_SCAFFOLD_2026-04-26.md` now records concrete evidence from sub-plan 1 Sections 5-7, `../doctrine`, and `../lessons_studio`; Sections 5 and 6 choose the scaffold target architecture and call-site audit while keeping implementation unauthorized until phase-plan and consistency gates pass.
- 2026-04-26 Sub-plan 2 phase-plan completed. Section 7 now gives a six-phase depth-first implementation plan covering install-surface guardrails, Doctrine config and target discovery, minimum source scaffold authoring, emit/receipt/parity proof before sync, approved runtime/root sync plus minimal docs, and the Codex `gpt-5.4` `xhigh` completion consult/critic gate. This was a planning-only pass; implementation remains unauthorized until later gates clear it.
- 2026-04-26 Sub-plan 2 consistency-pass equivalent completed with repairs. One Codex `gpt-5.4` `xhigh` explorer found a blocking execution-order drift between the planning helper and Section 7; the parent pass repaired it by distinguishing the pre-implementation `implementation_authorization_consult` from the Phase 6 `completion_consult`, strengthened Section 8 parity proof language, and repaired `doc_type`. Sub-plan 2 is now awaiting the required Codex `gpt-5.4` `xhigh` implementation authorization consult/critic; Phase 1 has not started.
- 2026-04-26 Sub-plan 2 Codex `gpt-5.4` `xhigh` implementation authorization consult at `/tmp/fresh-consult/arch-epic-subplan2-implementation-authorization-20260426TXXXXXX-rhHum6/` returned `fail`. Blocking findings were stale Section 7 gate wording, a root-doc alternate-entrypoint branch, and non-canonical shared-runtime receipt/proof branching. The parent pass repaired all three; rerun required before Phase 1 can start.

# Decision Log

- 2026-04-26 User approved the six-sub-plan decomposition and requested autonomous end-to-end orchestration. Execution should use Codex `gpt-5.4` `xhigh` for fresh consults and spawned Codex checks where the governing skill permits subprocesses. `$arch-epic` and `$arch-step` controller transitions still follow their session-scoped hook contracts; arch-step sub-plan controllers are not moved into parallel `codex exec` subprocesses.
- 2026-04-26 The sub-plan 1 North Star gate is satisfied by the user's autonomous approval plus the Codex `gpt-5.4` `xhigh` fresh consult verdict of `pass-with-notes` with no blockers. The useful consult notes were folded into the sub-plan before activation.
- 2026-04-26 User approved continuing through controller friction. To avoid the installed Stop-hook conflict gate for multiple session controller states, this epic may run the `auto-plan` stages for sub-plan 1 as explicit arch-loop-managed parent passes against the same DOC_PATH: research, deep-dive pass 1, deep-dive pass 2, phase-plan, then consistency-pass. Do not create a nested `.codex/auto-plan-state.019dc9ab-bcea-7e92-8e64-89a72c56ebe6.json` while `.codex/arch-loop-state.019dc9ab-bcea-7e92-8e64-89a72c56ebe6.json` is armed.
- 2026-04-26 Active arch-loop raw requirements supersede the initial critic preference for all future orchestration checks. The historical `raw_goal` stays as captured, but future fresh-consults, spawned checks, and epic scope-drift critic runs must use Codex `gpt-5.4` `xhigh` unless the user gives a newer explicit model/runtime instruction.
- 2026-04-26 Sub-plan 1 may not advance to sub-plan 2 on consistency-pass alone. The next required gate is a Codex `gpt-5.4` `xhigh` completion consult or epic critic against `docs/FREEZE_CURRENT_BEHAVIOR_AND_CHOOSE_DOCTRINE_ARCHITECTURE_2026-04-26.md`; only a no-blocker verdict can make sub-plan 1 complete.
- 2026-04-26 Sub-plan 1 completion consult passed with notes at `/tmp/fresh-consult/arch-epic-subplan1-completion-rerun2-20260426T132653Z-9g0nR0/`. Because no blocking findings remain, sub-plan 1 is complete and sub-plan 2 may begin. The sub-plan 2 DOC_PATH is `docs/ADD_DOCTRINE_SOURCE_AND_EMIT_SCAFFOLD_2026-04-26.md`; its initial state is draft-created, not North-Star-approved.
- 2026-04-26 Sub-plan 2 North Star gate is satisfied by the user's autonomous approval plus Codex `gpt-5.4` `xhigh` fresh consult verdict `pass-with-notes` at `/tmp/fresh-consult/arch-epic-subplan2-north-star-20260426T133843Z-ZM7UJh/`. No blocking findings remain, so `docs/ADD_DOCTRINE_SOURCE_AND_EMIT_SCAFFOLD_2026-04-26.md` is active for planning. Implementation remains blocked until later planning passes and completion consult/critic gates pass.
