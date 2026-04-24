# Stepwise Resilience Refactor

Status: canonical implementation plan for the `$stepwise` resilience
refactor. This document supersedes
`docs/stepwise_failure_reconciliation_refactor.md` for implementation
planning.

Audience: anyone deciding how to change `skills/stepwise/` so failure
repair stops being brittle and so the system gets smarter over time.

Scope: `skills/stepwise/SKILL.md`, its `references/`, its `scripts/`,
plus one new learnings ledger path. No target-repo changes.

Lenses: `$prompt-authoring`'s `prompt-pattern-contract.md` (section
ownership, commander's intent placement, anti-heuristic framing) and
`$skill-authoring`'s `skill-pattern-contract.md` (role boundaries,
progressive disclosure, scripts-only-when-earned).

The design aims for **one mode, one invariant, no heuristic gates**.
Every rule in this plan derives from the single mission sentence below.

---

## 1. The mission

Stepwise maintains a truthful chain from user intent to manifest, from
manifest to owner skill, from owner skill to worker action, from worker
action to evidence, and from evidence to critic judgment.

When the chain breaks, stepwise locates the break and restores truth. It
does not paper over the break.

In plainer terms: stepwise is a thoughtful diagnoser and orchestrator, not a
naive runner with a critic attached.

This is the commander's intent. Every other rule — the critic is
observational, the orchestrator authors repair, the worker never sees
stepwise vocabulary, upstream traversal is part of the normal protocol,
learnings carry applicability — derives from this one sentence. If a
proposed rule does not defend truthful propagation, it does not belong
in the skill.

## 2. Why the current design breaks the chain

The current design puts two responsibilities on the critic that don't
belong there, and it hides the chain instead of propagating it:

1. **The critic authors the worker's next command.** `resume_hint.required_fixes`
   is a concrete execution checklist. `step-prompt-contract.md` wraps it
   as "binding." `SKILL.md` forbids orchestrator commentary. The critic's
   repair text lands in the worker's prompt verbatim. If the critic
   misjudges the repair shape — as in the copy-gate case where "do not
   undo" was the wrong constraint for a timeline-sensitive breach — the
   worker is pointed at a fix that cannot honestly succeed.

2. **There is no place for stepwise to reason between breach and repair.**
   The protocol jumps from `verdict=fail` to `step-resume` with the
   critic's checklist. Stepwise has no authority to inspect evidence,
   hold a diagnostic conversation with the struggling agent, or locate
   the root cause. The chain break is invisible to the skill.

3. **The chain is assumed to be local.** Current upstream routing
   requires the critic to set `route_to_step_n` on a fail. If the root
   cause is upstream and the critic doesn't notice, stepwise hammers a
   local fix. Bad inputs from step 3 become step 6's invented-evidence
   problem. The chain is silently broken upstream; downstream paper-over
   masks it.

The copy-gate incident put all three on display. Fixing it needs one
unified protocol where stepwise reasons about where the chain broke
(here or upstream), talks to the relevant agents, and authors the repair
at the root cause — without the critic handing it a prescription.

## 3. The three roles

Truth propagation needs three orthogonal roles. Each role owns one
surface. Ambiguity belongs to the orchestrator by default, because the
orchestrator is the only role that sees the whole chain.

### Worker

Owns: target-repo changes inside one step's scope. Reads the owner
runbook it was pointed at. Invokes declared support.

Does not own: multi-step planning, self-certification, critique of
other steps.

Recognition test for scope creep: a worker turn that plans future work,
self-judges pass/fail, or narrates process mechanics outside its step.

### Critic

Owns: **observation**. A single question — did the attempt honor its
contract? — answered with evidence. The critic names the breach, points
to the transcript/artifact lines that prove it, and cites the contract
clause the breach violates.

Does not own: the worker's next command. Repair direction. Candidate
fixes. Locus of root cause (current step vs. upstream). Process
recommendations. Timeline-sensitivity flags. Overconstraint risk
analysis. None of these belong to the critic.

Recognition test for scope creep: any critic output that reads like a
prescription. Lists of steps. Paths to read. Commands to run. Words like
"should" about future worker behavior. All of these are stepwise's job.

### Orchestrator (stepwise itself)

Owns: interpreting the user prompt, drafting the manifest, spawning
subprocesses, reading verdicts as evidence, holding diagnostic
conversations with any session (current or upstream), locating the chain
break through reasoning, authoring repair prompts, extracting and
consulting learnings, producing the run report.

Does not own: target-repo edits, overruling the critic's pass/fail
verdict, overruling the worker's scope.

Recognition test for scope creep: an orchestrator action that writes to
a target-repo file, invents a rule not traceable to user prompt /
manifest / owner runbook / critic evidence / diagnostic confirmation, or
lets stepwise vocabulary leak into an agent prompt.

This separation is the skill's peer-group contract. Every later rule
checks against "does this keep the three roles orthogonal and the chain
truthful?"

## 4. The single failure-handling mode

There is one protocol. It runs on every `verdict=fail` and every
`verdict=abstain` whose reason points at inspectable evidence. It has
no branches selected by heuristics. Simple failures converge in one
diagnostic turn; complex ones converge in more; upstream-rooted
failures walk upstream on the same protocol.

### 4.1 The invariant

