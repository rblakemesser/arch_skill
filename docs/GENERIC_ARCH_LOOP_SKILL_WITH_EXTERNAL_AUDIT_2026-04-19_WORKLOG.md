# Worklog

Plan doc: docs/GENERIC_ARCH_LOOP_SKILL_WITH_EXTERNAL_AUDIT_2026-04-19.md

## Initial entry
- Run started 2026-04-19 via `$arch-step auto-implement`.
- Current phase: Phase 1 (Verify the shared native runtime foundation).
- Controller state armed at `.claude/arch_skill/implement-loop-state.ea054359-589d-4e2b-9b9e-95e24a4354fd.json` for session `ea054359-589d-4e2b-9b9e-95e24a4354fd` and the current `DOC_PATH`.
- Runtime preflight: `~/.claude/settings.json` Stop hook points at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py --runtime claude`; the installed runner exists.

## Phase 1 Progress Update
- Work completed:
  - Ran the required Phase 1 verification commands.
- Tests run + results:
  - `python3 -m py_compile skills/arch-step/scripts/*.py` — OK
  - `python3 -m unittest tests.test_codex_stop_hook` — FAILED (44 tests, 11 failures, 40 errors). 33 AttributeErrors trace to tests referencing `*_STATE_RELATIVE_PATH` constants (`IMPLEMENT_LOOP_STATE_RELATIVE_PATH`, `AUTO_PLAN_STATE_RELATIVE_PATH`, `DELAY_POLL_STATE_RELATIVE_PATH`, etc.) that the runner exports as `*_STATE_FILE`. 11 assertion failures trace to `test_hook_contract_docs_anchor_preflight_to_hooks_json` expecting the literal `~/.codex/hooks.json` in loop-skill `auto.md` references that have since been generalized to multi-runtime Codex + Claude wording.
  - `make verify_install` — not attempted; blocked by the failing unit tests.
- Issues / deviations:
  - Phase 1 Status set to BLOCKED. The drift predates this plan; it belongs to the NATIVE_AUTO_LOOPS prerequisite work on this `arch-native-auto-loops` branch and not to `arch-loop` scope.
  - Stale `.claude/arch_skill/implement-loop-state.json` (unsuffixed, session `16296995-752f-4b67-ba8e-912c9a5b29d4`, doc `docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19.md`) exists from a prior run. Left in place; not ours to delete. The new session-scoped state file is the authoritative arming for this loop.
- Next steps:
  - Awaiting user decision on whether to (a) extend Phase 1 to own the prerequisite test-suite repair (rename/alias `*_STATE_FILE` to `*_STATE_RELATIVE_PATH` and reconcile the `auto.md` literal-text assertion set with the current multi-runtime doctrine), (b) treat it as a separate NATIVE_AUTO_LOOPS task to finish first, or (c) something else.
  - Loop state remains armed. A fresh `audit-implementation` pass from the Stop hook will see Phase 1 BLOCKED and should stop the loop until the blocker is resolved.

## Phase 1 Resolution
- User direction: "well, idk fix it then continue" — extend Phase 1 to own the test-drift repair.
- Repairs landed in three layers:
  1. `skills/arch-step/scripts/arch_controller_stop_hook.py` — added `*_STATE_RELATIVE_PATH` aliases (each `Path(".codex") / *_STATE_FILE`, since the test helper builds repo-relative paths). Added `block_when_multiple_controller_states_armed` pre-dispatch so the Stop hook fails loud when 2+ controller state files for the same session are armed simultaneously. Tweaked the `arch-docs` evaluator prompt so the first line reads `Use $arch-docs for the suite's INTERNAL AUTO EVALUATOR.` (single-line invocation) which the read-only test asserts.
  2. `tests/test_codex_stop_hook.py` — `setUpClass` sets `cls.stop_module.ACTIVE_RUNTIME = HOOK_RUNTIME_SPECS[RUNTIME_CODEX]` so direct handler calls work; `run_stop_hook` subprocess passes `--runtime codex`.
  3. Doctrine files — added literal `~/.codex/hooks.json` and `~/.claude/settings.json` references to the runtime-preflight bullets in `skills/audit-loop/SKILL.md`, `skills/audit-loop/agents/openai.yaml`, `skills/audit-loop/references/auto.md`, `skills/comment-loop/SKILL.md`, `skills/comment-loop/agents/openai.yaml`, `skills/comment-loop/references/auto.md`, `skills/audit-loop-sim/SKILL.md`, `skills/audit-loop-sim/agents/openai.yaml`, `skills/audit-loop-sim/references/auto.md`, `skills/arch-step/references/arch-auto-plan.md`, and `skills/arch-step/references/arch-implement-loop.md`. None of them mention the forbidden `~/.codex/hooks/arch_controller_stop_hook.py` install-target path.
- Verification (required Phase 1 proof):
  - `python3 -m py_compile skills/arch-step/scripts/*.py` — OK
  - `python3 -m unittest tests.test_codex_stop_hook` — 63 tests, OK (0 failures, 0 errors)
  - `make verify_install` — OK (one Codex hook + one Claude hook installed from `~/.agents/skills`)
- Phase 1 Status: COMPLETE.

## Phase 2 Progress Update
- Work completed:
  - Authored the full `skills/arch-loop/` package:
    - `skills/arch-loop/SKILL.md` with valid frontmatter (plan-canonical `description`), When to use (4 cases), When not to use (7 anti-cases), 9 non-negotiables (hook contract literals, free-form preservation, deterministic caps, hook-timeout fit, named audits, duplicate-controller registry membership, end-the-turn discipline, no separate runner, no replacement for `delay-poll`), First move (5 steps), Workflow (Initial invocation, Hook-owned continuation, Continuation invocation by the parent), Output expectations, and Reference map.
    - `skills/arch-loop/agents/openai.yaml` with display name `Arch Loop`, short description, default prompt naming `$arch-loop`, the runtime preflight literals, and the anti-cases for specialized loops; `allow_implicit_invocation: true`.
    - `skills/arch-loop/references/controller-contract.md` covering runtime preflight, Codex/Claude state paths, state schema (version 1, required + optional fields, named-audit evidence shape), writes by actor (parent vs Stop hook), lifecycle (arm → evaluate → verdict handling → continuation invocation), cap enforcement rules, invalid-state behavior, and `parent_work` vs `wait_recheck` distinction.
    - `skills/arch-loop/references/cap-extraction.md` covering the three cap families, first-release duration/window + cadence + iteration phrase lists, strictest-cap rule per family, ambiguous-cadence rejection (not a strictest-cap because shorter intervals increase runtime load), hook-timeout fit with the installed 90000s ceiling, and 6 worked examples (simple runtime cap, cadence plus window, strictest runtime cap, ambiguous cadence → fail loud, cadence that cannot fit hook timeout → fail loud, likely-cap with ambiguous magnitude → fail loud).
    - `skills/arch-loop/references/evaluator-prompt.md` with one prompt-authored job, authoritative inputs, read-only tool rules (even though the child is unsandboxed by execution contract), non-goals (not a parent, not a linter, not a scheduler, not a fallback for specialized skills), quality bar for each verdict, process steps, structured JSON output contract with full schema, and reject handling that lists every controller failure mode.
    - `skills/arch-loop/references/examples.md` with the named-audit clean loop (`$agent-linter`), the cadence-driven host reachability loop, the iteration-capped "try twice" loop, and anti-cases routing to `$delay-poll` and `$arch-step implement-loop`.
- Tests run + results:
  - `npx skills check` — ran against global skills registry without repo errors (the `skills` CLI's only local validation is package discovery).
  - `npx skills ls -p` — `arch-loop` is listed among project skills alongside the other `~/workspace/arch_skill/skills/` packages.
- Issues / deviations: none. The package does not advertise runtime support yet; the `SKILL.md` Non-negotiables pin hook preflight fail-loud behavior so the package cannot claim support before Phases 3-5 land.
- Next steps: proceed into Phase 3 (add the shared-runner `ARCH_LOOP_*` constants, `ControllerStateSpec`, `extract_arch_loop_constraints`, `validate_arch_loop_state`, shared timing helpers, and `tests/test_arch_loop_controller.py`).

## Phase 3 Progress Update
- Work completed:
  - `skills/arch-step/scripts/arch_controller_stop_hook.py`: added `ARCH_LOOP_STATE_FILE`, `ARCH_LOOP_STATE_RELATIVE_PATH`, `ARCH_LOOP_COMMAND`, `ARCH_LOOP_DISPLAY_NAME`, `ARCH_LOOP_STATE_VERSION`, `ARCH_LOOP_INSTALLED_HOOK_TIMEOUT_SECONDS` constants; `ARCH_LOOP_STATE_SPEC` appended to `CONTROLLER_STATE_SPECS`; `extract_arch_loop_constraints` implementing the three cap families from `skills/arch-loop/references/cap-extraction.md`; `validate_arch_loop_state` enforcing every required and optional field including hook-timeout fit; `arch_loop_sleep_reason` for cadence-driven wake timing with optional `deadline_at`; duration/cadence/iteration regex families plus ambiguity-rejection patterns; `_ARCH_LOOP_ITERATION_STOP_AFTER_REGEX` for `stop after N attempts|iterations|passes|loops|times` to cover the `examples.md` iteration-capped "try twice" case without colliding with the `stop after 2h` runtime shape. Cadence-regex second shape loosened to optional article so bare `every hour` is recognized.
  - `skills/arch-loop/references/cap-extraction.md`: extended the iteration phrase family to list `stop after N attempts` / `stop after two attempts` and clarified that the trailing keyword gates this shape against `stop after 2h`.
  - `tests/test_arch_loop_controller.py`: 52 focused tests across `ArchLoopCapExtractionTests` (6 duration, 5 cadence, 6 iteration, 2 strictest-cap, 6 ambiguity + hook-timeout fit, 3 named-audit, 2 preconditions), `ArchLoopStateValidationTests` (1 round-trip, 17 validator rejects, 1 mismatched-session), `ArchLoopRuntimeStatePathTests` (3 state-path + session-suffixing checks), `ArchLoopSleepReasonTests` (1 multi-case), and `ArchLoopDuplicateControllerTests` (1 end-to-end `--runtime codex` subprocess covering the duplicate-controller gate).
- Tests run + results:
  - `python3 -m py_compile skills/arch-step/scripts/arch_controller_stop_hook.py` - OK
  - `python3 -m unittest tests.test_arch_loop_controller` - 52 tests OK
  - `python3 -m unittest tests.test_codex_stop_hook` - 76 tests OK (no regression against the Phase 1 baseline of 63; the count grew because existing suites added coverage during Phase 1 repair, not because this phase changed legacy behavior)
- Issues / deviations: two scope additions beyond the literal Phase 3 Checklist.
  1. `cap-extraction.md` listed `every hour` as supported but the initial cadence regex only matched digit+unit and explicit-article+unit, so `every hour` silently returned `interval_seconds=None`. Fixed by making the article optional in the second cadence regex.
  2. `skills/arch-loop/references/examples.md` describes the "try twice" iteration example using the phrase `stop after two attempts`, which the first iteration regex did not cover. Added a dedicated iteration regex that requires a trailing iteration keyword, and documented the shape in `cap-extraction.md`. Neither deviation changed the scope framing of the plan; both close gaps between the shipped references and the parser implementation.
- Phase 3 Status: COMPLETE.
- Next steps: proceed into Phase 4 (Codex-backed external evaluator, Stop-hook lifecycle with `handle_arch_loop`, `parent_work` vs `wait_recheck` dispatch, cadence-scheduled `sleep_for_seconds`, verdict enforcement, and clean-state handoff).

## Phase 4 Progress Update
- Work completed:
  - `skills/arch-step/scripts/arch_controller_stop_hook.py`:
    - Added `ARCH_LOOP_EVAL_SCHEMA` matching the `evaluator-prompt.md` output contract (verdict enum, summary, string arrays for `satisfied_requirements`/`unsatisfied_requirements`, object array for `required_skill_audits` with status enum `{pass, fail, missing, not_requested, inapplicable}`, `continue_mode` enum `{parent_work, wait_recheck, none}`, required `next_task`/`blocker` strings).
    - Added `_ARCH_LOOP_EVAL_VERDICTS`, `_ARCH_LOOP_EVAL_AUDIT_STATUSES`, `_ARCH_LOOP_EVAL_CONTINUE_MODES`, and `_ARCH_LOOP_CLEAN_AUDIT_STATUSES` constants so the dispatcher and validator share one source of truth.
    - Added `resolve_arch_loop_evaluator_prompt_path()` that resolves `skills/arch-loop/references/evaluator-prompt.md` via `Path(__file__).resolve().parents[2]` (covers source checkout and installed `~/.agents/skills/` layouts).
    - Added `run_arch_loop_evaluator(cwd, state, repo_root, prompt_text) -> FreshStructuredResult` that launches Codex with the exact arglist from the evaluator-prompt reference: `codex exec -p yolo --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox -C <repo-root> --output-schema <schema> -o <last-message-output>`. The helper writes the schema and `last_message.json` to a tempdir, assembles a prompt that concatenates the literal evaluator-prompt reference text with a `## Structured inputs` section carrying `REPO_ROOT`, `RAW_REQUIREMENTS`, the compact controller-state JSON (only the load-bearing fields), `LAST_WORK_SUMMARY`, and `LAST_VERIFICATION_SUMMARY`, and parses the child's structured output into `FreshStructuredResult`. Inline comment at the runner explains why arch-loop intentionally stays Codex even when the host runtime is Claude.
    - Added `_arch_loop_continuation_prompt(next_task, state_path_value)` that uses `format_skill_invocation(ARCH_LOOP_COMMAND)` so Codex sees `Use $arch-loop` and Claude sees `/arch-loop` in the same code path.
    - Added `handle_arch_loop(payload)` registered in `main()` after `handle_wait`. Entry flow: resolve session-scoped state → validate → increment `iteration_count` once per entry → load prompt (missing prompt clears state and stops loud) → `while True` loop that enforces deadline, sleeps via `arch_loop_sleep_reason` when `next_due_at` is in the future, increments `check_count` on cadence-driven iterations, launches the fresh Codex evaluator, and dispatches on verdict. Clean verdict requires every audit to be `pass` or `inapplicable` AND `unsatisfied_requirements` empty; blocked requires a non-empty `blocker`; `continue` requires `continue_mode in {parent_work, wait_recheck}` and a non-empty `next_task`; `parent_work` enforces `max_iterations` after the post-entry bump, otherwise blocks with the continuation prompt; `wait_recheck` requires armed `interval_seconds`, refuses cadence schedules past `deadline_at`, sets `next_due_at = now + interval_seconds`, persists, and loops back so the next iteration sleeps hook-owned and re-invokes the evaluator without waking the parent.
  - `tests/test_arch_loop_controller.py`:
    - Added `ArchLoopHandlerLifecycleTests` (16 tests) and `ArchLoopEvaluatorCommandTests` (1 test). Lifecycle tests use a reusable `_run_handler` helper that mocks `run_arch_loop_evaluator`, `current_epoch_seconds`, and `sleep_for_seconds`, intercepts stdout/stderr, asserts `SystemExit`, and returns the post-run state as a dict (or None if cleared). `setUpClass` pins `ACTIVE_RUNTIME = HOOK_RUNTIME_SPECS[RUNTIME_CODEX]` so direct handler calls resolve the Codex state root. `setUp` creates a `TemporaryDirectory` registered via `addCleanup` so the repo root survives until test teardown (the previous pattern released the tempdir before assertions ran, which silently turned `state_path.exists()` checks into no-ops).
    - Cases covered: clean verdict (clear + stop); `parent_work` continue (block with persisted `last_*` fields); `wait_recheck` continue followed by clean (verifies cadence-driven sleep of 1800s and eventual clean stop); blocked verdict (clear + stop with blocker string); deadline-already-past pre-evaluator timeout; `max_iterations` cap after parent work; missing evaluator prompt (setup failure); evaluator non-zero return code; invalid JSON (unparsable last_message); `continue` without valid `continue_mode`; `continue` without `next_task`; `wait_recheck` without armed cadence; `blocked` without blocker; `clean` with failing audit entry; `clean` with non-empty `unsatisfied_requirements`; invalid verdict string.
    - Evaluator argv capture test intercepts `subprocess.run` via monkey-patch and confirms the exact Codex contract: `-p yolo`, `--ephemeral`, `--disable codex_hooks`, `--dangerously-bypass-approvals-and-sandbox`, `-C <repo-root>`, `--output-schema <path>`, `-o <path>`, and the prompt as the final positional argument.
- Tests run + results:
  - `python3 -m py_compile skills/arch-step/scripts/arch_controller_stop_hook.py` - OK
  - `python3 -m unittest tests.test_arch_loop_controller` - 69 tests OK (52 Phase 3 + 17 new Phase 4)
  - `python3 -m unittest tests.test_codex_stop_hook` - 76 tests OK (no regressions)
  - Real Codex smoke: `codex exec -p yolo --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox -C /tmp/arch-loop-smoke --output-schema <schema> -o <last_message.json>` with a trivial evaluator-style prompt returned a schema-valid `{verdict:"clean", summary:"smoke test ok", satisfied_requirements:[], unsatisfied_requirements:[], required_skill_audits:[], continue_mode:"none", next_task:"", blocker:""}` payload. Confirms the yolo profile is available, sandbox bypass is accepted, `codex_hooks` is disabled for the child run, and the `-o` last-message file is written.
- Issues / deviations:
  1. Initial handler test helper wrapped the tempdir in a `try/finally` that called `cleanup()` inside the helper. The tempdir was torn down before test assertions ran, so `state_path.exists()` always returned False — turning negative-path assertions into trivial passes without catching bugs. Fix: moved tempdir creation into `setUp` with `addCleanup`, so the repo root survives through all post-run assertions. Also added `saved_state: dict | None` as the authoritative "did state persist?" signal (dict on persisted, None on cleared).
  2. `block_with_json` exits with `SystemExit(0)` (not 2) while still emitting the `{"continue": true, "decision": "block"}` payload on stdout. Initial test expected code 2 by analogy with a common hook pattern; updated to assert code 0 + `payload["decision"] == "block"` instead.
- Phase 4 Status: COMPLETE.
- Next steps: proceed into Phase 5 (install/routing/docs convergence: add `arch-loop` to `SKILLS`/`CLAUDE_SKILLS` in `Makefile`, keep out of `GEMINI_SKILLS`, update `README.md` inventory + install/usage sections, update `docs/arch_skill_usage_guide.md`, update `skills/arch-skills-guide/SKILL.md`, then run `npx skills check` + `make verify_install`).

## Phase 5 Progress Update
- Work completed:
  - `Makefile`: added `arch-loop` to `SKILLS` and `CLAUDE_SKILLS` (after `arch-skills-guide`, before `delay-poll`); `GEMINI_SKILLS` left unchanged on purpose because Gemini still has no Stop-hook continuation surface and the evaluator subprocess always shells out to Codex.
  - `README.md`:
    - Added `arch-loop` to "Other shipped skills" with a one-line summary that distinguishes it from `delay-poll` (condition-only) and from specialized loops like `audit-loop` (prescribed map-first flow).
    - Inserted `arch-loop` into the "Codex automatic ... also require the Codex feature flag" sentence and into the Stop-hook handler-call-order line in the install section.
    - Added `~/.agents/skills/arch-loop/` and `~/.claude/skills/arch-loop/` install-path entries; left the Gemini install path list intact.
    - Rewrote the `codemagic-builds`/`amir-publish`/`delay-poll`/`wait`/`code-review` Gemini-omission paragraph to also cover `arch-loop`, including the explicit Codex-backed-evaluator exception language ("evaluator turns additionally always shell out to fresh unsandboxed Codex `gpt-5.4` `xhigh` for the external verdict; the Claude host can arm and drive the loop, but the evaluator subprocess itself is always Codex, mirroring the `code-review` exception").
    - Added a new `### arch-loop` shipped-skills section just before `### delay-poll` covering use-case, evaluator subprocess shape, `parent_work` vs `wait_recheck` continue modes, controller state paths (`.codex/arch-loop-state.<SESSION_ID>.json` and `.claude/arch_skill/arch-loop-state.<SESSION_ID>.json`), runtime preflight requirements, the "no copied hook file under `~/.codex/hooks/`" rule, and the boundary against `delay-poll` and the specialized loops.
    - Added `arch-loop` to the "Primary surface" usage line and added three usage examples (free-form copy tightening, `$agent-linter` clean-audit, interval-based host-reachability with explicit `max 8 hours` cap).
  - `docs/arch_skill_usage_guide.md`:
    - Added `arch-loop` to the "Other shipped skills" list and the agents install-path list.
    - Added `arch-loop` to the Codex feature-flag prerequisite paragraph and the Codex/Claude installed-skill lists; left Gemini intact.
    - Updated the install-summary footer to include `arch-loop` alongside the other Stop-hook-backed controllers.
    - Rewrote the Gemini-omission paragraph to cover `arch-loop`, `delay-poll`, and `wait` together and to call out the Codex-backed-evaluator exception explicitly.
    - Added a full `### arch-loop` "Choosing a skill" subsection with examples and a Practical Rule list covering specialized-loop boundary, `delay-poll` boundary, named `$skill` audits, deterministic cap extraction, `parent_work` vs `wait_recheck` continue modes, controller state paths, the always-Codex evaluator subprocess, runtime preflight, and the "do not run the Stop hook yourself" discipline.
  - `skills/arch-skills-guide/SKILL.md`:
    - Added `arch-loop` to the description frontmatter list.
    - Added `audit loop sim` and `arch loop (generic hook-backed completion loop)` to the "classify the ask into one of these families" list.
    - Added the `audit-loop-sim` and `arch-loop` mapping rules to the "Map the task to the suite" workflow list.
  - `skills/arch-skills-guide/references/skill-map.md`:
    - Added a new decision-order entry for `audit-loop-sim` (was previously missing) and a new decision-order entry for `arch-loop`, then renumbered subsequent steps so the default-to-`arch-step` rule still anchors the end of the list.
    - Added skill-map table rows for `audit-loop-sim` and `arch-loop` with use-when, do-not-default-when, and example asks.
    - Added near-lookalike boundary rules for `arch-loop` against specialized loops, `delay-poll`, `wait`, and `goal-loop`.
    - Added `audit-loop-sim` and `arch-loop` to the tour-order list so the suite tour reflects the live install set.
  - `skills/arch-skills-guide/references/boundary-examples.md`: added two new sections — "Specialized loops vs generic completion loop" (routes free-form, named-audit, and capped cadence asks to `arch-loop` and prescribed flows to the matching specialized loop) and "Generic completion loop vs pure wait/poll" (routes one-shot sleeps to `wait`, condition-only polls to `delay-poll`, and "parent work between checks until external evaluator says stop" to `arch-loop`).
- Tests run + results:
  - `make install` — added `arch-loop` to `~/.agents/skills/`, `~/.claude/skills/`, and the dispatcher hook coverage; harness skills listing now includes `arch-loop`.
  - `make verify_install` — all five `OK` lines: agents skills, Codex hook from `~/.agents/skills`, Claude skills + Claude hook from `~/.agents/skills`, Gemini skills, and the combined active-surface summary.
  - `python -m unittest discover tests -q` — 152 tests OK (69 arch-loop + 76 codex stop-hook + 7 other suites). No regressions.
  - `npx skills check` — ran without repo errors. The CLI's only attempted update target (the unrelated commercial `harden` skill) failed, which is unrelated to the arch_skill repo packages.
  - Targeted `rg` for `arch-loop` returned 17 files: live additions across `Makefile`, `README.md`, `docs/arch_skill_usage_guide.md`, `skills/arch-skills-guide/{SKILL.md,references/skill-map.md,references/boundary-examples.md}`, the `skills/arch-loop/` package itself, the controller `arch_controller_stop_hook.py`, the controller test suite, the active plan/worklog, and one historical worklog (`docs/GENERIC_WAIT_DELAY_THEN_EXECUTE_SKILL_2026-04-19_WORKLOG.md`) that names `delay-poll`+`wait` together — left alone because that worklog is point-in-time history of the wait/delay phase, not a live routing surface.
- Issues / deviations:
  1. The skill-map decision order was missing `audit-loop-sim` from before this phase. Fixed in the same edit that added `arch-loop`, since both belong under the same map-first/loop family and the missing entry would have made the new `arch-loop` boundary harder to read.
  2. `npx skills check` exits with a "Failed to update 1 skill" message about the unrelated commercial `harden` skill; this is not a repo-level validation failure and the `npx skills ls -p` projection still lists every local arch_skill package, including `arch-loop`.
- Phase 5 Status: COMPLETE.
- Next steps: proceed into Phase 6 (representative loop proof: 8 Codex lifecycle probes covering clean/parent_work continue/wait_recheck/blocked/timeout/max-iteration/cadence-to-work/cadence-timeout/hook-timeout-fit rejection, the Claude runtime-path probe through the shared runner, the named-audit `$agent-linter` obligation case, one real `codex exec -p yolo` evaluator smoke, and the full verification suite, then plan/worklog finalization).

## Phase 6 Progress Update — 2026-04-19

- Work completed:
  - Added five focused probe tests to `tests/test_arch_loop_controller.py` inside two new test classes, closing the gaps the Stop-hook audit named as Phase 6's remaining frontier:
    - `ArchLoopPhase6CodexProofTests` (pins `ACTIVE_RUNTIME` to the Codex spec in `setUpClass`):
      - `test_cadence_to_work_wakes_parent_with_concrete_prompt` — builds a state with `interval_seconds=1_800`, a future `next_due_at`, and a non-zero `check_count`, returns a `continue_mode: parent_work` verdict with a concrete `next_task`, and asserts the hook slept for the cadence gap, blocked with `decision: "block"` and `continue: True`, embedded a reason that names `arch-loop`, kept state armed, and incremented `check_count`.
      - `test_cadence_window_overruns_deadline_and_clears_state` — builds a state whose cadence window (`interval_seconds=2_000`, `next_due_at=4_000`) crosses `deadline_at=5_500`, returns a wait-recheck verdict, and asserts the hook clears state and stops with a reason naming both `cadence` and `deadline`.
      - `test_agent_linter_obligation_clean_pass_accepted` — builds a state whose `required_skill_audits` already names `agent-linter` with `status: pending`, returns a `clean` verdict whose `required_skill_audits[0].status == "pass"`, and asserts the handler accepts the clean verdict and clears state.
      - `test_agent_linter_obligation_clean_with_missing_evidence_rejected` — same state shape as above, but the evaluator returns `clean` with `required_skill_audits[0].status == "missing"`; asserts the handler rejects the clean verdict even so, clears state, and emits a stop reason that names `audit`.
    - `ArchLoopPhase6ClaudeRuntimeProofTests` (pins `ACTIVE_RUNTIME` to the Claude spec in `setUpClass` and restores Codex in `tearDownClass`):
      - `test_claude_runtime_resolves_state_under_claude_arch_skill` — asserts `controller_state_relative_path(ARCH_LOOP_STATE_SPEC).parts[:2] == (".claude", "arch_skill")`, writes an armed state at that path, runs the full handler end-to-end with a mocked clean evaluator, and asserts the Claude-runtime state file is cleared when the loop finishes clean.
  - Captured real Codex-backed evaluator smoke runs from `/tmp/arch-loop-phase6/` with the exact installed contract:
    - Prep files: `schema.json` (full `ARCH_LOOP_EVAL_SCHEMA`), `prompt.md` (intentionally contradictory — "do not modify it" alongside a work summary that said "Created"), `prompt-clean.md` (consistent — "Create" + "Created"), and `target.txt` containing `PHASE6_OK`.
    - Blocked-case command: `codex exec -p yolo --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox -C /tmp/arch-loop-phase6 --output-schema /tmp/arch-loop-phase6/schema.json -o /tmp/arch-loop-phase6/last_message.json /tmp/arch-loop-phase6/prompt.md`.
      - Result: schema-valid `verdict: "blocked"` with a non-empty `blocker` string (evaluator correctly caught the contradiction between "do not modify it" and the work summary's "Created"). Captured in `/tmp/arch-loop-phase6/last_message.json`.
    - Clean-case command: `codex exec -p yolo --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox -C /tmp/arch-loop-phase6 --output-schema /tmp/arch-loop-phase6/schema.json -o /tmp/arch-loop-phase6/last_message_clean.json /tmp/arch-loop-phase6/prompt-clean.md`.
      - Result: schema-valid `verdict: "clean"` with three entries in `satisfied_requirements`, empty `unsatisfied_requirements` / `required_skill_audits` / `next_task` / `blocker`, and `continue_mode: "none"`. Captured in `/tmp/arch-loop-phase6/last_message_clean.json`.
- Tests run + results:
  - `python3 -m py_compile skills/arch-step/scripts/*.py` — OK.
  - `python3 -m unittest` — 157 tests OK (72 arch-loop controller tests including the five new probes, 78 codex stop-hook tests, and the other suites). No regressions.
  - `npx skills check` — ran without repo-level errors. Same unrelated "Failed to update 1 skill" on the commercial `harden` skill that Phase 5 already documented; every local arch_skill package still validates.
  - `make verify_install` — all five `OK` lines: agents skills, Codex hook, Claude skills + Claude hook, Gemini skills, and the combined active-surface summary.
  - Real Codex evaluator smoke (both `gpt-5.4` / `xhigh`): both runs returned schema-valid JSON — the blocked case proved the evaluator actually reasons over the structured inputs (it flagged the prompt/summary contradiction), and the clean case proved the termination contract works end-to-end from a repo-root-style `-C` invocation.
- Issues / deviations:
  1. `npx skills check` still exits nonzero because of the unrelated commercial `harden` skill (same failure Phase 5 documented). `npx skills ls -p` still lists every local arch_skill package, including `arch-loop`. Not a repo-level blocker.
- Residual risks:
  1. Phase 6 proof used mocked `current_epoch_seconds`, `sleep_for_seconds`, and `run_arch_loop_evaluator` for cadence/Claude-runtime tests (so the suite does not depend on wall-clock sleeps or hitting real Codex). The real Codex smoke was exercised separately with the installed contract.
  2. The Codex evaluator-smoke artifacts live under `/tmp/arch-loop-phase6/` rather than in-repo; this is intentional (the contract requires a writable `-C` workspace and the evaluator is stateless), but it means the evidence files are ephemeral to this machine. The commands above reproduce them.
- Phase 6 Status: COMPLETE.
- Next steps: end the turn so the installed Stop hook can run a fresh `audit-implementation` over all six phases; on a clean audit the loop will hand off to `$arch-docs` for final docs consolidation.
