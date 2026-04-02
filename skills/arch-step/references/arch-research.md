# `research` Command Contract

Use this reference when the user runs `arch-step research`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for Sections `0`, `2`, and `3`.
- Carry forward the strict question policy, alignment checks, and evidence philosophy from `shared-doctrine.md`.

## Artifact sections this command reads for alignment

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 2) Problem Statement`
- any existing `# 3) Research Grounding`

## Artifact sections or blocks this command updates

- `# 3) Research Grounding (external + internal “ground truth”)`
- `arch_skill:block:research_grounding`

## Quality bar for what this command touches

Good research looks like:

- internal ground truth with concrete file paths and why they are authoritative
- reusable internal patterns so the plan does not reinvent them
- optional external anchors with explicit adopt or reject logic
- open questions framed as evidence needed, not vague TODOs

Research is weak when it is generic, unanchored, cargo-culted, or disconnected from the plan.

## Consistency duties beyond local ownership

- If research disproves an assumption already stated in TL;DR or Section 0, repair the smallest clearly stale claim so the doc stays honest.
- If research materially changes likely architecture or verification choices, note that plainly and point the next move to `deep-dive` or `phase-plan` as appropriate.
- Do not rewrite Sections 4 through 8 here, but do not leave obvious contradictions unmarked.

## Hard rules

- Docs-only. Do not modify code.
- Resolve `DOC_PATH`.
- Respect the strict question policy from `shared-doctrine.md`.
- If the North Star or UX scope is unclear or contradictory, pause for a quick doc edit before continuing.
- If repo evidence reveals likely code changes, write them into `DOC_PATH` as anchored plan implications. Do not implement them here.

## Artifact preservation

- Preserve the canonical scaffold when it already exists.
- If the doc uses the exact canonical heading, preserve that wording and numbering.
- If this command needs to insert the section into a canonical doc, use the canonical Section 3 heading, not a loose variant.
- If the doc is materially non-canonical outside this command's safe repair boundary, stop and route to `reformat`.

## Update rules

Placement order:

1. replace inside `arch_skill:block:research_grounding`
2. otherwise update an existing research-like section
3. otherwise insert a new top-level research section

If `DOC_PATH` is already canonical, preserve or insert the section as:

- `# 3) Research Grounding (external + internal “ground truth”)`

Use this block shape:

```text
<!-- arch_skill:block:research_grounding:start -->
# Research Grounding (external + internal “ground truth”)
## External anchors (papers, systems, prior art)
- <source> — <adopt/reject + what exactly> — <why it applies>

## Internal ground truth (code as spec)
- Authoritative behavior anchors (do not reinvent):
  - `<path>` — <what it defines / guarantees>
- Existing patterns to reuse:
  - `<path>` — <pattern name> — <how we reuse it>

## Open questions (evidence-based)
- <question> — <what evidence would settle it>
<!-- arch_skill:block:research_grounding:end -->
```

## Console contract

- North Star reminder
- punchline
- what changed in research grounding
- issues or risks only if real
- next action
- need from the user only if required
