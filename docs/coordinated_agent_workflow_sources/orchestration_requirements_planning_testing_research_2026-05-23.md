# Requirements, Planning, Testing, And Orchestration Source Notes

Captured: 2026-05-23

Status: research notes for requirements gathering only.

Scope: recent practitioner material, public repos, official docs, papers, and
installable skills related to requirements gathering, phase planning,
architecture-before-code, testing, anti-overbuilding, review gates, and
coordinated coding-agent execution.

This file does not propose the future architecture. It records source-backed
patterns and the requirements pressure they create.

## Collection Method

Sources used in this pass:

- Grok/X query against the user's open Grok conversation, then direct X page
  checks for the returned posts.
- Skills CLI searches via `npx skills find` for requirements, planning, TDD,
  code review, architecture, specification, scope control, and test planning.
- Temporary local clones under `/tmp/arch_skill_orchestration_research/` for
  source inspection.
- Official Claude Code and Codex docs.
- Recent arXiv papers on coding-agent action bias and overeager edits.

The temporary clone path is a capture workspace only. Durable source handles
are the GitHub and docs links in this file.

## Recent X / Grok Leads

These came from a Grok query asking for posts from the last one to two months
about requirements gathering, phase planning, architecture-before-code, test
planning/execution, review gates, anti-overbuilding, and coordinator layers.

### LearnWithBrij: Claude Code five-layer agent development kit

- Source: `https://x.com/LearnWithBrij/status/2050803172793372769`
- Date: 2026-05-03
- Status: checked directly on X.
- Pattern: describes a layered Claude Code setup:
  - `CLAUDE.md` as memory for architecture rules, naming, test expectations,
    and repo maps.
  - Skills as on-demand, task-specific context.
  - Hooks as deterministic guardrails around tool use and session lifecycle.
  - Subagents with isolated context, model, tools, and permissions.
  - Plugins as a distribution unit for skills, agents, hooks, and commands.
- Requirement pressure: the future coordinator should separate always-on
  memory, on-demand skills, deterministic guardrails, and role-isolated agents
  instead of putting every instruction into one prompt.

### Atenov_D: plan mode, CLAUDE.md router, compact loops, hooks

- Source: `https://x.com/Atenov_D/status/2051623265685180587`
- Date: 2026-05-05
- Status: checked directly on X.
- Pattern: uses planning mode before code, `/init` to create a short
  `CLAUDE.md` architecture cheatsheet, Superpowers-style skills, GSD
  subagents, compaction, repeat/loop commands, and hooks.
- Confidence: high for the workflow ingredients; lower for numeric claims
  such as error-rate reductions.
- Requirement pressure: root guidance should stay short and route to deeper
  skills/docs. The coordinator needs an explicit plan-before-code mode.

### gbadamosixxl: architecture mapping before Cursor implementation

- Source: `https://x.com/gbadamosixxl/status/2056320840765985239`
- Date: 2026-05-18
- Status: checked directly on X.
- Pattern: Claude maps product architecture before code; Cursor implements a
  large share while the developer directs, reviews, and corrects.
- Confidence: thin post, but direct evidence of an architecture-before-code
  handoff.
- Requirement pressure: architecture planning and implementation can be
  separate roles or tools, but the handoff needs a written artifact.

### goyalshaliniuk: Claude Code as agent OS

- Source: `https://x.com/goyalshaliniuk/status/2057348162613088733`
- Date: 2026-05-21
- Status: checked directly on X.
- Pattern: describes an "agent OS" with input/permission handling, a knowledge
  layer, task graph, context compressor, memory, execution layer, event bus,
  hooks, subagent spawning, teammate mailboxes, finite-state protocol, task
  board, and worktree isolation.
- Confidence: useful conceptual decomposition, but not proof of a fully
  implemented workflow.
- Requirement pressure: orchestration state needs explicit concepts for
  permissions, tasks, memory, events, workspaces, and role communication.

### hanabusa104: Codex review gate in Claude Code

