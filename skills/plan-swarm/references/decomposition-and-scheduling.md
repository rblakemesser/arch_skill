# Decomposition And Scheduling

The swarm ledger is schedule and evidence, not a competing plan. It is a
human-readable coordination aid that helps the parent agent decide which
workers can run in parallel.

## Slice Shape

Each slice needs:

- id and title
- goal
- source truth
- likely owning and adjacent areas
- dependencies
- likely collision risk
- parallelization strategy
- scarce resources
- proof needed
- assigned worker and session id when known
- status

Good slices are large enough for a capable worker to reason and small enough to
finish without owning the whole phase.

## Split By

- canonical owner boundary
- dependency boundary
- proof boundary
- replacement-before-deletion boundary
- scarce resource boundary
- collision risk

Do not split by one file per worker, arbitrary equal chunks, or tiny TODOs that
share one design decision.

## Wave Rules

- Launch slices whose dependencies are complete and whose edits are unlikely to
  collide.
- Do not launch two workers into the same unsettled design decision.
- Do not let multiple workers monopolize the same expensive test, simulator,
  browser, generator, or migration resource.
- Give tightly coupled work to one worker or run it serially.
- Run replacement paths before deletion or cleanup paths.
- Keep full-suite verification for a designated verification worker or parent
  checkpoint unless a worker has an explicit lease.

## Chunk Table

Record the current chunking in the `Current Phase Work Slices` table in
`swarm-ledger.md`. Each row should make the parallelization strategy visible:
why the slice can run in parallel now, why it is waiting, or why it should be
owned by one worker serially. If two slices share one unsettled design decision,
the table should show that relationship instead of pretending they are
independent.

## Defaults

- Cursor Agent implementation max parallelism: `4`.
- Codex or Claude implementation max parallelism: `2` unless the user pins a
  different value.
- Parent may reduce parallelism when the repo state is conflicted, proof is
  unclear, or workers are touching unexpectedly overlapping surfaces.
