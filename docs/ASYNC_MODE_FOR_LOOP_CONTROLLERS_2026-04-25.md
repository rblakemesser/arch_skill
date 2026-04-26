---
title: "Async Mode For Loop Controllers - Architecture Plan"
date: 2026-04-25
status: active
fallback_policy: forbidden
owners: [Amir]
reviewers: []
doc_type: architectural_change
related:
  - README.md
  - docs/arch_skill_usage_guide.md
  - skills/_shared/controller-contract.md
  - skills/arch-step/scripts/arch_controller_stop_hook.py
  - skills/stepwise/references/model-and-effort.md
  - skills/stepwise/references/execution-routing.md
---

# TL;DR

## Outcome

Add an opt-in async execution mode across the arch_skill loop controllers so a casual request like "do it async", "run async on opus high", or "use gpt 5.4 xhigh async" can route the actual loop work through fresh external Claude or Codex child runs.

The existing Stop-hook state machines still own orchestration. Async mode only changes where the next leaf unit of work runs.

## Problem

Several controllers already launch fresh child reviews, checks, or evaluators, but the behavior is scattered and inconsistent:

- `arch-step` and `miniarch-step` can run fresh audit children, but implementation and planning stages mostly happen in the visible parent context.
- `arch-loop` already has a fresh evaluator child, but its requested parent work resumes in the visible parent context.
- `audit-loop`, `comment-loop`, `audit-loop-sim`, `arch-docs auto`, and `delay-poll` already launch children, but their model/runtime behavior is controller-specific rather than shared.
- Model and effort shorthand such as "opus high", "gpt 5.4 mini xhigh", or "Claude max" is handled better elsewhere, especially Stepwise, than in the loop controllers.
- There is no shared persisted execution policy saying exactly why a loop chose Codex or Claude, which model was selected, what effort was requested, and whether the choice was explicit, inferred, or a controller default.

## Approach

Introduce one shared async execution policy and resolver in the shared Stop-hook runner, then adopt it controller-by-controller for every real loop family:

- `arch-step`
- `miniarch-step`
- `arch-loop`
- `arch-docs auto`
- `audit-loop`
- `comment-loop`
- `audit-loop-sim`
- `delay-poll`
- `wait` as an explicit already-async/no-child no-op

Keep each loop's existing state owner, verdict source, ledger/doc contract, and Stop-hook lifecycle. Async mode changes the executor for eligible work units, not the controller.

## Plan

Research and deepen the current controller registry, child-run helpers, Stepwise model-resolution doctrine, and each loop's stop-hook path. Then implement in layers:

1. A shared async intent and model/effort resolver.
2. A persisted async execution policy on controller state.
3. Shared Codex and Claude child-run adapters with no-sandbox and hook-suppression guarantees.
4. Controller-specific adoption rules that externalize only the right leaf work.
5. Tests that lock down parser behavior, command shapes, state validation, hook-recursion prevention, and unchanged non-async behavior.

## Non-negotiables

- No new public loop command names.
- No complex syntax required from the user.
- No prompt-only fake automation.
- No hook recursion from child runs.
- No sandboxing for async worker or evaluator children unless an existing controller is explicitly read-only by design.
- No silent model-version substitution.
- No controller state ownership moves out of the shared Stop-hook runner.
- No child process may recursively arm or run the same controller loop.
- No silent downgrade or alias substitution for a model version the user named.
- No per-controller reimplementation of model shorthand parsing.

<!-- arch_skill:block:planning_passes:start -->
<!--
arch_skill:planning_passes
deep_dive_pass_1: done 2026-04-25
recommended_flow: research -> deep dive -> phase plan -> implement
note: This block tracks stage order only. It never overrides readiness blockers caused by unresolved decisions.
-->
<!-- arch_skill:block:planning_passes:end -->

# 0) Holistic North Star

## 0.1 The claim (falsifiable)

After this change, a user can ask any supported arch_skill loop controller to "run async", "do it async", "use async with opus high", "async on gpt 5.4 xhigh", or similar casual language, and the controller will either:

- arm with a fully resolved async execution policy and run each eligible loop work unit in a fresh hook-suppressed Claude or Codex child process, or
- fail loud before arming with one concise question naming the missing runtime/model/effort fact that cannot be safely inferred.

The visible parent session must stay the orchestrator surface: it owns arming, state validation, terminal summaries, and user questions. Fresh children own only the leaf work they were launched to perform.

The intended mental model is:

- The user talks naturally to the parent agent.
- The parent arms the normal loop controller with an optional async execution policy.
- The Stop hook advances the loop exactly as it does today.
- When a loop reaches eligible "do work now" or "evaluate/check/review now" work, the hook launches a fresh external child process.
- The child starts from disk state and an explicit prompt, not from inherited chat history.
- The child writes or reports the one leaf result it was asked for.
- The Stop hook validates the result and either advances, asks the user, retries according to the loop's existing rules, or disarms.

## 0.2 In scope

- A shared async execution policy for shared Stop-hook controllers.
- Natural-language async intent detection for casual phrases such as:
  - "do it async"
  - "run this async"
  - "fresh context"
  - "background it"
  - "do the loop async"
  - "use opus high async"
  - "do this with gpt 5.4 xhigh"
  - "run the arch loop async on Claude"
- A user-facing contract that casual language is enough. Structured flags can exist as internal/debug affordances, but normal use must not require complex syntax.
- Model/runtime/effort resolution based on the existing Stepwise-style rules:
  - `gpt`, `gpt-5.4`, `gpt 5.4 mini`, and similar Codex-family phrases resolve to Codex runnable model ids.
  - `opus`, `sonnet`, `haiku`, `claude opus 4.7`, and similar Claude-family phrases resolve to Claude runnable model ids.
  - exact versions are preserved; `5.5` never silently becomes `5.4`, and `4.7` never silently becomes another Claude version.
  - effort names resolve to the runtime-supported values already documented in the repo.
  - raw user text and normalized resolution are both persisted for auditability.
  - model family can imply runtime when unambiguous: GPT-family model means Codex; Claude-family model means Claude.
  - runtime-only requests can use controller defaults only where the controller has a documented default; otherwise the controller asks once before arming.
- Controller adoption for:
  - `arch-step auto-plan`, `implement-loop`, and `auto-implement`
  - `miniarch-step auto-plan`, `implement-loop`, and `auto-implement`
  - `arch-loop`
  - `arch-docs auto`
  - `audit-loop auto`
  - `comment-loop auto`
  - `audit-loop-sim auto`
  - `delay-poll`
- Clear no-op / already-async treatment for `wait`, because it has no work child to externalize.
- Explicitly preserving existing pinned defaults where a controller already has one, such as miniarch's Codex `gpt-5.4-mini` `xhigh` audit child.
- Persistent async child run artifacts for debugging: prompt, invocation, stream log, final message or JSON output, start/end timestamps, exit code, and resolved execution policy.
- Explicit command contracts for Codex and Claude children, including hooks disabled, no sandboxing, cwd set to the repo, and no nested controller arming.

## 0.3 Out of scope

- Gemini support for async loop controllers.
- Changing the user's command surface to require flags like `EXTERNAL_WORK=1`.
- Making async mode the default for all loop invocations.
- Replacing existing controller verdict semantics.
- Moving controller state out of `.codex/` or `.claude/arch_skill/`.
- Adding a separate background daemon, scheduler, queue, or service.
- Changing `code-review`'s reviewer identity or treating one-shot review as a loop.
- Changing Stepwise's manifest-driven orchestration model.
- Creating a new global preference system for model choice.
- Automatically deciding that one provider is better for a task category such as writing, coding, reviewing, or planning unless that rule already exists in local doctrine and is explicitly adopted.
- Running multiple async workers concurrently inside the same controller state before the sequential safety model exists.

## 0.4 Definition of done (acceptance evidence)

- A casual async phrase resolves to a persisted execution policy in controller state, including runtime, model, effort, source phrase, and resolution reason.
- Missing or ambiguous model/runtime/effort information fails loud before arming unless the controller has an explicit documented default policy.
- Async children for Claude always run with hooks disabled and dangerous permissions.
- Async children for Codex always disable Codex hooks and bypass approvals/sandbox.
- Existing non-async controller behavior remains unchanged when async mode is not requested.
- Every adopted loop controller has tests covering default behavior, async command shape, state validation, and blocked child-run failure.
- Skill docs and README usage text explain casual async language and shorthand model resolution without requiring users to learn structured flags.
- `npx skills check` passes after skill package changes.
- Docs-only edits have been re-read, and any new commands or paths in the docs have been verified with `rg` or direct file checks.

## 0.5 Key invariants (fix immediately if violated)

- The Stop hook is the only controller dispatcher and disarmer.
- Child runs must not arm nested controllers for the same task.
- Child runs must not clear or mutate controller state except through the explicitly allowed yield/status fields for their controller.
- Existing controller ledgers and plan docs remain the durable truth; child transcripts are evidence, not a second plan.
- Model shorthand resolution must be exact-version preserving and fail-loud on ambiguity.
- Async mode must never weaken the no-progress rule, hook-timeout discipline, or state conflict gate.

## 0.6 The important nuance

This feature is not "make the hook run everything in the background." It is "let loop controllers orchestrate external fresh-context children for eligible leaf work."

That distinction matters because these loop controllers are already state machines. The parent context is allowed to be short, stale, or even mostly unaware of the full repo, but the state machine cannot be confused. The Stop hook must remain the single place that knows:

- which controller is active,
- which step is next,
- what state file is authoritative,
- what ledger/doc markers prove progress,
- whether the loop is allowed to continue,
- whether the user must answer a question,
- and when to disarm.

Fresh child runs are valuable precisely because they do not inherit accumulated chat context. They must be given a narrow task, enough file/state references to reconstruct context from disk, and an explicit instruction to avoid nested controller commands. They should finish, emit a small summary or machine-readable result, and exit.

## 0.7 What "async" means in this plan

The word "async" is overloaded. For this feature it means:

- external child process,
- fresh model context,
- hook-suppressed execution,
- no sandbox / no approval gating,
- persistent artifacts,
- controller-owned continuation after the child exits.

It does not necessarily mean concurrent execution. Initial implementation should be sequential per controller state unless a later phase explicitly proves concurrent children are safe for that controller. Sequential externalization solves the context-freshness problem without creating state races.

# 1) Key Design Considerations (what matters most)

## 1.1 Priorities (ranked)

