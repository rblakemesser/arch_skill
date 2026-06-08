---
title: "Arch Epic - Strict Auto Implement Gates - Architecture Plan"
date: 2026-06-08
status: active
fallback_policy: forbidden
owners: [aelaguiz]
reviewers: [plan-audit, Composer25Fast, thermo-nuclear-code-quality-review]
doc_type: phased_refactor
related:
  - docs/ARCH_EPIC_AUTO_PLAN_AUTO_IMPLEMENT_2026-06-07.md
  - docs/ARCH_EPIC_STRICT_SUBPLAN_AUTO_PLAN_GATES_2026-06-08.md
  - skills/arch-epic/SKILL.md
  - skills/arch-epic/references/workflow-contract.md
  - skills/arch-epic/references/arch-step-integration.md
  - skills/arch-epic/references/resume-semantics.md
  - skills/arch-epic/references/epic-doc-contract.md
  - skills/arch-epic/references/examples.md
  - skills/arch-step/references/arch-implement-loop.md
  - skills/arch-step/references/arch-implement.md
  - skills/arch-step/references/arch-audit-implementation.md
---

# TL;DR

- **Outcome:** Repair `$arch-epic auto-implement <EPIC_DOC_PATH>` so it is an exhaustive epic-level driver over real `$arch-step auto-implement <SUBPLAN_DOC_PATH>` runs. It must implement one planned sub-plan at a time, let ArcStep own the full implementation-frontier loop and `audit-implementation`, run the epic critic only after ArcStep reports `Verdict (code): COMPLETE`, and advance only after that critic passes.
- **Problem:** The current ArcEpic same-session `auto-implement` prose names the right commands, but it is still too thin. A future agent can read it as "call auto-implement once, notice an audit block, run the critic, move on" without carrying ArcStep's exhaustive implement/prove/audit/reopen methodology into the epic-level loop.
- **Approach:** Keep this prompt-first. Strengthen ArcEpic doctrine so ArcEpic is only the ordered driver and state reconciler; ArcStep remains the owner of implementation-frontier work, proof, worklog truth, phase reopenings, and code-completeness audit. The epic critic remains the owner of cross-sub-plan scope drift after ArcStep is clean.
- **Skill lane:** Use `$skill-authoring` and `$prompt-authoring` discipline. This is an edited skill contract, not a new script, controller, runner, state file, or spawned-worker lane.
- **Review lane:** Run this plan through ArcStep-style receipt gating, get a Cursor Agent `composer-2.5-fast` fresh consult before implementation, run `$plan-audit` before implementation, implement with `$plan-implement`, then run an unbiased Composer completion consult and `$thermo-nuclear-code-quality-review` before commit/push and `$amir-publish`.
- **Non-negotiables:** No fake implementation completion, no skipping ArcStep `audit-implementation`, no marking a sub-plan `complete` without `Verdict (code): COMPLETE` and an epic critic `pass`, no planning inside `auto-implement`, no parallel sub-plan implementation, no new broad harness, and no commit/push/publish until all requested review gates pass.

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
recommended_flow: deep dive -> deep dive again -> phase plan -> consistency pass -> Composer25Fast plan consult -> plan audit -> plan implement -> Composer25Fast completion consult -> thermonuclear review -> commit/push -> amir-publish
note: This plan exists because ArcEpic same-session auto-implement must be as methodical at the epic layer as ArcStep implement-loop is for a single plan. ArcEpic should drive the loop; it must not emulate or weaken it.
receipt_note_research: completed 2026-06-08; internal ground truth anchored to ArcStep implement-loop, implement, audit-implementation, readiness gate, and ArcEpic critic contracts.
receipt_note_deep_dive_1: completed 2026-06-08; first pass identified the owning ArcEpic surfaces and confirmed the gap is contract sharpness rather than missing deterministic plumbing.
receipt_note_deep_dive_2: completed 2026-06-08; second pass expanded the repair to resume semantics, epic doc mutation rules, examples, and public docs so stale or shortcut completion cannot survive adjacent surfaces.
receipt_note_phase_plan: completed 2026-06-08; implementation is split into core contract, examples/public docs, and verification/review/publish gates.
receipt_note_consistency: completed 2026-06-08; consistency pass found no unresolved decisions, no unauthorized scope cuts, and no need for a new controller or script.
-->
<!-- arch_skill:block:planning_passes:end -->

