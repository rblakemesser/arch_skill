---
title: "arch_skill - Generic Wait Delay-Then-Execute Skill - Architecture Plan"
date: 2026-04-19
status: active
fallback_policy: forbidden
owners: [amir]
reviewers: []
doc_type: new_system
related:
  - skills/delay-poll/SKILL.md
  - skills/arch-step/scripts/arch_controller_stop_hook.py
---

# TL;DR

- **Outcome:** A new installable skill (`wait` or similar) that pauses the current Codex or Claude Code thread for a user-specified duration (e.g. `30m`, `1h`, `2d`) and then resumes with a literal follow-up prompt the user supplied up front. Falsifiable: after running `$wait 30m then <prompt>` the session goes idle, then ~30 minutes later the installed Stop hook resumes the same thread and runs `<prompt>` verbatim.
- **Problem:** The suite already has `delay-poll` for wait-and-recheck-a-condition flows and `/loop` / `schedule` for recurring work. There is no clean primitive for "sleep exactly this long, then do exactly this one thing." Users currently have to either hand-roll `ScheduleWakeup`, abuse `delay-poll` with a stub check, or schedule a remote agent when they really just want one pure delay.
- **Approach:** Reuse the existing `arch_skill` Stop-hook controller surface (the same runner `delay-poll` rides on) and arm a new tiny controller state that encodes `deadline_utc` + literal `resume_prompt`. No polling loop, no condition check - the hook just sleeps until the deadline and fires the resume prompt once. Parse common duration strings (`30m`, `1h`, `2d`, `90s`) into an absolute UTC deadline at arm time.
- **Plan:**
  1. Nail scope and duration grammar (this doc + North Star confirmation).
  2. Research current controller surface, state-file schema, and Stop-hook dispatch so the new skill plugs in without forking the runner.
  3. Deep-dive target architecture and call-site audit (new skill package, runner branch for `wait`, docs).
  4. Phase-plan the implementation in coherent units (runner support → skill package → install/test).
  5. Implement + audit.
- **Non-negotiables:**
  - Must be real hook-backed waiting in both Codex and Claude Code. No fake "set a reminder" stub.
  - `wait` is single-slot per session. Re-arming `wait` while `wait` state already exists for the same session overwrites the prior state (same semantics as every other arm-and-end-turn skill). Multiple different arch_skill controller kinds may be armed in the same session; the installed Stop hook dispatches one per turn in priority order (`wait` runs last). This matches the real runner, not an invented mutual-exclusion rule.
  - No polling, no condition re-check - this is strictly a one-shot delayed-resume primitive.
  - Default maximum wait window cap inherited from `delay-poll` (24h) unless the user explicitly raises it.
  - Fail-loud boundaries: unparseable durations, missing runtime preflight, missing Stop hook all refuse to arm rather than silently degrading.

<!-- arch_skill:block:implementation_audit:start -->
# Implementation Audit (authoritative)
Date: 2026-04-19
Verdict (code): COMPLETE
Manual QA: pending (non-blocking)

## Code blockers (why code is not done)
- None. The approved ordered code-bearing frontier — Phase 1 (Duration parser), Phase 2 (Runner wiring: spec, validator, handler, dispatch), Phase 3 (Skill package `skills/wait/`), and Phase 4 (Install surface + live routing docs) — is fully landed in code, backed by programmatic proof. Phase 5 is entirely manual smoke in fresh host sessions and is recorded as non-blocking per the skill's evidence-split rule.

## Reopened phases (false-complete fixes)
- None. Every code-bearing Phase 1-4 Checklist item and Exit criterion is satisfied against repo reality. No phase made a completion claim that the audit can falsify.

## Verified landings (evidence-anchored)
- Phase 1 (Duration parser) — COMPLETE
  - `skills/arch-step/scripts/arch_controller_stop_hook.py:353` defines `parse_wait_duration(text: str) -> int` backed by `_WAIT_DURATION_FULL_RE` (`^(?:[0-9]+[smhd])+$`), `_WAIT_DURATION_COMPONENT_RE`, and `_WAIT_UNIT_MULTIPLIERS = {s:1, m:60, h:3600, d:86400}`; per-component summation; fail-loud on empty, whitespace (leading/trailing/embedded), unknown units, zero/negative components, and duplicate units; accepts unordered components.
  - `tests/test_codex_stop_hook.py:1901` `WaitDurationParserTests` covers every accept case (`90s→90`, `30m→1800`, `1h→3600`, `2d→172800`, `1h30m→5400`, `2h15m30s→8130`, unordered `30s1h→3630`) and every reject case enumerated in the Phase 1 Checklist (empty, leading/trailing/embedded whitespace, unknown `w`/`y`/`ms`, zero, negative, duplicate `h`, natural-language `half an hour` and `30 minutes`).
  - `python3 -m unittest discover -s tests` reports 83 tests, 0 failures, 0 errors (well under the Phase 1 Exit "no NEW errors/failures vs. baseline" criterion and strictly better than the pre-change 43-bad-outcome baseline recorded in Section 8.1).
- Phase 2 (Runner wiring) — COMPLETE
  - `arch_controller_stop_hook.py:34,63,76` define `WAIT_STATE_FILE`, `WAIT_COMMAND = "wait"`, `WAIT_DISPLAY_NAME = "wait"`; `:171` defines `WAIT_STATE_SPEC`; `:234` registers `WAIT_STATE_SPEC` inside `CONTROLLER_STATE_SPECS`.
  - `arch_controller_stop_hook.py:1742` defines `_WAIT_FORBIDDEN_DELAY_POLL_FIELDS = (interval_seconds, check_prompt, attempt_count, last_check_at, last_summary)`; `:1751` `validate_wait_state` enforces `version == 1`, positive `armed_at`, `deadline_at > armed_at`, non-empty trimmed `resume_prompt`, and explicitly rejects each forbidden delay-poll-only field with `clear_state` + `block_with_message` (exit 2) — matching the Section 5.3 schema contract verbatim.
  - `arch_controller_stop_hook.py:3511` `handle_wait` is a one-shot: resolve via `resolve_controller_state_for_handler(payload, WAIT_STATE_SPEC)` → `validate_wait_state` → `sleep_for_seconds(max(0, deadline_at - current_epoch_seconds()))` → `clear_state(state_path)` → `block_with_json(...)` with the literal `resume_prompt`. No loop, no child run, no re-arm. State file is unlinked before continuation fires.
  - `arch_controller_stop_hook.py:3588` appends `handle_wait(payload)` to `main()` as the last dispatched handler, after `handle_code_review(payload)`; no earlier handler is reordered.
  - `tests/test_codex_stop_hook.py:1976` `WaitHandlerTests` covers pre-deadline sleep-then-fire, past-deadline immediate fire, wrong-session ignore, state-file-unlinked-before-`block_with_json`, bad version, deadline-not-after-armed-at, empty resume_prompt, and explicit rejection of each of the five forbidden delay-poll-only fields. `tests/test_codex_stop_hook.py:2200` `WaitConflictGateTests` proves `block_when_multiple_controller_states_armed` halts the turn with both state-file paths listed when `wait` coexists with another armed kind.
  - Minor benign drift outside this plan: an unrelated `arch-loop` feature appended `ARCH_LOOP_STATE_SPEC` to `CONTROLLER_STATE_SPECS` after `WAIT_STATE_SPEC` on this branch. `handle_wait` is still the last entry dispatched in `main()`, so the plan's "trailing dispatch position" obligation is preserved. This is not a wait-plan code gap.
- Phase 3 (Skill package `skills/wait/`) — COMPLETE
  - `skills/wait/SKILL.md` carries the `name: wait` frontmatter, describes when to use / when not to use / non-negotiables / first move / workflow / output expectations / reference map, and states the conflict-gate and single-slot semantics without fresh-child-run language.
  - `skills/wait/references/arm.md` documents the Section 5.3 state schema verbatim, the Phase 1 grammar (accept + reject tables), the runtime preflight (Codex + Claude Code variants, explicit omission of the Claude hook-suppressed child-run leg with justification), the 24h default cap with explicit-override carve-out, and every fail-loud condition.
  - `skills/wait/agents/openai.yaml` declares `interface.display_name`, `short_description`, a pure-delay `default_prompt` (no child run, no re-check), and `policy.allow_implicit_invocation: true`.
- Phase 4 (Install surface + live routing docs) — COMPLETE
  - `Makefile:4-6` includes `wait` in `SKILLS` and `CLAUDE_SKILLS` and deliberately omits it from `GEMINI_SKILLS` (matches the `delay-poll` precedent; Gemini has no native Stop hook).
  - `README.md:26` adds the `wait` inventory bullet with a one-liner distinguishing it from `delay-poll` (condition re-check) and `/loop` / `schedule` (recurring). `README.md:50` adds `wait` to the Codex feature-flag list. `README.md:65` priority-order paragraph describes the conflict-gate truth and ends the structural handler order `..., delay-poll, code-review, wait`. `README.md:90` and `:114` add the `~/.agents/skills/wait/` and `~/.claude/skills/wait/` install-paths lines (no `~/.gemini/skills/wait/`). `README.md:271` adds the dedicated `### wait` routing section. `README.md:321` primary-surface sentence names `wait`. `README.md:355` examples list includes the `Use $wait 1h30m then continue...` example.
  - `docs/arch_skill_usage_guide.md:26,46,72,97,121,154,363` all include `wait` per the Phase 4 Checklist; the Gemini installed-skills block at `:132` intentionally omits `wait`.
  - Worklog Pass 3 records `make install` clean, `make verify_install` → `OK: active skill surface installed...`, `ls ~/.agents/skills/wait/` and `ls ~/.claude/skills/wait/` both populated, and `ls ~/.gemini/skills/wait/` → "No such file or directory" (correct exclusion).
  - Full Python test suite post-Phase-4: `python3 -m unittest discover -s tests` → `Ran 83 tests in 0.745s, OK` (0 failures, 0 errors), re-verified in this audit pass.

