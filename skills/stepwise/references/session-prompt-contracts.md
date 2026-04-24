# Session prompt contracts

Stepwise sends three kinds of prompts to worker sessions:

- **Initial prompt** on first attempt (`try-1`).
- **Diagnostic prompt** after an observational critic fail or inspectable
  abstain. Diagnostic prompts are read-only and do not consume a repair bounce.
- **Repair prompt** after Stepwise has diagnosed root cause. Repair prompts are
  operational and consume one repair bounce for the repaired session.

The worker never receives Stepwise-internal vocabulary. It sees its step,
owner doctrine, evidence from its own transcript, and source-grounded repair
instructions.

## Initial prompt

```text
You are executing step {{step_n}} of {{total_steps}} in a multi-step
process. Complete this step's declared outcome using the owner skill or
instruction below as authority. Stay inside this step's outcome; do not take
over adjacent stages. End your turn when this step's work is complete.

## Process

{{target_process_name}} - defined in {{target_repo_absolute_path}}.

## Step

{{step_label}}

## Owner instruction

Follow the skill or instruction:

{{skill_or_instruction}}

Owner runbook: {{doctrine_path_for_this_step}}

Read the owner runbook first. Then execute the step. If the owner runbook
names supporting skills, primitives, configs, commands, or MCP tools, load and
use them as part of this step. Required support is not scope drift.

## Expected artifact

{{expected_artifact_block}}

## Boundaries

- Work inside {{target_repo_absolute_path}} only. Do not edit files outside it.
- Preserve the confirmed step outcome and expected artifact.
- Follow the owner runbook's ordering. If it says read doctrine first, do that
  before editing. If it names authoritative support, use that support before
  repo-wide discovery.
- Do not claim work you did not do. If a sub-step is infeasible, first run the
  safe read/help/list command or inspect the owning doctrine path that would
  prove the blocker, then say so explicitly and stop with that evidence.
- Do not jump to a different stage owner, restart the whole process, or invoke
  unrelated workflow/loop skills.
- Do not replace declared authority with repo-wide guessing. When the owner
  runbook or declared support names the authoritative primitive, config,
  endpoint, or command, use that first.
- Do not claim tool availability, support loading, or primitive use that the
  transcript does not show.

When done, end your turn. An independent reader will inspect your work.
```

## Diagnostic prompt

Use this same shape for the current failed worker, an upstream worker, or an
intermediate session during upstream traversal. It is read-only by default.

```text
Diagnostic conversation only. Do not modify files. Do not run commands beyond
safe reads explicitly allowed below. Do not attempt repair.

## What the transcript already shows

- Tool calls during this attempt: {{short_tool_call_list}}
- Owner runbook paths you read or did not read: {{short_runbook_list}}
- Artifact state after the attempt: {{short_artifact_state}}
- Contract clauses this attempt is being judged against: {{short_clause_list}}

## Questions

1. What did you believe this step was asking, and which owner-runbook line made
   you believe it?
2. Which of your actions in this attempt supports that belief, and which of
   them contradicts it?
3. What evidence does the owner contract actually require here?
4. Where did each input to this step come from? Did any of those inputs look
   wrong to you at the time?

End with exactly one line:
CONFIRMATION: <one sentence naming what you now understand about the issue,
citing the owner-runbook clause that implies the correct behavior>.
```

If the answer invents a stricter rule than the owner doctrine supports, stay in
the same diagnostic conversation and ask:

```text
Continue diagnostic conversation only. You stated: "{{quoted_line}}".
Where does the owner runbook or declared support say that? If it is not in the
owner doctrine, what is the owner-doctrine rule you are actually trying to
honor?
```

This is not a separate mode. It is the same evidence conversation refusing to
turn an overcorrection into a new constraint.

## Repair prompt

Stepwise authors repair prompts only after the diagnostic conversation
converges on root cause.

```text
Your prior attempt on this step did not honor its contract. We have diagnosed
the issue.

Execute the repair below. Do not add constraints beyond the user prompt,
manifest, owner runbook, and confirmed repair.

## Confirmed issue

{{one paragraph grounded in the diagnostic conversation}}

## Hard boundaries

- {{boundary with source tag}}

## Repair steps

1. {{instruction with source tag}}
2. {{instruction with source tag}}

## Evidence to leave

- {{artifact state, readback, receipt, or explicit honesty about retroactive work}}

## Stop instead of finishing if

- {{precondition that would make this repair dishonest}}

When the fixes are in place, end your turn.
```

Every numbered repair step must carry one source tag. Valid source tags are:

- `[source: user]`
- `[source: manifest]`
- `[source: owner runbook]`
- `[source: critic evidence]`
- `[source: confirmed diagnosis]`

If a numbered step has no source tag, it is invented and must be removed before
the prompt is sent.

## What stays out of worker prompts

Do not put these internal terms in worker-facing prompts:

- critic
- reconciliation
- breach
- legacy retry-hint field names
- learning
- ledger
- orchestrator
- stepwise

The worker acts on owner doctrine, evidence from its own attempt, and
source-grounded repair instructions. Internal process names are for Stepwise's
run record only.

## Session continuity

Initial prompt goes to a fresh session. Diagnostic and repair prompts resume
the relevant existing session via `-r <session-id>` for Claude or `codex exec
resume <session-id>` for Codex.

After an upstream repair, downstream steps respawn fresh. Do not resume a
downstream session whose history was built on broken upstream input.