<!-- arch_skill:block:auto_plan_receipts:start -->
{
  "version": 1,
  "digest": "sha256:bce2954eaaa566d51d0d0ebfd102055bbc7fde920634c664d62e762ee1c802b9",
  "receipts": [
    {
      "stage": "research",
      "command": "research",
      "status": "complete",
      "started_at": "2026-06-08T18:07:05Z",
      "command_ref_hash": "sha256:5ad5dc9efcb3c7d0d42e1d9014e3ee66fd24b8d2f1c85eef2c5ee96543e05c96",
      "doc_hash_before": "sha256:030293856f0da92ee5bfa74b4ce82d80552fc471bd511e43eafe79a4d98fb242",
      "completed_at": "2026-06-08T18:07:14Z",
      "doc_hash_after": "sha256:def5c21565f7051549c90a2390a306fa33556b27fb4086c234ab3498626d877b"
    },
    {
      "stage": "deep-dive-pass-1",
      "command": "deep-dive",
      "status": "complete",
      "started_at": "2026-06-08T18:07:19Z",
      "command_ref_hash": "sha256:c06af6026c9d59dec9c11dae8319ead3a2864dd67c05a2b8b07392ce1c62597a",
      "doc_hash_before": "sha256:def5c21565f7051549c90a2390a306fa33556b27fb4086c234ab3498626d877b",
      "completed_at": "2026-06-08T18:07:28Z",
      "doc_hash_after": "sha256:65e82e6e82e134342cf93dfe89818983af09979321390983f1d4d423a84e12ce"
    },
    {
      "stage": "deep-dive-pass-2",
      "command": "deep-dive",
      "status": "complete",
      "started_at": "2026-06-08T18:07:33Z",
      "command_ref_hash": "sha256:c06af6026c9d59dec9c11dae8319ead3a2864dd67c05a2b8b07392ce1c62597a",
      "doc_hash_before": "sha256:65e82e6e82e134342cf93dfe89818983af09979321390983f1d4d423a84e12ce",
      "completed_at": "2026-06-08T18:07:44Z",
      "doc_hash_after": "sha256:4bf3420fa823dec477f77d224a8e7d62cdfe95f2322d4cae8281c498068406e1"
    },
    {
      "stage": "phase-plan",
      "command": "phase-plan",
      "status": "complete",
      "started_at": "2026-06-08T18:07:51Z",
      "command_ref_hash": "sha256:1ce4687beab44819933a8a404a02b8e1345823a7a996f7d651f3dd25a0c54aa3",
      "doc_hash_before": "sha256:4bf3420fa823dec477f77d224a8e7d62cdfe95f2322d4cae8281c498068406e1",
      "completed_at": "2026-06-08T18:07:58Z",
      "doc_hash_after": "sha256:d85b8ee8f4ba7236ebfe3e5cd8973d008647899f0c651dbaaab08d388854ac26"
    },
    {
      "stage": "consistency-pass",
      "command": "consistency-pass",
      "status": "complete",
      "started_at": "2026-06-08T18:08:04Z",
      "command_ref_hash": "sha256:439e1ccf2a90587bbec572e8bf46c4e08f16c9c81c75fcf835f736db479d3d74",
      "doc_hash_before": "sha256:d85b8ee8f4ba7236ebfe3e5cd8973d008647899f0c651dbaaab08d388854ac26",
      "completed_at": "2026-06-08T18:08:12Z",
      "doc_hash_after": "sha256:b3ed75cac2f59c08aecfa8c9134940f2822d7e8634998319a644a5616a8d9c5b"
    }
  ]
}
<!-- arch_skill:block:auto_plan_receipts:end -->

# 0) Holistic North Star And Requirements

## 0.1 The Claim (Falsifiable)

When this change is complete, `$arch-epic auto-implement <EPIC_DOC_PATH>` will be a strict same-session goal-loop driver over the existing ArcStep `implement-loop` / `auto-implement` contract. Given an approved epic whose non-complete sub-plans are `planned`, ArcEpic will choose the first planned or implementing sub-plan in decomposition order, verify that its exact DOC_PATH still passes the ArcStep readiness gate, invoke or continue the real `$arch-step auto-implement <SUBPLAN_DOC_PATH>` loop, wait for ArcStep's authoritative `arch_skill:block:implementation_audit` to say `Verdict (code): COMPLETE`, run the existing epic critic, and only then mark the sub-plan `complete` and move to the next one.

The failure case is equally falsifiable: if an agent can use `$arch-epic auto-implement` to skip the ArcStep implementation-frontier loop, run the epic critic before ArcStep audit is clean, mark a sub-plan complete from worklog optimism or broad green tests, ignore reopened phases, implement sub-plans in parallel, or start implementation while a non-complete sub-plan is not truly `planned`, this plan has failed.

## 0.2 Requirements

The intended behavior is:

1. `arch-epic auto-implement` runs inside native goal mode when the user wants exhaustive continuation.
2. It starts only after every non-complete sub-plan is `planned` or already `complete`; stale `planned` status must be reconciled against the exact ArcStep readiness command.
3. It handles sub-plans one at a time, in approved decomposition order.
4. For each selected sub-plan, ArcEpic must run `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc <SUBPLAN_DOC_PATH>` before implementation starts or resumes.
5. If readiness fails, ArcEpic must set or keep that sub-plan at `planning` and route to `$arch-epic auto-plan <EPIC_DOC_PATH>`. It must not implement from marker-only planning text.
6. ArcEpic must invoke or continue the real `$arch-step auto-implement <SUBPLAN_DOC_PATH>` flow. ArcEpic must not emulate ArcStep's phase ledger, worklog, implementation pass, proof collection, or `audit-implementation` block.
7. ArcStep must own the full implementation methodology for each sub-plan: current approved ordered implementation frontier, phase checklist and exit criteria, credible proof, worklog truth, plan truth, then `audit-implementation` against current repo state.
8. If ArcStep audit is missing or says anything other than `Verdict (code): COMPLETE`, ArcEpic must keep or set the sub-plan to `implementing` and continue or report the exact `$arch-step auto-implement <SUBPLAN_DOC_PATH>` command. It must not run the epic critic yet.
9. Only after ArcStep audit is COMPLETE may ArcEpic run the existing epic critic.
10. The epic critic must remain a read-only scope-drift and epic-requirement-coverage gate. It does not replace ArcStep code-completeness audit.
11. Only after the epic critic returns `pass` may ArcEpic write the verdict path, mark the sub-plan `complete`, and move to the next sub-plan.
12. If the critic returns `scope_change_detected`, ArcEpic must halt for a scope-preserving decision. It must not auto-drop, auto-defer, or mark complete.
13. If the critic returns `incomplete`, ArcEpic must treat that as an upstream state mismatch or missing code-completeness issue and keep the sub-plan in implementation; it must not advance.
14. Only after every sub-plan is `complete` may ArcEpic set the epic `status: complete`.
15. In native goal mode, ArcEpic keeps moving through the next required bounded action until all sub-plans are complete or a true blocker stops the run. Outside goal mode, it runs one bounded transition and names the exact next command.
16. Resume routing must reconcile `resume-semantics.md`, `workflow-contract.md`, and `arch-step-integration.md`: resumed same-session `auto-implement` runs continue ArcStep until audit is clean, while ordinary interactive runs may surface the next exact command.
17. The core doctrine must say plainly that one `$arch-step auto-implement <DOC_PATH>` invocation is not completion. Completion means ArcStep's implement/prove/audit loop has reached `Verdict (code): COMPLETE`.
18. `$skill-authoring` and `$prompt-authoring` are operational requirements, not labels: implementation must treat this as an existing skill edit, keep the package prompt-first, repair the right sections instead of smearing guidance everywhere, preserve agent judgment, and avoid scripts/controllers unless the plan proves prompt guidance cannot work.

## 0.3 Implementation Scope

- Strengthen `skills/arch-epic/SKILL.md` so the entrypoint says same-session `auto-implement` is a strict sequential driver over real ArcStep `auto-implement`, not a loose implementation shortcut.
- Strengthen `skills/arch-epic/references/workflow-contract.md` so the `auto-implement` mode spells out readiness, real ArcStep invocation, audit-clean waiting, critic gating, continuation, and fail-loud behavior.
- Strengthen `skills/arch-epic/references/arch-step-integration.md` so status transitions from `planned` and `implementing` cannot skip ArcStep readiness, implementation-frontier work, clean implementation audit, or critic-pass completion. This file must distinguish same-session `auto-implement` continuation from ordinary interactive "surface the next command" behavior.
- Strengthen `skills/arch-epic/references/resume-semantics.md` so stored epic status is reconciled against sub-plan readiness, implementation audit truth, worklog/audit evidence, and critic verdicts before action, then routes resumed same-session `auto-implement` through continue-until-clean behavior instead of stopping at stale interactive wording.
- Strengthen `skills/arch-epic/references/epic-doc-contract.md` so `auto-implement` mutation rules and orchestration log examples reflect the strict gates.
- Update `skills/arch-epic/references/examples.md`, `README.md`, and `docs/arch_skill_usage_guide.md` only enough to prevent users and future agents from misunderstanding same-session `auto-implement`.
- Preserve the role-based spawned-harness `auto-run` lane as a separate explicit workflow. Do not make spawned workers invoke nested automatic commands.
- Preserve prompt-first skill design. Add no new scripts, controller state, polling loop, runner, or formal parameter schema unless implementation proves prompt doctrine cannot express the required behavior. The expected answer is no new mechanism.

## 0.4 Out Of Scope

- Changing ArcStep's `implement-loop`, `implement`, `audit-implementation`, or `arch_stage_gate.py` behavior.
- Making ArcEpic edit target repo implementation code directly.
- Adding a deterministic ArcEpic auto-implement runner or new same-session state file.
- Redesigning the spawned-harness `auto-run` lane.
- Adding wording tests that lock skill doctrine to exact phrasing.
- Using external model delegation for implementation. Fresh consults are read-only review gates only.
- Committing, pushing, or publishing before the plan, consult, audit, implementation, completion consult, and thermonuclear gates are satisfied.