1. Preserve controller correctness and state ownership.
2. Make casual async user language work without complex syntax.
3. Resolve runtime/model/effort safely from shorthand when possible.
4. Keep async child invocations auditable and debuggable.
5. Avoid duplicating per-controller subprocess logic.
6. Preserve existing pinned evaluator/audit defaults unless the user explicitly overrides an eligible policy.
7. Keep non-async behavior byte-for-byte boring from the user's perspective.

## 1.2 Constraints

- The shared runner already owns all supported Stop-hook controller dispatch.
- Codex and Claude have different child-run flags, output shapes, model identifiers, and hook-suppression mechanics.
- Some controllers already have fresh child runs; the change should converge those onto shared policy rather than inventing a parallel path.
- Some loop controllers do work in the parent pass today; async mode must not make the parent invisible or powerless to ask the user.
- Existing installed hook timeout and state-file conflict behavior remain authoritative.
- Child processes cannot rely on the current chat transcript. Anything important must be passed in the child prompt or read from disk.
- Controller state lives under existing `.codex/` and `.claude/arch_skill/` roots. Async policy must be an additive state field, not a state-root migration.
- `arch-epic` already warns against shelling out into nested `arch-step` controllers because controller state collisions are possible. This feature must be implemented inside the shared controller runner, not as an outer wrapper that invokes loop commands.
- The feature must work for both Codex-hosted and Claude-hosted hooks, but runtime choice for a child is independent of the host when the policy says so.
- Some child helpers currently support different knobs. For example, Codex child helpers already accept model and effort; Claude helpers must be checked and likely extended for model selection.

## 1.3 Architectural principles (rules we will enforce)

- Shared resolver, controller-specific defaults: one parser/resolver for async execution policy, with small controller-owned defaults only where already justified.
- Runtime-native child execution: Claude children use Claude CLI, Codex children use Codex CLI.
- Fail loud over guessing: unresolved exact-version model mapping, runtime family ambiguity, missing effort where no default exists, or missing CLI support stops before arming.
- Leaf-only children: children run one explicit controller work unit, review, audit, check, or evaluator prompt and then exit.
- State is not a transcript: child artifacts help debugging but do not replace controller state, ledgers, plan docs, or audit blocks.
- Preserve verdict ownership: an async worker can do implementation, planning, review, or checking work, but it cannot overrule the loop's existing completion/audit/evaluator semantics.
- Explicit policy beats defaults. If the user says `opus high`, do not silently use an existing Codex pinned default for an eligible worker slot. If a controller's evaluator must remain pinned by design, document that as a separate evaluator policy.
- Exact command rendering is testable behavior. The flags that disable hooks and bypass sandbox/approvals are part of the contract, not incidental CLI details.
- Controller-specific prompts must be generated from explicit state and disk paths. Avoid prompt text that says "as discussed above" or assumes inherited chat memory.

## 1.4 Known tradeoffs (explicit)

- Bare "do it async" is convenient but can hide model-cost preferences. The initial design should allow controller defaults only when documented; otherwise it asks one concise execution-policy question before arming.
- Supporting all loop controllers is broader than the original arch-step-only request, but the shared runner is already the canonical owner and the feature would drift if each loop invents its own parser.
- `wait` is included in documentation only as already async/no child work, not as a model-routed controller.
- Sequential async is less fast than true parallel async, but it avoids state races and still gives the main benefit: fresh context for each loop unit.
- Keeping existing pinned evaluator defaults can surprise a user who expected one model phrase to apply everywhere. The docs and persisted policy need to distinguish `worker` policy from `evaluator` policy.
- Asking a question before arming is less magical than guessing, but it prevents silent expensive or wrong-provider execution.

## 1.5 Model and effort policy rules

The resolver should be shared, deterministic, and conservative.

Minimum supported inputs:

- Runtime family words: `codex`, `gpt`, `openai`, `claude`, `anthropic`.
- Model family words: `gpt`, `gpt-5.4`, `gpt 5.4`, `gpt 5.4 mini`, `gpt-5.5`, `opus`, `sonnet`, `haiku`, `claude opus`, `claude opus 4.7`.
- Effort words: `low`, `medium`, `high`, `xhigh`, plus any Claude-specific effort names that local doctrine and CLI help confirm.
- Mode words: `async`, `background`, `fresh context`, `external`, `external run`, `clean context`.

Resolver rules:

- Preserve the exact model family and version the user named.
- Infer runtime from model family only when unambiguous.
- Do not infer a specific model version from a vague provider word unless the controller has a documented default for that slot.
- Do not rewrite user shorthand to a cheaper/faster/smaller model without saying so and asking.
- Treat model and effort as separate fields. `gpt 5.4` does not imply `xhigh`; `xhigh` does not imply a model.
- Store both raw source text and normalized policy in state.
- Store a source label per field: `explicit`, `inferred_from_model`, `controller_default`, or `unresolved`.
- If any required field remains unresolved, do not arm the controller. Ask one concise question that names all missing fields.

Examples:

- "do it async" means async intent is explicit, but worker runtime/model/effort may still need a controller default or a question.
- "do it async on opus high" resolves runtime `claude`, model family `opus` with whatever exact version rules local doctrine supports, effort `high`.
- "async gpt 5.4 xhigh" resolves runtime `codex`, model `gpt-5.4`, effort `xhigh`.
- "use claude async" resolves runtime `claude`, but model and effort remain unresolved unless a controller default applies.
- "use 5.4 async" is ambiguous unless local doctrine explicitly treats bare `5.4` as GPT/Codex; safest behavior is to ask.

## 1.6 Child process command contracts

Codex child runs should be rendered through one shared adapter with this shape:

```sh
codex exec \
  --ephemeral \
  --disable codex_hooks \
  --cd <repo> \
  --dangerously-bypass-approvals-and-sandbox \
  --model <model> \
  -c model_reasoning_effort="<effort>" \
  -o <final-output-path> \
  <prompt>
```

Claude child runs should be rendered through one shared adapter with this shape, subject to confirmation against the installed CLI:

```sh
claude -p \
  --output-format json \
  --dangerously-skip-permissions \
  --settings '{"disableAllHooks":true}' \
  --model <model> \
  --effort <effort> \
  <prompt>
```

Command rules:

- Do not use Codex `--full-auto` for these children.
- Do not use a read-only sandbox for async worker/evaluator children unless that controller's existing design is explicitly read-only and the adoption plan preserves it.
- Do not combine Claude `--permission-mode` with `--dangerously-skip-permissions`.
- Close stdin for children unless a specific CLI requires otherwise.
- Capture stdout, stderr, final output path, JSON output when available, exit code, and duration.
- Include hook-suppression flags every time, even for children expected not to trigger hooks.
- Pass repo cwd explicitly.
- Include a prompt-level instruction that the child must not invoke loop-controller commands or arm nested auto modes.

# 2) Problem Statement (existing architecture + why change)

## 2.1 What exists today

The shared Stop-hook runner dispatches all installed controller families from one registry. It already launches fresh children for several review/evaluator/check paths, including implementation audits, arch-loop evaluators, audit-loop reviews, docs evaluators, and delay-poll checks. Those launches use a mix of helper functions, controller-specific pinned models, host-native runtime behavior, and direct prompt construction.

Important existing shapes:

- `arch-step auto-plan` arms state and then feeds literal next commands back into the visible parent session. It may run stages such as research, deep-dive, phase-plan, plan-enhance, fold-in, consistency-pass, and review-gate, but the planning work is not currently externalized as separate fresh worker children.
- `arch-step implement-loop` and `auto-implement` run implementation in the visible parent context, then trigger a fresh audit child. The audit result decides whether to continue or complete.
- `miniarch-step` mirrors the arch-step shape with a smaller workflow and a pinned mini audit child.
- `arch-loop` has a fresh evaluator that decides whether to continue, wait, or ask for parent work. When it asks for parent work, that work currently returns to the visible parent session.
- `arch-docs auto`, `audit-loop`, `comment-loop`, `audit-loop-sim`, and `delay-poll` already have child-run behavior, but they do not share one async execution policy object.
- `wait` sleeps/rechecks and resumes once; it has no model-routed worker child to externalize.

## 2.2 What’s broken / missing (concrete)

- There is no shared `async` intent model across loop skills.
- There is no shared execution-policy state object.
- There is no shared shorthand model/runtime/effort resolver for loop controllers.
- Existing child-run helpers do not uniformly capture persistent invocation artifacts.
- Parent-work continuations such as arch-step implementation and arch-loop parent work cannot currently be moved into fresh context as an opt-in mode.
- User-facing docs still imply structured controller commands rather than casual "do it async" language.
- Existing child helpers are close to what this feature needs, but their behavior is not centrally testable as "the async child contract."
- Existing pinned defaults are embedded in controller logic instead of represented as policy that can be inspected.
- There is no single artifact layout for child prompts, invocations, logs, outputs, and policy snapshots.
- There is no controller-wide way to say "this loop is async-capable, but this particular child slot must keep its existing evaluator default."

## 2.3 Constraints implied by the problem

- The implementation must be centered in `skills/arch-step/scripts/arch_controller_stop_hook.py` because that is the installed dispatcher for all loop skills.
- Skill doctrine must be updated in the owning skills, but it should not duplicate model-resolution rules in every `SKILL.md`.
- Tests must guard command flags because the dangerous/no-sandbox/hook-disabled details are easy to regress.
- State migration must be additive. Existing active states that lack async fields must continue to behave as non-async states.
- The feature must not depend on archived command files at runtime.
- The implementation needs to be careful about hook timeouts. A child run can be long, but the hook must already have a pattern for long-running controller children; this plan should reuse that pattern rather than inventing a daemon.

## 2.4 What success looks like in one scenario

User says:

```text
$arch-step auto-implement do it async on gpt 5.4 xhigh
```

Expected behavior:

1. The parent detects `auto-implement`, async intent, model `gpt-5.4`, effort `xhigh`, runtime `codex`.
2. The controller state stores an async worker policy with raw source text and normalized fields.
3. The parent arms the normal arch-step implement-loop state.
4. On Stop, the hook launches a fresh Codex worker child for the next implementation unit using hooks disabled and no sandbox.
5. The worker child reads the plan/doc/state from disk, performs only the requested implementation unit, writes a short result/worklog, and exits.
6. The hook launches or schedules the existing audit child according to the normal implement-loop contract.
7. If the audit says complete, the hook clears state and reports completion. If not complete, the next implementation unit is another fresh child.
8. If progress stalls, the existing no-progress rule blocks rather than spinning children forever.

