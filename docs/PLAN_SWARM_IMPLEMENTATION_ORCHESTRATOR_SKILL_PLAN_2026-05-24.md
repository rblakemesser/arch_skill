# Plan Swarm Implementation Orchestrator Skill Plan

Status: planning document only. Do not treat this as implemented behavior.

Date: 2026-05-24

Working skill name: `plan-swarm`

Related prerequisite doc:
`docs/cursor_agent_cli_integration_deep_dive_2026-05-24.md`

## 0. User Problem

The current slow path is a single agent trying to implement a plan phase
serially. A typical prompt looks like:

```text
Finish only Phase 14 of the puzzle DevTab Theme Parity Plan in
docs/PACKS/puzzle_dev_tab_theme_parity_2026-05/puzzle-dev-tab-parity-plan.md.

Current inferred open phase: ### 14. Split Command Metadata From Execution And
Share QA Adapters.

Use that pack as the only source of truth for Phase 14 scope, owner
boundaries, cleanup, validation, and save/QA behavior. Do not create a second
plan and do not continue into broader final-pack signoff work.

Phase 14 target state: scene tuning command metadata is passive, execution goes
through SurfaceSceneDevCommandService and SurfaceSceneDevSession, lesson/puzzle
QA adapters only register feature-owned QA commands, shared
ui/playable_surface/** does not import feature QA types, overlays do not call
raw writers/providers, and legacy direct mutation/save paths are removed or
tightly walled off with an explicit deletion checkpoint.

Before editing, re-read Phase 14 plus the pack's Definition Of Done items that
mention QA adapters, overlays, command service, persistence, owner-boundary
tests, old mutation paths, and legacy removal. If Phase 14 lacks execution
detail, recover the real contract from owning code, tests, schemas, generated
artifacts, and current behavior.
```

That prompt is good as a phase goal, but it gives the runtime only one worker.
On broad implementation phases, a single worker spends too much wall time
reading, editing, testing, reviewing, and repairing in sequence.

`plan-swarm` should preserve the plan as the source of truth while using
parallel implementation workers, session reuse, and review gates to reduce
wall-clock time without lowering the quality bar.

## 1. North Star

Build a reusable implementation orchestrator skill that takes a plan document
and one active phase, decomposes that phase into independently executable
slices, dispatches implementation agents in parallel through the selected
runtime, reuses useful worker sessions for related repair, coordinates scarce
test resources, writes durable work logs next to the plan, and refuses to move
past a phase until independent review and maintainability review agree the
phase is actually complete.

The skill is optimized for velocity with quality control, not for ceremony.
Workers should receive real goals and enough context to reason. They should
not be boxed into tiny mechanical prompts that prevent useful adjacent fixes.

## 2. Mechanism Choice

This should be a skill, not only a one-shot prompt, because the workflow is
repeated, multi-step, stateful, and easy to execute poorly by hand.

It should be script-backed, not purely prompt-only, because the core value
depends on deterministic orchestration details:

- launching multiple child agents concurrently
- capturing `session_id` / `thread_id` handles
- resuming the right worker for related repairs
- tracking worker health and repeated failure
- scheduling waves based on dependencies and shared resources
- writing per-worker artifacts and human work logs
- parsing status footers from child outputs
- preserving one state file that can be resumed after interruption
- avoiding ambiguous "latest session" behavior

This is one of the cases where skill-authoring doctrine allows a runner: the
user explicitly wants orchestration, and natural-language-only execution would
make the slow manual coordination problem reappear.

The skill should still stay prompt-first at the edges. The runner owns
plumbing and receipts. The skill prose owns judgment, phase interpretation,
slice quality, prompt contracts, review standards, and when to ask or stop.

## 3. Peer Boundary

Nearest lookalikes:

- `agent-delegate`: launches one or more foreground workers. It is the child
  execution primitive, not the plan-phase owner.
- `fresh-consult`: read-only cold opinions. It does not implement or repair.
- `model-consensus`: two-model plan convergence. It does not run a plan phase.
- `stepwise`: strict ordered named process execution. It is serial by process
  step and critic loop, not a plan-phase parallel accelerator.
- `arch-epic`: decomposes a large goal into ordered sub-plans around
  `arch-step`. It is depth-first multi-plan orchestration, not parallel
  execution inside one approved phase.
- `arch-loop` / `goal-loop`: hook-backed repeat loops. They do not decompose a
  plan phase into parallel worker slices.
- `code-review`: deterministic review product. It reviews; it does not own
  implementation dispatch.
- `thermo-nuclear-code-quality-review`: maintainability review rubric. It is a
  quality gate used by this skill, not the implementation orchestrator.

`plan-swarm` owns the throughline from an active plan phase to parallel
implementation and phase closure. It should call or reuse the lower-level
child-agent runtime contracts instead of becoming a generic review, planning,
or arch-step replacement.

## 4. Canonical User Asks

Good trigger asks:

- "Use Cursor Agent to finish Phase 14 of this plan as fast as possible with
  parallel agents, then hold the quality bar."
- "Run the current open phase in this plan with parallel Codex workers and
  keep a work log next to the plan."
- "Take this plan doc phase through implementation using parallel delegated
  agents, review the work, fix the review findings, and stop at the phase
  boundary."

Anti-case:

- "Break this giant product goal into sub-plans and run them one at a time."
  Use `arch-epic`.

Another anti-case:

- "Run this named ordered workflow with a critic per step." Use `stepwise`.

