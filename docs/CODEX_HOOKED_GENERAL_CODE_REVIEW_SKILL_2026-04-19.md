---
title: "arch_skill - Codex Hooked General Code Review Skill - Architecture Plan"
date: 2026-04-19
status: active
fallback_policy: forbidden
owners: [aelaguiz]
reviewers: []
doc_type: new_system
related:
  - skills/codex-review-yolo/SKILL.md
  - skills/codex-review-yolo/references/prompt-template.md
  - skills/audit-loop/SKILL.md
  - skills/arch-step/scripts/arch_controller_stop_hook.py
  - docs/NATIVE_AUTO_LOOPS_FOR_CODEX_AND_CLAUDE_2026-04-19.md
  - README.md
  - Makefile
  - ../psmobile/scripts/review/render_pr_agent_extra_instructions.py
  - ../psmobile/.github/claude/repo_review_policy.md
  - ../psmobile/.github/claude/partials/spam_guardrails.md
  - /Users/aelaguiz/.agents/skills/skill-authoring/SKILL.md
  - /Users/aelaguiz/.agents/skills/prompt-authoring/SKILL.md
  - /Users/aelaguiz/.agents/skills/agent-linter/SKILL.md
---

# TL;DR

- Outcome:
  - Ship a reusable `code-review` skill that can review any codebase or diff from Codex or Claude Code, but always runs the actual reviewer as a fresh unsandboxed Codex `gpt-5.4` `xhigh` process with a hook-backed continuation path where the host supports it.
- Problem:
  - The repo has a narrow `codex-review-yolo` skill for manual independent reviews and shared hook-controller machinery, but it does not yet ship a general code-review skill that combines exhaustive code audit, current external best-practice research, genericized PR-review requirements, docs-drift checks, agent-project linting, and Codex/Claude hook invocation into one reusable runtime contract.
- Approach:
  - Author a new skill package using `skill-authoring` for package shape and `prompt-authoring` for the reviewer prompt, reusing the existing Codex shell-out and hook-controller patterns instead of inventing a parallel orchestration layer. The reviewer must build a repo-grounded map, consult current primary sources where best-practice claims matter, fan out parallel Codex `gpt-5.4-mini` `xhigh` subreviews, synthesize findings, and return high-confidence code-review output only.
- Plan:
  - First ground the current review and hook surfaces, then design the skill package, prompt contract, controller integration, Claude shell-out behavior, agent-linter trigger, and verification path. Implementation should add the smallest live skill/runtime surface that satisfies the review contract without reviving archived prompts or creating another review framework.
- Non-negotiables:
  - The reviewer is always Codex `gpt-5.4` `xhigh`; Claude invocation shells out to Codex rather than asking Claude to be the reviewer.
  - Default review execution is unsandboxed according to the repo's existing Codex patterns, not a best-effort sandboxed substitute.
  - Exhaustive review means mapped, evidence-backed, and parallelized through required Codex mini review-lens agents; it does not mean noisy speculative findings.
  - Any agent, prompt, skill, or agent-runtime project must explicitly invoke `$agent-linter` and use that audit lens before finalizing review feedback.
  - Documentation, comments, instructions, and other live truth surfaces must be checked for update-or-delete drift whenever code behavior changes.
  - No generic checklist theater: findings must be introduced by the changed code, cite evidence, and explain the concrete risk.

<!-- arch_skill:block:implementation_audit:start -->
# Implementation Audit (authoritative)
Date: 2026-04-19
Verdict (code): NOT COMPLETE
Manual QA: n/a (non-blocking)

## Code blockers (why code is not done)
- Phase 1 skill package is only partially authored. `skills/code-review/SKILL.md` and `skills/code-review/references/reviewer-prompt.md` exist and reference three sibling references plus a runner script that do not exist on disk, so the package is internally inconsistent and not self-contained.
- Phase 2 deterministic Codex runner was never implemented. `skills/code-review/scripts/` is an empty directory, so `SKILL.md`'s invocation recipe is broken and none of the Codex `gpt-5.4` `xhigh` reviewer, parallel `gpt-5.4-mini` `xhigh` lens fan-out, artifact capture, coverage accounting, or fail-loud failure-mode behavior exists.
- Phase 3 shared-dispatcher integration was never landed. `skills/arch-step/scripts/arch_controller_stop_hook.py` has no `code-review` state spec or handler, so neither `.codex/code-review-state.<SESSION_ID>.json` nor `.claude/arch_skill/code-review-state.<SESSION_ID>.json` is resolvable and the hook-backed path documented in `SKILL.md` cannot run.
- Phase 4 install inventory and public docs were never published. `code-review` is absent from `Makefile` `SKILLS`/`CLAUDE_SKILLS`, `README.md`, and `docs/arch_skill_usage_guide.md`, so the skill is not installed and not discoverable.
- Phase 5 runtime proof cannot exist while Phases 1-4 are incomplete. No `WORKLOG_PATH` was created, no smoke artifacts exist, and no Codex/Claude hook-backed smoke runs were recorded.
- Phase 6 final preservation/readiness audit cannot have run while the prior frontier is incomplete, and the plan itself was not annotated with any phase-status or worklog evidence.

## Reopened phases (false-complete fixes)
No phase was ever marked complete in this doc; the full approved Section 7 ordered frontier remains open. Listing phases for explicit reopen so the frontier is unambiguous:
- Phase 1 (Author the canonical `code-review` skill package) — reopened because:
  - `skills/code-review/references/review-requirements.md` is missing but is required by the checklist and is referenced by `SKILL.md`.
  - `skills/code-review/references/output-contract.md` is missing but is required by the checklist, is referenced by `SKILL.md`, and is what the runner/prompt must both honor.
  - `skills/code-review/references/invocation.md` is missing but is required by the checklist, is referenced by `SKILL.md`, and is the exact flag and artifact contract.
  - `npx skills check` has not been run against the new package.
- Phase 2 (Implement the deterministic Codex review runner) — reopened because:
  - `skills/code-review/scripts/run_code_review.py` does not exist; the entire runner (target resolution, parallel Codex `gpt-5.4-mini` `xhigh` lens fan-out, final Codex `gpt-5.4` `xhigh` synthesis, artifact tree, fail-loud coverage) is unimplemented.
- Phase 3 (Integrate hook-backed review through the shared dispatcher) — reopened because:
  - `arch_controller_stop_hook.py` has no `code-review` controller spec, no state handler, and no Codex-from-Claude-host exception wiring. Synthetic Codex and Claude state probes cannot resolve.
- Phase 4 (Publish install inventory and live docs truth) — reopened because:
  - `Makefile` `SKILLS` and `CLAUDE_SKILLS` do not include `code-review`.
  - `README.md` does not mention the skill, its Codex-as-reviewer posture, or its hook behavior.
  - `docs/arch_skill_usage_guide.md` does not mention the skill or its selection vs. `codex-review-yolo`.
  - `make verify_install` against the new skill has not been run.
- Phase 5 (Prove review behavior and failure modes) — reopened because:
  - No direct review smoke artifacts (no-findings, seeded duplication/docs-drift, agent-surface) exist.
  - No Codex-host or Claude-host hook-backed smoke artifacts exist.
  - No `WORKLOG_PATH` exists to carry proof evidence.
- Phase 6 (Final preservation and implementation-readiness audit) — reopened because:
  - Cannot run while Phases 1-5 are incomplete; there is nothing yet to re-read as a cohesive system.

## Missing items (code gaps; evidence-anchored; no tables)
- Phase 1 package completion
  - Evidence anchors:
    - skills/code-review/SKILL.md:80-82 (references review-requirements.md, output-contract.md, invocation.md)
    - skills/code-review/references/ (only reviewer-prompt.md present)
  - Plan expects:
    - review-requirements.md, output-contract.md, invocation.md authored to the `$prompt-authoring`/`$skill-authoring` quality bar; package passes `npx skills check`.
  - Code reality:
    - Three referenced files missing; no package check recorded.
  - Fix:
    - Author the three references end to end, then run `npx skills check` and re-read the package as a whole.
- Phase 2 deterministic Codex runner
  - Evidence anchors:
    - skills/code-review/scripts/ (empty)
    - skills/code-review/SKILL.md:52-57 (invocation recipe calling run_code_review.py)
  - Plan expects:
    - `run_code_review.py` with target resolution, namespaced run directory, parallel `gpt-5.4-mini` `xhigh` Codex lens fan-out, final `gpt-5.4` `xhigh` Codex synthesis, coverage metadata, and fail-loud behavior on missing Codex / ambiguous target / failed subreview / malformed verdict / missing required agent-linter.
  - Code reality:
    - No runner; the skill's documented invocation path cannot execute.
  - Fix:
    - Implement the runner per Phase 2 checklist, run `python3 -m py_compile`, and execute the Phase 2 verification smoke runs.
- Phase 3 shared-dispatcher integration
  - Evidence anchors:
    - skills/arch-step/scripts/arch_controller_stop_hook.py (no `code-review` state spec or handler; grep for `code.review|code_review|CODE_REVIEW` returns nothing)
  - Plan expects:
    - A `code-review` controller spec, `CodeReviewHookState` fields, a handler that invokes the runner from both Codex and Claude host state namespaces, and the documented exception that the review subprocess remains Codex even from Claude-host runs. Existing shared installers preserved; no second Stop hook added.
  - Code reality:
    - None of this is wired.
  - Fix:
    - Add the state spec and handler, preserve existing controller families, add the short boundary comment at the Claude-host→Codex-reviewer exception, and run the Phase 3 synthetic Codex/Claude probes plus `python3 -m py_compile`.
- Phase 4 install inventory and live docs
  - Evidence anchors:
    - Makefile (no `code-review` in `SKILLS`/`CLAUDE_SKILLS`)
    - README.md (no `code-review` mention)
    - docs/arch_skill_usage_guide.md (no `code-review` mention)
  - Plan expects:
    - `code-review` added to `SKILLS` and `CLAUDE_SKILLS` (kept out of `GEMINI_SKILLS`), README skill inventory and runtime/hook docs updated to describe Codex-as-reviewer and the Claude→Codex shell-out, and the usage guide updated for skill selection vs. `codex-review-yolo`. Preserve existing generic Codex+Claude hook truth instead of broad rewrites. Run `npx skills check` and `make verify_install`.
  - Code reality:
    - No install or docs updates made.
  - Fix:
    - Land the additive Makefile/README/usage-guide edits and run the stated verifications.
- Phase 5 runtime proof
  - Evidence anchors:
    - docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19_WORKLOG.md does not exist
    - No review run artifacts in the repo
  - Plan expects:
    - Direct review smoke artifacts for no-findings, seeded duplication/docs-drift, and agent-surface cases; Codex- and Claude-host hook-backed smoke artifacts; recorded fail-loud behavior for missing Codex, ambiguous target, missing agent-linter, failed subreview, malformed verdict; final synthesis matches `output-contract.md`.
  - Code reality:
    - None run; no worklog created.
  - Fix:
    - After Phases 1-4 land, execute the Phase 5 smoke matrix and record artifacts/decisions in the worklog.
- Phase 6 final preservation/readiness audit
  - Evidence anchors:
    - No final re-read performed; prior phases not complete
  - Plan expects:
    - One canonical detailed review prompt owner (`skills/code-review/references/reviewer-prompt.md`); no duplicated review doctrine in README/Makefile/`codex-review-yolo`; no `../psmobile` runtime dependency inside the shipped skill; no stale unsupported Gemini claims; `npx skills check` and `make verify_install` green or explicitly explained.
  - Code reality:
    - Not attempted.
  - Fix:
    - After Phases 1-5 are genuinely done, run the Phase 6 re-read and verification pass and only then consider the plan code-complete.