The same pattern should work when the user says the casual version:

```text
do it async
```

but only if the controller has enough documented default policy to resolve runtime/model/effort. Otherwise the controller asks once before arming.

# 3) Research Grounding (external + internal “ground truth”)

<!-- arch_skill:block:research_grounding:start -->
# Research Grounding (external + internal “ground truth”)

## External anchors (papers, systems, prior art)

- Local `codex exec --help` - adopt as the command source of truth for Codex children. It confirms `--model`, `--cd`, `--ephemeral`, `--disable <FEATURE>`, `--dangerously-bypass-approvals-and-sandbox`, `--sandbox`, `--output-schema`, and `-o/--output-last-message`. It does not list model names, so exact Codex model availability still belongs to local model discovery or fail-loud user confirmation.
- Local `claude -p --help` - adopt as the command source of truth for Claude children. It confirms `--output-format json`, `--dangerously-skip-permissions`, `--settings`, `--model`, `--effort <low|medium|high|xhigh|max>`, `--json-schema`, and `--no-session-persistence`. The plan’s proposed Claude `--effort` shape is therefore valid for the installed CLI.
- No external web anchors are needed for this research pass. The relevant facts are local runtime CLI contracts and repo-owned controller behavior, not general agent-orchestration literature.

## Internal ground truth (code as spec)

- Authoritative behavior anchors (do not reinvent):
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - owns the installed Stop-hook controller registry and dispatches `implement-loop`, `auto-plan`, `miniarch-step-implement-loop`, `miniarch-step-auto-plan`, `arch-docs-auto`, `audit-loop`, `comment-loop`, `audit-loop-sim`, `delay-poll`, `code-review`, `wait`, and `arch-loop`.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - `run_codex_text_child` already uses `codex exec --ephemeral --disable codex_hooks --cd <cwd> --dangerously-bypass-approvals-and-sandbox`, optional `--model`, optional `-c model_reasoning_effort="<effort>"`, and `-o <last_message_path>`.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - `run_claude_text_child` already uses `claude -p --output-format json --dangerously-skip-permissions --settings '{"disableAllHooks":true}'` and optional `--effort`; it does not yet accept a model argument.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - structured Codex children currently use `--sandbox read-only` for some evaluator/check paths. Async mode must distinguish worker children from intentionally read-only evaluator/check children instead of blindly removing read-only semantics everywhere.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - miniarch audit defaults are pinned as `MINIARCH_STEP_AUDIT_MODEL = "gpt-5.4-mini"` and `MINIARCH_STEP_AUDIT_MODEL_REASONING_EFFORT = "xhigh"`.
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - arch-loop evaluator is intentionally Codex-only and fresh; tests lock the dangerous/no-sandbox and hook-disabled evaluator command shape.
  - `.gitignore` - ignores `.codex/*-state*.json` and `.claude/arch_skill/`, but does not currently ignore `.arch_skill/`. If `.arch_skill/async-runs` remains the artifact root, implementation must update ignore rules.
- Canonical path / owner to reuse:
  - `skills/arch-step/scripts/arch_controller_stop_hook.py` - canonical runtime owner for async mode. The feature must extend this dispatcher and its child-run helpers rather than creating a parallel orchestrator.
  - `skills/_shared/controller-contract.md` - canonical doctrine owner for shared controller state, parent-pass discipline, conflict gates, and hook-owned disarm behavior.
  - `skills/stepwise/references/model-and-effort.md` - canonical doctrine to reuse for exact-version-preserving model shorthand, runtime inference, effort resolution, and one consolidated question when required execution defaults are missing.
- Adjacent surfaces tied to the same contract family:
  - `skills/arch-step/SKILL.md` and `skills/miniarch-step/SKILL.md` - user-facing auto-plan and implement-loop doctrine must learn the async wording and preserve pinned audit defaults.
  - `skills/arch-loop/SKILL.md` and `skills/arch-loop/references/controller-contract.md` - must describe async parent-work mode while preserving the evaluator as the verdict source.
  - `skills/audit-loop/references/audit-loop-controller.md`, `skills/comment-loop/references/comment-loop-controller.md`, and `skills/audit-loop-sim/references/audit-loop-sim-controller.md` - already describe fresh child review paths and should converge onto shared async policy language.
  - `skills/delay-poll/references/delay-poll-controller.md` and `skills/wait/references/wait-controller.md` - delay-poll check children can adopt policy; wait should be documented as already async/no-child.
  - `README.md` and `docs/arch_skill_usage_guide.md` - public usage surfaces must explain casual async language if the invocation contract changes.
  - `tests/test_codex_stop_hook.py`, `tests/test_arch_loop_controller.py`, `tests/test_controller_registry.py`, `tests/test_claude_session_id_required.py`, `tests/test_legacy_fallback_removed.py`, and `tests/test_staleness_sweep.py` - existing regression surface for controller registry, state paths, child command shapes, and hook semantics.
- Compatibility posture (separate from `fallback_policy`):
  - Preserve existing non-async behavior. Async mode is opt-in, additive, and must not alter current controller state semantics when `async_execution` is absent.
  - Preserve existing controller command names. Do not introduce new public loop commands.
  - Preserve current pinned evaluator/audit defaults unless a controller explicitly opts into evaluator override.
  - Use a clean additive state extension (`async_execution`) rather than a compatibility shim or alternate runtime state root.
- Existing patterns to reuse:
  - `run_codex_text_child` and `run_claude_text_child` - runtime-native child invocation patterns with hooks disabled.
  - `load_controller_state`, `resolve_controller_state_for_handler`, and controller state specs - state validation and session-scoped lookup patterns.
  - `block_when_multiple_controller_states_armed` - conflict gate that async mode must respect before launching workers.
  - Existing tests around miniarch auto-plan state and miniarch audit model/effort - proof surface for keeping default behavior stable.
- Prompt surfaces / agent contract to reuse:
  - `skills/stepwise/references/model-and-effort.md` - shorthand model and effort contract.
  - `skills/stepwise/references/session-resume.md` - useful contrast for resumable sessions, but loop-controller async should start with one-shot fresh leaf children.
  - `skills/arch-epic/references/arch-step-integration.md` - explicitly warns against shelling out to nested arch-step work because parallel controllers would collide. This plan adopts that warning by keeping async orchestration inside the shared Stop hook.
- Native model or agent capabilities to lean on:
  - Codex CLI - model selection, effort configuration through `-c model_reasoning_effort`, cwd selection, ephemeral sessions, hook disabling, output-last-message capture, and no-sandbox execution.
  - Claude CLI - model selection, effort selection including `max`, JSON output, hook-suppressed settings, and dangerous permissions.
  - Existing child prompts - enough native model capability already exists for fresh audit/review/check work; this feature should improve routing and context isolation before adding heavier deterministic scaffolding.
- Existing grounding / tool / file exposure:
  - Child processes can read repo files and controller state from disk via explicit cwd and prompt paths.
  - The Stop hook can write state, create artifacts, and inspect doc markers before deciding whether to continue.
- Duplicate or drifting paths relevant to this change:
  - Child launch logic is split across text child helpers, structured child helpers, arch-loop evaluator logic, and review/check helpers.
  - Model/runtime/effort policy exists in Stepwise doctrine but not in loop-controller state.
  - Fresh child artifacts are currently temporary or controller-specific instead of persisted through one artifact contract.
- Capability-first opportunities before new tooling:
  - Use better child prompts and explicit disk grounding before adding a daemon, queue, or scheduler.
  - Use one shared policy resolver before adding per-controller parser syntax.
  - Use existing controller state validation before inventing a second state machine.
- Behavior-preservation signals already available:
  - `tests/test_codex_stop_hook.py` - command-shape and controller handler tests for core Stop-hook behavior.
  - `tests/test_arch_loop_controller.py` - arch-loop state/evaluator behavior and command-shape tests.
  - `tests/test_controller_registry.py` - controller registry completeness.
  - `tests/test_claude_session_id_required.py`, `tests/test_legacy_fallback_removed.py`, and `tests/test_staleness_sweep.py` - session-scoped state and stale/legacy state behavior.
  - `npx skills check` - package-level skill validation after `skills/` edits.

## Decision gaps that must be resolved before implementation

- None requiring user input before implementation. User confirmed the North Star on 2026-04-25.
- Phase planning resolves the remaining implementation choices:
  - Artifact root: use `.arch_skill/async-runs` and add the matching ignore rule.
  - Evaluator overrides: out of scope for v1; worker policy is user-selectable, evaluator/audit defaults stay controller-owned.
  - State hashes: hash the raw source text plus normalized worker/evaluator policy JSON.
  - Read-only structured slots: preserve read-only posture for existing read-only evaluator/check slots, including arch-docs evaluator and delay-poll checks; do not apply read-only posture to async worker children.
<!-- arch_skill:block:research_grounding:end -->

# 4) Current Architecture (as-is)

<!-- arch_skill:block:current_architecture:start -->
## 4.1 On-disk structure

The runtime owner is one Python Stop-hook runner:

```text
skills/arch-step/scripts/arch_controller_stop_hook.py
```

That runner is shared by the arch suite, including the miniarch surface. It defines:

- runtime roots: Codex state under `.codex/`, Claude state under `.claude/arch_skill/`
- controller state files: `implement-loop-state.json`, `auto-plan-state.json`, `miniarch-step-implement-loop-state.json`, `miniarch-step-auto-plan-state.json`, `arch-docs-auto-state.json`, `audit-loop-state.json`, `comment-loop-state.json`, `audit-loop-sim-state.json`, `delay-poll-state.json`, `wait-state.json`, `code-review-state.json`, and `arch-loop-state.json`
- controller registry entries in `CONTROLLERS`
- per-controller state specs in `ControllerStateSpec`
- child helpers for Codex and Claude text/structured children
- handler functions for every installed controller

The user-facing doctrine and references live beside the shipped skills:

```text
skills/_shared/controller-contract.md
skills/arch-step/SKILL.md
skills/arch-step/references/
skills/miniarch-step/SKILL.md
skills/arch-loop/SKILL.md
skills/arch-loop/references/
skills/audit-loop/references/
skills/comment-loop/references/
skills/audit-loop-sim/references/
skills/delay-poll/references/
skills/wait/references/
skills/stepwise/references/model-and-effort.md
skills/stepwise/references/session-resume.md
README.md
docs/arch_skill_usage_guide.md
```

