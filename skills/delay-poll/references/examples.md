# delay-poll Examples

Canonical asks, their parsed caps, and resulting state snapshots. Use these
to sanity-check arm-time behavior; they also document what the Stop hook
expects to find on every hook read.

## Example 1: poll for a remote commit every 30 minutes, 24-hour cap

**User ask**

> Keep checking every 30 minutes whether branch `feature/x` has been pushed
> to origin. When it has, pull it and integrate it into my working branch.
> Give up after 24 hours.

**Parsed caps**

- `interval_seconds: 1800` (from "every 30 minutes")
- `deadline_at = armed_at + 86400` (from "Give up after 24 hours")

**State snapshot after arm**

```json
{
  "version": 2,
  "command": "delay-poll",
  "session_id": "e1f3c0b9",
  "interval_seconds": 1800,
  "armed_at": 1770000000,
  "deadline_at": 1770086400,
  "check_prompt": "Check whether branch feature/x has been pushed to origin by inspecting the remote.",
  "check_prompt_hash": "<sha256 of check_prompt>",
  "resume_prompt": "Pull branch feature/x and integrate it into the active working branch.",
  "resume_prompt_hash": "<sha256 of resume_prompt>",
  "cap_evidence": [
    {"type": "interval", "source_text": "every 30 minutes", "normalized": "1800s"},
    {"type": "deadline", "source_text": "Give up after 24 hours", "normalized": "86400s"}
  ],
  "attempt_count": 0,
  "last_check_at": null,
  "last_summary": ""
}
```

## Example 2: hourly poll with explicit shorter cap

**User ask**

> Every hour check whether the staging deploy from PR #421 has gone green.
> Cap at 6 hours. When green, resume smoke-testing.

**Parsed caps**

- `interval_seconds: 3600`
- `deadline_at = armed_at + 21600`

**State snapshot**

```json
{
  "version": 2,
  "interval_seconds": 3600,
  "deadline_at_minus_armed_at": 21600,
  "check_prompt": "Check whether the staging deploy from PR #421 is green.",
  "resume_prompt": "Resume smoke-testing against the staging deploy for PR #421.",
  "cap_evidence": [
    {"type": "interval", "source_text": "Every hour", "normalized": "3600s"},
    {"type": "deadline", "source_text": "Cap at 6 hours", "normalized": "21600s"}
  ]
}
```

Key fields elided; the shape is the same as Example 1.

## Example 3: condition already true — do not arm

**User ask**

> Every 15 minutes check whether migration `0042_user_schema` has been
> applied to prod. When it has, resume the follow-up backfill script.

**Immediate grounded check**

The parent pass runs one read-only check and finds the migration has
already landed. The parent continues from the same turn with the resume
prompt and the latest summary; **no state file is written**. The
conditional-arm deviation (documented in `skills/_shared/controller-contract.md`)
exists precisely for this case.

## Example 4: interval exceeds installed hook timeout — loud reject

**User ask**

> Every 26 hours check whether the monthly billing report has been
> generated.

**Outcome**

Arm fails loud. The parent pass must not write state because
`interval_seconds = 93600 >= 90000` (installed Stop-hook timeout). The
`delay-poll` SKILL says plainly: shorten the interval or use a different
workflow. Do not silently clamp.

## Example 5: parent edits check_prompt after arm — mutation detected

State was armed at version 2 with `check_prompt_hash` pinned. A later
parent turn re-reads state and edits `check_prompt` to narrow the
condition. On the next Stop hook entry, the recomputed hash no longer
matches `check_prompt_hash`. The hook clears state with
`delay-poll check_prompt mutation detected`. The parent must re-arm with
the original literal condition; it cannot silently reshape the wait.
