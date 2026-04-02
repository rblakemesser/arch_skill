# `overbuild-protector` Command Contract

Use this reference when the user runs `arch-step overbuild-protector`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for Section `0)`, Section `7)`, and helper-block expectations.
- The point of this command is mechanical scope discipline, not vague simplification advice.

## Artifact sections this command reads for alignment

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 7) Depth-First Phased Implementation Plan`
- in-scope and out-of-scope declarations
- definition of done

## Artifact sections or blocks this command updates

- `arch_skill:block:overbuild_protector`
- in `MODE=apply`, the existing phase-plan section in place

## Quality bar for what this command touches

- make scope decisions explicit
- keep the phase plan as the one authoritative execution checklist
- move out-of-scope work to intentional follow-ups rather than letting it hide in blocking tasks
- reject known bug vectors and overbuilt ceremony by default

## Hard rules

- Docs-only. Do not modify product code.
- Single SSOT: the phase plan remains the authoritative execution checklist.
- Resolve `DOC_PATH`.
- Use the North Star and in-scope or out-of-scope sections as scope authority.
- If no phase plan exists, stop and point to `phase-plan` rather than inventing a new format.

## Artifact preservation

- Preserve the canonical scaffold and keep the authoritative phase plan inside that scaffold.
- In `MODE=apply`, rewrite only the existing phase-plan section.
- If the doc is materially non-canonical, route to `reformat` before scope triage.

## Modes

- `MODE=report`:
  - write the triage block only
- `MODE=apply`:
  - write the triage block
  - rewrite the existing phase plan in place so only ship-blocking work stays blocking

Defaults:

- `MODE=report`
- `STRICT=1`

## Classification buckets

- `A` Explicit ask:
  - directly requested by the user or locked in TL;DR or in-scope sections
- `B` North-Star necessary:
  - required to satisfy the claim, done criteria, or explicit invariants
- `C` Parity necessary:
  - required to match an existing internal pattern or contract, with a real anchor
- `D` Risk mitigation necessary:
  - minimal work required to avoid a concrete regression or correctness failure
- `E` Optional quality:
  - good improvement, but not required to ship the North Star
- `F` Scope creep:
  - expands UX scope or adds unjustified work beyond the plan
- `G` Bug vector:
  - introduces brittle gates, long-lived complexity, or wrong-by-default safety theater

Tie-breakers:

- `STRICT=1`:
  - ambiguity defaults to follow-up, not include
- `STRICT=0`:
  - ambiguity defaults to optional, not include
- parity is never assumed without an anchor

## Update rules

Write or update:

- `arch_skill:block:overbuild_protector`

Capture:

- summary counts
- include ship-blocking items
- optional items
- follow-ups
- rejected bug vectors
- parity anchors
- notes about scope-contract gaps

If apply mode is used:

- preserve completed checkbox items
- remove follow-ups and rejected bug vectors from the phase plan
- label optional items as optional rather than blocking

## Console contract

- North Star reminder
- punchline
- `DOC_PATH` plus `MODE` and `STRICT`
- what was reclassified
- next action
