# `auto-plan` Command Contract

## What this command does

- take one approved canonical full-arch doc through the planning arc automatically
- arm one hook-backed multi-turn planning controller over `research`, `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`
- run only the first stage from the parent `auto-plan` pass, then rely on the installed Stop hook to feed one literal next command per later turn
- use the installed Codex runtime continuation support to move stage to stage
- stop after planning is complete and hand off cleanly to `implement-loop`
- keep `DOC_PATH` and loop state aligned while the controller is armed

## Planning North Star

Running `auto-plan` should end in one of two honest states:

- `ready`:
  - research grounding is present
  - deep-dive pass 1 is present
  - deep-dive pass 2 is present
  - the authoritative phase plan is present
  - the `consistency-pass` helper block is present, says `Decision-complete: yes`, and says `Decision: proceed to implement? yes`
  - no unresolved decisions remain in the authoritative artifact
  - no implementation has started
  - the final message says the doc is decision-complete and ready for `implement-loop`
- `blocked`:
  - the controller state is cleared
  - the blocker or early stop is explicit
  - the run stops instead of silently pretending the planning arc finished

User-facing invocation is just `auto-plan`. Do not run the Stop hook yourself. After the controller is armed, just end the turn and let Codex run the installed Stop hook. The quality bar for this controller is one stage per turn: the parent `auto-plan` pass runs only `research`, ends its turn, then the Stop hook feeds the next literal command on later turns. If the installed runtime support for real automatic sequencing is absent or disabled, this command must fail loud instead of pretending prompt-only chaining is the same feature.

## Shared references to carry in

- `artifact-contract.md`
- `shared-doctrine.md`
- `section-quality.md` for Section 3, Section 4, Section 5, Section 6, Section 7, and `planning_passes`
- `arch-research.md`
- `arch-deep-dive.md`
- `arch-phase-plan.md`
- `arch-consistency-pass.md`

## Inputs and `DOC_PATH` resolution

- treat the user ask as steering plus any planning preferences
- if the ask includes a `docs/<...>.md` path, use it
- otherwise resolve `DOC_PATH` from the normal `arch-step` defaults
- if the current session just created or most recently updated one canonical full-arch doc, prefer that doc
- if the doc path is truly ambiguous after best effort, ask the user to choose from the top 2-3 candidates

## Writes

- `DOC_PATH`
- `planning_passes`
- `.codex/auto-plan-state.<SESSION_ID>.json`

## Required runtime preflight

Before arming the controller, verify all of these:

- Codex runtime is the active host
- `~/.codex/hooks.json` contains the repo-managed `Stop` entry pointing at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`
- the installed `arch-step` runner exists at `~/.agents/skills/arch-step/scripts/arch_controller_stop_hook.py`
- `codex features list` shows `codex_hooks` enabled
- the target doc exists and frontmatter `status` is `active` or `complete`

If any check fails, name the broken prerequisite and stop.

Do not downgrade to prompt-only same-session chaining.
Do not preflight against a copied hook file under `~/.codex/hooks/`; that is not the install contract.

## Active planning-state contract

Resolve `SESSION_ID` from `CODEX_THREAD_ID`, then create `.codex/auto-plan-state.<SESSION_ID>.json` before the first research pass.

Minimal shape:

```json
{
  "version": 1,
  "command": "auto-plan",
  "session_id": "<SESSION_ID>",
  "doc_path": "docs/<PLAN>.md",
  "stage_index": 0,
  "stages": ["research", "deep-dive-pass-1", "deep-dive-pass-2", "phase-plan", "consistency-pass"]
}
```

Lifecycle:

- create or refresh it after preflight and before the research pass
- write the current `session_id` into the state file at arm time
- leave it armed while automatic planning is active
- only the Stop hook may advance `stage_index`, and only after the required canonical outputs for that stage were updated
- only the Stop hook may delete it after successful `phase-plan`
- delete it before stopping on a blocker, ambiguity, or other early stop so the controller does not re-enter falsely

## Hard rules

- docs-only; do not modify code
- this command is a bounded controller over `research`, `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, and `consistency-pass`; do not invent a second planning surface
- `auto-plan` is one command; if the required runtime continuation support is absent or disabled, fail loud
- use the same `DOC_PATH` for every stage in the controller
- the second `deep-dive` pass is required for this controller even when external research was not run
- in Codex, the installed runtime continuation path owns stage-to-stage continuation
- the initial parent `auto-plan` pass must run only `research`, then end its turn naturally
- later planning stages are hook-owned only; the parent pass must not self-run `deep-dive` pass 1, `deep-dive` pass 2, `phase-plan`, or `consistency-pass` in the same turn
- the parent pass must not clear successful controller state, claim the planning arc is complete, or emit the `implement-loop` handoff
- planning stages stay in the same visible Codex thread across separate turns; do not hide them in silent child planning runs or collapse them into one long same-turn chain
- if a stage stops before it updates the required canonical outputs, clear `.codex/auto-plan-state.<SESSION_ID>.json`, stop, and report that truth plainly
- if any stage uncovers an unresolved decision that repo truth cannot settle, clear `.codex/auto-plan-state.<SESSION_ID>.json`, stop, and ask the exact blocker question instead of continuing
- if `consistency-pass` leaves `Decision: proceed to implement? no`, the Stop hook clears `.codex/auto-plan-state.<SESSION_ID>.json`, stops, and reports that the doc is not ready for `implement-loop`
- after successful `consistency-pass`, the Stop hook clears `.codex/auto-plan-state.<SESSION_ID>.json`, stops, and says the doc is decision-complete and ready for `implement-loop`
- do not auto-run `external-research`, helper commands other than the required `consistency-pass`, `implement`, `implement-loop`, or `audit-implementation`