## Remaining frontier (manual QA; non-blocking)
- Phase 5 (End-to-end manual smoke) — Manual QA pending. The full deliverable is real-session smoke against Codex and Claude Code plus coexistence and re-arm smokes, with timestamped evidence captured in `WORKLOG_PATH`. This is manual evidence by the skill's evidence-split rule and does not by itself block `Verdict (code): COMPLETE`. Required smokes (consolidated so the next operator can execute them as one frontier):
  - Codex short-wait smoke: `$wait 60s then say the wait fired` arms `.codex/wait-state.<SESSION_ID>.json` with the Section 5.3 schema; the installed Stop hook fires after ~60s; the literal resume prompt arrives once; the state file is unlinked.
  - Claude Code short-wait smoke: same flow against `.claude/arch_skill/wait-state(.<SESSION_ID>).json` (session-scoped or legacy-claim unsuffixed as applicable).
  - Conflict-gate smoke: arm `wait` in a session that already has another armed `arch_skill` controller; confirm the next turn halts with a `Multiple suite controller states are armed` message listing both state files and that neither handler dispatches. Clear the conflicting state and rerun to confirm single-armed dispatch still fires cleanly.
  - Re-arm smoke: arm `wait` twice in the same session before the first fire; confirm the second arm overwrites the first and only one resume fires.
  - Record per-arm evidence (arm timestamp, host, parsed duration, resume-prompt text, deadline, fire timestamp, state-file-after state) as a new Pass entry in `docs/GENERIC_WAIT_DELAY_THEN_EXECUTE_SKILL_2026-04-19_WORKLOG.md` before closing Phase 5.

## Notes on plan weakening (checked; none found)
- Phase 1 / Phase 2 Exit criteria were rewritten from "full suite green" to "no NEW errors/failures vs. documented baseline" (Pass 1 of the worklog) because the pre-existing test harness was out of sync with an unrelated uncommitted runner refactor (`_STATE_RELATIVE_PATH` → `_STATE_FILE`). That rewrite was scope-neutral: the shipped code in fact meets the original "full suite green" bar (current suite is 83/83 green with 0 bad outcomes), so the weakened criterion is not hiding unfinished work. Recorded and ratified by Decision Log 2026-04-19 "Test harness baseline drift".
- The "priority-dispatch coexistence" → conflict-gate repair (Pass 2) was a correction of a plan narrative that contradicted repo truth (`block_when_multiple_controller_states_armed` in `main()`). The conflict-gate contract is stricter than priority dispatch, not weaker, and the Phase 2 integration test was updated to prove the actual shipped behavior rather than a fiction. Recorded by Decision Log 2026-04-19 "One controller per session invariant reaffirmed".
- The Gemini exclusion repair (Pass 3) was a correction of a plan that originally required `GEMINI_SKILLS` inclusion; Gemini has no native Stop hook, so shipping `wait` there would have been dishonest. Scope correction, not weakening. Recorded by Decision Log 2026-04-19 "Gemini exclusion for `wait`".
- No requested behavior, acceptance criterion, or phase obligation was silently cut.
<!-- arch_skill:block:implementation_audit:end -->

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-04-19
phase_plan_pass_1: done 2026-04-19
recommended_flow: research -> deep dive -> phase plan -> implement
note: This block tracks stage order only. It never overrides readiness blockers caused by unresolved decisions.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

After this change ships, a user can invoke the new `wait` skill in Codex or Claude Code with a human duration and a literal follow-up prompt (e.g. `$wait 30m then continue phase 3 of DOC_PATH`). The current thread ends its turn. Approximately the requested duration later, the installed Stop hook wakes the same thread and runs the supplied prompt verbatim, with no intervening condition check. If the duration is unparseable, the runtime preflight fails, or another arch_skill controller is already armed, the skill refuses to arm and says so plainly.

## 0.2 In scope

- A new skill package at `skills/wait/` (slug resolved by deep-dive; see Decision Log 2026-04-19).
- Runner support in `skills/arch-step/scripts/arch_controller_stop_hook.py` for a new controller kind (`WAIT_STATE_SPEC` + `validate_wait_state` + `handle_wait`) owning pure delay-then-resume behavior.
- Duration grammar: `<N><unit>` with `s|m|h|d`, accepting singletons (`30m`, `1h`, `2d`, `90s`) and simple compositions (`1h30m`, `2h15m30s`). Resolved by deep-dive.
- Host-aware controller state paths consistent with `delay-poll`: `.codex/wait-state.<SESSION_ID>.json` and `.claude/arch_skill/wait-state(.<SESSION_ID>).json`.
- Install-surface updates: `Makefile` `SKILLS` and `CLAUDE_SKILLS` lists (not `GEMINI_SKILLS`, because Gemini has no Stop hook to back `wait` — this matches `delay-poll`'s precedent), `README.md` inventory + priority-order list, `docs/arch_skill_usage_guide.md` routing line.
- Runtime preflight modeled on `delay-poll`: active host runtime is Codex or Claude Code, repo-managed `Stop` entry pointing at the installed shared runner, that runner exists on disk, and in Codex `codex_hooks` is enabled. `wait` does not launch a fresh child during the wait, so the Claude hook-suppressed child-run preflight leg is not required and is intentionally omitted.
- Re-arming `wait` for the same session overwrites the prior `wait` state file (single-slot per session). The installed Stop hook's conflict gate (`block_when_multiple_controller_states_armed`) enforces one controller kind armed per session: if another arch_skill controller (e.g. `delay-poll`, `auto-plan`, `implement-loop`) is already armed, arming `wait` causes the next turn to halt with a conflict message listing both state files. `wait` is appended to the handler dispatch order as the last entry (structurally after `code-review`), which only matters for the single-kind case since the conflict gate blocks multi-kind dispatch entirely.

## 0.3 Out of scope

- Recurring schedules. Recurring work belongs to `/loop` or `schedule`.
- Condition-aware waiting. That remains `delay-poll`'s job.
- Background daemons, OS-level cron, or work that must survive host shutdown.
- Mutating the project while sleeping. The resume prompt owns all mutation after the wait.
- A wait primitive for non-hook runtimes. This skill is Codex + Claude Code only, same as `delay-poll`.
- Rich natural-language duration parsing (`half an hour`, `tomorrow at 3pm`). Locked grammar only.

## 0.4 Definition of done (acceptance evidence)

- Manual smoke: arm `$wait 90s then echo READY_AT $(date)` in Claude Code, end turn, observe the hook resume the thread after ~90s and run the literal prompt. Same smoke in Codex against its `Stop` hook entry.
- `npx skills check` passes for the new skill package.
- `make verify_install` passes after changes to install surface (if any).
- Unit-level parser check for durations (exact tests locked in phase plan).
- Coexistence check: the shared runner's `block_when_multiple_controller_states_armed` gate in `main()` is the enforcement point. With exactly one kind armed for a session, that kind (including `wait`) dispatches. With two or more kinds armed for the same session, the gate halts the turn with a conflict message and no handler dispatches — `wait` inherits that contract unchanged.
- Preflight failure check: with the repo-managed `Stop` entry missing, `$wait` refuses to arm and names the missing surface.

## 0.5 Key invariants (fix immediately if violated)

- `wait` is single-slot per session. Re-arming overwrites. Multiple different arch_skill controller kinds may coexist per session — the shared Stop hook owns priority dispatch; do not invent extra mutual-exclusion on top.
- No fallbacks or runtime shims. Missing preflight = refuse.
- Resume prompt is stored and fired literally; the skill never rewrites or summarizes it.
- No polling, no condition re-check, no silent re-arming after fire.
- No new parallel runner binary. The new controller kind lives inside the existing shared Stop-hook runner.
- State files, naming conventions, and preflight surface stay consistent with `delay-poll` so the suite has one shape, not two. `wait`'s preflight intentionally omits the Claude hook-suppressed child-run leg because `wait` never launches a fresh child.

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)

1. Correctness of the resume - the literal prompt must fire once, after approximately the requested delay, in the same session.
2. Fail-loud preflight and mutual exclusion.
3. Minimal surface: reuse the shared runner instead of forking a parallel controller.
4. Clear duration grammar that maps cleanly to a UTC deadline.
5. Install and docs coherence with the rest of the suite.

## 1.2 Constraints

- Must work in both Codex and Claude Code under the existing Stop-hook contract.
- Must not require new packages, new runtime dependencies, or new daemons.
- Session-scoped state only. No cross-session memory.

## 1.3 Architectural principles (rules we will enforce)

- Single owner for controller dispatch (the shared Stop-hook runner).
- State files use the same host-aware path scheme as `delay-poll`.
- No runtime shims for missing hooks, missing auth, or unparseable input.
- The new skill is explicitly not a scheduler; the doc and SKILL.md say so.

## 1.4 Known tradeoffs (explicit)

