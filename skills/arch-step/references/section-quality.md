# Arch Step Section Quality

Use this file when you need to judge what a section is for, what strong looks like, and what weak looks like. This is the quality bar behind the canonical artifact.

Use these bars as execution gates:

- `strong`: later commands can trust the section directly
- `decent`: later commands can proceed, but should do so carefully
- `weak`: the section is not done for planning purposes
- `missing`: the artifact has not reached this part yet

## `# TL;DR`

Purpose:

- give the highest-signal truth about the plan in a few lines
- constrain the rest of the document rather than merely summarize it

Strong when:

- `Outcome` is falsifiable
- `Problem` is concrete
- `Approach` names the actual architectural move
- `Plan` names real phases or work slices
- `Non-negotiables` materially constrain decisions

Weak when:

- it reads like marketing copy
- the plan is generic or empty
- the non-negotiables do not actually rule anything out
- it disagrees with Section 0 or Section 7

Must stay consistent with:

- Section 0
- Section 7

Downstream can trust it when:

- it gives one stable sentence for outcome, problem, approach, and plan shape
- later commands do not need to reinterpret what this plan is trying to do

## `# 0) Holistic North Star`

Purpose:

- align the whole workflow before deeper planning
- lock scope, evidence, and invariants early enough to prevent drift

Strong when:

- the claim is falsifiable
- in-scope and out-of-scope are explicit
- definition of done is observable
- evidence uses the smallest credible signal
- invariants are actionable, not slogans
- fallback policy is explicit and respected
- it gives later commands a default answer for ordinary tradeoffs and scope calls

Weak when:

- the claim is vague or unmeasurable
- scope boundaries are missing
- definition of done depends on bespoke ceremony
- invariants are generic platitudes
- it reads like an inspirational statement instead of an execution contract

Must stay consistent with:

- TL;DR
- Sections 1, 7, and 8

Downstream can trust it when:

- later commands can answer "is this in scope?" and "what evidence is enough?" without guessing
- there is one clear fallback stance instead of hidden compatibility assumptions

## `# 1) Key Design Considerations (what matters most)`

Purpose:

- record the ranked priorities and constraints that should bias technical choices

Strong when:

- priorities are meaningfully ranked
- constraints are real and grounded
- principles reflect enforceable architecture rules
- tradeoffs and rejected alternatives are explicit

Weak when:

- priorities are interchangeable
- constraints are generic boilerplate
- principles do not affect decisions

Must stay consistent with:

- Section 0
- Section 5

Downstream can trust it when:

- technical choices can be ranked against it instead of argued from taste

## `# 2) Problem Statement (existing architecture + why change)`

Purpose:

- explain the current reality and why change is justified

Strong when:

- current behavior is concrete
- symptoms and root-cause hypotheses are specific
- the why-now case is explicit
- constraints flow from reality, not taste

Weak when:

- it only restates the desired future
- the current system is not actually described
- root causes are hand-wavy

Must stay consistent with:

- Section 4
- Section 6

Downstream can trust it when:

- the reason for change is specific enough to judge whether the target architecture really solves it

## `# 3) Research Grounding (external + internal “ground truth”)`

Purpose:

- anchor the plan in repo truth and relevant prior art

Strong when:

- internal anchors cite concrete file paths and explain why they are authoritative
- reusable patterns are named explicitly
- external anchors use adopt or reject reasoning instead of cargo cult
- open questions are framed as evidence needed

Weak when:

- it is generic or unanchored
- external references are decorative
- open questions are just vague TODOs

Must stay consistent with:

- Section 2
- Section 5
- external research when present

Downstream can trust it when:

- later commands can point to concrete repo anchors and prior art instead of rediscovering them

## `# 4) Current Architecture (as-is)`

Purpose:

- describe the current structure and behavior precisely enough to plan real change

Strong when:

- relevant on-disk structure is grounded in real files
- main control paths are named
- ownership boundaries and failure behavior are explicit
- UI states are captured when UI is in scope

Weak when:

- it is just a restatement of the repo tree
- flows are missing
- ownership and failure behavior are unclear

Must stay consistent with:

- Section 2
- Section 6

Downstream can trust it when:

- the current control flow and ownership boundaries are concrete enough to audit planned changes against them

## `# 5) Target Architecture (to-be)`

Purpose:

- specify the future architecture tightly enough to implement without guessing

Strong when:

- the future structure is concrete
- contracts and boundaries are explicit
- SSOT is clear
- no parallel paths are tolerated without explicit approval
- invariants are enforceable

Weak when:

- it describes aspirations instead of contracts
- boundaries are mushy
- it leaves multiple plausible architectures open

Must stay consistent with:

- Section 1
- Section 6
- Section 7
- Section 8

Downstream can trust it when:

- implementation can proceed without inventing missing contracts or choosing among multiple plausible architectures

## `# 6) Call-Site Audit (exhaustive change inventory)`

