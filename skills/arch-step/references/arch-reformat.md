# `reformat` Command Contract

Use this reference when the user runs `arch-step reformat`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for `# TL;DR`, `# 0)`, and the canonical sections the source doc must be mapped into.
- Treat the input doc as the source of truth for meaning-bearing content.

## Artifact sections this command reads

- the source doc in full
- any existing frontmatter, TL;DR, North Star, plan, decision notes, references, and open questions

## Artifact sections this command establishes or repairs

- the full canonical scaffold from `artifact-contract.md`
- `# TL;DR`
- `planning_passes`
- `# 0)` through `# 10)`
- `Appendix A` and `Appendix B` when needed

## Why this command exists

- recover the canonical full-arch artifact when the source doc has useful content but the wrong shape
- preserve meaning while restoring one doc that later commands can trust
- make TL;DR and Section 0 explicit enough that the rest of the workflow has a stable alignment lock

## Quality bar for what this command touches

- preserve all meaning-bearing content
- infer only from explicit source evidence
- mark uncertain synthesis as draft inference
- use appendices rather than dropping or hallucinating content
- normalize heading drift back to the canonical `arch-step` shape
- repair obvious contradictions when source content can be reconciled safely

## Hard rules

- Docs-only. Do not modify code.
- Do not rewrite from scratch.
- Preserve links, code blocks, tables, decisions, TODOs, and open questions.
- If content cannot be confidently placed, keep it in the output rather than dropping it.
- If `OUT=...` is provided, write to the new path and leave the input doc unchanged.
- Do not introduce new scope; only structure and lightly clarify existing content.

## Consistency duties before stopping

- TL;DR, Section 0, and the phase plan should not contradict each other after conversion.
- Preserve the strongest explicit source claims about scope, evidence, fallbacks, and sequencing.
- If the source doc is ambiguous, keep the ambiguity visible in draft form or appendices rather than hiding it.

## Conversion behavior

1. Read the source doc fully.
2. Create the canonical skeleton from `artifact-contract.md`.
3. Map existing material into the most appropriate canonical sections.
4. Prefer placing content once, unless duplication is the only safe way to avoid losing meaning.
5. Draft TL;DR and Section 0 from source evidence rather than invention.
6. Add:
   - `Appendix A) Imported Notes` for content that could not be confidently placed
   - `Appendix B) Conversion Notes` for high-level moves and remaining gaps
7. Preserve or insert the canonical `planning_passes` block.
8. Make one final consistency pass across TL;DR, Section 0, and Section 7.

## Stop condition

After rewriting the doc into canonical format:

- print the drafted TL;DR
- print the drafted North Star
- ask for confirmation or edits
- stop

## Console contract

- North Star reminder
- punchline
- output doc path
- drafted TL;DR
- drafted North Star
- ask for `yes/no` confirmation
