---
title: arch_skill Prompt Binding Contract
purpose: "Define how to interpret prompt markdown when reading it directly (without /prompts invocation)."
---

# Prompt Binding Contract (when reading prompt markdown directly)

Codex placeholder expansion (`$ARGUMENTS`, `$1`…`$9`, `KEY=value`) happens when you **invoke** `/prompts:<name>`.
If you instead open/read a prompt file as plain Markdown, you must apply these bindings explicitly.

## 1) What to ignore
- Ignore the YAML frontmatter block (`--- … ---`) at the top of prompt files.
  - It is metadata for Codex’s prompt picker (description, argument-hint).

## 2) `$ARGUMENTS`
- Treat `$ARGUMENTS` as the user’s current freeform request text.
- If the user’s request is ambiguous (or missing), ask for a 1–3 sentence blurb and stop until you have it.

## 3) Positional args (`$1`…`$9`)
- If the prompt references `$1`…`$9`, treat them as space-separated positional args.
- If the user didn’t provide them, ask only for the missing ones that are required to proceed.

## 4) Named args (`FOO=bar`)
- If the prompt references named placeholders (e.g., `$DOC_PATH`, `$FILES`) that normally come from `KEY=value` args:
  - First try to resolve from the conversation and repo context (e.g., infer DOC_PATH from a `docs/<...>.md` mentioned earlier).
  - If not resolvable, ask for the smallest missing key.

## 5) Prompt file discovery
Prefer installed prompts first:
1) `~/.codex/prompts/<prompt>.md`
2) If working inside the arch_skill repo: `prompts/<prompt>.md`

## 6) Safety rule
If the prompt says “documentation-only (planning)” then do not modify code.
If it says “do not commit/push”, do not commit/push unless explicitly instructed.