## Non-blocking follow-ups (manual QA / screenshots / human verification)
- None. This plan has no manual-QA-only items, so nothing here is eligible as non-blocking; all remaining items above are code work.
<!-- arch_skill:block:implementation_audit:end -->

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-04-19
external_research_grounding: done 2026-04-19
deep_dive_pass_2: done 2026-04-19
phase_plan: done 2026-04-19
consistency_pass: done 2026-04-19
local_runtime_refresh: done 2026-04-19
recommended_flow: deep dive -> external research grounding -> deep dive again -> phase plan -> implement
note: This block tracks stage order only. It never overrides readiness blockers caused by unresolved decisions.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

If this repo adds a self-contained general code-review skill whose runtime path always shells out to a fresh unsandboxed Codex `gpt-5.4` `xhigh` reviewer, and whose prompt requires repo-grounded exhaustive mapping, current external best-practice grounding, parallel `gpt-5.4-mini` `xhigh` subreviews, docs-drift checks, and `$agent-linter` on agent-building work, then users can invoke one review skill from either Codex or Claude Code and receive high-confidence findings that catch correctness, architecture, duplication, proof, and documentation drift without depending on the caller model's session memory.

## 0.2 In scope

- A new live skill package under `skills/` for general code review.
- The reviewer prompt and supporting references needed to make the code review portable across repos, languages, and frameworks.
- A hook-backed invocation story for Codex and Claude Code that fits the repo direction in `docs/NATIVE_AUTO_LOOPS_FOR_CODEX_AND_CLAUDE_2026-04-19.md`.
- A deterministic shell-out path that invokes local Codex as the reviewer with:
  - model `gpt-5.4`
  - reasoning effort `xhigh`
  - unsandboxed execution using the repo's existing dangerous-bypass pattern or an explicitly equivalent configured profile
  - no inherited conversation context as review authority
- Parallel review-lens behavior launched by the runner as separate Codex `gpt-5.4-mini` `xhigh` subprocess agents:
  - code correctness and regressions
  - architecture, encapsulation, and duplicate-path drift
  - proof, tests, and automation adequacy
  - docs, comments, instructions, telemetry, and user-facing contract drift
  - agent-linter audit when the target repo builds agents, prompts, skills, flows, or instruction-bearing runtime surfaces
- Genericized review requirements scraped from `../psmobile`'s PR-agent hook and policy:
  - no pattern duplication or parallel paths
  - no unnecessary branches, shims, or test-only code paths
  - platform and external-boundary error handling
  - self-describing names, constants, and predicates for complex logic
  - proof proportional to changed risk, especially integration-shaped behavior
  - user-facing behavior, telemetry, and live documentation intent drift checks
  - concise, evidence-backed findings only
- Installation, README, and verification updates when the new skill name, routing, or hook behavior becomes live.

## 0.3 Out of scope

- Asking Claude, Gemini, or another caller model to perform the final review instead of the fresh Codex reviewer.
- Generic security/PII auditing unless the changed code introduces a concrete security, privacy, or secret-handling risk.
- Style-only, formatting-only, naming-only, or speculative architecture feedback that does not create a material correctness, maintainability, reviewability, or drift risk.
- A PR-Agent integration, GitHub bot, or hosted CI product. This plan is for an installable local agent skill and its hook/runtime support.
- Reviving archived pre-skill command surfaces or depending on archived prompts at runtime.
- Adding repo-cleanliness validators whose main purpose is policing strings, deleted files, or doc inventories instead of reviewing real changed behavior.

## 0.4 Definition of done (acceptance evidence)

- The new skill package passes `npx skills check` and keeps `SKILL.md` lean, self-contained, and trigger-accurate.
- The reviewer prompt passes the `prompt-authoring` quality bar: single job, clear success/failure, authoritative inputs, tool rules, process, quality bar, output contract, and fail-loud conditions.
- The skill package passes the `skill-authoring` quality bar: concrete leverage claim, 2-3 canonical asks, one clear anti-case, progressive disclosure, and no hidden repo context dependency.
- The default review command can be verified locally as a fresh Codex `gpt-5.4` `xhigh` unsandboxed invocation from a repo root.
- Claude Code invocation is verified to shell out to Codex for review rather than using Claude as the reviewer.
- The hook-backed story is implemented and verified for both Codex and Claude Code through the shared dispatcher, without fake parity claims.
- A representative code review demonstrates:
  - the reviewer maps the diff and relevant call sites before findings
  - external research is used for current best-practice claims, and claims are anchored to primary or authoritative sources where possible
  - parallel `gpt-5.4-mini` `xhigh` Codex subprocess review lenses run for required coverage
  - documentation drift is checked
  - agent-project surfaces trigger `$agent-linter`
  - low-confidence or policy-restatement noise is omitted
- `README.md`, `Makefile`, and any touched install or hook docs agree on the final skill inventory and runtime behavior.

## 0.5 Key invariants (fix immediately if violated)

- Always Codex as reviewer: `gpt-5.4` plus `xhigh`, fresh context, unsandboxed by default.
- Caller runtime is not review authority; Codex is.
- No fake hook parity: Codex and Claude Code support claims must match real installed behavior.
- No parallel review prompts that can drift from the new skill's canonical prompt contract.
- No duplicated review doctrine across `SKILL.md`, references, README prose, and controller prompts; keep one owner and link deeper truth.
- No noisy checklist output. Findings must be changed-code-specific, evidence-backed, and actionable.
- No documentation drift: touched live docs, comments, examples, install instructions, and agent instructions either stay true, get updated, or get deleted.
- Agent-building targets must run `$agent-linter` and incorporate its highest-value findings into the review synthesis.
- External research informs best-practice judgments but never overrides repo truth, user intent, or authoritative local contracts.
- No runtime fallbacks or compatibility shims unless this plan later records an explicit approved exception with a removal path.

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)

1. Make the reviewer genuinely independent, fresh, and strong by pinning review execution to Codex `gpt-5.4` `xhigh`.
2. Make the skill portable across codebases while still honoring repo-local instructions and canonical patterns.
3. Prevent drift: duplicate code paths, stale docs, stale prompts, stale comments, stale telemetry/contracts, and parallel review doctrine are first-class review risks.
4. Use external research only where it strengthens current best-practice judgment, and prefer primary sources or official docs over generic blog advice.
5. Keep findings sparse and high-confidence; an exhaustive audit should improve signal, not generate noise.
6. Fit Codex and Claude Code hook behavior into the repo's native-auto-loop direction without creating a second runtime architecture.

## 1.2 Constraints

- `docs/NATIVE_AUTO_LOOPS_FOR_CODEX_AND_CLAUDE_2026-04-19.md` and its worklog are active local truth for the generic Codex/Claude controller work; later implementation must coordinate with that completed local runtime contract rather than re-planning generic hook parity.
- Current worktree install behavior already includes shared Codex and Claude `Stop` hook wiring, runtime-local state roots, host-native child execution for generic auto controllers, and successful local proof; no `code-review` controller state or runner exists yet.
- `codex-review-yolo` already owns one manual independent-review pattern using `codex exec -p yolo`; this plan resolves the overlap by shipping `code-review` as a sibling skill with a stronger general-review contract and preserving `codex-review-yolo` unchanged.
- Existing controller code already shells out to `codex exec --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox` for fresh review/audit paths.
- The requested reviewer needs both judgment-heavy model behavior and deterministic invocation glue; package prose must not pretend to grant host permissions.
- Required parallel review coverage uses separate Codex subprocess lens agents, so implementation must not depend on native child subdelegation being available inside `codex exec`.

## 1.3 Architectural principles (rules we will enforce)

- One canonical review skill, not several overlapping review prompts.
- One deterministic reviewer invocation path, with caller-specific adapters only where the host runtime requires them.
- Prompt-first for review judgment; scripts only for reliable invocation, state, or hook glue.
- Repo truth first, external research second, generic best-practice slogans last.
- Parallelize review lenses through deterministic Codex subprocess agents and synthesize them into one findings-first report.
- Use existing install and hook owner surfaces (`Makefile`, `README.md`, `arch_controller_stop_hook.py`) before inventing new runtime machinery.
- Treat docs, comments, examples, telemetry catalogs, generated artifacts, and agent instructions as live contract surfaces when they describe changed behavior.

## 1.4 Known tradeoffs (explicit)

- A universal reviewer needs generic doctrine, but the best findings are repo-specific; the prompt must teach how to derive repo-local rules rather than ship a giant fixed checklist.
- Running unsandboxed Codex buys realistic verification and repo access but increases the need for clear "review-only" boundaries and no secret leakage in prompts.
- Parallel subreviews improve coverage but can duplicate findings; synthesis must dedupe aggressively and preserve the highest-confidence evidence.
- Hook-based review after every coding stop can be powerful but expensive; later design must decide whether default hook behavior is opt-in, explicit command-backed, or only active for armed review state.
- External research helps with current framework practices but can become decorative or stale; the reviewer must adopt or reject sources with reasoning.

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today

- `skills/codex-review-yolo/` provides a manual independent Codex review pattern using the local `yolo` profile.
- `skills/arch-step/scripts/arch_controller_stop_hook.py` already launches fresh unsandboxed Codex review/audit children for several hook-backed loops.
- `README.md` and `Makefile` install live skills for agents/Codex, Claude Code, and Gemini; the current worktree includes Claude hook wiring and verification, but the general code-review skill is still missing.
- `../psmobile/scripts/review/render_pr_agent_extra_instructions.py` renders repo review instructions from trusted policy files, giving a concrete source for genericizable review doctrine.
- `../psmobile/.github/claude/repo_review_policy.md` contains strong review priorities around duplication, unnecessary code paths, platform boundaries, self-describing code, real automation, user-facing intent drift, telemetry consistency, and review spam control.

## 2.2 What's broken / missing (concrete)

- There is no general live skill named and scoped for code review across arbitrary codebases.
- The existing `codex-review-yolo` skill is mechanism-focused and manual; it does not own exhaustive diff mapping, external research, docs drift, parallel subreviews, agent-linter integration, or hook-based Codex/Claude invocation.
- The repo's existing hook controllers prove the shell-out pattern, but there is no code-review controller state or hook contract for a reusable review skill.
- The psmobile review policy is useful but repo-specific; the generic review skill needs the reusable principles without importing PokerSkill-only facts.
- Current docs and install inventory do not mention the new skill or its runtime behavior.

## 2.3 Constraints implied by the problem

- The new skill is a sibling of `codex-review-yolo`, with a narrower "code review" trigger and stronger general-review runtime contract.
- The review prompt must be authored as a prompt contract, not as a pile of best-practice bullets.
- The skill must be self-contained; it can say "derive repo-local policy from AGENTS/CLAUDE/README/etc." but cannot depend on `../psmobile` files at runtime.
- Hook support must align with the native-auto-loop plan and must not claim code-review Claude parity until the repo-owned Claude hook path is verified for this skill.
- Verification needs both package checks and at least one realistic review smoke test.

# 3) Research Grounding (external + internal "ground truth")

## 3.1 External anchors (papers, systems, prior art)

- Google Engineering Practices, Code Review:
  - Source: https://google.github.io/eng-practices/review/reviewer/looking-for.html and https://google.github.io/eng-practices/review/reviewer/standard.html.
  - Adopt:
    - Review design, functionality, complexity, tests, naming, comments, style, consistency, documentation, every assigned line, and broader system context.
    - Treat code health as the review standard: approve when the change improves the system overall, but do not accept changes that make the system less maintainable, readable, understandable, or tested.
    - Documentation is part of review scope when a change affects how users build, test, interact with, or release code; deleted or deprecated code should also trigger doc deletion consideration.
    - Review context beyond the diff hunk when needed; a small local edit can expose a larger function, module, or system-level problem.
  - Reject:
    - Do not copy Google-specific CL terminology or require perfection. The skill should keep "improves code health" and "technical facts over preference", but findings must remain changed-code-specific and avoid nit noise.
