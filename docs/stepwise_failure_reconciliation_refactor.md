# Stepwise Failure Reconciliation Refactor Recommendations

Date: 2026-04-24
Scope: `skills/stepwise/`
Audience: maintainers deciding how to make `$stepwise` less brittle after critic failures.

## Executive Summary

The current `$stepwise` failure path is too brittle because it treats the
critic's `resume_hint` as the repair prompt. That makes the critic responsible
for diagnosing the breach, choosing the recovery strategy, and wording the
worker's next command. In the failed copy-gate run, the critic correctly found
the breach but produced a harmful recovery constraint: preserve the already
landed copy edit. Because the breach was timeline-sensitive, preserving the
edit pushed the worker toward retroactive proof instead of true recovery.

The recommended refactor is to split failure handling into three distinct
jobs:

1. The critic reports only the observed breach and evidence.
2. The stepwise orchestrator reconciles the failure by talking directly to the
   struggling step session, then walking upstream through prior sessions and
   artifacts when the child's input may be wrong.
3. Only after root cause is understood does the orchestrator send an
   operational repair prompt to the child session that owns the earliest broken
   link.

This should happen for every critic failure. The loop can be bounded, but it
should not be gated by brittle heuristics about whether a failure is "simple"
or "worth diagnosis." A missing file can reconcile in one round. A
process/provenance failure may need several rounds. The universal invariant is:
no raw critic `resume_hint` goes straight to worker repair.

The same loop handles local worker confusion and bad upstream inputs. There is
not a special upstream mode. Stepwise follows evidence to the first broken
link, repairs there, then continues downstream with context hygiene.

Add a persistent learning protocol alongside this. Stepwise should record
failure learnings and process recommendations in a shared, append-only ledger
outside individual run directories. Future runs should consult the ledger
through an applicability test, not blindly import every prior lesson.

## North Stars

The refactor should make `$stepwise` a thoughtful diagnoser and orchestrator,
not a naive runner with a critic bolted onto it. The goal is not more rigid
retry machinery. The goal is a skill that understands the confirmed plan,
understands the owner skills, watches how subprocess agents are interpreting
their task, diagnoses confusion when they drift, and repairs the
communication loop before asking for more target-repo work.

### 1. Stepwise reasons before it routes

Stepwise should never act like a pipe from critic output to worker input. On
each failure, it should reason about:

- what the manifest actually asked for
- which owner skill or runbook governed the step
- what evidence the transcript contains
- what evidence is missing
- what the worker appears to have misunderstood
- whether the obvious-looking recovery would add a new constraint or preserve
  a bad state
- whether the current child received a bad upstream input
- where the earliest broken link is: current worker, upstream step,
  intermediate transformation, manifest, or user intent

The critic verdict is input to this reasoning. It is not the reasoning.

### 2. Teach judgment, not shortcuts

The Stepwise doctrine should be written like a strong prompt, following the
same spirit as `$prompt-authoring`: teach the mission, success/failure
recognition, evidence standards, and recovery reasoning. Do not replace that
with keyword triggers, brittle failure categories, or canned action menus.

Bad shape:

```text
If the failure mentions process evidence, ask diagnostics. If it mentions
artifact missing, send repair.
```

Better shape:

```text
Every failure needs reconciliation. Simple failures converge quickly because
the evidence and repair are obvious. Complex failures expose mistaken models,
bad constraints, or upstream scope issues. Stepwise must inspect the evidence
and decide which conversation is needed before repair.
```

### 3. Diagnose agent confusion as a first-class artifact

The worker is another agent with a model of the task. When it fails, Stepwise
should diagnose that model instead of assuming the worker merely needs a
longer checklist. The diagnostic exchange should answer:

- what did the worker think counted as completion?
- what rule did it invent, skip, or misread?
- what constraint did it think it was under?
- what would make the next repair overconstrained?
- what exact evidence would prove the repair was honest?

That diagnosis should be written to the run directory so the user can inspect
what Stepwise learned, not just whether the final artifact passed.

### 4. Trace upstream to root cause

Stepwise must assume that the struggling child might be downstream of the real
problem. The child may be confused, or it may be reacting correctly to a bad
input. When evidence points upstream, Stepwise should talk to the prior
owning child session and any intermediate sessions needed to locate the first
broken link.

The goal is not to make the current child patch around bad input. The goal is
to repair the earliest owning artifact, then continue downstream from a clean
chain of evidence.

### 5. Keep role boundaries while increasing agency

Stepwise should become more thoughtful without becoming the worker. The
orchestrator may inspect run artifacts, read the owner contract, interrogate
the worker, author prompts, maintain learning ledgers, and route failures. It
still must not edit target-repo work products or certify work without a critic.

The richer behavior belongs in orchestration judgment, not in target-work
shortcuts.

### 6. Persist learning without creating hidden law

Learning should make Stepwise better over time, but not by turning every prior
incident into automatic doctrine. A learning must carry evidence,
applicability, and contraindications. Stepwise should consult learnings as part
of reasoning and state why a learning applies before using it.

The durable loop is:

```text
failure -> reconciliation -> repair -> critic recheck -> learning candidate
-> future applicability check -> possible promotion into doctrine
```

### 7. Simplify the control surface

The best version of this refactor removes complexity instead of adding
ceremony. Do not add failure modes, retry modes, critic repair hints, route
fields, or keyword taxonomies. The control surface should be:

```text
one critic breach report
one Stepwise root-cause reconciliation loop
one owner repair prompt
one critic recheck
one learning extraction step
```

The intelligence belongs in the Stepwise prompt contract: why it is
diagnosing, what evidence matters, how to talk to children, how to trace
upstream, and how to avoid context poisoning. The plumbing should stay small.

## Current Failure Mode

The live contract currently says:

- `skills/stepwise/SKILL.md`: on critic fail, resume the same step session with
  only the critic's `resume_hint`.
- `skills/stepwise/references/step-prompt-contract.md`: the retry prompt wraps
  the critic's `resume_hint` as binding required fixes.
- `skills/stepwise/references/critic-contract.md`: `resume_hint.required_fixes`
  are "not suggestions"; the orchestrator renders them verbatim.
- `skills/stepwise/references/critic-contract.md`: `route_to_step_n` lets the
  critic nominate the upstream repair target, which still makes the critic
  part of the repair cycle instead of keeping it focused on evidence.
- `skills/stepwise/references/workflow-contract.md`: Phase 4c is mostly
  mechanical after the verdict; the critic's verdict is the authority.

That shape is good for a narrow class of mechanical misses, but it collapses
under failures where the worker's mental model is wrong. The critic can see
that a worker skipped a gate, fabricated proof, or misunderstood a support
skill. The critic is not the right component to hold a conversation with the
worker and debug that misunderstanding.

The bad pattern is:

```text
critic detects breach
-> critic writes required_fixes
-> stepwise forwards required_fixes verbatim
-> worker tries to satisfy checklist shape
-> worker may still misunderstand the underlying contract
```

The resilient pattern is:

```text
critic detects breach
-> stepwise reads verdict, transcript, artifact, and owner contract
-> stepwise resumes worker in diagnostic-only mode
-> worker explains its mistaken model and repair understanding
-> stepwise asks whether the worker's inputs were already wrong
-> stepwise traces upstream through prior sessions and artifacts when needed
-> stepwise writes a root-cause record
-> stepwise repairs through the owner of the earliest broken link
-> stepwise continues downstream with context hygiene
-> critic judges the repaired chain
```

## Design Principles

### 0. The orchestrator owns the diagnosis

Stepwise should treat diagnosis as its own work product. It is not enough to
know that a step failed. Stepwise needs to explain why the worker failed in
terms of the plan, the owner skill, the attempted evidence, and the worker's
stated or implied misunderstanding.

The diagnosis should be specific enough that a human can tell whether Stepwise
understood the problem before it asked the worker to touch the target repo
again. If the diagnosis is only "critic failed the step," Stepwise is still
acting like a brittle runner.

### 1. The critic observes; stepwise reconciles

The critic should remain the pass/fail authority for a completed attempt. It
should not be the repair-prompt author of record.

The critic should return:

- observed breach
- evidence
- contract clause or owner surface implicated
- affected artifacts or inputs, when visible from evidence
- uncertainty that prevents a responsible judgment

The orchestrator should own:

- transcript-aware diagnosis
- worker interrogation
- upstream root-cause tracing
- overconstraint challenge
- final repair prompt
- persistent learning extraction

### 2. Worker self-explanation is evidence, not truth

The diagnostic loop works because the worker can expose its mistaken model.
That explanation must not be blindly trusted. Stepwise should compare the
worker's answer against:

- the transcript
- the final message
- artifact state
- owner runbook
- declared support skill evidence
- critic evidence
- user instruction and manifest boundaries

If the worker says "I thought X was allowed," stepwise asks:

- which instruction made you think that?
- does the transcript prove that instruction was followed?
- what would be overconstraint here?
- what exact evidence is required, and what evidence are you inventing?

### 3. Every failure gets reconciliation

Do not decide in advance that only process failures deserve diagnosis. That
classification is itself a heuristic and can miss the real issue. Instead,
run the same reconciliation protocol for every fail and let simple cases exit
quickly.

For a missing file, the worker can answer in one round:

```text
I claimed the file existed, but transcript and disk evidence show I never wrote
it. The repair is to write the declared file and rerun the selector. No extra
constraints are needed.
```

For process/provenance failures, the same protocol naturally takes longer.

### 4. No shortcut heuristics

Do not replace raw `resume_hint` pass-through with a new decision table like
"artifact failures get direct repair, process failures get diagnostics." That
is still a brittle runner, just with more branches.

The universal process is evidence-first reconciliation. The depth of the
conversation emerges from the evidence:

- if the worker simply did not write a declared file, the reconciliation is
  short because the contradiction is obvious
- if the worker skipped support, fabricated provenance, or followed a perceived
  constraint, reconciliation goes deeper because the mental model matters
- if the critic's own evidence looks confused or incomplete, Stepwise
  reconciles that before disturbing the worker

The prompt should teach that reasoning, not encode a finite routing menu.

### 5. Constraints must name their source

The current retry prompt can accidentally add constraints that the user did
not ask for and the owner runbook did not require. A refactored repair prompt
should separate constraints by authority:

- user or manifest hard boundary
- owner runbook hard boundary
- artifact preservation preference
- critic evidence or diagnostic concern
- worker-proposed recovery detail, treated as evidence rather than authority

Any "do not redo" or "preserve X" constraint must state why it is safe. If the
failure is timeline-sensitive, preservation may be the wrong repair.

### 6. Learning is not doctrine until promoted