Between the critic saying "fail" and the worker receiving an
operational repair prompt, stepwise holds a diagnostic conversation
with the agents involved in the chain break, reasons about where in
the chain the break actually lives, and authors a repair prompt that
cites its sources.

The critic's verdict is evidence. The worker's answers are evidence.
The manifest is evidence. The owner doctrine is evidence. None of them
are the repair prompt. The repair prompt is stepwise's synthesis,
grounded in all of them.

### 4.2 The protocol

```
critic.verdict == fail
    |
    v
[Intake]
    Read critic observation + evidence.
    Read transcript, artifacts, owner doctrine, manifest.
    Write own diagnosis of where in the chain truth is suspect.
    |
    v
[Diagnostic conversation]
    Loop (bounded by sanity cap, see 4.4):
        Pick the session most likely to hold the break.
            First pass: the failing step's worker.
            Later passes: upstream sessions when evidence points there.
        Resume that session read-only with a diagnostic prompt.
        Read the agent's answer.
        Compare to evidence in hand.
        Decide one:
            (a) Root cause is local, repair plan is clear   -> exit loop
            (b) Root cause is upstream at step M            -> next iter, session M
            (c) Root cause is owner-doctrine ambiguity      -> halt, ask user
            (d) Sanity cap exhausted without convergence    -> halt with record
    |
    v
[Repair authorship]
    Write a repair prompt for the session that owns the root cause.
    Every instruction carries a source tag (see 6.3).
    No stepwise vocabulary in the worker-facing text.
    |
    v
[Repair execution]
    Resume the root-cause session with the repair prompt.
    Consume one repair bounce on that session's max_retries.
    |
    v
[Critic re-judge]
    Run a fresh critic against the repaired attempt.
    |
    v
    If pass and the repaired session was upstream:
        Respawn each downstream step fresh (step-spawn, new try-1).
        Their session history was built on the broken upstream
        artifact; resuming them would compound the error.
    If fail:
        Re-enter the same protocol from Intake.
    If bounces exhausted on any repaired session:
        Halt with the full diagnostic record.
```

This is the whole protocol. One mode. One flow. The decision tree
inside the diagnostic loop is not a heuristic tree; it is the
orchestrator reasoning from evidence toward the root cause.

### 4.3 Upstream traversal is the same protocol

When the diagnostic conversation with the current worker reveals that
its inputs were already wrong, stepwise walks upstream. It does not
switch modes to do so.

Mechanics:
- The step descriptor's `inputs` field lists the artifacts the step
  reads. Each input traces to an earlier step's `expected_artifact`.
- Stepwise reads the manifest to identify the upstream step whose
  artifact is implicated.
- Stepwise `step-resume` (read-only) that upstream session with the
  same diagnostic prompt shape. The upstream agent answers against its
  own session history and owner doctrine.
- If the upstream agent's evidence matches what the current step
  received, the break is between them — intermediate steps, the
  manifest's wiring, or the handoff. Walk forward from upstream toward
  the current step.
- If the upstream agent reveals its own mistaken model or bad input,
  the break is at or above it. Either repair upstream or traverse
  further.
- When the root cause is located, repair at that session. Then respawn
  downstream steps fresh.

What this buys:
- Bad inputs stop becoming invented-evidence problems at downstream
  steps. The user's concern — "something this child is getting as
  input is wrong, actually go talk to that upstream agent" — is the
  default behavior, not a special mode.
- Paper-over fixes become impossible. Stepwise cannot repair a
  downstream symptom when the diagnostic conversation has surfaced an
  upstream cause.
- The current `autonomous_repair` + `route_to_step_n` pair disappears
  as a distinct mode. It was a narrower version of this protocol
  gated on the critic noticing. Now stepwise notices through its own
  reasoning.

### 4.4 Budget

One budget concept: each session has `max_retries` (existing, default
5). A repair bounce = one operational repair prompt sent to that
session plus the critic's rejudgement of it. Diagnostic conversations
are read-only and do not consume bounces.

One sanity cap: total diagnostic turns per failure, across all
sessions touched, capped at 10. This is containment, not a heuristic
gate. If a failure needs more than 10 read-only turns to converge, the
chain break is not locatable from within the run and halt-with-record
is the honest move.

If any session's `max_retries` is exhausted during repair execution,
halt with the diagnostic record. This matches the existing exhaustion
semantics; it just applies to whichever session was repaired, not
only the current step.

### 4.5 Learnings are consulted, never prescribed

At intake and at repair authoring, stepwise consults the learnings
ledger for entries whose applicability test plausibly matches the
current context. For each candidate it considers, stepwise states
why it applies or why it does not apply.

Applicable learnings inform stepwise's reasoning and repair phrasing.
They never appear in agent prompts as stepwise vocabulary. If a
learning says "treat reused copy as copy-lane," that becomes an
owner-doctrine-backed operational instruction in the repair prompt, or
it does not appear. Learnings are not hidden doctrine injected into
agents.

See section 7 for ledger mechanics.

## 5. Critic contract (radically simplified)

The critic is purely observational. Nothing the critic produces
prescribes what any agent does next.

### 5.1 Verdict schema