- Hook-backed wait means a long-running CLI process (the host's Stop-hook sleep loop) while waiting. Acceptable - same tradeoff `delay-poll` already makes.
- Grammar is intentionally narrow now; can be broadened later if users hit the wall.

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today

- `delay-poll`: wait-and-recheck-condition controller. Needs a `check_prompt` + poll interval + max window.
- `/loop` (dynamic) and `schedule` (cron-backed): recurring work, not one-shot delays.
- No public "pause exactly N, then do one thing" primitive in the suite.

## 2.2 What's broken / missing (concrete)

- Users who want pure delay either misuse `delay-poll` with a trivial always-false check, hand-roll `ScheduleWakeup` in prompts, or create a remote schedule for a one-shot job.
- There is no single source of truth for "wait N then resume in this thread," so different flows invent different shapes.

## 2.3 Constraints implied by the problem

- The primitive has to be native to the Codex/Claude Stop-hook world so it can resume the same thread.
- It has to be tiny and unambiguous or it becomes a drag on every flow that wants to compose with it.

# 3) Research Grounding (external + internal "ground truth")

<!-- arch_skill:block:research_grounding:start -->

## 3.1 External anchors (papers, systems, prior art)

- None adopted. This is internal plumbing that sits fully on top of the existing Codex/Claude Stop-hook surface. No third-party scheduler or timing library is relevant.

## 3.2 Internal ground truth (code as spec)

- Authoritative behavior anchors (do not reinvent):
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - single Python dispatcher for all arch_skill auto-controllers. Lines 24-46 define nine `..._STATE_SPEC` constants (one per controller kind: `IMPLEMENT_LOOP`, `AUTO_PLAN`, `MINIARCH_STEP_IMPLEMENT_LOOP`, `MINIARCH_STEP_AUTO_PLAN`, `ARCH_DOCS_AUTO`, `AUDIT_LOOP`, `COMMENT_LOOP`, `AUDIT_LOOP_SIM`, `DELAY_POLL`). Lines 176-186 define `CONTROLLER_STATE_SPECS` as the authoritative tuple registry. `main()` around lines 2522-2541 runs one handler per kind in sequence.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py:460-481` - `detect_active_controller_states()` + `stop_for_conflicting_controller_states()` enforce "one arch_skill controller per session" by scanning every registered spec. The new skill inherits this enforcement automatically by registering its spec.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py:1346-1458` - `validate_delay_poll_state()` is the closest existing schema: fields `version`, `armed_at` (UTC epoch), `deadline_at` (UTC epoch > armed_at), `check_prompt`, `resume_prompt`, `attempt_count`, `interval_seconds`, plus optional `last_check_at` / `last_summary`. The `deadline_at` + `resume_prompt` pair is exactly the primitive the new wait controller needs; the `check_prompt`, `interval_seconds`, and `attempt_count` fields are unused by a pure delay.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py:2402-2519` - `handle_delay_poll()` is the reference flow: sleep until `next_due_at` (capped by `deadline_at`), run one check, then decide ready/timeout/loop. A pure wait handler collapses to: sleep until `deadline_at`, then fire `resume_prompt` unconditionally.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py:2501-2510` - resume is fired via `block_with_json(reason)` with the literal `resume_prompt` prefixed to the reason. `block_with_json` emits `{"continue": True, "decision": "block", "reason": ...}`, which the host injects back into the same thread. This is the shared resume primitive; the new skill must use it verbatim.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py:289-293` - `current_epoch_seconds()` and `sleep_for_seconds()` are the UTC-time and sleep primitives. Reuse.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py:284-286` - `write_state()` is the shared JSON state-file writer (creates parent dirs). Reuse.
- Canonical path / owner to reuse:
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - the new controller kind must live here as a new spec constant + handler, not in a separate runner binary. The SKILL doctrine already forbids a dedicated `wait_controller.py` by analogy with `delay-poll`.
  - `skills/arch-step/scripts/upsert_claude_stop_hook.py` + `upsert_codex_stop_hook.py` + `Makefile` `install` target - install is already centralized on the shared runner; the new skill does not install its own hook.
- Adjacent surfaces tied to the same contract family:
  - `skills/delay-poll/` - the closest sibling in behavior and shape. Its `SKILL.md`, `references/arm.md`, and `references/check.md` define the preflight, state-file naming (`.codex/delay-poll-state.<SESSION_ID>.json` and `.claude/arch_skill/delay-poll-state(.<SESSION_ID>).json`), and 24h default max-window conventions that the new skill must mirror in name shape and fail-loud posture.
  - `skills/audit-loop/`, `skills/audit-loop-sim/`, `skills/comment-loop/` - other arm-and-end-turn skills. All arm distinct state files and dispatch through the same runner. Patterns to mirror but no shared code to reuse beyond `write_state`.
  - `skills/arch-step/SKILL.md` and `skills/miniarch-step/SKILL.md` - describe the `auto-plan` and `implement-loop` controllers that share the mutual-exclusion invariant. They are reads-only adjacent; the new skill does not change them.
  - `Makefile` (`install`, `install_skill`, `agents_install_skill`, `verify_install`) and `README.md` skill inventory - install surface and user-visible inventory that must be updated when the new skill ships.
- Compatibility posture (separate from `fallback_policy`):
  - `clean cutover (additive)` - this is a new skill and a new controller kind. No existing contract is being changed. The wait primitive does not replace or deprecate `delay-poll`; both ship side by side. The `CONTROLLER_STATE_SPECS` tuple is append-only, so adding a new kind is non-breaking for the other eight.
- Existing patterns to reuse:
  - `skills/arch-step/scripts/arch_controller_stop_hook.py:340-350` - session-id resolution (`current_session_id(payload)`) and session-suffixed path derivation (`session_state_relative_path()`). Reuse directly.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py:416-435, 544-587` - legacy unsuffixed → session-claim fallback (`resolve_active_controller_state`, `validate_session_id(..., allow_claim=True)`). Reuse for the new kind so parallel Claude sessions work the same way `delay-poll` does.
- Prompt surfaces / agent contract to reuse:
  - Not applicable. The runner's `block_with_json(reason)` already owns resume-prompt injection. No prompt-engineering work is needed; the skill's `SKILL.md` + `references/` files will be authored in prose and routed by the host.
- Native model or agent capabilities to lean on:
  - Codex + Claude Code Stop hook with session id in payload - already documented in the runner (`payload["session_id"]` at lines 340-344). The runner already handles both runtimes' quirks (session id availability, unsuffixed claim fallback).
- Existing grounding / tool / file exposure:
  - `tests/test_codex_stop_hook.py:144-151` - minimal integration harness that invokes the runner with a mocked Stop payload including `session_id`. Extendable as a preservation signal.
  - `make verify_install` - runs `verify_agents_install verify_codex_install verify_claude_install`, which check that the runner and Stop entries are actually installed.
- Duplicate or drifting paths relevant to this change:
  - None. No other skill implements a pure delay primitive. No shared "arm-and-end-turn" helper has been extracted across the eight controller skills; each duplicates the arm-time flow, but that is a broader refactor out of scope here.
- Capability-first opportunities before new tooling:
  - The new handler is ~20 lines: `deadline_at` field already exists in the state schema pattern, `sleep_for_seconds()` + `block_with_json()` already exist. No new harness, parser framework, or sidecar runtime is needed. Duration parsing is a single regex over `<N>(s|m|h|d)` with simple aggregation.
- Behavior-preservation signals already available:
  - `tests/test_codex_stop_hook.py` - covers dispatch scaffolding. Extending it with a wait-kind case would protect the new handler without inventing new machinery.
  - `make verify_install` - verifies install wiring survives.
  - Manual smoke with a short duration (e.g. `60s`) in each host is the definitive end-to-end proof.

## 3.3 Decision gaps that must be resolved before implementation

All three prior decision gaps are resolved by deep-dive against repo truth plus approved intent. See the 2026-04-19 Decision Log entries for rationale.

- Skill slug = `wait`. Resolved from approved intent in TL;DR + Section 0.1 ("the new `wait` skill") and the user's original ask.
- Duration grammar = singleton and composite `<N>(s|m|h|d)` (e.g. `30m`, `1h`, `2d`, `90s`, `1h30m`). Resolved from approved scope text in Section 0.2.
- New controller kind (not a mode flag on `delay-poll`). Resolved from the runner's existing shape — `CONTROLLER_STATE_SPECS` is a tuple of nine distinct kinds, each with its own spec + handler, and there is no mode-flag precedent.

No open gaps remain for the authoritative plan.
<!-- arch_skill:block:research_grounding:end -->

## 3.1 External anchors (papers, systems, prior art)

See block above.

## 3.2 Internal ground truth (code as spec)

See block above.

## 3.3 Decision gaps that must be resolved before implementation

See block above.

# 4) Current Architecture (as-is)

<!-- arch_skill:block:current_architecture:start -->
The relevant live surface is the shared Stop-hook runner plus its sibling arm-and-end-turn skills. `wait` will plug into this surface as one more controller kind, appended last to the existing dispatch list.
<!-- arch_skill:block:current_architecture:end -->

## 4.1 On-disk structure

- `skills/arch-step/scripts/arch_controller_stop_hook.py` — the one shared Python dispatcher for every arch_skill auto controller. 2500+ lines; owns state constants, state specs, validators, per-kind handlers, and the `main()` dispatch.
- `skills/arch-step/scripts/upsert_codex_stop_hook.py` and `skills/arch-step/scripts/upsert_claude_stop_hook.py` — install-time writers that put one repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime codex|claude` into `~/.codex/hooks.json` or `~/.claude/settings.json`. Verify mode is the same script with `--verify`.
- `Makefile` — declares `SKILLS`, `CLAUDE_SKILLS`, `GEMINI_SKILLS` lists and drives `install`, `install_skill`, `agents_install_skill`, `claude_install_skill`, `gemini_install_skill`, `verify_install` and friends. Install copies `skills/<slug>/` into `~/.agents/skills/<slug>/` and parallel Claude/Gemini targets.
- `README.md` — user-visible skill inventory plus the install + priority-order summary that names every active auto controller.
- `docs/arch_skill_usage_guide.md` — workflow selection doc; touches routing for the arch suite but does not currently mention `delay-poll` or any wait primitive.
- `skills/delay-poll/` — the closest sibling. Ships `SKILL.md`, `references/arm.md`, `references/check.md`, `agents/openai.yaml`. No runner code of its own; it declares behavior and defers to the shared runner.
- `skills/audit-loop/`, `skills/comment-loop/`, `skills/audit-loop-sim/`, `skills/arch-docs/`, `skills/miniarch-step/`, `skills/arch-step/` — the other arm-and-end-turn skill packages. Same shape: `SKILL.md` + `references/*.md` + `agents/openai.yaml`. None of them own a runner binary.
- `tests/test_codex_stop_hook.py` — integration-style tests that import the runner module and run per-handler harnesses (`run_delay_poll_handler`, `run_auto_plan_handler`, etc.) plus end-to-end stop-hook invocations. The file is the existing preservation signal for any runner change.
- Runtime state directories (per repo, host-aware):
  - Codex: `.codex/<controller>-state.<SESSION_ID>.json`
  - Claude Code: `.claude/arch_skill/<controller>-state(.<SESSION_ID>).json` (unsuffixed legacy path is claimed into a session-scoped path on the first Stop-hook turn).

## 4.2 Control paths (runtime)

Arm flow (parent pass):

1. User invokes a skill that runs an arm helper (`$delay-poll`, `$audit-loop auto`, `$miniarch-step auto-plan`, etc.).
2. The skill runs its runtime preflight — repo-managed `Stop` entry points at the installed shared runner, the runner file exists, and Codex has `codex_hooks` enabled (Claude additionally requires that hook-suppressed child runs via `claude -p --settings '{"disableAllHooks":true}'` work for controllers that need a fresh child pass).
3. The skill resolves the host-aware state path, writes the controller state JSON (kind-specific fields plus `version`, `command`, `session_id`), and tells the user to end the turn.

Stop-hook flow (per turn):

1. Host (Codex or Claude Code) reaches a stop point and invokes the installed runner with a JSON payload containing `cwd` and `session_id` (when available).
2. The runner runs `main()`. `main()` calls each `handle_X` in a fixed order:
   - `handle_miniarch_step_implement_loop`
   - `handle_implement_loop`
   - `handle_miniarch_step_auto_plan`
   - `handle_auto_plan`
   - `handle_arch_docs_auto`
   - `handle_audit_loop`
   - `handle_comment_loop`
   - `handle_audit_loop_sim`
   - `handle_delay_poll`
3. Each handler calls `resolve_controller_state_for_handler(payload, SPEC)`; if no matching state exists for this session, it returns `0` and the next handler runs.
4. When a handler finds its armed state, it does its work (sleep / fresh child run / etc.) and calls `block_with_json(reason)` (continue=True — inject the reason back into the session) or `stop_with_json(stop_reason)` (continue=False — stop the session with a message). Both functions `sys.exit`, so only one handler fires per turn. The remaining handlers never run that turn.
5. Same-session stacking semantics follow from that dispatch order: if two kinds are armed at once, the earlier-dispatched kind runs this turn and the later-dispatched kind waits until the earlier one clears its state.
6. Different-session state files (matched via `session_id`) are silently ignored by each handler.

Resume primitive:

- `block_with_json(reason)` emits `{"continue": true, "decision": "block", "reason": "<prompt + context>"}`. Both hosts inject `reason` back into the same thread as a literal continuation prompt. This is the one resume primitive; all controllers that continue use it.

## 4.3 Object model + key abstractions

- `HookRuntimeSpec(name, state_root)` — one per host runtime. `HOOK_RUNTIME_SPECS[RUNTIME_CODEX]` points at `.codex/`, `HOOK_RUNTIME_SPECS[RUNTIME_CLAUDE]` points at `.claude/arch_skill/`. `ACTIVE_RUNTIME` is set at `main()` entry from `--runtime` flag.
- `ControllerStateSpec(relative_path, expected_command, display_name)` — declarative record for one controller kind. Ships one per kind (`IMPLEMENT_LOOP_STATE_SPEC`, `AUTO_PLAN_STATE_SPEC`, …, `DELAY_POLL_STATE_SPEC`). The registry is `CONTROLLER_STATE_SPECS` — a module-level tuple that dispatch walks implicitly by calling each handler.
- `ResolvedControllerState(spec, state_path, is_legacy)` — the result of looking up a session-scoped or legacy unsuffixed state file on disk. Returned by `resolve_active_controller_state` / `resolve_controller_state_for_handler`.
- Shared primitives:
  - `current_session_id(payload)` — reads `payload["session_id"]`.
  - `session_state_relative_path(relative_path, session_id)` — appends `.<SESSION_ID>` before the `.json` suffix.
  - `session_state_path(cwd, spec, session_id)` — full host-aware path.
  - `write_state(path, state)` — JSON writer that creates parent dirs.
  - `load_state(path, name)` — JSON reader with fail-loud clearing on parse errors.
  - `validate_session_id(...)` — enforces session ownership with a `allow_claim` branch for unsuffixed legacy state.
  - `current_epoch_seconds()`, `sleep_for_seconds(n)` — time primitives.
  - `block_with_json(reason, system_message=None)`, `stop_with_json(stop_reason, system_message=None)` — the two exit primitives.
  - `clear_state(path)` — unlink helper used by every handler before it exits.
- `validate_delay_poll_state(payload, resolved_state)` — the closest reference validator. Returns `(state, state_path)` or `None`. Enforces `version == 1`, positive `interval_seconds`, `deadline_at > armed_at`, non-empty `check_prompt` and `resume_prompt`, non-negative `attempt_count`, and optional `last_check_at`, `last_summary`.
- `handle_delay_poll(payload)` — the closest reference handler. Runs a `while True:` loop: compute `next_due_at`, handle timeout, sleep, run a fresh host-native child check, update `attempt_count` / `last_check_at` / `last_summary`, and fire `block_with_json` on ready or `stop_with_json` on timeout/failure.

## 4.4 Observability + failure behavior today

- No structured telemetry. The observable surface is the host's Stop-hook stdout/stderr plus the state JSON on disk.
- Every validator fails loud via `block_with_message` (exit 2) when state is malformed — clears the state first.
- Every handler fails loud via `stop_with_json` on missing child-run tools, unparseable child output, or blown deadlines.
- Parent-pass skills that arm state are responsible for their own preflight failure messaging; the runner assumes install-surface truth.

## 4.5 UI surfaces (ASCII mockups, if UI work)

Not applicable (CLI skill).

# 5) Target Architecture (to-be)

<!-- arch_skill:block:target_architecture:start -->
`wait` ships as a new controller kind appended last to the existing shared runner's dispatch list. It owns its own spec, validator, handler, and one-shot sleep-then-resume semantics. The install surface and user-visible inventory pick it up additively with no changes to the pre-existing kinds or the hook contract.
<!-- arch_skill:block:target_architecture:end -->

## 5.1 On-disk structure (future)

- `skills/wait/SKILL.md` — new. Declares the `wait` skill and its non-negotiables. Routed identically to `delay-poll`: no dedicated runner binary, preflight must pass, arm-and-end-turn invocation.
- `skills/wait/references/arm.md` — new. Describes runtime preflight, state file schema, duration grammar, and arm rules.
- `skills/wait/agents/openai.yaml` — new. `default_prompt` mirrors `delay-poll`'s shape but swaps in pure-delay language and makes clear that no fresh child run happens during the wait.
- `skills/arch-step/scripts/arch_controller_stop_hook.py` — edited additively:
  - new constants `WAIT_STATE_FILE`, `WAIT_COMMAND = "wait"`, `WAIT_DISPLAY_NAME = "wait"`
  - new `WAIT_STATE_SPEC` appended to `CONTROLLER_STATE_SPECS`
  - new `parse_wait_duration(text) -> int` helper (seconds)
  - new `validate_wait_state(payload, resolved_state)` validator
  - new `handle_wait(payload)` handler
  - `main()` gains a trailing `handle_wait(payload)` call
- `Makefile` — `SKILLS` and `CLAUDE_SKILLS` lists each gain `wait`. `GEMINI_SKILLS` does not, because Gemini has no native Stop hook to back `wait` (same reason `delay-poll` is excluded from `GEMINI_SKILLS`). No other Makefile change needed; install paths are macro-driven.
- `README.md` — skill inventory + install summary + priority-order list each gain `wait`. The priority-order list names the dispatch order including `wait` last.
- `docs/arch_skill_usage_guide.md` — add one routing line for `wait` and a contrast line distinguishing it from `delay-poll` and `/loop` / `schedule`.
- `tests/test_codex_stop_hook.py` — add `parse_wait_duration` unit tests and `handle_wait` integration tests covering: already-past-deadline immediate fire, before-deadline sleep then fire, wrong-session ignore, malformed state fail-loud, and coexistence with one other armed controller.
- Runtime state path (arm time and hook time):
  - Codex: `.codex/wait-state.<SESSION_ID>.json`
  - Claude Code: `.claude/arch_skill/wait-state.<SESSION_ID>.json` when session id is available before the first Stop-hook turn; otherwise `.claude/arch_skill/wait-state.json` and let the first Stop-hook turn claim session ownership (same legacy-claim branch delay-poll uses).

## 5.2 Control paths (future)

Arm flow (parent pass running the `wait` skill):

1. Parse the user invocation into `duration_seconds` (via `parse_wait_duration`) and `resume_prompt` (literal text after `then`).
2. Run the runtime preflight identical to `delay-poll`'s, minus the Claude hook-suppressed child-run check — `wait` never launches a fresh child, so that preflight leg is unnecessary. Preflight checks the active host runtime, the repo-managed `Stop` entry, the installed runner path, and `codex_hooks` in Codex.
3. If preflight fails or duration is unparseable or out of range (≤0, > 24h when no explicit override), refuse to arm and name the failure.
4. Compute `armed_at = current_epoch_seconds()`, `deadline_at = armed_at + duration_seconds`.
5. Resolve the host-aware state path. Write the state JSON using `write_state`.
6. Tell the user plainly to end the turn and let the installed Stop hook own the wait.

Stop-hook flow:

1. `main()` calls `handle_wait(payload)` as the last dispatched handler (after `handle_delay_poll`).
2. `handle_wait` calls `resolve_controller_state_for_handler(payload, WAIT_STATE_SPEC)`. If no matching state for this session, returns 0.
3. `validate_wait_state(payload, resolved_state)` enforces the schema (see 5.3). Invalid state clears itself and fails loud.
4. Compute `remaining = max(0, deadline_at - current_epoch_seconds())`. If `remaining > 0`, call `sleep_for_seconds(remaining)`.
5. After the sleep, call `clear_state(state_path)` and `block_with_json(reason)` where `reason` is built from the literal `resume_prompt` plus a short suffix such as `The requested wait elapsed (<N>s).`.
6. No retry, no re-check, no re-arm. One fire, then state is cleared.

Coexistence with other controllers:

- Only one arch_skill controller kind may be armed per session at a time. The shared runner runs `block_when_multiple_controller_states_armed` before any handler dispatch; if it finds two or more armed state files for this session, it halts with a conflict message and the session must clear the stale state manually. `wait` inherits that contract — arming `wait` while another kind is armed for the same session will produce the same conflict halt, not priority-order dispatch.
- Within a single turn where `wait` is the only armed kind, `main()`'s handler call order places `handle_wait(payload)` after `handle_code_review(payload)`. That trailing position is a structural guarantee so later additions don't reorder earlier handlers; it is not a priority race, since the conflict gate already guarantees at most one kind is armed.
- Re-arming `wait` for the same session overwrites the existing `wait` state file (`write_state` is a plain overwrite). No stacking of multiple `wait` instances per session; the primitive is single-slot.

## 5.3 Object model + abstractions (future)

- `WAIT_STATE_FILE = Path("wait-state.json")`
- `WAIT_COMMAND = "wait"`
- `WAIT_DISPLAY_NAME = "wait"`
- `WAIT_STATE_SPEC = ControllerStateSpec(relative_path=WAIT_STATE_FILE, expected_command=WAIT_COMMAND, display_name=WAIT_DISPLAY_NAME)`
- `CONTROLLER_STATE_SPECS` is extended to include `WAIT_STATE_SPEC` appended last, preserving the existing relative order of all prior entries.
- State schema (JSON):
  ```json
  {
    "version": 1,
    "command": "wait",
    "session_id": "<SESSION_ID>",
    "armed_at": <int epoch seconds>,
    "deadline_at": <int epoch seconds, > armed_at>,
    "resume_prompt": "<literal continuation prompt>"
  }
  ```
  - No `interval_seconds`, no `check_prompt`, no `attempt_count`, no `last_check_at`, no `last_summary`. These `delay-poll` fields are irrelevant for a pure delay and must not be copied.
- `parse_wait_duration(text: str) -> int` — pure function. Accepts `<N><unit>` components concatenated, where unit is one of `s|m|h|d` and `N` is a positive integer. Examples that must parse:
  - `90s` → 90
  - `30m` → 1800
  - `1h` → 3600
  - `2d` → 172800
  - `1h30m` → 5400
  - `2h15m30s` → 8130
  Strings that must fail-loud (raise `ValueError` with a specific message):
  - empty string
  - leading/trailing whitespace not stripped by caller (caller is responsible for strip; parser rejects embedded spaces)
  - unknown units (`1w`, `1y`, `1ms`)
  - zero or negative component (`0m`, `-1h`)
  - natural-language forms (`half an hour`, `30 minutes`)
  - duplicate units (`1h2h`)
  - components out of descending order are accepted (the parser sums components; it does not enforce order).
- `validate_wait_state(payload, resolved_state) -> tuple[dict, Path] | None` — structural twin of `validate_delay_poll_state`:
  - reuses `load_controller_state`, `validate_session_id`
  - enforces `version == 1`
  - enforces `armed_at: int > 0`
  - enforces `deadline_at: int > armed_at`
  - enforces non-empty trimmed `resume_prompt: str`
  - rejects any of the `delay-poll`-only fields if present (`interval_seconds`, `check_prompt`, `attempt_count`, `last_check_at`, `last_summary`) — fail-loud and clear state. This keeps the schemas from drifting.
- `handle_wait(payload)` — structural simplification of `handle_delay_poll`:
  - resolves state via `resolve_controller_state_for_handler(payload, WAIT_STATE_SPEC)`
  - validates via `validate_wait_state`
  - sleeps the remaining window via `sleep_for_seconds(max(0, deadline_at - current_epoch_seconds()))`
  - clears state and fires `block_with_json(f"{resume_prompt} The requested wait elapsed. Former wait state: {state_path_value}.", system_message="wait elapsed; continuing the task.")`
  - no retry, no child run, no loop

## 5.4 Invariants and boundaries

- Single source of truth for controller dispatch: the shared runner. No dedicated `wait_controller.py`.
- Single source of truth for controller state schemas: the per-kind validator. `validate_wait_state` owns the `wait` schema; it must reject `delay-poll`-only fields.
- Single resume primitive: `block_with_json`. `wait` never invents its own continuation protocol.
- Fail-loud boundaries:
  - Unparseable duration → parent skill refuses to arm.
  - Missing runtime preflight → parent skill refuses to arm.
  - Malformed state at hook time → validator clears state and exits 2.
  - Session-id mismatch → legacy-claim branch if unsuffixed, otherwise clear state and exit.
- No polling, no re-check, no re-arm after fire. Mutation belongs to the resumed main thread after the deadline.
- Default maximum wait window is 24 hours. Inherit the `delay-poll` cap for consistency; users may explicitly raise it at arm time.
- Conflict-gate coexistence: the shared runner's `block_when_multiple_controller_states_armed` gate runs before any handler and halts the turn when ≥2 controller state files are armed for the same session. `wait` inherits that contract. Appending `handle_wait(payload)` after `handle_code_review(payload)` in `main()` preserves every earlier handler's relative dispatch order but is not a priority race — the gate ensures at most one kind dispatches per turn.
- No fallbacks or runtime shims. `fallback_policy: forbidden` is preserved.
- Instruction-bearing surfaces (`SKILL.md`, `references/arm.md`, `agents/openai.yaml`) stay consistent with `delay-poll`'s shape — same preflight language, same hook-backed non-negotiables, different pure-delay semantics.

## 5.5 UI surfaces (ASCII mockups, if UI work)

Not applicable.

# 6) Call-Site Audit (exhaustive change inventory)

<!-- arch_skill:block:call_site_audit:start -->

## Change map (table)

| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
|------|------|--------------------|------------------|-----------------|-----|--------------------|----------------|
| Skill package | `skills/wait/SKILL.md` | n/a (new file) | Does not exist | Create canonical `SKILL.md` with frontmatter (`name: wait`, short description, metadata), "When to use / When not to use / Non-negotiables / First move / Workflow / Output expectations / Reference map" sections mirroring `delay-poll`'s shape but for pure delay | Defines the public skill surface and its non-negotiables; required for `npx skills check` and install | Public skill `wait` | `npx skills check` |
| Skill package | `skills/wait/references/arm.md` | n/a (new file) | Does not exist | Create; covers runtime preflight (without the Claude hook-suppressed child-run leg), state file contract (schema), duration grammar, arm rules, 24h cap, fail-loud conditions | The SKILL.md routes to this reference; runner behavior must match it | — | — |
| Skill package | `skills/wait/agents/openai.yaml` | n/a (new file) | Does not exist | Create with `interface.display_name`, `short_description`, `default_prompt` tuned to pure delay + one-shot resume; `policy.allow_implicit_invocation: true` | Agent routing file; required for consistency with the other shipped skills | — | — |
| Runner constants | `skills/arch-step/scripts/arch_controller_stop_hook.py:24-56` | New constants near the existing `*_STATE_FILE`, `*_COMMAND`, `*_DISPLAY_NAME` block | Nine controller kinds only | Add `WAIT_STATE_FILE = Path("wait-state.json")`, `WAIT_COMMAND = "wait"`, `WAIT_DISPLAY_NAME = "wait"` | Required for the spec + validator + handler to reference stable identifiers | New constants | `tests/test_codex_stop_hook.py` imports module |
| Runner spec | `skills/arch-step/scripts/arch_controller_stop_hook.py:92-195` | New `WAIT_STATE_SPEC` + extend `CONTROLLER_STATE_SPECS` | Existing specs registered (the current live kinds) | Append `WAIT_STATE_SPEC = ControllerStateSpec(...)` and add it to `CONTROLLER_STATE_SPECS` as its new last entry, preserving the relative order of every pre-existing spec | Required so `resolve_controller_state_for_handler` can find wait state for this session | `CONTROLLER_STATE_SPECS` grows by one (wait is appended last) | Existing share-session / session-isolation tests still pass; new tests reference `WAIT_STATE_SPEC` |
| Runner parser | `skills/arch-step/scripts/arch_controller_stop_hook.py` (new function) | `parse_wait_duration(text: str) -> int` | No duration parser exists anywhere in the runner | Add pure function: regex `^([0-9]+[smhd])+$` with per-unit multipliers, sum components, reject zero/negative/unknown/duplicates/whitespace | Required at arm time to translate user input into `deadline_at` | New function | New unit tests in `tests/test_codex_stop_hook.py` |
| Runner validator | `skills/arch-step/scripts/arch_controller_stop_hook.py:1307-1419` region (new function added nearby) | `validate_wait_state(payload, resolved_state)` | `validate_delay_poll_state` is the closest analogue | Add validator that enforces `version == 1`, positive `armed_at`, `deadline_at > armed_at`, non-empty `resume_prompt`, rejects `delay-poll`-only fields | Required so malformed wait state fails loud the same way other kinds do | New validator | New validator tests |
| Runner handler | `skills/arch-step/scripts/arch_controller_stop_hook.py:2363-2481` region (new function added nearby) | `handle_wait(payload)` | `handle_delay_poll` is the closest analogue | Add one-shot sleep-then-fire handler (no loop, no child run); on elapsed deadline, clear state and `block_with_json(resume_prompt + " The requested wait elapsed. Former wait state: ...")` | The real runtime behavior the skill promises | New handler | New handler tests |
| Runner dispatch | `skills/arch-step/scripts/arch_controller_stop_hook.py` (current `main()` body) | `main()` | Dispatches the existing handler list whose current last entry is `handle_code_review(payload)` | Append `handle_wait(payload)` as the new last entry (after `handle_code_review(payload)`) | Required so the hook actually runs the new handler; trailing position preserves every earlier handler's relative order | Dispatch order grows by one | Existing dispatch tests still pass |
| Install surface | `Makefile:4-6` | `SKILLS`, `CLAUDE_SKILLS`, `GEMINI_SKILLS` | Three parallel lists of shipped skill slugs | Add `wait` to `SKILLS` and `CLAUDE_SKILLS` only; `GEMINI_SKILLS` is intentionally skipped because Gemini has no native Stop hook (mirrors `delay-poll`'s exclusion) | Required so `make install` and `make claude_install_skill` actually copy the skill; `verify_install` picks it up on the supported surfaces | — | `make verify_install` |
| User-visible inventory | `README.md` (skill inventory bullet list) | "Other shipped skills are:" section | Lists `delay-poll` and siblings | Add a `wait` bullet right next to `delay-poll` with a one-line description distinguishing it from `delay-poll` and `/loop` | Keeps the inventory honest | — | — |
| Priority-order list | `README.md` install section (the paragraph describing the conflict-gate truth and structural handler order) | Conflict-gate paragraph | Names the structural handler order ending with `code-review` | Repair the paragraph to describe the conflict gate accurately and end the structural order with `..., delay-poll, code-review, wait` | Keeps the README reflection of `main()` dispatch and the conflict-gate contract accurate | — | — |
| Routing doc | `docs/arch_skill_usage_guide.md` | Wherever delay-poll / loop / schedule routing lives (or a new short line if absent) | May not currently mention delay-poll by name | Add one routing line for `wait` distinguishing it from `delay-poll` (condition re-check) and `/loop` / `schedule` (recurring) | Keeps live routing doc in sync with shipped behavior | — | — |
| Tests | `tests/test_codex_stop_hook.py` | New test class or test methods on existing classes | Covers dispatch, session scoping, and each existing handler | Add: `parse_wait_duration` parser cases (accept + reject); `handle_wait` pre-deadline sleep + fire; `handle_wait` past-deadline immediate fire; wrong-session ignore; malformed-state fail-loud; coexistence with one other armed controller (dispatch order preserved) | Preservation + forward signal for the new handler | New tests extending `stop_module` harness | Run via `python3 -m unittest tests.test_codex_stop_hook` |

Rows may reference non-code surfaces when they participate in the same contract family or migration boundary.

## Migration notes

- **Canonical owner path / shared code path:** `skills/arch-step/scripts/arch_controller_stop_hook.py` owns all controller dispatch. `wait` gets one new kind inside this single runner; no new runner binary.
- **Deprecated APIs:** None. No existing API is being changed or deprecated.
- **Delete list:** None. This is a clean additive cutover.
- **Adjacent surfaces tied to the same contract family:**
  - `skills/delay-poll/` — sibling skill. `delay-poll` behavior and files are unchanged. The two skills ship side by side.
  - `skills/audit-loop/`, `skills/comment-loop/`, `skills/audit-loop-sim/` — other arm-and-end-turn skills. No change. `wait` inherits their per-turn dispatch semantics implicitly by registering its own spec.
  - `skills/miniarch-step/`, `skills/arch-step/`, `skills/arch-docs/` — other controller kinds. No change. `wait` is independent of their plans.
- **Compatibility posture / cutover plan:** Clean additive cutover. `CONTROLLER_STATE_SPECS` is an append-only tuple; `main()` dispatch is an append-only call list; state file names are new and do not collide with any existing kind. No breaking changes, no timeboxed bridge required.
- **Capability-replacing harnesses to delete or justify:** None. `wait` is not agent-backed behavior; it is pure plumbing. No prompt engineering or native-capability work applies.
- **Live docs/comments/instructions to update or delete:**
  - `README.md` skill inventory + priority-order list: update to include `wait`.
  - `docs/arch_skill_usage_guide.md`: add one routing line.
  - No stale truth left behind; every touched live doc gets synced to shipped reality in the same phase.
- **Behavior-preservation signals for refactors:**
  - Existing `tests/test_codex_stop_hook.py` tests for `handle_delay_poll`, `handle_auto_plan`, dispatch ordering, and session scoping must continue to pass.
  - `make verify_install` must continue to pass.
  - Manual smoke in Codex and Claude Code for a short wait (e.g. `60s`) is the definitive end-to-end proof for the new handler.

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)

| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude/blocker question) |
| ---- | ------------- | ---------------- | ---------------------- | ------------------------------------- |
| Runner | `arch_controller_stop_hook.py` state-spec + validator + handler triad | Append-only registration inside `CONTROLLER_STATE_SPECS` plus dispatch in `main()` | `wait` follows the existing kinds exactly; no new pattern is introduced | include (baseline; no consolidation work beyond matching the existing triad) |
| Runner | Shared arm-time helper (hypothetical — does not exist) | Extract a common "arm and end turn" helper used by all arm-and-end-turn skills | Each of the nine existing skills reimplements preflight + state writing; that duplication already exists and is not blocking | defer (out of scope for this skill; broader refactor across all arm-and-end-turn skills) |
| Skill docs | `delay-poll` preflight language in `SKILL.md` + `references/arm.md` | Shared preflight boilerplate referenced from each skill | `wait` will repeat most of `delay-poll`'s preflight language with one leg dropped (Claude hook-suppressed child auth), and every arm-and-end-turn skill today duplicates similar language | defer (broader authoring cleanup; copy `delay-poll`'s working language into `wait` for v1 and leave generalization to a later pass) |
| README | Priority-order sentence + skill inventory | Mechanically generated from `CONTROLLER_STATE_SPECS` | Today the README priority order is hand-maintained; divergence is a real drift risk | defer (scope creep beyond shipping `wait`; flag as follow-up) |
<!-- arch_skill:block:call_site_audit:end -->