## 5. Source Of Truth Rules

The plan document is authoritative for:

- active phase scope
- owner boundaries
- cleanup expectations
- validation and proof obligations
- save/QA behavior
- phase-local exclusions
- broader plan Definition Of Done items that explicitly apply to the active
  phase

The orchestrator must not create a second plan. Its decomposition is an
execution schedule and evidence ledger, not a competing requirements source.

If the phase lacks execution detail, workers may recover the real contract from
owning code, tests, schemas, generated artifacts, current behavior, and local
instructions. Those recovered facts are evidence for executing the plan; they
do not rewrite or expand the approved scope unless the plan itself requires the
discovered work.

The orchestrator stops at the requested boundary:

- one phase if the user names one phase
- the current inferred open phase if the user asks for the current phase
- the full plan only if the user explicitly asks for the whole plan

## 6. Required Cursor Agent Prerequisite

Before `plan-swarm` can use Cursor Agent as an implementation runtime, add
`runtime=agent` support to the child-agent skills it depends on:

- `fresh-consult`
- `agent-delegate`
- `model-consensus`

The local research already found that `agent` is Cursor Agent CLI and supports:

- `agent -p` for non-interactive execution
- prompt stdin
- `--output-format json`
- `--output-format stream-json`
- terminal `result.result`
- terminal `result.session_id`
- `--resume <session_id>`
- `--workspace <path>`
- `--model <model>`
- `--force`
- `--sandbox disabled`
- `--trust`

Cursor-specific integration rules:

- Treat `agent`, `cursor`, `cursor agent`, and `cursor-agent` as
  `runtime=agent`.
- For implementation workers using Cursor Agent, default the model to
  `composer-2.5-fast` unless the user explicitly overrides it.
- Store Cursor effort as `encoded-in-model` or `not-applicable` for the default
  Composer path. Do not invent a separate Cursor `--effort` flag.
- Always pass `--output-format` explicitly because local help and official docs
  disagreed on the default.
- Capture final text by parsing the terminal `result` event and writing
  `final.txt`.
- Capture resumable session identity from terminal `result.session_id`.
- Use `--resume <session_id>` only. Never use `--continue`, `agent resume`, or
  latest-session selection.
- Do not use `--worktree` in this workflow unless a future user explicitly asks
  for a worktree-based variant. Current repo policy says never create
  worktrees unless specifically asked.

## 7. Execution Policy

The user supplies or implies the implementation runtime.

Accepted runtime choices after prerequisite work:

```text
implementation_runtime: codex | claude | agent
implementation_model: <runnable model id>
implementation_effort: low | medium | high | xhigh | max | encoded-in-model | not-applicable
review_runtime: codex | claude | agent
review_model: <runnable model id>
review_effort: low | medium | high | xhigh | max | encoded-in-model | not-applicable
```

Suggested defaults only when the user explicitly says to use Cursor Agent:

```text
implementation_runtime: agent
implementation_model: composer-2.5-fast
implementation_effort: encoded-in-model
```

The skill should not silently choose Codex or Claude models. For non-Cursor
runtimes, ask one consolidated question when runtime, model, or effort is
missing.

Review policy can default to the implementation runtime only if the user says
"same model for review" or similar. Otherwise, ask once because review model
quality materially changes the phase gate.

## 8. Lifecycle

The orchestrator has seven stages.

1. **Intake.** Resolve plan path, active phase, repo root, implementation
   runtime, review runtime, and stop boundary.
2. **Phase contract extraction.** Read the active phase plus plan-level
   Definition Of Done items that mention the phase's surfaces.
3. **Execution graph.** Decompose the phase into independent and dependent
   slices, with expected proof and resource needs.
4. **Parallel implementation waves.** Launch available slices through
   `agent-delegate`-style resumable workers.
5. **Merge and evidence check.** Inspect worker reports, repo state, work logs,
   changed files, proof output, and conflicts.
6. **Arbiter review loop.** Use an `agent-delegate` review worker to judge
   exact plan completion and architectural cleanliness. Route accepted findings
   back to workers.
7. **Phase quality gate.** Run thermonuclear maintainability review, triage
   findings, repair accepted items in parallel, then mark the phase done only
   when the phase contract, arbiter, and thermonuclear gate are clean enough.

At whole-plan completion only, add a heavier final review lane:

- broad fresh consult or code-review across the full plan outcome
- final proof sweep
- final worklog summary

Do not spend final-plan review budget on every ordinary phase unless the user
asks for that heavier mode.

## 9. Active Phase Contract Extraction

The first substantive output of the orchestrator is a compact phase contract.
It should be written to the run directory and summarized in the human worklog.

Suggested file:

```text
<plan-dir>/<plan-basename>_plan_swarm/<phase-slug>/phase-contract.md
```

The phase contract should contain:

```markdown
# Phase Contract

- Plan path:
- Active phase heading:
- Stop boundary:
- Target state:
- In-scope surfaces:
- Out-of-scope surfaces:
- Owner boundaries:
- Cleanup obligations:
- Validation obligations:
- Save / QA behavior obligations:
- Definition Of Done excerpts that apply:
- Recovered code/test/schema facts:
- Unknowns that workers may resolve from repo evidence:
- Unknowns that require user input:
```

The contract must stay small enough to fit into child prompts. If the plan is
long, point children to paths and headings instead of copying the whole plan.

## 10. Execution Graph

The execution graph is not a second plan. It is the orchestrator's schedule and
evidence model for one phase.

