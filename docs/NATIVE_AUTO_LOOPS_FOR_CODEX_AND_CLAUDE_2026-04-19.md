---
title: "arch_skill - native auto loops for Codex and Claude Code - Architecture Plan"
date: 2026-04-19
status: active
fallback_policy: forbidden
owners: [aelaguiz]
reviewers: []
doc_type: parity_plan
related:
  - skills/arch-step/SKILL.md
  - skills/arch-docs/SKILL.md
  - skills/delay-poll/SKILL.md
  - skills/arch-step/scripts/arch_controller_stop_hook.py
  - skills/arch-step/scripts/upsert_codex_stop_hook.py
  - skills/arch-step/scripts/upsert_claude_stop_hook.py
  - README.md
  - Makefile
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/settings
---

# TL;DR

- Outcome:
  - Ship the repo's auto-loop-enabled skill surface so it works natively in both Codex and Claude Code, with each runtime using its intended hook model and with the same user-facing contract wherever parity is actually supportable.
- Problem:
  - Today the auto-loop story is real in Codex and either missing or hacked in Claude Code. Claude has first-class hooks, but the current local pattern is a Claude Stop hook feeding a Codex-oriented controller, which is not the repo-owned or Claude-native design the user asked for.
- Approach:
  - Separate the shared auto-controller contract from runtime-specific hook implementation details. Keep one truthful skill/doctrine layer for loop-capable workflows, then add a Claude-native install, state, and verification path that uses Claude's intended settings-level hook model instead of piggybacking on Codex assumptions.
- Plan:
  - Inventory every shipped auto-loop-enabled skill and current controller surface, ground the Codex and Claude runtime contracts from real docs and local installs, choose the native Claude control pattern, then phase the repo changes so skill doctrine, controller code, install surfaces, and verification converge without fake parity claims.
- Non-negotiables:
  - No shipping Claude support as a thin wrapper around Codex controller semantics.
  - No fake parity claims without real hook-backed execution in both runtimes.
  - No new parallel skill surfaces for the same workflows.
  - No silent fallback mode when a runtime cannot actually continue the loop.
  - Real research and local runtime testing are required before claiming the plan is ready or shipped.

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-04-19
external_research_grounding: not started
deep_dive_pass_2: done 2026-04-19
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
note: This block tracks stage order only. It never overrides readiness blockers caused by unresolved decisions.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

If this repo refactors its auto-loop-enabled skill family around one shared runtime-agnostic contract and implements a repo-owned Claude-native hook/controller path alongside the existing Codex-native path, then the same skill family can offer real hook-backed looping in both runtimes without relying on a Claude Stop hook that delegates to Codex-specific behavior. If any loop mode cannot be supported cleanly in Claude on Claude's own terms, that mode must remain explicitly unsupported instead of shipping as a hack.

## 0.2 In scope

- Every shipped skill or command in this repo whose live contract promises automatic looping, hook-backed continuation, or hook-owned stop-versus-continue control.
- The shared controller doctrine for those skills, including when they are allowed to claim automation and when they must fail loud.
- Runtime-specific controller ownership for Codex and Claude Code:
  - hook install surfaces
  - hook settings and discovery model
  - controller state ownership
  - recursion guards
  - fresh external review or check strategy
  - stop-versus-continue semantics
- Repo-owned verification and install surfaces that must truthfully support both runtimes:
  - `Makefile`
  - `README.md`
  - skill docs and agent shims
  - verification commands
- Local research and live runtime testing needed to prove the chosen Claude design is real, not theoretical.

## 0.3 Out of scope

- Shipping Claude support by keeping the current "Claude hook calls a Codex-oriented controller" pattern as the final design.
- Extending this plan to Gemini or other runtimes unless later research shows a touched surface must move for correctness.
- Broad redesign of non-auto skills that do not promise looped or hook-backed behavior.
- Forcing identical internals across Codex and Claude when the runtimes legitimately need different native hook machinery.
- New fallback shims, background daemons, or speculative orchestration layers whose main job is hiding runtime mismatch.

## 0.4 Definition of done (acceptance evidence)

- The plan names the full in-scope auto-loop-enabled surface and the current gaps between shared doctrine, Codex runtime truth, and Claude runtime truth.
- The target architecture says plainly what is shared across runtimes and what is runtime-specific.
- The repo install surface can install and verify the required Codex and Claude hook/controller paths from repo-owned files.
- Each in-scope skill has one truthful runtime contract:
  - supported in both Codex and Claude
  - or explicitly unsupported in one runtime with a grounded reason
- Local runtime testing proves at least one real hook-backed continue cycle in Codex and one in Claude using the supported repo install path.
- Missing-hook or disabled-hook cases fail loud in both runtimes instead of pretending looped automation still exists.
- `README.md`, `docs/arch_skill_usage_guide.md`, and touched skill surfaces agree on the final support story.

## 0.5 Key invariants (fix immediately if violated)

- No Claude-as-Codex wrapper story in the shipped design.
- No fake automation when the real hook path is absent or disabled.
- No dual sources of truth for the auto-controller contract.
- No silent drift between repo source and installed skill mirrors.
- No regression of the currently working Codex auto-loop behavior without explicit preservation proof.
- Prefer native prompt, hook, and runtime capabilities before inventing extra scripts or wrappers.
- No runtime fallbacks or shims unless the plan later gets an explicit approved exception with a timeboxed removal path.

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)

1. Make Claude support real on Claude's own terms, not just cosmetically present.
2. Preserve the already-shipped Codex auto-loop behaviors while converging toward a shared contract.
3. Keep one truthful public story for loop-capable skills across repo docs, installed mirrors, and runtime installers.
4. Make install and verification first-class so parity claims are grounded in runnable local truth.
5. Keep the architecture bounded; do not turn loop support into a generic autonomous orchestration platform.

## 1.2 Constraints

- Codex and Claude expose different hook configuration surfaces and different native hook capabilities.
- The repo currently installs a Codex hook path directly, but not a repo-owned Claude hook path.
- Some live skill surfaces explicitly market hook-backed automation as Codex-only today.
- Claude support must be grounded in current official Claude Code hook behavior and real local testing, not analogy from Codex.
- The design must stay self-contained in the live repo surfaces rather than depending on ad hoc machine-local edits.

## 1.3 Architectural principles (rules we will enforce)

- One shared skill contract, runtime-native controllers.
- Fail loud when hook-backed continuation is unavailable.
- Keep runtime-specific behavior in the smallest owning install/controller surface.
- Reuse native hook lifecycle and settings models before inventing wrapper processes.
- Preserve one canonical owner path for each loop-capable workflow; no parallel skill surfaces.

## 1.4 Known tradeoffs (explicit)

- The same user-facing skill may need different controller internals in Codex and Claude.
- Some currently shipped auto modes may need to stay Codex-only if Claude cannot support them cleanly.
- Adding real Claude parity likely increases install and verification complexity.
- Shared doctrine may need to become more explicit about runtime support boundaries, which could narrow previously fuzzy claims.

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today

- The repo already ships multiple skills that promise hook-backed or auto-looped behavior.
- Codex has a repo-owned install path for the shared controller hook.
- Claude Code has first-class hooks, but the repo does not yet own a native Claude install and verification path for the loop-capable skill family.
- Current local Claude wiring can trigger the shared controller, but that controller still assumes Codex-oriented execution paths.

## 2.2 What's broken / missing (concrete)

- The repo cannot honestly say that all auto-loop-enabled skills work natively in both Codex and Claude Code.
- Claude support is not yet expressed as a repo-owned, runtime-native contract.
- Install, verification, and docs are not yet converged around a dual-runtime story.
- The current architecture leaves open whether loop behavior is shared, runtime-specific, or partially hacked together.

## 2.3 Constraints implied by the problem

- The plan must inventory all loop-capable skills before it proposes shared abstractions.
- Claude design choices must be grounded in Claude's official hook model and proven locally.
- Any convergence work must preserve working Codex behavior while avoiding Codex leakage into Claude's final design.
- The final support story must be simple enough that users can install, verify, and trust it without local tribal knowledge.