Stepwise should persist learnings, but persisted learnings should not become
hard runtime doctrine by accident. A learning must carry an applicability test
and a contraindication. Future runs consult it only when the current step
matches the applicability test.

Repeated or user-confirmed learnings can later be promoted into
`skills/stepwise/references/*.md`. Until then, they are advisory process
memory.

## Proposed Runtime Model

Use one failure path for every critic fail:

```text
critic fail -> Stepwise investigates -> Stepwise talks to the struggling child
-> Stepwise traces root cause upstream if evidence points there -> Stepwise
repairs through the owning child session -> Stepwise reruns or resumes affected
downstream work with context hygiene -> critic rechecks -> learning candidate
```

There are no new operating modes. There is one intelligent diagnostic loop.
The loop can be short when the evidence is simple, but it is always the same
kind of work: understand the break in the chain from plan to evidence before
asking for more target-repo edits.

### Step 1: Ingest The Failure Without Repair Hints

Inputs:

- `steps/<n>/try-<k>/critic/verdict.json`
- step descriptor
- worker final message
- worker transcript
- expected artifact block
- owner doctrine path
- prior step descriptors and artifacts that fed this step

Output:

- `steps/<n>/try-<k>/reconciliation/failure-intake.md`

The critic's job ends at breach reporting. It should not tell Stepwise how to
repair, which worker to resume, what not to redo, or whether to route
upstream. Stepwise writes the first diagnosis note itself:

```markdown
# Failure Intake

Step: 6
Try: 1
Verdict: fail

Observed breach:
- The worker changed learner-visible copy before the declared copy gate.

Evidence:
- Transcript shows manifest write before baseline/grounding evidence.
- Proof note claims pre-write baseline loading.

Initial Stepwise diagnosis:
- The artifact may be clean, but the provenance chain is broken.
- The next question is whether this worker misunderstood the copy gate, was
  operating under a bad retry constraint, or received bad upstream input.

No repair prompt has been issued.
```

### Step 2: Interrogate The Struggling Child

Stepwise resumes the same worker session in diagnostic-only mode. No target
edits. No repair. Commands are read-only only when Stepwise explicitly asks
for exact transcript or artifact evidence.

The point is not to get an apology. The point is to expose the worker's model
of the step:

1. What did you believe the step was asking you to do?
2. What did you treat as your inputs?
3. Which input, artifact, or instruction might have been wrong before you
   touched anything?
4. What did you do wrong, independent of any prior repair wording?
5. Which part of the manifest, owner skill, support skill, upstream artifact,
   or prior prompt did you misread, overweight, underweight, or invent?
6. What evidence is actually required by the owner contract?
7. What would be overconstraint here?
8. Is Stepwise itself operating under a bad constraint from the critic,
   manifest, prior retry prompt, run machinery, or upstream artifact?
9. Where is the earliest point in the run where the chain seems to break?
10. What should make Stepwise stop instead of approving a repair?

The answer is evidence for Stepwise. It is not accepted as truth until
Stepwise checks it against the run directory, manifest, owner doctrine, and
artifact state.

### Step 3: Trace Root Cause Upstream When Inputs Look Wrong

Stepwise must be explicitly willing to say: the current child may not be the
root cause. A worker can fail because it misunderstood the task, but it can
also fail because the step's inputs were already wrong.

When the child, transcript, artifact state, or owner contract points upstream,
Stepwise traces the dependency chain instead of forcing the current child to
patch around bad input.

Root-cause tracing stays inside the same failure path:

1. Identify the exact upstream artifact, assumption, or step output the current
   child depended on.
2. Read the upstream step descriptor, transcript, final message, artifact, and
   critic verdict.
3. If intermediate steps transformed or relied on that artifact, inspect those
   step records too.
4. Resume the upstream child session in diagnostic-only mode and ask what it
   believed it produced, what inputs it used, and whether it now sees the
   mismatch.
5. Continue upstream only while the evidence points to an earlier broken link.
6. Stop at the earliest owning step whose session can repair the root cause, or
   stop for the user if the manifest or user intent itself is wrong.

This is root-cause analysis, not an upstream mode. Stepwise is following the
evidence back to the first broken link.

### Step 4: Write One Root-Cause Record

Before any repair prompt, Stepwise writes:

```text
steps/<n>/try-<k>/reconciliation/root-cause.md
```

Minimum shape:

```markdown
# Root Cause

Failed step:
- Step 6: L1 placeholder cleanup

Earliest broken link:
- Step 6 worker misunderstood copy-gate applicability.

Upstream checked:
- Step 5 copy lane: no evidence it supplied a bad L1 input.
- Step 4 materialization: no evidence it forced placeholder cleanup exemption.

Why repair belongs here:
- The bad action was Step 6's self-waiver. The manifest and owner runbook were
  sufficient; the worker skipped the pre-write gate.

What would be overconstraint:
- Requiring every support skill to emit a receipt id.
- Preserving an already-landed edit as if it proved pre-write compliance.

Continuation plan:
- Repair Step 6 under the owner contract, then re-run its critic.
```

For an upstream-rooted failure, the same file names the upstream owner:

```markdown
Earliest broken link:
- Step 3 playable manifest supplied the wrong walkthrough stage. Step 4 copy
  correctly detected that its input contradicted the pinned Brief.

Why repair belongs upstream:
- Step 4 cannot honestly write copy around a structurally wrong Step 3
  artifact. Step 3 owns the artifact and has the session context needed to
  repair it.

Continuation plan:
- Resume Step 3 for repair.
- Recheck Step 3.
- Re-run or resume affected downstream steps only after context hygiene review.
```