```json
{
  "step_n": 6,
  "verdict": "pass | fail | abstain",
  "checks": [
    {
      "name": "skill_order_adherence | no_substep_skipped | artifact_exists | no_fabrication | doctrine_quote_fidelity",
      "status": "pass | fail | inapplicable",
      "evidence": "specific transcript or artifact pointer"
    }
  ],
  "observed_breach": "one sentence naming what the attempt failed to honor, or null when verdict=pass",
  "evidence_pointers": [
    "specific transcript line range or artifact assertion"
  ],
  "contract_clauses_implicated": [
    "owner runbook path:line or manifest clause"
  ],
  "summary": "1-3 sentences for the run report",
  "abstain_reason": "plain English, or null when not abstaining"
}
```

Removed from the previous schema:
- `resume_hint` (with `headline`, `required_fixes`, `do_not_redo`).
- `route_to_step_n`. Upstream routing is stepwise's reasoning, not the
  critic's.
- Any candidate-direction, overconstraint-risk, repair-locus, or
  timeline-sensitivity field.

What remains is observation + evidence + contract citation. That is
the entirety of the critic's contribution. The critic is a function
from (attempt) to (did it honor the contract, and where does the
evidence show it).

### 5.2 Critic prompt body (proposed)

```text
You are the critic for step {{step_n}} of a multi-step process. Your
job is to observe whether this attempt honored its contract, and to
produce evidence-grounded observation only. You are not the repair
author. Do not suggest worker commands. Do not propose fixes. Do not
flag where the repair should happen. Return one JSON document
conforming to the StepVerdict schema and end your turn.

## Step descriptor

{{step_descriptor_json}}

## Active checks

{{active_checks_with_short_definitions}}

## Target repo

{{target_repo_absolute_path}}

## Doctrine paths the step should have followed

{{doctrine_paths_list}}

## What the step produced

- Final assistant message: {{step_final_message_path}}
- Full transcript: {{step_stream_log_path}}
- Session id: {{step_session_id}}

## Artifacts to inspect

{{expected_artifact_block}}

Inspect each listed artifact by reading it or running the declared
read-only verification. Do not write.

## How to judge

For each active check, gather evidence. Record evidence succinctly.
A check passes only when the evidence backs it. "It looks fine" is
not evidence.

If verdict=fail:
- Name the breach in one sentence. Do not prescribe what the worker
  should do next.
- Cite specific transcript lines or artifact assertions as evidence.
- Cite the owner-runbook or manifest clause the breach violates.

If verdict=pass:
- Set observed_breach, evidence_pointers, contract_clauses_implicated,
  abstain_reason all to null / empty as per schema.

If verdict=abstain:
- Name the specific evidence you could not inspect.
- Do not guess the underlying verdict.

Return JSON only.
```

What is removed from today's prompt:
- The "Strong required_fixes say..." block.
- The operational checklist guidance.
- Any mention of timeline-sensitivity, retroactive proof, candidate
  repair directions, overconstraint risks, or upstream routing
  decisions. All of those are stepwise's reasoning, not the critic's.

## 6. Orchestrator repair authorship

The orchestrator authors every repair prompt. It never forwards critic
output as agent-facing text.

### 6.1 Authoritative sources

Every operational instruction in a repair prompt must trace to one of
exactly five sources:

1. The user's raw instructions.
2. The confirmed manifest (step descriptors, expected artifacts,
   boundaries).
3. The owner runbook of the session being repaired (including its
   declared support).
4. The critic's evidence (observation, evidence pointers, contract
   clauses).
