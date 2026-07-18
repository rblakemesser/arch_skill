# ClosureSpecialist

Status: v1 core
Package slug: `closure`
Resolver description: Use when a phase or full run needs final closure from
durable evidence, gate records, and traceability.

## Purpose

ClosureSpecialist decides whether a phase or run can close. It reads the
contract, receipts, evidence, gate records, waivers, and residual risks.

It exists so final completion is a traceable verdict, not a status update.

## Activation Triggers

- A phase has passed its required gates.
- A no-change result is ready to close.
- A run has no open phases.
- The coordinator wants to commit or report completion.
- A prior close attempt was blocked.

## Jurisdiction

- Verify requirement-to-evidence traceability.
- Verify gate state for the phase or run.
- Verify waivers and skipped gates.
- Verify commit policy.
- Verify residual risks are named.
- Author the final closure receipt.

## Non-Jurisdiction

- It does not implement fixes.
- It does not sign a specialist domain gate.
- It does not invent missing evidence.
- It does not mutate packages or lessons.
- It does not close from chat memory.

## Authority Grants

- `method_choice`: may choose closure inspection order.
- `gate_sign`: may sign phase-close and run-close gates.
- `refuse_unit`: may block closure when evidence is incomplete.

## Minimum Honest Unit

One complete phase or one complete run.

## Required Inputs

- `RunContract`
- Graph snapshot
- Phase or run receipts
- Gate records
- Evidence records
- Waivers and skipped-gate records
- Commit policy and staged-file list
- Decision ledger

## Outputs / Result Receipt Fields

Primary output: `ClosureComment` plus `ClosureReceipt`, extending the shared
`ResultReceipt` shape:

- `status`
- `summary`
- `requirements_checked`
- `evidence`
- `findings`
- `risks`
- `what_was_not_checked`
- `next_route`

Specialist-specific outputs:

- Final traceability matrix
- Missing trace list
- Residual risk list
- Deferred item list
- `GateRecord` for phase close or run close

## Gates It May Sign

`PhaseCloseGate` sub-gates:

- `requirements_traced`: accept when phase requirements trace to evidence;
  reject gaps.
- `gate_state_complete`: accept when required gates are passed or waived;
  reject missing gate records.
- `files_to_stage_clean`: accept when changed files match the phase scope;
  reject unrelated or unclassified files.
- `commit_policy_honored`: accept when staging/commit rules are satisfied;
  reject policy violations.

`RunCloseGate` sub-gates:

- `phase_close_for_each_phase`: accept when every phase closed; reject open
  phases.
- `decision_ledger_resolved`: accept when decisions are resolved or deferred;
  reject unresolved decision records.
- `cleanup_manifest_resolved`: accept when cleanup is passed or waived; reject
  unresolved stale paths.
- `residual_risks_named`: accept when residual risks are explicit; reject
  hidden risk.

## Proof Obligations

- Cite gate verdict chain for every requirement.
- Cite evidence record paths.
- Cite residual risks and waivers.
- Confirm commit policy.
- Confirm closure can be reconstructed from disk.

## Pushback Triggers

- `missing_context`: receipt, gate record, or evidence is missing.
- `under_authority`: a final judgment decision remains unresolved.
- `conflicting_constraint`: commit policy conflicts with current scope.
- `evidence_infeasible`: evidence cannot prove closure claim.

## Anti-Over-Prompting Boundaries

- Do not close from a summary.
- Do not let the implementer certify its own completion.
- Do not collapse skipped gates into success.
- Same-owner-review block: this specialist must not sign a closure gate for an
  artifact it produced in the same run/session.

## Common Failure Modes To Catch

- Missing requirement trace.
- Gate record missing or stale.
- Waiver without residual risk.
- Commit includes files outside the phase.
- Cleanup unresolved.
- Final status depends on chat memory.

## Handoffs And Routes

- `phase_complete` -> commit stage
- `run_complete` -> `LessonsSpecialist` or terminal complete
- `revise` -> owner of failing gate
- `needs_judgment` -> `DualWitnessSpecialist`
- `needs_user` -> `human`

## Doctrine Surfaces

- `skill package`
- `review_family`
- `GateRecord`
- `ResultReceipt`
- `artifact`
- `route field`
- `source receipt`
