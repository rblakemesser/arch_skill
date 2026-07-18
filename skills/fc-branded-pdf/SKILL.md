---
name: fc-branded-pdf
description: "Convert Markdown or document content into FC / Poker Skill branded PDF artifacts using the bundled letterhead CSS, logo, and local renderer. Use for reports, memos, briefs, packets, audits, summaries, exported document tabs, or any ask for an FC-branded PDF / FC letterhead PDF. Not for Drive archival, slide decks, image/video generation, or ordinary chat answers."
license: MIT
---

# FC Branded PDF

Use this skill to produce local FC / Poker Skill branded PDFs from Markdown or
document-like content.

What it covers:
- a reusable Markdown report template
- local Markdown -> branded PDF rendering
- FC / Poker Skill letterhead styling through bundled CSS and logo assets
- verification before the PDF is shared or attached

## When to use

Use when:
- you are producing a report-like artifact for FC / Fun Country / Poker Skill
- the deliverable should be a polished branded PDF
- the user asks for an FC-branded PDF, FC letterhead, or a PDF packet
- you want a durable local Markdown source plus a rendered local PDF

Typical outputs:
- analysis packet
- memo
- experiment readout
- QA summary
- postmortem
- investor or operator brief

Do not use when:
- a normal chat reply is enough
- the deliverable is primarily slides, images, or video
- the task is to archive or upload a file to Drive

## Linked files in this skill

- `templates/report_template.md`
- `scripts/render_markdown_to_pdf.sh`
- `assets/pokerskill.css`
- `assets/logo_web.png`

## Core workflow

1. Identify the source content and decide whether it is already Markdown.
2. If the source is a Google Doc export, `.docx`, `.html`, notes, pasted text,
   or multiple files, make a clean Markdown staging file first. Preserve the
   source order, headings, links, tables, and important images.
3. Start from `templates/report_template.md` when creating a new report from
   scratch. Use an existing Markdown artifact when the content already exists.
4. Render the Markdown with `scripts/render_markdown_to_pdf.sh`.
5. Verify page count, extracted text, and visual preview for layout-sensitive
   PDFs before reporting the result.
6. Return the local PDF path. If the host supports file attachments, attach the
   rendered PDF from that path.

## Render command

```bash
bash "{baseDir}/scripts/render_markdown_to_pdf.sh" \
  "/abs/path/to/report.md" \
  --title "Human-readable report title"
```

Default behavior:
- renders a branded FC / Poker Skill PDF
- outputs next to the source Markdown file unless `--out` is provided
- uses the local bundled CSS/logo inside this skill

Theme notes:
- preferred env var: `FC_BRANDED_PDF_THEME`
- legacy fallback env vars: `HERMES_PDF_THEME`, then `AGENTS_PDF_THEME`
- bundled branded theme: `fc` (alias: `pokerskill`)
- fallback minimal theme: `plain`

## Source conversion notes

- For `.md` input, render directly.
- For `.docx`, use `pandoc source.docx -t gfm -o source.md` first, then render
  the Markdown.
- For `.html`, use `pandoc source.html -t gfm -o source.md` first, then render.
- For pasted content, write a local Markdown source file first.
- For multiple inputs, combine them into one ordered Markdown packet before
  rendering.
- Do not use this skill to upload, archive, or move the PDF to Drive.

## QA before shipping

Preview the PDF as images before sending if layout matters, and verify text
extraction for important headings/sections.

```bash
pdfinfo "/abs/path/to/report.pdf" | grep '^Pages'

OUT_DIR="/tmp/fc-branded-pdf-preview"
mkdir -p "$OUT_DIR"

pdftoppm -png -r 300 -f 1 -l 3 \
  "/abs/path/to/report.pdf" \
  "$OUT_DIR/report_page"

pdftotext "/abs/path/to/report.pdf" "$OUT_DIR/report_text.txt"
rg "Executive Summary|TL;DR|Appendix" "$OUT_DIR/report_text.txt"
```

Check for:
- clipped wide tables
- broken headers
- missing images
- ugly wrapping
- raw Markdown syntax leaking into the PDF

## Layout rules

- prefer fewer columns
- shorten headers aggressively
- split wide tables if needed
- move very wide data to an appendix or image
- keep tables readable in preview, not just locally
- Mermaid/code-fenced diagrams render as raw code with the stock Markdown ->
  HTML -> PDF path. If a visual diagram matters, pre-render it to an image or
  HTML before PDF generation; otherwise accept the readable code block.

## Wide-table fallback learned from FC audit PDFs

When combining long Markdown packets into a letter-size PDF, normal pipe tables with 5+ columns can render technically unclipped but still unreadable: headers split mid-word and long identifiers wrap across many arbitrary line breaks.

Reusable fallback:
- before rendering, convert Markdown pipe tables with 5+ columns into compact “row cards” / nested bullet blocks
- preserve every cell, but represent each row as:
  - `- **<first column header>:** <first cell>`
  - nested bullets for the remaining columns
- add CSS to prevent card-like bullets from splitting mid-row:

```html
<style>
.page-break { page-break-before: always; break-before: page; }
li { break-inside: avoid; page-break-inside: avoid; }
code { white-space: pre-wrap; }
</style>
```

Verification discipline:
- do not only check page count and first pages
- use `pdftotext` to find pages containing wide sections such as `Routing table`, `Metrics`, or `summary table`
- render those pages with `pdftoppm`
- inspect with vision; if a row is cut off or a table is cramped, regenerate with row-card fallback and re-preview the affected pages

## Good outcome

A good report has:
- durable Markdown source
- branded PDF that looks like the shared Poker Skill theme
- clean table handling
- a local absolute PDF path
- no Drive archive or upload side effect

## Notes

- The branded asset bundle stays inside the skill itself:
  - `assets/pokerskill.css`
  - `assets/logo_web.png`
  - `scripts/render_markdown_to_pdf.sh`
- If the renderer or theme drifts, update this skill bundle instead of inventing a parallel PDF workflow.