Tests already cover the key runtime seams:

```text
tests/test_codex_stop_hook.py
tests/test_arch_loop_controller.py
tests/test_controller_registry.py
tests/test_claude_session_id_required.py
tests/test_legacy_fallback_removed.py
tests/test_staleness_sweep.py
```

Current ignore behavior matters for the proposed artifact root: `.gitignore` ignores `.codex/*-state*.json` and `.claude/arch_skill/`, but it does not ignore `.arch_skill/`.

## 4.2 Control paths (runtime)

The current controller lifecycle is:

1. Parent agent interprets the skill command.
2. Parent writes a session-scoped state file.
3. Parent ends its turn.
4. The installed Stop hook invokes `arch_controller_stop_hook.py`.
5. The runner resolves the active session state through `resolve_controller_state_for_handler`.
6. The runner validates state shape and session ownership.
7. The handler either launches a child, returns a parent continuation prompt, sleeps, disarms, or fails loud.

Current child execution paths:

- `run_codex_text_child` launches `codex exec --ephemeral --disable codex_hooks --cd <cwd> --dangerously-bypass-approvals-and-sandbox`, optionally with `--model` and `-c model_reasoning_effort="<effort>"`, and captures the final message with `-o`.
- `run_claude_text_child` launches `claude -p --output-format json --dangerously-skip-permissions --settings '{"disableAllHooks":true}'`, optionally with `--effort`; it does not yet accept `--model`.
- `run_codex_structured_child` launches a structured Codex child with `--sandbox read-only`; this is correct for existing read-only evaluator/check children but is not the right default for async worker children.
- `run_claude_structured_child` launches a structured Claude child with `--json-schema`, dangerous permissions, and hooks disabled.
- `run_arch_loop_evaluator` bypasses the generic structured Codex helper and launches a Codex-only evaluator with `-p yolo`, `--ephemeral`, `--disable codex_hooks`, `--dangerously-bypass-approvals-and-sandbox`, `-C <repo>`, `--output-schema`, and `-o`.

Current loop-specific behavior:

- `arch-step auto-plan` uses `AUTO_PLAN_STAGES`: `research`, `deep-dive-pass-1`, `deep-dive-pass-2`, `phase-plan`, and `consistency-pass`.
- `miniarch-step auto-plan` uses `MINIARCH_STEP_AUTO_PLAN_STAGES`: `research`, `deep-dive`, and `phase-plan`.
- `auto_plan_stage_complete` and `miniarch_step_auto_plan_stage_complete` detect progress by doc markers, not by controller-local progress state.
- `handle_auto_plan` and `handle_miniarch_step_auto_plan` return continuation prompts to the visible parent for the next planning stage.
- `handle_implement_loop` and `handle_miniarch_step_implement_loop` run a fresh audit child after parent implementation work, then keep or clear state based on `Verdict (code): COMPLETE|NOT COMPLETE`.
- `run_fresh_audit` can pin model and effort; miniarch uses that hook to pin audit to `gpt-5.4-mini` `xhigh`.
- `handle_arch_loop` runs the Codex evaluator, validates structured verdict fields, and returns parent work when the evaluator chooses `continue_mode=parent_work`.
- `run_fresh_review`, `run_fresh_comment_review`, and `run_fresh_sim_review` launch host-native fresh review children for audit/comment/sim loops.
- `run_delay_poll_check` launches host-native fresh structured check children.
- `handle_wait` has no model child; it is a time-based resume controller.

## 4.3 Object model + key abstractions

The current object model is mostly implicit:

- `HookRuntimeSpec` chooses state root by host runtime.
- `ControllerStateSpec` defines expected command and state filename.
- `ResolvedControllerState` points a handler at the active session-scoped state file.
- Per-controller `validate_*_state` functions enforce required fields, session ownership, and malformed `requested_yield` handling.
- `FreshAuditResult` and `FreshStructuredResult` carry subprocess results.
- `BLOCK_MARKERS` are the durable planning-stage completion contract for auto-plan controllers.
- Parent continuations are free-text prompts returned through `block_with_json`.

Missing abstraction:

- There is no `AsyncExecutionPolicy`.
- There is no first-class `ChildRunSpec`.
- There is no normalized worker/evaluator policy split.
- There is no shared artifact contract for child prompts, commands, logs, outputs, and policy snapshots.
- There is no single parser for casual async/model/effort language across loop controllers.

## 4.4 Observability + failure behavior today

Current strengths:

- Session-scoped state prevents the current session from accidentally consuming unrelated controller state.
- `block_when_multiple_controller_states_armed` prevents ambiguous concurrent controller ownership.
- Invalid JSON, wrong command, missing session id, mismatched session id, and malformed state disarm loudly.
- Existing tests lock important command shapes, including unsandboxed fresh review/audit paths and arch-loop evaluator flags.
- Miniarch audit pinning is already covered by tests.

Current gaps:

- Text children use temporary directories; prompt/command/stdout/stderr/final output are not preserved in a durable run directory.
- Structured children and arch-loop evaluator have separate command builders.
- Claude text children can set effort but not model.
- Existing child runtime decisions are scattered across helper functions and controller-specific code.
- Controller state does not explain why a child used a runtime, model, effort, or default.
- `.arch_skill/async-runs` is not currently ignored, so using it as an artifact root needs an ignore-rule change.

## 4.5 UI surfaces (ASCII mockups, if UI work)

Not applicable. The user surface is skill invocation language and terminal/controller messages.
<!-- arch_skill:block:current_architecture:end -->

# 5) Target Architecture (to-be)

<!-- arch_skill:block:target_architecture:start -->
## 5.1 On-disk structure (future)

Keep the canonical runtime owner and implement v1 inside it:

```text
skills/arch-step/scripts/arch_controller_stop_hook.py
```

Do not add a second runtime module in v1. Helper extraction can be a later refactor only after the in-runner contract is proven by tests.

Add or update tests in the existing test surface before creating new test families:

```text
tests/test_codex_stop_hook.py
tests/test_arch_loop_controller.py
tests/test_controller_registry.py
tests/test_claude_session_id_required.py
tests/test_legacy_fallback_removed.py
tests/test_staleness_sweep.py
```

Chosen artifact root:

```text
.arch_skill/
  async-runs/
    <controller>/
      <session-id>/
        <run-id>/
          policy.json
          prompt.txt
          command.json
          stdout.log
          stderr.log
          final.txt
          result.json
          metadata.json
```

Implementation must add `.arch_skill/async-runs/` to `.gitignore` in the same phase that creates artifacts. Do not move controller state into `.arch_skill/`; state stays under `.codex/` or `.claude/arch_skill/`.

## 5.2 Control paths (future)

Future generic path:

1. Parent detects the normal loop command and optional async intent from casual text.
2. Parent resolves an execution policy before arming or asks one consolidated question.
3. Parent writes the normal controller state plus optional `async_execution`.
4. Stop hook validates session ownership, controller conflicts, and async policy before launching children.
5. Handler reaches an eligible leaf slot.
6. Handler builds a `ChildRunSpec` from controller state, doc/ledger paths, prompt text, and worker/evaluator policy.
7. Shared child adapter renders the Codex or Claude command.
8. Child runs with hooks disabled and the intended sandbox/permission posture.
9. Handler records artifact metadata and validates the controller-specific marker, verdict, or structured result.
10. Handler advances, returns a continuation, waits, asks, completes, or disarms according to the existing controller contract.

Compatibility posture:

- Non-async behavior is preserved when `async_execution` is absent.
- Existing command names are preserved.
- Existing controller state roots are preserved.
- Existing pinned evaluator/audit defaults are preserved unless a controller explicitly adds an override contract.
- No runtime fallback or shim is introduced.

### 5.2.1 Async policy slots

Use separate policy slots:

- `worker`: implementation work, planning work, arch-loop parent work, or review/check work when the child is performing the main leaf task.
- `evaluator`: audit/evaluator/check slots whose identity is already part of controller correctness.

The user’s model phrase applies to `worker` by default. It applies to `evaluator` only when that controller explicitly supports evaluator override. This prevents “use opus high async” from silently replacing the arch-loop Codex evaluator or miniarch audit default.

### 5.2.2 `arch-step` and `miniarch-step` auto-plan

Async mode externalizes planning-stage work only after state is armed and the hook selects the next incomplete stage.

Rules:

- Non-async auto-plan continues to return a parent-visible continuation.
- Async auto-plan launches one fresh child for the next stage.
- Each stage child receives `DOC_PATH`, stage name, required completion marker, and relevant skill references.
- Children must not run `auto-plan`, `implement-loop`, `arch-loop`, or any nested loop-controller command.
- Hook advances only when marker validation passes.
- Miniarch keeps its trimmed stage list: `research`, `deep-dive`, `phase-plan`.

### 5.2.3 `arch-step` and `miniarch-step` implement-loop / auto-implement

Async mode externalizes implementation leaf work before the existing fresh audit gate.

Rules:

- Non-async implementation flow remains unchanged.
- Async worker child performs the next implementation unit from the approved Section 7 frontier.
- Existing audit child still owns the completion verdict.
- Miniarch audit remains pinned to Codex `gpt-5.4-mini` `xhigh`.
- Existing no-progress discipline must include worker and audit evidence in the fingerprint.

### 5.2.4 `arch-loop`

Async mode externalizes only evaluator-requested parent work.

Rules:

- `run_arch_loop_evaluator` remains the verdict source.
- Evaluator default remains the current Codex evaluator contract.
- `continue_mode=parent_work` launches an async worker child when async is enabled.
- `continue_mode=wait_recheck` remains hook-owned cadence behavior.
- Worker child receives `last_next_task`, compact state, raw requirements, caps, and no-progress context.
- After worker result, the hook returns to evaluator flow.

### 5.2.5 Already-child-based loop controllers

For `arch-docs auto`, `audit-loop`, `comment-loop`, `audit-loop-sim`, and `delay-poll`, async mode primarily converges existing children onto shared policy and artifacts.

Rules:

- Existing verdict semantics remain unchanged.
- Existing read-only structured evaluator/check children may remain read-only if their controller contract requires it.
- User model/effort policy applies only to eligible child slots.
- Default non-async behavior remains unchanged.

### 5.2.6 `wait` and `code-review`

