---
title: "Arch Epic - Strict Subplan Auto Plan Gates - Architecture Plan"
date: 2026-06-08
status: active
fallback_policy: forbidden
owners: [aelaguiz]
reviewers: [plan-audit, Composer25Fast, thermo-nuclear-code-quality-review]
doc_type: phased_refactor
related:
  - docs/ARCH_EPIC_AUTO_PLAN_AUTO_IMPLEMENT_2026-06-07.md
  - docs/ARCH_EPIC_AUTO_PLAN_AUTO_IMPLEMENT_2026-06-07_PLAN_AUDIT.md
  - skills/arch-epic/SKILL.md
  - skills/arch-epic/references/workflow-contract.md
  - skills/arch-epic/references/arch-step-integration.md
  - skills/arch-epic/references/resume-semantics.md
  - skills/arch-step/references/arch-auto-plan.md
  - skills/arch-step/scripts/arch_stage_gate.py
---

# TL;DR

- **Outcome:** Repair `$arch-epic auto-plan` so it cannot fake sub-plan planning. It must drive every approved sub-plan through the real `$arch-step auto-plan <SUBPLAN_DOC_PATH>` flow, one sub-plan at a time, and mark a sub-plan `planned` only after the ArcStep generated receipt gate proves that planning is complete.
- **Problem:** The current ArcEpic same-session `auto-plan` contract can still be read as allowing ArcEpic to create or massage sub-plan docs and treat them as planned from prose confidence. That misses Amir's intent: the sub-phases must systematically walk the ArcStep auto-plan stages, not merely look planned.
- **Approach:** Keep this prompt-first and small. Tighten ArcEpic doctrine so ArcEpic is only the sequential driver; ArcStep remains the owner of each sub-plan's planning arc, generated receipts, readiness proof, and blocker truth.
- **Plan:** Re-read the live ArcEpic and ArcStep contracts, write this canonical plan, run `$arch-step auto-plan` on this plan until its own receipts pass, run `$plan-audit` until ready, get Composer25Fast fresh consult agreement that the plan enforces systematic sub-plan walkthrough, implement through `$plan-implement`, then run fresh consult plus thermonuclear review before commit/push.
- **Non-negotiables:** No new broad harness, no fake readiness, no parallel sub-plan planning, no marker-only proof, no status update to `planned` without `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <SUBPLAN_DOC_PATH>` exiting 0, and no commit/push until the requested reviews pass.

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-06-08
external_research_grounding: not started
deep_dive_pass_2: done 2026-06-08
phase_plan: done 2026-06-08
consistency_pass: done 2026-06-08
implementation_authorization_consult: passed Composer25Fast 2026-06-08
completion_consult: passed Composer25Fast 2026-06-08
recommended_flow: deep dive -> external research grounding if useful -> deep dive again -> phase plan -> consistency pass -> plan audit -> Composer25Fast plan consult -> plan implement -> Composer25Fast completion consult -> thermonuclear review -> commit/push
note: This plan exists because the prior ArcEpic auto-plan change preserved the right command names but did not make fake sub-plan planning impossible enough. The repair must force real ArcStep auto-plan receipt gates for each sub-plan.
-->
<!-- arch_skill:block:planning_passes:end -->

<!-- arch_skill:block:auto_plan_receipts:start -->
{
  "version": 1,
  "digest": "sha256:a2effdcd75ded42ce8ec05d1d1aeed6caa9943c8ae305f835761fac6153d556b",
  "receipts": [
    {
      "stage": "research",
      "command": "research",
      "status": "complete",
      "started_at": "2026-06-08T13:57:08Z",
      "command_ref_hash": "sha256:5ad5dc9efcb3c7d0d42e1d9014e3ee66fd24b8d2f1c85eef2c5ee96543e05c96",
      "doc_hash_before": "sha256:e00c4f3467745ba53482e89b167186c00bdc029072f00e46b60bf9acc6525380",
      "completed_at": "2026-06-08T13:58:16Z",
      "doc_hash_after": "sha256:0857fe59c3b21b54622a5a06792421833ea369c459f423460bcc8fe182be1cd5"
    },
    {
      "stage": "deep-dive-pass-1",
      "command": "deep-dive",
      "status": "complete",
      "started_at": "2026-06-08T13:58:32Z",
      "command_ref_hash": "sha256:c06af6026c9d59dec9c11dae8319ead3a2864dd67c05a2b8b07392ce1c62597a",
      "doc_hash_before": "sha256:0857fe59c3b21b54622a5a06792421833ea369c459f423460bcc8fe182be1cd5",
      "completed_at": "2026-06-08T13:59:41Z",
      "doc_hash_after": "sha256:3153774f0a78d0d090bec3317c62d83bbdc3d5817255b1129847ac0e83f6174a"
    },
    {
      "stage": "deep-dive-pass-2",
      "command": "deep-dive",
      "status": "complete",
      "started_at": "2026-06-08T13:59:54Z",
      "command_ref_hash": "sha256:c06af6026c9d59dec9c11dae8319ead3a2864dd67c05a2b8b07392ce1c62597a",
      "doc_hash_before": "sha256:3153774f0a78d0d090bec3317c62d83bbdc3d5817255b1129847ac0e83f6174a",
      "completed_at": "2026-06-08T14:00:20Z",
      "doc_hash_after": "sha256:d14fcf3fdbaf1fdd89022779be0861243e3825419bfd6e6bf24a4456c04dfb89"
    },
    {
      "stage": "phase-plan",
      "command": "phase-plan",
      "status": "complete",
      "started_at": "2026-06-08T14:00:27Z",
      "command_ref_hash": "sha256:1ce4687beab44819933a8a404a02b8e1345823a7a996f7d651f3dd25a0c54aa3",
      "doc_hash_before": "sha256:d14fcf3fdbaf1fdd89022779be0861243e3825419bfd6e6bf24a4456c04dfb89",
      "completed_at": "2026-06-08T14:01:14Z",
      "doc_hash_after": "sha256:7f17d4217cf99a7729869989b80dcc35196092d7ce39986651c18ceeaeb171b8"
    },
    {
      "stage": "consistency-pass",
      "command": "consistency-pass",
      "status": "complete",
      "started_at": "2026-06-08T14:01:35Z",
      "command_ref_hash": "sha256:439e1ccf2a90587bbec572e8bf46c4e08f16c9c81c75fcf835f736db479d3d74",
      "doc_hash_before": "sha256:7f17d4217cf99a7729869989b80dcc35196092d7ce39986651c18ceeaeb171b8",
      "completed_at": "2026-06-08T14:04:12Z",
      "doc_hash_after": "sha256:a850fabae3e3a3a2052041dd97176091bcf00150c4fdb9d110aceff9d50b6d20"
    }
  ]
}
<!-- arch_skill:block:auto_plan_receipts:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

