# Plan Audit Implementation Audit Mode Proposal

Status: proposal document only. Do not treat this as implemented behavior.

Date: 2026-05-24

Target skill: `plan-audit`

Proposed mode name: `implementation-audit`

## Doctrine-Only Constraint

This proposal is for a doctrine-only extension to `plan-audit`.

The future mode should be built as agent guidance: `SKILL.md` routing, shared
reference docs, prompt contracts, audit-log rules, output contracts, and
examples.

Do not turn this into:

- a deterministic harness
- a runner
- a controller
- a workflow orchestrator
- a code-review subprocess launcher
- a rule engine
- a scorer
- a checklist executor
- a grep gate
- an automated architecture validator
- a test runner
- a proof collector
- a truth arbiter
- a script that decides whether implementation is elegant, complete, or clean

The checklists in this document are doctrine for reviewer judgment. They are
not specifications for a deterministic engine. The audit log is a durable
Markdown review ledger beside the plan, not a state machine and not a second
implementation plan.

## 1. North Star

Add a heavy implementation-audit mode to `plan-audit` that reviews implemented
or claimed-implemented code against the plan that authorized it.

The pre-implementation `plan-audit` question is:

```text
Will this plan produce the cleanest, simplest, most convergent architecture
the repo can support?
```

The implementation-audit question is:

```text
Did the code actually realize that plan, at the same quality bar, without
adding duplicate truth, side doors, drift, or unnecessary complexity?
```

The mode should be able to audit:

- the full plan
- all work through a named phase
- one named phase
- a named plan section or acceptance slice, when the plan format supports that

The output should tell the user whether the implementation passes code review
for the requested scope, what code-review blockers exist, what architecture got
worse, and what should be fixed before the work is treated as clean.

## 2. Why This Belongs Inside `plan-audit`

This should be a mode inside `plan-audit`, not a separate skill.

The reason is drift prevention. A plan audit and its implementation audit must
look at the same sources of truth:

- the same North Star
- the same done-state requirements
- the same requirements and non-requirements
- the same constraints and non-constraints
- the same ambiguity decisions
- the same code-quality canon
- the same relevant-code map
- the same delete list and side-door list
- the same canonical owner and SSOT expectations
- the same depth-first phase obligations
- the same code-quality expectations
- the same durable audit log

A separate implementation-audit skill would slowly develop its own vocabulary,
its own checklist, and its own interpretation of completion. That is exactly
the kind of drift this skill should prevent.

The clean design is:

- `plan-audit` owns the plan quality canon.
- `plan-audit` owns the sidecar audit log.
- `plan-audit` gains an `implementation-audit` mode that reuses the same canon,
  lenses, child prompt contract, audit log, and output discipline.
- Implementation-specific references are overlays on the existing material, not
  a fork of the doctrine.

## 3. Peer Boundary

This mode is not generic code review.

| Skill or workflow | Boundary |
| --- | --- |
| `plan-audit` pre-implementation mode | Audits a plan before work starts. |
| `plan-audit implementation-audit` | Audits code after work, but only against a planning artifact and its promised outcomes. |
| `code-review` | Reviews a diff, PR, branch, or code completion claim as a general code review. It is not plan-audit's source of truth. |
| `thermo-nuclear-code-quality-review` | Reviews maintainability harshly. `implementation-audit` imports that severity, but remains plan-scoped. |
| `arch-step audit-implementation` | Audits an arch-step artifact and may reopen phases inside that artifact. `plan-audit implementation-audit` should be generic across any planning doc format. |
| `plan-swarm` | Implements plan phases with workers. `implementation-audit` reviews the result and does not coordinate implementation. |

The mode must not dictate the user's workflow. It answers whether the code
matches the plan and the shared quality bar. It does not tell the user which
implementation process to use.

It is also not an honesty investigation. It should not assume implementers,
worklogs, CI, or tests are lying. It reviews code against the plan. When the
user, CI surface, or surrounding workflow says tests ran and passed, the mode
accepts that as background context instead of trying to prove it again.

## 4. Mode Contract

`implementation-audit` is a read-only code and plan audit mode, except for the
shared audit log.

Default write behavior:

- It may create or update `<PLAN_STEM>_PLAN_AUDIT.md`.
- It must not edit code.
- It must not silently rewrite the plan.
- It may recommend that a phase be reopened.
- It may update phase status only when the user or containing workflow
  explicitly grants that authority.

The mode reviews code directly. Summaries, worklogs, checked boxes, phase
labels, and test-pass claims help define scope, but they do not replace reading
the implementation.

The mode must not:

- run unit tests, integration tests, build commands, lint commands, or CI
  checks
- ask for test logs or command output
- verify that tests really ran
- investigate whether a completion claim is truthful
- compare plan history to look for hidden intent
- treat missing test logs as a code-review blocker

