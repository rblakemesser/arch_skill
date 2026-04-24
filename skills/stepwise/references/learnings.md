# Learnings ledger

Stepwise records durable process lessons in an orchestrator-local ledger. The
ledger exists to make repeated failure modes visible without turning them into
hidden worker doctrine.

## Location

Learnings live under the orchestrator repo:

```text
.arch_skill/stepwise/learnings/
├── index.jsonl
├── accepted.md
├── candidates/
├── accepted/
└── rejected/
```

Run directories stay ignored at `.arch_skill/stepwise/runs/`. Learnings are
intended to be visible and shareable.

## Entry schema

```json
{
  "schema_version": 1,
  "id": "LRN-YYYYMMDD-<hash>",
  "created_at": "2026-04-24T00:00:00Z",
  "updated_at": "2026-04-24T00:00:00Z",
  "status": "candidate",
  "applied_success_count": 0,
  "applied_null_count": 0,
  "source": {
    "run_id": "...",
    "step_n": 6,
    "try_k": 2,
    "diagnostic_path": "steps/6/try-2/diagnostic/"
  },
  "scope": {
    "owner_skill": "$lesson-copy-discipline",
    "failure_class": "bad-input-propagation-from-upstream",
    "surface": "learner-visible-copy",
    "support_skills": []
  },
  "observation": "what happened",
  "underlying_principle": "the owner-doctrine-backed rule",
  "applicability_test": "when to consult this",
  "contraindications": "when not to apply this",
  "process_change_suggestion": "what Stepwise should do differently",
  "promotion_target": "where this belongs if promoted",
  "fingerprint": "sha256(normalized scope + underlying_principle)"
}
```

`observation` says what happened. `underlying_principle` says what durable rule
survives. `applicability_test` and `contraindications` are both required; an
entry without both is a slogan, not a learning.

## Status model

`index.jsonl` is append-only. Current status derives from the latest event for
each id.

- `candidate`: first write.
- `accepted`: explicit user accept, same fingerprint recorded in two
  independent runs, or `applied_success_count >= 2`.
- `rejected`: user rejection or retrospective applicability failure.
- `superseded`: replaced by a sharper learning.
- `promoted`: human moved the principle into live doctrine.

Promotion is deliberate. A learning does not silently rewrite the skill.

Automatic acceptance is evidence of repeated usefulness, not automatic
doctrine. A candidate may become `accepted` after two recorded successful
applications. It becomes `promoted` only when a human or agent deliberately
moves the underlying principle into live skill doctrine.

## Consult discipline

Stepwise consults learnings at intake and repair authorship. The deterministic
script returns structural-scope matches. Stepwise decides applicability in
prose and records:

- why each accepted learning applies, or
- why a near-miss does not apply.

Near-misses are named and dismissed. This prevents stale process lore from
reappearing just because surface words match.

## Script ownership

`scripts/stepwise_learnings.py` owns deterministic ledger operations:

- `append --entry-file`
- `query --scope-json`
- `accept <id>`
- `reject <id>`
- `record-application <id> --outcome success|null --run-id <id>
  --diagnostic-path <path> [--note <text>]`
- `promote <id> [--target-path <path> --summary <text>]`
- `export-md`
- `sync-from-md`
- `fingerprint --scope-json --principle`

The script uses file locking for append operations. It does not decide whether
a learning applies to a run; Stepwise does that in the diagnostic record.

`record-application` updates counts after Stepwise has already decided whether
the learning helped. `success` means applying the learning materially improved
the diagnosis or repair. `null` means Stepwise considered it and learned that
it did not apply. If a candidate reaches `applied_success_count >= 2`, the
script marks it `accepted`.

## Promotion workflow

Promotion extracts the durable principle from a learning and places it in the
smallest owning live surface:

1. Read the accepted learning and its applicability/contraindication text.
2. Choose the owning doctrine target: usually `SKILL.md` for the core runtime
   contract, a Stepwise reference file for deeper workflow teaching, or a
   deterministic script when the learning is bookkeeping that language keeps
   getting wrong.
3. Edit the target so it teaches the principle and why it matters. Do not paste
   the incident as hidden lore, and do not turn one example into a routing
   shortcut.
4. Validate the owning surface.
5. Mark the learning promoted with `promote <id> --target-path <path>
   --summary <what changed>`.

## Reporting

`report.md` includes:

- accepted learnings applied this run,
- candidate learnings written this run,
- non-applicable near-misses considered and dismissed.
