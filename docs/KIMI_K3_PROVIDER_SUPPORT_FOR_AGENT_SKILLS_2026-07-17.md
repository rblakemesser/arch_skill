---
title: "Kimi K3 + Grok 4.5 Harness Support for Agent Skills — Architecture Plan"
date: 2026-07-18
status: complete
completed: 2026-07-18
fallback_policy: forbidden
owners: [aelaguiz]
reviewers: [aelaguiz]
doc_type: new_system
related:
  - skills/_shared/model_resolution.py
  - skills/_shared/agent-orchestration-policy.md
  - skills/agent-delegate/references/model-and-invocation.md
  - skills/fresh-consult/references/model-and-invocation.md
  - skills/model-consensus/references/model-and-invocation.md
  - skills/arch-epic/scripts/run_arch_epic.py
  - skills/stepwise/scripts/run_stepwise.py
  - tests/test_arch_epic_auto.py
---

# TL;DR

- **Outcome:** Every live generic skill that shells out to external model providers gains a first-class fifth runtime, `kimi`, through the Kimi Code CLI running Kimi K3 (`kimi-code/k3`). The existing Grok runtime also moves its natural-language default from the retired `grok-build` assumption to the current `grok-4.5` model. Users can say `kimi`, `kimi k3 high`, `k3 low`, `grok high`, `grok build medium`, or `grok-4.5 low` without provider or version loss.
- **Problem:** The external-provider surface is hard-coded to four runtimes — `claude`, `codex`, `agent` (Cursor Agent), and `grok` — across one shared resolver, three prompt-first invocation references, two deterministic orchestrator scripts, and their doctrine. Kimi cannot be resolved, invoked, resumed, or receipted, while the Grok resolver still maps bare Grok and natural `Grok Build` wording to `grok-build`, which is absent from the current authenticated catalog.
- **Approach:** Keep model identity and defaults in the shared resolver; add only provider-specific argv and stream parsing to the two existing scripts; extend the three prompt-first transport references with exact Kimi fresh/resume contracts; update live provider enumerations and negative guardrails; and prove the behavior with resolver, argv, parser, dispatch, and package checks. Do not add a new runner, skill, registry, or fallback path.
- **Ground truth:** Kimi mechanics were verified live against `kimi` 0.26.0, including K3 discovery, headless fresh/resume, stream events, and effort overrides. Grok mechanics were verified against `grok` 0.2.91 and its current authenticated catalog, which exposes `grok-4.5` as the sole/default model with `low`, `medium`, and `high` efforts. The corrected product target is `grok-4.5`, not Grok Composer and not a model named “Grok Build 2.5.”

# North Star

A user on any host can name Kimi K3 or the current Grok model in natural language, and every transport-owning skill resolves the same canonical runtime/model/effort tuple. Kimi runs through the real `kimi` CLI with exact session receipts; Grok runs through `grok` with `grok-4.5`; neither lane silently falls back, rewrites an explicitly named model ID, or substitutes an effort.

Success looks like:

- `resolve_execution_phrase("kimi k3 high")` → `runtime=kimi, model=kimi-code/k3, effort=high`.
- `resolve_execution_phrase("kimi")` → `runtime=kimi, model=kimi-code/k3, effort=max, effort_source=model_default`.
- `resolve_execution_phrase("grok build medium")` → `runtime=grok, model=grok-4.5, effort=medium`.
- `resolve_execution_phrase("grok-build high")` preserves the explicit legacy ID and succeeds only if that exact ID is discoverable; it is never silently rewritten to `grok-4.5`.
- `$agent-delegate` runs a fresh-resumable kimi worker, captures `session_id` from the stream, and resumes it later with `kimi -r <id>`.
- `$fresh-consult` and `$model-consensus` accept kimi participants through the same doctrine block as Grok.
- `run_arch_epic.py` and `run_stepwise.py` spawn/finalize/resume kimi workers and critics with the same receipt guarantees as the Claude lane.
- Every enumeration that today says "Claude, Codex, Cursor Agent, or Grok" says "Claude, Codex, Cursor Agent, Grok, or Kimi".

# Verified Kimi ground truth (2026-07-18, kimi 0.26.0)

Checked against the local CLI, `~/.kimi-code/config.toml`, `kimi provider list --json`, official docs, and two live headless probes.

## Model and thinking levels

