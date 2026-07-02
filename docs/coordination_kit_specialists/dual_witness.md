# DualWitnessSpecialist

Status: later
Package slug: `dual_witness`
Resolver description: Use when an unexpected snag or high-judgment decision
needs two independent model reads and a recorded decision.

## Purpose

DualWitnessSpecialist resolves judgment-heavy problems with two independent
expert reads before convergence. It records the decision, rejected options, and
whether the plan must change.

It exists so the system does not invent a workaround on the fly when the right
answer needs deeper judgment.

## Activation Triggers

- Any specialist emits `under_authority`.
- Proof policy is disputed.
- Architecture or plan direction is contested.
- A tempting workaround appears.
- A specialist says the plan must change before implementation continues.
- User explicitly requests two-model judgment.

## Jurisdiction

- Run two independent reads from the same evidence bundle.
- Compare first-pass positions.
- Force convergence or name the smallest unresolved decision.
- Record rejected alternatives.
- Emit a decision artifact.
- Route to plan amendment, user, or implementation.

## Non-Jurisdiction

- It does not perform ordinary review.
- It does not edit implementation.
- It does not replace user approval for scope changes.
- It does not sign domain gates.
- It does not run for trivial factual checks.

## Authority Grants

- `method_choice`: may choose the witness dialogue shape.
- `sub_dispatch`: may run the two witness turns through typed receipts.
- `peer_consult`: may request domain evidence.
- `refuse_unit`: may block when evidence is insufficient.
- `recommend_new_gate`: may propose a missing decision gate.

## Minimum Honest Unit

One concrete decision with evidence, options, and consequences.

## Required Inputs

- Snag or pushback receipt.
- `RunContract`
- Relevant plan section.
- Evidence records.
- Source/reference document when required.
- Candidate options or the reason options are unknown.

## Outputs / Result Receipt Fields

Primary receipt: `DualWitnessReceipt`, extending the shared `ResultReceipt`
shape:

- `status`
- `summary`
- `requirements_checked`
- `evidence`
- `findings`
- `risks`
- `what_was_not_checked`
- `next_route`

Specialist-specific outputs:

- `JudgmentReceipt`
- Decision artifact in `DecisionLedger`
- Independent witness summaries
- Converged decision or unresolved question
- Required plan amendment route

## Gates It May Sign

`JudgmentResolutionGate` sub-gates when enabled:

- `independent_reads_complete`: accept when both witnesses formed first-pass
  views before seeing each other; reject one-sided or contaminated reads.
- `evidence_grounded`: accept when the decision cites real artifacts; reject
  unsupported opinion.
- `decision_scope_clear`: accept when the result says what changes; reject
  vague guidance.
- `plan_amendment_required_when_needed`: accept when plan changes are routed;
  reject implementation continuing on stale plan.

## Proof Obligations

- Preserve both independent first-pass positions.
- Name evidence each witness used.
- Name rejected alternatives.
- State the final decision or the exact unresolved question.
- State whether the plan must be amended before work resumes.

## Pushback Triggers

- `missing_context`: evidence bundle is incomplete.
- `evidence_infeasible`: required grounding source is missing and gate requires
  it.
- `under_authority`: decision belongs to the user.
- `over_narrow`: the framed decision hides a larger tradeoff.

## Anti-Over-Prompting Boundaries

- Do not let the coordinator ask for validation of its preferred workaround.
- Do not collapse two witnesses into one combined answer.
- Do not use this for ordinary lint or review.
- Same-owner-review block: this specialist must not sign a gate for a decision
  artifact it produced unless the graph routes review to a distinct signer.

## Common Failure Modes To Catch

- Expedient workaround chosen without research.
- Kitchen-sink compromise.
- Hidden scope change.
- Decision based on stale plan.
- One model's answer pasted as consensus.
- Unresolved decision disguised as implementation guidance.

## Handoffs And Routes

- `decision_recorded` -> `PlanSpecialist` for amendment or next stage
- `user_decision_needed` -> `human`
- `evidence_missing` -> `ContractAmendment`
- `resume_implementation` -> `ImplementationSpecialist`

## Doctrine Surfaces

- `skill package`
- `receipt`
- `artifact DecisionLedger`
- `SubDispatchRequest`
- `route field`
- `review` optional