## 0.5 Definition Of Done

- This plan's own ArcStep receipt gate passes: `python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc docs/ARCH_EPIC_STRICT_AUTO_IMPLEMENT_GATES_2026-06-08.md`.
- Cursor Agent `composer-2.5-fast` fresh consult passes on whether the plan is exhaustive, convention-aligned, prompt-first, and uses `$skill-authoring` / `$prompt-authoring`.
- `$plan-audit` records a ready verdict for this plan before implementation starts.
- `skills/arch-epic/SKILL.md` states the strict same-session `auto-implement` driver rule at the entrypoint and in non-negotiables.
- `skills/arch-epic/references/workflow-contract.md` makes `auto-implement` choose one sub-plan, require ArcStep readiness, run real `$arch-step auto-implement`, wait for `Verdict (code): COMPLETE`, run the epic critic, and advance only after `pass`.
- `skills/arch-epic/references/workflow-contract.md` explicitly says native goal mode must continue the ArcStep implement/prove/audit loop until `Verdict (code): COMPLETE` or a true blocker stops it; one invocation is not completion.
- `skills/arch-epic/references/arch-step-integration.md` maps `planned`, `implementing`, and critic `incomplete` states so ArcEpic cannot skip implementation-frontier work, fresh audit, or critic pass.
- `skills/arch-epic/references/resume-semantics.md` explains stale `planned`, false `implementing`, audit-clean, critic-pass, stale `complete`, and resumed `auto-implement` continuation reconciliation.
- Public docs and examples describe same-session `auto-implement` as an exhaustive sequential driver over ArcStep implementation, not a one-call shortcut.
- Required verification for skill package changes runs: `rtk proxy npx skills check`.
- Targeted existing tests run unless no deterministic/script behavior is touched and there is a defensible reason to skip them. The default here is to run `tests/test_arch_stage_gate.py` and `tests/test_arch_epic_auto.py` for assurance.
- Composer completion consult passes after implementation.
- Thermonuclear maintainability review finds no unresolved overbuild, prompt-contract, fake-gate, side-door, file-size, or structure blocker.
- The final committed diff contains only intended plan/docs/skill changes; unrelated untracked files remain untouched.
- Commit, push, and `$amir-publish` complete after all gates pass.

## 0.6 Key Invariants

- ArcStep owns sub-plan implementation rigor.
- ArcEpic owns epic ordering, state reconciliation, scope-preserving halts, and handoff to the next sub-plan.
- A sub-plan is not implementation-ready unless its exact DOC_PATH passes `arch_stage_gate.py ready`.
- A sub-plan is not epic-complete unless ArcStep audit is `COMPLETE` and the epic critic returns `pass`.
- A clean local test, a worklog entry, a completed phase status, or implementation confidence is not enough for ArcEpic to advance.
- Reopened phases are current work. ArcEpic must route back through `$arch-step auto-implement <DOC_PATH>`.
- The epic critic cannot bless missing ArcStep code-completeness. It only runs after ArcStep says code is complete.
- One sub-plan is active at a time during same-session `auto-implement`.
- Native goal-mode continuation is the repetition mechanism; this repair should not add a loop controller.
- Prompt-first repair is the default; deterministic support already exists in ArcStep's readiness gate and ArcEpic's critic plumbing.

# 1) Key Design Considerations

## 1.1 Priorities

1. Make false epic-level implementation completion impossible in normal ArcEpic doctrine execution.
2. Reuse ArcStep's existing `implement-loop` / `auto-implement` methodology instead of duplicating it.
3. Preserve the ordered epic model: sub-plan N must be clean and critic-passed before sub-plan N+1 starts.
4. Keep same-session auto-implement separate from spawned-harness `auto-run`.
5. Keep the fix small, self-contained, and prompt-first.

## 1.2 Constraints

- `skills/arch-step/references/arch-implement-loop.md` is the authoritative single-plan implementation loop.
- `skills/arch-step/references/arch-implement.md` owns implementation-pass discipline, phase checklist execution, proof, worklog, and plan truth.
- `skills/arch-step/references/arch-audit-implementation.md` owns code-completeness audit and phase reopening.
- `skills/arch-epic/references/critic-contract.md` owns the epic-level scope-drift gate after ArcStep is clean.
- `skills/arch-epic` doctrine is the owning surface for the epic driver behavior.
- Repo instructions require `rtk proxy npx skills check` after skill package changes under `skills/`.
- The user explicitly required `$skill-authoring`, `$prompt-authoring`, Composer25Fast plan consult, `$plan-audit`, Composer completion consult, thermonuclear review, commit/push, and `$amir-publish`.

## 1.3 Architectural Principles

