# Codex and Claude Session Storage Catalog

Last reviewed: 2026-05-02.

This is a format and storage map for building a future session-search skill. It
does not define or implement that skill.

Scope:

- Codex source was reviewed at `~/workspace/codex`.
- Codex local state was sampled at `~/.codex`.
- Claude Code source was not available. Claude local state was inferred from
  `~/.claude` and cross-checked against Codex's external-agent session importer.

Privacy note: every primary transcript/log path below can contain prompts, tool
arguments, command output, file contents, screenshots, generated image paths,
and reasoning summaries. Treat all scraped data as private by default.

## Short Map

Codex primary stores:

- `~/.codex/sessions/YYYY/MM/DD/rollout-YYYY-MM-DDThh-mm-ss-<thread_id>.jsonl`
  is the canonical local full transcript.
- `~/.codex/archived_sessions/...` is the supported archive root for the same
  rollout files. It was not present on this machine.
- `~/.codex/state_5.sqlite` is the local thread metadata database.
- `~/.codex/logs_2.sqlite` is the structured tracing log database.
- `~/.codex/log/codex-tui.log` is the plain-text tracing log.
- `~/.codex/history.jsonl` is global submitted-prompt recall, not a transcript.
- `~/.codex/session_index.jsonl` is an append-only thread-name index.
- `~/.codex/shell_snapshots/`, `~/.codex/generated_images/`,
  `~/.codex/memories/`, and opt-in rollout trace bundles are adjacent stores
  that can explain transcript references.
- Codex slash/TUI command text is not a durable first-class history stream.
  For commands such as `/goal`, scrape durable effects first and use logs only
  as best-effort command evidence.

Claude primary stores:

- `~/.claude/projects/<project-key>/<session_id>.jsonl` is the main full
  transcript store.
- `~/.claude/projects/<project-key>/<session_id>/subagents/agent-*.jsonl`
  stores subagent/sidechain transcripts.
- `~/.claude/history.jsonl` is global submitted-prompt recall, not a full
  transcript.
- `~/.claude/paste-cache/`, `~/.claude/file-history/`,
  `~/.claude/shell-snapshots/`, `~/.claude/tasks/`, `~/.claude/plans/`, and
  `~/.claude/telemetry/` are adjacent stores that can be relevant when
  explaining what happened in a session.
- Claude slash command displays are often recoverable from
  `~/.claude/history.jsonl`; queued slash commands can also appear as
  `queue-operation` records in project JSONL.

Observed local counts on this machine:

- Codex: 3,325 rollout JSONL files, 10,449 history lines, 12 session-index
  lines, 1,583,445 structured log rows, 6,640,837 text log lines, 3,322
  `threads` rows, 49 shell snapshots, 10 generated images, 260 memory files.
- Claude: 3,263 project JSONL files, 900 subagent JSONL files, 3,414 global
  history lines, 7,263 file-history files, 122 paste-cache files, 43 shell
  snapshots, 683 task JSON files, 171 plan Markdown files.

## Codex Source Anchors

The important source files in `~/workspace/codex` are:

- `codex-rs/utils/home-dir/src/lib.rs`: `CODEX_HOME` resolution.
- `codex-rs/core/src/config/mod.rs`: `codex_home`, `sqlite_home`, `log_dir`,
  `history`, `ephemeral`, and `experimental_thread_store`.
- `codex-rs/rollout/src/recorder.rs`: local rollout writer/reader.
- `codex-rs/rollout/src/list.rs`: rollout discovery.
- `codex-rs/rollout/src/session_index.rs`: `session_index.jsonl`.
- `codex-rs/rollout/src/policy.rs`: which events get persisted.
- `codex-rs/protocol/src/protocol.rs`: `RolloutItem` and `EventMsg`.
- `codex-rs/protocol/src/models.rs`: `ResponseItem`.
- `codex-rs/core/src/message_history.rs`: `history.jsonl`.
- `codex-rs/state/src/lib.rs`, `runtime.rs`, `runtime/logs.rs`,
  `log_db.rs`: SQLite state and structured logs.
- `codex-rs/core/src/shell_snapshot.rs`: shell snapshot files.
- `codex-rs/core/src/stream_events_utils.rs`: generated image artifact paths.
- `codex-rs/rollout-trace/README.md` and `codex-rs/rollout-trace/src/*`:
  opt-in raw trace bundles.
- `codex-rs/external-agent-sessions/src/*`: Claude-like external session
  import detection and conversion.

## Codex Home And Config

Codex home:

- If `CODEX_HOME` is set and non-empty, Codex uses that existing directory.
- Otherwise Codex defaults to `~/.codex`.

SQLite home:

- `sqlite_home` in config wins.
- Else `CODEX_SQLITE_HOME` wins.
- Else SQLite files live in `codex_home`.

Logs:

- `log_dir` defaults to `$CODEX_HOME/log`.
- The TUI appends to `$log_dir/codex-tui.log`.

Persistence switches:

- `ephemeral = true` disables session persistence.
- `experimental_thread_store = "local"` is the default and means rollout JSONL
  plus SQLite metadata.
- `experimental_thread_store = { remote = { endpoint = ... } }` can make local
  rollout files incomplete or absent for remote threads.
- Debug builds also have an in-memory thread store.

## Codex Rollout JSONL

Path:

```text
~/.codex/sessions/YYYY/MM/DD/rollout-YYYY-MM-DDThh-mm-ss-<thread_id>.jsonl
~/.codex/archived_sessions/YYYY/MM/DD/rollout-YYYY-MM-DDThh-mm-ss-<thread_id>.jsonl
```

Filename details:

- The directory and filename timestamp is local time.
- The line timestamps inside the file are UTC/RFC3339 with milliseconds.
- The `<thread_id>` is the canonical session/thread id.

Every line is one JSON object:

```json
{
  "timestamp": "2026-05-02T12:56:12.345Z",
  "type": "session_meta | response_item | compacted | turn_context | event_msg",
  "payload": {}
}
```

Reader behavior:

- Empty lines are skipped.
- Invalid JSON lines are counted and skipped.
- The first `session_meta.id` is treated as canonical.
- Legacy `ghost_snapshot` rollout lines are skipped.
- Legacy `ghost_snapshot` entries inside compacted replacement history are
  stripped during load.

### `session_meta`

Purpose: the session header.

Common payload fields:

- `id`
- `forked_from_id`
- `timestamp`
- `cwd`
- `originator`
- `cli_version`
- `source`
- `agent_nickname`
- `agent_role` or legacy alias `agent_type`
- `agent_path`
- `model_provider`
- `base_instructions`
- `dynamic_tools`
- `memory_mode`
- `git`

The optional `git` object is collected asynchronously and can include:

- `commit_hash`
- `branch`
- `repository_url`

### `response_item`

Purpose: persisted model-visible conversation items.

The payload is `ResponseItem`, internally tagged with its own `type`.
Persisted variants include:

- `message`
- `reasoning`
- `local_shell_call`
- `function_call`
- `tool_search_call`
- `function_call_output`
- `tool_search_output`
- `custom_tool_call`
- `custom_tool_call_output`
- `web_search_call`
- `image_generation_call`
- `compaction`

`ResponseItem::Other` is not persisted.

Important nested shapes:

- `message`: `role`, `content`, optional `phase`; `id` is skipped on
  serialization.
- `reasoning`: `summary`, optional non-raw `content`, `encrypted_content`;
  `id` is skipped.
- Tool call/output records carry the tool call ids, tool names, arguments, and
  result payloads defined in `codex-rs/protocol/src/models.rs`.

### `turn_context`

Purpose: the model-visible environment and config snapshot for a turn.

Payload fields include:

- `turn_id`
- `trace_id`
- `cwd`
- `current_date`
- `timezone`
- `approval_policy`
- `sandbox_policy`
- `permission_profile`
- `network`
- `file_system_sandbox_policy`
- `model`
- `personality`
- `collaboration_mode`
- `realtime_active`
- `effort`
- `summary`
- `user_instructions`
- `developer_instructions`
- `final_output_json_schema`
- `truncation_policy`

This is important for search because the same user prompt can behave
differently under different working directories, sandbox settings, models, or
developer instructions.

### `compacted`

Purpose: records context compaction.

Payload fields:

- `message`
- `replacement_history`

`replacement_history` is a list of `ResponseItem` values that replaced older
history after compaction.

### `event_msg`

Purpose: UI/protocol events that Codex decides to persist.

Known `EventMsg` variants in source:

- `Error`
- `Warning`
- `GuardianWarning`
- `RealtimeConversationStarted`
- `RealtimeConversationRealtime`
- `RealtimeConversationClosed`
- `RealtimeConversationSdp`
- `ModelReroute`
- `ModelVerification`
- `ContextCompacted`
- `ThreadRolledBack`
- `TurnStarted`
- `TurnComplete`
- `TokenCount`
- `AgentMessage`
- `UserMessage`
- `AgentMessageDelta`
- `AgentReasoning`
- `AgentReasoningDelta`
- `AgentReasoningRawContent`
- `AgentReasoningRawContentDelta`
- `AgentReasoningSectionBreak`
- `SessionConfigured`
- `ThreadNameUpdated`
- `ThreadGoalUpdated`
- `McpStartupUpdate`
- `McpStartupComplete`
- `McpToolCallBegin`
- `McpToolCallEnd`
- `WebSearchBegin`
- `WebSearchEnd`
- `ImageGenerationBegin`
- `ImageGenerationEnd`
- `ExecCommandBegin`
- `ExecCommandOutputDelta`
- `TerminalInteraction`
- `ExecCommandEnd`
- `ViewImageToolCall`
- `ExecApprovalRequest`
- `RequestPermissions`
- `RequestUserInput`
- `DynamicToolCallRequest`
- `DynamicToolCallResponse`
- `ElicitationRequest`
- `ApplyPatchApprovalRequest`
- `GuardianAssessment`
- `DeprecationNotice`
- `BackgroundEvent`
- `UndoStarted`
- `UndoCompleted`
- `StreamError`
- `PatchApplyBegin`
- `PatchApplyUpdated`
- `PatchApplyEnd`
- `TurnDiff`
- `GetHistoryEntryResponse`
- `McpListToolsResponse`
- `ListSkillsResponse`
- `RealtimeConversationListVoicesResponse`
- `SkillsUpdateAvailable`
- `PlanUpdate`
- `TurnAborted`
- `ShutdownComplete`
- `EnteredReviewMode`
- `ExitedReviewMode`
- `RawResponseItem`
- `ItemStarted`
- `ItemCompleted`
- `HookStarted`
- `HookCompleted`
- `AgentMessageContentDelta`
- `PlanDelta`
- `ReasoningContentDelta`
- `ReasoningRawContentDelta`
- `CollabAgentSpawnBegin`
- `CollabAgentSpawnEnd`
- `CollabAgentInteractionBegin`
- `CollabAgentInteractionEnd`
- `CollabWaitingBegin`
- `CollabWaitingEnd`
- `CollabCloseBegin`
- `CollabCloseEnd`
- `CollabResumeBegin`
- `CollabResumeEnd`