# 7) Depth-First Phased Implementation Plan (authoritative)

<!-- arch_skill:block:phase_plan:start -->

> Rule: systematic build, foundational first; split Section 7 into the best sequence of coherent self-contained units, optimizing for phases that are fully understood, credibly testable, compliance-complete, and safe to build on later. If two decompositions are both valid, bias toward more phases than fewer. `Work` explains the unit and is explanatory only for modern docs. `Checklist (must all be done)` is the authoritative must-do list inside the phase. `Exit criteria (all required)` names the exhaustive concrete done conditions the audit must validate. Resolve adjacent-surface dispositions and compatibility posture before writing the checklist. Before a phase is valid, run an obligation sweep and move every required promise from architecture, call-site audit, migration notes, delete lists, verification commitments, docs/comments propagation, approved bridges, and required helper follow-through into `Checklist` or `Exit criteria`. Refactors, consolidations, and shared-path extractions must preserve existing behavior with credible evidence proportional to the risk. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly (delete superseded paths). If a bridge is explicitly approved, timebox it and include removal work; otherwise plan either clean cutover or preservation work directly. Prefer programmatic checks per phase; defer manual/UI verification to finalization. Avoid negative-value tests and heuristic gates (deletion checks, visual constants, doc-driven gates, keyword or absence gates, repo-shape policing). Also: document new patterns/gotchas in code comments at the canonical boundary (high leverage, not comment spam).

