# Worklog

Plan doc: docs/NATIVE_AUTO_LOOPS_FOR_CODEX_AND_CLAUDE_2026-04-19.md

## Initial entry
- Run started.
- Current phase: Phase 1 - Establish explicit runtime identity and installer ownership

## Phase 1 (Establish explicit runtime identity and installer ownership) Progress Update
- Work completed:
  - Added the repo-owned Claude hook installer at `skills/arch-step/scripts/upsert_claude_stop_hook.py`.
  - Updated the Codex installer to require `--runtime codex` and the Claude installer to require `--runtime claude`.
  - Wired `Makefile` so install, verify, and remote install now own both runtime hook surfaces and include `delay-poll` in `CLAUDE_SKILLS`.
- Tests run + results:
  - `python3 -m py_compile skills/arch-step/scripts/*.py` - passed.
- Issues / deviations:
  - None at this phase.
- Next steps:
  - Refactor the shared dispatcher around explicit runtime adapters and runtime-local state.

## Phase 2 (Refactor the shared dispatcher into runtime-native adapters) Progress Update
- Work completed:
  - Refactored `skills/arch-step/scripts/arch_controller_stop_hook.py` to parse `--runtime`, use runtime-local state roots, and branch fresh child execution by host runtime.
  - Preserved Codex `.codex/...` state and added Claude `.claude/arch_skill/...` state with first-stop session claiming when needed.
  - Replaced the attempted Claude `--bare` child path with `claude -p --settings '{"disableAllHooks":true}'` after local proof showed `--bare` broke auth on this machine.
- Tests run + results:
  - `python3 -m py_compile skills/arch-step/scripts/*.py` - passed.
  - Hook-suppressed Claude child prompt and structured-output probes - passed.
- Issues / deviations:
  - `claude --bare` was rejected after local proof because it skipped the host auth path here.
- Next steps:
  - Rewrite the in-scope skill doctrine and public docs to the new runtime contract.

## Phase 3 (Make every auto-controller doctrine surface host-aware) Progress Update
- Work completed:
  - Updated the live auto-controller skill packages, references, and agent shims so they describe the same dual-runtime contract.
  - Removed stale Codex-only claims from the shipped dual-runtime surfaces.
  - Repaired the final runtime-wording leak after proof surfaced that several doctrine files still described the required `Stop` entry without `--runtime codex|claude`.
- Tests run + results:
  - `npx skills check` - failed only on the unrelated global `harden` update path; no local `arch_skill` package failure was surfaced.
- Issues / deviations:
  - The repo's required skill check still has an unrelated global-skill failure outside the touched surface.
- Next steps:
  - Finish public docs sync and runtime proof.

## Phase 4 (Update public install and operations truth surfaces) Progress Update
- Work completed:
  - Rewrote `README.md` and `docs/arch_skill_usage_guide.md` to the explicit dual-runtime install, verify, state-path, and fail-loud story.
  - Kept the public command surface unchanged while documenting the runtime-bearing hook commands and repo-managed install locations.
- Tests run + results:
  - Public docs were re-read after the rewrite.
  - Targeted repo searches were used to catch stale public Codex-only wording.
- Issues / deviations:
  - None at this phase.
- Next steps:
  - Run final install verification and full local runtime proof.

## Phase 5 (Prove the dual-runtime controllers with real local runs) Progress Update
- Work completed:
  - Proved a real Codex auto-plan continuation and a real Claude auto-plan continuation using the repo-managed hook installs.
  - Proved short `delay-poll` continuation in both runtimes.
  - Proved fail-loud missing-hook behavior in both runtimes and restored the managed hook state afterward.
  - Synced the plan doc with the final Claude child-run decision, phase completion truth, and clean implementation audit.
- Tests run + results:
  - `make install` - passed.
  - `make verify_install` - passed.
  - Installed hook command inspection in `~/.codex/hooks.json` and `~/.claude/settings.json` - passed.
  - Codex positive continuation proof - passed.
  - Claude positive continuation proof with hook debug evidence - passed.
  - Codex short `delay-poll` proof - passed.
  - Claude short `delay-poll` proof - passed.
  - Codex missing-hook fail-loud proof - passed.
  - Claude missing-hook fail-loud proof - passed.
- Issues / deviations:
  - `npx skills check` still fails only on the unrelated global `harden` update path.
- Next steps:
  - If desired later, run `$arch-docs` to retire or consolidate the planning artifacts after the new controller surface has baked.
