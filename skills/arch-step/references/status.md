# Arch Step Status

Use this file when `arch-step status` needs to summarize the exact artifact against the bundled quality bar, not just against heading presence.

## What status inspects first

Before grading stages, inspect the canonical artifact itself:

- required frontmatter keys
- `# TL;DR`
- `planning_passes`
- `# 0) Holistic North Star`
- exact canonical top-level sections `# 1)` through `# 10)`
- required command-owned blocks
- `WORKLOG_PATH` and `implementation_audit` when implementation has started
- the relevant quality bars from `section-quality.md`

## What status reports

Report the artifact first:

1. Plan artifact

Then report the core arc in order:

1. North Star
2. Research
3. Deep dive
4. External research
5. Phase plan
6. Implementation
7. Audit

Then report a short helper summary:

- plan enhancer
- reference pack / fold-in
- overbuild protector
- review gate

## Allowed grades

Use exactly:

- `strong`
- `decent`
- `weak`
- `missing`
- `not needed`

`not needed` is only for external research and helper commands.

## Artifact evidence rules

### Plan artifact

Inspect:

- required frontmatter
- `# TL;DR`
- `planning_passes`
- exact canonical headings for `# 0)` through `# 10)`

Grade:

- `strong` when the doc is structurally canonical, the major sections are present with credible content, and the core sections agree with each other
- `decent` when the structure is mostly canonical but one important section or heading-level expectation is thin
- `weak` when the doc is usable but structurally drifted, partially canonical, missing multiple required sections, or internally inconsistent
- `missing` when there is no credible canonical full-arch artifact yet

When the structure is weak, say why plainly, for example missing sections, heading drift, or absent `planning_passes`.
A doc cannot be artifact-strong if TL;DR, Section 0, Section 5, Section 6, or Section 7 are still weak.

Also check the "big 3" audit bar:

- target architecture fully specified
- architecture sufficiently idiomatic
- call sites audited exhaustively enough to trust the plan

### North Star

Inspect:

- frontmatter `status`
- `# TL;DR`
- `# 0) Holistic North Star`

Grade:

- `strong` when TL;DR and Section 0 are concrete, scoped, falsifiable, evidence-aware, and `status` is `active` or `complete`
- `decent` when the content is mostly real but still thin in one important place
- `weak` when the draft is vague, contradictory, or still obviously placeholder-heavy
- `missing` when the doc is not credibly bootstrapped

North Star cannot be stronger than the artifact that contains it.

### Research

Inspect:

- `arch_skill:block:research_grounding`
- or an equivalent `Research Grounding` section with the canonical structure

Grade:

- `strong` when the block is present with authoritative internal anchors, reusable patterns, explicit adopt or reject logic, and evidence-based open questions
- `decent` when present but thinner than the contract expects
- `weak` when present but generic or under-anchored
- `missing` when absent

Research cannot be stronger than the artifact that contains it.

### Deep dive

Inspect:

- `arch_skill:block:current_architecture`
- `arch_skill:block:target_architecture`
- `arch_skill:block:call_site_audit`
- `planning_passes`

Grade:

- `strong` when current architecture is grounded, target architecture is fully specified, and the call-site audit is exhaustive enough to drive implementation and audit
- `decent` when all are present but one is still thin
- `weak` when one or more exist but do not meet the section-quality depth bar
- `missing` when one or more are absent

Also report whether pass 1 or pass 2 has been completed based on the planning-passes block.

Deep dive cannot be stronger than the artifact that contains it.

### External research

Inspect:

- `arch_skill:block:external_research`
- `planning_passes.external_research_grounding`

Grade:

- `strong` when the block exists, uses narrow relevant topics with authoritative sources, and clearly ties adopt or reject guidance back to this plan
- `decent` when useful but thin
- `weak` when present but not really synthesized
- `missing` when warranted but absent
- `not needed` when the plan is repo-local and external best practice does not materially affect correctness or idiomatic design

External research cannot be stronger than the artifact that contains it.

### Phase plan

Inspect:

- `arch_skill:block:phase_plan`

Grade:

- `strong` when the authoritative phased plan exists, remains the single execution checklist, and each phase has concrete work, verification, exit criteria, and rollback
- `decent` when present but one or more phases are thin
- `weak` when generic or incomplete
- `missing` when absent

Phase plan cannot be stronger than the artifact that contains it.

### Implementation

Inspect:

- `WORKLOG_PATH`
- phase status updates in `DOC_PATH`
- implementation progress notes that match the `arch-implement` contract

Grade:

- `strong` when worklog and doc both reflect real phased progress or completion, ledger-like completeness is visible, and the doc matches reality
- `decent` when implementation is real but progress truth is thin
- `weak` when there are claims of progress without credible worklog or doc evidence
- `missing` when no implementation evidence exists

Implementation cannot be stronger than the artifact that contains it.

### Audit

Inspect:

- `arch_skill:block:implementation_audit`
- reopened phase notes

Grade:

- `strong` when the implementation audit block is present, evidence-anchored, and clearly distinguishes missing code from non-blocking manual QA
- `decent` when present but thin
- `weak` when nominal but not convincingly reconciled
- `missing` when absent

Audit cannot be stronger than the artifact that contains it.

## Helper summary rules

- `plan-enhance` is present when `arch_skill:block:plan_enhancer` exists
- `fold-in` is present when `arch_skill:block:reference_pack` exists
- `overbuild-protector` is present when `arch_skill:block:overbuild_protector` exists
- `review-gate` is present when `arch_skill:block:review_gate` exists

Helpers should usually be summarized in one compact line, for example:

- `Helpers are mixed: plan enhancer is strong, fold-in is missing, overbuild protector is not needed, review gate is decent.`

## Output shape

Keep the status output compact and human:

- one short line for the canonical artifact
- one short line per core stage
- one short helper summary line
- one short `Best next move:` line

Do not emit the longer `arch-flow` checklist here.

## Best-next-move rule

Choose the command that most improves artifact completeness or core-flow progress:

- no canonical doc yet -> `new`
- non-canonical existing doc -> `reformat`
- draft North Star -> no command yet; confirm and activate the doc before deeper work
- weak TL;DR or weak Section 0 in an otherwise canonical doc -> `reformat`
- missing research -> `research`
- weak or incomplete current architecture, target architecture, or call-site audit -> `deep-dive`
- missing current/target/audit blocks -> `deep-dive`
- warranted but missing external research -> `external-research`
- weak or competing execution checklist -> `phase-plan`
- missing phase plan -> `phase-plan`
- code progress without worklog truth -> `implement`
- missing implementation audit -> `audit-implementation`