- Source: `https://x.com/hanabusa104/status/2057586093990752745`
- Date: 2026-05-21
- Status: checked directly on X.
- Pattern: mentions `/codex:setup --enable-review-gate` and `/codex:review`
  as ways to insert Codex review at Claude Code task boundaries.
- Confidence: low-view post, but the command names match public plugin repos.
- Requirement pressure: stop-time or phase-boundary review gates are active
  current practice, but they need token-cost, timeout, and loop-prevention
  controls.

## Skills CLI Leads

The Skills CLI searches were useful because they surfaced concrete skill
packages with install counts and discoverable source repos.

High-signal searches:

- `requirements`
  - `github/awesome-copilot@create-github-issues-for-unmet-specification-requirements`
    - about 8.6K installs.
  - `jwynia/agent-skills@requirements-analysis` - about 2K installs.
  - `cexll/myclaude@product-requirements` - about 894 installs.
  - `softaworks/agent-toolkit@requirements-clarity` - about 516 installs.
  - `softaworks/agent-toolkit@frontend-to-backend-requirements` - about
    463 installs.
  - `aj-geddes/useful-ai-prompts@requirements-gathering` - about 448 installs.
- `planning`
  - `supercent-io/skills-template@task-planning` - about 11.3K installs, but
    the guessed GitHub repo did not clone publicly in this pass.
  - `othmanadi/planning-with-files@planning-with-files-zh` - about 9.4K
    installs.
  - `othmanadi/planning-with-files@pi-planning-with-files` - about 5.9K
    installs.
  - `addyosmani/agent-skills@planning-and-task-breakdown` - about 3.8K
    installs.
- `tdd`
  - `mattpocock/skills@tdd` - about 149.1K installs.
  - `affaan-m/everything-claude-code@tdd-workflow` - about 5.7K installs.
  - framework-specific TDD skills for Spring Boot, Django, Laravel, and others.
  - `am-will/codex-skills@tdd-test-writer` - about 857 installs.
- `code review`
  - `obra/superpowers@requesting-code-review` - about 95.8K installs.
  - `obra/superpowers@receiving-code-review` - about 75.9K installs.
  - `wshobson/agents@code-review-excellence` - about 19.7K installs.
  - `supercent-io/skills-template@code-review` - about 12.5K installs.
- `architecture`
  - `mattpocock/skills@improve-codebase-architecture` - about 155.2K installs.
  - `wshobson/agents@architecture-patterns` - about 16.1K installs.
  - `github/awesome-copilot@architecture-blueprint-generator` - about 10.3K
    installs.
  - `flutter/skills@flutter-apply-architecture-best-practices` - about 9.9K
    installs.
  - `wshobson/agents@react-native-architecture` - about 9.5K installs.
- `specification`
  - `github/awesome-copilot@create-specification` - about 11.1K installs.
  - `github/awesome-copilot@create-github-action-workflow-specification` -
    about 9.3K installs.
  - `github/awesome-copilot@create-github-pull-request-from-specification` -
    about 9K installs.
  - `github/awesome-copilot@update-specification` - about 8.7K installs.
- `scope control`
  - Search quality was poor. Most results were generic or low-signal.
  - The practical scope-control material came from requirements, planning,
    adversarial review, and paper sources instead.
- `test planning`
  - Search quality was weak by install count, but `softaworks/agent-toolkit`
    contains an explicit `qa-test-planner` skill worth mining.

Requirement pressure:

- Skill discovery should be part of future design research, but install count
  alone is not enough. The coordinator needs a source-quality label:
  installed/popular, inspected, adopted, rejected, or lead-only.

## Specific Skills And Repos Inspected

Exact files and prompts worth mining later are indexed in
`external_skill_artifact_index_2026-05-23.md`.

### GitHub Awesome Copilot: specification workflows

