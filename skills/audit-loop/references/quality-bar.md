# Audit Loop Quality Bar

## Strong triage

- the shipped code surface and the proof surface are mapped exhaustively
- critical paths and outcome-critical surfaces are explicit
- major unresolved risk fronts are explicit and come from the completed map
- priorities reflect consequence first, then proof weakness, then fragility signals such as churn, dead code, and duplication
- the proof plan and post-change audit focus are explicit before edits begin
- `SKIP` entries are deliberate and explained
- unavailable signals are recorded as `unknown`, not silently ignored

## Weak triage

- the map is sampled or obviously incomplete
- priority order follows file size, aesthetics, or guesswork
- the ledger has no clear consequence model or proof-surface inventory
- the pass picked something that looked fixable before the map was complete
- the pass keeps cashing out on low-amplitude fixes while a larger risk front stays open
- `SKIP` means "did not feel like it"
- the same low-value area keeps returning with no justification

## Strong findings

- file anchors are concrete
- the description names the behavior or fragility clearly and ties it back to the mapped consequence
- the proposed fix matches the actual finding
- dead code and duplication are treated as real cleanup work, not optional polish
- multiple related findings may be resolved together when that is what the risk front demands
- audit-loop-added or materially rewritten tests explain why the protected behavior matters and what correct user-visible or externally observable outcome should happen
- the final diff passes an explicit post-change audit for safety, downstream consequences, elegance, and duplication
- same-story duplication is converged instead of spread into a second copy

## Weak findings

- vague "needs refactor" notes
- no file anchors
- broad design critiques not tied to a fixable risk
- test additions that only protect implementation details
- new or materially rewritten tests whose comments only restate assertions or internal mechanics
- a "fix" that works only because the same logic or fallback handling was copied into another place
- a pass that never audited the resulting diff after the first test run

## Strong stop decisions

- `CONTINUE` names a concrete next mapping tranche or risk front
- `CLEAN` means the map is complete and there is no credible major unresolved pass worth the cost
- `CLEAN` means the latest editful pass also passed the post-change audit
- `BLOCKED` names the real blocker plainly

## Weak stop decisions

- `CONTINUE` with no next area
- `CLEAN` before the exhaustive map is complete
- `CLEAN` while obvious `P0` or `P1` work still exists
- `CLEAN` because one small patch landed even though the same larger risk front still has open justified work
- `CLEAN` because tests passed even though the resulting diff is still awkward, unsafe, or duplicative
- `BLOCKED` when the real issue is simply lack of triage discipline
