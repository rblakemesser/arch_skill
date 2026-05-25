# Exhaustive Code Review Skill Plan

Status: planning document only. Do not treat this as implemented behavior.

Date: 2026-05-25

Working skill name: `exhaustive-code-review`

Related existing skills and surfaces:

- `code-review`
- `plan-audit`
- `thermo-nuclear-code-quality-review`
- `codex-review-yolo`
- `plan-implement`
- `plan-swarm`
- `audit-loop`
- `comment-loop`
- `verify-this`

## 0. User Problem

The repo already has strong review doctrine, but the existing review lanes are
optimized for high-signal findings, plan-backed architecture review, external
fresh eyes, or maintainability pressure. The missing lane is a deliberately
exhaustive code review skill that treats coverage itself as a first-class
artifact.

The desired review does not start by asking "what issues do I notice?" It
starts by building a literal inventory:

- every touched file
- every changed hunk
- every touched symbol
- every abstraction, contract, feature, route, schema, prompt, config surface,
  test surface, generated artifact, and doc surface affected by those changes
- every canonical owner path and adjacent same-behavior path that could keep
  the system split between old and new behavior

The review then closes those inventories one item at a time. A file, symbol, or
abstraction is not "reviewed" until the reviewer has read the relevant code,
mapped its owner and callers, checked the applicable review lenses, and either
opened findings or explicitly marked the item clean with coverage notes.

Canonical user asks:

```text
Run exhaustive-code-review on this full branch. I want every touched file and
abstraction checked, especially split-brain abstractions and missed central
owner paths.
```

```text
Use exhaustive-code-review for just the code touched by Phase 4 of
docs/PAYMENTS_PLAN.md.
```

```text
Do the meticulous review: file checklist, abstraction checklist, line-by-line
diff review, side-door search, centralization check, and native parallel agents.
```

Anti-cases:

- "Give this small diff a normal review." Use `code-review`.
- "Review implemented code only against this plan's quality bar." Use
  `plan-audit` in `implementation-audit` mode.
- "Run an especially harsh maintainability pass." Use
  `thermo-nuclear-code-quality-review`.
- "Get an external Codex second opinion." Use `codex-review-yolo`.
- "Implement the plan with parallel workers." Use `plan-swarm` or
  `plan-implement`, depending on scope.
- "Verify a measurable claim with before/after proof." Use `verify-this`.

## 1. North Star

Build a review-only skill that makes missing coverage hard.

The future skill should perform a line-by-line, file-by-file,
abstraction-by-abstraction, feature-by-feature code review over a user-selected
scope. It must begin with explicit checklists and it must not return an
approval verdict until those checklists are closed or an honest coverage
blocker is reported.

The skill's special value is not that it is "more intense" in a vague way. Its
special value is that it forces the review to name and close the concrete
surfaces where large bugs hide:

- touched files that were never fully read
- changed symbols whose callers were not checked
- old and new abstractions both left live
- duplicate truth split across two owners
- bypasses around a centralized service, helper, schema, route, prompt, or
  config owner
- direct callers still using the old path
- tests that prove a duplicate contract instead of the real behavior
- docs, examples, generated artifacts, prompts, or stable IDs that still teach
  the wrong path
- security and boundary surfaces whose failure modes were not reviewed

The review is exhaustive in coverage discipline, not noisy in output. A clean
result is allowed. Cosmetic nits and generic "could be cleaner" notes are
dropped unless they create concrete correctness, maintainability, drift,
reviewability, or future-change risk.

## 2. Mechanism Choice

This should be a skill because the workflow is reusable, high-stakes, and easy
to underdo. It needs a durable process, review lenses, native parallel-agent
prompt contracts, checklist artifacts, and a strict output contract.

V1 should be prompt-first. Do not build a deterministic runner, controller,
state machine, scorer, grep gate, automated architecture validator, or
checklist executor. The hard part is reviewer judgment: deciding what the
changed code means, what abstractions it touches, which existing owner path
should have been used, and whether a finding is real.

The checklists are not a replacement for judgment. They are a coverage ledger.
They force the reviewer to know what was checked and what was not checked.

Native parallel agents are mandatory for a formal run. This means native
subagents or parallel-agent features provided by the current coding harness.
It does not mean:

- using `$agent-delegate`
- using `$fresh-consult`
- using `$code-review`
- using `$codex-review-yolo`
- manually spawning `codex`, `claude`, `agent`, or another coding-harness
  executable
- hiding the workflow inside a Python runner

If the current harness cannot provide native parallel agents, the future skill
should return `coverage-blocked` unless the user explicitly asks for a
sequential fallback. It should not pretend that the required review happened.

Scripts are not part of V1. A future script may be justified only for narrow
mechanics such as creating a blank Markdown checklist, normalizing child report
headings, or extracting changed-file metadata. A script must never decide
whether code is correct, centralized, elegant, or approved.

## 3. Reviewed Doctrine Inputs

This plan is grounded in the current review and audit doctrine in this repo.
The important inspected sources are:

| Source | Existing doctrine to reuse |
| --- | --- |
| `skills/code-review/SKILL.md` | General review is findings-first, evidence-backed, review-only, and maps changed behavior before findings. |
| `skills/code-review/references/review-requirements.md` | Required checks include correctness, architecture, proof adequacy, docs drift, risk-triggered security, duplication, drift, external-boundary errors, and unauthorized shims or fallback paths. |
| `skills/code-review/references/reviewer-prompt.md` | Each reviewer must read repo truth directly, read every changed line, derive local policy first, cite evidence, and treat lens outputs as evidence rather than the verdict. |
| `skills/code-review/references/output-contract.md` | Review output must be sparse, findings-first, structured, and explicit about coverage failures. |
| `skills/plan-audit/SKILL.md` | Plan-backed audits use native subagents for broad independent read-only slices and keep parent synthesis as the real verdict owner. |
| `skills/plan-audit/references/implementation-audit-mode.md` | Strong implementation review checks plan-code fit, requirement traceability, canonical ownership, source of truth, side-door closure, drift-proof coupling, caller invariants, elegance, test code as code, docs drift, agent capability, security boundaries, and scope creep. |
| `skills/plan-audit/references/architecture-quality-canon.md` | Architecture review starts from code truth, tiny-team maintainability, canonical ownership, existing patterns, caller shape, drift-proof coupling, abstraction value, legacy deletion, and meaningful proof. |
| `skills/plan-audit/references/child-prompt-contract.md` | Native subagents are the preferred acceleration path; external harness-spawning skills are not the ordinary path; parent spot-checking and synthesis remain mandatory. |
| `skills/plan-audit/references/proper-audit-checklist.md` | A strong audit records relevant-code coverage, native subagent read quality, architecture quality, finding quality, and unresolved coverage. |
| `skills/plan-implement/references/native-subagent-contract.md` | Native subagents are good for code mapping, side-door search, comparable-pattern reading, docs/config drift, tests-as-code review, and one implementation-audit lens; the parent dedupes and spot-checks. |
| `vendor/cursor/plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md` | Harsh maintainability review looks for code-judo simplification, file sprawl, spaghetti conditionals, wrong-layer logic, thin wrappers, cast-heavy contracts, duplicate helpers, and missed decomposition. |
| `skills/codex-review-yolo/SKILL.md` | External context-free review is useful but is a different mechanism. This new skill should not depend on a separate CLI profile. |
| `skills/plan-swarm/SKILL.md` | Worker orchestration and review gates are useful in implementation swarms, but this new skill is review-only and should use native harness agents, not delegated external workers. |
| `skills/audit-loop/references/review.md` | A review pass should decide whether the map is complete, whether the latest pass actually reduced risk, and whether the resulting diff survived safety, downstream, elegance, and duplication checks. |
| `skills/audit-loop/references/quality-bar.md` | Strong findings have concrete file anchors, tie risk to consequence, converge duplicate logic, and avoid vague "needs refactor" feedback. |
| `skills/comment-loop/references/shared-doctrine.md` | Exhaustive mapping should precede edits; canonical owner boundaries matter more than scattered local explanations. |
| `vendor/cursor/plugins/cursor-team-kit/skills/review-and-ship/SKILL.md` | Pre-ship review prioritizes correctness, regressions, security, intent fit, and tests over style-only comments. |
| `vendor/cursor/plugins/cursor-team-kit/skills/verify-this/SKILL.md` | Verification proves or disproves a falsifiable claim; this future skill reviews code and proof adequacy, but should not become the proof runner unless explicitly asked. |