When this change is complete, `$arch-epic auto-plan <EPIC_DOC_PATH>` will be a strict sequential driver over real `$arch-step auto-plan` runs. Given an approved epic with multiple sub-plans, ArcEpic will select the first non-complete sub-plan, ensure it has a canonical ArcStep DOC_PATH, invoke or continue `$arch-step auto-plan <SUBPLAN_DOC_PATH>`, require the ArcStep generated receipt gate to prove readiness, and only then mark that sub-plan `planned` and move to the next one. A reviewer should be able to read the skill doctrine and reject any ArcEpic behavior that marks sub-plans planned from marker text, copied sections, confidence, or ArcEpic-authored shortcut prose.

The failure case is equally falsifiable: if an agent can use `$arch-epic auto-plan` to produce plausible sub-plan docs, skip one of ArcStep's ordered planning stages, hand-edit receipt-looking text, or mark `planned` without the actual ArcStep readiness command passing for that sub-plan, this plan has failed.

## 0.2 In scope

Amir is not asking for a nicer description of `arch-epic auto-plan`. He is asking for enforcement.

The intended behavior is:

1. `arch-epic auto-plan` runs inside a native goal loop.
2. It plans sub-plans one at a time, in decomposition order.
3. For each sub-plan, ArcEpic must invoke or continue the real `$arch-step auto-plan <SUBPLAN_DOC_PATH>` flow.
4. ArcStep must perform its systematic sequence: `research`, `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`.
5. Each ArcStep stage must be proven by generated receipts written by `skills/arch-step/scripts/arch_stage_gate.py`.
6. ArcEpic must run `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <SUBPLAN_DOC_PATH>` before it marks that sub-plan `planned`.
7. If the gate does not pass, ArcEpic must continue or report the exact `$arch-step auto-plan <SUBPLAN_DOC_PATH>` next command. It must not pretend planning is complete.
8. Only after sub-plan N is genuinely ready may ArcEpic move to sub-plan N+1.
9. Only after every non-complete sub-plan is genuinely `planned` may `$arch-epic auto-implement` begin implementing in order.

The correction is not "add more ArcEpic planning prose." The correction is "make ArcEpic unable to substitute its own prose for ArcStep's auto-plan receipt gate."

The implementation scope is:

- Repair `$arch-epic auto-plan` doctrine so it is explicitly a sequential driver over real `$arch-step auto-plan`, not a sub-plan planning simulator.
- Strengthen `skills/arch-epic/references/workflow-contract.md` so the `auto-plan` mode requires ArcStep stage progression and gate proof for each sub-plan before status changes.
- Strengthen `skills/arch-epic/references/arch-step-integration.md` so every relevant status transition routes through real ArcStep auto-plan truth.
- Strengthen `skills/arch-epic/references/resume-semantics.md` so resume derives `planned` from ArcStep readiness proof and no implementation evidence, not from ArcEpic's prior status text alone.
- Add fail-loud wording for marker-only sub-plan docs, hand-edited receipt blocks, copied planning sections, or any ambiguous state where ArcStep readiness cannot be proven.
- Update examples and public docs only as needed to prevent users and future agents from misunderstanding the strict driver behavior.
- Preserve the existing spawned-harness `auto-run` lane as separate from same-session `auto-plan`.
- Use `$skill-authoring` and `$prompt-authoring` as the design lane for the skill repair.
- Run this plan through `$arch-step auto-plan` until its own receipt gate passes.
- Run `$plan-audit` until the plan is ready.
- Get Composer25Fast fresh-consult agreement that the plan requires the systematic sub-plan walkthrough and does not permit fake readiness.
- Implement with `$plan-implement` after plan readiness and consult agreement.
- Run a Composer25Fast completion consult or equivalent fresh consult after implementation, plus thermonuclear code-quality review, before commit/push.

## 0.3 Out of scope

- Adding a new Python runner, controller, polling harness, state database, or formal parameter schema for ArcEpic same-session `auto-plan`.
- Replacing `$arch-step auto-plan` or duplicating its internal stage logic in ArcEpic.
- Making ArcEpic edit target repo implementation code.
- Changing the existing role-based spawned-harness `auto-run` execution policy unless required to clarify that it is separate.
- Adding wording tests that lock skill doctrine to exact phrases.
- Committing or pushing before the plan, consult, implementation, and thermonuclear review gates are satisfied.

## 0.4 Definition of done (acceptance evidence)

- This plan's own `$arch-step auto-plan` receipts pass `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc docs/ARCH_EPIC_STRICT_SUBPLAN_AUTO_PLAN_GATES_2026-06-08.md`.
- `$plan-audit` records a ready verdict for this plan.
- Composer25Fast fresh consult agrees the plan requires ArcEpic to run real ArcStep auto-plan walkthroughs for every sub-plan and cannot mark planned from fake or marker-only evidence.
- `skills/arch-epic/SKILL.md` states the strict driver rule at the entrypoint and in non-negotiables.
- `skills/arch-epic/references/workflow-contract.md` makes the `auto-plan` mode choose the next sub-plan, invoke or continue `$arch-step auto-plan`, and refuse `planned` until `arch_stage_gate.py ready` passes for that exact sub-plan DOC_PATH.
- `skills/arch-epic/references/arch-step-integration.md` maps statuses so ArcEpic cannot skip from `pending`, `north-star-approved`, or `planning` to `planned` without real ArcStep gate proof.
- `skills/arch-epic/references/resume-semantics.md` explains that stored epic status is reconciled against sub-plan DOC_PATH truth and generated receipts before action.
- Public docs and examples describe same-session `auto-plan` as a strict sequential driver, not a bulk doc creation shortcut.
- Required verification for skill package changes runs: `rtk proxy npx skills check`.
- Targeted tests run when deterministic script behavior is touched. If scripts are not touched, the final report says so plainly.
- Thermonuclear review finds no unresolved maintainability, overbuild, fake-gate, or prompt-contract blocker.
- Commit and push happen only after all above evidence exists.

