---
name: eli10
description: "Write, repair, or audit user-facing decision questions as ELI10 decision briefs: re-ground the project/task, explain the stakes in plain English a 16-year-old could follow, recommend one option, compare real options with pros/cons, and close with a Net line. Use when the user asks for ELI10/ELI16-style decision framing, plain-English question context, or recommendation-backed choices. Not for generic simplification, tutoring, prompt-package authoring, or questions the agent can answer from repo/tool evidence."
metadata:
  short-description: "Format decisions with ELI10 stakes and recommendations"
---

# ELI10 Decision Briefs

Use this skill when the job is to ask, write, or repair a user-facing decision question so the user can choose without re-prompting for context, stakes, and a recommendation.

This is a prompt-only skill. Do not add scripts, controller state, a runner, or a formal input schema. The skill owns the shape and quality of the decision brief, not the surrounding workflow that discovered the decision.

## When to use

- The user asks for an `ELI10`, `ELI16`, "explain like I am 10/16", or similar decision-question format.
- The user wants a choice rewritten so it includes plain-English context, stakes, a recommendation, pros/cons, and the real tradeoff.
- A skill, prompt, or workflow needs to ask a non-trivial user decision and the host runtime supports an AskUserQuestion-style tool or an equivalent user-input step.
- The user reports that questions are too terse, too jargon-heavy, missing the recommendation, or just listing options.

## When not to use

- The agent can answer the question from repo, tool, config, docs, or user-provided evidence. Answer it instead of asking.
- The user wants generic simplification, teaching, or an explainer that is not tied to a decision.
- The user wants a reusable prompt contract or skill package authored. Use `$prompt-authoring` or `$skill-authoring`.
- The decision is a true safety, destructive, legal, financial, or access-control gate whose owning workflow requires a stricter approval format.
- The runtime does not need a user decision. Do the work and report the result.

## Non-negotiables

- Every real user decision question is a decision brief, not a bare options list.
- Use plain English a 16-year-old could follow. Explain the situation and stakes with concrete nouns, not function names, implementation labels, or workflow jargon.
- Always include a recommendation. If the choice is neutral, say that explicitly while still choosing a default.
- Keep exactly one `(recommended)` label on the default option. Auto-decision workflows may depend on that label.
- Make the options genuinely comparable. If options differ in coverage, score completeness; if they differ in kind, say so instead of inventing scores.
- Use honest pros and cons. A real choice needs at least two concrete pros and one concrete con per option.
- Close with `Net:` so the user sees the actual tradeoff in one sentence.
- If the host runtime exposes an AskUserQuestion-style tool, send the brief through that tool. If it does not, render the same brief in the host's closest user-input path or in prose.

## First move

1. Identify the actual decision the user needs to make. If there is no real decision, do not force this format.
2. Re-ground on the project, branch, task, or artifact from available context. Do not ask the user for facts that local evidence can answer.
3. Choose the recommended option before drafting the brief. A weak or missing recommendation usually means the agent has not understood the stakes.
4. Decide whether options differ in coverage or in kind.

## Decision Brief Contract

Use this shape for every real decision question:

```text
D<N> — <one-line question title>
Project/branch/task: <1 short grounding sentence using the available project, branch, or task context>
ELI10: <plain English a 16-year-old could follow, 2-4 sentences, name the stakes>
Stakes if we pick wrong: <one sentence on what breaks, what user sees, what's lost>
Recommendation: <choice> because <one-line reason>
Completeness: A=X/10, B=Y/10   (or: Note: options differ in kind, not coverage — no completeness score)
Pros / cons:
A) <option label> (recommended)
  ✅ <pro — concrete, observable, ≥40 chars>
  ❌ <con — honest, ≥40 chars>
B) <option label>
  ✅ <pro>
  ❌ <con>
Net: <one-line synthesis of what you're actually trading off>
```

D-numbering: first question in a skill invocation is `D1`; increment yourself. This is a model-level instruction, not a runtime counter.

ELI10 is always present, in plain English, not function names. Recommendation is ALWAYS present. Keep the `(recommended)` label; auto-decision behavior depends on it.

Completeness: use `Completeness: N/10` only when options differ in coverage. 10 = complete, 7 = happy path, 3 = shortcut. If options differ in kind, write: `Note: options differ in kind, not coverage — no completeness score.`

Pros / cons: use ✅ and ❌. Minimum 2 pros and 1 con per option when the choice is real; minimum 40 characters per bullet. Hard-stop escape for one-way/destructive confirmations: `✅ No cons — this is a hard-stop choice`.

Neutral posture: `Recommendation: <default> — this is a taste call, no strong preference either way`; `(recommended)` stays on the default option for auto-decision behavior.

Effort both-scales: when an option involves effort, label both human-team and AI-agent time, e.g. `(human: ~2 days / agent: ~15 min)`. Makes AI compression visible at decision time.

Net line closes the tradeoff. Per-skill instructions may add stricter rules.

## Workflow

1. **Resolve the ask.** Decide whether the user wants a new decision brief, a rewrite of an existing question, or an audit of a decision question.
2. **Ground the context.** Name the project, branch, task, artifact, or workflow in one short sentence. Use available evidence first.
3. **Write the ELI10 paragraph.** Use 2-4 sentences. Explain what is happening, why the user is being asked, and what is at stake.
4. **Pick the default.** Write the recommendation before listing options. If there is no strong preference, use the neutral posture line and still choose a default.
5. **Compare options honestly.** Use completeness scores only for coverage-different options; use the kind-note for choices that differ by approach, taste, risk posture, runtime, or ownership.
6. **Validate the shape.** Run the self-check below before emitting.
7. **Emit through the right channel.** Use the host's user-input tool when available. Otherwise, return the decision brief as the final or next-step text.

## Self-check before emitting

- [ ] `D<N>` header present
- [ ] `Project/branch/task:` grounding present
- [ ] `ELI10:` paragraph present, with concrete stakes
- [ ] `Stakes if we pick wrong:` present
- [ ] `Recommendation:` present with a concrete reason
- [ ] Completeness scored for coverage choices, or kind-note present for kind choices
- [ ] Every real option has at least two ✅ and one ❌, each at least 40 characters, unless the hard-stop escape applies
- [ ] Exactly one `(recommended)` label is present
- [ ] Dual-scale effort labels appear on effort-bearing options
- [ ] `Net:` closes the decision
- [ ] The question is being emitted through the host's user-input path when that path exists

## Output expectations

- `write`: return or ask with the completed decision brief.
- `repair`: return the corrected decision brief and briefly name what was missing.
- `audit`: return findings first, tied to the missing contract elements, then provide the smallest corrected brief if the user asked for one.

