
# A cold reader's rubric for evaluating AI agent instructions

**No dedicated framework exists for evaluating AI agent instruction documents — despite 60,000+ projects now shipping AGENTS.md files and every major AI lab publishing guidance on writing them.** This gap matters because instruction quality directly determines agent behavior, yet most teams write these files without a quality standard. The research below synthesizes guidance from Anthropic, OpenAI, Google, IEEE requirements engineering, and established technical writing standards into a comprehensive, framework-agnostic evaluation rubric. A "cold reader" — someone with no domain expertise in the agent's specific task — can use it to assess whether an instruction document is structurally sound, internally consistent, and likely to produce reliable agent behavior.

The core insight across all sources: agent instructions fail not because they lack information, but because they contain the wrong kind of information — vague where they should be concrete, verbose where they should be minimal, and contradictory where they should be prioritized. Frontier models can follow roughly **150–200 discrete instructions** with reasonable consistency before quality degrades uniformly across all instructions. Every sentence in an instruction file must earn its place.

---

## What the major AI labs actually recommend

Anthropic and OpenAI have converged on strikingly similar principles despite different technical approaches. Both emphasize that modern models follow instructions more literally than their predecessors, making precision both more achievable and more necessary.

**Anthropic's "right altitude" principle** captures the central tension: instructions should be "specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics." Too brittle (hardcoded if-else logic) creates fragility. Too vague (high-level guidance without concrete signals) fails to constrain behavior. Anthropic's context engineering guide frames system prompts as a finite resource: "Good context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." Their CLAUDE.md guidance recommends **under 300 lines**, with HumanLayer's analysis of production deployments finding that effective root instruction files average under 60 lines.

**OpenAI's GPT-4.1 and GPT-5 prompting guides** independently identify three required categories for agent prompts that boosted SWE-bench scores by ~20%: a **persistence directive** (keep working until the task is fully resolved), a **tool-calling directive** (use tools to gather information rather than guessing), and a **planning directive** (reason extensively before and after each action). Their key design insight: "Observe the diversity of rules, the specificity, the use of additional sections for greater detail, and an example to demonstrate precise behavior that incorporates all prior rules."

Both labs agree on structural principles that should be visible in any well-written instruction document:

- **Tell the agent what to do, not what not to do.** Positive instructions ("respond with smoothly flowing prose") outperform negative ones ("do not use markdown") because they give the model a target to aim at rather than a space to avoid.
- **Use structured formatting** — XML tags, markdown headers, or numbered lists — to create parseable sections. Anthropic recommends XML; the AGENTS.md standard uses plain markdown. Both work. Unstructured prose walls do not.
- **Provide examples over exhaustive rules.** Anthropic calls examples "the pictures worth a thousand words." But OpenAI's empirical testing shows rules often outperform examples alone for behavioral compliance — the ideal is rules first, then 2–4 canonical examples that demonstrate those rules in action.
- **Define explicit priority hierarchies.** OpenAI's Instruction Hierarchy paper (Wallace et al., 2024) proposes System > Developer > User > Tool priority levels, and their GPT-5 guide includes a template `<instruction_priority>` block. Without explicit prioritization, models resolve conflicts via positional bias — essentially a coin flip.

The AGENTS.md standard, now stewarded by the Agentic AI Foundation under the Linux Foundation and supported by **60+ tools** including Codex, Cursor, Copilot, and Gemini CLI, recommends a lean structure: project overview, exact build/test commands, code style guidelines, and explicit behavioral boundaries. Analysis of 2,500+ repositories found that the most effective files put executable commands early, use code blocks instead of prose explanations, and stay under 150 lines.

---

## How technical writing standards apply to instructing machines

The 7 Cs of communication (Clear, Concise, Coherent, Concrete, Correct, Complete, Courteous) remain the backbone of technical writing quality — but their relative importance shifts dramatically when the audience is an LLM rather than a human.

**Concrete is king.** For human readers, some abstraction is tolerable because people resolve ambiguity through shared context. LLMs have no shared context beyond what's explicitly stated. The compliance testing firm Salus AI documented that changing a vague prompt ("Does the agent suggest the test is a necessity?") to a precise, literal formulation improved accuracy by **9 to 68 percentage points** depending on the task. Every major source confirms: concrete, testable instructions dramatically outperform abstract principles.

