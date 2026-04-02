# Arch Step Shared Doctrine

Use this file for the cross-cutting planning doctrine shared across `arch-step` stages. This is the quality layer above block placement.

## Convergence rule

- `arch-step` always works toward one finished full-arch artifact.
- Local block ownership is real, but it is subordinate to artifact convergence.
- If a command updates one part of the plan and can see that nearby sections are now stale, it should repair the smallest safe set of contradictions before it exits.

## Repo-evidence-first question policy

- Answer everything discoverable from repo code, tests, fixtures, logs, docs, and tooling before asking the user.
- Allowed questions are narrow:
  - true product or UX decisions not encoded anywhere
  - external constraints not present in repo or docs
  - real doc-path ambiguity after best-effort resolution
  - missing access or permissions
- If a question is still necessary, say where you already looked first.
- Do not ask the user technical questions that code or docs can answer.

## Alignment checks before deeper work

The North Star is an alignment lock, not a mission statement.

- TL;DR should say what is changing and why.
- Section 0 should say what must remain true while we do it.
- Later commands should use those sections to resolve ordinary tradeoffs without re-asking the user.

Run these checks before any substantive planning or implementation step:

- North Star:
  - concrete and scoped
  - falsifiable claim, not vibes
  - smallest credible acceptance signal, preferably an existing check
- UX scope:
  - explicit in-scope and out-of-scope surfaces
  - no silent scope expansion
  - no contradiction with TL;DR, Section 0, or the phase plan

If North Star or UX scope is unclear or contradictory, stop for a quick doc correction before going deeper.

## Consistency repair doctrine

- Do not knowingly leave the plan internally contradictory just because the local section you owned is now correct.
- If target architecture changes, check TL;DR, Section 0, Section 1, Section 7, and Section 8 for stale claims.
- If sequencing or verification changes, check TL;DR, Section 0, Section 7, Section 8, and Section 10.
- If rollout or telemetry implications change, check Section 9 and Section 10.
- Prefer minimal truthful edits over broad rewrites.
- Record meaningful drift or approved exceptions in the Decision Log instead of silently rewriting history.

## Evidence philosophy

- Prefer the smallest credible signal.
- Prefer existing tests, typecheck, lint, build, instrumentation, or log signatures before new harnesses.
- If no existing programmatic signal is cheap and credible, use a short manual checklist.
- Manual QA is usually non-blocking until finalization and should not be mistaken for missing code.
- Avoid verification bureaucracy.

Negative-value defaults to avoid:

- deleted-code proof tests
- visual-constant or unstable-golden tests
- doc-inventory gates
- mock-only interaction tests with no behavior assertion
- bespoke harnesses or frameworks added just to create ceremony

## Architecture doctrine

- Code is ground truth.
- Prefer the most idiomatic existing repo pattern unless there is a concrete reason not to.
- Single source of truth is the default. Avoid parallel implementations, duplicate writers, and shadow contracts.
- Boundaries and invariants should be enforceable, not merely described.
- Prefer hard cutover, explicit deletes, and fail-loud boundaries over compatibility shims.
- Runtime fallbacks or shims are forbidden unless the plan explicitly approves them via `fallback_policy: approved` plus a Decision Log entry with a removal plan.

## Scope-authority defaults

- Treat the plan's scope as authoritative.
- If a related change is clearly in scope, include it and proceed.
- If it expands scope or meaningfully increases work, default to follow-up, defer, or exclude and keep going.
- Only stop and ask when the plan is internally contradictory, such as required work being declared out of scope.

## Warn-first sequencing

The recommended core flow is:

1. Deep dive pass 1
2. External research grounding when warranted
3. Deep dive pass 2 if the external research materially changes the plan
4. Phase plan
5. Implement

This sequence is a warn-first quality guard, not a hard blocker. Missing passes should be surfaced clearly but should not automatically stop useful planning work.

## Authoritative surfaces

- `DOC_PATH` is the one planning source of truth.
- `WORKLOG_PATH` is execution evidence, not a second plan.
- The phase plan is the single authoritative execution checklist.
- Helper blocks may sharpen or constrain the plan, but they must not create competing execution surfaces.
- The Decision Log is append-only and should capture real plan drift, approved exceptions, and meaningful sequencing changes.

## Pattern propagation

- When introducing a new SSOT, contract, lifecycle primitive, or non-obvious sharp edge, note where a short code comment should live at the canonical boundary.
- Prefer a few high-leverage comments over comment spam.
- The point is future drift prevention, not prose volume.

## Console behavior

- Start with a one-line North Star reminder.
- Then give the punchline plainly.
- Keep console output high-signal and natural.
- Put exhaustive details in `DOC_PATH` or `WORKLOG_PATH`, not in console output.

## Quality principle

Presence is not enough.

- A section is only useful when it is concrete enough for later phases to trust.
- A stage is only complete when the sections it owns are both present and strong enough to support downstream decisions.
- Consistency across sections matters as much as local section quality.
