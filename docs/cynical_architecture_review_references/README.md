# Cynical Architecture Review Reference Pack

Date: 2026-06-25

Parent brief:
[Cynical Architecture Review Intention](../CYNICAL_ARCHITECTURE_REVIEW_INTENTION_2026-06-25.md)

Status: source/reference material for the implemented
[`cynical-architecture-review`](../../skills/cynical-architecture-review/)
skill. This folder is not the runtime skill package and should not be
installed as runtime behavior.

## Documents

- [Simplicity and architecture research](SIMPLICITY_AND_ARCHITECTURE_RESEARCH.md)
  - Source-backed synthesis of subtraction-first architecture ideas from Musk,
    Ousterhout, Parnas, Brooks, Wirth, Hoare, Hickey, Fowler, McIlroy, Gall,
    and related architecture doctrine.
- [Doctrine notes](CYNICAL_ARCHITECTURE_REVIEW_DOCTRINE_NOTES.md)
  - Converts the research into reviewer behavior, operating questions, and
    quality bars.
- [Failure-pattern catalog](ARCHITECTURE_FAILURE_PATTERNS.md)
  - Concrete patterns the review should hunt: sprawl, split ownership,
    abstraction laundering, permanent compatibility paths, registries, flags,
    state spread, and architecture that "just happened."
- [Future skill shape](FUTURE_SKILL_SHAPE.md)
  - Source lane, trigger, boundaries, workflow, and output shape folded into
    the prompt-only `cynical-architecture-review` skill.

## Research Source Map

Primary or near-primary sources used in the research synthesis:

- Elon Musk engineering algorithm, Everyday Astronaut Starbase tour:
  <https://everydayastronaut.com/starbase-tour-and-interview-with-elon-musk/>
- John Ousterhout, Stanford CS190 complexity notes:
  <https://web.stanford.edu/~ouster/cgi-bin/cs190-spring16/lecture.php?topic=complexity>
- John Ousterhout, `A Philosophy of Software Design` book page:
  <https://web.stanford.edu/~ouster/cgi-bin/book.php>
- David Parnas, `On the Criteria To Be Used in Decomposing Systems into Modules`:
  <https://prl.khoury.northeastern.edu/img/p-tr-1971.pdf>
- Fred Brooks, `No Silver Bullet`:
  <https://www.cs.unc.edu/techreports/86-020.pdf>
- Fred Brooks, conceptual integrity excerpt:
  <https://warwick.ac.uk/fac/sci/dcs/research/em/teaching/cs405-0708/conceptual_integrity.pdf>
- Niklaus Wirth, `A Plea for Lean Software`:
  <https://people.inf.ethz.ch/wirth/Articles/LeanSoftware.pdf>
- Tony Hoare, `The Emperor's Old Clothes`:
  <https://worrydream.com/refs/Hoare_1981_-_The_Emperors_Old_Clothes.pdf>
- Rich Hickey, `Simple Made Easy`:
  <https://www.infoq.com/presentations/Simple-Made-Easy/>
- Martin Fowler, `Yagni`:
  <https://martinfowler.com/bliki/Yagni.html>
- Martin Fowler, `Technical Debt`:
  <https://martinfowler.com/bliki/TechnicalDebt.html>
- Doug McIlroy / Unix philosophy summary:
  <https://principles.design/examples/unix-philosophy>
- John Gall, Gall's Law quote page:
  <https://www.goodreads.com/quotes/9353506-a-complex-system-that-works-is-invariably-found-to-have>
- Thoughtworks, fitness function-driven development:
  <https://www.thoughtworks.com/en-us/insights/articles/fitness-function-driven-development>

Repo-local doctrine cross-links:

- [Cynical code review skill proposal](../CYNICAL_CODE_REVIEW_SKILL_PROPOSAL_2026-06-25.md)
- [Architecture pattern convergence](../architecture_pattern_convergence.md)
- [Plan review skill plan](../PLAN_REVIEW_SKILL_PLAN_2026-05-24.md)
- [`skills/plan-audit/references/architecture-quality-canon.md`](../../skills/plan-audit/references/architecture-quality-canon.md)
- [`skills/cynical-code-review/SKILL.md`](../../skills/cynical-code-review/SKILL.md)
- [`vendor/cursor/plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`](../../vendor/cursor/plugins/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)

## Main Synthesis

The review should be built around one plain idea:

```text
Architecture does not deserve trust because it exists. It earns trust only
when it is the smallest robust structure that preserves the real user
experience, hard constraints, and experiment requirements.
```

The review should therefore be subtractive before it is additive:

1. Name the intended user experience.
2. Name the real requirements and constraints.
3. Identify complexity that is essential to those requirements.
4. Treat every remaining layer, owner, path, flag, state, helper, wrapper, and
   abstraction as suspect.
5. Prefer deletion, consolidation, ownership repair, and simpler boundaries
   over adding new structures.
