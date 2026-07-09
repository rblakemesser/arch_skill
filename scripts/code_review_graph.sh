#!/usr/bin/env bash
set -u

action="${1:-session-start}"

if [ -n "${CRG_REPO_ROOT:-}" ]; then
  repo_root="$(git -C "$CRG_REPO_ROOT" rev-parse --show-toplevel 2>/dev/null || true)"
else
  repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
fi

if [ -z "$repo_root" ]; then
  exit 0
fi

script_dir="$(cd "$(dirname "$0")" && pwd -P)"
script_path="$script_dir/$(basename "$0")"
repo_script="$repo_root/scripts/code_review_graph.sh"
managed_file="${XDG_CONFIG_HOME:-$HOME/.config}/code-review-graph/managed-common-dirs"

repo_is_managed() {
  if [ -f "$repo_script" ]; then
    return 0
  fi

  if [ -f "$repo_root/.mcp.json" ]; then
    if command -v rg >/dev/null 2>&1; then
      rg -q '"code-review-graph"' "$repo_root/.mcp.json" && return 0
    elif grep -q '"code-review-graph"' "$repo_root/.mcp.json"; then
      return 0
    fi
  fi

  [ -f "$managed_file" ] || return 1

  common_dir="$(git -C "$repo_root" rev-parse --git-common-dir 2>/dev/null || true)"
  [ -n "$common_dir" ] || return 1
  case "$common_dir" in
    /*) ;;
    *) common_dir="$repo_root/$common_dir" ;;
  esac
  common_dir="$(cd "$common_dir" 2>/dev/null && pwd -P || true)"
  [ -n "$common_dir" ] || return 1

  while IFS= read -r managed_dir; do
    case "$managed_dir" in
      ""|\#*) continue ;;
    esac
    if [ "$common_dir" = "$managed_dir" ]; then
      return 0
    fi
  done < "$managed_file"

  return 1
}

if [ "${CRG_MANAGED_ONLY:-0}" = "1" ]; then
  if [ -f "$repo_script" ] && [ "$script_path" != "$repo_script" ]; then
    exec bash "$repo_script" "$@"
  fi
  repo_is_managed || exit 0
fi

graph_dir="${CRG_DATA_DIR:-$repo_root/.code-review-graph}"
database="$graph_dir/graph.db"
marker="$graph_dir/.baseline-v1.complete"
lock_dir="$graph_dir/.lifecycle.lock"
log_file="$graph_dir/lifecycle.log"
lock_held=0
backup_active=0

repo_args=(--repo "$repo_root")
if [ -n "${CRG_DATA_DIR:-}" ]; then
  repo_args+=(--data-dir "$CRG_DATA_DIR")
fi

has_cli() {
  command -v code-review-graph >/dev/null 2>&1
}

baseline_ready() {
  [ -f "$database" ] && [ -f "$marker" ]
}

status_output() {
  code-review-graph status "${repo_args[@]}"
}

status_file_count() {
  output="$(status_output 2>/dev/null)" || return 1
  count="$(printf '%s\n' "$output" | awk '/^Files:/{print $2}' | tr -d ',')"
  case "$count" in
    ""|*[!0-9]*) return 1 ;;
  esac
  [ "$count" -gt 0 ] || return 1
  printf '%s\n' "$count"
}

write_marker() {
  files="$1"
  version="$(code-review-graph --version 2>/dev/null || printf 'unknown')"
  marker_tmp="$marker.tmp.$$"
  {
    printf 'repo=%s\n' "$repo_root"
    printf 'files=%s\n' "$files"
    printf 'built_at=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'tool=%s\n' "$version"
  } > "$marker_tmp"
  mv "$marker_tmp" "$marker"
}

release_lock() {
  if [ "$lock_held" = "1" ]; then
    rm -f "$lock_dir/pid"
    rmdir "$lock_dir" 2>/dev/null || true
    lock_held=0
  fi
}

acquire_lock() {
  mkdir -p "$graph_dir"

  if mkdir "$lock_dir" 2>/dev/null; then
    printf '%s\n' "$$" > "$lock_dir/pid"
    lock_held=1
    return 0
  fi

  old_pid="$(cat "$lock_dir/pid" 2>/dev/null || true)"
  case "$old_pid" in
    ""|*[!0-9]*) old_pid="" ;;
  esac
  if [ -n "$old_pid" ] && kill -0 "$old_pid" 2>/dev/null; then
    return 1
  fi

  rm -f "$lock_dir/pid"
  rmdir "$lock_dir" 2>/dev/null || return 1
  mkdir "$lock_dir" 2>/dev/null || return 1
  printf '%s\n' "$$" > "$lock_dir/pid"
  lock_held=1
}

cleanup() {
  if [ "$backup_active" = "1" ] && [ -d "$backup_dir" ]; then
    restore_graph_state
  fi
  release_lock
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

backup_graph_state() {
  backup_dir="$graph_dir/.rebuild-backup.$$"
  mkdir "$backup_dir" || return 1
  for state_file in "$database" "$database-wal" "$database-shm" "$marker"; do
    if [ -e "$state_file" ]; then
      mv "$state_file" "$backup_dir/$(basename "$state_file")" || return 1
    fi
  done
  backup_active=1
}

restore_graph_state() {
  for state_name in graph.db graph.db-wal graph.db-shm .baseline-v1.complete; do
    rm -f "$graph_dir/$state_name"
    if [ -e "$backup_dir/$state_name" ]; then
      mv "$backup_dir/$state_name" "$graph_dir/$state_name"
    fi
  done
  rmdir "$backup_dir" 2>/dev/null || true
  backup_active=0
}

discard_graph_backup() {
  for state_name in graph.db graph.db-wal graph.db-shm .baseline-v1.complete; do
    rm -f "$backup_dir/$state_name"
  done
  rmdir "$backup_dir" 2>/dev/null || true
  backup_active=0
}

run_full_build() {
  acquire_lock || {
    printf 'code-review-graph: another lifecycle operation is already running for %s\n' "$repo_root"
    return 0
  }

  if ! backup_graph_state; then
    printf 'code-review-graph: could not back up the existing graph for %s\n' "$repo_root" >&2
    if [ -n "${backup_dir:-}" ] && [ -d "$backup_dir" ]; then
      restore_graph_state
    fi
    return 1
  fi
  printf 'code-review-graph: building a complete baseline for %s\n' "$repo_root"
  if ! code-review-graph build "${repo_args[@]}"; then
    printf 'code-review-graph: baseline build failed for %s\n' "$repo_root" >&2
    restore_graph_state
    return 1
  fi

  files="$(status_file_count)" || {
    printf 'code-review-graph: build finished, but status did not report a usable graph for %s\n' "$repo_root" >&2
    restore_graph_state
    return 1
  }
  if ! write_marker "$files"; then
    printf 'code-review-graph: could not mark the completed baseline for %s\n' "$repo_root" >&2
    restore_graph_state
    return 1
  fi
  discard_graph_backup
  printf 'code-review-graph: baseline ready with %s files\n' "$files"
}

start_background_build() {
  mkdir -p "$graph_dir"
  if [ -f "$lock_dir/pid" ]; then
    active_pid="$(cat "$lock_dir/pid" 2>/dev/null || true)"
    case "$active_pid" in
      ""|*[!0-9]*) active_pid="" ;;
    esac
    if [ -n "$active_pid" ] && kill -0 "$active_pid" 2>/dev/null; then
      return 0
    fi
  fi

  printf 'code-review-graph: baseline is missing for %s, building it in the background\n' "$repo_root"
  CRG_REPO_ROOT="$repo_root" nohup bash "$script_path" ensure >>"$log_file" 2>&1 </dev/null &
}

run_update() {
  if ! baseline_ready; then
    start_background_build
    return 0
  fi

  acquire_lock || return 0
  {
    printf '\n[%s] incremental update for %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$repo_root"
    code-review-graph update --skip-flows "${repo_args[@]}"
  } >>"$log_file" 2>&1 || {
    printf 'code-review-graph: incremental update failed; see %s\n' "$log_file" >&2
    return 1
  }
}

run_pre_commit() {
  if ! baseline_ready; then
    start_background_build
    return 0
  fi

  run_update || return 0
  code-review-graph detect-changes --brief "${repo_args[@]}" >>"$log_file" 2>&1 || true
}

case "$action" in
  ensure)
    if ! has_cli; then
      printf 'code-review-graph: CLI not installed\n' >&2
      exit 1
    fi
    if baseline_ready && status_output; then
      exit 0
    fi
    rm -f "$marker"
    run_full_build
    ;;
  rebuild)
    if ! has_cli; then
      printf 'code-review-graph: CLI not installed\n' >&2
      exit 1
    fi
    run_full_build
    ;;
  adopt)
    if ! has_cli; then
      printf 'code-review-graph: CLI not installed\n' >&2
      exit 1
    fi
    minimum="${2:-1}"
    case "$minimum" in
      ""|*[!0-9]*)
        printf 'usage: %s adopt [minimum-file-count]\n' "$0" >&2
        exit 2
        ;;
    esac
    mkdir -p "$graph_dir"
    files="$(status_file_count)" || {
      printf 'code-review-graph: no usable graph to adopt for %s\n' "$repo_root" >&2
      exit 1
    }
    if [ "$files" -lt "$minimum" ]; then
      printf 'code-review-graph: refusing to adopt %s files; minimum is %s\n' "$files" "$minimum" >&2
      exit 1
    fi
    write_marker "$files"
    printf 'code-review-graph: adopted existing baseline with %s files\n' "$files"
    ;;
  session-start)
    has_cli || exit 0
    if baseline_ready; then
      if status_output; then
        exit 0
      fi
      rm -f "$marker"
    fi
    start_background_build
    ;;
  enter-worktree)
    has_cli || exit 0
    baseline_ready || start_background_build
    ;;
  update)
    has_cli || exit 0
    run_update || true
    ;;
  pre-commit)
    has_cli || exit 0
    run_pre_commit || true
    ;;
  status)
    has_cli || {
      printf 'code-review-graph: CLI not installed\n' >&2
      exit 1
    }
    status_output
    ;;
  *)
    printf 'usage: %s {ensure|rebuild|adopt|session-start|enter-worktree|update|pre-commit|status}\n' "$0" >&2
    exit 2
    ;;
esac