## 4. Peer Boundary

The future skill should have a clear lane next to the existing review skills.

### `code-review`

`code-review` is the general branch, diff, PR, or completion-claim review
powered by Codex subprocess lenses and a final synthesis. It is high-signal and
broad.

`exhaustive-code-review` is coverage-ledger driven. It must produce and close a
touched-file checklist, touched-abstraction checklist, and touched-feature
checklist. It must use native parallel agents from the current harness, not the
`code-review` runner.

### `plan-audit implementation-audit`

`plan-audit implementation-audit` reviews implemented code against a specific
plan artifact. Its source of truth is the plan and audit log.

`exhaustive-code-review` may accept a plan-backed scope, but it is still a code
review skill. Its source of truth is the selected code scope plus any plan,
diff, branch, or path target the user names. It may import plan obligations,
but it should not update the plan audit log unless the user explicitly asks.

### `thermo-nuclear-code-quality-review`

`thermo-nuclear-code-quality-review` is a harsh maintainability lens.

`exhaustive-code-review` should include that severity as one lens, but it owns
more than maintainability: changed-line coverage, abstraction centralization,
feature correctness, caller shape, side doors, proof adequacy, drift, docs,
security, and agent/prompt surfaces when relevant.

### `codex-review-yolo`

`codex-review-yolo` shells out to a context-free Codex CLI profile for a second
opinion.

`exhaustive-code-review` should not shell out. It should use native subagents
from the current coding harness and parent synthesis in the same session.

### `plan-swarm`

`plan-swarm` implements plan phases through delegated workers and review gates.

`exhaustive-code-review` does not implement, repair, commit, push, open PRs, or
route repair waves. It returns findings and coverage.

### `audit-loop`

`audit-loop` is an ongoing audit-and-fix workflow with a root ledger.

`exhaustive-code-review` is a bounded review over a selected branch, diff, plan
scope, commit range, or path set. It should not keep running until no possible
repo work remains.

### `verify-this`

`verify-this` proves a falsifiable claim with before/after evidence.

`exhaustive-code-review` reviews proof quality and may recommend proof, but it
should not become a verification workflow unless the user explicitly asks.

## 5. Scope Modes

The skill should accept natural-language scope without forcing flags.

Supported review scopes:

- `worktree`: staged and unstaged changes in the current repo.
- `branch`: the current branch or a named branch against a base ref such as
  `main`.
- `commit-range`: a named commit range.
- `plan-full`: all code touched by an implementation of a plan.
- `plan-through-phase`: all code obligations due through a named phase.
- `plan-phase`: one phase, plus prerequisites and plan-wide contracts touched
  by that phase.
- `plan-section`: one named section or acceptance slice.
- `paths`: explicit files or directories.
- `completion-claim`: a user-named claim whose affected code must be
  reconstructed from plan text, worklogs, commit messages, changed files, or
  explicit paths.

Scope resolution must produce a target record before review starts:

```markdown
Review target:
- Mode:
- Baseline:
- Head/current state:
- User objective:
- Plan artifact, if any:
- Plan scope, if any:
- Explicit paths:
- Changed-file source:
- Local instruction files read:
- Known exclusions:
- Coverage risk:
```

If the target cannot be resolved, the review should stop with
`coverage-blocked`. A review with an unknown target is worse than no review.

## 6. Hard Requirements

The future skill must obey these rules.

### Review-only

Do not edit product code, tests, docs, config, generated artifacts, prompts, or
skill files during the review. The only allowed write is the review coverage
artifact, preferably outside the repo by default.

Do not commit, push, open PRs, apply patches, or route repairs.

### Local truth first

Read local instructions and repo conventions before applying generic review
doctrine. Relevant local sources include `AGENTS.md`, `CLAUDE.md`, `README.md`,
language config, lint or formatter config, CI config, nearby code, and the plan
artifact when a plan scope is used.

### Checklist first

The first real artifact is the checklist set:

- file checklist
- abstraction checklist
- feature or behavior checklist
- native-agent coverage checklist

Findings before a coverage map are suspect.

### Native parallel agents required

For formal runs, use native parallel agents provided by the current coding
harness. At minimum, separate independent read-only review work into parallel
agents by file group, abstraction family, feature path, or review lens.

If native parallel agents are unavailable, return `coverage-blocked` unless the
user explicitly asks for a sequential fallback.

### Parent owns synthesis

Child agents provide evidence, not the verdict. The parent must spot-check
important evidence, dedupe findings, reject out-of-scope findings, fill the
checklists, and own the final verdict.

### Every touched file is closed

Each touched file must end as one of:

- `clean`
- `has-blocking-finding`
- `has-non-blocking-finding`
- `not-applicable-deleted`
- `coverage-blocked`

No file may remain `unread`, `partial`, or `unknown` in an approval verdict.

### Every touched abstraction is closed

Each touched abstraction must end as one of:

- `centralized-and-clean`
- `intentionally-local`
- `split-brain-blocker`
- `wrong-owner-blocker`
- `drift-risk`
- `coverage-blocked`

No abstraction may remain unclassified in an approval verdict.

### Every changed hunk is read

The reviewer must read every changed hunk. If a changed hunk depends on
surrounding code, the surrounding function, class, module, or caller path must
also be read.

### Tests are reviewed as code