- Google Engineering Practices, Small CLs:
  - Source: https://google.github.io/eng-practices/review/developer/small-cls.html.
  - Adopt:
    - Review size and scope as quality signals because large changes are harder to review thoroughly and more likely to hide defects.
    - Prefer self-contained changes with related tests; refactor-only work should usually be separated from feature or bug changes when mixing them obscures risk.
    - Horizontal and vertical slicing guidance supports modular encapsulation: shared abstractions and layer boundaries should make changes easier to review, not create speculative frameworks.
  - Reject:
    - Do not bake in line-count thresholds as hard policy. Use size as a risk multiplier that changes the reviewer depth and proof expectations.
- Microsoft Engineering Fundamentals Playbook, Code Review:
  - Source: https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/ and https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/.
  - Adopt:
    - Human review should focus on architectural correctness, functional correctness, changed tests, readability, maintainability, error handling, and scope fit while automation handles nits where possible.
    - Reviewers should read every changed line, inspect surrounding code when context is missing, and avoid blocking on unrelated pre-existing issues.
    - Code-quality review should explicitly cover complexity, single responsibility, unnecessary functionality, graceful error handling, race conditions, security flaws, privacy/PII logging, and sensible tests.
  - Reject:
    - Do not import team-process guidance such as SLA, standup, or workflow metrics into the runtime skill unless a later implementation adds optional PR-process review.
- OWASP Code Review Guide:
  - Source: https://owasp.org/www-project-code-review-guide/.
  - Adopt:
    - Manual code review still matters because automated scanners miss context-sensitive vulnerabilities and weakness patterns.
    - Security review should be risk-triggered by changed code boundaries: auth, input validation, crypto, secrets, deserialization, SSRF, injection, file/network/process execution, logging, privacy, and dependency or infrastructure changes.
  - Reject:
    - Do not turn every review into a broad security audit. Security findings must be tied to the diff, reachable paths, and concrete exploit or data-risk reasoning.
- OpenAI Codex docs:
  - Sources: https://developers.openai.com/api/docs/guides/code-generation and https://developers.openai.com/codex/cli/reference.
  - Adopt:
    - Codex is an OpenAI coding agent for writing, reviewing, and debugging code, and OpenAI currently recommends `gpt-5.4` as a strong default for code work.
    - `codex exec` is the non-interactive/scripted run surface; official docs document the scripted mode and dangerous unsandboxed flag, while local CLI help is the source of truth for exact installed flags.
    - The unsandboxed flag is explicitly dangerous and should only be used inside an externally hardened environment. This plan preserves the user's requested default and the repo's existing pattern, but the skill must document that boundary honestly.
  - Reject:
    - Do not rely solely on hosted docs for exact local CLI syntax. Deep-dive must verify installed `codex --version`, `codex exec --help`, `codex exec review --help`, and the active `~/.codex/config.toml` profile before implementation.
- Claude Code hooks docs:
  - Source: https://code.claude.com/docs/en/hooks.
  - Adopt:
    - Claude hooks are configured through JSON settings and can run command handlers at lifecycle points such as `Stop`.
    - `Stop` hooks can prevent Claude from stopping by returning a blocking decision with a reason, and Stop input includes `cwd`, `transcript_path`, `stop_hook_active`, and the last assistant message.
    - Claude supports skill-scoped hooks, but repo-owned settings-level hooks remain the safer implementation target for this repo's existing native-auto-loop plan.
  - Reject:
    - Do not use Claude's hook agent or prompt type as the reviewer. The user explicitly requires the reviewer identity to remain Codex; Claude may trigger or continue the workflow, but the code-review subprocess must shell out to Codex.

## 3.2 Internal ground truth (code as spec)

- `skills/codex-review-yolo/SKILL.md`:
  - Existing live skill for context-free fresh Codex review.
  - Requires `codex -p yolo`, where the profile carries `gpt-5.4`, `xhigh`, fast tier, and `danger-full-access`.
  - Review prompt must include role/posture, objective, ground truth, claims/completion targets, what to check, tooling hints, and a strict verdict block.
  - Adopt the fresh-review posture and output capture pattern. Do not stretch this skill into the new general reviewer if that would blur triggers.
- `skills/codex-review-yolo/references/prompt-template.md` and `references/verdict-contract.md`:
  - Existing verdict contract: `VERDICT`, `BLOCKING`, `NON-BLOCKING`, and `ACCURACY OF CLAIMS / COMPLETION`.
  - Adopt as a reference shape, but the new `code-review` skill should own a code-review-specific output contract that starts with findings and includes docs/research/subagent coverage.
- Local Codex CLI and profile evidence:
  - `codex --version` reports `codex-cli 0.122.0-alpha.3`.
  - `codex exec --help` supports `--model`, `--profile`, `--sandbox`, `--dangerously-bypass-approvals-and-sandbox`, `--cd`, `--ephemeral`, `--output-schema`, and `-o`.
  - `codex exec review --help` exists for code review but does not expose `--profile` in the local help output; strict yolo/profile behavior should therefore use `codex exec -p yolo` or explicit `--model gpt-5.4 -c model_reasoning_effort="xhigh" --dangerously-bypass-approvals-and-sandbox`.
  - `~/.codex/config.toml` currently defines `[profiles.yolo]` with `model = "gpt-5.4"`, `model_reasoning_effort = "xhigh"`, `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`, and `tool_output_token_limit = 25000`.
- `skills/arch-step/scripts/arch_controller_stop_hook.py`:
  - The current shared dispatcher is runtime-aware and requires `--runtime codex|claude` from the installed hook command.
  - It keeps Codex controller state under `.codex/` and Claude controller state under `.claude/arch_skill/`, with session-scoped filenames and first-stop session claiming for legacy or unsuffixed Claude state.
  - Codex fresh review/audit subprocesses use `codex exec --ephemeral --disable codex_hooks --cd <cwd> --dangerously-bypass-approvals-and-sandbox -o <last_message> <prompt>`.
  - Claude fresh child work for generic auto controllers uses `claude -p --settings '{"disableAllHooks":true}' --output-format json --dangerously-skip-permissions`; the earlier `--bare` approach is rejected because local proof showed it broke auth.
  - Existing miniarch audit constants already use `gpt-5.4-mini` and `xhigh`, matching the requested subagent model/effort.
  - There is no `code-review` controller state spec or handler yet.
  - Adopt the existing Codex invocation style for hook-driven code-review subprocesses, but keep `code-review` as an intentional exception to the generic host-native child-run rule: even from Claude host state, the review subprocess remains Codex.
- `skills/arch-step/scripts/upsert_codex_stop_hook.py`:
  - Existing Codex hook installer verifies exactly one repo-managed Stop hook pointing at `arch_controller_stop_hook.py --runtime codex`.
  - Adopt the "one repo-owned hook dispatcher" architecture rather than adding a second Codex Stop hook for code review.
- `skills/arch-step/scripts/upsert_claude_stop_hook.py`:
  - New local Claude hook installer verifies exactly one repo-managed settings-level `Stop` hook pointing at `arch_controller_stop_hook.py --runtime claude`.
  - It removes stale repo-managed entries and should remain shared, not review-specific.
- `docs/NATIVE_AUTO_LOOPS_FOR_CODEX_AND_CLAUDE_2026-04-19.md`:
  - The native-auto-loop plan and worklog now record completed local generic dual-runtime hook support: install, verify, remote install, runtime-local state, Claude child-run proof, Codex and Claude continuation proof, `delay-poll` proof, and missing-hook fail-loud proof.
  - That plan's generic Claude child-work direction is host-native, but this code-review skill is a deliberate exception: Claude may own hook continuation while the reviewer subprocess remains Codex by product requirement.
  - Implementation must not rework generic hook infrastructure; it must add only the missing `code-review` skill package, runner, state handler, install inventory, and docs.
- `Makefile` and `README.md`:
  - Live inventory currently includes `codex-review-yolo` but not a general `code-review` skill.
  - `Makefile` now owns `CLAUDE_SETTINGS_FILE`, `claude_install_hook`, `verify_claude_install`, and remote Claude hook installation.
  - `CLAUDE_SKILLS` now includes hook-capable skills such as `delay-poll` but still omits `code-review`; `GEMINI_SKILLS` should continue to omit `code-review`.
  - `README.md` and `docs/arch_skill_usage_guide.md` now describe dual-runtime hook install, runtime-local state, and hook-suppressed Claude child runs; adding `code-review` should be an additive docs update, not a broad Codex-only cleanup pass.
  - `npx skills check` is required after skill package changes under `skills/`.
- `../psmobile/scripts/review/render_pr_agent_extra_instructions.py`:
  - Existing PR-Agent hook renders review policy from `.github/claude/repo_review_policy.md` and `.github/claude/partials/spam_guardrails.md`.
  - Runtime generic skill must not depend on `../psmobile`; this file is only a source for extracting portable principles.
- `../psmobile/.github/claude/repo_review_policy.md` and `../psmobile/.github/claude/partials/spam_guardrails.md`:
  - Genericizable review requirements:
    - no duplicate patterns or second paths that can drift
    - no unnecessary feature flags, shims, test-only branches, or hypothetical fallbacks
    - handle platform, SDK, network, auth, storage, process, and other external-boundary failures explicitly
    - keep names, constants, and conditionals self-describing
    - require proof proportional to behavior risk, with real app/simulator/integration automation for integration-shaped changes
    - check user-facing intent, telemetry contracts, stable IDs, docs, comments, instructions, and generated artifacts for drift
    - output only strong changed-code findings with exact paths, symbols, lines, and risk reasoning
  - Non-portable psmobile specifics must stay out of the new skill.
- `skills/audit-loop/SKILL.md`:
  - Provides map-first exhaustive audit doctrine: understand repo topology, proof surface, and risk fronts before edits.
  - Adopt map-first coverage and post-review self-audit, but keep the new skill review-only and findings-first.
- `/Users/aelaguiz/.agents/skills/skill-authoring/SKILL.md`:
  - New skill must have a concrete job-to-be-done, a tight trigger, 2-3 canonical asks, one anti-case, progressive disclosure, and validation.
  - Adopt: keep `SKILL.md` lean, move detailed prompt/review doctrine into references only when it earns reuse.
- `/Users/aelaguiz/.agents/skills/prompt-authoring/SKILL.md`:
  - Reviewer prompt must have one job, explicit success/failure, inputs and ground truth, process, tool rules, quality bar, output contract, and fail-loud behavior.
  - Adopt: design a canonical prompt template rather than embedding a checklist blob in `SKILL.md`.
- `/Users/aelaguiz/.agents/skills/agent-linter/SKILL.md`:
  - Applies to prompts, skill packages, flows, agent definitions, and repo instruction-bearing surfaces.
  - Adopt: when a reviewed project builds agents or edits agent-facing instructions, the review must invoke `$agent-linter` and synthesize its highest-value findings into the code-review output. Do not use it for generic code defects.

## 3.3 Decision gaps that must be resolved before implementation

- None after the external-research and follow-up deep-dive passes.
- Resolved defaults from research:
  - New live skill name: `code-review`.
  - Relationship to `codex-review-yolo`: keep `codex-review-yolo` as the narrower manual fresh-eyes helper and ship `code-review` as a sibling skill.
  - Reviewer invocation: default to explicit fresh Codex `gpt-5.4` `xhigh` unsandboxed execution rather than relying only on a mutable profile.
  - Claude invocation: Claude can install, trigger, and hook-continue the skill through the now-verified shared dispatcher, but the actual code-review subprocess shells out to Codex by requirement.
  - Parallel subreviews: the runner launches separate parallel Codex `gpt-5.4-mini` `xhigh` subprocess review agents for required lens coverage.
  - External research: bundle source-selection and review-principle doctrine, not a static encyclopedia of language rules.
  - Hook infrastructure posture: reuse the completed generic Codex/Claude hook installers and dispatcher; add only a narrow `code-review` state spec and handler.