- Repo: `https://github.com/github/awesome-copilot`
- Skills:
  - `https://skills.sh/github/awesome-copilot/create-specification`
  - `https://skills.sh/github/awesome-copilot/update-specification`
  - `https://skills.sh/github/awesome-copilot/create-github-issues-for-unmet-specification-requirements`
  - `https://skills.sh/github/awesome-copilot/create-github-issue-feature-from-specification`
- Pattern:
  - Specs are AI-ready, self-contained Markdown files.
  - Requirements, constraints, guidelines, interfaces, data contracts,
    acceptance criteria, test automation, rationale, dependencies, examples,
    edge cases, and validation criteria are separate sections.
  - Requirements and acceptance criteria get stable IDs such as `REQ-001` and
    `AC-001`.
  - Downstream skills extract unmet requirements into implementation issues
    and avoid duplicate issue creation.
- Requirement pressure:
  - Future plan artifacts need stable requirement IDs and explicit traceability
    from requirement to task to verification.
  - "Create issues for unmet spec requirements" is a useful pattern for
    converting strict plan review into actionable work without losing the
    original contract.

### Obra Superpowers: planning, subagent execution, TDD, verification

- Repo: `https://github.com/obra/superpowers`
- Skills:
  - `https://skills.sh/obra/superpowers/writing-plans`
  - `https://skills.sh/obra/superpowers/subagent-driven-development`
  - `https://skills.sh/obra/superpowers/test-driven-development`
  - `https://skills.sh/obra/superpowers/verification-before-completion`
  - `https://skills.sh/obra/superpowers/requesting-code-review`
- Prompt files inspected:
  - `skills/writing-plans/plan-document-reviewer-prompt.md`
  - `skills/subagent-driven-development/spec-reviewer-prompt.md`
  - `skills/subagent-driven-development/code-quality-reviewer-prompt.md`
- Pattern:
  - Planning runs before code and saves a concrete plan file.
  - Plans map files before tasks, avoid placeholders, include exact commands,
    include expected failures/passes, and use small TDD steps.
  - Subagent-driven development dispatches a fresh subagent per task, then
    runs two reviews: spec compliance first, code quality second.
  - The spec reviewer is told not to trust the implementer's report; it reads
    code and checks actual compliance.
  - Verification-before-completion forbids completion claims without fresh
    evidence.
- Requirement pressure:
  - A future coordinator must separate spec compliance review from code quality
    review. Passing one does not imply passing the other.
  - A task cannot be "done" because the implementer said so. The coordinator
    must validate evidence directly or through an independent verifier.

### Addy Osmani Agent Skills: spec gates, task breakdown, doubt, simplicity

- Repo: `https://github.com/addyosmani/agent-skills`
- Skills:
  - `https://skills.sh/addyosmani/agent-skills/spec-driven-development`
  - `https://skills.sh/addyosmani/agent-skills/planning-and-task-breakdown`
  - `https://skills.sh/addyosmani/agent-skills/incremental-implementation`
  - `https://skills.sh/addyosmani/agent-skills/doubt-driven-development`
  - `https://skills.sh/addyosmani/agent-skills/code-simplification`
  - `https://skills.sh/addyosmani/agent-skills/code-review-and-quality`
- Pattern:
  - Spec-driven development has gated phases: specify, plan, tasks,
    implement. Each phase needs human review before advancement.
  - Specs include commands, project structure, testing strategy, and boundaries
    grouped as Always, Ask First, and Never.
  - Task breakdown is read-only planning with dependency graphs, vertical
    slices, acceptance criteria, verification, dependencies, likely files, and
    checkpoints after small batches.
  - Doubt-driven development uses a fresh-context adversarial reviewer for
    non-trivial decisions, with a bounded loop and explicit reconciliation.
  - Incremental implementation emphasizes one vertical slice at a time and no
    speculative features.
- Requirement pressure:
  - Future planning must explicitly separate "always allowed," "ask first,"
    and "never allowed" actions for each run.
  - Overbuilding controls should be part of the plan review gate, not a vague
    personal preference.

### Matt Pocock Skills: behavior-first TDD and architecture investigation