Changed tests are reviewed for behavior value, fake contracts, duplicate
business rules, misleading fixtures, test-only production paths, overmocking,
and whether they protect the right user-visible or externally observable
behavior.

The skill reviews proof adequacy. It does not need to execute tests unless the
user explicitly asks for verification or local instructions require it.

### Docs and generated surfaces are live review surfaces

Docs, examples, prompt files, generated artifacts, schemas, telemetry names,
stable IDs, and install surfaces are part of review when the changed code
alters what they describe or consume.

### No generic noise

Do not emit style preferences, broad architecture vibes, or "consider"
feedback. Findings need concrete risk, concrete evidence, and a concrete repair
target.

## 7. Review Artifact Model

For non-trivial reviews, the future skill should create a run artifact outside
the repo by default:

```text
/tmp/exhaustive-code-review/<scope-slug>-<timestamp>/
  target.md
  file-checklist.md
  abstraction-checklist.md
  feature-checklist.md
  native-agents.md
  child-prompts/
  child-reports/
  synthesis.md
  verdict.md
```

This keeps ordinary review runs from dirtying the repository. If a plan-backed
workflow needs a durable repo artifact, the user can explicitly ask for one.

### File checklist item

Each file item should use this shape:

```markdown
## FILE-001: <path>

- Status: unread | partial | clean | has-blocking-finding |
  has-non-blocking-finding | not-applicable-deleted | coverage-blocked
- Git status: added | modified | deleted | renamed | copied | mode-change
- Old path:
- New path:
- Role: production | test | docs | config | schema | generated | prompt |
  skill | script | asset | unknown
- Changed hunks:
- Changed symbols:
- Owning abstraction(s):
- Canonical owner path:
- Callers or consumers read:
- Adjacent same-behavior paths read:
- Tests/proof surfaces read:
- Docs/contracts/generated surfaces read:
- Native agent reports:
- Parent spot-check:
- Findings:
- Closure note:
```

### Abstraction checklist item

Each abstraction item should use this shape:

```markdown
## ABS-001: <name>

- Type: service | module | component | hook | command | route | schema |
  adapter | prompt | config | data model | state model | helper | workflow |
  generated contract | other
- Status: unreviewed | centralized-and-clean | intentionally-local |
  split-brain-blocker | wrong-owner-blocker | drift-risk | coverage-blocked
- Touched files:
- Canonical owner:
- Existing comparable patterns:
- Public callers:
- Internal callers:
- Readers:
- Writers:
- Side doors:
- Old path:
- New path:
- Invariants:
- Centralization question:
- Split-brain question:
- Drift surfaces:
- Proof surfaces:
- Native agent reports:
- Parent spot-check:
- Findings:
- Closure note:
```

### Feature checklist item

Each feature or behavior item should use this shape:

```markdown
## FEAT-001: <behavior or obligation>

- Status: unreviewed | clean | has-blocking-finding |
  has-non-blocking-finding | coverage-blocked
- Source: plan requirement | user objective | diff behavior | API |
  route | UI path | CLI | job | prompt behavior | config behavior
- User-visible or externally observable outcome:
- Code path:
- State or persistence:
- Error and boundary behavior:
- Callers or entrypoints read:
- Tests/proof read:
- Docs/contracts read:
- Native agent reports:
- Parent spot-check:
- Findings:
- Closure note:
```

## 8. Required Review Lenses

Each formal run should apply these lenses. The parent may shard them across
native agents by file, abstraction, feature, or risk surface.

### `file-line-by-line`

Read every changed hunk in every touched file. Check local correctness,
surrounding control flow, deleted behavior, renamed behavior, edge cases,
imports, exports, lifecycle, errors, and whether the changed lines make sense
inside the full file.

### `abstraction-and-central-owner`

Check whether the change uses the existing canonical owner path. Flag bypasses,
duplicate readers, duplicate writers, shadow contracts, old/new APIs both live,
partial migrations, and wrong-layer logic.

This is the main lens for the user's split-brain concern.

### `feature-and-behavior`

Review the user-visible, API-visible, CLI-visible, job-visible, prompt-visible,
or externally observable behavior changed by the diff. Check whether the
behavior is correct across success, failure, empty, repeated, concurrent, and
boundary cases that the changed code actually reaches.

### `caller-invariants-and-state`

Review from the caller side. Correct usage should be obvious and invalid usage
hard. Flag magic flags, partial state, nullable modes, lifecycle knowledge
leaking to callers, duplicate validation, and impossible state combinations.

### `side-doors-and-deletes`

Search for old behavior still reachable through old files, commands, routes,
scripts, jobs, UI affordances, prompt paths, generated artifacts, fixtures,
examples, fallback readers or writers, and direct calls into old APIs.

If the change intended centralization or deletion, old live paths are blockers
unless explicitly approved.

### `duplication-and-drift`

Check rules, schemas, prompts, constants, validation logic, config names,
telemetry names, generated artifacts, tests, and docs for duplicate truth that
can drift. Prefer one source of truth, one adapter boundary, one schema, one
validator, or fail-loud generation.

### `proof-and-tests`

Review tests, typechecks, build checks, assertions, instrumentation, and manual
proof claims for adequacy proportional to risk. Flag missing behavior
assertions, mock-only proof for integration behavior, tests that duplicate
business rules, brittle timing or visual constants, and proof that cannot catch
the bug the change could create.

### `docs-contract-generated-drift`

Check docs, examples, comments, prompt files, generated files, schemas,
fixtures, package metadata, Makefile targets, README commands, stable IDs, and
telemetry names that describe or consume changed behavior.

### `maintainability-and-code-judo`

Apply the thermonuclear maintainability bar: can a simpler structure delete
branches, helpers, modes, wrappers, or special cases? Flag spaghetti condition
growth, file sprawl, thin wrappers, identity abstractions, duplicate helpers,
cast-heavy contracts, wrong-layer logic, and missed decomposition.

### `security-boundary`

Required when the change touches auth, authorization, secrets, input validation,
deserialization, command execution, file/process/network access, dependency
trust, privacy, or infrastructure boundaries. Findings must be reachable from
changed code and cite concrete data or exploit risk.

### `agent-and-prompt-surface`

Required when the change touches skills, prompts, agents, MCP, model behavior,
tool orchestration, instruction-bearing files, or generated agent surfaces.
Check that prompt/native capability got first right of refusal, scripts remain
narrow deterministic helpers, and the change did not replace model judgment
with unjustified scaffolding.

Do not invoke a separate agent-linter skill by default. Encode this as a native
review lens so the future skill remains native-harness based.

### `negative-space`

Ask what was not touched but should have been. Search for same-contract,
same-behavior, same-symbol, same-command, same-route, same-schema, same-prompt,
or same-generated-artifact surfaces that could keep the system bifurcated.

This lens exists because many review misses are omissions, not bad changed
lines.

## 9. Native Parallel Agent Plan

