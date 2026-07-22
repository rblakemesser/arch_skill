# Aim Account Rotation For Codex

Shared mechanics for continuing Codex work across hard usage limits by
rotating the active `aim` account and resuming the exact same session. Any
skill that runs or supervises a Codex process may point here; the owning skill
keeps its own trigger signals (pane strings, `stderr.log` shapes) and its own
process mechanics (tmux keys, subprocess relaunch).

## aim facts

- `aim status` — pool summary; the `CODEX` block shows the live
  `active_label` and `account_id`.
- `aim status --accounts` — per-account `5h_used`, `5h_in` (reset), `wk_used`,
  `wk_in`, status, and flags.
- `aim codex use [label]` — rewrites `~/.codex/auth.json`. No label =
  round-robin auto-pick, which only weighs round-robin/5h and can land on a
  90%+-weekly account — pass an explicit `<label>` to control the choice.
- Prefer a `ready` account with low `5h_used` AND low `wk_used`. Skip accounts
  with `st=reauth` / `missing_credentials`, and skip any flagged `5h_full`.
- `aim`'s `5h_full` / 100% is a *leading* flag, not a hard block; codex
  commonly keeps working past it. Rotate on the runtime's real usage-limit
  signal, not on the percentage.
- Do not use the aim "Tend" path (`aim codex run --tend`) for rotation; drive
  it explicitly with `aim codex use` plus a manual restart.

## codex facts that make rotation work

- **Auth is cached at startup.** codex reads `~/.codex/auth.json` once at
  process start. Swapping the file mid-session does nothing until the process
  restarts. `aim codex use` ⇒ restart the codex process.
- **Resume appends to the same session.** `codex resume <SESSION_ID>` reopens
  the existing rollout file and appends; goal and history are preserved.
  Prefer the explicit id over `--last` so a stray newer session cannot be
  picked by mistake.
- Match the original launch shape on resume; the profile flag is
  global-before-subcommand in practice (`codex -p <profile> resume
  <SESSION_ID>`).
- The session id is in the newest file under
  `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*-<SESSION_ID>.jsonl` when it
  was not captured elsewhere.

## Core rotation sequence

1. **Confirm the limit is real.** A hard usage-limit signal or a dead
   process — never a lone transient reconnect, which self-heals.
2. **Pick and switch.** `aim status --accounts`, choose a healthy label,
   `aim codex use <label>`. Verify `aim status` shows the new `active_label`
   and `~/.codex/auth.json` `tokens.account_id` matches.
3. **Restart the codex process** through whatever mechanism owns it (tmux
   pane, subprocess relaunch). A live process never picks up the new auth.
4. **Resume the exact session** with the captured session id and the original
   launch shape.
5. **Verify it actually resumed work** on the new account — real progress
   signals, not an immediate re-limit.

## Pool-pressure caveat

Codex work often spawns its own children (`codex exec ...`, delegated
reviews). Children consume the same account pool and can rotate
`active_label` themselves. Re-read `aim status` at restart time and act on
whatever is currently active and healthy rather than assuming the last label
you set.
