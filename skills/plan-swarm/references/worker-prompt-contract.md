# Worker Prompt Contract

Prompt workers like capable colleagues entering cold. Give them enough truth to
move fast without turning them into brittle checklist executors.

## Include

- Mission: one slice outcome.
- Authoritative inputs: plan path, phase contract, swarm ledger slice, and
  relevant repo paths.
- Sibling context: other workers may be editing nearby code; do not revert
  unfamiliar changes.
- Success bar: behavior, tests, owner boundaries, cleanup, and proof needed.
- Freedom: workers may inspect adjacent owning code and make necessary
  task-relevant edits.
- Constraint: do not broaden product scope, push, stash, or revert unrelated
  work. Parent owns commit checkpoints unless this worker prompt explicitly
  assigns you one.

## Avoid

- Micromanaged file-by-file scripts.
- "Do not touch anything else" guardrails that prevent required adjacent fixes.
- Large copied plan sections when a path and heading is enough.
- Asking workers to run scarce full-suite checks without a lease.
- Treating workers as checklist executors. They are engineers responsible for
  real implementation within the slice mission.

## Required Footer

```text
STATUS: done | blocked | needs-parent | failed
SLICE: <slice id>
CHANGED FILES: <paths or none>
VERIFICATION: <commands/results or not run: reason>
PROOF: <phase requirements covered>
SESSION HEALTH: healthy | struggling | stuck | unknown
BLOCKERS: <none or concrete blocker>
FOLLOW-UP: <none or next recommended action>
SUMMARY: <one paragraph>
```