The parent agent coordinates native parallel agents in waves. The exact number
depends on scope, but formal runs require parallelism.

### Wave 0: parent target and checklist setup

The parent resolves scope, reads local instructions, creates the run artifact,
and writes initial file, abstraction, and feature checklist rows.

The parent should not launch findings agents before there is enough checklist
structure to assign non-overlapping work.

### Wave 1: mapping agents

Use native parallel agents for independent read-only mapping:

- changed-file mapper: read every changed file, identify symbols and local
  roles
- abstraction mapper: identify canonical owners, comparable patterns, public
  callers, internal callers, readers, and writers
- side-door mapper: search old paths, alternate entrypoints, direct callers,
  fallback paths, docs, examples, prompts, generated artifacts, and fixtures
- plan-scope mapper, when plan-backed: map plan obligations to code surfaces

Each mapper returns files read, symbols read, likely missing surfaces, and
coverage limits.

### Wave 2: lens reviewers

Use native parallel agents for review lenses. Good shards include:

- one file group per area
- one abstraction family per reviewer
- one feature path per reviewer
- docs/generated/proof surfaces as their own reviewer
- security or agent-surface conditional reviewers

Lens reviewers must use the checklist IDs they are assigned. They must not
broaden into the whole review unless they discover a concrete missing surface.

### Wave 3: adversarial gap review

After Wave 2, launch at least one native agent whose only job is to find what
the review missed:

- unchecked files
- unchecked symbols
- unchecked callers
- abstractions without canonical owner classification
- old and new paths both live
- generated/docs/tests/prompts not checked
- findings that rely on unverified assumptions

The parent must fold any valid gap back into the checklists and rerun the
relevant lens if needed.

### Native child prompt footer

Every native child prompt should include:

```text
You are one read-only reviewer in an exhaustive code review.

Work root: <repo root>
Review target: <target record>
Assigned checklist IDs: <FILE/ABS/FEAT ids>
Assigned lens: <lens name>

Read repo truth directly. Do not edit files. Do not run broad test suites
unless the parent explicitly assigned verification. Do not invoke external
agent skills or manually spawn codex, claude, agent, or other coding-harness
executables. Use only native capabilities provided by this harness.

Return:
- checklist IDs covered
- files and symbols read
- findings, if any
- clean items, if any
- coverage limits
- missing surfaces the parent should add to the checklist

Every finding must include file, symbol or line, concrete risk, evidence, and
the repair target. If your assigned scope is clean, say that plainly.
```

## 10. End-to-End Workflow

The future skill should run in this order.

1. Resolve the scope and baseline.
2. Read local instructions and repo convention sources.
3. Create the review run artifact.
4. Build the initial file checklist from the diff, path set, branch, commit
   range, or plan scope.
5. Read enough of the changed files to seed changed symbols and initial
   abstractions.
6. Build the initial abstraction checklist.
7. Build the initial feature or behavior checklist.
8. Launch native Wave 1 mapping agents.
9. Merge mapping reports into the checklists.
10. Add missing files, abstractions, callers, side doors, docs, tests, prompts,
    generated artifacts, and config surfaces discovered by mappers.
11. Launch native Wave 2 lens reviewers.
12. Parent reads every changed hunk or verifies that a native file reviewer did
    and spot-checks risky examples.
13. Parent spot-checks child findings and important clean claims.
14. Launch Wave 3 adversarial gap review.
15. Fold valid gaps into the checklists.
16. Rerun any lens whose scope changed materially.
17. Close every file checklist item.
18. Close every abstraction checklist item.
19. Close every feature checklist item.
20. Dedupe findings.
21. Classify findings as blocking, non-blocking, out-of-scope, wrong, or
    coverage-blocking.
22. Emit the final verdict.

The workflow may loop from step 15 back to step 11 when the negative-space pass
finds a real missed surface. That loop is the point: missed surfaces are not
notes, they are review work.

## 11. Specific Risks To Hunt

The future skill should explicitly train reviewers to hunt these risks. This
section is the substance of the review. The process above prevents missed
coverage; this catalog tells reviewers what bad code shapes look like once they
are reading the right surfaces.

Each risk pattern should be reviewed with the same discipline:

- name the live concept the code is changing
- identify the canonical owner, or state that no owner exists yet
- search for old and alternate paths that can still express the concept
- read representative callers, readers, writers, tests, docs, prompts, schemas,
  generated artifacts, config, and examples
- decide whether the current shape converges the system or leaves two ways to
  be right
- flag only changed-code or changed-scope risks with concrete evidence

Good findings sound like:

```text
The new route writes through `OrderDraftStore`, but the old admin action still
mutates `orders.draft_json` directly. That leaves two writers for the same
draft contract, so validation can drift depending on entrypoint.
```

Weak findings sound like:

```text
This could maybe be more centralized.
```

The first one names the concept, the old and new paths, the concrete drift
risk, and where the repair should go. The second one is just a preference.

### Split-brain or bifurcated abstraction

Flag when the system now has two live ways to express, mutate, validate,
render, serialize, route, prompt, or configure the same concept.

Common signs:

- old service and new service both callable
- old command path and new command path both registered
- two schemas describe the same contract
- one feature reads from the central store while another reads a local copy
- tests build fixtures for a duplicate model
- docs or examples teach an old path that still works
- prompt instructions name a retired flow
- direct mutation bypasses the intended owner
- two generated artifacts can drift

What to read:

- new owner and old owner
- all public entrypoints that reach either owner
- representative internal callers
- tests and fixtures that instantiate either model
- docs, examples, prompts, schemas, and generated artifacts that name either
  model
- delete or migration plan, if one exists

Block when:

- both paths remain live and can affect real behavior
- the bridge between old and new paths is implicit, optional, or memory-based
- callers can choose which model to use without a hard boundary
- tests make both paths look valid
- docs still teach the old path as a supported path

Do not block when:

- the old path is unreachable and only present as dead code scheduled for
  deletion in the same change
- the two paths intentionally support different products, tenants, versions, or
  runtime modes and that distinction is encoded in names, routing, and tests
- the bridge is a short, explicit migration shim with a deletion checkpoint and
  no new callers

Example findings:

```markdown
### [BLOCKING] New session writer bypasses the canonical save service

- Checklist IDs: FILE-004, ABS-002, FEAT-001
- File: src/editor/ToolbarSaveButton.tsx
- Symbol / line: `handleSave`
- Risk: The button now calls `writeSessionDraft` directly while the rest of
  the editor saves through `EditorSessionService.save`. That creates two live
  save paths with different validation and retry behavior, so draft state can
  diverge by entrypoint.
- Evidence: `ToolbarSaveButton.tsx` calls `writeSessionDraft`; existing callers
  in `src/editor/session/` use `EditorSessionService.save`.
- Repair target: Route toolbar save through the canonical session service or
  move the new validation into the service and migrate callers.
- Lens: abstraction-and-central-owner
```

