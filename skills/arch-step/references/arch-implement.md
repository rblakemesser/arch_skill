# `implement` Command Contract

Use this reference when the user runs `arch-step implement`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for Sections `0`, `5`, `6`, `7`, `8`, `WORKLOG_PATH`, and `implementation_audit`.
- This command owns execution truth, not just code edits. Code, plan, and worklog must stay aligned.

## Artifact sections this command reads for alignment

- the full plan doc
- especially `# 0)`, `# 5)`, `# 6)`, `# 7)`, and `# 8)`
- helper blocks that introduce real obligations

## Artifact sections or blocks this command updates

- product code
- `WORKLOG_PATH`
- phase status in the plan
- Decision Log when the plan meaningfully drifts

## Quality bar for what this command touches

- implement systematically from the phase plan
- keep the plan current as reality changes
- keep implementation completeness visible via a lightweight ledger mindset
- use value-driven verification, not ceremony
- do not let code progress outrun the plan artifact

## Hard rules

- Resolve `DOC_PATH`.
- Never implement directly on `main` or the default branch.
- Read `DOC_PATH` fully before changing code.
- Read `artifact-contract.md` and `shared-doctrine.md` before changing code.
- Derive implementation obligations from the strongest planning artifacts:
  - phase tasks
  - call-site audit
  - migration notes and delete lists
  - include items from follow-through sweeps
- Reconcile those obligations at phase boundaries.
- No fallbacks or shims unless the doc explicitly approves them.
- If the doc is materially non-canonical, repair it or route to `reformat` before treating it as the source of truth.

## Quick alignment checks

Before meaningful code changes:

- North Star is concrete and scoped
- UX in-scope and out-of-scope are explicit
- the phase plan is real enough to execute

If these are contradictory, stop for a quick doc edit before continuing.

## Implementation ledger discipline

- Keep a compact in-memory ledger of in-scope obligations.
- Each obligation should be concrete enough to classify later as:
  - done
  - blocked
  - deferred
  - still todo
- This is working memory, not a second plan doc. Only write it down when it materially helps explain status or blockers.

## Warn-first preflight

- Check `planning_passes` before coding.
- If recommended earlier planning passes are incomplete or unknown, warn clearly but continue.
- Respect North Star and UX scope. Do not wing it.

## Execution discipline

- Follow the phase plan in order.
- At phase boundaries, re-check North Star, UX scope, and invariants.
- If sequencing or assumptions materially drift, update the plan and append a Decision Log entry.
- Do not silently drop obligations because the happy path works.
- If a planned item is truly out of scope, record that explicitly with rationale.

## Verification discipline

- After each meaningful chunk, run the smallest credible programmatic signal.
- Prefer existing checks before adding new tests or harnesses.
- Write tests only when they buy real confidence.
- Avoid negative-value tests and brittle proof machinery.
- Defer manual QA and UI automation to finalization by default.
- Add short boundary comments for new SSOTs or tricky gotchas when they would genuinely prevent future drift.

## Worklog contract

`implement` owns `WORKLOG_PATH`:

- derive it from `DOC_PATH`
- create it if missing
- add plan or worklog cross-links
- append short phase progress updates

Preferred worklog entry shape:

```text
## Phase <n> (<phase name>) Progress Update
- Work completed:
  - <item>
- Tests run + results:
  - <command> — <result>
- Issues / deviations:
  - <issue>
- Next steps:
  - <step>
```

## Finish criteria

- all phases or checklist items needed for this run are resolved
- every in-scope obligation is either done, blocked, or explicitly deferred with rationale
- the North Star is satisfied by code and evidence
- the plan reflects reality

## Final output contract

The console close-out must say whether the run is:

- `complete`
- or `partial`

If `partial`, name unresolved ledger items plainly.