It may read test files as code when tests are part of the changed surface or
help explain the intended behavior. Reading a test file is not the same thing
as running tests or proving they passed.

The mode should produce sparse but hard findings. A clean result is allowed.
No findings is better than noisy architecture theater.

## 5. Invocation Shapes

The skill should accept natural-language scope in whatever form the user gives
it. Examples:

```text
Use $plan-audit implementation-audit on docs/PAYMENTS_PLAN.md.
```

```text
Use $plan-audit implementation-audit on docs/PAYMENTS_PLAN.md through Phase 4.
```

```text
Use $plan-audit implementation-audit on Phase 2 of docs/PAYMENTS_PLAN.md.
```

```text
Audit the implementation of the migration section in docs/PAYMENTS_PLAN.md.
```

```text
Run plan-audit implementation audit for the full thing.
```

The scope resolver should support:

- `full`: every requirement and phase in the plan
- `through phase <n>`: every obligation due up to and including that phase
- `phase <n>`: one phase, plus prerequisites, shared invariants, and plan-wide
  contracts that the phase touches
- `section <name>`: one named section or acceptance slice, when the plan has a
  section that can be audited independently
- `claimed-complete`: the scope claimed by worklogs, checked boxes, commit
  messages, or user text, used only to define what code should be reviewed

For `phase <n>`, the reviewer must not audit only the changed files in that
phase. It must also inspect:

- the phase's prerequisites
- plan-wide architecture contracts
- canonical owner expectations
- delete and side-door obligations created by the phase
- call sites and old paths that can still exercise the same behavior

For `through phase <n>`, the review covers code obligations due before or at
that boundary. It does not certify that all tests, CI, or manual validation
happened.

## 6. Authoritative Inputs

The mode should resolve and read these inputs when applicable:

- plan artifact, in whatever format it uses
- existing `<PLAN_STEM>_PLAN_AUDIT.md`
- user-requested audit scope
- current worktree state
- relevant diff, commit range, branch diff, or changed files
- implementation worklog, if present
- phase checklist, exit criteria, acceptance criteria, and done-state claims
- original plan-audit findings and resolved decision records
- local instructions such as `AGENTS.md` and `CLAUDE.md`
- repo package, generated-artifact, routing, prompt, and contract conventions

The mode audits against the current plan and audit log unless the user
explicitly asks for historical comparison. It should not search history looking
for hidden intent.

## 7. Review Posture

This mode is a code review, not a verification audit.

It reads:

- current code and runtime contracts
- generated artifacts, schemas, config, commands, routes, prompts, fixtures,
  docs, and install surfaces that govern behavior
- changed tests as code, when relevant
- plan text and audit-log obligations
- worklogs or summaries as scope context

It does not run or prove:

- unit tests
- integration tests
- build commands
- lint commands
- CI checks
- screenshots
- manual QA
- verification logs

If the surrounding workflow says tests passed, accept that and keep reviewing
the code. If there is no test-pass claim, still do not run tests or demand
logs. The review may say "test execution was not reviewed because this mode is
code-review only."

## 8. Progressive Audit Order

Implementation audit should have a fixed order so it remains plan-backed code
review instead of becoming either a generic diff review or a phase-status
rubber stamp.

### 8.1 Resolve Scope And Authority

- Resolve the plan artifact.
- Resolve the requested scope: full, through phase, individual phase, section,
  or claimed-complete.
- Resolve the audit log path as `<PLAN_STEM>_PLAN_AUDIT.md`.
- Read the existing audit log before reviewing.
- Read local instructions and repo code conventions.
- Determine whether the mode is allowed to update only the audit log or also
  the plan's phase status.

### 8.2 Read The Plan As Written

- Read the full plan or enough surrounding plan context to understand the
  requested scope clearly.
- Extract the North Star and done-state requirements.
- Extract requirements, non-requirements, constraints, non-constraints,
  assumptions, and complexity sources.
- Extract phase boundaries, checklists, exit criteria, delete lists,
  compatibility posture, and side-door expectations.
- Extract ambiguity decisions that were resolved during planning.
- Do not silently narrow the plan to what implementation happened to finish.

### 8.3 Reconstruct The Review Claim

Identify what code should be reviewed:

- full implementation
- all code through a phase boundary
- one phase
- one section
- refactor
- delete or migration
- behavior-preservation change

Then identify where that scope comes from:

- user text
- checked plan boxes
- phase status lines
- worklog
- commit messages
- branch name
- implementation notes

These inputs define review scope. They are not treated as lies to investigate
or claims to re-validate.

### 8.4 Reopen The Outcome Contract

Before looking at files, restate what must be true if the implementation is
done:

- user-facing or outcome-facing behavior works
- code-quality requirements are satisfied
- canonical owner path owns the behavior
- duplicate truth is gone or explicitly out of scope
- required deletes happened
- side doors are closed
- callers use the new contract
- shared dependencies cannot drift silently

If the plan cannot support this extraction, that is a plan-integrity finding
inside the implementation audit because the code review cannot tell what code
standard to apply.

### 8.5 Build The Changed-Behavior Map

Map what implementation actually changed:

- changed files
- changed symbols
- new files
- deleted files
- generated artifacts
- migrations
- config changes
- prompt or instruction changes
- test-file changes, reviewed only as code
- docs and examples touched
- public commands, routes, APIs, UI paths, jobs, scripts, or package surfaces
  affected

Use git and repo tooling to build the map, but do not stop at the diff. A
clean implementation audit also reads relevant unchanged code that can still
route to old behavior.

### 8.6 Build The Relevant-Code Map

Read or assign native subagents to map:

- files and symbols named by the plan
- current and target owner paths
- public caller families
- representative internal call sites
- legacy paths that should delete or converge
- alternate entrypoints and side doors
- comparable existing patterns
- schemas, adapters, generated artifacts, fixtures, config, prompts, and docs
- changed test files, when relevant as code
- install, routing, command, or package surfaces when relevant

Native subagents or parallel-agent features provided by the current coding
harness should be required for broad implementation audits when available. The
parent still owns synthesis.

Do not manually spawn separate coding-harness executables such as `codex`,
`claude`, or `agent` for ordinary acceleration unless the user explicitly
assigns that action and local instructions allow it.

### 8.7 Review Plan Obligations Against Code

For every obligation due in scope, classify it:

- satisfied by code
- missing code
- implemented differently but equivalent
- implemented differently and not equivalent
- scope cut
- unclear from code

Obligations include:

- explicit requirements
- done-state requirements
- checklist items
- exit criteria
- phase prerequisites
- named migrations
- call-site changes
- deletes and cleanup
- compatibility decisions
- no-shim or no-fallback promises
- docs, comments, prompts, examples, and instructions the plan said to update
  or delete
- behavior-preservation expectations visible in code shape

Do not accept broad statements like "core path done" when explicit
sub-obligations remain.

### 8.8 Run Implementation Lenses

Run the implementation-specific lens set defined in this proposal. For broad
audits, split lenses or code areas across native subagents. Child reports are
review input, not verdicts.

### 8.9 Review Phase Fit

For each phase in scope:

- If code obligations are missing, the phase has a blocking code-review
  finding.
- If required deletes did not happen, the phase has a blocking code-review
  finding.
- If a forbidden shim, fallback, duplicate writer, or parallel path was
  introduced, the phase has a blocking code-review finding.
- Missing unit-test output, CI logs, screenshots, or manual validation are out
  of scope for blocker decisions in this mode.

For `through phase <n>`, review every phase in the frontier. Do not report one
local gap while ignoring later code obligations in scope.

### 8.10 Challenge Elegance

Ask whether the implementation realized the plan in the simplest strong shape:

- Can this be simpler without breaking requirements?
- Did the implementation add concepts the plan did not need?
- Did it leave old concepts alive?
- Did it create a wrapper where ownership should have moved?
- Did it preserve branches that the new state model should delete?
- Did it make callers remember lifecycle rules?
- Did it use a custom mechanism where an existing library or repo pattern
  would be safer?
- Did it create two nearly identical paths that can drift?
- Did it keep compatibility scaffolding beyond the approved bridge?

Elegance findings should be concrete and code-anchored. Do not produce taste
comments.

### 8.11 Keep Test Execution Out Of Scope

The mode must not run or verify tests.

Do not:

- run unit tests
- run integration tests
- run build commands
- run lint commands
- run CI commands
- ask for test logs
- fail the review because test output was not supplied

Do:

- trust the containing workflow or user when they say tests passed
- read changed test files as code when they matter to the review
- flag test-code issues only when the test code itself creates a real
  maintenance, drift, or behavior-contract problem
- keep runtime verification outside this mode

### 8.12 Update The Shared Audit Log

For file-backed non-trivial audits:

- add a pass entry with `Mode: implementation-audit`
- update current code-review verdict
- add implementation findings with stable IDs
- carry unresolved plan findings forward when they still affect implementation
- resolve findings only with plan or code anchors
- update relevant-code coverage
- record test-execution and manual-QA status only as accepted external context
  when the user or workflow supplied it

The audit log should stay a review ledger. It should not become a second plan
or an implementation checklist.

### 8.13 Return The Verdict

The final answer should lead with:

- code-review verdict
- scope reviewed
- blocking code findings
- architecture/elegance blockers
- relevant code read
- relevant code not read
- audit log path
- smallest next repair

## 9. Implementation-Specific Lenses

