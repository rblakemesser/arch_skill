# X And Web Prior-Art Source Notes

Captured: 2026-05-23

Scope: recent public source material about long-running coding agents,
multi-agent dispatch, role/domain split agents, worktree isolation, task boards,
review/test arbiters, persistent plan docs, and Codex/Claude Code workflows.

Primary collection method: BrowserOS against signed-in X/Grok and direct X
status pages.

Secondary checks: OpenAI official docs, public GitHub repositories, and a small
Firecrawl search pass. The Firecrawl results were lower signal than Grok/X for
current practitioner examples, so they are not the main evidence source.

## Strong Source Notes

### Simon Last: large projects, plans, persistent tasks, role sessions

- Source: `https://x.com/simonlast/status/2057978156183957995`
- Date: 2026-05-22
- Status: verified through direct X pages for posts 1-6 and 8-10.
- Relevant pattern: use coding agents for larger units of work, keep a
  long-running implementer session, drive it with a persistent task list,
  write self-contained plan docs, require fresh read-only review before task
  completion, maintain specialized long-lived roles, and improve the meta
  process.

### Flower: worktree topology with Claude, Codex, smux, beads, double review

- Source: `https://x.com/flowerornament/status/2057927123906838915`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page.
- Relevant pattern: three permanent worktrees/branches per project; two agents
  per worktree; Claude handles high-level long-context work; Codex handles
  frequent code work; `smux` provides inter-agent messaging; `beads` provides
  shared task tracking; agents know their topology; work is double-reviewed by
  default.

### Uncle Bob Martin: architect, coder, reviewer handoff

- Source: `https://x.com/unclebobmartin/status/2045477573535142212`
- Date: 2026-04-18
- Status: verified by BrowserOS direct X page.
- Relevant pattern: three-agent network with architect, coder, and reviewer.
  The architect plans structure and writes acceptance tests. The coder
  interprets acceptance tests, writes unit tests, and makes them pass. The
  reviewer refactors using quality tools. Claude is used as architect; Codex is
  used for the lower-level code and review roles.

### Paul Iusztin: Squid AI engineering team in Claude Code

- Source: `https://x.com/pauliusztin_/status/2057076372720460010`
- Date: 2026-05-20
- Status: verified by BrowserOS direct X page.
- Relevant pattern: six specialized roles inside Claude Code: PM, SWE, tester,
  PR reviewer, on-call, and self-improve. The key rule is that no agent writes
  code and decides whether that same code is correct. The on-call role exists
  because CI kept getting skipped inside the SWE/tester loop. Completed runs
  feed workflow improvements back into `CLAUDE.md`, skills, and subagents.

### Danila Poyarkov: Vibe as stateful OTP-supervised agent harness

- Source: `https://x.com/dan_note/status/2057966143369777407`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page.
- Relevant pattern: Vibe is an Elixir-focused coding-agent harness meant for
  background tasks and long-running agent workflows. It has stateful sessions,
  supervised subagents with their own sessions, persistent SQLite storage,
  semantic events, plugins, skills, gateways, telemetry, remote access, and a
  TUI/web interface. The system is designed so the agent can inspect, patch,
  verify, and hot-reload parts of the harness while boundaries stay explicit.

### Thomas Rice: Quest Board with analyst, coder, reviewer, human gate

- Source: `https://x.com/thomasrice_au/status/2057691971339296969`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page.
- Relevant pattern: AI analysts propose "quests" or code updates. Proposals go
  to a Quest Board. A coding agent implements. An AI reviewer sends the work
  back or forwards it to the human for final checks.

### Superset: local control desk for many CLI coding agents

- X source: `https://x.com/yutaaaalll/status/2058082540058235044`
- Repo source: `https://github.com/superset-sh/superset`
- Date: X post on 2026-05-23; repo checked on 2026-05-23.
- Status: X post verified by BrowserOS; repo verified through GitHub page.
- Relevant pattern: Superset describes itself as a code editor for the AI
  agents era. It orchestrates CLI-based coding agents across isolated git
  worktrees, including Claude Code and OpenAI Codex CLI. It supports parallel
  execution, agent monitoring, built-in diff review, one-click editor handoff,
  and workspace setup/teardown commands.

### OpenAI Codex app and docs: official direction for parallel agents

- Codex app launch: `https://openai.com/index/introducing-the-codex-app/`
- Codex product page: `https://openai.com/codex/`
- Codex automations: `https://developers.openai.com/codex/app/automations`
- Codex worktrees: `https://developers.openai.com/codex/app/worktrees`
- Codex subagents: `https://developers.openai.com/codex/subagents`
- Codex AI-native engineering team guide:
  `https://developers.openai.com/codex/guides/build-ai-native-engineering-team`
- Iterative repair loop cookbook:
  `https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex`
- Status: official docs checked with web browsing on 2026-05-23.
- Relevant pattern: Codex is explicitly positioned as a command center for
  multiple agents, parallel work, worktree isolation, reviewable agent diffs,
  long-running tasks, automations that wake up over time, background review
  loops, and iterative review/repair/validate loops with structured feedback.

## Medium Source Notes

### Lightsprint: team layer for AI-native development