- **Driver, not implementer:** ArcEpic drives `$arch-step auto-implement`; it does not implement or audit sub-plan code itself.
- **Audit before critic:** ArcStep `Verdict (code): COMPLETE` is required before the epic critic runs.
- **Critic before completion:** Epic critic `pass` is required before ArcEpic marks a sub-plan `complete`.
- **Sequential progress:** sub-plan N+1 starts only after sub-plan N is complete by both gates.
- **Truth from disk:** every resume re-reads the epic doc, sub-plan docs, worklogs, implementation audit blocks, and verdict artifacts.
- **No new harness:** improve prompt contracts first; do not create a new same-session automation mechanism.

## 1.4 Known Tradeoffs

- Same-session `auto-implement` may be slower because it forces every sub-plan through ArcStep's full implement/prove/audit loop. That is the intended quality bar.
- The doctrine will repeat the audit/critic ordering in multiple owning surfaces. That repetition is acceptable where it prevents future agents from confusing ArcStep completion with epic completion.
- ArcEpic may halt more often on stale status, missing critic policy, or scope-change discoveries. That is better than silently advancing a false-complete epic.

# 2) Problem Statement

The repo already has the right pieces:

- `$arch-step auto-implement` is the exact alias of `implement-loop` for one canonical plan.
- `implement-loop` already requires planning readiness, implementation-frontier execution, credible proof, worklog/doc synchronization, and `audit-implementation`.
- `$arch-epic auto-implement` is supposed to run those single-plan loops across an approved epic's sub-plans in order.

The gap is not missing code plumbing. The gap is doctrine sharpness. ArcEpic currently says it invokes `$arch-step auto-implement` and then runs the critic after a COMPLETE audit, but it does not forcefully carry the full ArcStep methodology into the epic loop. The wording leaves room for a future agent to treat the ArcStep call as a one-off action rather than a repeat-until-clean implementation loop, to run the epic critic too early, or to mark sub-plans complete from stored status rather than current audit and verdict truth.

This repair should tighten the orchestration boundary. ArcEpic must be as strict for many sub-plans as ArcStep is for one plan: do the current sub-plan fully, audit it fully, critic it fully, reconcile the epic ledger, then move on.

# 3) Research Grounding

<!-- arch_skill:block:research_grounding:start -->
## External Anchors

No external research is needed. The authoritative behavior is local skill doctrine and existing deterministic helpers. Adding a new external orchestration pattern would risk overbuilding a prompt-first skill repair.

## Internal Ground Truth

- `skills/arch-step/references/arch-implement-loop.md` defines the exhaustive single-plan loop: readiness gate, implementation pass, proof, doc/worklog truth, `audit-implementation`, and repeat until clean or blocked.
- `skills/arch-step/references/arch-implement.md` defines how implementation executes the current approved ordered implementation frontier and keeps the plan/worklog/code aligned.
- `skills/arch-step/references/arch-audit-implementation.md` defines the authoritative code-completeness verdict and false-complete phase reopening behavior.
- `skills/arch-step/scripts/arch_stage_gate.py` is the readiness proof owner before implementation starts.
- `skills/arch-epic/references/workflow-contract.md` currently owns same-session `auto-implement` mode but needs sharper exhaustive-loop language.
- `skills/arch-epic/references/arch-step-integration.md` currently maps `planned` and `implementing` statuses but needs stronger current-state reconciliation and continuation rules.
- `skills/arch-epic/references/critic-contract.md` and `critic-prompt.md` already describe the epic critic as read-only scope drift after ArcStep audit is clean; this should be reused, not replaced.
<!-- arch_skill:block:research_grounding:end -->

# 4) Current Architecture

<!-- arch_skill:block:current_architecture:start -->
## ArcStep Single-Plan Implementation

ArcStep has a mature implementation loop for one plan. `implement-loop` / `auto-implement` first requires `arch_stage_gate.py ready --doc <DOC_PATH>` to pass. It then executes the current approved ordered implementation frontier, keeps `DOC_PATH` and `WORKLOG_PATH` truthful, runs credible proof, and runs `audit-implementation`. The audit block owns `Verdict (code): COMPLETE|NOT COMPLETE`; reopened phases and missing code work keep the loop alive.

## ArcEpic Same-Session Auto-Implement

ArcEpic has an `auto-implement` mode in `workflow-contract.md`. It requires non-complete sub-plans to be `planned`, selects the first `planned` or `implementing` sub-plan, runs the ArcStep readiness gate, invokes or continues `$arch-step auto-implement <DOC_PATH>` if the implementation audit is not COMPLETE, runs the epic critic when audit is COMPLETE, and marks the sub-plan complete if the critic passes.

The current shape is directionally right but underspecified. It names the right gates without teaching enough of the ArcStep implementation methodology and without repeating the fail-loud states in the entrypoint, resume semantics, examples, and public docs.