### Step 5: Repair Through The Owning Child

Only now does Stepwise send a repair prompt, and it sends it to the session
that owns the earliest broken link. The repair prompt is Stepwise-authored from
the root-cause record, owner doctrine, run evidence, and diagnostic
conversation. It is not derived from critic repair text.

Repair prompt shape:

```markdown
Your prior attempt failed this step. Stepwise has diagnosed the root cause.

Execute only the confirmed repair. Do not add constraints beyond the user
prompt, manifest, owner runbook, and root-cause record.

## Root Cause

{{root_cause_summary}}

## Why This Is Your Step To Repair

{{ownership_reason}}

## Hard Boundaries

{{hard_boundaries}}

## Repair Steps

{{ordered_repair_steps}}

## Evidence To Leave

{{required_evidence}}

## Stop Instead Of Approving If

{{stop_conditions}}

When the fixes are in place, end your turn.
```

### Step 6: Continue Downstream With Context Hygiene

After an upstream repair, Stepwise must decide how affected downstream work
continues by reasoning about context integrity, not by applying a fixed mode.

Principle:

```text
Do not ask a worker to do target work from a session whose working context is
materially built on false upstream facts.
```

That usually means fresh-spawning downstream steps after an upstream artifact
changes. The old downstream diagnostic conversation remains valuable: Stepwise
can summarize it into the new downstream prompt as run evidence. If the
downstream child had not yet acted on the bad input, Stepwise may resume it,
but only after writing why the session is not context-poisoned.

This preserves the user's intent to continue the run after upstream repair
without blindly reusing a contaminated child context.

### Step 7: Critic Recheck And Learning Extraction

The critic rechecks the repaired owner step. If upstream changed, affected
downstream steps are rechecked after fresh or justified continuation.

After any failed attempt and after any repaired pass, Stepwise writes learning
candidates. A learning candidate is not automatic doctrine. It is a structured
note with an applicability test.

Examples from the copy-gate incident:

- "Do not treat reused learner-visible copy as exempt from copy-gate
  ordering."
- "Preservation language can be harmful when the breach is timeline-sensitive."
- "Support skill evidence differs by support type: lenses need visible
  invocation and application; primitives may produce receipts; KB claims need
  ans-* or equivalent identifiers."

## Persistent Learning Protocol

### Storage

Use a shared ledger outside individual run directories:

```text
.arch_skill/stepwise/learnings/
|-- index.jsonl
|-- accepted.md
|-- candidates/
|   `-- LRN-<hash>.md
`-- rejected/
    `-- LRN-<hash>.md
```

This path is intentionally under `.arch_skill/stepwise/`, not inside a
particular run. Multiple parallel runs in the same project can see it. It is
also visible to the user on disk.

If human review wants a checked-in summary, add an explicit promotion command
or manual process that copies selected accepted learnings into a real doc such
as `docs/stepwise-learnings.md`. Do not auto-write version-controlled docs
during a run.

### Concurrency

Parallel stepwise runs should append through a small deterministic script with
file locking:

```text
skills/stepwise/scripts/stepwise_learnings.py append
skills/stepwise/scripts/stepwise_learnings.py query
skills/stepwise/scripts/stepwise_learnings.py accept
skills/stepwise/scripts/stepwise_learnings.py reject
skills/stepwise/scripts/stepwise_learnings.py export-md
```

This script is justified because natural-language ledger management is
repeatable and concurrency-sensitive. It should own:

- JSON schema validation
- id generation
- append locking
- duplicate detection by normalized fingerprint
- status transitions
- query filtering by applicability fields

### Learning Schema

Recommended JSONL shape:

```json
{
  "schema_version": 1,
  "id": "LRN-20260424-8f31c2a0",
  "created_at": "2026-04-24T03:10:00Z",
  "updated_at": "2026-04-24T03:10:00Z",
  "status": "candidate",
  "confidence": "observed_once",
  "source": {
    "run_id": "2026-04-24T02-37-55Z-1a48f620",
    "step_n": 6,
    "try_k": 2,
    "verdict_path": "steps/6/try-2/critic/verdict.json",
    "reconciliation_path": "steps/6/try-2/reconciliation/summary.md"
  },
  "scope": {
    "target_repo_fingerprint": "lessons_studio",
    "owner_skill": "$lesson-copy-discipline",
    "surface": "learner_visible_copy",
    "observed_signals": ["timeline_sensitive_ordering", "learner_visible_copy"],
    "support_skills": ["$poker-kb", "$catalog-ops", "$lessons-ops"]
  },
  "learning": "If learner-visible copy is inserted or moved into a manifest field, the copy gate applies even when the string already exists elsewhere.",
  "applicability_test": "Apply when a step edits learner-visible copy fields and argues that reuse, placeholder cleanup, or bounded cleanup exempts it from copy-gate ordering.",
  "contraindications": "Do not apply to deterministic structural validation steps that do not author or move learner-visible copy.",
  "recommended_process_change": "During reconciliation, ask whether the worker is treating reused copy as non-copy and require a pre-write or honest recovery timeline.",
  "promotion_target": "skills/stepwise/references/failure-reconciliation.md",
  "fingerprint": "sha256(normalized scope + learning)"
}
```

### Status Model

Use simple states:

- `candidate`: written automatically after a failure or repaired pass.
- `accepted`: user accepted it, or the same learning appeared independently in
  at least two runs and a later run confirmed usefulness.
- `rejected`: user or maintainer rejected it.
- `superseded`: replaced by a sharper learning.
- `promoted`: moved into live stepwise doctrine or a support skill.

The orchestrator may consult `candidate` and `accepted` learnings, but it must
label them differently:

```text
Applicable accepted learning:
- LRN-...: ...