These lenses reuse the existing `plan-audit` lens philosophy. They are not a
new doctrine fork.

### 9.1 `scope-and-baseline`

Check whether the audit target is clear:

- plan path
- audit log path
- full, through-phase, phase, section, or claimed-complete scope
- current worktree or diff baseline
- local instructions

Block when the audit cannot identify what was supposed to be implemented.

### 9.2 `plan-code-fit`

Check whether the current code fits the current plan contract:

- requirements map to code
- cleanup promises map to code changes
- delete promises map to actual absence or unreachable old paths
- exit criteria describe code states the reviewer can inspect
- behavior-preservation claims make sense from the changed code shape

Do not investigate intent. Do not search history for hidden motives. If the
current plan and current code do not line up, report the code-review issue
plainly.

### 9.3 `outcome-realization`

Check whether the code appears to implement the North Star outcome. This is not
"did the tasks happen?" It is "does the code shape support the desired world?"

Block when checklists can be marked done while the outcome remains false.

### 9.4 `requirement-traceability`

Trace every due requirement, done-state truth, checklist item, exit criterion,
and sub-obligation to code.

Block orphan obligations.

### 9.5 `phase-frontier-review`

For full or through-phase audits, review the ordered frontier:

- earlier phases are actually integrated
- later phases did not build on unproven assumptions
- phase status matches code reality
- complete labels are not leaving code obligations unreviewed

Block breadth-first completion claims that only discover integration risk at
the end.

### 9.6 `code-and-diff-map`

Build the actual changed-behavior map and compare it to plan expectations.

The review unit is the changed subsystem and affected call sites, not isolated
files.

### 9.7 `canonical-owner-and-ssot`

Verify the implementation converged onto the planned or best canonical owner.

Block:

- duplicate writers
- duplicate readers where one should own behavior
- shadow contracts
- old and new APIs both live without an approved bridge
- wrong-layer logic
- direct mutation paths around the owner

### 9.8 `existing-pattern-fit`

Verify the implementation used the best local pattern or justified divergence.

Classify related code:

- `migrated now`
- `deleted now`
- `left different for a real reason`
- `named follow-up`
- `still unresolved`

Block a locally good implementation that leaves related old patterns live and
unclassified.

### 9.9 `deletion-and-side-door-closure`

Search for old behavior still reachable through:

- old files
- old commands
- alternate routes
- scripts
- jobs
- UI affordances
- prompts
- generated artifacts
- fixtures
- examples
- docs or instructions
- compatibility flags
- fallback readers or writers
- direct calls into old APIs

If the plan said delete, the implementation must delete. Git is the archive.

### 9.10 `drift-proof-coupling`

Check whether coupled components can silently drift:

- schemas
- generated artifacts
- fixtures
- adapters
- prompts
- docs
- tests
- runtime config
- shared constants
- validation rules
- API contracts

Prefer one source of truth, generated artifacts from one owner, typed
contracts, fail-loud validation, or one adapter boundary.

Block duplicated rule text, duplicated command strings, duplicated schema
fragments, or copied prompt fragments when they can diverge.

### 9.11 `caller-invariant-state`

Review from the caller side:

- correct usage obvious
- invalid usage hard
- callers do not need internal lifecycle knowledge
- no magic flags
- no partial states that encode impossible combinations
- invariants live in the owner path, type model, state model, or runtime
  boundary
- state transitions are atomic where needed

Block implementations that satisfy the plan only when every caller remembers
unwritten rules.

### 9.12 `elegance-and-code-judo`

Search for the simpler code shape that deletes concepts.

Check:

- concepts added
- concepts deleted
- concepts merged
- concepts privatized
- branches removed
- wrappers avoided
- helpers that actually remove complexity
- custom mechanisms avoided when a proven library or local pattern would do

Block fake abstractions that add a noun without removing burden.

### 9.13 `tiny-team-maintainability`

Check whether three developers can comfortably own this code:

- self-documenting names
- direct control flow
- one obvious debug path
- minimal framework surface
- proven libraries for solved problems
- simple local patterns
- no broad config system unless required
- no speculative plugin layer
- no infrastructure that needs a platform team to babysit it

### 9.14 `test-code-review`

Review test files only as code when they are part of the changed or relevant
surface.

Check:

- tests do not create a second fake contract
- tests do not rely on test-only production paths
- test helpers do not hide real behavior
- changed tests do not encode duplicate business rules that can drift
- test names and fixtures still describe the behavior clearly

Do not run tests. Do not ask for test logs. Do not make missing test execution
records a blocker.

### 9.15 `docs-contract-drift`

Required when implementation changes behavior, commands, install surfaces,
APIs, examples, prompts, telemetry, stable IDs, user-facing contracts, or
instructions.

Flag touched or routing-relevant docs, comments, examples, prompts, and
instructions that now teach the wrong path.