Suggested machine file:

```text
.arch_skill/plan-swarm/<plan-slug>/<phase-slug>/<run-id>/execution-graph.json
```

Suggested human file:

```text
<plan-dir>/<plan-basename>_plan_swarm/<phase-slug>/execution-ledger.md
```

Each slice should have:

```json
{
  "id": "qa-adapters-feature-owned-commands",
  "title": "Make lesson/puzzle QA adapters register only feature-owned commands",
  "goal": "One outcome a capable agent can own without micromanagement.",
  "source_truth": [
    "docs/.../plan.md#14-split-command-metadata-from-execution-and-share-qa-adapters",
    "docs/.../plan.md#definition-of-done"
  ],
  "primary_expected_areas": [
    "feature adapter files",
    "tests covering QA registration"
  ],
  "likely_adjacent_areas": [
    "shared command registration contracts"
  ],
  "depends_on": [],
  "blocks": [],
  "collision_group": "qa-adapters",
  "resource_needs": [],
  "proof_needed": [
    "owner-boundary test or equivalent grep/assertion",
    "changed behavior described in worker worklog"
  ],
  "session_affinity": "resume-for-related-repair",
  "status": "pending"
}
```

The scheduler uses the graph to choose parallel waves:

- slices with unmet dependencies wait
- slices in the same collision group prefer the same worker or serial waves
- slices using scarce resources need a lease
- cleanup/deletion slices usually run after the replacement path exists
- final save/persistence proof usually waits until related implementation
  slices finish

## 11. Decomposition Principles

A good slice is large enough for a smart worker to reason, small enough to
finish without owning the entire phase, and independent enough to run beside
other slices.

Split by:

- canonical owner boundary
- dependency boundary
- proof boundary
- deletion/replacement boundary
- scarce-resource boundary
- collision risk

Do not split by:

- one file per worker when the concept spans several files
- one TODO per worker when the TODOs share one design decision
- arbitrary equal-sized chunks
- brittle keyword categories
- hard write scopes that prevent needed adjacent cleanup

Useful slice shapes:

- "Move execution through the command service/session boundary."
- "Convert QA adapters to feature-owned command registration."
- "Remove direct writer/provider mutation paths after replacement flow exists."
- "Add owner-boundary tests and persistence/save coverage."
- "Update overlays so they call the service/session instead of raw writers."

Bad slice shapes:

- "Edit file A only."
- "Change all references to string X."
- "Do not inspect anything outside this folder."
- "Make these five mechanical changes and stop even if the tests reveal the
  ownership model is wrong."

## 12. Avoiding Over-Prompted Workers

The most common failure mode is prompting workers so narrowly that they cannot
solve the real problem.

Worker prompts should give:

- the phase contract
- the slice outcome
- the plan path and headings to read
- primary expected areas
- proof expected
- coordination/worklog requirements
- the fact that siblings may be editing concurrently

Worker prompts should not give:

- a long list of forbidden files unless the plan truly forbids them
- a command-by-command implementation recipe
- a speculative diagnosis from the parent as if it were ground truth
- tiny mechanical steps that prevent the worker from following repo evidence
- arbitrary "do not touch" limits that block obvious adjacent repairs

Use this wording style:

```text
Your primary expected areas are X and Y. Use judgment for adjacent edits that
are needed to make this slice correct. Do not revert unfamiliar work. If the
right fix requires expanding beyond the expected areas in a surprising way,
pause and report the evidence instead of silently broadening the phase.
```

That preserves autonomy while still preventing scope drift.

## 13. Implementation Worker Prompt Contract

The prompt should be durable, but not bloated.

Suggested skeleton:

```markdown
You are a plan-swarm implementation worker for one slice of an approved plan
phase. You do not have the parent chat context. Read the repo and plan evidence
directly from disk.

# Mission

Complete this slice so it genuinely satisfies the active phase contract and can
be reviewed by another agent from the plan, diff, tests, and worklog.

# Source Of Truth

- Work root: <absolute repo root>
- Plan path: <absolute plan path>
- Active phase: <heading>
- Phase contract path: <path>
- Slice ledger path: <path>
- Your worklog path: <path>

# Slice

- Slice id: <id>
- Goal: <one outcome>
- Primary expected areas: <paths/symbols/modules>
- Likely adjacent areas: <paths/symbols/modules or "unknown">
- Dependencies already satisfied: <short evidence>
- Sibling work in flight: <slice ids and rough areas>
- Scarce-resource policy: <what this worker may or may not run>

# Operating Rules

1. Read the active phase and phase contract before editing.
2. Use repo evidence to recover missing execution detail.
3. Make the smallest coherent implementation that satisfies the slice.
4. Use judgment for adjacent edits needed for correctness.
5. Do not revert unfamiliar changes.
6. If a sibling conflict is real, report the files and evidence instead of
   guessing.
7. Leave durable evidence in your worklog.

# Verification

Run focused checks that are safe under your resource policy. If a needed check
requires a leased resource you do not own, write the exact requested check in
your worklog.

# Report Contract

End with this footer:

STATUS: done | partial | blocked | failed
SLICE ID: <id>
CHANGED FILES: <paths or "none">
WORKLOG: <path and summary of entries added>
VERIFICATION: <commands/results or "not run: reason">
RESOURCE REQUESTS: <scarce checks needed or "none">
SIBLING CONFLICTS: <files/evidence or "none">
BLOCKERS: <bullets or "none">
FOLLOW-UP NEEDED: <bullets or "none">
SESSION HEALTH: good | uncertain | bad
SUMMARY FOR PARENT: <one concise paragraph>
```