## Phase 1 — Duration parser (`parse_wait_duration`)

* Goal: Ship a pure, deterministic parser that converts the user-facing duration grammar into integer seconds, with fail-loud rejection of every unsupported form. This is the most foundational unit: the validator, handler, and arm flow all depend on its contract.
* Work: Add `parse_wait_duration(text: str) -> int` to `skills/arch-step/scripts/arch_controller_stop_hook.py` near the other module-level helpers. Implement as a single anchored regex (`^([0-9]+[smhd])+$`) plus per-component summation against the multiplier table `{s:1, m:60, h:3600, d:86400}`. No natural-language handling. No whitespace tolerance. Zero/negative per-component values raise. Duplicate units raise. Unknown units raise.
* Checklist (must all be done):
  - `parse_wait_duration` is defined at module scope in `arch_controller_stop_hook.py`.
  - Accepts `90s`, `30m`, `1h`, `2d`, `1h30m`, `2h15m30s` and returns exactly `90`, `1800`, `3600`, `172800`, `5400`, `8130`.
  - Rejects with `ValueError` (specific message per case): empty string, embedded whitespace, unknown units (`1w`, `1y`, `1ms`), zero/negative components (`0m`, `-1h`), duplicate units (`1h2h`), natural language (`half an hour`, `30 minutes`).
  - Component order is not enforced (parser sums all matches; `30s1h` is accepted).
  - Unit tests covering every accept case and every reject case above are added to `tests/test_codex_stop_hook.py` and named so the audit can confirm coverage.