5. The diagnostic conversation record (what the agents said about
   their own state and the chain's truth).

Applicable accepted learnings can shape the orchestrator's phrasing
but must surface as owner-doctrine-backed operational instructions, or
they do not appear in the prompt.

Sources explicitly disallowed:
- The orchestrator's general knowledge of the domain.
- Candidate (unaccepted) learnings as binding text.
- Doctrine from adjacent skills not declared by the owner.
- Constraints invented during diagnosis to sound more rigorous.

### 6.2 The diagnostic prompt (one shape for any session)

This prompt is used for the current failing worker, for upstream
workers during traversal, and for any session stepwise needs to
interrogate. It is read-only by default.

```text
Diagnostic conversation only. Do not modify files. Do not run commands
beyond safe reads explicitly allowed below. Do not attempt repair.

## What the transcript already shows

- Tool calls during this attempt: {{short list}}
- Owner runbook paths you read or did not read: {{short list}}
- Artifact state after the attempt: {{short list}}
- Contract clauses the attempt is being judged against: {{short list}}

## Questions

1. What did you believe this step was asking, and which owner-runbook
   line made you believe it?
2. Which of your actions in this attempt supports that belief, and
   which of them contradicts it?
3. What evidence does the owner contract actually require here?
4. Where did each input to this step come from? Did any of those
   inputs look wrong to you at the time?

End with exactly one line:
CONFIRMATION: <one sentence naming what you now understand about the
breach, citing the owner-runbook clause that implies the correct
behavior>.
```

Deliberate choices (prompt-authoring discipline):

- **No stepwise vocabulary.** The agent never sees "critic,"
  "reconciliation," "breach report," "resume_hint," "diagnostic
  phase," "learning," "ledger." These are orchestrator-internal
  concepts. The agent works against owner doctrine and its own
  transcript.
- **No prescriptive framing.** The prompt does not say "your answer
  is wrong" or "you should have done X." It asks the agent to reason
  from its own history and owner doctrine.
- **A question about inputs.** Question 4 is what makes upstream
  traversal possible. If the agent says "the input from step 3
  already contained a placeholder that was never grounded," stepwise
  has a signal to walk upstream.
- **The confirmation cites owner doctrine.** A CONFIRMATION line
  without an owner-runbook citation is incomplete. Stepwise treats
  it as evidence-of-not-yet-converged and continues the conversation.

When stepwise notices the agent stating a rule not derivable from the
owner runbook (the overcorrection pattern the user's test surfaced),
it asks a follow-up in the same conversation:

```text
Continue diagnostic conversation only. You stated: "{{quoted line}}".
Where does the owner runbook or declared support say that? If it is
not in the owner doctrine, what is the owner-doctrine rule you are
actually trying to honor?
```

This is not a separate challenge mode. It is the same diagnostic
conversation noticing invented rules and asking for their source.

### 6.3 The repair prompt

```text
Your prior attempt on this step did not honor its contract. We have
diagnosed the failure.

Execute the repair below. Do not add constraints beyond the user
prompt, manifest, owner runbook, and confirmed repair.

## Confirmed issue

{{one paragraph grounded in the diagnostic conversation}}

## Hard boundaries

- {{boundary with source tag, e.g. "user prompt", "manifest step 6",
  "$lesson-copy-discipline SKILL.md:L42"}}

## Repair steps

1. {{instruction with source tag}}
2. {{instruction with source tag}}

## Evidence to leave

- {{artifact state, readback, receipt, or explicit honesty about
  retroactive work}}

## Stop instead of finishing if

- {{precondition that would make this repair dishonest}}

When the fixes are in place, end your turn.
```

The **source tag on every numbered step** is the mechanical guardrail
against orchestrator scope creep. If a step has no source tag, it is
invented and gets deleted during authoring. A grep-level leak test
enforces this in validation.

When the repair is sent to an upstream session during traversal, the
shape is identical. The repair is about that session's work, not about
the downstream step that triggered the diagnostic.

## 7. Learnings protocol

### 7.1 Location and visibility

Learnings live at
`<orchestrator_repo_root>/.arch_skill/stepwise/learnings/`.

For these to be visible across the user's machine cluster (via
`$amir-publish`), the current gitignore rule has to narrow.

Change: `run-directory-layout.md` currently says *"Add `.arch_skill/`
to the orchestrator repo's `.gitignore` on first write if not already
present."* Replace with *"Add `.arch_skill/stepwise/runs/` to
`.gitignore` on first write."* Runs stay machine-local (they are
ephemeral bookkeeping). Learnings become trackable.

Layout:
```
.arch_skill/stepwise/learnings/
├── index.jsonl        # append-only events; authoritative
├── accepted.md        # regenerated human-scannable summary
├── candidates/LRN-*.md
├── accepted/LRN-*.md
└── rejected/LRN-*.md
```

The user reads `accepted.md` to see current rules at a glance and the
per-entry markdown files for provenance.

### 7.2 Entry schema

```json
{
  "schema_version": 1,
  "id": "LRN-YYYYMMDD-<hash>",
  "created_at": "iso",
  "updated_at": "iso",
  "status": "candidate | accepted | rejected | superseded | promoted",
  "applied_success_count": 0,
  "applied_null_count": 0,
  "source": {
    "run_id": "...",
    "step_n": 6,
    "try_k": 2,
    "diagnostic_path": "steps/6/try-2/diagnostic/"
  },
  "scope": {
    "owner_skill": "$lesson-copy-discipline",
    "failure_class": "e.g. bad-input-propagation-from-upstream",
    "surface": "e.g. learner-visible-copy",
    "support_skills": []
  },
  "observation": "what happened, one sentence",
  "underlying_principle": "what owner doctrine actually requires, phrased as a positive rule",
  "applicability_test": "plain English for when to consult this",
  "contraindications": "when NOT to apply",
  "process_change_suggestion": "what stepwise should do differently when this applies (phrasing in the diagnostic, choice of upstream vs local repair)",
  "promotion_target": "where this becomes live doctrine if accepted",
  "fingerprint": "sha256(normalized scope + underlying_principle)"
}
```

Discipline:
- `observation` = what happened.
- `underlying_principle` = the owner-doctrine-backed rule the agent
  should have known. This is the part that survives promotion.
- `applicability_test` + `contraindications` are both required.
  Without both, the entry is a slogan, not a learning, and is
  rejected at append.
- `process_change_suggestion` describes what stepwise does
  differently, not what the worker does differently. Workers act on
  owner doctrine.

### 7.3 Status transitions and dedup

Append-only JSONL. State transitions are append events referencing
the id. Current status derives from the latest event per id.

Transitions:
- `candidate` on first write.
- `accepted` after one of: user explicit accept, `applied_success_count
  >= 2` across independent runs, or same fingerprint recorded in 2+
  independent runs.
- `rejected` on user rejection, or when the applicability test fails
  retrospectively.
- `superseded` when a sharper learning replaces it.
- `promoted` when a human moves the underlying_principle into live
  doctrine (reference file edit). Promotion is always a deliberate
  human gesture.

Fingerprint dedup: `append` computes `fingerprint` and, if already
present, returns the existing id as a no-op.

### 7.4 Consult discipline

Stepwise consults learnings at intake and at repair authorship. For
each candidate returned by the structural scope match, stepwise states
in writing:

- Why it applies to the current failure (concrete citation of current
  scope overlap), or
- Why it does not apply (the contraindication that fires, or the scope
  mismatch).

Non-applicable near-misses are named and dismissed, not silently
filtered. This is the forcing function against stale lore being reused
just because it matches surface words.

### 7.5 Parallel-run safety

`scripts/stepwise_learnings.py` owns append/query/accept/reject/
promote/export-md/fingerprint. Append takes an `fcntl.flock` on
`index.jsonl`. Readers do not cache; each consult re-reads the ledger
so a candidate written by parallel run A is visible to run B's next
consult.

Applicability judgment is not in Python. The script's `query` returns
candidates whose structural scope matches. The orchestrator narrates
applicability in prose. Scripts own determinism; judgment stays in the
orchestrator.

### 7.6 Surfacing to the user

The run report (`report.md`) includes:
- Applied learnings this run (accepted only).
- Candidate learnings written this run.
- Non-applicable near-misses considered and dismissed (short list).

The user accepts/rejects/promotes learnings via the CLI or by editing
`accepted.md` and running `stepwise_learnings.py sync-from-md`.

## 8. File-by-file changes

Packaging discipline: `SKILL.md` stays lean, references own protocol
detail, scripts own determinism only. No new files beyond what the
protocol requires.

### 8.1 `skills/stepwise/SKILL.md`

Replace the mission paragraph with the truthful-chain sentence from
section 1.

Replace the current non-negotiables list so the goals are front and
center and the mechanics follow from them:

```markdown
## Non-negotiables

- Truthful propagation is the single invariant. Every pass corresponds
  to honest evidence. Every fail is diagnosed to root cause before
  repair. No step passes with fabricated evidence; no repair prompt
  contains invented constraints.
- The critic observes; the orchestrator reasons; the worker executes.
  The critic never writes agent commands. The orchestrator never
  invents constraints. The worker never sees orchestrator-internal
  vocabulary.
- Every critic fail enters the same diagnostic protocol. Stepwise
  holds a read-only diagnostic conversation with the agents involved,
  walking upstream when evidence points there, until the root cause
  is located or the diagnostic turn cap is exhausted.
- Stepwise is willing to go upstream. When the diagnostic conversation
  shows that a step received bad input from an earlier step, stepwise
  resumes the upstream session with the same diagnostic shape and
  repairs at the root cause. Downstream steps respawn fresh after an
  upstream repair; stepwise never papers over an upstream break with
  a downstream patch.
- Every operational instruction in a repair prompt carries a source
  tag (user / manifest / owner runbook / critic evidence / confirmed
  diagnosis). Instructions without a source tag are invented and get
  removed.
- Learnings are consulted with applicability tests and surfaced in
  the orchestrator's reasoning. They never appear as agent-facing
  text. Agents act on owner doctrine, not on stepwise's process
  memory.
```

Remove the old "On critic FAIL, resume the same step's session with
ONLY the critic's `resume_hint`" rule. It contradicts every other
rule above.

Update the workflow phase summary so Phase 4 references the single
diagnose-and-repair protocol rather than the old verdict arithmetic.

### 8.2 `references/workflow-contract.md`

Collapse Phase 4c into one section titled "Diagnose and repair." The
section owns the full protocol from section 4 of this doc: intake,
diagnostic conversation, upstream traversal, repair authorship,
repair execution, critic rejudge, downstream respawn.

Update "Where judgment lives" in Phase 4 to:

```markdown
The critic owns pass/fail observation. The orchestrator owns the
diagnostic conversation, the decision of where in the chain to
repair, and the repair prompt itself. The worker owns target-repo
changes. The run directory holds every artifact of that separation.
```

Remove the separate "autonomous_repair upstream-routing" branch.
Upstream traversal is the default protocol, not a special stop
discipline. `stop_discipline` keeps its remaining meaning (what to
do after repair bounces are exhausted).

### 8.3 `references/critic-contract.md`

Replace `resume_hint` and `route_to_step_n` with the observational
schema from section 5.1.

Remove the "Routing a fail" section. Upstream routing is no longer
the critic's decision.

Tighten "What the critic never does" to explicitly list:
- No prescription.
- No repair steps.
- No path recommendations.
- No command sequences.
- No upstream-routing decisions.
- No timeline-sensitivity or overconstraint analysis.

### 8.4 `references/critic-prompt.md`

Replace the fail-branch body with section 5.2 of this doc.

Remove all guidance about writing `required_fixes`. Remove the
timeline-sensitivity instruction (stepwise figures it out from
evidence). Remove the routing-decision guidance.

Add one explicit anti-pattern example showing what the critic must
not produce.

### 8.5 `references/step-prompt-contract.md`

Rename to `references/session-prompt-contracts.md` — it now holds
contracts for three kinds of prompt sent to agent sessions:

- Initial prompt (unchanged shape).
- Diagnostic prompt (section 6.2; same shape for worker-in-question
  and any upstream session).
- Repair prompt (section 6.3; same shape whether repairing current
  step or an upstream one).

Add a "What stays in the orchestrator's head" section listing
stepwise vocabulary that must not appear in any agent prompt:
critic, reconciliation, breach, resume_hint, learning, ledger,
diagnostic phase, orchestrator, stepwise.

Add the source-tag rule for repair prompts.

### 8.6 `references/diagnose-and-repair.md` (NEW)

