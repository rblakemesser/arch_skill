#!/usr/bin/env bash
# codex-cleanup.sh — purge stale state under ~/.codex older than a week.
#
# Default is dry-run. Pass --apply to actually delete. The script refuses to
# touch anything if it sees a live `codex` process.
#
# See ../SKILL.md and ../references/targets.md for rationale.

set -euo pipefail

# -------- Defaults --------------------------------------------------------

AGE_DAYS=7
APPLY=0
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

# -------- CLI parsing -----------------------------------------------------

usage() {
  cat <<EOF
Usage: codex-cleanup.sh [--dry-run|--apply] [--age-days N] [--codex-home PATH]

Default: --dry-run, --age-days 7, --codex-home \$HOME/.codex.

The script refuses to do anything if any 'codex' process is running.
Always run it after stopping every codex session.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) APPLY=0; shift ;;
    --apply)   APPLY=1; shift ;;
    --age-days)
      [[ $# -ge 2 ]] || { echo "ERROR: --age-days needs a value" >&2; exit 2; }
      AGE_DAYS="$2"; shift 2 ;;
    --codex-home)
      [[ $# -ge 2 ]] || { echo "ERROR: --codex-home needs a value" >&2; exit 2; }
      CODEX_HOME="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR: unknown arg: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [[ "$AGE_DAYS" -lt 1 ]]; then
  echo "ERROR: --age-days must be a positive integer (got: $AGE_DAYS)" >&2
  exit 2
fi

# -------- Safety rails on $CODEX_HOME ------------------------------------

if [[ ! -d "$CODEX_HOME" ]]; then
  echo "ERROR: --codex-home is not a directory: $CODEX_HOME" >&2
  exit 2
fi

# Resolve to an absolute, symlink-free path so we can sanity-check it.
if command -v realpath >/dev/null 2>&1; then
  RESOLVED_HOME="$(realpath "$CODEX_HOME")"
else
  RESOLVED_HOME="$(cd "$CODEX_HOME" && pwd -P)"
fi

case "$(basename "$RESOLVED_HOME")" in
  .codex|codex) ;;
  *) echo "ERROR: refusing to operate on $RESOLVED_HOME (basename must be .codex or codex)" >&2; exit 2 ;;
esac

case "$RESOLVED_HOME" in
  "$HOME"/*) ;;
  *) echo "ERROR: refusing to operate outside \$HOME (resolved: $RESOLVED_HOME)" >&2; exit 2 ;;
esac

# -------- Live-process gate ----------------------------------------------

# Match codex CLI/TUI processes; tolerate paths and quoted invocations.
# Filter our own PID / parent / the script itself so we don't self-trip.
self_pid=$$
parent_pid=$PPID
if pids=$(pgrep -f '(^|/)codex( |$)' 2>/dev/null); then
  filtered=""
  while IFS= read -r pid; do
    [[ -z "$pid" ]] && continue
    if [[ "$pid" == "$self_pid" || "$pid" == "$parent_pid" ]]; then
      continue
    fi
    cmd=$(ps -o command= -p "$pid" 2>/dev/null || true)
    case "$cmd" in
      *codex-cleanup.sh*) continue ;;
    esac
    filtered+="${pid}|${cmd}"$'\n'
  done <<< "$pids"
  if [[ -n "$filtered" ]]; then
    echo "ERROR: codex processes are running. Stop them and re-run." >&2
    echo "       Matched processes (pid|cmd):" >&2
    printf '       %s\n' "${filtered%$'\n'}" | sed 's/|/  /' >&2
    exit 1
  fi
fi

# -------- Helpers --------------------------------------------------------

mode_label() { [[ "$APPLY" -eq 1 ]] && echo "APPLY" || echo "DRY-RUN"; }

# Print a consistent "would" / "did" prefix.
prefix() { [[ "$APPLY" -eq 1 ]] && printf 'DID  ' || printf 'WOULD'; }

# Human-readable size of one path. "-" if missing.
hsize() {
  local p="$1"
  if [[ -e "$p" ]]; then
    du -sh "$p" 2>/dev/null | awk '{print $1}'
  else
    echo "-"
  fi
}

bytes() {
  local p="$1"
  if [[ -e "$p" ]]; then
    if stat -f%z "$p" >/dev/null 2>&1; then
      stat -f%z "$p"   # macOS
    else
      stat -c%s "$p"   # GNU
    fi
  else
    echo 0
  fi
}

# Delete files matching a find expression older than AGE_DAYS, under a base
# dir. Reports the count and total bytes. Args: <base_dir> <find-name-pattern>
purge_old_files() {
  local base="$1" pattern="$2" label="$3"
  if [[ ! -d "$base" ]]; then
    echo "  $(prefix) skip   $label: $base (missing)"
    return 0
  fi
  local count_bytes
  count_bytes=$(
    find "$base" -type f -name "$pattern" -mtime +"$AGE_DAYS" -print0 2>/dev/null \
      | xargs -0 -I{} stat -f '%z' {} 2>/dev/null \
      | awk 'BEGIN{c=0;b=0} {c++; b+=$1} END{print c, b}'
  )
  local count="${count_bytes%% *}"
  local bytes_total="${count_bytes##* }"
  count=${count:-0}
  bytes_total=${bytes_total:-0}
  echo "  $(prefix) prune  $label: $count file(s), $bytes_total byte(s) older than $AGE_DAYS days under $base"
  if [[ "$APPLY" -eq 1 && "$count" -gt 0 ]]; then
    find "$base" -type f -name "$pattern" -mtime +"$AGE_DAYS" -delete
  fi
}

# Same but for a flat dir where every file qualifies.
purge_old_anyfile() {
  local base="$1" label="$2"
  purge_old_files "$base" '*' "$label"
}

# -------- Banner ---------------------------------------------------------

echo "codex-cleanup [$(mode_label)]  age_days=$AGE_DAYS  codex_home=$RESOLVED_HOME"

cutoff_ts=$(( $(date +%s) - AGE_DAYS * 86400 ))
cutoff_human=$(date -r "$cutoff_ts" '+%Y-%m-%d %H:%M:%S' 2>/dev/null \
              || date -d "@$cutoff_ts" '+%Y-%m-%d %H:%M:%S' 2>/dev/null \
              || echo "$cutoff_ts")
echo "cutoff: $cutoff_human (unix=$cutoff_ts)"

# Snapshot key sizes BEFORE.
echo
echo "Before:"
echo "  $(hsize "$RESOLVED_HOME") total $RESOLVED_HOME"
for p in \
  "$RESOLVED_HOME/logs_2.sqlite" \
  "$RESOLVED_HOME/logs_2.sqlite-wal" \
  "$RESOLVED_HOME/state_5.sqlite" \
  "$RESOLVED_HOME/state_5.sqlite-wal" \
  "$RESOLVED_HOME/log/codex-tui.log" \
  "$RESOLVED_HOME/sessions" \
  "$RESOLVED_HOME/cache/codex_apps_tools" \
  "$RESOLVED_HOME/generated_images"
do
  echo "  $(hsize "$p")  $p"
done

# -------- 1. File-mtime targets ------------------------------------------

echo
echo "File-mtime purges (>$AGE_DAYS days):"

# Sessions: rollout-*.jsonl under YYYY/MM/DD/.
purge_old_files "$RESOLVED_HOME/sessions" 'rollout-*.jsonl' 'sessions/rollout-*.jsonl'

# Generated images cache.
purge_old_anyfile "$RESOLVED_HOME/generated_images" 'generated_images/*'

# Apps/tools response cache.
purge_old_anyfile "$RESOLVED_HOME/cache/codex_apps_tools" 'cache/codex_apps_tools/*'

# Internal temp dirs.
purge_old_anyfile "$RESOLVED_HOME/.tmp" '.tmp/*'
purge_old_anyfile "$RESOLVED_HOME/tmp" 'tmp/*'

# Old config backups (`config.toml.bak.*`).
purge_old_files "$RESOLVED_HOME" 'config.toml.bak.*' 'config.toml.bak.*'

# Stale Electron-app atomic-write leftovers.
purge_old_files "$RESOLVED_HOME" '.codex-global-state.json.tmp-*' \
  '.codex-global-state.json.tmp-* (Electron desktop app temp files)'

# Prune emptied date dirs under sessions/.
if [[ -d "$RESOLVED_HOME/sessions" ]]; then
  empty_count=$(find "$RESOLVED_HOME/sessions" -type d -empty 2>/dev/null | wc -l | tr -d ' ')
  echo "  $(prefix) prune  empty session dirs: $empty_count"
  if [[ "$APPLY" -eq 1 && "$empty_count" -gt 0 ]]; then
    find "$RESOLVED_HOME/sessions" -depth -type d -empty -delete
  fi
fi

# -------- 2. SQLite content prune ----------------------------------------

echo
echo "SQLite maintenance:"

LOGS_DB="$RESOLVED_HOME/logs_2.sqlite"
STATE_DB="$RESOLVED_HOME/state_5.sqlite"

if [[ -f "$LOGS_DB" ]]; then
  if ! command -v sqlite3 >/dev/null 2>&1; then
    echo "  ERROR: sqlite3 not found on PATH; install it or skip SQLite maintenance" >&2
    exit 3
  fi
  pre_logs_bytes=$(bytes "$LOGS_DB")
  pre_logs_wal=$(bytes "${LOGS_DB}-wal")
  echo "  $(prefix) prune  $LOGS_DB: DELETE FROM logs WHERE ts < $cutoff_ts; checkpoint+vacuum"
  echo "         (logs.rs delete_logs_before semantics; cutoff ts is unix seconds)"
  if [[ "$APPLY" -eq 1 ]]; then
    sqlite3 "$LOGS_DB" "DELETE FROM logs WHERE ts < $cutoff_ts;"
    sqlite3 "$LOGS_DB" "PRAGMA wal_checkpoint(TRUNCATE);"
    sqlite3 "$LOGS_DB" "VACUUM;"
    post_logs_bytes=$(bytes "$LOGS_DB")
    post_logs_wal=$(bytes "${LOGS_DB}-wal")
    echo "         logs_2.sqlite: $pre_logs_bytes -> $post_logs_bytes bytes (WAL: $pre_logs_wal -> $post_logs_wal)"
  fi
else
  echo "  $(prefix) skip   $LOGS_DB: missing"
fi

if [[ -f "$STATE_DB" ]]; then
  pre_state_bytes=$(bytes "$STATE_DB")
  pre_state_wal=$(bytes "${STATE_DB}-wal")
  echo "  $(prefix) ckpt   $STATE_DB: PRAGMA wal_checkpoint(TRUNCATE) (no row delete)"
  if [[ "$APPLY" -eq 1 ]]; then
    sqlite3 "$STATE_DB" "PRAGMA wal_checkpoint(TRUNCATE);"
    post_state_bytes=$(bytes "$STATE_DB")
    post_state_wal=$(bytes "${STATE_DB}-wal")
    echo "         state_5.sqlite: $pre_state_bytes -> $post_state_bytes bytes (WAL: $pre_state_wal -> $post_state_wal)"
  fi
else
  echo "  $(prefix) skip   $STATE_DB: missing"
fi

# -------- 3. TUI log rotation --------------------------------------------

echo
echo "TUI log rotation:"

TUI_LOG="$RESOLVED_HOME/log/codex-tui.log"
if [[ -f "$TUI_LOG" ]]; then
  pre_tui_bytes=$(bytes "$TUI_LOG")
  echo "  $(prefix) rotate $TUI_LOG: keep last 200 KB as codex-tui.log.tail; truncate primary"
  if [[ "$APPLY" -eq 1 ]]; then
    # Save tail for forensic comfort. tail -c is portable on macOS bash.
    tail -c 204800 "$TUI_LOG" > "$TUI_LOG.tail" 2>/dev/null || true
    : > "$TUI_LOG"  # truncate in place; preserves inode and 0600 perms
    post_tui_bytes=$(bytes "$TUI_LOG")
    echo "         codex-tui.log: $pre_tui_bytes -> $post_tui_bytes bytes (tail saved to ${TUI_LOG}.tail)"
  fi
else
  echo "  $(prefix) skip   $TUI_LOG: missing"
fi

# -------- After snapshot --------------------------------------------------

echo
echo "After:"
echo "  $(hsize "$RESOLVED_HOME") total $RESOLVED_HOME"
for p in \
  "$RESOLVED_HOME/logs_2.sqlite" \
  "$RESOLVED_HOME/logs_2.sqlite-wal" \
  "$RESOLVED_HOME/state_5.sqlite" \
  "$RESOLVED_HOME/state_5.sqlite-wal" \
  "$RESOLVED_HOME/log/codex-tui.log" \
  "$RESOLVED_HOME/sessions" \
  "$RESOLVED_HOME/cache/codex_apps_tools" \
  "$RESOLVED_HOME/generated_images"
do
  echo "  $(hsize "$p")  $p"
done

echo
if [[ "$APPLY" -eq 1 ]]; then
  echo "Done. Next codex session will re-create WAL/SHM files normally."
else
  echo "Dry run only. Re-run with --apply to perform deletes."
fi