## Spawned-Harness Lane

ArcEpic also has an explicit role-based `auto-run` lane. Spawned workers apply ArcStep doctrine directly from disk and must not invoke nested `auto-plan`, `implement-loop`, or `auto-implement`. This plan keeps that lane separate.
<!-- arch_skill:block:current_architecture:end -->

# 5) Target Architecture

<!-- arch_skill:block:target_architecture:start -->
## Same-Session Auto-Implement Contract

ArcEpic `auto-implement` becomes a strict epic-level driver over ArcStep's existing implementation loop:

1. Re-read the epic doc, every non-complete sub-plan DOC_PATH, worklog state, implementation audit blocks, and existing epic critic verdict fields.
2. Refuse to start if any non-complete sub-plan is not `planned` or `implementing`.
3. For each stored `planned` sub-plan, re-run `arch_stage_gate.py ready --doc <DOC_PATH>` before implementation. If it fails, reset or keep status `planning` and route to `auto-plan`.
4. Select the first `planned` or `implementing` sub-plan in decomposition order.
5. If its implementation audit is absent or not COMPLETE, invoke or continue `$arch-step auto-implement <DOC_PATH>`. Keep status `implementing`; do not run the epic critic.
6. Require ArcStep to own the implementation pass, proof, worklog, plan truth, phase reopenings, and `audit-implementation`.
7. When the implementation audit says `Verdict (code): COMPLETE`, run the existing epic critic with the current epic doc, sub-plan doc, worklog, and schema.
8. If critic verdict is `pass`, write the verdict path, mark the sub-plan `complete`, append compact log entries, and continue to the next sub-plan in native goal mode.
9. If critic verdict is `scope_change_detected`, set epic `status: halted`, set sub-plan `scope-changed`, record the scope-preserving decision options, and ask the user.
10. If critic verdict is `incomplete`, keep or set sub-plan `implementing`, record the mismatch, and route back through the ArcStep implementation loop or ask only when the evidence is unreadable or contradictory. Do not use the current interactive-mode halt wording for same-session `auto-implement`.
11. After all sub-plans are `complete`, set epic `status: complete` and print the summary.

## Prompt-First Skill Repair

The change belongs in ArcEpic prompt doctrine because no deterministic behavior is missing from the repo. The repair should strengthen:

- the `SKILL.md` mission and non-negotiables,
- `workflow-contract.md` mode steps and failure modes,
- `arch-step-integration.md` status mappings,
- `resume-semantics.md` state derivation,
- `epic-doc-contract.md` mutation/log rules,
- examples and public docs.

## No New Mechanism

No new same-session controller, state file, runner, polling loop, or script should be added. Deterministic proof remains in ArcStep's readiness gate and ArcEpic's existing critic subprocess plumbing.
<!-- arch_skill:block:target_architecture:end -->

# 6) Call-Site And Drift Audit

<!-- arch_skill:block:call_site_audit:start -->
## Owning Surfaces To Change

- `skills/arch-epic/SKILL.md`
  - Entry mission, non-negotiables, mode list, and output expectations should say `auto-implement` is exhaustive, sequential, and gated by ArcStep audit plus epic critic.
- `skills/arch-epic/references/workflow-contract.md`
  - `auto-implement` mode should carry the full implement/prove/audit/reopen/critic/advance loop and precise failure modes.
- `skills/arch-epic/references/arch-step-integration.md`
  - `planned` and `implementing` mappings should reject stale readiness, missing/non-complete audit, early critic runs, and false completion.
- `skills/arch-epic/references/resume-semantics.md`
  - Resume should derive status from current readiness, implementation audit, worklog/audit truth, and critic verdict fields instead of trusting stored status alone.
- `skills/arch-epic/references/epic-doc-contract.md`
  - Mutation rules and log examples should reflect audit-clean then critic-pass before `complete`.
- `skills/arch-epic/references/examples.md`
  - Same-session `auto-implement` example should show the full ArcStep loop, not only one invocation.
- `README.md` and `docs/arch_skill_usage_guide.md`
  - Public descriptions should say same-session `auto-implement` is a strict sequential implementation driver over ArcStep's implementation-frontier loop plus epic critic.

## Surfaces To Leave Alone Unless Evidence Forces A Change

- `skills/arch-step/references/arch-implement-loop.md`, `arch-implement.md`, `arch-audit-implementation.md`, and `arch_stage_gate.py`.
  - These already own the single-plan methodology. The ArcEpic repair should reference and enforce them, not change them.
- `skills/arch-epic/scripts/run_arch_epic.py`.
  - Existing critic plumbing is sufficient for the expected prompt-first repair.
- `skills/arch-epic/references/auto-harness-prompts.md`.
  - Spawned-harness mode remains separate unless wording search finds a contradiction that would route spawned workers into nested automatic commands.

