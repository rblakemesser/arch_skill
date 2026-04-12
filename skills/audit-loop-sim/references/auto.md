# `auto` Mode

## Goal

Run repeated strong real-app automation audit passes until a fresh review says no credible major unresolved automation risk remains or the loop is genuinely blocked.

## What `auto` does

- verifies the Codex runtime preflight
- resolves `SESSION_ID` from `CODEX_THREAD_ID` and creates or refreshes `.codex/audit-loop-sim-state.<SESSION_ID>.json`
- runs one truthful `run` pass
- lets the installed Stop hook launch a fresh `review` pass
- continues only while the review verdict remains `CONTINUE`

User-facing invocation is just `Use $audit-loop-sim auto`. If real hook support is absent or disabled, fail loud instead of pretending prompt-only repetition is the same feature.
Do not run the Stop hook yourself. After `auto` is armed, just end the turn and let Codex run the installed Stop hook.

## Required runtime preflight

Before arming the controller, verify all of these:

- Codex runtime is the active host
- the installed suite controller runner exists under `~/.agents/skills/arch-step/scripts/`
- the installed arch_skill-managed Codex Stop hook is present
- `codex features list` shows `codex_hooks` enabled

If any check fails, name the broken prerequisite and stop.

## State file contract

Resolve `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/audit-loop-sim-state.<SESSION_ID>.json` before the first `run` pass.

Minimal shape:

```json
{
  "version": 1,
  "command": "auto",
  "session_id": "<SESSION_ID>",
  "ledger_path": "_audit_sim_ledger.md",
  "gitignore_created": false,
  "gitignore_entry_added": true
}
```

Lifecycle:

- create or refresh it after preflight and before the first `run`
- keep it armed while verdicts are `CONTINUE`
- delete it before stopping on `BLOCKED`
- delete it on `CLEAN` before removing the ledger and `.gitignore` entry

## Hard rules

- `auto` is one controller command, not a suggestion to keep winging it forever
- `auto` must not degrade into a tiny-safe-fix treadmill
- the review pass must run in fresh context
- `review` stays docs-only
- do not continue after `BLOCKED`
- do not continue after `CLEAN`
- do not auto-commit findings
- use the repo's sanctioned simulator, emulator, and automation surfaces instead of inventing a second runtime story

## Hook behavior

When the loop is armed, the installed suite Stop hook should:

1. no-op when no active audit-loop-sim state matches the current session
2. launch `codex exec --ephemeral --disable codex_hooks` with `$audit-loop-sim review`
3. read the controller verdict from `_audit_sim_ledger.md`
4. on `CONTINUE`, keep state armed and continue with the next `$audit-loop-sim` pass
5. on `BLOCKED`, clear state and stop honestly
6. on `CLEAN`, clear state, delete `_audit_sim_ledger.md`, and remove the `.gitignore` entry