Owns the unified protocol end to end. Section 4 of this doc becomes
the body. Houses:
- The invariant.
- The protocol flow chart.
- Upstream traversal mechanics (reading the manifest to find the
  upstream session, resuming by session id).
- Diagnostic turn cap (10) and sanity rules.
- Repair bounce budget semantics (per-session `max_retries`).
- Downstream respawn rule after upstream repair.
- Halt conditions (doctrine ambiguity, exhausted bounces, cap
  exhausted).

Progressive disclosure: this is the highest-leverage new surface.
Folding it into workflow-contract.md would bury it.

### 8.7 `references/learnings.md` (NEW)

Owns ledger mechanics (section 7). Schema, status transitions,
applicability test discipline, dismissal-rationale rule,
parallel-run safety, user surfacing.

### 8.8 `references/run-directory-layout.md`

Add the `diagnostic/` subdirectory per try:

```
steps/<n>/try-<k>/
├── prompt.md                        # initial or repair prompt verbatim
├── stdout.final.json
├── stream.log
├── session_id.txt
├── critic/
│   └── verdict.json
└── diagnostic/
    ├── intake.md                    # orchestrator's own diagnosis
    ├── applicable-learnings.md
    ├── turn-1.with-step-6.prompt.md
    ├── turn-1.with-step-6.response.md
    ├── turn-2.with-step-4.prompt.md      # upstream traversal
    ├── turn-2.with-step-4.response.md
    ├── ...
    └── root-cause.md                # earliest broken link, owner, repair rationale
```

Repairs executed against an upstream session as a result of the
diagnostic live in that upstream step's own try directory
(`steps/4/try-K/`), with a back-reference to the diagnostic path
that triggered them.

Document the `.arch_skill/stepwise/learnings/` tree. Update the
gitignore rule to narrow to `runs/`.

Add a repair status: `repaired-upstream-for-step-<n>` on upstream
steps whose repair was triggered by a downstream failure's
diagnostic.

### 8.9 `references/step-verdict.schema.json`

Rewrite with the observational schema from section 5.1.
`resume_hint` and `route_to_step_n` removed. Codex normalization
(`_codex_strict_schema`) still applied to required-but-nullable
fields (`observed_breach`, `abstain_reason`).

### 8.10 `references/examples.md`

Replace Example 3 (fabrication catch) and Example 7 (upstream route)
with one worked example of the unified protocol that covers both
cases in one diagnostic conversation.

The copy-gate case works well here:
- Critic returns observation only.
- Intake: stepwise writes own diagnosis.
- Diagnostic turn 1 (with step-6 worker): surfaces the
  placeholder-cleanup-is-not-copy misread.
- Follow-up in the same turn: catches an invented stricter rule
  ("every support skill emits a receipt id") and asks for owner
  source.
- Agent corrects itself.
- Repair authored at step 6 with source tags, including honest
  acknowledgment of retroactive grounding.
- Critic re-judges and passes.

Also add an upstream-traversal example: a copy step fails because
its input headline was itself ungrounded upstream. Diagnostic
walks to step 3, catches the ungrounded output, repairs step 3,
respawns steps 4 and 5 fresh, step 4 now passes clean.

### 8.11 `scripts/run_stepwise.py`

Grow plumbing only. Interpretation stays in prose.

- Save every initial/repair prompt as `try-<k>/prompt.md` in
  addition to `invocation.sh`.
- Add `step-diagnose --session-id --round-k --with-step-m` as a
  thin wrapper around `step-resume` that writes output into
  `diagnostic/turn-<k>.with-step-<m>.{prompt,response}.md` and
  does not increment `try-<k>`.
- Reject critic verdicts containing `resume_hint` or
  `route_to_step_n` with a clear error message naming the schema
  change.
- Helpers for upstream traversal: read the manifest, look up a
  session id by `(step_n, latest_try)`, prepare a diagnostic
  prompt file from a template.

### 8.12 `scripts/stepwise_learnings.py` (NEW)

Subcommands (all locked where they touch `index.jsonl`):
- `append --entry-file` — validates schema, computes fingerprint,
  idempotent by fingerprint.
- `query --scope-json` — returns structural-scope-matching
  candidates. No applicability judgment.
- `accept <id>` / `reject <id>` / `promote <id>` — append state
  event.
- `export-md` — regenerate `accepted.md`.
- `sync-from-md` — reconcile edits to `accepted.md` into events.
- `fingerprint --scope-json --principle` — helper.

### 8.13 `scripts/test_run_stepwise.py`

Extend for:
- New observational critic schema validation (good + bad payloads).
- Rejection of stale verdicts containing `resume_hint`.
- `diagnostic/` directory creation on `step-diagnose`.
- Ledger idempotency by fingerprint.
- Ledger status derivation from event history.
- Parallel append safety (lock contention).

## 9. Anti-heuristic guardrails

Three rules. The skill fails its mission if any of them weakens.

1. **No prescription from the critic.** The critic returns
   observation, evidence, and contract citations. No repair steps. No
   paths to read. No commands. No routing. If the critic prompt or
   schema grows any prescriptive field, we have slipped back into the
   broken shape. Mechanical check: grep the schema for fields that
   describe future worker behavior.

