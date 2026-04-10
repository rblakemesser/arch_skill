---
title: "arch_skill - arch-step implement-loop clean-audit delivery - Architecture Plan"
date: 2026-04-10
status: active
fallback_policy: forbidden
owners: [aelaguiz]
reviewers: []
doc_type: architectural_change
related:
  - skills/arch-step/SKILL.md
  - skills/arch-step/references/arch-implement.md
  - skills/arch-step/references/arch-audit-implementation.md
  - skills/arch-step/references/arch-implement-loop.md
  - README.md
  - /Users/aelaguiz/workspace/codex/codex-rs/hooks/src/engine/discovery.rs
  - /Users/aelaguiz/workspace/codex/codex-rs/core/src/codex.rs
---

# TL;DR

- Outcome:
  - Ship `arch-step implement-loop` as a hook-backed Codex delivery loop that reuses `implement` plus `audit-implementation`, keeps the feature inside the existing `arch-step` surface, and refuses to pretend prompt-only repetition is real automation.
- Problem:
  - The user wants to invoke the loop from inside an existing Codex session, but without an installed Stop hook there is no real loop: Codex can stop, but nothing deterministic re-enters with a fresh audit pass, so prompt-only “looping” is fake.
- Approach:
  - Ground the design in actual repo and Codex runtime truth, keep `implement-loop` as the front door inside `arch-step`, and make the actual automation entirely hook-owned: installed Codex Stop hook, explicit loop-state handoff, fresh child audit, deterministic continue-or-stop routing.
- Plan:
  - Align the repo-owned contract around “no hook, no loop,” add the hook runner plus Codex install wiring, validate the hook in a real Codex session, and then audit against that shipped hook-backed scope.
- Non-negotiables:
  - No separate skill.
  - No non-hook automation story.
  - No unsupported Codex `prompt` or `agent` hooks.
  - The hook owns stop-versus-continue control.
  - Fresh audit is required for the automated loop and must receive explicit `DOC_PATH`.
  - Installed skill mirrors must not silently drift from the repo source of truth.
  - `implement-loop` remains bounded and must stop on real blockers instead of becoming a generic autonomous daemon.

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-04-10
external_research_grounding: not started
deep_dive_pass_2: done 2026-04-10
phase_plan: done 2026-04-10
recommended_flow: implement
note: This is a warn-first checklist only. It should not hard-block execution.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

If `arch-step` owns an explicit `implement-loop` command and this repo installs a Codex Stop hook that reads loop state, launches a fresh child audit, and deterministically decides continue-versus-stop from that audit result, then a user can invoke the loop from an existing Codex session and get real automatic re-entry until the audit is clean or blocked. If the hook is absent or disabled, the command must fail loud instead of pretending the loop still exists.

## 0.2 In scope

- The existing `arch-step` skill surface in this repo, including `SKILL.md`, command references, and public docs.
- The `implement-loop` controller contract and its relationship to `implement` and `audit-implementation`.
- The Codex hook-owned automation path:
  - Stop hook continuation behavior
  - fresh child audit subprocess behavior
  - hook feature gating
  - deterministic loop-state ownership
- Install surfaces that must ship the working Codex hook and the updated skill mirrors.

## 0.3 Out of scope

- A new standalone loop skill.
- Prompt-only non-hook looping as a “good enough” implementation.
- Cross-runtime automation parity for Claude Code or Gemini in this change.
- Direct feature work inside the Codex repo.
- Generic open-ended autonomy outside the bounded implement then audit loop.
- New fallback shims, alternate product modes, or speculative orchestration infrastructure.

## 0.4 Definition of done (acceptance evidence)

- The plan names the authoritative `arch-step` owner surfaces and the real Codex runtime constraints with concrete file anchors.
- The target design makes clear that actual Codex automation requires an installed Stop hook and does not claim a non-hook fallback.
- The hook design names the recursion guard, explicit `DOC_PATH` handoff, and the deterministic state contract that decides whether a stop belongs to an active loop.
- The command surface and docs in this repo use one final name and one contract.
- The Codex install surface includes the working hook and the updated skill mirror, or the doc says plainly that the feature is not yet shipped.
- Required verification is identified up front:
  - `npx skills check`
  - `git diff --check`
  - `make verify_install`
  - a real Codex session exercise before claiming the automatic loop works

## 0.5 Key invariants (fix immediately if violated)

- No separate skill or competing control surface.
- No hook, no loop.
- No unsupported Codex hook types assumed.
- No hidden install drift in touched surfaces.
- No fallbacks or runtime shims unless explicitly approved later.
- If the hook is missing or `codex_hooks` is disabled, `implement-loop` must fail loud instead of pretending prompt repetition is real automation.
- Fresh audit passes must receive explicit `DOC_PATH` and current repo context when they run outside the parent session.
- If a Stop hook launches a child audit, selectivity lives in the hook command itself and the child must disable hooks or otherwise guard recursion.
- The hook, not the parent model turn, decides whether the session continues after a stop attempt.
- The loop must stop on real blockers instead of fabricating progress.

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)

1. Make the feature real: actual Codex automation requires an installed Stop hook.
2. Fail loud when the hook path is unavailable instead of selling prompt-only looping.
3. Keep `implement-loop` inside the existing `arch-step` surface as the invocation front door.
4. Preserve one shipped command name and one hook-backed contract across repo source and installed mirrors.

## 1.2 Constraints

- `arch-step` is doctrine and packaging in this repo, not a runtime daemon.
- This repo currently ships no `.codex/hooks.json`, no hook runner, and no repo-local loop-state contract; today it ships doctrine plus skill install surfaces only.
- In Codex, skill use is turn-scoped and recomputed from each turn's input.
- Stop hooks are command-only, synchronous-only, matcherless for the Stop event, and gated by `codex_hooks`, which is under development and default-off.
- The public TS SDK exposes `startThread()` and `resumeThread()` but not a public fork helper; fresh child contexts beyond that live in CLI or app-server surfaces.
- The local install model copies `skills/` into `~/.agents/skills/`, `~/.codex/skills/`, `~/.claude/skills/`, and `~/.gemini/skills/`.
- Any installed Stop hook will run on every Codex stop, so it must self-filter cheaply and deterministically when no active `implement-loop` state exists for the current session.

