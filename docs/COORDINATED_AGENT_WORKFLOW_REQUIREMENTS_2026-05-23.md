# Coordinated Agent Workflow Requirements

Status: requirements gathering only.

Date: 2026-05-23.

Scope: observed Codex usage patterns from recent local history, plus the
current request to move ArcSkill-style workflows toward explicit roles and a
top-level coordinator that dispatches agents.

This document intentionally does not propose an implementation architecture.
It records what the future workflow must protect, what behavior the user has
repeatedly asked for, and what evidence led to those requirements.

## Evidence Scope

The history pass used `$agent-history` against local Codex history. The doc
also includes external X/Grok material supplied by the user, direct BrowserOS
checks against signed-in X pages, a targeted read of the psmobile visual-proof
methodology, and a small secondary web-search pass.

Assumptions:

- Runtime: Codex.
- Time window: roughly the last 36 hours before the current session, with the
  current request included separately.
- Project scope: both the current `arch_skill` repo and all-project Codex
  history, because many relevant workflow sessions occurred in adjacent repos
  while using ArcSkill patterns.
- Evidence quality: `/goal` commands and user prompts are exact when sourced
  from `~/.codex/history.jsonl` or rollout JSONL. Session summaries from
  `state_5.sqlite` are exact metadata but still only summaries.

Primary helper runs:

- `sessions --scope all-projects --since 36h`: 115 matches.
  Run: `/var/folders/cr/8sccc69d0rg1b8dsp42v7q900000gn/T/agent-history/20260523T121445Z-sessions-83070f37`
- `commands --scope all-projects --since 36h`: 59 matches.
  Run: `/var/folders/cr/8sccc69d0rg1b8dsp42v7q900000gn/T/agent-history/20260523T121447Z-commands-dcdfd461`
- Current-project prompt recall: 244 matches.
  Run: `/var/folders/cr/8sccc69d0rg1b8dsp42v7q900000gn/T/agent-history/20260523T121425Z-prompts-fbcda249`
- Correction/friction search.
  Run: `/tmp/agent-history/arch-req-corrections/20260523T121503Z-search-7b83eb41`
- Visual/proof search.
  Run: `/tmp/agent-history/arch-req-visproof/20260523T121503Z-search-7b83eb41`
- Plan/work-log search.
  Run: `/tmp/agent-history/arch-req-docs/20260523T121502Z-search-7b83eb41`

Limitations:

- Some prompt recall records are global Codex prompt history. They are exact
  user text, but not always strong evidence of the current repo.
- The search helpers can return repeated `thread_goal_updated` events for one
  long-running goal. Repetition was treated as reinforcement of the same
  pattern, not as independent new requirements.
- This pass did not do a full transcript audit of every session. It sampled
  exact prompts, commands, session summaries, and bounded search output.
- Grok was useful for finding current X leads quickly, but its summaries were
  treated as lead material until checked against direct X posts, public repos,
  or official docs.
- Generic web search was lower signal for current practitioner behavior than
  Grok plus direct X verification. It was used as a secondary check, not as
  the primary evidence source.
- psmobile was inspected read-only. Its dirty and untracked files were treated
  as user-owned and not modified.

## External Source: Simon Last X Thread

The user supplied a Simon Last thread from 2026-05-22 about running coding
agents on large projects. BrowserOS was used to find the source posts on X and
fill in the truncated "Show more" portions visible in the user's pasted copy.

Source posts found:

- 1: `https://x.com/simonlast/status/2057978156183957995`
- 2: `https://x.com/simonlast/status/2057978157500961133`
- 3: `https://x.com/simonlast/status/2057978158796959775`
- 4: `https://x.com/simonlast/status/2057978160231428447`
- 5: `https://x.com/simonlast/status/2057978161632280829`
- 6: `https://x.com/simonlast/status/2057978162982891596`
- 8: `https://x.com/simonlast/status/2057978164253794594`
- 9: `https://x.com/simonlast/status/2057978165616873837`
- 10: `https://x.com/simonlast/status/2057978167080738872`

Searches for `from:simonlast "7/"` and `from:simonlast "11/" "agent"` did
not find matching posts from this thread. The thread evidence is therefore
recorded as posts 1-6 and 8-10, rather than assuming a missing post.

Requirements read from the thread:

- The workflow must support larger units of work than a single small ticket.
  The planning surface should be able to hold projects that would normally
  occupy a strong engineer for weeks.
- A long-running implementer role must be considered a first-class operating
  mode. The coordinator should not assume every implementation phase starts
  with a blank short-lived session.
- Persistent task lists are central state. Each task needs the work request,
  verification method, and completion proof notes before it can be trusted.
- Planning should be a primary activity, not a side note. Plan docs need enough
  interface-level detail and end-to-end verification detail for another agent
  to execute without reconstructing intent from chat.
- Review must happen before task completion. A fresh read-only reviewer should
  compare the diff against the task and plan, then return gaps before a task is
  treated as done.
- The role model needs at least planner, implementer, adversarial reviewer,
  black-box tester, issue triager, and deep code reviewer responsibilities.
  These can be distinct agents or distinct role contracts, but their boundaries
  must be explicit.
- The human should not be the normal executor for PR creation, terminal
  testing, CI checking, or proof gathering. The coordinator must make the agent
  produce the proof, leaving the human to inspect and steer.
- The workflow must have a meta-improvement loop. Mistakes discovered during a
  run should become future instructions, task templates, verification rules, or
  harness improvements.
- The workflow must also guard against over-engineering. Adversarial review and
  meta-process changes are necessary, but they need scope boundaries so they do
  not turn every task into a redesign.

Fit with the user's current request:

- The thread reinforces the move from one in-session Codex worker to a
  coordinator that dispatches specialized roles.
- It supports the user's desire for persistent plan docs, explicit proof
  notes, independent arbiters, and less human-in-the-loop execution.
- It also adds a tension that the future design must preserve: be aggressive
  enough to remove bad defaults and improve the process, but bounded enough
  not to create a bloated workflow that makes ordinary work harder.

## External Source: Grok Research And Prior Art

The user also supplied an open Grok conversation:

- Grok conversation:
  `https://x.com/i/grok?conversation=2058159982198087747`
- Archived Grok answer notes:
  `docs/coordinated_agent_workflow_sources/grok_conversation_2058159982198087747.md`
- Verified source notes:
  `docs/coordinated_agent_workflow_sources/x_prior_art_source_notes_2026-05-23.md`
- UI visual-quality source notes:
  `docs/coordinated_agent_workflow_sources/ui_visual_quality_research_2026-05-23.md`
- Requirements, planning, testing, and orchestration source notes:
  `docs/coordinated_agent_workflow_sources/orchestration_requirements_planning_testing_research_2026-05-23.md`
- External skill and prompt artifact index:
  `docs/coordinated_agent_workflow_sources/external_skill_artifact_index_2026-05-23.md`

The Grok conversation produced useful recent X leads, especially for
practitioner examples from April and May 2026. Direct X verification then
separated stronger workflow evidence from lower-confidence launch posts or
one-off observations.

Strong prior-art patterns captured from the verified source notes:

- Worktree isolation is now a common coordination primitive. Sources describe
  permanent worktrees, per-task worktrees, or one worktree per agent/task so
  parallel agents do not collide.
- Several users combine models by role. Examples include Claude for
  high-level architecture or long-context planning and Codex for lower-level
  implementation, refactoring, or frequent code changes.
- Stronger systems separate implementation from verification. Paul Iusztin's
  "Squid" pattern states the core rule clearly: no agent writes code and also
  decides whether that same code is correct.
- Persistent task state is recurring prior art. Examples include task lists,
  quest boards, beads, plan docs, `CLAUDE.md`, `AGENTS.md`, and work logs.
- Review gates are not only final code review. Sources describe adversarial
  reviewers, domain specialists, PR reviewers, testers, on-call CI loopers,
  and double-review defaults.
- Coordinator layers are appearing as several shapes: desktop control desks,
  IDEs, voice orchestrators, OTP-supervised harnesses, task boards, and parent
  agent sessions.
- There is an unresolved role-vs-domain split tension. Role splits such as
  planner/coder/reviewer are common and easy to reason about. Domain splits
  may compound repository knowledge better, but need stronger routing and
  ownership rules.
- Official Codex material supports the same broad direction: the Codex app is
  positioned around multiple agents, parallel work, worktree isolation,
  long-running tasks, automations that wake up over time, reviewable diffs,
  and iterative review/repair/validate loops.
- Current Codex `/goal` usage in the wild mirrors this repo's pattern:
  long-running goal loops are being treated as operational contracts with
  objectives, boundaries, verification steps, evidence requirements, and stop
  conditions.

Requirement implications from this prior art:

- The future coordinator must make the work unit durable before execution:
  goals, tasks, acceptance criteria, proof expectations, routing, and stop
  conditions must be explicit.
- The workflow must allow long-running implementer sessions, but it must also
  support fresh-context reviewers/testers/arbiters around that implementer.
- The coordinator must preserve agent topology. Agents need to know their
  assigned role or domain, worktree, communication channel, task source, and
  completion gate.
- The system must record whether an external lead is verified, medium
  confidence, or lead-only. Grok/X discoveries should not silently become
  doctrine.
- The design must account for both role-based and domain-based delegation
  before hard-coding one model as the only path.
- The workflow should treat verification capacity as a first-class bottleneck.
  If generation speed increases but proof remains manual, the human becomes
  the choke point.
- The coordinator must have a meta-improvement loop that can update future
  instructions, task templates, skills, or verification harnesses when a run
  exposes a repeatable mistake.
- The workflow must avoid using heavy orchestration for tiny tasks unless the
  user explicitly asks for that rigor. Several sources imply that coordination
  layers are valuable because projects are large, parallel, or long-running.

## Requirements, Planning, Testing, And Anti-Overbuilding Research

The latest research pass focused on how current practitioners and skill
authors are making coding agents gather requirements, plan phases, review
architecture before code, prove implementation through tests, avoid
overbuilding, and coordinate multiple roles.

New source note:

- `docs/coordinated_agent_workflow_sources/orchestration_requirements_planning_testing_research_2026-05-23.md`

Recent X/Grok patterns:

- `@LearnWithBrij` described Claude Code as a five-layer stack:
  `CLAUDE.md`, skills, hooks, subagents, and plugins. This reinforces that
  always-on context, on-demand procedure, deterministic guardrails, and
  isolated role work should be separate surfaces.
- `@Atenov_D` described plan mode, `/init`, a short `CLAUDE.md` router,
  Superpowers-style skills, compaction, loop commands, and hooks. This
  reinforces the need for a plan-before-code role contract and a small root
  instruction file.
- `@gbadamosixxl` described a handoff where Claude maps product architecture
  before Cursor implements. Thin source, but aligned with the architecture
  role the user is asking for.
- `@goyalshaliniuk` described Claude Code as an agent OS with permissions,
  task graph, memory, event bus, hooks, subagents, teammate mailboxes, task
  board, and worktree isolation. This is useful as conceptual vocabulary, not
  proof of an implemented system.
- `@hanabusa104` pointed to `/codex:setup --enable-review-gate` and
  `/codex:review` as task-boundary review mechanisms. Related plugin repos
  confirm that stop-time and background review gates are current practice, but
  also show token-cost, timeout, and loop-risk issues.

Specific external skill/repo patterns worth mining later:

- GitHub Awesome Copilot specification skills use self-contained specs with
  stable requirement IDs, constraints, data contracts, acceptance criteria,
  test strategy, examples, edge cases, and validation criteria.
- Obra Superpowers separates plan writing, subagent-driven implementation,
  spec compliance review, code quality review, TDD, and verification before
  completion.
- Addy Osmani's skills split spec-driven work into specify, plan, tasks, and
  implement phases, with explicit Always / Ask First / Never boundaries.
- Matt Pocock's TDD skill emphasizes public-interface behavior and vertical
  tracer bullets rather than writing all tests first and all code later.
- Softaworks requirements clarity scores vague requirements, iterates
  questions until the spec is concrete enough, and outputs a PRD. Its QA test
  planner is a concrete role template for test plans, cases, regression
  suites, Figma validation, and bug reports.
- jwynia's requirements analysis treats requirements as hypotheses and
  diagnoses no problem statement, solution-first thinking, vague needs, hidden
  constraints, and scope creep before system design.
- wshobson/agents keeps `AGENTS.md` as a table of contents while pushing
  procedures into skills and deeper reference into docs.
- Everything Claude Code is useful as a broad cross-harness reference list,
  especially for selective install, no-duplicate-surface warnings,
  language/framework-specific testing rules, and mobile-related rule packs.
- metaswarm is the closest public SDLC-shaped prior art found in this pass:
  research, plan, design review, work-unit decomposition, orchestrated
  execution, final review, PR shepherding, and closure/learning. Its plan gate
  uses feasibility, completeness, and scope/alignment reviewers. Its work-unit
  loop is implement, validate, adversarial review, commit.
- `openai/codex-plugin-cc` and `sendbird/cc-plugin-codex` show review and
  rescue commands crossing Claude Code and Codex in both directions, including
  background status/result handles and optional stop-time review gates.
- The external artifact index records exact files to revisit later, including
  Obra plan/spec/code-quality prompts, metaswarm plan/design/review gates,
  Awesome Copilot specification and mobile-testing agents, Softaworks
  requirements/QA skills, Addy Osmani spec/plan skills, ECC mobile test/review
  surfaces, and Codex/Claude review-gate plugin prompts.

Official docs reinforce the source-surface split:

- Claude Code docs say skills are on-demand `SKILL.md` instructions with
  supporting scripts, templates, examples, and references. Claude Code docs
  also say `CLAUDE.md` can import `AGENTS.md`, and that procedures that bloat
  `CLAUDE.md` are better as skills.
- Claude Code subagent docs describe delegation to specialized agents with
  independent work and returned results.
- Claude Code hook docs show deterministic lifecycle events around prompts,
  tool use, tasks, subagents, worktrees, compaction, and stop behavior.