- Repo: `https://github.com/mattpocock/skills`
- Skills:
  - `https://skills.sh/mattpocock/skills/tdd`
  - `https://skills.sh/mattpocock/skills/improve-codebase-architecture`
- Pattern:
  - TDD should be behavior-first through public interfaces.
  - Avoid horizontal "write all tests, then all implementation" planning.
  - Use vertical tracer bullets: one behavior, one failing test, one minimal
    implementation, repeat.
  - Architecture improvement begins with domain vocabulary and ADRs, then
    investigates deepening opportunities before proposing changes.
- Requirement pressure:
  - Test planning should specify behavior and public interfaces, not just
    internal implementation details.
  - Architecture work should begin with current domain language and existing
    decisions before adding abstractions.

### Softaworks Agent Toolkit: requirements clarity and QA planning

- Repo: `https://github.com/softaworks/agent-toolkit`
- Skills:
  - `https://skills.sh/softaworks/agent-toolkit/requirements-clarity`
  - `https://skills.sh/softaworks/agent-toolkit/frontend-to-backend-requirements`
  - `skills/qa-test-planner/SKILL.md` in the repo.
- Pattern:
  - Requirements clarity scores vague requirements out of 100 across
    functional clarity, technical specificity, implementation completeness,
    and business context.
  - The process iterates questions until the requirement is clear enough, then
    writes a PRD.
  - The frontend-to-backend requirements skill separates frontend needs from
    backend implementation choices and records uncertainties.
  - The QA planner produces test plans, manual test cases, regression suites,
    Figma validation notes, and bug reports with traceable steps.
- Requirement pressure:
  - The coordinator needs a requirements-clarity gate before phase planning
    when the request is vague, cross-team, or multi-day.
  - QA planning is its own role. It should not be bolted on at the end by the
    implementer.

### jwynia Agent Skills: requirements as hypotheses and system-design states

- Repo: `https://github.com/jwynia/agent-skills`
- Skill: `https://skills.sh/jwynia/agent-skills/requirements-analysis`
- Pattern:
  - Requirements are treated as hypotheses about what will solve a problem.
  - Diagnostic states include no problem statement, solution-first thinking,
    vague needs, hidden constraints, scope creep, and validated requirements.
  - Interventions include Jobs-to-be-Done, problem archaeology, specificity
    ladders, constraint inventory, assumption mapping, risk pre-mortem,
    MoSCoW, walking skeletons, and deferred-feature triggers.
  - The paired system-design material diagnoses under-engineering,
    over-engineering, missing integration points, unidentified risks, and no
    walking skeleton.
- Requirement pressure:
  - Future requirements gathering should explicitly detect solution-first
    prompts and scope creep before generating implementation phases.
  - Deferred work should have triggers for reconsideration, not just an
    unbounded backlog.

### wshobson/agents: AGENTS.md as a map, not encyclopedia

- Repo: `https://github.com/wshobson/agents`
- Pattern:
  - One source repo emits agents, skills, commands, and generated harness
    outputs for Claude Code, Codex, Cursor, OpenCode, and Gemini.
  - `AGENTS.md` is deliberately short and acts as a table of contents.
  - Claude imports `AGENTS.md` through `CLAUDE.md`.
  - Procedural detail lives in skills; reference material lives in docs.
  - Quality gates include structural validation, drift checks, tests, and
    smoke tests against generated artifacts.
- Requirement pressure:
  - Always-on coordinator guidance should be a router, not a giant operating
    manual.
  - The future system should be generated or validated across harnesses rather
    than hand-maintained in many slightly different files.

### Everything Claude Code: broad skill/rule marketplace and Codex support

- Repo: `https://github.com/affaan-m/ECC`
- Pattern:
  - Large cross-harness package with agents, skills, commands, hooks, rules,
    MCP configs, examples, and Codex support.
  - Uses specialized reviewers, TDD workflows, E2E runners, security review,
    language/framework-specific rules, and selective install profiles.
  - Contains examples of project-level `CLAUDE.md` files for real stacks and
    rules for Flutter/Dart, Kotlin/Android/KMP, Swift, web, and others.
  - The root docs explicitly warn not to stack install methods, because
    duplicated runtime surfaces cause broken setups.
