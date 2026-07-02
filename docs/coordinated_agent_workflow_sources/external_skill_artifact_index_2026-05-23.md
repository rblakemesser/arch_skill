# External Skill And Prompt Artifact Index

Captured: 2026-05-23

Status: research index for requirements gathering only.

Purpose: preserve concrete external artifacts worth mining during the later
design phase. This file is not an implementation proposal. It records exact
repos, files, and patterns discovered while researching coordinated coding
agents, requirements gathering, phase planning, testing, review gates,
anti-overbuilding, and native-mobile UI proof.

Temporary inspection root:

- `/tmp/arch_skill_orchestration_research/`

The temporary clones are not durable project state. Use the repo URLs and file
paths below as the durable handles.

## Repo Snapshots Inspected

| Repo | Branch | Snapshot | Notes |
|---|---:|---:|---|
| `https://github.com/github/awesome-copilot` | `main` | `5b049e4` | Large marketplace of agents, skills, and instructions. |
| `https://github.com/obra/superpowers` | `main` | `f2cbfbe` | Strong planning, subagent execution, spec review, and verification doctrine. |
| `https://github.com/addyosmani/agent-skills` | `main` | `250ffaa` | Clear spec/plan/task/implementation gates and portable commands. |
| `https://github.com/mattpocock/skills` | `main` | not re-read in this pass | TDD and architecture-investigation skills already summarized elsewhere. |
| `https://github.com/softaworks/agent-toolkit` | `main` | `3027f20` | Requirements clarity, QA planner, C4 architecture, handoff docs. |
| `https://github.com/jwynia/agent-skills` | `main` | `e02ec7e` | Requirements-as-hypotheses and system-design diagnostic patterns. |
| `https://github.com/wshobson/agents` | `main` | not re-read in this pass | Short AGENTS/CLAUDE router pattern and generated cross-harness artifacts. |
| `https://github.com/affaan-m/ECC` | `main` | `1e8c7e7` | Broad multi-harness reference with mobile, language, test, review, and prompt surfaces. |
| `https://github.com/dsifry/metaswarm` | `main` | `398be78` | Closest public SDLC-shaped multi-agent scaffold found. |
| `https://github.com/openai/codex-plugin-cc` | `main` | `807e03a` | Codex review/rescue plugin for Claude Code. |
| `https://github.com/sendbird/cc-plugin-codex` | `main` | `fd9379c` | Claude Code review/rescue plugin for Codex. |

## Highest-Value Artifacts To Mine Later

### Requirements And Specification

- `github/awesome-copilot`
  - `skills/create-specification/SKILL.md`
  - `skills/update-specification/SKILL.md`
  - `skills/create-github-issues-for-unmet-specification-requirements/SKILL.md`
  - `skills/create-github-issue-feature-from-specification/SKILL.md`
  - Pattern to steal: stable requirement and acceptance IDs, data contracts,
    edge cases, validation criteria, and conversion of unmet requirements into
    actionable implementation issues.
- `softaworks/agent-toolkit`
  - `skills/requirements-clarity/SKILL.md`
  - `skills/frontend-to-backend-requirements/SKILL.md`
  - Pattern to steal: clarity scoring, focused clarification rounds, explicit
    feature boundaries, and PRD output after requirements are concrete.
- `jwynia/agent-skills`
  - `skills/requirements-analysis/SKILL.md`
  - Pattern to steal: detect no problem statement, solution-first prompts,
    vague needs, hidden constraints, scope creep, and requirements as
    hypotheses before system design starts.
- `addyosmani/agent-skills`
  - `skills/spec-driven-development/SKILL.md`
  - Pattern to steal: specify, plan, tasks, implement gates; assumptions first;
    success criteria; and Always / Ask First / Never boundaries.

Requirement pressure:

- The future coordinator needs an explicit requirements-clarity role before
  architecture and phase planning when the request is vague, solution-first,
  cross-cutting, or multi-day.
- Requirement IDs should survive into tasks, tests, review gates, proof notes,
  and final status.
- "No code change required" and "ask before scope change" must be valid
  outcomes, not failures to make progress.

### Planning And Phase Decomposition

- `obra/superpowers`
  - `skills/writing-plans/SKILL.md`
  - `skills/writing-plans/plan-document-reviewer-prompt.md`
  - Pattern to steal: plans map files before tasks, include exact commands and
    expected results, forbid placeholders, and are written for implementers
    with little repo context.
- `addyosmani/agent-skills`
  - `skills/planning-and-task-breakdown/SKILL.md`
  - `.claude/commands/plan.md`
  - Pattern to steal: read-only plan mode, dependency graph, vertical slices,
    task size limits, checkpoints, and explicit parallelization constraints.
- `github/awesome-copilot`
  - `skills/create-implementation-plan/SKILL.md`
  - `skills/update-implementation-plan/SKILL.md`
  - `skills/structured-autonomy-plan/SKILL.md`
  - Agents: `agents/planner.agent.md`, `agents/task-planner.agent.md`,
    `agents/implementation-plan.agent.md`,
    `agents/project-architecture-planner.agent.md`
  - Pattern to steal: machine-readable plans with phase goals, tasks, files,
    dependencies, testing, risks, assumptions, and alternatives.