- `wait`: document as already async/no-child. Do not add model routing.
- `code-review`: exclude from v1 because it is a one-shot review flow, not a loop controller. Its existing pinned review behavior stays unchanged.

## 5.3 Object model + abstractions (future)

Add an optional `async_execution` object to controller state:

```json
{
  "async_execution": {
    "enabled": true,
    "source_text": "do it async on gpt 5.4 xhigh",
    "source_hash": "sha256:...",
    "mode": "external_child",
    "worker": {
      "runtime": "codex",
      "model": "gpt-5.4",
      "effort": "xhigh",
      "runtime_source": "inferred_from_model",
      "model_source": "explicit",
      "effort_source": "explicit",
      "reason": "user requested gpt 5.4 xhigh"
    },
    "evaluator": {
      "runtime": "codex",
      "model": "gpt-5.4-mini",
      "effort": "xhigh",
      "runtime_source": "controller_default",
      "model_source": "controller_default",
      "effort_source": "controller_default",
      "reason": "miniarch audit default"
    },
    "artifact_root": ".arch_skill/async-runs/miniarch-step/SESSION",
    "active_child": null,
    "last_child": null,
    "progress_fingerprint": "sha256:...",
    "no_progress_count": 0
  }
}
```

Core abstractions:

- `AsyncIntent`: detected async/fresh-context intent and raw source text.
- `ModelEffortRequest`: extracted runtime/model/effort fragments before normalization.
- `ResolvedExecutionPolicy`: normalized runtime/model/effort with source labels and reasons.
- `ControllerAsyncDefaults`: per-controller and per-slot defaults.
- `ChildRunSpec`: role, runtime, model, effort, cwd, prompt, output paths, timeout, environment, and permission posture.
- `ChildRunResult`: process result, parsed output, artifact directory, duration, and failure summary.
- `ProgressFingerprint`: controller-specific evidence hash for no-progress detection.

Do not build a general orchestration framework. This is a policy plus child-adapter convergence inside the existing runner.

## 5.4 Invariants and boundaries

State boundaries:

- Stop hook remains the only dispatcher and disarmer.
- Children cannot clear controller state.
- Children cannot mutate `async_execution` directly.
- Children can write normal repo/doc outputs only when their assigned role allows it.
- Controller state roots remain `.codex/` and `.claude/arch_skill/`.

Runtime boundaries:

- Codex policy uses `codex exec`.
- Claude policy uses `claude -p`.
- Host runtime does not force child runtime.
- Model family implies runtime only when unambiguous.
- Requested exact model versions are not substituted.

Permission boundaries:

- Worker children run unsandboxed/no-approval with hooks disabled.
- Read-only evaluator/check children may preserve read-only semantics where the existing controller contract requires it.
- No `--full-auto` for Codex children.
- No Claude `--permission-mode` combined with `--dangerously-skip-permissions`.

Prompt/native-capability split:

- Native model capability owns the actual planning, implementation, review, and synthesis work inside each fresh child.
- Deterministic code owns state validation, policy resolution, command rendering, artifact capture, marker/verdict parsing, caps, conflict gates, and no-progress protection.
- Do not add OCR, fuzzy retrieval, or other capability-replacing harnesses; the feature needs better orchestration and grounding, not model substitution.

## 5.5 UI surfaces (ASCII mockups, if UI work)

Not applicable. The user-facing surface is natural language on existing skill commands:

```text
$miniarch-step auto-plan docs/PLAN.md do it async on gpt 5.4 xhigh
$arch-loop do it async on opus high
$audit-loop auto async with claude sonnet high
```
<!-- arch_skill:block:target_architecture:end -->

# 6) Call-Site Audit (exhaustive change inventory)

<!-- arch_skill:block:call_site_audit:start -->
## 6.1 Change map (table)

| Area | File | Symbol / Call site | Current behavior | Required change | Why | New API / contract | Tests impacted |
| ---- | ---- | ------------------ | ---------------- | --------------- | --- | ------------------ | -------------- |
| Controller registry | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `CONTROLLERS`, `ControllerStateSpec`, state constants | Registers all supported controllers with fixed state files and handlers. | Preserve registry; add async support inside registered handlers, not by adding public commands. | Avoid wrapper/orchestrator drift and arch-epic-style state collisions. | Existing controller names remain stable; `async_execution` is optional state. | `tests/test_controller_registry.py`, `tests/test_codex_stop_hook.py` |
| State resolution | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `resolve_controller_state_for_handler`, `load_controller_state`, `validate_session_id` | Resolves one session-scoped state and disarms invalid/mismatched state. | Validate optional `async_execution` after base state/session validation. | Async policy must not weaken session ownership or conflict gates. | Malformed async policy fails loud before child launch. | `tests/test_claude_session_id_required.py`, `tests/test_legacy_fallback_removed.py`, `tests/test_staleness_sweep.py` |
| Conflict gate | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `block_when_multiple_controller_states_armed` | Blocks when multiple suite controller states are armed for the same session. | Preserve unchanged; async children must not arm additional loop states. | Prevents nested controller races. | Child prompts and env must forbid nested loop arming. | `tests/test_codex_stop_hook.py`, `tests/test_arch_loop_controller.py` |
| Async intent parser | `skills/arch-step/scripts/arch_controller_stop_hook.py` | New parser/helper | No shared parser. | Add casual async/fresh-context intent detection. | User will say “do it async” rather than structured flags. | `AsyncIntent`, `ModelEffortRequest`, `ResolvedExecutionPolicy`. | New parser tests in existing stop-hook test surface or new focused test file |
| Model/effort resolver | `skills/stepwise/references/model-and-effort.md`; runner helper | New resolver/helper | Stepwise has doctrine; loop controllers do not. | Reuse Stepwise-style exact-version-preserving resolution and one-question failure shape. | Prevent silent provider/model/effort guessing. | Field sources: `explicit`, `inferred_from_model`, `controller_default`, `unresolved`. | New resolver tests |
| Controller defaults | `skills/arch-step/scripts/arch_controller_stop_hook.py` | New `ControllerAsyncDefaults` table | Defaults are hard-coded in helper calls or comments. | Represent worker/evaluator defaults per controller. | Needed to preserve pinned evaluator/audit defaults while letting workers vary. | Separate `worker` and `evaluator` policies. | Miniarch audit tests, arch-loop evaluator tests |
| Codex text child | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `run_codex_text_child` | Already supports model/effort and unsandboxed hook-suppressed execution, but uses temp dirs. | Route through `ChildRunSpec`, preserve command shape, add durable artifacts. | Good base path; needs observability and policy coupling. | `ChildRunSpec` -> Codex argv; artifact capture. | `tests/test_codex_stop_hook.py` command-shape tests |
| Claude text child | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `run_claude_text_child` | Supports dangerous permissions, hooks-disabled settings, JSON output, optional effort; no model argument. | Add model support and artifact capture. | User may request Claude model shorthand. | Claude text child accepts model and effort from policy. | Claude command-shape tests |
| Structured children | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `run_codex_structured_child`, `run_claude_structured_child` | Codex structured helper is read-only; Claude structured helper uses dangerous permissions. | Make permission posture explicit in `ChildRunSpec`; preserve read-only where intentional. | Async worker children need unsandboxed execution, but read-only check/evaluator slots should stay read-only. | `permission_posture`: `worker_unsandboxed` or `readonly_evaluator`. | Existing read-only evaluator/check tests plus new policy tests |
| Arch-loop evaluator | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `run_arch_loop_evaluator`, `ARCH_LOOP_EVAL_SCHEMA` | Codex-only evaluator with yolo, unsandboxed, hooks disabled, schema output. | Preserve as evaluator policy; optionally route artifact capture through shared child result path without changing argv. | Evaluator identity is part of correctness. | Evaluator default remains pinned unless explicit future override. | `tests/test_arch_loop_controller.py` |
| Arch-step auto-plan | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `AUTO_PLAN_STAGES`, `auto_plan_stage_complete`, `handle_auto_plan` | Hook returns parent-visible continuation for next planning stage. | If async enabled, launch one child for the selected stage and validate markers before advancing. | Externalizes planning work into fresh context while preserving doc-marker truth. | Stage child prompt contract. | Stop-hook handler tests |
| Miniarch auto-plan | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `MINIARCH_STEP_AUTO_PLAN_STAGES`, `miniarch_step_auto_plan_stage_complete`, `handle_miniarch_step_auto_plan` | Same parent-continuation pattern with trimmed stages. | Same async stage-child path, trimmed to `research`, `deep-dive`, `phase-plan`. | Requested scope includes miniarch. | Miniarch stage child prompt contract. | `tests/test_codex_stop_hook.py` |
| Implement loop | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `handle_implement_loop`, `handle_miniarch_step_implement_loop`, `run_fresh_audit` | Parent does implementation; hook runs fresh audit after parent stops. | If async enabled, launch worker child before the existing audit. | Makes actual implementation run from clean context while audit remains authoritative. | Worker result then audit result; progress fingerprint. | Implement-loop handler tests |
| Audit defaults | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `MINIARCH_STEP_AUDIT_MODEL`, `MINIARCH_STEP_AUDIT_MODEL_REASONING_EFFORT` | Miniarch audit is pinned to `gpt-5.4-mini` `xhigh`. | Preserve as evaluator policy. | Prevent user worker policy from accidentally downgrading audit. | `evaluator.source=controller_default`. | Existing miniarch audit pin tests |
| Arch-loop parent work | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `handle_arch_loop`, `last_next_task`, `last_continue_mode` | Evaluator asks parent to run next task. | If async enabled and mode is `parent_work`, launch worker child for `last_next_task`; then evaluate again. | This is the main arch-loop async expansion. | `arch-loop` worker prompt contract. | `tests/test_arch_loop_controller.py` plus new async parent-work tests |
| Arch-docs auto | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `run_arch_docs_evaluator`, `handle_arch_docs_auto` | Fresh evaluator exists; Codex structured evaluator is read-only. | Route eligible child policy/artifacts through shared path while preserving docs verdict semantics. | Prevent drift among child launch paths. | Existing evaluator result contract unchanged. | Existing/new arch-docs auto tests |
| Audit/comment/sim loops | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `run_fresh_review`, `run_fresh_comment_review`, `run_fresh_sim_review`, handlers | Fresh host-native review children exist. | Apply shared policy/artifacts when async/model preference is present. | These are already external loops and should not have separate policy parsing. | Review child policy slot. | `tests/test_codex_stop_hook.py` |
| Delay-poll | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `run_delay_poll_check`, `validate_delay_poll_state`, `handle_delay_poll` | Fresh structured check child; no parent work. | Route eligible check child through shared policy/artifacts; preserve interval/deadline/hash guards. | Include all looping skills without weakening wait semantics. | Check child policy slot; `requested_yield` remains invalid. | Delay-poll tests in `tests/test_codex_stop_hook.py` |
| Wait | `skills/arch-step/scripts/arch_controller_stop_hook.py` | `validate_wait_state`, `handle_wait` | Time-based resume only. | No model-routed async implementation; docs may state no-op. | There is no child work to externalize. | Async unsupported/no-op for wait. | Existing wait tests |
| Code review | `skills/code-review/*`; `handle_code_review` | One-shot review runner, not loop. | Exclude from v1. | User asked for looping skills; code-review has separate semantics. | No change. | Existing code-review tests |
| Artifact ignore | `.gitignore` | `.arch_skill/` missing | `.arch_skill/async-runs` would be tracked unless ignored. | Add ignore rule if `.arch_skill/async-runs` is final root. | Avoid polluting git status with child logs. | `.arch_skill/` or narrower path. | Simple file check plus docs verification |
| Shared doctrine | `skills/_shared/controller-contract.md` | Controller contract sections | No shared async execution policy. | Document optional `async_execution`, child no-recursion, artifact requirements, and slot defaults. | Keeps skill doctrine concise and consistent. | Shared async controller contract. | `npx skills check` |
| Skill docs | `skills/arch-step/SKILL.md`, `skills/miniarch-step/SKILL.md`, loop references | Auto modes documented as parent/hook continuations. | Add concise casual async wording and defaults. | User-facing behavior must match implementation. | Existing commands accept natural async language. | `npx skills check` |
| Usage docs | `README.md`, `docs/arch_skill_usage_guide.md` | No async mode examples. | Add examples and scope notes if public invocation behavior changes. | Prevent hidden feature knowledge. | Examples use casual language, not flags. | Docs re-read and path/command checks |