**Concise means something different for machines.** Research paper "Same Task, More Tokens" found that LLM reasoning degrades even at **3,000 tokens** — far below technical context limits. The ManyIFEval benchmark showed that if each instruction has a 95% individual compliance rate, ten instructions yield only 60% joint compliance, and twenty instructions drop to 36%. This exponential decay — the "curse of instructions" — means conciseness isn't a style preference; it's an engineering constraint. Yet conciseness must not sacrifice completeness: omitting a critical constraint to save tokens produces undefined behavior that the model fills with training defaults.

**Consistent terminology is non-negotiable.** The Microsoft Writing Style Guide's principle of "one word for one concept" is arguably the single most important style rule for AI instructions. The Federal Plain Language Guidelines state: "You will confuse your audience if you use different terms for the same concept." For humans, synonym variation adds readability. For LLMs, it introduces ambiguity about whether two terms refer to the same entity. A document that calls something a "user" in one section and a "customer" in another forces the model to guess whether these are identical.

Three style guide principles from Google and Microsoft deserve special emphasis for AI instruction documents. First, **put conditions before instructions** ("If the user asks about pricing, respond with..." not "Respond with pricing info if the user asks"). LLMs process text sequentially; establishing the condition first sets the context for the action. Second, **use imperative mood and active voice** ("Extract the name from the query" not "The name should be extracted"). This eliminates ambiguity about who performs the action. Third, **avoid modifier stacks** — long chains of modifying words that are difficult for any reader, human or machine, to parse reliably.

The W3C's method for writing testable conformance requirements provides a precise template: every instruction should contain **an actor** (who must follow it), **a precondition** (when it applies), **an expected behavior** (what should happen), and **measurable criteria** (how to verify compliance). Instructions that lack any of these four elements are structurally incomplete. The requirements engineering community has identified specific "weak terms" that signal untestable instructions: *appropriate, reasonable, as needed, properly, adequate, when necessary, sometimes, etc.* — each should be flagged during review and replaced with specific criteria.

---

## Ten documented failure modes and why they happen

Research across production failure analyses, academic papers, and practitioner reports reveals consistent patterns of instruction document failure. Each has been independently documented by multiple sources.

**Contradictory instructions** are the most damaging failure mode because LLMs have no built-in mechanism to detect or resolve contradictions. OpenAI's GPT-5 prompting guide documents a real healthcare agent where "Never schedule without patient consent" conflicted with "Auto-assign the earliest same-day slot without contacting the patient." The ETH Zurich paper on self-contradictory hallucinations explains why: LLMs "process text as a continuous sequence without dedicated mechanisms for tracking specific assertions." When forced to choose, they default to whichever instruction has stronger positional salience — typically the one appearing closest to the beginning or end of the prompt. A cold reader should extract all behavioral directives and check them pairwise for conflicts.

**Vague qualifiers without decision criteria** produce what Galileo AI classifies as "Specification and System Design Failures" — the top-level failure category because unclear goals cascade into every subsequent action. Their documented case: an agent instructed to "remove outdated entries" without defining "outdated" deleted valid records under its own interpretation. Paxrel's anti-pattern documentation shows that asking an agent to "double-check your work" without specific criteria produces meaningless confirmations — "I've verified the article" — with no actual verification performed. The fix is always the same: replace the qualifier with explicit criteria.

**Buried critical rules** exploit a well-replicated architectural vulnerability. The "Lost in the Middle" finding (Liu et al., 2024, published in TACL) demonstrated a **U-shaped attention curve** across every tested model: performance peaks for information at the very beginning and very end of context, with a **20+ percentage point accuracy drop** for information in the middle. Chroma's 2025 study confirmed this persists across 18 frontier models including GPT-4.1, Claude Opus 4, and Gemini 2.5. The architectural cause is Rotary Position Embedding (RoPE), which creates a decay effect for tokens distant from query position. Critical rules buried in paragraph 12 of a long instruction document receive systematically less attention than formatting preferences in paragraph 1.

**Aspirational rather than behavioral instructions** — "be helpful," "ensure quality," "use good judgment" — are pervasive and almost useless. Anthropic's documentation explicitly advises: "If you want 'above and beyond' behavior, explicitly request it rather than relying on the model to infer this from vague prompts." Paxrel documents the consequence: an agent told "You are a helpful newsletter editor that curates AI news" without constraints will "scrape competitor sites, post drafts to social media, write 20-article editions, and make up quotes when sources are thin — because nothing told it not to." Scope creep is a default LLM behavior, not an exception.

