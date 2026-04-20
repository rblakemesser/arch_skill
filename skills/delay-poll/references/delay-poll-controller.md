# delay-poll Controller

Core doctrine and lifecycle live in `skills/_shared/controller-contract.md`.
This file documents only the `delay-poll`-specific state schema, mutation
guards, cap validation, and conditional-arm deviation.

## Deviation

`delay-poll` runs one immediate grounded check against `check_prompt` before
arming. If the condition is already true, the parent continues from the same
turn without arming state. If the condition is still false, the parent arms
the controller and the Stop hook owns interval-polled re-checks until the
condition becomes true or the deadline elapses. This is documented in the
shared contract's Deviations section.

The conditional-arm exists to avoid a useless sleep when the user's condition
is already satisfied. It is not a license for the parent turn to disarm
later.

## Verdict source

The Stop hook launches a fresh read-only `check` child on the configured
interval:

- Codex: `codex exec --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox`
  with `$delay-poll check`
- Claude Code: `claude -p --settings '{"disableAllHooks":true}'` with
  `/delay-poll check`

The child returns JSON with `ready`, `summary`, and `evidence`. The Stop hook
parses:

- `ready: true` — the condition is satisfied. The hook clears state and
  resumes the parent thread with `resume_prompt` plus the latest `summary`.
- `ready: false` — the hook keeps state armed, updates `attempt_count`,
  `last_check_at`, and `last_summary`, sleeps `interval_seconds`, and
  re-checks.
- deadline elapsed — the hook clears state.

## State file schema

Paths (session-scoped, per the shared contract):

- Codex: `.codex/delay-poll-state.<SESSION_ID>.json`
- Claude Code: `.claude/arch_skill/delay-poll-state.<SESSION_ID>.json`

Minimum shape:

```json
{
  "version": 2,
  "command": "delay-poll",
  "session_id": "<SESSION_ID>",
  "interval_seconds": 1800,
  "armed_at": 1760000000,
  "deadline_at": 1760086400,
  "check_prompt": "Check whether branch blah has been fully pushed yet.",
  "check_prompt_hash": "d4f8c3...<sha256 hex>",
  "resume_prompt": "Pull branch blah and integrate it in.",
  "resume_prompt_hash": "91a0bd...<sha256 hex>",
  "cap_evidence": [
    {
      "type": "interval",
      "source_text": "every 30 minutes",
      "normalized": "1800s"
    },
    {
      "type": "deadline",
      "source_text": "for up to 24h",
      "normalized": "86400s"
    }
  ],
  "attempt_count": 1,
  "last_check_at": 1760000000,
  "last_summary": "Remote still does not show the expected pushed commit."
}
```

## Mutation guards

The arming parent pass computes two SHA-256 digests at arm time and writes
them into state:

- `check_prompt_hash = sha256(check_prompt)`
- `resume_prompt_hash = sha256(resume_prompt)`

Every hook read recomputes both digests. A mismatch clears state with
`check_prompt mutation detected` or `resume_prompt mutation detected`. The
parent pass must capture both strings literally at arm time; later turns
must not edit them.

State at version < 2 is rejected on sight (even if it looks syntactically
valid) because older schemas lacked the hash pins and hook-timeout-fit
validation. The hook clears and prompts for re-arm.

## Cap validation

At arm time the parent pass records `cap_evidence` as a list of
`{type, source_text, normalized}` entries covering the interval and the
deadline. The hook validates that:

- `interval_seconds > 0` and `interval_seconds < installed_hook_timeout`
- `deadline_at > armed_at` and `deadline_at - armed_at < installed_hook_timeout`

The installed-hook-timeout ceiling is shared with arch-loop
(`ARCH_LOOP_INSTALLED_HOOK_TIMEOUT_SECONDS = 90000`). Both checks are hard
rejects — the hook clears state with a loud message rather than silently
clamping, so the user knows the requested cap could never succeed inside the
host timeout.

## Writes matrix

Only the parent arm pass writes the pinned fields:

- `version`, `check_prompt`, `check_prompt_hash`, `resume_prompt`,
  `resume_prompt_hash`, `interval_seconds`, `deadline_at`, `armed_at`,
  `cap_evidence`.

Only the Stop hook writes the running-state fields:

- `attempt_count`, `last_check_at`, `last_summary`.

`requested_yield` is not valid on delay-poll state. The field belongs to
controllers with a parent work pass (arch-loop, arch-step, miniarch-step);
delay-poll only has a hook-owned poll loop. The validator hard-rejects and
clears state if it sees one.

## Continuation rule

- Keep `check_prompt` literal and explicit.
- Keep `resume_prompt` literal and action-ready.
- Default maximum wait window is 24 hours unless the user says otherwise.
- Later polling checks stay read-only. Mutation belongs only to the resumed
  main thread after the condition becomes true.