## 0.5 Key invariants (fix immediately if violated)

- ArcStep owns sub-plan planning rigor.
- ArcEpic owns only epic-level ordering, status reconciliation, and handoff.
- A sub-plan is not `planned` until the exact sub-plan DOC_PATH passes `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <SUBPLAN_DOC_PATH>`.
- Generated receipts, not marker presence, prove ArcStep stage completion.
- ArcEpic must never hand-edit `arch_skill:block:auto_plan_receipts`.
- One sub-plan is active at a time during same-session `auto-plan`.
- Native goal-mode continuation is the repetition mechanism; this repair should not add a new loop controller.
- If ArcStep says the sub-plan is not ready, ArcEpic must continue `$arch-step auto-plan <SUBPLAN_DOC_PATH>` or report the exact blocker. It must not synthesize readiness.
- `auto-implement` remains gated behind all non-complete sub-plans being `planned`.
- Prompt-first repair is the default. Deterministic support already exists in `arch_stage_gate.py`; do not add new determinism unless the plan proves a real gap.

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)

1. Make fake sub-plan planning impossible in normal ArcEpic doctrine execution.
2. Reuse the working ArcStep auto-plan stage gate instead of building another harness.
3. Keep ArcEpic readable as an orchestrator, not a second planning engine.
4. Preserve the user's desired goal-loop behavior: keep moving sub-plan by sub-plan until all are planned or a true blocker stops the run.
5. Keep the change small enough that future agents can follow it without learning a new state machine.

## 1.2 Constraints

- The prior change was committed as `af4dbdb Add arch-epic auto plan drivers`; this plan repairs that behavior rather than starting from scratch.
- `skills/arch-step/references/arch-auto-plan.md` is the authoritative source for the ordered planning sequence and receipt gates.
- `skills/arch-step/scripts/arch_stage_gate.py` already exists to prevent marker-only readiness claims.
- `skills/arch-epic` doctrine is the owning surface for the new driver behavior.
- Repo instructions require `rtk proxy npx skills check` after skill package changes under `skills/`.
- The user explicitly requested Composer25Fast fresh consult agreement and thermonuclear review before commit/push.

## 1.3 Architectural principles (rules we will enforce)

- **Driver, not planner:** ArcEpic drives `$arch-step auto-plan`; it does not recreate ArcStep planning inside ArcEpic prose.
- **Gate before status:** ArcEpic status updates follow ArcStep gate proof, never the other way around.
- **Receipt truth over document shape:** plausible sections without generated receipts are incomplete.
- **Sequential progress:** sub-plan N+1 starts only after sub-plan N is truly `planned`.
- **Goal-loop compatible:** inside native goal mode, ArcEpic keeps taking the next required bounded action until the epic auto-plan North Star is met or blocked.
- **No new harness by default:** improve prompt contracts first; use the existing Python gate as the deterministic proof.

## 1.4 Known tradeoffs (explicit)

- Same-session `auto-plan` will be slower because it forces every sub-plan through ArcStep's full planning arc. That is the point: speed cannot come from fake readiness.
- ArcEpic may need to stop more often when a sub-plan DOC_PATH is ambiguous or non-canonical. That is better than silently minting a bad plan.
- The doctrine will be stricter and a little more repetitive around gates. That repetition is acceptable where it prevents future agents from collapsing the ArcStep sequence.

# 2) Problem Statement (existing architecture + why change)

The repo already has two pieces that should solve this problem together:

- `$arch-step auto-plan` is a receipt-gated planning loop for one canonical plan
  doc.
- `$arch-epic auto-plan` is intended to drive many sub-plan docs through that
  same loop before implementation begins.

The problem is that the current ArcEpic contract still leaves too much room for
the parent orchestrator to think "I created or repaired the sub-plan doc, and it
looks planned, so I can mark it `planned`." That is the fake-readiness loophole.
ArcStep's Python gate was created specifically to prevent that shape of failure:
marker blocks and convincing plan text do not prove that `research`, both
`deep-dive` passes, `phase-plan`, and `consistency-pass` actually ran.

This repair should tighten ArcEpic at the orchestration boundary. ArcEpic must
not become a second planning engine. It should repeatedly drive the existing
ArcStep planning engine for each sub-plan, one at a time, and use ArcStep's
generated receipts as the only proof that a sub-plan is ready.

# 3) Research Grounding (external + internal "ground truth")

<!-- arch_skill:block:research_grounding:start -->
# Research Grounding (external + internal "ground truth")

## External anchors (papers, systems, prior art)

- No external research is needed for this repair. The authoritative behavior is
  local skill doctrine plus the existing deterministic ArcStep gate. Adding a
  new external orchestration pattern would risk overbuilding the exact prompt
  repair Amir asked to keep small.

## Internal ground truth (code as spec)

- Authoritative behavior anchors (do not reinvent):
  - `skills/arch-step/references/arch-auto-plan.md` defines the single-plan
    auto-plan sequence: `research`, `deep-dive` pass 1, `deep-dive` pass 2,
    `phase-plan`, and `consistency-pass`, with generated receipts for every
    stage.
  - `skills/arch-step/scripts/arch_stage_gate.py` is the deterministic proof
    owner. It writes `arch_skill:block:auto_plan_receipts`, enforces receipt
    order, requires each stage to begin and complete, rejects unchanged docs
    after `begin`, validates required stage markers, and returns `READY
    next=implement-loop` only after all receipts and the approved consistency
    pass are present.
  - `tests/test_arch_stage_gate.py` proves the gate's intended anti-fake
    behavior: manual research blocks without receipts do not unlock the next
    stage, deep-dive pass 2 needs a separate receipt, readiness fails until all
    receipts exist, and readiness fails if consistency-pass says not to
    proceed.
  - `README.md` and `docs/arch_skill_usage_guide.md` already document that
    marker-only plan text is not enough for `$arch-step auto-plan`; `DOC_PATH`
    is the planning ledger and native goal mode supplies repeated turns.

