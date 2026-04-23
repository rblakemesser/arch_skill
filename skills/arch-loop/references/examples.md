# `arch-loop` Examples

These examples illustrate how `arch-loop` preserves free-form requirements, parses caps and cadence, seeds named audits, and defers the stop verdict to the fresh external Codex `gpt-5.4` `xhigh` evaluator. They are not a finite rulebook; the skill should understand similar requests that combine these patterns.

## 1) Named-audit clean loop

**Ask:** "Implement `docs/AGENTS_MD_AUTHORING_SKILL_2026-04-17.md` and don't stop until the plan is fully implemented and you get a clean audit by `$agent-linter`. Max runtime 5h."

**What `arch-loop` does on the initial invocation:**

- captures the full ask literally in `raw_requirements`
- parses `max runtime 5h` → `deadline_at = created_at + 18000`, `cap_evidence: [{type: "runtime", source_text: "Max runtime 5h", normalized: "deadline_at=<+18000s>"}]`
- detects `$agent-linter` → `required_skill_audits: [{skill: "agent-linter", target: "skills/agents-md-authoring", requirement: "clean bill of health", status: "pending", ...}]`
- runs arm-time ensure-install (`arch_controller_stop_hook.py --ensure-installed --runtime <codex|claude>`); aborts loudly if the installer fails
- writes the runtime-specific state file (`.codex/arch-loop-state.<SESSION_ID>.json` or `.claude/arch_skill/arch-loop-state.<SESSION_ID>.json`)
- does one bounded implementation pass toward the plan doc's Section 7 frontier
- runs `$agent-linter` during that pass, updates its `required_skill_audits` entry with `status`, `latest_summary`, and an optional `evidence_path`
- updates `last_work_summary` and `last_verification_summary`
- ends the turn naturally

**What the Stop hook does on subsequent turns:**

- if `deadline_at` is past, clears state and stops with a timeout summary
- otherwise launches the fresh external Codex `gpt-5.4` `xhigh` evaluator with the prompt at `references/evaluator-prompt.md`
- on `continue` + `parent_work` + a concrete `next_task`, blocks with a continuation prompt naming `$arch-loop` and the next task
- on `blocked`, clears state and stops with the evaluator's `blocker`
- on `clean`, clears state and stops with the evaluator's `summary`

**Stop condition:** the evaluator verifies that `$agent-linter` has passing evidence, the plan doc is concretely implemented, and no unsatisfied requirement remains. Only then can it return `clean`.

## 2) Cadence-driven host reachability loop

**Ask:** "Every 30 minutes, check whether host `example.com` is reachable, for the next 6 hours."

**What `arch-loop` does on the initial invocation:**

- captures the ask literally in `raw_requirements`
- parses `every 30 minutes` → `interval_seconds = 1800`
- parses `for the next 6 hours` → `deadline_at = created_at + 21600`
- `cap_evidence` records both source phrases
- `required_skill_audits` is empty (no named audit)
- runs one immediate grounded reachability check using a read-only probe appropriate for the target (for example a single `curl -sSf --max-time 10 https://example.com/` or equivalent network check)
- writes `last_verification_summary` with the probe result
- ends the turn naturally

**What the Stop hook does on subsequent turns:**

- launches the fresh external evaluator
- if the probe shows the host is reachable and `raw_requirements` is satisfied, the evaluator returns `clean`
- otherwise the evaluator returns `continue` with `continue_mode: wait_recheck` and a specific `next_task` (for example: "retry the same read-only reachability probe against example.com")
- the Stop hook sets `next_due_at = now + 1800`, sleeps until `min(next_due_at, deadline_at)`, and reruns the evaluator/check without waking the parent thread
- if `deadline_at` is reached with the host still unreachable, the hook clears state and stops with a timeout summary

