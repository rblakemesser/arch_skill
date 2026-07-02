# Grok CLI Harness Support Worklog - 2026-06-04

## Goal

Research the local Grok CLI well enough to add future support for Grok child
processes in this repo's subprocess-oriented skills, without implementing that
support in this pass.

Target models from the user ask:

- Grok Build: `grok-build`
- Grok Composer 2.5: `grok-composer-2.5-fast`

This worklog is research and methodology only. No skill package, resolver, or
script was changed.

## Repo Surfaces Read

Harness and routing surfaces:

- `skills/_shared/model_resolution.py`
- `skills/agent-delegate/SKILL.md`
- `skills/agent-delegate/references/model-and-invocation.md`
- `skills/fresh-consult/SKILL.md`
- `skills/fresh-consult/references/model-and-invocation.md`
- `skills/model-consensus/SKILL.md`
- `skills/model-consensus/references/model-and-invocation.md`
- `skills/plan-swarm/SKILL.md`
- `skills/plan-swarm/references/session-reuse.md`
- `skills/plan-swarm/references/arbiter-and-review.md`
- `skills/stepwise/references/model-and-effort.md`
- `skills/stepwise/scripts/run_stepwise.py`
- `skills/arch-epic/references/model-and-effort.md`
- `skills/arch-epic/scripts/run_arch_epic.py`
- `skills/code-review/scripts/run_code_review.py`
- `README.md`

Skill authoring guidance read:

- `skills/skill-authoring/references/skill-pattern-contract.md`
- `skills/skill-authoring/references/peer-groups-and-boundaries.md`

Local Grok docs read:

- `/Users/aelaguiz/.grok/docs/user-guide/02-authentication.md`
- `/Users/aelaguiz/.grok/docs/user-guide/05-configuration.md`
- `/Users/aelaguiz/.grok/docs/user-guide/08-skills.md`
- `/Users/aelaguiz/.grok/docs/user-guide/14-headless-mode.md`
- `/Users/aelaguiz/.grok/docs/user-guide/18-sandbox.md`
- `/Users/aelaguiz/.grok/docs/user-guide/22-permissions-and-safety.md`
- `/Users/aelaguiz/.grok/README.md`

## Current Harness Map

`agent-delegate` is the broad worker lane. It launches one or more Claude,
Codex, or Cursor Agent subprocesses that may edit the shared worktree. It owns
fresh one-shot, fresh-resumable, and explicit same-runtime resume behavior.

`fresh-consult` is the read-only second-opinion lane. It launches fresh child
processes and reports their verdicts without editing files or continuing a
long workflow.

`model-consensus` is the two-participant dialogue lane. It launches resumable
child sessions and manually relays rounds until the participants converge or
expose a small unresolved decision.

`plan-swarm` is a parent orchestrator. It delegates implementation workers
through `agent-delegate`; it should not grow its own Grok subprocess mechanics.
Its arbiter/review policy currently allows Codex or Claude only.

`stepwise` and `arch-epic` are script-backed orchestration lanes. Their Python
scripts build subprocess argv, parse session IDs, and manage repair/resume
state. Adding a new runtime here is materially more work than updating the
prompt-first skills.

`code-review` is intentionally Codex-only. It runs a deterministic Codex
review product with fixed model policy and coverage lenses. Grok support would
be a recharter, not a small provider addition.

## Grok CLI Evidence

Local binary:

```text
/Users/aelaguiz/.local/bin/grok -> /Users/aelaguiz/.grok/bin/grok
grok 0.2.22 (967574cb117)
```

Model discovery:

```text
You are logged in with grok.com.

Default model: grok-build

Available models:
  - grok-composer-2.5-fast
  * grok-build (default)
```

Top-level help confirmed these relevant flags:

- `-p, --single <PROMPT>`
- `--prompt-file <PATH>`
- `--prompt-json <JSON>`
- `--cwd <CWD>`
- `-m, --model <MODEL>`
- `--effort <LEVEL>`
- `--reasoning-effort <EFFORT>`
- `--output-format plain|json|streaming-json`
- `--permission-mode default|acceptEdits|auto|dontAsk|bypassPermissions|plan`
- `--always-approve`
- `--no-memory`
- `--no-subagents`
- `--disable-web-search`
- `--max-turns <N>`
- `-r, --resume [<SESSION_ID>]`
- `-c, --continue`
- `--sandbox <PROFILE>`
- `grok models`
- `grok sessions list`
- `grok export <SESSION_ID> [OUTPUT]`

The installed docs also mention `--yolo` and `-s/--session-id`. Both are
accepted by the local CLI, but `--always-approve` and explicit captured
`--resume <sessionId>` are better first-pass choices because they appear in
current `grok --help` and match this repo's explicit-resume doctrine.

`grok inspect` evidence:

- CWD: `/Users/aelaguiz/workspace/arch_skill`
- Project trusted: `no`
- Project instructions loaded from Claude/Grok compatibility surfaces,
  including repo `AGENTS.md`/`CLAUDE.md` equivalents.
- Skills discovered from Grok plus Claude/Cursor compatibility surfaces.
- Hooks discovered from plugin and Claude compatibility sources.
- No project-local Grok MCP servers were configured by `grok mcp list`, though
  `grok inspect` listed compatibility MCP sources from Claude/Cursor settings.

Important isolation finding: no documented Grok equivalent of Claude
`--settings '{"disableAllHooks":true}'` or Codex `--disable codex_hooks` was
found. Do not invent a hook-suppression flag. Use Grok's documented headless
controls and keep any hook-isolation question explicit in future design.

## Smoke Test Artifacts

All test artifacts were written under:

```text
/tmp/grok-cli-research-20260604
```

Successful model smoke tests:

- `grok-build.events.jsonl`: exited `0`, final text `GROK_BUILD_OK`
- `grok-composer.events.jsonl`: exited `0`, final text `GROK_COMPOSER_OK`
- `grok-build.output.json`: exited `0`, final text `GROK_JSON_OK`
- `grok-build-resume.events.jsonl`: exited `0`, final text `GROK_RESUME_OK`
- `grok-no-auto-update.output.json`: exited `0`, final text
  `GROK_NO_AUTO_UPDATE_OK`
- `grok-rust-log-off.output.json`: exited `0`, final text
  `GROK_RUST_LOG_OFF_OK`

Failure tests:

- `grok-bad-resume.output.json`: exited `1`, stdout was
  `{"type":"error","message":"Couldn't create session: Session does not exist"}`
- `grok-bad-resume-rust-log-off.output.json`: same failure with
  `RUST_LOG=off`; stderr still preserved the human-readable error.
- `grok-clean.output.json`: exited `1` when both `--no-subagents` and
  `--disallowed-tools Agent` were supplied. The error was a tool requirement
  conflict around `run_terminal_cmd` background settings. Do not combine those
  flags in the first support pass.

Session export:

- `grok export 019e937d-e0ab-7761-a27e-6ebfe806f049
  /tmp/grok-cli-research-20260604/grok-rust-log-off.export.md` exited `0`.
- The export contained a simple Markdown transcript with `## User` and
  `## Assistant` sections.

## Output Contracts

`--output-format json` writes one JSON object to stdout on success:

```json
{
  "text": "GROK_JSON_OK",
  "stopReason": "EndTurn",
  "sessionId": "019e937b-a3b1-70e3-9999-107569d4a816",
  "requestId": "79bf8ac5-4b1c-46e7-83cd-d2b24b53b25a",
  "thought": "The user query is: \"Reply with exactly GROK_JSON_OK and no other text.\"\n"
}
```

`--output-format streaming-json` writes JSONL events to stdout. The observed
event types were:

```json
{"type":"thought","data":"The"}
{"type":"text","data":"G"}
{"type":"end","stopReason":"EndTurn","sessionId":"019e937a-5fba-74a0-8667-266384b6f256","requestId":"bcef3484-09e7-48b4-9997-8ab3b94416f0"}
```

Final text extraction for streaming mode:

1. Read `events.jsonl` line by line.
2. Parse JSON objects.
3. Concatenate `data` for every event with `type == "text"`.
4. Capture the session handle from the final `type == "end"` event's
   `sessionId`.
