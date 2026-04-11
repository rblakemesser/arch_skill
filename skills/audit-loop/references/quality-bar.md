# Audit Loop Quality Bar

## Strong triage

- critical paths are explicit
- major unresolved risk fronts are explicit
- priorities reflect real risk, churn, coverage, dead code, and duplication
- `SKIP` entries are deliberate and explained
- unavailable signals are recorded as `unknown`, not silently ignored

## Weak triage

- priority order follows file size, aesthetics, or guesswork
- the ledger has no clear critical paths
- the pass keeps cashing out on low-amplitude fixes while a larger risk front stays open
- `SKIP` means "did not feel like it"
- the same low-value area keeps returning with no justification

## Strong findings

- file anchors are concrete
- the description names the behavior or fragility clearly
- the proposed fix matches the actual finding
- dead code and duplication are treated as real cleanup work, not optional polish
- multiple related findings may be resolved together when that is what the risk front demands

## Weak findings

- vague "needs refactor" notes
- no file anchors
- broad design critiques not tied to a fixable risk
- test additions that only protect implementation details

## Strong stop decisions

- `CONTINUE` names a concrete next risk front
- `CLEAN` means there is no credible major unresolved pass worth the cost
- `BLOCKED` names the real blocker plainly

## Weak stop decisions

- `CONTINUE` with no next area
- `CLEAN` while obvious `P0` or `P1` work still exists
- `CLEAN` because one small patch landed even though the same larger risk front still has open justified work
- `BLOCKED` when the real issue is simply lack of triage discipline
