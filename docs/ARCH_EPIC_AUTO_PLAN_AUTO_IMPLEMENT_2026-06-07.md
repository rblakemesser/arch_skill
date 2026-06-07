---
title: Arch Epic Auto Plan And Auto Implement
date: 2026-06-07
doc_type: implementation_plan
status: complete
---

# TL;DR

Add two explicit `arch-epic` doctrine commands: `auto-plan` and
`auto-implement`. `auto-plan` should create or repair every approved sub-plan
DOC_PATH and drive each one through the same receipt-gated `arch-step
auto-plan` readiness bar before any implementation starts. `auto-implement`
should then implement planned sub-plans in order through the existing
`arch-step implement-loop` / `auto-implement` contract and run the normal
epic critic before advancing. This is a prompt-first skill change, not a new
script, controller, or heuristic harness.

# North Star

When a user has an approved `arch-epic` decomposition, they can ask for:

- `arch-epic auto-plan`: plan all sub-plans completely first.
- `arch-epic auto-implement`: implement those planned sub-plans in order until
  the epic is complete or a real blocker appears.

The epic remains the orchestration ledger. Each sub-plan remains a real
`arch-step` plan. `arch-epic` must not replace `arch-step`'s planning or
implementation rigor with its own shortcut rules.

# Requirements

- Add `auto-plan` and `auto-implement` to the `arch-epic` public command
  surface and examples.
- Preserve the existing interactive mode.
- Preserve the existing explicit spawned-harness automatic lane for users who
  ask for role-based planner / implementation worker / critic subprocesses.
- Make the new commands same-session, native-goal friendly drivers over
  existing artifact truth.
- `auto-plan` must plan every sub-plan before implementation begins.
- `auto-plan` must use `arch-step` readiness proof:
  `research`, two `deep-dive` passes, `phase-plan`, `consistency-pass`, and
  `skills/arch-step/scripts/arch_stage_gate.py ready`.
- `auto-implement` must implement sub-plans in decomposition order and run the
  epic critic after each sub-plan's `arch-step` audit is clean.
- Add a `planned` sub-plan status so the epic can represent "planning complete,
  implementation not started."
- Avoid a new runner, state file, policy schema, polling loop, or model
  selection flow for these commands.
- Update `README.md` and `docs/arch_skill_usage_guide.md` because the installed
  skill surface changes.

# Non-Requirements

- Do not delete or redesign the existing `auto-run` spawned harness lane in
  this change.
- Do not add tests that assert exact skill wording.
- Do not make the new commands depend on archived command files.
- Do not teach `arch-epic` to hand-edit `arch-step` receipt blocks.
- Do not let `auto-implement` start if any non-complete sub-plan has not
  passed the `auto-plan` readiness bar.

# Code And Doctrine Anchors Read

- `skills/arch-step/SKILL.md`
- `skills/arch-step/references/arch-auto-plan.md`
- `skills/arch-step/references/arch-implement-loop.md`
- `skills/arch-step/references/full-auto.md`
- `skills/arch-step/scripts/arch_stage_gate.py`
- `skills/arch-epic/SKILL.md`
- `skills/arch-epic/references/workflow-contract.md`
- `skills/arch-epic/references/epic-doc-contract.md`
- `skills/arch-epic/references/arch-step-integration.md`
- `skills/arch-epic/references/resume-semantics.md`
- `skills/arch-epic/references/auto-harness-prompts.md`
- `skills/arch-epic/scripts/run_arch_epic.py`
- `README.md`
- `docs/arch_skill_usage_guide.md`

# Target Shape

## `arch-epic auto-plan`

`auto-plan` is an explicit epic-level planning driver. It runs only after the
decomposition is approved.

For the first sub-plan whose status is not `planned` or `complete`:

1. If the sub-plan has no DOC_PATH, assign the normal
   `docs/epic/<EPIC_SLUG_WITH_DATE>/PHASE_<NN>_<SUBPLAN_SLUG>_<YYYY-MM-DD>.md`
   path.
2. Create or repair that DOC_PATH by applying the `arch-step` `new` artifact
   contract directly, seeded from the approved decomposition, raw epic goal,
   prior sub-plan gates, and an Epic Requirement Coverage section. This is
   direct skill doctrine work in the same visible session, not a spawned
   planner worker and not a new script.
3. Treat the approved decomposition as enough authority only when the sub-plan
   North Star is a direct, unambiguous expansion of the approved epic scope. If
   two valid interpretations remain, stop and ask the user instead of guessing.
4. Invoke or continue `$arch-step auto-plan <DOC_PATH>`.
5. Require `skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`
   to exit 0 before marking the sub-plan `planned`.