`UserMessage` stores the visible user message, images, local images, and text
elements.

Not every variant above is persisted locally. Persistence is controlled by
`ThreadEventPersistenceMode`.

Limited mode persists:

- `UserMessage`
- `AgentMessage`
- `AgentReasoning`
- `AgentReasoningRawContent`
- `TokenCount`
- `ThreadNameUpdated`
- `ContextCompacted`
- `EnteredReviewMode`
- `ExitedReviewMode`
- `ThreadRolledBack`
- `UndoCompleted`
- `TurnAborted`
- `TurnStarted`
- `TurnComplete`
- `ImageGenerationEnd`
- `ItemCompleted` for plan items only

Extended mode adds:

- `Error`
- `GuardianAssessment`
- `WebSearchEnd`
- `ExecCommandEnd`
- `PatchApplyEnd`
- `McpToolCallEnd`
- `ViewImageToolCall`
- `CollabAgentSpawnEnd`
- `CollabAgentInteractionEnd`
- `CollabWaitingEnd`
- `CollabCloseEnd`
- `CollabResumeEnd`
- `DynamicToolCallRequest`
- `DynamicToolCallResponse`

Extended `ExecCommandEnd` is bounded before persistence:

- `stdout`, `stderr`, and formatted output are cleared.
- `aggregated_output` is capped at 10,000 bytes.

High-volume deltas, begin events, approval prompts, hook start/end events, and
most startup/status events are not normally persisted to rollout JSONL.

## Codex `history.jsonl`

Path:

```text
~/.codex/history.jsonl
```

Purpose: global prompt recall. It is useful for "what prompt did I run", but it
is not enough to reconstruct a session.

Current line shape:

```json
{
  "session_id": "<thread_uuid>",
  "ts": 1777700000,
  "text": "<submitted user prompt>"
}
```

Notes:

- Persistence is controlled by `[history] persistence = "save-all" | "none"`.
- Optional `max_bytes` can cap file size.
- The writer uses lock/retry behavior and 0600 permissions on Unix.
- Some older comments/types in the source mention `conversation_id`; scrapers
  should tolerate either `session_id` or `conversation_id`.

## Codex `session_index.jsonl`

Path:

```text
~/.codex/session_index.jsonl
```

Purpose: append-only thread-name index.

Line shape:

```json
{
  "id": "<thread_uuid>",
  "thread_name": "<name>",
  "updated_at": "<RFC3339 timestamp>"
}
```

Most recent entry wins for a given `id`.

## Codex `state_5.sqlite`

Path:

```text
~/.codex/state_5.sqlite
~/.codex/state_5.sqlite-shm
~/.codex/state_5.sqlite-wal
```

Purpose: local metadata/index database. It is usually the best first pass for
finding candidate sessions by `cwd`, title, timestamps, archived state, model,
or parent/child thread relationship.

Tables observed:

- `_sqlx_migrations`
- `threads`
- `thread_dynamic_tools`
- `thread_goals`
- `thread_spawn_edges`
- `stage1_outputs`
- `backfill_state`
- `jobs`
- `agent_jobs`
- `agent_job_items`
- `device_key_bindings`
- `remote_control_enrollments`

Important `threads` columns:

- `id`
- `rollout_path`
- `created_at`, `updated_at`
- `created_at_ms`, `updated_at_ms`
- `source`
- `model_provider`
- `cwd`
- `title`
- `sandbox_policy`
- `approval_mode`
- `tokens_used`
- `has_user_event`
- `archived`, `archived_at`
- `git_sha`, `git_branch`, `git_origin_url`
- `cli_version`
- `first_user_message`
- `agent_nickname`
- `agent_role`
- `memory_mode`
- `model`
- `reasoning_effort`
- `agent_path`

Important relationship tables:

- `thread_spawn_edges`: parent thread id to child/subagent thread id.
- `thread_goals`: goal objective/status/budget and token/time usage.
- `thread_dynamic_tools`: dynamic tool definitions attached to a thread.
- `stage1_outputs`: memory summaries derived from rollouts.
- `agent_jobs` and `agent_job_items`: batch/agent job metadata and assigned
  thread ids.

## Codex `logs_2.sqlite`

Path:

```text
~/.codex/logs_2.sqlite
~/.codex/logs_2.sqlite-shm
~/.codex/logs_2.sqlite-wal
```

Purpose: structured tracing logs. This is operational history, not clean
conversation history, but it can recover timings, tool-call context, failures,
and thread-bound trace events.

Schema:

```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts INTEGER NOT NULL,
    ts_nanos INTEGER NOT NULL,
    level TEXT NOT NULL,
    target TEXT NOT NULL,
    feedback_log_body TEXT,
    module_path TEXT,
    file TEXT,
    line INTEGER,
    thread_id TEXT,
    process_uuid TEXT,
    estimated_bytes INTEGER NOT NULL DEFAULT 0
);
```

Indexes:

- `idx_logs_ts`
- `idx_logs_thread_id`
- `idx_logs_thread_id_ts`
- `idx_logs_process_uuid_threadless_ts`

