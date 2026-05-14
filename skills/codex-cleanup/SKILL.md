---
name: codex-cleanup
description: "Purge stale state under ~/.codex that is older than a week so parallel codex CLI/TUI sessions stop locking up on a bloated logs SQLite, an unrotated 4 GB+ TUI log, and months of dated session JSONL. Use when ~/.codex is multi-GB, when 12+ parallel codex instances stall on `database is locked`, when the WAL on logs_2.sqlite has grown past 100 MB, or when you want a routine weekly purge. Not for editing live config (auth.json, config.toml, version.json, installation_id, .codex-global-state.json), not for the codex git repo, not for cleaning unrelated caches outside ~/.codex."
metadata:
  short-description: "Weekly purge of stale ~/.codex state to relieve multi-instance contention"
---

# Codex Cleanup

Use this skill when the job is reclaiming disk and relieving SQLite/WAL contention under `~/.codex`, not authoring or auditing code.

The skill ships one bundled bash script. Default is dry-run; nothing is destructive without `--apply`. The script refuses to run if any `codex` process is alive.

## Install

```bash
git clone git@github.com:aelaguiz/arch_skill.git
cd arch_skill
make install
```

After install the script lives at `~/.agents/skills/codex-cleanup/scripts/codex-cleanup.sh` (and the Claude / Gemini mirrors).

## When to use

- `~/.codex` is multi-gigabyte and you don't know which subtree is the bloat.
- 12+ parallel codex sessions are stalling on `database is locked` or feel unusually slow.
- `~/.codex/log/codex-tui.log` has grown past a few hundred MB (no rotation exists upstream).
- `~/.codex/logs_2.sqlite` plus its `-wal` exceed ~200 MB combined.
- You want a routine weekly hygiene pass on a developer machine.

## When not to use

- The work is editing or rewriting codex config (`auth.json`, `config.toml`, `version.json`, `installation_id`, `.codex-global-state.json`). This skill never touches those.
- The bloat is in the codex git repo (`~/workspace/codex/codex-rs/target`, etc.) rather than `~/.codex`. Use ordinary cargo/git tooling.
- You want to retire stale repo documentation. Use `$arch-docs` instead.
- You want to audit an agent-definition file. Use `$agent-definition-auditor`.
- The stale data is on a CI runner or someone else's machine — this skill is local-only and assumes you own the codex install.

## Non-negotiables

- Refuse the run if `pgrep -f '(^|/)codex( |$)'` matches a live process. Print the PIDs and exit non-zero. No partial cleanup with codex alive — the SQLite vacuum and the TUI log truncate would race the live writers.
- Default is `--dry-run`. The user has to ask for `--apply` explicitly.
- Operate only inside `$CODEX_HOME` (default `~/.codex`), and only when the resolved path is inside `$HOME` and its basename is `.codex` or `codex`. No symlink traversal surprises.
- Never touch live state: `auth.json`, `.credentials.json`, `config.toml`, `version.json`, `installation_id`, `models_cache.json`, `hooks.json`, `RTK.md`, `AGENTS.md`, `memories/`, `plugins/`, `skills/`, `prompts/`, `vendor_imports/`, `ambient-suggestions/`, `mobile-sim/`, `shell_snapshots/` (it self-cleans), `.codex-global-state.json`, `.codex-global-state.json.bak`, `history.jsonl`, `session_index.jsonl`.
- SQL prune of `logs_2.sqlite` mirrors the runtime's own retention semantics in `codex-rs/state/src/runtime/logs.rs:288` (`delete_logs_before(cutoff_ts)`) so this skill stays consistent with upstream rather than inventing a parallel contract.
- Idempotent: re-running on a clean tree reports zero work and exits 0.

## First move

1. Ask the user to stop every codex session before running `--apply`. (Dry-run is safe regardless, but the live-process gate will refuse `--apply` anyway.)
2. Run the script in dry-run and read the report.
3. If the report looks right, re-run with `--apply`.

```bash
~/.agents/skills/codex-cleanup/scripts/codex-cleanup.sh --dry-run
~/.agents/skills/codex-cleanup/scripts/codex-cleanup.sh --apply
```

Optional flags: `--age-days N` (default 7), `--codex-home PATH` (default `${CODEX_HOME:-$HOME/.codex}`).

## Workflow

1. Live-process gate: `pgrep -f '(^|/)codex( |$)'` must return zero matching codex processes (after filtering the script's own PID).
2. Compute cutoff: `now - age_days` in unix seconds.
3. Snapshot before-sizes for the load-bearing paths.
4. File-mtime purges (delete files mtime >age_days, prune empty date dirs):
   - `sessions/**/rollout-*.jsonl`
   - `generated_images/*`
   - `cache/codex_apps_tools/*`
   - `.tmp/*`, `tmp/*`
   - `config.toml.bak.*`
   - `.codex-global-state.json.tmp-*` (Electron desktop-app temp leftovers)
5. SQLite content prune (only on `--apply`):
   - `logs_2.sqlite`: `DELETE FROM logs WHERE ts < cutoff` then `wal_checkpoint(TRUNCATE)` then `VACUUM`.
   - `state_5.sqlite`: `wal_checkpoint(TRUNCATE)` only — no row delete; this DB holds live thread/job state.
6. TUI log rotation (only on `--apply`): truncate `log/codex-tui.log` in place (preserves inode + 0600 perms) after saving the last 200 KB to `codex-tui.log.tail`.
7. Snapshot after-sizes and print the diff.

## Output expectations

A successful `--apply` run typically:

- Drops `logs_2.sqlite` from multi-GB to under 100 MB and the WAL to a few MB.
- Drops `state_5.sqlite-wal` to a few KB.
- Empties `codex-tui.log` (inode preserved; tail saved alongside).
- Removes thousands of dated rollout JSONL files older than `age_days`.
- Reports a per-target before/after table.

If sqlite returns `database is locked`, a stray codex process slipped past the gate. Stop it and re-run.

If `--apply` is invoked while codex is running, the script exits 1 with the offending PIDs printed. That is the contract — fix the live processes, do not bypass.

## Reference map

- `references/targets.md` — per-target rationale, sizes, and pointers into `codex-rs/` source for the upstream retention constants.
- `scripts/codex-cleanup.sh` — the deterministic implementation. Read it before running `--apply` if you want to verify the exact SQL and `find` predicates.