## 6.2 Migration notes

* Canonical owner path / shared code path:
  * `skills/arch-step/scripts/arch_controller_stop_hook.py` owns runtime behavior.
  * `skills/_shared/controller-contract.md` owns shared doctrine.
  * `skills/stepwise/references/model-and-effort.md` owns the model/effort resolution rule to reuse.
* Deprecated APIs (if any):
  * None for v1. Existing commands and state roots remain.
* Delete list (what must be removed; include superseded shims/parallel paths if any):
  * No user-facing delete in v1.
  * If helper extraction creates replacement child adapters, retire duplicate per-controller command rendering inside the same implementation phase rather than keeping parallel helpers.
* Adjacent surfaces tied to the same contract family:
  * Include: arch-step, miniarch-step, arch-loop, arch-docs auto, audit-loop, comment-loop, audit-loop-sim, delay-poll, wait docs.
  * Exclude: code-review one-shot review.
  * Defer: Gemini support and true concurrent workers.
* Compatibility posture / cutover plan:
  * Preserve current non-async behavior.
  * Additive optional `async_execution` state.
  * Clean convergence for child launch policy; no runtime bridge or fallback.
* Capability-replacing harnesses to delete or justify:
  * None found. Do not add daemon/queue/OCR/fuzzy/parser scaffolding for model reasoning; use prompt/context grounding and shared deterministic boundaries.
* Live docs/comments/instructions to update or delete:
  * Update shared controller doctrine, arch-step/miniarch-step docs, arch-loop docs, audit/comment/sim/delay/wait controller references, usage guide, and README if invocation text changes.
  * Preserve the existing arch-loop comment explaining evaluator authority split; update only if async parent-work changes the comment’s wording needs.
* Behavior-preservation signals for refactors:
  * `tests/test_codex_stop_hook.py`
  * `tests/test_arch_loop_controller.py`
  * `tests/test_controller_registry.py`
  * `tests/test_claude_session_id_required.py`
  * `tests/test_legacy_fallback_removed.py`
  * `tests/test_staleness_sweep.py`
  * `npx skills check` after skill package edits

## Pattern Consolidation Sweep (anti-blinders; scoped by plan)

| Area | File / Symbol | Pattern to adopt | Why (drift prevented) | Proposed scope (include/defer/exclude/blocker question) |
| ---- | ------------- | ---------------- | ---------------------- | -------------------------------------------------------- |
| Child invocation | `run_codex_text_child`, `run_claude_text_child`, structured helpers, arch-loop evaluator | `ChildRunSpec` plus shared artifact capture | Prevents four command builders from drifting on hooks/sandbox/model flags | include |
| Execution policy | Stop-hook state validators and Stepwise model doctrine | `async_execution` with worker/evaluator policy slots | Prevents per-controller parsing and hidden model defaults | include |
| Auto planning | `handle_auto_plan`, `handle_miniarch_step_auto_plan` | Stage-child prompt plus marker validation | Keeps auto-plan real while making work fresh-context | include |
| Implementation loops | `handle_implement_loop`, `handle_miniarch_step_implement_loop` | Worker child before existing audit child | Externalizes implementation without moving audit authority | include |
| Arch-loop | `handle_arch_loop`, `run_arch_loop_evaluator` | Async worker for `parent_work`, evaluator unchanged | Solves stale parent context without replacing evaluator truth | include |
| Review/check loops | audit/comment/sim/delay helpers | Shared policy/artifacts around existing child slots | Prevents already-external loops from becoming second-class async paths | include |
| Wait | `handle_wait` | Explicit no-op/no-child doctrine | Avoids fake model routing where no child exists | include docs only |
| Code review | `handle_code_review`, `skills/code-review/*` | Keep separate one-shot review architecture | Not a loop controller in requested scope | exclude |
| Artifact root | `.gitignore`, artifact writer | Ignore the chosen async artifact root | Prevents child logs in git status | include if `.arch_skill/async-runs` is kept |
<!-- arch_skill:block:call_site_audit:end -->

# 7) Depth-First Phased Implementation Plan (authoritative)

<!-- arch_skill:block:phase_plan:start -->
# Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; split Section 7 into the best sequence of coherent self-contained units, optimizing for phases that are fully understood, credibly testable, compliance-complete, and safe to build on later. If two decompositions are both valid, bias toward more phases than fewer. `Work` explains the unit and is explanatory only for modern docs. `Checklist (must all be done)` is the authoritative must-do list inside the phase. `Exit criteria (all required)` names the exhaustive concrete done conditions the audit must validate. Resolve adjacent-surface dispositions and compatibility posture before writing the checklist. Before a phase is valid, run an obligation sweep and move every required promise from architecture, call-site audit, migration notes, delete lists, verification commitments, docs/comments propagation, approved bridges, and required helper follow-through into `Checklist` or `Exit criteria`. The authoritative checklist must name the actual chosen work, not unresolved branches or "if needed" placeholders. Refactors, consolidations, and shared-path extractions must preserve existing behavior with credible evidence proportional to the risk. For agent-backed systems, prefer prompt, grounding, and native-capability changes before new harnesses or scripts. No fallbacks/runtime shims - the system must work correctly or fail loudly. If a bridge is explicitly approved, timebox it and include removal work; otherwise plan either clean cutover or preservation work directly. Prefer programmatic checks per phase; defer manual verification to finalization. Avoid negative-value tests and heuristic gates such as deletion checks, stale-term greps, doc inventory checks, and repo-shape policing. Also: document new patterns and gotchas in code comments at the canonical boundary when that prevents future misuse.

## Phase 1 - Async Policy Contract And Resolver

* Goal:
  * Establish the shared policy object and conservative natural-language resolver without changing any controller behavior when async mode is absent.
* Work:
  * Add the optional `async_execution` state contract, async intent parsing, model/runtime/effort normalization, controller defaults, and validation hooks that every later phase will reuse.
* Checklist (must all be done):
  * Define `AsyncIntent`, `ModelEffortRequest`, `ResolvedExecutionPolicy`, `ControllerAsyncDefaults`, and a validation result/failure shape in `skills/arch-step/scripts/arch_controller_stop_hook.py`.
  * Implement casual async intent detection for phrases including `async`, `background`, `fresh context`, `external`, `external run`, and `clean context`.
  * Implement exact-version-preserving model phrase normalization using Stepwise doctrine: GPT-family phrases infer Codex when unambiguous, Claude-family phrases infer Claude when unambiguous, and exact versions are never substituted.
  * Implement effort parsing for Codex values and Claude values confirmed by local CLI: `low`, `medium`, `high`, `xhigh`, and `max` for Claude.
  * Implement one consolidated unresolved-policy failure object that names every missing runtime/model/effort field instead of guessing.
  * Implement a controller defaults table with separate `worker` and `evaluator` slots.
  * Encode v1 evaluator policy: evaluator/audit defaults are not user-overridable; user model phrases apply to worker slots only.
  * Add `async_execution` validation after normal state/session validation and before any child launch.
  * Add source hashing over raw source text plus normalized worker/evaluator policy JSON.
  * Preserve current behavior when `async_execution` is absent.
* Verification (required proof):
  * Add resolver/state unit tests covering `do it async`, `background it`, `fresh context on opus high`, `gpt 5.4 xhigh`, exact version preservation, ambiguous bare versions, missing model/effort, controller defaults, malformed async state, source hash mismatch, and no-async backward compatibility.
  * Run the new resolver/state tests and the existing controller-state tests that cover session ownership and stale state.
* Docs/comments (propagation; only if needed):
  * Add one short code comment at the async policy definition explaining that `worker` and `evaluator` policy are intentionally separate because evaluator identity can be part of controller correctness.
* Exit criteria (all required):
  * Existing controller states without `async_execution` validate and behave exactly as before.
  * A valid async policy is inspectable in state with raw source text, normalized worker/evaluator policy, source labels, reasons, and source hash.
  * Missing or ambiguous required execution choices fail before controller arming or before child launch, never by falling back to a hidden model.
  * Evaluator override is impossible in v1 unless a later explicit plan changes the contract.
* Rollback:
  * Remove the optional async policy parser/validation code and tests. Since no handler behavior changes in this phase, rollback restores current behavior by deleting the additive state support.

## Phase 2 - Shared Child Adapter And Durable Artifacts

* Goal:
  * Converge external child process execution onto one auditable adapter while preserving existing Codex and Claude command semantics.
