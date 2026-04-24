# Step prompt contract

Each step sub-session receives one of two prompts:

- **Initial prompt** on first attempt (`try-1`)
- **Resume prompt** on retry (`try-k` for `k >= 2`)

The content of both is strictly bounded. Anything outside these contracts
is orchestrator overreach.

## Initial prompt

```
You are executing step {{step_n}} of {{total_steps}} in a multi-step
process. Complete this step's declared outcome using the owner skill or
instruction below as authority. Stay inside this step's outcome; do not take
over adjacent stages. End your turn when this step's work is complete.

## Process

{{target_process_name}} — defined in {{target_repo_absolute_path}}.

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

- Work inside {{target_repo_absolute_path}} only. Do not edit files
  outside it.
- Preserve the confirmed step outcome and expected artifact.
- Follow the owner runbook's ordering. If it says read doctrine first, do
  that before editing. If it names authoritative support, use that support
  before repo-wide discovery.
- Do not claim work you did not do. If a sub-step is infeasible,
  first run the safe read/help/list command or inspect the owning
  doctrine path that would prove the blocker, then say so explicitly
  and stop with that evidence.
- Do not jump to a different stage owner, restart the whole process, or invoke
  unrelated workflow/loop skills.
- Do not replace declared authority with repo-wide guessing. When the owner
  runbook or a declared support skill names the authoritative primitive,
  config, endpoint, or command, use that first.
- Do not claim tool availability, support loading, or primitive use that the
  transcript does not show.

When done, end your turn. A critic will inspect your work.
```

## Resume prompt

The resume prompt is the critic's `resume_hint` rendered with a fixed,
direct failure wrapper. The orchestrator does not add its own repair ideas,
commentary, apology, or "does this make sense?" question. The step session
already has the full context of the prior attempt in its session history.

```
Your prior attempt failed this step. The critic's findings below are binding.

Do not justify the prior attempt. Do not summarize these instructions back.
Execute the required fixes in order. If a required path, tool, command, or
write primitive is unavailable, stop and report the exact blocker with the
command or path that proved it.

## Failure

{{resume_hint.headline}}

## Required fixes

{{numbered_list_of_resume_hint.required_fixes}}

## Do not redo

{{bulleted_list_of_resume_hint.do_not_redo}}

When the fixes are in place, end your turn.
```

That is the whole resume prompt. No "hope this helps" line. No "let me
know if you need clarification." The step gets a binding recovery order,
not a suggestion to re-interpret the failure.

## Why the discipline

Two temptations must be resisted:

**Tempt 1:** pad the initial prompt with generic advice ("remember to
test thoroughly"). Don't. The runbook at `doctrine_path_for_this_step`
is the owner entrypoint. Our job is to point the step at the owner path and
let that owner path bring in its declared support, not restate it badly or
override it with Stepwise's guesses.

**Tempt 2:** on retry, re-explain the whole step. Don't. The session
already has the initial prompt, the work it did, and any tool output.
Re-explaining wastes tokens and muddies the critic's request. Send the
fixed wrapper plus only the critic's delta.

## Session continuity

Initial prompt goes to a fresh session (capture session id per
`session-resume.md`). Resume prompt goes to the same session via
`-r <session-id>` (Claude) or `codex exec resume <session-id>` (Codex).
Do not start a fresh session on retry — that discards the attempt
history the step session can learn from.

## Step session boundaries

A step session is expected to:

- Read the owner runbook it was pointed at.
- Execute the declared skill or instruction, including owner-declared support
  skills, primitives, configs, commands, and MCP tools when the runbook needs
  them.
- Produce the declared artifact.
- Resolve obvious safe blockers inside its own step before stopping:
  missing-path claims need the exact path checked, command-availability
  claims need the help/list output or owning doctrine read, and support-path
  claims need evidence from the owner or support path.
- End its turn.

A step session is not expected to:

- Plan multi-step work beyond its single step.
- Validate its own work. (The critic does that.)
- Adjust the process or the manifest. (That is a user decision handled
  outside this skill.)
- Treat stale repo-local discovery as higher authority than the owner runbook
  or its declared support.

If a step session finds that the declared step is genuinely impossible
(missing prerequisite, contradicted doctrine, unavailable owner primitive,
etc.), it should say so plainly with the exact path, command, or doctrine
evidence and end its turn. The critic will decide whether this is a fail,
an abstain with a known unblock, or a true user-facing blocker.