- `dsifry/metaswarm`
  - `skills/plan-review-gate/SKILL.md`
  - `rubrics/plan-review-rubric-adversarial.md`
  - Pattern to steal: three independent plan reviewers for feasibility,
    completeness, and scope/alignment; all must pass before a plan is
    presented.

Requirement pressure:

- Plan readiness cannot be only a parent-agent judgment on substantial runs.
  The plan needs separate pressure for feasibility, completeness, and scope.
- A plan that contains placeholders, fabricated paths, missing verification,
  missing dependency order, or unbounded tasks should fail before
  implementation.
- Parallel work needs non-overlapping file scopes, explicit shared contracts,
  and a checkpoint rule for integration.

### Implementation Orchestration

- `obra/superpowers`
  - `skills/subagent-driven-development/SKILL.md`
  - `skills/subagent-driven-development/implementer-prompt.md`
  - `skills/subagent-driven-development/spec-reviewer-prompt.md`
  - `skills/subagent-driven-development/code-quality-reviewer-prompt.md`
  - Pattern to steal: fresh implementer per task, spec compliance review first,
    code quality review second, and refusal to trust implementer reports.
- `dsifry/metaswarm`
  - `skills/orchestrated-execution/SKILL.md`
  - `skills/orchestrated-execution/guides/agent-coordination.md`
  - Pattern to steal: work-unit loop of implement, validate, adversarial
    review, commit; persistent context document; file-scope verification; and
    fresh reviewer on every re-review.
- `github/awesome-copilot`
  - `agents/gem-orchestrator.agent.md`
  - Pattern to mine carefully, not copy blindly: full phase router with
    researcher, planner, implementer, reviewer, critic, debugger,
    documentation writer, browser tester, mobile tester, and wave execution.

Requirement pressure:

- The future coordinator should decide whether a long-running implementer,
  fresh task implementer, or persistent domain worker is the right mode per
  work unit.
- Same-agent self-verification is not enough. The coordinator or a separate
  verifier must inspect commands, diffs, artifacts, and file scope directly.
- Review retries need fresh reviewers when independence matters, especially
  when the prior reviewer found blocking issues.

### Review Gates And Arbiters

- `obra/superpowers`
  - `skills/subagent-driven-development/spec-reviewer-prompt.md`
  - `skills/subagent-driven-development/code-quality-reviewer-prompt.md`
  - Pattern to steal: separate "did it build the requested thing" from "is it
    clean and maintainable."
- `dsifry/metaswarm`
  - `skills/design-review-gate/SKILL.md`
  - `skills/plan-review-gate/SKILL.md`
  - `rubrics/adversarial-review-rubric.md`
  - `rubrics/code-review-rubric.md`
  - `rubrics/test-coverage-rubric.md`
  - Pattern to steal: product, architecture, design, security, and CTO review
    before expensive implementation; binary pass/fail adversarial review
    against written Definition of Done.
- `openai/codex-plugin-cc`
  - `README.md`
  - `prompts/adversarial-review.md`
  - `prompts/stop-review-gate.md`
  - Pattern to mine: `/codex:review`, `/codex:adversarial-review`,
    `/codex:rescue`, `/codex:status`, `/codex:result`, `/codex:cancel`, and
    optional `/codex:setup --enable-review-gate`.
- `sendbird/cc-plugin-codex`
  - `README.md`
  - `prompts/adversarial-review.md`
  - `prompts/stop-review-gate.md`
  - `internal-skills/review-runtime/runtime.md`
  - Pattern to steal: background review jobs with status/result/cancel,
    no-edit skip rules, timeout, nested-session gate suppression, and
    structured review output.

Requirement pressure:

- Completion gates need to know what surface they are judging: plan
  completeness, spec compliance, code quality, visual proof, security, or
  final integration.
- Heavy stop-time gates must skip status-only, review-only, setup-only, and
  no-edit turns.
- Background arbiters need durable job IDs and result handles. Fire-and-forget
  subprocesses are too easy to lose.

### Testing And QA Planning

- `softaworks/agent-toolkit`
  - `skills/qa-test-planner/SKILL.md`
  - Pattern to steal: independent QA role that creates test plans, manual test
    cases, regression suites, Figma validation notes, and bug reports with
    preconditions, steps, expected results, environments, and evidence.
- `mattpocock/skills`
  - `skills/tdd/SKILL.md`
  - Pattern already summarized: test through public interfaces and use
    vertical tracer bullets.
- `addyosmani/agent-skills`
  - `skills/test-driven-development/SKILL.md`
  - `skills/incremental-implementation/SKILL.md`
  - Pattern to steal: small vertical slices and no speculative features.
- `affaan-m/ECC`
  - `.github/prompts/tdd.prompt.md`
  - `commands/flutter-test.md`
  - `commands/kotlin-test.md`
  - `commands/test-coverage.md`
  - Pattern to mine: language-specific test runners and coverage gates across
    Flutter/Dart, Kotlin, Swift, web, and other stacks.