- Requirement pressure:
  - Selective install and no-duplicate-surface rules matter. A future
    coordinator should avoid stacking old and new workflows in ways that leave
    conflicting defaults.
  - Domain-specific mobile testing rules can be mined later, especially for
    Flutter, Kotlin/Android, Swift, and HarmonyOS-like native surfaces.

### metaswarm: production-style multi-agent SDLC scaffold

- Repo: `https://github.com/dsifry/metaswarm`
- Status: cloned and inspected on 2026-05-23.
- Pattern:
  - 18 to 19 specialized agent personas, depending on file count/version.
  - 13 orchestration skills, plus rubrics, templates, commands, and install
    surfaces for Claude Code, Gemini CLI, and Codex CLI.
  - A nine-phase workflow: research, plan, design review gate, work-unit
    decomposition, orchestrated execution, final review, PR creation,
    PR shepherd, closure and learning.
  - A four-phase work-unit loop: implement, validate, adversarial review,
    commit.
  - Design review gate uses five reviewers: product manager, architect,
    designer, security, and CTO.
  - Plan review gate uses three adversarial reviewers: feasibility,
    completeness, and scope/alignment. All must pass before the plan is
    presented.
  - Adversarial review is binary pass/fail against written Definition of Done
    items. Evidence requires concrete file and line references.
  - Execution state and approved plans persist to disk under `.beads/` so
    context compaction does not erase the run.
  - Self-reflection extracts repeated user corrections, disagreements, and
    friction points into future skills, rubrics, or knowledge entries.
- Requirement pressure:
  - The user's desired workflow is very close to the stronger metaswarm shape,
    but the future design should not blindly copy it. It should preserve the
    useful gates while matching this repo's existing ArcSkill conventions and
    the user's stronger deletion/no-side-door posture.

### Codex plugin for Claude Code: `/codex:*` review and rescue

- Repo: `https://github.com/openai/codex-plugin-cc`
- Pattern:
  - Claude Code hosts commands such as `/codex:review`,
    `/codex:adversarial-review`, `/codex:rescue`, `/codex:status`,
    `/codex:result`, `/codex:cancel`, and `/codex:setup`.
  - `/codex:review` is read-only and can run in the background.
  - `/codex:adversarial-review` is steerable and focuses on tradeoffs,
    hidden assumptions, and risk areas.
  - `/codex:rescue` delegates tasks to Codex and can resume prior repo-scoped
    threads.
  - `/codex:setup --enable-review-gate` installs a stop-time review gate. The
    docs warn it can create long-running loops and drain usage.
  - The stop-gate prompt only blocks when the previous Claude turn actually
    made code changes and the reviewer finds a blocking issue.
- Requirement pressure:
  - Review gates need skip rules for status-only turns, setup-only turns, and
    no-edit turns.
  - Background review jobs need status, result, cancellation, and resume
    handles, not just a fire-and-forget subprocess.

### Sendbird `cc-plugin-codex`: Claude Code from Codex

- Repo: `https://github.com/sendbird/cc-plugin-codex`
- Pattern:
  - Codex hosts commands such as `$cc:review`, `$cc:adversarial-review`,
    `$cc:rescue`, `$cc:status`, `$cc:result`, `$cc:cancel`, and `$cc:setup`.
  - Background jobs are tracked per session and can nudge the parent thread
    when results are ready.
  - Review gate is disabled by default, skips no-edit turns, has a 15-minute
    timeout, and suppresses nested-session gate loops.
  - Model aliases default to strong Claude models for review, with flags to
    adjust model and effort.
- Requirement pressure:
  - The coordinator should distinguish parent/user-facing sessions from child
    worker sessions.
  - Review gates should be explicit opt-in for heavy runs, not a permanent
    hidden tax on all stops.

