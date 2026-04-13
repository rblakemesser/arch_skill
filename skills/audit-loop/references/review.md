# `review` Mode

## Goal

Run a fresh, docs-only audit verdict pass that decides whether the exhaustive map is complete, whether the current ranking is still truthful, and whether a major unresolved risk front still justifies more work.

## Writes

- `_audit_ledger.md`
- root `.gitignore` when the ledger is missing and must be repaired

No product code changes are allowed in `review`.

## Procedure

1. Create or repair `_audit_ledger.md` and the `.gitignore` entry if they are missing.
2. Re-read:
   - controller block
   - Phase 1 triage
   - open findings
   - test additions
   - decisions log
3. Inspect current repo state from fresh context:
   - changed files
   - relevant tests, build checks, or scanner output when needed
   - whether the exhaustive map is complete
   - whether the current or next front comes from the ranked map
   - whether the latest pass actually reduced the top open risk
   - whether the same risk front still has justified unresolved work
   - whether the latest pass used proof proportional to the front's consequence and blast radius
   - whether audit-loop-added or materially rewritten tests make the protected behavior, why it matters, and the expected user-visible or externally observable outcome clear enough to catch misunderstanding later
   - treat unrelated dirty or untracked files as ordinary context, not as an automatic blocker
4. Set the controller block:
   - `CONTINUE` when a concrete worthwhile next mapping tranche or risk front remains
   - `CLEAN` when the map is complete, only fixed items or explicit `SKIP`s remain, and no credible major audit pass is justified
   - `BLOCKED` when the next move would be speculative, repeated, or stopped by a real blocker
5. Update `Last Review`.
6. Keep the ledger truthful about why the decision was made.

## Verdict rules

### `CONTINUE`

Use only when:

- the exhaustive map is not complete and a concrete next mapping tranche exists, or a concrete next risk front exists
- the current or next front is still justified by the priority matrix
- the current front still has unresolved work or the next front clearly dominates the repo
- the latest pass did not leave key new verification ambiguous or underexplained
- the next pass would not merely repeat the last failed idea

`Next Area` is required. It may name an unfinished mapping tranche, risk front, or problem cluster, not just a tiny local file.

### `CLEAN`

Use only when:

- the highest-priority unresolved risk fronts have been fixed or explicitly skipped
- the exhaustive map is complete
- no credible `P0`, `P1`, or justified `P2` audit pass remains
- rescanning would likely just relitigate prior `SKIP` decisions
- the loop is not merely stopping because the next useful work touches a broader surface

`Stop Reason` should be blank.

### `BLOCKED`

Use when:

- the next move depends on missing access, tooling, or evidence
- the failing baseline or current repo state makes the next pass unsafe
- the next pass would rerun the same idea without a changed lever
- the ledger is too weak to continue honestly without first repairing the investigation
- the only honest next move would change an existing product, API, or behavior contract instead of fixing a bug inside it
- the claimed risk reduction depends on new or materially rewritten tests whose intent is too unclear to trust

`Stop Reason` is required.

A dirty worktree by itself is not enough for `BLOCKED`. An incomplete map is also not enough for `BLOCKED`; use `CONTINUE` for unfinished mapping work. Use `BLOCKED` only when the current repo state directly conflicts with the next justified pass or makes verification unsafe.