**Stop condition:** the host becomes reachable before the deadline, or the deadline expires. The parent thread is only woken if the evaluator switches to `parent_work` (for example, if the user's request required follow-up work after reachability) or if the loop stops.

## 3) Iteration-capped "try twice" loop

**Ask:** "Implement the fix, run the smoke script, and stop after two attempts. If it still fails, surface the blocker."

**What `arch-loop` does:**

- captures the ask literally
- parses `stop after two attempts` (word-form magnitude) → `max_iterations = 2`
- runs one bounded implementation pass, runs the smoke script, writes `last_work_summary` and `last_verification_summary`
- ends the turn naturally

**What the Stop hook does:**

- evaluator returns `continue` + `parent_work` if the smoke still fails and more work is possible
- the hook blocks with the next task; the parent does one more bounded pass
- after the second parent pass, `iteration_count` reaches `max_iterations`; if the evaluator still returns `continue`, the hook clears state and stops with a max-iterations summary that includes `unsatisfied_requirements`
- if the evaluator returns `clean` before the cap, the loop stops clean

## 4) Drift catch: evaluator reverses a parent-claimed `pass`

**Ask:** "Keep working on `skills/example-skill` and do not stop until `$agent-linter` is clean on the package. Max runtime 1h."

**What `arch-loop` does on the initial invocation:**

- captures the ask literally and computes `raw_requirements_hash = sha256(raw_requirements)`
- seeds `required_skill_audits: [{skill: "agent-linter", target: "skills/example-skill", requirement: "clean", status: "pending", ...}]`
- parses `max runtime 1h` → `deadline_at = created_at + 3600`
- does one bounded implementation pass, runs `$agent-linter`, sees one lingering warning on `skills/example-skill/SKILL.md:12`
- refreshes the audit entry's `latest_summary` ("one warning remains at SKILL.md:12") without touching `status`
- ends the turn; the Stop hook runs the evaluator, copies `status: fail` into state, and asks the parent to fix the warning

**What the next parent pass does under drift pressure (and what the hook catches):**

- parent pass edits the warned line, reruns the linter locally, sees clean output in its own shell, and — drifting — writes `status: pass` directly into `required_skill_audits[0].status` alongside a reassuring `latest_summary`
- parent ends the turn
- Stop hook reads state, recomputes `audits_authoritative_fingerprint` over `(skill, target, requirement, status)`, and sees it no longer matches the fingerprint the hook stored after the last evaluator run
- hook clears state with `audit status mutation detected` and a loud one-line reason; the parent must re-arm with truthful state

**Alternate path (no parent cheating):**

- parent refreshes only `latest_summary` / `evidence_path`, leaves `status` untouched, ends the turn
- hook launches the fresh evaluator; the evaluator reads the repo directly (not the parent's narrative), finds the linter actually reports a different warning the parent missed, and returns `status: fail` with `evidence: "npx skills check skills/example-skill"` and a specific `next_task`
- hook copies the evaluator's `fail` into state, recomputes the fingerprint, and dispatches `continue` + `parent_work`

**Stop condition:** `clean` only when the evaluator — running its own repo check — returns `status: pass` with a reproducible `evidence` pointer. A parent-written `pass` never reaches `clean`.

## 5) Long-running background job — parent yields with `sleep_for`

**Ask:** "Optimize the handset-eval sampler. Run the `trials=4` benchmark at `/tmp/he_sampleropt_3p_t4` against the 3p serial-toggle baseline, copy logs/time/metrics into `diagnostics/handset_eval_opt_<DATE>/`, run semantic parity, and either commit the sampler change if both 2p and 3p are faster with parity or revert it and profile the next hotspot. Max runtime 4h."

**What `arch-loop` does on the initial invocation:**

- captures the full ask literally in `raw_requirements`
- parses `Max runtime 4h` → `deadline_at = created_at + 14400`; `cap_evidence` records the phrase
- `required_skill_audits` is empty (no `$`-named audit in this ask)
- runs arm-time ensure-install and writes the runtime-specific state file
- kicks the benchmark off as a detached background process writing its finish marker to `/tmp/he_sampleropt_3p_t4.time`; logs go to `/tmp/he_sampleropt_3p_t4.log`
- writes `last_work_summary` naming the marker path and expected wall-clock (e.g. "benchmark launched; marker `/tmp/he_sampleropt_3p_t4.time` appears when trials=4 finish, typically ~10 min")
- ends the turn naturally

**First Stop-hook pass:**

- the fresh external evaluator inspects the repo, sees the marker is still empty and no diagnostics were copied yet, and returns `continue` + `parent_work` with `next_task` shaped roughly as: *"Let the active /tmp/he_sampleropt_3p_t4 trials=4 process finish, then copy `/tmp/he_sampleropt_3p_t4.{log,time}` and its `metrics.json` into `diagnostics/handset_eval_opt_<DATE>`, run semantic parity, update INVESTIGATION.md, and commit-or-revert."*
- the hook blocks with the continuation prompt naming `$arch-loop` and the full `next_task`

**What the next parent pass does (the lesson):**

- reads `last_next_task`, recognizes the *"Let the active X finish, then …"* shape
- runs the marker check once (for example `ls -la /tmp/he_sampleropt_3p_t4.time`); sees the file is still 0 bytes
- writes the minimal child-yield request into state and ends the turn:

  ```jsonc
  "requested_yield": {
    "kind": "sleep_for",
    "seconds": 600,
    "reason": "waiting on /tmp/he_sampleropt_3p_t4.time marker; nothing for parent to do until the benchmark lands"
  }
  ```

- refreshes `last_work_summary` with the one-line marker status so the next evaluator pass has grounded context ("benchmark still running; yielded sleep_for 600s on marker")
- ends the turn

**What the Stop hook does with the yield:**

- honors `requested_yield` at the top of dispatch per `skills/arch-loop/references/controller-contract.md` §Child-requested yield — clears the field and persists state before sleeping, so a crash mid-sleep cannot replay the same yield
- sleeps in-process `min(seconds, deadline_at - now, installed_hook_timeout - safety_margin)`
- falls through to the normal evaluator launch exactly once after the sleep — one Codex `gpt-5.4` `xhigh` pass at the end of the wait instead of one per short poll turn

**What the parent does NOT do:**

- does not poll `date` / `ls` / `tail` in a tight loop and end the turn naturally between each poll — every natural turn-end pays a fresh evaluator child
- does not self-declare `blocked` because the wait feels expensive or the evaluator is costly; that is forbidden by SKILL.md's **No invented budgets** rule and `skills/_shared/controller-contract.md` §No invented budgets
- does not invent a cadence — `continue_mode: wait_recheck` requires user-armed `interval_seconds` in `raw_requirements`, which this ask does not contain
- does not edit `raw_requirements`, `required_skill_audits[].status`, or either hash field (the runner would clear state on mutation)

**Sizing the `seconds:` value:** pick a window that beats the cost of an evaluator run for this wait. A good default is "expected wall-clock to the next meaningful marker change" (benchmark ETA ~10 min → `seconds: 600`). If the wait outlasts one window, arm another `sleep_for` on the next pass; per `skills/_shared/controller-contract.md` §Choosing the yield kind, detached jobs of any wall-clock length (hours, days) stay on the `sleep_for` track as long as the check is automatable. The hook clamps `seconds` into `min(seconds, deadline_at - now, installed_hook_timeout - safety_margin)`, so oversizing is safe.

**Stop condition:** evaluator returns `clean` only when the marker landed, benchmarks were copied into `diagnostics/handset_eval_opt_<DATE>/`, semantic parity ran, INVESTIGATION.md was updated with measured 2p/3p results, and the commit-or-revert decision is in the repo with reproducible evidence pointers.

## Anti-case: pure wait-until-true (use `$delay-poll` instead)

**Ask:** "Wait until the remote branch `feature/x` is pushed, then pull it and integrate."

This is a pure wait-until-true request with no free-form requirement set, no external-audit contract, and no named skill audit. The canonical owner is `$delay-poll`:

- `delay-poll` already has literal `check_prompt`/`resume_prompt` preservation, interval-based waiting inside the installed Stop hook, and clean resume-on-true semantics.
- Routing this request to `arch-loop` would add an unnecessary external Codex evaluator and a heavier controller state for a purpose `delay-poll` already covers.

`arch-loop` should route the user to `$delay-poll` (by invocation guidance, not by silently re-armig the wrong controller). If the user explicitly asks for `$arch-loop` for a pure wait or names a real external-audit requirement, `arch-loop` may own it. Otherwise prefer the narrower skill.

## Anti-case: canonical full-arch plan (use `$arch-step implement-loop` instead)

**Ask:** "Run the implement-loop against `docs/SOMETHING.md` until the plan's Section 7 frontier is clean and the implementation audit is clean."

This is the canonical full-arch plan flow. `$arch-step implement-loop` (also callable as `$arch-step auto-implement`) already owns:

- the `implement`/`audit-implementation` cycle
- the fresh Stop-hook-owned implementation audit
- the approved Section 7 frontier as the authoritative scope
- the `Use $arch-docs` handoff after a clean audit

`arch-loop` should route the user to `$arch-step implement-loop` and not attempt to be a second full-arch controller.

## What these examples intentionally omit

- Exact evaluator JSON output (see `evaluator-prompt.md` for the contract).
- State file shape and write ownership (see `controller-contract.md`).
- Cap/cadence parser phrase families and ambiguity rules (see `cap-extraction.md`).
- Specialized loops that already own narrower workflows (`$audit-loop`, `$comment-loop`, `$audit-loop-sim`, `$arch-docs auto`, `$goal-loop`).
- Exact `seconds:` sizing math for `requested_yield: sleep_for`. Example 5 shows the shape and rubric; the actual value is a context judgment call by the parent, bounded by the hook's own clamp.