`SESSION HEALTH` is important. The orchestrator uses it when deciding whether
to resume the same worker for related repairs.

## 14. Review Arbiter Contract

The review arbiter is a delegated agent, not the parent doing a vibes check.
Use `agent-delegate` in a review-only prompt with allowed write scope `none`.
The child should not edit files.

The arbiter answers two questions:

1. Was this part of the plan implemented exactly as specified?
2. Is the implementation architecturally clean enough, or is there a simpler
   and more canonical structure the phase should use before it is accepted?

Suggested skeleton:

```markdown
You are the plan-swarm phase arbiter. You are reviewing the current work
against the approved plan phase. Do not edit files.

# Source Of Truth

- Work root: <absolute repo root>
- Plan path: <absolute plan path>
- Active phase: <heading>
- Phase contract path: <path>
- Execution ledger path: <path>
- Worker worklogs: <paths>
- Diff target: current uncommitted diff unless otherwise stated

# Review Job

Determine whether the implemented work satisfies the phase contract exactly
and whether the implementation is architecturally clean.

Read the plan, the worklogs, the changed files, and whatever owning code/tests
you need. Look for dropped requirements, owner-boundary leaks, unproven save/QA
behavior, direct mutation paths that should be gone, weak tests, and structural
mess introduced by the implementation.

# Scope Discipline

Do not expand the phase. A finding must be tied to one of:

- the active phase contract
- a Definition Of Done item that applies to this phase
- behavior changed by this phase
- maintainability damage introduced by this phase's diff
- an architectural cleanup explicitly required by the phase

Pre-existing unrelated debt is not a blocking finding for this phase unless the
phase depends on it.

# Output Contract

VERDICT: pass | incomplete | architecture-blocked | scope-drift | inconclusive
BLOCKING FINDINGS: <bullets with file/symbol/evidence or "none">
NON-BLOCKING FINDINGS: <bullets or "none">
ARCHITECTURE CLEANLINESS: clean | acceptable | needs-rework | unclear
PLAN COVERAGE: <bullets mapping phase requirements to evidence>
PROOF GAPS: <commands/tests/evidence still needed or "none">
RECOMMENDED ROUTING: <which slice/worker should handle each accepted finding>
EVIDENCE READ: <paths/commands actually inspected>
CONFIDENCE: high | medium | low
SUMMARY FOR PARENT: <one concise paragraph>
```

The parent may disagree with the arbiter, but it must record why and cite the
plan or repo evidence that overrides the arbiter.

## 15. Thermonuclear Quality Gate

When the phase contract looks satisfied and the arbiter is clean enough, run a
strict maintainability pass using the installed
`$thermo-nuclear-code-quality-review` rubric.

Recommended shape:

- launch a read-only delegate with a prompt that explicitly says to use
  `$thermo-nuclear-code-quality-review`
- target the current phase diff and changed files
- include the phase contract and worklogs as context
- ask for high-conviction structural findings only
- require every finding to say whether it is introduced by this phase, exposed
  by this phase, or unrelated pre-existing debt

The parent then triages findings:

```text
accepted: in current phase scope, introduced by current work, or needed to keep
the phase's architecture clean

deferred: valid but belongs to a later plan phase or final plan signoff

rejected: not supported by evidence, arbitrary scope expansion, or unrelated
pre-existing debt
```

Accepted thermonuclear findings become repair slices and should be routed in
parallel when independent. Prefer resuming the worker that owns the related
implementation slice unless that worker has poor session health.

## 16. Session Reuse Policy

Default: resume the same worker for related repair.

Resume when:

- the finding is in the worker's slice or direct adjacent area
- the worker reported `SESSION HEALTH: good`
- the worker made real progress
- the fix depends on context the worker already built
- the failure is a normal miss, not a broken mental model

Spawn fresh when:

- the worker reported `SESSION HEALTH: bad`
- the worker repeatedly fails the same requirement
- the worker misunderstood the phase contract in a way that would poison
  repair
- the repair depends on upstream work that invalidates the worker's history
- the session handle is missing or `UNRECOVERABLE`
- the repair crosses several slices and needs a clean integrator

Use the same runtime when resuming. Do not cross-resume Codex into Claude,
Claude into Cursor Agent, or Cursor Agent into Codex.

Every worker record should keep:

```json
{
  "worker_id": "impl-qa-adapters-01",
  "slice_ids": ["qa-adapters-feature-owned-commands"],
  "runtime": "agent",
  "model": "composer-2.5-fast",
  "effort": "encoded-in-model",
  "session_id": "<runtime session id>",
  "latest_run_dir": "<agent-delegate run dir>",
  "health": "good",
  "changed_files": [],
  "last_status": "done",
  "resume_count": 0,
  "failure_count": 0
}
```

## 17. Resource Leases

Parallel editing is useful. Parallel expensive verification can be destructive
or wasteful.

The orchestrator should maintain resource leases for shared bottlenecks:

- full test suite
- mobile simulator
- browser automation profile
- local dev server
- database or fixture store
- generated artifact writer
- long-running build
- high-core CPU task

Default rule:

- implementation workers can run cheap, focused checks
- only one worker at a time can hold a scarce verification lease
- the parent can designate a verification worker for full-suite, simulator, or
  expensive integration checks