```markdown
### [BLOCKING] Old command registry still exposes retired command metadata

- Checklist IDs: FILE-009, ABS-004, FEAT-003
- File: src/commands/legacyRegistry.ts
- Symbol / line: `registerSceneCommands`
- Risk: Phase scope moved command execution to the session command service, but
  the legacy registry still exposes executable command metadata. Users can
  still reach the old command path, so the system is not actually centralized.
- Evidence: `legacyRegistry.ts` still registers `scene.tune.*`; the new service
  registers the same command family in `SurfaceSceneDevCommandService`.
- Repair target: Delete the old registration or make it a non-executable
  adapter into the canonical service with a documented deletion point.
- Lens: side-doors-and-deletes
```

### Missing centralized abstraction

Flag when the code adds local logic that belongs in an existing central owner.

Common signs:

- a caller repeats validation instead of using the service, schema, helper, or
  adapter that owns it
- one package knows internals of another package
- a component reaches around the state/session owner
- a script reimplements runtime behavior
- tests encode production business rules instead of calling the canonical
  behavior
- a prompt or skill copies policy that should live in a shared reference

What to read:

- existing service, helper, schema, adapter, prompt reference, or config owner
  that appears to own the concept
- all new local copies of validation, normalization, parsing, routing, or
  policy
- callers that now choose between central and local behavior
- tests that may have copied the rule instead of exercising the owner

Block when:

- local code repeats a rule that already has one obvious owner
- a caller must remember to call two helpers in the right order
- the new helper exists only because the central owner was inconvenient
- a test can pass while production behavior diverges from the owner
- the new code makes the central owner less authoritative

Do not block when:

- the local rule is truly presentation-only or test-only and cannot affect the
  shared contract
- the repeated shape is just ordinary adapter glue with no business meaning
- the central owner does not actually own the changed concept after reading the
  code

Example findings:

```markdown
### [BLOCKING] Form validation duplicates the account schema

- Checklist IDs: FILE-002, ABS-001, FEAT-001
- File: src/account/AccountForm.tsx
- Symbol / line: `validateLocalAccount`
- Risk: The form now reimplements account-name validation instead of using
  `accountSchema`. The API and UI can now disagree on valid names, and future
  schema changes will not update this form.
- Evidence: `validateLocalAccount` checks length and character rules locally;
  `src/account/accountSchema.ts` already owns the same contract.
- Repair target: Route form validation through the canonical schema or extract
  the shared rule into the schema owner.
- Lens: abstraction-and-central-owner
```

```markdown
### [NON-BLOCKING] New test helper hides the production parser

- Checklist IDs: FILE-007, ABS-003
- File: tests/helpers/makeCommandFixture.ts
- Symbol / line: `makeCommandFixture`
- Risk: The helper hand-builds parsed command objects instead of calling the
  production parser. Tests can keep passing even if parser behavior breaks.
- Evidence: The helper returns `ParsedCommand` directly; no call reaches
  `parseCommandMetadata`.
- Repair target: Build fixtures from raw command text or add one integration
  assertion through the production parser.
- Lens: proof-and-tests
```

### Partial migration

Flag when the changed files migrate one route, caller, feature, or command but
leave adjacent same-contract paths using the old model without an explicit
bridge or follow-up.

Common signs:

- one UI action uses the new service while another action still calls the old
  writer
- one route accepts the new schema while a sibling route accepts the old shape
- one generated file is updated but another generated consumer is stale
- one command family moved to a new registry but aliases still point at the old
  registry
- a feature flag keeps both paths selectable after the migration is claimed
- tests update the happy path but leave legacy fixtures as valid examples

What to read:

- all adjacent routes, commands, jobs, components, prompts, scripts, and API
  methods that expose the same behavior
- old aliases, backward-compatibility flags, fallback readers, and direct
  mutation paths
- docs and examples that a future caller would copy
- delete list, migration notes, and plan scope when available

Block when:

- the user-facing behavior can still enter through the old path
- old and new data shapes both remain accepted without a hard adapter boundary
- plan scope or branch intent promised a migration, centralization, or delete
  that did not happen
- future code can copy a stale example and remain "supported"

Do not block when:

- the changed scope explicitly migrates only one isolated caller and leaves a
  named follow-up with no shared invariant broken
- compatibility is required and enforced by a single adapter that normalizes to
  the new internal model immediately

Example finding:

```markdown
### [BLOCKING] CLI migrated to the new config loader but scheduled jobs did not

- Checklist IDs: FILE-003, FILE-006, ABS-002, FEAT-002
- File: src/jobs/nightlyImport.ts
- Symbol / line: `loadImportConfig`
- Risk: The branch centralizes config loading for the CLI, but nightly jobs
  still read env vars directly. The same import can run with different defaults
  depending on entrypoint.
- Evidence: `src/cli/import.ts` now calls `ConfigService.loadImportConfig`;
  `nightlyImport.ts` still reads `process.env.IMPORT_BATCH_SIZE`.
- Repair target: Move the job to `ConfigService.loadImportConfig` or add a
  single adapter that both entrypoints use.
- Lens: side-doors-and-deletes
```

### Wrong-layer logic

Flag feature-specific logic in shared layers, transport details in domain
logic, persistence details in UI, product judgment in low-level utilities, or
agent workflow policy hidden in scripts.

Common signs:

- a shared helper knows a specific feature name
- UI components directly write persistence state
- domain models know HTTP request fields or GraphQL response details
- scripts decide product, workflow, or agent-review policy instead of doing
  narrow mechanics
- a prompt or skill hardcodes repo-local workflow policy that belongs in
  `AGENTS.md` or a reference file
- test utilities mutate production state through private internals

What to read:

- package or module boundaries around the changed file
- imports added by the change
- naming and ownership in nearby files
- existing adapters or service boundaries that normally isolate the concern
- tests that now need internal knowledge to use the changed code

Block when:

- a lower layer imports or names a higher-level product feature
- callers must understand internal persistence or lifecycle details
- future features are likely to copy the wrong layer because this change made
  it look normal
- scripts or generated artifacts now own reasoning that should remain agent or
  application judgment

Do not block when:

- the boundary is intentionally thin and the dependency direction already
  matches local architecture
- the code is a true adapter whose job is to translate between layers and it
  immediately normalizes the shape

Example finding:

```markdown
### [BLOCKING] Shared renderer now imports lesson-specific QA types

- Checklist IDs: FILE-005, ABS-003
- File: src/ui/playable_surface/renderSurface.ts
- Symbol / line: `renderSurfaceControls`
- Risk: The shared playable-surface renderer now imports lesson QA command
  types. That leaks feature-specific QA behavior into the shared rendering
  layer and makes puzzle surfaces inherit lesson-only concepts.
- Evidence: `renderSurface.ts` imports `LessonQaCommand`; nearby shared
  surface files depend only on surface interfaces.
- Repair target: Move the lesson command mapping behind a lesson-owned adapter
  or pass only the shared command interface into the renderer.
- Lens: caller-invariants-and-state
```

