# Output Contract

Every review saves a disk artifact under:

```text
/tmp/exhaustive-code-review/<scope-slug>-<timestamp>/
```

The artifact must be readable without chat history. It should contain these
files:

```text
target.md
coverage.md
findings.md
verdict.md
```

Do not add a runner state file, machine protocol, generated schema, or workflow
ledger. These are review notes for a human and future agent to inspect.

## `target.md`

Record:

- review target in the user's words
- resolved scope: worktree, branch diff, commit range, explicit paths,
  plan-scope, or completion claim
- baseline and head/current state when known
- local instruction and convention files read
- important exclusions or unresolved target ambiguity

## `coverage.md`

Record what was reviewed:

- touched files
- changed hunks
- touched symbols
- touched abstractions and canonical owners
- relevant callers, readers, writers, side doors, and old paths
- behavior or feature surfaces
- tests, fixtures, proof, docs, examples, comments, schemas, generated
  artifacts, prompts, config, telemetry, stable IDs, install surfaces, and
  package metadata when relevant
- native parallel agent usage summary
- known coverage gaps

Keep this as prose and compact lists. It is not a formal checklist engine.

## `findings.md`

Use this shape for each finding:

```markdown
### [BLOCKING|NON-BLOCKING] <short title>

- File: <repo-relative path>
- Symbol / line: <symbol or line>
- Risk: <concrete risk in plain language>
- Evidence: <diff, file, child report, command output, source anchor, or "see file">
- Repair target: <what must change, without writing the patch>
- Review pattern: <catalog pattern>
```

Rules:

- Findings must be tied to changed code or the requested review scope.
- Findings must cite evidence the reviewer actually read.
- Do not include suggested patch blocks.
- Do not include generic style advice.
- Empty findings are valid.

## `verdict.md`

Use one verdict:

- `approve`: exhaustive review completed and no blocking findings were found
- `approve-with-notes`: exhaustive review completed with only non-blocking
  findings
- `not-approved`: blocking findings exist
- `coverage-incomplete`: the review could not honestly cover the requested
  scope

Use this shape:

```markdown
# Exhaustive Code Review Verdict

VERDICT: approve | approve-with-notes | not-approved | coverage-incomplete

## Blocking Findings

<findings or "No blocking findings.">

## Non-Blocking Findings

<findings or "No non-blocking findings.">

## Coverage Summary

- Scope reviewed:
- Native parallel agents:
- Files/hunks/abstractions covered:
- Side doors and adjacent surfaces:
- Proof/docs/generated/prompt surfaces:
- Coverage gaps:

## Next Action

<one exact repair, rerun, or coverage action>
```

## Chat Reply

After saving the artifact, reply briefly:

- verdict
- blocking findings, if any
- notable non-blocking findings, if material
- artifact path
- one next action from the review

Do not prescribe the user's broader workflow.
