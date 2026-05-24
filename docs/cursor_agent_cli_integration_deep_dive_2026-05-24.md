# Cursor Agent CLI Integration Deep Dive

Date: 2026-05-24

Question: can the local `agent` command be used as a third child-agent runtime
alongside `codex` and `claude` in `fresh-consult`, `agent-delegate`, and
`model-consensus`?

Short answer: yes, with integration work. The local `agent` command is Cursor
Agent CLI. It supports headless scripting, prompt stdin, JSON and NDJSON output,
model selection, workspace pinning, force/yolo execution, sandbox selection,
and explicit session resume. The main differences from the current Codex and
Claude paths are:

- effort is encoded in Cursor model ids, not passed as a separate `--effort`
  flag
- final-output capture must be implemented by parsing stdout; there is no
  Codex-style `-o` final-message flag
- no local help flag was found for hook suppression equivalent to
  `--disable codex_hooks` or Claude `--settings '{"disableAllHooks":true}'`
- Cursor's rules/MCP behavior is its own runtime surface, so it should be
  modeled as `runtime=agent`, not as an alias for Codex or Claude

## Evidence Checked

Local command evidence:

- `command -v agent` -> `/Users/aelaguiz/.local/bin/agent`
- `agent --version` -> `2026.05.20-2b5dd59`
- `agent --help` confirmed:
  - `-p, --print`
  - `--output-format text | json | stream-json`
  - `--stream-partial-output`
  - `--mode plan | ask`
  - `--resume [chatId]`
  - `--continue`
  - `--model <model>`
  - `--list-models`
  - `-f, --force` and `--yolo`
  - `--sandbox enabled | disabled`
  - `--trust`
  - `--workspace <path>`
  - `--plugin-dir <path>`
  - `--approve-mcps`
  - `-w, --worktree [name]`
- `agent models` and `agent --list-models` both listed account-available model
  ids. Examples included `composer-2.5-fast`, `gpt-5.5-high`,
  `gpt-5.5-extra-high`, `gpt-5.4-xhigh`, `claude-opus-4-7-thinking-xhigh`,
  `gpt-5.4-mini-xhigh`, and many others.
- `agent status --format json` and `agent about` confirmed the local CLI is
  authenticated. Account-identifying details are intentionally omitted here.
- `agent create-chat` returned a UUID-shaped chat id.
- A JSON smoke test succeeded:

```bash
agent -p \
  --mode ask \
  --output-format json \
  --trust \
  --sandbox disabled \
  --model composer-2.5-fast \
  "Do not read files or run tools. Reply with exactly: OK"
```

The response was a single JSON object with:

```json
{
  "type": "result",
  "subtype": "success",
  "is_error": false,
  "duration_ms": 7184,
  "duration_api_ms": 7184,
  "result": "OK",
  "session_id": "<uuid>",
  "request_id": "<uuid>",
  "usage": {
    "inputTokens": 71523,
    "outputTokens": 33,
    "cacheReadTokens": 5888,
    "cacheWriteTokens": 0
  }
}
```

- A `stream-json` smoke test succeeded and produced NDJSON records with
  `system`, `user`, `assistant`, and terminal `result` events.
- An explicit resume smoke test succeeded:

```bash
agent -p \
  --mode ask \
  --output-format json \
  --trust \
  --sandbox disabled \
  --model composer-2.5-fast \
  --resume "<session_id>" \
  "Do not read files or run tools. Reply with exactly: RESUMED"
```

The response returned the same `session_id`.

- A stdin smoke test succeeded:

```bash
printf %s "Do not read files or run tools. Reply with exactly: STDIN" | \
  agent -p \
    --mode ask \
    --output-format json \
    --trust \
    --sandbox disabled \
    --model composer-2.5-fast
```

Official docs checked:

- [Cursor output format reference](https://docs.cursor.com/en/cli/reference/output-format)
- [Cursor CLI usage](https://docs.cursor.com/en/cli/using)
- [Cursor headless CLI guide](https://docs.cursor.com/en/cli/headless)

Useful doc-backed facts:

- Cursor documents `--print` as the non-interactive path for scripts and CI.
- Cursor documents `--output-format json` as a single terminal JSON object.
- Cursor documents `--output-format stream-json` as newline-delimited JSON with
  a terminal `result` event.
- Cursor documents `--resume [thread id]`, `cursor-agent resume`, and
  `cursor-agent ls` for history/resume.
- Cursor documents that the CLI reads `.cursor/rules`, project-root
  `AGENTS.md`, and project-root `CLAUDE.md`.
- Cursor documents MCP auto-detection from `mcp.json`.

Important mismatch: local `agent --help` says default `--output-format` is
`text`, while the official output-format page says the print-mode default is
`stream-json`. Integration should always pass `--output-format` explicitly.

## Capability Matrix

| Requirement | Codex path today | Claude path today | Agent CLI evidence | Integration status |
| --- | --- | --- | --- | --- |
| Non-interactive run | `codex exec` | `claude -p` | `agent -p` | Supported |
| Prompt from stdin | yes | yes | smoke-tested yes | Supported |
| Work root pinning | `-C` / `--cd` | run from root | `--workspace <path>` | Supported |
| Model selection | `--model` | `--model` | `--model` | Supported |
| Effort selection | config flag | `--effort` | encoded in model id | Needs resolver changes |
| Live JSON stream | `--json` | `stream-json` | `--output-format stream-json` | Supported |
| Final output file | `-o` | parse `type=result` | parse terminal `result` | Needs adapter |
| Session id capture | `thread.started` | final result event | terminal `result.session_id` | Supported |
| Explicit resume | `codex exec resume <id>` | `-r <id>` | `--resume <id>` | Supported |
| Avoid latest resume | avoid `--last` | avoid `--continue` | avoid `--continue` and `agent resume` | Supported by policy |
| Hook suppression | `--disable codex_hooks` | `disableAllHooks` setting | no equivalent found | Gap or not applicable |
| Permission bypass | dangerous bypass | dangerous skip | `--force`, `--yolo`, `--sandbox disabled` | Supported with different flags |
| Read-only planning | prompt contract | prompt contract | `--mode ask` / `--mode plan` | Supported, but verify sandbox semantics |
| JSON schema final answer | available in other Codex paths | `--json-schema` in other Claude paths | no schema flag found | Not supported by CLI help |
| Worktree isolation | not used by these skills | not used by these skills | `-w, --worktree` exists | Do not use for current shared-worktree skills |

## Model And Effort Handling

Current skills carry separate values:

```text
runtime=<claude|codex>
model=<runnable id>
effort=<low|medium|high|xhigh|max>
```

Cursor Agent does not expose a separate `--effort` flag. Its model list embeds
effort in the runnable model id:

```text
gpt-5.5-high
gpt-5.5-extra-high
gpt-5.4-xhigh
claude-opus-4-7-thinking-xhigh
claude-opus-4-7-thinking-max
gpt-5.4-mini-xhigh
```

Recommended rule for `runtime=agent`:

- Keep asking the user for runtime, model, and effort in the skill contract
  until the skill prose is intentionally changed.
- Resolve `model + effort` into one exact Cursor model id from `agent models`.
- Store the execution record as:

```json
{
  "runtime": "agent",
  "model": "<cursor model id>",
  "effort": "encoded-in-model:<requested effort>"
}
```

- If the requested effort has no exact model-id equivalent, ask for the runnable
  `agent models` id instead of guessing.
- Do not map `xhigh` to `extra-high` blindly across families. Local examples
  use both spellings depending on model family.

## Candidate Invocation Shapes

Use `stream-json` as the default integration format. It gives live progress and
the final result in one artifact stream.

### Fresh Consult

For read-only or planning-style consults, prefer `--mode ask` or `--mode plan`,
no `--force`, and an explicit output format:

```bash
agent -p \
  --mode ask \
  --output-format stream-json \
  --trust \
  --workspace "<work_root>" \
  --model "<resolved_agent_model>" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

After exit:

```bash
jq -s -r '[.[] | select(.type=="result" and .subtype=="success")][-1].result // empty' \
  "$EVENTS_PATH" > "$FINAL_PATH"
```

Treat the run as malformed when the process exits zero but no terminal
`result` event exists, `result` is empty, or the child omits the required
verdict footer.

### Agent Delegate

For editful foreground delegation, `agent` has the needed headless controls:

```bash
agent -p \
  --force \
  --sandbox disabled \
  --output-format stream-json \
  --trust \
  --workspace "<work_root>" \
  --model "<resolved_agent_model>" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Extract final text and session id:

```bash
jq -s -r '[.[] | select(.type=="result" and .subtype=="success")][-1].result // empty' \
  "$EVENTS_PATH" > "$FINAL_PATH"

jq -s -r '[.[] | select(.type=="result" and .subtype=="success")][-1].session_id // empty' \
  "$EVENTS_PATH" > "$SESSION_PATH"
```

For explicit resume, use the same runtime and explicit id:

```bash
agent -p \
  --force \
  --sandbox disabled \
  --output-format stream-json \
  --trust \
  --workspace "<same_work_root>" \
  --model "<resolved_agent_model>" \
  --resume "<session_id>" \
  < "$PROMPT_PATH" \
  > "$EVENTS_PATH" \
  2> "$STDERR_PATH"
```

Do not use `--continue`, `agent resume`, or any "latest" selection in these
skills. They are ambiguous in the same way Claude `--continue` and Codex
`--last` are ambiguous.

Do not use `-w` / `--worktree` for `agent-delegate` unless the skill is
explicitly redesigned. The current skill is shared-worktree only.

### Model Consensus

`model-consensus` can use `agent` as one or both participants. Start each
participant as a fresh resumable session and capture its `session_id` from the
terminal result event:

```bash
agent -p \
  --mode plan \
  --output-format stream-json \
  --trust \
  --workspace "<work_root>" \
  --model "<resolved_agent_model>" \
  < "$RUN_DIR/round-01/model-a-prompt.md" \
  > "$RUN_DIR/round-01/model-a-events.jsonl" \
  2> "$RUN_DIR/round-01/model-a-stderr.log"
```

Resume later rounds explicitly:

```bash
agent -p \
  --mode plan \
  --output-format stream-json \
  --trust \
  --workspace "<same_work_root>" \
  --model "<resolved_agent_model>" \
  --resume "<session_id>" \
  < "$RUN_DIR/round-02/model-a-prompt.md" \
  > "$RUN_DIR/round-02/model-a-events.jsonl" \
  2> "$RUN_DIR/round-02/model-a-stderr.log"
```

If the consensus participant should be a hands-on worker instead of a planning
participant, that is no longer `model-consensus`; route to `agent-delegate`.

## Fit By Skill

### `fresh-consult`

Fit: good, after output parsing and model-resolution changes.

Use `agent` for cold read-only consults when the user asks for Cursor Agent or
an Agent CLI model. `--mode ask` or `--mode plan` plus no `--force` is the
closest local read-only shape.

Caveat: the current fresh-consult contract says children are hook-suppressed
and unsandboxed. Agent does not expose a matching hook-suppression flag. This
is likely acceptable for Codex/Claude hook recursion because Cursor Agent is a
separate runtime, but it should be named in the skill docs rather than hidden.

### `agent-delegate`

Fit: strong, after output parsing, model-resolution, and resume-doc changes.

Agent supports foreground non-interactive editful work with:

- `-p`
- `--force`
- `--sandbox disabled`
- `--trust`
- `--workspace`
- `--model`
- `--resume <session_id>`
- `stream-json`

This maps well to shared-worktree delegated implementation. The child still
needs the same prompt boundaries: read local instructions, do not revert
unfamiliar work, report changed files, run verification, and do not commit or
push unless explicitly asked.

Caveat: local docs say Cursor reads project-root `AGENTS.md` and `CLAUDE.md`;
they do not prove nested AGENTS.md handling. The delegation prompt should keep
the existing instruction that the child must read applicable local
instructions before editing.

### `model-consensus`

Fit: good, with one design choice.

Agent can participate as either model session because explicit session resume
works and stream-json gives an inspectable event log. The parent can run:

- Codex vs Agent
- Claude vs Agent
- Agent vs Agent using two different Cursor model ids

Design choice: if both participants are `runtime=agent`, they share Cursor
Agent's system/tooling layer even if their underlying model ids differ. That is
still useful, but it is not the same kind of runtime diversity as Codex vs
Claude.

## Risks And Gaps

- `--output-format` default conflict: local help says `text`; official docs say
  `stream-json` for print-mode defaults. Always pass the format.
- No separate `--effort`: the shared model resolver needs a Cursor branch that
  resolves model-plus-effort into one runnable model id.
- No final-output file flag: always parse stdout and write `final.txt`
  ourselves.
- No final-answer JSON schema flag found: keep using footer contracts for these
  three skills.
- No hook-suppression flag found: treat Cursor Agent as a distinct runtime with
  no Codex/Claude hook recursion, but do not claim hooks are disabled.
- Rules and MCP can affect behavior: Cursor reads `.cursor/rules`,
  project-root `AGENTS.md`, project-root `CLAUDE.md`, and MCP config. This is a
  feature for local work, but it means `agent` is not a sterile model caller.
- Trivial fresh runs loaded large context on this repo. The JSON smoke test
  reported about 71k input tokens for a no-tool prompt. Resumed runs were much
  smaller because the session cache was reused. This matters for cost and
  latency when using Agent as a "fresh" participant in large repos.
- `--stream-partial-output` can produce multiple assistant events. Use the
  terminal `result` event as canonical.
- `agent create-chat` exists and emits a UUID, but the three skills do not need
  pre-created chats. They can capture `session_id` from the first terminal
  result event.
- `--continue`, `agent resume`, and `agent ls` are interactive/latest-session
  surfaces. They are not safe for deterministic child orchestration.
- `-w` / `--worktree` exists but conflicts with the current shared-worktree
  contract for `agent-delegate`.

## Implementation Impact If We Add It

Minimum skill-package changes:

1. Add `agent` to the supported runtime list in:
   - `skills/fresh-consult/SKILL.md`
   - `skills/fresh-consult/references/model-and-invocation.md`
   - `skills/agent-delegate/SKILL.md`
   - `skills/agent-delegate/references/model-and-invocation.md`
   - `skills/model-consensus/SKILL.md`
   - `skills/model-consensus/references/model-and-invocation.md`
2. Extend runtime inference:
   - `agent`, `cursor`, `cursor agent`, and `cursor-agent` imply
     `runtime=agent`
   - underlying provider words such as `gpt` or `claude` should continue to
     imply Codex/Claude unless the user also says Cursor/Agent
3. Add Agent model resolution:
   - inspect `agent models` or `agent --list-models`
   - resolve exact family/version/effort to one Cursor model id
   - ask when no exact model id exists
4. Add Agent invocation blocks:
   - fresh one-shot
   - resumable first turn
   - explicit resume
   - stream-json parsing into `final.txt` and `session_id.txt`
5. Update output contracts:
   - `events.jsonl` is Agent NDJSON stdout
   - `final.txt` is parsed from terminal `result.result`
   - `session_id.txt` is parsed from terminal `result.session_id`
6. Update failure behavior:
   - missing `agent` CLI
   - unresolved model id
   - child exits non-zero
   - no terminal `result` event
   - empty `result`
   - missing status/verdict footer
7. Update README skill descriptions if the live runtime support claim changes
   from Claude/Codex to Claude/Codex/Agent.
8. Run `npx skills check` after changing files under `skills/`.

## Recommended Decision

Add `agent` support to these three skills, but do it as a real third runtime,
not as a thin alias to `codex` or `claude`.

The clean v1 should support:

- `fresh-consult`: read-only Cursor Agent consults with `--mode ask` or
  `--mode plan`, stream-json, and parsed final result
- `agent-delegate`: editful Cursor Agent workers with `--force`,
  `--sandbox disabled`, explicit workspace, stream-json, and explicit
  `--resume <session_id>`
- `model-consensus`: Cursor Agent as one or both resumable participants

Do not include in v1:

- Cursor `--worktree`
- `--continue` or latest-session resume
- automatic MCP approval
- assumptions about nested AGENTS.md handling
- schema-enforced final answers

Before shipping the skill changes, run one editful throwaway-repo test for
`agent-delegate` to confirm `--force --sandbox disabled` writes files and emits
tool-call events as expected. The read-only smoke tests above prove scripting,
JSON, stdin, and explicit resume, but they do not prove edit semantics.
