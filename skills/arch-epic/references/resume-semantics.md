# Resume Semantics: Every Invocation Is A Resume

The skill does not have a dedicated `resume` command. Every invocation of
`$arch-epic` reads the epic doc, reads the relevant sub-plan docs and automatic
run artifacts, figures out where the epic is, does the next action, and ends the
turn. "Pick up where we left off" is the only mode of operation.

## The Re-entry Routine

Every turn the skill runs this sequence:

1. Identify the epic doc.
   - If the user named an explicit path, use it.
   - If session context has a recently touched epic doc, use it and announce which one.
   - Otherwise, look for `EPIC_*.md` files with `doc_type: epic` in frontmatter. If there is exactly one active or halted epic, propose it. If there are several, list them and ask the user to pick. If there are none, treat this as a fresh `start`.
2. Validate the epic doc per `epic-doc-contract.md`. On validation failure, print the exact problem and ask for artifact repair. Do not auto-repair.
3. Compute each sub-plan's current Status by cross-referencing:
   - the stored Status in the Decomposition
   - the sub-plan DOC_PATH frontmatter when it exists
   - planning markers such as `arch_skill:block:research_grounding`, architecture blocks, `arch_skill:block:phase_plan`, and `arch_skill:block:consistency_pass`
   - the `arch_skill:block:implementation_audit` block when present
   - automatic-mode run state and child artifacts under `.arch_skill/arch-epic/auto/<epic-slug>/run-<ts>/` when `auto_execution` is present
4. If the stored Status disagrees with observed doc truth, update the stored Status before acting and append an Orchestration Log entry naming the discrepancy.
5. Route per `arch-step-integration.md`.
6. End the turn. The next turn re-runs the same routine.

## State Authority

Interactive mode does not add an `arch-epic`-owned state file. The epic doc is
the orchestration surface, and sub-plan DOC_PATHs are the implementation
contracts.

Automatic mode intentionally owns spawned harnesses outside arch-step's visible
session. It writes a compact `state.json` plus child artifacts under
`.arch_skill/arch-epic/auto/<epic-slug>/run-<ts>/`. That run state is
operational evidence, not a competing source of product truth: the epic doc
remains the approved goal/decomposition/decision surface, and sub-plan DOC_PATHs
remain the implementation contract.

This also means resuming works across CLI restarts. There is no volatile cache
in RAM that disappears between sessions; the disk is the state.

## Disagreements Between Stored Status And Observed Reality

The most common cause: a previous turn wrote a Status update, then the user
edited the doc or invoked arch-step commands manually. When reading in step 3
above, the skill treats observed DOC_PATH truth as authoritative and updates the
stored Status.

Example:

- Stored Status: `planning`.
- Observed: `arch_skill:block:implementation_audit` says `Verdict (code): COMPLETE`.
- Action: update stored Status to `implementing`, then advance per the Status `implementing` + audit COMPLETE rule by running the epic critic.
- Log: `Sub-plan N stored status was 'planning' but observed doc truth indicates implementation is complete. Updating and running critic.`

The log entry is important because the user reading the epic later sees the
reconciliation happened and why.

## Natural Phrasing

The skill's description field and `When to use` include the natural phrasings
that map to this single re-entrant pass:

- "continue my epic"
- "keep going on <topic>"
- "pick up where we left off on the <goal> epic"
- "resume <docs/EPIC_*.md>"
- "status of my epic"
- "what's left on this epic?"

Status-query phrasings trigger `summary` mode. Everything else triggers the
re-entry routine.

## What The Skill Does Not Do On Resume

- Re-ask decomposition approval if `sub_plans_approved: true`.
- Re-ask per-sub-plan North Star if arch-step's DOC_PATH has `status: active`.
- Re-run the epic critic on a sub-plan already marked `complete`.
- Restart a sub-plan from scratch because something looks weird. If something looks weird, surface it with a specific question, not a silent reset.
