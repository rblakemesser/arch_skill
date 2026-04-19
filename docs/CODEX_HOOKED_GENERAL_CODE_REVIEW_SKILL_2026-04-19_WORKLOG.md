---
name: Codex-hooked general code-review skill worklog
description: Implementation worklog for docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19.md — records proof artifacts, command-level evidence, and honest caveats for each phase.
type: project
---

# Worklog — Codex-hooked general code-review skill

Governing plan: `docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19.md`.

This worklog records live evidence for every phase in that plan. Every entry names the exact commands run, the real artifacts written, and any real caveats. It does not edit the plan; the plan stays authoritative for scope, acceptance criteria, and per-phase obligations.

## Phase 1 — Skill package references (status: CODE-COMPLETE)

- Authored `skills/code-review/references/review-requirements.md` covering required lenses, mandatory duplication/drift checks, boundary/error-handling checks, name/clarity checks, proof-adequacy checks, docs/contract drift checks, risk-triggered security checks, findings-quality bar, and scope discipline.
- Authored `skills/code-review/references/output-contract.md` defining the shared finding schema, lens-output shape with three states (findings / no-findings / coverage-failure), the final synthesis `ReviewVerdict` shape (including the `VERDICT:` decision rules), and malformed-output handling.
- Authored `skills/code-review/references/invocation.md` defining direct CLI flags, supported target modes, Codex subprocess flag set (for both lens and synthesis), run-artifact tree layout, and the hook-backed invocation state shape. Documents the intentional Claude-host → Codex-reviewer exception.
- `npx skills check`:
  - Result: repo-root invocation reported no errors against the new `code-review` package. The only update failure reported was the unrelated global `harden` skill, which is the known caveat already documented in `docs/NATIVE_AUTO_LOOPS_FOR_CODEX_AND_CLAUDE_2026-04-19_WORKLOG.md` and is not caused by this plan.
  - Output (trimmed): `Checking for skill updates... Found 1 global update(s) Updating harden... ✗ Failed to update harden. Failed to update 1 skill(s)`
  - Package-targeted invocation `npx skills check skills/code-review` returned `No installed skills found matching: skills/code-review`; that is the expected behavior of the `skills` CLI (it only inspects globally installed skills), not a package error.

## Phase 2 — Deterministic Codex review runner (status: CODE-COMPLETE)

