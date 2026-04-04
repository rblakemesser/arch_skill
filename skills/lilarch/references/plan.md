# Lilarch Plan Mode

## Goal

Write the minimal architecture and delivery plan needed to ship the feature cleanly.

## Required work

1. Read the doc and verify the task still fits 1-3 phases.
2. Gather the smallest useful repo evidence:
   - implementation anchors
   - representative call sites
   - tests or verification surfaces
   - prompt surfaces, native capabilities, and existing tool/file/context exposure when the feature is agent-backed
3. Write or repair:
   - `research_grounding`
   - `current_architecture`
   - `target_architecture`
   - `call_site_audit`
   - `phase_plan`
   - make the capability-first choice explicit before adding custom tooling for agent-backed behavior
4. Run the internal plan audit and write the result into `lilarch:block:plan_audit`.

## Plan shape

- Phase 1:
  - core implementation or cutover
- Phase 2:
  - dependent follow-through or validation
- Phase 3:
  - cleanup only if cleanup is real work, not wishful thinking

## Escalation rule

- If the plan wants a fourth phase, broad rollout logic, or heavy plan shaping, stop and escalate to `arch-step reformat`.