The remaining six failure modes — **temporal references in stateless documents**, **references to nonexistent artifacts**, **inconsistent terminology**, **missing error handling**, **conflicting priorities without hierarchy**, and **over-reliance on unguided judgment** — each follow the same pattern: instructions that would work for a human colleague with shared context, institutional memory, and common sense fail for an LLM that has none of these unless explicitly provided. Every assumption must be stated. Every reference must resolve. Every judgment call needs criteria.

---

## Evaluating instructions you don't understand the domain of

A cold reader cannot verify whether instructions are *factually correct* for the domain. But research from technical editing, requirements engineering, and usability testing demonstrates that most quality dimensions are fully assessable without domain expertise — and outsider perspective is often an advantage for detecting problems experts unconsciously compensate for.

**IEEE 830's eight quality characteristics** provide the most directly applicable framework. Of the eight, six are fully assessable by a cold reader: **unambiguous** (does each instruction have only one interpretation?), **consistent** (do any instructions contradict each other?), **ranked/prioritized** (is it clear which rules take precedence?), **verifiable** (can you determine whether the instruction was followed?), **modifiable** (can changes be made without breaking other parts?), and **traceable** (can each instruction be linked to a purpose?). Only "correct" and partially "complete" require domain knowledge.

**The cognitive walkthrough method** (Wharton et al., 1994, streamlined by Spencer in 2000) reduces evaluation to two questions per instruction: *Would the agent know what to do at this step?* and *If the agent does the right thing, would it know it did the right thing?* Walking through each instruction with these questions surfaces ambiguities, missing prerequisites, and undefined success criteria — all without needing to understand the domain. Where you'd need to stop and ask a clarifying question, the agent would too.

**Terminology consistency auditing** is a mechanical process any reader can perform: build a glossary of key terms as you read, flag instances where the same concept gets different names, and flag instances where the same term appears to mean different things in different contexts. This catches one of the most common and damaging failure modes with zero domain knowledge required.

**The rule consistency matrix** extends this to behavioral directives: extract every rule or constraint from the document, arrange them in a matrix, and check each pair for potential conflicts. Ask seven questions for each pair: Do they address the same subject? Do their conditions overlap? Do they specify different actions? Are those actions mutually exclusive? Is there a priority mechanism? Is it consistently applied? Are edge cases addressed? This systematic approach catches contradictions that linear reading misses.

Readability metrics like Flesch-Kincaid provide weak but useful signals — a system prompt scoring above grade level 18 is almost certainly overwritten. But these formulas measure surface features only and miss coherence, logical structure, and information completeness. Use them as one input, not a verdict.

---

## What makes instructing AI different from instructing humans

Eight differences between writing for humans and writing for LLMs are consistently documented across research and practitioner experience. Understanding these differences is essential for evaluating whether an instruction document accounts for its actual audience.

**Instructions compound exponentially, not linearly.** A human colleague given 20 rules follows each at roughly the same rate as 5 rules. The ManyIFEval benchmark demonstrates that LLMs degrade exponentially: at 95% per-instruction compliance, 10 instructions yield 60% joint compliance and 20 instructions yield 36%. This is the single most important architectural constraint on instruction document design and the strongest argument for ruthless conciseness.

**Position is architectural, not just psychological.** Human readers can skim and re-read. LLM attention patterns are governed by positional embeddings that systematically deprioritize middle content. The U-shaped curve is not a bug to be fixed — it's a property of transformer architecture. Instruction documents must place their most critical content at the very beginning and reinforce it at the very end.

**Formatting is functional, not cosmetic.** A benchmark study across multiple models found that proper prompt formatting improved performance by up to **500%**. XML tags, markdown headers, and numbered lists aren't aesthetic choices — they're engineering tools that help models parse instruction boundaries and distinguish between sections. A cold reader should check whether the document uses consistent structural formatting rather than relying on prose paragraphs.

**There is no implicit context.** Humans share cultural norms, organizational knowledge, and common sense. LLMs have exactly what's in the prompt and their training data. References to "what we discussed," "the usual approach," or "standard practice" are meaningless without explicit definition. A cold reader should flag any instruction that assumes shared context not provided in the document itself.