## 1.3 Architectural principles (rules we will enforce)

- Reuse the existing `implement` plus `audit-implementation` split instead of collapsing them.
- Keep the controller explicit; do not silently auto-promote it from unrelated commands.
- The actual automatic loop lives in the Stop hook, not in prompt-only repetition.
- Prefer native hook and CLI lifecycle surfaces before inventing wrappers.
- Treat install mirrors as real runtime truth, not optional afterthoughts.

## 1.4 Known tradeoffs (explicit)

- The working feature is Codex-specific; Claude Code and Gemini do not get the same automation from this plan.
- Same-turn Stop-hook continuation is real in Codex, but it only exists when the hook is installed and `codex_hooks` is enabled.
- Shipping the feature now means owning a Codex hook install surface, not just repo doctrine.
- The repo source can be correct while local installed skill copies or hook config remain stale until reinstall.

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today

- The repo-local `arch-step` surface now names `implement-loop` as the bounded controller command.
- The repo-local `skills/arch-step/agents/openai.yaml` shim still omits `implement-loop` from its default prompt, so repo-owned command surfaces are not yet fully converged.
- `implement` and `audit-implementation` remain separate contracts and are the intended building blocks of the loop.
- This repo currently ships no `.codex/hooks.json`, no hook runner, and no loop-state contract, so no real in-session Codex automation is installed from this repo today.
- Codex skill invocation is explicit and turn-scoped.
- Codex supports Stop-hook continuation and fresh execution surfaces, but they are constrained by the live hook and thread APIs.
- The install system mirrors `skills/` into multiple runtime-specific skill directories.

## 2.2 What's broken / missing (concrete)

- There was no canonical full-arch plan artifact for this feature before this run.
- The current repo surface still describes a controller command but does not ship the hook required to make that controller real in Codex.
- All copied install mirrors currently still expose `implement-until-clean` and still carry `references/arch-implement-until-clean.md`, so the runtime surface is stale in `.agents`, `.codex`, `.claude`, and `.gemini`.
- The repo-owned `skills/arch-step/agents/openai.yaml` default prompt is stale relative to the repo command surface.
- There is still no shipped Codex hook install surface, no deterministic loop-state handoff, and no fail-loud contract for “hook missing or disabled.”
- Without grounded runtime research, it is easy to over-assume unsupported `prompt` hooks, `agent` hooks, sticky skill activation across turns, or a public TS SDK fork surface that does not exist.

## 2.3 Constraints implied by the problem

- The design must keep one source of truth for the command inside `arch-step`.
- The design must treat the hook as required for actual Codex automation, not as a preference.
- Stop-hook selectivity has to live inside the hook command, because the Stop event does not use matcher filtering.
- The plan must include a shipped hook install surface and a deterministic loop-state contract, or else it is not solving the requested behavior.

# 3) Research Grounding (external + internal "ground truth")

<!-- arch_skill:block:research_grounding:start -->
## 3.1 External anchors (papers, systems, prior art)

- None yet - reject external web research for now because the decisive constraints are repo-local `arch-step` packaging plus the local Codex runtime and codebase, not generic agent-loop prior art.

## 3.2 Internal ground truth (code as spec)

- Authoritative behavior anchors (do not reinvent):
  - `skills/arch-step/SKILL.md` - the live repo command surface, non-negotiables, and the explicit-controller framing for `implement-loop`.
  - `skills/arch-step/references/arch-implement-loop.md` - the bounded controller contract, fresh-audit preference ladder, and stop conditions.
  - `skills/arch-step/references/arch-implement.md` - the single implementation-pass contract that `implement-loop` must reuse instead of replacing.
  - `skills/arch-step/references/arch-audit-implementation.md` - the docs-only audit contract and false-complete reopening rules that make the loop meaningful.
  - `README.md` and `Makefile` - the install and verification surfaces that copy `skills/` into runtime mirrors and define when install validation is available.

- Canonical path / owner to reuse:
  - `skills/arch-step/` - the existing owning surface for the full-arch workflow; this change should stay here instead of creating a second loop skill.

- Existing patterns to reuse:
  - `skills/arch-step/references/advance.md` - explicit controller commands stay explicit; the workflow should not auto-promote the loop except when the user directly asks for it.
  - `skills/arch-step/references/arch-implement.md` plus `skills/arch-step/references/arch-audit-implementation.md` - preserve the current "write code here, audit there" split instead of blending implementation and auditing into one opaque step.

- Prompt surfaces / agent contract to reuse:
  - `skills/arch-step/SKILL.md` - the runtime doctrine the model sees when the user explicitly invokes `$arch-step`.
  - `/Users/aelaguiz/workspace/codex/codex-rs/core-skills/src/injection.rs` - Codex loads selected `SKILL.md` files into `SkillInstructions`, which means the skill is prompt injection and turn-scoped, not a persistent controller process.
  - `/Users/aelaguiz/workspace/codex/codex-rs/protocol/src/user_input.rs` and `/Users/aelaguiz/workspace/codex/codex-rs/tui/src/chatwidget.rs` - skill mentions are represented as `UserInput::Skill` and collected from the current turn's input.

