---
title: "Arch Skill - Doctrine Source And Emit Scaffold - Architecture Plan"
date: 2026-04-26
status: active
fallback_policy: forbidden
owners: [aelaguiz]
reviewers: [fresh-consult, arch-epic]
doc_type: phased_refactor
related:
  - docs/EPIC_ARCH_SKILL_DOCTRINE_PORT_2026-04-26.md
  - docs/FREEZE_CURRENT_BEHAVIOR_AND_CHOOSE_DOCTRINE_ARCHITECTURE_2026-04-26.md
  - Makefile
  - README.md
  - AGENTS.md
  - skills/
  - ../doctrine
  - ../lessons_studio
---

# TL;DR

- **Outcome:** Add the first runnable Doctrine source/build scaffold for `arch_skill` without porting the whole skill suite.
- **Problem:** Sub-plan 1 chose a Doctrine architecture, but this repo still has no `pyproject.toml`, locked Doctrine environment, source prompt roots, emit targets, receipt checks, or Makefile build/sync commands.
- **Approach:** Protect the install surface first, then add a minimal Doctrine scaffold that can emit a representative package, generated root docs, and generated shared runtime references into disposable build outputs with receipt verification.
- **Plan:** Start from the sub-plan 1 architecture, prove install copy excludes source/build trees, add Doctrine config and source roots, emit `pr-authoring` plus root/shared-runtime targets, verify receipts, and sync only parity-approved runtime output.
- **Non-negotiables:** This sub-plan creates the scaffold only. It does not port the whole suite, does not change runtime behavior, does not change skill matrices, does not add first-party `doctrine.skill.lock`, and does not let installed packages depend on hidden Doctrine source.

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
north_star_gate: pass-with-notes 2026-04-26
deep_dive_pass_1: done 2026-04-26
external_research_grounding: done 2026-04-26
deep_dive_pass_2: done 2026-04-26
phase_plan: done 2026-04-26
consistency_pass: done 2026-04-26
implementation_authorization_consult: pending
completion_consult: pending
recommended_flow: north star gate -> deep dive -> external research grounding -> deep dive again -> phase plan -> consistency pass -> implementation authorization consult/critic -> implement Phase 1 through Phase 6 -> completion consult or epic critic -> next sub-plan
note: The planning artifact is decision-complete after consistency-pass repair, but scaffold implementation is still blocked until the Codex gpt-5.4 xhigh implementation authorization consult/critic records no blocking findings. The completion consult remains part of Phase 6 after implementation.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

When this sub-plan is complete, `arch_skill` will have a working Doctrine source/build scaffold that can emit a representative runtime skill package, generated root instruction files, and generated shared runtime references from configured source targets, while preserving the current live install contract. A later agent should be able to run the documented scaffold commands, inspect receipts, and know exactly which generated outputs are safe to sync into `skills/` and which source/build files must never be installed.

## 0.2 In scope

- Add the minimum Doctrine project scaffold: `pyproject.toml`, locked environment, compile roots, emit target registry, and any required generated-output ignores.
- Add repo-local shared prompt roots under `shared/prompts/arch_skill/` with the seed module files chosen in sub-plan 1.
- Add `prompts/repo_home/SKILL.prompt` as the source owner for generated `AGENTS.md` plus a thin `CLAUDE.md` shim, emitting to `build/repo_home/`.
- Add `prompts/shared_runtime/SKILL.prompt` as the source owner for installed shared runtime references, emitting to `build/shared_runtime/`.
- Add representative `skills/pr-authoring/prompts/SKILL.prompt` and a configured emit target because sub-plan 1 chose `pr-authoring` as the first scaffold package.
- Add `scripts/list_doctrine_skill_targets.py` as the selected target-discovery helper for deriving configured skill targets from `pyproject.toml`.
- Add Makefile targets for Doctrine emit, receipt verification, and explicit parity-approved sync into live runtime files.
- Update the install copy boundary so runtime installs exclude `prompts/` and disposable `build/` subtrees before those subtrees exist broadly.
- Preserve agents/Codex, Claude Code, and Gemini matrices, `_shared` installation, Gemini frontmatter stripping, hook wiring, stale-surface cleanup, remote install behavior, and archived command cleanup.
- Update only the minimum docs/root instruction wording needed to prevent future agents from hand-editing emitted outputs once the scaffold exists.

## 0.3 Out of scope

- Porting every live skill package to Doctrine.
- Extracting all shared arch-suite doctrine into complete shared components.
- Rewriting the public docs and root instructions as their final epic form.
- Changing the supported runtime matrix or adding/removing installed skills.
- Replacing current hook/controller scripts, state behavior, runner semantics, or install roots.
- Introducing first-party local `doctrine.skill.lock`.
- Using `../doctrine`, `../lessons_studio`, or archived command files as runtime dependencies.

## 0.4 Definition of done (acceptance evidence)

- Install copy behavior excludes `prompts/` and disposable `build/` subtrees for local and remote installs without changing active package matrices.
- The repo has a runnable Doctrine config and locked environment.
- The configured Doctrine scaffold can emit the representative `pr-authoring` package, root-doc package, and shared-runtime package into disposable build outputs.
- Every emitted skill target has a current `SKILL.source.json` receipt.
- Root-doc and shared-runtime outputs are emitted as `SKILL.prompt` skill-package targets with current `SKILL.source.json` receipts, plus explicit compile/emit proof and sync/parity evidence.
- First-party local sources do not create or require `doctrine.skill.lock`.
- A narrow sync path exists and syncs only parity-approved runtime files into the live `skills/` surface.
- `npx skills check` runs after synced runtime package changes.
- `make verify_install` runs if install behavior changes or full installed-surface validation is intentionally performed.
- Added commands and paths are reflected in the minimum necessary docs/root instructions and verified with `rg`.
- A Codex `gpt-5.4` `xhigh` completion consult or epic critic finds no blocking scaffold, install-boundary, receipt, or no-loss problem before this sub-plan completes.

## 0.5 Key invariants (fix immediately if violated)

- `skills/` remains the live runtime install surface.
- `prompts/` and `build/` subtrees are source/build internals and must not be installed.
- Runtime packages stay self-contained after install.
- `Makefile` remains the install owner.
- `AGENTS.md` and `CLAUDE.md` may become generated outputs only through the chosen Doctrine root instruction source; until synced, current root instructions remain authoritative.
- Scripts, schemas, fixtures, and `agents/openai.yaml` are bundled runtime assets unless a later pass explicitly chooses a Doctrine-authored replacement.
- No runtime fallback, dual live source, or hidden source dependency is approved.

# 1) Key Design Considerations

## 1.1 Priorities

1. Preserve the live install surface before adding source/build files inside `skills/`.
2. Make the smallest scaffold that proves the chosen Doctrine architecture is executable.
3. Keep receipts and sync boundaries explicit enough to prevent hand-editing emitted runtime files.
4. Avoid whole-suite porting until the scaffold and no-loss method are proven.
5. Keep verification proportional to the changed surface.

## 1.2 Constraints

- Sub-plan 1 is the architecture source for this work and must not be contradicted.
- Current install commands copy package directories directly enough that source/build exclusion has to be solved before broad source tree creation.
- `pr-authoring` is the representative scaffold package selected by sub-plan 1.
- `Makefile`, `README.md`, `docs/arch_skill_usage_guide.md`, `AGENTS.md`, and `CLAUDE.md` form one install/source-instruction contract family.
- The active arch-loop requirement pins consults and critics to Codex `gpt-5.4` at `xhigh`.

## 1.3 Architectural principles

- Add source ownership without changing runtime behavior.
- Emit to disposable outputs first; sync live runtime files only after parity approval.
- Receipts prove source-to-runtime lineage; broad install checks do not replace receipt checks.
- Shared modules should seed the architecture, not absorb local skill judgment prematurely.
- Runtime code stays code. Doctrine source may author instructions and references, not hook scheduling or subprocess dispatch.

## 1.4 Known tradeoffs

- The representative scaffold will prove the path before the shared doctrine is complete, so some duplication may remain temporarily.
- Generating root instructions early helps future agents, but this sub-plan should avoid turning into the full docs rewrite.
- A simple target-discovery helper may be worth adding now to avoid duplicating emit target lists, but it should stay narrow and config-derived.

