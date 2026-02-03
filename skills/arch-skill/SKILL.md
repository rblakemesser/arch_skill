---
name: arch-skill
description: "Router + invariants for the arch_skill prompt suite. Use it to keep a single SSOT plan doc + worklog, enforce strict question policy, and route to the right /prompts:* command for architecture planning and execution."
---

# arch-skill

This skill runs **alongside** the existing `/prompts:*` commands:
- Use it to decide which prompt to run next and to enforce the workflow invariants.
- Then invoke the prompt directly (preferred) or load its markdown procedure on demand.

## When to Use
- User asks for architecture planning, a phased plan, a call-site audit, or “arch_skill flow”.
- Work needs a single plan doc + worklog and minimal, credible verification.
- You want to route the user to the correct `/prompts:*` command (and keep the process consistent).

## Non‑Negotiables (Workflow Invariants)
- **Single-document rule (SSOT):** exactly one plan doc under `docs/` is authoritative. Worklog is derived from it.
- **Code is ground truth:** anchor claims in file paths/symbols/commands; do not speculate.
- **Minimal verification:** prefer existing tests/commands; avoid inventing new harnesses by default.
- **Question policy (strict):** only ask questions that cannot be answered by searching the repo/docs/fixtures or running existing tooling.
- **Output format:** when you invoke a prompt, follow that prompt’s output format (don’t restate style rules here).

## Routing Rule (How to “Load Prompts on Demand”)
Prefer invoking prompts:
- Use `/prompts:<name> …` whenever possible (Codex handles placeholder expansion).

If you must **load the markdown procedure directly** (no `/prompts` invocation), then:
- Open the prompt file and follow it as the procedure.
- Apply the placeholder binding contract in `resources/BINDING_CONTRACT.md` (especially `$ARGUMENTS`).

Prompt discovery order:
1) Installed prompts: `~/.codex/prompts/<name>.md`
2) Repo prompts (when working inside this repo): `prompts/<name>.md`

## Prompt Index
See `resources/PROMPT_INDEX.md` for the canonical mapping from intent → prompt name.

## Common Prompts (Most Used)
These are the prompts you should reach for first. (There are others under `/prompts:*`.)

| Prompt | What it does | Args |
| --- | --- | --- |
| `/prompts:arch-new` | Create a new canonical plan doc + draft TL;DR/North Star (then ask for confirmation). | Freeform blurb |
| `/prompts:arch-reformat` | Convert an existing doc into canonical arch_skill format (preserve content; draft TL;DR/North Star; confirm). | Input `.md` path; optional `OUT=...` |
| `/prompts:arch-ui-ascii` | Add current/target ASCII UI mockups (only when the plan touches UI/UX). | DOC_PATH or guidance |
| `/prompts:arch-implement` | Execute the plan end-to-end (systematic, test-as-you-go), update worklog, then finalize. | DOC_PATH or guidance |
| `/prompts:arch-research-agent` | Write Research Grounding (internal anchors + patterns + optional external), using subagents when helpful. | DOC_PATH or guidance |
| `/prompts:arch-deep-dive-agent` | Produce current/target architecture + exhaustive call-site audit (agent-assisted). | DOC_PATH or guidance |
| `/prompts:arch-external-research-agent` | Do web-based best-practice research and write grounded notes into DOC_PATH with sources. | DOC_PATH or guidance |
| `/prompts:arch-codereview` | Run external review via Claude CLI, then apply the feedback you agree with. | DOC_PATH + scope notes |
| `/prompts:arch-open-pr` | Finalize: merge default branch, run preflight checks, commit/push, and open a detailed PR. | Optional title/constraints |