Applicable candidate learning:
- LRN-...: ... (treat as caution, not doctrine)
```

### Applicability Read

At Phase 1 or before Phase 4 failure repair, Stepwise should query learnings
with current context:

- target repo path or fingerprint
- owner skill
- step label
- expected artifact kind
- active checks
- observed signals from the failure intake
- support skills named by owner runbook

The query returns only learnings whose `applicability_test` plausibly matches.
Stepwise must still state why it is applying each learning:

```markdown
## Applicable Learnings Considered

- LRN-20260424-8f31c2a0 applies because this failed step edits
  learner-visible copy and the worker treated placeholder cleanup as exempt.
- LRN-20260424-1d9a0e21 does not apply because this step has no KB grounding
  or learner-visible copy surface.
```

This keeps the ledger useful across parallel runs without turning it into a
global bag of stale advice.

## File-Level Refactor Plan

### `skills/stepwise/SKILL.md`

Change the mission and non-negotiables so the entrypoint teaches Stepwise's
new identity:

- Replace "resumes with the critic's findings" with "diagnoses critic failures
  against the plan, owner skills, worker transcript, artifact evidence, and
  upstream inputs; traces the earliest broken link; then sends a root-cause
  repair prompt to the owning child session."
- Delete or replace the rule "On critic FAIL, resume the same step's session
  with ONLY the critic's `resume_hint`."
- Add a non-negotiable: every critic fail gets diagnostic reconciliation
  before repair.
- Add a non-negotiable: critic output is evidence for Stepwise's diagnosis,
  not binding prompt text.
- Add a non-negotiable: no shortcut failure taxonomy may bypass
  reconciliation; simple failures reconcile quickly, but still reconcile.
- Add a non-negotiable: persistent learnings are consulted through
  applicability tests and never blindly applied.

Proposed replacement language:

```markdown
- On critic FAIL, Stepwise must diagnose before it repairs. Read the verdict,
  transcript, artifact evidence, manifest, owner contract, and upstream inputs;
  identify what the struggling child appears to have misunderstood or whether
  it received bad input; interrogate child sessions in diagnostic-only mode as
  needed; write a root-cause record; then send a Stepwise-authored repair
  prompt to the owning child session. The critic's verdict remains
  authoritative for pass/fail. The critic does not write worker instructions or
  choose the repair route.
- Every failure gets reconciliation. Do not use shortcut categories to skip
  diagnosis. A trivial artifact miss should produce a short reconciliation; a
  process, provenance, support-skill, or repeated failure should naturally
  produce a deeper conversation.
- Persist process learnings from failures and repaired passes into the
  stepwise learning ledger. Consult applicable learnings before repair, but
  apply them only when the current step matches their applicability test.
