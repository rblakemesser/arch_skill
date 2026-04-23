# Execution defaults: user-supplied, asked if missing

Six base values must be known before Phase 2 can draft a runnable manifest:

- `execution_defaults.step.runtime` - `claude` or `codex` for worker steps
- `execution_defaults.step.model` - model for worker steps
- `execution_defaults.step.effort` - reasoning effort for worker steps
- `execution_defaults.critic.runtime` - `claude` or `codex` for critics
- `execution_defaults.critic.model` - model for critics
- `execution_defaults.critic.effort` - reasoning effort for critics

These are defaults, not a promise that every step uses the same runtime. The
manifest may contain per-step overrides resolved from explicit user
preferences or hard target-repo doctrine. See `execution-routing.md`.

## Why the user supplies defaults

Different work deserves different price points. A lesson-authoring run may
want strong worker steps and a strong critic. A many-step drill may want cheap
workers and a stronger critic. The right baseline is a user judgment, not a
skill heuristic.

Asking once at the start is cheap. Guessing wrong is expensive: wrong runtime
or model wastes money or quality; wrong effort blows budget on trivial work or
under-powers hard work.

## Acceptable shapes in the user's prompt

The intake phase parses whatever the user wrote. Any of these is clear:

- "use Claude Opus 4.7 xhigh for steps and Codex gpt-5.4 xhigh for critic"
- "Codex gpt-5.4 high everywhere" (one value reused for all defaults)
- "steps on gpt-5.4 high, critic on gpt-5.4-mini xhigh"
- "default to Codex gpt-5.4 high, but use Claude Opus 4.7 for copywriting"

None of these is magic. The intake reads the phrase, maps the baseline into
execution defaults, records routing preferences separately, and prints back
the interpretation before executing.

## Asking when missing

If one or more required defaults is unspecified and cannot be inferred
unambiguously, ask ONE consolidated question listing what is missing and what
it controls:

```
I need base execution choices before planning steps.

- step runtime/model/effort: runs each step unless a confirmed per-step
  preference overrides it.
- critic runtime/model/effort: independently checks each step. Worker routing
  preferences do not apply to critics unless you say so.

What should I use?
```

Do not ask six separate questions. Do not default to a favorite model "just
this once". Ask and wait.

If the user answers with one complete value ("Codex gpt-5.4 medium
everywhere"), apply it to both worker and critic defaults and announce that
before executing. If they answer with a worker-only override ("copywriting on
Claude Opus 4.7") but no baseline, still ask for the missing defaults.

## Runtime inference

Runtime is separate from model and effort.

Infer runtime only when the evidence is unambiguous:

- a target repo says "run with Codex"
- the user says "Claude Opus 4.7" or "Codex gpt-5.4"
- an installed CLI supports only the named model family and the user clearly
  intended that family

When inference is ambiguous, ask. Do not build a hidden model-name lookup
table. The runtime choice must be explainable in the Phase 1 announcement.

Critic runtime defaults to the critic default from intake. If the user gives
only one "everywhere" choice, critic and step defaults match. If the user gives
worker-specific preferences, critics keep critic defaults unless explicitly
overridden.

## Pinning

Once set, the full execution policy is written into `state.json` and pinned
with `execution_sha256`. The policy includes defaults and unresolved routing
preferences. Changing it mid-run clears run state.

Per-step retries reuse the same resolved execution block as the original try.
A user who wants a different model for retries should re-invoke the skill with
new execution choices; this skill does not change horses mid-stream.