Pruning:

- Per-thread and threadless partitions are pruned by row count/estimated bytes.
- This means logs are useful but not necessarily complete forever.

## Codex `log/codex-tui.log`

Path:

```text
~/.codex/log/codex-tui.log
```

Purpose: plain-text tracing log.

Format:

```text
<RFC3339 timestamp> <LEVEL> <target or span>: <message and structured fields>
```

Observed examples include auth refresh messages, session spans with
`thread_id=...`, and serialized tool-call previews. This file can be very large
and can contain raw prompt/tool data.

The TUI opens this file append-only with 0600 permissions on Unix.

## Codex Shell Snapshots

Path:

```text
~/.codex/shell_snapshots/<thread_id>.<unix_epoch_nanos>.sh
~/.codex/shell_snapshots/<thread_id>.<unix_epoch_nanos>.ps1
~/.codex/shell_snapshots/<thread_id>.tmp-<unix_epoch_nanos>
```

Purpose: shell state replay scripts for active sessions.

Format:

- Shell script text.
- Starts after a `# Snapshot file` marker.
- Includes alias cleanup, functions, shell options, aliases, and exported
  environment variables.
- `PWD` and `OLDPWD` are excluded.

Retention:

- Snapshot cleanup removes files without matching rollouts or whose rollout has
  not been updated within 3 days.
- The active session id is exempt from cleanup.

Search relevance:

- These are not transcripts.
- They can explain why later shell commands had a specific environment.
- They can contain sensitive environment variables.

## Codex Generated Images

Path:

```text
~/.codex/generated_images/<session_id>/<call_id>.png
```

Purpose: image generation artifacts.

Path generation:

- `session_id` and `call_id` are sanitized to ASCII alphanumeric, hyphen, and
  underscore.
- Empty sanitized values become `generated_image`.

Search relevance:

- Rollouts can include `ImageGenerationEnd` events and image generation
  response items.
- The image bytes live here, not inline in the rollout.

## Codex Rollout Trace Bundles

This is opt-in and not under `~/.codex` by default.

Enablement:

```text
CODEX_ROLLOUT_TRACE_ROOT=<directory>
```

Bundle layout:

```text
<trace-root>/<bundle>/
  manifest.json
  trace.jsonl
  payloads/*.json
  state.json        # optional, from trace reduction
```

`manifest.json` fields:

- `schema_version`
- `trace_id`
- `rollout_id`
- `root_thread_id`
- `started_at_unix_ms`
- `raw_event_log`
- `payloads_dir`

`trace.jsonl` raw event fields:

- `schema_version`
- `seq`
- `wall_time_unix_ms`
- `rollout_id`
- `thread_id`
- `codex_turn_id`
- `payload`

Payload files:

- Stored under `payloads/<ordinal>.json`.
- Referenced as `raw_payload:<ordinal>`.

Search relevance:

- These bundles can be more complete than rollout JSONL.
- They can contain raw requests, raw responses, terminal output, tool
  inputs/outputs, and compaction data.
- They only exist when the environment variable was set.

## Codex External-Agent Import Ledger

Path if present:

```text
~/.codex/external_agent_session_imports.json
```

It was not present on this machine.

Purpose: tracks Claude-like external sessions imported into Codex.

Shape:

```json
{
  "records": [
    {
      "source_path": "/absolute/path/to/source.jsonl",
      "content_sha256": "<sha256>",
      "imported_thread_id": "<codex_thread_id>",
      "imported_at": 1777700000
    }
  ]
}
```

Codex detects external-agent sessions under:

```text
<external_agent_home>/projects/*/*.jsonl
```

The importer accepts source record types `user`, `assistant`, `custom-title`,
and `ai-title`, skips `isMeta` and `isSidechain` messages, and converts
tool-use/tool-result blocks into bounded text tags in a Codex rollout.

## Codex Memories And Derived Stores

Paths observed:

```text
~/.codex/memories/MEMORY.md
~/.codex/memories/memory_summary.md
~/.codex/memories/raw_memories.md
~/.codex/memories/rollout_summaries/*.md
```

The SQLite `stage1_outputs` table also stores memory summaries tied to thread
ids.

Search relevance:

- These are derived from prior sessions.
- They are not a full log source.
- They can help find old session topics quickly, then jump back to rollout ids.

## Codex Other Observed State

Session-adjacent:

- `~/.codex/.codex-global-state.json`: UI/app state with keys such as
  `pinned-thread-ids`, `queued-follow-ups`, workspace roots, window bounds, and
  project order.
- `~/.codex/ambient-suggestions/*/ambient-suggestions.json`: observed local
  suggestion cache, not part of the core transcript source map.
- `~/.codex/vendor_imports/`: cached imported/vendor skill material, not
  transcript history.

Not session history:

- `~/.codex/auth.json`, `.credentials.json`, `installation_id`.
- `~/.codex/config.toml`, `hooks.json`.
- `~/.codex/models_cache.json`, `version.json`.
- `~/.codex/prompts/`, `skills/`, `plugins/`, `templates/`, `cache/`.
- `~/.codex/mobile-sim/`.
- `~/.codex/sqlite/codex-dev.db`, which on this machine held automation/inbox
  tables rather than session transcript data.

## Codex Slash, TUI, And Goal Commands

Codex has two different concepts that are easy to mix up:

- Durable conversation history: `history.jsonl`, rollout JSONL, and SQLite.
- TUI local recall: the in-memory Up-arrow recall list inside the active TUI.

