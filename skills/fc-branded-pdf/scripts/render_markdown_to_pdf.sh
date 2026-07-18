#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  render_markdown_to_pdf.sh <input.md> [--out <output.pdf>] [--title <title>] [--theme <theme>]

Purpose:
  Render a Markdown artifact into an FC / Poker Skill branded PDF.

Implementation:
  - pandoc: Markdown -> standalone HTML
  - headless Chrome/Chromium: HTML -> PDF (print-to-pdf)

Themes:
  - Default theme is controlled by:
      1) CLI flag: --theme <theme>
      2) Env var:  FC_BRANDED_PDF_THEME
      3) Legacy fallback env vars: HERMES_PDF_THEME, then AGENTS_PDF_THEME
      4) Fallback: fc

  Supported themes:
  - fc / pokerskill (branded)
  - plain (legacy minimal)

Notes:
  - Designed to run on macOS and Linux hosts.
  - Fails loud if required binaries are missing.
  - Default output goes next to the source Markdown file unless you pass `--out`.

Examples:
  # Default output (same folder, same stem):
  render_markdown_to_pdf.sh "/abs/path/to/report.md"

  # Explicit output path:
  render_markdown_to_pdf.sh "/abs/path/to/report.md" \
    --out "/abs/path/to/report.pdf"

  # Force legacy theme:
  render_markdown_to_pdf.sh "./artifact.md" --theme plain
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

input_path="$1"
shift

out_path=""
title_override=""
theme="${FC_BRANDED_PDF_THEME:-${HERMES_PDF_THEME:-${AGENTS_PDF_THEME:-fc}}}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)
      out_path="${2:-}"
      if [[ -z "${out_path}" ]]; then
        echo "ERROR: --out requires a non-empty value" >&2
        exit 2
      fi
      shift 2
      ;;
    --title)
      title_override="${2:-}"
      if [[ -z "${title_override}" ]]; then
        echo "ERROR: --title requires a non-empty value" >&2
        exit 2
      fi
      shift 2
      ;;
    --theme)
      theme="${2:-}"
      if [[ -z "${theme}" ]]; then
        echo "ERROR: --theme requires a non-empty value" >&2
        exit 2
      fi
      shift 2
      ;;
    *)
      echo "ERROR: unknown arg: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required (used for path normalization + file:// URI handling)" >&2
  exit 127
fi

input_path="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "${input_path}")"
if [[ ! -f "${input_path}" ]]; then
  echo "ERROR: input file not found: ${input_path}" >&2
  exit 1
fi

if [[ -z "${out_path}" ]]; then
  default_out_dir="$(dirname "${input_path}")"
  base_name="$(basename "${input_path}")"
  base_stem="${base_name%.*}"
  out_path="${default_out_dir}/${base_stem}.pdf"
fi
out_path="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "${out_path}")"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "ERROR: pandoc is required to render Markdown -> PDF but was not found on PATH" >&2
  echo "Install (mac): brew install pandoc" >&2
  echo "Install (linux): apt-get install pandoc" >&2
  exit 127
fi

