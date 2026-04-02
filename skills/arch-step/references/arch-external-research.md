# `external-research` Command Contract

Use this reference when the user runs `arch-step external-research`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for `External Research`, Section `5`, and Section `8`.
- Carry forward the relevance filter, topic budget, primary-source preference, disagreement handling, and anti-cargo-cult rules from the bundled doctrine.

## Artifact sections this command reads for alignment

- `# TL;DR`
- `# 0) Holistic North Star`
- `# 3) Research Grounding`
- `# 5) Target Architecture`
- `# 7) Depth-First Phased Implementation Plan` when present

## Artifact sections or blocks this command updates

- `planning_passes.external_research_grounding`
- `arch_skill:block:external_research`
- when truly needed, the affected plan sections or Decision Log if research materially changes the plan

## Quality bar for what this command touches

- research only topics that are both plan-adjacent and broadly generalizable
- keep the topic set narrow, usually 2-5 topics
- prefer primary or clearly authoritative sources
- synthesize best practice into adopt or reject guidance for this plan
- avoid research sprawl and avoid cargo-culting outside advice into the plan

## Consistency duties beyond local ownership

- If external guidance changes the preferred architecture, sequencing, or verification stance, repair the smallest clearly stale claims elsewhere in the doc.
- Add or update a Decision Log entry when the research changed an earlier conclusion in a meaningful way.
- Do not leave the external research block saying one thing while TL;DR, Section 0, or Section 8 still say another.

## Hard rules

- Docs-only. Do not modify code.
- Resolve `DOC_PATH`.
- Use web research when external best practice is applicable outside this repo.
- Keep the topic set narrow and relevant.
- Prefer primary sources and synthesize adopt or reject guidance for this plan.
- If sources disagree, summarize the disagreement and choose a default recommendation. Do not bounce the decision back to the user unless it is a true product decision.
- If North Star or UX scope is contradictory, pause for a quick doc edit first.

## Artifact preservation

- Preserve the canonical scaffold when it already exists.
- If the doc already has numbered or canonical placement around Research Grounding, preserve that structure.
- Insert `External Research` without renaming or displacing canonical Sections 3 through 10.
- If the doc is materially non-canonical outside this command's safe repair boundary, stop and route to `reformat`.

## Relevance filter

Only research a topic when both are true:

- the plan touches it or will be blocked by it
- the topic has broadly reusable external guidance

Skip project-trivia topics that do not generalize.

## Planning-passes update rule

- ensure the `planning_passes` block exists
- set:
  - `external_research_grounding: done <YYYY-MM-DD>`
- preserve other fields

## Update rules

Write or update:

- `arch_skill:block:external_research`

Use this canonical block shape:

```text
<!-- arch_skill:block:external_research:start -->
# External Research (best-in-class references; plan-adjacent)

> Goal: anchor the plan in idiomatic, broadly-accepted practices where applicable. This section intentionally avoids project-specific internals.

## Topics researched (and why)
- <topic> — <why it applies>

## Findings + how we apply them

### <Topic A>
- Best practices (synthesized):
  - <bullet>
- Recommended default for this plan:
  - <bullet>
- Pitfalls / footguns:
  - <bullet>
- Sources:
  - <title> — <url> — <why it’s authoritative>

## Adopt / Reject summary
- Adopt:
  - <what we will do + where it impacts the plan>
- Reject:
  - <what we will not do + why>

## Open questions (ONLY if truly not answerable)
- <question> — evidence needed: <what would settle it>
<!-- arch_skill:block:external_research:end -->
```

If research changes the architecture, sequencing, or constraints in a real way, update the affected plan sections and append a Decision Log entry when an earlier decision changed.

## Console contract

- North Star reminder
- punchline
- what topics were researched and how they changed the plan
- issues or risks only if real
- next action