- Native model or agent capabilities to lean on:
  - `codex exec` - `--ephemeral`, `--cd`, `--output-schema`, and `--json` are exposed by the installed CLI and provide a credible fresh audit subprocess surface with explicit working context and structured output.
  - `/Users/aelaguiz/workspace/codex/sdk/typescript/src/codex.ts` and `/Users/aelaguiz/workspace/codex/sdk/typescript/src/thread.ts` - the public TS SDK exposes `startThread()` and `resumeThread()` and runs turns through fresh CLI subprocesses.
  - `/Users/aelaguiz/workspace/codex/codex-rs/app-server-protocol/src/protocol/common.rs` and `/Users/aelaguiz/workspace/codex/codex-rs/app-server/src/codex_message_processor.rs` - lower-level runtime surfaces support `thread/start`, `thread/resume`, and `thread/fork`, which are the real fresh or branched thread primitives behind higher-level interfaces.

- Existing grounding / tool / file exposure:
  - `/Users/aelaguiz/workspace/codex/codex-rs/config/src/state.rs` and `/Users/aelaguiz/workspace/codex/codex-rs/hooks/src/engine/discovery.rs` - project `.codex/` folders are config layers, and `hooks.json` is discovered from config folders rather than skill state.
  - `/Users/aelaguiz/workspace/codex/codex-rs/hooks/schema/generated/stop.command.input.schema.json` - Stop hook input already includes `cwd`, `session_id`, `turn_id`, `transcript_path`, `last_assistant_message`, and `stop_hook_active`, which is enough to route a fresh audit subprocess with explicit context.
  - `/Users/aelaguiz/workspace/codex/codex-rs/core/src/codex.rs` - Stop-hook continuation is recorded back into the same conversation as a synthetic user message, so the native hook loop is same-turn continuation rather than a brand-new top-level turn.

- Duplicate or drifting paths relevant to this change:
  - `/Users/aelaguiz/.agents/skills/arch-step/SKILL.md` - currently still names `implement-until-clean`, which proves the installed agents mirror can drift from repo source until reinstall.
  - `README.md` and `Makefile` - the repo intentionally mirrors the skill surface into `~/.agents/skills/`, `~/.codex/skills/`, `~/.claude/skills/`, and `~/.gemini/skills/`, so any shipped command rename has real copied-surface implications.

- Capability-first opportunities before new tooling:
  - Existing skill injection plus explicit `$arch-step` invocation - enough to keep the entrypoint inside the current skill surface, but not enough to create real automation without the Stop hook.
  - Codex Stop hooks - the native runtime surface that can actually own same-turn continuation, so this is the required automation path rather than an optional extra layer.
  - `codex exec --ephemeral` or SDK/app-server thread primitives - already provide fresh-context execution surfaces before any custom wrapper is justified.

- Behavior-preservation signals already available:
  - `npx skills check` - required repo validation for skill package changes in this repo.
  - `git diff --check` - catches whitespace and patch-hygiene regressions in the touched docs surface.
  - `make verify_install` - required because the shipped feature includes the Codex hook install surface.
  - a real Codex session exercise - required before claiming the hook-backed loop works.

## 3.3 Open questions from research

- Resolved default: real Codex automation requires an installed Stop hook; prompt-only repetition is rejected as a fake loop.
- Resolved default: the first shipped child-audit path should be `codex exec --ephemeral --disable codex_hooks --cd <cwd>` because a Stop-hook command can invoke that public CLI surface directly without new client code.
- Resolved default: the hook should read a repo-local active-loop state file and self-filter by `session_id` plus `DOC_PATH`; without matching active state, it must no-op cheaply.
- Resolved default: if the hook is missing or `codex_hooks` is disabled, `implement-loop` must fail loud instead of claiming a degraded same-session fallback.
- Resolved default: Codex rollout must include hook installation and a real Codex-session exercise before the feature is called shipped.
<!-- arch_skill:block:research_grounding:end -->

<!-- arch_skill:block:current_architecture:start -->
# 4) Current Architecture (as-is)

## 4.1 On-disk structure

- Repo source of truth for the feature currently spans:
  - `skills/arch-step/SKILL.md`
  - `skills/arch-step/references/arch-implement-loop.md`
  - `skills/arch-step/references/arch-implement.md`
  - `skills/arch-step/references/arch-audit-implementation.md`
  - `skills/arch-step/references/artifact-contract.md`
  - `skills/arch-step/references/shared-doctrine.md`
  - `skills/arch-step/agents/openai.yaml`
  - `README.md`
  - `docs/arch_skill_usage_guide.md`
  - `Makefile`
- Copied runtime mirrors live at:
  - `~/.agents/skills/arch-step/`
  - `~/.codex/skills/arch-step/`
  - `~/.claude/skills/arch-step/`
  - `~/.gemini/skills/arch-step/`
- Current drift is concrete:
  - repo source uses `implement-loop`
  - all copied mirrors still use `implement-until-clean`
  - all copied mirrors still carry `references/arch-implement-until-clean.md`
  - `skills/arch-step/agents/openai.yaml` still omits `implement-loop` from `interface.default_prompt`
- Codex runtime reference truth for the in-session loop lives outside this repo in:
  - `/Users/aelaguiz/workspace/codex/codex-rs/core-skills/src/render.rs`
  - `/Users/aelaguiz/workspace/codex/codex-rs/core-skills/src/injection.rs`
  - `/Users/aelaguiz/workspace/codex/codex-rs/core/src/codex.rs`
  - `/Users/aelaguiz/workspace/codex/codex-rs/hooks/src/engine/discovery.rs`
  - `/Users/aelaguiz/workspace/codex/codex-rs/hooks/src/engine/dispatcher.rs`
  - `/Users/aelaguiz/workspace/codex/codex-rs/hooks/src/events/stop.rs`
  - `/Users/aelaguiz/workspace/codex/codex-rs/cli/src/main.rs`
  - `/Users/aelaguiz/workspace/codex/sdk/typescript/src/codex.ts`
  - `/Users/aelaguiz/workspace/codex/sdk/typescript/src/thread.ts`
  - `/Users/aelaguiz/workspace/codex/sdk/typescript/src/exec.ts`
  - `/Users/aelaguiz/workspace/codex/codex-rs/app-server-protocol/src/protocol/common.rs`
  - `/Users/aelaguiz/workspace/codex/codex-rs/app-server-protocol/src/protocol/v2.rs`
- This repo currently ships no `.codex/hooks.json`, no hook runner, and no loop-state contract.

## 4.2 Control paths (runtime)

- Skill activation path in Codex today:
  1. Codex renders available skills in the developer prompt surface.
  2. The user invokes `$arch-step` or the UI inserts a structured skill mention.
  3. Codex turns that input into `UserInput::Skill` or text mentions for the current turn.
  4. Core recomputes mentioned skills from current input, resolves the matching `SKILL.md`, and injects it as `SkillInstructions`.
  5. Skill behavior is therefore turn-scoped prompt injection, not a persistent runtime service.
- Loop doctrine path in this repo today:
  1. `implement-loop` exists only as doctrine and packaging in `arch-step`.
  2. It delegates actual work to `implement` and `audit-implementation`.
  3. The repo does not currently install the Stop hook required to make the loop real in Codex, so the command is not backed by actual runtime automation today.
- Stop-hook path in Codex today:
  1. Hooks are discovered from config-layer folders such as project `.codex/`.
  2. Stop handlers are selected without matcher filtering.
  3. Discovery accepts only synchronous command handlers; `prompt`, `agent`, and `async: true` command hooks are skipped.
  4. Stop hook input includes `cwd`, `session_id`, `turn_id`, `transcript_path`, `last_assistant_message`, `model`, `permission_mode`, and `stop_hook_active`.
  5. A Stop hook can block with a non-empty continuation reason and core will append that reason as synthetic user input and continue the same turn.
  6. Multiple Stop hooks are preserved and their continuation fragments are merged in display order.
- Fresh-context path in Codex today:
  - top-level CLI exposes `codex resume` and `codex fork`
  - `codex exec` exposes `--ephemeral` and `resume`, but not an `exec fork` surface
  - the TS SDK exposes `startThread()` and `resumeThread()` and implements turns through fresh CLI subprocesses
  - the lower-level app-server protocol exposes `thread/start`, `thread/resume`, and `thread/fork`

## 4.3 Object model + key abstractions

- Planning state:
  - `DOC_PATH` is the canonical artifact
  - `implement-loop` is the explicit controller contract
  - `implement` is the single code-writing pass contract
  - `audit-implementation` is the docs-only audit contract
- Packaging state:
  - repo source under `skills/arch-step/`
  - copied runtime mirrors managed by `Makefile`
- Codex runtime state:
  - turn-scoped skill injection
  - turn-scoped Stop hook execution
  - fresh child subprocess or thread primitives
- Missing runtime state in this repo:
  - no shipped `.codex/hooks.json`
  - no repo-owned hook runner asset
  - no repo-local `.codex/implement-loop-state.json` contract

## 4.4 Observability + failure behavior today

- `codex_hooks` is under development and default-off.
- Stop hooks are limited to synchronous command handlers.
- Stop hooks cannot rely on matcher-based selectivity.
- Invalid Stop-hook block output fails rather than degrading into a block.
- Same-turn continuation is real in Codex, but only if a valid Stop hook is installed and enabled.
- Without that hook, `implement-loop` has no deterministic re-entry point and therefore no real automatic loop.
- Repo-source correctness does not propagate to installed mirrors until install runs.
- Every copied runtime mirror is currently stale for this feature.

## 4.5 UI surfaces (ASCII mockups, if UI work)

- Not a UI change.
<!-- arch_skill:block:current_architecture:end -->

<!-- arch_skill:block:target_architecture:start -->
# 5) Target Architecture (to-be)

## 5.1 On-disk structure (future)

- `skills/arch-step/` remains the sole canonical owner of the command.
- Repo-owned supporting surfaces stay aligned with it:
  - `skills/arch-step/agents/openai.yaml`
  - `skills/arch-step/scripts/implement_loop_stop_hook.py`
  - `skills/arch-step/scripts/upsert_codex_stop_hook.py`
  - `README.md`
  - `docs/arch_skill_usage_guide.md`
  - `Makefile`
- `Makefile` owns both copied skill propagation and the Codex hook install/update path.
- The working Codex install surface includes:
  - the copied skill under `~/.codex/skills/arch-step/`
  - a generated or updated `~/.codex/hooks.json` entry that points at the installed hook runner
- Active runtime loop state lives in the target repo at `.codex/implement-loop-state.json` and is created and cleared by the command and hook flow; it is runtime state, not a second plan artifact.

## 5.2 Control paths (future)

- Hook-backed Codex flow:
  1. The user invokes `$arch-step implement-loop DOC_PATH` in an existing Codex session.
  2. `implement-loop` verifies that the Codex hook path is installed and enabled enough to work; if not, it fails loud instead of claiming a degraded loop.
  3. `implement-loop` writes or refreshes `.codex/implement-loop-state.json` with explicit `DOC_PATH`, command identity, and any other minimal fields the hook needs to self-filter safely.
  4. `implement-loop` runs one `implement` pass against that doc.
  5. When Codex tries to stop, the installed Stop hook runs.
  6. Because Stop hooks ignore matchers, the hook command reads `.codex/implement-loop-state.json`, claims the current `session_id` into state on the first matching stop, verifies ownership on later stops, and otherwise exits without effect.
  7. For an active loop, the hook launches a fresh child audit context through `codex exec --ephemeral --disable codex_hooks --cd <cwd>`.
  8. The child audit receives explicit `DOC_PATH` and current repo working context and runs `audit-implementation` in fresh context.
  9. The child audit updates `DOC_PATH`, and the hook reads the authoritative `Verdict (code)` from that doc.
  10. The hook routes that result deterministically:
     - `clean`: clear the active loop state and allow stop
     - `continue`: return a continuation prompt so Codex keeps going in the same turn
     - `blocked child-audit failure`: clear the active loop state and return one final continuation prompt so the parent can surface the blocker honestly and stop on the next attempt