Requirement pressure:

- QA planning should happen before implementation for risky or user-visible
  work, not only after the implementer says code is done.
- Tests must map to requirements and acceptance criteria, not just to code
  paths that were easy to test.
- For bug fixes, reproducing or falsifying the issue should be part of the
  workflow before patching when feasible.

### Native Mobile And UI Verification

- `github/awesome-copilot`
  - `agents/gem-mobile-tester.agent.md`
  - `agents/gem-designer-mobile.agent.md`
  - `agents/gem-implementer-mobile.agent.md`
  - Pattern to mine: mobile tester role with iOS/Android simulator checks,
    Detox/Maestro/Appium, logs, screenshots, crash reports, gestures,
    lifecycle, push notifications, platform-specific UI concerns, and
    performance checks.
- `affaan-m/ECC`
  - `agents/flutter-reviewer.md`
  - `agents/kotlin-reviewer.md`
  - `agents/swift-reviewer.md`
  - `commands/flutter-test.md`
  - `commands/kotlin-test.md`
  - `.cursor/rules/flutter*` did not appear in this clone, but related
    Flutter/Kotlin/Swift review and test surfaces are present.
- `dsifry/metaswarm`
  - `skills/visual-review/SKILL.md`
  - Pattern to mine for web/presentation capture only. It is not sufficient
    for native mobile by itself.
- Local psmobile research remains the stronger native-mobile proof source:
  `docs/coordinated_agent_workflow_sources/ui_visual_quality_research_2026-05-23.md`.

Requirement pressure:

- Native-mobile UI proof needs a dedicated role contract, not a web visual
  reviewer with different commands.
- Evidence should include simulator/device identity, app bundle/package,
  platform, OS/API version, orientation, screen size, route/state, gesture
  sequence, screenshots, logs, and accessibility/UI hierarchy when available.
- A simulator launch, passing build, widget test, generated XCUITest/Espresso
  test, or one screenshot does not prove UI quality by itself.

### AGENTS, CLAUDE, Skills, Hooks, And Install Surfaces

- `addyosmani/agent-skills`
  - `AGENTS.md`
  - `CLAUDE.md`
  - Pattern to steal: root guidance points to skills and commands, forbids
    vague skills, and avoids duplicated content between skills.
- `wshobson/agents`
  - `AGENTS.md`
  - `CLAUDE.md`
  - `docs/agents.md`
  - Pattern to steal: AGENTS as map/table of contents; detail lives in skills
    and docs; generated harness artifacts are validated.
- `affaan-m/ECC`
  - `.codex/AGENTS.md`
  - `.codex/agents/reviewer.toml`
  - `.codex/agents/explorer.toml`
  - `.codex/agents/docs-researcher.toml`
  - `.cursor/hooks/*`
  - `.kiro/hooks/*`
  - Pattern to mine: cross-harness distribution, subagent configs, hooks, and
    explicit warnings about duplicate runtime surfaces.
- `dsifry/metaswarm`
  - `AGENTS.md`
  - `CLAUDE.md`
  - `templates/AGENTS.md`
  - `templates/CLAUDE.md`
  - `hooks/session-start.sh`
  - Pattern to mine: platform-specific instruction routing and diagnostic
    status checks.

Requirement pressure:

- Root always-on instructions should stay short and act as a router.
- New coordinator surfaces must not leave stale duplicate command, skill, or
  instruction paths that users can accidentally invoke.
- Any generated harness artifacts need a clear generated/validated/owned
  status, so agents do not hand-edit stale copies.

## Patterns To Preserve As Raw Materials

- Requirements analyst: problem statement, assumptions, constraints,
  in-scope, out-of-scope, acceptance criteria, open questions.
- Plan reviewers: feasibility, completeness, scope/alignment.
- Design reviewers: product manager, architect, designer, security, CTO.
- Implementation loop: implement, coordinator-run validation, fresh
  adversarial review, commit.
- Review split: spec compliance first, code quality second.
- UI proof split: visual/taste review, deterministic geometry/accessibility
  review, native-mobile device/simulator proof, and design-source parity.
- Status surface: active plan, phase, gate state, blocking findings, last
  commit, next action.
- Cleanup posture: delete known-bad paths in scope and use Git history as the
  archive, while protecting unrelated user-owned work.

## Cautions From The Source Material

- `github/awesome-copilot/agents/gem-orchestrator.agent.md` is intentionally
  maximal and says the orchestrator never executes code directly. That is a
  useful contrast point, not necessarily a fit for Codex in this repo.
- `dsifry/metaswarm` is close to the user's desired shape, but copying its full
  SDLC scaffold could overbuild smaller tasks. The future design needs
  risk-scaled activation.
- Stop-time review gates can be expensive and can loop. They need explicit
  skip rules, timeout behavior, nested-session suppression, and result handles.
- Broad marketplaces like `affaan-m/ECC` and `github/awesome-copilot` contain
  many low-signal or domain-specific artifacts. Mine exact files, do not adopt
  by install count alone.