* Work:
  * Add `ChildRunSpec`, `ChildRunResult`, command rendering, artifact capture, and permission-posture handling for Codex and Claude children.
* Checklist (must all be done):
  * Implement `ChildRunSpec` with role, runtime, model, effort, cwd, prompt, output paths, timeout or inherited timeout behavior, environment, and permission posture.
  * Implement `ChildRunResult` with process result, parsed final text or JSON, artifact dir, duration, and failure summary.
  * Preserve Codex worker command shape: `codex exec --ephemeral --disable codex_hooks --cd <repo> --dangerously-bypass-approvals-and-sandbox --model <model> -c model_reasoning_effort="<effort>" -o <final> <prompt>`.
  * Preserve Claude worker command shape: `claude -p --output-format json --dangerously-skip-permissions --settings '{"disableAllHooks":true}' --model <model> --effort <effort> <prompt>`.
  * Add Claude model support to the text child path.
  * Preserve read-only permission posture for existing structured read-only evaluator/check slots, including arch-docs evaluator and delay-poll check.
  * Preserve arch-loop evaluator argv exactly and add artifact capture around the existing invocation without changing its tested command contract.
  * Write durable artifacts under `.arch_skill/async-runs/<controller>/<session-id>/<run-id>/`: `policy.json`, `prompt.txt`, `command.json`, `stdout.log`, `stderr.log`, final output as `final.txt` or `result.json`, and `metadata.json`.
  * Add `.arch_skill/async-runs/` to `.gitignore`.
  * Add a prompt footer for async worker children forbidding nested loop-controller commands and controller state cleanup.
  * Capture child failures with exit code, stderr/stdout summary, artifact dir, and controller-safe failure reason.
* Verification (required proof):
  * Add command-shape tests for Codex worker, Claude worker, Codex read-only structured child, Claude structured child, and arch-loop evaluator preservation.
  * Add artifact tests proving success and failure both leave the expected files.
  * Run the existing command-shape tests in `tests/test_codex_stop_hook.py` and `tests/test_arch_loop_controller.py`.
* Docs/comments (propagation; only if needed):
  * Add a concise code comment near permission-posture rendering explaining why worker children are unsandboxed while some evaluator/check children remain read-only.
* Exit criteria (all required):
  * Every new async child launch goes through the shared adapter.
  * Existing helper behavior remains test-proven for current non-async audit/review/evaluator/check paths.
  * Child artifacts are written under the ignored `.arch_skill/async-runs/` root.
  * Hook disabling and no-recursion prompt language are present on every async worker path.
* Rollback:
  * Revert the adapter and artifact wiring, remove the `.gitignore` entry if no artifact path remains, and restore helper calls to their previous command builders.

## Phase 3 - Arch-Step And Miniarch Planning Workers

* Goal:
  * Let `arch-step auto-plan` and `miniarch-step auto-plan` run planning stages in fresh external worker contexts when async mode is requested.
* Work:
  * Add async stage-worker execution to the auto-plan handlers while preserving the existing parent-visible continuation path for non-async runs.
* Checklist (must all be done):
  * Add stage prompt builders for arch-step stages: `deep-dive-pass-1`, `deep-dive-pass-2`, `phase-plan`, and `consistency-pass`.
  * Add stage prompt builders for miniarch stages: `deep-dive` and `phase-plan`.
  * Include `DOC_PATH`, stage name, required marker, relevant skill references, and no-nested-controller instruction in every stage worker prompt.
  * Modify `handle_auto_plan` so async-enabled states launch a stage worker instead of returning parent work for the selected stage.
  * Modify `handle_miniarch_step_auto_plan` the same way with the trimmed miniarch stage list.
  * Preserve current non-async continuation messages byte-for-byte where feasible.
  * Validate stage completion using existing marker functions after worker exit.
  * Fail loud and leave artifacts when a child exits non-zero or does not create the required marker.
  * Preserve legal reruns on partially complete docs by selecting from document truth, not controller-local progress fields.
* Verification (required proof):
  * Add handler tests for non-async arch-step auto-plan continuation unchanged.
  * Add handler tests for non-async miniarch auto-plan continuation unchanged.
  * Add async handler tests proving each family launches exactly one stage child for the next incomplete stage.
  * Add tests proving missing required markers block advancement and keep enough failure evidence.
  * Add tests proving completed stages are not rerun.
* Docs/comments (propagation; only if needed):
  * Add short doctrine notes to arch-step and miniarch auto-plan references after implementation, or defer wording to Phase 7 if no docs are touched in this code phase.
* Exit criteria (all required):
  * Async auto-plan uses fresh worker children for planning stage work.
  * Non-async auto-plan remains unchanged.
  * The hook still owns continuation and disarm.
  * Children cannot nested-run `auto-plan`, `implement-loop`, or `arch-loop`.
  * Miniarch keeps exactly one deep-dive pass.
* Rollback:
  * Remove the async branch in both auto-plan handlers and keep the policy/adapter foundation for later phases if still useful; otherwise roll back through Phase 2.

## Phase 4 - Arch-Step And Miniarch Implementation Workers

* Goal:
  * Let `implement-loop` and `auto-implement` run implementation work in fresh worker contexts before the existing fresh audit gate.
* Work:
  * Add async implementation-worker execution to arch-step and miniarch implement-loop handlers while preserving audit authority and non-async behavior.
* Checklist (must all be done):
  * Add implementation worker prompt builders that include `DOC_PATH`, `WORKLOG_PATH`, approved Section 7 frontier rules, reopened/incomplete phase guidance, and no-nested-controller instruction.
  * Modify `handle_implement_loop` to run an async worker child before `run_fresh_audit` only when async mode is enabled.
  * Modify `handle_miniarch_step_implement_loop` the same way.
  * Preserve `run_fresh_audit` as the authoritative completion gate.
  * Preserve miniarch audit evaluator default as Codex `gpt-5.4-mini` `xhigh`.
  * Add progress fingerprinting that includes relevant doc/worklog hashes, git diff or touched-file evidence, worker result summary, audit verdict, and next-task text.
  * Enforce the existing no-progress rule across async worker cycles.
  * Ensure worker failure blocks with artifact path and does not run audit as if implementation succeeded.
  * Ensure audit `COMPLETE` and `NOT COMPLETE` behavior remains the authoritative disarm/continue decision.
* Verification (required proof):
  * Add async implement-loop tests for worker launch before audit, worker failure, audit failure, audit `COMPLETE`, audit `NOT COMPLETE`, progress fingerprint changes, and no-progress block.
  * Preserve existing miniarch audit pin tests.
  * Run targeted implement-loop tests in `tests/test_codex_stop_hook.py`.
* Docs/comments (propagation; only if needed):
  * Add one code comment at the worker-before-audit boundary explaining that implementation can be externalized but audit still owns completion truth.
* Exit criteria (all required):
  * Async implementation work happens in a fresh child.
  * Audit verdict remains the only completion authority.
  * Non-async implement-loop behavior remains unchanged.
  * Miniarch audit default cannot be displaced by worker model policy.
  * Repeated no-progress async cycles fail loud rather than spinning.
* Rollback:
  * Remove the worker-before-audit branch and progress fingerprint additions; audit-only loop behavior remains as before.

## Phase 5 - Arch-Loop Async Parent Work

* Goal:
  * Let `arch-loop` run evaluator-requested parent work in fresh child contexts without changing evaluator authority.
* Work:
  * Add async worker execution for `continue_mode=parent_work`, then return to the existing evaluator flow.
* Checklist (must all be done):
  * Preserve `run_arch_loop_evaluator` as Codex-only evaluator policy.
  * Preserve existing evaluator command-shape tests and structured verdict validation.
  * Add an arch-loop worker prompt builder using raw requirements, compact state, `last_next_task`, caps, required skill audits, no-progress context, and no-nested-controller instruction.
  * Modify `handle_arch_loop` so async-enabled `parent_work` launches the worker child instead of returning a visible parent continuation.
  * Preserve non-async `parent_work` continuation behavior.
  * Preserve `wait_recheck` cadence behavior without launching worker children.
  * Record worker result summary and artifact dir in state fields that the next evaluator prompt can read.
  * Update no-progress fingerprinting for worker/evaluator cycles.
  * Fail loud on worker non-zero exit or missing result.
* Verification (required proof):
  * Add arch-loop tests for non-async parent continuation unchanged, async worker launch, worker failure, worker result recorded, evaluator rerun path, `wait_recheck` no-worker behavior, and evaluator default preservation.
  * Run targeted arch-loop tests in `tests/test_arch_loop_controller.py`.
* Docs/comments (propagation; only if needed):
  * Update or preserve the existing arch-loop authority-split comment so it remains true after async parent work is added.
* Exit criteria (all required):
  * Async arch-loop parent work runs in a fresh child.
  * Evaluator remains the sole qualitative verdict source.
  * Wait/recheck remains hook-owned.
  * Non-async arch-loop behavior remains unchanged.
* Rollback:
  * Remove the async branch for `parent_work` and retain existing evaluator-driven parent continuation behavior.

## Phase 6 - Existing Review, Docs, And Poll Loops

* Goal:
  * Converge already-child-based loop controllers onto shared async policy and artifacts without changing their verdict semantics.
* Work:
  * Route arch-docs, audit-loop, comment-loop, audit-loop-sim, and delay-poll child launches through the shared policy/adapter where eligible; document wait as no-op/no-child.
* Checklist (must all be done):
  * Update `run_arch_docs_evaluator` to use shared child result/artifact capture while preserving structured read-only evaluator behavior.
  * Update `run_fresh_review`, `run_fresh_comment_review`, and `run_fresh_sim_review` to accept eligible async worker policy and write durable artifacts.
  * Update `run_delay_poll_check` to use shared child result/artifact capture while preserving interval, deadline, prompt hash, resume hash, and read-only check semantics.
  * Keep `requested_yield` invalid for delay-poll.
  * Keep `wait` model-routing-free and no-child.
  * Preserve all existing ledger/controller block parsing semantics.
  * Preserve default behavior when async policy is absent.
* Verification (required proof):
  * Add/update tests for arch-docs evaluator command posture, audit-loop child policy routing, comment-loop child policy routing, audit-loop-sim child policy routing, delay-poll check policy/artifacts, delay-poll hash guards, and wait no-op behavior.
  * Run targeted tests in `tests/test_codex_stop_hook.py`.
* Docs/comments (propagation; only if needed):
  * Update loop reference docs in Phase 7; do not scatter user-facing docs in this code phase unless tests require fixture text updates.