- No fake fallback path:
  - without the installed hook path, there is no automatic loop
  - prompt-only same-session repetition does not count as this feature

## 5.3 Object model + abstractions (future)

- Prompt/native-capability responsibilities:
  - resolve the command
  - reason over the plan doc
  - write the active loop-state file
  - run implementation passes
  - clear loop state before stopping on a real blocker
  - consume continuation prompts produced by the hook
- Deterministic runtime responsibilities:
  - discover and run hooks
  - claim the current `session_id` into loop state on first matching stop
  - self-filter stop events against active loop state
  - block or continue the same turn
  - create the fresh audit subprocess
  - clear loop state on `clean` or `blocked`
  - install copied skill and hook assets
- Required contract surfaces:
  - `implement-loop`
  - `implement`
  - `audit-implementation`
  - `skills/arch-step/scripts/implement_loop_stop_hook.py`
  - `~/.codex/hooks.json`
  - `.codex/implement-loop-state.json`
- Forbidden abstractions:
  - non-hook prompt-only looping presented as real automation
  - second loop skill
  - sticky hidden session-state assumptions
  - unsupported `prompt` or `agent` hook designs
  - unbounded autonomous daemon behavior

## 5.4 Invariants and boundaries

- Repo source remains the canonical owner.
- Copied runtime mirrors must converge before rollout can be called complete.
- `skills/arch-step/agents/openai.yaml` must stay aligned with the public command surface.
- No hook, no loop.
- If the hook path is missing or disabled, `implement-loop` must fail loud.
- Stop-hook selectivity lives inside the hook command, not in matcher config.
- The hook must self-filter by active loop state and `session_id`, not by vague heuristics.
- Fresh audit children must receive explicit `DOC_PATH`.
- Stop-hook-launched child audits must disable hooks or use an equivalent recursion guard.
- The automated Codex meaning of `implement-loop` is hook-backed only.
- No second skill, no second plan artifact, and no unsupported hook type may be introduced.

## 5.5 UI surfaces (ASCII mockups, if UI work)

- Not a UI change.
<!-- arch_skill:block:target_architecture:end -->

<!-- arch_skill:block:call_site_audit:start -->
# 6) Call-Site Audit (exhaustive change inventory)

## 6.1 Change map (table)

| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| ---- | ---- | ------------------ | ---------------- | --------------- | --- | ------------------ | -------------- |
| Repo skill contract | `skills/arch-step/SKILL.md` | frontmatter description, command-shaped trigger list, public command surface, explicit controller block, reference map | repo source already names `implement-loop` but still leaves room for host-dependent interpretation | rewrite the command as hook-backed Codex automation and fail-loud when the hook path is absent | this is the primary user-facing owner | hook-backed `implement-loop` | `npx skills check` |
| Repo agent shim | `skills/arch-step/agents/openai.yaml` | `interface.default_prompt` | still lists `implement` then `audit-implementation` but omits `implement-loop` | add the final command surface or deliberately narrow the shim | repo-owned invocation guidance must not drift from the shipped skill | `implement-loop` | `npx skills check` |
| Controller contract | `skills/arch-step/references/arch-implement-loop.md` | hard rules, loop procedure, hook requirement, loop-state contract | bounded loop exists but still allows a fake non-hook reading | require installed hook, define `.codex/implement-loop-state.json`, and make missing-hook behavior fail loud | removes the fake automation story | hook-backed `implement-loop` | `npx skills check` |
| Implementation pass | `skills/arch-step/references/arch-implement.md` | single-pass note | already framed as the subordinate execution pass | keep single-pass ownership explicit | preserve split between implementation and audit | `implement` under `implement-loop` | `npx skills check` |
| Audit pass | `skills/arch-step/references/arch-audit-implementation.md` | audit-pass note | already framed as the subordinate audit pass | keep docs-only audit semantics explicit | the loop only works if audit truth stays independent | `audit-implementation` under `implement-loop` | `npx skills check` |
| Shared doctrine | `skills/arch-step/references/artifact-contract.md` | canonical state objects, write-boundary rule | repo source already treats `implement-loop` as code-writing | keep ownership and write boundaries aligned with any final contract edits | prevents stale contract claims | `implement-loop` | `npx skills check` |
| Shared doctrine | `skills/arch-step/references/shared-doctrine.md` | worktree and execution discipline | repo source already lists `implement-loop` as code-writing | keep cross-command doctrine aligned | avoid partial convergence | `implement-loop` | `npx skills check` |
| Hook runner | `skills/arch-step/scripts/implement_loop_stop_hook.py` | Stop-hook command entrypoint | no repo-owned hook runner exists today | add the deterministic hook runner that reads loop state, spawns fresh audit, and routes stop-versus-continue | the feature is not real without this file | Codex Stop-hook command | real Codex session plus install verification |
| Hook install helper | `skills/arch-step/scripts/upsert_codex_stop_hook.py` | install-time `hooks.json` upsert and verification | no repo-owned helper exists today | add the minimal hook-config helper so local and remote installs can update Codex config without clobbering unrelated hooks | install behavior must stay deterministic and repeatable | installed `arch-step` Stop hook | `make verify_install` |
| Public docs | `README.md` | skill inventory, install surfaces, examples | repo docs already mention `implement-loop` | keep install, rollout, and examples aligned with final rollout scope | public docs are part of the shipped surface | `implement-loop` | `npx skills check` |
| Public docs | `docs/arch_skill_usage_guide.md` | examples and controller explanation | repo docs already mention `implement-loop` | keep usage guidance aligned with final runtime wording | users rely on this for operational guidance | `implement-loop` | `npx skills check` |
| Install propagation | `Makefile` | skill install targets plus Codex hook install/update and verify targets | install copies whole skill directories into four mirrors but does not install the Codex hook | add hook install/update so Codex rollout actually ships the feature | copied skills alone do not create a loop | copied `implement-loop` plus `~/.codex/hooks.json` | `make verify_install` |
| Codex config | `~/.codex/hooks.json` | Stop-hook registration | no installed `arch-step` hook entry exists today | install and verify a Stop-hook entry that points at the installed hook runner | this is the runtime trigger that makes the loop real | installed `arch-step` Stop hook | `make verify_install` plus real Codex session |
| Runtime state contract | `.codex/implement-loop-state.json` | active loop metadata keyed by current session | no deterministic loop-state handoff exists today | define the minimal fields and lifecycle for active-loop state | the hook needs a cheap deterministic way to know whether to act | active loop-state contract | real Codex session |
| Installed mirror | `/Users/aelaguiz/.agents/skills/arch-step/SKILL.md` | copied skill body | stale, still uses `implement-until-clean` | overwrite through install as part of rollout | current local agents runtime is stale | copied `implement-loop` surface | manual check or `make verify_install` |
| Installed mirror | `/Users/aelaguiz/.codex/skills/arch-step/SKILL.md` | copied skill body | stale, still uses `implement-until-clean` | overwrite through install as part of rollout | current local Codex mirror is stale | copied `implement-loop` surface | manual check or `make verify_install` |
| Installed mirror | `/Users/aelaguiz/.claude/skills/arch-step/SKILL.md` | copied skill body | stale, still uses `implement-until-clean` | overwrite through install as part of rollout | current local Claude mirror is stale | copied `implement-loop` surface | manual check or `make verify_install` |
| Installed mirror | `/Users/aelaguiz/.gemini/skills/arch-step/SKILL.md` | copied skill body | stale, still uses `implement-until-clean` | overwrite through install as part of rollout | current local Gemini mirror is stale | copied `implement-loop` surface | manual check or `make verify_install` |
| Installed mirror | copied `references/arch-implement-until-clean.md` in all four runtime mirrors | old controller reference file | stale old reference still exists in every installed mirror | remove by reinstalling the copied skill directories | copied mirrors still point at the old reference path | copied `arch-implement-loop.md` surface | manual check or `make verify_install` |
| Codex runtime reference | `/Users/aelaguiz/workspace/codex/codex-rs/core-skills/src/render.rs`, `/Users/aelaguiz/workspace/codex/codex-rs/core-skills/src/injection.rs`, `/Users/aelaguiz/workspace/codex/codex-rs/core/src/codex.rs`, `/Users/aelaguiz/workspace/codex/codex-rs/protocol/src/user_input.rs` | `render_skills_section`, `collect_explicit_skill_mentions`, `build_skill_injections`, turn input handling | skill activation is recomputed per turn and injected as current-turn instructions | keep doctrine and any controller design explicit per turn; do not assume sticky skill state | this is the real runtime constraint for in-session looping | turn-scoped `arch-step` invocation | none in this repo |
| Codex runtime reference | `/Users/aelaguiz/workspace/codex/codex-rs/hooks/src/engine/discovery.rs`, `/Users/aelaguiz/workspace/codex/codex-rs/hooks/src/engine/dispatcher.rs`, `/Users/aelaguiz/workspace/codex/codex-rs/hooks/src/events/stop.rs`, `/Users/aelaguiz/workspace/codex/codex-rs/core/src/codex.rs` | hook discovery, `select_handlers`, `StopRequest`, stop continuation | Stop hooks are matcherless, sync command-only, same-turn continuation surfaces | build the feature directly on that hook path and keep selectivity in the hook command | this is the actual runtime trigger | required Codex Stop-hook path | real Codex session |
| Codex runtime reference | `/Users/aelaguiz/workspace/codex/codex-rs/cli/src/main.rs`, `/Users/aelaguiz/workspace/codex/sdk/typescript/src/exec.ts`, `/Users/aelaguiz/workspace/codex/codex-rs/exec/src/cli.rs`, `/Users/aelaguiz/workspace/codex/codex-rs/exec/src/lib.rs` | `--disable`, `--ephemeral`, `CodexExec.run`, child exec bootstrap | public CLI subprocess surfaces exist for a fresh child audit | use `codex exec --ephemeral --disable codex_hooks --cd <cwd>` as the shipped child-audit path | keeps the hook implementation on a public surface | required fresh audit child context | real Codex session |

## 6.2 Migration notes

* Canonical owner path / shared code path:
  - `skills/arch-step/` is the only owning skill surface.
- `Makefile` is the propagation path into copied runtime mirrors and the Codex hook install surface.
  - `codex_hooks` remains an explicit Codex feature gate; install does not auto-edit `~/.codex/config.toml`.
* Deprecated APIs (if any):
  - `implement-until-clean`
  - copied `references/arch-implement-until-clean.md`
* Delete list (what must be removed; include superseded shims/parallel paths if any):
  - stale copied `references/arch-implement-until-clean.md` in `.agents`, `.codex`, `.claude`, and `.gemini` mirrors during rollout
* Capability-replacing harnesses to delete or justify:
  - reject prompt-only looping as a fake parallel control path
  - the only allowed controller surface in this plan is the Codex Stop hook plus fresh child audit subprocess
* Live docs/comments/instructions to update or delete:
  - `skills/arch-step/agents/openai.yaml`
  - `~/.codex/hooks.json`
  - copied skill mirrors in `.agents`, `.codex`, `.claude`, and `.gemini`
  - public docs and install instructions because the hook is now part of the shipped feature
* Behavior-preservation signals for refactors:
  - `npx skills check`
  - `git diff --check`
  - `make verify_install`
  - real Codex session validation for hook-owned continue-or-stop behavior

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)

| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude) |
| ---- | ------------- | ---------------- | ---------------------- | ------------------------------------- |
| Repo owner surfaces | `skills/arch-step/agents/openai.yaml` | same final command surface as `SKILL.md` | avoids repo-internal invocation drift | include |
| Public docs | `README.md`, `docs/arch_skill_usage_guide.md` | same final command name and rollout language | prevents user-visible naming drift | include |
| Install mirrors | copied `arch-step` skill directories | copied mirror should exactly match repo source after install | prevents runtime/source divergence | include |
| Codex user config | `~/.codex/hooks.json` | shipped `arch-step` Stop-hook entry | without it there is no real automatic loop | include |
| Runtime state contract | `.codex/implement-loop-state.json` | one deterministic active-loop state file | prevents vague hook triggering and fake automation | include |
| Codex repo code | `~/workspace/codex` runtime files | code changes in Codex itself | outside current repo scope unless later phases explicitly widen scope | exclude |
| Custom wrapper/controller tooling | any new script in this repo | bespoke loop runner | avoid architecture theater when native hooks and fresh child contexts already exist | exclude |
<!-- arch_skill:block:call_site_audit:end -->

<!-- arch_skill:block:phase_plan:start -->
# 7) Depth-First Phased Implementation Plan (authoritative)

WORKLOG_PATH: `docs/ARCH_STEP_IMPLEMENT_LOOP_CLEAN_AUDIT_2026-04-10_WORKLOG.md`

> Rule: systematic build, foundational first; every phase has exit criteria + explicit verification plan (tests optional). Refactors, consolidations, and shared-path extractions must preserve existing behavior with the smallest credible signal. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly (delete superseded paths). Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests (deletion checks, visual constants, doc-driven gates). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).

Warn-first note:
- `external_research_grounding` remains not started, but that is non-blocking here because the decisive constraints are already grounded in repo-owned skill surfaces and local Codex runtime code.

## Phase 1 - Rewrite the repo-owned contract around “no hook, no loop”

Status: COMPLETE

Completed work:
- Rewrote the live `arch-step` doctrine so `implement-loop` is explicitly hook-backed and fails loud when the Codex hook path is absent or disabled.
- Synced `skills/arch-step/agents/openai.yaml`, `README.md`, and `docs/arch_skill_usage_guide.md` to the same hook-only contract.
- Tightened the loop-state contract so the first Stop-hook pass claims `session_id` instead of asking the prompt to guess it.

* Goal:
- Make the repo-owned `arch-step` package tell one truthful story: actual Codex automation is hook-backed, and prompt-only looping does not count.

* Work:
- Update `skills/arch-step/agents/openai.yaml` so the repo-owned shim exposes the same public command surface as `skills/arch-step/SKILL.md`.
- Tighten `skills/arch-step/references/arch-implement-loop.md` and any directly affected supporting references so the hook requirement, fail-loud behavior, and loop-state contract are explicit.
- Sync `README.md` and `docs/arch_skill_usage_guide.md` to the final hook-backed contract.
- Remove any wording that markets a non-hook same-session loop as a real feature.

* Verification (smallest signal):
- `npx skills check`
- `git diff --check`
- `rg -n "implement-until-clean|implement-loop" skills/arch-step README.md docs/arch_skill_usage_guide.md`

* Docs/comments (propagation; only if needed):
- Update touched live docs and instructions in the same phase; no new code comments unless a canonical boundary becomes surprisingly easy to misuse.

* Exit criteria:
- Repo-owned surfaces use one command name, one hook-backed loop contract, and one explicit statement that missing hook path means the feature is unavailable.
- `skills/arch-step/agents/openai.yaml` is no longer drifted from the owning skill surface.

* Rollback:
- Revert any wording that creates a second control surface or reintroduces fake non-hook automation claims.

## Phase 2 - Ship the Codex hook path

Status: COMPLETE

Completed work:
- Added `skills/arch-step/scripts/implement_loop_stop_hook.py` as the installed Stop-hook runner.
- Added `skills/arch-step/scripts/upsert_codex_stop_hook.py` so local and remote installs can upsert and verify the Codex hook entry without clobbering unrelated hooks.
- Updated `Makefile` so `make install` now installs the Codex hook entry and `make verify_install` validates it.
- Refreshed the local installed skill mirrors through `make install`.

* Goal:
- Install the hook runner and Codex hook config so the feature exists at runtime instead of only in docs.

* Work:
- Add `skills/arch-step/scripts/implement_loop_stop_hook.py` as the deterministic Stop-hook runner.
- Add `skills/arch-step/scripts/upsert_codex_stop_hook.py` so install and verify can upsert the Codex hook entry without clobbering unrelated hooks.
- Update `Makefile` so Codex install writes or updates the `~/.codex/hooks.json` entry that points at the installed hook runner and refreshes the copied `~/.codex/skills/arch-step/` surface.
- Refresh the copied skill mirrors so `implement-loop` replaces `implement-until-clean` everywhere the repo still owns those installs.
- Keep Codex repo code changes out of scope.

* Verification (smallest signal):
- `npx skills check`
- `git diff --check`
- `make verify_install`
- targeted `rg` against `~/.codex/hooks.json` and the copied runtime mirrors

* Docs/comments (propagation; only if needed):
- Keep `README.md`, Section 9, and Section 10 honest about the shipped hook install surface.

* Exit criteria:
- `make install` or the equivalent install path leaves Codex with both the updated skill mirror and the installed `arch-step` Stop hook.
- The repo no longer claims the feature is shipped without that hook.

* Rollback:
- Revert any partial hook-install claim instead of leaving docs and runtime in disagreement.

## Phase 3 - Validate real Codex stop-and-continue behavior, then audit

Status: IN PROGRESS

