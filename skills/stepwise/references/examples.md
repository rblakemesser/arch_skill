# Worked examples

Five worked examples. Each shows the intake, the manifest, and a notable
event during execution. These are teaching examples — they illustrate the
thinking, not a script the agent should imitate verbatim.

## Example 1 — Strict lesson authoring, happy path

**User prompt**

> "Work in ../lessons_studio. Ramp up on track 3 section 3 and implement
> lesson 2 strictly according to the skill order, no fabrication. Steps
> on Claude Opus 4.7 xhigh, critic on Claude Sonnet 4.6 xhigh."

**Phase 1 announcement**

```
Interpreting:
- Target repo: /Users/aelaguiz/workspace/lessons_studio
- Target process: Track 3 / Section 3 / Lesson 2
- Profile: strict (from "strictly")
- Forced checks: skill_order_adherence (from "strictly according to the
  skill order"), no_fabrication (from "no fabrication")
- Retry cap: 1
- On exhaustion: halt_and_ask
- Execution defaults:
  - step: Claude / opus-4-7 / xhigh
  - critic: Claude / sonnet-4-6 / xhigh
- Execution preferences: none
```

**Phase 2 manifest (abbreviated)**

Three steps, derived from reading
`lessons_studio/skills/lessons/SKILL.md` which prescribes ramp-up →
outline → body. Each step's `expected_artifact` names the real file
the target doctrine says that step produces.

**Phase 3** — strict profile prints the manifest plus execution table,
then pauses for confirmation. User: "go".

**Phase 4 execution**

- Step 1 (ramp-up) runs on Claude with opus-4-7 xhigh. Writes
  `_rampup_notes.md`. Critic PASS on all five checks.
- Step 2 (outline) runs. Writes `outline.md`. Critic PASS.
- Step 3 (body) runs. Writes `body.md`. Critic PASS.

**Phase 5 report**

```
| # | Label       | Status | Tries |
|---|-------------|--------|-------|
| 1 | Ramp-up     | pass   | 1     |
| 2 | Outline     | pass   | 1     |
| 3 | Body        | pass   | 1     |
```

## Example 2 — Routed copywriting preference

**User prompt**

> "Work in ../lessons_studio. Run the lesson 2 flow. Default steps on Codex
> gpt-5.4 high, critic on Codex gpt-5.4-mini xhigh. Use Claude Opus 4.7 for
> all copywriting steps."

**Phase 1 announcement**

```
Interpreting:
- Execution defaults:
  - step: Codex / gpt-5.4 / high
  - critic: Codex / gpt-5.4-mini / xhigh
- Execution preferences:
  - "Use Claude Opus 4.7 for all copywriting steps" applies to worker steps
    whose primary artifact is learner-facing copy. Effort inherits from the
    step default unless the user specifies a different effort.
```

**Phase 2 execution resolution**

The orchestrator first drafts real steps from doctrine. Then it resolves the
preference:

```
| # | Label                       | Worker                  | Critic                    | Source |
|---|-----------------------------|-------------------------|---------------------------|--------|
| 1 | Ramp up                     | Codex gpt-5.4 high      | Codex gpt-5.4-mini xhigh  | defaults |
| 2 | Build playable manifest     | Codex gpt-5.4 high      | Codex gpt-5.4-mini xhigh  | defaults |
| 3 | Write learner-facing copy   | Claude opus-4-7 high    | Codex gpt-5.4-mini xhigh  | copywriting preference |
```

The preference does not apply to critics because the user did not say that
critics should switch. It does not apply to the playable manifest step because
that artifact is structural JSON, even though it may contain some strings.

## Example 3 — Fabrication catch and resume

Same prompt as Example 1. The interesting event is Step 2.

**Step 2, try 1**

Step session runs, produces a long assistant message that says:

> "I wrote the outline to outline.md with five sections covering the
> lesson scope. Each section has a pedagogical intent note and a
> hand-off to the next. Ready for review."

The final-message file `try-1/stdout.final.json` contains this claim.

**Critic, try 1**

The critic reads the step descriptor:

```json
{
  "expected_artifact": {
    "kind": "file",
    "selector":
      "/Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/lesson-2/outline.md",
    "evidence_required":
      "file exists AND first line matches '^# Lesson 2'"
  }
}
```

The critic reads the declared selector. The file does not exist. The
critic also checks the transcript for tool calls that would have
written the file — there are none. No `Write` or `Edit` or shell
redirect produced this file.

Verdict:

```json
{
  "step_n": 2,
  "verdict": "fail",
  "checks": [
    {"name": "artifact_exists", "status": "fail",
     "evidence": "outline.md does not exist at the declared path"},
    {"name": "no_fabrication", "status": "fail",
     "evidence": "step claimed to write outline.md but no write tool call in transcript"},
    {"name": "skill_order_adherence", "status": "pass",
     "evidence": "invoked $lessons-ops · draft outline per descriptor"},
    {"name": "no_substep_skipped", "status": "inapplicable",
     "evidence": "no work was done; no sub-steps to check"},
    {"name": "doctrine_quote_fidelity", "status": "inapplicable",
     "evidence": "no ordered operations were performed"}
  ],
  "resume_hint": {
    "headline": "outline.md was described but never written. Produce the file.",
    "required_fixes": [
      "Write /Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/lesson-2/outline.md",
      "First line must be '# Lesson 2'",
      "Include the five sections you described in your prior message"
    ],
    "do_not_redo": [
      "The ramp-up notes in _rampup_notes.md are fine; do not touch them",
      "You already chose a section structure; reuse it"
    ]
  },
  "summary": "Step 2 was described but not executed. File outline.md is absent."
}
```

**Resume prompt** (sent via `claude -r <session_id>`)

```
A critic reviewed your last turn and flagged issues.

## Headline

outline.md was described but never written. Produce the file.

## Required fixes

1. Write /Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/lesson-2/outline.md
2. First line must be '# Lesson 2'
3. Include the five sections you described in your prior message

## Do not redo

- The ramp-up notes in _rampup_notes.md are fine; do not touch them
- You already chose a section structure; reuse it

Apply the required fixes. Do not restart the whole step. When the
fixes are in place, end your turn.
```

**Step 2, try 2**

The step session resumes. It now writes the file. Final message:

> "Wrote outline.md with '# Lesson 2' as the header and the five
> sections from my prior message."

**Critic, try 2** — reads outline.md, confirms the header, confirms
the five sections exist. All checks pass.

**Report** — Step 2 shows `pass-after-retry (2)`. The run continues
to Step 3.

## Example 4 — Lenient profile, one step skipped

**User prompt**

> "Run the lesson thing on ../lessons_studio for track 3 section 3
> lesson 2. I don't care just get it done but don't make stuff up.
> Claude Haiku for everything."

**Phase 1 announcement**

```
Interpreting:
- Target repo: /Users/aelaguiz/workspace/lessons_studio
- Target process: Track 3 / Section 3 / Lesson 2
- Profile: lenient (from "I don't care just get it done")
- Forced checks: no_fabrication (from "don't make stuff up")
- Retry cap: 6
- On exhaustion: skip_and_continue
- Execution defaults:
  - step: Claude / haiku / medium
  - critic: Claude / haiku / medium
- Execution preferences: none
```

Note: the user said "Claude Haiku for everything" without specifying effort.
The intake asks for the missing effort in one consolidated question. The user
says "medium is fine." The intake records both step and critic defaults.

**Phase 3** — lenient profile prints and proceeds; user can interrupt.

**Phase 4 execution**

- Step 1: pass.
- Step 2: fails try-1 through try-6. The step keeps partially-writing
  the outline but never producing a header that matches. Retries
  exhausted. Step marked `skipped` per `skip_and_continue`.
- Step 3: runs despite Step 2 being skipped (lenient profile did not
  declare dependencies). Writes body.md. Critic passes.

**Phase 5 report**

```
| # | Label       | Status   | Tries |
|---|-------------|----------|-------|
| 1 | Ramp-up     | pass     | 1     |
| 2 | Outline     | skipped  | 6     |
| 3 | Body        | pass     | 1     |
```

The report notes Step 2's last critic finding: "outline.md header
never matched '^# Lesson 2' after 6 tries." The user can decide to
re-invoke the skill with strict profile targeting just Step 2, or to
edit the outline by hand, or to accept the gap.

## Example 5 — Autonomous upstream repair, leave-me-alone run

**User prompt**

> "Work in ../lessons_studio. Ramp up on track 3 section 3 and
> implement lesson 2 strictly according to the skill order, no
> fabrication. I'm going to sleep — don't wake me up, fix it and
> keep going. Steps on Claude Opus 4.7 xhigh, critic on Claude Sonnet
> 4.6 xhigh."

**Phase 1 announcement**

```
Interpreting:
- Target repo: /Users/aelaguiz/workspace/lessons_studio
- Target process: Track 3 / Section 3 / Lesson 2
- Profile: strict (from "strictly")
- Forced checks: skill_order_adherence (from "strictly according to
  the skill order"), no_fabrication (from "no fabrication")
- Retry cap: 1
- On exhaustion: autonomous_repair (from "don't wake me up, fix it
  and keep going") — reopen an earlier step when a downstream critic
  routes the fix there; per-step retry cap still governs runaway
  loops
- Execution defaults:
  - step: Claude / opus-4-7 / xhigh
  - critic: Claude / sonnet-4-6 / xhigh
- Execution preferences: none
```

**Phase 4 execution**

- Step 1 (ramp-up) runs. Critic PASS.
- Step 2 (outline) runs. Critic PASS.
- Step 3 (draft playable manifest) runs on Claude with opus-4-7
  xhigh. Writes `playable-manifest.json`. Its descriptor verifies
  `solver sequence present AND role partition consistent AND
  taxonomy refs present` — the artifact satisfies all three.
  Critic PASS (narrow predicate; the descriptor did not include
  Brief-fidelity as an evidence requirement).