Do not require broad docs cleanup unrelated to the implementation unless the
plan made it part of completion.

### 9.16 `agent-capability`

Required when implementation touches skills, agents, prompts, MCP, model
behavior, or instruction-bearing surfaces.

Check:

- prompt/native model capability got first right of refusal
- no capability-replacing scaffolding was added without plan approval
- no manual spawning of external coding harness binaries was introduced as a
  substitute for native subagents or prompt design
- skill doctrine remains self-contained
- scripts, if any, are narrow deterministic helpers rather than workflow owners

### 9.17 `security-boundary`

Required when implementation touches auth, permissions, secrets, input
validation, deserialization, command execution, file/process/network access,
privacy, or dependency trust.

Find only reachable changed-code risks. Do not emit generic security advice.

### 9.18 `scope-creep-and-non-requirements`

Check whether implementation added product scope, variants, modes, frameworks,
or compatibility behavior that the plan explicitly did not require.

Block scope creep when it adds bug vectors, live concepts, drift surfaces, or
maintenance cost.

## 10. Verdicts

The implementation mode should use code-review verdicts while keeping the same
findings-first output discipline. These verdicts are not a certificate that
tests ran, not a certificate that CI passed, and not a final completion stamp.
They are the reviewer's judgment on the code inspected.

Recommended verdicts:

- `approve`: No blocking code-review findings remain in the requested scope.
- `approve-with-notes`: No blocking code-review findings remain, but
  non-blocking code-quality, architecture, drift, cleanup, or maintainability
  notes exist.
- `not-approved`: Blocking code-review findings exist in the requested scope.
- `scope-inconclusive`: The review target cannot be resolved, or required code
  surfaces cannot be read.

The final verdict must not be softer than the worst unresolved blocker.

## 11. Blocking Finding Standard

An implementation finding is blocking when it means the requested scope should
not pass code review.

Blocking examples:

- requirement promised by the plan is not built
- phase checklist item is missing
- exit criterion is not satisfied
- required delete did not happen
- old path remains callable
- caller migration is incomplete
- duplicate writer was introduced
- SSOT was not achieved
- implementation used a forbidden shim or fallback
- plan-required prompt/native capability work was replaced with unjustified
  scaffolding
- refactor changes behavior in a way the plan did not authorize
- touched docs, prompts, examples, comments, or instructions still route users
  to wrong behavior when the plan made that cleanup part of completion
- changed tests, fixtures, or helpers create a misleading second contract or a
  test-only production path

Non-blocking examples:

- manual QA, CI, or test-pass context is not present
- broader docs consolidation that belongs after code is stable
- possible simplification that would be nice but does not create meaningful
  drift, bug risk, or maintenance burden
- unrelated pre-existing issue that the implementation did not introduce or
  worsen

## 12. Audit Log Extension

Use the same audit log as plan audit:

```text
<PLAN_STEM>_PLAN_AUDIT.md
```

Do not create a separate implementation audit log by default. One shared log is
the least drift-prone design.

The existing audit-log contract should be extended with mode-aware fields.

### 12.1 Header Additions

```markdown
# Plan Audit Log

Plan: <path>
Audit log: <path>
Modes covered: plan-audit, implementation-audit
Current plan verdict: ready | not-ready | blocked-on-decision | inconclusive
Current implementation code-review verdict: approve | approve-with-notes | not-approved | scope-inconclusive | not-run
Last reviewed: <date/time>
Current scope: <whole plan | through phase n | phase n | section | pasted plan>
```

### 12.2 Implementation Findings

Use stable implementation IDs:

```markdown
## Current Implementation Blocking Findings

- [ ] IMP-001 - <title>
  - Lens:
  - Scope:
  - Plan expects:
  - Code reality:
  - Anchors:
  - Required implementation repair:
  - Status: open | resolved | accepted-risk | out-of-scope | wrong
  - Resolution anchor:
```

Keep `PLA-*` or existing plan-audit IDs for plan-readiness findings. Use
`IMP-*` for implementation findings. If one problem spans both, link the IDs
instead of duplicating the text.

### 12.3 Implementation Scope Ledger

```markdown
## Implementation Scope Ledger

| Scope | Claimed status | Code-review verdict | Code blockers | Test/CI context | Last checked |
| --- | --- | --- | --- | --- | --- |
| Full plan |  |  |  |  |  |
| Through Phase <n> |  |  |  |  |  |
| Phase <n> - <title> |  |  |  |  |  |
```

### 12.4 Obligation Ledger

```markdown
## Implementation Obligation Ledger

| Obligation | Source | Due in scope | Evidence | Status |
| --- | --- | --- | --- | --- |
| <requirement/checklist/delete item> | <plan anchor> | yes/no | <code anchor> | satisfied/missing/unclear |
```