- workers without a lease should write requested checks into their worklog

Machine state:

```json
{
  "resource_leases": {
    "full_test_suite": {
      "holder": "verify-phase-01",
      "status": "held",
      "started_at": "2026-05-24T00:00:00Z",
      "purpose": "phase-level regression after wave 2"
    },
    "simulator": {
      "holder": null,
      "status": "available"
    }
  }
}
```

Worker prompt language:

```text
You may run focused file/package checks that do not monopolize shared
resources. Do not run the full suite, start a shared simulator, or take over a
long-lived dev server unless this prompt grants that lease. If you need one of
those checks, record the exact command and reason in RESOURCE REQUESTS.
```

## 18. Work Logs

The skill should write logs next to the plan, not inside chat only.

For a plan:

```text
docs/PACKS/example/example-plan.md
```

Use:

```text
docs/PACKS/example/example-plan_plan_swarm/
  phase-14-split-command-metadata/
    phase-contract.md
    execution-ledger.md
    orchestration-log.md
    agents/
      impl-command-service.md
      impl-qa-adapters.md
      impl-overlays.md
      verify-phase.md
    reviews/
      arbiter-01.md
      thermo-01.md
      final-plan-review.md
```

Heavy event streams stay under `.arch_skill/plan-swarm/...`, not in docs.

Human worklogs should include:

- what was assigned
- which agent/session owns it
- what changed
- verification attempted
- requested scarce checks
- review findings
- repair routing
- accepted/rejected thermonuclear findings
- current phase status

Do not mark a phase complete because a worker said it was complete. Mark it
complete only after the orchestrator can point to plan coverage, proof, arbiter
result, and quality-gate triage.

## 19. Runtime Artifact Layout

Machine artifacts should be ignored by git unless the user explicitly wants to
commit them. This repo already ignores `.arch_skill/arch-epic/`; implementing
this skill should add `.arch_skill/plan-swarm/` to `.gitignore`.

Suggested layout:

```text
.arch_skill/plan-swarm/<plan-slug>/<phase-slug>/<run-id>/
  state.json
  execution-policy.json
  phase-contract.md
  execution-graph.json
  leases.json
  workers/
    <worker-id>/
      worker.json
      attempts/
        001/
          prompt.md
          final.txt
          events.jsonl
          stderr.log
          execution.json
          session_id.txt
  reviews/
    arbiter-001/
      prompt.md
      final.txt
      events.jsonl
      stderr.log
      verdict.json
    thermo-001/
      prompt.md
      final.txt
      events.jsonl
      stderr.log
      triage.json
  waves/
    wave-001.json
    wave-002.json
  reports/
    status.md
    final-phase-report.md
```

The docs-side worklog is for humans. The `.arch_skill` tree is for resumption,
debugging, parsing, and exact child receipts.

## 20. Runner Interface

Recommended script:

```text
skills/plan-swarm/scripts/run_plan_swarm.py
```

The runner should have subcommands that keep the parent agent in control:

```text
init-run
extract-phase
write-graph
spawn-wave
resume-worker
spawn-arbiter
spawn-thermo
triage-review
status
report
```

The runner should not decide what the phase means. The parent skill does that
from the plan and repo evidence.

Runner responsibilities:

- create run directories
- validate execution policy
- write prompts passed by the parent
- invoke Codex, Claude, or Cursor Agent using the resolved runtime
- capture streams, final text, session ids, and exit codes
- parse footers into machine records
- enforce explicit resume handles
- track resource leases
- record wave state
- render status summaries from state

Parent-skill responsibilities:

- interpret the plan phase
- choose slice decomposition
- write good worker prompts
- decide which findings are accepted
- decide whether to resume or respawn
- decide whether the phase is complete
- report the state to the user

## 21. Child Runtime Adapter

The implementation should avoid copying three separate subprocess command
builders into every future skill.

Recommended shared helper:

```text
skills/_shared/child_agent_runtime.py
```

It should expose:

```python
spawn_child(runtime, mode, policy, work_root, prompt_path, artifact_dir)
resume_child(runtime, policy, session_id, work_root, prompt_path, artifact_dir)
parse_final(runtime, events_path, final_path)
parse_session_id(runtime, events_path, final_path)
```

Supported runtimes:

- `codex`
- `claude`
- `agent`

This helper can later replace duplicated logic in `arch-epic` and `stepwise`,
but the first implementation should not refactor those skills unless needed.
Keep the initial change scoped to the new skill and the Cursor Agent
integration prerequisite.

## 22. State Machine

`state.json` should be the resumable truth.

Suggested top-level shape:

```json
{
  "schema_version": 1,
  "plan_path": "/abs/path/to/plan.md",
  "plan_sha256_at_start": "<hash>",
  "work_root": "/abs/path/to/repo",
  "active_phase": {
    "heading": "### 14. Split Command Metadata From Execution And Share QA Adapters",
    "slug": "phase-14-split-command-metadata",
    "status": "implementing"
  },
  "stop_boundary": "phase-only",
  "execution_policy": {
    "implementation": {
      "runtime": "agent",
      "model": "composer-2.5-fast",
      "effort": "encoded-in-model"
    },
    "review": {
      "runtime": "codex",
      "model": "gpt-5.5",
      "effort": "xhigh"
    }
  },
  "slices": {},
  "workers": {},
  "waves": [],
  "resource_leases": {},
  "reviews": [],
  "thermo_reviews": [],
  "accepted_findings": [],
  "rejected_findings": [],
  "phase_completion": {
    "plan_coverage": "unknown",
    "proof": "unknown",
    "arbiter": "unknown",
    "thermo": "unknown"
  }
}
```