## Official Docs Checked

### Claude Code

- Skills and slash commands:
  `https://code.claude.com/docs/en/slash-commands`
  - Skills load on demand from `SKILL.md`.
  - They can include templates, scripts, examples, and references.
  - Skills can use dynamic context injection.
  - Claude Code docs explicitly position project skills as a better place for
    procedures that would otherwise bloat `CLAUDE.md`.
- Subagents:
  `https://code.claude.com/docs/en/sub-agents`
  - Claude delegates matching tasks to specialized subagents that work
    independently and return results.
  - Descriptions are the routing handle.
- Hooks:
  `https://code.claude.com/docs/en/hooks`
  - Hook events include session start, prompt submit, pre/post tool use,
    task created/completed, subagent start/stop, stop, worktree create/remove,
    pre/post compaction, and instruction loading.
  - Hooks can block actions with a specific exit behavior.
  - The docs describe `/goal` as a session-scoped stop hook shortcut.
- Memory:
  `https://code.claude.com/docs/en/memory`
  - Claude reads `CLAUDE.md`, not `AGENTS.md`.
  - For repos with `AGENTS.md`, the docs recommend a thin `CLAUDE.md` that
    imports `@AGENTS.md`.

### OpenAI Codex

- AGENTS.md guide:
  `https://developers.openai.com/codex/guides/agents-md`
  - Codex uses repository instructions and supports nested/specialized
    instruction files.
  - Overrides should live near the specialized work.
  - Alternate fallback instruction filenames can be configured.
- Subagents:
  `https://developers.openai.com/codex/subagents`
  - Custom Codex agents can specify fields such as model, effort, sandbox,
    MCP servers, and skills config.
  - Official examples include read-only explorers, reviewers, and docs
    researchers.
- Worktrees:
  `https://developers.openai.com/codex/app/worktrees`
- Automations:
  `https://developers.openai.com/codex/app/automations`
  - Thread automations can wake the same conversation on a recurring schedule,
    preserving thread context.
- Use cases:
  `https://developers.openai.com/codex/use-cases`
  - Official use cases include following durable goals, saving workflows as
    skills, reviewing pull requests, creating CLIs Codex can use, building
    responsive UIs with visual checks, native development, and QA via
    computer use.

Requirement pressure:

- The future coordinator should treat `AGENTS.md`/`CLAUDE.md`/skills/hooks as
  separate surfaces with separate jobs.
- "Plan mode" can be implemented as a role contract even when the harness
  does not expose the exact Claude UI feature.
- Hooks are useful for deterministic guardrails, but the primary workflow
  contract should still be visible in plan/run artifacts.

## Recent Papers Relevant To Anti-Overbuilding

### Coding Agents Don't Know When to Act

- Source: `https://arxiv.org/abs/2605.07769`
- Date: 2026-05-08.
- Finding: the authors introduce FixedBench, a benchmark of 200 coding tasks
  where no code changes are required. They report that even strong agents
  propose undesirable code changes in 35% to 65% of cases.
- Requirement pressure:
  - The coordinator needs an explicit "no code change required" success path.
  - Reproducing or proving the issue should be a gate before patching, when
    the work is framed as a bug fix.

### Overeager Coding Agents

- Source: `https://arxiv.org/abs/2605.18583`
- Date: 2026-05-19.
- Finding: OverEager-Bench measures out-of-scope actions on benign tasks
  across Claude Code, OpenHands, Codex CLI, Gemini CLI, and multiple base
  models. The abstract reports about 7,500 runs and shows that removing
  consent increases overeager behavior on shared models.
- Requirement pressure:
  - Extra features, unrelated refactors, and "while I was here" edits should
    be treated as review failures unless explicitly accepted into the plan.
  - The future workflow needs consent and scope gates that make inaction or
    refusal to edit a valid completion outcome.

## Prompt And Artifact Patterns Worth Preserving

These are not adopted designs yet. They are reusable patterns to keep available
for the next design phase.