- Model alias: `kimi-code/k3` (upstream model id `k3`), 1,048,576-token context, capabilities `thinking, always_thinking, image_in, video_in, tool_use`. It is the local `default_model`.
- **Three catalog-advertised thinking efforts:** `supportEfforts = ["low", "high", "max"]`, with `defaultEffort = "max"`. These are the levels the system may choose by default or inference. The official `KIMI_MODEL_THINKING_EFFORT` override accepts all five repo-wide effort values and bypasses the catalog support list, so an explicit `medium` or `xhigh` request is preserved as a forced override. Receipts and docs must not describe those two levels as catalog-supported.
- Other installed aliases (`kimi-code/kimi-for-coding`, `kimi-code/kimi-for-coding-highspeed`, K2.7-era, boolean thinking) exist but are out of scope for this rollout; the phrase grammar targets K3 only.

## Headless invocation (probe-verified)

- Fresh: `KIMI_CODE_NO_AUTO_UPDATE=1 KIMI_MODEL_THINKING_EFFORT=<effort> kimi -m <model> -p "<prompt>" --output-format stream-json > events.jsonl 2> stderr.log` exits 0 and uses print mode's automatic approval. That is not a full permission, hook, or static-denial bypass. `--yolo`, `--auto`, and `--plan` conflict with `-p` and must not be added.
- Resume: `kimi -r <session_id> -p "<prompt>" --output-format stream-json` — verified live: the resumed run answered from prior-session context. `-r` is a hidden alias of `-S/--session`.
- Event stream shapes (verified):
  - `{"role":"assistant","content":"..."}` — final text. Concatenate `role=assistant` contents after exit (Grok-style receipt).
  - `{"role":"meta","type":"session.resume_hint","session_id":"session_<uuid>","command":"kimi -r session_<uuid>"}` — the durable session handle emitted after a successful turn. A failed or malformed turn may omit it; any workflow promising continuation treats that as unrecoverable.