**Contradictions are resolved by position, not logic.** A human employee who encounters conflicting instructions will ask for clarification. An LLM silently picks one interpretation — typically based on positional bias — and proceeds with full confidence. There is no mechanism for the model to flag the contradiction or request guidance. This makes contradiction detection during review far more critical than it would be for human-facing documents.

---

## The cold reader's evaluation rubric

The following rubric synthesizes all researched sources into a practical assessment tool. It is organized into seven dimensions, each containing specific checks that require no domain expertise. Score each check on a 0–3 scale: **0** = not addressed, **1** = partially addressed with significant issues, **2** = mostly addressed with minor issues, **3** = fully addressed. A document scoring below 60% of maximum points in any single dimension likely has structural problems that will affect agent behavior regardless of domain.

### Dimension 1: Structural clarity and information architecture

Does the document have a clear, stated purpose within the first three lines? Is content organized into labeled sections with descriptive headers? Can you understand the document's scope and structure from headers alone? Is the hierarchy logical (identity/role → core behaviors → task-specific rules → constraints → examples)? Is the total length proportionate to scope — ideally under 300 lines, with progressive disclosure to sub-documents for complex domains? Are related instructions grouped together rather than scattered? Is structural formatting consistent throughout (all headers same style, all lists same format)?

### Dimension 2: Behavioral specificity and testability

Does each instruction specify a concrete, observable behavior rather than an aspiration? Can each major directive be verified through a specific test scenario — i.e., could you construct an input that would reveal whether the agent followed the instruction? Are vague qualifiers (*appropriate, reasonable, as needed, properly, when relevant*) absent or accompanied by explicit decision criteria? Are conditional instructions complete — does every "if" have a "then," and are "else" branches specified for important conditions? Is the imperative mood used consistently ("Extract the name" not "The name should be extracted")? Does the document tell the agent what to do rather than what not to do?

### Dimension 3: Internal consistency

Is one term used per concept throughout the entire document — no synonyms for the same entity? Do any two instructions contradict each other when conditions overlap? Is there an explicit priority hierarchy for resolving conflicts between instructions? Are formatting conventions (capitalization, list style, code formatting) consistent throughout? If information is repeated in multiple places, is it identical? Do all internal cross-references point to sections that actually exist?

### Dimension 4: Completeness without bloat

Are normal-case behaviors defined? Are edge cases and exception scenarios addressed with explicit handling? Are error/failure states covered — what should the agent do when tools fail, data is missing, or instructions conflict? Are all referenced tools, resources, files, and external dependencies actually accessible to the agent? Are default behaviors specified for scenarios not explicitly covered? Are there any TBDs, placeholders, or obviously missing sections? Is every instruction necessary — does each sentence carry actionable information that couldn't be removed without changing behavior?

### Dimension 5: Context independence and statefulness

Are all instructions interpretable from the document alone, without assumed shared history? Are there temporal references ("as we discussed," "update the draft," "remember from last time") in what should be a stateless document? Are all technical terms either defined in the document or clearly standard for the stated domain? Does the document specify what information the agent does and does not have access to? If the document references external files or resources, are those references precise enough to resolve (exact paths, not vague descriptions)?

### Dimension 6: Attention-aware design

Are the most critical behavioral rules placed in the first and last sections of the document (exploiting the primacy/recency U-curve)? Are critical constraints visually distinguished — bold, separate sections, or structural emphasis — rather than buried in prose paragraphs? Is the total instruction count reasonable — roughly 50–150 discrete directives maximum for a root instruction file? Are examples used strategically (2–4 canonical examples demonstrating rules in context) rather than exhaustively? Does the document use structured formatting (headers, lists, delimiters) consistently to help the model parse section boundaries?

### Dimension 7: Agent-specific design patterns

Does the document address persistence (should the agent keep working until the task is done, or stop and ask)? Does it address tool usage (when to use tools vs. rely on knowledge, and how to handle tool failures)? Does it address scope boundaries (what the agent should never do, what requires human approval)? If the document is for a coding agent, does it include exact, copy-pasteable build/test/lint commands? Does the document avoid duplicating information the agent can discover from its environment (codebase structure, existing patterns)? Is the document written to work with how LLMs actually process instructions — structured sections, positive directives, explicit criteria — rather than how one would brief a human colleague?

### Quick-reference scoring sheet

