# `review` Mode

## Goal

Run a fresh, docs-only automation verdict pass that decides whether a major unresolved real-app automation risk front still justifies more work, or whether the loop should stop clean or blocked.

## Writes

- `_audit_sim_ledger.md`
- root `.gitignore` when the ledger is missing and must be repaired

No product code changes are allowed in `review`.

## Procedure

1. Create or repair `_audit_sim_ledger.md` and the `.gitignore` entry if they are missing.
2. Re-read:
   - controller block
   - Phase 1 triage
   - open findings
   - automation additions
   - decisions log
3. Inspect current repo state from fresh context:
   - changed files
   - relevant automation files, runner output, build checks, or logs when needed
   - whether the latest pass actually reduced the top open automation risk
   - whether the same automation risk front still has justified unresolved work
   - whether a cross-platform front still needs Android confirmation before it can honestly be called done
4. Set the controller block:
   - `CONTINUE` when a concrete worthwhile next automation risk front remains
   - `CLEAN` when only fixed items or explicit `SKIP`s remain and no credible major automation pass is justified
   - `BLOCKED` when the next move would be speculative, repeated, or stopped by a real blocker
5. Update `Last Review`.
6. Keep the ledger truthful about why the decision was made.

## Verdict rules

### `CONTINUE`

Use only when:

- a concrete next automation risk front exists
- that risk front is still justified by the priority matrix
- the current front still has unresolved work or the next front clearly dominates the app
- the next pass would not merely repeat the last failed idea

`Next Area` is required. It may name a real-app automation risk front or problem cluster, not just a tiny local file.

### `CLEAN`

Use only when:

- the highest-priority unresolved automation risk fronts have been fixed or explicitly skipped
- no credible `P0`, `P1`, or justified `P2` automation pass remains
- rescanning would likely just relitigate prior `SKIP` decisions
- the loop is not merely stopping because the next useful work touches a broader automation surface
- any cross-platform front that was iterated on iOS has a credible Android closeout when Android still matters for that story

`Stop Reason` should be blank.

### `BLOCKED`

Use when:

- the next move depends on missing access, tooling, or evidence
- the failing baseline or current repo state makes the next pass unsafe
- the next pass would rerun the same idea without a changed lever
- the ledger is too weak to continue honestly without first repairing the investigation
- the remaining work would require inventing a parallel automation system instead of using the repo's existing surfaces

`Stop Reason` is required.
