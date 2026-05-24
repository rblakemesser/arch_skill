# Workflow Contract

`plan-swarm` turns one approved plan phase into a parallel implementation loop.
It does not write a new plan or broaden the requested boundary.

## Parent Agent Owns Orchestration

- Interpret the plan phase and applicable Definition of Done.
- Recover missing execution detail from owning code, tests, schemas, generated
  artifacts, and current behavior.
- Write the phase contract and swarm ledger next to the plan.
- Use `$agent-delegate` to launch and resume implementation workers.
- Write worker, arbiter, and repair prompts with prompt-authoring discipline.
- Inspect worker reports, changed files, and proof after every batch.
- Coordinate expensive validation so workers do not stampede the same resource.
- Decide whether a review finding is accepted, rejected, or deferred.
- Decide whether to resume a worker, spawn fresh, pause, or ask the user.

## Coordination Shape

Parallelism is part of the parent agent's normal work: reason about
independence, launch workers with the existing delegation skill, inspect the
real worktree, and keep a human ledger. Any optional helper belongs below that
judgment layer as a narrow utility, such as a blank ledger template or stale
wording check.

## Lifecycle

1. Intake: plan path, phase, stop boundary, work root, implementation policy,
   review policy, and max parallelism.
2. Phase contract: source-of-truth requirements and proof obligations.
3. Swarm ledger: independent/dependent slices, likely collisions, scarce
   resources, assigned workers, session ids, and proof needed.
4. Implementation batches: launch independent slices in parallel through
   `$agent-delegate`.
5. Merge/evidence check: read worker reports and inspect repo state.
6. Arbiter loop: delegated observation-only review against the phase contract.
7. Thermonuclear gate: strict maintainability review and triage.
8. Final report: evidence, findings, remaining gaps, and stop at boundary.

## Stop Discipline

- Stop after the named phase unless the user asked for a phase range or whole
  plan.
- Whole-plan final review is only for whole-plan completion or explicit final
  signoff.
- Do not use worker success footers as completion proof by themselves.