- Source: `https://x.com/lightsprintai/status/2057607939456971248`
- Date: 2026-05-21
- Status: verified by BrowserOS direct X page.
- Relevant pattern: visual plan mode, parallel cloud agents, and PR preview
  environments. This is a launch/product-positioning source, not a detailed
  personal workflow breakdown.

### BridgeMind: voice orchestrator controlling coding agents

- Source: `https://x.com/bridgemindai/status/2057804855146696841`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page.
- Relevant pattern: voice interface that spawns coding agents, assigns tasks,
  provides codebase context, and follows up on completion. This is useful as a
  dispatch-interface example, but less detailed about verification and failure
  handling.

### Yicheng Wang: Runner desktop app

- X source: `https://x.com/pipiracoon/status/2057658238255185922`
- Repo source: `https://github.com/yicheng47/runner`
- Date: 2026-05-21
- Status: verified by BrowserOS direct X page; repo page loaded by web search.
- Relevant pattern: local desktop app where Claude Code, Codex, and other
  agents run together as a crew. Each gets a PTY tab and role such as
  architect, implementer, or reviewer. The system bubbles `ask_human` when
  stuck. The X post is low-view and the project is pre-1.0, so treat it as a
  small but concrete implementation example.

### Cristian Pena: domain-split subagents

- Source: `https://x.com/CristianPenaOK/status/2057888005462106610`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page.
- Relevant pattern: argues for domain-based subagents instead of generic
  role-based agents. Claimed production flow: review triage, two or three
  domain specialists, adversarial reviewer, and automatic file-level LOC
  budgets. Treat as important design tension, but the account has low
  engagement on this post and the claim is not independently verified here.

### LiveMatrixCode: Codex `/goal` as operational contract

- Source: `https://x.com/LiveMatrixCode/status/2057079243788476925`
- Date: 2026-05-20
- Status: verified by BrowserOS direct X page.
- Relevant pattern: a 12-hour Codex `/goal` run is framed as an operational
  contract with objectives, boundaries, verification steps, evidence
  requirements, and stop conditions. Low engagement, but directly matches this
  repo's observed `/goal` usage pattern.

### Herki Parn: multi-day Codex goal loop

- Source: `https://x.com/herkiparn/status/2056810895330648145`
- Date: 2026-05-19
- Status: verified by BrowserOS direct X page.
- Relevant pattern: one focused Codex goal loop running for seven days and
  seven hours on Rust web-engine work and long-running tests. This is evidence
  that multi-day Codex goal loops are being attempted, but not a detailed
  architecture source.

### Rohit: Anthropic long-running-agent harness discussion

- Source: `https://x.com/rohit4verse/status/2044846994074828888`
- Date: 2026-04-16
- Status: verified by BrowserOS direct X page.
- Relevant pattern: references compaction strategies, disk-backed task list
  state across parallel agents, and `CLAUDE.md` hierarchy. Useful as an
  intermediary pointer, but the underlying Anthropic material should be
  checked directly before becoming design input.

## Lower-Confidence Or Lead-Only Notes

### AgentKit v2.0

- X source: `https://x.com/TheGoldenAnvil/status/2057599140788351168`
- Repo source: `https://github.com/NullLabTests/AgentKit`
- Date: 2026-05-21
- Status: X post and repo page loaded.
- Relevant pattern: claims memory, skills, guardrails, workflows, multi-agent
  orchestration, specialized roles, and TDD automation. Engagement on the X
  post is very low. Keep as a repo/tool lead, not as proof of mature practice.

### Firecrawl secondary pass

- Files:
  - `.firecrawl/multi-agent-coding-may-2026.json`
  - `.firecrawl/codex-multi-agent-roles-2026.json`
  - `.firecrawl/agent-qa-verification-2026.json`
- Status: ran successfully but returned mostly generic articles, social
  mirrors, and broader tool lists.
- Relevant finding: for current practitioner practice on X, Grok plus direct
  BrowserOS verification was more useful than generic web search.

## Cross-Source Pattern Summary

- Worktree isolation is a repeated default for running agents in parallel.
- Strong workflows separate implementation from verification. Several sources
  explicitly reject same-agent self-verification.
- Persistent plans, task boards, queues, or context files are central. Common
  names include `AGENTS.md`, `CLAUDE.md`, task boards, quest boards, and shared
  task trackers.
- The human role shifts toward planning, queuing, reviewing outcomes, and
  improving the process, not manually running every test or managing every PR.
- The coordinator layer appears in multiple forms: desktop app, IDE/control
  desk, voice orchestrator, OTP harness, task board, or parent Codex/Grok
  session.
- Role splits and domain splits are both present. Role splits are easier to
  understand; domain splits may preserve deeper codebase knowledge but need
  more routing discipline.
- The strongest review loops use independent readers/testers/arbiters and
  concrete evidence: diffs, tests, CI, screenshots, browser sessions, logs, or
  explicit acceptance criteria.
- Meta-improvement is not optional in the stronger examples. Completed runs
  should feed back into instructions, skills, and verification harnesses.
- Over-engineering is a real risk. Several sources imply that heavy
  coordination pays off for larger projects but can be too much for small
  changes.