## Drift Risks

- Public docs can still describe `auto-implement` as a vague "implements planned sub-plans" command.
- Resume semantics can let stored `complete` or `implementing` status outrun current sub-plan audit or critic truth.
- Workflow contract can fail to state that NOT COMPLETE audit means "continue ArcStep", not "run critic anyway".
- Examples can teach the shortcut by showing only a single command invocation.
<!-- arch_skill:block:call_site_audit:end -->

# 7) Phase Plan

<!-- arch_skill:block:phase_plan:start -->
## Phase 1 - Core Auto-Implement Contract

Status: PLANNED

Work: Tighten the runtime ArcEpic contract so same-session `auto-implement` is unambiguously an exhaustive sequential driver over real ArcStep auto-implement.

Checklist (must all be done):
- Apply `$skill-authoring` and `$prompt-authoring`: treat this as an existing skill edit, keep the repair prompt-first, put durable rules in owning sections, avoid brittle heuristics, and do not add a runner/controller/script unless prompt guidance is proven insufficient.
- Update `skills/arch-epic/SKILL.md` to state that `auto-implement` handles one planned sub-plan at a time through real `$arch-step auto-implement <DOC_PATH>`, waits for ArcStep `Verdict (code): COMPLETE`, then waits for the epic critic `pass`.
- Update `skills/arch-epic/references/workflow-contract.md` so `auto-implement` carries readiness, real ArcStep invocation, missing/non-complete audit handling, critic gating, critic `incomplete` handling, continuation, and all-complete behavior.
- In `workflow-contract.md`, explicitly say native goal mode continues the real ArcStep implement/prove/audit loop until the audit block is COMPLETE or a true blocker stops progress; one `$arch-step auto-implement` invocation is not enough.
- Update `skills/arch-epic/references/arch-step-integration.md` so `planned` and `implementing` statuses cannot skip readiness, implementation-frontier work, clean audit, or critic pass, and so same-session `auto-implement` continues ArcStep on NOT COMPLETE audit instead of merely surfacing and waiting.
- Update `arch-step-integration.md` critic `incomplete` handling so same-session `auto-implement` keeps the sub-plan `implementing` and routes back through ArcStep unless evidence is unreadable or contradictory; it must not mark complete or advance.
- Update `skills/arch-epic/references/resume-semantics.md` so stored status is reconciled against current sub-plan proof and verdict truth before acting, and so resumed same-session `auto-implement` routes through the same continue-until-clean rules as the workflow contract.
- Update `skills/arch-epic/references/epic-doc-contract.md` so mutation/log examples and allowed status changes match the strict gates.

Verification:
- Re-read changed files.
- `rg` for strict gate language and stale weak wording.
- `rtk proxy npx skills check`.

Docs/comments:
- This phase changes shipped skill doctrine. No code comments expected.

Exit criteria (all required):
- No core ArcEpic surface allows a sub-plan to be marked `complete` from stored status, worklog optimism, local proof, or ArcStep audit alone.
- Every core ArcEpic surface says ArcStep clean audit precedes epic critic and epic critic `pass` precedes sub-plan `complete`.
- Stale readiness and NOT COMPLETE audit route back to `auto-plan` or `auto-implement` respectively.
- The resume-routing, `workflow-contract.md`, and `arch-step-integration.md` surfaces agree on same-session `auto-implement`: continue ArcStep until audit COMPLETE; do not stop at ordinary interactive "surface to user" wording unless there is a true blocker or unreadable evidence.
- Critic `incomplete` is represented in the workflow failure modes and status mapping.

## Phase 2 - Examples And Public Docs

Status: PLANNED

Work: Align examples and public docs so users and future agents learn the same strict same-session `auto-implement` behavior.

Checklist (must all be done):
- Update `skills/arch-epic/references/examples.md` to show `auto-implement` continuing ArcStep implement-loop until clean audit, then running critic, then advancing.
- Update `README.md` so the inventory and arch-epic command section describe strict sequential ArcStep implementation-frontier behavior.
- Update `docs/arch_skill_usage_guide.md` with the same public rule.
- Confirm spawned-harness `auto-run` remains clearly separate from same-session auto commands.

Verification:
- `rg` for public command examples and same-session/spawned-harness boundary.
- `rtk proxy npx skills check`.

Docs/comments:
- Public docs are touched only where the installed skill surface is described.

Exit criteria (all required):
- Public docs do not imply `auto-implement` is a one-call shortcut.
- Examples show the ordered sequence: all planned -> selected sub-plan -> readiness gate -> real ArcStep auto-implement until clean audit -> epic critic -> complete -> next sub-plan.
- Example 4 no longer teaches a single-invocation shortcut; it names repeat-until-clean behavior in native goal mode.

## Phase 3 - Verification, Completion Reviews, Commit, And Publish