### Thin or fake abstraction

Flag wrappers that pass arguments through unchanged, helpers that hide the
important edge case, generic frameworks built before examples justify them,
and abstractions that add a concept without deleting a larger concept.

Common signs:

- `FooManager` only forwards to `foo`
- a helper exists for one call site and has no domain name
- an abstraction accepts a bag of flags because it does not own a real state
  model
- a wrapper makes tests mock the wrapper instead of the real behavior
- the new layer has the same method names as the wrapped layer
- "future flexibility" is the only reason the abstraction exists
- the abstraction makes invalid state easier, not harder

What to read:

- call sites before and after the abstraction
- repeated logic the abstraction claims to remove
- invariants the abstraction claims to own
- tests that now mock the abstraction
- local patterns for service, adapter, hook, component, or helper extraction

Block when:

- the abstraction adds a live concept but removes no meaningful complexity
- it hides the dangerous boundary rather than making it explicit
- it creates a second API that callers now need to choose between
- it forces broad mocking or makes behavior proof weaker

Do not block when:

- the wrapper names a real domain concept, hides a risky boundary, reduces
  caller burden, or makes invalid use harder
- extraction is needed to split a large file and the extracted unit has a clear
  owner and tests at the right level

Example findings:

```markdown
### [BLOCKING] `CommandExecutionFacade` is a second command API, not a simplifier

- Checklist IDs: FILE-006, ABS-004
- File: src/commands/CommandExecutionFacade.ts
- Symbol / line: `execute`
- Risk: The facade forwards every call to `CommandService.execute` with the
  same arguments. It gives callers two equivalent APIs and no new invariant,
  so command execution can drift between facade and service over time.
- Evidence: `CommandExecutionFacade.execute` delegates unchanged; new callers
  import the facade while existing callers use `CommandService`.
- Repair target: Delete the facade or move a real invariant into the canonical
  command service.
- Lens: maintainability-and-code-judo
```

```markdown
### [NON-BLOCKING] Extracted helper is valid but the name hides the invariant

- Checklist IDs: FILE-001, ABS-001
- File: src/billing/renewal.ts
- Symbol / line: `normalize`
- Risk: The helper is useful, but `normalize` hides that it specifically
  converts provider renewal state into internal subscription state. That makes
  future callers likely to use it for unrelated normalization.
- Evidence: The helper reads provider-specific fields and returns
  `SubscriptionRenewalState`.
- Repair target: Rename around the provider-to-domain conversion boundary.
- Lens: maintainability-and-code-judo
```

### Drift-prone proof

Flag tests that pass by duplicating the implementation rule, testing mocks
instead of behavior, asserting deletion without behavior proof, or ignoring the
highest-risk integration point.

Common signs:

- test repeats the same conditional as production code
- test asserts a helper was called but not the behavior that matters
- integration behavior is tested only through mocked adapters
- deletion is tested by grep or absence without proving old behavior is
  unreachable
- test fixtures build impossible states that production cannot produce
- snapshot tests bless a stale contract without a semantic assertion
- tests only prove the framework renders or the compiler accepts the code

What to read:

- changed tests and fixtures
- production behavior under test
- existing higher-level tests for the same behavior
- bug or plan obligation the proof is supposed to protect
- proof surfaces that would actually fail if the high-risk behavior regressed

Block when:

- risky behavior changed with no proof at the behavior boundary
- tests prove mocks, duplicated rules, or implementation details while missing
  the real integration
- fake fixtures make the implementation look valid in impossible states
- a plan or branch claims deletion but old behavior is still reachable

Do not block when:

- the change is a low-risk local refactor covered by typecheck, build, or
  existing tests
- a unit test is the right proof because the changed rule is truly isolated and
  callers share that rule through one owner

Example findings:

```markdown
### [BLOCKING] Test repeats the permission rule instead of exercising it

- Checklist IDs: FILE-008, FEAT-002
- File: tests/admin/deleteUser.test.ts
- Symbol / line: `canDeleteFixture`
- Risk: The test duplicates the admin permission conditional in fixture setup.
  If production permission logic changes, the test can still pass because the
  fixture changed independently from the real permission owner.
- Evidence: `canDeleteFixture` checks role and org status locally; production
  permission lives in `src/auth/permissions.ts`.
- Repair target: Build the test through the production permission API or add an
  integration assertion that reaches it.
- Lens: proof-and-tests
```

```markdown
### [BLOCKING] Delete proof only checks removed imports, not reachability

- Checklist IDs: FILE-010, FEAT-003
- File: tests/legacyCommandRemoval.test.ts
- Symbol / line: `does not import legacy registry`
- Risk: The test proves the new command service does not import the old
  registry, but it does not prove users cannot still execute legacy commands
  through aliases. The old behavior can remain live while this test passes.
- Evidence: Test asserts import absence; `src/commands/aliases.ts` still maps
  old command names.
- Repair target: Add behavior proof that legacy command aliases are removed or
  routed through the canonical service.
- Lens: proof-and-tests
```

### Stale truth surfaces

Flag docs, comments, examples, prompt references, generated files, telemetry
names, stable IDs, and install commands that now teach the wrong thing.

Common signs:

- README command uses the old CLI or env var
- docs point to deleted files or old module names
- examples instantiate old APIs
- comments explain a retired invariant
- prompt instructions tell agents to use an archived workflow
- generated artifacts were not regenerated after schema changes
- telemetry event names still imply the old behavior
- stable IDs or route names changed without migration notes where needed

What to read:

- touched docs and docs that mention changed symbols, commands, routes, schemas,
  env vars, prompts, generated artifacts, and public APIs
- comments near changed code
- examples, fixtures, generated output, snapshots, package metadata, Makefile
  targets, and README snippets
- agent-facing files such as `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, prompt
  references, and `agents/openai.yaml`

Block when:

- a future developer or agent would copy stale instructions and reintroduce the
  old path
- generated artifacts or schemas are now inconsistent with runtime code
- public commands, env vars, or install behavior changed but live docs teach
  the old contract
- comments hide a changed invariant in code that future maintainers will rely
  on

Do not block when:

- the doc is historical and clearly marked as historical
- the changed behavior is internal and no live doc, prompt, generated artifact,
  or example describes it
- a docs update is outside scope and the stale surface is unrelated to the
  changed behavior

Example finding:

```markdown
### [BLOCKING] README still teaches direct writer usage after service migration

- Checklist IDs: FILE-011, ABS-002, FEAT-001
- File: README.md
- Symbol / line: `Saving drafts`
- Risk: The code migrates draft writes behind `DraftService`, but the README
  still shows callers importing `writeDraft` directly. Future agents or
  developers can copy the stale example and bypass the centralized owner.
- Evidence: README example imports `writeDraft`; changed production code
  routes through `DraftService.save`.