<!-- arch_skill:block:research_grounding:start -->
# 3) Research Grounding (external + internal "ground truth")

## 3.1 External anchors (papers, systems, prior art)

- `https://code.claude.com/docs/en/hooks` - adopt Claude's official settings-level `Stop` hook model, `decision: "block"` stop control, `stop_hook_active`, and the supported hook handler types (`command`, `http`, `prompt`, `agent`) as the native Claude continuation surface; reject async hooks as the primary controller because async hooks cannot block or control Claude's behavior after the action completes.
- `https://code.claude.com/docs/en/settings` - adopt Claude's settings JSON hierarchy as the official installation surface. Default recommendation: if arch_skill keeps its current machine-local installer posture, the Claude hook install target should be `~/.claude/settings.json`, not ad hoc local edits and not target-repo-owned `.claude/settings.json` by default.
- `https://code.claude.com/docs/en/hooks-guide` - adopt Claude's intended operational model of hook-driven workflow automation and explicit debugging/inspection rather than treating Claude support as a Codex compatibility shim.

## 3.2 Internal ground truth (code as spec)

- Authoritative behavior anchors (do not reinvent):
  - `Makefile` - repo-owned install and verification surface. It installs one Codex hook through `codex_install_hook`, installs Claude skills through `claude_install_skill`, and `verify_claude_install` checks only skill copies and stale prompt cleanup, not Claude hooks.
  - `README.md` - public support contract. It explicitly markets `arch-step auto-plan`, `implement-loop`, `auto-implement`, `arch-docs auto`, `audit-loop auto`, `comment-loop auto`, `audit-loop-sim auto`, and `delay-poll` as Codex-only automatic controllers backed by `~/.codex/hooks.json`.
  - `docs/arch_skill_usage_guide.md` - the longer operator guide repeats the same Codex-only continuation story and names the one repo-managed Codex `Stop` hook as the runtime owner for the current auto-controller family.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - current shared controller runner. It already emits Claude-compatible stop-control JSON (`decision: "block"` and `continue` / `stopReason`), but the controller state lives under `.codex/...` and every fresh audit / evaluator / review path shells out to `codex exec`, proving the shipped implementation is still Codex-shaped underneath.
  - `skills/arch-step/scripts/upsert_codex_stop_hook.py` - only repo-owned hook installer today. There is no parallel Claude settings upsert helper in the repo.
- Canonical path / owner to reuse:
  - `skills/arch-step/scripts/` - canonical shared controller implementation path for the suite's hook-backed auto controllers.
  - `Makefile`, `README.md`, and `docs/arch_skill_usage_guide.md` - canonical install, verify, and public support-story surfaces that must stay in sync with any runtime parity change.
