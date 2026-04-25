# Critic model and effort: user-supplied, asked once

Only the epic critic needs a model+effort pair. arch-step's own
internal children (research, deep-dive, implement, audit-implementation,
etc.) run under arch-step's own discipline — the epic skill does not
override those.

Three values must be known before any sub-plan reaches completion:

- `critic_runtime` — `claude` or `codex`
- `critic_model` — the runnable model identifier (e.g.
  `claude-opus-4-7`, `claude-sonnet-4-6`, `gpt-5.4`,
  `gpt-5.4-mini`, `haiku`)
- `critic_effort` — the reasoning effort level. Claude accepts
  `low | medium | high | xhigh | max`. Codex accepts the same set
  via `-c model_reasoning_effort="<level>"`.

## Why the user picks

The critic's job is important (scope drift detection) but narrow
(four checks, structured output). Different users have different
price points and model preferences. Asking once at `start` mode and
pinning the choice is cheap. Guessing wrong means either wasting
money on oversized critics or underpowering the scope-drift check
that the epic skill's value hinges on.

## Acceptable shapes in the user's start-mode prompt

Any of these unambiguously names the three values:

- "critic on claude opus-4-7 xhigh"
- "use codex gpt-5.4 high for the critic"
- "haiku medium critic"
- "sonnet-4-6 xhigh, claude"

The skill reads the prompt, maps it, prints back the interpretation.
The user can correct in one line.

## Model phrase resolution

The user's model text is intent, not always the exact command-line token.
Before writing `critic_model` into frontmatter or invoking a critic
subprocess, resolve the phrase to the runnable identifier for the chosen
runtime.

This is exact-version normalization, not a lookup table:

- Preserve the model family and numeric version exactly. You may add a
  required provider prefix or change spaces/dots to the runtime's separator,
  but never change the requested version. `opus 4.7` may become
  `claude-opus-4-7`; it may not become any other Opus version.
- For Claude, if the runtime is Claude and the user gives family plus version,
  prefer `claude-<family>-<version-with-hyphens>`. Thus "critic on claude
  opus-4-7 xhigh" resolves to `critic_runtime: claude`,
  `critic_model: claude-opus-4-7`, `critic_effort: xhigh`.
- For Codex, inspect the installed CLI's model list when needed
  (`codex debug models`) and choose the available model with the same family
  and exact version. "codex gpt 5.5 high" resolves to `gpt-5.5` only if that
  exact model is available.
- Family-only aliases such as `opus`, `sonnet`, or `haiku` are acceptable only
  when the user did not pin a version. If a version is pinned, do not fall
  back to a family alias that lets the CLI choose a different version.
- If runtime is missing, discovery is unavailable, the exact version is not
  present, or multiple runnable identifiers could satisfy the phrase, ask the
  user for the missing piece or exact id.
- Do not run paid trial prompts to test Claude model names.

Print the raw-to-resolved mapping before writing the epic doc, for example:
`claude opus-4-7 xhigh -> runtime=claude, model=claude-opus-4-7,
effort=xhigh`.

## Asking when missing

If the user's prompt does not specify, ask one consolidated question
at `start` mode before writing the epic doc:

```
Before I draft the decomposition, I need the epic critic's runtime
and model. The critic runs once per sub-plan at completion to detect
scope drift — compare what shipped against the North Star you
approved.

- Runtime: claude or codex?
- Model: which specific model phrase or runnable id (e.g. Claude Opus 4.7,
  claude-opus-4-7, gpt-5.4, gpt-5.4-mini, haiku)?
- Reasoning effort: low, medium, high, xhigh, or max?

Example: "claude opus-4-7 xhigh" resolves to `claude-opus-4-7`;
"codex gpt-5.4-mini high" stays `gpt-5.4-mini`.
```

Do not default silently. If the user answers with one value only
("opus-4-7"), ask the missing runtime and effort. Once runtime is known, do
same-version model resolution instead of passing raw shorthand to the CLI.

## Pinning

Once set, the three values live in the epic doc's frontmatter and
are pinned by `models_sha256` (hash of the tuple). Future critic
runs read the frontmatter and use the pinned values. `critic_model` stores the
resolved runnable identifier; the raw user phrase belongs in the prompt
interpretation and Orchestration Log, not in the executable field.

Changing any of the three later updates frontmatter and re-hashes.
Past verdicts keep their own records (run directory has the
invocation.sh and prompt.md of whatever model ran at the time).
The skill does not re-run past verdicts on model changes.

## When the user wants to change

The user may say mid-epic: "swap the critic to sonnet-4-6 xhigh."
The skill:

1. Reads the new runtime+model+effort from the user's prose and resolves the
   model to the runnable same-version identifier.
2. Updates the epic doc's frontmatter.
3. Recomputes `models_sha256`.
4. Appends an Orchestration Log entry: `Critic runtime/model/effort
   changed to <new triple>.`
5. Continues at whatever sub-plan the skill was working on. The
   change takes effect for the next critic run.

## Runtime-specific notes

When `critic_runtime: claude`:
- Script uses `claude -p --output-format json --dangerously-skip-permissions
  --settings '{"disableAllHooks":true}' --model <critic_model>
  --effort <critic_effort> --json-schema <inline-schema-json>`.
- Structured verdict arrives in the top-level JSON's
  `structured_output` field.
- cwd for the subprocess is the orchestrator repo root (not the
  target of the sub-plan's DOC_PATH — the critic needs to read
  both files and the critic prompt passes absolute paths).

When `critic_runtime: codex`:
- Script uses `codex exec --ephemeral --dangerously-bypass-approvals-and-sandbox
  --skip-git-repo-check --model <critic_model> -c
  model_reasoning_effort="<critic_effort>" --output-schema
  <schema-file> --json -o <verdict-file>`.
- Structured verdict is written verbatim to the `-o` file.
- `--cd` points at the orchestrator repo root for the same reason.

Both runtimes MUST get the dangerous/skip-permissions/no-sandbox
flags per repo convention. The critic is still read-only in practice
because its prompt tells it not to write and its schema gives it
exactly one output field.