Slash commands use the second path first.

### Slash command text

When the TUI sees a recognized slash command, the composer stages the submitted
command text for local recall, then commits it after command dispatch. The
relevant source path is:

```text
~/workspace/codex/codex-rs/tui/src/bottom_pane/chat_composer.rs
~/workspace/codex/codex-rs/tui/src/chatwidget/slash_dispatch.rs
```

That staged slash-command history is not the same as
`~/.codex/history.jsonl`. It is local TUI recall state, not a durable file.

Normal user messages and `!` shell prompts go through `Op::AddToHistory`, which
writes `~/.codex/history.jsonl`. Plain slash command dispatch generally does
not. Some slash commands also submit a normal user turn after handling the mode
change. For example `/plan <prompt>` switches to Plan mode and submits
`<prompt>` as user text; the durable history gets the submitted prompt text, not
necessarily the literal `/plan <prompt>` command line.

### `/goal`

The `/goal` command is TUI control surface over persisted thread-goal state.

Observed command behavior from source:

- Bare `/goal`: emits `OpenThreadGoalMenu`, reads the current thread goal, and
  renders a goal summary in the TUI.
- `/goal <objective>`: emits `SetThreadGoalObjective` and writes/replaces the
  current goal objective.
- `/goal pause`: emits `SetThreadGoalStatus` with `paused`.
- `/goal resume`: emits `SetThreadGoalStatus` with `active`.
- `/goal clear`: emits `ClearThreadGoal` and deletes the current goal row.

Durable goal state lives here:

```text
~/.codex/state_5.sqlite
table: thread_goals
```

Important fields:

- `thread_id`
- `goal_id`
- `objective`
- `status`
- `token_budget`
- `tokens_used`
- `time_used_seconds`
- `created_at_ms`
- `updated_at_ms`

Join `thread_goals.thread_id` to `threads.id` for `cwd`, `title`,
`rollout_path`, timestamps, model, and git metadata.

Limits:

- `thread_goals` holds the current goal for a thread, not a full append-only
  goal-command history.
- `/goal clear` deletes the row, so cleared goals are not recoverable from
  `thread_goals`.
- `ThreadGoalUpdated` exists as a live event, but rollout persistence excludes
  it, so it is not normally saved in `rollout-*.jsonl`.
- The literal typed `/goal ...` command is not normally in `history.jsonl` or
  rollout JSONL.

Best-effort command evidence:

- `~/.codex/log/codex-tui.log`: search for goal/app-server diagnostics, but do
  not treat it as a complete command journal.
- `~/.codex/logs_2.sqlite`: search tracing rows by `thread_id`, `target`, and
  `feedback_log_body`; useful for errors and some operational clues.
- `CODEX_TUI_RECORD_SESSION=1`: when set before launching Codex, the TUI writes
  an opt-in JSONL session log. Default path is under `log_dir` as
  `session-YYYYMMDDThhmmssZ.jsonl`, or `CODEX_TUI_SESSION_LOG_PATH` if set.
  It records session start/end, selected app events, and outbound `AppCommand`
  payloads. Goal app events are logged by variant in this path, not as a
  complete typed `/goal <objective>` command journal, so still join to
  `thread_goals` for objective/status.

Agent-set goals:

- The model-facing tools are `create_goal` and `update_goal`.
- Those tool calls are normal persisted `ResponseItem::FunctionCall` and
  `FunctionCallOutput` records in rollout JSONL.
- To find goals set by the agent rather than by user `/goal`, search rollouts
  for tool calls named `create_goal` or `update_goal`, then join to
  `thread_goals` for current state.

### Other Codex TUI commands

Use three tiers:

1. Durable effects.
   Check the store changed by the command. Examples: `/rename` updates thread
   title metadata and `session_index.jsonl`; `/compact` creates compaction
   rollout records; `/review` starts a review turn; `/model`, `/fast`,
   `/permissions`, and similar settings commands may emit turn-context override
   ops or config changes.

2. Rollout records.
   If the command caused a normal user turn, inspect `event_msg.UserMessage`
   and `response_item.message`. If it only changed TUI/app state, rollout JSONL
   may contain nothing.

3. Logs.
   Use `codex-tui.log`, `logs_2.sqlite`, and opt-in TUI session logs as
   best-effort evidence. They can explain what the TUI did, but they are not a
   guaranteed complete command stream.

Scraper rule: for Codex commands, never assume command text exists. Build a
command-evidence object with:

- `source`: `history`, `rollout`, `state_db`, `text_log`, `structured_log`, or
  `tui_session_log`
- `confidence`: `exact`, `inferred`, or `best_effort`
- `thread_id`
- `timestamp`
- `cwd`
- `command_name`
- `typed_text` when exact
- `durable_effect` when inferred

## Claude Project Transcripts

Path:

```text
~/.claude/projects/<project-key>/<session_id>.jsonl
~/.claude/projects/<project-key>/<session_id>/subagents/agent-*.jsonl
```

Observed project-key behavior:

- Project directories are path-like keys, for example
  `-Users-aelaguiz-workspace-project`.
- Do not rely on reversing this key to a path. Use the `cwd` field inside JSONL
  records as the authority.

Line format:

- JSON Lines.
- Each line is one event/message record.
- `type` is the top-level record discriminator.

Common message record fields:

