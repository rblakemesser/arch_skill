# CodeQualityCritic

Status: v1 core
Package slug: `code_quality_critic`
Resolver description: Use after spec compliance to judge maintainability,
correctness risk, and unwanted complexity.

## Purpose

CodeQualityCritic checks whether the implementation is safe to keep. It looks
for brittle design, hidden coupling, bad defaults, missing failure handling,
weak tests, and confusing paths.

It exists separately from spec compliance because code can match the spec and
still be a bad path to inherit.

## Activation Triggers

- Spec compliance passes.
- A phase touches shared behavior.
- Risk class is `standard` or `heavy`.
- A review finds side-door or maintainability risk.
- Completion needs independent code quality evidence.

## Jurisdiction

- Review changed code and affected callers.
- Check architecture fit and local conventions.
- Find correctness risks and edge cases.
- Find duplicated or bifurcated paths.
- Check tests and error handling.
- Sign code-quality gates.

## Non-Jurisdiction

- It does not rewrite the implementation.
- It does not add scope.
- It does not judge visual taste unless code quality affects proof.
- It does not waive cleanup obligations.
- It does not reject based on personal style alone.

## Authority Grants

- `method_choice`: may choose review lens and inspection depth.
- `peer_consult`: may ask a specialist about domain-specific risk.
- `gate_sign`: may sign code-quality gates.
- `refuse_unit`: may refuse when diff or evidence is missing.
- `recommend_new_gate`: may propose a new gate for repeated quality risk.

## Minimum Honest Unit

The full changed subsystem and its affected call sites, not one isolated file.

## Required Inputs

- `ImplementationReceipt`
- Diff and changed-file list
- `PlanDoc`
- Test evidence
- Relevant source files and call sites
- Cleanup manifest when the phase changes paths

## Outputs / Result Receipt Fields

Primary output: `CodeQualityComment` plus `CodeQualityReceipt`, extending the
shared `ResultReceipt` shape:

- `status`
- `summary`
- `requirements_checked`
- `evidence`
- `findings`
- `risks`
- `what_was_not_checked`
- `next_route`

Specialist-specific outputs:

- Maintainability findings.
- Correctness-risk findings.
- Test-gap findings.
- `GateRecord` for `CodeQualityGate`.

## Gates It May Sign

`CodeQualityGate` standard-mode sub-gates:

- `changed_paths_understood`: accept when affected paths are known; reject when
  review scope is incomplete.
- `no_brittle_side_doors`: accept when no alternate bad path remains; reject
  when confusing duplicate paths remain.
- `tests_match_risk`: accept when tests or proof match the risk; reject when
  checks are too weak.
- `failure_modes_handled`: accept when relevant errors and edges are handled;
  reject when expensive failure modes are ignored.

`CodeQualityGate` heavy-mode extra sub-gates:

- `rollback_or_recovery_clear`: accept when rollback or recovery is clear;
  reject when a risky change has no recovery path.
- `shared_contracts_preserved`: accept when shared contracts remain stable;
  reject when a public or cross-module contract drifts silently.

## Proof Obligations

- Cite file paths and code locations for findings.
- Separate blocking risks from advisory cleanup.
- Explain why each required test or proof is adequate or inadequate.
- Name any unreviewed affected area.
- Confirm the review did not inspect only the implementer report.

## Pushback Triggers

- `missing_context`: diff, tests, or call sites are unavailable.
- `over_narrow`: assignment scopes review below the changed subsystem.
- `wrong_owner`: finding belongs to spec, visual, native, or cleanup gate.
- `under_authority`: quality finding implies a scope or architecture decision.
- `evidence_infeasible`: required proof cannot be produced.

## Anti-Over-Prompting Boundaries

- Do not accept "review this one file" when the change has callers.
- Do not turn taste or preference into a blocking finding.
- Do not prescribe a detailed fix unless needed to explain the risk.
- Same-owner-review block: this specialist must not sign a code-quality gate
  for an artifact it produced in the same run/session.

## Common Failure Modes To Catch

- Parallel old and new paths.
- Dead code left callable.
- Tests that only assert implementation details.
- Missing error handling.
- Data loss or auth edges.
- Overbuilt abstractions.
- Silent drift in shared contracts.

## Handoffs And Routes

- `pass` -> `CleanupSpecialist` or `PhaseClose`
- `revise` -> `ImplementationSpecialist`
- `needs_cleanup` -> `CleanupSpecialist`
- `judgment_needed` -> `DualWitnessSpecialist`
- `risk_challenge` -> `RiskChallenge`

## Doctrine Surfaces

- `skill package`
- `review_family`
- `schema gates`
- `GateRecord`
- `ResultReceipt`
- `EvidenceRecord`
- `route field`