Purpose:

- make implementation completeness auditable
- prevent drift and missed migrations

Strong when:

- call sites are concrete and exhaustive enough to drive work
- migration notes and delete list are explicit
- consolidation sweep names related adopters and default dispositions

Weak when:

- it only lists the obvious path
- deletes and cleanup are absent
- the audit cannot be used to verify completeness

Must stay consistent with:

- Section 4
- Section 5
- Section 7

Downstream can trust it when:

- implementation and later audit can use it to prove completeness rather than merely get started

## `# 7) Depth-First Phased Implementation Plan (authoritative)`

Purpose:

- serve as the single authoritative execution checklist
- convert the rest of the document into an implementation order that can actually ship

Strong when:

- the plan is foundational-first
- each phase has goal, work, verification, exit criteria, and rollback
- verification is small and credible
- manual QA is deferred to finalization when appropriate
- there is no second execution checklist elsewhere
- phases make the required deletes, cleanup, and follow-through visible rather than burying them

Weak when:

- phases are generic or unordered
- tasks are too vague to implement
- helper blocks compete with the phase plan
- sequencing hides required cleanup or migration work

Must stay consistent with:

- TL;DR
- Section 5
- Section 6
- Section 8

Downstream can trust it when:

- implement can execute from it directly and audit can reopen work against it concretely

## `# 8) Verification Strategy (common-sense; non-blocking)`

Purpose:

- explain how the plan will be trusted without turning verification into bureaucracy
- define enough evidence to believe the work without inventing a second project

Strong when:

- it prefers existing checks
- unit, integration, or end-to-end signals are used only where they buy confidence
- manual verification is short and purposeful
- it explicitly avoids negative-value tests

Weak when:

- it introduces a large new harness by default
- it depends on visual constants, doc gates, or deletion proofs
- it conflicts with Section 0 evidence expectations

Must stay consistent with:

- Section 0
- Section 7

Downstream can trust it when:

- each phase has a believable smallest-signal verification story and final QA expectations are proportionate

## `# 9) Rollout / Ops / Telemetry`

Purpose:

- capture rollout, telemetry, and operational follow-through when relevant

Strong when:

- rollout, rollback, telemetry, and runbook implications are concrete
- it is concise when the change does not need much operational surface

Weak when:

- it is absent for a change that clearly needs rollout or telemetry thought
- it is generic boilerplate with no operational value

Must stay consistent with:

- Section 0
- Section 5

Downstream can trust it when:

- rollout or operational follow-through is explicit enough that implementation and finalization will not forget it

## `# 10) Decision Log (append-only)`

Purpose:

- record real decisions, approved exceptions, and plan drift over time

Strong when:

- entries are concrete and append-only
- exceptions such as fallbacks are explicitly time-boxed and justified
- sequencing or scope shifts are recorded when they matter

Weak when:

- decisions disappear into narrative edits
- exceptions are made without any record

Must stay consistent with:

- frontmatter
- the rest of the plan after any meaningful drift

Downstream can trust it when:

- plan changes, approved exceptions, and fallback decisions are visible without diff archaeology

## Supporting block: `planning_passes`

Purpose:

- track the recommended planning sequence without hard-blocking work

Strong when:

- pass fields are updated additively
- it reflects real planning progress
- it helps status and advance choose the next move

Downstream can trust it when:

- it reflects what actually happened and does not mislead `status` or `advance`

Weak when:

- it is missing from a canonical doc
- fields are wiped or left misleadingly stale

## Supporting block: `external_research`

Purpose:

- bring in narrowly scoped, plan-adjacent best practice with sources

Strong when:

- topics are narrow and relevant
- sources are authoritative
- findings become adopt or reject guidance for this plan

Downstream can trust it when:

- target architecture or verification choices can cite it without cargo-culting

Weak when:

- it is broad research sprawl
- it summarizes without affecting the plan

## Helper blocks

Use these to sharpen the main artifact, not compete with it.

- `plan_enhancer`: best-possible-by-our-standards hardening
- `reference_pack`: folded materials plus phase-aligned obligations
- `overbuild_protector`: scope triage without creating a second checklist
- `review_gate`: local idiomatic and completeness review record

Helper blocks are strong only when they improve the main artifact and keep Section 7 as the execution SSOT.

## `WORKLOG_PATH`

Purpose:

- record short execution evidence and progress truth

Strong when:

- it links to the plan
- it records real progress at phase boundaries
- it does not become a second planning document

Downstream can trust it when:

- implementation truth can be reconstructed quickly without rereading the entire code diff

## `implementation_audit`

Purpose:

- stop false-complete claims and force evidence-anchored completeness

Strong when:

- code blockers are concrete
- missing items cite evidence anchors
- false-complete phases are reopened
- manual QA is tracked as non-blocking follow-up rather than missing code

Downstream can trust it when:

- the repo can be judged code-complete or not without hand-waving
