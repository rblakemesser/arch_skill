---
description: "11) Implement plan: execute next phase + update doc."
argument-hint: <optional guidance>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
If DOC_PATH is not provided, locate the most relevant architecture doc by semantic match to $ARGUMENTS and the current conversation; prefer the doc that explicitly matches the topic and is most recently updated among relevant candidates. If you cannot determine a clear winner, ask the user to choose from the top 2–3 candidates.
Do not ask the user questions during investigation. Resolve by reading more code and searching the repo. Ask only if required information is not present in the repo or doc and cannot be inferred (e.g., product choice or external constraint).
Derive WORKLOG_PATH from DOC_PATH using the same directory and suffix: `<DOC_BASENAME>_WORKLOG.md`. If missing, create it. Add cross-links: plan doc should reference the worklog near the top; worklog should link back to the plan doc.
Execution notes belong in the worklog. The plan doc is only updated for audits, decisions, or blockers that change scope/requirements.

1) Read the doc and identify the current phase:
   - If a phase is explicitly named in $ARGUMENTS, use it.
   - Otherwise, pick the highest phase with incomplete exit criteria or no “Phase <n> Progress Update”.
2) Implement only that phase.
3) Run the phase’s test plan (or the closest available test if the exact one is not runnable).
4) Write a Phase Progress Update to WORKLOG_PATH. Add a Decision Log entry to the plan doc only if a real decision was made.
5) If the plan requires external reviews (opus/gemini), trigger the review gate and integrate changes you agree with.
6) Commit only files you touched; ignore other dirty files. Push if requested or if previous phases used push‑per‑phase.

OUTPUT FORMAT (console only):
Summary:
- Doc: <path>
- Worklog: <path>
- Phase executed: <n>
- Code changes: <high-level>
- Tests run: <command> — <result>
- Worklog updated: <yes/no>
- Plan updated (audits/decisions only): <yes/no>
- Review gate: <done/pending>
Next:
- <next phase or action>
