# `run` Mode

## Goal

Run one bounded audit/fix pass that leaves `_audit_ledger.md` more truthful and the repo meaningfully safer.

## Writes

- `_audit_ledger.md`
- root `.gitignore`
- product code when the pass reaches a justified fix
- tests only when they protect meaningful behavior

## Pass shape

One `run` pass owns one coherent area. A coherent area is the highest-priority open surface where the findings share either:

- one implementation surface
- one failure mode
- one verification surface

Do not force the pass to stop after one finding when the evidence says the same area needs two or three tightly related fixes.

Do stop when the next move would switch to a different area or require a fresh audit cycle.

## Procedure

1. Create or repair `_audit_ledger.md` and the `.gitignore` entry.
2. Refresh `Started` and `Last updated` dates as needed.
3. Build or refresh Phase 1:
   - identify critical paths
   - measure churn
   - gather coverage signal when available
   - gather dead-code and duplication signals when available
   - write priorities and explicit `SKIP` decisions
4. Choose the highest-priority open area from Phase 1.
5. Read the implementation in that area before reading its tests.
6. Log precise findings in Phase 2 with file anchors and finding type.
7. Read the existing tests and decide what verification is missing.
8. Fix the coherent work package for that area:
   - bug fix
   - dead-code deletion
   - duplication extraction
   - high-value test addition
9. Verify:
   - run the smallest targeted signal that proves the fix
   - run the broader relevant suite when that signal exists and is credible
10. Update:
   - finding status
   - test additions
   - `Last updated`
   - `Next Area` or `Stop Reason` if the next move is obvious
11. Stop before drifting into a second area.

## Triage reminders

- A critical-path file with low coverage is usually more important than a noisier utility.
- Dead code on a critical path is immediately worth deleting.
- Duplication on a critical path is immediately worth consolidating.
- Low-risk, low-churn, already-tested code is a good `SKIP`.

## Verification rules

- Prefer behavior-level verification over implementation-detail checks.
- Critical paths deserve at least one realistic integration signal where feasible.
- If the best evidence is a targeted test plus a broader existing suite, run both.
- If the repo has no credible automated signal for the fix, say so plainly in the ledger.
