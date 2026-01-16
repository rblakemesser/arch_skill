---
description: Audit code vs arch plan; add a canonical gaps & concerns list.
argument-hint: DOC_PATH=<path>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Compare the architecture doc at $DOC_PATH against the actual code in the current repo.
Find gaps, drift, missed call sites, and violations of conventions/patterns.
Update the doc with a **Gaps & Concerns List** using the exact format below.

OUTPUT FORMAT (append near the end, before Decision Log):
# Gaps & Concerns List (audit vs code)
## Summary
- Coverage: <what % or rough completeness>
- Primary risk areas:
  - <risk>

## Gaps Table
| Area | File | Symbol / Call site | Expected (per plan) | Actual (in code) | Impact | Fix | Status |
| ---- | ---- | ------------------ | ------------------- | ---------------- | ------ | --- | ------ |
| <module> | <path> | <fn/cls> | <plan intent> | <observed> | <risk> | <proposed> | open |

## Drift / Convention violations
- <rule violated> — <where> — <why it matters>

## Missed spots (unimplemented or partially implemented)
- <spot> — <symptom> — <what remains>

## Follow-ups / questions
- <question>