5. Treat missing final `end`, missing `sessionId` in resumable mode, empty
   final text, or non-zero exit as malformed.

Do not include `thought` text in `final.txt`. It is useful monitoring/debug
data, not the child answer.

On startup failure with `--output-format json`, Grok may write an error object
to stdout:

```json
{"type":"error","message":"Couldn't create session: Session does not exist"}
```

Failure handling should check process exit code first and preserve stdout and
stderr for debugging.

## Recommended Grok Command Shape

Use Grok headless mode, not `grok agent headless`, for the first provider
support pass. `grok agent ...` is ACP/WebSocket integration and is heavier than
the existing subprocess pattern.

Fresh one-shot or fresh-resumable, streaming mode:

```bash
RUST_LOG=off grok \
  --cwd "<work_root>" \
  --no-auto-update \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model "<resolved_grok_model>" \
  --effort "<resolved_effort>" \
  --output-format streaming-json \
  --prompt-file "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Resume:

```bash
RUST_LOG=off grok \
  --cwd "<work_root>" \
  --no-auto-update \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model "<resolved_grok_model>" \
  --effort "<resolved_effort>" \
  --output-format streaming-json \
  --resume "<session_id>" \
  --prompt-file "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Notes:

- `RUST_LOG=off` suppressed noisy successful-run stderr logs while preserving
  useful failure errors in the tested fake-resume path.
- Do not pass `--sandbox disabled`. That is not a built-in Grok profile.
  Sandbox is off by default. If a future caller wants a sandbox, use one of
  the documented profiles: `workspace`, `read-only`, or `strict`.
- Do not combine `--no-subagents` with `--disallowed-tools Agent` until the
  tool requirement conflict is understood and retested.
- `--always-approve` is the current help-visible spelling. `--yolo` works in
  local docs and local version checks, but using the help-visible flag is less
  surprising.
- Use `--prompt-file` for long prompts. It was tested successfully with JSON
  output and avoids command-line prompt length problems.
- Use `streaming-json` for harnesses that need live monitoring. Use `json`
  only for simple one-shot utility calls where no stream is needed.

## Model Resolution Methodology

Add a distinct runtime, likely `grok`, instead of folding Grok into Cursor
Agent or Codex.

Exact local model IDs:

- `grok-build`
- `grok-composer-2.5-fast`

Suggested inference rules:

- `grok`, `grok cli`, `grok build`, or `grok-build` implies
  `runtime=grok`, `model=grok-build` unless the user names Composer.
- `grok composer`, `grok composer 2.5`, `grok-composer-2.5-fast`, or
  `composer 2.5` in an already-Grok context implies
  `runtime=grok`, `model=grok-composer-2.5-fast`.
- Bare `composer`, `composer 2.5`, or bare `2.5` becomes ambiguous once Grok is
  added. Preserve existing Cursor behavior only in an explicit Cursor Agent
  context. Outside a Grok or Cursor context, ask for the runtime.
- Never route Grok model IDs through Cursor Agent. Cursor uses
  `composer-2.5-fast`; Grok uses `grok-composer-2.5-fast`.
- Never route GPT/GBT/OpenAI models through Grok.
- Confirm availability with `grok models` when needed. If `grok models` cannot
  run, ask for a runnable Grok model ID instead of guessing.

Effort:

- Grok accepts `--effort low|medium|high|xhigh|max` per `grok --help`.
- The first-pass command should use `--effort`, not `--reasoning-effort`,
  because `--effort` is documented as the headless effort flag and was tested.
- If effort is missing for a Grok child, ask unless the owning skill chooses to
  treat a model as having an encoded default. Since Grok exposes an effort flag,
  asking is cleaner and closer to Codex/Claude behavior.

## Proposed Support Plan

No implementation was done. If support is added later, make the changes in
this order.

1. Update `skills/_shared/model_resolution.py`.
   - Add `grok` to valid runtimes.
   - Add Grok model family parsing.
   - Add a conservative `discover_grok_models()` helper that shells out to
     `grok models` and returns the model IDs.
   - Preserve the existing exact-version and fail-loud doctrine.
   - Repair Cursor Composer ambiguity so bare `composer 2.5` only resolves
     when the runtime context is explicit.