Status: PLANNED

Work: Prove the plan and implementation against the requested gates, then commit, push, and publish across Amir's machines.

Checklist (must all be done):
- Run this plan through ArcStep receipt gate until `READY next=implement-loop`.
- Run Cursor Agent `composer-2.5-fast` fresh consult before implementation; require `VERDICT: pass`.
- Run `$plan-audit` before implementation; require a ready verdict.
- Implement through the `$plan-implement` lane with a concise implementation log.
- Run `rtk proxy npx skills check`.
- Run `rtk python3 -m unittest tests/test_arch_stage_gate.py`.
- Run `rtk python3 -m unittest tests/test_arch_epic_auto.py`.
- Run `rtk git diff --check`.
- Run Cursor Agent `composer-2.5-fast` completion consult after implementation; require `VERDICT: pass`.
- Run `$thermo-nuclear-code-quality-review`; fix any blocker.
- Commit only intended tracked/new files.
- Push current branch.
- Run `$amir-publish`.

Verification:
- Record commands, consult directories, verdicts, and review results in the implementation log.

Docs/comments:
- The plan, audit log, and implementation log are durable proof artifacts.

Exit criteria (all required):
- All requested review gates pass.
- Final commit is on `origin/main`.
- Remote install succeeds on all reachable `$amir-publish` hosts, with failures reported if any.
<!-- arch_skill:block:phase_plan:end -->

# 8) Verification Strategy

- Skill package validation: `rtk proxy npx skills check`.
- Existing deterministic tests: `rtk python3 -m unittest tests/test_arch_stage_gate.py` and `rtk python3 -m unittest tests/test_arch_epic_auto.py`.
- Whitespace diff check: `rtk git diff --check`.
- Plan readiness gate: `rtk python3 skills/arch-step/scripts/arch_stage_gate.py ready --doc docs/ARCH_EPIC_STRICT_AUTO_IMPLEMENT_GATES_2026-06-08.md`.
- Targeted grep/readback:
  - stale weak wording around `auto-implement` completion,
  - strict sequence language,
  - spawned-harness separation.
- External gates:
  - Composer25Fast plan consult,
  - `$plan-audit`,
  - Composer25Fast completion consult,
  - `$thermo-nuclear-code-quality-review`,
  - `$amir-publish`.

# 9) Consistency Pass

<!-- arch_skill:block:consistency_pass:start -->
## Consistency Pass

- North Star preserved: yes
- Requirements represented in phases: yes
- Existing pattern reused: yes
- Prompt-first and skill-authoring discipline preserved: yes
- New runner/controller/harness added: no
- ArcStep remains implementation owner: yes
- ArcEpic remains epic ordering/state/critic owner: yes
- Spawned-harness lane kept separate: yes
- Public docs included when installed skill surface changes: yes
- Verification gates explicit: yes
- Unresolved decisions: none
- Unauthorized scope cuts: none
- Decision-complete: yes
- Decision: proceed to implement? yes
<!-- arch_skill:block:consistency_pass:end -->

# 10) Decision Log

- 2026-06-08 Plan started from Amir's clarified intent: ArcEpic same-session `auto-implement` must have the same rigorous, gated methodology as ArcStep `auto-implement`, applied one sub-plan at a time at the epic level.
- 2026-06-08 Mechanism choice: prompt-first skill repair. Existing ArcStep implementation loop and ArcEpic critic plumbing are sufficient; no new same-session harness or script is planned.
- 2026-06-08 Composer25Fast plan consult turn 1 failed with four specification gaps: resume-routing conflict, critic `incomplete` owning-surface mismatch, `$skill-authoring` / `$prompt-authoring` not operationalized, and one-shot ArcStep invocation ambiguity. This revision assigns those repairs to concrete plan requirements and Phase 1/2 checklist items before `$plan-audit`.
- 2026-06-08 Composer25Fast plan consult turn 2 passed with high confidence. Chain: `/tmp/fresh-consult/arch-epic-strict-auto-implement-plan-20260608-SUqPqa`; session: `639eb03c-28b4-44e5-8330-a738651cacd3`. Verdict: pass; failure reasons: none.
- 2026-06-08 Composer25Fast completion consult turn 3 passed with high confidence. Chain: `/tmp/fresh-consult/arch-epic-strict-auto-implement-plan-20260608-SUqPqa`; session: `639eb03c-28b4-44e5-8330-a738651cacd3`. Verdict: pass; failure reasons: none. The consult found the implementation closes the resume-routing, critic-`incomplete`, prompt-first, and one-shot-completion gaps.
- 2026-06-08 Thermonuclear code quality review passed. Review found no structural regression, no new same-session runner/controller/script, no spawned-harness drift, no 1k-line file crossing, no ad-hoc code branching, and no clearer code-judo move than repairing the existing owning prompt surfaces.
