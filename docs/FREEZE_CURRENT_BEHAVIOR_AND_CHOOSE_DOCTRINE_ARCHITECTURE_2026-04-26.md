---
title: "Arch Skill - Behavior Freeze and Doctrine Architecture - Architecture Plan"
date: 2026-04-26
status: active
fallback_policy: forbidden
owners: [aelaguiz]
reviewers: [fresh-consult, arch-epic]
doc_type: parity_plan
related:
  - docs/EPIC_ARCH_SKILL_DOCTRINE_PORT_2026-04-26.md
  - AGENTS.md
  - README.md
  - Makefile
  - docs/arch_skill_usage_guide.md
  - ../doctrine
  - ../lessons_studio
---

# TL;DR

- **Outcome:** Create the canonical behavior-freeze and target-architecture plan for porting `arch_skill` to Doctrine without changing installed skill behavior.
- **Problem:** The repo currently ships live hand-authored skill packages under `skills/`, install behavior in `Makefile`, public inventory in `README.md`, and repo rules in `AGENTS.md`; porting those surfaces without a current inventory and target source architecture would make it too easy to drop triggers, workflow rules, shared references, scripts, runtime metadata, or install semantics.
- **Approach:** Audit current runtime skill packages, shared files, scripts, docs, and install paths; compare them to `../doctrine` and `../lessons_studio`; then choose a Doctrine source, emit, shared-component, and verification architecture that later sub-plans can implement.
- **Plan:** First freeze current behavior and install truth, then define target Doctrine source ownership, then map every live package and shared component to its future source owner, then name the preservation and verification evidence later sub-plans must satisfy.
- **Non-negotiables:** This sub-plan is docs/planning only; no skill is ported here, no install behavior changes here, no runtime behavior changes here, and no instruction-bearing nuance may be summarized away without a recoverable source and an explicit reason.

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-04-26
external_research_grounding: done 2026-04-26
deep_dive_pass_2: done 2026-04-26
phase_plan: done 2026-04-26
consistency_pass: done 2026-04-26
completion_consult: pass-with-notes 2026-04-26
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> consistency pass -> completion consult or epic critic -> next sub-plan
note: This block tracks stage order only. It never overrides readiness blockers caused by unresolved decisions or the epic critic gate.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

When this sub-plan is complete, `docs/FREEZE_CURRENT_BEHAVIOR_AND_CHOOSE_DOCTRINE_ARCHITECTURE_2026-04-26.md` will be the decision-complete architecture source for the rest of the epic. A later agent should be able to read this one doc and know, for every current live skill and install/support surface, what behavior must be preserved, where the Doctrine source should live, which shared component owns repeated doctrine, what gets emitted into `skills/`, and which verification command proves the next change did not drift.

## 0.2 In scope

- Inventory the live runtime surface under `skills/`, including each `SKILL.md`, `references/`, `scripts/`, `assets/` if present, and `agents/openai.yaml`.
- Inventory shared runtime files such as `skills/_shared/controller-contract.md` and the hook/controller scripts that shipped skills reference.
- Inventory install and verification behavior in `Makefile`, `README.md`, `CLAUDE.md`, and `AGENTS.md`.
- Inventory runtime-specific install behavior, including per-runtime skill matrices, `_shared` copy-through, Gemini frontmatter stripping, Codex mirror removal, archived prompt backup cleanup, hook wiring, `codex_hooks` gating, `remote_install`, and `make verify_install` parity.
- Compare the current repo to `../doctrine` authoring rules and the `../lessons_studio` Doctrine skill-source pattern.
- Choose the target source architecture for Doctrine `.prompt` files, shared prompt roots, emitted runtime package layout, source receipts or locks, install targets, and verification flow.
- Choose the source ownership model for root instructions: whether `AGENTS.md` and `CLAUDE.md` stay hand-authored or become Doctrine-emitted, and which Doctrine surface owns them if generated.
- Define the behavior-preservation matrix that later sub-plans must satisfy before they port, emit, install, or delete anything.
- Apply `$doctrine-learn`, `$skill-authoring`, `$prompt-authoring`, and `$agents-md-authoring` quality bars to the architecture and future work gates.

## 0.3 Out of scope

- Porting any live skill package to Doctrine.
- Adding Doctrine dependencies, emit targets, lock files, generated outputs, or build/install commands.
- Editing runtime behavior, hook behavior, controller scripts, install paths, or shipped skill semantics.
- Deleting archived command surfaces, stale docs, or redundant skill prose.
- Changing the public skill inventory, supported runtime matrix, or install contract.
- Rewriting `AGENTS.md`, `README.md`, or `CLAUDE.md` beyond planning notes inside this doc.

## 0.4 Definition of done (acceptance evidence)

- The current-state inventory names every live skill package in `Makefile`/`README.md`, every shared directory installed beside skills, every script-bearing skill, every runtime metadata file, and every install/verify command that must be preserved.
- The install inventory freezes runtime-specific behavior: active skill matrices for agents/Codex, Claude Code, and Gemini; Gemini frontmatter stripping; `_shared` directory installation; stale mirror and archived prompt cleanup; hook wiring; feature-gate docs; remote install behavior; and verify targets.
- The target architecture chooses one source owner model for Doctrine-authored skills, shared prompt roots, emitted runtime packages, hand-kept scripts/assets, generated docs, root instructions, and install docs.
- The target architecture explicitly decides root-instruction ownership for `AGENTS.md` and `CLAUDE.md`.
- The migration/parity matrix maps each live skill and shared file to a future Doctrine source owner or a justified non-Doctrine owner.
- The no-loss parity matrix treats trigger and runtime metadata as first-class: frontmatter `description`, nearest-peer boundaries, `when_to_use`, `when_not_to_use`, `agents/openai.yaml`, script presence/absence, schemas, and intentionally absent metadata.
- The architecture names exact verification commands for docs-only changes, skill source changes, emitted runtime changes, install behavior changes, and full install verification.
- The plan records a no-loss review method for preserving frontmatter descriptions, when-to-use boundaries, non-negotiables, first moves, workflows, output contracts, references, scripts, runtime metadata, and install semantics.
- Structure-preserving transfer is explicit for instruction-bearing content: ordered steps, hard negatives, escalation rules, hook ownership, manual recovery flows, and examples that constrain behavior must survive or remain recoverable.
- A Codex `gpt-5.4` `xhigh` fresh consult has reviewed the sub-plan seed or resulting architecture for missing no-loss constraints; blocking findings and useful non-blocking no-loss constraints are folded into this doc before implementation begins.

## 0.5 Key invariants (fix immediately if violated)

- `skills/` remains the live runtime install surface until a later approved sub-plan changes the source/build pipeline.
- Existing skill behavior, trigger intent, workflow order, hard negatives, references, scripts, and metadata are preservation targets, not raw material to simplify.
- Runtime-specific install details are preservation targets, including omissions, transformations, cleanup behavior, hooks, and recovery commands.
- Trigger descriptions and runtime metadata are part of behavior, not decorative packaging.
- Instruction-bearing content must transfer structure-preservingly unless the plan records why condensation is safe and where the source remains recoverable.
- Doctrine source should make shared truth cheaper and clearer; it must not make shipped skills depend on hidden repo context at runtime.
- Exact truth should move into typed Doctrine surfaces where Doctrine supports it; judgment and explanation should remain readable, plain-English prose.
- Install behavior stays owned by `Makefile` and documented in `README.md`.
- Repo instruction behavior stays owned by `AGENTS.md` and `CLAUDE.md`.
- Runtime fallbacks, transitional shims, and dual live sources are forbidden unless a later user-approved Decision Log entry timeboxes and removes them.

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)

1. Preserve existing shipped behavior and installed-surface semantics.
2. Make future source ownership unambiguous: Doctrine source, emitted runtime files, hand-kept scripts/assets, and docs must each have one owner.
3. Fold real repeated doctrine into shared components without hiding local skill boundaries.
4. Keep emitted runtime packages self-contained for Codex, Claude Code, and Gemini.
5. Keep verification narrow, current, and runnable for each changed surface.

## 1.2 Constraints

- This repo already has a live install surface consumed from `skills/`; the architecture must preserve that runtime contract while introducing Doctrine source ownership.
- `Makefile` currently controls active skill lists, shared directories, hook install, stale-surface cleanup, remote install, and verification.
- `README.md` is the public install and inventory truth; it must not drift from `Makefile`.
- `AGENTS.md` is always-on agent guidance and should stay compact; deeper architecture detail belongs in docs or skills.
- Some skill packages ship deterministic scripts and JSON schemas; those files are runtime package assets, not prose to rewrite.
- Some skills intentionally ship runtime metadata and some do not; both presence and absence are part of the parity inventory.
- `AGENTS.md` and `CLAUDE.md` must get an explicit source-owner decision before any later rewrite claims to finish the architecture.

## 1.3 Architectural principles (rules we will enforce)

- Source truth has one owner per surface.
- Emitted runtime truth is generated or copied intentionally; do not hand-edit emitted files once a source owner exists.
- Shared doctrine is imported or emitted from a named shared component; do not copy the same reusable law across many skills.
- Runtime packages must stay self-contained after install.
- Verification follows changed surface: docs-only checks for docs-only work, `npx skills check` for skill package changes, and `make verify_install` for install behavior changes or intentional install validation.

## 1.4 Known tradeoffs (explicit)

- A faithful port may initially preserve more local wording than a fresh Doctrine rewrite would choose. That is acceptable; lossless migration comes before style compression.
- Shared components reduce duplication but can overcentralize. The architecture must distinguish true cross-skill law from local skill judgment.
- Generated source architecture adds build steps. The later scaffold sub-plan must make those commands obvious and cheap enough to run.

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today

`arch_skill` ships installable agent skills directly from `skills/`. `Makefile` copies those packages into `~/.agents/skills`, `~/.claude/skills`, and `~/.gemini/skills`, with runtime-specific omissions and hook wiring. `README.md` describes the install surface and current skill inventory. Current `AGENTS.md` routes skill package work to `$skill-authoring`, `AGENTS.md` work to `$agents-md-authoring`, and workflow execution to the matching shipped skills; it does not yet require `$doctrine-learn` or `$prompt-authoring` for future Doctrine/prompt-source work. That requirement is part of this epic's target architecture and later root-instruction rewrite.

## 2.2 What's broken / missing (concrete)

- The repo lacks a canonical source architecture for converting the whole skill directory to Doctrine.
- Repeated doctrine already exists across skill packages and references, but only some shared runtime files are centralized.
- Before this sub-plan, future agents did not have one parity matrix that said what must be preserved for every skill before and after emitting from Doctrine.
- The install and docs surfaces are mature enough that an unplanned port could accidentally change runtime behavior.

## 2.3 Constraints implied by the problem

- The first move must be an inventory and architecture decision, not a mass port.
- The target architecture must preserve install behavior and runtime self-containment.
- No later sub-plan should be allowed to claim success without comparing emitted outputs against this behavior freeze.

# 3) Research Grounding (external + internal "ground truth")

<!-- arch_skill:block:research_grounding:start -->
## 3.1 External anchors (papers, systems, prior art)

- `../doctrine/skills/doctrine-learn/prompts/refs/principles.prompt` — adopt. Doctrine is the authoring layer, not the runtime harness; always-on context is a budget; repeated truth should move into named reusable declarations; exact truth belongs in typed surfaces; shipped prose should stay plain.
- `../doctrine/skills/doctrine-learn/prompts/refs/skills_and_packages.prompt` — adopt. `skill package` with `SKILL.prompt` is the source model for real emitted packages; ordinary bundled files copy byte-for-byte; `agents/openai.yaml` is runtime metadata; `emit:` owns generated Markdown companions; `SKILL.source.json` is the build receipt.
- `../doctrine/skills/doctrine-learn/prompts/refs/emit_targets.prompt` — adopt. Doctrine emit targets live in `[tool.doctrine.emit]`; emitted Markdown is runtime output and should not be hand-edited once a source owner exists; external source targets can write `SKILL.source.json` and `doctrine.skill.lock` receipts.
- `../doctrine/skills/doctrine-learn/prompts/refs/imports_and_refs.prompt` — adopt. Shared Doctrine truth should use imports, typed refs, and configured prompt roots instead of quoted-name duplication. Additional prompt roots are allowed, collisions fail loud, and runtime agent packages (`AGENTS.prompt` emitting `AGENTS.md`) are separate from skill packages (`SKILL.prompt` emitting `SKILL.md`).
- `../doctrine/skills/doctrine-learn/prompts/refs/verify_and_ship.prompt` — adopt. Verification must match the changed surface; generated Markdown, `SKILL.source.json`, `SKILL.contract.json`, schemas, and final-output contract files are emitted artifacts and must not be hand-edited.
- `../lessons_studio/README.md` and `../lessons_studio/pyproject.toml` — adopt the broad shape, not the domain. It keeps skill source under `skills/<name>/prompts/SKILL.prompt`, emits via configured `doctrine.emit_skill` targets, uses `doctrine.skill.lock` for source receipts, and builds generated root instruction files from `prompts/claude_home/`.
- `../lessons_studio/Makefile`, `../lessons_studio/scripts/list_doctrine_skill_targets.py`, and `../lessons_studio/scripts/build_skills.sh` — adopt the operational lesson that one command should derive skill emit targets from `pyproject.toml`, clear stale build outputs, emit all configured skill targets, verify receipts, and wire runtime install roots. This repo's equivalent must still preserve its Codex, Claude Code, Gemini, hook, and stale-surface cleanup semantics instead of replacing them with local symlinks.
- `../lessons_studio/prompts/claude_home/SKILL.prompt` — adopt with adaptation. It proves root instruction files can be generated from Doctrine source with `emit:` companions, but this repo should preserve the current `CLAUDE.md` shim semantics unless deep-dive pass 2 records a better generated-shim owner.
- `skills/skill-authoring/references/skill-pattern-contract.md` — adopt. Trigger descriptions are runtime behavior, `SKILL.md` should stay lean, heavy doctrine belongs in `references/`, runtime-specific metadata belongs in machine-readable files, scripts are package assets only when earned, and every package must be self-contained.
- `skills/prompt-authoring/references/prompt-pattern-contract.md` — adopt. Refactors must preserve useful prompt behavior by moving it to the right section, not flattening it into slogans or heuristic lists.
- `skills/agents-md-authoring/references/agents-md-pattern-contract.md` — adopt. Root instruction files are always-on budget; they should contain non-inferable repo truth, exact commands, blocked-state rules, and a compact docs map, not historical backstory or architecture dumps.

