#!/usr/bin/env bash
# cf_share.sh - upload local files/dirs to the team Cloudflare R2 share bucket
# and print a public share URL. Also deletes a share by slug.
#
# usage:
#   cf_share.sh [--slug SLUG] [--entry NAME] <file-or-dir> [more paths...]
#   cf_share.sh --delete SLUG
#
# Secrets are read from $CF_SHARE_ENV (default ~/.config/cf-share/env):
#   CF_SHARE_API_TOKEN   Cloudflare API token with Workers R2 Storage: Edit
#   CF_SHARE_ACCOUNT_ID  Cloudflare account id
#   CF_SHARE_BUCKET      R2 bucket name (fc-share)
#   CF_SHARE_BASE_URL    public base URL (https://share.fun.country)
#
# Known gotchas handled here (do not "simplify" them away):
#   - curl sends "Expect: 100-continue" for bodies >1KB; api.cloudflare.com
#     resets those connections (exit 56). We always send "Expect:".
#   - R2 serves the Content-Type set at upload; without it everything becomes
#     application/octet-stream and HTML downloads instead of rendering.
#   - The REST object endpoint caps a single object around 300 MB.
set -euo pipefail

ENV_FILE="${CF_SHARE_ENV:-$HOME/.config/cf-share/env}"
MAX_BYTES=$((250 * 1024 * 1024))
API="https://api.cloudflare.com/client/v4"

die() { echo "cf-share error: $*" >&2; exit 1; }

usage() {
  sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

[ $# -ge 1 ] || usage 1

[ -f "$ENV_FILE" ] || die "missing secret file $ENV_FILE
Set it up per the cf-share skill references/setup.md (token with Workers R2 Storage: Edit)."
# shellcheck disable=SC1090
source "$ENV_FILE"
for v in CF_SHARE_API_TOKEN CF_SHARE_ACCOUNT_ID CF_SHARE_BUCKET CF_SHARE_BASE_URL; do
  [ -n "${!v:-}" ] || die "$v is not set in $ENV_FILE"
done

OBJ_BASE="$API/accounts/$CF_SHARE_ACCOUNT_ID/r2/buckets/$CF_SHARE_BUCKET/objects"
AUTH=(-H "Authorization: Bearer $CF_SHARE_API_TOKEN")

urlencode_path() { # percent-encode each path segment, keep the slashes
  python3 -c 'import sys, urllib.parse; print("/".join(urllib.parse.quote(s, safe="") for s in sys.argv[1].split("/")))' "$1"
}

content_type() {
  local f="$1" ext
  ext="${f##*.}"; ext="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"
  case "$ext" in
    html|htm) echo "text/html; charset=utf-8" ;;
    css)      echo "text/css; charset=utf-8" ;;
    js|mjs)   echo "text/javascript; charset=utf-8" ;;
    json|map) echo "application/json; charset=utf-8" ;;
    txt|log)  echo "text/plain; charset=utf-8" ;;
    md)       echo "text/markdown; charset=utf-8" ;;
    csv)      echo "text/csv; charset=utf-8" ;;
    xml)      echo "application/xml" ;;
    pdf)      echo "application/pdf" ;;
    png)      echo "image/png" ;;
    jpg|jpeg) echo "image/jpeg" ;;
    gif)      echo "image/gif" ;;
    svg)      echo "image/svg+xml" ;;
    webp)     echo "image/webp" ;;
    ico)      echo "image/x-icon" ;;
    mp4)      echo "video/mp4" ;;
    webm)     echo "video/webm" ;;
    mov)      echo "video/quicktime" ;;
    mp3)      echo "audio/mpeg" ;;
    wav)      echo "audio/wav" ;;
    woff)     echo "font/woff" ;;
    woff2)    echo "font/woff2" ;;
    ttf)      echo "font/ttf" ;;
    wasm)     echo "application/wasm" ;;
    zip)      echo "application/zip" ;;
    gz|tgz)   echo "application/gzip" ;;
    *)        file -b --mime-type "$f" 2>/dev/null || echo "application/octet-stream" ;;
  esac
}

delete_slug() {
  local slug="$1" keys deleted=0
  keys=$(curl -sS "${AUTH[@]}" "$OBJ_BASE?prefix=$(urlencode_path "$slug/")&per_page=1000" \
    | python3 -c 'import sys, json; [print(o["key"]) for o in json.load(sys.stdin).get("result", [])]')
  [ -n "$keys" ] || die "no objects found under slug '$slug'"
  while IFS= read -r key; do
    curl -sS -X DELETE "${AUTH[@]}" -o /dev/null "$OBJ_BASE/$(urlencode_path "$key")"
    deleted=$((deleted + 1))
  done <<< "$keys"
  echo "deleted $deleted object(s) under $CF_SHARE_BASE_URL/$slug/"
}