- Codex docs describe nested `AGENTS.md` guidance, custom subagents with
  model/effort/sandbox/skills settings, worktrees, automations, and use cases
  such as durable goals, skills, pull-request review, native development,
  visual checks, and QA via computer use.

Recent papers add a stronger anti-overbuilding requirement:

- `https://arxiv.org/abs/2605.07769` reports that coding agents often change
  code even when no code change is required. The future coordinator needs a
  no-change/no-code success path.
- `https://arxiv.org/abs/2605.18583` studies overeager out-of-scope actions
  across agent products including Claude Code and Codex CLI. The future
  coordinator must treat unrequested features, unrelated refactors, and
  "while I was here" edits as review failures unless the plan was updated and
  the scope change was accepted.

Requirement implications:

- Requirements gathering must come before architecture and phase planning when
  the request is vague, solution-first, or missing constraints.
- Each non-trivial run needs a written contract: problem statement,
  assumptions, constraints, in-scope work, out-of-scope work, acceptance
  criteria, verification, likely files, dependencies, and proof notes.
- Each requirement should be traceable from requirement ID to task, test,
  review gate, proof artifact, and final status.
- Plans need explicit "no code change required" and "ask before changing
  scope" outcomes.
- Plan review should cover feasibility, completeness, and scope/alignment
  before implementation starts.
- Implementation review should distinguish spec compliance from general code
  quality.
- Same-agent self-verification cannot be the normal completion standard.
- Heavy gates need bounded iterations, timeout behavior, background job
  status/result handles, and nested-session loop prevention.
- Root `AGENTS.md` and `CLAUDE.md` should stay small and route to deeper
  skills/docs rather than absorbing every workflow rule.

## Visual-Quality And UI Verification Research

The user called out a recurring weak spot: agents can produce UI that is ugly,
awkward to use, overlapping, clipped, or visually unconvincing, then claim the
work is done because pixels changed or a screenshot exists. The research pass
therefore inspected psmobile's current visual proof method, recent
practitioner posts about browser/screenshot-based UI agent workflows, and
native-mobile workflows for iOS Simulator and Android Emulator.

Local psmobile findings:

- psmobile explicitly separates app-side diagnostic captures from final
  user-visible proof. App-side captures can hide chrome or isolate layers and
  are useful for source/mask sanity checks, but Mobile MCP or another
  host/device screenshot path is required for what the user actually saw.
- Its scene-tuning proof matrix is the strongest observed local pattern:
  before/after/off Mobile MCP screenshots, same-target binding, per-phase
  provenance, app-surface crops, target/protected/readability ROI metrics,
  contact sheets, receipt JSON, and an explicit visual inspection verdict.
- The psmobile proof contract rejects screenshot existence, command success,
  app-side capture, replay coverage, and metric-only pixel deltas as sufficient
  proof. Pixel changes that harm readability are treated as failures.
- The method is still domain-specific. It proves Lighting/Colors behavior well,
  but it is not yet a general reusable UI-quality reviewer for overlap,
  clipping, spacing, hierarchy, touch targets, focus states, or unpleasant
  aesthetics.

Recent X/Grok findings:

- `@JinjingLiang` described giving Codex/Claude Code screenshot ability through
  `agent-browser` or `playwright-cli` to improve UI/UX output.
- `@bettercallsalva` described wiring Claude Code or Codex to Playwright so the
  agent opens the page, clicks through, and reads the real DOM before claiming
  done.
- `@aakashgupta` described a Puppeteer skill where Claude renders HTML,
  screenshots it, measures overflow/page dimensions, and iterates before human
  review.
- `@49agents` pointed to a Claude Code plus Playwright plus Figma MCP loop that
  closes the gap from design context to working UI to verification.
- `@pankona` described natural-language E2E creation through Claude Code plus
  Playwright or agent browsers, while noting it is slow and token-heavy.
- `@leaf_sanren` described Figma-Context-MCP as moving coding agents beyond
  code context into design layout, component, and spacing context.
- Native-mobile Grok leads were checked directly on X. `@TimJayas` described
  Claude Code reading iOS Simulator screenshots and accessibility trees,
  interacting through mobile gestures, checking debug logs, and returning a
  structured pass/fail report. `@Bitomule` described `mav`, a CLI for coding
  agents to drive an iOS Simulator or device, run repeatable flows, and create
  human-reviewable evidence. `@Baconbrix` described using Claude Desktop or
  Codex with `npx serve-sim` while building mobile apps. `@kalvinmizzi`
  described Claude Code researching XCUITest, writing UI tests, and running
  them in the iOS Simulator. `@BeauJohnson89` pointed to an Android Claude
  Code skill pack with a UI quality gate. `@lukasiuu` described a Flutter
  DevTools/network MCP for runtime visibility. `@y_ogi` usefully separated
  "it launched in Simulator" from "the UI polish is good."

Official tooling docs reinforce the same split:

- Playwright MCP uses accessibility snapshots for interaction and screenshots
  for visual layout, canvas/chart content, and bug documentation.
- Figma MCP gives agents structured design context such as components,
  variables, layout data, and design details.
- Storybook/Chromatic and Percy show mature models for visual snapshots,
  responsive widths, cloud/browser rendering, layout testing, and baseline
  review.
- BrowserOS exposes browser automation tools to Codex and Claude Code and is
  explicitly positioned for agentic coding tasks such as testing web apps and
  reading console errors.
- Native mobile docs add a second proof model. Mobile MCP and iOS Simulator
  MCP expose simulator/device screenshots, accessibility snapshots or UI
  hierarchies, gestures, app launch/terminate, and coordinate fallback.
  Maestro has an MCP server, accessibility-layer mobile flows, screenshots,
  and experimental screenshot-plus-LLM assertions. Appium exposes application
  source, element rects, accessible labels/roles, full screenshots, element
  screenshots, and image comparison plugins. Detox records device screenshots,
  element screenshots, videos, logs, and view-hierarchy artifacts. Flutter
  `integration_test` proves in-app flows, while Patrol covers native gaps such
  as permissions, WebView/OAuth, notifications, app exit/resume, device
  settings, and native UI tree inspection.

Local skills worth mining later:

- `frontend-design`, `critique`, `polish`, `arrange`, `typeset`, `adapt`,
  `harden`, `normalize`, `optimize`, and `overdrive` cover taste, anti-generic
  UI checks, spacing, typography, responsiveness, edge cases, performance, and
  effect verification.
- `mobile-mcp-app-walkthrough`, `flutter-dev-return`, and `audit-loop-sim`
  cover real app/device proof, surface capture/restore, and map-first
  simulator automation.
- `figma-best-practices` covers source-backed visual parity and Figma file
  fidelity.
- `contact-sheet-builder`, `theme-preview`, `theme_tuner`, `theme_builder`,
  and `chroma-key-transparency` cover contact sheets, visual review boards,
  generated-asset QA, and metrics-backed image cleanup.

Requirement implications:

- Future UI work needs a visual-review role or role contract that is separate
  from the implementer.
- A visual claim must name the captured surface, source tool, route/state,
  viewport/device, interaction sequence, and inspection verdict.