* Verification (required proof): `python3 -m unittest tests.test_codex_stop_hook -k parse_wait_duration` passes locally and the audit can re-run it.
* Docs/comments (propagation; only if needed): No live doc touches required here; the grammar is documented by Phase 3's `references/arm.md`.
* Exit criteria (all required):
  - New `parse_wait_duration` function lives in `arch_controller_stop_hook.py` and is importable by tests.
  - Every accept/reject case in the Checklist has a named unit test and all pass.
  - No NEW test errors or failures are introduced in `tests/test_codex_stop_hook.py` relative to the documented pre-change baseline (see Section 8.1 and Decision Log 2026-04-19 "Test harness baseline drift").
* Rollback: Remove the new function plus its unit tests. Nothing else is wired to it yet, so rollback is local.

## Phase 2 — Runner wiring (spec, validator, handler, dispatch)

* Goal: Register the `wait` controller kind inside the shared Stop-hook runner — constants, spec, validator, handler, and `main()` dispatch — so a written state file actually drives a real sleep-then-resume. Foundational for Phase 3's skill package to have something real to arm.
* Work: Add `WAIT_STATE_FILE`, `WAIT_COMMAND`, `WAIT_DISPLAY_NAME`, `WAIT_STATE_SPEC`. Append `WAIT_STATE_SPEC` to `CONTROLLER_STATE_SPECS` as the tenth entry. Add `validate_wait_state(payload, resolved_state)` modeled on `validate_delay_poll_state`: `version == 1`, positive integer `armed_at`, `deadline_at > armed_at`, non-empty trimmed `resume_prompt`, explicit rejection of `delay-poll`-only fields (`interval_seconds`, `check_prompt`, `attempt_count`, `last_check_at`, `last_summary`). Add `handle_wait(payload)` modeled on `handle_delay_poll` but as a one-shot: resolve state, validate, compute `remaining = max(0, deadline_at - current_epoch_seconds())`, `sleep_for_seconds(remaining)` if >0, `clear_state(state_path)`, then `block_with_json(f"{resume_prompt} The requested wait elapsed. Former wait state: {state_path}.", system_message="wait elapsed; continuing the task.")`. Append `handle_wait(payload)` as the last call in `main()` after `handle_delay_poll(payload)`.
* Checklist (must all be done):
  - `WAIT_STATE_FILE = Path("wait-state.json")`, `WAIT_COMMAND = "wait"`, `WAIT_DISPLAY_NAME = "wait"` are defined alongside existing `*_STATE_FILE` / `*_COMMAND` / `*_DISPLAY_NAME` blocks.
  - `WAIT_STATE_SPEC` is constructed from those constants and appended to `CONTROLLER_STATE_SPECS` as its new last entry, preserving the relative order of every pre-existing spec. No earlier entry is reordered or renamed.
  - `validate_wait_state` is added and enforces every field rule listed in Section 5.3, including the explicit rejection of the five `delay-poll`-only fields (`interval_seconds`, `check_prompt`, `attempt_count`, `last_check_at`, `last_summary`) with clear-state-then-exit-2 semantics.
  - `handle_wait` is added and implements exactly the one-shot sleep-then-fire behavior from Section 5.2 steps 1-6. No loop. No child run. No re-arm. State is cleared before `block_with_json`.
  - `main()`'s dispatch call list is extended with `handle_wait(payload)` as the last handler (after `handle_code_review(payload)`, which is currently the last dispatched handler); no earlier handler call is reordered.
  - Integration tests in `tests/test_codex_stop_hook.py` cover: pre-deadline sleep-then-fire; past-deadline immediate fire; wrong-session ignore; malformed-state (each of the five forbidden delay-poll-only fields — `interval_seconds`, `check_prompt`, `attempt_count`, `last_check_at`, `last_summary` — present) fail-loud; conflict-gate coexistence (arming `wait` alongside one other armed controller kind for the same session makes `block_when_multiple_controller_states_armed` halt the turn with a conflict message and neither handler dispatches); state file is unlinked before `block_with_json`.
  - Behavior-preservation check: no NEW test errors or failures are introduced in `tests/test_codex_stop_hook.py` relative to the documented pre-change baseline (see Section 8.1 and Decision Log 2026-04-19 "Test harness baseline drift"). The new wait-specific tests must pass. Pre-existing baseline failures caused by the uncommitted `_STATE_RELATIVE_PATH` → `_STATE_FILE` rename drift are tracked separately and are not in this plan's scope.