# 2) Problem Statement

## 2.1 What exists today

The repo currently has a hand-authored runtime `skills/` tree, `Makefile` install and verification behavior, public install docs, and root instructions. It has no Doctrine config, no locked Doctrine environment, no prompt source roots, no build outputs, no source receipts, and no sync commands.

## 2.2 What's broken / missing

- There is no executable source/build path for the architecture chosen in sub-plan 1.
- Runtime install copying does not yet have a documented source/build exclusion boundary.
- Future agents do not yet have commands for emitting, verifying receipts, or syncing parity-approved outputs.
- Root/public docs do not yet explain that some runtime files will become emitted outputs.

## 2.3 Constraints implied by the problem

- The scaffold must be introduced before whole-suite porting.
- The install boundary must be safe before source/build subtrees appear broadly under `skills/`.
- Verification must distinguish Doctrine emit/receipt proof from existing skill package and install checks.

# 3) Research Grounding

<!-- arch_skill:block:research_grounding:start -->
This pass used local source grounding rather than web research because the relevant external truth is the adjacent `../doctrine` authoring source and the adjacent `../lessons_studio` Doctrine implementation precedent named by the epic. The verified anchors are:

## 3.1 Sub-plan 1 architecture anchors

- `docs/FREEZE_CURRENT_BEHAVIOR_AND_CHOOSE_DOCTRINE_ARCHITECTURE_2026-04-26.md` Section 5 chooses Doctrine as the source layer while keeping `skills/` as the live runtime install surface.
- Section 5 chooses `pyproject.toml`, `uv.lock`, `shared/prompts/arch_skill/`, `prompts/repo_home/SKILL.prompt`, `prompts/shared_runtime/SKILL.prompt`, `skills/<slug>/prompts/SKILL.prompt`, and disposable build outputs as the future source/build shape.
- Section 5 requires runtime installs to exclude `prompts/` and `build/`, preserve agents/Codex 28, Claude Code 28, Gemini 24, and keep Gemini omitting only `arch-loop`, `delay-poll`, `wait`, and `code-review`.
- Section 6 chooses `skills/pr-authoring/` as the representative scaffold package because it is installed in all matrices, has one bundled reference, has `agents/openai.yaml`, and has no scripts or fixtures.
- Section 6 chooses `prompts/shared_runtime/SKILL.prompt` as the source owner for installed `_shared` runtime references, with `skills/_shared/controller-contract.md` staying installed beside every runtime root.
- Section 7 says Phase 1 must protect local and remote runtime install copy semantics before source/build subtrees are broadly added, and Phase 2 may then add the Doctrine scaffold and representative emit/sync path.
- Section 7 requires `uv sync`, Doctrine emit, `doctrine.verify_skill_receipts`, `npx skills check`, and `make verify_install` during implementation, not during this planning-only pass.

## 3.2 Doctrine source anchors

- `../doctrine/skills/doctrine-learn/prompts/refs/skills_and_packages.prompt` says a real skill package source root is `SKILL.prompt`; it emits a real tree with `SKILL.md`, `SKILL.source.json`, bundled references, bundled scripts/assets, and runtime metadata such as `agents/openai.yaml`.
- The same reference says ordinary bundled files copy byte-for-byte under the same relative path. That preserves `skills/pr-authoring/references/pr-body-scaffold.md` and `skills/pr-authoring/agents/openai.yaml` in the first scaffold package.
- `../doctrine/skills/doctrine-learn/prompts/refs/emit_targets.prompt` says configured emit targets live in `[tool.doctrine.emit]` in `pyproject.toml`, with required `name`, `entrypoint`, and `output_dir` fields.
- The emit target reference says `emit_skill` accepts `SKILL.prompt`, `emit_docs` accepts `AGENTS.prompt` or `SOUL.prompt`, and emitted trees should land in disposable build output directories.
- The same reference says `source_root`, `source_id`, and `lock_file` are for external source-root targets, and the lock file must stay outside emitted skill trees. This confirms the sub-plan 1 no-lock decision for first-party local `arch_skill` sources.
- `../doctrine/skills/doctrine-learn/prompts/refs/imports_and_refs.prompt` says `additional_prompt_roots` is the config mechanism for shared prompt roots and duplicate module identities fail loud.
- `../doctrine/skills/doctrine-learn/prompts/refs/verify_and_ship.prompt` says emitted Markdown and sidecars are compiler-owned, should not be hand-edited, and should be verified with the narrow command for the changed surface.

## 3.3 `lessons_studio` precedent anchors

- `../lessons_studio/pyproject.toml` uses `doctrine-agents>=4.0.0,<5`, `[tool.uv] package = false`, and an editable local `doctrine-agents = { path = "../doctrine", editable = true }` source.
- Its `[tool.doctrine.compile]` uses `additional_prompt_roots`, matching the selected `shared/prompts/arch_skill/` shape for this repo.
- Its local skill targets use `skills/<name>/prompts/SKILL.prompt` and `skills/<name>/build`, matching the selected representative `skills/pr-authoring/prompts/SKILL.prompt` -> `skills/pr-authoring/build` scaffold.
- Its external psmobile targets use `source_root`, `source_id`, and `lock_file = "doctrine.skill.lock"`, confirming that locks belong to external source roots rather than first-party local sources.
- Its root instruction generator is configured at `prompts/claude_home/SKILL.prompt` and copied from `build/claude_home/` by the Makefile. This is the closest adjacent precedent for the sub-plan 1 choice of `prompts/repo_home/SKILL.prompt`.
- `../lessons_studio/Makefile` derives skill target names from `scripts/list_doctrine_skill_targets.py`, emits skills through `uv run --locked python -m doctrine.emit_skill`, emits root instructions through a separate target, and has a `clean-build` target.
- `../lessons_studio/scripts/list_doctrine_skill_targets.py` parses `pyproject.toml` with `tomllib`, selects targets whose `output_dir` starts with `skills/`, and can print target names or output dirs for Makefile/shell use.
- `../lessons_studio/scripts/build_skills.sh` clears emitted output dirs, emits configured skill targets, verifies receipts, and then wires local symlinks. This repo should reuse the config-derived target discovery and clean-build ideas, but not the symlink install strategy because `arch_skill` uses Makefile copy installs, remote `scp`, hook wiring, and Gemini frontmatter stripping.

## 3.4 Decisions carried into deep-dive pass 2

- `scripts/list_doctrine_skill_targets.py` is selected, not still open. It should stay narrow and derive targets from `pyproject.toml`.
- `prompts/repo_home/SKILL.prompt` is the chosen source owner for root docs because sub-plan 1 chose it and `lessons_studio` proves a nearby `SKILL.prompt` root-doc generator pattern. The scaffold must prove this target emits compact `AGENTS.md` and thin `CLAUDE.md`; a compiler rejection is an implementation blocker that reopens planning, not a live entrypoint switch.
- `prompts/shared_runtime/SKILL.prompt` is the chosen source owner for installed `_shared` runtime references. It emits as a skill-package target, so it must receive `SKILL.source.json` receipt verification plus file-level sync/parity evidence for the installed `_shared` files.
- First-party local sources must not create or require `doctrine.skill.lock`; future external source-root targets may use locks only with `source_root` and `source_id`.
- The scaffold can add source/config/build commands only after the phase-plan, consistency, and Codex `gpt-5.4` `xhigh` implementation authorization gates pass. This pass authorizes planning truth, not implementation.
<!-- arch_skill:block:research_grounding:end -->

<!-- arch_skill:block:external_research:start -->
## External Research Grounding

- Scope: local adjacent source grounding only, because the requested external anchors are `../doctrine` and `../lessons_studio`.
- Adopted: `pyproject.toml` emit target registry, `additional_prompt_roots`, first-party `skills/<slug>/prompts/SKILL.prompt` sources, disposable `skills/<slug>/build` outputs, config-derived target discovery, receipt verification for skill targets, and Makefile-owned emit/clean/sync commands.
- Adopted with guardrail: `prompts/repo_home/SKILL.prompt` as the root-doc source owner, with a hard compile/emit smoke gate before sync. There is no implementation-time alternate entrypoint path; a compiler rejection reopens planning.
- Rejected for this repo: `lessons_studio` symlink install wiring and first-party local `doctrine.skill.lock`.
<!-- arch_skill:block:external_research:end -->