The ledger should stay compact. It is a review aid, not a second plan.

### 12.5 Test And CI Context

```markdown
## Test And CI Context

| Context | Source | Reviewed? | Notes |
| --- | --- | --- | --- |
| Tests passed | <user/workflow/CI summary if supplied> | no execution review | accepted as context |
```

This section is informational only. The mode does not run tests, require logs,
or verify test execution.

### 12.6 Pass History Additions

Each pass should record:

```markdown
### Pass <n> - <date/time>

- Mode: implementation-audit
- Scope:
- Baseline reviewed:
- Diff/commit/worktree reviewed:
- Test/CI context accepted, if supplied:
- Native subagents/lenses run:
- Code areas read:
- Obligations checked:
- Findings added:
- Findings resolved:
- Verdict:
- Next audit focus:
```

## 13. Native Subagent Contract

Broad implementation audits should require native subagents or parallel-agent
features when available.

Use native subagents for:

- changed-behavior mapping
- call-site migration audits
- old-path and side-door search
- changed test-file review when tests are relevant as code
- generated artifact and schema inspection
- docs/prompt/instruction drift
- comparable-pattern reads
- security or boundary-specific reads
- elegance and code-judo review

Do not replace native subagents by manually spawning separate coding-harness
executables such as `codex`, `claude`, or `agent` for ordinary acceleration.
That is different from using the harness's native subagent feature.

Child prompts should be read-only and bounded:

```text
You are doing one read-only plan-audit implementation-audit lens.

Work root: <repo/path>
Plan artifact: <path>
Audit log: <path or none>
Requested scope: <full | through phase n | phase n | section>
Audit lens: <lens name>

Read repo code directly. Do not edit files. Do not fix code. Do not run tests.
Do not ask for logs. Do not produce a second plan. Do not invent scope. Return
only findings your lens owns. If the implementation is clean for your lens,
say that plainly.

For every finding include:
- title
- blocking or non-blocking
- problem
- why it matters
- plan anchor
- code anchor
- required implementation repair
- coverage limits

Use native subagents or parallel-agent features provided by your current
coding harness when helpful. Do not manually spawn separate coding-harness
executables unless the parent explicitly assigns that action.
```

The parent must:

- spot-check child code anchors
- dedupe findings
- classify blockers
- reject findings outside the requested scope
- preserve genuine unresolved decisions
- own the final verdict

## 14. Output Contract

The final output should be findings-first and scope-explicit.

Recommended shape:

```markdown
# Plan Implementation Audit Verdict

VERDICT: approve | approve-with-notes | not-approved | scope-inconclusive
Confidence: high | medium | low
Mode: implementation-audit
Scope reviewed: <full | through phase n | phase n | section>
Plan artifact: <path>
Audit log: <path or not applicable>
Baseline reviewed: <worktree | diff | commit range | branch diff | unknown>
Test/CI context: <accepted if supplied | not supplied | not reviewed by this mode>

## Blocking Findings

1. <finding title>
   - Problem:
   - Why it blocks code-review approval:
   - Plan expects:
   - Code reality:
   - Anchors:
     - <plan path:line or heading>
     - <code path:line or symbol>
   - Required implementation repair:
   - Review lens:

## Non-Blocking Findings

<same shape, shorter>

## Scope Review

- Claimed scope:
- Code reviewed:
- Code blockers:
- Test/CI assumptions accepted:
- Phase status recommendations:

## Architecture And Elegance

- Canonical owner:
- SSOT status:
- Duplicate truth or parallel paths:
- Simpler code-judo move:
- Tiny-team maintainability risk:

## Deletes, Side Doors, And Drift

- Required deletes satisfied:
- Old paths still live:
- Side doors still callable:
- Drift-prone shared dependencies:
- Docs/prompts/examples/instructions drift:

## Relevant Code Coverage

- Code areas read:
- Relevant code not yet read:
- Native subagents/lenses run:
- Coverage blockers:

## Recommended Next Move

<one exact implementation repair, plan reconciliation, or code-review step>
```

Do not include placeholder sections with filler. Omit empty sections unless
the omission would hide important coverage.

## 15. Proper Implementation-Audit Checklist

An implementation audit has not been done properly unless these are true or
explicitly marked not applicable.

### Artifact Setup

- [ ] Plan artifact resolved.
- [ ] Requested implementation scope resolved.
- [ ] Audit log path resolved.
- [ ] Existing audit log read before review.
- [ ] Local instructions read.
- [ ] Baseline reviewed: worktree, diff, commit range, or branch diff.
- [ ] Test/CI pass claims accepted as context when supplied, without rerunning
  or proving them.
- [ ] The final output names what was not checked.

### Plan Obligation Extraction