find_chrome_bin() {
  if command -v chromium >/dev/null 2>&1; then
    echo "chromium"
    return 0
  fi
  if command -v chromium-browser >/dev/null 2>&1; then
    echo "chromium-browser"
    return 0
  fi
  if command -v google-chrome >/dev/null 2>&1; then
    echo "google-chrome"
    return 0
  fi
  if command -v google-chrome-stable >/dev/null 2>&1; then
    echo "google-chrome-stable"
    return 0
  fi
  if [[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
    echo "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    return 0
  fi
  if [[ -x "/Applications/Chromium.app/Contents/MacOS/Chromium" ]]; then
    echo "/Applications/Chromium.app/Contents/MacOS/Chromium"
    return 0
  fi
  return 1
}

chrome_bin="$(find_chrome_bin || true)"
if [[ -z "${chrome_bin}" ]]; then
  echo "ERROR: Chrome/Chromium is required to render HTML -> PDF but was not found." >&2
  echo "Expected one of: chromium, google-chrome, or /Applications/Google Chrome.app/..." >&2
  exit 127
fi

mkdir -p "$(dirname "${out_path}")"

tmpdir="$(mktemp -d)"
cleanup() {
  rm -rf "${tmpdir}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

html_path="${tmpdir}/doc.html"
header_path="${tmpdir}/header.html"
before_body_path="${tmpdir}/before_body.html"

# Title metadata (used in HTML head + top ribbon)
title="${title_override}"
if [[ -z "${title}" ]]; then
  title="$(basename "${input_path}")"
fi

# Escape title for safe HTML injection
html_escape() {
  python3 - <<'PY'
import html
import sys
print(html.escape(sys.stdin.read().rstrip('\n')))
PY
}

title_html="$(printf '%s' "${title}" | html_escape)"

generated_at="$(date '+%Y-%m-%d %H:%M %Z')"
generated_at_html="$(printf '%s' "${generated_at}" | html_escape)"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
assets_dir="${script_dir}/../assets"

include_before_body_args=()

case "${theme}" in
  fc|pokerskill)
    css_path="${assets_dir}/pokerskill.css"
    logo_path="${assets_dir}/logo_web.png"

    if [[ ! -f "${css_path}" ]]; then
      echo "ERROR: missing FC / Poker Skill PDF theme CSS: ${css_path}" >&2
      exit 1
    fi

    printf '<style>\n' >"${header_path}"
    cat "${css_path}" >>"${header_path}"
    printf '\n</style>\n' >>"${header_path}"

    logo_b64=""
    if [[ -f "${logo_path}" ]]; then
      logo_b64="$(python3 - <<PY "${logo_path}"
import base64
import pathlib
import sys
p = pathlib.Path(sys.argv[1])
print(base64.b64encode(p.read_bytes()).decode('ascii'))
PY
)"
    fi

    if [[ -n "${logo_b64}" ]]; then
      logo_img="<img class=\"ps-logo\" src=\"data:image/png;base64,${logo_b64}\" alt=\"FC / Poker Skill\"/>"
    else
      logo_img="<div style=\"font-weight:700;color:#10141C\">FC</div>"
    fi

    cat >"${before_body_path}" <<HTML
<div class="ps-topbar">
  <div class="ps-topbar-left">
    ${logo_img}
    <div class="ps-topbar-tag">FC Artifact</div>
  </div>
  <div class="ps-topbar-right">
    <div class="ps-topbar-doc-title">${title_html}</div>
    <div class="ps-topbar-date">Generated ${generated_at_html}</div>
  </div>
</div>
HTML

    include_before_body_args=(--include-before-body "${before_body_path}")
    ;;

  plain)
    # Legacy minimal CSS (kept intentionally boring)
    cat >"${header_path}" <<'HTML'
<style>
  :root {
    --text: #111827;
    --muted: #6b7280;
    --bg: #ffffff;
    --code-bg: #f6f8fa;
    --border: #e5e7eb;
  }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 12pt;
    line-height: 1.45;
    margin: 2.2rem;
  }
  h1, h2, h3 { line-height: 1.2; }
  h1 { font-size: 22pt; margin: 0 0 0.8rem 0; }
  h2 { font-size: 16pt; margin: 1.4rem 0 0.6rem 0; }
  h3 { font-size: 13pt; margin: 1.1rem 0 0.5rem 0; }
  p { margin: 0.6rem 0; }
  a { color: #2563eb; text-decoration: none; }
  a:hover { text-decoration: underline; }
  blockquote {
    border-left: 4px solid var(--border);
    padding: 0.3rem 0.9rem;
    margin: 0.9rem 0;
    color: var(--muted);
  }
  code, pre {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: 10.5pt;
  }
  pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    padding: 0.75rem 0.9rem;
    border-radius: 10px;
    overflow-x: auto;
    white-space: pre-wrap;
  }
  code {
    background: var(--code-bg);
    border: 1px solid var(--border);
    padding: 0.08rem 0.26rem;
    border-radius: 6px;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.8rem 0;
    font-size: 11pt;
  }
  th, td {
    border: 1px solid var(--border);
    padding: 0.45rem 0.55rem;
    vertical-align: top;
  }
  th { background: #f9fafb; }
  hr { border: 0; border-top: 1px solid var(--border); margin: 1.2rem 0; }
</style>
HTML
    ;;

  *)
    echo "ERROR: unknown theme: ${theme}. Supported: fc | pokerskill | plain" >&2
    exit 2
    ;;
esac

resource_dir="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).parent.resolve())' "${input_path}")"
pandoc_input_path="${tmpdir}/pandoc_input.md"

# Some doctrine artifacts place standalone HTML anchors directly above ATX headings:
#   <a id="section"></a>
#   ## Heading
# In CommonMark/Pandoc, that raw HTML block can swallow the following heading line
# unless there is a blank line after the anchor, which leaves literal `##` text in
# the rendered PDF. Normalize by inserting a blank line after standalone anchor tags
# when the next line is non-empty.
python3 - <<'PY' "${input_path}" "${pandoc_input_path}"
import pathlib
import re
import sys

