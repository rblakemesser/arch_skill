# Simplicity And Architecture Research

Date: 2026-06-25

Parent brief:
[Cynical Architecture Review Intention](../CYNICAL_ARCHITECTURE_REVIEW_INTENTION_2026-06-25.md)

Sibling references:

- [Doctrine notes](CYNICAL_ARCHITECTURE_REVIEW_DOCTRINE_NOTES.md)
- [Failure-pattern catalog](ARCHITECTURE_FAILURE_PATTERNS.md)
- [Future skill shape](FUTURE_SKILL_SHAPE.md)

## Research Claim

The strongest architecture thinkers converge on the same practical stance:
software architecture improves when accidental complexity is removed, ownership
is clarified, and the system reflects one coherent design idea.

The useful review question is not:

```text
How can we justify this architecture?
```

It is:

```text
Which parts of this architecture are forced by the intended user experience,
hard constraints, and experiment requirements?
```

Everything else is a deletion candidate, consolidation candidate, or ownership
repair candidate.

## Source Synthesis

### Elon Musk: delete before optimize

Source:
[Everyday Astronaut, Starbase Tour and Interview with Elon Musk](https://everydayastronaut.com/starbase-tour-and-interview-with-elon-musk/)

Relevant idea:
Musk's engineering sequence starts by challenging requirements, then deleting
parts or process steps, then simplifying and optimizing, then increasing speed,
then automating. The order matters because the common expert failure is
optimizing something that should not exist.

Architecture-review translation:

- Every requirement must have a responsible owner and must survive challenge.
- Delete structure before refining structure.
- Do not speed up, automate, generalize, or polish a bad architecture path.
- If nothing has to be added back after deletion, the review was probably too
  timid.

Review question:

```text
What part of this architecture would disappear if we questioned the requirement
that supposedly forced it?
```

### John Ousterhout: complexity accumulates through small dependencies

Sources:

- [Stanford CS190 complexity notes](https://web.stanford.edu/~ouster/cgi-bin/cs190-spring16/lecture.php?topic=complexity)
- [A Philosophy of Software Design book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)

Relevant idea:
Ousterhout frames complexity as anything that makes software hard to evolve.
Dependencies and obscurity are central causes. His notes stress that programs
evolve continuously, working code is not enough, and complexity accumulates
through many small dependencies over time.

Architecture-review translation:

- "It only adds one small dependency" is how architecture debt spreads.
- A structure can be locally reasonable and globally corrosive.
- Architecture review should attack accumulated dependencies and obscurity,
  not only large visible messes.
- The reviewer should ask whether the change makes future evolution easier or
  harder.

Review question:

```text
What new thing must a future maintainer know, remember, configure, call, or keep
in sync because this structure exists?
```

### David Parnas: modules should hide volatile design decisions

Source:
[On the Criteria To Be Used in Decomposing Systems into Modules](https://prl.khoury.northeastern.edu/img/p-tr-1971.pdf)

Relevant idea:
Parnas contrasts decomposition by processing steps with decomposition by
information hiding. The stronger modules hide design decisions likely to change
and reveal as little as possible through their interfaces.

Architecture-review translation:

- A file split is not automatically good architecture.
- Ownership should follow hidden design decisions, not incidental execution
  order.
- Split ownership is invalid when several modules must know the same private
  representation, lifecycle, or state rule.
- A boundary is suspect when it exposes internal sequencing or storage details.

Review question:

```text
Which design decision is this owner hiding, and why is that the right owner?
```

### Fred Brooks: conceptual integrity beats many independent good ideas

Sources:

- [Conceptual integrity excerpt](https://warwick.ac.uk/fac/sci/dcs/research/em/teaching/cs405-0708/conceptual_integrity.pdf)
- [No Silver Bullet](https://www.cs.unc.edu/techreports/86-020.pdf)

Relevant idea:
Brooks treats conceptual integrity as central to system design. A system should
reflect one coherent set of design ideas. In `No Silver Bullet`, he separates
essential complexity from accidental complexity and discusses how some tools
remove complexity that was never inherent in the program.

Architecture-review translation:

- Many "good" local ideas can make one bad architecture.
- Accidental complexity is removable; essential complexity is the real problem
  domain.
- A review should not accept arbitrary complexity just because it has already
  become familiar.
- Conceptual integrity is a user-experience concern, not an ivory-tower
  preference. A user-friendly system often omits things that do not fit the
  design.

Review question:

```text
Does this system now express one design idea, or several local ideas that happen
to coexist?
```

### Niklaus Wirth: lean software is a design responsibility

Source:
[A Plea for Lean Software](https://people.inf.ethz.ch/wirth/Articles/LeanSoftware.pdf)

Relevant idea:
Wirth argues against bloated software and treats complexity and size reduction
as a design duty, not a later optimization. His complaint is especially useful
for architecture review because bloat often arrives as harmless features,
options, and generalized machinery.

Architecture-review translation:

- Lines of code are not productivity when they create future maintenance drag.
- Feature accretion is a primary source of architectural obesity.
- Lean architecture should be judged across specification, design, and detailed
  code, not only at the end.

Review question:

```text
What did this add that the required user experience does not actually need?
```

### Tony Hoare: obvious simplicity is stronger than hidden cleverness

Source:
[The Emperor's Old Clothes](https://worrydream.com/refs/Hoare_1981_-_The_Emperors_Old_Clothes.pdf)

Relevant idea:
Hoare's Turing lecture argues for designs that make good ideas elegantly
expressible and warns against complexity that hides deficiencies.

Architecture-review translation:

- Clever architecture that hides its failure modes is dangerous.
- The best design should make the central idea easier to express.
- If the architecture needs a long explanation to seem reasonable, it may be
  protecting accidental complexity.

Review question:

```text
What would the architecture look like if the central idea had to be obvious?
```

### Rich Hickey: simple is not the same as easy

Source:
[Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/)

Relevant idea:
Hickey separates simplicity from ease. Easy things are nearby or familiar.
Simple things are not interwoven. Complexity comes from intertwinement.

Architecture-review translation:

- Existing architecture can be easy because it is nearby, while still being
  complex because it tangles responsibilities.
- A new wrapper may feel easy to add but can increase intertwinement.
- The review should reward designs that separate concerns even when the first
  edit is less convenient.

Review question:

```text
Did this choose the nearby path because it was easy, or the separated path
because it is simple?
```

### Martin Fowler: do not build presumptive features, and pay down cruft

Sources:

- [Yagni](https://martinfowler.com/bliki/Yagni.html)
- [Technical Debt](https://martinfowler.com/bliki/TechnicalDebt.html)

Relevant idea:
Fowler's `Yagni` note argues against building future capability before it is
needed. His technical debt discussion frames internal-quality cruft as a cost
that slows future changes.

Architecture-review translation:

- Do not accept abstraction for imagined future use.
- Presumptive extension points are complexity unless current requirements
  force them.
- Cruft matters most when work will continue in the same area; repeated
  iteration compounds bad architecture.

Review question:

```text
What future requirement is this architecture betting on, and is that requirement
real enough to charge today's complexity tax?
```

### Doug McIlroy and Unix: small composable units

Source:
[Unix philosophy summary](https://principles.design/examples/unix-philosophy)

Relevant idea:
The Unix tradition values small programs that do one thing well, work together,
and can be rebuilt when the old shape becomes clumsy.

Architecture-review translation:

- A component should have one clear job and a clean composition boundary.
- Extending an old component by piling on features can be worse than building a
  small new unit.
- Composition is useful only when the pieces are clean and the interfaces stay
  simple.

Review question:

```text
Is this component doing one real job, or has it become the place where nearby
work gets dumped?
```

### John Gall: working complexity grows from working simplicity

Source:
[Gall's Law quote page](https://www.goodreads.com/quotes/9353506-a-complex-system-that-works-is-invariably-found-to-have)

Relevant idea:
Gall's Law says working complex systems tend to evolve from working simple
systems. That does not excuse accidental sprawl. It says complexity should grow
from a simple working core, not from an invented complex architecture.

Architecture-review translation:

- If the simple core is missing, complexity is probably unstable.
- If the code grew complexity before proving the integrated path, the review
  should push back.
- The reviewer should identify the simple core and ask whether current
  structures still serve it.

Review question:

```text
Where is the working simple system inside this, and which parts no longer serve
it?
```

### Thoughtworks evolutionary architecture: architecture needs live feedback

Source:
[Fitness function-driven development](https://www.thoughtworks.com/en-us/insights/articles/fitness-function-driven-development)

Relevant idea:
Evolutionary architecture uses feedback to keep architecture aligned with
desired qualities as systems change. This is useful as a principle, but it
should not be misread as a mandate to build heavy proof harnesses.

Architecture-review translation:

- Architecture quality is not a one-time declaration. It drifts unless review
  keeps checking it.
- The skill can name architecture qualities and drift risks without
  building a deterministic validator.
- Feedback can be human review, code reading, and source-truth comparison in
  v1.

Review question:

```text
What architecture quality is this structure supposed to preserve, and what is
the lightest honest way to keep it from drifting?
```

## Combined Doctrine

The `cynical-architecture-review` skill should treat architecture as guilty of
accidental complexity until proven otherwise.

The review should:

1. Start from user experience and constraints, not from the existing file map.
2. Separate essential complexity from accidental complexity.
3. Challenge requirements before challenging implementation details.
4. Delete or consolidate before optimizing.
5. Prefer one coherent design idea over several locally reasonable ideas.
6. Assign ownership by hidden design decisions and invariants, not by who added
   the last feature.
7. Penalize dependencies, obscurity, intertwinement, presumptive features, and
   future-bet abstractions.
8. Protect experiment requirements, but reject complexity that merely claims to
   protect them.
9. Return findings that make future code simpler to write, not just current
   code easier to explain.

## Practical Review Heuristics

Use these as judgment prompts, not rigid rules:

- If a concept appears in three places, find the real owner.
- If two places can write the same truth, one of them is probably wrong.
- If an abstraction mostly passes data through, it is probably hiding confusion.
- If a flag changes architecture rather than behavior, it may be a split-brain
  path.
- If a helper exists only for one caller, ask whether direct code is clearer.
- If a registry maps things that could be normal imports or types, ask what
  runtime variability forced it.
- If a new layer mostly exists to keep old code alive, ask why the old code was
  not deleted.
- If a design needs docs to prevent misuse, ask whether the API shape should
  prevent misuse instead.
- If the implementation has more concepts than the user experience, ask which
  concepts are accidental.