- Adjacent surfaces tied to the same contract family:
  - `skills/arch-step/SKILL.md` - owns `auto-plan`, `implement-loop`, and `auto-implement`.
  - `skills/miniarch-step/SKILL.md` - trimmed full-arch auto controllers with the same parity problem.
  - `skills/arch-docs/SKILL.md`, `skills/audit-loop/SKILL.md`, `skills/comment-loop/SKILL.md`, and `skills/audit-loop-sim/SKILL.md` - all ship `auto` modes that are currently Codex-only by contract.
  - `skills/delay-poll/SKILL.md` - Codex-only delay controller today, and it is not included in `CLAUDE_SKILLS` in `Makefile`, so Claude parity for the full auto family is currently incomplete even at install time.
  - `~/.claude/settings.json` - current local machine has a Stop hook pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`, but that path is outside the repo-owned install contract, so local Claude behavior can drift from repo truth.
- Compatibility posture (separate from `fallback_policy`):
  - Preserve the existing Codex automatic-controller contract.
  - For Claude, use a clean cutover from today's unsupported or machine-local-hacky state to one repo-owned native hook/install path.
  - No timeboxed bridge that keeps Claude support piggybacking on Codex-specific execution as the shipped behavior.
- Existing patterns to reuse:
  - `skills/arch-step/scripts/upsert_codex_stop_hook.py` - idempotent upsert-and-verify pattern for runtime hook registration.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - one runner dispatching across multiple controller-state files, with session-scoped file resolution and fail-loud state validation.
  - `README.md` - existing session-scoped state-file contract (`.codex/...<SESSION_ID>.json`) that already prevents concurrent Codex runs from trampling each other.
- Prompt surfaces / agent contract to reuse:
  - `skills/arch-step/SKILL.md`, `skills/miniarch-step/SKILL.md`, `skills/arch-docs/SKILL.md`, `skills/audit-loop/SKILL.md`, `skills/comment-loop/SKILL.md`, `skills/audit-loop-sim/SKILL.md`, and `skills/delay-poll/SKILL.md` - these are the live runtime contracts that currently declare which auto modes are Codex-only and therefore must become the authoritative surfaces for any Claude parity or explicit Claude exclusions.
  - `Makefile` `CLAUDE_SKILLS` and `README.md` installed-path inventory - these define which skills Claude even receives today, separate from whether their hook-backed auto modes actually work there.
- Native model or agent capabilities to lean on:
  - Claude hooks natively support `command`, `prompt`, and `agent` handlers on `Stop`; the controller does not need a fake second orchestration product to continue work.
  - The installed Claude CLI (`claude 2.1.114`) exposes `--settings`, `--debug-file`, `--include-hook-events`, and `--setting-sources`, which gives a real hook-suppressed child path plus a real debugging surface for Claude-native controller work.
  - Codex already has working hook continuation and `codex exec --ephemeral --disable codex_hooks`, so preserving Codex while splitting runtime-specific execution is practical.
- Existing grounding / tool / file exposure:
  - Claude's official Stop-hook input includes `session_id`, `transcript_path`, `cwd`, `permission_mode`, `stop_hook_active`, and `last_assistant_message`, which is enough to implement session-scoped controller routing without transcript scraping as the first move.
  - `~/.claude/settings.json` is the official local Claude config surface, and `.claude/settings.json` is the official repo-scoped shared surface if later planning decides the target repo should own Claude hook config instead of this installer.
  - Claude exposes a `/hooks` browser plus debug output, while Codex already exposes the installed `~/.codex/hooks.json` and feature flag status.
- Duplicate or drifting paths relevant to this change:
  - The repo owns Codex hook installation, but not Claude hook installation.
  - The shared runner already speaks Claude's stop-control JSON, but its subprocess model is still hardcoded to `codex exec`.
  - Claude receives most of the relevant skills via `CLAUDE_SKILLS`, but those same skill docs still describe the auto modes as Codex-only.
  - `delay-poll` is excluded from Claude install today even though the user asked for all auto-loop-enabled skills to work in both runtimes if support is truly possible.
- Capability-first opportunities before new tooling:
  - Use Claude's official settings-level Stop hook before inventing a plugin, daemon, or repo-policing wrapper.
  - Keep deterministic runtime ownership in a hook installer plus shared controller code, but let Claude-native `prompt` or `agent` hook evaluation remain a candidate for lightweight stop decisions where a full child CLI run would be unnecessary.
  - Prefer command-line hook suppression via `--settings '{"disableAllHooks":true}'` for Claude child runs, because it avoids hook recursion while keeping the host's normal auth path intact.
- Behavior-preservation signals already available:
  - `npx skills check` - required repo validation for skill-package changes.
  - `make verify_install` - current install validation surface; it already proves Codex hook install truth and would need to grow a Claude hook verification story.
  - `python3 -m py_compile skills/arch-step/scripts/*.py` - cheap preservation signal if controller installer or runner scripts change.
  - Real local runtime proof is available for both CLIs:
    - Codex hook state and feature gate can be exercised directly.
    - Claude has an installed local CLI plus official hook-debug surfaces and a live local settings file.

## 3.3 Decision gaps that must be resolved before implementation

- Resolved default: the first shipped Claude controller path uses one repo-managed settings-level `Stop` command hook as the deterministic dispatcher. Claude `prompt` or `agent` hooks remain optional future optimizations, not the primary suite controller surface.
- Resolved default: the repo-managed Claude install target is `~/.claude/settings.json`, because this repo's install model is machine-local skill installation rather than editing downstream project repos. Optional project-scoped Claude hook install is deferred unless later implementation evidence makes it necessary.
- Resolved default: `delay-poll` stays inside the parity target. If implementation later proves that Claude cannot support it cleanly under the same quality bar, the plan must be repaired explicitly instead of silently leaving it Codex-only.
<!-- arch_skill:block:research_grounding:end -->

<!-- arch_skill:block:current_architecture:start -->
# 4) Current Architecture (as-is)

## 4.1 On-disk structure

- Repo-owned source of truth for the current auto-controller family spans:
  - `skills/arch-step/scripts/arch_controller_stop_hook.py`
  - `skills/arch-step/scripts/upsert_codex_stop_hook.py`
  - `skills/arch-step/SKILL.md`
  - `skills/miniarch-step/SKILL.md`
  - `skills/arch-docs/SKILL.md`
  - `skills/audit-loop/SKILL.md`
  - `skills/comment-loop/SKILL.md`
  - `skills/audit-loop-sim/SKILL.md`
  - `skills/delay-poll/SKILL.md`
  - the matching `references/auto.md`, `references/arm.md`, `references/arch-auto-plan.md`, and `references/arch-implement-loop.md` files for those skills
  - `Makefile`
  - `README.md`
  - `docs/arch_skill_usage_guide.md`
- Runtime installation today is asymmetric:
  - `~/.agents/skills/*` is the shared installed skill mirror for Codex and the generic local agent surface
  - `~/.codex/hooks.json` gets one repo-managed `Stop` hook entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`
  - `~/.claude/skills/*` gets copied skills, but no repo-managed Claude hook entry is installed or verified
  - `CLAUDE_SKILLS` in `Makefile` excludes `delay-poll`, so Claude does not even receive the full current auto-controller family
- Repo-local controller state today is Codex-shaped:
  - `.codex/auto-plan-state.<SESSION_ID>.json`
  - `.codex/implement-loop-state.<SESSION_ID>.json`
  - `.codex/miniarch-step-auto-plan-state.<SESSION_ID>.json`
  - `.codex/miniarch-step-implement-loop-state.<SESSION_ID>.json`
  - `.codex/arch-docs-auto-state.<SESSION_ID>.json`
  - `.codex/audit-loop-state.<SESSION_ID>.json`
  - `.codex/comment-loop-state.<SESSION_ID>.json`
  - `.codex/audit-loop-sim-state.<SESSION_ID>.json`
  - `.codex/delay-poll-state.<SESSION_ID>.json`
- The shared runner also still recognizes legacy unsuffixed `.codex/<controller>-state.json` files, so even the migration layer is Codex-specific today.
- The installed hook command strings today are also runtime-implicit:
  - Codex currently calls the runner as bare `python3 .../arch_controller_stop_hook.py`
  - the current unmanaged local Claude settings file uses the same bare command string
  - there is no explicit runtime argument or env var telling the shared runner which host contract it should enforce
- Local Claude behavior can exist outside repo truth because `~/.claude/settings.json` may be edited manually. The current local machine does have a Stop hook pointing at the shared runner, but that is not owned or verified by this repo.

## 4.2 Control paths (runtime)

- Codex control path today:
  1. The user invokes an auto controller such as `$arch-step auto-plan`, `$arch-step implement-loop`, `$arch-docs auto`, or `$delay-poll`.
  2. The parent pass preflights `~/.codex/hooks.json`, the installed runner path, and `codex_hooks`, then writes a session-scoped `.codex/...<SESSION_ID>.json` state file.
  3. The parent pass does one truthful work unit and ends the turn naturally.
  4. Codex runs the installed `Stop` hook.
  5. `arch_controller_stop_hook.py` resolves the active controller state for the current session, reads doc or ledger truth, and either:
     - feeds the next literal command by returning block/continue JSON, or
     - launches a fresh child `codex exec --ephemeral --disable codex_hooks` run for audit/review/check work, then returns continue-or-stop JSON based on the result.
  6. Codex continues the same visible thread or stops cleanly.
- Claude control path today:
  1. The repo's public docs and skill doctrine still describe the auto controllers as Codex-only, so there is no repo-owned supported Claude path.
  2. If a local Claude `Stop` hook points at the same runner, Claude can invoke the runner and the runner can read `session_id` / `cwd` and emit Claude-compatible stop-control JSON.
  3. That local path is still not native in repo terms because the runner's active state surfaces and child subprocess behavior remain Codex-specific:
     - state discovery is `.codex/...`
     - fresh audit/review/check work shells out to `codex exec`
  4. Result: Claude support exists only as local drift or a compatibility accident, not as a shipped repo contract.

## 4.3 Object model + key abstractions

- `arch_controller_stop_hook.py` is one shared dispatcher over all current controller families.
- The dispatcher keys controller ownership through `ControllerStateSpec`, which currently carries:
  - relative state path
  - expected command string
  - display name
- Runtime is not yet a first-class input to the dispatcher; the current shared runner has one code path and one child-execution model, both effectively Codex-shaped.
- The active controller families today are:
  - `arch-step` `auto-plan`
  - `arch-step` `implement-loop`
  - `miniarch-step` `auto-plan`
  - `miniarch-step` `implement-loop`
  - `arch-docs auto`
  - `audit-loop auto`
  - `comment-loop auto`
  - `audit-loop-sim auto`
  - `delay-poll`
- Progress truth lives in the canonical plan doc or ledger. The session-scoped state file is only the armed controller state, not a progress ledger.
- Session scoping is derived from `session_id` and appended to the relative path; the runner also validates the claimed command and session before honoring any state file.
- Fresh external auditing or checking is implemented in the runner itself, not in the skill docs. That implementation is currently hard-wired to Codex CLI child runs.

## 4.4 Observability + failure behavior today

- Codex is repo-owned and fail-loud:
  - `verify_codex_install` checks for exactly one repo-managed `Stop` entry in `~/.codex/hooks.json`
  - every auto-controller doctrine names the same Codex preflight
  - the runner stops or blocks loudly on missing doc paths, invalid state payloads, duplicate controllers, child-run failures, blank or invalid structured output, and mismatched sessions
- Claude has native observability available, but the repo does not currently own it:
  - official runtime surfaces include `/hooks`, `--debug-file`, and `--include-hook-events`
  - no repo command verifies Claude hook presence or correctness
  - README and skill docs do not tell users how Claude auto controllers are supposed to work because the repo still claims they are Codex-only
- Current failure behavior is therefore asymmetric:
  - missing Codex hook support is a first-class unsupported state
  - missing Claude hook support is mostly invisible at repo level because Claude is not yet a supported automatic-controller runtime

## 4.5 UI surfaces (ASCII mockups, if UI work)

- There is no visual UI. The user-facing surface is the same command language across runtimes, but only Codex currently has a real automatic continuation path:

```text
User command -> parent pass -> repo-local controller state -> Stop hook -> shared runner
             -> next literal command OR fresh child audit/review/check -> continue or stop
```
<!-- arch_skill:block:current_architecture:end -->

<!-- arch_skill:block:target_architecture:start -->
# 5) Target Architecture (to-be)

## 5.1 On-disk structure (future)

- Keep the canonical auto-controller implementation under `skills/arch-step/scripts/`.
- Preserve the stable installed hook entrypoint path `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`.
- Keep `upsert_codex_stop_hook.py` for Codex and add a sibling `upsert_claude_stop_hook.py` that installs and verifies one repo-managed Claude `Stop` hook entry in `~/.claude/settings.json`.
- Make runtime explicit at installation time:
  - Codex installs `python3 .../arch_controller_stop_hook.py --runtime codex`
  - Claude installs `python3 .../arch_controller_stop_hook.py --runtime claude`
- Do not rely on payload-shape inference, transcript-path heuristics, or cwd conventions to guess the host runtime.
- Extend the living install surfaces in `Makefile`, `README.md`, and `docs/arch_skill_usage_guide.md` so Codex and Claude support are both repo-owned and explicit.
- Expand `CLAUDE_SKILLS` to include `delay-poll`, because the parity target includes the full current auto-controller family.
- Preserve existing Codex repo-local state paths under `.codex/`.
- Introduce a Claude repo-local transient state namespace under `.claude/arch_skill/`, for example:
  - `.claude/arch_skill/auto-plan-state.<SESSION_ID>.json`
  - `.claude/arch_skill/implement-loop-state.<SESSION_ID>.json`
  - `.claude/arch_skill/arch-docs-auto-state.<SESSION_ID>.json`
  - corresponding state files for the rest of the controller family
- Do not add a second plugin system, daemon, service, or user-facing controller binary.

## 5.2 Control paths (future)

- Codex path is preserved as the currently shipped runtime:
  - same `~/.codex/hooks.json` install target
  - same user-facing commands
  - same `.codex/...<SESSION_ID>.json` state files
  - same `codex exec --ephemeral --disable codex_hooks` child-run pattern where fresh external audit/review/check context is required
- Claude path becomes a first-class native runtime:
  1. The user invokes the same auto-controller command in Claude.
  2. The parent pass preflights `~/.claude/settings.json` for the repo-managed `Stop` hook entry and the installed shared runner path.
  3. The parent pass writes a session-scoped Claude controller state file under `.claude/arch_skill/`.
  4. The turn ends naturally.
  5. Claude runs the repo-managed settings-level `Stop` command hook.
  6. The shared runner resolves the matching Claude state for the current session and controller.
  7. The runner either:
     - returns `{"decision":"block","reason":"..."}` to continue the same visible thread with the next literal command or next task instruction, or
     - returns `{"continue":false,"stopReason":"..."}` when the controller is clean or blocked.
  8. When a controller needs a fresh external audit/review/check context, the Claude runtime path launches a fresh `claude -p --settings '{"disableAllHooks":true}'` child process with explicit context and no hook recursion.
- The first shipped Claude controller surface is one settings-level `Stop` command hook. Claude `prompt` and `agent` hooks are not the dispatcher because the suite needs dynamic multi-controller routing, deterministic state validation, and long-running synchronous stop control.
- `delay-poll` remains synchronous and Stop-hook-owned in both runtimes. Do not move it to async hooks, because async hooks cannot block or control continuation after the hook returns.

## 5.3 Object model + abstractions (future)

- Keep one shared suite dispatcher, but make its runtime handling explicit rather than accidental.
- Introduce a runtime adapter split inside the shared controller surface:
  - explicit host runtime argument from the installed hook command
  - host preflight contract
  - state namespace resolution
  - fresh child process launcher
  - continue-versus-stop output shape
- The shared object model stays consistent across runtimes:
  - `DOC_PATH` or ledger remains the progress ledger
  - the state file remains armed controller state only
  - one session may arm only one controller at a time
  - all controller state files remain session-scoped and namespaced to avoid concurrent collisions
- Runtime-specific child execution becomes native:
  - Codex child work: `codex exec --ephemeral --disable codex_hooks`
  - Claude child work: `claude -p --settings '{"disableAllHooks":true}'` with explicit context and hook avoidance
- The shared runner parses the installer-owned runtime argument first, then:
  - resolves only that runtime's state namespace
  - applies only that runtime's preflight assumptions
  - launches only that runtime's child executor
  - emits the stop-control payload shape the host runtime expects
- The child-run split is by host runtime, not by user-facing command. A Claude flow must never shell out to `codex exec` as its authoritative fresh reviewer.
- Skill doctrine becomes host-aware rather than Codex-only:
  - same user-facing command names
  - runtime-specific preflight and state file paths
  - identical honesty rule: if the required hook install or feature/runtime support is absent, fail loud instead of pretending prompt-only looping exists

## 5.4 Invariants and boundaries

- One public command surface per workflow. No `auto-plan-claude`, `implement-loop-claude`, or parallel skill package.
- Codex behavior is preserved unless an explicit approved improvement is made.
- Claude support is a clean cutover from unsupported/manual drift to repo-owned native support.
- The stable shared hook entrypoint stays `arch_controller_stop_hook.py`; the design may refactor internals, but it must not create competing runtime entrypoints that drift.
- Repo-managed hook entries must identify their host runtime explicitly. Bare shared-runner command strings without `--runtime` are not part of the final supported install contract.
- No Codex subprocesses from the Claude runtime path.
- No prompt-only fallback if the hook install or runtime support is missing.
- No wrapper whose job is to fake deterministic behavior that the host runtime already supports natively.
- README, usage guide, Makefile, and every touched auto-controller skill/reference must tell the same runtime support story.

## 5.5 UI surfaces (ASCII mockups, if UI work)

- User-facing behavior stays intentionally uniform across runtimes:

```text
Codex or Claude user
  -> same auto-controller command
  -> host-specific preflight + session-scoped state file
  -> host Stop hook
  -> shared dispatcher
  -> next literal command or fresh host-native child audit/review/check
  -> continue same thread or stop cleanly
```
<!-- arch_skill:block:target_architecture:end -->

<!-- arch_skill:block:call_site_audit:start -->
# 6) Call-Site Audit (exhaustive change inventory)

## 6.1 Change map (table)

| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Codex install | `skills/arch-step/scripts/upsert_codex_stop_hook.py` | `expected_command`, `install_hook`, `verify_hook` | Owns the only repo-managed hook installer/verifier and writes a Codex `Stop` entry in `~/.codex/hooks.json` with a bare runner command | Preserve behavior, but update the installed command to identify `--runtime codex` and align messages and shared assumptions with the Claude installer | Codex must remain the preserved runtime while the suite grows dual-runtime support and the runner must not guess its host | Codex stays on one repo-managed `Stop` entry in `~/.codex/hooks.json`, now with an explicit runtime argument | `python3 -m py_compile`, real Codex install/verify |
| Claude install | `skills/arch-step/scripts/upsert_claude_stop_hook.py` | new file | No repo-owned Claude hook installer exists | Add idempotent install and verify for one repo-managed Claude `Stop` command hook in `~/.claude/settings.json`, using the official Claude settings schema and `--runtime claude` | Claude support cannot be native if the repo does not own the hook registration surface or if the shared runner still has to infer host runtime | Claude gets one repo-managed settings-level `Stop` entry pointing at the installed shared runner with an explicit runtime argument | `python3 -m py_compile`, real Claude install/verify |
| Shared dispatcher | `skills/arch-step/scripts/arch_controller_stop_hook.py` | arg parsing, controller specs, runtime dispatch, child-run helpers, `main()` | Dispatches all controllers, but uses only Codex-shaped state files and `codex exec` child runs, with no explicit host-runtime input | Refactor into a runtime-aware shared dispatcher that first parses installer-owned runtime identity, then preserves Codex and adds Claude-native state resolution plus hook-suppressed Claude child execution | This is the canonical owner for actual automatic continuation behavior and must not guess which host it is serving | One shared dispatcher, explicit runtime adapters, no Claude-to-Codex subprocess path, no payload-heuristic host inference | `python3 -m py_compile`, real Codex + Claude hook probes |
| Top-level install | `Makefile` | `CLAUDE_SKILLS`, `claude_install_skill`, `verify_claude_install`, `remote_install`, `verify_install` | Installs Claude skills only, excludes `delay-poll`, and does not install or verify Claude hooks | Add `delay-poll` to `CLAUDE_SKILLS`, add Claude hook install/verify wiring, and extend remote install accordingly | Install behavior must match the advertised runtime support surface | `make install` and `make verify_install` become truthful for both runtimes | `make verify_install`, remote spot check if needed |
| Public docs | `README.md` | install and shipped-skill sections | Markets automatic controllers as Codex-only and documents only the Codex hook path | Rewrite to a host-aware support story with explicit Codex and Claude requirements, state namespaces, and troubleshooting | Public contract must stop lying once Claude parity ships | Same user-facing commands, runtime-specific preflight, no fake parity claims | Re-read plus `rg` on stale Codex-only claims |
| Operator guide | `docs/arch_skill_usage_guide.md` | install, verify, workflow sections | Repeats the Codex-only controller story and Codex-only preflight commands | Rewrite to cover both runtimes, the new Claude installer/verify path, and the parity status of each auto controller | This is the detailed operator truth surface | One guide, explicit per-runtime requirements | Re-read plus `rg` on stale Codex-only claims |
| Full-arch auto-plan | `skills/arch-step/SKILL.md`, `skills/arch-step/references/arch-auto-plan.md` | `auto-plan` contract | Codex-only automatic planning controller using `.codex/auto-plan-state.<SESSION_ID>.json` | Make the contract host-aware, preserve Codex behavior, and add Claude preflight plus Claude state namespace | `arch-step auto-plan` is part of the parity target | Same command, runtime-specific hook preflight and state path | `npx skills check`, doc re-read |
| Full-arch delivery loop | `skills/arch-step/SKILL.md`, `skills/arch-step/references/arch-implement-loop.md` | `implement-loop`, `auto-implement` | Codex-only full-frontier controller using `.codex/implement-loop-state.<SESSION_ID>.json` and Codex child audits | Make the contract host-aware and require runtime-native fresh audit child behavior | The clean-auditor loop is central to the parity goal | Same command names, runtime-native fresh auditor | `npx skills check`, local loop probe per runtime |
| Mini full-arch controllers | `skills/miniarch-step/SKILL.md`, `skills/miniarch-step/references/arch-auto-plan.md`, `skills/miniarch-step/references/arch-implement-loop.md` | `auto-plan`, `implement-loop`, `auto-implement` | Codex-only or Codex-assumed automatic controllers | Apply the same host-aware split as `arch-step` | `miniarch-step` is explicitly in scope as an auto-controller family | Same commands, host-specific preflight and state namespace | `npx skills check`, local probe per runtime |
| Docs cleanup loop | `skills/arch-docs/SKILL.md`, `skills/arch-docs/references/auto.md`, `skills/arch-docs/references/internal-evaluator.md` | `auto` | Codex-only docs-cleanup controller with fresh external evaluator | Add Claude-native continuation and fresh evaluator path | `arch-docs auto` is in the parity target and relies on the same shared runner | Same `auto` command, host-specific evaluator child | `npx skills check`, read-only loop probe per runtime |
| Repo audit loop | `skills/audit-loop/SKILL.md`, `skills/audit-loop/references/auto.md` | `auto` | Codex-only auto controller that launches fresh `codex exec` review passes | Add Claude-native continuation and Claude-native fresh review path | Audit-loop parity must use the host runtime as the real reviewer | Same `auto` command, host-native fresh review | `npx skills check`, read-only loop probe per runtime |
| Comment loop | `skills/comment-loop/SKILL.md`, `skills/comment-loop/references/auto.md` | `auto` | Codex-only auto controller that launches fresh `codex exec` review passes | Add Claude-native continuation and Claude-native fresh review path | Comment-loop parity has the same controller boundary as audit-loop | Same `auto` command, host-native fresh review | `npx skills check`, read-only loop probe per runtime |
| Automation audit loop | `skills/audit-loop-sim/SKILL.md`, `skills/audit-loop-sim/references/auto.md` | `auto` | Codex-only real-app automation loop | Add Claude-native continuation and review path without inventing a second simulator orchestration story | This loop is part of the parity target and uses the shared runner | Same `auto` command, host-native review child | `npx skills check`, loop probe plus simulator sanity as needed |
| Delay controller | `skills/delay-poll/SKILL.md`, `skills/delay-poll/references/arm.md` | `delay-poll` | Codex-only, excluded from `CLAUDE_SKILLS`, and uses `.codex/delay-poll-state.<SESSION_ID>.json` | Include it in Claude install, make preflight host-aware, and add Claude state namespace while keeping synchronous Stop-hook waiting | The user asked for all auto-loop-enabled skills, and Claude's synchronous Stop hooks can support controlled waiting | Same `delay-poll` command, host-specific preflight and state path | `npx skills check`, real short-interval Claude + Codex wait probe |

## 6.2 Migration notes

- Canonical owner path / shared code path:
  - `skills/arch-step/scripts/arch_controller_stop_hook.py`
  - `skills/arch-step/scripts/upsert_codex_stop_hook.py`
  - `skills/arch-step/scripts/upsert_claude_stop_hook.py`
  - the touched auto-controller `SKILL.md` and reference files
  - `Makefile`, `README.md`, and `docs/arch_skill_usage_guide.md`
- Deprecated APIs (if any):
  - No user-facing command rename or replacement is planned. Existing command names stay authoritative.
- Delete list (what must be removed; include superseded shims/parallel paths if any):
  - Codex-only claims in touched auto-controller docs once Claude support is shipped
  - the shared runner docstring and any hardcoded wording that still describes the suite runner as Codex-only
  - any remaining Claude-to-Codex subprocess path inside the shared runner
  - bare repo-managed hook command entries that do not identify `--runtime codex` or `--runtime claude`
  - `delay-poll` exclusion from `CLAUDE_SKILLS`
  - reliance on machine-local unmanaged Claude hook edits as if they were part of the repo contract
- Adjacent surfaces tied to the same contract family:
  - `README.md`
  - `docs/arch_skill_usage_guide.md`
  - `Makefile`
  - `skills/arch-step/SKILL.md`
  - `skills/miniarch-step/SKILL.md`
  - `skills/arch-docs/SKILL.md`
  - `skills/audit-loop/SKILL.md`
  - `skills/comment-loop/SKILL.md`
  - `skills/audit-loop-sim/SKILL.md`
  - `skills/delay-poll/SKILL.md`
  - the per-skill auto-controller reference files listed in the change map
- Compatibility posture / cutover plan:
  - Preserve Codex command names, preflight shape, and `.codex/...<SESSION_ID>.json` state paths.
  - Perform a clean cutover for Claude from unsupported/manual drift to one repo-managed `~/.claude/settings.json` Stop-hook install path.
  - Do not ship a bridge where Claude controllers still depend on `codex exec`.
- Capability-replacing harnesses to delete or justify:
  - Do not add a plugin-only hook layer, parser wrapper, daemon, or orchestration service.
  - Use official Claude settings hooks and command-line hook suppression before inventing new deterministic scaffolding.
- Live docs/comments/instructions to update or delete:
  - `README.md`
  - `docs/arch_skill_usage_guide.md`
  - all touched auto-controller `SKILL.md` and reference files
  - the shared runner docstring and any stale internal comments that still describe a Codex-only runtime
- Behavior-preservation signals for refactors:
  - `npx skills check`
  - `python3 -m py_compile skills/arch-step/scripts/*.py`
  - `make verify_install`
  - direct inspection of the installed hook command strings in `~/.codex/hooks.json` and `~/.claude/settings.json`
  - real local Codex and Claude controller probes, including at least one successful continuation and one fail-loud missing-hook case per runtime

## 6.3 Pattern Consolidation Sweep (anti-blinders; scoped by plan)

| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude/blocker question) |
| --- | --- | --- | --- | --- |
| Full-arch controllers | `skills/arch-step/*auto*`, `skills/miniarch-step/*auto*` | Host-aware shared-controller contract with runtime-native hook preflight | Prevents `arch-step` and `miniarch-step` from drifting into different parity stories | include |
| Looping support skills | `skills/arch-docs/*auto*`, `skills/audit-loop/*auto*`, `skills/comment-loop/*auto*`, `skills/audit-loop-sim/*auto*` | Same shared dispatcher plus host-native fresh review/evaluator child behavior | These controllers all share the same stop-hook contract family | include |
| Wait controller | `skills/delay-poll/*` and `Makefile` `CLAUDE_SKILLS` | Same dual-runtime controller contract with synchronous Stop-hook waiting | Prevents `delay-poll` from becoming the one permanent Codex-only exception without proof | include |
| Install + docs surfaces | `Makefile`, `README.md`, `docs/arch_skill_usage_guide.md` | One runtime support story and one install/verify story | Prevents repo docs from diverging from actual hook install behavior | include |
| Shared host boundary | `skills/arch-step/scripts/upsert_*_stop_hook.py`, `skills/arch-step/scripts/arch_controller_stop_hook.py` | Installer-owned explicit runtime identity (`--runtime codex|claude`) | Prevents brittle host inference and keeps one shared dispatcher honest across two runtimes | include |
| Project-scoped Claude settings install | repo-level `.claude/settings.json` support | Optional project-owned Claude hook install path | Useful later, but not required for this repo's current machine-local install model | defer |
| Non-auto operator skills | `codemagic-builds`, `amir-publish`, non-auto arch skills | Runtime auto-controller parity | These skills are outside the auto-loop contract family | exclude |
| Gemini runtime | `~/.gemini/skills/*` and Gemini docs | Full automatic controller parity | User ask and grounded research are about Codex and Claude only | exclude |
<!-- arch_skill:block:call_site_audit:end -->

<!-- arch_skill:block:phase_plan:start -->
# 7) Depth-First Phased Implementation Plan (authoritative)

WORKLOG_PATH: `docs/NATIVE_AUTO_LOOPS_FOR_CODEX_AND_CLAUDE_2026-04-19_WORKLOG.md`

> Rule: systematic build, foundational first; split Section 7 into the best sequence of coherent self-contained units, optimizing for phases that are fully understood, credibly testable, compliance-complete, and safe to build on later. If two decompositions are both valid, bias toward more phases than fewer. `Work` explains the unit and is explanatory only for modern docs. `Checklist (must all be done)` is the authoritative must-do list inside the phase. `Exit criteria (all required)` names the exhaustive concrete done conditions the audit must validate. Resolve adjacent-surface dispositions and compatibility posture before writing the checklist. Before a phase is valid, run an obligation sweep and move every required promise from architecture, call-site audit, migration notes, delete lists, verification commitments, docs/comments propagation, approved bridges, and required helper follow-through into `Checklist` or `Exit criteria`. The authoritative checklist must name the actual chosen work, not unresolved branches or "if needed" placeholders. Refactors, consolidations, and shared-path extractions must preserve existing behavior with credible evidence proportional to the risk. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly (delete superseded paths). If a bridge is explicitly approved, timebox it and include removal work; otherwise plan either clean cutover or preservation work directly. Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests and heuristic gates (deletion checks, visual constants, doc-driven gates, keyword or absence gates, repo-shape policing). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).

Warn-first note:
- `external_research_grounding` remains not started, but that is non-blocking here because the decisive runtime contracts are already grounded in official Claude docs, current local installs, and repo-owned install/controller code.

## Phase 1 - Establish explicit runtime identity and installer ownership

Status: COMPLETE

Completed work:
- Added `skills/arch-step/scripts/upsert_claude_stop_hook.py` and updated the Codex installer to require explicit `--runtime codex` / `--runtime claude` hook commands.
- Wired `Makefile` install and verify flows so the repo now owns both Codex and Claude hook installation, verification, and remote install behavior.
- Expanded the Claude install surface to include `delay-poll` and preserved the stable installed runner path under `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`.

* Goal:
- Make host runtime explicit and repo-owned so the shared dispatcher no longer has to guess whether it is serving Codex or Claude.

* Work:
- Create the Claude hook upsert/verify helper and update the Codex hook upsert helper so both installers own an explicit runtime-bearing command string.
- Wire `Makefile` install/verify surfaces around the new Claude hook installer and include `delay-poll` in `CLAUDE_SKILLS`.
- Update the shared runner only enough to parse and validate installer-owned runtime identity before deeper controller refactors build on it.

* Checklist (must all be done):
- Add `skills/arch-step/scripts/upsert_claude_stop_hook.py` with install and verify support for one repo-managed `Stop` command hook in `~/.claude/settings.json`.
- Update `skills/arch-step/scripts/upsert_codex_stop_hook.py` so its expected command string includes `--runtime codex`.
- Make the Claude hook installer write and verify `--runtime claude`.
- Update `Makefile` `claude_install_skill`, `verify_claude_install`, `verify_install`, and `remote_install` so the repo installs and verifies the Claude hook path.
- Add `delay-poll` to `CLAUDE_SKILLS` and ensure `NON_CLAUDE_SKILLS` still excludes only the intended non-Claude skills.
- Teach `skills/arch-step/scripts/arch_controller_stop_hook.py` to parse the explicit runtime argument and fail loud on missing or unsupported runtime values.
- Preserve the stable installed entrypoint path `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`.

* Verification (required proof):
- `python3 -m py_compile skills/arch-step/scripts/*.py`
- `make verify_install`
- Inspect the installed hook command strings in `~/.codex/hooks.json` and `~/.claude/settings.json`

* Docs/comments (propagation; only if needed):
- Add a short high-leverage internal comment near the shared runner's runtime adapter boundary if the argument-driven split would otherwise be easy to break accidentally.

* Exit criteria (all required):
- Codex install writes and verifies one repo-managed `Stop` hook entry with `--runtime codex`.
- Claude install writes and verifies one repo-managed `Stop` hook entry with `--runtime claude`.
- `delay-poll` is part of the Claude install surface.
- The shared runner no longer depends on payload heuristics or ambient assumptions to determine host runtime.

* Rollback:
- Revert the new installer wiring and explicit runtime parsing together; do not leave the repo with mismatched hook command expectations across runtimes.

## Phase 2 - Refactor the shared dispatcher into runtime-native adapters

Status: COMPLETE

Completed work:
- Refactored `skills/arch-step/scripts/arch_controller_stop_hook.py` around explicit runtime parsing, runtime-local state roots, and host-native child runners.
- Preserved Codex `.codex/...` session-scoped state and added Claude `.claude/arch_skill/...` session-scoped state with first-stop session claiming when needed.
- Removed authoritative Claude-to-Codex child execution and replaced it with hook-suppressed Claude child runs via `claude -p --settings '{"disableAllHooks":true}'`.

* Goal:
- Preserve Codex behavior while making the shared dispatcher truly dual-runtime internally.

* Work:
- Refactor `arch_controller_stop_hook.py` around runtime-aware state namespaces, preflight assumptions, child process launchers, and output helpers.
- Keep one shared dispatcher entrypoint and one controller-family model while splitting host-native execution cleanly.

* Checklist (must all be done):
- Introduce explicit runtime adapter boundaries in `skills/arch-step/scripts/arch_controller_stop_hook.py`.
- Preserve Codex state resolution under `.codex/...<SESSION_ID>.json`.
- Add Claude state resolution under `.claude/arch_skill/...<SESSION_ID>.json`.
- Preserve legacy Codex state compatibility only as far as needed to avoid breaking current installed users during reinstall-driven cutover.
- Route Codex fresh child work through `codex exec --ephemeral --disable codex_hooks`.
- Route Claude fresh child work through `claude -p --settings '{"disableAllHooks":true}'` with explicit context and no hook recursion.
- Ensure every controller family handled by the shared runner uses the current host runtime's state namespace and child execution path only.
- Preserve duplicate-controller detection, session validation, and fail-loud invalid-state behavior across both runtimes.
- Remove any remaining authoritative Claude-to-Codex subprocess path from the runner.

* Verification (required proof):
- `python3 -m py_compile skills/arch-step/scripts/*.py`
- deterministic hook payload probes for Codex and Claude runtime paths
- direct inspection that Claude controller state lands under `.claude/arch_skill/` and Codex state remains under `.codex/`

* Docs/comments (propagation; only if needed):
- Update or add succinct comments at the runtime adapter seam and state-namespace resolution helpers.

* Exit criteria (all required):
- The shared runner deterministically routes by explicit runtime argument.
- Codex controllers still use Codex state and Codex child execution.
- Claude controllers use Claude state and Claude child execution.
- No controller family in the Claude path shells out to `codex exec`.

* Rollback:
- Revert the runtime-adapter refactor as one unit if either runtime loses deterministic controller behavior.

## Phase 3 - Make every auto-controller doctrine surface host-aware

Status: COMPLETE

Completed work:
- Updated the in-scope auto-controller skill packages and agent shims to describe Codex and Claude runtime support truthfully with runtime-local state paths and fail-loud preflight.
- Repaired the last live doctrine leak found during proof by making the required `Stop` entry wording explicit about `--runtime codex` and `--runtime claude`.
- Kept the existing user-facing command names while removing stale Codex-only claims for the shipped dual-runtime surfaces.

* Goal:
- Bring the live skill contracts into alignment with the actual dual-runtime controller design.

* Work:
- Rewrite the touched `SKILL.md` and auto-controller reference files so they describe the same user-facing commands with runtime-specific preflight, state namespaces, and honest support boundaries.

* Checklist (must all be done):
- Update `skills/arch-step/SKILL.md` and `skills/arch-step/references/arch-auto-plan.md`.
- Update `skills/arch-step/references/arch-implement-loop.md`.
- Update `skills/miniarch-step/SKILL.md`, `skills/miniarch-step/references/arch-auto-plan.md`, and `skills/miniarch-step/references/arch-implement-loop.md`.
- Update `skills/arch-docs/SKILL.md`, `skills/arch-docs/references/auto.md`, and `skills/arch-docs/references/internal-evaluator.md`.
- Update `skills/audit-loop/SKILL.md` and `skills/audit-loop/references/auto.md`.
- Update `skills/comment-loop/SKILL.md` and `skills/comment-loop/references/auto.md`.
- Update `skills/audit-loop-sim/SKILL.md` and `skills/audit-loop-sim/references/auto.md`.
- Update `skills/delay-poll/SKILL.md` and `skills/delay-poll/references/arm.md`.
- Remove Codex-only claims in touched doctrine where Claude support is now real.
- Keep the same user-facing command names and fail-loud posture in both runtimes.

* Verification (required proof):
- `npx skills check`
- targeted `rg` over touched skills for stale Codex-only claims and stale `.codex/`-only instructions where Claude support should now exist

* Docs/comments (propagation; only if needed):
- None beyond the touched live doctrine surfaces; this phase is the doctrine propagation phase.

* Exit criteria (all required):
- Every in-scope auto-controller skill/reference describes the same runtime support story as the installed code.
- No touched doctrine surface still markets a dual-runtime-supported controller as Codex-only.
- Runtime-specific preflight and state-path instructions are explicit where the user needs them.

* Rollback:
- Revert doctrine changes together if they get ahead of the actual installed runtime behavior.

## Phase 4 - Update public install and operations truth surfaces

Status: COMPLETE

Completed work:
- Rewrote `README.md` and `docs/arch_skill_usage_guide.md` so install, verify, troubleshooting, and state-path guidance match the shipped dual-runtime controller design.
- Documented the repo-managed Codex and Claude hook locations, explicit runtime-bearing hook commands, and fail-loud behavior when hook support is missing or disabled.

* Goal:
- Make the repo's public install, verify, and usage docs match the shipped dual-runtime support contract.

* Work:
- Rewrite the public docs so they describe the supported runtimes, the install behavior, the verification story, and the fail-loud contract accurately.

* Checklist (must all be done):
- Update `README.md` install, verify, and shipped-skill sections.
- Update `docs/arch_skill_usage_guide.md` install, verification, and workflow guidance.
- Document the explicit runtime-bearing hook commands, Claude settings install target, runtime-specific state namespaces, and the supported parity scope.
- Document the fail-loud behavior when Codex or Claude hook support is missing or disabled.
- Remove stale Codex-only claims for controllers that now support Claude.
- Preserve explicit Codex-only wording only for any controller that still cannot support Claude after implementation proof.

* Verification (required proof):
- Re-read the touched docs end to end.
- `rg` for stale public Codex-only claims across `README.md` and `docs/arch_skill_usage_guide.md`

* Docs/comments (propagation; only if needed):
- This phase is the public-doc propagation phase; no extra comment work is expected.

* Exit criteria (all required):
- Public docs describe the actual installed support matrix and hook locations truthfully.
- A user can follow the docs to install and verify both runtimes without relying on local folklore.
- Public docs do not promise unsupported parity or hide runtime-specific requirements.

* Rollback:
- Revert the public doc rewrite if it gets ahead of shipped runtime behavior.

## Phase 5 - Prove the dual-runtime controllers with real local runs

Status: COMPLETE

Completed work:
- Proved real hook-backed continuation in both runtimes with auto-plan and short `delay-poll` fixtures, including Claude hook debug evidence and Codex stop-hook continuation evidence.
- Proved fail-loud missing-hook behavior in both runtimes by removing the runtime hook config, confirming the controller refused to arm, and restoring the managed install state afterward.
- Re-ran install verification on the restored local state and captured the remaining repo-verification caveat: `npx skills check` still fails only on the unrelated global `harden` update path.

* Goal:
- Establish real local proof that the shipped controllers continue and stop honestly in both runtimes.

* Work:
- Exercise at least one representative controller continuation in Codex and Claude, plus fail-loud missing-hook cases, and capture the results needed to support shipping.

* Checklist (must all be done):
- Run at least one real Codex auto-controller continuation through the repo-managed install path.
- Run at least one real Claude auto-controller continuation through the repo-managed install path.
- Run and confirm at least one fail-loud missing-hook or disabled-hook case in Codex.
- Run and confirm at least one fail-loud missing-hook or disabled-hook case in Claude.
- Run a short `delay-poll` proof in both runtimes or, if Claude `delay-poll` still fails the quality bar, stop and repair the plan before claiming parity is shipped.
- Inspect installed hook command strings after install to confirm the runtime-bearing commands actually landed in both runtimes.
- Update the plan or decision log truthfully if any controller remains unsupported after proof.

* Verification (required proof):
- `make verify_install`
- real local continuation transcripts or hook-driven turn outcomes for Codex and Claude
- any lightweight debug output needed from Claude (`/hooks`, `--debug-file`, or `--include-hook-events`) to confirm hook execution

* Docs/comments (propagation; only if needed):
- If proof changes the actual support matrix, update the relevant docs and doctrine in the same phase before calling the work complete.

* Exit criteria (all required):
- At least one real successful continuation is proven in Codex and one in Claude.
- At least one fail-loud unsupported case is proven in Codex and one in Claude.
- The shipped support matrix is backed by local proof rather than inference.
- If a claimed parity surface fails, the docs and plan reflect that truth immediately instead of shipping a quiet exception.

* Rollback:
- If Claude parity proof fails materially, stop and preserve Codex support; do not ship misleading dual-runtime claims.
<!-- arch_skill:block:phase_plan:end -->

# 8) Verification Strategy (common-sense; non-blocking)

## 8.1 Unit tests (contracts)

- Prefer existing lightweight checks around controller-state parsing, installer idempotence, and structured continue-or-stop verdict handling before inventing a new test harness.
- Use `python3 -m py_compile skills/arch-step/scripts/*.py` as the cheap syntax and import-sanity proof for installer and shared-runner changes.

## 8.2 Integration tests (flows)

- Verify repo install surfaces for both runtimes.
- Use deterministic hook payload probes where possible to test runner behavior without pretending they replace real runtime proof.
- Use `make verify_install` plus direct inspection of the installed hook command strings in `~/.codex/hooks.json` and `~/.claude/settings.json` to confirm the runtime-bearing hook contract actually landed.
- Run `npx skills check` after the touched skill doctrine surfaces change.

## 8.3 E2E / device tests (realistic)

- Run at least one real local Codex loop continuation and one real local Claude loop continuation through the supported install path.
- Prove the fail-loud case when the required hook path is missing or disabled.
- Include one real short-interval `delay-poll` proof in both runtimes unless implementation evidence forces an explicit supported-scope reduction.

# 9) Rollout / Ops / Telemetry

## 9.1 Rollout plan

- Roll out by truthful runtime support level. Do not market dual-runtime parity until both install and live runtime proof are in place.

## 9.2 Telemetry changes

- None expected. If temporary debug output is needed while proving the hook paths locally, treat it as operational troubleshooting rather than as a new shipped telemetry contract.

## 9.3 Operational runbook

- The final design must say how to install, verify, inspect, and troubleshoot the Codex and Claude controller paths without machine-specific folklore.

<!-- arch_skill:block:implementation_audit:start -->
# Implementation Audit (authoritative)
Date: 2026-04-19
Verdict (code): COMPLETE
Manual QA: n/a (non-blocking)

## Code blockers (why code is not done)
- None. Fresh audit against the full approved Phase 1-5 frontier found no missing required code, migration, delete, touched-doctrine cleanup, runtime-boundary work, or phase-exit proof that should reopen implementation.

## Reopened phases (false-complete fixes)
- None.

## Missing items (code gaps; evidence-anchored; no tables)
- None.

## Fresh audit evidence
- `skills/arch-step/scripts/upsert_codex_stop_hook.py`, `skills/arch-step/scripts/upsert_claude_stop_hook.py`, and `Makefile` now install and verify runtime-bearing Codex and Claude hook commands, and `make verify_install` passed against the installed surfaces.
- `skills/arch-step/scripts/arch_controller_stop_hook.py` requires `--runtime`, keeps Codex state under `.codex/`, keeps Claude state under `.claude/arch_skill/`, and routes fresh child work through host-native child launchers. A fresh search found no Claude runtime path routed to `codex exec`.
- `README.md`, `docs/arch_skill_usage_guide.md`, and the touched auto-controller skill/reference surfaces describe the host-aware support story, the runtime-specific hook entries, state namespaces, and fail-loud requirements without leaving supported dual-runtime controllers as Codex-only.
- Fresh verification run during this audit:
  - `python3 -m py_compile skills/arch-step/scripts/*.py` - passed.
  - `make verify_install` - passed.
  - installed hook command inspection in `~/.codex/hooks.json` and `~/.claude/settings.json` - passed.
  - deterministic Codex and Claude `auto-plan` Stop-hook payload probes - passed.
  - `codex features list | rg '^codex_hooks\s+.*\strue$'` - passed.
  - `npx skills check` ran and still reported only the unrelated global `harden` update failure; no local `arch_skill` package failure surfaced.

## Non-blocking follow-ups (manual QA / screenshots / human verification)
- Optional: use `$arch-docs` later if you want broader cleanup or retirement of the plan/worklog artifacts after the new controller surface has sat long enough to be comfortable.
<!-- arch_skill:block:implementation_audit:end -->

# 10) Decision Log (append-only)

## 2026-04-19 - Claude parity must be native, not piggybacked

Context

- The user wants all auto-loop-enabled skills to work in both Codex and Claude Code in the best way Claude intends, not as a hack.
- Current local evidence says Claude has first-class hooks, but the current local pattern still routes through a Codex-oriented controller path.

Options

- Keep the current Claude trigger around Codex-specific controller behavior.
- Build a repo-owned Claude-native controller and install path while preserving Codex-native behavior.
- Leave loop-capable skills Codex-only.

Decision

- Plan toward a repo-owned Claude-native design and treat Codex piggybacking as non-shippable for this goal.

Consequences

- The repo may need a real Claude install/verify surface and clearer runtime-specific doctrine.
- Some auto modes may remain explicitly unsupported in Claude if clean parity is not actually possible.

Follow-ups

- Ground the full in-scope surface and current runtime truth before phase planning.
- Confirm the exact Claude-native control pattern through official docs and local testing.

## 2026-04-19 - Use one shared dispatcher with per-runtime hook installers

Context

- The suite already has one shared Stop-hook dispatcher and one repo-owned Codex installer.
- Claude has a real native hook model, but the repo currently does not own the Claude install or child-execution story.

Options

- Keep the suite Codex-only and treat Claude as unsupported.
- Keep one shared dispatcher, preserve Codex as-is, add a repo-owned Claude settings installer, and make child execution host-native.
- Split into separate public controller binaries or separate Claude-only commands.

Decision

- Keep one shared dispatcher at the stable `arch_controller_stop_hook.py` entrypoint, preserve Codex behavior, add a repo-owned Claude `Stop` hook installer for `~/.claude/settings.json`, keep Codex state under `.codex/`, add Claude state under `.claude/arch_skill/`, and use host-native child execution (`codex exec` for Codex, `claude -p --settings '{"disableAllHooks":true}'` for Claude).

Consequences

- The install and verify surface must grow a Claude hook story.
- Every touched auto-controller doctrine surface must become host-aware instead of Codex-only.
- Claude support will no longer be allowed to shell out to `codex exec` as the authoritative fresh reviewer.
- `delay-poll` joins the parity implementation surface instead of staying excluded from Claude install.

Follow-ups

- Implement the Claude hook upsert and verification helper.
- Refactor the shared dispatcher around explicit runtime adapters and installer-owned runtime identity.
- Update the touched skill docs, references, README, and usage guide to the same support matrix.
- Prove one real local continuation in each runtime before claiming parity is shipped.

## 2026-04-19 - Host runtime identity is installer-owned, not inferred

Context

- The shared runner must serve both Codex and Claude.
- The current installed hook command strings are bare and do not identify which host contract the runner should enforce.
- Payload-based inference would be brittle because the two runtimes share core fields like `session_id`, `cwd`, and `hook_event_name`.

Options

- Infer host runtime from hook payload shape, transcript paths, or cwd conventions.
- Split into separate runtime-specific runner entrypoints.
- Keep one shared runner and make the installed hook command identify `--runtime codex` or `--runtime claude`.

Decision

- Keep one shared runner and make host runtime an installer-owned explicit argument in the repo-managed hook command.

Consequences

- Codex and Claude installers and verifiers must both own the exact expected command string.
- The shared runner can route state namespaces, preflight, child execution, and output shape deterministically without heuristics.
- Old bare repo-managed hook entries become stale install state and must be repaired by reinstall.

Follow-ups

- Update `upsert_codex_stop_hook.py` to write and verify the explicit Codex runtime argument.
- Implement `upsert_claude_stop_hook.py` with the explicit Claude runtime argument.
- Teach the shared runner to parse runtime first and dispatch only within that runtime's contract.

## 2026-04-19 - Claude child runs suppress hooks through settings, not `--bare`

Context

- Claude child review and check runs need a fresh host-native Claude context without recursively re-entering the same Stop hook.
- The first implementation attempt used `claude --bare`, but on this machine `--bare` also skipped the normal auth path and broke child-run usability.

Options

- Use `claude --bare` and accept its auth and environment restrictions.
- Use normal `claude -p` child runs and risk hook recursion.
- Use normal `claude -p` child runs with `--settings '{"disableAllHooks":true}'`.

Decision

- Use `claude -p --settings '{"disableAllHooks":true}'` for Claude child review and check runs.

Consequences

- Claude child runs stay host-native, avoid Stop-hook recursion, and preserve the machine's normal Claude auth path.
- The dispatcher must own a runtime-specific Claude child launcher instead of sharing the old Codex-only subprocess path.

Follow-ups

- Prove a real Claude child structured-output run with hooks disabled.
- Prove a real Claude Stop-hook continuation using the repo-managed install path.
- Keep live doctrine explicit that Claude fresh child runs depend on hook-suppressed auth-working `claude -p` execution.

<!-- arch_skill:block:consistency_pass:start -->
## Consistency Pass
- Reviewers: self-integrator
- Scope checked:
  - frontmatter, TL;DR, Sections 0 through 10
  - `planning_passes`
  - research, deep-dive, and phase-plan alignment
  - install/runtime boundary, migration notes, verification, and rollout alignment
- Findings summary:
  - Section 8 was under-specifying the concrete proof set implied by Section 7.
  - Section 9.2 still used vague telemetry wording instead of a clean expectation.
- Integrated repairs:
  - tightened Section 8 to include `python3 -m py_compile`, `make verify_install`, hook-command inspection, `npx skills check`, and explicit `delay-poll` proof expectations
  - tightened Section 9.2 to `None expected` with operational-debug wording instead of speculative telemetry language
- Remaining inconsistencies:
  - none
- Unresolved decisions:
  - none
- Unauthorized scope cuts:
  - none
- Decision-complete:
  - yes
- Decision: proceed to implement? yes
<!-- arch_skill:block:consistency_pass:end -->