2. Update prompt-first skill doctrine for `agent-delegate`,
   `fresh-consult`, and `model-consensus`.
   - Add Grok to descriptions, non-negotiables, required values, model
     resolution examples, command shapes, parsing rules, and failure behavior.
   - Keep Grok as its own provider lane.
   - State that Grok has no known hook-suppression flag; do not invent one.
   - Use `grok` command shapes from this worklog.

3. Update `plan-swarm` only where it delegates to `agent-delegate`.
   - Allow Grok workers if the user chooses them.
   - Decide separately whether Grok can be an arbiter/review runtime. Current
     review policy is Codex/Claude only.
   - Keep all actual child launching through `agent-delegate`.

4. Treat `stepwise` and `arch-epic` as a later, script-level project.
   - Their Python scripts currently branch only on `claude` and `codex`.
   - Adding Grok requires argv builders, session parsing, final extraction,
     state schema updates, tests, and doctrine updates.
   - Grok does not expose an observed schema-enforced output flag comparable
     to Codex `--output-schema` or Claude `--json-schema`, so do not add Grok
     as a critic runtime until structured verdict handling is designed and
     tested.

5. Leave `code-review` Codex-only unless the user explicitly recharters it.
   - Its fixed Codex lens fan-out is the product.
   - Grok support would change the review guarantees, not just a CLI flag.

6. Update install/readme surfaces only if runtime support is actually added.
   - `README.md` currently says subprocess skills require `claude`, `codex`,
     or `agent`. That would need `grok`.
   - Makefile install lists probably do not change unless a new skill is added.

## Verification Commands Run

Representative commands:

```bash
rtk grok --version
rtk grok --help
rtk grok agent --help
rtk grok agent headless --help
rtk grok models
rtk grok inspect
rtk grok sessions list -n 5
rtk grok export 019e937d-e0ab-7761-a27e-6ebfe806f049 /tmp/grok-cli-research-20260604/grok-rust-log-off.export.md
```

Representative successful model runs:

```bash
RUST_LOG=off rtk proxy grok \
  --cwd /Users/aelaguiz/workspace/arch_skill \
  --no-auto-update \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model grok-build \
  --effort low \
  --output-format json \
  -p 'Reply with exactly GROK_RUST_LOG_OFF_OK and no other text.'
```

```bash
rtk proxy grok \
  --cwd /Users/aelaguiz/workspace/arch_skill \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model grok-composer-2.5-fast \
  --effort low \
  --output-format streaming-json \
  -p 'Reply with exactly GROK_COMPOSER_OK and no other text.'
```

Representative resume test:

```bash
rtk proxy grok \
  --cwd /Users/aelaguiz/workspace/arch_skill \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model grok-build \
  --effort low \
  --output-format streaming-json \
  --resume 019e937a-5fba-74a0-8667-266384b6f256 \
  -p 'Reply with exactly GROK_RESUME_OK and no other text.'
```

Representative failure test:

```bash
RUST_LOG=off rtk proxy grok \
  --cwd /Users/aelaguiz/workspace/arch_skill \
  --no-auto-update \
  --no-memory \
  --no-subagents \
  --disable-web-search \
  --permission-mode bypassPermissions \
  --always-approve \
  --model grok-build \
  --effort low \
  --output-format json \
  --resume definitely-not-a-real-session \
  -p 'This should not run.'
```

Observed result:

- Exit code: `1`
- Stdout: `{"type":"error","message":"Couldn't create session: Session does not exist"}`
- Stderr: `Error: Couldn't create session: Session does not exist`

## Completion State

The methodology is definitive for adding Grok to prompt-first child-process
skills that need fresh, resumable, or explicitly resumed headless subprocesses:
`agent-delegate`, `fresh-consult`, and `model-consensus`.

The methodology is intentionally not a green light for schema-enforced critics
in `stepwise` or `arch-epic`. Those require extra design because the tested
Grok CLI surfaces do not show a schema-enforced output flag.