- A native-mobile visual claim must also name the platform, simulator/device
  ID, app bundle/package, build artifact, OS version, orientation, screen size,
  and whether the evidence came from OS-visible screenshots, accessibility/UI
  hierarchy, framework-level app state, or app-side diagnostic capture.
- Rendered screenshots, semantic/accessibility/DOM or app snapshot data, and
  design-system/Figma context should be combined when available.
- "The pixels changed," "the screenshot exists," and "the app-side capture
  changed" are not acceptable completion evidence by themselves.
- Visual proof depth must scale with risk, because full browser or Mobile MCP
  loops can be slow and token-heavy.

## User's Current Requirement Seed

The current request describes the target shape:

- Move many ArcSkill workflows from "everything in the Codex session" toward a
  more formalized multi-role workflow.
- Add a top-level coordinator that dispatches agents.
- Capture actual usage patterns from recent Codex history before designing.
- Treat the present phase as requirements gathering, not solution design.
- Preserve the aggressive cleanup posture: remove confusing bad behaviors and
  bad defaults rather than leaving them on disk.
- Use Git history as the archive when deleting known-bad paths.
- Make incorrect future use harder by removing side doors, stale defaults, and
  confusing secondary paths.
- Make plan readiness depend on model consensus plus a strict fresh-consult
  arbiter.
- Make phase completion depend on strict fresh-context review before commit
  and before advancing.
- Escalate unexpected judgment calls to model consensus and ground the result
  in the repo's science/reference docs before proceeding.

## Observed Workflow Patterns

### 1. Long `/goal` prompts are being used as orchestration contracts

The user commonly encodes the whole workflow in one `/goal`: plan path,
quality bar, child-model use, phase gates, audit expectations, commit policy,
and escalation rules.

Evidence:

- 2026-05-23T06:23:13-05:00, command `r0001`: revise
  `docs/PACKS/animation_engine_references_2026-05-23/PLAN.md`, use
  `$model-consensus opus 4.7 max and gpt 5.5 xhigh`, require a
  `$fresh-consult gpt 5.5 xhigh` before the plan is considered ready.
- 2026-05-22T22:15:34-05:00, command `r0005`: implement
  `docs/PACKS/animation_engine_references_2026-05-23/PLAN.md`, keep a work
  log, get fresh consult signoff at phase boundaries, and avoid bifurcated
  code paths.
- 2026-05-22T22:17:27-05:00, command `r0004`: implement and test
  `docs/PACK/scene_tuning/perspective_lighting_effects_fix_and_sim_test_plan.md`
  in the iPhone 17 simulator, use model consensus for slow-moving pieces, and
  avoid accepting hacked outcomes.
- 2026-05-22T19:15:56-05:00, command `r0015`: after closing items in
  `docs/REGRET_MAP_STREET_NAMESPACE_ARCHITECTURE_PLAN_2026-05-22.md`, get a
  fresh consult review, then run thermonuclear review, then route unresolved
  review items through model consensus.

Requirement:

The future coordinator must treat a user goal prompt as a workflow contract,
not as a plain task description. It must preserve named artifacts, role
assignments, gates, escalation triggers, cleanup posture, and commit policy.

### 2. The user wants model consensus for judgment, not for trivial checks

The user repeatedly asks for `$model-consensus` when the problem requires
architectural judgment, plan revision, proof-policy decisions, or unexpected
snags.

Evidence:

- 2026-05-22T05:54:54-05:00, command `r0045`: use `$model-consensus` with
  Claude Opus 4.7 max and GPT-5.5 xhigh to review the full regret-map
  collision story and produce an on-disk prevention architecture.
- 2026-05-22T16:48:21-05:00, command `r0019`: use `$model-consensus` to build
  a new scrobbler plan after revising the desired behavior.
- 2026-05-22T11:27:59-05:00, command `r0035`: if an unforeseen snag appears
  that would tempt a workaround, go to model consensus.
- 2026-05-22T09:43:00-05:00, prompt search `r0043`: the user explicitly says
  model consensus is not needed for simple bug checks that can be inspected
  directly; it is for things that require judgment.

Requirement:

The coordinator must know the difference between ordinary inspection and
judgment escalation. It must not waste model-consensus cycles on simple facts,
but it must call model consensus when architecture, proof policy, plan scope,
or non-obvious tradeoffs are at stake.

### 3. Fresh consult is used as a strict independent arbiter

The user uses `$fresh-consult` or "GPT-55X-HI" as an independent gate for plan
readiness and phase completion.

Evidence:

- 2026-05-22T13:37:14-05:00, command `r0030`: every phase in
  `docs/REGRET_MAP_STREET_NAMESPACE_ARCHITECTURE_PLAN_2026-05-22.md` needs a
  strict `$fresh-consult gpt 5.5 xhigh` signoff for completeness, side doors,
  elegance, architectural purity, and test faithfulness before commit.
- 2026-05-22T12:25:07-05:00, command `r0031`: each phase boundary in
  `docs/PACKS/glass_action_pane_globalization_2026-05/README.md` needs
  `$fresh-consult gpt 5.5 xhigh` to verify full and elegant implementation.
- 2026-05-23T04:44:11-05:00, docs search `r0091`: a fresh consult prompt was
  generated for Phase 6 signoff with no prior chat context.
- 2026-05-23T04:43:23-05:00, docs search `r0095`: post-cleanup preflight
  passed, then fresh `gpt-5.5` / `xhigh` signoff was run.

Requirement:

Fresh consult must be an external-to-the-current-context completion gate. The
coordinator must pass it the plan, implementation evidence, tests, diffs, and
known risks, then treat rejection as blocking until resolved or explicitly
overruled by the user.

### 4. Thermonuclear review is a final pressure test, not ordinary review

The user often places thermonuclear review after fresh-consult signoff and
before final commit or phase advancement.

Evidence:

- 2026-05-22T22:21:12-05:00, command `r0003`: after implementing
  `docs/REGRET_COLLISION_DIAGNOSTIC_SURFACE_AUDIT_2026-05-23.md`, get fresh
  consult review, then thermonuclear code review.
- 2026-05-22T19:15:56-05:00, command `r0015`: get fresh consult, then do
  another thermonuclear code review; route unresolved findings through model
  consensus.
- 2026-05-22T16:03:16-05:00, command `r0020`: after consensus says complete,
  get thermonuclear code review; real reopened work should go to model
  consensus and planning docs.
- 2026-05-22T12:31:38-05:00, prompt `r0052`: direct invocation of
  `$thermo-nuclear-code-quality-review`.

Requirement:

Thermonuclear review must be a harsh completion and maintainability gate. It
must not be treated as ordinary lint. Findings must be triaged into real work,
non-goal churn, or doc-only noise, and real work must feed back into the plan
before advancing.

### 5. Parallel read-only agents are used to find missed paths

The user frequently asks for parallel agents with fresh context to audit the
codebase against the plan.

Evidence:

- 2026-05-22T17:02:42-05:00, command `r0018`: after finishing each phase,
  use parallel agents with clean context to audit the full codebase for missed
  paths, side doors, inelegance, bifurcated patterns, and cleanup gaps.
