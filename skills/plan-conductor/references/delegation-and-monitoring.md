# Delegation And Monitoring

Every dispatch maps onto `$agent-delegate` with no new machinery. That skill
owns invocation mechanics — command shapes, run directories, session capture,
hook suppression, model/effort resolution, and failure handling. This
reference only maps conductor situations onto its modes and defines the
conductor's monitoring and token-economy posture.

## Mode Mapping

- **Initial slice dispatch → `fresh-resumable`** (agent-delegate's default).
  The child starts cold from disk plus the slice contract. Record the run
  directory and captured session id in the conductor log.
- **Send-back / repair → `resume`** with the exact captured session id, same
  runtime, and a new bounded findings prompt. The session already holds the
  slice context — that continuity is exactly why the resumable path exists.
  Never `--continue`, never "latest," never cross-runtime.
- **Respawn → new `fresh-resumable`** child with a sharpened brief. Use when
  the session is unhealthy (caps in the audit reference), the repair moved to
  a different owner surface, or a cold implementation view is needed.
- **Cold verifier → `fresh-one-shot`**, final gate only. Statelessness is the
  feature: no conductor context, no resume, just refutation from code
  reality.
- **Parallel waves** use agent-delegate's parallel group path: one group
  directory, one ordinary child run directory per worker, every child briefed
  that siblings may be editing the repo, must not revert unfamiliar changes,
  and must report actual conflicts with file evidence rather than resolving
  them by guesswork.

## Worker Identity

The user supplies worker runtime/model/effort at kickoff; ask one
consolidated question if missing, and never pick a favorite default. The
intended fleet is "smart but not the smartest" — fast, cheap implementation
models — while the conductor runs on the expensive model. Announce the
raw-to-resolved model mapping before the first launch, per agent-delegate's
resolution doctrine. Do not silently change runtime, model, or effort
mid-run; if a worker model is clearly failing the work, that is a user
decision, not a silent substitution.

## Patient Monitoring

- Prefer waiting on process completion over polling at all: launch the
  delegate command and consume results when it exits. Where the host only
  supports polling, check at a **five-minute-or-slower cadence**.
- When checking, read only cheap signals: process liveness, `stderr.log`
  size, file mtimes, `git status --short`. **Never stream `events.jsonl`
  into conductor context during normal operation.** It is a diagnostic
  artifact for post-mortems on non-zero exits or malformed output.
- **Quiet is not stuck.** Big slices, high-effort thinking, long tests,
  installs, and simulators go silent for minutes. Normal delegated work takes
  5+ minutes; broad slices at high effort reasonably take 20-40 minutes.
  Roughly five quiet minutes starts *inspection*, not replacement. Replace or
  respawn only on evidence the worker is stuck, harmful, or dead — never on
  silence alone.

## Conductor Token Economy

The conductor's context is the most expensive resource in the run. Explicit
spending rules:

- The plan gets one full read, at intake. Afterwards re-read only the
  anchored sections named by the slice under audit.
- The conductor log is the durable memory. Never re-derive what the log
  records; after interruption or compaction, rebuild from log plus plan,
  never from chat history.
- Evidence intake is layered, cheapest first: (1) the worker's status footer
  from `final.txt` — read solely to enumerate the claims to falsify, never as
  the account of what happened; (2) `git status` / `git diff --stat` to check
  the `CHANGED FILES` and `DELETES EXECUTED` claims against reality; (3)
  targeted `git diff -- <paths>` hunks, file reads, and authority-path traces
  for the actual audit. Never "read the repo to see what happened," and never
  read worker transcripts. Cheap intake bounds token spend; it never lowers
  the audit bar — the burden of proof stays on the worker's output
  (`references/audit-and-send-back.md`).
- Batch findings into one resume prompt per repair round, not one message per
  nit. Each round-trip costs conductor context and wall clock.
- All proof runs are delegated. The conductor reads proof results; it does
  not produce them.
- Chat output stays compact: one small status table per wave; detail goes to
  the log.