Completed work:
- Verified the installed hook entry in `~/.codex/hooks.json`.
- Enabled `codex_hooks` locally and confirmed the feature gate is on.
- Ran a real `codex exec` session in this repo with the installed hook path active and no loop state armed; the session completed cleanly.
- Started a live installed-hook probe with an armed `.codex/implement-loop-state.json`; the hook claimed `session_id` and launched a nested fresh `codex exec` audit as designed.

Blocked on:
- The live fresh-audit probe did not finish inside this run, so hook-owned continue-versus-stop evidence is still incomplete.

* Goal:
- Prove the hook-backed loop actually works in a real Codex session and reopen anything falsely marked done.

* Work:
- Exercise `$arch-step implement-loop DOC_PATH` in a real Codex session with the hook installed.
- Confirm the hook no-ops when no active loop state exists, spawns a fresh child audit when active state exists, and deterministically routes `clean`, `continue`, and `blocked`.
- Run `audit-implementation` against the finished repo state and reopen anything false-complete in repo surfaces, install surfaces, or runtime behavior.

* Verification (smallest signal):
- `npx skills check`
- `git diff --check`
- `make verify_install`
- real Codex session evidence of hook-owned continue-or-stop behavior

* Docs/comments (propagation; only if needed):
- Update Section 8, Section 9, and Section 10 to reflect the actual shipped hook behavior and runtime validation.

* Exit criteria:
- The final audit verdict matches what is truly shipped for this run.
- No touched live instruction surface still points at the old command name or claims a non-hook automation path.
- A real Codex session proves the hook is the thing deciding whether the loop stops or continues.

* Rollback:
- Reopen the affected phase and clear any premature completion claims rather than papering over disagreement between repo source, installed hook state, and observed Codex behavior.
<!-- arch_skill:block:phase_plan:end -->

# 8) Verification Strategy (common-sense; non-blocking)

- Use repo-native validation first:
  - `npx skills check`
  - `git diff --check`
- Use targeted text searches to catch stale command names, drifted install docs, or hook-install drift.
- Treat `make verify_install` as required because the shipped feature includes the Codex hook install surface.
- Required runtime check before claiming success:
  - inspect `~/.codex/hooks.json`
  - inspect `~/.codex/skills/arch-step/`
  - confirm `codex features list` shows `codex_hooks` enabled
  - exercise a real Codex session and confirm the hook owns continue-versus-stop behavior
- Manual non-blocking checks for the remaining copied mirrors:
  - inspect `~/.agents/skills/arch-step/SKILL.md`
  - inspect `~/.claude/skills/arch-step/SKILL.md`
  - inspect `~/.gemini/skills/arch-step/SKILL.md`
  - restart the relevant clients after install

# 9) Rollout / Ops / Telemetry

- The shipped Codex feature is not just repo doctrine; rollout includes the installed `~/.codex/hooks.json` entry plus the copied `~/.codex/skills/arch-step/` surface.
- `make install` must leave Codex with the updated skill mirror and the installed hook before the feature is called shipped.
- `codex_hooks` still has to be enabled explicitly; install does not auto-edit `~/.codex/config.toml`.
- Restart Codex after install so the runtime picks up both the skill and the hook config.
- No new telemetry is required for the repo-local hook-backed delivery change itself.

# 10) Decision Log (append-only)

- 2026-04-10 - Bootstrapped this canonical artifact during `research` because no existing full-arch doc governed the `implement-loop` work.
- 2026-04-10 - Locked scope to the existing `arch-step` surface; no new skill is allowed for this feature.
- 2026-04-10 - Codex code under `~/workspace/codex` is reference truth for runtime capability and constraints, not an implementation target in this repo by default.
- 2026-04-10 - Current repo source and copied installed agents skill surface are already drifted on the command name (`implement-loop` vs `implement-until-clean`); later phases must either fix or explicitly defer copied-surface rollout.
- 2026-04-10 - Deep-dive confirmed this repo currently ships doctrine and copied skill packages only; it does not ship `.codex/hooks.json` or a loop runner.
- 2026-04-10 - Deep-dive confirmed all four local runtime mirrors are stale and still carry both the old command name and the old controller reference file.
- 2026-04-10 - Preferred Codex fast path is same-turn Stop-hook continuation plus a fresh child audit context, with hook selectivity inside the hook command and explicit recursion guarding.
- 2026-04-10 - For `arch_skill`-owned optional Codex guidance, the practical child-audit path is Stop hook -> `codex exec --ephemeral --disable codex_hooks --cd <cwd>`; deeper native Codex integrations should prefer app-server `thread/fork(thread_id, ephemeral: true)`.
- 2026-04-10 - Hook automation remains an optional Codex optimization rather than always-on `implement-loop` doctrine because `codex_hooks` is under development, default-off, and not shipped by this repo.
- 2026-04-10 - Phase planning locked a package-first execution order: converge repo-owned surfaces first, treat copied-mirror refresh as an explicit rollout-boundary choice, then audit against the chosen scope.
- 2026-04-10 - Superseded the fake optional-hook framing: for this feature, no hook means no loop, and prompt-only repetition does not count as a working implementation.
- 2026-04-10 - North Star now requires a shipped Codex Stop hook plus fresh child audit subprocess; real stop-versus-continue control belongs to the hook, not to best-effort prompt behavior.
- 2026-04-10 - Deep-dive consistency pass aligned research, call-site audit, and rollout language to the hook-only requirement; earlier optional-hook and package-first assumptions are historical and superseded.
- 2026-04-10 - Implementation tightened the loop-state contract so the first Stop-hook invocation claims `session_id`; the prompt only has to arm the loop with `DOC_PATH`.
- 2026-04-10 - Install now writes `~/.codex/hooks.json`, but Codex feature enablement remains explicit via `codex features enable codex_hooks` instead of silently rewriting user config.