2. **No invented constraints in repair prompts.** Every operational
   step carries a source tag. A step without a source tag is invented
   and gets removed at authoring. Mechanical check: grep repair
   prompts for numbered steps missing a source tag.

3. **No stepwise vocabulary in agent prompts.** Agents act on owner
   doctrine. They never see the words critic, reconciliation, breach,
   resume_hint, learning, ledger, orchestrator, stepwise. Mechanical
   check: grep every prompt file under `steps/*/try-*/` and
   `steps/*/try-*/diagnostic/*.prompt.md` for those words.

Each guardrail is mechanical, not cultural. Mechanical enforcement
survives refactors and new contributors.

## 10. What this removes

To keep the plan honest about the complexity it drops:

- `resume_hint` (with `required_fixes`, `do_not_redo`, `headline`).
- `route_to_step_n` as a critic field.
- Candidate repair directions, overconstraint risks, timeline
  sensitivity, repair locus — all from the critic schema.
- `autonomous_repair` as a distinct stop discipline. Upstream
  traversal is the default. `stop_discipline` keeps its remaining
  meaning (halt/ask/skip/escalate when bounces exhausted).
- Separate "reconciliation" and "repair" phases in the workflow.
  One protocol, named "Diagnose and repair."
- Dual budgets (reconciliation vs. repair). One budget per session,
  plus one sanity cap on total diagnostic turns.
- "Challenge round" as a distinct phase. Challenging an invented
  rule is what the diagnostic conversation does when it notices
  one. Same prompt shape.
- "Anti-theater" as a distinct safeguard. The conversation's own
  requirement (citation of owner doctrine in the confirmation)
  catches theater naturally.

What remains is a smaller, sharper protocol: observe → reason →
converse → repair at root cause → respawn downstream when needed.

## 11. What this preserves

- Fresh-per-step worker sessions.
- Stateless critic sub-sessions.
- Manifest confirmation as the single source of truth for run
  boundaries.
- Forced checks and strictness profiles.
- Orchestrator never edits target-repo files.
- Run directory stays under orchestrator control and never pollutes
  the target repo.
- `per_step_retry_cap` and its default of 5.
- Run-id layout and `.arch_skill/stepwise/runs/` location for runs.

Everything the existing skill got right stays. What changes is the
failure-handling path, which is where the skill was blind to the
chain it was supposed to be propagating.

## 12. Validation plan

### 12.1 Package

```bash
cd /Users/aelaguiz/workspace/arch_skill
npx skills check
```