- Canonical path / owner to reuse:
  - `skills/arch-epic/SKILL.md` owns the top-level trigger and non-negotiable
    behavior for ArcEpic.
  - `skills/arch-epic/references/workflow-contract.md` owns the `auto-plan`
    mode actions and must say that ArcEpic invokes or continues real
    `$arch-step auto-plan <SUBPLAN_DOC_PATH>` until the ArcStep gate proves
    readiness for that exact sub-plan.
  - `skills/arch-epic/references/arch-step-integration.md` owns the sub-plan
    status mapping and must prevent status transitions from bypassing ArcStep
    gate truth.
  - `skills/arch-epic/references/resume-semantics.md` owns state
    reconciliation and must treat observed sub-plan DOC_PATH truth plus
    generated receipts as stronger than stored epic status.

- Adjacent surfaces tied to the same contract family:
  - `skills/arch-epic/references/epic-doc-contract.md` defines allowed sub-plan
    statuses and mutation rules; it must stay aligned with any stricter
    definition of `planned`.
  - `skills/arch-epic/references/examples.md` currently teaches same-session
    `auto-plan`; it must not show bulk doc creation as the meaningful work.
  - `README.md` and `docs/arch_skill_usage_guide.md` are the user-facing command
    inventory; they should describe strict sequential ArcStep auto-plan driving
    when they mention `$arch-epic auto-plan`.
  - `skills/arch-epic/references/auto-harness-prompts.md` and
    `skills/arch-epic/references/model-and-effort.md` are adjacent only to keep
    same-session `auto-plan` separate from spawned-harness `auto-run`.

- Compatibility posture (separate from `fallback_policy`):
  - Clean doctrine cutover. Existing command names stay the same, but the
    interpretation of same-session `auto-plan` becomes stricter. No fallback
    lane should allow fake readiness for the old looser behavior.

- Existing patterns to reuse:
  - ArcStep's receipt-gated `auto-plan` pattern: choose next stage from
    `arch_stage_gate.py status`, write only through the owning stage, complete
    through `arch_stage_gate.py complete`, and require `ready` before
    implementation.
  - ArcEpic's existing one-sub-plan-at-a-time ordering: the epic selects the
    first non-complete sub-plan and advances only after the relevant gate.
  - Skill authoring's prompt-first default: repair the reusable prompt contract
    before adding scripts, runners, or formal inputs.

- Prompt surfaces / agent contract to reuse:
  - `skills/arch-epic/SKILL.md` should carry the high-level "driver, not
    planner" rule.
  - `workflow-contract.md`, `arch-step-integration.md`, and
    `resume-semantics.md` should carry the detailed routing and proof rules.
  - `$prompt-authoring` guidance says to fix the right section and teach
    recognition tests instead of smearing new rules everywhere.

- Native model or agent capabilities to lean on:
  - Codex / Claude native goal mode already supplies repeated turns. ArcEpic
    does not need a new polling loop to keep moving sub-plan by sub-plan.
  - The agent can invoke slash-command skills in the visible session; ArcEpic
    already says same-session work does not shell out to child CLIs.

- Existing grounding / tool / file exposure:
  - The agent can read the epic doc, each sub-plan DOC_PATH, and run
    `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc
    <SUBPLAN_DOC_PATH>` directly.
  - The generated receipt block lives in each sub-plan DOC_PATH and is
    protected by a digest; hand edits produce a digest mismatch.

- Duplicate or drifting paths relevant to this change:
  - ArcEpic currently mentions both "create or repair sub-plan docs" and
    "runs `$arch-step auto-plan`." The repair must make creation/repair only
    the setup step, never the readiness proof.
  - ArcEpic's `planning` mapping currently checks the consistency-pass block
    before running the readiness gate. The target wording should make the
    generated receipt gate the decisive proof, not consistency markers alone.

- Capability-first opportunities before new tooling:
  - Stronger ArcEpic prompt doctrine plus the existing ArcStep gate should solve
    the failure. A new ArcEpic Python orchestrator would be overbuilt unless
    Composer25Fast or later implementation evidence proves prompt repair cannot
    enforce the behavior.

- Behavior-preservation signals already available:
  - `rtk proxy npx skills check` validates skill package shape after doctrine
    changes.
  - `rtk python3 -m unittest tests/test_arch_stage_gate.py` validates the
    deterministic receipt gate if touched or if we need a direct proof signal.
  - `rtk python3 -m unittest tests/test_arch_epic_auto.py` protects existing
    spawned-harness automation script behavior if the implementation touches
    adjacent ArcEpic automation docs/scripts.

## Decision gaps that must be resolved before implementation

- None. Repo evidence and Amir's clarified intent settle the key architecture:
  strengthen ArcEpic as a sequential driver over real ArcStep auto-plan and do
  not add a new harness.
<!-- arch_skill:block:research_grounding:end -->

# 4) Current Architecture (as-is)

<!-- arch_skill:block:current_architecture:start -->
# Current Architecture (as-is)

ArcEpic is a prompt-first orchestrator skill. It does not run a compiled
state machine for same-session `auto-plan`; the operating behavior lives in:

- `skills/arch-epic/SKILL.md` for top-level trigger, non-negotiables, mode list,
  and output expectations.
- `skills/arch-epic/references/workflow-contract.md` for explicit modes and the
  `auto-plan` action list.
- `skills/arch-epic/references/arch-step-integration.md` for sub-plan Status to
  ArcStep command routing.
