# Coordinated Agent Standalone Architecture Plan

Status: architecture plan only. Do not implement from this document until the
plan-review gates pass.

Date: 2026-05-23.

Working package name: `coordination-kit`.

## 0. North Star

Build a standalone coordinator skill package for long-running coding-agent
projects. It must coordinate expert roles, preserve durable state, enforce
independent verification, and let new specialists plug in without changing the
coordinator runtime.

The coordinator must not depend on existing local workflow skills. It can learn
from prior usage research, but its runtime, contracts, graph, gates, and
specialist interface must stand alone.

The architecture follows Doctrine authoring practice:

- Thin runtime, fat skills.
- Typed truth over prose for anything downstream must trust.
- Load depth only when the active stage needs it.
- Keep always-on coordinator context small.
- Put reusable judgment in specialist packages and references.
- Put exact routing, gates, verdicts, receipts, artifacts, and graph edges in
  typed contracts.
- Emit source receipts and fail loud when contracts drift.
- Write prompts and docs in plain human language.

## 1. Non-Negotiables

- `coordination-kit` is standalone. No runtime dependency on any existing local
  skill package.
- The first version is one installable package with bundled starter
  specialists. Later specialists can split into independent packages because
  the manifest and receipt contracts are stable.
- The runtime is thin. It creates run folders, loads the compiled graph,
  dispatches packets, validates receipts, records state, and routes by typed
  route fields.
- The runtime does not own expert judgment, proof rules, domain methods, review
  gates, or taste.
- Experts get outcomes, jurisdiction, authority, context, constraints, and
  proof obligations. They do not get coordinator-written microtasks.
- Pushback is a first-class result, not a failure to comply.
- Same-agent self-verification is structurally blocked.
- No-code/no-change success is a valid result.
- Cleanup is part of the contract. In-scope bad paths and stale defaults are
  deleted or explicitly protected by typed rows.
- User-owned dirty work is protected. Ambiguous deletion blocks until the path
  is classified.
- Every non-trivial completion claim must trace from requirement to dispatch to
  result receipt to evidence to gate record.

## 2. Doctrine Interpretation

Doctrine is the authoring layer, not the runtime. It should produce the
contracts and prompt packages the runtime consumes.

Use Doctrine surfaces this way:

- `skill package`: emits the coordinator package and bundled specialists.
- `host_contract`: binds shared run inputs and emitted receipts once per
  specialist.
- `output schema`: owns machine-readable final responses and receipts.
- `route field`: owns next-owner choices; prose route text is not trusted.
- `review` and `review_family`: own gate verdicts and per-gate failure detail.
- `schema`: owns reusable gate contracts, evidence records, role manifests, and
  closed contract shapes.
- `enum`: owns closed vocabularies such as risk class, result status, gate
  state, cleanup posture, pushback codes, evidence provenance, assignment kind,
  and role authority.
- `table`: owns repeated typed rows such as cleanup overrides and native
  platform proof matrix rows.
- `receipt`: owns durable handoff facts between stages.
- `artifact`: names durable files and evidence bundles.
- `stage`, `skill_flow`, and `skill_graph`: own graph shape, routes, policies,
  emitted views, and graph source receipt.

Do not hide machine-trustable facts in prose. Prose is for judgment, domain
reasoning, examples, and taste.

## 3. Architecture

The system has three layers.

### Thin Runtime

The runtime is a small coordinator executable or command layer. It owns:

- Creating `.coord/runs/<RUN-ID>/`.
- Loading the compiled graph snapshot for the run.
- Loading run contract and role manifests.
- Validating dispatch packets before send.
- Starting specialist turns.
- Persisting dispatches, receipts, evidence records, gate records, and event
  log entries.
- Reading typed route fields and selecting the next stage.
- Rendering `STATUS.md` from on-disk records.
- Enforcing commit boundaries from gate state.

The runtime does not own:

- Domain methods.
- Proof rules.
- Review criteria.
- Prompt depth.
- Tool-specific specialist instructions.
- Gate definitions.
- Specialist authority.
- Package mutation.

### Coordination Graph

`skill_graph CoordinationGraph` is the single authored graph boundary. It owns:

- Stages.
- Stage owners.
- Stage receipts.
- Durable artifacts.
- Review gates.
- Route choices.
- Pushback resolution routes.
- Specialist inventory.
- Graph policies and warnings.
- Emitted graph views.
- Graph source receipt.