Wrong pattern:

- arm state, run `research`, then immediately self-run both `deep-dive` passes, `phase-plan`, and `consistency-pass` in the same assistant turn, then disarm the controller as if the hook had owned continuation

Right pattern:

- arm state, run exactly one stage, end the turn naturally, let the Stop hook feed the next literal command, and repeat until the hook clears state after successful `phase-plan`

## Stage completion signals

Use these signals before the Stop hook continues automatically:

- `research`:
  - `arch_skill:block:research_grounding` is present and was updated in this stage
- `deep-dive` pass 1:
  - `arch_skill:block:current_architecture` is present
  - `arch_skill:block:target_architecture` is present
  - `arch_skill:block:call_site_audit` is present
  - `planning_passes` marks `deep_dive_pass_1: done <YYYY-MM-DD>`
- `deep-dive` pass 2:
  - the same three architecture blocks are present
  - `planning_passes` marks `deep_dive_pass_2: done <YYYY-MM-DD>`
- `phase-plan`:
  - `arch_skill:block:phase_plan` is present and was updated in this stage
- `consistency-pass`:
  - `arch_skill:block:consistency_pass` is present and was updated in this stage
  - the helper block says `Decision-complete: yes`
  - the helper block says `Unresolved decisions: none`
  - the helper block says `Decision: proceed to implement? yes`
  - if the helper block says `Decision: proceed to implement? no`, the controller stops blocked instead of handing off

## Controller procedure

1. Read `DOC_PATH` fully and run the same alignment checks required by the planning commands it will invoke.
2. Run the runtime preflight. If the `~/.codex/hooks.json` entry, the installed runner, or `codex_hooks` is unavailable, fail loud.
3. Resolve `SESSION_ID` from `CODEX_THREAD_ID`, then create or refresh `.codex/auto-plan-state.<SESSION_ID>.json` for the current Codex session and `DOC_PATH`.
4. Run one truthful `research` pass using the `research` contract. The parent `auto-plan` pass stops there; it must not self-run later planning stages in the same turn.
5. Let Codex try to stop. The installed runtime should:
   - no-op when no active auto-plan state matches the current session
   - after `research`, feed `Use $arch-step deep-dive <DOC_PATH>` as deep-dive pass 1
   - after `deep-dive` pass 1, feed `Use $arch-step deep-dive <DOC_PATH>` as deep-dive pass 2
   - after `deep-dive` pass 2, feed `Use $arch-step phase-plan <DOC_PATH>`
   - after `phase-plan`, feed `Use $arch-step consistency-pass <DOC_PATH>`
   - after `consistency-pass` with `Decision-complete: yes` and `Decision: proceed to implement? yes`, clear state and stop with the `implement-loop` handoff message
6. On each hook-driven continuation, run the literal next planning command against the same `DOC_PATH`, keep the controller state aligned, and stop naturally after that one stage finishes.
7. If a stage ends early, does not update the required canonical outputs, uncovers a blocker question, or the next move is no longer credible, clear `.codex/auto-plan-state.<SESSION_ID>.json`, stop, and report that state plainly.
8. If `consistency-pass` ends with `Decision: proceed to implement? no`, clear `.codex/auto-plan-state.<SESSION_ID>.json`, stop, and report that the doc still needs planning repair before implementation.

## Console contract

- one-line North Star reminder
- one-line punchline
- ordinary stage output should stay visible because the planning commands run in the same Codex thread across separate turns
- the final stop message should name `DOC_PATH` and say it is decision-complete and ready for `implement-loop`, or print the exact blocker question that stopped the controller