Run `make verify_install` only if install surfaces change (they don't).

### 12.2 Leak tests (mechanical)

Three greps, run on every run directory:

```bash
# Guardrail 1: no prescription in critic output.
rg -n 'required_fixes|resume_hint|route_to_step_n' \
   .arch_skill/stepwise/runs/*/steps/*/try-*/critic/verdict.json \
   && exit 1

# Guardrail 2: every numbered step in a repair prompt has a source tag.
python3 scripts/check_source_tags.py \
   .arch_skill/stepwise/runs/*/steps/*/try-*/prompt.md

# Guardrail 3: no stepwise vocabulary in agent-facing prompts.
rg -n -i 'critic|reconciliation|breach|resume_hint|learning|ledger|orchestrator|stepwise' \
   .arch_skill/stepwise/runs/*/steps/*/try-*/prompt.md \
   .arch_skill/stepwise/runs/*/steps/*/try-*/diagnostic/*.prompt.md \
   && exit 1
```

Any hit on guardrails 1 or 3 is a failure. Missing source tags on
guardrail 2 is a failure.

### 12.3 Scenario tests

Small fixture repos, real stepwise invocations:

- **Mechanical miss.** Worker claims a write it did not do. Protocol
  converges in one diagnostic turn. Repair prompt has one numbered
  step with one source tag. Pass on retry.
- **Timeline-sensitive breach.** Worker edits before a gate. Intake
  diagnosis names the clause. Diagnostic turn surfaces the mistaken
  model. Follow-up catches overcorrection. Repair either redoes
  under the gate or acknowledges retroactive grounding honestly. No
  fabricated pre-gate claim.
- **Upstream root cause.** Step 6 fails because its input from step
  3 was ungrounded. Diagnostic turn with step-6 points at the input.
  Diagnostic turn with step-3 confirms the ungrounded output.
  Repair lands on step 3. Steps 4 and 5 respawn fresh. Step 4 now
  passes clean.
- **Doctrine ambiguity.** Owner runbook is genuinely unclear about a
  required step. Diagnostic surfaces the ambiguity. Stepwise halts
  and asks the user instead of inventing a rule.
- **Parallel ledger.** Two stepwise runs write candidate learnings
  with overlapping scope. Ledger remains valid; both entries
  visible; fingerprints dedup correctly.

### 12.4 Unit tests

- Observational verdict schema good + bad payloads.
- Stale `resume_hint` verdict rejected loudly.
- Diagnostic directory creation on `step-diagnose`.
- Ledger append idempotency.
- Ledger status derivation from event history.
- Source-tag checker.
- Upstream session id lookup from manifest.

## 13. Migration ordering

Five passes, each shippable independently. Each pass is smaller than
the current ship because we are removing complexity, not adding modes.

1. **Doctrine pass.** Update SKILL.md, workflow-contract.md,
   critic-contract.md, critic-prompt.md,
   session-prompt-contracts.md, diagnose-and-repair.md,
   examples.md. No script change. Proves the prose model holds
   end-to-end, including upstream traversal and downstream context
   hygiene.
2. **Run-directory pass.** Update `run_stepwise.py` to save
   `prompt.md` explicitly per try, add `step-diagnose` subcommand,
   add `diagnostic/` layout with `root-cause.md`. Reject verdicts
   with stale fields.
3. **Learnings pass.** Add `learnings.md` reference. Add
   `stepwise_learnings.py`. Narrow `.gitignore` write target to
   `.arch_skill/stepwise/runs/`. Start writing candidates.
4. **Critic schema pass.** Ship the observational schema.
   `resume_hint` and `route_to_step_n` removed. Codex normalization
   updated. Stale verdicts fail loudly; no silent adapter.
5. **Promotion pass.** Document human promotion flow (accepted →
   live reference file or owner doctrine). Add one worked
   upstream-traversal example to `examples.md`.

Passes 1 and 4 are tightly coupled (prose must match schema), but
they can ship in separate commits.

## 14. Decisions the user owns

Each of these is a policy call, not a technical unknown. A
recommendation follows each.

- **Gitignore narrowing.** Change write target to
  `.arch_skill/stepwise/runs/`. Recommended yes. This is the single
  change that makes learnings visible and shareable across the
  machine cluster.
- **Backward compat on the critic schema.** Clean break at pass 4.
  Recommended yes. Runs are short-lived; silent adapter from
  `resume_hint` to the observational schema would mask prompts that
  still contain binding required_fixes language.
- **Diagnostic turn cap.** 10 total turns per failure across all
  sessions. Recommended. Tight enough to prevent runaway, loose
  enough to handle 2-3 upstream hops comfortably.
- **Learning acceptance threshold.** Two independent runs by
  fingerprint, or explicit user accept. Recommended.
- **Ledger residence.** Inside the orchestrator repo's
  `.arch_skill/stepwise/learnings/`. Recommended over per-target-
  repo residence; consolidates process memory across projects.
- **Upstream traversal default.** On by default, no opt-in flag. The
  whole point of the refactor. If a user wants to disable it for a
  specific run, they can use `stop_discipline=halt_and_ask` to
  escalate at the first failure, but the protocol itself does not
  carry a traversal toggle.

## 15. Writing discipline (why this skill reads the way it does)

Every section above is written against `prompt-pattern-contract.md`
and `skill-pattern-contract.md`. The deliberate choices:

- **Commander's intent at the top.** One sentence, mission-level,
  does not hardcode mechanics. Every other rule defends it.
- **Operating principles before process.** Principles teach the why
  (truthful propagation, role separation, no prescription). Process
  shows how those principles play out.
- **High-leverage sections do real work.** System context explains
  the user experience: diagnostic records on disk, learnings
  visible across machines, no fabricated state. Quality bar names
  what strong runs feel like (defensible passes from artifacts
  alone) and contrasts with weak runs (orchestrator's word for it).
  Output contract is precise (schema, directory layout, report
  shape).
- **No keyword-triggered shortcuts.** Failure type is not detected
  by regex on critic text. Repair shape is not selected by mode
  flag. The skill reasons from evidence.
- **Examples teach, not define.** The copy-gate example illustrates
  the protocol; it does not become the protocol's definition.
- **Anti-patterns are explicit.** "Paper over an upstream break with
  a downstream patch" is named as wrong. "Let critic text land in a
  worker prompt" is named as wrong. "Invent a rule to sound more
  rigorous" is named as wrong.

The skill knows what it is for, what good looks like, what
unacceptable looks like, and what to do when the chain breaks. It
does not need a lookup table.

---

## Summary (for the reply)

One mode. One invariant. Three roles. No poisoning surfaces.

- **Mission:** stepwise maintains a truthful chain from user intent
  to critic judgment, and restores truth when the chain breaks.
- **Single failure mode:** every `verdict=fail` enters the same
  diagnostic protocol — read evidence, converse with the agent(s),
  walk upstream when evidence points there, repair at the root
  cause, respawn downstream fresh.
- **Critic is observational only.** No `resume_hint`,
  `route_to_step_n`, candidate directions, or prescriptions.
  Observation + evidence + contract citation. Full stop.
- **Upstream traversal is the default.** When a step's input is
  implicated, stepwise resumes the upstream session with the same
  diagnostic prompt shape and repairs at the root. `autonomous_
  repair` as a distinct mode disappears.
- **Repair authorship is stepwise's.** Every operational step in a
  repair prompt carries a source tag tracing to user, manifest,
  owner runbook, critic evidence, or confirmed diagnosis. Untagged
  steps are invented and removed.
- **No stepwise vocabulary in agent prompts.** Agents act on owner
  doctrine. Mechanical leak test enforces it.
- **Learnings persist with applicability + contraindication**,
  consulted thoughtfully (near-misses dismissed in writing),
  surfaced to the user via `accepted.md` and the run report,
  shareable across the machine cluster after gitignore narrowing.

What this removes that the prior draft kept: dual budgets, the
challenge-round phase, every critic field beyond pure observation,
`autonomous_repair` as a separate mode. Complexity drops because
the protocol is one shape operating on different sessions, not
several shapes stitched together.

Five-pass migration: doctrine → run-dir plumbing → learnings →
critic schema clean break → promotion workflow.
