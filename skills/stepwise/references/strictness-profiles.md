# Strictness and repair policy

Phase 1 resolves four things from the user's prompt:

- `profile`: `strict`, `balanced`, or `lenient`.
- `forced_checks`: critic checks the user specifically cares about.
- `stop_discipline`: what to do after diagnosis cannot produce a permitted
  repair or after repair bounces are exhausted.
- `per_step_retry_cap`: how many operational repair bounces a broken session
  gets.

Announce all four before Phase 2.

## Repair limit

Default to **5 repair bounces per broken session**.

A repair bounce is one operational repair prompt sent to a worker session plus
the critic's rejudgement of that repaired attempt. The first worker attempt
does not count. Diagnostic read-only conversations do not count.

Use a different number only when the prompt gives a concrete maximum in
ordinary language. "Up to three times" means 3 repair bounces. "No retries"
means 0 repair bounces. If the user speaks generally about persistence or
impatience without naming a concrete maximum, keep the default 5 and announce
it.

Strict, balanced, and lenient do not change the repair limit. Strictness
changes critic posture and stop behavior, not repair-bounce count.

Store the resolved limit in `per_step_retry_cap` and copy it into each step's
`max_retries`.

## Profiles

### `strict`

The user wants the process followed exactly.

- Stop discipline: `halt_and_ask`.
- Checks run: all five checks.
- Critic posture: adversarial. Prefer fail-on-ambiguity over pass-on-hope.

Strict still repairs known orchestration defects before asking. It does not
permit fabricated proof or silent third repairs past the resolved limit.

### `balanced`

The user wants the process followed with reasonable tolerance for minor
recoveries.

- Stop discipline: `halt_and_ask`.
- Checks run: `artifact_exists`, `no_fabrication`,
  `skill_order_adherence`.
- Critic posture: rigorous. Require evidence; tolerate imperfect form.

Balanced is the default when the user does not speak strongly either way.

### `lenient`

The user wants completion more than process purity. Hallucination still fails.

- Stop discipline: `skip_and_continue`.
- Checks run: `artifact_exists`, `no_fabrication`.
- Critic posture: pragmatic. Fail on fabrication and missing artifacts. Do not
  fail on style or ordering unless the user forced that check.

Downstream steps run only when the manifest permits meaningful continuation
after a skipped step.

## Stop discipline

Stop discipline applies only after known unblocks, diagnosis, and permitted
repair bounces are exhausted.

- `halt_and_ask`: mark the step blocked, stop the loop, report root cause and
  pending work.
- `skip_and_continue`: mark the step skipped, continue only if later steps can
  run meaningfully without its artifact.
- `escalate_to_user`: print the diagnostic record and ask the user whether to
  halt or skip this step.

There is no separate upstream-repair stop discipline. Upstream traversal is
part of the normal diagnose-and-repair protocol whenever evidence points to bad
input.

## Forced checks

Forced checks override the profile's default check set for that check.

- "no fabrication" / "no made-up steps" -> force `no_fabrication`.
- "strictly in skill order" / "follow the skill order" -> force
  `skill_order_adherence`.
- "every sub-step" / "no skipping any step" -> force `no_substep_skipped`.
- "as the doctrine says" / "in the order the SKILL.md lists" -> force
  `doctrine_quote_fidelity`.

Example: a lenient prompt that also says "strictly in skill order" keeps
lenient stop discipline, but `skill_order_adherence` runs on every step and a
violation fails the step.

## When to ask

Ask one clarifying question when:

- Two clear signals point at opposite profiles and no ordering cue resolves
  them.
- The user requires a specific repair limit but gives no concrete maximum.
- The target repo or target process cannot be resolved.
- The user asks for strict process enforcement, but the named process has no
  declared sub-steps or verifiable artifacts.

Do not ask when the only uncertainty is vague retry patience. Keep the default
5 repair bounces and announce it.

## Announcement shape

```text
Interpreting:
- Profile: strict (from "strict usage")
- Forced checks: skill_order_adherence (from "strictly according to the skill order"), no_fabrication (from "no fabrication")
- Broken-step repair limit: 5 operational repair bounces
- Diagnostic turn cap: 10 read-only turns per critic failure
- On exhaustion: halt_and_ask
```