The state file should not contain secrets. It may contain paths, commands, and
model choices.

## 23. Scheduling Policy

The scheduler should optimize for wall-clock velocity under real constraints.

Inputs:

- dependency graph
- collision groups
- worker session health
- changed-file overlap
- resource leases
- number of safe parallel workers
- user-pinned max parallelism when present

Default max parallelism:

- `agent` / Cursor Agent implementation: 4 workers
- Codex implementation: ask or use 2-3 depending on model/cost if the user did
  not specify
- Claude implementation: ask or use 2-3 depending on model/cost if the user did
  not specify

These are not hard skill defaults until implemented. They are planning
recommendations. A skill that spends real budget should ask when the user's
execution preference is not clear.

Wave rules:

- launch all dependency-free slices that do not share a collision group
- if two slices share a collision group but are naturally one concept, assign
  them to the same worker instead of two workers
- run replacement path before deletion path
- keep full verification until after implementation wave results are merged
- if a wave produces conflicts or unclear owner drift, pause new launches and
  resolve the conflict before adding more workers

## 24. Merge And Conflict Handling

Because the current path is shared-worktree execution, the parent must inspect
repo state after every wave.

After each wave:

1. Read every child footer.
2. Read every worker worklog.
3. Run `git status --short`.
4. Inspect changed-file overlap.
5. Identify unresolved merge/conflict markers if any.
6. Update the execution ledger.
7. Decide next wave, repair, or review.

The parent must not revert unknown changes. If a worker appears to have changed
unrelated files, inspect before deciding. If it is truly unrelated and unsafe,
route a repair prompt or ask the user before destructive cleanup.

## 25. Verification Strategy

Verification is a phase resource, not a worker free-for-all.

Proof should be layered:

- slice-local checks by implementation workers
- parent-side status/diff inspection after waves
- designated verification worker for expensive tests
- arbiter review for phase-contract coverage
- thermonuclear review for maintainability
- final-plan review only at the end of the whole plan

Suggested verification worker prompt:

```markdown
You are the plan-swarm verification worker. You hold the scarce verification
lease for this phase. Do not make implementation edits unless the check cannot
run without a tiny obvious harness fix; report that instead if it is not
obvious.

Read the phase contract, execution ledger, worker worklogs, and current diff.
Run the focused checks requested by workers and the phase contract. Prefer the
smallest check set that proves the phase behavior. Record exact commands,
results, failures, and remaining proof gaps.

End with:

STATUS: pass | fail | blocked | inconclusive
COMMANDS RUN: <commands/results>
FAILURES: <evidence or "none">
PROOF COVERAGE: <phase requirements covered>
REMAINING GAPS: <gaps or "none">
SUMMARY FOR PARENT: <one paragraph>
```

## 26. Phase Completion Rule

A phase is complete only when all are true:

- the active phase contract is covered by implementation evidence
- required cleanup/deletion checkpoints are done or explicitly walled off by
  the plan's own rules
- owner-boundary checks are present when the plan requires them
- save/persistence/QA behavior is proven when the phase requires it
- worker worklogs are up to date
- arbiter verdict is `pass`, or any non-pass findings are explicitly triaged
  with evidence
- thermonuclear findings are accepted/repaired or rejected/deferred with
  recorded rationale
- current repo state has no unresolved conflicts from the swarm
- verification is proportional to the changed surface
- no worker is still holding a blocking resource request

The final response should never say "done" only because all workers returned
`STATUS: done`.

## 27. Final Plan Completion Rule

When the requested boundary is the whole plan, or when the active phase is the
last phase and the user asked for full-plan signoff, add a final-review lane.

Recommended final-review sequence:

1. Run a broad fresh-consult or code-review against the whole plan completion
   claim.
2. Ask the reviewer to compare the plan, all worklogs, changed files, and
   proof evidence.
3. Route accepted findings into new repair slices.
4. Run final verification after repairs.
5. Write a final plan summary next to the plan.

Do not run this heavy lane after every phase by default. The user explicitly
wants speed during execution and heavier review near the end.

## 28. Failure Handling

Fail loud when:

- the plan path does not exist
- the active phase cannot be identified and the user did not name one
- execution runtime/model cannot be resolved
- Cursor Agent was requested before `agent-delegate` supports `runtime=agent`
- the phase contract has a user-level ambiguity that repo evidence cannot
  answer
- a child CLI is missing
- a child run exits non-zero without usable output
- a session id is missing for a planned resume
- repeated worker repair is not making progress
- the arbiter and parent cannot reconcile whether a finding is in scope
- verification requires a resource the orchestrator cannot access

Do not fail just because:

- the phase text is high level and code evidence can recover the contract
- a worker found adjacent edits needed for correctness
- workers overlap in expected files before a real conflict exists
- a test fails and points to an in-scope repair
- the arbiter found a valid gap that can be routed

## 29. User-Facing Progress Updates

The skill should keep the user informed without flooding them.

Good updates:

- "I extracted Phase 14 into five slices. Three can run now; two wait on the
  command-service slice."
- "Wave 1 finished. The QA adapter worker is clean, the overlay worker needs a
  persistence follow-up, and no scarce-resource checks ran yet."
- "The arbiter found one in-scope boundary leak. I am resuming the command
  service worker for that repair."