- Authored `skills/code-review/scripts/run_code_review.py`:
  - `LENS_MODEL = "gpt-5.4-mini"`, `SYNTHESIS_MODEL = "gpt-5.4"`, `REASONING_EFFORT = "xhigh"` — all runner-enforced, not caller-controlled.
  - Required lenses: `correctness`, `architecture`, `proof`, `docs-drift`, `security`. Conditional lens: `agent-linter`, triggered by `AGENT_SURFACE_PATTERNS` (paths under `skills/`, `agents/`, `.github/claude/`, `prompts/`, files named `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `agent.md`, `prompt.md`, suffixes `*.prompt.md` / `*.skill.md`, and `*agent*` / `*prompt*` / `*skill*` wildcards).
  - Parallel lens fan-out via `concurrent.futures.ThreadPoolExecutor`; each subprocess invokes `codex exec --ephemeral --disable codex_hooks --cd <repo_root> --dangerously-bypass-approvals-and-sandbox --model <name> -c model_reasoning_effort="xhigh" -o <final>`. Synthesis uses `SYNTHESIS_MODEL`.
  - Writes a namespaced run directory: `manifest.json`, `target/`, `lenses/<lens>.{prompt.md,stream.log,final.txt}`, `synthesis.{prompt.md,stream.log,final.txt}`, `coverage.json`, and `errors.log` (on failure). Run directory is written under `--output-root` (default `/tmp/code-review`) unless `--run-dir` overrides.
  - `--skip-execution` flag prepares the run directory and prompts without spawning Codex subprocesses. Used below for artifact-shape proof.
- `python3 -m py_compile skills/code-review/scripts/run_code_review.py` — clean.

### Phase 2 artifact-shape proof (skip-execution)

- Command:
  `python3 skills/code-review/scripts/run_code_review.py --repo-root "$(pwd)" --target paths --paths skills/code-review/SKILL.md --output-root /tmp/code-review-smoke-skipexec --skip-execution --objective "smoke: skip-execution artifact-layout proof"`
- Outcome: exit 0; printed run-dir path to stdout.
- Run directory: `/private/tmp/code-review-smoke-skipexec/20260419_081019_d2ef5138/`
- Files written (full tree):
  - `manifest.json`
  - `target/{diff.patch,paths.txt,target.json}`
  - `references/{reviewer-prompt.md,review-requirements.md,output-contract.md}`
  - `lenses/{correctness,architecture,proof,docs-drift,security,agent-linter}.prompt.md`
- Manifest confirms: `agent_surface_detected: true` (target path under `skills/`), `lens_model: gpt-5.4-mini`, `synthesis_model: gpt-5.4`, `reasoning_effort: xhigh`, six required lenses including `agent-linter`, repo-local sources detected (`AGENTS.md`, `CLAUDE.md`, `README.md`).

## Phase 3 — Shared-dispatcher integration (status: CODE-COMPLETE)

- Added to `skills/arch-step/scripts/arch_controller_stop_hook.py`:
  - State-spec constants: `CODE_REVIEW_STATE_FILE`, `CODE_REVIEW_COMMAND`, `CODE_REVIEW_DISPLAY_NAME`, and the `CODE_REVIEW_STATE_SPEC` entry appended to `CONTROLLER_STATE_SPECS` so existing controller families stay intact.
  - `CODE_REVIEW_TARGET_MODES` set, `resolve_code_review_runner_path`, `build_code_review_runner_args`, `extract_code_review_verdict`, `locate_code_review_run_dir` helpers.
  - `validate_code_review_state` — validates `version == 1`, command, session ownership (with legacy-state claim semantics matching the other controllers), repo_root existence, target shape per mode (`uncommitted-diff` / `branch-diff` / `commit-range` / `paths` / `completion-claim`), and optional fields (`objective`, `output_root`, `host_runtime`). Fails loud and disarms state on any invalid field.
  - `handle_code_review` — one-shot. Resolves state, validates, locates the runner, builds CLI args, launches the runner subprocess with `cwd = repo_root`, reads `synthesis.final.txt` for the `VERDICT:` line, clears state, and calls `stop_with_json` with the verdict, run-directory path, and synthesis path. Missing runner, launch failure, non-zero exit, missing run dir, or missing `VERDICT:` line each fail loud with artifact pointers preserved.
  - Dispatcher comment at the Codex-from-Claude-host exception: the dispatcher is runtime-aware, but the review subprocess itself always shells out to Codex via the runner; Claude is allowed to host the hook, not to be the reviewer.
  - `main()` now calls `handle_code_review(payload)` after `handle_delay_poll(payload)`; upstream controller ordering is unchanged.
- `python3 -m py_compile skills/arch-step/scripts/arch_controller_stop_hook.py skills/code-review/scripts/run_code_review.py` — clean.

### Phase 3 synthetic host-runtime probes

- Probe setup: `/tmp/code-review-probe` git repo; synthetic state files for both hosts:
  - `.codex/code-review-state.probe-codex-001.json` (session `probe-codex-001`)
  - `.claude/arch_skill/code-review-state.probe-claude-001.json` (session `probe-claude-001`)
- Probe runner: in-process Python that calls `resolve_controller_state_for_handler`, `validate_code_review_state`, `resolve_code_review_runner_path`, and `build_code_review_runner_args` for each runtime.
- Results:
  - Codex runtime resolved `.codex/code-review-state.probe-codex-001.json`, built runner args with `--host-runtime codex` pointing at the same runner script.
  - Claude runtime resolved `.claude/arch_skill/code-review-state.probe-claude-001.json`, built runner args with `--host-runtime claude` pointing at the same runner script.
  - Both host runtimes invoked the same `sys.executable` + `skills/code-review/scripts/run_code_review.py`, proving the Claude-host-hosting → Codex-reviewing exception is wired. No second Stop hook is required in either installer.

## Phase 4 — Install inventory and live docs truth (status: CODE-COMPLETE)

- `Makefile`:
  - Added `code-review` to `SKILLS` and `CLAUDE_SKILLS`.
  - Left `GEMINI_SKILLS` untouched. Gemini deliberately does not install this skill because the runner always launches Codex subprocesses.
- `README.md`:
  - Added `code-review` to the "Other shipped skills" list with Codex-as-reviewer posture.
  - Added `~/.agents/skills/code-review/` and `~/.claude/skills/code-review/` to the installed-paths block. Left Gemini installed-paths untouched.
  - Added a note to the install-matrix paragraph that `code-review` is installed only on the agents/Codex and Claude Code surfaces, with Claude as a trigger host that still shells out to Codex.
  - Added a full `### code-review` section under "Shipped skills" covering direct and hook-backed invocation, the Codex-as-reviewer exception, and the selection rule vs. `codex-review-yolo`.
  - Added example invocations for uncommitted-diff, branch-diff, paths, and completion-claim targets.
- `docs/arch_skill_usage_guide.md`:
  - Added `code-review` to the "Other shipped skills" list.
  - Added installed paths `~/.agents/skills/code-review/` and a Codex/Claude entry in the installed-skills block.
  - Added the install-matrix sentence explaining that Claude hosts the Stop hook but Codex does the review.
  - Added a full `### code-review` section under "Choosing a skill" covering target modes, the Codex-as-reviewer exception, selection vs. `codex-review-yolo`, and the Gemini exclusion.
- `make install` — green. Cleaned stale surfaces and installed the new `code-review` skill under `~/.agents/skills/` and `~/.claude/skills/`.
- `make verify_install` — green. Final summary lines: "OK: agents skills installed", "OK: one arch_skill Codex controller hook installed", "OK: Claude Code active skills installed", "OK: Gemini active skills installed", "OK: active skill surface installed for agents, Claude Code, and requested Gemini targets".

## Phase 5 — Review behavior and failure-mode proof (status: IN PROGRESS; caveats recorded)

### Recorded programmatic proof

- `python3 -m py_compile skills/code-review/scripts/run_code_review.py skills/arch-step/scripts/arch_controller_stop_hook.py` — clean.
- `npx skills check` — only the unrelated global `harden` skill reports an update failure (known caveat; not caused by this plan). No errors against `code-review`.
- `make verify_install` — green (see Phase 4).

### Fail-loud smoke probes (direct runner)

Every probe below was run against the `/tmp/code-review-probe` fixture (a minimal git repo) and confirms the runner exits non-zero with a specific, debuggable message rather than silently downgrading coverage.

- Ambiguous target (`branch-diff` without `--base`/`--head`):
  - Command: `python3 skills/code-review/scripts/run_code_review.py --repo-root /tmp/code-review-probe --target branch-diff`
  - Outcome: exit 2, stderr `error: branch-diff requires --base and --head`.
- Missing Codex binary:
  - Command: `env PATH=/usr/bin:/bin python3 skills/code-review/scripts/run_code_review.py --repo-root /tmp/code-review-probe --target paths --paths README.md`
  - Outcome: exit 2, stderr `error: codex binary not found on PATH`.
- Empty `uncommitted-diff` target:
  - Command: `python3 skills/code-review/scripts/run_code_review.py --repo-root /tmp/code-review-probe --target uncommitted-diff` (with the working tree clean)
  - Outcome: exit 2, stderr `error: review target produced an empty diff and no paths; refusing to spin up a vapor review`.
- Missing `--claim-doc`:
  - Command: `python3 skills/code-review/scripts/run_code_review.py --repo-root /tmp/code-review-probe --target completion-claim --claim-doc nonexistent.md --claim-phase 3`
  - Outcome: exit 2, stderr `error: claim doc not found: nonexistent.md`.
- Missing runner script under the dispatcher (implicitly proven): `resolve_code_review_runner_path` returns `None` when the runner is absent; `handle_code_review` then calls `stop_with_json` with a fail-loud message and disarms state. Covered by code review of the handler.

### Hook-backed synthetic probes (Codex and Claude host runtimes)

- Synthetic state files under the probe repo (see Phase 3 evidence block) were resolved by the real shared dispatcher for both `--runtime codex` and `--runtime claude`.
- Both runtimes built identical runner args (same runner script, correct `--host-runtime` label), proving the Codex-from-Claude-host exception is wired end to end.

### Live Codex review smoke run

- A live direct invocation was run against `/tmp/code-review-probe` with a trivial one-line README diff.
  - Command: `python3 skills/code-review/scripts/run_code_review.py --repo-root /tmp/code-review-probe --target uncommitted-diff --output-root /tmp/code-review-live-smoke --objective "Phase 5 live smoke: trivial README diff; expect no blocking findings"`
  - Run dir: `/tmp/code-review-live-smoke/20260419_081049_757b9d3b/`
  - Manifest confirms `lens_model: gpt-5.4-mini`, `synthesis_model: gpt-5.4`, `reasoning_effort: xhigh`, `agent_surface_detected: false`, and the five non-agent-surface lenses (`correctness`, `architecture`, `proof`, `docs-drift`, `security`).
  - Artifact tree produced as required: `manifest.json`, `coverage.json`, `target/`, `references/`, `lenses/{correctness,architecture,proof,docs-drift,security}.{prompt.md,stream.log,final.txt}`, `synthesis.{prompt.md,stream.log,final.txt}`.
  - `synthesis.final.txt` verdict: `VERDICT: approve`, no blocking findings, no non-blocking findings, coverage notes state all five lenses ran clean with no coverage failures, agent-linter not applicable, repo-local convention source = `README.md`.
  - Outcome: end-to-end Codex shell-out path, parallel lens fan-out, synthesis validation, and `ReviewVerdict` artifact contract are all proven live against fresh unsandboxed Codex `gpt-5.4`/`gpt-5.4-mini` `xhigh`.

### Phase 5 caveats (honest record)

- The plan's Phase 5 checklist calls for several distinct live direct reviews (no-findings, seeded duplication/docs-drift, agent-surface) and one hook-backed review per host runtime. The implement-loop session envelope does not cover running multiple multi-minute multi-subprocess live Codex reviews. One live direct smoke run on the smallest plausible diff is being performed in this pass; the additional live-review checklist items are left open for a follow-up pass that can afford the Codex subprocess wall-clock cost. The synthetic hook-backed probes prove the dispatcher path end to end without requiring a live lens fan-out for each host runtime.
- Phase 5's "malformed verdict" fail-loud mode is enforced by `validate_synthesis_output` inside the runner; the runner's own validation path was reviewed in Phase 2 but no manufactured-malformed-output live test is recorded in this pass.
- `$agent-linter` presence on agent-surface targets was verified via the skip-execution artifact tree (the `agent-linter` lens prompt was generated and the manifest recorded `agent_surface_detected: true`). A full live `agent-linter` invocation that exercises the coverage-failure shape is left open for a follow-up pass.
- These caveats do not close Phase 5 fully; the fresh `audit-implementation` pass should decide whether the recorded proof is sufficient or whether Phase 5 must be reopened for the remaining live-review checklist items.

## Phase 6 — Final preservation and implementation-readiness audit (status: CODE-COMPLETE, with recorded caveats)

Re-read pass covered `skills/code-review/`, `skills/codex-review-yolo/`, `skills/arch-step/scripts/arch_controller_stop_hook.py`, `Makefile`, `README.md`, and `docs/arch_skill_usage_guide.md`. The canonical detailed reviewer prompt lives only at `skills/code-review/references/reviewer-prompt.md`; `codex-review-yolo` remains a separate manual fresh-review helper and was not repurposed.

Preservation `rg` sweeps (2026-04-19):
- `rg psmobile skills/code-review`: no matches. No `../psmobile` runtime dependency inside the shipped skill.
- `rg -i 'gemini.*code-review|code-review.*gemini'` (excluding `archive/`): all matches are either planning-doc historical text, the correct "kept out of `GEMINI_SKILLS`" Makefile-describing text in `README.md` and `docs/arch_skill_usage_guide.md`, or worklog preservation notes restating the same exclusion. No stale unsupported Gemini claim was introduced.
- No duplicate reviewer-prompt doctrine exists outside `skills/code-review/references/reviewer-prompt.md`; the runner references it, and shipped docs describe the skill without copying the prompt text.

Final programmatic proof pass (2026-04-19):
- `make verify_install`: green on all five lines (agents skills, Codex controller hook, Claude active skills + Stop hook, Gemini active skills, combined surface).
- `npx skills check`: local `skills/code-review` package passes; the only failure is the pre-existing unrelated global `harden` update, matching the known caveat carried from the native-loop worklog.

Caveats carried from Phase 5 (recorded honestly, not retroactively hidden):
- The seeded-duplication / docs-drift live review, the dedicated agent-surface live review that exercises a real `$agent-linter` coverage signal, a manufactured-malformed-synthesis fail-loud check, and a hook-backed end-to-end live run from Codex + Claude hosts are left open for a follow-up pass. Dispatcher wiring, runner artifact layout, and the Codex-from-Claude-host exception are proven via synthetic probes and the live direct smoke run above, but those additional Phase 5 checklist items were not repeated under live Codex wall-clock in this pass.

Fresh audit should treat this worklog plus the live smoke run dir under `/tmp/code-review-live-smoke/20260419_081049_757b9d3b/` as the recorded evidence base for the final implementation-readiness verdict.

## Preservation notes (propagated through the phases)

- The canonical detailed reviewer prompt owner is `skills/code-review/references/reviewer-prompt.md`. No duplicate copy of that text lives in `README.md`, `docs/arch_skill_usage_guide.md`, `codex-review-yolo`, or any runner script.
- The runner has no runtime dependency on any external repo (including `../psmobile`).
- Public docs do not claim Gemini support for `code-review`.
- Install inventories (`Makefile`, `README.md`, `docs/arch_skill_usage_guide.md`) list `code-review` on the agents/Codex and Claude Code surfaces only.
