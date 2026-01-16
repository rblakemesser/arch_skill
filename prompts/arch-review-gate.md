---
description: Request external review for completeness/idiomatic fit.
argument-hint: DOC_PATH=<path>
---
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Request reviews from opus/gemini with the explicit question:
“Is this idiomatic and complete relative to the plan?”
Provide any files they request. Integrate feedback you agree with.
Update $DOC_PATH before moving to the next phase.

OUTPUT FORMAT:
## Review Gate
- Reviewers: <opus|gemini>
- Question asked: “Is this idiomatic and complete relative to the plan?”
- Feedback summary:
  - <item>
- Integrated changes:
  - <item>
- Decision: proceed to next phase? (yes/no)