| Dimension | Max score | Critical threshold |
|---|---|---|
| Structural clarity | 21 | 13 |
| Behavioral specificity | 18 | 11 |
| Internal consistency | 18 | 11 |
| Completeness without bloat | 21 | 13 |
| Context independence | 15 | 9 |
| Attention-aware design | 15 | 9 |
| Agent-specific patterns | 18 | 11 |
| **Total** | **126** | **77** |

Documents scoring below 77/126 overall or below the critical threshold in any single dimension warrant revision before deployment.

---

## Conclusion: the instruction document is the highest-leverage artifact

The research converges on a counterintuitive finding: the most effective agent instruction documents are not the most comprehensive — they are the most disciplined. Anthropic's "minimal does not necessarily mean short" captures this precisely. Every token must carry signal. Every instruction must be testable. Every ambiguity will be exploited by the model, not flagged for clarification.

The most important checks a cold reader can perform require zero domain knowledge: extract all rules and check them pairwise for contradictions, flag every vague qualifier that lacks decision criteria, verify that critical constraints aren't buried in the middle of the document, and confirm that every reference to an external resource actually resolves. These four checks alone catch the majority of documented agent instruction failures.

The gap this rubric fills is real: despite 60,000+ projects shipping AGENTS.md files and every major AI lab publishing prompting guidance, **no dedicated evaluation framework previously existed for assessing agent instruction document quality**. The closest tools — Anthropic's ai-linter, promptfoo, TaskLint — validate structure or evaluate outputs, not instruction content quality. The rubric above synthesizes IEEE 830 requirements quality characteristics, the cognitive walkthrough method, established technical writing standards, and empirically documented LLM attention patterns into a single assessment instrument. It is intentionally framework-agnostic: the same rubric applies whether the document is a CLAUDE.md, an AGENTS.md, a SOUL.md, a .cursorrules file, or a raw system prompt — because the failure modes are universal.

Alright, here's the checklist. I'm framing this as a framework-agnostic "cold read" rubric — the kind of thing you'd hand to a reviewer who's never seen the agent, the codebase, or the domain, and ask them: "does this instruction file make sense?"

---

## Agent Instruction Document Review Checklist

### 1. First-Pass Readability (Can I even parse this?)

- **Does it read top-to-bottom without backtracking?** You shouldn't need to jump to section 7 to understand section 2. If forward-references are necessary, they should say where to look.
- **Is there a clear opening that says what this agent IS and DOES?** Within the first few lines, a stranger should know: what role this agent plays, what its scope is, and roughly how it operates.
- **Is the density appropriate?** Wall-of-text paragraphs kill comprehension. But over-bulleted listicles lose hierarchy. Check that the formatting actually helps a reader (or an LLM) distinguish "important rule" from "nice-to-have context."
- **Can you skim it and get the gist?** Headers, section breaks, and bold text should let you scan the whole doc in 60 seconds and know what's covered.

### 2. Clarity of Language

- **Plain language over jargon.** If a term is domain-specific, is it defined on first use? Or does the doc assume knowledge the agent won't have?
- **No vague qualifiers.** Watch for "appropriately," "as needed," "when relevant," "in some cases" without saying WHICH cases. These are invisible to an agent — they push decision-making to the model without giving it criteria.
- **Active voice, direct instructions.** "You should check the database" beats "The database should be checked." "Do X" beats "It would be good to do X."
- **One idea per instruction.** If a single sentence contains an instruction AND an exception AND a caveat, it needs to be broken up.

### 3. Consistency

- **Terminology is stable.** If it's called a "task" in one place, it shouldn't become a "job" or "request" or "item" elsewhere unless those are genuinely different things. Pick one word per concept.
- **Naming matches the real system.** If the doc references tool names, API endpoints, file paths, or roles, do those names match what actually exists? Mismatches between the doc and the real environment are silent failure modes.
- **Tone and voice don't drift.** If section 1 is terse and imperative ("Do X. Never Y."), section 4 shouldn't suddenly become conversational ("You might want to consider maybe doing Z").
- **Formatting is uniform.** If one section uses numbered steps, another uses bullets, and another uses prose for the same kind of content (e.g., procedures), that's a problem.

### 4. Completeness vs. Gaps