- `parentUuid`
- `isSidechain`
- `message`
- `requestId` for assistant records
- `promptId` for user/tool-result records
- `type`
- `uuid`
- `timestamp`
- `userType`
- `entrypoint`
- `cwd`
- `sessionId`
- `version`
- `gitBranch`
- `permissionMode` on some user records
- `sourceToolAssistantUUID` on tool-result user records
- `toolUseResult` on many tool-result user records
- `agentId` and `attributionAgent` in subagent files

Top-level record types observed across all local Claude project JSONL:

- `agent-name`: `agentName`, `sessionId`, `type`.
- `ai-title`: `aiTitle`, `sessionId`, `type`.
- `assistant`: assistant model message; has `message.content`.
- `attachment`: non-message context attachment.
- `custom-title`: `customTitle`, `sessionId`, `type`.
- `file-history-snapshot`: pointer metadata for `~/.claude/file-history`.
- `last-prompt`: `lastPrompt`, `leafUuid`, `sessionId`, `type`.
- `permission-mode`: `permissionMode`, `sessionId`, `type`.
- `pr-link`: `prNumber`, `prRepository`, `prUrl`, `sessionId`,
  `timestamp`, `type`.
- `queue-operation`: queued prompt operation; `operation`, optional `content`,
  `sessionId`, `timestamp`, `type`.
- `system`: operational/system event.
- `user`: user message, tool result, or synthetic user-side event.

Observed top-level record counts on this machine:

- `agent-name`: 5,617
- `ai-title`: 9,808
- `assistant`: 246,478
- `attachment`: 36,262
- `custom-title`: 7,584
- `file-history-snapshot`: 8,033
- `last-prompt`: 39,089
- `permission-mode`: 17,428
- `pr-link`: 366
- `queue-operation`: 8,739
- `system`: 8,185
- `user`: 171,853

## Claude Message Content Blocks

For `assistant` and some `user` records, `message.content` can be a string or
an array of content blocks.

Observed block types:

- `text`
- `thinking`
- `tool_use`
- `tool_result`
- `image`

Observed block shapes:

```json
{"type": "text", "text": "..."}
{"type": "thinking", "thinking": "...", "signature": "..."}
{"type": "tool_use", "id": "...", "name": "...", "input": {}, "caller": {}}
{"type": "tool_result", "tool_use_id": "...", "content": "...", "is_error": false}
{"type": "image", "source": {}}
```

Observed block counts on this machine:

- `image`: 480
- `text`: 44,818
- `thinking`: 46,174
- `tool_result`: 159,310
- `tool_use`: 159,322

## Claude `toolUseResult`

Many `user` records that represent tool results also carry a top-level
`toolUseResult`.

Observed value types:

- object: 122,898
- string: 7,177
- array: 687

Common object keys:

- `stdout`
- `stderr`
- `interrupted`
- `isImage`
- `noOutputExpected`

Other observed object keys include tool-specific results for file edits,
search, tasks, agents, MCP, web fetches, command execution, plans, todos, and
background jobs. Important keys seen across the corpus include:

- `file`, `filePath`, `originalFile`, `structuredPatch`, `userModified`
- `oldString`, `newString`, `replaceAll`
- `stdout`, `stderr`, `interrupted`, `returnCodeInterpretation`
- `command`, `commandName`, `durationMs`, `timeoutMs`
- `task`, `taskId`, `task_type`
- `agentId`, `agentType`, `prompt`, `status`, `usage`
- `content`, `results`, `retrieval_status`, `query`
- `newTodos`, `oldTodos`
- `plan`, `planContent`, `planFilePath`, `planWasEdited`
- `persistent`, `durable`, `backgroundTaskId`
- `pending_mcp_servers`, `authUrl`

Array `toolUseResult` values were observed as arrays of blocks such as
`{"type":"text","text":"..."}`.

## Claude System And Operational Records

Observed `system.subtype` values:

- `api_error`
- `away_summary`
- `compact_boundary`
- `informational`
- `local_command`
- `scheduled_task_fire`
- `stop_hook_summary`
- `turn_duration`

Observed `queue-operation.operation` values:

- `enqueue`
- `dequeue`
- `remove`
- `popAll`

Observed permission modes:

- `acceptEdits`
- `auto`
- `bypassPermissions`
- `default`
- `plan`

Subagents:

- Nested subagent files use the same JSONL format.
- Their records commonly set `isSidechain: true`.
- They add `agentId`.
- Assistant records can add `attributionAgent`.

Search relevance:

- Include or exclude `isSidechain` deliberately.
- For a "main conversation only" answer, skip sidechains.
- For "what did delegated agents do", include sidechains and group by
  `agentId`.

## Claude Attachments

`attachment` records carry non-message context. Observed attachment key
families include:

- file or diff names: `addedNames`, `removedNames`, `addedLines`,
  `addedBlocks`
- skill context: `content`, `skillCount`, `isInitial`, `skills`, `skillNames`,
  `skillDir`
- hooks: `hookEvent`, `hookName`, `toolUseID`
- reminders: `reminderType`
- plans: `planContent`, `planFilePath`, `planExists`
- command output: `stdout`, `stderr`, `exitCode`, `durationMs`, `command`
- file snippets and paths: `path`, `displayPath`, `filename`, `snippet`

Attachments can be important when a user prompt says "this file" or "the pasted
thing" without putting the content directly in `message.content`.

## Claude `history.jsonl`

Path:

```text
~/.claude/history.jsonl
```

Purpose: global submitted-prompt recall.

Observed line shape:

```json
{
  "display": "<display text>",
  "pastedContents": {},
  "project": "<project path or key>",
  "sessionId": "<session uuid>",
  "timestamp": 1777700000000
}
```

`pastedContents` shape:

```json
{
  "1": {
    "id": 1,
    "type": "...",
    "contentHash": "..."
  }
}
```

Some entries store `content` directly instead of `contentHash`.

Search relevance:

- Good for prompt recall.
- Join to project JSONL by `sessionId`.
- If `pastedContents` has `contentHash`, load the matching text from
  `~/.claude/paste-cache`.

## Claude Slash Commands

Claude slash command recovery is better than Codex for the typed command line,
because `~/.claude/history.jsonl` stores a `display` string for submitted input.

Primary source:

```text
~/.claude/history.jsonl
```

Observed command-line evidence:

- Lines whose `display` starts with `/` are slash-command submissions.
- Join by `sessionId` to `~/.claude/projects/**/*.jsonl`.
- Use `project` as a hint, then confirm with `cwd` records in the project JSONL.
- `pastedContents` can point to `~/.claude/paste-cache/<hash>.txt` when the
  command included pasted content.

On this machine, 727 `history.jsonl` entries had `display` values starting with
`/`.

Secondary source:

```text
~/.claude/projects/<project-key>/<session_id>.jsonl
```

Observed command-line evidence:

- `queue-operation` records can carry slash-prefixed `content`.
- On this machine, 340 `queue-operation` records had `content` starting with
  `/`.
- User transcript records did not show direct string `message.content` values
  starting with `/` in the sampled corpus. Treat project `user` records as the
  post-command conversation/effect layer, not the primary typed-command layer.

Command definitions:

```text
~/.claude/commands/prompts/**/*.md
```

These define custom prompt commands. They are not history, but they help map a
stored command name such as `/arch-step` to the prompt body or workflow that ran
at that time. If definitions changed over time, pair command history with file
mtime or git/source control where available; the command history itself does
not snapshot the command definition.

No dedicated Claude goal store was observed. A Claude `/goal` command, if one
exists on a machine, should be treated as an ordinary slash command unless a
separate custom workflow creates its own state under `~/.claude` or the
workspace.

## Claude Paste Cache

Path:

```text
~/.claude/paste-cache/<hash>.txt
```

Purpose: raw pasted content referenced from `history.jsonl` and possibly
transcript records.

Format:

- UTF-8 text files.
- Filename stem is the content hash used in history metadata.

Search relevance:

- Needed for prompt reconstruction when the submitted prompt included large
  pasted content.
- Can contain arbitrary copied user data.

## Claude File History

Path:

```text
~/.claude/file-history/<session_id>/<file_hash>@v<version>
```

Purpose: raw file snapshots used by Claude's file-history tracking.

Format:

- Raw file contents, without a standard extension.
- Files can be source code, Markdown, text, or other edited content.

Transcript pointer record:

```json
{
  "type": "file-history-snapshot",
  "messageId": "<message uuid>",
  "isSnapshotUpdate": true,
  "snapshot": {
    "messageId": "<message uuid>",
    "timestamp": "<RFC3339 timestamp>",
    "trackedFileBackups": {
      "<file path or key>": {
        "backupFileName": "<file_hash>@vN or null>",
        "version": 1,
        "backupTime": "<RFC3339 timestamp>"
      }
    }
  }
}
```

Observed note:

- Some `trackedFileBackups` entries had `backupFileName: null`.
- Do not assume every pointer has a backing file.

Search relevance:

- This is the store for "what file content did Claude see before/after edits"
  style questions.
- It is not a conversational transcript by itself.

## Claude Shell Snapshots

Path:

```text
~/.claude/shell-snapshots/snapshot-<shell>-<unix_epoch_ms>-<nonce>.sh
```

Purpose: shell-state snapshot scripts.

Format:

- UTF-8 shell script text.
- Observed zsh snapshots.

Search relevance:

- Not a transcript.
- Can explain environment-sensitive command behavior.
- Can contain exported variables and should be treated as sensitive.

## Claude Tasks, Plans, Telemetry, And State

Tasks:

```text
~/.claude/tasks/<session_id>/<number>.json
```

Observed task JSON keys:

- `id`
- `subject`
- `description`
- `activeForm`
- `status`
- `blocks`
- `blockedBy`

Plans:

```text
~/.claude/plans/*.md
```

Observed as Markdown plan files. They are not full transcripts, but can capture
user-visible planning state or follow-up work.

Telemetry:

```text
~/.claude/telemetry/*.json
```

Observed telemetry JSON lines/array entries with:

- `event_type`
- `event_data`

This is operational/analytics failure data, not transcript history.

Reserved or light state:

- `~/.claude/session-env/`: present but empty on this machine.
- `~/.claude/sessions/`: present but empty on this machine.
- `~/.claude/state/`: present but no files found at the sampled depth.
- `~/.claude/ide/*.lock`: IDE integration lock files.

Config/cache, not transcript history:

- `~/.claude/settings.json`
- `~/.claude/settings.json.bak`
- `~/.claude/stats-cache.json`
- `~/.claude/mcp-needs-auth-cache.json`
- `~/.claude/cache/`
- `~/.claude/commands/`
- `~/.claude/plugins/`
- `~/.claude/skills/`
- `~/.claude/downloads/`
- `~/.claude/backups/`

## Search Strategy For The Future Skill

For "what prompt did I run here?"

