# Examples And Anti-Examples

Use these examples to calibrate judgment. Do not turn them into a routing table.

## Good: flow owner plus specialists

User ask:

> Design a set of skills for writing and auditing reusable onboarding agents.

Good shape:

- `skill-flow` defines the skill suite, default handoffs, and flow-level audit checks.
- `skill-authoring` writes or repairs each individual skill package.
- `prompt-authoring` strengthens any prompt contracts inside those packages.
- `agent-linter`, when available, audits Doctrine-authored packages or the flow with evidence.

Why it works:

- the flow owner keeps the throughline
- each specialist owns one active question
- no skill pretends to execute the whole workflow every time

## Good: ordered with a repair loop

Good flow:

1. Design the flow and handoff artifacts.
2. Author the first skill package.
3. Author the next skill package from the prior handoff artifact.
4. Audit the flow.
5. Repair only the smallest owning surface when the audit finds a real issue.

Why this is still ordered:

- the default path is visible
- the audit loop is based on evidence
- repair returns to the owner of the defect, not to a vague "make better" stage

## Anti-example: router disguised as a skill

Bad shape:

```markdown
If the user says "prompt", call prompt-authoring.
If the user says "skill", call skill-authoring.
If the user says "Doctrine", call doctrine-learn.
If the user says "audit", call agent-linter.
```

Why it fails:

- keywords replace judgment
- mixed requests get routed by accident
- the flow owner stops thinking about artifacts and handoffs

Better shape:

Ask what the active question is. Use the specialist whose job owns that question, and keep the flow-level handoff in `skill-flow`.

## Anti-example: private workflow fossilized as doctrine

Bad shape:

- every flow must use exactly five stages
- every stage must pass a named gate before the next stage can start
- every flow must consult a specific external model
- every audit must create the same files

Why it fails:

- it encodes one person's current process as universal law
- it makes the skill hard to use in new repos
- it turns a judgment skill into an execution harness

Better shape:

Teach what the flow must prove: distinct jobs, concrete handoffs, peer boundaries, and evidence-based audit.

## Anti-example: arch-epic confusion

Bad ask for `skill-flow`:

> Break this large implementation goal into sub-plans and run each one through arch-step.

Use `arch-epic`.

Good ask for `skill-flow`:

> Design the reusable skill suite we should use for authoring, reviewing, and publishing skill flows.

Why the boundary matters:

- `arch-epic` executes one large goal by decomposing it into approved sub-plans.
- `skill-flow` designs or audits the durable skills and handoffs that could be reused across many goals.

## Anti-example: stage names hide duplicate work

Bad flow:

1. Strategy skill
2. Planning skill
3. Architecture skill
4. Improvement skill

Why it fails:

- the stage names are broad and overlapping
- none names an artifact or proof burden
- the handoff is hidden in the author's memory

Better flow:

1. Flow design skill leaves a table of skill jobs and handoff artifacts.
2. Skill authoring skill creates one package from one row of that table.
3. Prompt authoring skill repairs prompt contracts inside the package when needed.
4. Flow audit skill reports evidence-backed boundary or handoff defects.

The better flow still needs real names, but each row now has a job and an output.

## Quick diagnosis prompts

Use these when a flow feels wrong:

- "What artifact does this skill leave behind?"
- "Could the next skill start from that artifact without hidden context?"
- "Which nearby skill would a model choose by mistake?"
- "Is this a real stage, or just another way to say quality?"
- "Is this rule teaching judgment, or trying to route by keyword?"
