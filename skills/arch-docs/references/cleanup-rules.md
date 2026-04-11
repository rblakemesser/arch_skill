# Cleanup Rules

The bias is delete-and-consolidate, not add-and-preserve.

## Commit, then delete

- TEMP, DRAFT, WIP, OLD, or DEPRECATED files whose subject is already shipped, removed, or superseded
- duplicate docs when another doc covers the same topic better
- docs for features or systems that no longer exist
- empty or near-empty stubs
- obsolete working docs after their durable truth is promoted elsewhere

Before deleting a bounded batch of these docs:

- stage the docs in that delete batch
- create a backup git commit first
- do not stage unrelated dirty files elsewhere in the repo
- if the commit cannot be created, stop instead of deleting

## Consolidate then delete

- Merge the good parts into the canonical surviving doc.
- Delete the weaker duplicate in the same run.
- Do not leave a live redirect stub that only says "see other file." Those rot quickly.

## Plan and worklog retirement

- Treat plan docs, worklogs, investigation notes, and similar working artifacts as temporary unless they are transformed into the one canonical evergreen doc.
- Mine durable truth into evergreen docs first.
- If the plan doc can be transformed in place into the one clean evergreen doc, do that and remove the arch scaffolding.
- Otherwise fold the durable truth into better homes and delete the obsolete working docs.

## Dated doc retirement

- Treat launch notes, rollout docs, migration one-offs, completed audits, temporary investigations, incident-era notes, and similar point-in-time artifacts as disposable unless current readers still need them.
- Use `git log` when a doc looks time-bound or suspiciously untouched and the keep/delete call is unclear.
- Look for the last meaningful content change, not moves, renames, formatting churn, or mechanical edits.
- Keep the durable truth, not the moment-in-time wrapper. Fold forward what still matters, then delete the rest.
- Do not keep a doc just because it once mattered or because it feels safer to preserve it. Git is the archive.

## Reference repair

- After every delete or move, grep the repo for references to the deleted path.
- Fix or remove broken references in the same pass.
- Broken internal links are a docs-cleanup failure, not optional polish.

## Concision rules

- Remove history that is no longer needed to understand the current state.
- Remove hedging and filler.
- Remove examples that no longer run against the current codebase.
- Do not use fixed age thresholds as a stale-doc shortcut.
- If a sentence cannot be grounded confidently, delete it instead of keeping an aspirational guess.

## Ledger rule

- Use `.doc-audit-ledger.md` as temporary scaffolding only.
- It should include:
  - repo doc profile
  - inventory
  - topic map
  - deletions
  - fixes applied
  - final doc map while the pass is active
- Delete the ledger before the cleanup is declared complete.