- 2026-05-22T12:34:30-05:00, prompt `r0049`: use parallel agents to review
  code versus the scrobbler plan and identify anything missed, inelegant, or
  bifurcated.
- 2026-05-23T06:00:25 to 06:00:36, sessions `r0011` to `r0014`: multiple
  read-only audit agents were launched in parallel for the animation engine
  plan.
- 2026-05-22T20:01 to 20:04, sessions `r0043` to `r0046`: parallel audit
  agents were scoped to separate regret-map surfaces: policy lifecycle,
  RTS/live solve, storage/persistence/metrics, and runtime policy/query.

Requirement:

The coordinator must be able to split audits into independent read-only scopes,
dispatch them in parallel, and merge findings without letting children edit
files or drift outside their assigned surface.

### 6. The user wants deletion of bad paths, not passive archival

The current request is explicit: use Git as the archive and delete known-bad
defaults, confusing old behavior, and bad code paths instead of leaving them on
disk.

Evidence:

- Current request: "use Git as our archive" and "I just want deletion of the
  bad shit."
- 2026-05-22T06:32:10-05:00, prompt `r0054`: delete old style references from
  global input so the system stops being confused and stops using them.
- Many `/goal` commands use the same failure language: no side doors, no
  secondary paths, no conflicting sources of truth, no cruft.

Requirement:

The future workflow must have an explicit cleanup mandate. When a path is
known to be wrong, confusing, stale, or unsafe by default, the expected outcome
is deletion unless the user explicitly asks to preserve it. The coordinator
must not treat "archive on disk" as the safe default.

### 7. "No side doors" is a repeated acceptance criterion

The phrase changes, but the target is consistent: eliminate secondary paths,
escape hatches, duplicate sources of truth, legacy access routes, and
bifurcated patterns.

Evidence:

- 2026-05-22T15:17:29-05:00, command `r0027`: audit all code paths and leave
  no cruft, secondary paths, side doors, or confusing sources of truth.
- 2026-05-22T15:01:48-05:00, command `r0028`: same audit shape for scene
  tuning and actual visual effect proof.
- 2026-05-22T13:37:14-05:00, command `r0030`: fresh consult must audit side
  doors, remaining code paths, competing sources of truth, architectural
  purity, and test faithfulness.
- 2026-05-22T06:22:13-05:00, prompt `r0056`: audit whether residual code would
  create bifurcated code paths or legacy side doors.

Requirement:

Acceptance must include a side-door audit. A phase cannot pass only because
the new path works. It must also prove that stale paths are deleted, disabled,
or made impossible to use incorrectly.

### 8. Plan docs must be updated, not merely discussed

The user repeatedly corrects agents that explain plan changes without writing
them into the plan.

Evidence:

- 2026-05-22T08:04:55-05:00, search `r0050`: "did this go into the plan doc
  or are you just telling me for some reason? ... update the doc."
- 2026-05-22T08:05:02-05:00, prompt `r0048`: "did this all make it into the
  planning doc?"
- 2026-05-22T08:07:42-05:00, prompt `r0047`: take all this back to model
  consensus and fresh consult; it is not done until exhaustively specified.
- 2026-05-23T05:57:26-05:00, corrections search `r0053`: "go read the plan"
  and check whether the implementation matched the animations listed there.

Requirement:

The coordinator must persist decisions into the plan/work log as a required
step. A chat answer is not a plan update. Completion claims must point to the
updated plan section, work log, commit, test, or arbiter artifact.

### 9. Work logs are used as durable execution state

Several goals require a work log beside the plan, and later audits inspect
those work logs for drift or false completion.

Evidence:

- 2026-05-22T22:15:34-05:00, command `r0005`: keep a work log next to the
  phase currently being worked on.
- 2026-05-22T11:27:59-05:00, command `r0035`: keep a work log alongside the
  plan document.
- 2026-05-23T06:01:17-05:00, docs search `r0032`: an audit found that the
  work log marked Phase 1 "complete enough" while admitting no binary golden
  and non-durable simulator PNG evidence.
- 2026-05-23T04:42:55-05:00, docs search `r0099`: the work log was updated
  after cleanup decisions and then verification was rerun so it did not lean
  on stale pre-cleanup results.

Requirement:

The coordinator must keep durable phase state outside chat. The work log must
record work performed, verification commands, arbiter results, cleanup
decisions, known failures, skipped checks, and any reason a gate passed despite
residual risk.

### 10. Verification must prove the intended behavior, not just activity

The user repeatedly rejects tests that only prove "something changed" or "a
command ran" when the real requirement is a specific visual or behavioral
effect.

Evidence:

- 2026-05-22T14:12:27-05:00, prompt `r0020`: ask whether verification checks
  the effect looks right, not just that it does something.
- 2026-05-22T15:01:48-05:00, command `r0028`: "It is not sufficient that a
  test just runs it must have the visual effect we want."
- 2026-05-23T05:56:48-05:00, docs search `r0045`: challenge whether the
  animation-engine proof was just a blinking-button version rather than the
  animations promised in the plan.
- 2026-05-23T06:56:17-05:00, corrections search `r0010`: the user says the
  black floor issue is not only an effect-layer issue; the entire floor is
  black, so the test must catch the deeper bug.
- 2026-05-23T07:02:45-05:00, visual/proof search `r0006`: model consensus
  required a no-shadow base-floor falsifier before shadow proof can count.

Requirement:

Verification must be semantic. It must prove the intended result and reject
false positives where a metric passes but the user-visible outcome is wrong.
Visual work needs visual evidence; simulator/mobile proof needs captures or
other artifacts that can falsify the specific failure mode.

### 11. Faster paths are welcome only when they preserve proof quality

The user wants to avoid slow, overly conservative loops, but not by weakening
the proof.

Evidence:

- 2026-05-22T22:17:27-05:00, command `r0004`: avoid getting stuck running one
  tiny slow thing at a time; use model consensus to find acceleration paths.
- 2026-05-22T09:36:26-05:00, prompt `r0045` in earlier search output: the user
  questioned slow screenshot methodology and wanted Mobile MCP considered for
  faster visual inspection.
- 2026-05-22T12:14:27-05:00, prompt `r0069` in prompt recall: ask whether a
  careful inspection step was part of normal process or whether generation,
  horizon, and cropping could run faster.
- Current request: the doc bug hand 12 issue should improve without hacked
  force-iteration behavior because the system uses better code paths.

Requirement:

The coordinator must distinguish proof-preserving acceleration from hacked
shortcuts. It must search for faster canonical paths when work is bogging down,
but it must not pass weak evidence to satisfy a checklist.

### 12. Unexpected snags must update the plan before implementation continues

The current request makes this explicit: when an unexpected issue would tempt
an expedient workaround, invoke model consensus, ground the answer in the
repo's research/science markdown, and update the plan before proceeding.

Evidence:

- Current request: invoke model consensus on unexpected issues, have the
  models do research in `doc/science`, update the plan, then continue.
- 2026-05-22T11:27:59-05:00, command `r0035`: if an unforeseen snag appears
  and a workaround is tempting, go to model consensus and have them help make
  decisions.