SLUG=""
ENTRY=""
PATHS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --slug)   SLUG="$2"; shift 2 ;;
    --entry)  ENTRY="$2"; shift 2 ;;
    --delete) [ -n "${2:-}" ] || die "--delete needs a slug"; delete_slug "$2"; exit 0 ;;
    -h|--help) usage 0 ;;
    -*)       die "unknown flag $1" ;;
    *)        PATHS+=("$1"); shift ;;
  esac
done
[ ${#PATHS[@]} -ge 1 ] || die "nothing to upload"

[ -n "$SLUG" ] || SLUG="$(date +%Y%m%d)-$(openssl rand -hex 6)"

# Build "localfile<TAB>relative key" pairs. A directory arg contributes its
# contents relative to itself; a file arg contributes its basename. Dotfiles
# and .DS_Store are skipped.
PAIRS=()
for p in "${PATHS[@]}"; do
  if [ -d "$p" ]; then
    while IFS= read -r f; do
      PAIRS+=("$f"$'\t'"${f#"${p%/}"/}")
    done < <(find "${p%/}" -type f -not -path '*/.*' -not -name '.DS_Store' | sort)
  elif [ -f "$p" ]; then
    PAIRS+=("$p"$'\t'"$(basename "$p")")
  else
    die "no such file or directory: $p"
  fi
done
[ ${#PAIRS[@]} -ge 1 ] || die "no files found to upload"

uploaded=0
failed=0
URLS=()
for pair in "${PAIRS[@]}"; do
  f="${pair%%$'\t'*}"; rel="${pair#*$'\t'}"
  size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f")
  if [ "$size" -gt "$MAX_BYTES" ]; then
    echo "SKIP $rel ($((size / 1024 / 1024)) MB > 250 MB REST cap; use the R2 S3 API for this one)" >&2
    failed=$((failed + 1)); continue
  fi
  key="$SLUG/$rel"
  ct="$(content_type "$f")"
  ok=0
  for attempt in 1 2; do
    resp=$(curl -sS -X PUT "${AUTH[@]}" -H "Content-Type: $ct" -H "Expect:" \
      --data-binary @"$f" "$OBJ_BASE/$(urlencode_path "$key")" 2>&1) || { sleep 1; continue; }
    if printf '%s' "$resp" | grep -q '"success": *true'; then ok=1; break; fi
    sleep 1
  done
  if [ "$ok" = 1 ]; then
    uploaded=$((uploaded + 1)); URLS+=("$CF_SHARE_BASE_URL/$(urlencode_path "$key")")
  else
    failed=$((failed + 1)); echo "FAIL $rel: $(printf '%s' "$resp" | head -c 300)" >&2
  fi
done

[ "$uploaded" -ge 1 ] || die "all uploads failed"

# Pick the entry URL: --entry match, else index.html, else the only file,
# else the first (alphabetical) .html, else the first file.
entry_url=""
if [ -n "$ENTRY" ]; then
  for u in "${URLS[@]}"; do case "$u" in *"$ENTRY"*) entry_url="$u"; break ;; esac; done
  [ -n "$entry_url" ] || die "--entry '$ENTRY' did not match any uploaded file"
fi
if [ -z "$entry_url" ]; then
  for u in "${URLS[@]}"; do case "$u" in */index.html) entry_url="$u"; break ;; esac; done
fi
if [ -z "$entry_url" ]; then
  for u in "${URLS[@]}"; do case "$u" in *.html) entry_url="$u"; break ;; esac; done
fi
[ -n "$entry_url" ] || entry_url="${URLS[0]}"

status=$(curl -s -o /dev/null -w '%{http_code}' -I "$entry_url" || echo "000")

echo "URL: $entry_url"
if [ "$status" = "200" ]; then
  echo "shared $uploaded file(s) under $CF_SHARE_BASE_URL/$SLUG/ (verified HTTP 200)"
else
  echo "shared $uploaded file(s) under $CF_SHARE_BASE_URL/$SLUG/ (verify FAILED: HTTP $status)"
fi
if [ "$failed" -gt 0 ]; then
  echo "$failed file(s) failed; see stderr above"
fi
if [ "$uploaded" -gt 1 ] && [ "$uploaded" -le 6 ]; then
  for u in "${URLS[@]}"; do [ "$u" = "$entry_url" ] || echo "also: $u"; done
fi
echo "delete later with: cf_share.sh --delete $SLUG"
[ "$failed" -eq 0 ] && [ "$status" = "200" ]