## 3.4 Implementation verification tasks, not user blockers

- Verify the exact local `codex exec` command that pins `gpt-5.4`, `xhigh`, fresh context, unsandboxed permissions, disabled hooks, working directory, and final-message artifact capture.
- Verify the runner can launch and collect separate parallel Codex `gpt-5.4-mini` `xhigh` subprocess review agents.
- Verify the final `ReviewVerdict` shape in a real smoke run and adjust `skills/code-review/references/output-contract.md` before shipping if the first version is hard to consume.
- Verify hook state ownership in both runtime namespaces: `.codex/code-review-state.<SESSION_ID>.json` and `.claude/arch_skill/code-review-state.<SESSION_ID>.json`.
- Verify an agent-surface target actually triggers `$agent-linter` coverage or fails loud when the skill is unavailable.
- Preserve the already-proven generic hook install and continuation behavior; code-review implementation proof should focus on the new review state path and Codex reviewer shell-out.

## 3.5 Local runtime refresh after Codex/Claude parity work

- Worktree evidence:
  - `Makefile` now installs and verifies both Codex and Claude repo-managed Stop hooks; `code-review` is still absent from `SKILLS`, `CLAUDE_SKILLS`, and `GEMINI_SKILLS`.
  - `skills/arch-step/scripts/upsert_codex_stop_hook.py` now expects the installed command with `--runtime codex`.
  - `skills/arch-step/scripts/upsert_claude_stop_hook.py` exists locally and expects the installed command with `--runtime claude`.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` now has runtime specs, runtime-local state roots, host-native child helpers, and no `code-review` state spec.
  - `README.md` and `docs/arch_skill_usage_guide.md` already describe dual-runtime hook install and state behavior.
  - `docs/NATIVE_AUTO_LOOPS_FOR_CODEX_AND_CLAUDE_2026-04-19_WORKLOG.md` records local proof: Python compile, hook-suppressed Claude probes, `make install`, `make verify_install`, installed hook inspection, Codex and Claude continuation proof, `delay-poll` proof, and missing-hook fail-loud proof. Its `npx skills check` run failed only on an unrelated global `harden` update path, so implementation must rerun it and report the same caveat if it recurs.
- Plan impact:
  - Do not add or redesign generic Codex/Claude hook installers.
  - Do not make `code-review` use Claude-native child review just because generic auto controllers do; this skill has an explicit Codex-reviewer requirement.
  - Keep the remaining work focused on the new skill package, Codex runner, dispatcher state handler, install inventory, additive docs, and code-review-specific smoke proof.

<!-- arch_skill:block:external_research:start -->
# External Research (best-in-class references; plan-adjacent)

> Goal: anchor the code-review skill in broadly accepted review and coding-convention practice without turning it into a static language-style encyclopedia.

## Topics researched (and why)

- Code-review scope and signal quality - the skill must know what high-value review covers and how to avoid noisy checklist output.
- Coding conventions, naming, local consistency, and documentation - the user explicitly asked for generic best practices that cover modular encapsulation, repeated-code drift, self-describing code, and docs staying current.
- Duplication, abstraction, and refactoring safety - the requested reviewer must flag repeat logic that can drift without rewarding premature or obscuring abstractions.
- Proof, tests, and risk-triggered security review - the reviewer must judge proof adequacy and use security guidance only when changed code introduces real risk.
- Codex and Claude hook/runtime behavior - the skill must be hook-friendly for Codex and Claude while keeping Codex as the actual reviewer.

## Findings + how we apply them

### Code-review scope and signal quality

- Best practices (synthesized):
  - Human review should focus on correctness, design, maintainability, readability, tests, and changed behavior while automation handles formatting and low-value nits where possible.
  - Reviewers should inspect every changed line, surrounding code when context is missing, and the PR/task intent; they should not block on unrelated pre-existing issues.
  - Review size and scope are risk multipliers: bigger or mixed-purpose diffs need stronger mapping and proof, not arbitrary line-count rejection.
- Adopt for this plan:
  - The `code-review` prompt must require a repo-grounded map before findings and must keep output sparse, evidence-backed, and changed-code-specific.
  - The reviewer must separate blocking changed-code risks from non-blocking follow-ups and explicitly say when no findings are found.
  - Style-only findings are allowed only when they create real maintainability, readability, convention-drift, or contract risk.
- Reject for this plan:
  - Do not copy team-process guidance such as review SLAs, standup management, or PR ceremony into the skill.
  - Do not impose a global "small diff" policy; treat size as a risk signal that raises audit depth.
- Pitfalls / footguns:
  - A broad checklist can produce false confidence if it causes the reviewer to skim the actual code.
  - Reviewers can overreach by blocking on adjacent technical debt that the change did not introduce or worsen.
- Sources:
  - Google Engineering Practices, Code Review - https://google.github.io/eng-practices/review/reviewer/looking-for.html - authoritative generalized review guidance from Google's public engineering practices.
  - Google Engineering Practices, Small CLs - https://google.github.io/eng-practices/review/developer/small-cls.html - authoritative guidance on why reviewable scope matters.
  - Microsoft Engineering Fundamentals Playbook, Reviewer Guidance - https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/ - authoritative engineering-playbook review checklist.
  - Microsoft Engineering Fundamentals Playbook, Process Guidance - https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/ - authoritative guidance on automation, PR size, and human-review focus.

### Coding conventions, naming, local consistency, and documentation

- Best practices (synthesized):
  - Clarity and local consistency matter more than universal taste. Language/project style should be preferred, then nearby local style, then broader external guidance.
  - Names should make the purpose, role, and important distinctions predictable; confusing conditionals should be extracted or named when the name clarifies behavior.
  - Documentation and comments are live reader-facing surfaces. They should explain why or contract-level usage, stand on their own, and be updated when behavior, build, API, or usage changes.
- Adopt for this plan:
  - The reviewer must derive coding conventions from repo-local evidence first: `AGENTS.md`, `CLAUDE.md`, `README.md`, language config, formatter/linter config, nearby files, and existing idioms.
  - The prompt must explicitly audit docs, comments, examples, install instructions, generated docs, telemetry names, stable IDs, and agent instructions when changed behavior makes them stale.
  - The review should flag convention violations only when they make code harder to read, maintain, refactor, or keep consistent with the surrounding codebase.
- Reject for this plan:
  - Do not ship a baked-in style-guide preference such as one language's naming convention as universal truth.
  - Do not require comments for obvious code; prefer comments and docs for contracts, gotchas, invariants, examples, and non-obvious decisions.
- Pitfalls / footguns:
  - "Consistency" can preserve bad legacy style. If the new change worsens an existing deviation, spreads it to more surfaces, or creates a bug, local consistency is no longer a defense.
  - Documentation review can become doc-policing; it should be tied to changed behavior or live contract drift.
- Sources:
  - Google Go Style Guide - https://google.github.io/styleguide/go/guide - authoritative style principles prioritizing clarity, simplicity, concision, maintainability, and consistency.
  - PEP 8 - https://peps.python.org/pep-0008/ - authoritative Python style guide that explicitly prioritizes project and local consistency.
  - Google Developer Documentation Style Guide - https://developers.google.com/style - authoritative developer-doc style hierarchy that prioritizes project-specific guidance and clarity.
  - Effective Go - https://go.dev/doc/effective_go - authoritative language guidance on comments, doc comments, and naming.

### Duplication, abstraction, and refactoring safety

- Best practices (synthesized):
  - Repeated code is costly when the repeated logic can drift or when readers must compare near-duplicates to find the meaningful differences.
  - Good abstraction makes important distinctions more visible; bad abstraction hides critical edge cases, couples unrelated callers, or adds functionality not presently needed.
  - Refactoring is behavior-preserving work and should be done in small, safe steps with proof proportional to risk.
- Adopt for this plan:
  - The reviewer must flag duplication when a single rule, condition, prompt fragment, schema, command string, policy, or runtime contract is expressed in multiple places that can drift.
  - The reviewer must also flag over-abstracted helpers when they obscure important behavior, hide an edge case, or create a new parallel path.
  - For refactor-heavy changes, the reviewer must require credible preservation evidence such as existing tests, typecheck/build, focused regression tests, or behavior-level smoke checks.
- Reject for this plan:
  - Do not apply "DRY" as a raw line-similarity rule. Similar-looking code can be correct when callers have different reasons to change.
  - Do not force an extraction on the first or second similar instance unless drift risk is concrete and the abstraction is already clear.
- Pitfalls / footguns:
  - "No duplication" can become architecture theater if it creates a generic framework before the system has enough examples to reveal the right abstraction.
  - A helper can make code worse if it hides critical logic or future changes need different behavior per caller.
- Sources:
  - Google Go Style Guide - https://google.github.io/styleguide/go/guide - authoritative guidance on repetitive code, unnecessary abstraction, maintainability, and local consistency.
  - Martin Fowler, Refactoring - https://martinfowler.com/books/refactoring.html - authoritative refactoring reference framing refactoring as small behavior-preserving transformations.
  - Google Engineering Practices, Code Review - https://google.github.io/eng-practices/review/reviewer/looking-for.html - authoritative review guidance on complexity, over-engineering, and tests.

### Proof, tests, and risk-triggered security review

- Best practices (synthesized):
  - Tests and proof should match changed risk: logic, contracts, integration boundaries, user flows, and refactors need different evidence.
  - Security code review is valuable because scanners miss context, but broad security audits should be triggered by changed attack surfaces rather than applied ceremonially to every diff.
  - Secure coding standards are language/platform-specific; the generic skill should route to authoritative language/framework guidance when the changed code touches security-sensitive areas.
- Adopt for this plan:
  - The reviewer must inspect test adequacy, not just test presence. Changed behavior that crosses runtime, network, auth, file, process, SDK, plugin, or UI-boundary seams needs stronger proof than a narrow unit test.
  - Security review should be risk-triggered for auth, authorization, input validation, crypto, secrets, deserialization, SSRF, injection, file/process/network execution, logging, privacy, dependencies, and infrastructure boundaries.
  - If a best-practice finding depends on a current framework/API/security rule, the reviewer must research and cite current authoritative sources.
- Reject for this plan:
  - Do not require a full OWASP or CERT checklist for every ordinary code review.
  - Do not add negative-value proof requirements such as tests that only prove files were deleted, docs inventories, or brittle implementation-detail assertions.
- Pitfalls / footguns:
  - "Tests changed" is not the same as "the risk is covered".
  - Security advice without reachability and changed-code causality becomes noisy and easy to ignore.
- Sources:
  - OWASP Code Review Guide - https://owasp.org/www-project-code-review-guide/ - authoritative application-security review guide emphasizing manual review and vulnerability identification.
  - SEI CERT Coding Standards - https://cmu-sei.github.io/secure-coding-standards/ - authoritative secure-coding standards for common languages and platforms.
  - Microsoft Engineering Fundamentals Playbook, Reviewer Guidance - https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/ - authoritative review guidance covering tests, error handling, complexity, and functionality.

### Codex and Claude hook/runtime behavior

- Best practices (synthesized):
  - Codex `exec` is the non-interactive/scripted run surface, and the unsandboxed bypass is intentionally dangerous and should be used only in hardened environments.
  - Claude hooks support blocking Stop-hook behavior through JSON decisions, making hook continuation feasible, but hook runtime identity should be explicit and repo-owned.
  - Runtime hook parity should not imply reviewer parity: the user can require one runtime to trigger a process whose reviewer is a different runtime.
- Adopt for this plan:
  - The skill must use explicit Codex model and effort where possible: `gpt-5.4` and `model_reasoning_effort="xhigh"`.
  - The skill must use unsandboxed Codex by default because the user requested it and this repo already uses that pattern, while documenting the risk honestly.
  - Claude support must be a trigger/continuation path that shells out to Codex for review. This is an intentional exception to the broader native-Claude child-run direction in the native-auto-loop plan.
- Reject for this plan:
  - Do not ask Claude to perform the final review.
    - Do not claim Claude hook support for `code-review` until the repo-owned Claude hook installer, runtime-aware dispatcher, and code-review state handler are part of the installed surface and verified.
- Pitfalls / footguns:
  - A `codex-review-yolo`-style human-invoked command is not enough for the requested hook-backed skill.
  - A hook that runs a reviewer without state, target, output capture, and fail-loud errors will be expensive and hard to trust.
- Sources:
  - OpenAI Codex CLI reference - https://developers.openai.com/codex/cli/reference - official CLI reference for `codex exec`, `--model`, and the unsandboxed bypass flag.
  - Claude Code Hooks reference - https://code.claude.com/docs/en/hooks - official Claude hook reference for Stop hooks and blocking decision control.

## Adopt / Reject summary

- Adopt:
  - Repo-local convention discovery before external style rules.
  - Findings-first review output, sparse blocking issues, exact evidence, and no placeholder sections.
  - Duplication checks based on drift risk, not raw line similarity.
  - Abstraction checks that reject both copy-paste drift and premature helper/framework extraction.
  - Live docs/comments/instructions/examples/telemetry drift as review scope when behavior changes.
  - Risk-proportional proof and security review, with authoritative external citations only when needed.
  - Explicit Codex `gpt-5.4` `xhigh` unsandboxed review execution, with parallel `gpt-5.4-mini` `xhigh` review lenses.
  - Claude hook support as a trigger that shells out to Codex, not as a Claude reviewer.
- Reject:
  - Static universal language-style doctrine.
  - Line-count or line-similarity gates.
  - Broad security checklists for ordinary changes.
  - Repo-policing tests, docs inventory gates, or absence checks as proof.
  - Hook parity claims that are not backed by installed and verified runtime behavior.

## Decision gaps that must be resolved before implementation

- None. Remaining unknowns are implementation verification tasks: exact local `codex exec` syntax, parallel subprocess artifact shape, and final state-file shape.
<!-- arch_skill:block:external_research:end -->

# 4) Current Architecture (as-is)

<!-- arch_skill:block:current_architecture:start -->
## 4.1 On-disk structure

- Live skill inventory:
  - `skills/codex-review-yolo/` is the only shipped Codex-review-like skill today.
  - `skills/audit-loop/`, `skills/comment-loop/`, and `skills/audit-loop-sim/` own broader audit loops, not ordinary diff/code-review output.
  - There is no `skills/code-review/` package.
- Existing review package shape:
  - `skills/codex-review-yolo/SKILL.md` is a mechanism skill for manual `codex exec -p yolo` fresh reviews.
  - `skills/codex-review-yolo/references/prompt-template.md` owns prompt shape examples.
  - `skills/codex-review-yolo/references/verdict-contract.md` owns a generic verdict footer.
  - `skills/codex-review-yolo/references/troubleshooting.md` owns local `codex` troubleshooting.
- Existing hook/runtime structure in the current worktree:
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` is the shared Stop-hook dispatcher.
  - It now parses `--runtime codex|claude`, keeps Codex state under `.codex/`, keeps Claude state under `.claude/arch_skill/`, and supports multiple controller state specs.
  - `skills/arch-step/scripts/upsert_codex_stop_hook.py` installs/verifies a Codex `Stop` command hook pointing at the installed dispatcher with `--runtime codex`.
  - `skills/arch-step/scripts/upsert_claude_stop_hook.py` exists in the current worktree and installs/verifies a Claude `Stop` command hook pointing at the same dispatcher with `--runtime claude`.
  - `Makefile` currently wires `claude_install_hook`, includes `delay-poll` in `CLAUDE_SKILLS`, and verifies the Claude hook.
