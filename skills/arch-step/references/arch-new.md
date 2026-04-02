# `new` Command Contract

Use this reference when the user runs `arch-step new`.

## Shared doctrine to carry in

- Read `shared-doctrine.md`.
- Read `section-quality.md` for `# TL;DR`, `# 0) Holistic North Star`, and `planning_passes`.
- Treat the freeform blurb as working intent, not as polished requirements.

## Artifact sections this command establishes

- frontmatter
- `# TL;DR`
- `planning_passes`
- `# 0) Holistic North Star`
- the canonical top-level scaffold for `# 1)` through `# 10)`

## Exact output shape this command must create

Create one canonical doc with:

- required frontmatter keys from `artifact-contract.md`
- `# TL;DR`
- the `planning_passes` block near the top
- `# 0) Holistic North Star`
- exact canonical headings for `# 1)` through `# 10)`

This command is responsible for bootstrapping the whole artifact shape, not just drafting the first section.

## Why these sections matter

- `# TL;DR` is the high-signal truth later stages should keep aligned with.
- `# 0)` is the alignment lock for scope, evidence, invariants, and fallback policy.
- The rest of the canonical scaffold exists so later steps sharpen one shared artifact instead of improvising their own structure.

## North Star doctrine

Treat TL;DR plus Section 0 as the planning lock:

- TL;DR says the outcome, problem, approach, and plan shape in the fewest lines possible.
- Section 0 says what is in scope, what is out of scope, what evidence is enough, what invariants must hold, and what fallback stance is allowed.
- Strong North Stars reduce later ambiguity. Weak North Stars force later commands to re-guess scope, architecture, and verification.
- This command should draft a North Star that is easy to confirm or correct, not a vague paragraph that only sounds thoughtful.

## Quality bar for what this command touches

- `# TL;DR` must not be generic when the blurb gives enough signal to draft it concretely.
- `# 0)` must be real enough to confirm or correct, not a placeholder disguised as prose.
- Sections `# 1)` through `# 10)` may begin as canonical scaffolding, but their exact headings must already be present.
- If the blurb clearly implies priorities, problem framing, verification bias, rollout implications, or a likely first decision-log entry, seed those sections lightly and truthfully instead of leaving pure ceremony behind.

## Hard rules

- Docs-only. Do not modify code.
- Name the file `docs/<TITLE_SCREAMING_SNAKE>_<YYYY-MM-DD>.md`.
- Apply the single-document rule.
- Do not create additional planning docs.
- Do not leave placeholders in TL;DR or Section 0 when the blurb supports filling them.
- `new` owns the full canonical scaffold from `artifact-contract.md`.
- Start the doc as `status: draft`.
- If the user confirms the North Star, update `status:` to `active` without silently changing scope.

## Consistency duties before stopping

- `title`, TL;DR, Section 0, and `fallback_policy` must tell the same story.
- If the blurb makes scope boundaries obvious, reflect them consistently in TL;DR and Section 0.
- If the blurb makes rollout or telemetry obviously irrelevant, Section 9 can say so briefly instead of pretending it is unknown.
- If the blurb reveals an immediate tradeoff or constraint, seed Section 1 or Section 10 with that fact rather than forcing later stages to rediscover it.

## Procedure

1. Derive the file name from the blurb.
2. Write the canonical scaffold from `artifact-contract.md`.
3. Draft TL;DR from the blurb:
   - falsifiable outcome
   - concrete problem
   - real approach
   - believable phased plan
   - non-negotiables that constrain later decisions
4. Draft Section 0 from the blurb:
   - falsifiable claim
   - in-scope and out-of-scope
   - smallest credible acceptance evidence
   - key invariants
   - strict fallback policy
5. Seed the remaining canonical sections without renaming them.
6. Make minimal consistency passes so frontmatter, TL;DR, Section 0, and any lightly seeded later sections agree.
7. Insert the canonical `planning_passes` block near the top.
8. Stop for North Star confirmation.

## Stop condition

After creating the doc and drafting TL;DR plus Section 0:

- print the drafted TL;DR
- print the drafted North Star
- ask for confirmation or edits
- stop

Do not proceed into research or architecture execution from the same `new` command.

## Console contract

- one-line North Star reminder
- one-line punchline stating the doc is created and what confirmation is needed
- doc path
- drafted TL;DR
- drafted North Star
- ask for `yes/no` plus edits if needed