```

### `skills/stepwise/references/workflow-contract.md`

Replace the current fail/resume path with one unified failure reconciliation
loop:

- ingest critic breach evidence without repair hints
- interrogate the struggling child in diagnostic-only mode
- trace upstream through prior sessions and artifacts when inputs may be wrong
- write a root-cause record naming the earliest broken link
- repair through the owning child session
- continue affected downstream work with context hygiene
- re-run critics and extract learnings

Update "Where judgment lives" from mostly mechanical arithmetic to:

```markdown
The critic owns pass/fail. The orchestrator owns failure reconciliation and
root-cause tracing. The worker owns target-repo changes. The learning ledger
stores process memory, not automatic doctrine. The critic does not own repair
route, retry wording, or upstream selection.
```

### `skills/stepwise/references/step-prompt-contract.md`

Replace the single resume prompt contract with three prompt contracts:

1. Initial prompt.
2. Diagnostic reconciliation prompt.
3. Root-cause repair prompt.

The diagnostic prompt is no-edit by default. The repair prompt is operational
and bounded, but it is authored after reconciliation rather than copied from
the critic.

Add a hard rule:

```markdown
Do not ask any child session to repair before Stepwise has written a
root-cause record. The root-cause record must say whether the break belongs to
the current child, an upstream child, an intermediate step, the manifest, or
the user request.
```

### `skills/stepwise/references/critic-contract.md`

Change the critic role from repair author to breach reporter and remove
`resume_hint` from new-run schemas entirely. Do not rename it to
`candidate_repair`, and do not keep a similarly shaped field. The old field
name and shape encode the bad path: critic writes worker instructions,
Stepwise forwards them, and the worker tries to satisfy checklist text instead
of reconciling the failure.

New StepVerdict shape should use `failure_report` and should remove
`route_to_step_n` from new runs. The critic can report affected inputs when it
can see them, but it must not choose the upstream repair target.

```json
{
  "failure_report": {
    "headline": "string",
    "observed_breach": "string",
    "evidence": ["string"],
    "implicated_contract": ["string"],
    "affected_inputs_or_artifacts": ["string"],
    "evidence_flags": ["timeline_sensitive_ordering"],
    "uncertainty": ["string"],
    "legacy_resume_hint_seen": false
  }
}
```

The critic can still help the orchestrator by reporting precise evidence, but
it should not return ordered fixes, `do_not_redo`, `route_to_step_n`,
diagnostic scripts, overconstraint advice, or any prompt-ready worker
instruction list.

Old run directories may contain `resume_hint`. If backward compatibility is
needed, adapt it only into a legacy field that is visible to Stepwise as old
input and mark `legacy_resume_hint_seen: true`. Never render old
`resume_hint` text directly to a worker.

### `skills/stepwise/references/critic-prompt.md`

Update the fail section:

Current:

```text
If verdict=fail, fill resume_hint carefully ... required_fixes are actions
the step must execute, in order.
```

Recommended:

```text
If verdict=fail, report the observed breach and evidence in failure_report.
Do not write ordered repair steps, do_not_redo lists, or worker-facing retry
instructions. Do not select an upstream route. You may name affected inputs or
artifacts when the evidence shows them. You may mark evidence flags such as
timeline-sensitive ordering, missing artifact, unsupported claim, or visibly
affected input. Do not tell Stepwise how to repair the failure.
```

The critic should be explicitly told to identify timeline-sensitive breaches:

```text
If the breach is about ordering, provenance, or proof timing, mark it as
timeline-sensitive evidence. Do not recommend retroactive proof as clean
compliance, and do not advise whether to retain or redo the already-landed
artifact.
```

### `skills/stepwise/references/run-directory-layout.md`

Add reconciliation and learning artifacts:

```text
steps/<n>/try-<k>/
|-- prompt.md
|-- stdout.final.json
|-- stream.log
|-- session_id.txt
|-- critic/
|   `-- verdict.json
`-- reconciliation/
    |-- failure-intake.md
    |-- applicable-learnings.md
    |-- current-child-diagnostic.prompt.md
    |-- current-child-diagnostic.response.json
    |-- upstream-trace.md
    |-- upstream-step-<m>-diagnostic.prompt.md
    |-- upstream-step-<m>-diagnostic.response.json
    |-- root-cause.md
    |-- round-1.prompt.md
    |-- round-1.response.json
    |-- round-1.summary.md
    `-- root-cause-repair.prompt.md
```

Also add the shared ledger:

```text
.arch_skill/stepwise/learnings/
|-- index.jsonl
|-- accepted.md
|-- candidates/
`-- rejected/
```

### `skills/stepwise/scripts/run_stepwise.py`

Keep this script deterministic. It should not decide what a failure means.
But it can grow safe plumbing:

- Save every step prompt explicitly as `prompt.md`, not only inside
  `invocation.sh`.
- Add a generic `step-message` or reuse `step-resume` for diagnostic prompts,
  but make the output directory distinguish diagnostic prompts, upstream
  trace prompts, and repair prompts.
- Add learning ledger script or subcommands with file locking.
- Add schema validation for learning entries.
- Add run-directory helpers that create `reconciliation/` paths.

Avoid putting judgment into Python. The script should write, lock, validate,
query, and spawn. The orchestrator still reasons.

### `skills/stepwise/references/examples.md`

Replace Example 4 with one unified failure example that demonstrates:

1. Critic reports breach evidence only.
2. Orchestrator writes failure intake.
3. Orchestrator resumes current worker diagnostic-only.
4. Worker identifies either its mistaken model or a suspect upstream input.
5. Orchestrator traces upstream when evidence points there.
6. Orchestrator writes a root-cause record.
7. Orchestrator repairs through the owning child session.
8. Orchestrator continues affected downstream work with context hygiene.
9. Critic rechecks the repaired chain.
10. Learning candidate is written.

Keep the old raw-resume example only as an anti-pattern, not a model.

## Prompt-Authoring Changes

Using the `prompt-authoring` frame, this is not just a retry-loop patch. It is
a prompt refactor for Stepwise's own operating mind. The current doctrine
teaches Stepwise to be a careful runner: draft manifest, spawn step, spawn
critic, forward retry text. The new doctrine should teach Stepwise to be a
diagnosing orchestrator: understand the plan, understand the owner skills,
inspect evidence, identify the agent's mistaken model, challenge
overconstraint, and only then issue repair instructions.

That means the Stepwise prompt surfaces need richer high-level sections:

- **Identity and mission:** Stepwise is an orchestrator that diagnoses and
  routes multi-agent work, not a subprocess runner.
- **Success/failure:** success is not only "all steps passed"; success is a
  run where failures were understood, repaired through the right role, and
  recorded with useful learning. Failure includes pass-through retry prompts,
  uninspected critic constraints, and worker confessions accepted without
  evidence.
- **System context:** Stepwise coordinates fallible agents working against
  fragile repo doctrine. A weak orchestration prompt can create false proof,
  preserve bad state, or hide a misunderstood owner skill.
- **Operating principles:** evidence before repair, root cause before
  instruction, no shortcut heuristics, role boundaries, context hygiene, and
  learning with applicability tests.
- **Output contract:** every failure leaves a visible failure intake,
  diagnostic exchange, root-cause record, and repair contract, not just
  another try directory.

The current retry prompt has the wrong section ownership:

- Commander intent is sound: enforce process adherence without orchestrator
  doing the work.
- The process mechanics are wrong: the critic's checklist is doing diagnostic
  and repair-prompt work.
- The output contract is under-specified: there is no artifact proving the
  orchestrator understood the root cause before repair.
- Error handling is too narrow: it handles "worker failed" but not "critic
  proposed a bad fix" or "worker overcorrected after diagnosis."

### Prompt North Star

The prompt should teach this durable principle:

```text
Stepwise's job is to maintain a truthful chain from user intent to manifest,
from manifest to owner skill, from owner skill to worker action, from worker
action to evidence, and from evidence to critic judgment. When that chain
breaks, Stepwise traces the earliest broken link before asking for more work.
```

This is the prompt-level replacement for the old `resume_hint` reflex.

Add these prompt contracts.

### Diagnostic Prompt Template

```markdown
Diagnostic conversation only. Do not modify files. Do not attempt repair.
Do not run commands unless explicitly allowed for safe read evidence.

