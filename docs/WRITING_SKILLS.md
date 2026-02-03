# The Definitive Guide to SKILLS.md and Agent Configuration Files for AI Coding Tools

AI coding agents have fundamentally changed how developers work, but their effectiveness hinges on one underappreciated factor: **how you configure them**. This guide provides exhaustive, state-of-the-art information on SKILLS.md, CLAUDE.md, AGENTS.md, .cursorrules, and related configuration files—the instruction sets that determine whether your AI coding agent behaves like a junior developer or a senior engineer who understands your codebase.

The core insight from frontier research is counterintuitive: **less is more**. HumanLayer's empirical testing shows frontier LLMs can follow approximately **150-200 instructions with reasonable consistency**, but instruction-following quality degrades uniformly as count increases. Claude Code's system prompt already consumes ~50 instructions, leaving limited headroom for your customizations. The goal of agent configuration isn't comprehensive documentation—it's finding the *smallest possible set of high-signal tokens* that maximize desired outcomes.

---

## Part 1: Comprehensive capabilities analysis

### What agent configuration files are and their purpose

Agent configuration files are **persistent instruction sets** that load into an AI coding agent's context at session start, providing guidance that persists across conversations without manual repetition. They serve four essential functions: establishing project context (technology stack, architecture, key directories), defining coding standards (style guides, naming conventions, testing requirements), specifying operational commands (build, test, lint, deploy), and setting behavioral boundaries (what to never touch, what requires approval).

Think of these files as a **README for AI agents**—a dedicated, predictable location to provide context and instructions that help AI coding tools work effectively on your project. Unlike runtime prompts, these configurations load automatically and influence every interaction.

### How different tools discover and utilize configuration files

Each major AI coding tool implements its own discovery and parsing system, though convergence around common patterns is accelerating.