* Verification (required proof): `python3 -m unittest tests.test_codex_stop_hook` shows the new wait-specific tests green and the error/failure count no higher than the documented baseline (Section 8.1).
* Docs/comments (propagation; only if needed): None in this phase. Live docs (`README.md`, `docs/arch_skill_usage_guide.md`) are synced in Phase 4. The SKILL package is added in Phase 3.
* Exit criteria (all required):
  - All Checklist items above are present in code.
  - Writing a valid `wait-state.<SESSION_ID>.json` and invoking the runner with a matching `session_id` payload causes a real sleep then a `{"continue": true, "decision": "block", ...}` JSON on stdout with the resume prompt embedded.
  - `CONTROLLER_STATE_SPECS` grows by exactly one (`WAIT_STATE_SPEC` appended last); no other entries reordered, renamed, or removed.
  - New wait-specific tests all pass. Total `tests/test_codex_stop_hook.py` error/failure count does not rise above the documented baseline (Section 8.1).
  - No existing test was deleted or weakened to accommodate the new code.
* Rollback: Remove the new symbols (three constants, one spec, one dispatch call, validator, handler, registry append, plus the new tests). The runner returns to its pre-change shape. `tests/test_codex_stop_hook.py` returns to its pre-change state.

## Phase 3 — Skill package (`skills/wait/`)

* Goal: Ship the public skill surface that arms the Phase 2 runner contract: `SKILL.md`, `references/arm.md`, and `agents/openai.yaml`. After this phase, `$wait <duration> then <prompt>` is a real routable skill whose arm path produces exactly the state Phase 2 validates.
* Work: Create `skills/wait/SKILL.md` mirroring `skills/delay-poll/SKILL.md`'s shape (frontmatter with `name: wait`, "When to use / When not to use / Non-negotiables / First move / Workflow / Output expectations / Reference map" sections) but with pure-delay semantics and no fresh-child-run language. Create `skills/wait/references/arm.md` documenting: preflight (same as delay-poll's minus the Claude hook-suppressed child-run leg), the state schema from Section 5.3, the grammar from Phase 1, the 24h cap, the single-slot per-session behavior, and every fail-loud condition. Create `skills/wait/agents/openai.yaml` with `interface.display_name`, `short_description`, `default_prompt`, and `policy.allow_implicit_invocation: true`, echoing `delay-poll`'s structure but swapping in pure-delay language and stating explicitly that no fresh child run happens during the wait.
* Checklist (must all be done):
  - `skills/wait/SKILL.md` exists, passes `npx skills check`, and routes to `references/arm.md`.
  - `skills/wait/references/arm.md` specifies every preflight leg required by Section 5.2 step 2 (active host runtime, repo-managed Stop entry, installed runner path, `codex_hooks` in Codex). It explicitly omits the Claude hook-suppressed child-run leg and explains why (no fresh child run).
  - `references/arm.md` documents the Section 5.3 state schema verbatim (version, command, session_id, armed_at, deadline_at, resume_prompt) and explicitly states that no delay-poll-only fields may appear.
  - `references/arm.md` documents the Phase 1 grammar (accept/reject cases) and the 24h default cap with the "user may explicitly raise it at arm time" carve-out from Section 5.4.
  - `skills/wait/agents/openai.yaml` declares the skill to the agent router with the same structural shape as `skills/delay-poll/agents/openai.yaml` but pure-delay wording.
  - `npx skills check` passes for the full `skills/` surface.
* Verification (required proof): `npx skills check` exits zero, and a hand inspection confirms the three new files exist at the expected paths with the required sections named above.
* Docs/comments (propagation; only if needed): None beyond the new skill files themselves. The README and usage guide are synced in Phase 4.
* Exit criteria (all required):
  - Three new files under `skills/wait/` exist and together make the skill loadable.
  - `npx skills check` passes.
  - A reader of `skills/wait/SKILL.md` + `references/arm.md` can follow the arm flow end to end without needing to cross-reference `delay-poll`.
* Rollback: Delete `skills/wait/` and re-run `npx skills check`. Phase 2 runner wiring is unaffected (it remains dormant until state is armed).

## Phase 4 — Install surface + live routing docs

