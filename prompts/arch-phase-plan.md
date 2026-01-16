---
description: Add a depth-first phased implementation plan to the architecture doc.
argument-hint: DOC_PATH=<path>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Insert a depth-first phased plan at the top of $DOC_PATH.
Each phase must include: Goal, Work, Test plan, Exit criteria, Rollback.
More phases are better than fewer. Keep them concrete.

OUTPUT FORMAT (insert at top):
# 7) Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; every phase has exit criteria + explicit test plan.

## Phase 0 — Baseline gates

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

## Phase 1 — <foundation>

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

## Phase N — <end state + cleanup>

* Goal:
* Work:
* Test plan:
* Exit criteria:
* Rollback:

