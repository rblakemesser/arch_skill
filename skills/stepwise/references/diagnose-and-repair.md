# Diagnose and repair

This is the single failure-handling protocol for Stepwise. It runs on every
critic `fail` and every critic `abstain` whose reason points at inspectable
evidence. There are no alternate failure modes selected by shortcuts.

## Invariant

Between the critic saying "fail" and any worker receiving an operational repair
prompt, Stepwise holds diagnostic conversation with the agents involved in the
chain break, reasons about where the break actually lives, and authors a repair
prompt that cites its sources.

The critic's verdict is evidence. The worker's answer is evidence. The
manifest is evidence. Owner doctrine is evidence. None of them is the repair
prompt. The repair prompt is Stepwise's synthesis, grounded in those sources.

## Protocol

1. **Intake**
   - Read the critic observation and evidence.
   - Read the worker transcript, artifacts, manifest descriptor, owner doctrine,
     and any declared support needed to understand the failed contract.
   - Query accepted learnings whose structural scope plausibly matches. Record
     which apply and which near-misses do not.
   - Write `diagnostic/intake.md` naming the suspected broken link in the
     truthful chain.

2. **Diagnostic conversation**
   - Pick the session most likely to hold the break. First pass usually starts
     with the failing worker.
   - Resume that session read-only with the diagnostic prompt from
     `session-prompt-contracts.md`.
   - Write the prompt and response into `diagnostic/turn-*.prompt.md` and
     `diagnostic/turn-*.response.md`.
   - Compare the answer to evidence in hand.
   - Continue until one of these is true:
     - Root cause is local and the repair shape is clear.
     - Root cause is upstream and the next session to question is known.
     - Owner doctrine is genuinely ambiguous.
     - The diagnostic turn cap is exhausted.

3. **Upstream traversal**
   - If the worker says an input was already wrong, read the manifest to find
     the earlier step whose expected artifact produced that input.
   - Resume that upstream session with the same diagnostic prompt shape.
   - If the upstream worker confirms its output was wrong, repair upstream.
   - If the upstream output was correct but the downstream received something
     else, inspect intermediate handoff steps.
   - Continue walking the chain until the earliest broken link is located.

4. **Repair authorship**
   - Write `diagnostic/root-cause.md` with the session that owns the repair, the
     evidence, the owner-doctrine clause, and any downstream sessions that must
     respawn fresh.
   - Author one repair prompt for the root-cause session.
   - Every numbered operational step carries a source tag:
     `[source: user]`, `[source: manifest]`, `[source: owner runbook]`,
     `[source: critic evidence]`, or `[source: confirmed diagnosis]`.
   - Delete any instruction that cannot be source-tagged.
   - Keep internal Stepwise vocabulary out of the worker-facing prompt.

5. **Repair execution**
   - Resume the root-cause session with the repair prompt.
   - This consumes one repair bounce on that session.
   - Run a fresh critic against the repaired attempt.

6. **After rejudgement**
   - If the repaired step passes and it was upstream of the original failure,
     respawn downstream steps fresh from the confirmed manifest.
   - If the repaired step fails, re-enter this protocol from intake.
   - If repair bounces are exhausted, halt with the diagnostic record.

## Budgets

- `max_retries` / `per_step_retry_cap` is the operational repair-bounce budget
  for each session. Default is 5.
- Diagnostic read-only turns do not consume repair bounces.
- A single critic failure may use at most 10 diagnostic turns across all
  sessions. This is a sanity cap, not a routing shortcut.

If the diagnostic turn cap is exhausted, halt with the record. A failure that
cannot be located after 10 read-only turns is not safe to repair by invention.

## Halt conditions

Halt instead of repairing when:

- Owner doctrine is genuinely ambiguous and a user decision is required.
- The root-cause session has exhausted repair bounces.
- The diagnostic turn cap is exhausted.
- Required evidence is unavailable and no bounded unblock remains.
- Repair would require the worker to claim a timeline or proof event that did
  not happen.

## Downstream context hygiene

If an upstream session is repaired, every downstream step whose context depended
on the old upstream artifact must respawn fresh. Do not resume downstream
sessions after upstream repair; their history was built on broken input.

## Learnings

Accepted learnings may shape intake and repair authorship only when their
applicability test matches and no contraindication applies. Record that
reasoning in `diagnostic/applicable-learnings.md`.

Candidate learnings are never binding. Learnings never appear as hidden
worker-facing doctrine. If a learning matters, translate it into an
owner-doctrine-backed instruction or leave it out of the worker prompt.