- [ ] North Star extracted.
- [ ] Done-state requirements extracted.
- [ ] Requirements and non-requirements extracted.
- [ ] Constraints and non-constraints extracted.
- [ ] Phase boundaries extracted.
- [ ] Checklists and exit criteria extracted.
- [ ] Delete list extracted.
- [ ] Side-door and legacy-path expectations extracted.
- [ ] Ambiguity decisions and plan carry-through checked.

### Review Scope Claim

- [ ] Claimed scope identified.
- [ ] Claim source identified.
- [ ] Checked boxes and status labels treated as scope context.
- [ ] Worklog or implementer summary used only to aim the code review.
- [ ] The mode did not investigate whether anyone was lying or hiding work.

### Relevant-Code Coverage

- [ ] Changed files read.
- [ ] Changed symbols read.
- [ ] Current canonical owner path read.
- [ ] Target owner path read.
- [ ] Public caller families read.
- [ ] Representative internal callers read.
- [ ] Legacy paths searched and read.
- [ ] Side doors searched and read.
- [ ] Comparable patterns searched and read.
- [ ] Schemas, generated artifacts, fixtures, config, adapters, prompts, and
  docs read when relevant.
- [ ] Changed tests read as code when relevant.
- [ ] Relevant unchanged code read, not just the diff.
- [ ] Unknown relevant code named explicitly.

### Native Subagent Quality

- [ ] Native subagents or parallel-agent features used for broad audits when
  available.
- [ ] Reason recorded if native subagents were not used.
- [ ] Child scopes were non-overlapping enough to be useful.
- [ ] Child reports cited exact files, symbols, and code anchors.
- [ ] Parent synthesis spot-checked child code anchors.
- [ ] No child output became the verdict by itself.
- [ ] External harness-spawning was not used for ordinary acceleration.

### Code Review And Phase Fit

- [ ] Every due requirement traced to code or missing status.
- [ ] Every due checklist item checked.
- [ ] Every due exit criterion checked.
- [ ] Every required migration checked.
- [ ] Every call-site migration checked.
- [ ] Every required delete checked.
- [ ] Every side-door closure checked.
- [ ] Full and through-phase scopes reviewed the whole ordered frontier.
- [ ] Individual phase scopes include prerequisites and plan-wide contracts
  touched by the phase.
- [ ] Missing test logs, CI logs, screenshots, or manual QA did not become a
  code blocker.

### Architecture Quality

- [ ] Canonical owner is real in code.
- [ ] SSOT is real in code.
- [ ] No unauthorized duplicate writer exists.
- [ ] No unauthorized parallel reader/path exists.
- [ ] No forbidden shim or fallback slipped in.
- [ ] Existing local patterns were followed or divergence is justified.
- [ ] Related old patterns are migrated, deleted, left different for a reason,
  or named as follow-up.
- [ ] Caller API is hard to misuse.
- [ ] Invariants live in code shape, state model, types, routing, or owner
  boundary.
- [ ] Partial-state risks checked.
- [ ] Drift-prone dependencies checked.
- [ ] Abstractions remove real complexity.
- [ ] Concept count did not grow without deleting larger complexity.

### Tiny-Team Elegance

- [ ] Code is self-documenting enough for a tiny team.
- [ ] Control flow is direct.
- [ ] Debug path is obvious.
- [ ] No speculative framework, plugin layer, or broad config system was added
  without a real requirement.
- [ ] Existing well-debugged libraries or repo patterns were used where they
  fit.
- [ ] Custom machinery is justified by a real boundary or repeated complexity.

### Test Execution Boundary

- [ ] No unit tests were run.
- [ ] No integration tests were run.
- [ ] No build, lint, or CI command was run.
- [ ] No test logs were requested.
- [ ] Test-pass claims were accepted as context.
- [ ] Changed tests were reviewed only as code, if relevant.

### Docs, Prompts, And Contract Drift

- [ ] Touched docs checked.
- [ ] Routing-relevant docs checked.
- [ ] Comments and examples checked when they affect future use.
- [ ] Prompts and instructions checked when model-facing behavior changed.
- [ ] Install, command, API, telemetry, and generated contract surfaces checked
  when changed.
- [ ] Stale surfaces required by the plan to be updated or deleted are not left
  live.

### Finding Quality

- [ ] Every blocking finding includes consequence, plan anchor, code anchor,
  and required implementation repair.
- [ ] Findings are deduped across lenses.
- [ ] Non-blocking findings are separated from blockers.
- [ ] Wrong, out-of-scope, accepted-risk, and resolved findings have reasons.
- [ ] The verdict is no softer than the worst unresolved blocker.
- [ ] The audit log was updated for non-trivial file-backed audits.

## 16. Future Skill Package Changes

When this proposal is implemented, prefer the smallest change that gives
`plan-audit` the new mode without forking doctrine.

