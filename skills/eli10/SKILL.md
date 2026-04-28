---
name: eli10
description: "Answer, explain, summarize, plan, review, or ask in ELI10/ELI16 style: plain English a 16-year-old can follow, concrete stakes, jargon translated on first use, technical facts preserved, and no baby talk. Use whenever the user explicitly asks for `$eli10`, `ELI10`, `ELI16`, `explain like I am 10/16`, or similar across ordinary answers, technical briefs, plans, recommendations, and decision questions. Not for changing the underlying task owner; if the response asks the user to choose, use the decision-brief sub-mode."
metadata:
  short-description: "Answer in plain-English ELI10 style"
---

# ELI10 Plain-English Answers

Use this skill as a response style for the user's current ask. When the user invokes `$eli10`, `ELI10`, `ELI16`, "explain like I am 10/16", or similar, answer the question in plain English a 16-year-old can follow, no matter whether the answer is a direct explanation, plan, status update, review, recommendation, or decision question.

This is a prompt-only skill. Do not add scripts, controller state, a runner, or a formal input schema. The skill changes how the answer is written; it does not change which underlying skill, repo workflow, tool, or safety rule owns the work.

## When to use

- The user explicitly asks for `$eli10`, `ELI10`, `ELI16`, "explain like I am 10/16", "ELI10 style", or equivalent plain-English framing.
- The user asks a normal question and wants the answer back in ELI10 style.
- The user wants a technical plan, audit, status, recommendation, or explanation rewritten so the stakes and moving parts are easy to understand.
- The user reports that prior output was too terse, too jargon-heavy, too abstract, or missing the "why this matters" layer.

## When not to use

- The user did not ask for this style and no active runtime explicitly loaded it.
- The user wants a prompt or skill authored rather than an answer styled for readability. Use `$prompt-authoring` or `$skill-authoring`, then apply ELI10 wording only if requested.
- The user asks for exact legal, medical, financial, security, or scientific guidance that requires formal wording. Still explain plainly, but do not remove required caveats, uncertainty, source grounding, or safety boundaries.
- The answer must be a machine-readable artifact, exact code patch, command output, JSON, schema, or quoted text. Keep that exact part exact, and use ELI10 prose around it only where prose is allowed.

## Non-negotiables

- Answer the actual question. Do not switch into a decision template unless the response actually asks the user to choose.
- Use short sentences, concrete nouns, and active voice.
- Translate jargon on first use, then keep the real term. Example: "AIVAT is the noise reducer; it tries to separate poker skill from card luck."
- Keep technical facts exact: commands, file paths, metrics, API names, probabilities, and failure modes must not be softened into vague analogies.
- Name the stakes. Say what breaks, what the user sees, what becomes easier, or what risk is avoided.
- Do not use baby talk, cute analogies, fake certainty, or "this is complicated" filler.
- Preserve the user's needed level of detail. ELI10 means understandable, not shallow.
- If the response asks the user to choose, use the decision-brief sub-mode below.

## First move

1. Identify the shape of the current ask: direct answer, explanation, plan, review, recommendation, rewrite, or decision question.
2. Keep the owning workflow intact. If another skill or tool owns the substance, use that owner and apply this style to the user-facing prose.
3. List the terms, metrics, or commands that must stay exact.
4. Decide what the user needs to understand first: the stakes, the moving parts, the recommendation, or the failure mode.

## Default Answer Contract

For ordinary answers, do not use a decision template. Use the natural structure that fits the question, with these requirements:

- Start with the concrete answer in 1-3 sentences.
- Explain the stakes before low-level mechanics when the stakes are not obvious.
- Define important jargon on first use.
- Use bullets or short sections when the answer has multiple moving parts.
- Keep code, commands, metrics, and quoted identifiers exact.
- End with a short `Net:` line when the answer is a plan, tradeoff, risk explanation, or recommendation.

Good ELI10 output feels like a sharp engineer translating the real issue for a smart person who has not been living inside the project. Weak output merely adds "plain English version" labels while leaving jargon, hidden assumptions, or vague claims intact.

## Decision-Brief Sub-mode

Use this only when the response is asking the user to choose between options. Do not use it for normal explanations, plans, or status answers.

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

D-numbering starts at `D1` within the current skill invocation. It is model-level numbering, not runtime state.

For real decisions, `ELI10`, `Recommendation`, exactly one `(recommended)` label, and `Net:` are mandatory. Use completeness scores only when options differ in coverage; otherwise write: `Note: options differ in kind, not coverage — no completeness score.`

Pros / cons: use ✅ and ❌. Minimum 2 pros and 1 con per option when the choice is real; minimum 40 characters per bullet. Hard-stop escape for one-way/destructive confirmations: `✅ No cons — this is a hard-stop choice`.

Neutral posture: `Recommendation: <default> — this is a taste call, no strong preference either way`; `(recommended)` stays on the default option for auto-decision behavior.

## Workflow

1. **Resolve the substance.** Answer, inspect, plan, or reason as the task requires. This skill does not replace the underlying work.
2. **Translate the answer.** Rewrite the user-facing prose so the first pass is understandable without a follow-up asking for ELI10.
3. **Preserve hard facts.** Check exact terms, commands, metrics, file names, and evidence before simplifying.
4. **Add stakes.** If the answer involves a plan, risk, measurement, or recommendation, say why it matters.
5. **Choose the output shape.** Use normal prose for answers and explanations; use the decision-brief sub-mode only for real user choices.
6. **Scrub weak simplification.** Remove baby talk, false analogies, vague "messy" explanations, and prose that hides the real mechanism.

## Self-check before emitting

- [ ] The answer addresses the user's actual question.
- [ ] The first 1-3 sentences give the concrete answer or direction.
- [ ] Key jargon is translated on first use without deleting the real term.
- [ ] Commands, paths, metrics, and technical identifiers remain exact.
- [ ] Stakes are named when the answer is a plan, risk, recommendation, or explanation of a failure.
- [ ] No baby talk, fake certainty, or vague placeholder explanation remains.
- [ ] Decision-brief format is used only if the response asks the user to choose.
- [ ] `Net:` appears when a plan, tradeoff, risk, or recommendation needs a closing synthesis.

## Output expectations

- `answer`: answer the current question in ELI10 style.
- `explain` or `rewrite`: preserve the technical truth while making the prose understandable.
- `plan`: keep the implementation meaning intact, define jargon, name stakes, and close with `Net:`.
- `review` or `audit`: lead with findings or the main judgment, then explain each issue plainly.
- `decision`: use the decision-brief sub-mode.