## 3.2 Internal ground truth (code as spec)

- Authoritative behavior anchors:
  - `skills/` — the live runtime package surface today. It contains 28 active skill packages, one shared runtime directory (`_shared`), 23 `agents/openai.yaml` metadata files, no `assets/` files found in the current tree, and script-bearing packages for `arch-step`, `arch-epic`, `code-review`, `skill-flow`, and `stepwise`.
  - `skills/_shared/controller-contract.md` — shared runtime doctrine copied beside installed skills. It is referenced by controller skills and must remain self-contained at runtime.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` — shared Stop-hook dispatcher and controller registry. It owns the session-scoped controller conflict gate, staleness sweep, and hook-backed dispatch behavior for the suite.
  - `Makefile` — authoritative install and verification behavior. `SKILLS` and `CLAUDE_SKILLS` each contain 28 packages. `GEMINI_SKILLS` contains 24 packages and intentionally omits `arch-loop`, `delay-poll`, `wait`, and `code-review`.
  - `Makefile` — copies `_shared` into every install root; strips YAML frontmatter from Gemini `SKILL.md`; removes old `~/.codex/skills/<skill>` mirrors; backs up archived prompt-era command files for Codex, Claude Code, and Gemini; installs Codex and Claude hooks; owns `remote_install`.
  - `Makefile` — `verify_install` expands to agents/Codex, Claude Code, hook-runner, and Gemini checks unless `NO_GEMINI=1`; `npx skills check` is the package validation command required by `AGENTS.md` after `skills/` package changes.
  - `README.md` — public install, runtime matrix, skill inventory, feature-gate, manual recovery, and verification truth.
  - `docs/arch_skill_usage_guide.md` — secondary usage and routing guide. It duplicates install/inventory truth and already needs final-docs alignment with `README.md` after the Doctrine architecture lands.
  - `AGENTS.md` — current repo instructions. It already says `skills/` is the live runtime surface, `Makefile` plus `README.md` own install behavior, uses `$skill-authoring` for skill package work, uses `$agents-md-authoring` for `AGENTS.md` work, and routes workflow execution to the matching shipped skills. It does not yet require `$doctrine-learn` or `$prompt-authoring` for future Doctrine/prompt-source work; the generated root-instruction target must add that.
  - `CLAUDE.md` — thin shim that points Claude Code to `AGENTS.md`; it intentionally does not duplicate repo rules.
- Canonical path / owner to reuse:
  - Runtime install surface stays `skills/<slug>/` until a later approved sub-plan changes the source/build pipeline.
  - Install behavior stays in `Makefile`; public install and supported-runtime behavior stay in `README.md`.
  - Root repo instructions stay in `AGENTS.md` with `CLAUDE.md` as the shim unless this plan explicitly chooses a Doctrine-generated root-instruction source.
  - Controller runtime behavior stays in `skills/arch-step/scripts/arch_controller_stop_hook.py` and `skills/_shared/controller-contract.md`; Doctrine may author the prose package, but it must not move runtime state or scheduling policy into prompt text.
- Adjacent surfaces tied to the same contract family:
  - `README.md`, `docs/arch_skill_usage_guide.md`, `Makefile`, and `AGENTS.md` all describe the install/routing surface and must be treated as one contract family during the final docs rewrite.
  - `skills/*/SKILL.md` frontmatter `description`, `agents/openai.yaml`, missing `agents/openai.yaml`, `references/`, `scripts/`, and any JSON schemas are behavior-preservation surfaces, not packaging noise.
  - `ARCHIVED_COMMAND_FILES` in `Makefile` is part of install behavior. The Doctrine port must not revive archived prompt-era command files or make shipped skills depend on them.
  - The ignored controller state roots (`.codex/*-state*.json`, `.claude/arch_skill/`) are runtime state, not Doctrine source.
- Compatibility posture (separate from `fallback_policy`):
  - Preserve the existing install and invocation contract while the port is in progress. The safe migration posture is source-first with emitted outputs checked against the frozen runtime surface, then a clean cutover for each group when parity is proven.
  - Runtime shims or dual live sources are not allowed by default. Any bridge must be explicitly timeboxed and logged before use.
- Existing patterns to reuse:
  - `../lessons_studio` source pattern: `skills/<name>/prompts/SKILL.prompt` as package source, configured emit targets, generated `SKILL.source.json`, lock-file verification for external source roots, and a single build command.
  - Doctrine package pattern: `emit:` generated references for shared prose, ordinary bundled files copied byte-for-byte for scripts/YAML/assets, and source receipts for source-to-runtime traceability.
  - Current `arch_skill` install pattern: `Makefile` controls runtime-specific lists and transformations; verification is split by affected surface.
- Prompt surfaces / agent contract to reuse:
  - `skills/skill-authoring/SKILL.md` and its references own skill package quality, trigger boundaries, runtime metadata, packaging, and validation.
  - `skills/prompt-authoring/SKILL.md` and its references own prompt refactor fidelity, section placement, anti-heuristic repair, and no hidden context.
  - `skills/agents-md-authoring/SKILL.md` and its references own root instruction files, command-first repo truth, scope layering, and budget discipline.
  - `../doctrine/skills/doctrine-learn/prompts/SKILL.prompt` owns the Doctrine teaching contract and reference map for skills/packages, emits, imports, typed truth, and verification.
- Native model or agent capabilities to lean on:
  - Codex and Claude Code can load local files, run repo searches, and execute the installed hook-backed controllers; Gemini receives installed skills but not hook-backed auto-controller behavior.
  - Fresh consults and critics should remain explicit child processes with hook suppression and disk-grounded prompts; they should not become hidden Doctrine runtime behavior.
- Existing grounding / tool / file exposure:
  - `rg --files skills` gives the current package inventory.
  - `Makefile` variables give the per-runtime install matrices.
  - `README.md` and `docs/arch_skill_usage_guide.md` give public routing and install claims.
  - `npx skills check`, `make verify_install`, and the specific `verify_*` targets are the existing verification levers.
- Duplicate or drifting paths relevant to this change:
  - Public skill inventory exists in both `README.md` and `docs/arch_skill_usage_guide.md`; those must converge when the architecture changes.
  - Controller doctrine appears both in shipped skill references and in runtime scripts. Shared doctrine should move into reusable Doctrine components, but runtime policy stays in the script/shared runtime contract.
  - No `pyproject.toml`, `doctrine.skill.lock`, `prompts/SKILL.prompt`, or `SKILL.source.json` exists in this repo today; the port must introduce source/receipt infrastructure before claiming any package is Doctrine-owned.
- Capability-first opportunities before new tooling:
  - Use Doctrine `skill package`, `emit:`, bundled-file copy-through, source receipts, additional prompt roots, and configured emit targets before adding custom generators.
  - Use existing install verification and `npx skills check` before creating new package-audit scripts.
  - Use structure-preserving prompt/source review before inventing line-by-line semantic diff tooling.
- Behavior-preservation signals already available:
  - `npx skills check` after runtime package changes.
  - `make verify_install` when install behavior changes or installed-surface validation is intentionally requested.
  - `make verify_agents_install`, `make verify_claude_install`, `make verify_gemini_install`, and `make verify_hook_runner` for targeted install-surface checks.
  - Direct re-read plus `rg` path/command checks for docs-only changes under current repo rules.

## 3.3 Deep-dive pass 2 inputs and disposition

The external-research pass turned the earlier branchy questions into concrete inputs. Deep-dive pass 2 consumed those inputs into Sections 5 and 6; this subsection remains as provenance for the decisions, not as unfinished work.

- Source tree shape — evidence checked: Doctrine `skill package` requires `SKILL.prompt` under a package source root; `../lessons_studio` uses `skills/<name>/prompts/SKILL.prompt`; this repo currently keeps live runtime files at `skills/<slug>/`. Disposition: Section 5 chooses `skills/<slug>/prompts/SKILL.prompt` as the first-party source path, emits to disposable `skills/<slug>/build/`, then syncs parity-approved runtime output into live `skills/<slug>/` while preserving `Makefile` install semantics.
- Root instruction ownership — evidence checked: Doctrine can emit root instruction documents from a dedicated package (`../lessons_studio/prompts/claude_home/SKILL.prompt`), while this repo currently keeps `AGENTS.md` as compact repo truth and `CLAUDE.md` as a thin shim. Disposition: Section 5 chooses `prompts/repo_home/SKILL.prompt` as the Doctrine source owner for generated `AGENTS.md` and a thin `CLAUDE.md` shim that still satisfies `$agents-md-authoring`: compact always-on truth, exact commands, scope layering, and no historical backstory.
- Shared component boundary — evidence checked: Doctrine supports shared declarations through imports and additional prompt roots; this repo already has runtime-shared `skills/_shared/controller-contract.md`, and repeated law appears across controller, authoring, install, and model-runtime skill prose. Disposition: Sections 5 and 6 classify shared Doctrine source into controller lifecycle, authoring quality bars, install/runtime invariants, and model/fresh-consult conventions. Runtime policy remains in `arch_controller_stop_hook.py` and installed `_shared` references; Doctrine source may author emitted references but must not move scheduling, state, hook verification, or subprocess dispatch into prompt prose.
- Receipt and lock policy — evidence checked: Doctrine emits `SKILL.source.json` for every skill package; `doctrine.skill.lock` is used when an emit target has an external `source_root`; this repo currently has no Doctrine source or receipts. Disposition: Section 5 requires `SKILL.source.json` for every Doctrine-emitted skill package, forbids a repo-level `doctrine.skill.lock` for first-party local sources, and allows a lock only if a later sub-plan intentionally uses external `source_root` targets outside emitted runtime skill trees.
- Runtime matrix preservation — evidence checked: `Makefile` installs 28 agents/Codex skills, 28 Claude Code skills, and 24 Gemini skills; Gemini omits `arch-loop`, `delay-poll`, `wait`, and `code-review` and strips frontmatter. Disposition: Sections 5 and 6 preserve these matrices, omissions, and the Gemini frontmatter transform exactly until a later explicit Decision Log entry changes them. Emitted Doctrine packages feed the same matrices without making Gemini load hook-backed controllers.
<!-- arch_skill:block:research_grounding:end -->

<!-- arch_skill:block:external_research:start -->
# External Research (best-in-class references; plan-adjacent)

> Goal: anchor the plan in idiomatic, broadly accepted practices where applicable. This section intentionally avoids project-specific internals except for adjacent source repos that are primary evidence for this port.

## Topics researched (and why)

- Doctrine skill-package emit model — this plan ports runtime skill packages to Doctrine and must not confuse source files with installed runtime artifacts.
- Shared prompt roots and imports — this plan must fold repeated doctrine into shared components without copying hidden context into every skill.
- Root instruction generation — this plan must decide whether `AGENTS.md` and `CLAUDE.md` stay hand-authored or become Doctrine-emitted.
- Receipts, locks, and verification — this plan must preserve behavior and prove emitted outputs did not drift.
- `lessons_studio` repo pattern — this is the closest local Doctrine skill-suite precedent.

## Findings + how we apply them

### Doctrine skill-package emit model

- Best practices synthesized:
  - `SKILL.prompt` is the source for a real skill package; `SKILL.md` is emitted runtime output.
  - Ordinary bundled files such as `references/*.md`, `scripts/*.py`, `assets/*`, and `agents/openai.yaml` copy through byte-for-byte unless authored through an explicit `emit:` companion.
  - Generated artifacts such as `SKILL.source.json` and `SKILL.contract.json` are compiler-owned and must not be hand-edited.
- Adopt for this plan:
  - Treat each current `skills/<slug>/SKILL.md` as behavior to freeze and port, not as the long-term source once a Doctrine owner exists.
  - Preserve script paths, fixtures, `agents/openai.yaml`, and intentionally absent metadata as parity surfaces.
  - Use `emit:` only when a companion reference should be Doctrine-authored instead of copied.
- Reject for this plan:
  - Do not put hook state, scheduling, subprocess invocation, install cleanup, or runtime adapter behavior into Doctrine source.
  - Do not hand-edit emitted runtime Markdown after a source owner exists.
- Pitfalls / footguns:
  - A package can become "Doctrine-authored" in name only if scripts, runtime metadata, or bundled references are copied without a receipt or parity check.
  - Condensing `SKILL.md` into terse Doctrine prose can silently lose triggers, hard negatives, examples, and workflow order.
- Sources:
  - `../doctrine/skills/doctrine-learn/prompts/refs/skills_and_packages.prompt` — authoritative Doctrine package surface, bundle behavior, metadata, `emit:`, receipts, and host binding.
  - `../doctrine/skills/doctrine-learn/prompts/refs/emit_targets.prompt` — authoritative emit-target and generated-artifact behavior.

### Shared prompt roots and imports

- Best practices synthesized:
  - Repeated truth belongs in named declarations and imports, not pasted prose.
  - `additional_prompt_roots` supports shared source roots, and duplicate module resolution fails loud.
  - Typed refs are preferred over quoted names because the compiler can check them.
- Adopt for this plan:
  - Use a repo-local shared Doctrine prompt root for repeated arch-suite law.
  - Keep shared runtime references self-contained by emitting or copying the resulting Markdown into installed skill packages or `skills/_shared`.
  - Let pass 2 classify repeated law before creating shared components: controller lifecycle, install invariants, model/runtime conventions, and authoring quality bars.
- Reject for this plan:
  - Do not create a hidden Doctrine-only context that shipped skills depend on but installed runtimes cannot read.
  - Do not use ad hoc string references to shared component names where Doctrine refs can carry the identity.
- Pitfalls / footguns:
  - Over-centralizing local judgment into shared law can blur skill boundaries. Shared components should own only cross-skill invariants.
  - Prompt-root collisions should fail loud; avoiding that by renaming casually would make ownership harder to audit.
- Sources:
  - `../doctrine/skills/doctrine-learn/prompts/refs/principles.prompt` — context-budget, reuse, typed-truth, and thin-harness rules.
  - `../doctrine/skills/doctrine-learn/prompts/refs/imports_and_refs.prompt` — imports, typed refs, multi-root resolution, and collision behavior.
  - `../lessons_studio/pyproject.toml` — concrete `additional_prompt_roots = ["shared/prompts", "psmobile/skills/shared/prompts"]` precedent.

### Root instruction generation

- Best practices synthesized:
  - Root instruction files are always-on context and should stay compact.
  - Doctrine can generate root docs, but the emitted files are runtime artifacts and should be regenerated from source.
  - The repo-specific shape still matters; generated `CLAUDE.md` does not have to duplicate `AGENTS.md` if this repo's owner model says it should remain a shim.
- Adopt for this plan:
  - Deep-dive pass 2 should choose one Doctrine source owner for `AGENTS.md` and the `CLAUDE.md` shim or record a narrow non-Doctrine owner if the shim stays hand-kept.
  - The generated `AGENTS.md` must explain the Doctrine source architecture, live emitted runtime surface, install and verify commands, and required future use of `$doctrine-learn`, `$skill-authoring`, `$prompt-authoring`, and `$agents-md-authoring`.
- Reject for this plan:
  - Do not copy `lessons_studio`'s byte-equal `AGENTS.md`/`CLAUDE.md` pattern if it would violate this repo's current thin-shim rule.
  - Do not dump full architecture history into always-on root instructions.
- Pitfalls / footguns:
  - If `AGENTS.md` becomes generated but `README.md` and `Makefile` remain hand-authored, pass 2 must still name docs/install alignment rules so the generated text does not drift.
- Sources:
  - `../lessons_studio/prompts/claude_home/SKILL.prompt` — concrete generated root instruction package using `emit:` to produce `AGENTS.md` and `CLAUDE.md`.
  - `../lessons_studio/Makefile` — `make agent-homes` emits and copies generated root instruction files.
  - `skills/agents-md-authoring/references/agents-md-pattern-contract.md` — local quality bar for root instruction content.

### Receipts, locks, and verification

- Best practices synthesized:
  - Verification should be narrow and surface-matched.
  - `SKILL.source.json` proves which source files built an emitted skill tree.
  - `doctrine.skill.lock` belongs to external source-root targets, not ordinary first-party local sources.
  - Build outputs should be safe to delete and re-create.
- Adopt for this plan:
  - Every emitted skill package needs a receipt.
  - First-party local sources should not require a lock unless pass 2 introduces external `source_root` targets.
  - Verification should layer Doctrine emit/receipt checks before current repo checks: `npx skills check` for changed runtime packages and `make verify_install` for install validation.
- Reject for this plan:
  - Do not invent a repo-shape policing script just to prove files are generated.
  - Do not use broad install verification as a substitute for source-to-output receipt validation.
- Pitfalls / footguns:
  - Deleting or recreating build outputs without verifying receipts can hide edited emitted artifacts.
  - A lock file inside an emitted skill tree would become runtime clutter and violate Doctrine's target rules.
- Sources:
  - `../doctrine/skills/doctrine-learn/prompts/refs/emit_targets.prompt` — `source_root`, `source_id`, `lock_file`, and `verify_skill_receipts`.
  - `../doctrine/skills/doctrine-learn/prompts/refs/verify_and_ship.prompt` — narrow verify-command discipline and emitted-artifact edit ban.
  - `../lessons_studio/scripts/build_skills.sh` — clears build outputs, emits all skill targets, verifies receipts, and rewires local skill roots.

### `lessons_studio` repo pattern

- Best practices synthesized:
  - `pyproject.toml` can be the single emit-target registry.
  - A helper script can derive skill target lists from configured `output_dir` values instead of duplicating target lists by hand.
  - A build command can emit skills and root instructions separately, keeping generated outputs and install wiring obvious.
- Adopt for this plan:
  - Use the `pyproject.toml` emit-target registry pattern.
  - Consider deriving Doctrine emit target lists programmatically from `pyproject.toml` to avoid target-list drift.
  - Keep this repo's install owner in `Makefile`; adapt build wiring rather than replacing it with `lessons_studio` symlinks.
- Reject for this plan:
  - Do not copy `lessons_studio`'s `.claude/skills` symlink strategy because this repo installs to `~/.agents/skills`, `~/.claude/skills`, and `~/.gemini/skills` with runtime-specific omissions and hook wiring.
  - Do not adopt its domain-specific root instructions, source roots, or skill categories.
- Pitfalls / footguns:
  - `lessons_studio` proves the pattern but not this repo's final paths. `arch_skill` must preserve Codex hook entries, Claude SessionStart hook, Gemini frontmatter stripping, stale-surface cleanup, and remote install.
- Sources:
  - `../lessons_studio/pyproject.toml` — configured emit targets, local and external source-root examples, shared prompt roots, and root instruction target.
  - `../lessons_studio/scripts/list_doctrine_skill_targets.py` — derives skill targets from `output_dir` values.
  - `../lessons_studio/scripts/build_skills.sh` — end-to-end emit, receipt verify, and runtime skill-root wiring precedent.

## Adopt / Reject summary

- Adopt:
  - Use Doctrine `skill package` sources under package-local `prompts/`.
  - Use configured emit targets and receipts for every emitted skill.
  - Use shared Doctrine declarations and prompt roots for repeated arch-suite law.
  - Generate or source-own root instruction files through Doctrine, while preserving this repo's compact `AGENTS.md` plus thin `CLAUDE.md` intent unless pass 2 records a different owner.
  - Keep `Makefile` as the install owner and adapt Doctrine build steps into it.
- Reject:
  - No hidden Doctrine runtime dependency for installed skills.
  - No symlink-only install rewrite copied from `lessons_studio`.
  - No lock file for ordinary local first-party sources.
  - No phase plan until deep-dive pass 2 writes the target architecture and call-site inventory.

## Decision gaps that must be resolved before implementation

- No new user-facing blocker was found in this pass. Deep-dive pass 2 consumed the Section 3.3 inputs into Sections 5 and 6, and the phase-plan pass consumed those decisions into Section 7. The remaining gate after consistency-pass is the Codex `gpt-5.4` `xhigh` completion consult or epic critic before sub-plan 2 starts.
<!-- arch_skill:block:external_research:end -->

<!-- arch_skill:block:current_architecture:start -->
# 4) Current Architecture (as-is)

## 4.1 On-disk structure

The live runtime source is the checked-in `skills/` tree. It currently contains 28 shipped skill packages, one shared runtime directory, 23 `agents/openai.yaml` metadata files, no `assets/` paths, and no Doctrine source receipts or source prompts. The current tree has no root `pyproject.toml`, no `doctrine.skill.lock`, no `SKILL.source.json`, and no `prompts/SKILL.prompt`; the packages are hand-authored runtime packages today.

The active package set in `Makefile` for agents/Codex and Claude Code is:

`arch-step`, `miniarch-step`, `arch-docs`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `goal-loop`, `north-star-investigation`, `arch-flow`, `arch-skills-guide`, `arch-loop`, `delay-poll`, `wait`, `agent-definition-auditor`, `agents-md-authoring`, `prompt-authoring`, `skill-authoring`, `pr-authoring`, `skill-flow`, `amir-publish`, `codex-review-yolo`, `fresh-consult`, `code-review`, `stepwise`, and `arch-epic`.

The Gemini package set is intentionally smaller. It installs the same surface except for `arch-loop`, `delay-poll`, `wait`, and `code-review`, because those packages depend on hook-backed continuation or fresh Codex review behavior that Gemini does not host.

Current package shapes:

- Every live package has a `skills/<slug>/SKILL.md` runtime instruction file.
- Many packages have `skills/<slug>/references/` with deeper runtime doctrine loaded by that skill on demand.
- `agents/openai.yaml` is present for 23 packages. Its presence and absence are both behavior-preservation facts because trigger metadata changes skill routing.
- Script-bearing packages are `arch-step`, `arch-epic`, `code-review`, `skill-flow`, and `stepwise`.
- `skills/_shared/controller-contract.md` is the only shared runtime directory named by `Makefile` through `SHARED_DIRS := _shared`; install copies it beside the packages in each target skill root.

The root support surfaces are hand-authored today:

- `Makefile` owns active package matrices, copy behavior, hook installation, stale-surface cleanup, remote install, and verification targets.
- `README.md` owns public install instructions, supported runtime matrix, feature-gate commands, skill inventory, manual recovery pointers, and verification commands.
- `docs/arch_skill_usage_guide.md` is a secondary usage/routing guide that repeats install and inventory truth from `README.md`.
- `AGENTS.md` owns repo rules for future agents, including current verification commands and skill-routing requirements.
- `CLAUDE.md` is a thin shim to `AGENTS.md`; it intentionally does not duplicate the repo rules.

## 4.2 Control paths (runtime)

Install and verification are Makefile-driven. `make install` expands to stale-surface cleanup plus skill install for agents/Codex, Claude Code, hook wiring, and Gemini unless `NO_GEMINI=1` is passed. `make remote_install HOST=user@host` directly uses `ssh` and `scp` to create remote skill directories, perform stale-surface cleanup, copy local `skills/` packages and `_shared`, install Codex and Claude hooks, and apply the Gemini frontmatter-stripping transform unless `NO_GEMINI=1` is passed. The current `remote_install` target does not run remote `make verify_install` or the remote `verify_*` targets.

The agents/Codex install path copies the 28 `SKILLS` packages into `~/.agents/skills`, copies `skills/_shared` into that same root, removes old `~/.codex/skills/<skill>` mirrors, removes or backs up archived prompt-era command files, and installs one repo-managed Codex `Stop` hook in `~/.codex/hooks.json`. That hook points at the installed runner:

`~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex`

The Claude Code install path copies the 28 `CLAUDE_SKILLS` packages into `~/.claude/skills`, copies `skills/_shared`, removes or backs up archived prompt-era command files, and installs one `Stop` hook plus one `SessionStart` hook in `~/.claude/settings.json`. The Stop hook points at the same installed runner with `--runtime claude`; the SessionStart hook caches the Claude session id needed by the runner.

The Gemini install path copies the 24 `GEMINI_SKILLS` packages into `~/.gemini/skills`, copies `skills/_shared`, and strips YAML frontmatter from each installed `SKILL.md` with the Makefile `awk` transform. Gemini receives several skills that also have Codex/Claude hook-backed behavior elsewhere, including `arch-step`, `miniarch-step`, `arch-docs`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `stepwise`, and `arch-epic`, but in Gemini they are installed only as prompt-readable skill packages with no Stop-hook continuation surface. Gemini intentionally omits `arch-loop`, `delay-poll`, `wait`, and the Codex-only `code-review` runner.

The hook-backed controller path is centralized in `skills/arch-step/scripts/arch_controller_stop_hook.py`. Controller arms and dispatches use these current rules:

- Every arm runs the installed runner's `--ensure-installed --runtime <codex|claude>` path, which idempotently upserts the canonical Stop hook and, for Claude, the SessionStart hook.
- Every Stop-hook dispatch runs `verify_installed_or_die(runtime)` before state is touched. Hook drift fails loudly instead of silently migrating.
- Controller state is runtime-local: `.codex/<controller>-state.<SESSION_ID>.json` for Codex and `.claude/arch_skill/<controller>-state.<SESSION_ID>.json` for Claude Code.
- `block_when_multiple_controller_states_armed` enforces the session-scoped single-controller gate. The current epic is deliberately running sub-plan auto-plan stages as arch-loop-managed parent passes to avoid arming `.codex/auto-plan-state.019dc9ab-bcea-7e92-8e64-89a72c56ebe6.json` beside the active arch-loop state.
- The registry currently includes controller families for `auto-plan`, `implement-loop`, `miniarch-step auto-plan`, `miniarch-step implement-loop`, `arch-docs auto`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `delay-poll`, `code-review`, `wait`, and `arch-loop`.
- `arch-loop` evaluator subprocesses are always fresh unsandboxed Codex `gpt-5.4` at `xhigh`, even when Claude hosts the Stop hook.

Archived command files are install behavior, not live runtime dependencies. `Makefile` names archived pre-skill command files and backs them up or removes them during install so old prompt-era surfaces do not compete with the shipped skill packages.

## 4.3 Object model + key abstractions

The current system is a runtime-package repository with install orchestration around it. The key objects are:

- **Skill package:** `skills/<slug>/` with `SKILL.md` as the runtime contract, optional `references/`, optional `scripts/`, optional `agents/openai.yaml`, and optional schemas or fixtures. The package must be self-contained after copy into an installed skill root.
- **Active runtime matrix:** `Makefile` variables `SKILLS`, `CLAUDE_SKILLS`, and `GEMINI_SKILLS`. These variables are behavior, not convenience lists, because they decide what each runtime can invoke.
- **Shared runtime directory:** `skills/_shared/`, currently used for `controller-contract.md`. It is copied beside installed packages and is allowed as runtime shared truth because it is installed with them.
- **Runtime metadata:** `agents/openai.yaml`, YAML frontmatter descriptions, and intentional metadata absence. These affect skill discovery and routing and must be treated as behavior.
- **Script asset:** executable or helper files under `skills/<slug>/scripts/`. These are package assets, not prose. Doctrine may own or emit the surrounding instructions later, but scripts must preserve paths, command contracts, schemas, fixtures, and exit behavior unless a later sub-plan deliberately changes them.
- **Install contract:** `Makefile` targets plus public docs. Install behavior is not owned by individual skills.
- **Hook controller:** a state-file-backed continuation loop run by the installed `arch_controller_stop_hook.py` dispatcher. The runner owns state lookup, conflict checks, staleness cleanup, subprocess invocation, and fail-loud hook verification.
- **Plan artifact:** docs such as this file and the epic doc. They are orchestration ledgers, not runtime skill package dependencies.
- **Fresh child artifact:** consult, evaluator, critic, and review subprocess output under `/tmp/fresh-consult/...`, `/tmp/code-review/...`, or hook-created temp dirs. These artifacts are evidence for a pass, not source truth to import into shipped skills.

## 4.4 Observability + failure behavior today

Verification follows the touched surface:

- After skill package changes under `skills/`, repo instructions require `npx skills check`.
- `make verify_install` validates the installed active skill surface across agents/Codex, Claude Code, hooks, and Gemini unless `NO_GEMINI=1`.
- Targeted verification exists as `make verify_agents_install`, `make verify_claude_install`, `make verify_gemini_install`, and `make verify_hook_runner`.
- The runner also exposes `--doctor`, `--list-controllers`, `--disarm`, and `--disarm-all` style recovery/inspection paths for hook-backed controller failures.
- Docs-only changes require re-reading edited files and verifying added commands or paths with `rg`; they do not imply `npx skills check` or `make verify_install` ran.

Current failure behavior is intentionally loud:

- Hook dispatch verifies canonical hook entries before touching controller state and exits with repair guidance if the installed hook is missing, stale, duplicated, or pointing at the wrong runner.
- The runner refuses multiple armed controller states in one session to avoid two controllers trying to own the same Stop-hook turn.
- Controller state schema, raw requirement hashes, audit status immutability, cadence/timeouts, and required fields are validated before continuation.
- Gemini frontmatter stripping is explicit install behavior, so Gemini drift should be verified at install time rather than papered over at runtime.
- Stale runtime surfaces are removed or backed up during install. The current contract forbids reviving archived command surfaces or making shipped skills depend on them.
- Ignored state roots such as `.codex/*-state*.json` and `.claude/arch_skill/` are operational state, not source and not doctrine.

## 4.5 UI surfaces (ASCII mockups, if UI work)

No UI surface is in scope.
<!-- arch_skill:block:current_architecture:end -->

<!-- arch_skill:block:target_architecture:start -->
# 5) Target Architecture (to-be)

## 5.1 On-disk structure (future)

This repo will use Doctrine as the source layer and keep `skills/` as the live runtime install surface. The important distinction is that `skills/<slug>/prompts/` and `skills/<slug>/build/` are source/build subtrees, while the runtime subset installed into `~/.agents/skills`, `~/.claude/skills`, and `~/.gemini/skills` is the emitted package content.

Chosen source and output layout:

```text
pyproject.toml                         Doctrine dependency, prompt roots, and emit target registry
uv.lock                                locked Doctrine environment once the scaffold is added
shared/prompts/arch_skill/             shared Doctrine declarations imported by skills
  controller_lifecycle.prompt          controller lifecycle and hook contract prose source
  install_runtime_invariants.prompt    install, stale-surface, matrix, and self-containment law
  authoring_quality.prompt             doctrine/skill/prompt/agents authoring bars
  model_runtime.prompt                 fresh-consult, spawned-check, critic, and model policy law
prompts/repo_home/SKILL.prompt         source owner for root `AGENTS.md` and thin `CLAUDE.md`
build/repo_home/                       generated root-doc build output; safe to delete
prompts/shared_runtime/SKILL.prompt    source owner for installed `_shared` runtime references
build/shared_runtime/                  generated shared-runtime build output; safe to delete
skills/<slug>/prompts/SKILL.prompt     first-party source owner for each live skill package
skills/<slug>/build/                   emitted parity tree for that package; safe to delete
skills/<slug>/SKILL.md                 live runtime output after parity-approved sync
skills/<slug>/references/              emitted or copied runtime references after sync
skills/<slug>/agents/openai.yaml       copied runtime metadata when present today
skills/<slug>/scripts/                 copied runtime scripts and fixtures when present today
skills/_shared/controller-contract.md  emitted shared runtime reference installed beside skills
```

`README.md` and `docs/arch_skill_usage_guide.md` remain public docs owned by the docs rewrite sub-plan, not hidden Doctrine runtime dependencies. They must describe the new source/runtime split after the scaffold exists. `AGENTS.md` and `CLAUDE.md` become Doctrine-emitted root instruction files from `prompts/repo_home/SKILL.prompt`; `CLAUDE.md` must continue to be a thin shim that imports or points to `AGENTS.md`, not a duplicate rule dump.

Every live skill package gets a Doctrine source owner at `skills/<slug>/prompts/SKILL.prompt`. Packages may import shared declarations from `shared/prompts/arch_skill/`. Heavy repeated prose should move into shared Doctrine declarations and emit into each package's local runtime references or into `skills/_shared` when it must be installed once beside all skills. Scripts, schemas, fixtures, binary assets, and `agents/openai.yaml` stay ordinary bundled files copied byte-for-byte unless a later sub-plan proves a specific file should be Doctrine-authored.

## 5.2 Control paths (future)

The future authoring path is:

1. Edit Doctrine source in `skills/<slug>/prompts/`, `shared/prompts/arch_skill/`, `prompts/repo_home/`, or `prompts/shared_runtime/`.
2. Run the Doctrine build target that emits configured skill and root-doc targets into `skills/<slug>/build/`, `build/repo_home/`, and `build/shared_runtime/`.
3. Verify Doctrine receipts with `doctrine.verify_skill_receipts` for emitted skill and shared-runtime targets.
4. Compare emitted output against the frozen behavior inventory before syncing a package group into the live runtime files under `skills/<slug>/`.
5. Sync only parity-approved emitted runtime files into the live runtime surface.
6. Run `npx skills check` after changed runtime packages under `skills/`.
7. Run `make verify_install` when install behavior changes or when the installed surface is intentionally validated.
8. Update `README.md`, `docs/arch_skill_usage_guide.md`, `AGENTS.md`, and `CLAUDE.md` when the source/runtime or install contract changes.

`Makefile` remains the install owner. It should gain Doctrine build/verify/sync targets, but the existing install targets still own runtime deployment for agents/Codex, Claude Code, Gemini, hooks, remote installs, stale-surface cleanup, and removed-skill cleanup. Runtime install copy must exclude source and disposable build subtrees such as `prompts/` and `build/`; installed packages may include generated receipts such as `SKILL.source.json`, but must not include Doctrine source `.prompt` files.

The runtime matrix stays unchanged:

- Agents/Codex installs the 28 `SKILLS` packages plus `_shared`.
- Claude Code installs the 28 `CLAUDE_SKILLS` packages plus `_shared`.
- Gemini installs the 24 `GEMINI_SKILLS` packages plus `_shared`, strips frontmatter from installed `SKILL.md`, and continues to omit `arch-loop`, `delay-poll`, `wait`, and `code-review`.
- Codex and Claude hook wiring continues to point at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`; the runner remains runtime code, not Doctrine-authored scheduling policy.

Cutover posture is source-first and clean per package group. A package is not considered ported until its live runtime files are emitted or copied from the Doctrine-owned source/bundle set, its behavior is compared to the frozen inventory, and the relevant verification has run. There is no dual live runtime source: after a package is cut over, future edits go to Doctrine source or bundled asset files, then re-emit and sync.

## 5.3 Object model + abstractions (future)

- **Doctrine emit target:** one `pyproject.toml` target per emitted skill package, shared-runtime package, and root instruction package. Target names should be stable and match package slugs where possible.
- **Skill source package:** `skills/<slug>/prompts/SKILL.prompt`, the long-term owner for a shipped skill's `SKILL.md`, package metadata, `when_to_use`, `when_not_to_use`, non-negotiables, first move, workflow, output expectations, and reference map.
- **Shared Doctrine module:** declarations under `shared/prompts/arch_skill/` imported by skill sources. These own repeated law, not local skill judgment.
- **Emitted parity tree:** `skills/<slug>/build/`, a disposable output tree used for review and receipt verification before runtime sync.
- **Live runtime package:** `skills/<slug>/` runtime files installed by `Makefile`. The installable subset excludes `prompts/` and `build/`.
- **Bundled runtime asset:** `scripts/`, fixtures, schemas, `agents/openai.yaml`, and assets copied byte-for-byte. These keep existing paths and command contracts.
- **Generated runtime reference:** a Markdown reference emitted from a shared or package-local Doctrine `document` through `emit:`.
- **Root instruction source package:** `prompts/repo_home/SKILL.prompt`, a Doctrine package that emits root `AGENTS.md` and thin `CLAUDE.md` into `build/repo_home/` for sync to repo root.
- **Shared runtime package:** `prompts/shared_runtime/SKILL.prompt`, a Doctrine package used to emit installed shared references such as `skills/_shared/controller-contract.md` through a sync step.
- **Source receipt:** `SKILL.source.json`, emitted for every Doctrine skill package and preserved as source-to-runtime proof. It is not the host contract.
- **Lock file:** `doctrine.skill.lock`, used only for future external `source_root` targets. First-party local `arch_skill` sources do not use a repo-level lock by default.

No host binding is part of the target architecture unless a later package genuinely needs typed host facts from a consuming agent. Most arch skills are self-contained runtime skills and should not add `host_contract:` just to share prose.

## 5.4 Invariants and boundaries

- Doctrine owns authoring. `Makefile`, hook scripts, and runtime CLIs own execution, install, scheduling, subprocess dispatch, and state.
- Emitted Markdown is runtime output. Do not hand-edit emitted `SKILL.md`, emitted references, generated root docs, `SKILL.source.json`, or `SKILL.contract.json`.
- `skills/<slug>/prompts/` and `skills/<slug>/build/` are never installed into runtime skill roots.
- Installed runtime packages remain self-contained: every reference a skill loads is either inside its installed package or inside installed `_shared`.
- `skills/_shared/controller-contract.md` remains installed beside skills. Its prose can become Doctrine-emitted, but controller state, conflict detection, hook verification, and subprocess invocation remain in `skills/arch-step/scripts/arch_controller_stop_hook.py`.
- First-party sources do not use `doctrine.skill.lock`; external source roots require `source_root`, `source_id`, and a lock outside the emitted skill tree.
- Runtime matrices, Gemini omissions, Gemini frontmatter stripping, stale mirror cleanup, archived command cleanup, and remote install behavior are preservation targets.
- Archived prompt-era command files stay retired. No emitted skill may depend on them at runtime.
- No runtime fallbacks, transitional shims, or dual live sources are approved.
- Public docs and root instructions must describe where to edit source, where emitted runtime files land, and which verification command applies to each changed surface.

## 5.5 UI surfaces (ASCII mockups, if UI work)

No UI surface is in scope.
<!-- arch_skill:block:target_architecture:end -->

<!-- arch_skill:block:call_site_audit:start -->
# 6) Call-Site Audit (exhaustive change inventory)

## 6.1 Live package parity/source-owner matrix

Legend: `A/C/G` means installed for agents/Codex, Claude Code, and Gemini. `A/C` means installed for agents/Codex and Claude Code only. Every row preserves `SKILL.md` frontmatter description, trigger intent, nearest-peer boundaries, `when_to_use`, `when_not_to_use`, hard negatives, first move, workflow order, output expectations, reference map, bundled references, scripts, schemas/fixtures, and `agents/openai.yaml` presence or absence before it can be called ported.

| Live package | Current runtime owner and package facts | Target Doctrine source owner | Runtime matrix to preserve | No-loss / asset parity notes |
| --- | --- | --- | --- | --- |
| `agent-definition-auditor` | `skills/agent-definition-auditor/SKILL.md`; `references/` has 1 file; `agents/openai.yaml` present; no scripts | `skills/agent-definition-auditor/prompts/SKILL.prompt` | A/C/G | Preserve auditor trigger boundaries and `agents/openai.yaml`; reference may be emitted from local source or copied with receipt-backed parity |
| `agents-md-authoring` | `skills/agents-md-authoring/SKILL.md`; `references/` has 5 files; `agents/openai.yaml` present; no scripts | `skills/agents-md-authoring/prompts/SKILL.prompt` plus shared authoring declarations where repeated | A/C/G | Preserve `$agents-md-authoring` root-instruction quality bar and reference set; do not flatten examples or scope rules |
| `amir-publish` | `skills/amir-publish/SKILL.md`; no references; no `agents/openai.yaml`; no scripts | `skills/amir-publish/prompts/SKILL.prompt` | A/C/G | Preserve intentional metadata absence and publish workflow boundaries |
| `arch-docs` | `skills/arch-docs/SKILL.md`; `references/` has 6 files; `agents/openai.yaml` present; no scripts | `skills/arch-docs/prompts/SKILL.prompt` plus shared controller lifecycle declarations | A/C/G | Preserve docs-cleanup controller semantics, canonical-home judgment, cleanup rules, and metadata |
| `arch-epic` | `skills/arch-epic/SKILL.md`; `references/` has 11 files including schemas; no `agents/openai.yaml`; script `scripts/run_arch_epic.py` | `skills/arch-epic/prompts/SKILL.prompt` plus shared model/runtime and controller declarations | A/C/G | Copy script and schemas byte-for-byte unless separately approved; preserve epic decomposition, critic, resume, model, and no-scope-drift contracts |
| `arch-flow` | `skills/arch-flow/SKILL.md`; `references/` has 3 files; `agents/openai.yaml` present; no scripts | `skills/arch-flow/prompts/SKILL.prompt` | A/C/G | Preserve read-only flow/status behavior, checklist rules, and recommendation boundaries |
| `arch-loop` | `skills/arch-loop/SKILL.md`; `references/` has 4 files; `agents/openai.yaml` present; no scripts | `skills/arch-loop/prompts/SKILL.prompt` plus shared controller and model/runtime declarations | A/C only | Preserve hook-backed loop semantics and Codex `gpt-5.4` `xhigh` evaluator rule; keep Gemini omitted |
| `arch-mini-plan` | `skills/arch-mini-plan/SKILL.md`; `references/` has 5 files; `agents/openai.yaml` present; no scripts | `skills/arch-mini-plan/prompts/SKILL.prompt` | A/C/G | Preserve one-pass mini planning boundary and handoff rules |
| `arch-skills-guide` | `skills/arch-skills-guide/SKILL.md`; `references/` has 2 files; `agents/openai.yaml` present; no scripts | `skills/arch-skills-guide/prompts/SKILL.prompt` | A/C/G | Preserve suite map, boundary examples, and routing behavior |
| `arch-step` | `skills/arch-step/SKILL.md`; `references/` has 20 files; `agents/openai.yaml` present; scripts `arch_controller_stop_hook.py`, `upsert_claude_session_start_hook.py`, `upsert_claude_stop_hook.py`, `upsert_codex_stop_hook.py` | `skills/arch-step/prompts/SKILL.prompt` plus shared controller lifecycle declarations | A/C/G | Copy scripts byte-for-byte unless a later phase explicitly changes them; preserve full-arch stage order, Stop-hook contracts, controller state rules, and Gemini prompt-only behavior |
| `audit-loop` | `skills/audit-loop/SKILL.md`; `references/` has 6 files; `agents/openai.yaml` present; no scripts | `skills/audit-loop/prompts/SKILL.prompt` plus shared controller lifecycle declarations | A/C/G | Preserve map-first audit loop contract, ledger, quality bar, and metadata |
| `audit-loop-sim` | `skills/audit-loop-sim/SKILL.md`; `references/` has 6 files; `agents/openai.yaml` present; no scripts | `skills/audit-loop-sim/prompts/SKILL.prompt` plus shared controller lifecycle declarations | A/C/G | Preserve simulation-specific ledger/review/run rules and metadata |
| `bugs-flow` | `skills/bugs-flow/SKILL.md`; `references/` has 6 files; `agents/openai.yaml` present; no scripts | `skills/bugs-flow/prompts/SKILL.prompt` | A/C/G | Preserve analyze/fix/review flow, bug-doc contract, and metadata |
| `code-review` | `skills/code-review/SKILL.md`; `references/` has 4 files; no `agents/openai.yaml`; script `scripts/run_code_review.py` | `skills/code-review/prompts/SKILL.prompt` plus shared model/runtime declarations | A/C only | Copy runner byte-for-byte unless separately approved; preserve Codex `gpt-5.4` `xhigh` synthesis, `gpt-5.4-mini` lens fan-out, review-only behavior, and Gemini omission |
| `codex-review-yolo` | `skills/codex-review-yolo/SKILL.md`; `references/` has 3 files; no `agents/openai.yaml`; no scripts | `skills/codex-review-yolo/prompts/SKILL.prompt` | A/C/G | Preserve intentional metadata absence, verdict contract, and troubleshooting reference |
| `comment-loop` | `skills/comment-loop/SKILL.md`; `references/` has 7 files; `agents/openai.yaml` present; no scripts | `skills/comment-loop/prompts/SKILL.prompt` plus shared controller lifecycle declarations | A/C/G | Preserve comment loop controller, commenting principles, ledger, review, run, and metadata |
| `delay-poll` | `skills/delay-poll/SKILL.md`; `references/` has 3 files; `agents/openai.yaml` present; no scripts | `skills/delay-poll/prompts/SKILL.prompt` plus shared controller lifecycle declarations | A/C only | Preserve delay/check examples and hook-backed resume boundary; keep Gemini omitted |
| `fresh-consult` | `skills/fresh-consult/SKILL.md`; `references/` has 2 files; `agents/openai.yaml` present; no scripts | `skills/fresh-consult/prompts/SKILL.prompt` plus shared model/runtime declarations | A/C/G | Preserve prompt-only subprocess contract, artifact paths, model/runtime/effort ask rules, and no silent provider downgrade |
| `goal-loop` | `skills/goal-loop/SKILL.md`; `references/` has 7 files; `agents/openai.yaml` present; no scripts | `skills/goal-loop/prompts/SKILL.prompt` plus shared controller lifecycle declarations | A/C/G | Preserve setup, context digest, flow status, iterate, quality bar, and metadata |
| `lilarch` | `skills/lilarch/SKILL.md`; `references/` has 6 files; `agents/openai.yaml` present; no scripts | `skills/lilarch/prompts/SKILL.prompt` | A/C/G | Preserve lightweight plan/start/finish boundaries and escalation to mini/full arch |
| `miniarch-step` | `skills/miniarch-step/SKILL.md`; `references/` has 14 files; `agents/openai.yaml` present; no scripts | `skills/miniarch-step/prompts/SKILL.prompt` plus shared controller lifecycle declarations | A/C/G | Preserve trimmed full-arch surface, auto-plan/implement-loop behavior, and metadata |
| `north-star-investigation` | `skills/north-star-investigation/SKILL.md`; `references/` has 5 files; `agents/openai.yaml` present; no scripts | `skills/north-star-investigation/prompts/SKILL.prompt` | A/C/G | Preserve bootstrap, investigation contract, iteration, quality bar, and metadata |
| `pr-authoring` | `skills/pr-authoring/SKILL.md`; `references/` has 1 file; `agents/openai.yaml` present; no scripts | `skills/pr-authoring/prompts/SKILL.prompt` | A/C/G | Chosen representative scaffold package; preserve publish-not-draft boundary, PR body scaffold behavior, metadata, and blocked-publication output |
| `prompt-authoring` | `skills/prompt-authoring/SKILL.md`; `references/` has 5 files; `agents/openai.yaml` present; no scripts | `skills/prompt-authoring/prompts/SKILL.prompt` plus shared authoring declarations | A/C/G | Preserve prompt refactor fidelity, anti-heuristic rules, examples, and metadata |
| `skill-authoring` | `skills/skill-authoring/SKILL.md`; `references/` has 8 files; `agents/openai.yaml` present; no scripts | `skills/skill-authoring/prompts/SKILL.prompt` plus shared authoring declarations | A/C/G | Preserve package quality bar, trigger/packaging/validation guidance, peer boundaries, and metadata |
| `skill-flow` | `skills/skill-flow/SKILL.md`; `references/` has 7 files; `agents/openai.yaml` present; script/fixtures `render_dag_d2.py`, `test_fixtures/tiny_substrate.expected.d2`, `test_fixtures/tiny_substrate.md` | `skills/skill-flow/prompts/SKILL.prompt` plus shared authoring/flow declarations | A/C/G | Copy renderer and fixtures byte-for-byte unless separately approved; preserve DAG substrate contract, parallel walk, waste-pattern catalog, and metadata |
| `stepwise` | `skills/stepwise/SKILL.md`; `references/` has 15 files including schemas; no `agents/openai.yaml`; scripts `check_source_tags.py`, `run_stepwise.py`, `stepwise_learnings.py`, `test_run_stepwise.py` | `skills/stepwise/prompts/SKILL.prompt` plus shared model/runtime declarations | A/C/G | Copy scripts and schemas byte-for-byte unless separately approved; preserve ordered step execution, critic, repair, learning, and model/effort routing |
| `wait` | `skills/wait/SKILL.md`; `references/` has 1 file; `agents/openai.yaml` present; no scripts | `skills/wait/prompts/SKILL.prompt` plus shared controller lifecycle declarations | A/C only | Preserve one-shot delay semantics and hook-backed resume boundary; keep Gemini omitted |

## 6.2 Shared/support source-owner matrix

| Surface | Current owner | Target owner | Preservation / verification obligation |
| --- | --- | --- | --- |
| Installed shared runtime reference | `skills/_shared/controller-contract.md` | `prompts/shared_runtime/SKILL.prompt` emitting to `skills/_shared/controller-contract.md` | Remains installed beside every runtime skill root and stays self-contained; verify with Doctrine receipts, `npx skills check` after sync, and `make verify_install` when `_shared` changes |
| Install matrices and copy behavior | `Makefile` variables `SKILLS`, `CLAUDE_SKILLS`, `GEMINI_SKILLS`, `SHARED_DIRS`, `REMOVED_SKILLS` | `Makefile`; not Doctrine-owned | Preserve 28 agents/Codex, 28 Claude Code, 24 Gemini, `_shared`, removed-skill cleanup, and runtime-subset copy excluding `prompts/` and `build/`; verify with targeted `make verify_*` and `make verify_install` |
| Gemini frontmatter transform | `Makefile` `gemini_install_skill` `awk` transform | `Makefile`; not Doctrine-owned | Preserve stripping behavior after emitted runtime sync; verify with `make verify_gemini_install` and installed file inspection when changed |
| Remote install | `Makefile` `remote_install` | `Makefile`; not Doctrine-owned | Use the same runtime-subset copy semantics as local install; verify with `make -n remote_install HOST=example.invalid NO_GEMINI=1`, re-read, and `rg` checks after target changes |
| Hook runner and hook upserters | `skills/arch-step/scripts/arch_controller_stop_hook.py`, `upsert_codex_stop_hook.py`, `upsert_claude_stop_hook.py`, `upsert_claude_session_start_hook.py` | Bundled runtime assets copied through the `arch-step` package | Preserve script paths, arguments, state schema behavior, conflict gate, and fail-loud hook verification; verify with `make verify_hook_runner` and existing script tests/checks when touched |
| Epic runner | `skills/arch-epic/scripts/run_arch_epic.py` | Bundled runtime asset copied through `arch-epic` | Preserve CLI contract and critic/resume semantics; verify with package-specific smoke/tests when touched |
| Code-review runner | `skills/code-review/scripts/run_code_review.py` | Bundled runtime asset copied through `code-review` | Preserve Codex-only review process, artifact layout, and no-edit contract; verify with runner smoke/tests when touched |
| Skill-flow renderer and fixtures | `skills/skill-flow/scripts/render_dag_d2.py`, `skills/skill-flow/scripts/test_fixtures/*` | Bundled runtime assets copied through `skill-flow` | Preserve DAG rendering contract and fixture expectations; run fixture smoke/tests when touched |
| Stepwise scripts and schemas | `skills/stepwise/scripts/*`, `skills/stepwise/references/*.schema.json` | Bundled runtime assets copied through `stepwise` | Preserve source-tag checks, runner, learning store, tests, and verdict schema behavior; run `skills/stepwise/scripts/test_run_stepwise.py` when touched |
| OpenAI metadata files | `skills/*/agents/openai.yaml` for 23 packages; absent for 5 packages | Copied byte-for-byte by each package emit/sync unless explicitly source-authored later | Preserve both presence and absence because routing changes behavior; verify with package parity review and `npx skills check` |
| Public install docs | `README.md`, `docs/arch_skill_usage_guide.md` | Hand-authored docs updated after scaffold/port; not hidden runtime dependencies | Keep install matrices, feature gates, hook behavior, stale cleanup, and verification commands aligned with `Makefile`; verify by re-read and `rg` |
| Root instructions | `AGENTS.md`, `CLAUDE.md` | `prompts/repo_home/SKILL.prompt` emitting compact `AGENTS.md` and thin `CLAUDE.md` | Keep always-on instructions concise and require `$doctrine-learn`, `$skill-authoring`, `$prompt-authoring`, and `$agents-md-authoring`; verify root-doc emit and re-read |
| Doctrine receipts and locks | none today | `SKILL.source.json` emitted for every Doctrine-owned skill; no first-party local `doctrine.skill.lock` | Verify receipts for every emitted package. Add `doctrine.skill.lock` only for future external `source_root` targets and keep it outside emitted runtime skill trees |
| Archived command cleanup | `Makefile` `ARCHIVED_COMMAND_FILES`, `clean_*_stale_surfaces`, verify targets | `Makefile`; not Doctrine-owned | Keep prompt-era commands retired and unavailable as runtime dependencies; verify with existing install checks |

## 6.3 Change map (table)

| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Doctrine config | `pyproject.toml` | `[project]`, `[tool.doctrine.compile]`, `[tool.doctrine.emit]` | No Doctrine config exists | Add Doctrine dependency/config, shared prompt roots, and emit targets for skills, root docs, and shared runtime docs | Makes Doctrine source ownership explicit and runnable | `uv run --locked python -m doctrine.emit_skill --target <target>` | Doctrine emit and receipt checks |
| Locked env | `uv.lock` | Doctrine dependency lock | No locked Python env exists | Add lock after adding `doctrine-agents` | Makes emit/verify reproducible | `uv run --locked ...` | `uv sync`; Doctrine emit checks |
| Shared source | `shared/prompts/arch_skill/*.prompt` | Shared declarations | No shared Doctrine prompt root exists | Add shared modules for controller lifecycle, install/runtime invariants, authoring quality bars, and model/runtime law | Folds repeated doctrine without hidden runtime context | Imported Doctrine declarations | Doctrine compile/emit |
| Root instructions source | `prompts/repo_home/SKILL.prompt` | Root instruction package | `AGENTS.md` and `CLAUDE.md` are hand-authored | Emit compact `AGENTS.md` and thin `CLAUDE.md` shim from Doctrine source | Gives root instructions a source owner while preserving always-on budget | Generated root docs synced from `build/repo_home/` | Docs re-read; root-doc emit |
| Shared runtime source | `prompts/shared_runtime/SKILL.prompt` | Shared runtime package | `skills/_shared/controller-contract.md` is hand-authored | Emit installed shared runtime references from Doctrine source | Gives `_shared` doctrine a source owner and keeps installed runtime self-contained | Sync generated `controller-contract.md` to `skills/_shared/` | Doctrine emit/receipt; install verification when synced |
| Skill sources | `skills/<slug>/prompts/SKILL.prompt` | 28 live skill packages | `skills/<slug>/SKILL.md` is hand-authored runtime source | Add a Doctrine source package for every live skill | Makes each skill fully Doctrine-authored | `skill package` source for each slug | Doctrine emit; parity review; `npx skills check` after sync |
| Emitted build trees | `skills/<slug>/build/` | Per-skill output | No emitted parity tree exists | Emit disposable build output for review before runtime sync | Allows parity checks before changing live runtime files | `skills/<slug>/build/SKILL.md` and receipt | Doctrine receipt verification |
| Runtime sync | `skills/<slug>/SKILL.md`, `references/`, `agents/`, `scripts/` | Live runtime packages | Runtime files are edited directly | Sync only parity-approved generated/copy-through runtime files from source/build | Prevents hand-edited emitted drift and source leakage | Live package is emitted runtime subset | `npx skills check`; targeted package diff review |
| Runtime metadata | `skills/*/agents/openai.yaml` | OpenAI metadata files | 23 packages have metadata, 5 do not | Preserve presence, absence, path, and content unless a later package port explicitly changes it | Metadata affects routing and is behavior | Copied byte-for-byte by Doctrine package emit/sync | `npx skills check`; parity review |
| Script assets | `skills/arch-step/scripts/*`, `skills/arch-epic/scripts/*`, `skills/code-review/scripts/*`, `skills/skill-flow/scripts/*`, `skills/stepwise/scripts/*` | Runtime scripts, fixtures, schemas | Scripts are runtime package assets | Keep byte-for-byte paths and command contracts while porting prose around them | Avoids behavior drift in controllers/reviewers/helpers | Bundled runtime assets | Existing script tests where present; hook doctor; code-review runner checks when touched |
| Install owner | `Makefile` | `install`, `agents_install_skill`, `claude_install_skill`, `gemini_install_skill` | Copies entire `skills/<slug>` directories | Preserve matrices but copy only runtime subset, excluding `prompts/` and `build/` | Prevents Doctrine source/build trees from becoming installed runtime behavior | Runtime-copy helper used by local and remote install targets | `make verify_install`; targeted `verify_*` |
| Build owner | `Makefile` | New Doctrine targets | No Doctrine build targets exist | Add targets to emit, verify receipts, and sync approved outputs | Keeps source-to-runtime workflow one-command and visible | `make doctrine_build`, `make doctrine_verify_receipts`, and `make doctrine_sync_approved` | Doctrine emit/receipt checks |
| Target discovery | `scripts/list_doctrine_skill_targets.py` | Emit target listing helper | No root script exists | Add helper derived from `pyproject.toml` | Avoids drift between config and Makefile build commands | Target names and output dirs from config | Unit/smoke check for helper |
| Ignored build output | `.gitignore` | Build artifacts | Only env/state/cache patterns are ignored | Ignore disposable `build/` and `skills/*/build/` if build outputs are not committed | Prevents generated parity trees from polluting commits | Committed live runtime files remain outside ignored build dirs | Git status check |
| Agents/Codex install | `Makefile` | `SKILLS`, `agents_install_skill`, `codex_install_hook` | Installs 28 skills and `_shared`, writes Codex hook | Preserve list and hook wiring; source/build dirs excluded from copied packages | Maintains current Codex behavior | Same installed `~/.agents/skills` contract | `make verify_agents_install`; `make verify_codex_install` |
| Claude install | `Makefile` | `CLAUDE_SKILLS`, `claude_install_skill`, `claude_install_hook` | Installs 28 skills and `_shared`, writes Stop and SessionStart hooks | Preserve list and hook wiring; source/build dirs excluded from copied packages | Maintains current Claude Code behavior | Same installed `~/.claude/skills` and settings contract | `make verify_claude_install`; `make verify_hook_runner` |
| Gemini install | `Makefile` | `GEMINI_SKILLS`, `gemini_install_skill` | Installs 24 skills, strips frontmatter | Preserve omissions and frontmatter stripping after runtime sync | Avoids installing hook-backed/Codex-only packages into Gemini | Same `~/.gemini/skills` contract | `make verify_gemini_install` |
| Remote install | `Makefile` | `remote_install` | Mirrors local install behavior by ssh/scp | Apply the same runtime-subset copy and Doctrine-output assumptions remotely | Remote machines must not receive source/build leakage or changed matrices | Same `HOST=user@host` contract | `make remote_install HOST=...`; `make verify_install` remotely when used |
| Stale cleanup | `Makefile` | `ARCHIVED_COMMAND_FILES`, `clean_*_stale_surfaces` | Retires prompt-era command files | Preserve cleanup list and behavior | Prevents archived commands from becoming competing runtime truth | Archived surfaces stay retired | Existing verify targets |
| Hook runner | `skills/arch-step/scripts/arch_controller_stop_hook.py` | Shared controller dispatcher | Owns state, hooks, evaluator, conflict gate | Keep as runtime script asset; do not reimplement in Doctrine | Doctrine is authoring layer, not scheduler | Script remains runtime owner | `make verify_hook_runner`; controller tests if changed |
| Public install docs | `README.md` | Install, inventory, verification sections | Describes current direct `skills/` install surface | Update after scaffold/port to describe Doctrine source, emitted runtime subset, matrices, and verify commands | Public docs must match Makefile | Source/runtime split documented | Docs re-read; path/command `rg` checks |
| Usage guide | `docs/arch_skill_usage_guide.md` | Install/routing guide | Mirrors current install and inventory truth | Update with new source/runtime split and routing changes | Prevents duplicate public truth drift | Same supported runtime story as README | Docs re-read; path/command `rg` checks |
| Repo instructions | `AGENTS.md` | Build/verify, routing, docs map | Hand-authored repo rules | Emit from `prompts/repo_home/SKILL.prompt`; require `$doctrine-learn`, `$skill-authoring`, `$prompt-authoring`, `$agents-md-authoring` for future instruction work | Makes always-on rules source-owned and current | Generated compact root instruction file | Root-doc emit; docs re-read |
| Claude shim | `CLAUDE.md` | Claude Code repo shim | Thin hand-authored shim to `AGENTS.md` | Emit from `prompts/repo_home/SKILL.prompt` as a thin shim | Keeps Claude behavior without duplicated rules | Generated shim | Root-doc emit; docs re-read |
| Epic and sub-plan docs | `docs/EPIC_ARCH_SKILL_DOCTRINE_PORT_2026-04-26.md`, this doc | Orchestration ledgers | Track staged migration | Keep statuses/logs truthful as sub-plans advance | Prevents controller/evaluator drift | Docs are planning state, not runtime deps | Docs re-read |

## 6.4 Migration notes

* Canonical owner path / shared code path: Doctrine source lives in `skills/<slug>/prompts/SKILL.prompt`, `shared/prompts/arch_skill/`, `prompts/repo_home/SKILL.prompt`, and `prompts/shared_runtime/SKILL.prompt`; live installed runtime files remain under `skills/<slug>/` and `skills/_shared/`.
* Deprecated APIs (if any): none introduced by this sub-plan. Archived prompt-era command files remain retired and must not be revived.
* Delete list (what must be removed; include superseded shims/parallel paths if any): no deletion happens in this planning sub-plan. Later implementation must remove any temporary generated-output staging that is not intended to stay, and must not keep a second live hand-authored `SKILL.md` source beside a Doctrine-owned source after package cutover.
* Adjacent surfaces tied to the same contract family: `Makefile`, `README.md`, `docs/arch_skill_usage_guide.md`, `AGENTS.md`, `CLAUDE.md`, `skills/_shared/controller-contract.md`, all 28 skill packages, runtime metadata files, script-bearing package assets, and installed hook configuration.
* Compatibility posture / cutover plan: preserve the installed contract. Cut over source ownership cleanly per package group after parity proof; do not ship a runtime bridge or alternate invocation surface.
* Capability-replacing harnesses to delete or justify: none. The existing hook runner remains the canonical runtime harness; Doctrine must not replace it.
* Live docs/comments/instructions to update or delete: update root instructions, README, usage guide, and any package reference text that mentions direct hand-editing or stale source ownership.
* Behavior-preservation signals for refactors: frozen behavior inventory, emitted-vs-current package diff review, `SKILL.source.json` receipt verification, `npx skills check` after runtime package changes, targeted `make verify_*` for install paths, and `make verify_install` for install behavior changes or intentional full install validation.

## 6.5 Pattern Consolidation Sweep (anti-blinders; scoped by plan)

| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude/blocker question) |
| --- | --- | --- | --- | --- |
| Controller lifecycle doctrine | `skills/arch-step`, `skills/arch-docs`, `skills/audit-loop`, `skills/comment-loop`, `skills/audit-loop-sim`, `skills/goal-loop`, `skills/delay-poll`, `skills/wait`, `skills/arch-loop`, `skills/_shared/controller-contract.md` | Shared Doctrine source for controller lifecycle prose, emitted into installed references | Prevents each controller skill from carrying slightly different hook law | include |
| Install/runtime invariants | `Makefile`, `README.md`, `docs/arch_skill_usage_guide.md`, `AGENTS.md` | Shared source and docs wording for matrices, frontmatter stripping, `_shared`, stale cleanup, remote install, and verification | Prevents public docs and install behavior from disagreeing | include |
| Model/runtime conventions | `skills/fresh-consult`, `skills/code-review`, `skills/arch-loop`, `skills/arch-epic`, `skills/stepwise` | Shared Doctrine source for explicit runtime/model/effort and no silent downgrade/provider switch | Prevents recurrence of the critic/runtime drift already repaired in the epic | include |
| Authoring quality bars | `../doctrine/skills/doctrine-learn` external refs, `skills/skill-authoring`, `skills/prompt-authoring`, `skills/agents-md-authoring`, root `AGENTS.md` | Shared Doctrine source or references for future instruction-bearing work | Keeps future skills from becoming half Markdown, half Doctrine, or losing prompt structure | include |
| Root instruction ownership | `AGENTS.md`, `CLAUDE.md`, `prompts/repo_home/SKILL.prompt` | Doctrine-emitted root docs with compact always-on rules | Prevents hand-edited root rules from drifting away from the Doctrine source model | include |
| Package runtime metadata | `skills/*/agents/openai.yaml` | Copy-through metadata parity checklist | Prevents trigger/routing drift while porting prose | include |
| Script-bearing packages | `arch-step`, `arch-epic`, `code-review`, `skill-flow`, `stepwise` scripts | Copy-through asset parity and command-contract review | Prevents prose port from breaking deterministic runners | include |
| Gemini runtime boundary | `GEMINI_SKILLS`, `gemini_install_skill` | Preserve omission/strip transform until explicitly changed | Prevents the intentionally omitted continuation-only or Codex-only packages (`arch-loop`, `delay-poll`, `wait`, `code-review`) from appearing in Gemini while preserving the current 24 prompt-readable package surface | include |
| Public docs inventory | `README.md`, `docs/arch_skill_usage_guide.md` | One docs rewrite pass after source/runtime scaffold is real | Prevents duplicated inventory and install claims from diverging | include |
| Broader stale-doc cleanup | unrelated old docs outside this epic | Use `$arch-docs` only after implementation/audit if needed | Avoids turning this planning pass into a repo-wide docs cleanup | defer |
<!-- arch_skill:block:call_site_audit:end -->

<!-- arch_skill:block:phase_plan:start -->
# 7) Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; split Section 7 into the best sequence of coherent self-contained units, optimizing for phases that are fully understood, credibly testable, compliance-complete, and safe to build on later. If two decompositions are both valid, bias toward more phases than fewer. `Work` explains the unit and is explanatory only for modern docs. `Checklist (must all be done)` is the authoritative must-do list inside the phase. `Exit criteria (all required)` names the exhaustive concrete done conditions the audit must validate. Resolve adjacent-surface dispositions and compatibility posture before writing the checklist. Before a phase is valid, run an obligation sweep and move every required promise from architecture, call-site audit, migration notes, delete lists, verification commitments, docs/comments propagation, approved bridges, and required helper follow-through into `Checklist` or `Exit criteria`. The authoritative checklist must name the actual chosen work, not unresolved branches or "if needed" placeholders. Refactors, consolidations, and shared-path extractions must preserve existing behavior with credible evidence proportional to the risk. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly. Runtime bridges and dual live sources are not approved. Prefer programmatic checks per phase; defer manual review to finalization when it is the honest proof. Avoid negative-value tests and heuristic gates such as keyword scans, absence-only checks, and repo-shape policing.

This phase plan is an implementation plan for the later scaffold and port work. This `phase-plan` pass does not add Doctrine config, create source files, port skills, change install behavior, or rewrite root docs.

## Phase 1 — Protect the live install surface before source trees exist

* Goal: Make it safe to add `skills/<slug>/prompts/` and `skills/<slug>/build/` without leaking source or disposable build output into installed runtimes.
* Work: Update the install boundary first, because later phases add source/build subtrees inside `skills/`.
* Checklist (must all be done):
  - Add a runtime-copy path in `Makefile` that installs only the runtime subset of each package and excludes `prompts/` and `build/`.
  - Apply that runtime-copy path to `agents_install_skill`, `claude_install_skill`, `gemini_install_skill`, and `remote_install`.
  - Preserve `SKILLS`, `CLAUDE_SKILLS`, `GEMINI_SKILLS`, `SHARED_DIRS`, `REMOVED_SKILLS`, and `ARCHIVED_COMMAND_FILES` exactly unless a later explicit Decision Log entry changes them.
  - Preserve Codex Stop-hook install, Claude Stop-hook plus SessionStart install, Gemini frontmatter stripping, stale command cleanup, old Codex mirror removal, and remote install behavior.
  - Keep `skills/_shared/controller-contract.md` installed beside runtime packages.
  - Add or update high-leverage comments at the Makefile runtime-copy boundary explaining why source/build subtrees are excluded.
* Verification (required proof):
  - Run `make verify_install`.
  - Re-read `Makefile` install and verify targets after changes.
  - Run `make -n remote_install HOST=example.invalid NO_GEMINI=1` and re-read `remote_install` to verify it uses the same runtime-subset copy helper as local install.
  - Verify with `rg` that referenced install paths and commands in docs still exist.
* Docs/comments (propagation; only if needed):
  - Update only the minimal install-boundary wording in `README.md`, `docs/arch_skill_usage_guide.md`, and `AGENTS.md` if this phase changes user-visible install behavior.
* Exit criteria (all required):
  - Installed agents/Codex, Claude Code, and Gemini skill surfaces still contain the same active skill matrices as before.
  - No installed package contains a `prompts/` or `build/` subtree.
  - Codex, Claude, Gemini, stale-surface cleanup, and `_shared` install verification pass.
  - Remote install uses the same runtime-subset copy semantics as local install.
* Rollback:
  - Revert the install-copy helper changes and restore the previous direct-copy rules before adding any Doctrine source/build directories.

## Phase 2 — Add Doctrine scaffold and representative emit/sync path

* Goal: Introduce Doctrine as a runnable source/build layer without attempting the whole suite port.
* Work: Add the minimum repo scaffold that can compile representative sources into disposable build trees, verify receipts, and sync a small approved runtime subset.
* Checklist (must all be done):
  - Add `pyproject.toml` with `doctrine-agents`, Doctrine compile roots, and emit targets for one representative skill package, `prompts/repo_home/SKILL.prompt`, and `prompts/shared_runtime/SKILL.prompt`.
  - Add `uv.lock` through the standard locked environment workflow.
  - Add `shared/prompts/arch_skill/` with the initial shared module files named in Section 5.1.
  - Add `prompts/repo_home/SKILL.prompt` that can emit compact `AGENTS.md` and a thin `CLAUDE.md` shim into `build/repo_home/`.
  - Add `prompts/shared_runtime/SKILL.prompt` that can emit the shared runtime reference tree into `build/shared_runtime/`.
  - Add representative `skills/pr-authoring/prompts/SKILL.prompt` first because `pr-authoring` is prompt-only, installed in all runtime matrices, has one reference, has `agents/openai.yaml`, and has no scripts.
  - Add `scripts/list_doctrine_skill_targets.py` as the target-discovery helper derived from `pyproject.toml`.
  - Add Makefile targets for Doctrine emit, receipt verification, and explicit parity-approved sync into the live runtime surface.
  - Do not add `doctrine.skill.lock` for first-party local sources; reserve locks for future external `source_root` targets only.
  - Update `.gitignore` for disposable build outputs that are not committed.
  - Sync only parity-approved emitted runtime files into live `skills/`; do not sync `.prompt` source files into installed packages.
* Verification (required proof):
  - Run `uv sync`.
  - Run the representative Doctrine emit command through the new Makefile target.
  - Run `doctrine.verify_skill_receipts` for emitted representative targets.
  - Run `npx skills check` after syncing the representative runtime package.
  - Run `make verify_install` because install/build behavior changed.
* Docs/comments (propagation; only if needed):
  - Update `README.md`, `docs/arch_skill_usage_guide.md`, and `AGENTS.md` enough to tell future agents that Doctrine source now exists and emitted runtime files must not be hand-edited.
* Exit criteria (all required):
  - Doctrine can emit the representative skill, root-doc package, and shared-runtime package from configured targets.
  - Each emitted skill target has a current `SKILL.source.json` receipt.
  - No first-party local source target creates or requires `doctrine.skill.lock`.
  - Live runtime install behavior remains unchanged for users.
  - Build/source trees are excluded from installed runtime packages.
  - The scaffold has no hidden runtime dependency on `../doctrine`, `../lessons_studio`, or archived command files.
* Rollback:
  - Remove the scaffold files and restore docs to the pre-scaffold source-ownership story; keep Phase 1 install guardrails only if they remain correct for the direct-runtime tree.

## Phase 3 — Freeze the parity matrix and no-loss transfer protocol

* Goal: Make behavior preservation auditable before bulk porting starts.
* Work: Expand the Section 6 source-owner matrix into package-by-package no-loss evidence rows before bulk package porting begins.
* Checklist (must all be done):
  - For all 28 active skills named in Section 6.1, record frontmatter description, trigger intent, nearest-peer boundaries, `when_to_use`, `when_not_to_use`, non-negotiables, first move, workflow order, output expectations, reference map, bundled references, scripts, schemas/fixtures, and `agents/openai.yaml` presence or absence.
  - Record the agents/Codex, Claude Code, and Gemini install disposition for every active skill.
  - Record the five script-bearing packages and the command/path contracts their scripts expose.
  - Record `_shared` runtime references and their installing behavior.
  - Record the docs/install surfaces that must move with the source/runtime architecture: `Makefile`, `README.md`, `docs/arch_skill_usage_guide.md`, `AGENTS.md`, and `CLAUDE.md`.
  - Define the no-loss review method for each package port: source transfer, emitted diff, behavior-preservation review, receipt verification, package validation, and install validation when required.
  - Identify repeated doctrine that must move into shared components and local skill judgment that must stay local.
* Verification (required proof):
  - Re-read the parity matrix against `rg --files skills`, `Makefile`, `README.md`, and the usage guide.
  - Use `rg` to verify every path, command, skill slug, and script path named in the matrix.
* Docs/comments (propagation; only if needed):
  - Keep the parity matrix in the canonical plan/worklog surface for this migration; do not create a competing plan.
* Exit criteria (all required):
  - Every active skill has a parity row before it is ported.
  - Runtime metadata presence and absence are explicitly captured.
  - Script-bearing packages have command-contract preservation notes.
  - Repeated shared-law candidates are classified before shared component extraction begins.
  - No package can enter bulk porting without a named parity baseline and verification path.
* Rollback:
  - Restore the previous parity matrix version from git and repeat the inventory pass before porting.

## Phase 4 — Build shared Doctrine components and shared runtime references

* Goal: Create the shared source homes that remove redundancy without hiding runtime truth.
* Work: Author the common arch-suite doctrine once and emit it into self-contained runtime references.
* Checklist (must all be done):
  - Create shared Doctrine declarations for controller lifecycle, install/runtime invariants, authoring quality bars, and model/runtime conventions.
  - Keep scheduling, hook state, subprocess dispatch, conflict detection, and hook verification owned by `skills/arch-step/scripts/arch_controller_stop_hook.py`.
  - Emit or copy `skills/_shared/controller-contract.md` from the shared-runtime source owner.
  - Ensure installed runtime references contain all text needed at runtime and do not point users to hidden Doctrine source as required context.
  - Replace duplicated cross-skill law only after its shared owner exists and emits cleanly.
  - Preserve local skill-specific judgment in the owning package instead of over-centralizing it.
* Verification (required proof):
  - Run Doctrine emit and receipt verification for shared-runtime targets.
  - Re-read emitted `_shared` references and source declarations for self-containment.
  - Run `npx skills check` after synced runtime references change.
  - Run `make verify_install` when `_shared` or install behavior changes.
* Docs/comments (propagation; only if needed):
  - Update docs that explain `_shared` ownership and the source/runtime split.
* Exit criteria (all required):
  - Shared components compile and emit.
  - `_shared` remains installed beside all runtime skill roots.
  - No shipped skill requires hidden repo docs or Doctrine source at runtime.
  - Redundant cross-skill law has one source owner or an explicit local reason to remain local.
* Rollback:
  - Restore the hand-authored `_shared` runtime reference and remove the shared-runtime emit target until the shared source can emit parity-clean output.

## Phase 5 — Port controller and arch-workflow skill packages

* Goal: Port the hook-backed and arch-workflow core without changing controller behavior.
* Work: Convert the controller-heavy and arch-flow packages to Doctrine source while preserving scripts, references, metadata, and behavior.
* Checklist (must all be done):
  - Port `arch-step`, `miniarch-step`, `arch-docs`, `arch-mini-plan`, `lilarch`, `bugs-flow`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `goal-loop`, `north-star-investigation`, `arch-flow`, `arch-skills-guide`, `arch-loop`, `delay-poll`, `wait`, and `arch-epic`.
  - For each package, create `skills/<slug>/prompts/SKILL.prompt` and configured emit target.
  - Preserve every trigger, workflow order, hard negative, first move, output contract, reference map, model/runtime rule, and runtime metadata fact from the parity matrix.
  - Copy scripts, fixtures, schemas, and `agents/openai.yaml` byte-for-byte unless the package-specific parity review approves a source-authored replacement.
  - Import shared controller/model/install doctrine only where it replaces true repeated law.
  - Sync emitted runtime files only after emitted-vs-current review passes.
  - Keep Gemini omissions for `arch-loop`, `delay-poll`, and `wait`.
* Verification (required proof):
  - Run Doctrine emit and receipt verification for every ported package in this phase.
  - Run emitted-vs-current behavior-preservation review for every ported package before sync.
  - Run `npx skills check` after runtime package sync.
  - Run `make verify_hook_runner` and `make verify_install` after controller package sync.
  - Run existing script tests for script-bearing packages where present, including `skills/stepwise/scripts/test_run_stepwise.py` when `stepwise` is touched in a later phase.
* Docs/comments (propagation; only if needed):
  - Update package-local references that describe source ownership or controller law.
* Exit criteria (all required):
  - All listed packages have Doctrine source owners and current receipts.
  - Installed controller behavior, state paths, hook wiring, and evaluator/runtime policies remain unchanged.
  - No controller package depends on archived command files or hidden Doctrine source at runtime.
  - Gemini still installs the current 24 prompt-readable `GEMINI_SKILLS` packages and still omits only `arch-loop`, `delay-poll`, `wait`, and `code-review`.
* Rollback:
  - Restore the affected package's pre-port runtime files from git and remove or ignore its emit target until parity is repaired.

## Phase 6 — Port authoring, review, publishing, and support skill packages

* Goal: Port the remaining live packages while preserving authoring guidance and review/publish runner contracts.
* Work: Convert the non-controller package group to Doctrine source and shared components.
* Checklist (must all be done):
  - Port `agent-definition-auditor`, `agents-md-authoring`, `prompt-authoring`, `skill-authoring`, `pr-authoring`, `skill-flow`, `amir-publish`, `codex-review-yolo`, `fresh-consult`, `code-review`, and `stepwise`.
  - Preserve authoring-quality guidance from `$doctrine-learn`, `$skill-authoring`, `$prompt-authoring`, and `$agents-md-authoring`.
  - Preserve `fresh-consult` runtime/model/effort rules and no silent downgrade/provider-switch behavior.
  - Preserve `code-review` Codex `gpt-5.4` `xhigh` synthesis and `gpt-5.4-mini` lens fan-out behavior.
  - Preserve `stepwise` scripts, schemas, learning behavior, and model/effort routing rules.
  - Preserve `skill-flow` DAG/rendering behavior and script fixtures.
  - Sync emitted runtime files only after per-package no-loss review passes.
  - Keep Gemini omission for `code-review`.
* Verification (required proof):
  - Run Doctrine emit and receipt verification for every ported package in this phase.
  - Run emitted-vs-current behavior-preservation review for every ported package before sync.
  - Run `npx skills check` after runtime package sync.
  - Run package script tests or smoke checks for `stepwise`, `skill-flow`, and `code-review` when their scripts or script-facing instructions changed.
  - Run `make verify_install` after this package group is synced.
* Docs/comments (propagation; only if needed):
  - Update package-local references that describe source ownership, review runners, or authoring workflow.
* Exit criteria (all required):
  - All 28 active skill packages now have Doctrine source owners and current receipts.
  - Every emitted runtime package is self-contained.
  - Authoring/review/publish skills retain their trigger boundaries, workflow orders, output contracts, and model/runtime semantics.
  - Gemini still omits `code-review`.
* Rollback:
  - Restore the affected package's pre-port runtime files from git and remove or ignore its emit target until parity is repaired.

## Phase 7 — Generate root instructions and align public docs

* Goal: Make repo instructions and public install docs explain the new architecture without historical backstory or duplicated stale truth.
* Work: Move root instruction ownership to Doctrine and align docs with `Makefile` and emitted runtime reality.
* Checklist (must all be done):
  - Emit `AGENTS.md` from `prompts/repo_home/SKILL.prompt`.
  - Emit `CLAUDE.md` as a thin shim that points to `AGENTS.md` and does not duplicate repo rules.
  - Ensure `AGENTS.md` explains where Doctrine source lives, where emitted runtime files land, how install targets work, and which verification command applies to each changed surface.
  - Ensure `AGENTS.md` requires `$doctrine-learn`, `$skill-authoring`, `$prompt-authoring`, and `$agents-md-authoring` for future instruction-bearing work.
  - Update `README.md` and `docs/arch_skill_usage_guide.md` for the source/runtime split, install matrices, Gemini frontmatter stripping, hook behavior, stale cleanup, remote install, and verification commands.
  - Remove or rewrite live docs/comments/instructions that still say runtime `SKILL.md` files are the long-term hand-authored source.
  - Keep deeper architecture detail in docs, not always-on root instructions.
* Verification (required proof):
  - Run root-doc Doctrine emit.
  - Re-read `AGENTS.md`, `CLAUDE.md`, `README.md`, and `docs/arch_skill_usage_guide.md`.
  - Verify every path and command added to docs with `rg`.
  - Run `npx skills check` if runtime package text changed in the same phase.
  - Run `make verify_install` if install docs changed alongside install behavior.
* Docs/comments (propagation; only if needed):
  - This phase owns the docs propagation; no separate docs cleanup plan may contradict it.
* Exit criteria (all required):
  - A fresh agent can identify source owners, emitted runtime locations, install targets, and verification commands without reading historical chat.
  - Root instructions are compact and generated from the chosen source owner.
  - Public docs and Makefile matrices agree.
  - No live doc presents archived command files or hand-authored runtime `SKILL.md` files as the current source architecture.
* Rollback:
  - Restore previous root docs and public docs, then regenerate from corrected `prompts/repo_home/SKILL.prompt` before retrying.

## Phase 8 — Run suite-wide parity, install verification, and completion audit

* Goal: Prove the Doctrine-emitted suite preserves the old runtime contract and is ready for the epic to advance.
* Work: Validate the full source-to-runtime path, installed surfaces, docs alignment, and no-loss requirements.
* Checklist (must all be done):
  - Emit every configured Doctrine skill, shared-runtime, and root-doc target from a clean state.
  - Verify every emitted skill receipt.
  - Confirm every live skill package has a Doctrine source owner and a current emitted runtime output.
  - Confirm no installed runtime package contains `prompts/` or disposable `build/` subtrees.
  - Confirm all 28 agents/Codex skills, all 28 Claude Code skills, all 24 Gemini skills, and `_shared` install as before.
  - Confirm Gemini frontmatter stripping still occurs and Gemini omissions remain unchanged.
  - Confirm Codex and Claude hook verification still points at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`.
  - Confirm archived command files remain retired and are not runtime dependencies.
  - Run a final no-loss review against the parity matrix for triggers, metadata, workflows, references, scripts, and install semantics.
  - Run a Codex `gpt-5.4` `xhigh` fresh consult or epic critic on the completion claim before marking the sub-plan complete.
* Verification (required proof):
  - Run Doctrine emit for all configured targets.
  - Run `doctrine.verify_skill_receipts` for all skill targets.
  - Run `npx skills check`.
  - Run `make verify_install`.
  - Run `make -n remote_install HOST=example.invalid NO_GEMINI=1` and re-read `remote_install` for source/build exclusion and matrix parity.
  - Re-read root/public docs and verify added paths/commands with `rg`.
  - Record the fresh consult or critic artifact path and verdict in the epic/sub-plan logs.
* Docs/comments (propagation; only if needed):
  - Update this plan, the epic doc, and any worklog with final verification evidence and residual risks.
* Exit criteria (all required):
  - All active skills are Doctrine-authored, receipt-backed, and self-contained at runtime.
  - All redundancy identified by the parity/consolidation sweep is either folded into shared components or has an explicit local reason.
  - Install behavior, runtime matrices, hooks, stale cleanup, and Gemini behavior match the frozen contract.
  - Public docs and root instructions match the implemented source/runtime architecture.
  - Fresh Codex `gpt-5.4` `xhigh` review finds no blocking scope drift or no-loss failure.
* Rollback:
  - Revert the failing package group or docs/root-instruction sync to the last verified state, keep the parity evidence, and rerun the smallest affected verification set before continuing.
<!-- arch_skill:block:phase_plan:end -->

# 8) Verification Strategy (common-sense; non-blocking)

## 8.1 Unit tests (contracts)

No unit tests are expected for this docs-only sub-plan unless later planning changes introduce deterministic tooling.

## 8.2 Integration tests (flows)

For planning-only passes in this sub-plan, verification is doc re-read and path/command existence checks only. Later implementation phases should layer checks by changed surface: Doctrine emit and receipt verification after source changes, emitted-vs-current parity review before runtime sync, `npx skills check` after runtime package changes under `skills/`, targeted `make verify_*` for install-path changes, and `make verify_install` when install behavior changes or full install validation is intentionally requested.

## 8.3 E2E / device tests (realistic)

No E2E or device tests are in scope for this docs-only architecture sub-plan.

# 9) Rollout / Ops / Telemetry

## 9.1 Rollout plan

No rollout happens in this sub-plan. The output is a plan artifact used by later sub-plans.

## 9.2 Telemetry changes

None.

## 9.3 Operational runbook

Later sub-plans must keep install and recovery commands aligned across `Makefile`, `README.md`, and emitted skills. This sub-plan only records the intended architecture and verification map.

<!-- arch_skill:block:consistency_pass:start -->
## Consistency Pass

- Reviewers: explorer 1, explorer 2, self-integrator
- Scope checked:
  - Frontmatter, TL;DR, Sections 0-10, and helper blocks against the epic gate.
  - Section 7 against obligations from Sections 0.4, 5, 6, and 8.
  - Current architecture, target architecture, call-site audit, verification strategy, rollout, and decision logs for stale or contradictory planning truth.
  - Epic orchestration state for model/runtime, status, and no-advance-before-critic requirements.
- Findings summary:
  - Explorer 1 initially blocked completion-consult preparation because the doc did not yet include a concrete package-level source-owner/parity matrix and Section 7 still left a representative package/helper choice open.
  - Explorer 2 found stale Section 3.3 and external-research text that still described `deep_dive_pass_2` as future work.
  - Explorer 2 found that Section 7 did not carry the no-`doctrine.skill.lock` rule for first-party local sources or a concrete remote-install proof burden.
  - Self-integration found the stale `planning_passes` marker and a decision-log consequence that still said Section 7 was unwritten.
- Integrated repairs:
  - Updated `planning_passes` to record `phase_plan`, `consistency_pass`, and the pending completion-consult/critic gate.
  - Converted Section 3.3 and the external-research decision-gap text from future pass-2 inputs into consumed decision provenance.
  - Added Section 6.1 and Section 6.2 matrices mapping every live package, shared file group, script-bearing package, runtime metadata set, install target, root/public doc surface, receipt/lock policy, and verification owner to current and target owners.
  - Chose `pr-authoring` as the representative Phase 2 scaffold package and `scripts/list_doctrine_skill_targets.py` as the target-discovery helper.
  - Carried the no-lock rule and remote-install dry-run/re-read proof into Section 7.
  - Repaired the stale decision-log consequence for Section 7.
- Remaining inconsistencies:
  - none
- Unresolved decisions:
  - none
- Unauthorized scope cuts:
  - none
- Decision-complete:
  - yes, for sub-plan 1 architecture planning and completion-critic handoff.
- Decision: proceed to implement? no — do not start sub-plan 2 until a Codex `gpt-5.4` `xhigh` completion consult or epic critic passes.
<!-- arch_skill:block:consistency_pass:end -->

<!-- arch_skill:block:completion_consult:start -->
## Completion Consult

- Runtime/model/effort: Codex `gpt-5.4` `xhigh`
- Runs:
  - `/tmp/fresh-consult/arch-epic-subplan1-completion-20260426T131145Z-pwMkGt/`
    - Verdict: `fail`
    - Blocking findings:
      - Section 4.2 overstated current `remote_install` behavior as remote-checkout plus remote verification. Repaired to say it directly uses `ssh`/`scp` for cleanup, copy, hook wiring, and Gemini frontmatter stripping, and does not run remote `make verify_install` or remote `verify_*` targets today.
      - Section 4.2 overstated the Gemini boundary as excluding all hook-backed controller packages. Repaired to say Gemini installs the 24 `GEMINI_SKILLS` packages, including several skills that have hook-backed behavior in Codex/Claude, but Gemini receives them only as prompt-readable packages with no Stop-hook continuation surface and omits `arch-loop`, `delay-poll`, `wait`, and `code-review`.
    - Non-blocking finding:
      - `docs/arch_skill_usage_guide.md` install inventory drifts from `README.md`/`Makefile` by omitting `pr-authoring`, `stepwise`, and `arch-epic`; this remains a later docs-alignment obligation already covered by this plan.
  - `/tmp/fresh-consult/arch-epic-subplan1-completion-rerun-20260426T131907Z-3fDeiW/`
    - Verdict: `fail`
    - Blocking findings:
      - Section 7 still used the false shorthand that Gemini omits hook-backed packages. Repaired the pattern sweep and Phase 5 exit criterion to preserve the exact 24-skill `GEMINI_SKILLS` surface and the four specific omissions: `arch-loop`, `delay-poll`, `wait`, and `code-review`.
      - Section 2.1 overstated current `AGENTS.md` as already requiring `$doctrine-learn` and `$prompt-authoring`. Repaired the current-state text to say live `AGENTS.md` routes skill package work to `$skill-authoring`, `AGENTS.md` work to `$agents-md-authoring`, and workflow execution to matching shipped skills; the `$doctrine-learn`/`$prompt-authoring` requirement is target root-instruction work.
    - Non-blocking finding:
      - Same usage-guide drift as the first consult; still deferred to the planned docs-alignment phase.
  - `/tmp/fresh-consult/arch-epic-subplan1-completion-rerun2-20260426T132653Z-9g0nR0/`
    - Verdict: `pass-with-notes`
    - Blocking findings: none
    - Non-blocking findings:
      - `docs/arch_skill_usage_guide.md` still omits `pr-authoring`, `stepwise`, and `arch-epic` from some suite/install lists; this remains deferred to the planned docs-alignment phase.
      - Section 6.5 used `skills/doctrine-learn` shorthand for external Doctrine refs; repaired to `../doctrine/skills/doctrine-learn`.
- Current verdict: `pass-with-notes`; no blocking findings
<!-- arch_skill:block:completion_consult:end -->

# 10) Decision Log (append-only)

## 2026-04-26 - Initial North Star seed

Context

This doc was created as sub-plan 1 of `docs/EPIC_ARCH_SKILL_DOCTRINE_PORT_2026-04-26.md`.

Options

- Start by porting skills immediately.
- Start by freezing behavior and choosing the Doctrine source architecture.

Decision

Start with behavior freeze and architecture selection. The epic explicitly requires no lost nuance, no lost meaning, consistent install behavior, and shared Doctrine components; those requirements need an inventory and target architecture before any mass port.

Consequences

This sub-plan is docs/planning only. Later sub-plans own scaffold changes, shared component creation, package porting, repo-instruction rewrites, and final verification.

Follow-ups

- Fold the Codex `gpt-5.4` `xhigh` fresh consult result from `/tmp/fresh-consult/arch-epic-subplan1-20260426T121854Z/` into this doc if it reports a blocking no-loss constraint.

## 2026-04-26 - Fresh consult no-loss constraints folded

Context

The Codex `gpt-5.4` `xhigh` fresh consult at `/tmp/fresh-consult/arch-epic-subplan1-20260426T121854Z/` returned `pass-with-notes` with no blocking findings.

Options

- Leave the notes for later research and keep the initial North Star seed minimal.
- Fold the no-loss constraints into Section 0 now so later planning cannot miss them.

Decision

Fold the notes into Section 0 and supporting sections now.

Consequences

The sub-plan now explicitly freezes runtime-specific install behavior, root-instruction source ownership, trigger/runtime metadata semantics, and structure-preserving transfer for instruction-bearing content.

Follow-ups

- Research and deep-dive must turn these constraints into a concrete behavior inventory, target architecture, and parity matrix.

## 2026-04-26 - North Star approved under autonomous epic gate

Context

The epic was approved for autonomous execution through `$arch-loop`, `$arch-epic`, `$arch-step`, and `$fresh-consult`. The Codex `gpt-5.4` `xhigh` fresh consult returned `pass-with-notes` with no blocking findings, and the useful no-loss notes were folded into Section 0 before this gate.

Options

- Wait for a separate manual confirmation of this sub-plan's North Star.
- Treat the user's autonomous approval plus the no-blocker fresh consult as sufficient North Star confirmation for this sub-plan.

Decision

Treat the existing autonomous approval and no-blocker consult as sufficient. This doc is now `status: active`.

Consequences

The sub-plan may proceed to planning once the governing controller can safely run the next `$arch-step` command.

Follow-ups

- Arm `$arch-step auto-plan` only when doing so will not create multiple active controller states for the same session.

## 2026-04-26 - Intent-derived: planning stages run under arch-loop controller

Blocker: `$arch-step auto-plan` normally arms `.codex/auto-plan-state.<SESSION_ID>.json`, but `$arch-loop` is already armed for this same session. The installed Stop hook fails loudly when multiple controller states are armed for one session.

Consulted: Section 0.4 acceptance evidence, Section 0.5 invariants, the epic Decision Log, and the user's approval to keep going without further pauses.

Intent says: preserve the same stage order and behavior while avoiding controller-state conflicts; do not create runtime shims or fake automation.

Decision: run sub-plan 1 planning as explicit, one-stage-per-pass `$arch-step` work under the active `$arch-loop`: research, deep-dive pass 1, deep-dive pass 2, phase-plan, and consistency-pass. Do not arm a nested `auto-plan` state while the active `arch-loop` state exists.

Consequences: The same DOC_PATH remains the planning ledger. At that point the epic recorded sub-plan 1 as `planning`; later passes update the epic status as the gate advances. The Stop hook's arch-loop evaluator continues to choose the next bounded parent pass.

## 2026-04-26 - Intent-derived: Doctrine target architecture selected

Context

Deep-dive pass 2 needed to turn Section 3.3 inputs into one target architecture before phase planning.

Options

- Move Doctrine sources outside `skills/` and keep `skills/` runtime-only.
- Put Doctrine sources under `skills/<slug>/prompts/` and update install copying so source/build subtrees are never installed.
- Replace the current install system with a `lessons_studio`-style local symlink tree.

Decision

Use `skills/<slug>/prompts/SKILL.prompt` as the first-party skill source path, `shared/prompts/arch_skill/` for shared source declarations, `prompts/repo_home/SKILL.prompt` for generated root instructions, and `prompts/shared_runtime/SKILL.prompt` for installed shared runtime references. Emit to disposable build trees, verify receipts, then sync parity-approved runtime outputs into the live `skills/` surface. Keep `Makefile` as the install owner and preserve the current agents/Codex, Claude Code, and Gemini runtime matrices.

Consequences

The later scaffold must add Doctrine config, build/verify/sync targets, and runtime-subset install copying that excludes `prompts/` and `build/`. Package porting must be behavior-preserving and receipt-backed. Section 7 was later filled by the `phase-plan` pass; no scaffold or package port has been implemented in this sub-plan.

## 2026-04-26 - Consistency pass repaired stale planning truth

Context

The arch-step consistency-pass equivalent cold-read Sections 0-10 against the epic gate with two Codex `gpt-5.4` `xhigh` explorers and a parent integration read.

Options

- Treat the phase-plan as complete and prepare the completion critic immediately.
- Repair the stale planning truth and missing source-owner/parity matrix before critic preparation.

Decision

Repair before critic preparation. The pass added the live package/source-owner matrix, shared/support surface matrix, concrete Phase 2 representative package and helper choices, no-lock and remote-install proof obligations, and stale-text fixes.

Consequences

This sub-plan is decision-complete for architecture planning, but implementation still must not start. The next gate is a Codex `gpt-5.4` `xhigh` completion consult or epic critic; sub-plan 2 stays blocked until that critic passes.

## 2026-04-26 - Completion consult passed and sub-plan 1 closed

Context

Two Codex `gpt-5.4` `xhigh` completion consult runs found blocking stale-current-state statements and Gemini/runtime shorthand. Those blockers were repaired, then the rerun at `/tmp/fresh-consult/arch-epic-subplan1-completion-rerun2-20260426T132653Z-9g0nR0/` returned `pass-with-notes` with no blocking findings.

Decision

Treat sub-plan 1 as complete. The non-blocking usage-guide inventory drift remains deferred to the later docs-alignment phase already covered by this plan.

Consequences

The epic may start sub-plan 2 at `docs/ADD_DOCTRINE_SOURCE_AND_EMIT_SCAFFOLD_2026-04-26.md`.