We are reconciling a critic failure before repair. The critic's verdict is
evidence, not a binding repair prompt.

Your job in this diagnostic turn is not to say the right apology. Your job is
to expose your model of the step so Stepwise can repair the communication
contract. Answer from your session history and the evidence provided. Do not
invent a stricter rule just to sound compliant.

## Evidence I Have

- Step: {{step_n}} / try {{try_k}}
- Critic breach: {{observed_breach}}
- Transcript evidence: {{short evidence bullets}}
- Artifact evidence: {{short evidence bullets}}
- Owner contract implicated: {{owner contract bullets}}
- Reconciliation risk: {{risk bullets}}

Answer plainly:

1. What did you believe the step was asking you to do?
2. What exactly did you do wrong, independent of any prior repair wording?
3. Which part of the manifest, owner skill, support skill, or prior prompt did
   you misread, overweight, underweight, or invent?
4. What evidence is actually required by the owner contract?
5. What would be overconstraint here?
6. Is Stepwise itself operating under any bad constraint from the critic,
   manifest, prior retry prompt, or run machinery?
7. Could any input you received already be wrong? If yes, name the exact
   upstream artifact, step, or assumption.
8. Where is the earliest broken link you can identify: current step, upstream
   step, intermediate transformation, manifest, or user request?
9. What should make Stepwise stop instead of approving a repair?

End with exactly one line:
CONFIRMATION: I understand the issue and the required fix is <one sentence>
```

### Overconstraint Challenge Template

```markdown
Continue diagnostic conversation only. Do not modify files.

Your prior answer may still be wrong or overconstrained. Reconcile:

1. Which constraints come from the user, manifest, or owner runbook?
2. Which constraints came only from critic verdict wording, prior prompt
   wording, or your own assumption?
3. Which evidence is required, useful-but-not-required, or invented?
4. What diagnosis would be too shallow here, and what diagnosis would be
   overcomplicated?
5. If the breach is timeline-sensitive, can the existing artifact be retained
   honestly? If yes, under what wording? If no, what must be redone?
6. State the least overconstrained repair that still leaves honest evidence.

End with exactly one line:
CONFIRMATION: corrected understanding = <one sentence>
```

### Root-Cause Repair Prompt Template

```markdown
Your prior attempt failed this step. Stepwise has traced the root cause.

Execute only the confirmed repair. Do not add constraints beyond the user
prompt, manifest, owner runbook, and root-cause record.

## Root Cause

{{root_cause_summary}}

## Why This Is Your Step To Repair

{{ownership_reason}}

## Hard Boundaries

{{hard_boundaries}}

## Repair Steps

{{ordered_repair_steps}}

## Evidence To Leave

{{required_evidence}}

## Stop Instead Of Approving If

{{stop_conditions}}