- Model selection: `-m <alias>` (e.g. `-m kimi-code/k3`).
- Effort selection: `KIMI_MODEL_THINKING_EFFORT=<low|medium|high|xhigh|max>` env var on the process. It forces `thinking.effort` on the wire for the Kimi provider and bypasses the catalog `supportEfforts` gate. There is no `--effort` CLI flag; `medium` and `xhigh` are explicit forced overrides, not advertised K3 levels.
- Model/effort discovery: `kimi provider list --json` returns a top-level `.models` object. Its object keys are the callable aliases; `discover_kimi_models()` must return those keys rather than inner upstream model values.
- Working directory: kimi has no `-C`/`--cd` flag; run the subprocess with `cwd=<work_root>`. Sessions are cwd-scoped, so resume from the same `work_root` (same rule as Claude).
- Long prompts: `-p` takes the prompt as one argv value. Kimi exposes no verified prompt-file or stdin form, so callers pass prompt text directly without a shell. The operating-system argv-size limit is a real constraint; do not claim every future prompt is guaranteed to fit.
- No documented hook-suppression flag: kimi hooks live in `~/.kimi-code/config.toml`; a subprocess inherits user config. Document this as a known difference from `claude --settings '{"disableAllHooks":true}'`; do not invent a flag. `--skills-dir` exists but default skill discovery is desirable for editful workers (matches agent-delegate's "workers can use installed skills" doctrine).
- No `--output-schema`/`--json-schema` equivalent: structured critic verdicts go inline in the prompt, exactly like the existing Grok critic path (`_prompt_with_schema`).
- Fresh Kimi runs still persist sessions. “Fresh” means no prior conversation is resumed; it does not mean ephemeral or session-free.

# Verified Grok ground truth (2026-07-18, grok 0.2.91)

- Invoke the Grok harness with the unambiguous `grok` executable, never the machine's `agent` command, which belongs to Cursor Agent on this host.
- `grok models` and the current local catalog expose one model: `grok-4.5`, marked default. Its advertised reasoning efforts are `low`, `medium`, and `high`, with `high` as the model default.
- This repo continues to require an explicit effort for ordinary Grok phrases. The model default is recorded as catalog fact but is not introduced as a new resolver omission rule in this change.
- Bare `grok`, natural `grok build`, and natural `grok cli` select `grok-4.5` as the model candidate; the repo's existing explicit-effort rule still applies. The phrase “Grok Build” identifies the harness/product experience; it is not itself the canonical model ID.
- An explicit slug such as `grok-build` or `grok-composer-2.5-fast` remains exact and is checked against discovery. Explicit legacy IDs are never rewritten to `grok-4.5`.
- `grok-4.5` accepts only its catalog-advertised `low`, `medium`, and `high` levels through this resolver. Generic CLI parser support for other effort words is not evidence that this model supports them.
- Existing fresh/resume invocation mechanics remain valid: `--model <model>`, `--effort <effort>`, `--prompt-file <path>`, `--output-format streaming-json`, and exact `--resume <session_id>`.
- Streaming final text is the ordered concatenation of `type=text` event data; the durable handle comes from `type=end.sessionId`. Explicit error events, session-only streams, or empty final text are malformed and fail loudly.

# Scope

## In scope — the transport-owning surface

### A. Shared core (the one place resolution logic lives)

1. `skills/_shared/model_resolution.py`
   - `VALID_RUNTIMES` → add `"kimi"`.
   - Module docstring routing rule → add Kimi Code/K3 and make `grok-4.5` the current natural Grok default.
   - New `_KIMI_MODEL_RE` / `_extract_kimi_model_candidate` / `_resolve_kimi_model` + `discover_kimi_models()` (parses `kimi provider list --json`; conservative empty-list fallback like `discover_codex_models`).
   - `_infer_runtime`: add `has_kimi` on `\b(kimi|moonshot|k3)\b` (careful: `k3` needs word-boundary discipline so `gpt-5.3`-style tokens never match; require `\bk[\s_-]*3\b` plus the explicit `kimi`/`moonshot` keywords). Add kimi to every mixing check so "kimi gpt 5.6 high" fails loud instead of routing through the wrong harness.
   - `resolve_execution_phrase`: new `elif runtime == "kimi"` branch — resolve model (default `kimi-code/k3` when the phrase names only "kimi") and accept any explicit effort from `VALID_EFFORTS` verbatim, including `medium`/`xhigh` (they ride the env var, which bypasses the declared-effort gate). Omitted effort on the kimi lane resolves to `max` with `effort_source="model_default"` (the Fugu `profile_default` precedent). Defaults and inference never pick `medium`/`xhigh`; only an explicit ask does.
   - New `kimi_model_args(model) -> list[str]` returning `["-m", model]`, plus documented `KIMI_EFFORT_ENV` and `KIMI_NO_AUTO_UPDATE_ENV` constants so both scripts use the same process configuration.
   - `resolve_role_execution_policy`: accept optional `kimi_models` list and thread it through (same as `grok_models`).
   - Docstring examples: add `"kimi k3 high" -> kimi / kimi-code/k3 / high` and `"kimi" -> kimi / kimi-code/k3 / max (model_default)`.
   - Replace the old natural Grok fallback with `PREFERRED_GROK_MODEL = "grok-4.5"`. Resolve bare `grok`, natural `grok build`, and natural `grok cli` to that model; parse an explicit `grok-*` token first so an exact legacy slug is preserved.
   - Validate `grok-4.5` efforts against `low | medium | high`; leave explicitly named other Grok models discovery-gated without inventing model-specific effort metadata.
2. `skills/_shared/agent-orchestration-policy.md`
   - Keep the policy provider-neutral where possible. Add Kimi only where an existing host/provider example would otherwise imply the four-provider list is exhaustive.
   - Preserve the policy's core decision: ordinary same-host work uses a capable native child; Kimi is an external lane when exact K3/provider/session behavior is the concrete benefit.

### B. The three parallel invocation references (same doctrine block × 3)

These three files carry independent full copies of the per-provider doctrine; each gets the same mechanical addition (section names adapted to each file's local prefix):

3. `skills/agent-delegate/references/model-and-invocation.md`
   - New `## Kimi Fresh` and `## Kimi Resume` sections after the Grok pair:
     ```bash
     KIMI_MODEL_THINKING_EFFORT="<resolved_effort>" \
     KIMI_CODE_NO_AUTO_UPDATE=1 \
     kimi \
       -m "<resolved_kimi_model>" \
       -p "$(cat "$PROMPT_PATH")" \
       --output-format stream-json \
       > "$EVENTS_PATH" \
       2> "$STDERR_PATH"
     ```
     Run from `work_root` (no `-C` flag exists). Resume adds `-r "<session_id>"` and nothing else changes. Never `-c/--continue` — that is latest-session selection, banned by the same doctrine that bans Claude `--continue` and Codex `--last`.
   - `## Required Values`: runtime enum gains `kimi`; session-id bullet gains "Kimi `session_id` from the `session.resume_hint` meta event".
   - `## Runtime Inference`: add — `kimi`, `kimi code`, `kimi k3`, `k3`, or `moonshot` implies `runtime=kimi`; an omitted model on the kimi lane resolves to `kimi-code/k3`; an omitted effort resolves to `max` (model default, reported as such).
   - `## Model Phrase Resolution`: kimi bullet — preserve `kimi-code/k3` exactly; do not route K2.7 aliases unless the user names them (out of scope here); add the announce-mapping examples `Kimi K3 high -> runtime=kimi, model=kimi-code/k3, effort=high` and `Kimi -> runtime=kimi, model=kimi-code/k3, effort=max, effort_source=model_default`.
   - `## Effort Resolution`: kimi effort rides the `KIMI_MODEL_THINKING_EFFORT` env var (no `--effort` flag). K3 advertises `low`, `high`, `max`; an explicit `medium`/`xhigh` is passed through verbatim as a forced override, but those two are never chosen as defaults or by inference. Never remap one effort to another.
   - `## Run Directory`: final-text rule gains "For Kimi, concatenate `role=assistant` event contents after exit; capture `session_id` from the `type=session.resume_hint` meta event".
   - `## Failure Behavior`: add — kimi exits without any `role=assistant` event; fresh-resumable kimi emits no `session.resume_hint`; caller asks for `kimi -c` / latest-session selection. Extend the closing no-silent-fallback line to "Claude, Codex, Cursor Agent, Grok, and Kimi".
   - Update Grok mapping examples and defaults to `grok-4.5`; distinguish natural `Grok Build` wording from exact legacy model slugs; record `low | medium | high` as the supported 4.5 effort set.
4. `skills/fresh-consult/references/model-and-invocation.md` — the same block as `## External Kimi Fresh Resumable` / `## External Kimi Resume`, plus the runtime enums in `## Required External Values`, the execution.json/chain.json `"runtime"` templates, runtime inference, phrase resolution, effort resolution, and the fail-loud closer. Consult-specific chain/turn receipt layout stays untouched.
5. `skills/model-consensus/references/model-and-invocation.md` — the same block as `## External Kimi: First Turn` / `## External Kimi: Resume Turn`, plus `## Required Participant Values` enum, phrase resolution, and worked mapping examples. `references/examples.md` may optionally gain one kimi-participant example.

All three references must remain prompt-first contracts. They may show exact commands and receipt parsing, but they must not acquire a new controller script, deterministic dialogue runner, or hidden fallback logic.

### C. Scripted orchestrators

6. `skills/arch-epic/scripts/run_arch_epic.py` (Grok is the template for every branch)
   - New `_kimi_argv(work_root, model, effort, prompt_path, *, session_id=None)` builder (analog of `_grok_argv` at :590): `["env", "KIMI_CODE_NO_AUTO_UPDATE=1", f"KIMI_MODEL_THINKING_EFFORT={effort}", "kimi", "-m", model, "-p", prompt_text, "--output-format", "stream-json"]`, adding `["-r", session_id]` after `kimi` when resuming. Kimi takes prompt text inline; retain argv boundaries and never invoke a shell.
   - Worker/critic wrappers `_kimi_worker_argv` / `_kimi_critic_argv` (analogs at :897/:996); critic schema via `_prompt_with_schema` into `prompt.kimi.md` (Grok path — kimi has no schema flag).
   - Parsers `_parse_kimi_final_json` (concatenate `role=assistant` contents; capture `session_id` from `session.resume_hint`) and `_parse_kimi_session_id` (analogs of `_parse_grok_final_json` :625 / `_parse_grok_session_id` :654).
   - Dispatch `elif`s: `_run_worker` (:1256-1288), `cmd_auto_critic_spawn` (:1393-1429), `cmd_critic_spawn` (:1707-1740), `_finalize_worker_try_dir` (:1145-1162), `_finalize_critic_run_dir` (:1196-1221).
   - argparse `critic-spawn --runtime` choices (:1958) gain `"kimi"`; module docstring (:11-13) updated; `_policy_from_file` (:772-783) gains optional `kimi_models` plumbing.
   - Harden the existing Grok parser while adding coverage: reject explicit error events and require non-empty final text rather than accepting a session-only stream.
   - Note: the `agent` (Cursor Agent) runtime currently has no argv branch in this script (would `_die("unknown worker runtime: agent")`). That pre-existing gap is out of scope; do not fix it here, but do not copy the mistake — kimi ships with full worker+critic coverage from day one.
7. `skills/stepwise/scripts/run_stepwise.py`
   - New `_kimi_argv` (analog of `_grok_argv` :703) + kimi branches in `cmd_step_spawn` (:865-869 area), `cmd_step_resume` (:984-992 area), `cmd_step_diagnose` (:1058-1103), `cmd_critic_spawn` (:1224-1233 area, schema inline).
   - Parsers `_parse_kimi_final_json` / `_parse_kimi_session_id` (analogs at :738/:767); session-capture dispatch at :874-895 and :999-1019 gains the kimi branch, with the same `"UNRECOVERABLE"` + exit 4 discipline.
   - argparse `choices=["claude","codex","grok"]` at :1522/:1542/:1562/:1576 gain `"kimi"`.
   - Apply the same Grok parser hardening as arch-epic so the two deterministic lanes share malformed-output semantics.

### D. Doctrine and metadata enumerations

8. `skills/arch-epic/references/model-and-effort.md` — external-lane sentence (:9), legacy `critic_runtime` enum (:21), shared-resolver bullet list (:76-89), acceptable phrasing (:99-107), phrase-resolution bullets (:116-141), mapping examples (:150-158).
9. `skills/stepwise/references/model-and-effort.md` — six-value external policy bullets (:15-20), acceptable shapes (:50-58), phrase resolution (:63-128), asking template (:137-147), runtime inference (:167-177).
10. `skills/stepwise/references/session-resume.md` — the CLI mechanics bible and the file to update **first** among doctrine docs: header "Verified against" line gains `Kimi Code CLI 0.26.0`; new `Kimi — step session (resumable)`, `Kimi — step resume`, `Kimi — critic (fresh, schema inline)` sections after the Grok triplet; flag-drift notes (env-var effort, meta-event session id, no hook suppression); three new numbered smoke invocations in the Verification block (fresh, resume, critic).
11. `skills/stepwise/references/manifest-schema.md` (:82-84) and `skills/stepwise/references/execution-routing.md` (:75-77 + JSON examples) — runtime enums gain `kimi`.
12. Critic schema-delivery trios → quartets: `skills/arch-epic/references/critic-prompt.md` (:212-215), `skills/arch-epic/references/critic-contract.md` (:15, :155-156, :225), `skills/stepwise/references/critic-prompt.md` (:150-153), `skills/stepwise/references/critic-contract.md` (:63-65) — each gains "Kimi receives the schema inline in the prompt" alongside the Grok path. `skills/stepwise/references/session-prompt-contracts.md` (:198-199) gains the kimi resume-mechanics line.
13. SKILL.md frontmatter + routing non-negotiables (descriptions are trigger logic; keep each under its runtime length cap):
    - `skills/agent-delegate/SKILL.md` description: "...Claude, Codex, Cursor Agent, Grok, or Kimi workers..." + provider-routing bullet gains the kimi clause.
    - `skills/fresh-consult/SKILL.md` (:3 description, :92-96 routing block).
    - `skills/model-consensus/SKILL.md` (:3 description, :93-98 routing block).
    - `skills/arch-epic/SKILL.md` (:396 `--runtime` line, :369-371 schema-delivery sentence, :37-47/:120-124 external-lane prose).
    - `skills/stepwise/SKILL.md` (:3 description, :99-103 external-defaults block, :209 reference-map line, :117-119/:126-132 external-lane bullets).
    - `skills/plan-conductor/SKILL.md` (:87-93 routing block) and `skills/plan-conductor/references/delegation-and-monitoring.md` (`## External Worker Identity`) — restated routing sentences only; the kimi lane itself is inherited from `$agent-delegate`.
14. `agents/openai.yaml` co-edits (skill-authoring non-negotiable: metadata must not drift from SKILL.md):
    - `skills/agent-delegate/agents/openai.yaml` — `default_prompt` provider list.
    - `skills/fresh-consult/agents/openai.yaml` (:4) — provider list.
    - `skills/model-consensus/agents/openai.yaml` (:4) — provider list.
    - `skills/arch-epic/agents/openai.yaml`, `skills/stepwise/agents/openai.yaml` — only if their prompts enumerate providers (verify during implementation; several, like plan-conductor's, are deliberately provider-generic and stay untouched).

15. Root routing and consistency surfaces:
    - `AGENTS.md`, `README.md`, and `docs/arch_skill_usage_guide.md` gain Kimi in the live provider inventory and use `grok-4.5` in current Grok examples/defaults.
    - Generic “do not manually spawn provider CLIs” guardrails in `plan-implement`, `plan-audit`, and the cynical review skills add `kimi`; these are wording-only consistency changes, not new transport owners.
    - Preserve unrelated user changes already present in `README.md` and `docs/arch_skill_usage_guide.md`; patch only the provider-specific paragraphs.
    - No Makefile change is required because the existing shared-directory and skill installation paths already carry the edited files.

### E. Tests

16. `tests/test_arch_epic_auto.py` (loads both `model_resolution` and `run_arch_epic` via importlib)
    - Phrase cases: `"kimi k3 high"` → `kimi / kimi-code/k3 / high`; `"k3 low"` → `kimi / kimi-code/k3 / low`; `"kimi"` → `kimi / kimi-code/k3 / max` with `effort_source="model_default"`; `"kimi max"` → explicit max.
    - Explicit-effort passthrough cases: `"kimi medium"` → `effort=medium` and `"kimi k3 xhigh"` → `effort=xhigh` (explicit asks honored verbatim; never produced by a default). Fail-loud cases stay cross-family: `"kimi gpt 5.6 high"` raises mixed-runtime; `"kimi claude opus high"` raises mixed-runtime.
    - `kimi_model_args` shape; `resolve_role_execution_policy` with a kimi role (`same as` inheritance included).
    - `_kimi_argv` / `_kimi_worker_argv` / `_kimi_critic_argv` shape tests (env assignment first, `-m`, `-p`, resume inserts `-r <id>`), and `_parse_kimi_final_json` / `_parse_kimi_session_id` against probe-captured event samples (assistant content + `session.resume_hint`).
    - Grok regressions: bare `grok`, natural `grok build`, and `grok cli` resolve to `grok-4.5`; explicit legacy slugs stay exact; 4.5 rejects `xhigh`/`max`; parsers reject explicit errors, empty text, and session-only streams.
    - Discovery fixtures prove `discover_kimi_models()` reads `.models` keys and degrades safely on malformed output or command failure.
17. `skills/stepwise/scripts/test_run_stepwise.py`
    - New `KimiInvocationFlags` class mirroring `ClaudeInvocationFlags` (:167): spawn/resume/diagnose/critic all carry `-m`, env effort, and `--output-format stream-json`; resume carries `-r <sid>`; critic prompt embeds the schema.
    - Kimi parse tests beside the existing `ClaudeShapeParsing` class.
    - Grok parser tests establish the same non-empty-final and explicit-error behavior as arch-epic.

## Out of scope (with rationale)

- `codex-review-yolo` — intentionally locked to the exact Codex `-p yolo` profile; the pinned profile **is** the contract. A future `kimi-review` receipt lane would be a new skill, not an edit here.
- `agent-history` — never shells out; it reads session stores from disk. Adding `~/.kimi-code/sessions` as a third history source is a real but separate feature (follow-up candidate).
- `chatgpt-web` — browser transport, not a CLI provider.
- `arch-mini-plan`, `audit-loop*`, `comment-loop`, `goal-loop`, `cynical-*`, `exhaustive-code-review`, `plan-audit`, `plan-implement`, `lilarch`, `bugs-flow` — no live provider-shell-out surface. A few generic negative guardrails need Kimi added so they do not imply it is an allowed side door, but they do not gain adapters. Their untracked `build/` copies are generated/stale and remain untouched.
- `codex-cleanup`, `codex-babysit` — Codex-specific housekeeping, not provider-generic transport.
- `agent` (Cursor Agent) runtime gaps in the orchestrator scripts (no argv branches) — pre-existing, unrelated to kimi; do not opportunistically fix.
- The `agent_skills` repo `psmobile-*` skills — no provider shell-out at all.
- K2.7-era aliases (`kimi-for-coding*`) — the phrase grammar targets K3 only; naming them later is an additive resolver change.

# Phase plan

Phase 0 — Verification already done (this doc): Kimi CLI shape, K3 efforts, fresh/resume probes, receipt events, Grok 4.5 discovery/efforts, and exhaustive live-surface inventory. No code.

Phase 1 — Shared resolver (`_shared/model_resolution.py`) + resolver tests in `tests/test_arch_epic_auto.py`.
Acceptance: Kimi resolution/discovery and Grok 4.5 alias/default/effort cases pass; exact legacy Grok IDs remain exact; full file is green via `python3 -m unittest tests/test_arch_epic_auto.py`.

Phase 2 — Script lanes: `run_arch_epic.py` + `run_stepwise.py` argv builders, parsers, dispatch, argparse, plus their script tests (`KimiInvocationFlags`, argv shapes, event parsing).
Acceptance: `python3 skills/stepwise/scripts/test_run_stepwise.py` green; arch-epic tests green; `python3 -m py_compile` on both scripts.

Phase 3 — Canonical invocation doctrine: `agent-delegate/references/model-and-invocation.md` first (it is the pattern source), then the two parallel copies (`fresh-consult`, `model-consensus`), then the minimal shared-policy clarification.
Acceptance: each file has complete Kimi fresh/resume, model/effort, receipt, and failure contracts; current Grok examples use 4.5; every runtime enum and fail-loud line covers all five runtimes; no new controller layer appears.

Phase 4 — Orchestrator doctrine + metadata: arch-epic/stepwise references (session-resume.md mechanics reference first), SKILL.md routing blocks and descriptions, plan-conductor restatements, root docs, negative guardrails, and `agents/openai.yaml` co-edits.
Acceptance: exact searches no longer find a live generic provider list that omits Kimi; Grok defaults/examples are 4.5; metadata matches its owning SKILL.md; unrelated dirty-file hunks are preserved.

Phase 5 — Verification and implementation audit.
- Run both targeted Python suites, full unittest discovery, Python compilation/import checks, `npx skills check`, and CRG changed-surface detection.
- Run narrow local Kimi fresh/resume/parser smoke tests only if they do not mutate the repo or user-owned session state beyond normal Kimi session receipts; retain no generated repo artifacts.
- Audit the final diff against this plan: all live transport owners covered, provider-specific exceptions still narrow, no generated/build/vendor edits, no silent fallback, and all user-owned pre-existing changes preserved.
- `make verify_install` is not required because install behavior does not change. Do not run `make install` merely to prove source doctrine.

# Design decisions locked

- **Runtime keyword:** `kimi`. Phrase triggers: `kimi`, `kimi code`, `kimi k3`, `k3`, `moonshot`. Cross-family mixing fails loud, same as existing Grok/Cursor rules.
- **Model value:** the CLI alias `kimi-code/k3` (what `-m` takes), preserved exactly; bare `k3` in a phrase normalizes to it. K3 is the kimi-lane default; other aliases are not auto-resolved in this rollout.
- **Effort:** K3 declares `low | high | max`; omitted → `max` (`effort_source="model_default"`, Fugu `profile_default` precedent). An explicit `medium`/`xhigh` ask is honored and passed verbatim through the env var — never a default, never inferred, never remapped.
- **Effort transport:** `KIMI_MODEL_THINKING_EFFORT` env var on the subprocess (there is no `--effort` flag); scripts set it via `env` in argv or `subprocess` env, never by mutating `~/.kimi-code/config.toml`.
- **Deterministic Kimi process:** every scripted launch also sets `KIMI_CODE_NO_AUTO_UPDATE=1`; print mode's automatic approval is not documented as yolo or a hook/static-denial bypass.
- **Session semantics:** successful Kimi turns emit `session.resume_hint`; fresh-one-shot and fresh-resumable share one command shape; resume is `kimi -r <exact id>` only — `-c/--continue` is banned as latest-session selection. Fresh runs still persist sessions.
- **Receipts:** final text = concatenated `role=assistant` contents; session id = `session.resume_hint` meta event; missing either after a zero exit = malformed run, preserve the run directory (same rule as Grok).
- **Critic structure:** schema inline in the prompt (Grok path); do not invent a schema flag.
- **No invented flags:** kimi has no hook-suppression, memory, or sandbox flags; the doctrine documents the inherited-config difference instead of fabricating equivalents.
- **Minimal-diff discipline:** kimi is added as a peer of Grok everywhere (Grok was the most recent runtime addition and is the structural template). No refactors of the existing four lanes, no build/ cleanup, no Cursor-Agent gap fixes.
- **Grok current default:** bare `grok`, natural `grok cli`, and natural `grok build` mean `grok-4.5`; the resolver still requires an explicit effort. Explicit `grok-*` slugs are exact and discovery-gated.
- **Grok 4.5 effort set:** `low | medium | high` only. The generic Grok CLI accepting additional effort words does not widen this model's catalog contract.
- **Prompt-first ownership:** `agent-delegate`, `fresh-consult`, and `model-consensus` remain reasoning-led skills with exact invocation examples. The two existing Python scripts stay narrow deterministic helpers for orchestration mechanics; no third harness abstraction is introduced.
- **No shared session framework:** the two runners have different artifact and lifecycle contracts, so this change does not introduce `external_session.py`, a provider plugin registry, or a resolver CLI. The shared resolver owns identity; each existing runner retains its small deterministic invocation/parsing switch. The prompt-first skills keep enough exact command detail to remain self-contained when installed independently.

# Risks and open questions

- **Prompt-in-argv length:** very large Kimi prompts ride one argv value and can hit the operating-system limit. If a future lane needs more, add only a verified upstream prompt-file/stdin mechanism rather than assuming one exists.
- **Env-var effort is process-global:** parallel kimi children at different efforts must each set their own subprocess env (the skills already spawn one process per child, so this holds; the parallel-group doctrine just needs the per-child env noted — it is in the Phase 3 block).
- **`kimi provider list --json` drift:** `discover_kimi_models()` follows the existing conservative discovery pattern and returns an empty list on command or shape failure. Resolution may still retain the canonical explicit candidate when discovery is unavailable, but a non-empty discovered catalog must reject a missing model. Never switch providers or models.
- **Kimi hooks/MCP inheritance:** a kimi subprocess runs the user's configured hooks and MCP servers. That is acceptable for editful lanes (matches how workers get skills) but is documented as a difference from the Claude `--settings` isolation, not hidden.
- **Thinking content:** kimi stream-json does not emit thinking blocks to stdout (docs confirm); receipts therefore capture visible output only — same effective guarantee as the other lanes' finals.
- **Legacy Grok IDs:** preserving an explicitly named slug means it may fail on a host whose catalog contains only `grok-4.5`. That failure is intentional and safer than semantic rewriting.

# Implementation result

Completed on 2026-07-18. The shipped surface now follows the locked design:

- `skills/_shared/model_resolution.py` owns Kimi runtime/model/effort resolution,
  Kimi model discovery, the shared Kimi process-variable names and model argv,
  natural Grok-to-`grok-4.5` resolution, exact legacy `grok-*` preservation, and
  model-specific effort validation. Multiple distinct effort labels fail loud;
  omission alone activates a model or profile default.
- `run_arch_epic.py` and `run_stepwise.py` both execute and resume Kimi through
  the same shared process contract, parse visible assistant output and exact
  `session.resume_hint` handles, reject malformed Kimi/Grok streams, preserve
  fresh-run receipts, and deliver critic schemas inline. Each runner retains
  its own existing lifecycle and artifact contract; no generalized provider or
  session framework was added.
- `$agent-delegate`, `$fresh-consult`, and `$model-consensus` carry complete
  prompt-first Kimi fresh/resume contracts and the corrected Grok mapping.
  `$arch-epic`, `$stepwise`, and `$plan-conductor` now route Kimi consistently,
  and the relevant metadata, root routing docs, and external-process guardrails
  enumerate the fifth provider without making external delegation automatic.
- Natural `Grok`, `Grok CLI`, and `Grok Build` requests resolve to `grok-4.5`.
  A natural phrase naming another numeric Grok version fails instead of being
  rewritten. Only an explicitly supplied `grok-*` slug enters the legacy exact-
  identity/discovery lane.
- Kimi defaults to `kimi-code/k3` at `max`; `low`, `high`, and `max` are the
  advertised K3 levels. Explicit `medium` and `xhigh` remain forced overrides,
  are receipted as such, and are never inferred or substituted.

# Verification

- `python3 -m unittest tests/test_arch_epic_auto.py` — 53 tests passed.
- `python3 skills/stepwise/scripts/test_run_stepwise.py` — 43 tests passed.
- `python3 -m unittest discover -s tests` — 85 tests passed.
- `python3 -m py_compile` over the shared resolver, both runners, and their
  changed test modules — passed.
- `npx skills check` — passed. It emitted the unrelated existing warning that
  four globally installed `pbakaus/impeccable` skills appear deleted upstream;
  non-interactive mode correctly skipped their deletion.
- `git diff --check` — passed.
- Exact searches found no stale four-provider enumeration, no generic
  “ephemeral critic” promise, and no live `grok-build` default. The remaining
  `grok-build`/Composer mentions document only exact legacy-id preservation.
- Code Review Graph inspected 46 changed tracked files and reported no affected
  flow. Its static test-gap list includes resolver functions that the
  importlib-loaded test suite exercises directly; the focused and full dynamic
  suites above are the authoritative proof for those paths.
- `make verify_install` was not run because install behavior did not change.
  No generated `build/`, vendored package, or unrelated untracked surface was
  edited. No additional live model-inference call was needed after the recorded
  Kimi fresh/resume probes and local provider-catalog verification.

# Implementation audit

The first read-only skeptical audit found three concrete gaps and blocked
approval:

1. contradictory effort labels could look like omission and activate Kimi's
   `max` default;
2. the two runners duplicated Kimi process-variable/model-argument literals
   instead of consuming the planned shared contract; and
3. generic CLI help called every critic “ephemeral,” although a fresh Kimi
   critic can persist a session that the workflow deliberately never resumes.

All three were repaired at their owning surfaces and covered by focused tests.
The same clean reviewer then re-audited those findings read-only and returned
`APPROVED` with high confidence and no remaining required repair.

# References

- [Kimi Code configuration files](https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files.html) — `[thinking] effort`, per-model `support_efforts` / `default_effort`
- [Kimi Code `kimi` command](https://www.kimi.com/code/docs/en/kimi-code-cli/reference/kimi-command.html) — `-p`, `-m`, `-r/--session`, `--output-format stream-json`, flag conflict rules
- [Kimi Code environment variables](https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/env-vars.html) — `KIMI_MODEL_THINKING_EFFORT`, `KIMI_CODE_HOME`
- [Grok Build overview](https://docs.x.ai/build/overview) — current Grok Build model identity (`grok-4.5`)
- Local verification: `kimi provider list --json`, `grok models`, and live Kimi fresh/resume stream-json probes in `/tmp/kimi-probe/`
