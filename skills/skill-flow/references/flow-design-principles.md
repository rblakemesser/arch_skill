# Flow Design Principles

Use this reference to decide whether a set of skills forms a clean flow.

## The intent spine

A good flow has one repeated user problem running through it. Each skill changes the state of that problem in a way the next skill can use.

Good intent spine:

- "Help authors design, write, and audit a reusable lesson-authoring skill suite."

Weak intent spine:

- "Collect all best practices for skills."

The second shape turns into a handbook. It does not tell the author what each skill owns or what the next skill receives.

## Separable jobs

Each skill should own one durable job. A stage earns a separate skill when it has a different artifact, proof burden, reader moment, or failure mode.

Strong split:

- Skill A chooses the flow shape and handoff artifacts.
- Skill B writes one skill package.
- Skill C audits the authored package or flow with evidence.

Weak split:

- Skill A says "plan the skill."
- Skill B says "make the skill better."
- Skill C says "polish the skill."

The weak split forces the agent to guess where work belongs. Rename the jobs until the owner and output are clear.

## Handoff artifacts

A handoff is not a vibe. It should be one of:

- a concrete artifact the next skill can read
- a blocker question the user must answer
- a verdict or finding set with evidence
- a scoped request for a specialist skill

If the next skill needs hidden context from the previous turn, the flow is not yet clean.

## What "ordered" means

Ordered does not mean one rigid path forever. Ordered means the default next move is visible.

Acceptable complexity:

- an audit can send work back to a repair step
- a Doctrine-authored flow can call on Doctrine-specific teaching
- a missing input can stop with one blocker question

Bad complexity:

- a keyword router that maps phrases to skills
- a gate maze where passing requires satisfying rules nobody can explain
- a flow that changes jobs mid-step because the upstream skill left no artifact

## Peer boundaries

`skill-flow` owns the design or audit of a group of skills. Nearby skills own narrower or different jobs:

- `skill-authoring` owns one skill package's trigger, scope, packaging, and validation.
- `prompt-authoring` owns one prompt contract's intent, section placement, examples, and anti-heuristic repair.
- `doctrine-learn` teaches Doctrine constructs when the author is writing Doctrine source and the skill is available.
- `agent-linter` audits Doctrine-authored prompts, packages, flows, and repo agent surfaces when available.
- `arch-epic` decomposes one execution goal into ordered `arch-step` sub-plans. It does not design a durable peer group of skills.
- `arch-skills-guide` explains which arch skill to use. It does not design or audit a new skill flow.
- `stepwise` executes an ordered process with worker sessions and critics. It is runtime orchestration, not authoring architecture.

When two peers seem relevant, ask what the active question is.
If the active question is "what should this group of skills be and how do they hand off?", stay in `skill-flow`.
If the active question is one package, one prompt, one Doctrine construct, or one execution run, hand off.

## Minimal complexity

The strongest flow is usually smaller than the first draft.

Prefer:

- one clear owner for each durable job
- one handoff artifact per step
- one nearest-peer boundary per skill
- examples that show judgment
- audits that cite evidence and name the smallest fix

Avoid:

- generic "quality" stages
- private workflow assumptions
- scripts that encode taste or routing
- copied doctrine in every skill
- validation gates that only prove the author followed the prompt

## Final self-check

- Can you state the whole flow in one sentence?
- Can you state each skill's job without using the word "better"?
- Does each stage leave an artifact, blocker, verdict, or scoped specialist request?
- Would a new reader know the next move in the normal case?
- Is every branch or loop explained by a real artifact state, not a keyword?
- Could the flow work in another repo without hidden context?