The runtime walks the compiled graph contract. It does not infer graph shape
from Markdown.

### Specialist Packages

Each specialist is a Doctrine `skill package`. In v1 these packages are bundled
inside `coordination-kit`. Each specialist ships:

- Short resolver-friendly `SKILL.md`.
- `host_contract` bindings.
- Role manifest.
- Dispatch compatibility.
- Result receipt compatibility.
- Proof rules.
- Pushback rules.
- Gate signing rights.
- Optional bundled agent prompts.
- Source receipt.

Specialists communicate only through typed receipts and declared artifacts.

## 4. Run Folder

Runtime state lives under:

```text
.coord/runs/<RUN-ID>/
  CONTRACT.json
  graph_snapshot/
    SKILL_GRAPH.contract.json
    SKILL_GRAPH.source.json
    receipts/
  stages/<stage-id>/
    DISPATCH.json
    RESULT.json
    GATE.json
    evidence/
  LOG.jsonl
  STATUS.md
```

`CONTRACT.json` is the lowered run contract. `graph_snapshot/` pins the graph
and receipt schemas used at run start. The runtime walks the snapshot, not the
live source tree, so running projects stay auditable while packages evolve.

## 5. Package Layout

Plan the package source tree as:

```text
coordination-kit/
  prompts/
    GRAPH.prompt
    contracts/
      run_contract.prompt
      dispatch.prompt
      result.prompt
      gate.prompt
      evidence.prompt
      native_platform_matrix.prompt
      science_reference.prompt
      proposals.prompt
      role_manifest.prompt
      enums.prompt
    reviews/
      plan_ready.prompt
      plan_pressure.prompt
      spec_compliance.prompt
      code_quality.prompt
      visual_proof.prompt
      native_platform.prompt
      cleanup.prompt
      phase_close.prompt
      run_close.prompt
    specialists/
      intake_router/SKILL.prompt
      requirements/SKILL.prompt
      plan/SKILL.prompt
      implementation/SKILL.prompt
      spec_compliance_critic/SKILL.prompt
      code_quality_critic/SKILL.prompt
      cleanup/SKILL.prompt
      cold_check/SKILL.prompt
      closure/SKILL.prompt
      assignment_lint/SKILL.prompt
    references/
      proof_rules_visual.md
      proof_rules_native_ios.md
      proof_rules_native_android.md
      side_door_inventory_method.md
      science_reference_lookup.md
```

The v1 source tree has one emit target. Nested specialist packages still emit
their own `SKILL.md` trees and source receipts.

## 6. Typed Contracts

### RunContract

Fields:

- `run_id`
- `goal_raw`
- `goal_resolved`
- `named_artifacts`
- `in_scope`
- `out_of_scope`
- `acceptance_criteria`
- `requested_models_raw`
- `requested_models_resolved`
- `cleanup_default`
- `cleanup_overrides`
- `commit_policy`
- `risk_class`
- `science_reference`
- `stop_conditions`
- `no_code_change_allowed`

`cleanup_default` is a `CleanupPosture` enum. `cleanup_overrides` is a typed
table of `CleanupOverrideRow` rows:

- `path_glob`
- `posture`
- `reason`

The enum is the default. The rows are the exact per-path truth.

### RoleManifest

Fields:

- `name`
- `version`
- `domain`
- `accepts`
- `declines`
- `minimum_unit`
- `authority_grants`
- `sub_dispatch_budget`
- `gate_signing_rights`
- `cost_class`
- `proof_schema_ref`

`sub_dispatch_budget` defaults to `0`. A specialist with sub-dispatch authority
must emit a typed `SubDispatchRequest`; the flag alone never grows the queue.

### DispatchPacket

Fields:

- `assignment_question`
- `assignment_kind`
- `jurisdiction_ref`
- `authority_grants`
- `context_bundle`
- `constraints`
- `proof_schema_ref`
- `non_goals`
- `escalation_routes`
- `dispatch_self_check`

`assignment_question` must be an outcome question. It must not be an imperative
step list. It is checked by a schema pattern and by the assignment-lint
specialist.

### ResultReceipt

Fields:

- `status`
- `summary`
- `requirements_checked`
- `evidence`
- `findings`
- `risks`
- `what_was_not_checked`
- `next_route`

`next_route` is a typed route field. It can choose continuation, revision,
reroute, split, merge, user input, no-change success, block, completion, or a
typed pushback route.

### GateRecord

Fields:

- `gate_symbol`
- `signer_role`
- `verdict`
- `state`
- `failing_gates`
- `evidence`
- `waiver`
- `next_route`

`verdict` is the review verdict. `state` is a separate `GateState` enum:

- `passed`
- `failed`
- `blocked`
- `waived`
- `skipped`

If `state` is `waived`, a `GateWaiver` block is required:

- `waiver_role`
- `reason`
- `residual_risk`
- `chosen_route`

The waiver block is forbidden for non-waived states.

### EvidenceRecord

Fields:

- `kind`
- `provenance`
- `source_tool`
- `surface_id`
- `device_or_sim_id`
- `os_version`
- `orientation`
- `path`
- `summary`
- `falsifier_note`

Evidence must say what claim it proves and what negative case it would have
caught.

### NativePlatformRow

Fields:

- `platform`
- `surface_kind`
- `sim_or_device`
- `os_version`
- `orientation`
- `font_scale_state`
- `locale_state`
- `dark_mode_state`

Native proof requirements live in this typed table. Prose may explain how to
inspect the result, but the required matrix is data.

### ScienceReferenceRef

Fields:

- `path`
- `topic_index`

This field is nullable. A missing reference emits a graph warning by default.
It blocks only when a gate declares source-backed grounding as required.

### Proposal Receipts

Lessons are advisory in v1. The package defines:

- `GateProposal`
- `SpecialistAmendmentProposal`
- `GraphAmendmentProposal`

Applying a proposal requires explicit user approval and a separate change.

## 7. Closed Enums

Declare these once and reuse them:

- `AssignmentKind`: `outcome`, `review`, `proof`, `implementation`, `routing`,
  `decision`
- `CleanupPosture`: `delete_in_scope`, `preserve_dirty`, `ask_per_path`
- `CommitPolicy`: `phase_only`, `manual_only`, `staged_only`
- `CostClass`: `cheap`, `medium`, `heavy`
- `DurableArtifactStatus`: `current`, `stale`, `invalidated`, `missing`
- `EscalationRoute`: `pushback`, `peer_consult`, `judgment_escalation`,
  `user_escalation`
- `EvidenceKind`: `diff`, `test_run`, `screenshot`, `accessibility_tree`,
  `contact_sheet`, `recording`, `log`, `decision`, `manual_note`
- `EvidenceProvenance`: `host_screenshot`, `app_screenshot`,
  `accessibility_tree`, `dom_geometry`, `contact_sheet`, `command_transcript`,
  `diff`, `decision_log`, `device_capture`
- `GateState`: `passed`, `failed`, `blocked`, `waived`, `skipped`
- `Orientation`: `portrait`, `landscape`
- `PushbackCode`: `wrong_domain`, `missing_context`, `over_narrow`,
  `wrong_owner`, `bad_decomposition`, `conflicting_constraint`,
  `under_authority`, `evidence_infeasible`
- `ResultStatus`: `pass`, `fail`, `partial`, `pushback`, `blocked`,
  `no_change`
- `RiskClass`: `light`, `standard`, `heavy`
- `RoleAuthority`: `method_choice`, `sub_dispatch`, `peer_consult`,
  `gate_sign`, `refuse_unit`, `recommend_new_gate`
- `StageStatus`: `not_started`, `in_progress`, `partial`, `awaiting_gate`,
  `blocked`, `complete`, `invalidated`

## 8. Skill Graph

`CoordinationGraph` roots one flow: `OneRunFlow`.

Stages:

- `Intake`
- `RequirementsClarify`
- `PlanAuthor`
- `PlanPressure`
- `TestStrategy`
- `PhaseImplement`
- `SpecCompliance`
- `CodeQuality`
- `VisualProof`
- `NativeProof`
- `Cleanup`
- `PhaseClose`
- `Commit`
- `UnexpectedSnag`
- `ContractAmendment`
- `RiskChallenge`
- `RunClose`
- `LessonsHarvest`

Artifacts:

- `RunContractDoc`
- `RequirementsDoc`
- `PlanDoc`
- `WorkLog`
- `EvidenceBundle`
- `DecisionLedger`
- `CleanupManifest`
- `ProposalLedger`
- `LessonsLog`

Graph policies:

- `dag acyclic`
- `require edge_reason`
- `require relation_reason`
- `require durable_checkpoint`
- `require route_targets_resolve`
- `require checked_skill_mentions`
- `require branch_coverage`
- `require stage_lane`
- `warn orphan_stage`
- `warn orphan_skill`
- `warn receipt_without_consumer`
- `warn stage_owner_shared`
- `warn missing_science_reference`
- `warn dispatch_below_minimum_unit`
- `warn gate_waived_without_evidence`

Architecture-specific fail-loud policies:

- `pushback_resolution_required`: after any pushback route, the next allowed
  target is `ContractAmendment`, `UnexpectedSnag`, `RiskChallenge`, or `human`.
- `no_same_owner_review`: a gate signer cannot be the same role/session that
  produced the reviewed artifact.
- `dispatch_question_required`: a dispatch without a passing assignment-lint
  receipt cannot be sent.

Emitted views:

- `SKILL_GRAPH.contract.json`
- `SKILL_GRAPH.source.json`
- `references/coordination-graph.md`
- `references/coordination-graph.mmd`
- `references/stage-contracts.md`
- `references/flow-registry.md`
- `references/recovery-audit.md`
- `references/skill-inventory.md`
- `references/artifact-inventory.md`
- `references/gate-matrix.md`
- `references/evidence-ledger.md`
- `references/receipt-schemas/*.schema.json`

## 9. Gate Model

Every gate is a `review` or a `review_family` case.

Rules:

- Each gate's `contract:` is a `schema`.
- Each schema declares named `gates:`.
- Each named gate gets a per-gate accept or reject line.
- Do not collapse multi-gate contracts into one rollup predicate.
- The implementer may produce evidence, but cannot sign completion for the same
  artifact.
- Skipped or waived gates must record why, who waived them, residual risk, and
  selected route.
- Risk scaling is selector-driven through `RiskClass`, not ad hoc prose.

Core gate families:

- Requirements readiness.
- Plan readiness.
- Plan pressure.
- Test strategy.
- Spec compliance.
- Code quality.
- Visual proof.
- Native platform proof.
- Cleanup.
- Phase close.
- Run close.

## 10. Anti-Over-Prompting Design

The main failure mode to prevent is the coordinator turning experts into
small-task runners. The architecture prevents that in three layers.

### Layer 1: Typed Dispatch Shape

`DispatchPacket.assignment_question` is an outcome question. The packet also
names:

- Jurisdiction.
- Authority grants.
- Context artifacts.
- Contract-derived constraints.
- Proof schema.
- Non-goals.
- Escalation routes.
- Assignment kind.

The coordinator cannot send a packet without these fields.

### Layer 2: Schema Pattern

The assignment question rejects obvious imperative openers such as:

- `implement`
- `add`
- `open`
- `modify`
- `write`
- `update`
- `apply`
- `run`
- `verify`
- `check`
- `ensure`

This catches common microtask envelopes before dispatch.

### Layer 3: Assignment-Lint Specialist

`AssignmentLintSpecialist` is a pre-dispatch gate. It reads the question, role
manifest, context bundle, minimum unit, proof schema, and assignment kind. It
emits `DispatchSelfCheck`.

It rejects:

- Step lists disguised as assignments.
- Pre-baked answers framed as questions.
- Units below the role's minimum honest unit.
- Missing authority.
- Wrong owner.
- Proof obligations too narrow to prove the claim.
- Coordinator-invented constraints not present in the run contract or upstream
  receipts.

Both the schema pattern and the lint receipt must pass before dispatch.

## 11. Pushback

Pushback is a typed route, not conversation.

Pushback codes:

- `wrong_domain`
- `missing_context`
- `over_narrow`
- `wrong_owner`
- `bad_decomposition`
- `conflicting_constraint`
- `under_authority`
- `evidence_infeasible`

A pushback route always blocks that unit. The coordinator cannot route-shop by
sending the same question elsewhere without first resolving the pushback.

Resolution routes:

- `ContractAmendment` for missing context, conflicting constraints, or
  over-narrow task shape.
