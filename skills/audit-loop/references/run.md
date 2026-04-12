# `run` Mode

## Goal

Run one serious audit/fix pass that leaves `_audit_ledger.md` more truthful and materially reduces the biggest unresolved risk in the repo.

## Writes

- `_audit_ledger.md`
- root `.gitignore`
- product code when the pass reaches a justified fix
- tests only when they protect meaningful behavior
- comments in audit-loop-added or materially rewritten tests when needed to explain the why and expected experience or outcome

## Pass shape

One `run` pass owns one risk front. A risk front is the highest-priority unresolved problem cluster where the findings share either:

- one critical-path story
- one failure mode
- one verification surface

The pass may cross multiple files, modules, or tests when that is what it takes to reduce the same risk front honestly.

Unrelated dirty or untracked files are normal context, not a blocker. Leave them untouched unless they directly conflict with the current risk front or make verification unsafe.

Do not force the pass to stop after one finding or one patch when the same risk front still has clearly justified work.

Do stop when the next move would require a genuinely different risk story, a fresh audit cycle, or a different verification basis.

## Procedure

1. Create or repair `_audit_ledger.md` and the `.gitignore` entry.
2. Refresh `Started` and `Last updated` dates as needed.
3. Build or refresh Phase 1:
   - identify critical paths
   - measure churn
   - gather coverage signal when available
   - gather dead-code and duplication signals when available
   - write priorities and explicit `SKIP` decisions
4. Choose the highest-priority unresolved risk front from Phase 1.
5. Read the implementation in that risk front before reading its tests.
6. Log precise findings in Phase 2 with file anchors and finding type.
7. Read the existing tests and decide what verification is missing. If the pass adds or materially rewrites a test, leave comments in the test code that explain why the behavior matters and what correct user-visible or externally observable outcome should happen.
8. Fix the strongest justified work across that risk front:
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
   - `Next Area` or `Stop Reason` if the next unresolved risk front or blocker is obvious
11. Stop only when further useful work would become a different audit story, not merely because another file or module is involved.

## Triage reminders

- A critical-path file with low coverage is usually more important than a noisier utility.
- Dead code on a critical path is immediately worth deleting.
- Duplication on a critical path is immediately worth consolidating.
- A tiny isolated fix does not win if the same critical-path failure mode still has obvious unresolved work.
- Low-risk, low-churn, already-tested code is a good `SKIP`.
- Unrelated dirty or untracked files do not justify stopping or downgrading the pass on their own.

## Verification rules

- Prefer behavior-level verification over implementation-detail checks.
- Critical paths deserve at least one realistic integration signal where feasible.
- If the best evidence is a targeted test plus a broader existing suite, run both.
- When you add or materially rewrite a test, make the intent locally clear in the test code itself. Do not rely on the ledger alone to carry the why or the expected experience or outcome.
- If the repo has no credible automated signal for the fix, say so plainly in the ledger.