- "Thermonuclear review found two real maintainability issues and one unrelated
  old debt item. I accepted the two and deferred the old debt."

Bad updates:

- raw stream dumps
- every child tool call
- vague "working on it" with no state
- declaring the phase done before review/proof gates

## 30. Package Shape

Recommended future package:

```text
skills/plan-swarm/
  SKILL.md
  agents/
    openai.yaml
  references/
    workflow-contract.md
    phase-contract.md
    decomposition-and-scheduling.md
    worker-prompt-contract.md
    arbiter-and-review.md
    resource-leases.md
    session-reuse.md
    run-state-and-artifacts.md
    examples.md
  scripts/
    run_plan_swarm.py
    test_run_plan_swarm.py
```

`SKILL.md` should stay lean. It should own trigger, scope, first move,
non-negotiables, and reference map. The detailed prompt skeletons and state
contracts belong in `references/`.

The script exists because this skill's whole job is orchestration. Keep the
script's default output compact:

```text
RUN_DIR: ...
STATUS: wave-launched | wave-complete | review-needed | blocked | complete
NEXT: ...
```

Full details live in artifacts, not stdout.

## 31. Proposed `SKILL.md` Contract

Draft trigger description:

```yaml
description: "Orchestrate fast implementation of a named phase or phase range from an existing plan document by decomposing the approved phase into independent slices, launching resumable delegated workers in parallel through Codex, Claude, or Cursor Agent, coordinating scarce test resources, writing worklogs next to the plan, and gating completion through delegated arbiter review plus thermonuclear maintainability triage. Use when the user wants plan-doc-backed implementation accelerated with parallel agents. Do NOT use for creating the plan (`arch-step`), multi-plan epic decomposition (`arch-epic`), strict ordered process execution (`stepwise`), one-shot delegation (`agent-delegate`), or read-only review (`fresh-consult`/`code-review`)."
```

This is long but likely under the common 1024-character cap. Validate during
implementation.

Core non-negotiables for `SKILL.md`:

- One active plan phase or explicit phase range at a time.
- Plan doc remains source of truth.
- Decomposition is execution schedule, not new plan scope.
- Implementation workers are delegated and resumable.
- Cursor Agent implementation defaults to `composer-2.5-fast` when user asks
  for Cursor Agent.
- Parent coordinates scarce verification resources.
- Workers are prompted with goals and evidence, not micromanaged recipes.
- Parent updates worklogs next to the plan.
- Arbiter review uses `agent-delegate` and does not edit files.
- Thermonuclear review is required before phase closure unless the user
  explicitly disables it.
- Accepted review findings route to workers, usually by resuming related
  sessions.
- Phase closure requires evidence, not worker self-certification.

## 32. Implementation Plan

### Phase 1: Add Cursor Agent To Existing Child Skills

Files:

- `skills/fresh-consult/SKILL.md`
- `skills/fresh-consult/references/model-and-invocation.md`
- `skills/agent-delegate/SKILL.md`
- `skills/agent-delegate/references/model-and-invocation.md`
- `skills/model-consensus/SKILL.md`
- `skills/model-consensus/references/model-and-invocation.md`
- `README.md`

Work:

- Add `agent` / Cursor Agent as supported runtime.
- Add runtime inference for `agent`, `cursor`, `cursor agent`, and
  `cursor-agent`.
- Document Cursor Agent command shapes.
- Document `composer-2.5-fast` default only when the user chooses Cursor Agent
  and the caller's policy allows that default.
- Document JSON parsing of terminal `result`.
- Document explicit resume via `--resume <session_id>`.
- Document no `--continue`, no `agent resume`, no latest session.
- Document no `--worktree` unless explicitly requested.

Verification:

- `npx skills check`
- re-read edited skill files
- run local non-edit smoke only if safe:
  `agent -p --mode ask --output-format json --trust --sandbox disabled --model composer-2.5-fast "Reply OK"`

### Phase 2: Shared Child Runtime Adapter

Files:

- `skills/_shared/child_agent_runtime.py`
- tests near existing script tests

Work:

- Implement command builders for Codex, Claude, and Cursor Agent.
- Implement final-text/session-id parsers.
- Implement fake-run or dry-run mode for tests.
- Keep no secrets in artifacts.
- Use exact command shapes already documented.

Verification:

- unit tests for argv construction
- unit tests for JSON/NDJSON parsing
- fixture tests for missing terminal result
- fixture tests for `UNRECOVERABLE` session behavior

### Phase 3: Create `plan-swarm` Skill Package

Files:

- `skills/plan-swarm/SKILL.md`
- `skills/plan-swarm/references/*`
- `skills/plan-swarm/agents/openai.yaml`
- `README.md`
- `Makefile`
- `.gitignore`

Work:

- Add package with lean entrypoint and references.
- Add to install lists for Codex, Claude, and Gemini if the runtime surface can
  execute the skill. The subprocess CLIs still need to exist locally.
- Add `.arch_skill/plan-swarm/` ignore rule.
- Add README inventory and usage guide entries.

Verification:

- `npx skills check`
- `make verify_install` if install behavior changes

### Phase 4: Implement Runner

Files:

- `skills/plan-swarm/scripts/run_plan_swarm.py`
- `skills/plan-swarm/scripts/test_run_plan_swarm.py`

Work:

- create run state
- write phase contract
- write execution graph
- launch waves
- resume workers
- launch review delegates
- track leases
- parse reports
- render status