Recommended package changes:

```text
skills/plan-audit/
  SKILL.md
  references/
    architecture-quality-canon.md
    review-lenses.md
    progressive-audit-order.md
    audit-log-contract.md
    proper-audit-checklist.md
    child-prompt-contract.md
    output-contract.md
    implementation-audit-mode.md
    examples.md
```

### 16.1 `SKILL.md`

Update the top-level contract so `plan-audit` has two modes:

- plan-readiness audit before implementation
- implementation audit after plan-backed work

Clarify that generic code diff review still belongs to `code-review`. The new
mode is only for plan-backed code review and architecture realization.

### 16.2 `references/implementation-audit-mode.md`

Add one dedicated mode reference that owns:

- invocation shapes
- scope resolution
- progressive implementation-audit order
- implementation-specific lenses
- phase review rules
- test-execution boundary
- native subagent usage
- verdict rules
- anti-patterns

This file should import the existing canon by reference instead of copying it.

### 16.3 Existing References

Update existing references lightly:

- `architecture-quality-canon.md`: add a short note that the same canon applies
  both before and after implementation.
- `review-lenses.md`: add an implementation-mode lens overlay or pointer to
  `implementation-audit-mode.md`.
- `progressive-audit-order.md`: route to the implementation order when the
  user asks for implementation audit.
- `audit-log-contract.md`: add mode-aware fields and `IMP-*` findings.
- `proper-audit-checklist.md`: add the implementation-audit checklist or point
  to the mode reference.
- `child-prompt-contract.md`: add implementation-audit child prompt skeleton.
- `output-contract.md`: add implementation code-review verdict shape.
- `examples.md`: add full, through-phase, and individual-phase examples.

### 16.4 Repo Routing Docs

Update routing only where needed:

- `README.md` if the skill inventory or description changes.
- `AGENTS.md` only if the repo's skill routing needs to mention the new mode.

Do not create a new `skills/plan-implementation-audit/` package.

### 16.5 Verification

Because this is skill doctrine:

- run `npx skills check` after skill package changes
- reread edited skill references
- use `rg` to verify the mode name, path references, and no accidental new
  standalone skill package
- do not add unit tests that assert exact doctrine wording
- do not add scripts for judgment

## 17. Anti-Patterns

Avoid these while implementing the mode:

- Creating a separate implementation-audit skill that forks the canon.
- Turning this into a generic `code-review` wrapper.
- Launching external coding-harness binaries for ordinary acceleration instead
  of using native subagents.
- Treating worklog claims, checked boxes, or phase labels as substitutes for
  reading code.
- Auditing only the diff and missing unchanged side doors.
- Auditing one phase without checking prerequisites and touched plan-wide
  contracts.
- Running unit tests, integration tests, build commands, lint commands, or CI.
- Asking for test logs, screenshots, or manual QA.
- Treating missing test output as a code-review blocker.
- Investigating whether someone was lying instead of reviewing the code.
- Allowing "archive", "retire", "leave documented", or "hide behind fallback"
  when the plan said delete.
- Accepting old and new paths live together without an approved bridge and
  removal plan.
- Treating docs, comments, prompts, examples, or instructions as irrelevant
  when they route future humans or agents to the old behavior.
- Letting an audit log become the new implementation plan.
- Emitting taste comments without concrete code consequence.
- Blocking on unrelated pre-existing issues the implementation did not touch.
- Softening blockers with words like optional, nice-to-have, or deferred.
- Making the mode dictate planning or implementation workflow.

## 18. Definition Of Done For This Proposal

This proposal is good enough to build from when it makes these points clear:

- The implementation audit belongs inside `plan-audit`.
- It is a mode, not a new skill.
- It shares the existing `plan-audit` canon, lenses, child prompt contract,
  output discipline, and audit log.
- It can audit full plans, through-phase scopes, individual phases, and named
  sections when the plan format supports them.
- It audits actual code against the plan's North Star, done-state
  requirements, requirements, constraints, delete list, side-door closure,
  canonical owner, drift-proofing, and phase obligations.
- It reads all relevant code, including unchanged code that can preserve old
  behavior.
- It uses native subagents for broad audits when available.
- It does not manually spawn external coding harness binaries unless explicitly
  assigned.
- It never runs unit tests, integration tests, build commands, lint commands,
  or CI.
- It trusts supplied test-pass claims as context and does not ask for logs.
- It is not an honesty investigation or truth arbiter.
- It preserves tiny-team simplicity, self-documenting code, existing patterns,
  and proven libraries as first-class quality concerns.
- It defines progressive audit order, implementation lenses, verdicts, audit
  log extensions, output shape, and a proper-audit checklist.
- It remains doctrine-only and does not introduce scripts, runners,
  controllers, workflow delegation, or deterministic readiness scoring.