- Repair target: Update the live example to use `DraftService` or remove the
  stale direct-writer snippet.
- Lens: docs-contract-generated-drift
```

### Error, boundary, and lifecycle gaps

Flag changed code that crosses a real boundary without carrying the boundary's
failure modes, lifecycle rules, or cleanup obligations.

Common signs:

- network call assumes success or ignores partial failure
- filesystem write is non-atomic where partial state matters
- process execution interpolates unsanitized input
- async tasks are launched without cancellation or joining
- subscription, timer, listener, or file handle is never cleaned up
- retry logic hides permanent failure
- error handling logs sensitive data or swallows the only useful diagnostic
- UI state updates after unmount or after stale request completion

What to read:

- boundary API docs when behavior depends on current platform or framework
  semantics
- existing wrappers around the same boundary
- error-handling conventions nearby
- caller expectations when the boundary fails
- tests, telemetry, and user-facing messages for the failure path

Block when:

- a changed external boundary has a reachable failure mode that would corrupt
  state, hide data loss, leak secrets, or leave resources alive
- the code handles success and silently drops failure
- lifecycle cleanup is now caller memory instead of owned by the abstraction

Do not block when:

- the boundary is already wrapped by a canonical helper that owns the failure
  mode and the changed code uses it correctly
- failure is impossible because the input is already validated or generated by
  a trusted local source, and that is visible in code

Example finding:

```markdown
### [BLOCKING] Import job can leave half-applied state on API failure

- Checklist IDs: FILE-004, FEAT-002
- File: src/jobs/importCustomers.ts
- Symbol / line: `runImport`
- Risk: The job writes imported customers before confirming the remote cursor
  update succeeded. If the cursor request fails, the next run can import the
  same page again and duplicate customers.
- Evidence: `saveCustomers(page.items)` runs before `updateCursor(page.next)`;
  the update error is logged but not used to roll back or retry atomically.
- Repair target: Move customer writes and cursor update behind one transaction
  or make the operation idempotent through the canonical import service.
- Lens: feature-and-behavior
```

### Caller contract and invariant leaks

Flag APIs where correct use depends on caller memory instead of shape,
ownership, or fail-loud enforcement.

Common signs:

- boolean flags select incompatible modes
- nullable fields allow impossible combinations
- caller must call `init` before `save` but type or runtime shape does not
  enforce it
- caller must pass matching arrays, indexes, or IDs by convention
- caller chooses between old and new APIs
- caller must know private lifecycle or persistence rules
- error-prone sequence is repeated across call sites

What to read:

- public API or exported function signatures
- all changed call sites and representative existing call sites
- type definitions and runtime guards
- tests that prove invalid states are impossible or fail loudly

Block when:

- the change creates a new state combination that should not exist
- new callers can misuse the API without an immediate failure
- the implementation moved an invariant out of the owner and into caller
  convention

Do not block when:

- the API is private to one file and all callers are visible and safe
- the impossible state is prevented by a stronger type, parser, schema, or
  runtime guard that the reviewer has read

Example finding:

```markdown
### [BLOCKING] New nullable state allows saved-but-unvalidated sessions

- Checklist IDs: FILE-002, ABS-001, FEAT-001
- File: src/session/sessionState.ts
- Symbol / line: `SessionState`
- Risk: `validatedAt?: Date` lets callers create a saved session with no
  validation timestamp, but downstream code treats any saved session as
  validated. That creates an impossible state the old model did not allow.
- Evidence: `saveSession` accepts `SessionState`; `renderSessionBadge` checks
  only `state.saved`.
- Repair target: Represent draft, validated, and saved states as distinct
  variants or make `saveSession` own validation.
- Lens: caller-invariants-and-state
```

### Agent, prompt, and skill surface regressions

Flag changes to instruction-bearing surfaces that make agents less capable,
less truthful, or more likely to bypass judgment.

Common signs:

- skill prose depends on hidden repo history instead of runtime context
- a script owns workflow judgment rather than narrow deterministic mechanics
- prompt text replaces reasoning with keyword rules or brittle checklists
- an agent-facing doc names archived commands as live runtime behavior
- multiple skills claim the same lane with no peer boundary
- generated skill output and source doctrine can drift
- install docs, runtime metadata, and `README.md` disagree on available skills

What to read:

- changed `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, prompt files, `agents/*.yaml`,
  generated `build/` outputs, install docs, and Makefile targets
- sibling skills with overlapping descriptions
- local skill-authoring or prompt-authoring doctrine when relevant

Block when:

- the change makes a shipped skill depend on archived command files at runtime
- the change moves judgment into a runner without a real deterministic reason
- the skill trigger overlaps a peer and would route the wrong requests
- source, generated, and install surfaces disagree about what ships

Do not block when:

- a checklist is used as a judgment aid and the agent still owns synthesis
- a script only performs narrow mechanics such as formatting, parsing, or API
  calls and reports bounded output

Example finding:

```markdown
### [BLOCKING] Skill trigger now overlaps `plan-audit` and hides the boundary

- Checklist IDs: FILE-003, ABS-002
- File: skills/example-review/SKILL.md
- Symbol / line: `description`
- Risk: The description claims both generic branch review and plan-backed
  implementation review. That makes the runtime unable to choose between this
  skill and `plan-audit implementation-audit`, and the two skills can develop
  separate completion doctrine.
- Evidence: The description says "review any branch or plan implementation";
  `plan-audit` already owns plan-backed implementation review.
- Repair target: Narrow the trigger to the actual lane and add a handoff line
  to `plan-audit` for plan-backed implementation audits.
- Lens: agent-and-prompt-surface
```

### Security and trust-boundary regressions

Flag only reachable security risks introduced or worsened by the reviewed
change. Do not generate generic security warnings.

Common signs:

- user input reaches command execution, SQL, shell, filesystem paths, HTML,
  templates, deserialization, or network requests
- auth or authorization checks move from owner to caller
- logs now include secrets, tokens, credentials, PII, or request bodies
- dependency or infrastructure trust changes without pinning or validation
- file upload, archive extraction, or path handling lacks normalization
- SSRF, redirect, CORS, CSRF, or tenant-boundary assumptions changed

What to read:

- changed trust boundary
- existing auth, validation, escaping, logging, and secret-handling owners
- all paths from input source to dangerous sink
- official docs or OWASP/CERT only when the security claim depends on current
  external behavior

Block when:

- a changed path lets untrusted input reach a dangerous sink
- authorization is enforced by caller memory instead of the canonical boundary
- sensitive data can be logged or exposed
- tenant, account, org, or workspace isolation can be bypassed

Do not block when:

- the changed value is not attacker-controlled and the reviewer can cite why
- the canonical boundary already validates the value and all changed paths use
  that boundary

Example finding:

```markdown
### [BLOCKING] Export path now trusts user-controlled filenames

- Checklist IDs: FILE-006, FEAT-003
- File: src/export/writeExport.ts
- Symbol / line: `writeExport`
- Risk: The export path joins a user-provided filename directly into the output
  path. A crafted filename can write outside the export directory.
- Evidence: `path.join(exportDir, request.filename)` is used without basename
  or path normalization checks; `request.filename` comes from the API body.
- Repair target: Normalize and validate filenames at the export boundary, or
  generate server-owned filenames.
- Lens: security-boundary
```

## 12. Output Contract

The final answer should point to the run artifact and include the verdict. The
full artifact owns the detailed checklists.

Verdicts:

- `approve`: every required checklist item is closed, native parallel agents
  ran, there are no blocking findings, and no trust-breaking coverage gap
  remains.
- `approve-with-notes`: every required checklist item is closed, native
  parallel agents ran, there are no blocking findings, and non-blocking
  findings remain.
- `not-approved`: one or more blocking findings remain.
- `coverage-blocked`: the review target, native parallel agents, changed-file
  inventory, abstraction inventory, or required code surfaces could not be
  resolved or inspected.

Final verdict shape:

```markdown
# ExhaustiveCodeReviewVerdict

VERDICT: approve | approve-with-notes | not-approved | coverage-blocked
Scope:
Run artifact:
Native parallel agents: used | unavailable | not used

## Blocking Findings

<findings or "No blocking findings.">

## Non-Blocking Findings

<findings or "No non-blocking findings.">

## Coverage Closure

- Files: <closed>/<total>, blockers: <count>
- Abstractions: <closed>/<total>, blockers: <count>
- Features/behaviors: <closed>/<total>, blockers: <count>
- Changed hunks read: yes | no
- Native child reports spot-checked: yes | no
- Negative-space pass: clean | found gaps | not run

## Open Coverage Gaps

<list or "No open coverage gaps.">

## Recommended Next Move

<one exact repair, rerun, or coverage action>
```

Finding shape:

```markdown
### [BLOCKING|NON-BLOCKING] <short title>

- Checklist IDs: <FILE-###, ABS-###, FEAT-###>
- File: <repo-relative path>
- Symbol / line: <symbol or line>
- Risk: <concrete risk in plain language>
- Evidence: <diff, file, child report, command output, or source anchor>
- Repair target: <what must change, without writing the patch>
- Lens: <review lens>
```

Rules:

- No placeholder sections with filler.
- No finding without file, symbol or line, risk, evidence, and repair target.
- No approval while any file, abstraction, or feature item is unclosed.
- No approval if native parallel agents did not run, unless the user explicitly
  asked for a sequential fallback and the verdict states that limitation.
- No claiming a child finding as verified until the parent spot-checks the
  anchor.
- No broad advice that is not tied to changed-code risk.

## 13. Approval Bar

The future skill should treat these as approval blockers:

- any touched file not fully reviewed
- any touched abstraction not classified
- any feature or behavior obligation not reviewed
- any changed hunk not read
- any required caller, side door, generated artifact, schema, prompt, doc, or
  proof surface not read and not ruled irrelevant
- native parallel agents unavailable or not used in a formal run
- old and new abstraction paths both live without an explicit approved bridge
- duplicate truth introduced or worsened
- changed code bypasses the canonical owner path
- old callers still route around the new owner
- tests prove duplicate rules, mocks, or implementation details instead of
  behavior where behavior is the real risk
- docs, prompts, examples, schemas, or generated artifacts still teach stale
  behavior
- security-boundary changes with unreviewed failure modes
- agent/prompt changes that replace judgment with unjustified scripts,
  runners, or scaffolding

The skill should allow approval when the code is genuinely clean. Exhaustive
does not mean suspicious forever. It means the review can name exactly what it
checked and why the remaining risk is acceptable.

## 14. Proposed Future Package Shape

When implemented later, the package should stay lean but split details into
references.

```text
skills/exhaustive-code-review/
  SKILL.md
  references/
    scope-resolution.md
    checklist-contract.md
    native-agent-prompts.md
    review-lenses.md
    split-brain-and-centralization.md
    output-contract.md
    examples.md
  agents/
    openai.yaml
```

Do not add `scripts/` in V1.

Expected ownership:

- `SKILL.md`: trigger contract, peer boundary, non-negotiables, first move,
  workflow, and reference map.
- `scope-resolution.md`: how to resolve worktree, branch, commit range,
  plan-backed, path, and completion-claim scopes.
- `checklist-contract.md`: file, abstraction, feature, and native-agent
  checklist schemas.
- `native-agent-prompts.md`: parent orchestration rules and native child prompt
  templates.
- `review-lenses.md`: the review lenses and their evidence requirements.
- `split-brain-and-centralization.md`: deep doctrine for bifurcated
  abstractions, source of truth failures, wrong owner paths, side doors, and
  partial migration.
- `output-contract.md`: final verdict and finding schema.
- `examples.md`: short examples showing branch review, plan-phase review,
  path-scope review, clean approval, and coverage-blocked output.

## 15. Implementation Plan For Later

Do not implement this now. When the user later asks to implement it, use
`$skill-authoring` and keep the work inside the future skill package.

Suggested later implementation phases:

1. Create the prompt-only skill package and metadata.
2. Write `SKILL.md` with the lean runtime contract and peer boundary.
3. Add `checklist-contract.md`, `native-agent-prompts.md`, `review-lenses.md`,
   `split-brain-and-centralization.md`, and `output-contract.md`.
4. Add small examples that prove trigger boundaries and output shape.
5. Run `npx skills check`.
6. Review the package manually against this planning document.
7. Update `README.md` and `docs/arch_skill_usage_guide.md` only if the new
   skill becomes part of the install or routing surface.

## 16. Open Design Decisions

These do not block the plan, but they should be decided during implementation:

- Whether formal reviews should always write `/tmp/exhaustive-code-review/...`
  artifacts or allow chat-only artifacts for tiny path scopes.
- Whether a sequential fallback should exist at all, or whether missing native
  parallel agents should always be `coverage-blocked`.
- Whether test execution is ever part of this skill or always delegated to
  `verify-this` or a user-requested verification pass.
- Whether plan-backed runs should optionally append findings to
  `<PLAN_STEM>_PLAN_AUDIT.md`, or whether that belongs only to `plan-audit`.
- Whether `code-review` should mention this skill as the exhaustive alternative
  once the package exists.

## 17. Success Test

The future skill is successful when a reviewer can answer these questions from
the final artifact without trusting memory:

- Which files changed?
- Which changed hunks were read?
- Which symbols changed?
- Which abstractions were touched?
- Which abstraction is the canonical owner?
- Which old paths, callers, side doors, docs, prompts, tests, schemas, and
  generated artifacts were checked?
- Which native agents ran, what did each inspect, and what did each skip?
- Which findings came from which checklist item?
- Which clean items were actually read and closed?
- What, if anything, remains unreviewed?

If those questions cannot be answered, the review was not exhaustive.