* Exit criteria (all required):
  * Already-child-based loops use the shared adapter/policy where eligible.
  * Existing verdict, ledger, cap, interval, and hash semantics are unchanged.
  * Delay-poll and arch-docs read-only structured semantics remain explicit.
  * Wait remains a no-child controller.
* Rollback:
  * Restore direct helper calls for review/docs/poll loops while keeping earlier async support for arch-step/miniarch/arch-loop if unaffected.

## Phase 7 - Doctrine, Usage Docs, And Install Surface Sync

* Goal:
  * Make the shipped skill surface describe exactly how async mode works without requiring complex syntax from users.
* Work:
  * Update shared doctrine, owning skill docs, loop references, README, and usage guide so public behavior matches implementation.
* Checklist (must all be done):
  * Update `skills/_shared/controller-contract.md` with optional `async_execution`, worker/evaluator slot semantics, child no-recursion, artifact contract, and fail-loud policy.
  * Update `skills/arch-step/SKILL.md` and relevant arch-step references with concise async examples for `auto-plan`, `implement-loop`, and `auto-implement`.
  * Update `skills/miniarch-step/SKILL.md` and relevant miniarch references with concise async examples and miniarch audit default preservation.
  * Update `skills/arch-loop/SKILL.md` and `skills/arch-loop/references/controller-contract.md` with async parent-work behavior and evaluator default preservation.
  * Update audit-loop, comment-loop, audit-loop-sim, delay-poll, and wait references with their async support/no-op dispositions.
  * Update `docs/arch_skill_usage_guide.md` with casual examples such as `do it async`, `use opus high async`, and `gpt 5.4 xhigh`.
  * Update `README.md` to mention async mode in the install/usage surface because public invocation behavior changes.
  * Keep all docs command-first and concise; do not duplicate the full resolver rules in every `SKILL.md`.
* Verification (required proof):
  * Re-read every edited doc.
  * Run `rg` checks for every new command/path/model example added.
  * Run `npx skills check`.
* Docs/comments (propagation; only if needed):
  * This phase is the docs propagation phase; no separate propagation is needed.
* Exit criteria (all required):
  * Users can understand async mode from shipped docs without learning flags.
  * Shared doctrine is the single source of truth for policy semantics.
  * Skill-specific docs state only their own defaults and supported slots.
  * `npx skills check` passes.
* Rollback:
  * Revert docs to the pre-async wording if the implementation is rolled back; remove async examples from README and usage guide.

## Phase 8 - End-To-End Verification And Rollout Guardrails

* Goal:
  * Prove the full async mode works across representative controllers and fails loudly in the right places.
* Work:
  * Run the complete targeted proof set, tighten failure messages, and verify rollout behavior before considering implementation complete.
* Checklist (must all be done):
  * Run targeted unit/handler tests for resolver, state validation, child command shape, artifacts, arch-step/miniarch auto-plan, arch-step/miniarch implement-loop, arch-loop parent work, audit/comment/sim loops, delay-poll, and wait.
  * Run the existing broader relevant test modules: `tests/test_codex_stop_hook.py`, `tests/test_arch_loop_controller.py`, `tests/test_controller_registry.py`, `tests/test_claude_session_id_required.py`, `tests/test_legacy_fallback_removed.py`, and `tests/test_staleness_sweep.py`.
  * Run `npx skills check`.
  * Manually inspect representative failure messages for unresolved policy, model ambiguity, CLI missing, child non-zero exit, marker missing, state conflict, and no-progress block.
  * Verify `.arch_skill/async-runs/` artifact directories contain prompt, command, policy, logs, output, and metadata for success and failure cases.
  * Verify no async child prompt permits nested loop-controller arming or state cleanup.
  * Verify non-async loop invocations still behave as before.
* Verification (required proof):
  * Record exact test commands and outcomes in implementation worklog.
  * Record at least one successful async worker artifact inspection and one failure artifact inspection.
* Docs/comments (propagation; only if needed):
  * Sync any doc wording found stale during verification before declaring complete.
* Exit criteria (all required):
  * Casual async language resolves or fails loud as designed.
  * Fresh worker children can run through Codex or Claude according to policy.
  * Existing pinned evaluator/audit defaults are preserved.
  * Every adopted loop controller either supports async mode or has an explicit no-op/out-of-scope disposition.
  * Non-async behavior is preserved by tests.
  * `npx skills check` passes.
* Rollback:
  * Revert the async feature as a sequence: disable async arming/validation first, then child adapter routing, then docs. Preserve unrelated controller fixes if they are independently valid and tested.
<!-- arch_skill:block:phase_plan:end -->

# 8) Verification Strategy (common-sense; non-blocking)

## 8.1 Unit tests (contracts)

- Resolver tests for casual async detection, runtime inference, exact-version-preserving model normalization, effort parsing, controller defaults, unresolved-policy failure, and evaluator override rejection.
- State validation tests for absent `async_execution`, valid async policy, malformed async policy, source hash mismatch, active child conflict, missing worker fields, and conflicting controller state.
- Command-rendering tests for Codex worker, Claude worker, Codex read-only structured evaluator/check, Claude structured child, and arch-loop evaluator preservation.
- Artifact tests for success and failure paths: `policy.json`, `prompt.txt`, `command.json`, `stdout.log`, `stderr.log`, final output, structured result, and metadata.

## 8.2 Integration tests (flows)

- Auto-plan handler tests for arch-step and miniarch: non-async continuation unchanged, async child launch, marker validation, missing-marker block, and completed-stage skip.
- Implement-loop handler tests for arch-step and miniarch: worker-before-audit order, worker failure, audit failure, `COMPLETE`, `NOT COMPLETE`, progress fingerprint updates, no-progress block, and miniarch audit pin preservation.
- Arch-loop handler tests for non-async parent continuation, async parent-work child, worker failure, result recorded for evaluator, `wait_recheck` no-worker behavior, and evaluator default preservation.
- Existing child-loop tests for arch-docs auto, audit-loop, comment-loop, audit-loop-sim, delay-poll, and wait.
- Existing regression modules to keep in the required proof set:
  - `tests/test_codex_stop_hook.py`
  - `tests/test_arch_loop_controller.py`
  - `tests/test_controller_registry.py`
  - `tests/test_claude_session_id_required.py`
  - `tests/test_legacy_fallback_removed.py`
  - `tests/test_staleness_sweep.py`

## 8.3 E2E / device tests (realistic)

- No UI or device E2E is required.
- Run `npx skills check` after `skills/` package docs or agent surfaces change.
- Inspect at least one successful async artifact directory and one failed async artifact directory during final verification.
- Manually inspect representative terminal failure messages for unresolved policy, model ambiguity, missing CLI, child non-zero exit, missing stage marker, state conflict, and no-progress block.

# 9) Rollout / Ops / Telemetry

## 9.1 Rollout plan

- Ship async mode as opt-in only.
- Preserve existing command names and installed Stop-hook entry points.
- Preserve non-async behavior when `async_execution` is absent.
- Roll out in the phase order in Section 7 so the resolver and adapter exist before any controller starts using async workers.
- Keep code-review out of v1 and document that exclusion.

## 9.2 Telemetry changes

- No external telemetry is required.
- Durable local artifacts under `.arch_skill/async-runs/` are the operational evidence trail.
- Each child run metadata file should include controller, session id, role, runtime, model, effort, command, artifact paths, start/end timestamps, exit code, and failure summary when present.

## 9.3 Operational runbook

- If async policy is unresolved, ask one consolidated model/runtime/effort question before arming or launching.
- If a child command cannot start, fail loud, keep artifacts when possible, and do not pretend the controller completed work.
- If a child exits non-zero, record the artifact directory and block according to the owning controller contract.
- If a stage marker or verdict is missing after a child exits cleanly, fail loud instead of advancing.
- If `.arch_skill/async-runs/` appears in git status, add or repair the `.gitignore` rule.
- If multiple controller states are armed for the same session, block before launching a child.
- If no-progress fingerprints repeat, stop via the existing no-progress rule rather than spinning more children.

# 10) Decision Log (append-only)

## 2026-04-25 - Initial async loop-controller plan

Context

- User requested an optional async/fresh-context mode for arch-step auto modes and then broadened scope to looping skills, including arch-loop.

Options

- Limit the plan to arch-step only.
- Build an outer wrapper that shells out to loop commands.
- Add shared async mode inside the existing Stop-hook controller runner.

Decision

- Plan shared async mode inside the existing Stop-hook controller runner, covering real loop controllers and keeping `code-review` out of v1 as a one-shot review flow.

Consequences

- Async mode changes where leaf work runs, not who owns state.
- The runner remains the only dispatcher and disarmer.
- Model/runtime/effort resolution must be shared instead of per-controller.

## 2026-04-25 - North Star confirmed

Context

- User said “yes to north stars” for the active plan.

Options

- Keep the plan in draft and ask for more confirmation.
- Mark the plan active and continue through miniarch auto-plan.

Decision

- Status moved to `active`, and miniarch auto-plan may proceed through research, deep-dive, and phase-plan.

Consequences

- The plan can now be treated as approved intent for downstream planning.
- Later commands should resolve ordinary tradeoffs from Section 0, TL;DR, and the call-site audit instead of re-asking.

## 2026-04-25 - Deep-dive completed

Context

- The initial draft had broad architecture placeholders.

Options

- Leave Sections 4-6 as broad prose.
- Ground Sections 4-6 in the actual runner, adjacent docs, ignore rules, and tests.

Decision

- Sections 4-6 now ground the current runner architecture, target async policy/child-adapter architecture, and call-site inventory against `arch_controller_stop_hook.py`, adjacent skill docs, `.gitignore`, and existing tests.

Consequences

- Section 7 can now plan implementation against concrete call sites and preservation signals.

## 2026-04-25 - Phase plan completed

Context

- The hook advanced miniarch auto-plan to `phase-plan`.

Options

- Keep the earlier provisional phase sketch.
- Replace it with a modern authoritative phase plan with exhaustive checklists and exit criteria.

Decision

- Section 7 now has eight implementation phases: async policy contract, child adapter/artifacts, planning workers, implementation workers, arch-loop parent work, existing child-loop convergence, docs/doctrine, and end-to-end rollout verification.

Consequences

- The plan is now implementation-ready from a planning perspective.
- Implementation must follow Section 7 as the authoritative checklist.