- Requirements analyst prompt:
  - Detect whether the user gave a problem, a solution-first proposal, a vague
    need, hidden constraints, or scope creep.
  - Produce problem statement, assumptions, constraints, out-of-scope list,
    acceptance criteria, and open questions.
- Plan reviewer prompts:
  - Feasibility reviewer verifies real files, dependency order, existing
    conventions, and unstated assumptions.
  - Completeness reviewer maps every user requirement to plan items and
    verification steps.
  - Scope/alignment reviewer finds overbuilding, under-scoping, and divergence
    from the request.
- Spec compliance reviewer prompt:
  - Read the spec and Definition of Done.
  - Inspect the diff, not the implementer's self-report.
  - Return pass/fail with file:line evidence.
- Adversarial code review prompt:
  - Challenge ship readiness by focusing on expensive or user-visible failure
    modes: auth, data loss, idempotency, retries, race conditions, empty
    states, timeouts, rollback, migration hazards, and observability.
- Stop review gate prompt:
  - Return `ALLOW:` for status-only, setup-only, review-only, and no-edit
    turns.
  - Return `BLOCK:` only for blocking issues in the immediately previous
    edit-producing turn.
- QA planner artifact:
  - Test plan with scope, entry/exit criteria, risks, environments,
    deliverables, high-priority cases, pass criteria, and traceability.
  - Test cases with preconditions, steps, expected results, test data, and
    postconditions.
- AGENTS/CLAUDE pattern:
  - Keep root guidance short.
  - Make it a map/router.
  - Move procedures to skills.
  - Move long reference material to docs.
  - Make generated harness artifacts explicitly generated, validated, and not
    hand-edited.

## Requirement Pressure For The Future Workflow

These are requirements pressure, not final design:

- The workflow must distinguish requirements gathering, architecture/design,
  phase planning, task decomposition, implementation, validation, spec
  compliance review, code quality review, UI/QA review, and meta-learning.
- A task must have a written contract before implementation: problem,
  assumptions, constraints, in-scope, out-of-scope, acceptance criteria,
  verification, likely files, dependencies, and proof notes.
- A plan must include a no-code/no-change success path where appropriate.
- A plan must include explicit Always / Ask First / Never boundaries.
- Each requirement should be traceable to task(s), test(s), reviewer checks,
  and completion evidence.
- Every non-trivial plan needs at least feasibility, completeness, and
  scope/alignment pressure before implementation.
- Extra unrequested work should fail review unless the plan was updated and
  the user or required arbiter accepted the scope change.
- Same-agent self-verification is not enough. The implementer may report, but
  the coordinator or a separate verifier must inspect evidence.
- Spec compliance review and code quality review are separate gates.
- UI and QA planning should be independent roles for visual/native mobile work.
- Root `AGENTS.md` or `CLAUDE.md` should stay short and route to deeper
  documents or skills.
- Heavy review gates must have bounded iterations, timeout behavior,
  background status/result handles, and loop-prevention for nested sessions.
- Repeated user corrections should be captured into future instructions,
  skills, rubrics, or tests, but only after source-quality filtering.
- The workflow must support larger, multi-week projects without making tiny
  one-file edits pay the full orchestration cost.

## Open Questions For Later Design

- Which of these external skills should be used as direct source material,
  and which should only be inspirational?
- Should the coordinator store requirement IDs in one spec file, a plan file,
  BEADS-like task state, or a repo-local ArcSkill artifact?
- What is the exact Codex-native equivalent of Claude plan mode in this repo?
- How should the future workflow encode "no code change required" as a
  successful outcome?
- Which review gates are automatic, which are explicit, and which depend on
  task size/risk?
- How should the system prevent stale duplicate install/runtime surfaces when
  introducing new skills or coordinator commands?
- What is the right default for background external review jobs: wait,
  background with status/result, or opt-in only?
- What exact prompts should become reusable artifacts, and where should they
  live so root doctrine stays short?