- 2026-05-23T07:05:19-05:00, corrections search `r0001`: a consensus result
  updated the plan to add Stage 0 base-floor readability when the black-floor
  issue showed the old proof was incomplete.

Requirement:

Unexpected judgment-heavy discoveries must trigger a plan-update loop, not an
in-session workaround. The future workflow must record the discovery, gather
repo evidence, ask the appropriate arbiters, update the plan, and only then
resume implementation.

Open item:

- The current `arch_skill` repo does not contain `doc/science` or
  `docs/science` in this pass. A target repo may still have that directory.
  The coordinator must resolve the user-named science/reference path per repo
  before using it as a grounding source.

### 13. Commit boundaries are phase gates

The user often asks for commits only after audit gates pass.

Evidence:

- 2026-05-22T15:17:29-05:00, command `r0027`: commit after each phase passes
  the audit gate.
- 2026-05-22T15:01:48-05:00, command `r0028`: commit after each phase passes
  the audit gate.
- 2026-05-22T13:37:14-05:00, command `r0030`: fresh consult signoff is needed
  before committing and moving to the next phase.
- 2026-05-23T04:49:48-05:00, docs search `r0061`: stage only the exact Phase 6
  files after `git diff --check` passed.

Requirement:

The coordinator must treat commits as gated phase records. It should not commit
before required reviews, verification, work-log updates, and cleanup decisions
are complete. It must stage only intended files and avoid sweeping unrelated
dirty work into the commit.

### 14. The user uses status queries to regain orientation

Recent history contains many prompts asking where the work is, which plan doc
is active, what remains, and what progress has been made.

Evidence:

- 2026-05-22T05:10:12-05:00, prompt `r0073`: ask where the work stands on
  `docs/REGRET_MAP_IDENTITY_COLLISION_SYSTEMATIC_PLAN_2026-05-22.md`.
- 2026-05-22T05:14:57-05:00, prompt `r0072`: ask what planning doc is being
  used.
- 2026-05-22T16:57:52-05:00, session `r0100`: find the doc used most recently
  on the branch.
- 2026-05-23T06:51:01-05:00, session `r0005`: ask `$agent-history` for the
  verbatim last two goal prompts in the repo.
- 2026-05-22T11:34:33-05:00, prompt `r0033`: "too much spam, just show me a
  table by phase."

Requirement:

The coordinator must make orientation cheap. A status view must be able to
answer: active plan, current phase, gates passed, gates blocking, last arbiter
result, last commit, next action, and remaining scope. The answer must be
concise enough to scan.

### 15. Child roles need strict boundaries

Recent spawned sessions show explicit role boundaries: model-consensus children
are collaborators, audit agents are read-only, fresh consult is an arbiter,
and parent agents own synthesis.

Evidence:

- 2026-05-23T07:05:34-05:00, session `r0004`: model-consensus child prompt
  says the model is not a prompt runner and must reason from evidence.
- 2026-05-23T06:00:25 to 06:00:36, sessions `r0011` to `r0014`: parallel audit
  agents are told "read-only audit only" and "do not edit files."
- 2026-05-22T20:12:22-05:00, session `r0041`: read-only audit scoped to a
  specific source-light slice.
- 2026-05-23T04:44:11-05:00, docs search `r0091`: fresh consult prompt says it
  has no prior chat context, must read artifacts directly, and must answer the
  user's ask for the parent agent, not fix files.

Requirement:

The coordinator must enforce role contracts. A child agent must receive its
scope, edit permissions, evidence obligations, output contract, and boundary
conditions in the prompt. Read-only agents must not edit. Arbiters must not
silently implement. Model-consensus children must produce evidence-backed
judgment, not generic advice.

### 16. The user wants aggressive cleanup but not uncontrolled scope creep

The user wants real cleanup and deletion, while also warning against runaway
review expansion.

Evidence:

- Current request: delete known-bad paths and defaults so future use inherits
  good defaults.
- 2026-05-22T22:21:12-05:00, command `r0003`: tackle thermonuclear issues
  agreed with, but "don't let it scope creep."
- 2026-05-22T16:03:16-05:00, command `r0020`: thermonuclear items that are
  "not doc bullshit" and are real work should go through model consensus and
  planning docs.
- 2026-05-22T16:01:28-05:00, command `r0021`: not every code review item needs
  to be addressed; if review is trying to change the work, the models should
  reject it.

Requirement:

The coordinator must keep cleanup strict and scope disciplined. It must remove
bad old paths that belong to the approved goal, but it must not accept every
review suggestion as in-scope work. Scope-changing review findings need a
decision gate.

### 17. The user expects model names and efforts to survive exactly enough to route

The prompts name models in inconsistent but meaningful shorthand:
`opus 4.7 max`, `Claude Opus 4.7 max`, `gpt 5.5 xhigh`,
`GPT-55X-HI`, `GBT55XI`, and similar variants.

Evidence:

- Repeated command rows name `opus 4.7 max` and `gpt 5.5 xhigh`.
- 2026-05-22T22:21:12-05:00, command `r0003`: uses "GBT55 XI" and later
  "GBT55XI".
- 2026-05-23T06:23:13-05:00, command `r0001`: uses `gpt 5.5 xhigh`.

Requirement:

The coordinator must preserve raw model phrases for auditability and resolve
them into runnable model/effort settings before dispatch. The run record must
show raw-to-resolved mapping.

### 18. The user values artifact-backed synthesis over chat memory

The observed workflows write model-consensus summaries, fresh-consult prompts,
work logs, and plan updates to disk.

Evidence:

- 2026-05-23T07:06:31-05:00, search `r0115`: a model-consensus summary was
  written to `/tmp/psmobile/model-consensus/no-shadow-black-floor-20260523T115830Z/summary.md`.
- 2026-05-23T04:44:11-05:00, docs search `r0091`: a fresh-consult prompt was
  written into a `/tmp/fresh-consult/...` run directory.
- 2026-05-22T20:49:39-05:00, command `r0012`: save the animation-engine plan
  back into its doc pack as an easy-to-consume plan.
- 2026-05-22T11:49:40-05:00, prompt `r0029`: save parallel-agent findings as
  open items in the plan README.

Requirement:

Every dispatched role must leave a durable handle. The coordinator must be able
to cite prompts, outputs, summaries, work logs, plan sections, verification
artifacts, and commits without depending on memory from the parent session.

## Role Requirements Captured So Far

### Top-level coordinator

The coordinator must:

- Preserve the user's raw goal and exact named artifacts.
- Resolve model names and efforts.
- Turn one long goal prompt into a run contract with phases, gates, roles,
  proof obligations, cleanup posture, and commit policy.
- Dispatch child agents with narrow roles and explicit permissions.
- Keep the plan and work log current.
- Merge child findings into one decision record.
- Decide when a finding is in scope, out of scope, or a scope-change request.
- Stop implementation when a gate fails.
- Escalate unexpected judgment-heavy problems to model consensus.
- Require fresh-consult or thermonuclear review where the user asked for it.
- Keep status concise and phase-oriented.

### Model-consensus participants

Model-consensus participants must:

- Read real repo evidence before agreeing.
- Preserve independent first-pass judgment before critique.
- Converge on a small answer or name the unresolved decision.
- Reject kitchen-sink accumulation.
- Judge plan completeness, proof policy, architecture, and unexpected snags.
- Update the parent with evidence and rejected alternatives.

### Fresh-consult arbiter

The fresh-consult arbiter must:

- Start from fresh context.
- Read plan, diff, work log, verification evidence, and known risks.
- Decide whether plan readiness or phase completion is actually satisfied.
- Be strict about elegance, completeness, missed paths, and test faithfulness.
- Return blocking issues clearly enough for the coordinator to reopen work.

### Thermonuclear reviewer

The thermonuclear reviewer must:

- Perform a harsh maintainability and code-quality pass.
- Find real side doors, bifurcated patterns, dead paths, hacks, and confusing
  defaults.
- Distinguish real implementation issues from churn or doc-only noise.
- Provide evidence paths that can be triaged.

### Parallel audit agents

Parallel audit agents must:

- Be read-only unless explicitly assigned implementation.
- Own one narrow surface or lens.
- Read the plan and relevant code deeply.
- Report missed paths, stale code, proof gaps, and cleanup risks.
- Avoid duplicating the same broad audit across every child.

### Requirements analyst

The requirements analyst role must:

- Run before architecture and phase planning when the request is vague,
  solution-first, missing constraints, cross-cutting, or likely to take
  multiple days.
- Separate the user's problem from the user's proposed solution.
- Surface assumptions before they harden into architecture.
- Produce a written problem statement, constraints, in-scope list,
  out-of-scope list, acceptance criteria, open questions, and no-code/no-change
  possibility where appropriate.
- Detect hidden constraints, missing reproduction steps, unclear success
  criteria, and likely scope creep.
- Turn repeated clarification into a durable PRD/spec artifact, not a chat
  memory.

### Architecture / design planner

The architecture or design planner must:

- Read existing code, docs, domain vocabulary, and decisions before proposing
  new abstractions.
- Produce architecture/design artifacts that can be reviewed before expensive
  implementation starts.
- Name alternatives considered and rejected.
- Identify integration points, data contracts, ownership boundaries, and
  risks.
- Preserve the user's cleanup posture when the right design means deleting
  stale or confusing paths.
- Avoid turning "architecture" into broad refactoring unless the cleanup is
  tied to the approved goal.

### Phase planner / work-unit decomposer

The phase planner must:

- Break accepted requirements into ordered phases and work units.
- Make dependencies explicit and verify file paths against the real repo.
- Prefer vertical, testable slices where the project shape allows them.
- Mark which work can run in parallel and which work must be serial.
- Give every work unit acceptance criteria, verification steps, likely files,
  dependencies, and proof notes.
- Flag placeholders, vague tasks, fabricated paths, and missing verification
  as plan failures.

### QA / test planner

The QA or test planner must:

- Create the test strategy before implementation for risky or user-visible
  work.
- Map tests to requirement IDs and acceptance criteria.
- Define entry criteria, exit criteria, environments, fixtures, test data,
  regression scope, and high-priority manual checks.
- Specify reproduction or falsification steps for bug fixes where feasible.
- Own user-facing flows, native-mobile device matrices, and visual proof
  requirements when the work needs them.
- Produce bug reports or failing-test descriptions with reproducible steps,
  expected results, actual results, environment, and evidence.

### Spec compliance reviewer

The spec compliance reviewer must:

- Review the diff against the task, plan, and Definition of Done.
- Ignore the implementer's self-report unless it is independently verified.
- Check for missing requirements, extra unrequested work, misunderstandings,
  and scope drift.
- Return pass/fail with concrete evidence.
- Run before broad code-quality review when the question is whether the right
  thing was built.

### Visual QA / UI critic

The visual QA role must:

- Be independent from the implementer whose UI it reviews.
- Inspect actual rendered output, not only source code.
- Prefer user-visible host/browser/device screenshots for user-visible claims.
- Treat app-side or layer-isolated captures as diagnostic unless the claim is
  explicitly about that diagnostic layer.
- Combine screenshots with semantic structure when available: accessibility
  trees, DOM geometry, Playwright snapshots, Flutter QA snapshots, Figma nodes,
  or design-system source.
- For native mobile, bind every claim to the specific iOS Simulator, Android
  Emulator, physical device, app bundle/package, build artifact, OS version,
  orientation, and screen size used for proof.
- Use Mobile MCP, iOS Simulator MCP, Maestro, Appium, Detox, XCUITest,
  Espresso, UI Automator, Flutter `integration_test`, Patrol, or repo-local
  simulator tooling when those are the right proof surface for the app.
- Capture native accessibility/UI hierarchy or framework snapshots when
  available, and mark coordinate-only interaction as weaker evidence.
- Check overlap, clipping, text readability, hierarchy, spacing, tap targets,
  keyboard focus, loading/empty/error states, responsive breakpoints, and
  reduced-motion behavior when relevant.
- For native mobile, also check safe areas/notches, status/navigation bars,
  soft keyboard overlays, permission dialogs, app background/resume, deep
  links, system back behavior, orientation, Dynamic Type/font scaling, dark
  mode, locale/RTL, tablets/foldables, and slow/offline network states when
  relevant.
- Reject pixel-delta-only proof and screenshot-existence-only proof.
- Leave reviewable artifacts: screenshot paths, viewport/device, route/state,
  interaction steps, issue list, verdict, and any contact sheet or manifest.

## Cross-Cutting Acceptance Requirements

A future coordinated workflow is not done until:

- Non-trivial work has a written contract: problem statement, assumptions,
  constraints, in-scope work, out-of-scope work, acceptance criteria,
  verification, likely files, dependencies, and proof notes.
- Requirements that survive planning have stable IDs or another traceable
  handle from requirement to task, test, review gate, proof artifact, and final
  status.
- The workflow has considered whether success means "no code change required"
  or "do not edit until scope is clarified."
- The plan is written to disk and names all required phases, gates, artifacts,
  and cleanup/deletion obligations.
- Plan readiness has been pressured for feasibility, completeness, and
  scope/alignment when the run is substantial enough to need that rigor.
- Model consensus has converged where the user required it.
- Fresh consult has approved plan readiness where the user required it.
- Each phase has concrete proof that matches the intended behavior.
- The implementer is not the only judge of completion; coordinator-run
  validation or an independent verifier has inspected the actual evidence.
- Spec compliance and code quality have been reviewed as separate questions
  when both are required.
- UI phases have user-visible visual evidence and semantic/accessibility or
  geometry evidence when the surface supports it.
- Native mobile UI phases have simulator/device proof from the target platform,
  not only a passing build, app launch, widget test, app-side capture, or one
  happy-path screenshot.
- Each phase has had the required fresh-context audit or arbiter pass.
- Real thermonuclear findings have been handled or explicitly rejected with
  evidence and scope rationale.
- Bad old paths and defaults in scope have been deleted, not left as traps.
- Work logs record commands, artifacts, failures, skipped checks, and review
  outcomes.
- The plan has been updated when reality changed.
- Commits happen only after gates pass and only include intended files.
- Status can be reconstructed from disk without reading the whole chat.
- New always-on instruction, command, or skill surfaces do not leave stale
  duplicate runtime paths that a future agent can accidentally invoke.