- `UnexpectedSnag` for under-authority decisions or infeasible evidence.
- `RiskChallenge` when risk class is wrong.
- `human` when the contract itself is ambiguous.

## 12. Risk Class

`IntakeRouter` writes the initial `risk_class` using typed heuristics:

- Expected file count.
- User-visible surface.
- Native mobile or visual proof involved.
- Data-loss, billing, auth, or migration risk.
- Requested model intensity.
- Explicit user risk request.
- No-code/no-change possibility.

`RequirementsSpecialist` may emit one `RiskClassChallenge` before planning.
Any later specialist may emit one more challenge if new evidence changes the
risk. Contested changes route to the user through `RiskClassDecision`.

Risk class controls gate density and review depth. It does not change the
standalone contract shape.

## 13. Cleanup

Cleanup is row-based.

`RunContract.cleanup_default` sets the default posture. `cleanup_overrides`
protects or strengthens specific paths.

Cleanup review checks:

- In-scope stale paths.
- Duplicate sources of truth.
- Confusing defaults.
- Side-door code paths.
- Dead docs or stale setup paths.
- Generated files that should not be hand-maintained.

If a path is dirty, untracked, or ambiguous, the cleanup specialist records the
ambiguity and blocks deletion until classified. It does not delete user-owned
work by inference.

## 14. First Specialist Set

Phase 6 ships the usable v1 set:

- `IntakeRouter`
- `RequirementsSpecialist`
- `PlanSpecialist`
- `ImplementationSpecialist`
- `SpecComplianceCritic`
- `CodeQualityCritic`
- `CleanupSpecialist`
- `ColdCheckSpecialist`
- `ClosureSpecialist`
- `AssignmentLintSpecialist`

Later phases add:

- `TestStrategySpecialist`
- `VisualSpecialist`
- `NativeIosVisualSpecialist`
- `NativeAndroidVisualSpecialist`
- `DualWitnessSpecialist`
- `LessonsSpecialist`
- Domain specialists such as game design, level design, and animation.

The graph can declare future stages with placeholder owners, but placeholders
must emit typed infeasible-evidence pushback and route to `human`. They must
not pretend unimplemented proof exists.

## 15. Specialist Plug-In Path

To add a specialist:

1. Add `prompts/specialists/<slug>/SKILL.prompt`.
2. Declare a resolver-friendly name and description.
3. Bind `host_contract` slots.
4. Declare `RoleManifest`.
5. Declare accepted and declined work.
6. Declare minimum honest unit.
7. Declare authority grants and gate signing rights.
8. Declare proof schema and references.
9. Add receipt compatibility.
10. Add stage ownership or route choices in `GRAPH.prompt`.
11. Re-emit and verify graph and source receipts.

The coordinator runtime does not change for a new specialist if the manifest,
dispatch, result, gate, and route contracts validate.

Existing runs stay pinned to their graph snapshot. Removing a live specialist
from the source tree does not change an active run.

## 16. Development Flow

The intended project flow:

1. Intake captures raw goal, named artifacts, risk guess, cleanup posture, and
   no-code/no-change possibility.
2. Requirements clarifies problem, constraints, scope, acceptance criteria, and
   open questions.
3. Plan authoring creates phases, dependencies, proof obligations, file targets,
   and cleanup obligations.
4. Plan pressure reviews feasibility, completeness, scope, and proof quality.
5. Test strategy maps requirements to falsifiable checks when risk requires it.
6. Implementation edits within assigned scope and emits evidence.
7. Spec compliance checks built behavior against the contract.
8. Code quality checks maintainability and failure modes.
9. Visual and native proof checks inspect actual rendered surfaces when
   relevant.
10. Cleanup checks stale paths and bad defaults.
11. Phase close checks traceability and gate state.
12. Commit happens only after phase gates pass.
13. Unexpected snags trigger typed decision artifacts and plan amendment.
14. Run close checks full traceability.
15. Lessons harvest emits advisory proposals for future changes.

## 17. Implementation Phases

### Phase 1: Shared Contracts

Author:

- `RunContract`
- `RoleManifest`
- `DispatchPacket`
- `SubDispatchRequest`
- `ResultReceipt`
- `GateRecord`
- `EvidenceRecord`
- Shared enums
- One placeholder specialist that round-trips a packet

