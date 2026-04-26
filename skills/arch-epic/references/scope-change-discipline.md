# Scope-Change Discipline: Approved Scope Is Locked

The epic critic runs after each sub-plan finishes and arch-step's audit
confirms code completion. Its unique job is to detect drift from approved
epic scope and force a scope-preserving response.

The rule is simple: the epic scope is the epic scope. Automatic mode must not
cut, narrow, park, drop, or move approved scope out of the epic. If a
requirement is present in the raw goal, approved Decomposition, sub-plan North
Star, Epic Requirement Coverage, Section 7 checklist, exit criteria, or
verification obligations, it must be implemented, carried by a named later
sub-plan, extended into the current sub-plan, or reported as blocked. Agent
judgment can choose where the work belongs; it cannot choose that the work no
longer matters.

This file teaches what to flag and what to ignore. The critic reads it. The
orchestrator reads it too, because the orchestrator decides how to preserve
scope after a finding.

## What Counts As Material Scope Drift

A discovery is material when it affects the decomposition or approved spec of a
sub-plan. Three patterns matter:

1. The sub-plan implementation revealed a new required surface that is not in a
   sub-plan's approved acceptance criteria. Example: sub-plan 1 shipped auth;
   the worklog shows session tokens need a background rotation job. The
   rotation job is not optional if the approved SSO behavior cannot stand
   without it.
2. The sub-plan implementation cut or downgraded approved behavior. Example:
   the phase plan listed "dashboard shows the last 30 days of audit events,"
   but the shipped code only shows 7 days. A Decision Log note written by an
   agent does not authorize that reduction.
3. The sub-plan implementation added unapproved product behavior. Example: the
   sub-plan said "use existing auth" but the shipped code added a new guest-mode
   bypass.

All three cause `verdict: scope_change_detected`.

## What Counts As Noise

A discovery is noise when it does not affect approved epic scope, the
decomposition, the sub-plan spec, or user-visible behavior promised by the plan.
The critic ignores it and does not emit a `discovered_items[]` entry.

Ignore:

- File renames during implementation.
- Internal helper refactors inside the declared sub-plan scope.
- Utility functions added to deduplicate code.
- Linter warnings suppressed or configuration tweaks.
- Dirty git working tree at audit time.
- Style choices inside the sub-plan's declared scope.
- Minor extra tests beyond what the phase plan required.
- A different third-party library choice if both serve the same contract and
  the North Star did not name a specific one.
- Observations such as "a WebSocket would be nicer than polling" when the
  approved North Star, Section 7 obligations, and gate are already satisfied.

Do not report nice-to-have observations as scope changes. Reporting them
creates a fake decision path and invites accidental scope cutting. If the item
is not required for approved scope, ignore it.

## Classifying A Discovered Item

When the critic finds material scope drift, it fills a `discovered_items[]`
entry:

```json
{
  "what": "one-sentence description of the scope-preserving work needed",
  "scope_relationship": "required_for_approved_scope",
  "recommendation": "extend_current"
}
```

`scope_relationship` is always `required_for_approved_scope` for new verdicts.
If the item is not required for approved scope, it is noise and should not
appear in `discovered_items[]`.

`recommendation` has only two valid values:

- `extend_current`: the item fits inside the current sub-plan's North Star and
  should be added to that sub-plan's Section 7 checklist and exit criteria
  before implementation continues.
- `new_sub_plan`: the item is a separate unit with its own North Star and
  should become a new arch-step sub-plan inserted into the epic.

There is no `defer` recommendation. There is no `drop` recommendation. There is
no `nice_to_have` classification.

## No Auto-Reduction Rule

Automatic mode never auto-applies a scope disposition that reduces or parks
scope. When the critic returns `verdict: scope_change_detected`, the
orchestrator halts and asks the user how to preserve the approved scope:

- extend the current sub-plan, or
- insert a new sub-plan.

If neither option can preserve the approved scope, the epic is blocked. The
orchestrator reports the blocker instead of marking the sub-plan complete.

Agent-written Decision Log entries are not approval to reduce scope. They are
evidence that a scope question exists. Only the user's original approved epic
scope and later visible user instructions define the scope; automatic children
do not get to shrink it.

## What The Orchestrator Tells The User

When the orchestrator halts on a scope change, it renders the critic's verdict
in plain English. The user sees:

```text
Sub-plan 2 (Build admin dashboard backed by SSO) is code-complete per arch-step.
The epic critic found one scope-preserving requirement that is not represented
in the approved sub-plan structure:

1. During implementation, the session store grew a new "locked" state to handle
   SSO revocation races. This is required for the approved SSO behavior to be
   safe, but it is not in any sub-plan's North Star or Section 7.
   Recommended: new_sub_plan.

Options:
  a. extend current sub-plan - add the locked-state behavior into this
     sub-plan's approved checklist and re-run implementation.
  b. new sub-plan - insert a new sub-plan before the next phase.

Which scope-preserving path should I use?
```

That format is the shape: concrete, scannable, one preservation decision at a
time. The user replies with one option or their own wording; the orchestrator
applies it and resumes.

## What The Orchestrator Does Not Do

- It does not park, drop, or treat approved scope as future work.
- It does not mark a sub-plan complete when approved requirements are missing.
- It does not treat an agent-written Decision Log entry as scope-reduction
  approval.
- It does not invent a compromise scope to keep automation moving.
- It does not report harmless nice-to-have observations as scope changes.
- It does not preemptively flag during implementation. Mid-implementation
  discoveries are handled by the worker's stop-line and arch-step doctrine.
  The epic critic is the cross-sub-plan guard.