# 4) Current Architecture

<!-- arch_skill:block:current_architecture:start -->
## 4.1 On-disk structure

Current checked-in source is still a hand-authored runtime skill repository. There is no Doctrine scaffold in this repo yet:

- Missing at repo root today: `pyproject.toml`, `uv.lock`, `prompts/`, `build/`, `shared/`, and `scripts/`.
- Missing across this repo today: `*.prompt`, `SKILL.source.json`, and `doctrine.skill.lock`.
- `.gitignore` currently ignores `.env`, `gemini/`, `.codex/*-state*.json`, `.claude/arch_skill/`, `__pycache__/`, and `*.py[cod]`. It does not yet name disposable Doctrine build outputs.
- `skills/` currently contains 28 live package directories plus one shared runtime directory at `skills/_shared/`.
- The live skill tree currently has 23 `agents/openai.yaml` files, 24 script files under script-bearing packages, no `assets/` paths, no `prompts/` source trees, and no Doctrine receipts.
- `skills/_shared/controller-contract.md` is the only installed shared runtime directory named by `Makefile` through `SHARED_DIRS := _shared`.

The representative package selected by sub-plan 1 is concrete and simple enough for the scaffold:

- `skills/pr-authoring/SKILL.md` is a prompt-only runtime skill package.
- `skills/pr-authoring/references/pr-body-scaffold.md` is the one bundled reference.
- `skills/pr-authoring/agents/openai.yaml` is runtime metadata and must copy through.
- `skills/pr-authoring/` has no scripts, fixtures, or assets, so it is a low-risk first package for proving source, emit, receipt, and sync.

Root instructions and public docs are hand-authored today:

- `AGENTS.md` says `skills/` is the live runtime surface and `Makefile` plus `README.md` own the Codex, Claude Code, and Gemini install surface.
- `AGENTS.md` currently routes skill package changes to `$skill-authoring`, `AGENTS.md` changes to `$agents-md-authoring`, and fresh second-opinion work to `$fresh-consult`. It does not yet describe Doctrine source ownership for this repo.
- `CLAUDE.md` is a thin shim that tells Claude Code to read `AGENTS.md`.
- `README.md` is the public install, runtime matrix, skill inventory, feature-gate, remote-install, and verification surface.

Adjacent Doctrine evidence checked in this pass:

- `../doctrine/skills/doctrine-learn/prompts/refs/skills_and_packages.prompt` says a real skill package source is `SKILL.prompt`, ordinary bundled files such as `references/`, `scripts/`, `assets/`, and `agents/openai.yaml` copy byte-for-byte, and every skill package emits `SKILL.source.json`.
- `../doctrine/skills/doctrine-learn/prompts/refs/emit_targets.prompt` says all configured emit targets live in `pyproject.toml`; `emit_docs` accepts `AGENTS.prompt` or `SOUL.prompt`; `emit_skill` accepts `SKILL.prompt`; `lock_file` is for external `source_root` targets and must stay outside emitted skill trees.
- `../doctrine/skills/doctrine-learn/prompts/refs/imports_and_refs.prompt` says `additional_prompt_roots` is the configured way to expose shared prompt roots, and duplicate dotted module identities fail loud.
- `../doctrine/skills/doctrine-learn/prompts/refs/verify_and_ship.prompt` says emitted Markdown and sidecars such as `SKILL.source.json` are compiler-owned and must not be hand-edited.
- `../lessons_studio/pyproject.toml` proves the nearby pattern: `doctrine-agents` in a locked Python project, `additional_prompt_roots`, many `[[tool.doctrine.emit.targets]]`, local `skills/<name>/prompts/SKILL.prompt` sources, external `source_root` targets with `doctrine.skill.lock`, and a root instruction target at `prompts/claude_home/SKILL.prompt`.
- `../lessons_studio/scripts/list_doctrine_skill_targets.py` is the selected helper pattern for deriving skill emit target names and output dirs from `pyproject.toml`.
- `../lessons_studio/scripts/build_skills.sh` clears emitted skill build outputs, runs `doctrine.emit_skill`, verifies receipts, then wires local `.claude/skills` and `.agents/skills` symlinks. This repo should reuse the target-discovery and clear-build lessons, but not the symlink install strategy.
- `../lessons_studio/Makefile` separates `skills`, `agent-homes`, and `clean-build`; that supports this repo's need to keep skill emits, root-doc emits, and cleanup as separate Makefile-owned operations.

## 4.2 Control paths (runtime)

Local install is Makefile-driven and currently copies whole runtime package directories:

- `make install` runs Codex stale-surface cleanup, agents/Codex skill install, Codex mirror cleanup, Codex hook install, Claude skill install, Claude hook install, and Gemini install unless `NO_GEMINI=1`.
- `agents_install_skill` removes old installed entries and then runs `cp -R skills/$$skill $(AGENTS_SKILLS_DIR)/$$skill` for each `SKILLS` entry.
- `claude_install_skill` runs the same whole-directory copy for each `CLAUDE_SKILLS` entry.
- `gemini_install_skill` runs the same whole-directory copy for each `GEMINI_SKILLS` entry, then strips YAML frontmatter from installed `SKILL.md`.
- Every runtime install copies `skills/_shared` wholesale beside the installed packages.
- `remote_install` recreates the same behavior over `ssh` and `scp -r`, including whole-directory skill copies, `_shared` copies, hook installation, stale-surface cleanup, and Gemini frontmatter stripping when Gemini is enabled.

That whole-directory copy is the key current scaffold risk. If this sub-plan adds `skills/<slug>/prompts/` or `skills/<slug>/build/` before changing the install copy boundary, the current local and remote install paths would install those source/build subtrees too. Therefore the first implementation phase must add a runtime-subset copy path before broad source/build trees appear under `skills/`.

Runtime matrices are Makefile-owned today:

- `SKILLS` installs 28 packages for agents/Codex.
- `CLAUDE_SKILLS` mirrors the same 28 packages for Claude Code.
- `GEMINI_SKILLS` installs 24 packages and omits `arch-loop`, `delay-poll`, `wait`, and `code-review`.
- `REMOVED_SKILLS` and `ARCHIVED_COMMAND_FILES` drive stale-surface cleanup and verification; these are part of install behavior, not Doctrine source.

Verification is also Makefile- and instruction-owned:

- `verify_install` expands to agents/Codex, Codex stale-surface/hook, Claude, hook-runner, and Gemini checks unless `NO_GEMINI=1`.
- `verify_agents_install`, `verify_claude_install`, and `verify_gemini_install` currently check installed `SKILL.md`, `_shared`, omitted/removed packages, and stale command files. They do not currently check that `prompts/` or `build/` are absent from installed packages because those paths do not exist yet.
- `verify_hook_runner` runs the installed controller runner's `--doctor`.
- `AGENTS.md` requires `npx skills check` after skill package changes under `skills/`, `make verify_install` when install behavior changes or installed-surface validation is intentional, and docs re-read plus `rg` for docs-only path/command changes.

Current public docs and runtime instructions expose this install path:

