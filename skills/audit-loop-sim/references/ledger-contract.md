# Audit Sim Ledger Contract

## Runtime artifacts

- `_audit_sim_ledger.md` lives at repo root.
- The root `.gitignore` must contain `_audit_sim_ledger.md` while the audit is active.
- `.codex/audit-loop-sim-state.<SESSION_ID>.json` exists only while Codex `auto` is armed, with `SESSION_ID` taken from `CODEX_THREAD_ID`.

## Ledger shape

The ledger is the single source of truth for exhaustive mapping, triage, findings, automation additions, explicit skips, and controller verdicts.

Keep this top block at the top of the file:

```md
# Audit Sim Ledger
Started: YYYY-MM-DD
Last updated: YYYY-MM-DD

<!-- audit_loop_sim:block:controller:start -->
Verdict: CONTINUE
Next Area:
Stop Reason:
Last Review:
<!-- audit_loop_sim:block:controller:end -->
```

Then keep these sections in order:

```md
## Phase 1: Triage (complete/in-progress)
### 1A: Journey And Surface Inventory
| # | Journey / Surface | App Surface | Why It Matters | Contract / Expected Outcome | Platform Scope | Current Real-App Proof | Proof Quality | Consequence if Wrong | Harness / Owner | Map Status |
|---|-------------------|-------------|----------------|-----------------------------|----------------|------------------------|---------------|----------------------|-----------------|------------|

### 1B: Automation And Harness Inventory
| # | Automation Surface | Covers | Platform | Entry / Command | Proof Quality | Gaps | Map Status |
|---|--------------------|--------|----------|-----------------|---------------|------|------------|

### 1C: Risk Front Ranking
| # | Risk Front | Journeys / Surfaces | Consequence | Proof Weakness | Fragility | Priority | Why Now |
|---|------------|---------------------|-------------|----------------|-----------|----------|---------|

### 1D: Proof Plan For Current Front
| Risk Front | Required Real-App Proof | Platform Closeout | Why This Depth | Status |
|------------|-------------------------|-------------------|----------------|--------|

## Phase 2: Findings
| # | File:Line | Type | Description | Fix | Status |
|---|-----------|------|-------------|-----|--------|

## Phase 3: Automation Additions
| # | Test/Harness | Covers | Platform | Why It Matters |
|---|--------------|--------|----------|----------------|

## Decisions Log
```

## Controller block rules

- Do not rename or remove the controller markers once the ledger is live.
- `Verdict` values are exactly:
  - `CONTINUE`
  - `CLEAN`
  - `BLOCKED`
- `Next Area` is required for `CONTINUE`.
- `Next Area` may name an unfinished mapping tranche, broader risk front, or problem cluster that spans multiple files or surfaces.
- `Stop Reason` is required for `BLOCKED`.
- `Last Review` is written by `review` in `YYYY-MM-DD` form.
- `review` owns the authoritative controller verdict used by `auto`.

## Findings vocabulary

- `Type` values:
  - `BUG`
  - `GAP`
  - `FLAKE`
  - `DRIFT`
  - `SMELL`
- `Status` values:
  - `OPEN`
  - `IN PROGRESS`
  - `FIXED (working tree)`
  - `FIXED (verified)`
  - `SKIP`
  - `BLOCKED`

## Priority matrix

- `P0` = high-consequence journey, surface, or risk front with weak, ambiguous, or missing real-app proof
- `P1` = high-consequence journey, surface, or risk front with partial proof or structural fragility worth fixing now
- `P2` = worthwhile but clearly secondary automation work with real proof gaps or repeated fragility
- `P3` = everything else
- `SKIP` = explicitly not worth investing in now after consequence and proof quality were evaluated

Primary journeys, onboarding, monetization, auth or session restore, core content progression, offline state, and platform ingress often dominate when the evidence supports that. Do not turn that into a rigid ranking table.

Every `SKIP` needs a reason in `## Decisions Log`.

## Tool-signal rules

- Use existing repo-native integration or device runners, simulator wrappers, QA commands, flow registries, and release-gate lanes first.
- Use git history, churn, telemetry, logs, or current automation artifacts when they sharpen keep or skip judgment.
- If a signal is unavailable, record `unknown` in triage and explain it in `## Decisions Log`.
- Do not auto-install new tools or create a parallel automation system just to satisfy the ledger.
- The exhaustive map must come from repo truth, not from canned category lists or grep-only shortcuts.

## Cleanup lifecycle

- When the workflow starts, ensure `_audit_sim_ledger.md` exists and `.gitignore` contains `_audit_sim_ledger.md`.
- Manual `run` leaves the ledger in place.
- `review` leaves the ledger in place.
- `auto` deletes `_audit_sim_ledger.md` only when the final verdict is `CLEAN`.
- On clean cleanup, remove the `_audit_sim_ledger.md` line from `.gitignore`.
- If the skill created `.gitignore` and it becomes empty after cleanup, delete `.gitignore`.
