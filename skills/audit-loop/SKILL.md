---
name: audit-loop
description: "Run the standalone repo-audit workflow with a root audit ledger: find and fix real bugs, dead code, duplication, and high-value regression gaps. Use when the user wants a repo-wide audit pass, wants the agent to push on the biggest real unresolved risks instead of harvesting tiny safe fixes, or wants to leave the loop running until no credible audit work remains. Not for a single known bug, feature planning, or generic optimization loops."
metadata:
  short-description: "Repo-wide bug hunt and cleanup loop"
---

# Audit Loop

Use this skill when the job is to inspect a codebase for its biggest real unresolved risks, push on the strongest current risk front until it is materially reduced, and leave a truthful audit ledger behind.

## When to use

- The user wants a repo-wide audit pass rather than help with one already-known bug.
- The user wants to find and fix real bugs, dead code, duplication, or missing high-value tests in priority order.
- The user wants to run one manual pass now or leave the audit running in Codex until the worthwhile work is exhausted.

## When not to use

- The task is a concrete known bug, crash, regression, or Sentry issue. Use `bugs-flow`.
- The work is fixed-scope feature delivery or architecture planning. Use `arch-step`, `arch-mini-plan`, or `lilarch`.
- The task is an open-ended optimization or investigation loop where the path is unknown and the job is not primarily bug finding. Use `goal-loop` or `north-star-investigation`.

## Non-negotiables

- `_audit_ledger.md` at repo root is the source of truth. Add it to the root `.gitignore` immediately.
- Triage before code changes. Do not skip straight to editing because one suspicious line looks fixable.
- Start with critical paths and existing repo-native evidence. Record unavailable signals as `unknown` instead of auto-installing new tooling.
- Reduce the top unresolved risk materially. Do not cash out a pass on a tiny safe fix while a bigger justified problem still dominates the repo.
- Dead code deletion counts as a fix. Duplication on critical paths counts as real bug prevention work.
- It is acceptable and often necessary to touch multiple files, modules, and tests when they belong to the same risk story.
- Prefer behavior-level verification and integration coverage on critical paths. Do not write negative-value tests.
- Unrelated dirty or untracked files are not a blocker. Leave them alone unless they directly conflict with the current risk front or make verification unsafe.
- Default invocation with no mode is `run`.
- `review` is docs-only.
- `auto` is Codex-only and must fail loud when hook support or `codex_hooks` is missing.
- No auto commits. Keep the ledger truthful without relying on git history.

## First move

1. Read `references/ledger-contract.md`.
2. Read `references/shared-doctrine.md`.
3. Resolve the mode:
   - `run`
   - `review`
   - `auto`
4. Resolve repo root, root `.gitignore`, `_audit_ledger.md`, and `.codex/audit-loop-state.<SESSION_ID>.json` when in `auto`, with `SESSION_ID` taken from `CODEX_THREAD_ID`.
5. Read the matching mode reference and `references/quality-bar.md`.

## Workflow

### 1) `run`

- Create or repair `_audit_ledger.md` and the `.gitignore` entry.
- Refresh triage from critical paths, churn, coverage, dead-code signals, duplication signals, and explicit `SKIP` decisions.
- Pick the highest-priority unresolved risk front.
- Read the implementation before the tests, log findings, and fix the strongest justified work across that risk front.
- Verify the changes, update the ledger, and stop only when further useful work would require a genuinely different audit story, a new reconnaissance pass, or a real blocker.

### 2) `review`

- Stay docs-only.
- Repair the ledger if it is missing or malformed.
- Re-read the ledger and current repo state from fresh context.
- Set the controller verdict to `CONTINUE`, `CLEAN`, or `BLOCKED` and name the next risk front or blocker plainly.

### 3) `auto`

- Run Codex-only preflight for hooks and feature flags.
- Derive `SESSION_ID` from `CODEX_THREAD_ID`, then create or refresh `.codex/audit-loop-state.<SESSION_ID>.json`.
- Do not run the Stop hook yourself. After `auto` is armed, just end the turn and let Codex run the installed Stop hook.
- Run one truthful `run` pass.
- Let the installed Stop hook launch a fresh `review` pass and continue only while the verdict stays `CONTINUE` because real unresolved risk still remains.

## Output expectations

- Update `_audit_ledger.md` in every mode.
- Keep console output short:
  - audit North Star reminder
  - punchline
  - current risk front or verdict
  - evidence or tests run
  - next action

## Reference map

- `references/ledger-contract.md` - root ledger shape, controller block, status vocabulary, and cleanup lifecycle
- `references/shared-doctrine.md` - prioritization, fix discipline, and anti-patterns
- `references/run.md` - risk-front audit/fix pass
- `references/review.md` - fresh docs-only verdict pass
- `references/auto.md` - Codex-only controller contract and state file
- `references/quality-bar.md` - strong vs weak triage, findings, tests, and stop decisions