## Failure Modes To Prevent

The future system must actively prevent:

- Treating the user's goal prompt as loose inspiration instead of a contract.
- Treating a solution-first prompt as settled architecture before the problem,
  constraints, and acceptance criteria are clear.
- Forcing a code edit when the correct outcome is no code change, better
  reproduction, or a clarified requirement.
- Starting implementation before plan readiness gates pass.
- Presenting a plan with placeholders, TODOs, fabricated paths, vague tasks,
  missing dependencies, or missing verification.
- Passing a phase because code changed, even though the intended behavior was
  not proven.
- Leaving deprecated code paths, bad defaults, stale docs, or old prompts on
  disk because "archive" feels safer.
- Creating a new secondary path while claiming to simplify.
- Marking work complete in a work log before evidence supports it.
- Answering "yes" in chat without updating the plan.
- Running model consensus for simple inspections.
- Skipping model consensus on architectural judgment or workaround temptation.
- Letting review findings scope creep without a decision gate.
- Letting audit agents edit files when their job is read-only.
- Letting implementers self-certify their own tests, file scope, visual
  quality, or spec compliance.
- Collapsing spec compliance review and code quality review into one vague
  "looks good" pass.
- Losing orientation about the active plan, phase, arbiter status, or latest
  commit.
- Using slow, conservative proof loops when a faster equivalent proof exists.
- Using faster proof loops that no longer catch the user-visible failure.
- Accepting app-side captures as proof for normal user-visible UI.
- Using a web-only verifier to sign off native iOS, Android, Flutter, React
  Native, Compose, or SwiftUI UI.
- Accepting a native mobile screenshot without proving the simulator/device,
  app ID, build, state, platform, orientation, and OS context.
- Treating "the app launched in Simulator" as proof of UI quality.
- Accepting pixel changes, visual diffs, or screenshot existence when the UI is
  still unreadable, overlapping, clipped, or hard to use.
- Letting the implementer be the only judge of whether its own UI looks good.
- Ignoring Figma/design-system source for design-backed UI work.
- Missing native-only failures: keyboard occlusion, safe-area clipping,
  permission sheets, iOS resume/deep-link behavior, Android back/navigation
  behavior, Dynamic Type/font scaling, locale/RTL, tablets/foldables, or
  offline/slow-network state.
- Bloated root `AGENTS.md` or `CLAUDE.md` files that bury routing rules in a
  giant operating manual.
- Duplicate live command, skill, plugin, or instruction surfaces that preserve
  old bad defaults beside the new intended workflow.
- Background review jobs that finish without a durable status/result handle.
- Stop-time review gates that run on no-edit/status-only turns or recurse
  inside child sessions.

## Open Requirements To Resolve Later

These are not solution proposals. They are requirements still needing sharper
definition before implementation planning:

- Canonical location for requirement/spec/PRD artifacts, and whether those are
  separate from plan and work-log artifacts.
- Canonical location for coordinator run state and artifacts.
- Exact schema for a run contract, phase record, gate record, and child-agent
  result.
- Exact scheme for requirement IDs, acceptance IDs, task IDs, test IDs, review
  gate IDs, and proof artifact handles.
- How model shorthand maps to runnable model IDs and efforts on this machine.
- How to classify a finding as in-scope cleanup versus scope creep.
- How to express "delete bad defaults" in a way that remains safe around
  user-owned dirty work.
- How to make "no code change required" a first-class successful completion
  state in run records, reviews, and final status.
- How to detect when a plan changed enough that implementation must pause for
  re-approval.
- Which gates are mandatory, which are risk-scaled, and which are explicit
  user-request gates.
- Whether feasibility/completeness/scope plan review should be implemented as
  separate roles, one role with separate passes, or a model-consensus/fresh
  consult prompt pattern.
- How to verify visual outcomes without recreating slow or brittle screenshot
  loops.
- How to define the minimum visual-proof bundle for web UI, Flutter mobile UI,
  native iOS, native Android, React Native, Compose/SwiftUI, and generated
  image/theme assets.
- Which native mobile proof tools are preferred by surface: Mobile MCP,
  iOS Simulator MCP, Maestro, Appium, Detox, XCUITest, Espresso, UI Automator,
  Flutter `integration_test`, Patrol, repo-local `sim`, or framework-specific
  MCPs.
- What the required device/platform matrix is for native mobile signoff:
  iOS/Android parity, small phone, large phone, tablet/foldable, portrait,
  landscape, keyboard open/closed, Dynamic Type/font scaling, locale/RTL, dark
  mode, and app lifecycle states.
- Whether UI taste critique, deterministic geometry/accessibility review, and
  design-source parity should be one specialist role or separate roles.
- How to locate and use `doc/science` or `docs/science` in each target repo.
- How to produce the concise "table by phase" status view from run artifacts.
- How to make the workflow usable from a single `/goal` while still preserving
  explicit role boundaries.
- Where reusable prompts should live so root doctrine stays short: skills,
  source docs, templates, commands, or generated harness artifacts.
- How to validate that new coordinator surfaces did not leave stale duplicate
  install/runtime paths behind.
- How background arbiter jobs report status, timeout, cancel, resume, and final
  result without becoming another hidden state system.

## Evidence Handles

The most reusable history handles from this pass:

- Current planning request:
  `/Users/aelaguiz/.codex/history.jsonl:18601`, session
  `019e54c0-1406-7963-96d2-6167f24cc9ea`.
- Animation-engine plan readiness goal:
  `/Users/aelaguiz/.codex/history.jsonl:18593`, session
  `019e547c-96dd-7930-b22a-5dcf6ae18d72`.
- Scene-tuning implementation goal:
  `/Users/aelaguiz/.codex/history.jsonl:18568`, session
  `019e52d4-fc5c-7981-b273-63c793e42cb7`.
- Animation-engine implementation goal:
  `/Users/aelaguiz/.codex/history.jsonl:18567`, session
  `019e52d2-2728-7462-84f5-d9437edd3514`.
- Regret diagnostic implementation goal:
  `/Users/aelaguiz/.codex/history.jsonl:18569`, session
  `019e52d8-23e0-7961-9d89-f7d106770774`.
- Regret-map architecture implementation goal:
  `/Users/aelaguiz/.codex/history.jsonl:18512`, session
  `019e51f2-fdee-7502-89c4-024fc188b583`.
- Scrobbler behavior revision goal:
  `/Users/aelaguiz/.codex/history.jsonl:18486`, session
  `019e5174-90ad-7641-9f7f-21635cee5bb4`.
- User correction about black floor:
  `/Users/aelaguiz/.codex/history.jsonl:18600`, session
  `019e52d4-fc5c-7981-b273-63c793e42cb7`.
- User correction about animation proof:
  `/Users/aelaguiz/.codex/history.jsonl:18586`, session
  `019e52d2-2728-7462-84f5-d9437edd3514`.
- User correction about model-consensus scope:
  `/Users/aelaguiz/.codex/history.jsonl:18344`, session
  `019e4d3a-0a46-7a10-b992-d1998433d984`.