- `README.md` documents `make install`, `make install NO_GEMINI=1`, `make remote_install HOST=user@host`, `make verify_install`, feature-gate checks, installed skill lists, and manual hook recovery commands.
- `README.md` says Codex reads from `~/.agents/skills/`, Claude Code reads from `~/.claude/skills/`, and Gemini reads from `~/.gemini/skills/`.
- `README.md` describes the hook-backed controller contract at `skills/_shared/controller-contract.md` and the installed runner at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`.
- `CLAUDE.md` delegates to `AGENTS.md`; it has no separate install or Doctrine-source logic.

Adjacent Doctrine and `lessons_studio` control paths:

- Doctrine emit commands are command-specific: `python -m doctrine.emit_docs` for root instruction packages and `python -m doctrine.emit_skill` for skill packages.
- `doctrine.verify_skill_receipts` verifies skill package receipts; it is not the same proof surface as root-doc `emit_docs`.
- `lessons_studio/scripts/list_doctrine_skill_targets.py` reads `pyproject.toml` and derives target names or output dirs where `output_dir` starts with `skills/`.
- `lessons_studio/scripts/build_skills.sh` uses that helper to remove old build outputs, emit all configured skill package targets, and verify receipts.
- `lessons_studio/Makefile` emits root instructions through a separate `agent-homes` target and copies generated `AGENTS.md`/`CLAUDE.md` from `build/claude_home/` to the repo root.

## 4.3 Object model + key abstractions

Current repo objects:

- **Live runtime package:** `skills/<slug>/` with `SKILL.md`, optional `references/`, optional `scripts/`, optional `agents/openai.yaml`, and optional schemas/fixtures. This is the current source and install unit.
- **Representative scaffold package:** `skills/pr-authoring/`, a prompt-only package with one reference and `agents/openai.yaml`. It is installed in all runtime matrices and has no script assets.
- **Shared runtime directory:** `skills/_shared/`, currently only `controller-contract.md`, copied beside every runtime install root.
- **Active runtime matrix:** `SKILLS`, `CLAUDE_SKILLS`, and `GEMINI_SKILLS` in `Makefile`.
- **Install transform:** Gemini frontmatter stripping after copy; Codex/Claude hook installation; stale prompt-era command cleanup; old Codex skill mirror removal.
- **Root instruction files:** `AGENTS.md` and `CLAUDE.md`, currently hand-authored always-on instructions.
- **Public docs:** `README.md` and related docs, currently hand-authored and installation-facing.
- **Ignored runtime state:** `.codex/*-state*.json` and `.claude/arch_skill/`, not Doctrine source.

Target-adjacent Doctrine objects that do not exist here yet:

- **Doctrine project config:** `pyproject.toml` with `doctrine-agents`, compile roots, and emit target registry.
- **Locked environment:** `uv.lock`.
- **Shared prompt root:** `shared/prompts/arch_skill/` as configured by `additional_prompt_roots`.
- **Root-doc source package:** `prompts/repo_home/SKILL.prompt` for generating compact `AGENTS.md` and thin `CLAUDE.md`.
- **Shared-runtime source package:** `prompts/shared_runtime/SKILL.prompt` for generating installed shared references.
- **Skill source package:** `skills/pr-authoring/prompts/SKILL.prompt` for the representative package in this sub-plan.
- **Emitted build output:** `skills/pr-authoring/build/`, `build/repo_home/`, and `build/shared_runtime/`, all disposable.
- **Skill receipt:** `SKILL.source.json`, emitted by `emit_skill` for the representative skill target.
- **Lock file:** `doctrine.skill.lock`, not used for first-party local sources; reserved for future external `source_root` targets only.

## 4.4 Observability + failure behavior today

Current signals that exist before the scaffold:

- `npx skills check` validates changed skill packages after runtime files under `skills/` change.
- `make verify_install` validates installed active surfaces, hooks, `_shared`, removed-skill cleanup, and Gemini when enabled.
- Targeted Makefile checks exist for agents, Codex, Claude, Gemini, and hook runner health.
- Docs-only changes are verified by re-reading and `rg` path/command checks under `AGENTS.md`.
- Hook-backed controller failures are designed to fail loud through `arch_controller_stop_hook.py` verification and recovery commands.

Current gaps the scaffold must close:

- Install verification does not yet detect source/build subtree leakage because no source/build subtrees exist today.
- `.gitignore` does not yet protect disposable Doctrine build outputs.
- No emit command, receipt verification command, target-discovery helper, sync command, or root-doc emit command exists in this repo.
- No current command distinguishes skill-package receipts from root-doc/shared-runtime emit proof.
- Public docs and root instructions do not yet tell agents where Doctrine source will live or which emitted outputs are compiler-owned.

The North Star gate for this sub-plan ran as a Codex `gpt-5.4` `xhigh` fresh consult at `/tmp/fresh-consult/arch-epic-subplan2-north-star-20260426T133843Z-ZM7UJh/` and returned `pass-with-notes` with no blocking findings. The useful notes were folded into this pass: `scripts/list_doctrine_skill_targets.py` is no longer a reopened helper choice, and non-skill emitted outputs need explicit emit/sync/parity proof rather than skill receipt proof.

## 4.5 UI surfaces (ASCII mockups, if UI work)

No UI surface is in scope.
<!-- arch_skill:block:current_architecture:end -->

# 5) Target Architecture

<!-- arch_skill:block:target_architecture:start -->
## 5.1 On-disk structure

This sub-plan adds the smallest runnable Doctrine scaffold. It does not port the full suite.

```text
pyproject.toml
uv.lock
shared/prompts/arch_skill/
  controller_lifecycle.prompt
  install_runtime_invariants.prompt
  authoring_quality.prompt
  model_runtime.prompt
prompts/repo_home/SKILL.prompt
build/repo_home/
prompts/shared_runtime/SKILL.prompt
build/shared_runtime/
skills/pr-authoring/prompts/SKILL.prompt
skills/pr-authoring/build/
scripts/list_doctrine_skill_targets.py
```

The live runtime surface remains `skills/`. `skills/pr-authoring/SKILL.md`, `skills/pr-authoring/references/pr-body-scaffold.md`, and `skills/pr-authoring/agents/openai.yaml` are the representative runtime files that may be replaced only by parity-approved emitted output. `skills/_shared/controller-contract.md` remains installed beside all runtime roots and becomes the first shared-runtime output only after parity proof.

`build/`, `skills/*/build/`, and `skills/*/prompts/` are source/build internals. They are never installed into `~/.agents/skills`, `~/.claude/skills`, `~/.gemini/skills`, or remote runtime roots.

## 5.2 Doctrine config and emit targets

`pyproject.toml` owns:

- `[project]` with `doctrine-agents>=4.0.0,<5`.
- `[tool.uv] package = false`.
- `[tool.uv.sources] doctrine-agents = { path = "../doctrine", editable = true }` while this repo follows the adjacent local workspace pattern.
- `[tool.doctrine.compile] additional_prompt_roots = ["shared/prompts"]`.
- `[tool.doctrine.emit]` targets for the representative skill, root-doc source, and shared-runtime source.

Initial target names should be stable and readable:

- `pr-authoring`: `entrypoint = "skills/pr-authoring/prompts/SKILL.prompt"`, `output_dir = "skills/pr-authoring/build"`, emitted with `doctrine.emit_skill`, receipt-verified.
- `repo-home`: `entrypoint = "prompts/repo_home/SKILL.prompt"`, `output_dir = "build/repo_home"`, emitted with `doctrine.emit_skill` and receipt-verified before any root-doc sync.
- `shared-runtime`: `entrypoint = "prompts/shared_runtime/SKILL.prompt"`, `output_dir = "build/shared_runtime"`, emitted with `doctrine.emit_skill`, receipt-verified, and then synced only into approved `_shared` runtime files.

First-party local targets omit `source_root`, `source_id`, and `lock_file`. `doctrine.skill.lock` is reserved for future external source-root targets only.

## 5.3 Makefile control paths

`Makefile` remains the command owner. The target architecture adds Doctrine commands without replacing install commands:

- A runtime-subset copy helper used by agents/Codex, Claude Code, Gemini, `_shared`, and remote install copy paths. It must exclude `prompts/` and `build/`.
- `doctrine_list_skill_targets` as the Makefile target or variable path around `scripts/list_doctrine_skill_targets.py`.
- `doctrine_emit` to emit the configured scaffold targets into disposable build outputs.
- `doctrine_verify_receipts` to run `doctrine.verify_skill_receipts` for emitted skill-package targets.
- `doctrine_clean_build` to remove disposable emitted outputs.
- `doctrine_sync_approved` as an explicit parity gate. It may sync only named approved outputs from `skills/pr-authoring/build/`, `build/repo_home/`, or `build/shared_runtime/` into live runtime files.

Existing install targets continue to own local install, remote install, hook installation, stale-surface cleanup, Gemini frontmatter stripping, and verification. The runtime matrices remain unchanged: agents/Codex 28, Claude Code 28, Gemini 24, with Gemini still omitting `arch-loop`, `delay-poll`, `wait`, and `code-review`.

## 5.4 Object model

- **Doctrine project config:** root `pyproject.toml` and `uv.lock`.
- **Shared prompt module:** declarations in `shared/prompts/arch_skill/`, imported by scaffold sources but not installed at runtime.
- **Representative skill source package:** `skills/pr-authoring/prompts/SKILL.prompt`.
- **Representative emitted tree:** `skills/pr-authoring/build/`, disposable and receipt-backed.
- **Representative live runtime package:** `skills/pr-authoring/`, installed only after parity-approved sync.
- **Root-doc source package:** `prompts/repo_home/SKILL.prompt`.
- **Root-doc build output:** `build/repo_home/`, disposable and synced to `AGENTS.md`/`CLAUDE.md` only after approval.
- **Shared-runtime source package:** `prompts/shared_runtime/SKILL.prompt`.
- **Shared-runtime build output:** `build/shared_runtime/`, disposable and synced to `skills/_shared/` only after approval.
- **Receipt:** `SKILL.source.json` for every emitted skill-package target, including `pr-authoring`, `repo-home`, and `shared-runtime`; not a substitute for file-level parity proof before sync.
- **Approved sync:** the only path from disposable build output to live runtime files.

## 5.5 Invariants and boundaries

- Implementation remains unauthorized until Section 7 phase planning, the consistency gate, and the Codex `gpt-5.4` `xhigh` implementation authorization consult/critic all pass.
- Source/build internals must be protected before broad `skills/<slug>/prompts/` or `skills/<slug>/build/` directories exist.
- Emitted Markdown, receipts, and compiler sidecars are not hand-edited.
- Runtime packages remain self-contained; installed files must not require `../doctrine`, `../lessons_studio`, hidden `.prompt` files, or archived command files.
- Scripts, schemas, fixtures, and `agents/openai.yaml` remain ordinary bundled runtime assets copied byte-for-byte unless a later pass explicitly chooses a Doctrine-authored replacement.
- Root instruction generation is limited to compact `AGENTS.md` plus thin `CLAUDE.md`; the full public docs rewrite remains out of scope for this sub-plan.
- `lessons_studio` symlink wiring is not adopted because this repo's install contract is copy-based and Makefile-owned.

## 5.6 UI surfaces

No UI surface is in scope.
<!-- arch_skill:block:target_architecture:end -->

# 6) Call-Site Audit

<!-- arch_skill:block:call_site_audit:start -->
## 6.1 Change inventory

| Surface | Current state | Target owner/change | Preservation obligation |
| --- | --- | --- | --- |
| `Makefile` package install macros | `agents_install_skill`, `claude_install_skill`, and `gemini_install_skill` use whole-directory `cp -R`; `remote_install` uses `scp -r` | Add one runtime-subset copy mechanism and apply it to local and remote skill/shared copies | Preserve installed package matrices, `_shared`, hooks, stale cleanup, Gemini frontmatter stripping, and removed-skill checks while excluding `prompts/` and `build/` |
| `Makefile` verification targets | Verify installed `SKILL.md`, `_shared`, omissions, removed packages, stale command files, and hook runner | Add explicit no-source/no-build leakage checks once the copy helper exists | `make verify_install` must still pass after install behavior changes |
| `Makefile` Doctrine targets | None | Add emit, receipt verification, clean-build, target listing, and parity-approved sync targets | Keep Doctrine build commands separate from runtime install commands |
| `README.md` | Public install, matrix, feature-gate, remote install, and verification docs; no Doctrine source split | Minimal scaffold wording only after commands exist | Do not complete the full docs rewrite in this sub-plan |
| `docs/arch_skill_usage_guide.md` | Workflow selection and usage guide; known deferred inventory drift from sub-plan 1 consult | Minimal source/runtime wording only if needed for scaffold commands | Full alignment belongs to the later docs sub-plan |
| `AGENTS.md` | Hand-authored repo instructions; routes `$skill-authoring`, `$agents-md-authoring`, and `$fresh-consult`; does not yet require `$doctrine-learn`/`$prompt-authoring` for future source work | Generated from `prompts/repo_home/SKILL.prompt` only after root-doc emit proof and sync approval | Must remain compact, command-first, and truthful about current source owners |
| `CLAUDE.md` | Thin shim to `AGENTS.md` | Generated thin shim after root-doc proof | Must not duplicate root rules |
| `.gitignore` | Does not name Doctrine build outputs | Ignore disposable root and per-skill build outputs as needed | Do not hide live runtime files or source prompts by accident |
| `pyproject.toml` | Missing | New Doctrine dependency/config/emit registry | Must be the single target registry for helper-derived emits |
| `uv.lock` | Missing | New locked environment | Must be created by the normal `uv` workflow during implementation |
| `shared/prompts/arch_skill/` | Missing | New shared prompt modules | Compile-only source; not runtime dependency |
| `prompts/repo_home/SKILL.prompt` | Missing | Root-doc source owner | Must emit successfully and be receipt-verified before any `AGENTS.md`/`CLAUDE.md` sync |
| `prompts/shared_runtime/SKILL.prompt` | Missing | Shared runtime skill-package source owner | Must emit successfully, be receipt-verified, and prove emitted `_shared` parity before sync |
| `scripts/list_doctrine_skill_targets.py` | Missing | New config-derived helper modeled on `lessons_studio` | Must stay narrow, parse `pyproject.toml`, and support Makefile-friendly target output |
| `skills/pr-authoring/SKILL.md` | Hand-authored runtime skill | Representative emitted runtime output after parity sync | Preserve publish-not-draft boundary, trigger intent, workflow, and blocked-publication behavior |
| `skills/pr-authoring/references/pr-body-scaffold.md` | Hand-authored bundled reference | Bundled or emitted from `skills/pr-authoring/prompts/` | Preserve PR body scaffold meaning and path |
| `skills/pr-authoring/agents/openai.yaml` | Runtime metadata | Ordinary bundled file copied byte-for-byte | Preserve metadata presence and path |
| `skills/pr-authoring/prompts/SKILL.prompt` | Missing | Representative source package | Must not be installed |
| `skills/pr-authoring/build/` | Missing | Disposable emitted package tree | Must not be installed |
| `skills/_shared/controller-contract.md` | Hand-authored shared runtime reference copied beside installs | Later emitted from `prompts/shared_runtime/SKILL.prompt` if parity passes | Preserve controller contract semantics and installed `_shared` availability |
| `../doctrine` | Adjacent source dependency for authoring/build only | Editable source dependency in `pyproject.toml` while local workspace pattern applies | Must not become runtime dependency of installed skills |
| `../lessons_studio` | Adjacent implementation precedent only | Reference for scaffold patterns | Must not become runtime dependency or copied source |

## 6.2 Migration notes

- **Canonical owners:** Doctrine source owns instruction/reference generation; `Makefile` owns build/install/sync commands; live `skills/` remains runtime output.
- **Deprecated APIs:** None are deprecated by this sub-plan. Archived command files stay retired and are not revived.
- **Deletion candidates:** None in this planning pass. Later implementation may delete only disposable build outputs during clean-build.
- **Adjacent surfaces:** Remote install, Gemini frontmatter stripping, `_shared`, hook install/verification, and stale-surface cleanup must be read and verified whenever copy behavior changes.
- **Compatibility posture:** Source-first but not dual-live. A runtime file is not cut over until emitted output has passed parity and the approved sync path updates the live surface.
- **Proof split:** All three scaffold skill-package targets need receipts; root docs and shared-runtime output also need compile/emit proof plus file-level parity/sync evidence before approved sync.

## 6.3 Consolidation sweep for phase planning

- Install copy exclusion is cross-cutting and should become one Makefile helper rather than repeated ad hoc `cp`/`scp` exclusions.
- Target discovery should be centralized in `scripts/list_doctrine_skill_targets.py`; Makefile and any shell wrapper should consume that helper instead of maintaining duplicate target lists.
- Root-doc generation uses the chosen `prompts/repo_home/SKILL.prompt` precedent from `lessons_studio`. The phase plan must put a compile/emit smoke test before sync; compiler rejection reopens planning instead of switching entrypoints during implementation.
- Shared prompt modules should start as seeds only: controller lifecycle, install/runtime invariants, authoring quality, and model/runtime. Full redundancy folding belongs to later sub-plans.
- First-party lock exclusion is a hard rule for this scaffold. `doctrine.skill.lock` appears only if a future external source-root target is introduced.
- Public docs/root instructions should be updated minimally in this sub-plan, then fully rewritten in the later docs sub-plan.
<!-- arch_skill:block:call_site_audit:end -->

# 7) Depth-First Phased Implementation Plan

<!-- arch_skill:block:phase_plan:start -->
## Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first. `Work` explains the coherent unit; `Checklist (must all be done)` is the authoritative must-do list inside each phase; `Exit criteria (all required)` names the concrete done-state that audit must validate. This phase plan is docs-only and does not authorize implementation. Do not start Phase 1 until this doc records a no-blocker Codex `gpt-5.4` `xhigh` implementation authorization consult/critic.

## Phase 1 - Protect the Runtime Install Surface

* Goal: Make local and remote installs source/build-safe before any broad `skills/<slug>/prompts/` or `skills/<slug>/build/` trees exist.
* Work: Convert the existing whole-directory copy behavior into one Makefile-owned runtime-subset copy path that preserves the current install contract while excluding Doctrine source and disposable build trees.
* Checklist (must all be done):
  - Re-read `Makefile` install, remote install, `_shared`, hook, stale-cleanup, and verification targets before editing.
  - Add one Makefile-owned local copy helper or macro for runtime skill/shared directories that copies runtime files while excluding `prompts/` and `build/`.
  - Apply the local runtime-subset helper to agents/Codex skill installs, Claude Code skill installs, Gemini skill installs, and `_shared` installs.
  - Add the equivalent remote copy behavior for agents/Codex, Claude Code, Gemini, and `_shared` remote installs.
  - Preserve `SKILLS`, `CLAUDE_SKILLS`, `GEMINI_SKILLS`, `SHARED_DIRS`, `REMOVED_SKILLS`, `ARCHIVED_COMMAND_FILES`, Codex mirror cleanup, Claude hook install, Codex hook install, Gemini frontmatter stripping, and stale-surface cleanup.
  - Extend install verification so installed active skill roots and installed `_shared` roots do not contain `prompts/` or `build/`.
  - Keep `skills/` as the live runtime source for install commands; do not introduce symlink installs.
* Verification (required proof):
  - Run `make verify_install`.
  - Run `make -n remote_install HOST=example.invalid NO_GEMINI=1` and re-read the dry-run output plus `remote_install` to confirm remote copy exclusions match local copy exclusions.
  - Use `rg` on `Makefile` to confirm remaining raw `cp -R` / `scp -r` skill-copy sites do not bypass the runtime-subset helper.
* Docs/comments (propagation; only if needed):
  - Add a short Makefile comment at the copy helper explaining that `prompts/` and `build/` are source/build internals and must not be installed.
* Exit criteria (all required):
  - Current agents/Codex, Claude Code, and Gemini runtime matrices are unchanged.
  - Local and remote installs exclude `prompts/` and `build/` for skill packages and `_shared`.
  - Installed runtime packages remain self-contained.
  - `make verify_install` passes with the new no-source/no-build checks.
  - Remote install dry-run shows no source/build leakage path.
* Rollback:
  - Restore the previous Makefile copy rules and verification checks before adding any Doctrine source/build directories.

## Phase 2 - Add Doctrine Project Config And Target Discovery

* Goal: Add the locked Doctrine project scaffold and one config-derived target-discovery path without authoring runtime content yet.
* Work: Create the repo-level Doctrine configuration, lock file, generated-output ignore rules, and narrow helper selected by Sections 3 and 6.
* Checklist (must all be done):
  - Add `pyproject.toml` with `doctrine-agents>=4.0.0,<5`, `[tool.uv] package = false`, and the local editable `doctrine-agents = { path = "../doctrine", editable = true }` workspace source.
  - Add `[tool.doctrine.compile] additional_prompt_roots = ["shared/prompts"]`.
  - Add `[tool.doctrine.emit]` targets for `pr-authoring`, `repo-home`, and `shared-runtime` using the paths chosen in Section 5.2.
  - Omit `source_root`, `source_id`, and `lock_file` for all first-party local targets.
  - Generate `uv.lock` through the standard `uv` workflow.
  - Add `.gitignore` entries for disposable root and per-skill build outputs without hiding `.prompt` source files or live runtime files.
  - Add `scripts/list_doctrine_skill_targets.py`, modeled on `../lessons_studio/scripts/list_doctrine_skill_targets.py`, to parse `pyproject.toml` with `tomllib` and print target names or output dirs for targets whose `output_dir` starts with `skills/`.
  - Add Makefile target discovery plumbing that consumes `scripts/list_doctrine_skill_targets.py` instead of maintaining a duplicate skill-target list.
* Verification (required proof):
  - Run `uv sync`.
  - Run `uv run python scripts/list_doctrine_skill_targets.py`.
  - Run `uv run python scripts/list_doctrine_skill_targets.py --make`.
  - Run `uv run python scripts/list_doctrine_skill_targets.py --output-dirs`.
  - Use `rg` to verify no first-party local target names `doctrine.skill.lock`.
* Docs/comments (propagation; only if needed):
  - Add a concise script docstring explaining that the helper lists Doctrine targets that emit runtime skill packages.
* Exit criteria (all required):
  - The repo has `pyproject.toml` and `uv.lock`.
  - The Doctrine compile root and three scaffold emit targets are configured.
  - The helper derives skill target names and output dirs from `pyproject.toml`.
  - No first-party local target creates or requires `doctrine.skill.lock`.
  - Disposable build outputs are ignored; source prompts and live runtime files are not ignored.
* Rollback:
  - Remove `pyproject.toml`, `uv.lock`, helper plumbing, and ignore entries, leaving the Phase 1 install guardrail in place only if it remains correct for the direct-runtime tree.

## Phase 3 - Author The Minimum Doctrine Source Scaffold

* Goal: Create the first source prompt roots and representative source package while preserving current runtime behavior.
* Work: Author only the seed sources needed to prove the scaffold: shared prompt modules, root-doc source, shared-runtime source, and the `pr-authoring` source package.
* Checklist (must all be done):
  - Add `shared/prompts/arch_skill/controller_lifecycle.prompt` with only the reusable controller lifecycle declarations needed by the scaffold.
  - Add `shared/prompts/arch_skill/install_runtime_invariants.prompt` with reusable install, matrix, source/build exclusion, and self-containment declarations.
  - Add `shared/prompts/arch_skill/authoring_quality.prompt` with only the reusable doctrine/skill/prompt/agents authoring quality declarations needed by the scaffold.
  - Add `shared/prompts/arch_skill/model_runtime.prompt` with reusable Codex `gpt-5.4` `xhigh`, fresh-consult, spawned-check, and critic policy declarations needed by the scaffold.
  - Add `prompts/repo_home/SKILL.prompt` as the chosen root-doc source owner for compact `AGENTS.md` and thin `CLAUDE.md` output.
  - Add `prompts/shared_runtime/SKILL.prompt` as the chosen source owner for emitted shared runtime references.
  - Add `skills/pr-authoring/prompts/SKILL.prompt` as the representative source package.
  - Copy the current `skills/pr-authoring/references/pr-body-scaffold.md` into source-side `skills/pr-authoring/prompts/references/pr-body-scaffold.md` so emitted output preserves the runtime reference path.
  - Copy the current `skills/pr-authoring/agents/openai.yaml` into source-side `skills/pr-authoring/prompts/agents/openai.yaml` so emitted output preserves runtime metadata byte-for-byte.
  - Preserve `pr-authoring` trigger intent, publish-not-draft boundary, workflow, output expectations, blocked-publication behavior, reference map, and metadata.
  - Keep shared modules as seeds; do not fold suite-wide redundancy in this sub-plan.
* Verification (required proof):
  - Re-read the new `.prompt` files.
  - Use `rg` to verify the source paths, bundled reference path, bundled metadata path, and import paths named in the new sources.
  - Use `rg` to compare the representative source package against current `skills/pr-authoring/SKILL.md`, `references/pr-body-scaffold.md`, and `agents/openai.yaml` for no obvious missing behavior.
* Docs/comments (propagation; only if needed):
  - Keep source comments sparse; add only comments that explain non-obvious source/runtime boundaries.
* Exit criteria (all required):
  - All source paths chosen in Section 5.1 exist.
  - `pr-authoring` source can account for every current runtime file in the representative package.
  - Shared prompt modules do not become runtime dependencies.
  - Root-doc and shared-runtime source owners exist but no generated root docs or `_shared` runtime files are synced yet.
* Rollback:
  - Remove the source prompt roots and representative source package; keep Phase 1 and Phase 2 only if they still pass their verification.

## Phase 4 - Emit, Resolve Receipts, And Prove Parity Before Sync

* Goal: Prove the scaffold emits reviewable output and receipts before any live runtime files are replaced.
* Work: Run the new Doctrine emit path into disposable build outputs, resolve the root-doc entrypoint proof, verify receipts where they apply, and compare emitted output against the frozen current behavior.
* Checklist (must all be done):
  - Add Makefile targets for `doctrine_emit`, `doctrine_verify_receipts`, and `doctrine_clean_build`, all wired to the Phase 2 target-list helper where skill target enumeration is needed.
  - Run `doctrine_clean_build` before the first full scaffold emit.
  - Run `doctrine_emit` for `pr-authoring`, `repo-home`, and `shared-runtime`.
  - Prove the chosen `prompts/repo_home/SKILL.prompt` path emits the required compact `AGENTS.md` and thin `CLAUDE.md` outputs. If Doctrine rejects that shape, stop implementation and reopen planning instead of switching entrypoints inside implementation.
  - Run `doctrine_verify_receipts` for every emitted skill-package target, including `pr-authoring`, `repo-home`, and `shared-runtime`.
  - Record explicit compile/emit proof plus file-level parity evidence for root-doc and shared-runtime outputs in addition to their receipts.
  - Compare emitted `pr-authoring` output against current `skills/pr-authoring/` and repair any lost trigger, workflow, non-negotiable, output, reference, or metadata meaning before sync.
  - Compare emitted shared-runtime output against `skills/_shared/controller-contract.md` and repair any lost controller-contract meaning before sync.
  - Confirm emitted outputs do not require `../doctrine`, `../lessons_studio`, `.prompt` source files, or archived command files at runtime.
* Verification (required proof):
  - Run `make doctrine_emit`.
  - Run `make doctrine_verify_receipts`.
  - Run targeted `diff` or equivalent file comparison for emitted `pr-authoring`, root-doc, and shared-runtime outputs against the current live runtime/root files.
  - Re-read every emitted output selected for later sync.
* Docs/comments (propagation; only if needed):
  - Update Makefile comments beside Doctrine targets if the command shape is not self-explanatory.
* Exit criteria (all required):
  - Disposable build outputs exist for representative skill, root docs, and shared runtime.
  - `pr-authoring` has a current `SKILL.source.json` receipt.
  - Root-doc and shared-runtime outputs have current receipts plus explicit compile/emit and parity proof.
  - The root-doc entrypoint shape is proven and no longer ambiguous.
  - No emitted runtime output has an unresolved no-loss finding.
* Rollback:
  - Delete disposable build outputs with `make doctrine_clean_build` and repair sources or target config before retrying.

## Phase 5 - Sync Approved Runtime Outputs And Minimal Docs

* Goal: Move only parity-approved scaffold output into the live runtime/root surfaces and update the minimum user-facing instructions required by the new source/runtime split.
* Work: Add and use an explicit sync gate for approved outputs, then validate runtime package and install behavior.
* Checklist (must all be done):
  - Add `doctrine_sync_approved` as the explicit Makefile sync target that accepts only named approved scaffold outputs.
  - Sync the approved representative `pr-authoring` emitted runtime files into `skills/pr-authoring/`.
  - Sync the approved shared-runtime output into `skills/_shared/`.
  - Sync the approved root-doc output into `AGENTS.md` and `CLAUDE.md`.
  - Ensure synced runtime files do not include `.prompt` source files, disposable `build/` trees, or hidden Doctrine-only dependencies.
  - Keep `CLAUDE.md` a thin shim rather than a duplicate rules file.
  - Update `README.md` and `docs/arch_skill_usage_guide.md` only enough to name the scaffold commands, source/runtime split, install boundary, and verification commands introduced by this sub-plan.
  - Ensure `AGENTS.md` now tells future agents to use `$doctrine-learn`, `$skill-authoring`, `$prompt-authoring`, and `$agents-md-authoring` for relevant instruction-bearing work, without claiming the full suite is already ported.
  - Preserve the current install matrices, Gemini omissions, Gemini frontmatter stripping, hook wiring, stale cleanup, and remote install behavior.
* Verification (required proof):
  - Run `npx skills check`.
  - Run `make verify_install`.
  - Run `make -n remote_install HOST=example.invalid NO_GEMINI=1` and re-read the dry run for source/build exclusion.
  - Re-read `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/arch_skill_usage_guide.md`, `skills/pr-authoring/SKILL.md`, `skills/pr-authoring/references/pr-body-scaffold.md`, `skills/pr-authoring/agents/openai.yaml`, and `skills/_shared/controller-contract.md`.
  - Use `rg` to verify every new path and command documented in root/public docs.
* Docs/comments (propagation; only if needed):
  - This phase owns the minimum docs/root-instruction propagation for the scaffold. The final full docs rewrite remains sub-plan 5.
* Exit criteria (all required):
  - Only approved emitted outputs have been synced into live runtime/root files.
  - `skills/pr-authoring/`, `skills/_shared/`, `AGENTS.md`, and `CLAUDE.md` match the proven scaffold outputs.
  - Public docs name the new scaffold commands and source/runtime split without overstating whole-suite port status.
  - `npx skills check` and `make verify_install` pass.
  - Remote install dry-run preserves the same source/build exclusion as local install.
* Rollback:
  - Restore the affected live runtime/root files from the last verified state, keep disposable build outputs for comparison, repair source, re-emit, and rerun the phase verification before syncing again.

## Phase 6 - Record Evidence And Pass The Sub-plan Completion Gate

* Goal: Make the scaffold outcome auditable and obtain the required Codex review before this sub-plan can complete or the epic can advance.
* Work: Record implementation truth, verification evidence, residual risks, and a fresh Codex `gpt-5.4` `xhigh` completion consult or arch-epic critic verdict.
* Checklist (must all be done):
  - Update this doc's Decision Log with the implemented scaffold, root-doc entrypoint outcome, receipt policy outcome, and verification commands that actually ran.
  - Update `docs/EPIC_ARCH_SKILL_DOCTRINE_PORT_2026-04-26.md` with truthful sub-plan 2 implementation status and evidence paths.
  - Run a Codex `gpt-5.4` `xhigh` completion consult or arch-epic critic against this sub-plan's completion claim.
  - Record the consult/critic artifact path and verdict in this doc and the epic doc.
  - Repair every blocking consult/critic finding in the owning phase before marking sub-plan 2 complete.
  - Leave sub-plan 3 unstarted until the completion verdict has no blocking findings.
* Verification (required proof):
  - Re-run or re-check the smallest verification set affected by any completion-consult repairs.
  - Re-read the final changed docs and verify added paths/commands with `rg`.
  - Confirm `git status --short --untracked-files=all` is understood and no unrelated user work was reverted or deleted.
* Docs/comments (propagation; only if needed):
  - Keep completion notes in this plan and the epic; do not create a competing sidecar plan.
* Exit criteria (all required):
  - The scaffold exists and runs through the documented emit, receipt/proof, sync, and install verification paths.
  - The representative skill, root-doc output, and shared-runtime output are source-owned and parity-approved.
  - No first-party local source uses `doctrine.skill.lock`.
  - No installed runtime package contains source/build internals.
  - The Codex `gpt-5.4` `xhigh` completion consult or arch-epic critic has no blocking findings.
  - The epic records sub-plan 2 as complete only after the no-blocker verdict.
* Rollback:
  - If the completion consult finds a blocking scaffold or no-loss issue, reopen the owning phase, repair it there, rerun its verification, and repeat the completion consult before advancing.
<!-- arch_skill:block:phase_plan:end -->

# 8) Verification Strategy

## 8.1 Unit tests / contract checks

Expected checks include Doctrine compile/emit command success, receipt verification, target-discovery helper tests or smoke checks, explicit root-doc/shared-runtime compile or receipt proof, and direct command/path existence checks for new docs.

## 8.2 Integration tests

Before sync, compare emitted `pr-authoring`, root-doc, and shared-runtime output against the current live runtime/root files for no-loss parity. Run `npx skills check` after synced runtime package changes. Run targeted `make verify_*` or `make verify_install` according to the actual install-surface change.

## 8.3 Operational proof

Run `make -n remote_install HOST=example.invalid NO_GEMINI=1` after remote install copy behavior changes and re-read `remote_install` to confirm source/build exclusion matches local install. Record the Codex `gpt-5.4` `xhigh` implementation authorization consult/critic before Phase 1 starts, and record the Phase 6 completion consult/critic before sub-plan 2 completes.

# 9) Rollout / Ops / Telemetry

## 9.1 Rollout plan

Roll out scaffold changes in the Section 7 order: install-copy guardrail first, Doctrine config and target discovery second, source scaffold third, emit/receipt/parity proof fourth, parity-approved sync plus minimum docs fifth, and evidence plus completion consult sixth.

## 9.2 Telemetry changes

None.

## 9.3 Operational runbook

Use the Makefile targets added by this sub-plan for emit, receipt verification, and sync. Do not hand-copy generated outputs unless the final phase plan explicitly names a temporary manual proof step.

<!-- arch_skill:block:consistency_pass:start -->
## Consistency Pass

- Reviewers: explorer 1, explorer 2, self-integrator
- Scope checked:
  - Frontmatter, TL;DR, Sections 0-10, planning helper, and helper-block drift against the epic gate.
  - Sections 3, 4, 5, 6, and 7 against sub-plan 1 Sections 5-7.
  - Section 7 against obligations from Sections 0.4, 3, 5, 6, and 8.
  - Current architecture, target architecture, call-site audit, verification strategy, rollout, Decision Log, and epic orchestration state.
- Findings summary:
  - Explorer 1 found one blocking execution-order drift: the planning helper treated the next consult as a pre-sub-plan completion gate instead of distinguishing implementation authorization from the Phase 6 completion consult.
  - Explorer 1 noted non-blocking Section 8 parity-proof thinness and canonical `doc_type` drift.
  - Explorer 2 found no blocking scope drift and confirmed Section 7 covers Sections 0.4, 3, 5, 6, and 8.
- Integrated repairs:
  - Rewrote `planning_passes` so the next order is consistency pass -> implementation authorization consult/critic -> implement Phases 1-6 -> completion consult/critic -> next sub-plan.
  - Renamed the pre-implementation gate to `implementation_authorization_consult` and kept `completion_consult` as the Phase 6 post-implementation gate.
  - Updated stale "later phase-plan" implementation-gate wording after Section 7 was written.
  - Strengthened Section 8 to name no-loss parity comparisons, root/shared proof, and the two distinct consult/critic gates.
  - Changed `doc_type` to `phased_refactor`.
  - After the implementation authorization consult failed, removed the root-doc alternate-entrypoint branch, made `repo-home` and `shared-runtime` explicitly receipt-backed `SKILL.prompt` targets, and fixed the stale Section 7 gate sentence.
- Remaining inconsistencies:
  - none
- Unresolved decisions:
  - none
- Unauthorized scope cuts:
  - none
- Decision-complete:
  - yes
- Decision: proceed to implement? yes, only after the Codex `gpt-5.4` `xhigh` implementation authorization consult/critic records no blocking findings
<!-- arch_skill:block:consistency_pass:end -->

# 10) Decision Log

## 2026-04-26 - Sub-plan 2 draft created

Context

Sub-plan 1 completed after the Codex `gpt-5.4` `xhigh` completion consult at `/tmp/fresh-consult/arch-epic-subplan1-completion-rerun2-20260426T132653Z-9g0nR0/` returned `pass-with-notes` with no blocking findings.

Decision

Create this canonical sub-plan 2 DOC_PATH as the draft architecture/implementation plan for adding the Doctrine source and emit scaffold without porting the whole suite.

Consequences

The next arch-loop pass should handle the North Star gate for this doc before running planning or implementation stages. This draft does not authorize implementation yet.

## 2026-04-26 - North Star gate passed and deep-dive pass 1 completed

Context

The Codex `gpt-5.4` `xhigh` fresh consult at `/tmp/fresh-consult/arch-epic-subplan2-north-star-20260426T133843Z-ZM7UJh/` reviewed the draft North Star against the epic, sub-plan 1 architecture, and core repo surfaces.

Options

- Keep the doc in draft because Sections 3-7 still contain placeholders.
- Activate the North Star because the consult found no blockers and then fill the first deep-dive/current-architecture pass.

Decision

Activate this doc for planning. Fold the consult notes by making `scripts/list_doctrine_skill_targets.py` a selected scaffold helper rather than a reopened conditional choice, and by requiring root-doc/shared-runtime outputs to have explicit emit plus sync/parity proof even where `SKILL.source.json` receipts do not apply. Fill Section 4 with repo-backed current-architecture evidence from `Makefile`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `skills/`, `../doctrine`, and `../lessons_studio`.

Consequences

Sub-plan 2 may continue to the external-research grounding and second deep-dive/target-architecture pass. Implementation is still not authorized.

## 2026-04-26 - External grounding and deep-dive pass 2 completed

Context

The next arch-loop task required verifying the listed Doctrine and `lessons_studio` anchors plus sub-plan 1 Sections 5-7, replacing the Section 3 placeholder with concrete evidence, and using that evidence to fill Sections 5 and 6.

Decision

Mark `external_research_grounding` and `deep_dive_pass_2` done. Record local source evidence from `../doctrine`, `../lessons_studio`, and sub-plan 1; choose the concrete scaffold target architecture; inventory the call sites affected by the scaffold; and keep implementation unauthorized until the later phase-plan and consistency gates pass.

Consequences

The next arch-loop pass should write the phase plan for this same DOC_PATH. No scaffold files, source prompts, Makefile changes, or runtime package changes are authorized by this planning pass.

## 2026-04-26 - Phase-plan completed

Context

Sections 0.4, 3, 5, 6, and 8 now define enough scaffold architecture, verification obligations, and call-site scope to produce the authoritative Section 7 execution plan.

Decision

Replace the Section 7 placeholder with a six-phase depth-first implementation plan: protect install copy behavior first, add Doctrine config and target discovery second, author the minimum source scaffold third, emit and prove parity before sync fourth, sync approved runtime/root outputs and minimal docs fifth, and record evidence plus the Codex `gpt-5.4` `xhigh` completion consult/critic sixth.

Consequences

This phase-plan pass is still docs-only. Implementation remains unauthorized until the later consistency gate and required Codex consult/critic authorization clear the plan.

## 2026-04-26 - Consistency-pass completed with repairs

Context

The consistency-pass equivalent cold-read checked Sections 0-10 against the epic gate, sub-plan 1 architecture, and Section 7 obligations from Sections 0.4, 3, 5, 6, and 8. Two Codex `gpt-5.4` `xhigh` explorers split the review, and the parent integrator cold-read the artifact directly.

Decision

Repair the blocking execution-order drift by distinguishing the pre-implementation `implementation_authorization_consult` from the Phase 6 `completion_consult`; keep the completion consult at the end of implementation, not before it. Strengthen Section 8's no-loss/parity proof language and repair the `doc_type` drift.

Consequences

The plan is decision-complete and may be sent to the required Codex `gpt-5.4` `xhigh` implementation authorization consult/critic. Phase 1 still must not start until that consult/critic records no blocking findings.

## 2026-04-26 - Implementation authorization consult failed and blockers repaired

Context

The Codex `gpt-5.4` `xhigh` fresh consult at `/tmp/fresh-consult/arch-epic-subplan2-implementation-authorization-20260426TXXXXXX-rhHum6/` returned `fail`.

Decision

Repair all three blocking findings before rerun: fix the stale Section 7 gate sentence, remove the root-doc alternate-entrypoint branch by committing to `prompts/repo_home/SKILL.prompt`, and make `prompts/shared_runtime/SKILL.prompt` an explicitly receipt-backed skill-package target.

Consequences

Implementation remains unauthorized. The implementation authorization consult must be rerun and record a no-blocker verdict before Phase 1 starts.