Codex:

- Start with `state_5.sqlite.threads` where `cwd` matches the current repo.
- Join candidate `id` values to `~/.codex/history.jsonl` by `session_id`.
- For exact context, open each `rollout_path` and read `event_msg.UserMessage`
  plus `response_item.message` records with `role = "user"`.
- Use `turn_context` to disambiguate cwd/model/sandbox/personality changes.

Claude:

- Start with `~/.claude/projects/**/*.jsonl`.
- Filter records where `cwd` matches the current repo.
- Group by `sessionId`.
- Read `type = "user"` records where `message.content` is a string or text
  block.
- Join `~/.claude/history.jsonl` by `sessionId` for the display prompt and
  pasted content references.

For "where did I correct the agent?"

Use a heuristic pass over user-authored messages, then show surrounding turns.

Good candidate signals:

- "no"
- "not"
- "wrong"
- "actually"
- "I meant"
- "you missed"
- "do not"
- "don't"
- "instead"
- "that's not"
- "you should have"
- "stop"
- "read the instructions"
- "follow the"

Codex extraction:

- Prefer `event_msg` with payload type `user_message`.
- Also inspect `response_item.message` with `role = "user"` for model-visible
  user text.
- Show the previous assistant message/tool result and the next assistant
  response.
- Include `turn_id`, `thread_id`, `cwd`, timestamp, and rollout path.

Claude extraction:

- Prefer top-level `type = "user"` records.
- Exclude user records whose `message.content` is only `tool_result` unless the
  query explicitly asks about tool errors.
- Exclude or separately group `isSidechain = true`.
- Show previous assistant `text` or `tool_use`, the correction user record, and
  the next assistant record.
- Include `sessionId`, `uuid`, `parentUuid`, `cwd`, timestamp, and JSONL path.

For "what happened in this repo?"

- Codex: use `state_5.sqlite.threads.cwd` first, then rollouts.
- Claude: use `cwd` fields in project JSONL, not just project directory names.
- Add fallback text search over path names only after metadata filtering.

For "what command or tool produced this output?"

- Codex: use rollout `response_item.function_call`,
  `response_item.function_call_output`, `event_msg.ExecCommandEnd`, and
  `logs_2.sqlite` rows by `thread_id`.
- Claude: use assistant `tool_use` blocks and following user `tool_result`
  blocks, plus top-level `toolUseResult`.

For "find subagent/delegated work"

- Codex: use `state_5.sqlite.thread_spawn_edges` and collaboration
  `Collab*` events when persisted.
- Claude: include `projects/*/<session_id>/subagents/agent-*.jsonl`, records
  with `isSidechain = true`, and `agentId`.

For "find goal and TUI commands"

- Codex `/goal`: query `state_5.sqlite.thread_goals` for current goals and join
  to `threads`; inspect rollouts for agent tool calls named `create_goal` or
  `update_goal`; use logs only as best-effort evidence for literal TUI command
  text.
- Codex other slash/TUI commands: infer from durable effects first, then
  rollouts, then logs. Use `CODEX_TUI_RECORD_SESSION=1` on future runs if exact
  TUI replay evidence matters.
- Claude slash commands: start with `~/.claude/history.jsonl` entries whose
  `display` begins with `/`; add `queue-operation.content` records that begin
  with `/`; join both to project JSONL by `sessionId`.

## Parser Rules

Codex:

- Parse rollouts as line-oriented JSON.
- Do not fail the whole file on one bad line.
- Treat `session_meta.id` as canonical when present.
- Use `state_5.sqlite.threads.rollout_path` when available, but tolerate
  missing or moved files.
- Support `session_id` and legacy `conversation_id` in `history.jsonl`.
- Keep `event_msg` and `response_item` as separate evidence types; they overlap
  but are not identical.
- Treat slash/TUI commands as a separate evidence class from user turns.
- Treat `/goal` as durable state in `thread_goals`, not as prompt history.

Claude:

- Parse project histories as line-oriented JSON.
- Do not assume all `message.content` values are strings.
- Handle array content blocks.
- Treat `tool_result` user records as tool output, not user-authored
  corrections.
- Use `cwd` from records as the project truth.
- Handle title records (`custom-title`, `ai-title`) independently from user
  prompts.
- Include nested subagent JSONL only when sidechain/delegated work is relevant.
- Treat `history.jsonl.display` slash-prefixed entries as the main typed
  command source.
- Treat project `queue-operation.content` slash-prefixed records as queued
  command evidence.

Performance:

- Use SQLite metadata before scanning 11 GB of Codex rollouts.
- Use `rg`/streaming JSONL parsing for Claude project JSONL rather than loading
  all 2.7 GB into memory.
- Cache per-file summaries keyed by path, size, mtime, and maybe content hash.
- Store only derived search indexes unless the user asks to export raw logs.

## Remaining Unknowns

Codex:

- Remote thread-store behavior depends on the configured remote endpoint. Local
  files may not be authoritative in that mode.
- Rollout trace bundles are opt-in and can be located anywhere
  `CODEX_ROLLOUT_TRACE_ROOT` points.

Claude:

- Format was inferred from local data, not source.
- Some directories were present but empty on this machine, especially
  `~/.claude/sessions`, `~/.claude/session-env`, and `~/.claude/state`.
- Hook-managed custom state can add repo- or skill-specific files under
  `~/.claude`; those should be cataloged as plugin/custom state, not core
  Claude transcript format.
