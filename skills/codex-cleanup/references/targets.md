# Cleanup Targets

Each row says: what it is, why it grows, why it is safe to purge past the age cutoff, and where the runtime's own contract for it lives in the codex source. Sizes are typical observations on a heavy-use developer machine; treat them as orders of magnitude.

## Purged: file mtime older than `age_days`

| Path                                         | Typical size       | Why it grows                                                                 | Why safe past cutoff                                                                                  |
|----------------------------------------------|--------------------|------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `sessions/YYYY/MM/DD/rollout-*.jsonl`        | 14 GB / thousands  | One rollout JSONL per codex session, dated, never auto-deleted               | Threads are looked up via the state DB, not by reading old rollout files; old JSONL are cold history. |
| `generated_images/*`                         | tens of MB         | Image-generation cache from app/tool calls                                   | Pure cache; no back-references.                                                                       |
| `cache/codex_apps_tools/*`                   | low MB             | Tool response cache (hash-named JSON)                                        | Pure cache; misses are cheap.                                                                         |
| `.tmp/*` and `tmp/*`                         | low MB             | Plugin staging, bundled-marketplace exports, ephemeral arg0 dirs             | These dirs are scratch space; nothing reads aged entries.                                             |
| `config.toml.bak.*`                          | low KB             | Backups left behind by config migrations                                     | Old enough to predate the current config; keep only the current `config.toml`.                       |
| `.codex-global-state.json.tmp-*`             | KB                 | Atomic-write leftovers from the Electron desktop app's `write_atomically`    | Stale temp files from interrupted writes; no live process owns them once mtime is past cutoff.       |

Empty `sessions/YYYY/MM/DD/` directories are pruned after the file pass.

## Purged: SQL row age (only on `--apply`)

| DB                                  | Typical size      | Operation                                                                  | Why safe                                                                                                                                  |
|-------------------------------------|-------------------|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `logs_2.sqlite` + `-wal`            | 2.4 GB + 133 MB   | `DELETE FROM logs WHERE ts < cutoff_ts; PRAGMA wal_checkpoint(TRUNCATE); VACUUM;` | Mirrors `delete_logs_before(cutoff_ts)` in `codex-rs/state/src/runtime/logs.rs:288`. The `ts` column is unix seconds. The runtime's own startup maintenance applies a 10-day retention via `LOG_RETENTION_DAYS` (`logs.rs:3`); this skill applies a tighter user-chosen cutoff. The `PRAGMA wal_checkpoint(PASSIVE)` upstream (`logs.rs:306`) cannot truncate when other instances hold readers, which is the WAL bloat root cause; we use `TRUNCATE` because the live-process gate guarantees no other holders. |

## Truncate WAL only (no row delete)

| DB                                  | Typical size      | Operation                                  | Why safe                                                                                                                                                                                  |
|-------------------------------------|-------------------|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `state_5.sqlite` + `-wal`           | 269 MB + 4 MB     | `PRAGMA wal_checkpoint(TRUNCATE);`         | This DB holds live thread/job state. Aged rows are still relevant data; only the WAL is bloat. With no other writers, `TRUNCATE` cleanly reclaims it.                                    |

## Rotated in place (only on `--apply`)

| Path                                   | Typical size | Operation                                                                              | Why safe                                                                                                                                                                                                                                |
|----------------------------------------|--------------|----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `log/codex-tui.log`                    | 4.7 GB       | `tail -c 204800 > codex-tui.log.tail; : > codex-tui.log` (truncate; preserve inode/perms) | The TUI opens this with `OpenOptions::new().create(true).append(true)` at `codex-rs/tui/src/lib.rs:961-980` with mode `0o600` and never rotates. With no codex running, in-place truncate is the only no-deps way to reclaim it.       |

## Never touched

`auth.json`, `.credentials.json`, `config.toml`, `version.json`, `installation_id`, `models_cache.json`, `hooks.json`, `RTK.md`, `AGENTS.md`, `memories/`, `plugins/`, `skills/`, `prompts/`, `vendor_imports/`, `ambient-suggestions/`, `mobile-sim/`, `shell_snapshots/` (already self-cleans via `cleanup_stale_snapshots()` in `codex-rs/core/src/shell_snapshot.rs:500`), `.codex-global-state.json`, `.codex-global-state.json.bak`, `history.jsonl` (cross-process advisory lock; runtime owns its own soft cap), `session_index.jsonl` (append-only journal whose readers may scan back).

## Upstream constants worth knowing

- `LOG_RETENTION_DAYS = 10` — `codex-rs/state/src/runtime/logs.rs:3`
- `LOG_PARTITION_SIZE_LIMIT_BYTES = 10 MiB`, `LOG_PARTITION_ROW_LIMIT = 1000` — `codex-rs/state/src/runtime.rs:79-80`
- `SNAPSHOT_RETENTION = 3 days` (shell snapshots) — `codex-rs/core/src/shell_snapshot.rs:34`
- `busy_timeout = 5s`, `journal_mode = WAL`, `synchronous = Normal` — `codex-rs/state/src/runtime.rs:160-167`
- Startup `PRAGMA wal_checkpoint(PASSIVE)` — `codex-rs/state/src/runtime/logs.rs:306`

The PASSIVE checkpoint is the reason 12+ parallel instances accumulate a multi-hundred-MB WAL: PASSIVE skips frames held by active readers, so when there's always another reader, the WAL never collapses. Truncating it while no codex is alive is the supported workaround.
