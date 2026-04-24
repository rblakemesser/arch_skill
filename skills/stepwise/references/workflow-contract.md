# Workflow contract: five phases

The skill runs five phases in order. Each phase has concrete inputs, concrete
outputs, and concrete failure modes. Judgment lives in Stepwise's prose
reasoning. Determinism lives in `scripts/run_stepwise.py`.

Across every phase, apply `unblocking.md`: if the current role knows a safe,
bounded repair that preserves the confirmed manifest and role boundaries, do
that repair before asking the user. Stop discipline applies after known
unblocks and the resolved repair limit are exhausted.

## Phase 1 - Intake and interpretation

**Inputs**

- Verbatim user prompt.
- Current working directory, treated as the orchestrator repo root.
- The orchestrator's own session id, used only for run-directory collision
  safety.

**Outputs** written into `state.json`

- `raw_instructions` and `raw_instructions_sha256`.
- `target_repo_path`, absolute and resolved.
- `target_process`.
- `profile`: `strict`, `balanced`, or `lenient`.
- `forced_checks`.
- `stop_discipline`: `halt_and_ask`, `skip_and_continue`, or
  `escalate_to_user`.
- `per_step_retry_cap`, default 5 unless the user names a concrete bound.
- `execution`, including base worker/critic runtime/model/effort and any
  unresolved execution preferences.

**Where judgment lives**

The agent reads the prompt, resolves profile/checks/stop posture, resolves the
target repo, parses execution defaults and preferences, and asks one
consolidated question if required defaults are missing.

**Where determinism lives**

Run-directory creation, hash computation, and initial state file writing.

**Failure modes**

- Target repo cannot be resolved -> ask.
- Genuinely contradictory signals with no tie-breaker -> ask.
- Missing required execution defaults -> ask once.
- No process or inferable target intent -> ask.

Do not proceed to Phase 2 with unresolved gaps.

## Phase 2 - Process grounding and manifest drafting

**Inputs**

- State from Phase 1.

**Outputs**

- `doctrine_paths`, the concrete target-repo files workers and critics should
  read.
- `manifest.json`, the full Step Manifest per `manifest-schema.md`, including
  resolved execution blocks.

**Where judgment lives**

The agent reads target doctrine and drafts the manifest. The manifest must name
real artifacts and real owner entrypoints. If the doctrine is ambiguous, ask
instead of guessing. After drafting steps, resolve execution preferences using
`execution-routing.md`: feasibility, hard doctrine, explicit step preference,
semantic preference, then defaults.

**Where determinism lives**

Reading files, writing `manifest.json`, and persisting the execution hash.

**Failure modes**

- Named process does not exist in target doctrine -> ask.
- A sub-step has no verifiable artifact -> ask.
- Doctrine contradicts itself -> surface the contradiction.
- Execution preference matches no steps, conflicts with hard doctrine, or is
  too ambiguous -> surface before execution.
- A prompt, descriptor, or run-directory artifact is malformed but intended
  meaning is clear -> repair the run-directory artifact, record it, continue.

## Phase 3 - Plan confirmation

**Inputs**

- Phase 1 interpretation.
- Phase 2 manifest.

**Outputs**

- User confirmation or user adjustments.

The printed plan always includes the resolved execution table. Lenient profile
prints and proceeds; strict and balanced pause according to
`strictness-profiles.md`.

If the user rejects the plan, re-enter the phase that generated the rejected
part. Do not patch the manifest in place without re-grounding.

## Phase 4 - Step execution loop

For each step `n` from 1 to N:

1. Spawn a worker sub-session.
2. Spawn an observational critic.
3. If the critic passes, advance.
4. If the critic fails or abstains with inspectable evidence, run
   `diagnose-and-repair.md`.

A repair bounce is one operational repair prompt sent to a worker session plus
the critic rejudgement of that attempt. The first worker attempt does not count
against the repair limit. Diagnostic read-only turns do not consume repair
bounces.

### 4a. Spawn worker sub-session

**Inputs**

- StepDescriptor for step `n`.
- Resolved worker runtime/model/effort.
- `target_repo_path`.

**Actions**

- Compose the initial prompt per `session-prompt-contracts.md`.
- Build the invocation per `session-resume.md`.
- Run the subprocess with stdin closed.
- Capture exit code, stdout, final output file, stream log, and session id.
- Write all artifacts to `steps/<n>/try-1/`, including `prompt.md`.

**Failure modes**

- Subprocess crashes -> treat as a failed attempt with crash evidence, subject
  to the same diagnose-and-repair protocol unless the crash is a known
  orchestration defect.
- Session id not captured -> inspect the raw stream for known Claude/Codex id
  shapes before marking `session_id.txt` as `UNRECOVERABLE`.

### 4b. Spawn critic sub-session

**Inputs**

- StepDescriptor, doctrine paths, worker artifacts, transcript, active checks,
  and `critic_execution`.

**Actions**

- Render the observation-only critic prompt per `critic-prompt.md`.
- Build the invocation per `session-resume.md`.
- Run the critic as a fresh ephemeral subprocess.
- Parse and semantically validate the observational StepVerdict.
- Write prompt, invocation, raw output, parsed verdict, and validation errors
  under `steps/<n>/try-<k>/critic/`.

**Failure modes**

- Known orchestration defect such as prompt rendering, schema shape, command
  flag drift, or missing run-directory file -> repair that run-directory
  defect, record it, and retry the critic once.
- Unknown runtime crash -> retry the critic once; on repeat, record blocked and
  apply stop discipline.
- Structured output parse failure -> do not guess. Repair only known bounded
  schema/rendering issues.
- Critic output fails semantic validation -> record
  `verdict.validation_errors.json`. Do not coerce invalid verdicts into
  pass/fail.
- Critic writes to disk -> fail loud. Critics are read-only by contract.

### 4c. Diagnose and repair

The critic owns pass/fail observation. The orchestrator owns the diagnostic
conversation, the decision of where in the chain to repair, and the repair
prompt itself. The worker owns target-repo changes. The run directory holds
every artifact of that separation.

On `verdict=fail` or inspectable `verdict=abstain`:

1. Write diagnostic intake from critic evidence, transcript, artifacts, owner
   doctrine, manifest, and applicable accepted learnings.
2. Resume the relevant worker session read-only with the diagnostic prompt.
3. Compare the answer to evidence in hand.
4. Continue diagnostic conversation, walking upstream when inputs are
   implicated, until root cause is located, owner doctrine is genuinely
   ambiguous, or the diagnostic turn cap is exhausted.
5. If root cause is local or upstream and repair bounces remain for that
   session, author a source-tagged repair prompt and resume the root-cause
   session operationally.
6. Run a fresh critic against the repaired attempt.
7. If an upstream repair passes, respawn downstream steps fresh. Do not resume
   downstream sessions that were built on the broken upstream artifact.
8. If the repair fails, re-enter this same protocol.

Halt when:

- The relevant session's repair bounces are exhausted.
- The diagnostic turn cap is exhausted without convergence.
- The owner doctrine is genuinely ambiguous and a user decision is required.
- The expected evidence is unavailable and no bounded unblock remains.

After halt, apply `stop_discipline`.

## Phase 5 - Report

**Inputs**

- `state.json`, `manifest.json`, per-step verdicts, diagnostic records, and
  learning records.

**Outputs**

- `report.md` in the run directory.
- A short console summary naming run id, status table, notable observations,
  diagnostic root cause if halted, applied learnings, candidate learnings, and
  pending work.

Do not use certification language. Report evidence and status.