- `skills/arch-epic/references/resume-semantics.md` for re-deriving state from
  the epic doc and sub-plan docs.
- `skills/arch-epic/references/epic-doc-contract.md` for allowed statuses,
  mutation rules, and log examples.

The June 7 change added same-session `auto-plan` and `auto-implement` and a
`planned` status. That improved the public command shape, but the current
wording still has a weak boundary:

- `SKILL.md` says same-session `auto-plan` creates or repairs each sub-plan
  DOC_PATH by applying the `arch-step new` artifact contract directly, then
  marks ready sub-plans `planned`.
- `workflow-contract.md` says the mode creates, repairs, or advances a sub-plan
  through `$arch-step auto-plan`, then runs `arch_stage_gate.py ready` before
  marking `planned`.
- `arch-step-integration.md` lets `planning` first look for a
  `consistency_pass` block with proceed fields, then says same-session
  `auto-plan` should run the readiness gate.
- `resume-semantics.md` considers planning markers and the readiness gate when
  deriving status, but the main prose still reads like markers are part of the
  status decision surface.

The deterministic ArcStep side is much stricter. `arch_stage_gate.py` writes a
digest-protected `arch_skill:block:auto_plan_receipts` block and refuses to
advance from marker-only plan text. Tests prove manual marker blocks do not
unlock the next stage, both deep-dive passes require separate receipts, and
`ready` fails until all receipts and an approved consistency-pass are present.

So the current architecture has the right proof mechanism, but ArcEpic does not
yet state plainly enough that ArcEpic must drive real ArcStep auto-plan until
that mechanism passes for each sub-plan. The weakness is prompt-contract
ambiguity, not missing deterministic machinery.
<!-- arch_skill:block:current_architecture:end -->

# 5) Target Architecture (to-be)

<!-- arch_skill:block:target_architecture:start -->
# Target Architecture (to-be)

ArcEpic same-session `auto-plan` becomes a strict sequential driver over
ArcStep. The ownership boundary is:

- ArcEpic owns epic ordering, sub-plan selection, DOC_PATH assignment, stored
  status reconciliation, orchestration log entries, and the "which sub-plan is
  next?" decision.
- ArcStep owns every sub-plan's planning arc, required stage order, generated
  receipts, section-quality checks, consistency pass, and readiness proof.

The target `auto-plan` loop is:

1. Read the epic doc and all relevant sub-plan DOC_PATHs.
2. Reconcile stored sub-plan Status against observed sub-plan truth.
3. Select the first sub-plan whose Status is neither `planned` nor `complete`.
4. If the sub-plan has no DOC_PATH, assign the normal grouped path.
5. If the DOC_PATH is missing, create only the canonical ArcStep scaffold needed
   for a real sub-plan plan target, seeded from approved epic scope and Epic
   Requirement Coverage. If scope is ambiguous, ask instead of guessing.
6. Invoke or continue `$arch-step auto-plan <SUBPLAN_DOC_PATH>` in the visible
   same session.
7. After each bounded continuation, inspect the sub-plan with
   `python3 skills/arch-step/scripts/arch_stage_gate.py status --doc
   <SUBPLAN_DOC_PATH>` or `ready --doc <SUBPLAN_DOC_PATH>`.
8. If the sub-plan is not ready, keep its status `planning` and continue or
   report the exact next `$arch-step auto-plan <SUBPLAN_DOC_PATH>` command.
9. If and only if `ready --doc <SUBPLAN_DOC_PATH>` exits 0, update the epic
   sub-plan Status to `planned`, append a compact log entry, and move to the
   next sub-plan.
10. Stop only when every non-complete sub-plan is `planned`, or when a true
    blocker prevents the next ArcStep auto-plan action.

The target status reconciliation rule is:

- If stored Status is `planned` but `ready --doc <SUBPLAN_DOC_PATH>` fails, the
  stored status is stale. ArcEpic must downgrade or keep the sub-plan at
  `planning`, append a compact reconciliation log entry, and continue
  `$arch-step auto-plan <SUBPLAN_DOC_PATH>`.
- If stored Status is `planning` and `ready --doc <SUBPLAN_DOC_PATH>` passes,
  ArcEpic may mark `planned` because the generated receipts prove the sub-plan
  planning arc completed.
- If stored Status is `pending` or `north-star-approved`, ArcEpic may start or
  continue setup, but it still cannot mark `planned` until the exact DOC_PATH
  passes the readiness command.
- If implementation worklog or implementation audit evidence already exists,
  ArcEpic must surface the mixed state instead of rewriting history to make the
  epic look cleanly pre-implementation.

The target doctrine must make fake states invalid:

- A consistency-pass marker without complete generated receipts is not enough.
- Existing Section 3-7 content without matching receipts is not enough.
- A stored epic Status of `planned` is not enough if the sub-plan DOC_PATH fails
  the readiness command on resume.
- ArcEpic must never hand-edit `arch_skill:block:auto_plan_receipts`.
- ArcEpic must not infer readiness from having created or repaired the sub-plan
  doc.

No new same-session runner is part of the target architecture. Native goal mode
does the repetition. The existing Python gate does the deterministic proof.
Prompt doctrine tells the agent to combine those two pieces correctly.
<!-- arch_skill:block:target_architecture:end -->

# 6) Call-Site Audit (exhaustive change inventory)

<!-- arch_skill:block:call_site_audit:start -->
# Call-Site Audit (exhaustive change inventory)

## Change map (table)

| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| ---- | ---- | ------------------ | ---------------- | --------------- | --- | ------------------ | -------------- |
| Skill entrypoint | `skills/arch-epic/SKILL.md` | same-session `auto-plan` prose, non-negotiables, mode list | Says ArcEpic creates/repairs sub-plan DOC_PATHs and runs `$arch-step auto-plan`, but does not strongly say creation/repair is never readiness proof | Add "strict sequential driver" language and explicitly require real `$arch-step auto-plan` plus `arch_stage_gate.py ready` per sub-plan before `planned` | This is the top-level runtime contract future agents read first | No new command name; stricter meaning for existing `$arch-epic auto-plan` | `npx skills check`; manual doctrine review |
| Workflow mode | `skills/arch-epic/references/workflow-contract.md` | `Mode: auto-plan` Actions / outputs / failure modes | Mentions `$arch-step auto-plan` and readiness gate, but still frames output as one DOC_PATH created/repaired/advanced and does not spell out repeated gate-reported ArcStep continuation | Rewrite action list around: select sub-plan, ensure DOC_PATH, invoke/continue real ArcStep auto-plan, inspect status/ready, keep `planning` until ready, only then set `planned`, continue next sub-plan in goal mode | This is the exact mode contract; ambiguity here causes fake sub-phase planning | Existing `$arch-epic auto-plan <EPIC_DOC_PATH>` | `npx skills check`; plan-audit/fresh-consult review |
| Status routing | `skills/arch-epic/references/arch-step-integration.md` | `pending`, `north-star-approved`, `planning`, `planned` mappings | `planning` first looks for consistency-pass proceed fields before gate proof; `planned` meaning says passed readiness bar but not enough fail-loud detail for stale stored status | Make generated receipt gate decisive. If consistency marker exists but `ready` fails, stay/return to `planning` and continue `$arch-step auto-plan`. Mention marker-only and copied-section states explicitly | This file is the operational cheat sheet; it must block status shortcuts | Same status vocabulary, stricter transition proof | `npx skills check`; possible `tests/test_arch_stage_gate.py` as proof of gate behavior |
| Resume state | `skills/arch-epic/references/resume-semantics.md` | Re-entry routine and disagreement examples | Reads planning markers and readiness gate; stored `planned` can sound reusable unless gate no longer passes | State that every resume must re-run or trust only current `ready --doc` output for non-implemented `planned`; stored `planned` is downgraded if the gate fails | Goal-loop resumes are where fake states can persist | No new state file; sub-plan DOC_PATH remains authority | `npx skills check`; manual review |
| Orchestration log | Epic doc `Orchestration Log` entries governed by `epic-doc-contract.md` | Status updates and reconciliation entries | Current examples include `Sub-plan N marked planned` without requiring the proof command in the log text | Make log examples or mutation rules name the readiness proof when marking `planned`, and name stale-status reconciliation when downgrading | A future reader should know why a status changed without trusting hidden parent memory | Existing epic doc log, no new schema | Manual review |
| Epic doc contract | `skills/arch-epic/references/epic-doc-contract.md` | Status list, mutation rules, log examples | Allows `planned` but definition can stay high-level | Tighten `planned` definition to "ArcStep readiness command exited 0 for this DOC_PATH after real auto-plan receipts"; mutation rule should forbid `planned` from marker-only content | Keeps the epic artifact honest for future readers | No schema change; stricter status semantics | `npx skills check` |
| Examples | `skills/arch-epic/references/examples.md` | Same-session `auto-plan` example | Example says native goal-mode repeats and readiness gate exits 0, but does not show fake-document rejection | Add one sentence or mini-failure note: created docs are setup only; if receipts are incomplete, status remains `planning` and ArcEpic continues `$arch-step auto-plan` | Examples teach future agents how not to shortcut | No API change | `npx skills check` |
| Public docs | `README.md`, `docs/arch_skill_usage_guide.md` | ArcEpic practical rule and examples | Says ArcEpic creates/repairs DOC_PATHs, runs `$arch-step auto-plan`, requires gate | Update to emphasize strict sequential ArcStep auto-plan driver and marker-only rejection, without bloating docs | Public surface should match runtime contract | Same user command | `npx skills check` because skill changed; docs readback |
| Existing deterministic gate | `skills/arch-step/scripts/arch_stage_gate.py` | Stage gate implementation | Already enforces ordered receipts and marker evidence | No change planned | The existing tool is sufficient; adding a second gate would overbuild | Existing CLI | If untouched, no script tests required; may run `tests/test_arch_stage_gate.py` as assurance |
| Existing tests | `tests/test_arch_stage_gate.py`, `tests/test_arch_epic_auto.py` | Gate and spawned-harness tests | Gate tests already prove marker-only anti-fake behavior; ArcEpic tests cover script-backed auto-run | Do not add wording tests. Add deterministic tests only if code changes; likely not needed because repair is doctrine/docs | Repo red line forbids exact-doctrine wording tests | Existing tests remain useful signals | Run if touched or for assurance |

## Migration notes

* Canonical owner path / shared code path: `skills/arch-epic` doctrine owns the
  repair; `skills/arch-step/scripts/arch_stage_gate.py` remains the deterministic
  proof owner.
* Deprecated APIs (if any): none. Command names remain the same.
* Delete list (what must be removed; include superseded shims/parallel paths if any): none planned.
* Adjacent surfaces tied to the same contract family: `SKILL.md`,
  `workflow-contract.md`, `arch-step-integration.md`, `resume-semantics.md`,
  `epic-doc-contract.md`, `examples.md`, README, and usage guide.
* Compatibility posture / cutover plan: clean doctrine cutover. Existing
  `$arch-epic auto-plan` invocations become stricter immediately.
* Capability-replacing harnesses to delete or justify: none. Do not add a new
  same-session ArcEpic harness.
* Live docs/comments/instructions to update or delete: README and usage guide
  wording only if implementation changes user-facing understanding.
* Behavior-preservation signals for refactors: `rtk proxy npx skills check`;
  optional `rtk python3 -m unittest tests/test_arch_stage_gate.py` to prove the
  existing gate; optional `tests/test_arch_epic_auto.py` if adjacent automation
  script behavior is touched.

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)

| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope |
| ---- | ------------- | ---------------- | ---------------------- | -------------- |
| ArcEpic same-session planning | `SKILL.md`, `workflow-contract.md`, `arch-step-integration.md`, `resume-semantics.md` | Driver over real ArcStep auto-plan plus readiness gate | Prevents ArcEpic from becoming a planning simulator | include |
| ArcEpic docs/status contract | `epic-doc-contract.md`, `examples.md` | `planned` means exact DOC_PATH passes ArcStep ready gate | Prevents stored status from outranking current sub-plan truth | include |
| Public docs | `README.md`, `docs/arch_skill_usage_guide.md` | strict sequential driver wording | Prevents user-facing docs from teaching bulk doc creation as auto-plan | include |
| Spawned-harness lane | `auto-harness-prompts.md`, `model-and-effort.md`, `run_arch_epic.py` | keep separate from same-session auto-plan | Avoids accidental nested auto-plan in child harnesses | exclude unless review finds drift |
| ArcStep gate script | `arch_stage_gate.py` | existing receipt-gated proof | Avoids new duplicate gate | preserve, no code change planned |
<!-- arch_skill:block:call_site_audit:end -->

# 7) Depth-First Phased Implementation Plan (authoritative)

<!-- arch_skill:block:phase_plan:start -->
# Depth-First Phased Implementation Plan (authoritative)

> Rule: depth-first implementation protects the full destination while proving
> the path early. Treat TL;DR, Section 0, Sections 5-6, and approved decisions
> as the destination map. `Checklist (must all be done)` is the authoritative
> must-do list inside each phase. `Exit criteria (all required)` names the
> concrete done conditions that review must validate.

## Phase 1 — Tighten the ArcEpic same-session driver contract

* Goal: Make the core ArcEpic doctrine impossible to read as permission to fake
  sub-plan planning.
* Work: Update the runtime contract and operational references so same-session
  `auto-plan` is explicitly a strict sequential driver over real ArcStep
  auto-plan runs.
* Checklist (must all be done):
  - Update `skills/arch-epic/SKILL.md` so the entrypoint, non-negotiables, mode
    summary, and output expectations say ArcEpic drives real
    `$arch-step auto-plan <SUBPLAN_DOC_PATH>` one sub-plan at a time and cannot
    mark `planned` until `arch_stage_gate.py ready` exits 0 for that exact
    DOC_PATH.
  - Update `skills/arch-epic/references/workflow-contract.md` so
    `auto-plan` actions explicitly select the next sub-plan, ensure DOC_PATH
    setup, invoke or continue real `$arch-step auto-plan`, inspect gate status,
    keep/downgrade `planning` when not ready, and set `planned` only after
    readiness passes.
  - Update `skills/arch-epic/references/arch-step-integration.md` so
    `pending`, `north-star-approved`, `planning`, and `planned` mappings all
    route through generated ArcStep receipt truth and reject marker-only or
    copied-section readiness.
  - Update `skills/arch-epic/references/resume-semantics.md` so stored
    `planned` status is reconciled against current sub-plan `ready --doc`
    output on resume; stale `planned` is downgraded or surfaced, not trusted.
  - Update `skills/arch-epic/references/epic-doc-contract.md` so `planned`
    status and log examples name the ArcStep readiness proof and stale-status
    reconciliation behavior.
  - Do not add scripts, runners, state files, model policies, or formal input
    schemas in this phase.
* Verification (required proof):
  - Read back changed core files.
  - Use `rg` to confirm strict-driver wording, readiness-gate requirements,
    marker-only rejection, and stale-status reconciliation appear in the owning
    files.
* Docs/comments (propagation; only if needed): None beyond the owning skill
  reference docs in this phase.
* Exit criteria (all required):
  - A future agent reading only the ArcEpic skill and core references would know
    it must run real `$arch-step auto-plan <SUBPLAN_DOC_PATH>` for each
    sub-plan.
  - No core ArcEpic wording presents sub-plan DOC_PATH creation/repair,
    consistency markers, or stored status as sufficient readiness proof.
  - No new deterministic machinery was introduced.
* Rollback: Revert the ArcEpic skill/reference wording changes from this phase.

## Phase 2 — Align examples and public docs without bloating the surface

* Goal: Make the public command surface teach the same strict driver behavior.
* Work: Update examples and user-facing docs only where they could otherwise
  preserve the older weaker mental model.
* Checklist (must all be done):
  - Update `skills/arch-epic/references/examples.md` so the same-session
    `auto-plan` example states that creating a sub-plan doc is setup only, and
    incomplete receipts keep the sub-plan in `planning`.
  - Update `README.md` ArcEpic wording to describe `$arch-epic auto-plan` as a
    strict sequential ArcStep auto-plan driver.
  - Update `docs/arch_skill_usage_guide.md` ArcEpic practical rule with the
    same strict sequential driver behavior.
  - Keep spawned-harness `auto-run` wording separate; do not make spawned
    workers invoke nested `$arch-step auto-plan`.
* Verification (required proof):
  - Read back changed public docs.
  - Use `rg` to confirm the docs distinguish same-session `auto-plan` from
    spawned-harness `auto-run`.
* Docs/comments (propagation; only if needed): Public docs updated in this
  phase are the propagation surface.
* Exit criteria (all required):
  - User-facing docs no longer read like ArcEpic bulk-creates plans and then
    marks them planned.
  - Examples show that generated receipts and `ready --doc` are the proof.
  - The spawned-harness lane remains clearly separate.
* Rollback: Revert public docs/example edits from this phase.

## Phase 3 — Verification, consult gates, and publish readiness

* Goal: Prove the skill repair is package-valid, reviewed against Amir's intent,
  and free of overbuilt or fake-gate regressions before commit/push.
* Work: Run the required package check, targeted tests if touched, requested
  consults, and thermonuclear review; fix any findings before publishing.
* Checklist (must all be done):
  - Run `rtk proxy npx skills check` after skill package changes.
  - Run `rtk python3 -m unittest tests/test_arch_stage_gate.py` if
    `arch_stage_gate.py` changes; otherwise run it as optional assurance or
    state why it was not required.
  - Run `rtk python3 -m unittest tests/test_arch_epic_auto.py` if
    script-backed ArcEpic automation changes; otherwise state why it was not
    required.
  - Run `$plan-audit` on this plan until the plan verdict is ready.
  - Get Composer25Fast fresh consult agreement before implementation that this
    plan enforces systematic per-sub-plan ArcStep auto-plan walkthrough.
  - After implementation, get a Composer25Fast completion consult or equivalent
    fresh consult focused on whether the requirements were met.
  - Run `$thermo-nuclear-code-quality-review` and fix any unresolved blockers.
  - Commit and push only after the above gates pass.