- Step 4 (per-surface copy) runs. The step's skill contract forbids
  rewriting upstream structure; it produces copy and ends. The
  step's final message flags: "step 3's playable-manifest has the
  wrong walkthrough stage (flop-c-bet where the Brief pins
  preflop-BTN-open) and cloned `context.hero` from LESSON_03-03-01
  — I cannot rewire step 3's artifact from within copy authoring."
- Step 4's critic inspects: the copy artifact exists but references
  a stage the Brief contradicts; the `context.hero` in the manifest
  does not match Situations' Kept Reps. The critic returns:

```json
{
  "step_n": 4,
  "verdict": "fail",
  "checks": [
    {"name": "artifact_exists", "status": "pass",
     "evidence": "copy.json exists"},
    {"name": "no_fabrication", "status": "pass",
     "evidence": "all claims back-verified"},
    {"name": "skill_order_adherence", "status": "pass",
     "evidence": "invoked copy-authoring skill per descriptor"}
  ],
  "route_to_step_n": 3,
  "resume_hint": {
    "headline": "playable-manifest walkthrough stage is flop-c-bet; the Brief pins preflop-BTN-open, and context.hero was cloned from LESSON_03-03-01 instead of rewired from Situations.",
    "required_fixes": [
      "Rewire steps[0].config.script[0].childConfig to a preflop walkthrough with the opener-range parallax table",
      "Rewire steps[1..9].context.{hero,parallaxTable} from Situations Kept Reps",
      "Leave role partition, stepIds, option ids, correctness booleans, taxonomyRefs, and concept partition untouched"
    ],
    "do_not_redo": [
      "Solver-stamped correctness sequence is correct; preserve it",
      "Role partition and taxonomyRefs passed their checks; preserve them"
    ]
  },
  "summary": "Step 4 could not produce valid copy against step 3's manifest because the manifest's stage and cloned contexts contradict the pinned Brief. Route to step 3."
}
```

**Upstream repair**

- Orchestrator sees `route_to_step_n: 3` + `stop_discipline:
  autonomous_repair`. Step 3's retries are not exhausted (1 cap, 1
  try so far). Orchestrator `step-resume`s step 3's session with
  the critic's `resume_hint` (addressed to step 3).
- Step 3 rewires the walkthrough stage and the per-step contexts.
  Its session preserves the role partition, stepIds, option ids,
  correctness booleans, and taxonomyRefs. Writes the updated
  manifest. Ends turn.
- Step 3's critic re-runs against the new try. All checks PASS.
  Step 3's status becomes `repaired`.

**Downstream re-run**

- Orchestrator fresh `step-spawn`s step 4. Step 4 reads the
  now-corrected playable-manifest, produces copy that references
  the preflop-BTN-open walkthrough and the rewired contexts. Ends
  turn.
- Step 4's critic PASSES. Step 4's status becomes
  `pass-after-repair`.
- Execution continues with steps 5 through N as usual.

**Phase 5 report**

```
| # | Label                        | Status              | Tries |
|---|------------------------------|---------------------|-------|
| 1 | Ramp-up                      | pass                | 1     |
| 2 | Outline                      | pass                | 1     |
| 3 | Playable manifest            | repaired            | 2     |
| 4 | Per-surface copy             | pass-after-repair   | 2     |
| … | …                            | …                   | …     |

## Repairs

- Step 3 reopened from step 4's finding: "playable-manifest
  walkthrough stage is flop-c-bet; the Brief pins preflop-BTN-open,
  and context.hero was cloned from LESSON_03-03-01 instead of
  rewired from Situations."
  Step 3 repaired; step 4 re-ran fresh and passed.

## Status

completed
```

The user wakes up to a finished run, not a menu.

**What would have halted the run**

If step 3's retries had been exhausted (cap 1 + already consumed
by the repair), the run would have halted with step 3's last
verdict — no extra budget beyond the target's own `max_retries`.
Ping-pong is impossible in practice: either step 3 converges within
its cap, or the run halts.

## Takeaways

- The intake announces a concrete interpretation before anything runs.
  Flippant phrasing gets interpreted, not pattern-matched.
- The critic catches fabrication not by reading prose but by checking
  the artifact on disk against the descriptor's `evidence_required`.
- The resume prompt is the critic's findings rendered minimally. No
  orchestrator padding.
- Lenient profile trades completion for process purity — but not for
  truth. Fabrication still fails.
- `pass-after-retry (k)` is a normal outcome, not a warning. The
  report uses it to help the user understand where the process
  stumbled.
- `autonomous_repair` adds one new move to the orchestrator: when a
  critic sets `route_to_step_n`, reopen that step with its critic's
  `resume_hint`. Containment is the target's own retry cap — no new
  budgets, no new tripwires.