6. In native goal mode, continue to the next sub-plan until every sub-plan is
   `planned` or `complete`, or until a real blocker stops the run. Outside
   native goal mode, perform one bounded transition and name the next exact
   command.

`auto-plan` must not invoke `implement-loop`, `auto-implement`, or spawned
automatic workers.

## `arch-epic auto-implement`

`auto-implement` is an explicit epic-level implementation driver. It requires
every non-complete sub-plan to be `planned` first.

For the first sub-plan whose status is `planned` or `implementing`:

1. Confirm the sub-plan passes
   `skills/arch-step/scripts/arch_stage_gate.py ready --doc <DOC_PATH>`.
2. Invoke or continue `$arch-step auto-implement <DOC_PATH>`; this is the same
   implementation-frontier contract as `implement-loop`.
3. If the sub-plan's `arch_skill:block:implementation_audit` is not COMPLETE,
   keep the sub-plan `implementing` and continue the implementation loop in
   native goal mode, or report the next bounded command outside goal mode.
4. When the `arch-step` audit is COMPLETE, run the existing epic critic.
5. Mark the sub-plan `complete` only after the epic critic passes.
6. In native goal mode, continue to the next planned sub-plan until all
   sub-plans are complete, or until a real blocker stops the run.

`auto-implement` must not plan new sub-plans. If planning is incomplete, it
should stop with `Use $arch-epic auto-plan <EPIC_DOC_PATH>`.

# Implementation Steps

1. Update `skills/arch-epic/SKILL.md`:
   - Add `auto-plan` and `auto-implement` to the trigger description,
     examples, public mode list, non-negotiables, and output expectations.
   - Explain the boundary between the new same-session drivers and the existing
     spawned-harness automatic lane.
   - Add `planned` to the status vocabulary where the entrypoint explains
     orchestration.

2. Update `skills/arch-epic/references/workflow-contract.md`:
   - Rename "six modes" to a neutral mode count.
   - Add `auto-plan` and `auto-implement` modes.
   - Make both modes one-transition-per-pass outside native goal mode and
     continuing commands inside native goal mode.
   - Keep `auto-run` as the role-based spawned-harness lane.

3. Update `skills/arch-epic/references/arch-step-integration.md`:
   - Add the `planned` status mapping.
   - Split interactive `planning` behavior from `auto-plan` behavior so the
     interactive run still proceeds directly into implementation, while
     `auto-plan` stops at `planned`.
   - State that `auto-implement` uses `$arch-step auto-implement <DOC_PATH>`
     or the exact same `implement-loop` contract.

4. Update `skills/arch-epic/references/epic-doc-contract.md`:
   - Add `planned` as an allowed sub-plan status.
   - Explain when `planned` is written.
   - Update log examples and validation text.

5. Update `skills/arch-epic/references/resume-semantics.md`:
   - Teach status derivation that a sub-plan with a ready `arch-step` receipt
     gate and no implementation worklog or implementation audit evidence is
     `planned`.
   - Keep the epic doc as the orchestration surface; do not add a state file.

6. Update `skills/arch-epic/references/examples.md`:
   - Add a small example showing all sub-plans moving to `planned` before
     implementation begins.

7. Update `README.md` and `docs/arch_skill_usage_guide.md`:
   - Add examples for `Use $arch-epic auto-plan ...` and
     `Use $arch-epic auto-implement ...`.
   - Summarize the difference between same-session auto commands and the
     spawned-harness automatic lane.

# Verification

- Run `npx skills check` because files under `skills/` changed.
- Re-read changed skill/docs surfaces.
- Use `rg` to confirm the public command examples, `planned` status, and
  same-session / spawned-harness boundary are consistent.
- Run targeted existing tests only if deterministic script behavior changes.
  This plan should not change `run_arch_epic.py`, so script unit tests are not
  required unless implementation touches the script.

# Risks And Safeguards

- Risk: `auto-plan` bypasses real North Star judgment.
  Safeguard: only treat approved decomposition as enough authority when the
  sub-plan North Star is a direct expansion of that approved scope; otherwise
  stop for the user.

- Risk: `auto-implement` starts before all plans are ready.
  Safeguard: require every non-complete sub-plan to be `planned`; otherwise
  route back to `auto-plan`.

- Risk: the new commands blur with existing `auto-run`.
  Safeguard: name the boundary clearly. `auto-plan` / `auto-implement` are
  same-session native-goal drivers over `arch-step`; `auto-run` is the
  role-based spawned-harness lane.

- Risk: doctrine becomes a hidden heuristic.
  Safeguard: add no new script, runner, policy table, model resolver, or state
  file. The skill tells the agent what to inspect, how to route, and what proof
  must exist.