- Install and docs surfaces:
  - `Makefile` `SKILLS` includes `codex-review-yolo` but not `code-review`.
  - `CLAUDE_SKILLS` includes `codex-review-yolo` but not `code-review`.
  - `GEMINI_SKILLS` includes `codex-review-yolo`; Gemini support for the new hook-backed review skill is not requested.
  - `README.md` and `docs/arch_skill_usage_guide.md` now describe the generic Codex plus Claude hook contract, but they do not yet list or explain `code-review`.
- Agent-authoring dependencies:
  - `/Users/aelaguiz/.agents/skills/skill-authoring/SKILL.md` and `/Users/aelaguiz/.agents/skills/prompt-authoring/SKILL.md` are external installed authoring references, not repo-local shipped skills.
  - `/Users/aelaguiz/.agents/skills/agent-linter/SKILL.md` is the requested agent-surface audit lens and is not currently shipped in this repo.

## 4.2 Control paths (runtime)

- Manual fresh-review path today:
  - Caller uses `$codex-review-yolo`.
  - The skill instructs the caller to create a namespaced temp run directory, write a prompt, and run `codex exec -p yolo -C <repo-root> -o <final> < prompt.md > stream.log 2>&1`.
  - The child Codex process reads the repo itself and returns a verdict footer.
  - This path is review-only and not hook-backed.
- Hook controller path today:
  - A host Stop hook invokes `arch_controller_stop_hook.py --runtime <host>`.
  - The dispatcher reads a host-specific state namespace, validates session ownership, rejects duplicate active controllers, and dispatches one of the known controller families.
  - Codex fresh child work uses `codex exec --ephemeral --disable codex_hooks --cd <cwd> --dangerously-bypass-approvals-and-sandbox`.
  - Claude fresh child work for generic auto controllers uses `claude -p --settings '{"disableAllHooks":true}' --output-format json --dangerously-skip-permissions`.
- Gap for the requested skill:
  - There is no `code-review` controller state family.
  - There is no runner that performs parallel code-review lenses and final synthesis.
  - The current shared dispatcher can distinguish host runtime, but it does not yet have the explicit code-review exception that shells out to Codex from a Claude-hosted review state.
  - There is no canonical prompt that combines repo-local convention discovery, external best-practice research, psmobile-derived generic review policy, docs-drift checks, and `$agent-linter` handling.

## 4.3 Object model + key abstractions

- Existing controller state pattern:
  - Session-scoped state files use JSON with at least `version`, `command`, `session_id`, and command-specific fields.
  - Current state filenames are derived from controller specs and session IDs, e.g. `.codex/auto-plan-state.<SESSION_ID>.json`.
  - The runtime-aware dispatcher resolves the state root from the installed hook's explicit runtime argument.
  - The same pattern should produce `.codex/code-review-state.<SESSION_ID>.json` and `.claude/arch_skill/code-review-state.<SESSION_ID>.json` once `CODE_REVIEW_STATE_SPEC` exists.
- Existing child-run result pattern:
  - `FreshAuditResult` captures a child process and optional last-message text.
  - `FreshStructuredResult` adds parsed structured JSON.
  - `run_codex_text_child` already supports optional `model` and `model_reasoning_effort`, which is the pattern needed for `gpt-5.4-mini` `xhigh` review lenses.
- Existing review artifact pattern:
  - `codex-review-yolo` uses temp run directories with prompt, stream log, and final output file.
  - The new code-review runner should reuse that artifact discipline rather than dumping long review output into hook stdout.
- Missing object model:
  - `ReviewTarget`: uncommitted diff, commit/range, branch diff, explicit path list, or plan-completion claim.
  - `ReviewRun`: run directory, generated prompt, subreview outputs, synthesis output, stream logs, source list, and coverage metadata.
  - `ReviewLens`: correctness/regression, architecture and duplicate-drift, proof/testing, docs/contracts/user-facing/telemetry, security when risk-triggered, and agent-linter when applicable.
  - `ReviewVerdict`: findings-first verdict with blocking/non-blocking findings, no-findings state, subreview coverage, docs-drift coverage, external-source coverage, and agent-linter coverage.
  - `CodeReviewHookState`: host runtime, session, repo root, target, objective, run directory or output directory, and whether review should run at Stop.

## 4.4 Observability + failure behavior today

- Existing dispatcher failures are fail-loud:
  - invalid state JSON clears or blocks with a clear message
  - duplicate controller states block
  - missing child runtime raises an explicit runtime error
  - child output is summarized into Stop-hook JSON messages with size limits
- Existing review failures in `codex-review-yolo` are manual:
  - caller checks `which codex`, profile config, final output, and stream log
  - malformed verdict requires rerun, not hand-written replacement
- Gap for the requested skill:
  - A hook-backed code-review run needs explicit missing-Codex, malformed-prompt, failed-subreview, missing-agent-linter, malformed verdict, no target, and output-path reporting.
  - The hook must not block indefinitely if review cannot run; it should fail loud with a path to the partial run artifacts.

## 4.5 UI surfaces (ASCII mockups, if UI work)

- Not applicable. This is a CLI/skill/runtime workflow.
<!-- arch_skill:block:current_architecture:end -->

# 5) Target Architecture (to-be)

<!-- arch_skill:block:target_architecture:start -->
## 5.1 On-disk structure (future)

- New skill package:
  - `skills/code-review/SKILL.md`
  - `skills/code-review/references/reviewer-prompt.md`
  - `skills/code-review/references/review-requirements.md`
  - `skills/code-review/references/output-contract.md`
  - `skills/code-review/references/invocation.md`
  - `skills/code-review/scripts/run_code_review.py`