* Goal: Make `wait` installable via `make install` and `make claude_install_skill` (not `make gemini_install_skill`, because Gemini has no native Stop hook — mirrors `delay-poll`'s exclusion), and sync every live reference doc so the shipped inventory, conflict-gate truth, and routing guidance match reality. This is the phase that exposes `wait` to real users.
* Work: In `Makefile`, append `wait` to `SKILLS` and `CLAUDE_SKILLS` only; do not add it to `GEMINI_SKILLS`. In `README.md`, add a `wait` entry to the skill inventory next to `delay-poll` with a one-line description distinguishing it from `delay-poll` (condition re-check) and `/loop` / `schedule` (recurring); add `wait` to the primary-surface sentence near the Usage heading; add a short `### wait` routing section next to `### delay-poll`; update the install-paths listings to cover `~/.agents/skills/wait/` and `~/.claude/skills/wait/` (and explicitly not `~/.gemini/skills/wait/`); repair the priority-order paragraph to describe the conflict-gate truth and end its structural handler order in `..., delay-poll, code-review, wait`. In `docs/arch_skill_usage_guide.md`, add `wait` to the shipped-skill inventory, the Codex feature list, the install-paths list, the Codex and Claude Code installed-skills blocks (but not the Gemini block), the install notes paragraph, and add one dedicated `### wait` routing section with a contrast line versus `delay-poll` and `/loop` / `schedule`.
* Checklist (must all be done):
  - `Makefile`'s `SKILLS` and `CLAUDE_SKILLS` macros both contain `wait`; `GEMINI_SKILLS` does not (matching `delay-poll`).
  - `make verify_install` passes against a fresh install target and confirms `skills/wait/` was copied into `~/.agents/skills/wait/` and `~/.claude/skills/wait/` (and not into `~/.gemini/skills/wait/`).
  - `README.md` skill inventory names `wait` with a distinguishing one-liner, and the Usage primary-surface sentence names `wait`.
  - `README.md` priority-order paragraph describes the conflict-gate truth (`block_when_multiple_controller_states_armed` halts the next turn when ≥2 kinds are armed) and ends its structural handler order in `..., delay-poll, code-review, wait` (exactly last, matching `main()` dispatch order).
  - `docs/arch_skill_usage_guide.md` has a dedicated `### wait` routing section, a contrast line versus `delay-poll` and `/loop` / `schedule`, and includes `wait` in every shipped-skill inventory location except the Gemini-installed block and the Gemini install-paths entry.
  - No earlier install list entry was renamed, deleted, or reordered.
* Verification (required proof): `make verify_install` exits zero. After `make install`, `ls ~/.agents/skills/wait/ ~/.claude/skills/wait/` both show a populated skill directory, and `ls ~/.gemini/skills/wait/` fails with "No such file or directory". The full python test suite stays green (`python3 -m unittest discover -s tests` — currently 83/83 after Phase 4 edits).
* Docs/comments (propagation; only if needed): Covered above. No other live doc references the shipped skill inventory at runtime; if one is discovered during execution, it must be synced in this phase rather than deferred.
* Exit criteria (all required):
  - `make install` and `make claude_install_skill` both copy `skills/wait/` to their expected targets; `make gemini_install_skill` does not, and that absence is verified.
  - `make verify_install` passes.
  - Every live doc that lists the shipped skill surface mentions `wait` everywhere it would be dishonest to omit it, and the README priority-order paragraph reflects both the conflict-gate truth and Phase 2's structural dispatch position (last).
* Rollback: Remove `wait` from `SKILLS` and `CLAUDE_SKILLS` in the Makefile and revert the README + usage-guide edits. Runner wiring (Phase 2) and skill package (Phase 3) can remain in place dormantly; only the install surface is reverted.

## Phase 5 — End-to-end manual smoke

Status: IN PROGRESS
Manual QA (non-blocking): pending — Codex short-wait smoke, Claude Code short-wait smoke, conflict-gate smoke, and re-arm smoke all still owed against real fresh sessions. Phases 1-4 are code-complete (see `arch_skill:block:implementation_audit`); the code side of Phase 5 has no remaining work, so this status does not reopen the phase.

* Goal: Prove the full arm → end turn → sleep → real hook-driven resume path works in both host runtimes against a real installed environment. This is the authoritative end-to-end signal for a primitive whose shipped behavior is "a real session wake."
* Work: Install the updated skill set via `make install` (Codex) and `make claude_install_skill` (Claude Code). In each host, invoke `$wait 60s then <literal prompt>`, observe the state file on disk at the expected host-aware path, end the turn, wait for the Stop hook to fire, and confirm the literal resume prompt is injected exactly once and the state file is cleared.
* Checklist (must all be done):
  - Codex smoke: `$wait 60s then say the wait fired` arms `.codex/wait-state.<SESSION_ID>.json` with the exact schema from Section 5.3, the Stop hook fires after ~60s, the resume prompt arrives once, and the state file is unlinked after firing.
  - Claude Code smoke: `$wait 60s then say the wait fired` arms the appropriate `.claude/arch_skill/wait-state...json`, the Stop hook fires after ~60s, the resume prompt arrives once, and the state file is unlinked.
  - Coexistence (conflict-gate) smoke: arm `wait` in a session that already has one other controller kind (e.g. `delay-poll`) active; confirm `block_when_multiple_controller_states_armed` halts the turn with a conflict message listing both state-file paths and that neither handler dispatches. Clear the conflicting state file and rerun to confirm the single-armed case still fires cleanly.
  - Re-arm smoke: arm `wait` twice in the same session before the first fire; confirm the second arm overwrites the first and only one resume fires.
  - Evidence (timestamps, host, duration, resume prompt text, state-file-after state) is captured in `WORKLOG_PATH` per arm.
* Verification (required proof): Worklog entries demonstrate each smoke case above with observable signals (arm timestamp, deadline, fire timestamp, prompt text injected, state file unlinked). Manual execution is acceptable here because the signal is a real session wake that cannot be synthesized without the host runtime.
* Docs/comments (propagation; only if needed): None; all live docs were synced in Phase 4.
* Exit criteria (all required):
  - Codex short-wait smoke passes with evidence in `WORKLOG_PATH`.
  - Claude Code short-wait smoke passes with evidence in `WORKLOG_PATH`.
  - Coexistence and re-arm smokes pass with evidence in `WORKLOG_PATH`.
  - No smoke case surfaced a contract divergence from Sections 5.2 / 5.3; if it did, the plan is reopened rather than papered over.
* Rollback: The smoke is read-only against production code. If a smoke case fails, reopen the relevant earlier phase and fix there; do not patch around the failure in this phase.
<!-- arch_skill:block:phase_plan:end -->

# 8) Verification Strategy (common-sense; non-blocking)

## 8.1 Unit tests (contracts)

- Duration parser round-trip tests (locked during phase-plan).
- Pre-change `tests/test_codex_stop_hook.py` baseline on 2026-04-19 (with the uncommitted runner refactor in place but without any wait-specific edits): `Ran 44 tests, failures=29, errors=14` — 43 bad outcomes. Root cause was an uncommitted `_STATE_RELATIVE_PATH` → `_STATE_FILE` rename plus `HookRuntimeSpec` runtime-initialization contract change in the shared runner that had not been propagated to the test harness.
- Minimum-scope harness repair performed during Phase 1 of this plan: `tests/test_codex_stop_hook.py` now initializes `ACTIVE_RUNTIME = HOOK_RUNTIME_SPECS[RUNTIME_CODEX]` in `CodexStopHookTests.setUpClass`, and `run_stop_hook` passes `--runtime codex` to the hook subprocess. Those two surgical edits were the minimum required for the existing `CodexStopHookTests` assertions to run at all against the post-refactor runner; the plan treats that as in-scope harness sync. After those edits and the Phase 2–4 work, post-change `python3 -m unittest discover -s tests` runs 83 tests with 0 failures and 0 errors (44 pre-existing CodexStopHookTests green, 19 new `WaitDurationParserTests` green, 13 new `WaitHandlerTests` / `WaitConflictGateTests` green, 7 unrelated prompt-contract tests green).
- Exit-criteria restatement: the wait work must keep the full-suite error+failure count at or below the recorded 43-bad-outcome ceiling while ensuring all new wait-specific tests pass. Current truth: 0 bad outcomes, 32 new wait-specific tests passing — well under the ceiling. Broader harness cleanup beyond the two surgical edits (e.g. any remaining doc-anchor drift in unrelated assertions, if discovered) remains a separate follow-up tracked in the Decision Log entry "Test harness baseline drift".

## 8.2 Integration tests (flows)

- Shared Stop-hook runner dispatch test for the new controller kind (locked during phase-plan).

## 8.3 E2E / device tests (realistic)

- Manual smoke in both Codex and Claude Code: short-duration arm, observe real hook-driven resume. Manual is acceptable here because the signal is a real session wake.

# 9) Rollout / Ops / Telemetry

## 9.1 Rollout plan

- Ship as a new skill. No migration of existing users. `delay-poll` stays exactly as-is.

## 9.2 Telemetry changes

- None beyond whatever the shared Stop-hook runner already logs.

## 9.3 Operational runbook

- TBD in phase-plan; at minimum: how to cancel an armed wait (delete the state file) and how to diagnose "the hook didn't fire."

# 10) Decision Log (append-only)

## 2026-04-19 - Plan created

Context: User asked for a generic pause-then-execute skill distinct from `delay-poll`.
Options: (a) new dedicated skill, (b) generalize `delay-poll` with a no-op check mode.
Decision: (a) new skill, pending North Star confirmation. Keeps `delay-poll`'s semantics clean and matches the mental model users describe.
Consequences: Small duplication in the shared runner for state-file reading; offset by clearer public surface.
Follow-ups: Research and deep-dive must still evaluate whether the new controller kind should reuse `delay-poll`'s state file shape or define its own.

## 2026-04-19 - Skill slug = `wait`

Context: Section 3.3 carried the slug choice as an open decision gap (`wait` / `wait-then` / `delay`).
Options: (a) `wait`, (b) `wait-then`, (c) `delay`, (d) other.
Decision: `wait`. TL;DR and Section 0.1 already said "the new `wait` skill" and the user's original ask used the word `wait`. No repo collision.
Consequences: Public surface is `$wait <duration> then <prompt>`. Skill package lives at `skills/wait/`. Install lists add `wait`.
Follow-ups: None.

## 2026-04-19 - Duration grammar = `<N>(s|m|h|d)` singleton + composite

Context: Section 3.3 carried the grammar scope as an open decision gap.
Options: (a) singleton only, (b) singleton + composite (`1h30m`), (c) natural language.
Decision: (b). Accept singletons (`30m`, `1h`, `2d`, `90s`) and composites (`1h30m`, `2h15m30s`). One regex plus per-component summation. Natural language is explicitly out of scope.
Consequences: Parser is small and deterministic. Covers everything the user described in the original ask.
Follow-ups: None.

## 2026-04-19 - New controller kind, not a `delay-poll` mode flag

Context: Section 3.3 carried the integration choice as an open decision gap.
Options: (a) new `WAIT_STATE_SPEC` + `handle_wait` in the shared runner, (b) mode flag on `delay-poll` state.
Decision: (a). Runner evidence: `CONTROLLER_STATE_SPECS` is a tuple of nine distinct kinds, each with its own spec + validator + handler, and there is no mode-flag precedent. Keeping `delay-poll`'s semantics clean, keeping `wait`'s semantics clean, and matching the established shape all point the same way.
Consequences: Tenth `ControllerStateSpec` registered, new validator + handler, trailing `handle_wait` call in `main()`. `delay-poll` is untouched.
Follow-ups: None.

## 2026-04-19 - Test harness baseline drift (tracked as separate follow-up)

Context: During Phase 1 execution of implement-loop, running `python3 -m unittest tests.test_codex_stop_hook` on the pre-change working tree returned `44 tests, failures=11, errors=40`. Root cause: `skills/arch-step/scripts/arch_controller_stop_hook.py` was refactored from `*_STATE_RELATIVE_PATH = Path(".codex/<name>.json")` constants to `*_STATE_FILE = Path("<name>.json")` constants backed by a `HookRuntimeSpec` state-root, but the test file `tests/test_codex_stop_hook.py` still references `*_STATE_RELATIVE_PATH` symbols and expects the old `~/.codex/hooks.json` anchor text in several SKILL/reference docs. That drift predates the wait work and is present on the `arch-native-auto-loops` branch head.
Options: (a) expand this plan to include a full harness-sync phase that renames every `_STATE_RELATIVE_PATH` reference and updates the doc-anchor expectations, (b) scope the plan to not regress the baseline and track the harness sync as a separate effort, (c) stop and refuse to ship anything until the harness is fixed.
Decision: (b). Repairing the harness is a large, unrelated edit surface (40+ call sites plus several doc-contract anchor expectations) that would delay shipping the `wait` primitive without serving its North Star. The wait work must not raise the baseline error/failure count; wait-specific tests must pass; pre-existing baseline failures remain as-is and are tracked for separate work.
Consequences: Phase 1 and Phase 2 Exit criteria now measure "no new failures relative to the recorded baseline" instead of "full suite green." Section 8.1 records the baseline number so the audit can verify it.
Follow-ups: Open a separate task to sync `tests/test_codex_stop_hook.py` with the current runner constants and to refresh the hook-contract doc-anchor expectations. Do not couple that repair to wait.

## 2026-04-19 - Gemini exclusion for `wait` (implementation pass correction)

Context: Section 0.2, Section 6 file map, Section 6 change-map row, and Phase 4 all originally said "add `wait` to `SKILLS`, `CLAUDE_SKILLS`, and `GEMINI_SKILLS`" and "`make install`, `make claude_install_skill`, and `make gemini_install_skill` all copy `skills/wait/`." Phase 4 implementation read repo truth and found that `wait` cannot function on Gemini because Gemini has no native Stop hook — the same reason `delay-poll` is excluded from `GEMINI_SKILLS` (line 6 of `Makefile`) and the same reason the README and usage guide already call out that exclusion explicitly for hook-backed controllers. Including `wait` in `GEMINI_SKILLS` would ship a skill that cannot work on that surface.
Options: (a) add `wait` to `GEMINI_SKILLS` as the plan originally said and ship a non-functional Gemini install, (b) mirror `delay-poll`'s precedent and install `wait` only on `SKILLS` (agents/Codex) and `CLAUDE_SKILLS` (Claude Code), and document the exclusion in every live doc.
Decision: (b). `wait` is Stop-hook-backed, Gemini has no Stop hook, and the precedent is already set by `delay-poll`. Installing a hook-backed skill on a surface with no hook would be dishonest and would immediately fail runtime preflight.
Consequences: Section 0.2 install-surface summary, Section 6 file map, Section 6 change-map "Install surface" row, and Phase 4 Goal / Work / Checklist / Exit criteria / Rollback are all retargeted to `SKILLS` + `CLAUDE_SKILLS` only. `README.md` and `docs/arch_skill_usage_guide.md` document the exclusion explicitly in the Gemini-surface and install-notes paragraphs. The Phase 4 verification step adds a positive check that `~/.gemini/skills/wait/` does NOT exist after `make install`.
Follow-ups: None.

## 2026-04-19 - "One controller per session" invariant reaffirmed (implementation pass correction)

Context: A mid-plan decision entry previously claimed multiple arch_skill controller kinds could coexist per session on the strength of `main()`'s "priority-dispatch" order. Phase 2 implementation read repo truth and found this is wrong: the shared runner's `main()` calls `block_when_multiple_controller_states_armed(payload)` before any handler dispatch, and that gate calls `stop_with_json(...)` when it finds two or more armed state files for the session. So multi-kind arming for a single session is actually a fail-loud conflict, not a priority race.
Options: (a) leave the plan's priority-dispatch claim and write a wait-specific test for behavior that does not exist, (b) repair the plan narrative (Section 0, Section 5.2, Section 5.4, Phase 2 checklist, Phase 5 smoke) to describe the existing conflict gate and the `wait`-inherits-it contract.
Decision: (b). Making the plan say what the code actually does costs nothing and prevents writing a fiction-validating test. `wait` inherits the existing conflict gate. Within a turn where `wait` is the only armed kind, it is still dispatched last by call-order (structural guarantee, not priority race), but that ordering is irrelevant when the gate already guarantees at most one kind is armed.
Consequences: Section 0.4 "Coexistence check" wording, Section 5.2 "Coexistence with other controllers" block, Section 5.4 "Priority-dispatch coexistence" bullet, Phase 2 Checklist integration-test enumeration, and Phase 5 smoke coexistence step are all retargeted to describe the conflict-gate contract. The Phase 2 integration test for coexistence becomes "arm `wait` + one other kind for the same session; `block_when_multiple_controller_states_armed` halts with a conflict message; neither handler dispatches," not "earlier-registered kind dispatches first."
Follow-ups: None for this skill. A suite-wide audit of other plans that reference "priority-dispatch coexistence" as if the model were cooperative is logged as a separate `arch-docs` follow-up.