Exit gates:

- Package emits.
- Receipts verify.
- Placeholder round trip validates.

### Phase 2: Coordination Graph Skeleton

Author `CoordinationGraph` with all stages, route fields, artifacts, and strict
policies. Use placeholder owners where needed.

Exit gates:

- Graph emits.
- Graph verifies.
- Mermaid view renders.
- Stage contracts view is generated.

### Phase 3: Thin Runtime CLI

Build the runtime loader and runner:

- Load graph snapshot.
- Create run folder.
- Persist run contract.
- Dispatch placeholder.
- Validate result receipt.
- Render status.

Exit gate:

- Synthetic run completes from intake to terminal route using only typed
  artifacts.

### Phase 4: First Real Review

Author `PlanReadyGate` as a typed review with named gates and per-gate accept
or reject lines.

Exit gates:

- A bad plan fails the exact gate.
- A fixed plan passes.
- Failure routes correctly.

### Phase 5: Anti-Over-Prompting Enforcement

Add:

- Assignment question schema pattern.
- `AssignmentLintSpecialist`.
- `DispatchSelfCheck`.
- Pushback resolution policy.
- Same-owner review block.

Exit gates:

- Imperative assignment fails.
- Step-list assignment fails.
- Too-small unit fails.
- Pushback cannot be route-shopped.

### Phase 6: Usable Core Specialists

Ship the v1 specialist set:

- Intake
- Requirements
- Plan
- Implementation
- Spec compliance
- Code quality
- Cleanup
- Cold check
- Closure
- Assignment lint

Exit gate:

- `RiskClass.standard` synthetic task runs end to end with independent gates.

### Phase 7: Visual Proof

Ship `VisualSpecialist` and visual evidence provenance.

Exit gates:

- Pixel-change-only evidence fails.
- Screenshot-with-context evidence can pass.
- Evidence record carries provenance and falsifier note.

### Phase 8: Native Proof

Ship iOS and Android native specialists plus `NativePlatformRow`.

Exit gates:

- Native screenshot without device/sim id fails.
- Native screenshot without OS/API version fails.
- Platform-specific gate cases route correctly.

### Phase 9: Judgment And Source Grounding

Ship the dual-witness judgment specialist, `UnexpectedSnag`, plan amendment,
and science/reference grounding.

Exit gates:

- `under_authority` pushback routes to judgment.
- Decision artifact lands.
- Plan amendment is required before implementation resumes.

### Phase 10: Risk Scaling

Add risk selectors on review families.

Exit gates:

- `light` skips heavy gates unless triggered.
- `standard` runs the normal gate set.
- `heavy` runs all gates.
- Risk challenge can reclassify the run.

### Phase 11: Lessons Harvest

Ship advisory proposal receipts.

Exit gates:

- Closed run emits typed proposals.
- No package mutates automatically.
- User approval is required to apply proposals.

## 18. Verification

For each phase:

- Run the package skill check after skill package changes.
- Emit graph artifacts when graph sources change.
- Verify graph artifacts are current.
- Verify skill/source receipts are current.
- Run a synthetic end-to-end coordinator run.
- Confirm `STATUS.md` can be rebuilt from disk without chat context.

Expected commands once the package exists:

```bash
npx skills check
uv run --locked python -m doctrine.emit_skill_graph --target coordination_kit
uv run --locked python -m doctrine.verify_skill_graph --target coordination_kit
uv run --locked python -m doctrine.verify_skill_receipts --target coordination_kit
```

The Doctrine target name is tentative until the package's emit target exists.

## 19. Model Consensus Record

Consensus artifact directory:

`.arch_skill/model-consensus/coordinated-agent-architecture-20260523T144713Z/`

Converged decisions:

- Standalone package.
- No dependency on existing local workflow skills.
- One package first, nested specialists first.
- Specialist split is mechanical later because contracts are stable.
- Typed graph owns routes, gates, stages, artifacts, and warnings.
- Runtime is thin and walks compiled contracts.
- Dispatch is typed and outcome-based.
- Assignment lint blocks over-prompting.
- Pushback routes are typed and blocking.
- Cleanup is row-based.
- Native proof matrix is table-based.
- Lessons are advisory in v1.
- Risk class can be challenged.

Remaining implementation choices are ordinary phase work, not architecture
blockers.
