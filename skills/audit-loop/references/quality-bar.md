# Audit Loop Quality Bar

## Strong triage

- critical paths are explicit
- priorities reflect real risk, churn, coverage, dead code, and duplication
- `SKIP` entries are deliberate and explained
- unavailable signals are recorded as `unknown`, not silently ignored

## Weak triage

- priority order follows file size, aesthetics, or guesswork
- the ledger has no clear critical paths
- `SKIP` means "did not feel like it"
- the same low-value area keeps returning with no justification

## Strong findings

- file anchors are concrete
- the description names the behavior or fragility clearly
- the proposed fix matches the actual finding
- dead code and duplication are treated as real cleanup work, not optional polish

## Weak findings

- vague "needs refactor" notes
- no file anchors
- broad design critiques not tied to a fixable risk
- test additions that only protect implementation details

## Strong stop decisions

- `CONTINUE` names a concrete next area
- `CLEAN` means there is no credible next pass worth the cost
- `BLOCKED` names the real blocker plainly

## Weak stop decisions

- `CONTINUE` with no next area
- `CLEAN` while obvious `P0` or `P1` work still exists
- `BLOCKED` when the real issue is simply lack of triage discipline