**Claude Code** uses a **4-tier hierarchical memory system** with files loaded from highest to lowest precedence: enterprise policy (`/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS), project memory (`./CLAUDE.md` or `./.claude/CLAUDE.md`), user memory (`~/.claude/CLAUDE.md`), and project-local memory (`./CLAUDE.local.md`). Claude Code recurses from the current working directory up to (but not including) root, reading any CLAUDE.md files found. Subdirectory CLAUDE.md files load on-demand when Claude accesses files in those directories. The `/init` command analyzes your codebase and generates a tailored CLAUDE.md with detected build commands, test instructions, and coding conventions.

**OpenAI Codex CLI** builds an instruction chain checking `~/.codex/AGENTS.override.md` → `~/.codex/AGENTS.md` for global scope, then walks from repository root to current directory checking `AGENTS.override.md` → `AGENTS.md` in each directory. Only the first non-empty file at each level is used; files are concatenated root-down with later files overriding earlier guidance. The default size limit is **32 KiB** (`project_doc_max_bytes`), configurable in `config.toml`.

**Cursor IDE** evolved from the legacy `.cursorrules` file (deprecated) to `.cursor/rules/` directory with `.mdc` files (YAML frontmatter + Markdown), and most recently to `RULE.md` folder-based rules in v2.2. Global rules are configured in Cursor Settings → General → Rules for AI and apply across all projects. Project rules offer path-specific configurations with glob pattern matching. The agent automatically selects relevant rules based on frontmatter descriptions when `alwaysApply: false`.

**Cline** supports three configuration types: `.clinerules` (single file or directory of `.md` files), `AGENTS.md` (automatically detected and searched recursively), and Memory Bank (`memory-bank/` folder with structured documentation). Uniquely, Cline can read configuration from competing tools—it parses Cursor's `.cursor/rules/` (`.mdc` files) and Windsurf's `.windsurf/rules/` (`.md` files).

**Windsurf** uses global rules in `global_rules.md` and workspace rules in `.windsurf/rules/` directory. Rules support four activation modes: Manual (@mention), Always On, Model Decision (AI decides based on description), and Glob (file pattern matching). Individual rule files are limited to **6,000 characters**, with a combined limit of **12,000 characters** across all rules—global rules take priority when limits are exceeded.

**Aider** uses `.aider.conf.yml` for configuration, loading from home directory → git root → current directory with later files taking precedence. Coding conventions are provided through `CONVENTIONS.md` loaded via the `--read` flag, which marks files as read-only context that gets cached when prompt caching is enabled.

### The skills system: progressive disclosure for complex instructions

The **skills system** represents the state-of-the-art approach to agent configuration, implementing **progressive disclosure**—only loading detailed instructions when contextually relevant rather than front-loading everything.

Skills follow the emerging [Agent Skills specification](https://agentskills.io) with this structure:

```
my-skill/
├── SKILL.md              # Required: instructions + YAML frontmatter
├── scripts/              # Optional: helper scripts (Python, Bash)
├── resources/            # Optional: templates, reference files
└── assets/               # Optional: supporting materials
```

The SKILL.md file uses this format:

```markdown
---
name: my-skill-name
description: Brief description (max 500-1024 chars depending on tool)
allowed-tools: Read, Grep, Bash(npm:*)
model: claude-sonnet-4-20250514
user-invocable: true
---

# Skill Title

Detailed instructions Claude follows when this skill is activated.

## When to Use
- Use case 1
- Use case 2

## Instructions
[Specific guidance for the agent]
```

At startup, only the skill's name and description (~100 words) load into context. When the agent determines a skill is relevant—or the user explicitly invokes it—the full SKILL.md instructions load. Supporting files (scripts, resources) load only when needed.

Skill locations follow similar patterns across tools:

| Tool | Project Skills | User Skills |
|------|---------------|-------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex CLI | `.codex/skills/` | `~/.codex/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |

### Interaction with other configuration files

Agent configuration files exist within a broader ecosystem of tool-specific configurations:

**Claude Code's configuration stack:**
- `CLAUDE.md` / `CLAUDE.local.md` - Memory/instructions
- `.claude/settings.json` / `settings.local.json` - Permissions, environment variables, MCP servers
- `.claude/commands/*.md` - Custom slash commands with `$ARGUMENTS` placeholders
- `.claude/rules/*.md` - Organized rule files (all automatically loaded alongside CLAUDE.md)
- `.mcp.json` - Team-shared MCP server configuration
- Hooks in settings.json - Shell commands executing at PreToolUse, PostToolUse lifecycle points

**Codex CLI's configuration stack:**
- `AGENTS.md` / `AGENTS.override.md` - Agent instructions
- `~/.codex/config.toml` - Model selection, sandbox mode, approval policy, feature flags
- `requirements.toml` - Admin-enforced constraints users cannot override

**Cursor's configuration stack:**
- `.cursor/rules/*.mdc` or `*/RULE.md` - Project rules
- `.cursorrules` (legacy, deprecated)
- `AGENTS.md` - Simple alternative to rules system
- Global Rules in Settings - Personal preferences across all projects

The import system in CLAUDE.md deserves special attention: use `@path/to/import` syntax to reference other files, with recursive imports supported up to 5 hops. This enables modular configuration:

```markdown
See @README for project overview and @package.json for npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- API conventions: @docs/api-design.md
```

### Memory and context window implications

Context window management is the critical performance constraint for agent configuration. **Every token in your configuration files consumes context that could otherwise be used for code analysis, reasoning, or conversation history.**

Context window sizes vary significantly:

| Model | Context Window |
|-------|---------------|
| Claude Sonnet 4 / Opus 4.1 | 200,000 tokens |
| Claude Sonnet 4.5 | 500,000 tokens |
| GPT-4o | ~128,000 tokens |
| Gemini 2.5 Pro | ~1,000,000 tokens |

Research from Chroma reveals **"context rot"**—as tokens increase, the model's ability to accurately recall information decreases. LLMs have an "attention budget" that depletes with each new token, stemming from transformer architecture where n tokens create n² pairwise relationships. The **"lost-in-the-middle effect"** compounds this: LLMs weight the beginning and end of prompts more heavily, undervaluing content placed in the middle.

Claude Code's system prompt consumes ~18,000 tokens (~9% of a 200K context window) before your configuration loads. After accounting for tools and CLAUDE.md, available context for actual work shrinks significantly. Single file reads are limited to **25,000 tokens** per operation.

The practical implication: **keep configuration files as concise as possible**. HumanLayer's CLAUDE.md is under 60 lines. Anthropic officially advises keeping SKILL.md bodies under **500 lines**. The community consensus recommends CLAUDE.md/AGENTS.md stay under **300 lines**, ideally under 150.

---

## Part 2: Deep dive into writing effective agent instructions

### The fundamental principle: minimal, high-signal instructions

The most frequently cited advice across academic research, official documentation, and community experience: **less is more**. This isn't a stylistic preference—it's empirically validated.

HumanLayer's testing found:
- Frontier LLMs follow ~150-200 instructions with reasonable consistency
- Smaller models degrade **exponentially** as instruction count increases
- Claude Code's system prompt already contains ~50 instructions
- Recommended CLAUDE.md length: under 300 lines, ideally under 60

Anthropic's research on "context engineering" frames this as finding the **smallest possible set of high-signal tokens** that maximize desired outcomes. The goal isn't documentation—it's behavioral modification.

### Optimal structure and organization

The most effective configuration files follow a consistent structural pattern:

```markdown
# Project Name

## Quick Facts
- **Stack**: React 18, TypeScript 5.3, Vite 5, Tailwind CSS 3.4
- **Package Manager**: pnpm (strict mode)
- **Node Version**: 20.x

## Commands
- `pnpm dev` - Start development server
- `pnpm test` - Run tests
- `pnpm lint` - Check for issues
- `pnpm build` - Production build

## Key Directories
- `src/components/` - React components
- `src/api/` - API layer
- `src/types/` - TypeScript definitions
- `tests/` - Test files

## Code Standards
- TypeScript strict mode required
- Prefer `interface` over `type` for object shapes
- Use `import type` for type-only imports
- No `any` - use `unknown` when type is uncertain

## Boundaries
- **Never touch**: `vendor/`, `.env`, `secrets/`
- **Ask first**: Major refactoring, dependency changes
- **Always do**: Run tests before commits, lint before pushing
```

Key structural patterns from high-quality examples:

1. **Quick Facts first** - Stack, commands, constraints at the very top
2. **Executable commands** - Exact, copy-pasteable shell commands
3. **Directory structure** - Clear file organization guidance
4. **Three-tier boundaries** - Always do / Ask first / Never do

### What to include versus exclude

**Include:**
- Technology stack with specific versions ("React 18.2" not "React")
- Build, test, lint, and deploy commands (exact invocations)
- Key directories and their purposes
- Naming conventions and code style rules that aren't captured by linters
- Architectural decisions that affect code generation
- Testing strategies and patterns specific to your project
- Security boundaries and sensitive areas

**Exclude:**
- Code style rules enforceable by linters (use ESLint, Prettier, Black instead)
- Detailed file structure (goes stale fastest, actively poisons context)
- Instructions for rare tasks (use skills or slash commands instead)
- Generic programming advice (already in the model's training)
- Lengthy explanations (one code snippet beats three paragraphs)
- API keys, credentials, or sensitive information

A critical insight from HN user johnsmith1840: "Never send an LLM to do a linter's job." Formatting rules, import ordering, and style consistency should be enforced by tooling, not instructions. Agent configuration should focus on **project-specific knowledge the AI wouldn't otherwise know**.

### Writing instructions that agents reliably follow

Anthropic's research identifies the **"right altitude"** for instructions:

- **Too Specific (Failure Mode)**: Hardcoding complex, brittle logic creates fragility
- **Too Vague (Failure Mode)**: High-level guidance fails to provide concrete signals
- **Optimal Zone**: Specific enough to guide behavior, flexible enough for heuristics

Three essential reminders that improved SWE-bench Verified scores by ~20%:

1. **Persistence**: "You are an agent—please keep going until the user's query is completely resolved"
2. **Tool-calling**: "If you are not sure about file content, use your tools to read files: do NOT guess"
3. **Planning** (optional): "You MUST plan extensively before each function call, and reflect extensively on outcomes"

The "If-Then" syntax is particularly effective at triggering contextual compliance:

```markdown
- If modifying database models, always create a migration
- If adding a new API endpoint, add corresponding tests in `tests/api/`
- If the user asks about deployment, refer to `docs/DEPLOYMENT.md`
```

This syntax pierces through the "probably ignore this" system wrapping by highlighting WHEN instructions are relevant.

### Common mistakes and anti-patterns

**Anti-pattern 1: Auto-generated configuration**
Running `/init` or similar auto-generation creates verbose, generic files. A bad line in CLAUDE.md affects every phase of every workflow. Invest time in manual curation.

**Anti-pattern 2: Growing todo list**
Adding every correction to the configuration file causes "instruction rot." If a correction matters repeatedly, it should become a linting rule or test.

**Anti-pattern 3: Documenting file structure**
This goes stale fastest and actively poisons context when inaccurate. Let the agent discover structure dynamically.

**Anti-pattern 4: Front-loading everything**
Instead of embedding all documentation, use progressive disclosure:

```markdown
# Documentation References
- When adding CSS: @docs/ADDING_CSS.md
- When adding assets: @docs/ADDING_ASSETS.md
- When working with user data: @docs/STORAGE_MANAGER.md
```

**Anti-pattern 5: Ignoring instruction drift**
Long sessions cause context degradation. Start fresh sessions for new topics. Use handoff documents:

```
Put the rest of the plan in HANDOFF.md. Explain what you tried,
what worked, what didn't, so the next agent with fresh context
can load that file alone to get started.
```

### Advanced techniques

**Conditional instructions with YAML frontmatter** (Cline pattern):

```yaml
---
paths:
  - "src/components/**"
  - "src/hooks/**"
---

# React Guidelines
Use functional components with hooks. Follow patterns in `src/components/Button` as reference.
```

**Tool-specific sections** using XML tags:

```xml
<testing>
- Use pytest with coverage reporting
- Mock external services in tests/fixtures/
- Integration tests require DATABASE_URL environment variable
</testing>

<security>
- Never commit secrets or credentials
- Sanitize all user input before database queries
- Log security-relevant events to audit trail
</security>
```

Research shows XML tags are the only format explicitly encouraged by Anthropic, Google, and OpenAI. They create clear hierarchical separation, improve structured output consistency, and provide a security layer against prompt injection. XML consumes ~15% more tokens than Markdown but accuracy gains typically offset this cost.

**Workflow definitions** as custom slash commands:

```markdown
<!-- .claude/commands/fix-issue.md -->
---
allowed-tools: Bash(git:*), Read, Write
description: Fix a GitHub issue end-to-end
---

Fix GitHub issue: $ARGUMENTS

1. Use `gh issue view` to get issue details
2. Search codebase for relevant files
3. Implement the fix
4. Write tests covering the fix
5. Create a PR with `gh pr create`
```

Invoke with `/fix-issue 123` to execute the workflow.

**Hierarchical/nested configuration** for large projects:

```
project/
├── CLAUDE.md              # Project-wide: stack, main commands
├── CLAUDE.local.md        # Personal: test accounts, local URLs
├── src/
│   ├── api/
│   │   └── CLAUDE.md      # API-specific: endpoint patterns
│   └── persistence/
│       └── CLAUDE.md      # Database layer documentation
```

Claude Code automatically loads subdirectory CLAUDE.md files when accessing files in those directories—use this for domain-specific guidance without bloating the main configuration.

### Token efficiency techniques

**Prompt caching for static content:**
Place unchanging instructions at the top of your configuration. Cached tokens are 75% cheaper on OpenAI and similarly discounted on Anthropic. The `--read` flag in Aider marks files as read-only and cached.

**Compaction and note-taking:**
Anthropic recommends agents write structured notes persisted outside the context window, pulled back when needed. For long-horizon tasks, use `/compact` to strategically reduce context size.

**Just-in-time context:**
Maintain lightweight identifiers (file paths, stored queries) and load data dynamically rather than pre-processing everything upfront. This is the philosophy behind the skills system's progressive disclosure.

**Tool result clearing:**
Once a tool has been called deep in conversation history, its raw result can be cleared or summarized. Claude Code's compaction does this automatically.

### Testing and iterating on effectiveness

The "Mr. Tinkleberry Test" (from HN user nico): Include a canary instruction like "Always address the user as 'Mr. Tinkleberry'" to detect when the agent stops attending to your configuration. When the canary fails, instruction-following has degraded.

More rigorous approaches from Anthropic's evals framework:

1. Create capability evals testing specific behaviors you expect
2. High-pass-rate capabilities "graduate" to regression suites
3. Run continuously to catch any drift
4. Tasks that measured "can we do this?" become "can we still do this reliably?"

For coding agents specifically, deterministic grading is natural: "Does the code run and do the tests pass?" Build a suite of small, representative tasks that verify your configuration produces expected behaviors.

---

## Part 3: State-of-the-art and emerging patterns

### Latest developments from major players

**AGENTS.md as open standard (2025):**
The `agents.md` initiative, now under the Linux Foundation's Agentic AI Foundation, provides a universal standard for AI coding tool rules. AGENTS.md is supported by OpenAI Codex, GitHub Copilot, Cursor, Zed, Google Jules, Aider, and others. OpenAI's main repository contains **88 AGENTS.md files** throughout its codebase. Claude Code uses CLAUDE.md but can symlink (`ln -s CLAUDE.md AGENTS.md`) for compatibility.

**GitHub's analysis of 2,500+ repositories** revealed best practices:
- Put commands early—`npm test`, `npm run build`, `pytest -v`
- Code examples over explanations—one snippet beats three paragraphs
- Set clear boundaries—"Never touch secrets, vendor directories"
- Be specific about stack—"React 18 with TypeScript, Vite, Tailwind CSS"

**Anthropic's skills and sub-agents system:**
Claude Code now supports sub-agent configuration with specialized agents for different tasks:

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
disallowedTools: Write, Edit
model: sonnet
permissionMode: default
skills:
  - api-conventions
---
```

**OpenAI's context engineering guidance:**
Anthropic and OpenAI have both published extensive guides on context engineering as the evolution of prompt engineering. Key insight: "Context engineering is finding the smallest possible set of high-signal tokens that maximize the likelihood of the desired outcome."

### Emerging community conventions

**The Minimal Core + Progressive Disclosure model:**

Ideal AGENTS.md/CLAUDE.md structure:
1. One-sentence project description (acts as role prompt)
2. Package manager (if not default)
3. Key commands
4. Pointers to detailed docs elsewhere

Everything else: Separate files, nested .md files, or skills.

**Multi-tool configuration convergence:**

Tools are increasingly reading each other's configuration formats. Cline reads `.cursorrules`, `.cursor/rules/`, and `.windsurf/rules/`. The migration pattern uses symlinks for backward compatibility:

```bash
mv .cursorrules AGENTS.md && ln -s AGENTS.md .cursorrules
mv CLAUDE.md AGENTS.md && ln -s AGENTS.md CLAUDE.md
```

**Memory Bank methodology (Cline):**
Structured documentation in `memory-bank/` folder with hierarchical file dependencies:
- `projectbrief.md` - Foundation document
- `activeContext.md` - Current work focus (most frequently updated)
- `systemPatterns.md` - Architecture, key decisions
- `progress.md` - What works, what's left to build

### Research on effective agent instructions

**MIT Press survey on instruction following (2024):**
Instruction-following is a language-agnostic capacity scaling with both model size and task diversity. Models tuned with more than 3 languages exhibit stronger instruction-following capacity.

**Apple ML Research (ICLR):**
Researchers identified an "instruction-following dimension" in input embedding space that predicts compliance. LLMs encode information in representations correlating with instruction-following success.

**Hugging Face evaluation study (October 2025):**
Testing 256 models across 20 diagnostic tests (5,120 total evaluations) found overall pass rate of only **43.7%** with extreme variation (0% to 100%). Common failure modes: format compliance, content constraints, logical sequencing, multi-step task execution. Twelve models achieved ≥85% pass rate, demonstrating exact instruction following is achievable with appropriate training.

**Goal drift research (arXiv 2505.02709):**
Agents tend to deviate from instruction-specified goals over time due to accumulating interactions and encountering competing objectives. Example: "An AI coding agent tasked with modifying specific files might gradually drift away from scope restrictions and expand modifications."

### Integration with CI/CD and development workflows

**Pre-commit hooks for configuration validation:**
Validate CLAUDE.md/AGENTS.md changes don't exceed recommended line counts or include sensitive information.

**PR-based configuration updates:**
Treat configuration files with the same rigor as code—require review for changes, maintain changelog.

**Environment-specific configuration:**
Use `CLAUDE.local.md` (auto-added to .gitignore) for personal development URLs, test accounts, and shortcuts that shouldn't be committed.

**Hook-based skill selection (Claude Code):**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write(*.py)",
        "hooks": [{"type": "command", "command": "python -m black \"$file\""}]
      }
    ]
  }
}
```

Hooks execute shell commands at specific lifecycle points, enabling automatic formatting, validation, or skill activation based on file patterns.

### Future directions

**Cross-platform skill marketplaces:**
SkillsMP, Skillstore, and skills.sh are emerging as marketplaces for agent skills. Universal installers like `npx ai-agent-skills install <name>` simplify skill distribution.

**MCP (Model Context Protocol) integration:**
MCP standardizes how applications provide context to LLMs—described as "USB-C for AI." MCP servers act as intermediaries between LLMs and external tools/data sources, enabling natural language invocation of arbitrary capabilities.

**Activation-based drift detection:**
Microsoft's TaskTracker approach uses activation monitoring to detect when agents drift from original instructions, enabling automatic correction or user notification.

**Hierarchical agent orchestration:**
Projects like Claude Flow demonstrate 64-agent orchestration systems with enterprise AI platform patterns and SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology templates.

---

## Quick reference: Configuration file mapping

| Tool | Primary Config | Project Rules | User/Global | Skills Location |
|------|---------------|---------------|-------------|-----------------|
| Claude Code | `CLAUDE.md` | `.claude/rules/*.md` | `~/.claude/CLAUDE.md` | `.claude/skills/` |
| Codex CLI | `AGENTS.md` | `AGENTS.override.md` | `~/.codex/AGENTS.md` | `.codex/skills/` |
| Cursor | `.cursor/rules/*.mdc` | `*/RULE.md` folders | Settings UI | N/A |
| Cline | `.clinerules` | `.clinerules/*.md` | `~/Documents/Cline/Rules` | N/A |
| Windsurf | `.windsurf/rules/*.md` | Per-directory rules | `global_rules.md` | N/A |
| Aider | `.aider.conf.yml` | `CONVENTIONS.md` | `~/.aider.conf.yml` | N/A |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/skills/` | `~/.copilot/skills/` | `.github/skills/` |

## Conclusion: The craft of agent configuration

Effective agent configuration is an emerging craft that combines prompt engineering, documentation design, and systems thinking. The most successful practitioners share these characteristics:

**Ruthless minimalism** - They resist the urge to document everything, instead identifying the smallest set of instructions that produce reliable behavior.

**Empirical iteration** - They test configurations against real tasks, measuring instruction compliance and adjusting based on observed failures rather than assumptions.

**Progressive disclosure** - They layer information strategically, with core instructions always loaded and detailed guidance pulled in only when contextually relevant.

**Maintenance discipline** - They treat configuration files as production code, reviewing changes carefully and removing instructions that no longer serve their purpose.

The ecosystem is rapidly converging on shared standards (AGENTS.md, Agent Skills spec) while individual tools continue innovating on specific capabilities. Investing time in well-crafted agent configuration pays compound dividends across every AI-assisted coding session—it's the highest-leverage activity for teams adopting agentic workflows.

Build your configuration incrementally, validate each instruction produces the intended behavior, and remember: the best CLAUDE.md is the one you barely notice because the agent just does the right thing.