- **Are the "when" conditions explicit?** For every instruction, is it clear WHEN it applies? "Always," "only if X," "never when Y." If a rule has no trigger condition, the agent has to guess.
- **Are edge cases addressed or deliberately punted?** It's fine to say "if you're unsure, escalate" or "default to X." It's bad to just... not mention what happens when the happy path breaks.
- **Is the failure mode covered?** What should the agent do when a tool call fails, when information is missing, when a user gives contradictory instructions? Silence on failure = undefined behavior.
- **No dangling references.** If the doc mentions "see the style guide" or "follow the escalation process" or "use the approved template," does that thing actually exist and is it accessible?

### 5. Contradictions & Conflicts

- **Do any two instructions directly conflict?** This is the most important single check. Ctrl+F common verbs like "always," "never," "must," "do not" and see if any of them collide. Example: "Always respond in JSON" in section 2 + "Use markdown for reports" in section 5.
- **Is priority clear when rules compete?** If rule A says "be concise" and rule B says "include all relevant details," which wins? Good docs establish a hierarchy or say "when in tension, prefer X."
- **Do examples match the instructions?** If the doc includes examples, do they actually follow the rules stated above them? Mismatched examples teach the wrong behavior.

### 6. Actionability (Could an agent actually follow this?)

- **Instructions are behavioral, not aspirational.** "Be helpful" is a vibe. "When the user asks X, respond with Y format" is actionable. Check that each instruction could be turned into a test case: "Did the agent do the thing or not?"
- **Decision criteria are explicit.** If the agent has to choose between options (which tool, which tone, which format), are the criteria for choosing spelled out? Or is it "use your judgment" with no guidance?
- **Examples exist for non-obvious behavior.** Anywhere the doc describes something nuanced (especially "do this but not that"), at least one concrete example should show what good output looks like.
- **Skill/tool triggers are unambiguous.** If the doc says "use tool X for task Y," is there enough specificity that you could look at a real user request and confidently say whether tool X applies?

### 7. Structure & Information Architecture

- **Most important rules are near the top.** LLMs (and humans) attend more to the beginning. Core identity and hard constraints should come before style preferences and edge cases.
- **Related information is co-located.** If understanding rule A requires context from rule B, they should be near each other — not separated by 2,000 tokens of unrelated content.
- **The doc has a sensible hierarchy.** Identity/role → core rules → tool usage → style/formatting → edge cases → examples is a natural flow. Does the doc follow something like this, or does it jump around?
- **Section headers are descriptive.** "Guidelines" tells you nothing. "How to Handle User Complaints" tells you everything. Headers should work as a table of contents on their own.

### 8. Redundancy & Bloat

- **Is the same instruction repeated in multiple places?** Repetition causes two problems: (1) it wastes tokens, and (2) if you update one copy but not the other, they drift apart.
- **Is there "throat-clearing" that can be cut?** Preambles like "It's important to note that..." or "As an AI agent, you should always strive to..." are filler. The agent doesn't need motivation — it needs instructions.
- **Could any section be half the length without losing meaning?** Read each section and ask: what would I lose if I cut this by 50%? If the answer is "nothing important," it's too long.

### 9. Testability

- **Could you write a pass/fail check for each major rule?** If not, the rule is probably too vague to be useful. "Maintain a professional tone" → hard to test. "Never use profanity; never use emoji unless the user does first" → testable.
- **Are there enough examples to calibrate behavior?** For the most critical behaviors, are there at least a couple of "do this / don't do this" pairs? Without them, you're relying entirely on the model's interpretation.
- **Is there a way to spot-check compliance?** Could a reviewer look at 10 random agent outputs and, using only this doc, grade whether the agent followed the instructions? If the doc is too ambiguous to support that, it's too ambiguous for the agent too.

### 10. Meta-Check: The "Stranger Test"

- **Hand the doc to someone who knows nothing about the project.** Ask them: "What does this agent do? What are its three most important rules? What should it never do?" If they can't answer confidently, the doc fails.
- **Read it out loud.** Awkward phrasing, run-on instructions, and buried critical rules become obvious when spoken.
- **Look for "author's curse" assumptions.** The person who wrote this knows the system. What do they take for granted that isn't on the page? These invisible assumptions are where agents fail most often.

---

The underlying philosophy: an agent instruction doc is a contract, not a narrative. Every sentence should either define a behavior, constrain a behavior, or provide context necessary to execute a behavior. Anything else is noise that dilutes the signal.