src_path = pathlib.Path(sys.argv[1])
out_path = pathlib.Path(sys.argv[2])
text = src_path.read_text(encoding='utf-8')
lines = text.splitlines()
anchor_re = re.compile(r"^\s*<a\s+id=(\"[^\"]+\"|'[^']+')\s*></a>\s*$")
out_lines = []
for idx, line in enumerate(lines):
    out_lines.append(line)
    if anchor_re.match(line):
        next_line = lines[idx + 1] if idx + 1 < len(lines) else None
        if next_line is not None and next_line.strip() != '':
            out_lines.append('')
normalized = '\n'.join(out_lines)
if text.endswith('\n'):
    normalized += '\n'
out_path.write_text(normalized, encoding='utf-8')
PY

pandoc \
  --from markdown+smart \
  --to html5 \
  --standalone \
  --embed-resources \
  --resource-path "${resource_dir}" \
  --metadata "title=${title}" \
  --include-in-header "${header_path}" \
  "${include_before_body_args[@]}" \
  --output "${html_path}" \
  "${pandoc_input_path}"

# Improve wrapping for common "unbreakable" tokens in PDFs (esp. table headers)
# by inserting explicit break opportunities.
python3 - <<'PY' "${html_path}"
import pathlib
import sys
p = pathlib.Path(sys.argv[1])
html = p.read_text(encoding='utf-8')
# Allow line breaks after arrows without changing appearance.
# (Safe to do as a raw replace because this glyph is overwhelmingly used in text,
# not in tag/attribute syntax.)
html = html.replace('→', '→<wbr>')
p.write_text(html, encoding='utf-8')
PY

file_uri="$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve().as_uri())' "${html_path}")"

chrome_profile_dir="${tmpdir}/chrome-profile"
chrome_out_path="${tmpdir}/rendered.pdf"
mkdir -p "${chrome_profile_dir}"
rm -f "${chrome_out_path}"

# Chrome 145 on macOS can leave headless print-to-pdf runs alive after the PDF
# is already written. Poll for a fresh temp output file, then tear down the
# renderer so local render flows do not hang behind a completed PDF write. Rendering
# into a temp path also avoids falsely "succeeding" against a stale existing
# destination PDF.
"${chrome_bin}" \
  --headless \
  --disable-gpu \
  --disable-dev-shm-usage \
  --disable-background-networking \
  --disable-breakpad \
  --disable-component-update \
  --no-default-browser-check \
  --no-first-run \
  --no-sandbox \
  --user-data-dir="${chrome_profile_dir}" \
  --no-pdf-header-footer \
  --print-to-pdf="${chrome_out_path}" \
  "${file_uri}" \
  >/dev/null 2>&1 &
chrome_pid=$!

for ((attempt = 0; attempt < 300; attempt += 1)); do
  if [[ -f "${chrome_out_path}" ]] && [[ "$(wc -c < "${chrome_out_path}" | tr -d ' ')" -ge 100 ]]; then
    break
  fi

  if ! kill -0 "${chrome_pid}" >/dev/null 2>&1; then
    wait "${chrome_pid}" || true
    break
  fi

  sleep 0.1
done

if kill -0 "${chrome_pid}" >/dev/null 2>&1; then
  kill "${chrome_pid}" >/dev/null 2>&1 || true
  for ((attempt = 0; attempt < 20; attempt += 1)); do
    if ! kill -0 "${chrome_pid}" >/dev/null 2>&1; then
      break
    fi
    sleep 0.1
  done

  if kill -0 "${chrome_pid}" >/dev/null 2>&1; then
    kill -9 "${chrome_pid}" >/dev/null 2>&1 || true
  fi

  wait "${chrome_pid}" >/dev/null 2>&1 || true
fi

if [[ ! -f "${chrome_out_path}" ]]; then
  echo "ERROR: PDF render failed; output file missing: ${chrome_out_path}" >&2
  exit 1
fi

if [[ "$(wc -c < "${chrome_out_path}" | tr -d ' ')" -lt 100 ]]; then
  echo "ERROR: PDF render produced an unexpectedly small file: ${chrome_out_path}" >&2
  exit 1
fi

mv -f "${chrome_out_path}" "${out_path}"

echo "${out_path}"
