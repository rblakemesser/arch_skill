# Manifest schema: ordered steps plus resolved execution

The manifest is the authoritative plan for a run. The orchestrator drafts it
in Phase 2 by reading target-repo doctrine, translating the named process into
real steps, and resolving execution preferences against those steps. The
manifest is locked at Phase 3 confirmation and does not change during
execution.

## Top-level shape

```json
{
  "schema_version": 2,
  "target_repo_path": "/abs/path/to/target/repo",
  "target_process": "Track 3 / Section 3 / Lesson 2",
  "doctrine_paths": [
    "/abs/path/to/target/repo/CLAUDE.md",
    "/abs/path/to/target/repo/skills/lessons/SKILL.md"
  ],
  "profile": "strict",
  "forced_checks": ["skill_order_adherence", "no_fabrication"],
  "stop_discipline": "halt_and_ask",
  "per_step_retry_cap": 1,
  "execution_defaults": {
    "step": {
      "runtime": "codex",
      "model": "gpt-5.4",
      "effort": "high",
      "source": "user prompt"
    },
    "critic": {
      "runtime": "codex",
      "model": "gpt-5.4-mini",
      "effort": "xhigh",
      "source": "user prompt"
    }
  },
  "execution_preferences": [
    {
      "source_quote": "all copywriting steps using Claude Opus 4.7",
      "applies_to": "steps whose primary artifact is learner-facing copy",
      "step_execution": {
        "runtime": "claude",
        "model": "opus-4-7"
      },
      "resolution_rationale": "Resolve after step drafting; applies to copy artifacts, not structural JSON that happens to contain strings."
    }
  ],
  "steps": [ /* StepDescriptor[] */ ]
}
```

`stop_discipline` is one of `halt_and_ask`, `skip_and_continue`,
`escalate_to_user`, or `autonomous_repair`. The first three govern behavior
when a step's self-retries are exhausted. `autonomous_repair` additionally
lets the orchestrator reopen an earlier step when a critic sets
`route_to_step_n` on a fail.

## Execution object

Resolved execution blocks appear on every step for both worker and critic:

```json
{
  "runtime": "claude",
  "model": "opus-4-7",
  "effort": "xhigh",
  "source": "execution_preferences[0]",
  "reason": "Matched learner-facing copy artifact lesson-copy.json."
}
```

Fields:

- `runtime`: `"claude"` or `"codex"`.
- `model`: CLI model name to pass to the runtime.
- `effort`: reasoning effort to pass to the runtime.
- `source`: where the value came from, such as `execution_defaults.step`,
  `execution_defaults.critic`, `execution_preferences[0]`, or target doctrine.
- `reason`: one sentence explaining why this execution block applies.

If a preference omits effort, inherit the relevant default effort. If a worker
preference says nothing about critics, critic execution stays on critic
defaults.

## StepDescriptor

```json
{
  "n": 1,
  "label": "Draft lesson outline from source material",
  "skill_or_instruction": "$lessons-ops · draft outline",
  "doctrine_path_for_this_step":
    "/abs/path/to/target/repo/skills/lessons/SKILL.md",
  "inputs": [
    "source: /abs/path/to/target/repo/tracks/track-3/section-3/lesson-2/brief.md"
  ],
  "expected_artifact": {
    "kind": "file",
    "selector":
      "/abs/path/to/target/repo/tracks/track-3/section-3/lesson-2/outline.md",
    "evidence_required":
      "file exists AND first line matches '^# Lesson 2' AND contains '^## '"
  },
  "step_execution": {
    "runtime": "codex",
    "model": "gpt-5.4",
    "effort": "high",
    "source": "execution_defaults.step",
    "reason": "No step-specific execution preference applied."
  },
  "critic_execution": {
    "runtime": "codex",
    "model": "gpt-5.4-mini",
    "effort": "xhigh",
    "source": "execution_defaults.critic",
    "reason": "No critic-specific execution preference was provided."
  },
  "critic_contract_ref": {
    "profile": "strict",
    "active_checks": [
      "skill_order_adherence",
      "no_substep_skipped",
      "artifact_exists",
      "no_fabrication",
      "doctrine_quote_fidelity"
    ]
  },
  "max_retries": 1
}
```

Field notes:

- `n`: 1-indexed position in the ordered sequence.
- `label`: short human-readable description of the step's outcome.
- `skill_or_instruction`: exactly what the step session is supposed to invoke.
  A skill reference (`$lessons-ops`) or a free-form instruction
  (`"run tests and record results"`). Specificity here is what
  `skill_order_adherence` keys off.
- `doctrine_path_for_this_step`: the single file the step session should read
  to learn how to do this step. If the doctrine is split, list the entry
  point; the step session reads onwards from there.
- `inputs`: prior artifacts or source files the step needs to read. Absolute
  paths.
- `expected_artifact`: the thing the critic will verify.
  - `kind`: `file`, `edit`, `file-exists`, or `command-success`.
  - `selector`: the path, pattern, or command string.
  - `evidence_required`: a plain-English predicate the critic translates into
    a read-only shell check.
- `step_execution`: resolved worker runtime/model/effort for this step.
- `critic_execution`: resolved critic runtime/model/effort for this step.
- `critic_contract_ref`: expanded check list for this step.
- `max_retries`: per-step cap, usually equal to `per_step_retry_cap`.