Do not make the runner interpret the plan alone. The parent skill should author
the phase contract and execution graph from source evidence. The runner should
validate and persist them.

Verification:

- unit tests for state transitions
- unit tests for wave scheduling
- unit tests for resource leases
- unit tests for session reuse policy
- fake child CLI integration tests
- artifact layout tests

### Phase 5: Fixture Repo Smoke

Create a tiny fixture repo in tests, not a real worktree:

- a plan with two independent slices and one dependent cleanup slice
- fake child CLIs that emit realistic Codex/Claude/Agent events
- expected worklog and state transitions

Verify:

- two independent workers launch in the same wave
- cleanup waits
- review finding resumes the related worker
- bad session health spawns fresh
- terminal result parsing works for Cursor Agent
- resource lease prevents two full-suite workers

### Phase 6: Real Throwaway Repo Trial

Use a throwaway repo or disposable branch only after fake tests pass.

Trial target:

- small plan phase
- Cursor Agent implementation runtime
- `composer-2.5-fast`
- two parallel workers
- one review arbiter
- one thermonuclear review

Success evidence:

- files changed as expected
- worklogs written next to plan
- session ids captured
- related repair resumes same session
- review findings route correctly
- final phase report is accurate

## 33. Validation Matrix

| Surface | Checks |
| --- | --- |
| Cursor Agent integration | local smoke, command shape docs, final result parsing |
| Skill package validity | `npx skills check` |
| Install surface | `make verify_install` when Makefile/README install lists change |
| Runner command builders | unit tests with fake CLIs |
| Session capture/resume | fixture events for Codex, Claude, Agent |
| Scheduler | dependency, collision, lease, max parallel tests |
| Worklog output | golden Markdown fixture |
| Review triage | accepted/deferred/rejected fixture findings |
| Phase completion | cannot pass without plan coverage, proof, arbiter, thermo triage |
| Dirty worktree safety | fixture status with unrelated changes |

## 34. Open Decisions

1. **Name.** `plan-swarm` is the working name. `implementation-orchestrator`
   is clearer but long.
2. **Default review runtime.** The skill should probably ask unless the user
   pins one. Cursor Agent implementation does not imply Cursor Agent review.
3. **Final whole-plan review.** Decide whether final signoff should default to
   `fresh-consult`, `code-review`, or a user-selected review lane.
4. **Runner reuse.** Decide whether to share the child runtime adapter with
   `stepwise` and `arch-epic` immediately or only after `plan-swarm` proves
   the adapter.
5. **Parallelism default.** Cursor Agent likely wants `4` by default for speed,
   but budget and shared-worktree risk may argue for asking on first run.
6. **Plan doc mutation.** The safest default is sidecar worklogs next to the
   plan, not modifying the plan body except maybe a single pointer entry if a
   plan already has a worklog section.
7. **Gemini installation.** The skill can be prompt-visible in Gemini, but it
   still shells out to local child CLIs. Confirm whether that is acceptable for
   this repo's install policy before adding it to `GEMINI_SKILLS`.

## 35. Explicit Non-Goals For V1

- no automatic git commits
- no pushes or PRs
- no worktree creation by default
- no long-lived detached workers that continue after the parent reports done
- no hidden fallbacks between runtimes
- no "latest session" resume
- no plan rewriting beyond append-only logs or explicitly allowed status
  updates
- no broad final-pack signoff when the user asked for one phase
- no replacing `arch-epic`, `stepwise`, `agent-delegate`, or `code-review`
- no schema-enforced child model output until the runtime adapters support it
  reliably for all three child runtimes

## 36. Definition Of Done For This Future Skill

The skill is ready when:

- Cursor Agent is supported in `fresh-consult`, `agent-delegate`, and
  `model-consensus`.
- `plan-swarm` can run a named phase from an existing plan doc.
- It writes a phase contract and execution graph without creating a second
  plan.
- It launches independent implementation slices in parallel.
- It captures and resumes worker sessions for Codex, Claude, and Cursor Agent.
- Cursor Agent workers use `composer-2.5-fast` by default when selected.
- It writes human worklogs next to the plan and heavy artifacts under
  `.arch_skill/plan-swarm/`.
- It coordinates scarce verification resources.
- It uses delegated arbiter review before phase closure.
- It runs thermonuclear maintainability review before phase closure.
- It routes accepted findings back to workers, preferring session resume when
  healthy.
- It rejects arbitrary scope expansion from reviewers.
- It stops at the requested phase boundary.
- It passes `npx skills check`.
- Install docs and `Makefile` are consistent if the package is added to the
  installed surface.

## 37. First Build Sequence

Recommended next implementation order:

1. Patch `agent-delegate` for `runtime=agent` first, because `plan-swarm`
   depends on editful workers and explicit resume.
2. Patch `fresh-consult` and `model-consensus` for `runtime=agent` using the
   same command doctrine.
3. Add shared child runtime adapter with fake CLI tests.
4. Create `plan-swarm` package with references but no full runner yet.
5. Implement runner state, scheduling, and fake child launches.
6. Add real child launch support.
7. Add arbiter and thermonuclear gates.
8. Add docs-side worklog rendering.
9. Run fixture repo smoke.
10. Update README, Makefile, and install verification.

This order keeps the fastest user-visible dependency first: once
`agent-delegate` supports Cursor Agent, manual parallel Cursor Agent delegation
becomes possible even before the full orchestrator ships.
