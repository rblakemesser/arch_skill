# Audit Loop Shared Doctrine

## Philosophy

- Critical paths first. Missing coverage on payments, auth, persistence, or permissions matters more than polishing a safe utility.
- Audit-loop exists to reduce the biggest real risks, not to harvest easy wins.
- Dead code is a bug waiting to happen. Delete it instead of preserving it.
- Duplication is deferred breakage. Consolidate one source of truth where the duplication matters.
- Tests exist to protect meaningful behavior. Coverage is a trailing indicator, not the product.
- Leave the codebase lighter than you found it when the evidence supports deletion or simplification.

## Triage order

1. Identify 5-10 critical paths first.
2. Measure recent churn.
3. Measure coverage on the critical paths, when coverage tooling already exists.
4. Scan for dead code and explicit fragility markers.
5. Scan for duplication.
6. Write the priority and explicit `SKIP` decisions into the ledger before coding.

## Fix discipline

- Read the code before the tests.
- Work one unresolved risk front at a time, not one arbitrary line item at a time.
- It is acceptable and expected to fix multiple findings together when they share one failure mode, critical path, or verification story.
- Do not block on unrelated dirty or untracked files. Leave them alone unless they directly conflict with the current risk front or make verification unsafe.
- Do not yield just because the next fix touches a second file, module, or test surface.
- Stop when the next credible move would require a different risk story, a new audit cycle, or verification that no longer belongs to the same front.
- Delete dead code boldly. Git is the history.
- Extract duplication into one well-named shared path. Do not build a framework.
- Prefer integration coverage on critical paths. Add unit tests only when the logic is best isolated there.
- Do not write a test for code you are deleting.

## Existing-tool guidance

- Churn baseline:
  - `git log --since="6 months ago" --pretty=format: --name-only | sort | uniq -c | sort -rn | head -40`
- Explicit fragility markers:
  - `rg -n "TODO|FIXME|HACK|XXX|DEPRECATED"`
- Example optional coverage or scanner commands when they already fit the repo:
  - `npx jest --coverage --coverageReporters=json-summary`
  - `pytest --cov=src --cov-report=json`
  - `npx ts-prune`
  - `npx knip`
  - `npx jscpd . --min-lines 6`
  - `vulture src/`
  - `pylint --disable=all --enable=duplicate-code src/`

Record `unknown` instead of auto-installing any of these.

## Anti-patterns

- Chasing 100 percent coverage.
- Adding a test for every function regardless of risk.
- Refactoring an entire module because one smell was noticed during audit.
- Spending the pass on a neat tiny fix while a larger justified critical-path risk is still open.
- Spending the pass on a flaky low-priority test instead of the highest-risk open area.
- Sneaking in formatting, linting, types, or tooling side quests that are not required by the finding.
- Pretending a low-value assertion is meaningful because it makes the coverage number move.