## Drafting discipline

The manifest is a read-then-think product, not a template. When drafting from
the target repo's doctrine:

1. Read `CLAUDE.md` / `AGENTS.md` at the repo root. Find the named process or
   skill.
2. Read the referenced SKILL.md. Identify ordered sub-steps. These become
   candidate steps.
3. For each sub-step, locate the concrete artifact it produces. If no artifact
   is named, look for a natural one. If there is no verifiable artifact, the
   step needs rethinking before execution.
4. Resolve execution for each step using `execution-routing.md`: feasibility,
   hard doctrine, explicit step preference, semantic preference, then defaults.
5. Write the manifest and include a Phase 3 execution table.

## Fail-loud cases

- The named process does not exist in target-repo doctrine. Do not guess. Ask
  which process the user means.
- A sub-step has no verifiable artifact. Ask what evidence of completion looks
  like, or redefine the boundary so artifacts are natural.
- Doctrine contradicts itself across files. Surface the contradiction.
- A routing preference matches no steps, conflicts with hard doctrine, or is
  too ambiguous to apply responsibly. Surface it in Phase 3 and ask.

## Worked example

The user said: "Work in ../lessons_studio. Ramp up on track 3 section 3 and
implement lesson 2 strictly according to the skill order, no fabrication.
Default steps on Codex gpt-5.4 high, critic on Codex gpt-5.4-mini xhigh.
Use Claude Opus 4.7 for copywriting steps."

After reading target doctrine, the orchestrator drafts an abbreviated
manifest:

```json
{
  "schema_version": 2,
  "target_repo_path": "/Users/aelaguiz/workspace/lessons_studio",
  "target_process": "Track 3 / Section 3 / Lesson 2",
  "profile": "strict",
  "forced_checks": ["skill_order_adherence", "no_fabrication"],
  "stop_discipline": "halt_and_ask",
  "per_step_retry_cap": 1,
  "execution_defaults": {
    "step": {
      "runtime": "codex",
      "model": "gpt-5.4",
      "effort": "high",
      "source": "user prompt"
    },
    "critic": {
      "runtime": "codex",
      "model": "gpt-5.4-mini",
      "effort": "xhigh",
      "source": "user prompt"
    }
  },
  "execution_preferences": [
    {
      "source_quote": "Use Claude Opus 4.7 for copywriting steps",
      "applies_to": "steps whose primary artifact is learner-facing copy",
      "step_execution": {
        "runtime": "claude",
        "model": "opus-4-7"
      },
      "resolution_rationale": "Apply only after comparing the drafted step label, instruction, and artifact."
    }
  ],
  "steps": [
    {
      "n": 1,
      "label": "Ramp up on track 3 / section 3 context",
      "skill_or_instruction": "$lessons-ops · ramp-up",
      "doctrine_path_for_this_step":
        "/Users/aelaguiz/workspace/lessons_studio/skills/lessons/SKILL.md",
      "inputs": [],
      "expected_artifact": {
        "kind": "file",
        "selector":
          "/Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/_rampup_notes.md",
        "evidence_required":
          "file exists AND contains '^## Key concepts'"
      },
      "step_execution": {
        "runtime": "codex",
        "model": "gpt-5.4",
        "effort": "high",
        "source": "execution_defaults.step",
        "reason": "Ramp-up is research/context gathering, not the requested copywriting class."
      },
      "critic_execution": {
        "runtime": "codex",
        "model": "gpt-5.4-mini",
        "effort": "xhigh",
        "source": "execution_defaults.critic",
        "reason": "No critic override was provided."
      },
      "critic_contract_ref": {
        "profile": "strict",
        "active_checks": [
          "skill_order_adherence", "no_substep_skipped",
          "artifact_exists", "no_fabrication",
          "doctrine_quote_fidelity"
        ]
      },
      "max_retries": 1
    },
    {
      "n": 4,
      "label": "Write learner-facing copy",
      "skill_or_instruction": "$lessons-ops · copy pass",
      "doctrine_path_for_this_step":
        "/Users/aelaguiz/workspace/lessons_studio/skills/lessons/SKILL.md",
      "inputs": [
        "/Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/lesson-2/playable-manifest.json"
      ],
      "expected_artifact": {
        "kind": "file",
        "selector":
          "/Users/aelaguiz/workspace/lessons_studio/tracks/track-3/section-3/lesson-2/copy.json",
        "evidence_required":
          "file exists AND contains learner-facing hint text"
      },
      "step_execution": {
        "runtime": "claude",
        "model": "opus-4-7",
        "effort": "high",
        "source": "execution_preferences[0]",
        "reason": "The primary artifact is learner-facing copy, matching the user's copywriting preference; effort inherited from the step default."
      },
      "critic_execution": {
        "runtime": "codex",
        "model": "gpt-5.4-mini",
        "effort": "xhigh",
        "source": "execution_defaults.critic",
        "reason": "The user did not route critics to Claude."
      },
      "critic_contract_ref": {
        "profile": "strict",
        "active_checks": [
          "skill_order_adherence", "no_substep_skipped",
          "artifact_exists", "no_fabrication",
          "doctrine_quote_fidelity"
        ]
      },
      "max_retries": 1
    }
  ]
}
```

The example is illustrative. Real manifests follow whatever target-repo
doctrine actually says.