When the fixes are in place, end your turn.
```

## Skill-Authoring Changes

Using the `skill-authoring` frame, this remains one skill. Do not split
failure reconciliation into a separate user-invoked skill. It is part of
Stepwise's core leverage claim: orchestrating multi-step subprocess work with
critics and same-session repair.

The skill package should get clearer, not broader. The refactor should add one
owning reference for failure reconciliation and one learning reference. It
should delete the old critic-authored repair concept instead of layering a new
concept beside it.

The right packaging is:

- `SKILL.md`: high-level contract and non-negotiables.
- `references/failure-reconciliation.md`: one root-cause reconciliation loop,
  prompt contracts, upstream tracing, repair ownership, overconstraint
  handling, and downstream context hygiene.
- `references/learnings.md`: ledger path, schema, status model,
  applicability read, promotion flow.
- `references/critic-contract.md`: `failure_report` schema and any legacy
  adapter notes for old run directories.
- `references/examples.md`: one worked failure reconciliation example.
- `scripts/stepwise_learnings.py`: deterministic ledger operations if
  implemented.

Do not bloat `SKILL.md` with the entire diagnostic protocol. The entrypoint
should say that every fail gets one root-cause reconciliation loop and point
to the reference.

## Validation Plan

Run validations at three levels.

### Package Validation

After changing skill files:

```bash
npx skills check
```

Only run `make verify_install` when install behavior or installed surfaces
change.

### Unit Tests

Add tests for deterministic plumbing:

- learning id generation is stable
- JSONL append uses lock and preserves existing entries
- query returns applicable entries and rejects non-matching entries
- prompt files are saved under expected paths
- v3 verdict schema validates good and bad outputs
- old v2 `resume_hint` verdicts, if supported for old run directories, are
  exposed only as legacy input metadata and are never rendered as worker
  prompts

Current focused command:

```bash
python3 skills/stepwise/scripts/test_run_stepwise.py
```

Use `rg` before documenting any broader test command in live doctrine.

### Scenario Tests

Use representative runs, not answer-leaking evals:

1. Mechanical artifact miss: worker claims file was written but it is absent.
   Expected: one diagnostic round, direct repair, pass, learning either none or
   low-value candidate.
2. Timeline-sensitive process failure: worker edits before gate, then tries
   retroactive proof. Expected: diagnostic catches timeline issue, repair
   prompt avoids false pre-write claim.
3. Support-skill overcorrection: worker turns "load support" into "every
   support emits receipt id." Expected: challenge round corrects the invented
   rule.
4. Upstream root cause: current worker identifies a broken upstream artifact.
   Expected: reconciliation traces the earliest broken link, repairs through
   the upstream owner session, then continues downstream with context hygiene.
5. Parallel learning append: two runs write learning candidates. Expected:
   ledger remains valid and both entries are visible.

## Migration Plan

### Pass 1: Remove Critic Repair Poisoning

Patch:

- `skills/stepwise/SKILL.md`
- `references/workflow-contract.md`
- `references/step-prompt-contract.md`
- `references/critic-contract.md`
- `references/critic-prompt.md`
- `references/run-directory-layout.md`
- `references/examples.md`

Delete `resume_hint` and critic-owned routing from all new-run prompting and
doctrine. The critic prompt must not ask for repair steps, `do_not_redo`,
`route_to_step_n`, or anything prompt-ready for the worker. The replacement
concept is `failure_report`, which is for observed breach evidence and cannot
be rendered directly as a worker repair prompt.

### Pass 2: Teach Stepwise The New Orchestrator Mindset

Patch the high-leverage prompt sections before adding more mechanics:

- `SKILL.md` identity and mission should say Stepwise diagnoses and
  orchestrates fallible sub-agents against a confirmed plan.
- Success/failure should say a raw pass-through retry is a failure even if it
  sometimes works.
- Operating principles should teach evidence-first reconciliation, no shortcut
  heuristics, upstream root-cause tracing, role boundaries, context hygiene,
  overconstraint challenge, and learning with applicability tests.
- Workflow should show where diagnosis lives and where target work remains out
  of bounds.
- Examples should demonstrate judgment, not a canned failure taxonomy.

This pass is important because otherwise the refactor can accidentally become
another naive runner with a different schema.

### Pass 3: Critic Schema And Script Validation

Patch `step-verdict.schema.json` and `run_stepwise.py` together:

- remove `resume_hint` from the schema for new verdicts
- remove `route_to_step_n` from the schema for new verdicts
- remove `_validate_resume_hint`
- add `failure_report` validation
- if old-run compatibility is needed, provide an explicit legacy adapter that
  marks old `resume_hint` as legacy input without mapping it into repair
  prompt text

The adapter must never produce a worker prompt.

### Pass 4: Run Directory And Prompt Artifacts

Patch `run_stepwise.py` so every prompt and reconciliation artifact is saved
in predictable paths. This improves auditability around the new diagnostic and
repair prompts.

### Pass 5: Learning Ledger

Add `references/learnings.md` and `scripts/stepwise_learnings.py`.

Start by appending `candidate` learnings only. Query and display applicable
learnings before repair, but do not let them become hard constraints.

### Pass 6: Promotion Workflow

Add a human-visible command or documented manual process to promote accepted
learnings into live doctrine. Promotion should be intentional because live
skill doctrine affects future machines and users.

## Risks And Countermeasures

### Risk: Reconciliation becomes performative confession

Countermeasure: Stepwise validates the worker's explanation against transcript
and artifact evidence. Confirmation lines are necessary but never sufficient.

### Risk: Diagnostic loops burn time

Countermeasure: Always reconcile, but cap rounds. Simple failures converge in
one round. If a worker cannot produce a coherent confirmed fix inside the cap,
blind repair is unsafe anyway.

### Risk: Learnings become stale global lore

Countermeasure: Every learning carries applicability and contraindication
fields. Stepwise must say why it applies or does not apply before using it.

### Risk: The ledger becomes hidden context

Countermeasure: Store it on disk in `.arch_skill/stepwise/learnings/` with a
human-readable `accepted.md` export. Mention applicable learnings in run
reports.

### Risk: The critic becomes toothless

Countermeasure: The critic remains pass/fail authority. The change only removes
its current role as binding repair-prompt author.

### Risk: The orchestrator starts doing target work

Countermeasure: Keep the existing red line. The orchestrator can inspect run
artifacts, talk to the worker, author prompts, and write run-directory
bookkeeping. It still cannot edit target-repo work products.

## Recommended End State

The strongest version of `$stepwise` is not stricter in the sense of more
checklists. It is more resilient because it separates the layers:

- Worker does target work.
- Critic judges the attempt.
- Orchestrator diagnoses failure and authors repair prompts.
- Learning ledger preserves reusable process memory.
- User can inspect the whole chain on disk.

The key invariant is:

```text
No critic failure is passed through raw.
```

Every fail becomes a small investigation into what the worker misunderstood,
what the critic observed, what the owner contract actually requires, and what
would be overconstraint. That is the behavior that fixed the copy-gate case,
and it is the behavior Stepwise should make routine.
