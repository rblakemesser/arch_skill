# Agent History Storage Map

This is the runtime storage reference for `agent-history`. Treat every path as
private: prompts, tool arguments, command output, file contents, images, and
summaries can all contain sensitive data.

## Codex

### Primary Stores

- `~/.codex/sessions/YYYY/MM/DD/rollout-YYYY-MM-DDThh-mm-ss-<thread_id>.jsonl`
  is the main local transcript.
- `~/.codex/archived_sessions/...` is the archive root for the same rollout
  shape when present.
- `~/.codex/state_5.sqlite` stores thread metadata and goal state.
- `~/.codex/history.jsonl` stores global submitted-prompt recall. It is not a
  full transcript.
- `~/.codex/session_index.jsonl` stores an append-only thread-name index.
- `~/.codex/logs_2.sqlite` stores structured tracing logs.
- `~/.codex/log/codex-tui.log` stores plain-text tracing logs.

Adjacent stores:

- `~/.codex/shell_snapshots/`
- `~/.codex/generated_images/`
- `~/.codex/memories/`
- rollout trace bundles under `CODEX_ROLLOUT_TRACE_ROOT` when enabled
- `~/.codex/external_agent_session_imports.json` when external sessions were
  imported

### Rollout JSONL

Each line is one JSON object. Empty or invalid lines should not kill the whole
scan.

Common `type` values:

- `session_meta`: session id, cwd, source, model/provider, git metadata, agent
  role, and related header data.
- `response_item`: model-visible conversation items such as user/assistant
  messages, reasoning summaries, shell calls, function calls, tool outputs,
  web search, image generation, and compaction.
- `event_msg`: selected UI/protocol events. Not every event is persisted.
- `turn_context`: cwd, date, timezone, model, sandbox, approval policy, user
  instructions, developer instructions, and other turn settings.
- `compacted`: compaction marker and replacement history.

Persistence limit: `ThreadGoalUpdated` exists as a live event but is normally
excluded from rollout persistence. High-volume deltas, begin events, approval
prompts, and many status events are also not normally persisted.

### `history.jsonl`

Typical line:

```json
{"session_id":"<thread_uuid>","ts":1777700000,"text":"<submitted prompt>"}
```

Older records may use `conversation_id`. Treat either as the thread id.

### `state_5.sqlite`

Important tables:

- `threads`: id, rollout path, cwd, title, timestamps, model, git metadata,
  first user message, archived state, agent role, and related metadata.
- `thread_goals`: current goal objective/status/budget/usage for a thread.
- `thread_spawn_edges`: parent/child thread relationships.
- `stage1_outputs`: derived memory summaries tied to thread ids.
- `thread_dynamic_tools`: dynamic tool definitions attached to a thread.

`thread_goals` columns:

- `thread_id`
- `goal_id`
- `objective`
- `status`
- `token_budget`
- `tokens_used`
- `time_used_seconds`
- `created_at_ms`
- `updated_at_ms`

### Codex Slash, TUI, And Goal Commands

Codex slash command text is not a durable first-class history stream.

- Normal user messages and `!` shell prompts go to `history.jsonl`.
- Recognized slash commands are staged for local TUI recall, not saved as a
  durable command journal.
- `/plan <prompt>` may submit `<prompt>` as user text after mode switching, so
  durable history may contain the prompt but not the literal slash command.

`/goal` behavior:

- `/goal <objective>` writes/replaces `thread_goals`.
- `/goal pause` and `/goal resume` update goal status.
- `/goal clear` deletes the goal row.
- Bare `/goal` opens or renders the goal state.

Limits:

- `thread_goals` stores current state, not an append-only command history.
- Cleared goals are not recoverable from `thread_goals`.
- Literal typed `/goal ...` usually is not in rollout JSONL or
  `history.jsonl`.
- `codex-tui.log`, `logs_2.sqlite`, and opt-in TUI session logs are
  best-effort command evidence.

Agent-set goals:

- Model-facing tools `create_goal` and `update_goal` persist as normal rollout
  function calls and outputs.

## Claude Code

### Primary Stores

- `~/.claude/projects/<project-key>/<session_id>.jsonl` is the main transcript
  store.
- `~/.claude/projects/<project-key>/<session_id>/subagents/agent-*.jsonl`
  stores subagent/sidechain transcripts.
- `~/.claude/history.jsonl` stores global submitted-prompt recall and slash
  command display text.

Adjacent stores:

- `~/.claude/paste-cache/`
- `~/.claude/file-history/`
- `~/.claude/shell-snapshots/`
- `~/.claude/tasks/`
- `~/.claude/plans/`
- `~/.claude/telemetry/`
- `~/.claude/commands/prompts/`

### Project JSONL

Each line is one event/message record. Top-level `type` is the discriminator.

Common record types:

- `user`: user message, tool result, or synthetic user-side event.
- `assistant`: assistant model message, text, thinking, or tool use.
- `queue-operation`: queued prompt operation; `content` can contain queued
  slash command text.
- `system`: operational/system event.
- `attachment`: non-message context such as file snippets, hooks, plans, or
  command output.
- `last-prompt`: latest prompt pointer.
- `custom-title`, `ai-title`, `agent-name`: title/name metadata.
- `file-history-snapshot`: pointer to `~/.claude/file-history`.
- `permission-mode`, `pr-link`: operational metadata.

Message content may be a string or a list of blocks. Observed block types:

- `text`
- `thinking`
- `tool_use`
- `tool_result`
- `image`

Use `cwd` fields inside records as project truth. The project directory name is
only a hint.

### `history.jsonl`

Typical line:

```json
{
  "display": "<display text>",
  "pastedContents": {},
  "project": "<project path or key>",
  "sessionId": "<session uuid>",
  "timestamp": 1777700000000
}
```

Lines whose `display` starts with `/` are slash-command submissions. If
`pastedContents` contains a `contentHash`, load the matching paste-cache file
when the pasted content matters.

### Claude Slash And Goal Commands

- Slash command displays are usually recoverable from
  `~/.claude/history.jsonl.display`.
- Queued slash commands can also appear in project JSONL
  `queue-operation.content`.
- User transcript records may contain post-command effects rather than the
  literal slash command.
- `~/.claude/commands/prompts/**/*.md` are command definitions, not history.
- No dedicated Claude goal store was observed. Treat a Claude `/goal` command,
  if present, as an ordinary slash command unless a custom workflow created its
  own state.

## Confidence Labels

- `exact`: directly stored user prompt, command text, message text, or tool
  call.
- `inferred`: durable state or transcript effect implies the event, but the
  literal command text is absent.
- `best_effort`: log-derived, pruned, partial, or operational evidence.
- `not_found_after_search`: searched the relevant stores and found no match;
  absence may still be limited by pruning, disabled persistence, or missing
  stores.