- Runtime integration:
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` gets a `code-review` controller spec and handler that invokes the code-review runner.
  - The handler must work from both Codex and Claude runtime namespaces, but the runner must always launch Codex for the actual review.
  - Existing `upsert_codex_stop_hook.py` and `upsert_claude_stop_hook.py` should not become review-specific; they remain shared hook installers.
- Install/docs:
  - Add `code-review` to `SKILLS` and `CLAUDE_SKILLS`.
  - Do not add it to `GEMINI_SKILLS`; Gemini invocation is outside this plan.
  - Update `README.md` and `docs/arch_skill_usage_guide.md` to list the skill, explain Codex-as-reviewer behavior, and preserve the already-current generic Codex plus Claude hook truth.

## 5.2 Control paths (future)

- Direct review path:
  - User invokes `$code-review` from Codex or Claude.
  - The skill resolves a review target from explicit input or defaults to the current repo diff when that is unambiguous.
  - The runner creates a namespaced run directory, launches parallel `gpt-5.4-mini` `xhigh` Codex review agents for independent lenses, then launches a final `gpt-5.4` `xhigh` Codex synthesis reviewer.
  - The final output is a findings-first review report captured to disk and summarized back to the caller.
- Hook-backed review path:
  - User arms a code-review state for the current session and target.
  - Codex Stop hook reads `.codex/code-review-state.<SESSION_ID>.json`; Claude Stop hook reads `.claude/arch_skill/code-review-state.<SESSION_ID>.json`.
  - The shared dispatcher invokes `skills/code-review/scripts/run_code_review.py`.
  - The runner shells out to Codex even when the host runtime is Claude.
  - The hook blocks the stop only long enough to run or fail the review, then reports the review artifact path and verdict summary.
- Parallel review path:
  - The runner launches separate parallel `codex exec --model gpt-5.4-mini -c model_reasoning_effort="xhigh"` subprocess review agents for each required review lens.
  - The final reviewer consumes the required subprocess lens artifacts and must not substitute an unverified native fan-out path for them.
  - Silent downgrade is forbidden. If required parallel subprocess fan-out fails, the review fails coverage rather than claiming exhaustive review.

## 5.3 Object model + abstractions (future)

- `ReviewTarget`:
  - `mode`: `uncommitted-diff`, `branch-diff`, `commit-range`, `paths`, or `completion-claim`
  - `base`, `head`, `paths`, and `objective` when applicable
  - resolved repo root and relevant git metadata
- `ReviewRun`:
  - run ID and run directory
  - primary prompt
  - per-lens prompts and outputs
  - final synthesis output
  - stream logs
  - source URLs used by the reviewer
  - coverage summary
- `ReviewLens`:
  - correctness/regressions
  - architecture, modularity, encapsulation, and duplicate-drift
  - tests/proof/automation adequacy
  - docs/comments/instructions/examples/telemetry/user-facing contract drift
  - risk-triggered security/privacy
  - agent-linter for agent, prompt, skill, flow, or instruction-bearing surfaces
- `ReviewVerdict`:
  - `VERDICT: approve | approve-with-notes | not-approved`
  - blocking findings
  - non-blocking findings
  - no-findings statement when applicable
  - coverage notes for external research, docs drift, subreviews, and agent-linter
- `CodeReviewHookState`:
  - `version`
  - `command: "code-review"`
  - `session_id`
  - `repo_root`
  - `target`
  - `objective`
  - `run_dir` or output root

## 5.4 Invariants and boundaries

- The reviewer is always a fresh Codex child process using `gpt-5.4` `xhigh`.
- The default Codex review execution is unsandboxed, using the repo's dangerous-bypass pattern, and must document that this is intentionally unsafe outside hardened local environments.
- The caller model can prepare, arm, or relay the review, but it cannot replace the Codex review verdict.
- The skill is review-only. It does not fix code and does not ask the Codex reviewer to fix code.
- Repo-local instructions and existing code patterns outrank generic external advice.
- External research is used only for current best-practice claims, framework/API/security behavior, or runtime docs; it must cite authoritative sources.
- Review output is findings-first and sparse. No placeholder sections, no "None." filler, no style-only nits unless they create material risk.
- Documentation drift is mandatory review scope when behavior, commands, install paths, APIs, examples, comments, prompts, telemetry, or user-facing contracts change.
- Agent-linter is mandatory only when the target actually includes agent-building or instruction-bearing surfaces. If required and unavailable, the review must report a coverage failure.

## 5.5 UI surfaces (ASCII mockups, if UI work)

- Not applicable.
<!-- arch_skill:block:target_architecture:end -->

# 6) Call-Site Audit (exhaustive change inventory)

<!-- arch_skill:block:call_site_audit:start -->
## Change map (table)

| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| ---- | ---- | ------------------ | ---------------- | --------------- | --- | ------------------ | -------------- |
| Skill package | `skills/code-review/SKILL.md` | New skill | Missing | Add lean `code-review` skill using `skill-authoring` and `prompt-authoring` doctrine | Owns the user-facing review contract | `$code-review` reviews code by shelling out to Codex | `npx skills check` |
| Review prompt | `skills/code-review/references/reviewer-prompt.md` | Canonical reviewer prompt | Missing | Add prompt contract for map-first review, external research, parallel lenses, docs drift, and agent-linter | Prevents parallel prompt drift | One canonical prompt template | `npx skills check`; smoke review |
| Review requirements | `skills/code-review/references/review-requirements.md` | Generic review doctrine | Missing | Add genericized requirements from psmobile plus external research adoption rules | Avoids runtime dependency on `../psmobile` while preserving reusable policy | Requirements reference used by prompt and runner | `npx skills check`; doc re-read |
| Output contract | `skills/code-review/references/output-contract.md` | Findings/verdict schema | Missing | Add findings-first output contract with coverage notes | Makes review consumable and fail-loud | `VERDICT`, findings, coverage, no-findings state | Smoke review validates shape |
| Invocation docs | `skills/code-review/references/invocation.md` | Codex CLI and hook behavior | Missing | Document direct and hook-backed invocation, run artifacts, and failure behavior | Keeps runtime details out of always-on `SKILL.md` | Codex `gpt-5.4` `xhigh` unsandboxed by default | Command/path truth via `rg` |
| Runner | `skills/code-review/scripts/run_code_review.py` | New deterministic runner | Missing | Add runner that resolves target, builds prompts, launches parallel mini review agents, runs final Codex synthesis, captures artifacts, and exits fail-loud | Shell-out, artifacts, and parallel subprocess fan-out are deterministic complexity that earns a script | CLI callable by skill and hook dispatcher | `python3 -m py_compile`; smoke review |
| Hook dispatcher | `skills/arch-step/scripts/arch_controller_stop_hook.py` | Controller specs and handlers | No code-review state or handler | Add `code-review` controller spec and handler that invokes the runner from Codex or Claude runtime namespaces | Reuses one shared Stop-hook dispatcher instead of adding a second hook | `.codex/code-review-state.<SESSION_ID>.json`; `.claude/arch_skill/code-review-state.<SESSION_ID>.json` | `python3 -m py_compile`; hook smoke |
| Codex hook installer | `skills/arch-step/scripts/upsert_codex_stop_hook.py` | Shared Codex Stop hook | Already installs shared dispatcher | Preserve; change only if current runtime-aware command or verification needs repair | Avoid review-specific hook installer drift | One repo-managed Codex Stop hook remains | `make verify_install` if install changes |
| Claude hook installer | `skills/arch-step/scripts/upsert_claude_stop_hook.py` | Shared Claude Stop hook | Exists in current worktree | Preserve; change only if review state needs installer awareness, which should not be necessary | Code-review should reuse generic Claude Stop hook | One repo-managed Claude Stop hook remains | `make verify_install` if install changes |
| Install inventory | `Makefile` | `SKILLS`, `CLAUDE_SKILLS`, `GEMINI_SKILLS` | `code-review` absent | Add `code-review` to `SKILLS` and `CLAUDE_SKILLS`; keep it out of `GEMINI_SKILLS` | Requested runtimes are Codex and Claude; reviewer requires local Codex | Installed to agents/Codex and Claude | `npx skills check`; `make verify_install` when install changes |
| README inventory | `README.md` | Skill list and install/runtime docs | Dual-runtime hook docs are current; `code-review` is missing | Add `code-review` and describe Codex-as-reviewer behavior without duplicating detailed prompt doctrine | New skill/routing/install behavior must be documented | Public usage and install contract | Re-read; `rg` commands/paths |
| Usage guide | `docs/arch_skill_usage_guide.md` | Skill selection and install docs | Dual-runtime hook docs are current; `code-review` is missing | Add `code-review` and explain when to use it versus `codex-review-yolo` | Prevents docs drift from new skill and current native-loop work | Usage docs explain Codex-as-reviewer from Claude | Re-read; `rg` commands/paths |
| Existing review helper | `skills/codex-review-yolo/*` | Manual fresh-eyes helper | Mechanism-focused manual review | Keep as a separate narrow helper; reuse only small compatible output-shape ideas without importing duplicate doctrine | Avoid breaking existing review workflow | `codex-review-yolo` remains manual second-opinion skill | `npx skills check` |
| Audit-loop skills | `skills/audit-loop/*`, `skills/comment-loop/*`, `skills/audit-loop-sim/*` | Broader audit loops | Not ordinary code review | Do not fold into `code-review`; reference only for map-first/parallel audit doctrine | Avoid scope bleed and duplicate controllers | Separate skills remain separate | None unless touched |
| Agent-linter integration | installed `/Users/aelaguiz/.agents/skills/agent-linter/SKILL.md` | Agent-surface audit lens | Installed outside repo, not shipped here | Runner/prompt must invoke it when target is agent-building; fail coverage if unavailable | User explicitly required this lens | Agent-project review includes agent-linter coverage | Agent-surface smoke review |

## Migration notes

* Canonical owner path / shared code path:
  * `skills/code-review/` owns review doctrine, prompt, output contract, and deterministic runner.
  * `skills/arch-step/scripts/arch_controller_stop_hook.py` remains the shared hook dispatcher and only gets a narrow `code-review` state handler.
* Deprecated APIs (if any):
  * None. `codex-review-yolo` stays live as a manual independent-review helper.
* Delete list (what must be removed; include superseded shims/parallel paths if any):
  * Delete no existing skill as part of this plan.
  * Do not add a second Codex or Claude Stop hook. Any review-specific hook path would be a duplicate runtime surface and should be rejected.
  * If implementation creates temporary prompt drafts outside `skills/code-review/references/`, remove them before completion.
* Adjacent surfaces tied to the same contract family:
  * `README.md`
  * `docs/arch_skill_usage_guide.md`
  * `Makefile`
  * `skills/arch-step/scripts/arch_controller_stop_hook.py`
  * `skills/arch-step/scripts/upsert_codex_stop_hook.py`
  * `skills/arch-step/scripts/upsert_claude_stop_hook.py`
  * `skills/codex-review-yolo/*`
  * installed `/Users/aelaguiz/.agents/skills/agent-linter/SKILL.md`
* Compatibility posture / cutover plan:
  * Additive new skill.
  * Preserve `codex-review-yolo` behavior.
  * Reuse the existing shared Stop-hook dispatcher.
  * No runtime fallback or shim is approved. If Codex is unavailable, review fails loud.
* Capability-replacing harnesses to delete or justify:
  * No model-replacing harness is allowed.
  * The runner is justified only for deterministic target resolution, artifact capture, hook state, required parallel subprocess fan-out, and fail-loud orchestration.
  * Review judgment remains in Codex prompts and child agents.
* Live docs/comments/instructions to update or delete:
  * Update `README.md` skill inventory and usage docs.
  * Update `docs/arch_skill_usage_guide.md` skill inventory and usage docs.
  * If touched, preserve the current Codex plus Claude hook install truth and add only the `code-review`-specific exception where needed.
  * Add concise comments in new runner only where they explain non-obvious runtime boundaries.
* Behavior-preservation signals for refactors:
  * `python3 -m py_compile skills/code-review/scripts/run_code_review.py skills/arch-step/scripts/arch_controller_stop_hook.py`
  * `npx skills check`
  * `make verify_install` if Makefile install surfaces are changed
  * Direct smoke review on a small diff and an agent-surface diff

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)

| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude/blocker question) |
| ---- | ------------- | ---------------- | ---------------------- | ------------------------------------- |
| Fresh Codex invocation | `skills/arch-step/scripts/arch_controller_stop_hook.py::run_codex_text_child` | Explicit `codex exec --ephemeral --disable codex_hooks --dangerously-bypass-approvals-and-sandbox` with optional model/effort | Prevents a second inconsistent Codex shell-out path | include |
| Manual review artifacts | `skills/codex-review-yolo/SKILL.md` | Namespaced run directory with prompt, stream log, and final output | Prevents clobbered or untraceable review runs | include |
| Verdict shape | `skills/codex-review-yolo/references/verdict-contract.md` | Structured verdict footer, adapted for code review coverage | Prevents narrative-only reviews | include |
| Hook installer ownership | `upsert_codex_stop_hook.py`, `upsert_claude_stop_hook.py` | One repo-managed hook per runtime, shared dispatcher | Prevents duplicate Stop hook drift | include |
| Runtime state ownership | `arch_controller_stop_hook.py` state specs | Session-scoped state under runtime-specific root | Prevents cross-session/controller collisions | include |
| Agent-surface review | `/Users/aelaguiz/.agents/skills/agent-linter/SKILL.md` | Use agent-linter only for agent/prompt/skill/flow/instruction-bearing surfaces | Prevents generic code review from becoming agent-definition lint noise | include |
| Generic code audit loops | `skills/audit-loop/*` | Map-first audit doctrine only, not controller reuse | Prevents `code-review` from becoming repo-wide audit-loop scope | defer |
| Gemini runtime | `GEMINI_SKILLS` | No hook-backed support until explicitly requested and verified | Prevents unsupported runtime claims | exclude |
<!-- arch_skill:block:call_site_audit:end -->

<!-- arch_skill:block:phase_plan:start -->
# 7) Depth-First Phased Implementation Plan (authoritative)

WORKLOG_PATH: `docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19_WORKLOG.md`

> Rule: systematic build, foundational first; split Section 7 into the best sequence of coherent self-contained units, optimizing for phases that are fully understood, credibly testable, compliance-complete, and safe to build on later. If two decompositions are both valid, bias toward more phases than fewer. `Work` explains the unit and is explanatory only for modern docs. `Checklist (must all be done)` is the authoritative must-do list inside the phase. `Exit criteria (all required)` names the exhaustive concrete done conditions the audit must validate. Resolve adjacent-surface dispositions and compatibility posture before writing the checklist. Before a phase is valid, run an obligation sweep and move every required promise from architecture, call-site audit, migration notes, delete lists, verification commitments, docs/comments propagation, approved bridges, and required helper follow-through into `Checklist` or `Exit criteria`. The authoritative checklist must name the actual chosen work, not unresolved branches or "if needed" placeholders. Refactors, consolidations, and shared-path extractions must preserve existing behavior with credible evidence proportional to the risk. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly. Prefer programmatic checks per phase; defer manual verification to finalization. Avoid negative-value tests and heuristic gates such as deletion checks, keyword absence checks, or repo-shape policing. Document new runtime boundaries in code comments only where the invariant would otherwise be easy to break.

## Phase 1 - Author the canonical `code-review` skill package

Status: CODE-COMPLETE (implement-loop 2026-04-19; see `docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19_WORKLOG.md` → Phase 1)

* Goal:
  * Establish one self-contained skill package that owns the user-facing review contract, prompt doctrine, review requirements, output contract, and invocation guidance.

* Work:
  * Create `skills/code-review/` as the canonical owner for general code review. Keep `SKILL.md` lean and move detailed reusable doctrine into references so the runtime surface stays trigger-accurate and maintainable.

* Checklist (must all be done):
  * Create `skills/code-review/SKILL.md` using the `$skill-authoring` quality bar: concrete job, tight triggers, 2-3 canonical asks, one clear anti-case, progressive disclosure, fail-loud boundaries, and validation.
  * Create `skills/code-review/references/reviewer-prompt.md` using the `$prompt-authoring` quality bar: one job, success and failure conditions, authoritative inputs, tool rules, map-first process, quality bar, output contract, and explicit fail-loud cases.
  * Create `skills/code-review/references/review-requirements.md` with portable requirements genericized from `../psmobile` and the external research in Section 3, with no runtime dependency on `../psmobile`.
  * Create `skills/code-review/references/output-contract.md` with a findings-first verdict shape, coverage notes, no-findings state, malformed-output failure behavior, and no placeholder sections.
  * Create `skills/code-review/references/invocation.md` with direct review, hook-backed review, run-artifact, default model, default reasoning-effort, and unsandboxed Codex behavior.
  * Encode that the reviewer is always fresh Codex `gpt-5.4` `xhigh` and unsandboxed by default.
  * Encode that Claude may trigger or continue the review but cannot be the reviewer.
  * Encode that agent, prompt, skill, flow, or instruction-bearing targets must run `$agent-linter` and incorporate its highest-value findings.
  * Keep `codex-review-yolo` as a separate manual fresh-eyes helper; do not fold it into the new skill or duplicate its whole prompt doctrine.

* Verification (required proof):
  * Re-read every new `skills/code-review/` markdown file end to end.
  * Run `npx skills check`.
  * Use `rg` to verify `../psmobile` appears only in this plan or development notes, not as a runtime dependency inside the shipped `code-review` skill package.

* Docs/comments (propagation; only if needed):
  * No public inventory docs move in this phase. The skill package itself may reference deeper files inside its own `references/` directory.

* Exit criteria (all required):
  * `skills/code-review/` exists with `SKILL.md`, `reviewer-prompt.md`, `review-requirements.md`, `output-contract.md`, and `invocation.md`.
  * The package is self-contained and can be understood without `../psmobile`.
  * The prompt and requirements have one canonical owner path and do not create parallel review doctrine in `README.md`, `Makefile`, or `codex-review-yolo`.
  * `npx skills check` passes for the new package.

* Rollback:
  * Remove the incomplete `skills/code-review/` package as a unit and leave `codex-review-yolo` untouched.

## Phase 2 - Implement the deterministic Codex review runner

Status: CODE-COMPLETE (implement-loop 2026-04-19; see `docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19_WORKLOG.md` → Phase 2)

* Goal:
  * Add the minimum deterministic runner needed for target resolution, artifact capture, Codex shell-out, parallel lens execution, final synthesis, and fail-loud coverage accounting.

* Work:
  * Implement `skills/code-review/scripts/run_code_review.py` as orchestration glue, not as the reviewer. Review judgment stays in the Codex prompts; the script owns repeatable process, artifacts, subprocess fan-out, and failure reporting.

* Checklist (must all be done):
  * Add a CLI in `skills/code-review/scripts/run_code_review.py` that accepts repo root, review target, objective, output root or run directory, host runtime, and hook/session metadata.
  * Resolve review targets for uncommitted diff, branch diff, commit range, explicit paths, and completion-claim review.
  * Create a namespaced run directory containing prompts, per-lens outputs, stream logs, final synthesis output, coverage metadata, and failure reports.
  * Build per-lens review prompts from the canonical references rather than embedding a second review checklist in Python.
  * Launch parallel `gpt-5.4-mini` `xhigh` Codex review lenses for correctness/regression, architecture and duplicate-drift, tests/proof, docs/contracts/user-facing drift, risk-triggered security/privacy, and agent-linter when applicable.
  * Launch separate parallel `codex exec` subprocess review agents for every required lens.
  * Fail loudly when required parallel subprocess fan-out cannot provide the required review coverage.
  * Launch final fresh Codex `gpt-5.4` `xhigh` synthesis with unsandboxed execution and disabled recursive hooks.
  * Ensure the runner never asks Claude, Gemini, or the host model to perform the final review.
  * Ensure the runner is review-only and never edits the target repo.
  * Record external-source coverage when a best-practice, framework, API, security, or runtime claim depends on current research.
  * Detect agent-project targets and require `$agent-linter` coverage; report a coverage failure when it is required but unavailable.
  * Fail loudly for missing Codex, ambiguous target, unsupported target mode, child process failure, missing lens output, malformed final verdict, and missing required coverage.

* Verification (required proof):
  * Run `python3 -m py_compile skills/code-review/scripts/run_code_review.py`.
  * Run the runner against a small local no-findings target and confirm it writes the expected artifact tree and final verdict.
  * Run the runner against a seeded duplicate or docs-drift target and confirm it produces one evidence-backed finding.
  * Run the runner against an agent-surface target and confirm `$agent-linter` coverage is present or the run fails loudly.

* Docs/comments (propagation; only if needed):
  * Add succinct comments only at non-obvious boundaries: unsandboxed Codex invocation, hook-recursion prevention, and parallel lens fan-out.

* Exit criteria (all required):
  * The runner can be called directly from a repo root and produces durable review artifacts.
  * The final reviewer is Codex `gpt-5.4` `xhigh`.
  * Every required subreview lens runs on Codex `gpt-5.4-mini` `xhigh` or the review fails loudly.
  * The runner has no code-fixing path and does not mutate the reviewed repo.
  * Required docs-drift, external-research, and agent-linter coverage is visible in the final verdict.

* Rollback:
  * Remove the runner and its script references from the skill package; keep Phase 1 markdown intact only if it no longer claims a runnable path.

## Phase 3 - Integrate hook-backed review through the shared dispatcher

Status: CODE-COMPLETE (implement-loop 2026-04-19; see `docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19_WORKLOG.md` → Phase 3)

* Goal:
  * Let Codex and Claude host runtimes trigger the same review runner through the already-shipped shared Stop-hook dispatcher without adding or redesigning generic hook infrastructure.

* Work:
  * Add a narrow `code-review` controller family to `skills/arch-step/scripts/arch_controller_stop_hook.py` that reads runtime-specific state, invokes the code-review runner, and reports the artifact path plus verdict summary.

* Checklist (must all be done):
  * Add a `code-review` state spec and handler to `skills/arch-step/scripts/arch_controller_stop_hook.py`.
  * Use `.codex/code-review-state.<SESSION_ID>.json` for Codex host sessions.
  * Use `.claude/arch_skill/code-review-state.<SESSION_ID>.json` for Claude host sessions.
  * Define `CodeReviewHookState` fields for version, command, session ID, repo root, target, objective, output root or run directory, and trigger metadata.
  * Invoke `skills/code-review/scripts/run_code_review.py` from the handler for both Codex and Claude host runtimes.
  * Ensure the handler always invokes Codex for the actual review, including when `--runtime claude` is the host runtime.
  * Document this as the explicit exception to generic host-native child execution: generic Claude auto-controller children stay Claude-native, but code-review shells out to Codex.
  * Preserve existing controller families and duplicate-controller/session-validation behavior.
  * Preserve the existing shared Codex and Claude hook installers; do not add a second Codex or Claude Stop hook.
  * Make invalid state, missing runner, failed runner, and malformed runner summary fail loudly with artifact paths where available.

* Verification (required proof):
  * Run `python3 -m py_compile skills/code-review/scripts/run_code_review.py skills/arch-step/scripts/arch_controller_stop_hook.py`.
  * Run a synthetic Codex-state handler probe that resolves `.codex/code-review-state.<SESSION_ID>.json`.
  * Run a synthetic Claude-state handler probe that resolves `.claude/arch_skill/code-review-state.<SESSION_ID>.json`.
  * Confirm no second Stop hook entry is required in either installer.

* Docs/comments (propagation; only if needed):
  * Add a short dispatcher comment at the intentional exception: Claude is allowed to host the hook, but the review subprocess must remain Codex.

* Exit criteria (all required):
  * A Codex Stop hook can trigger the code-review runner from Codex state.
  * A Claude Stop hook can trigger the same runner from Claude state.
  * Both host runtimes preserve Codex as the reviewer.
  * No review-specific hook installer or duplicate Stop hook exists.
  * Existing arch-step controller behavior remains preserved.

* Rollback:
  * Remove only the `code-review` controller spec and handler; leave unrelated shared dispatcher and installer behavior intact.

## Phase 4 - Publish install inventory and live docs truth

Status: CODE-COMPLETE (implement-loop 2026-04-19; see `docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19_WORKLOG.md` → Phase 4)

* Goal:
  * Make installed skill inventories and public docs match the new supported runtime story without claiming unsupported Gemini behavior.

* Work:
  * Wire `code-review` into the supported Codex/agents and Claude install surfaces, then update live docs that users rely on for skill selection, installation, hooks, and runtime expectations.

* Checklist (must all be done):
  * Add `code-review` to `Makefile` `SKILLS`.
  * Add `code-review` to `Makefile` `CLAUDE_SKILLS`.
  * Keep `code-review` out of `GEMINI_SKILLS`.
  * Update `README.md` skill inventory, install behavior, and hook behavior for the new code-review skill.
  * Update `docs/arch_skill_usage_guide.md` skill-selection and runtime guidance for `$code-review`.
  * Ensure docs state that Claude support shells out to Codex and does not make Claude the reviewer.
  * Ensure docs state that default review execution is unsandboxed Codex `gpt-5.4` `xhigh`.
  * Ensure docs state that `codex-review-yolo` remains the manual fresh-eyes helper and is not replaced.
  * Preserve the already-current generic Codex plus Claude hook truth and add only the `code-review`-specific runtime exception.

* Verification (required proof):
  * Run `npx skills check`.
  * If `npx skills check` fails on the known unrelated global `harden` update-path issue recorded in the native-loop worklog, record that caveat plainly and verify no local `code-review` package failure is present.
  * Run `make verify_install`.
  * Re-read `README.md`, `docs/arch_skill_usage_guide.md`, and the touched `Makefile` sections.
  * Use `rg` to verify documented commands, skill names, state paths, and script paths.

* Docs/comments (propagation; only if needed):
  * This phase is the public-doc propagation phase; do not add separate docs beyond the existing README and usage guide unless implementation discovers a real reader need.

* Exit criteria (all required):
  * `code-review` installs for Codex/agents and Claude.
  * `code-review` is not advertised or installed for Gemini.
  * Public docs and Makefile inventory agree on skill availability and runtime behavior.
  * Public docs do not create a second source of truth for the detailed reviewer prompt.

* Rollback:
  * Remove `code-review` from install inventories and public docs together if the runtime path is not ready to ship.

## Phase 5 - Prove review behavior and failure modes

Status: PARTIAL (implement-loop 2026-04-19; see `docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19_WORKLOG.md` → Phase 5 for the recorded programmatic proof, fail-loud probes, hook-backed synthetic probes, live-smoke status, and honest caveats about which live-review checklist items were deferred)

* Goal:
  * Verify that the shipped skill produces high-signal review output, records coverage honestly, and fails loudly instead of silently downgrading review depth.

* Work:
  * Run representative direct and hook-backed reviews that exercise no-findings, real-findings, docs-drift, parallel-lens, external-research, and agent-linter paths.

* Checklist (must all be done):
  * Run a direct review on a small target expected to produce no findings.
  * Run a direct review on a seeded duplicate-code or duplicate-doctrine target expected to produce a drift finding.
  * Run a direct review on a seeded docs/comment/instruction drift target expected to produce a docs-drift finding.
  * Run an agent-surface review and confirm `$agent-linter` coverage is present in the final synthesis.
  * Run a Codex hook-backed review from `.codex/code-review-state.<SESSION_ID>.json`.
  * Run a Claude hook-backed review from `.claude/arch_skill/code-review-state.<SESSION_ID>.json` and confirm the reviewer subprocess is Codex.
  * Confirm missing Codex, ambiguous target, unavailable required agent-linter, failed subreview, and malformed final verdict all fail loudly.
  * Confirm all review runs write prompt, stream log, final output, and coverage artifacts.

* Verification (required proof):
  * `npx skills check`
  * `python3 -m py_compile skills/code-review/scripts/run_code_review.py skills/arch-step/scripts/arch_controller_stop_hook.py`
  * `make verify_install`
  * Direct review smoke artifacts for no-findings, seeded finding, and agent-surface cases
  * Hook-backed smoke artifacts for Codex and Claude host runtimes

* Docs/comments (propagation; only if needed):
  * Update the skill invocation reference or public docs in the same phase if smoke testing changes the actual command, state path, artifact layout, or support matrix.

* Exit criteria (all required):
  * Direct review behavior is proven for no-findings, seeded findings, docs drift, and agent-surface coverage.
  * Hook-backed review behavior is proven from Codex and Claude host runtimes.
  * Parallel `gpt-5.4-mini` `xhigh` coverage is either present or the run fails loudly.
  * The final synthesis output matches `output-contract.md`.
  * Failure modes are observable and leave enough artifact context to debug.

* Rollback:
  * If review quality or runtime proof fails materially, remove hook exposure and install inventory while preserving any self-contained prompt/package work that remains truthful.

## Phase 6 - Final preservation and implementation-readiness audit

Status: CODE-COMPLETE (implement-loop 2026-04-19; see `docs/CODEX_HOOKED_GENERAL_CODE_REVIEW_SKILL_2026-04-19_WORKLOG.md` → Phase 6 for the recorded re-read pass, `rg` preservation sweeps, `npx skills check` + `make verify_install` final results, and the live Codex smoke verdict that confirmed the dispatcher-to-Codex path)

* Goal:
  * Close drift risks before handoff to implementation audit or docs cleanup.

* Work:
  * Re-read the shipped surfaces as one system and remove any temporary, duplicate, or stale truth that would undermine the new skill.

* Checklist (must all be done):
  * Re-read `skills/code-review/`, `skills/codex-review-yolo/`, `skills/arch-step/scripts/arch_controller_stop_hook.py`, `Makefile`, `README.md`, and `docs/arch_skill_usage_guide.md`.
  * Confirm there is one canonical detailed review prompt owner: `skills/code-review/references/reviewer-prompt.md`.
  * Confirm `codex-review-yolo` still works as a manual fresh-review helper and is not silently repurposed.
  * Remove temporary prompt drafts, scratch run instructions, or duplicate review doctrine created during implementation.
  * Confirm touched docs, comments, examples, and install instructions describe current behavior.
  * Confirm no shipped skill depends on archived command files or `../psmobile` at runtime.
  * Record any implementation deviations or proof gaps in the plan/worklog before calling the work complete.

* Verification (required proof):
  * `npx skills check`
  * `make verify_install`
  * `rg` for duplicated prompt owner text, stale `../psmobile` runtime dependencies, stale unsupported Gemini claims, and stale code-review runtime claims in touched files

* Docs/comments (propagation; only if needed):
  * Fold only durable user-facing truth into `README.md`, `docs/arch_skill_usage_guide.md`, or the owning skill references; do not add a new standalone doc for implementation history.

* Exit criteria (all required):
  * No duplicate code-review prompt doctrine exists outside the owning skill references.
  * No unsupported runtime claim remains in touched live docs.
  * No temporary artifacts or scratch prompts remain in shipped surfaces.
  * Verification proof is recorded and any skipped proof is explicitly explained.

* Rollback:
  * Revert only the final cleanup edits that proved inaccurate; do not undo already verified runtime or skill-package work.
<!-- arch_skill:block:phase_plan:end -->

# 8) Verification Strategy (common-sense; non-blocking)

- Package integrity:
  - run `npx skills check` after adding or changing files under `skills/`.
  - if `npx skills check` repeats the known unrelated global `harden` path failure from the native-loop worklog, report that exact caveat and still confirm the local `code-review` package did not introduce a package-check failure.
- Install behavior:
  - run `make verify_install` after adding `code-review` to install inventories or changing hook install behavior.
- Command/path truth:
  - use `rg` to verify every documented command, skill name, and script path added to docs.
- Runtime smoke tests:
  - run `python3 -m py_compile skills/code-review/scripts/run_code_review.py skills/arch-step/scripts/arch_controller_stop_hook.py` after the runner and dispatcher are present.
  - preserve the already-proven generic Codex/Claude hook installer behavior; new smoke proof should focus on the `code-review` state handler and Codex reviewer shell-out.
  - verify `codex` exists and the intended `gpt-5.4` `xhigh` unsandboxed invocation works from a real repo root.
  - verify Claude Code invocation shells out to Codex for review and does not use Claude as the reviewer.
  - verify failure is loud when Codex is unavailable, hook state is absent, or required parallel subprocess fan-out cannot run.
- Review-quality smoke tests:
  - run a small diff review that should produce no findings.
  - run a seeded duplication or docs-drift diff that should produce one clear finding.
  - run an agent-surface review that must invoke `$agent-linter`.

# 9) Rollout / Ops / Telemetry

- This is a local skill/runtime feature; no product telemetry is expected.
- Rollout is install-surface-driven:
  - generic Codex plus Claude Stop-hook infrastructure is already locally installed and verified by the native-loop worklog; do not re-roll it as part of `code-review`.
  - update `SKILLS` and `CLAUDE_SKILLS`; leave `GEMINI_SKILLS` unchanged for this feature.
  - update README inventory and usage docs in the same implementation if a new skill ships.
  - do not claim `code-review` Claude hook support until the Claude host path shells out to Codex and is verified.
- Failure behavior must be visible:
  - missing Codex binary
  - missing model/profile support
  - unsupported parallel subprocess fan-out
  - missing or unavailable agent-linter when an agent-surface review requires it
  - missing hook install
  - failed child review process
  - ambiguous or malformed verdict

<!-- arch_skill:block:consistency_pass:start -->
## Consistency Pass
- Reviewers: self-integrator same-session cold read
- Scope checked:
  - frontmatter, TL;DR, planning passes, Sections 0-10, external research block, target architecture, call-site audit, phase plan, verification, rollout, and decision log
- Findings summary:
  - The latest local Codex/Claude runtime work changed the baseline: shared dual-runtime Stop-hook installation, runtime-local state, host-native generic child execution, and generic controller proof are now complete local truth.
  - The remaining `code-review` work is additive: new skill package, deterministic Codex runner, narrow dispatcher state handler, install inventory, docs, and code-review-specific smoke proof.
  - The only intentional runtime asymmetry is now explicit: generic Claude auto-controller child work stays Claude-native, but `code-review` shells out to Codex from both Codex and Claude hosts because the reviewer must always be Codex.
- Integrated repairs:
  - Added the local runtime refresh to the planning-pass bookkeeping and Section 3.
  - Updated Sections 1 through 6 to treat generic Codex/Claude hook support as already shipped and verified, not as future code-review scope.
  - Tightened Section 7 so Phase 3 reuses existing hook infrastructure and Phase 4 performs additive `code-review` docs/inventory updates instead of broad hook-doc cleanup.
  - Updated Section 8 and Section 9 with the known `npx skills check` caveat and the narrower proof burden for code-review-specific behavior.
  - Preserved `codex-review-yolo` as a separate manual helper and kept Gemini out of the new skill support matrix.
- Remaining inconsistencies:
  - none
- Unresolved decisions:
  - none
- Unauthorized scope cuts:
  - none
- Decision-complete:
  - yes
- Decision: proceed to implement? yes
<!-- arch_skill:block:consistency_pass:end -->

# 10) Decision Log (append-only)

- 2026-04-19: Created draft North Star for a new general code-review skill. Initial scope locks the reviewer to fresh unsandboxed Codex `gpt-5.4` `xhigh`, requires parallel `gpt-5.4-mini` `xhigh` Codex review-lens agents, requires docs-drift review, requires `$agent-linter` for agent-building targets, and treats `../psmobile` PR-agent review policy as source material to genericize rather than a runtime dependency.
- 2026-04-19: Research pass set default decisions: ship the new skill as `code-review`, keep `codex-review-yolo` as a narrower manual fresh-eyes helper, use explicit Codex `gpt-5.4` `xhigh` unsandboxed invocation by default, treat Claude as a trigger/continuation host that shells out to Codex for review, and require parallel `gpt-5.4-mini` `xhigh` subprocess review lenses to either run or fail loudly instead of silently downgrading coverage.
- 2026-04-19: External research and follow-up deep-dive set the implementation architecture: `skills/code-review/` owns the skill, prompt, requirements, output contract, and deterministic runner; the existing shared Stop-hook dispatcher owns only a narrow `code-review` state handler; Codex and Claude hook installers remain shared; Claude support intentionally shells out to Codex for review; Gemini support is excluded until explicitly requested and verified.
- 2026-04-19: Phase plan and consistency pass made Section 7 authoritative and implementation-ready, and the planning-pass block now records both stages as done. The execution order is skill package first, deterministic Codex runner second, shared dispatcher integration third, install/docs publication fourth, runtime smoke proof fifth, and final drift audit sixth. Consistency review found no remaining unresolved decisions or unauthorized scope cuts, so the plan can proceed to implementation.
- 2026-04-19: Local runtime refresh integrated after the Codex/Claude auto-loop improvements landed in the worktree. Generic dual-runtime hook infrastructure is now treated as already installed and verified by the native-loop worklog, so the `code-review` plan no longer includes broad hook-parity work. Remaining implementation is additive: `skills/code-review/`, `run_code_review.py`, a narrow `code-review` dispatcher state handler, install inventory, docs, and review-specific smoke proof. The Claude-hosted review path remains an explicit exception to generic host-native child execution because the reviewer must always be Codex.
