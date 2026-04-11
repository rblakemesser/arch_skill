# Arch Skills Guide Boundary Examples

## Full arch vs mini plan

- "Do the full arch flow for this migration":
  - `arch-step`
- "Give me the mini plan version in one pass":
  - `arch-mini-plan`

## Full arch vs read-only flow

- "What is the next move on this doc?":
  - `arch-flow`
- "Advance this doc and run the next step":
  - `arch-step`

## Full arch vs docs cleanup

- "Implement the plan and audit the code against it":
  - `arch-step`
- "The code is clean; now clean up the feature docs and retire the plan doc":
  - `arch-docs`

## Single bug vs audit loop

- "Analyze this Sentry crash and fix it":
  - `bugs-flow`
- "Scan the repo for the next real bugs and keep cleaning until it is not worth continuing":
  - `audit-loop`

## Mini plan vs lilarch

- "Small feature, but I still want the canonical architecture blocks":
  - `arch-mini-plan`
- "This should fit in 1-3 phases, use little arch":
  - `lilarch`

## Bugs vs investigation loops

- "We need to explain a metric drop and test ranked hypotheses":
  - `north-star-investigation`
- "We know the goal but not the path, keep iterating bets":
  - `goal-loop`