* Verification (required proof):
  - Command outputs for package check and any tests run.
  - Plan-audit log with ready verdict.
  - Fresh consult artifacts or summary with pass/agreement.
  - Thermonuclear review result with no unresolved findings.
* Docs/comments (propagation; only if needed): Final report must state whether
  scripts were touched and which tests were or were not required.
* Exit criteria (all required):
  - All requested pre-implementation gates pass before implementation starts.
  - All requested post-implementation gates pass before commit/push.
  - Final commit contains only the intended plan/skill/doc repair surface.
* Rollback: If a review finds the approach wrong, stop before commit/push and
  repair the plan or implementation rather than publishing.
<!-- arch_skill:block:phase_plan:end -->

# 8) Verification Strategy (common-sense; non-blocking)

Verification follows the changed surface:

- Plan readiness:
  - `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc
    docs/ARCH_EPIC_STRICT_SUBPLAN_AUTO_PLAN_GATES_2026-06-08.md`
  - `$plan-audit` ready verdict
  - Composer25Fast fresh consult agreement before implementation
- Skill package validity:
  - `rtk proxy npx skills check`
- Deterministic gate assurance:
  - `rtk python3 -m unittest tests/test_arch_stage_gate.py` if the gate script
    changes, otherwise optional assurance because this plan relies on that
    existing behavior
- ArcEpic script-backed automation assurance:
  - `rtk python3 -m unittest tests/test_arch_epic_auto.py` if
    `run_arch_epic.py` or script-backed auto-run behavior changes
- Review before publish:
  - Composer25Fast completion consult or equivalent fresh consult
  - `$thermo-nuclear-code-quality-review`
  - `git diff --check`

# 9) Rollout / Ops / Telemetry

This is a docs-and-skill-doctrine rollout. There is no runtime deployment,
schema migration, persistent state migration, or production telemetry surface.

Rollout order:

1. Finish this plan's ArcStep readiness gate.
2. Run `$plan-audit` until the plan verdict is ready.
3. Get Composer25Fast agreement that the plan enforces systematic per-sub-plan
   ArcStep walkthrough and does not permit fake readiness.
4. Implement the planned doctrine/docs changes through the plan-backed path.
5. Run package verification, completion consult, thermonuclear review, and
   `git diff --check`.
6. Commit and push only after those gates pass.

Operational check after rollout: invoke `$arch-epic auto-plan` on an approved
multi-sub-plan epic and confirm it reports or continues the exact
`$arch-step auto-plan <SUBPLAN_DOC_PATH>` command until
`arch_stage_gate.py ready --doc <SUBPLAN_DOC_PATH>` passes for each sub-plan.
Any stored `planned` status that fails that readiness command must be treated
as stale.

Rollback is normal Git rollback of the docs/skill-doctrine commit. Because no
runtime script or state format changes are planned, rollback does not require a
data repair step.

<!-- arch_skill:block:consistency_pass:start -->
## Consistency Pass

- Reviewers: self-integrator using the ArcStep consistency-pass contract
- Scope checked: TL;DR, Section 0 North Stars and requirements, Section 1
  priorities, Section 2 problem statement, Section 3 grounding, Section 4
  current architecture, Section 5 target architecture, Section 6 change
  inventory, Section 7 phases, Section 8 verification, Section 9 rollout, and
  Section 10 decision log.
- Findings summary: Section 9 was still a placeholder after phase planning.
  The rest of the plan consistently points to a prompt-first ArcEpic repair
  that delegates sub-plan readiness to the real ArcStep generated receipt gate.
- Integrated repairs: Filled Section 9 with docs-only rollout, operational
  smoke check, rollback posture, and no-runtime-migration statement. Normalized
  Section 0 to the canonical ArcStep subsection numbering while keeping Amir's
  explicit requirements at the top under in-scope behavior. Marked the plan
  `active` because Amir confirmed the North Stars and requirements for this
  plan doc.
- Remaining inconsistencies: none
- Unresolved decisions: none
- Unauthorized scope cuts: none
- Decision-complete: yes
- Decision: proceed to implement? yes
<!-- arch_skill:block:consistency_pass:end -->

# 10) Decision Log (append-only)

- 2026-06-08 Initial plan doc started from Amir's clarified intent: ArcEpic must enforce real ArcStep auto-plan walkthroughs per sub-plan, not fake planning through ArcEpic-authored prose.
- 2026-06-08 Plan status set to `active` after Amir confirmed the plan should
  start with the North Stars and requirements captured at the top.
- 2026-06-08 Composer25Fast pre-implementation consult passed with high
  confidence. Chain:
  `/tmp/fresh-consult/arch-epic-strict-subplan-plan-20260608-1PD6zJ`;
  run: `turn-01`; session: `973c9c11-257b-4339-8ee9-8797db0af649`. Implementation
  must apply its sharpness note: make `workflow-contract.md` setup explicitly
  scaffold-only and replace `arch-step-integration.md` marker-first
  "planning is done" wording so no surface implies marker or doc creation is
  readiness proof.
- 2026-06-08 Composer25Fast post-implementation consult passed with high
  confidence. Chain:
  `/tmp/fresh-consult/arch-epic-strict-subplan-plan-20260608-1PD6zJ`;
  run: `turn-02`; session: `973c9c11-257b-4339-8ee9-8797db0af649`. The consult
  found no material fake-readiness loopholes. Its only residual note was to
  make the `resume-semantics.md` stored-`planned` skip wording clearer; that
  wording is now explicit that the skip applies only while the exact ArcStep
  readiness command still exits 0.
- 2026-06-08 Thermonuclear maintainability review passed. The review found no
  new runner/controller, no script changes, no file crossing 1000 lines, no
  scattered special-case branching, and no unresolved prompt-contract blocker.
  The strict-gate language lives in the existing ArcEpic owning surfaces and
  reuses the existing ArcStep readiness gate instead of adding a parallel
  mechanism.
