# Fugu Ultra Codex Profile Fix Plan

## Bottom Line

`fugu-ultra` is a Codex profile on this machine, not just a model id that can be
passed safely through `--model`.

The failing skills currently collapse "Codex execution choice" into
`runtime/model/effort`, resolve Fugu Ultra to `model=fugu-ultra`, check
`codex debug models`, then launch Codex as:

```bash
codex exec ... --model fugu-ultra -c model_reasoning_effort='"xhigh"' ...
```

That loses the profile's provider and custom catalog. The working invocation is:

```bash
codex exec -p fugu-ultra ...
```

with no `--model fugu-ultra` override.

## Verified Runtime Facts

Local CLI help confirms `-p, --profile <CONFIG_PROFILE_V2>` is supported by
`codex exec`; it layers `$CODEX_HOME/<name>.config.toml` onto the base config.

This machine has:

```text
/Users/aelaguiz/.codex/fugu-ultra.config.toml
```

The profile sets:

```toml
model = "fugu-ultra"
model_reasoning_effort = "xhigh"
model_provider = "sakana"
model_catalog_json = "/Users/aelaguiz/.codex/fugu.json"
```

`codex debug models` only listed these relevant OpenAI catalog models during the
check:

```text
gpt-5.5
gpt-5.4
gpt-5.4-mini
```

That means `codex debug models` is not a valid availability check for custom
profile-backed models such as `fugu` or `fugu-ultra` on this setup.

## Methodology Verified

The profile invocation was tested with a sentinel prompt:

```bash
codex exec -p fugu-ultra \
  --ephemeral \
  --disable codex_hooks \
  --skip-git-repo-check \
  --dangerously-bypass-approvals-and-sandbox \
  -C /tmp \
  -o /tmp/fugu_ultra_profile_ok.txt \
  "Reply with exactly FUGU_ULTRA_PROFILE_OK."
```

The same profile method was also tested with the JSON stream shape used by the
subprocess skills:

```bash
codex exec -p fugu-ultra \
  --ephemeral \
  --disable codex_hooks \
  --skip-git-repo-check \
  --dangerously-bypass-approvals-and-sandbox \
  -C /tmp \
  --json \
  -o /tmp/fugu_ultra_profile_json_final.txt \
  "Reply with exactly FUGU_ULTRA_PROFILE_JSON_OK." \
  > /tmp/fugu_ultra_profile_json_events.jsonl \
  2> /tmp/fugu_ultra_profile_json_stderr.log
```

Result:

```text
model: fugu-ultra
provider: sakana
approval: never
sandbox: danger-full-access
reasoning effort: xhigh
final: FUGU_ULTRA_PROFILE_OK
json final: FUGU_ULTRA_PROFILE_JSON_OK
json stream: thread.started event present
```

The warning about `codex_hooks` being deprecated is unrelated to Fugu Ultra.
It says the feature should eventually become `hooks`.

## Root Cause

The repo taught agents and scripts that `fugu` and `fugu-ultra` are exact Codex
model ids. That was only half true.

For the local Codex CLI, they are runnable through named profiles:

```bash
codex exec -p fugu
codex exec -p fugu-ultra
```

The profile carries the required provider/catalog config. Passing
`--model fugu-ultra` by itself asks the active Codex config to run a model id
without the `sakana` provider context, so model discovery and launch logic treat
it like an unavailable normal Codex model.

## Affected Surfaces

These shipped skill surfaces need the fix:

- `skills/_shared/model_resolution.py` returns only `runtime`, `model`, and
  `effort`; it has no field for Codex profile invocation.
- `skills/fresh-consult/references/model-and-invocation.md` says
  `fugu-ultra` is an exact runnable model id and its Codex launch template uses
  `--model "<resolved_model>"`.
- `skills/agent-delegate/references/model-and-invocation.md` has the same
  resolver doctrine and Codex launch templates.
- `skills/model-consensus/references/model-and-invocation.md` has the same
  Codex first-turn template.
- `skills/stepwise/references/model-and-effort.md` says Fugu/Fugu Ultra are
  model ids, while `skills/stepwise/scripts/run_stepwise.py` passes Codex
  execution through `--model`.
- `skills/arch-epic/references/model-and-effort.md` says Fugu/Fugu Ultra are
  model ids, while `skills/arch-epic/scripts/run_arch_epic.py` passes Codex
  workers and critics through `--model`.
- `tests/test_arch_epic_auto.py` currently tests Fugu as model ids, not
  profile-backed Codex execution choices.
- `README.md` and `docs/arch_skill_usage_guide.md` describe Fugu/Fugu Ultra as
  Codex models rather than Codex profiles.

Generated `skills/*/build/` copies also contain stale wording, but they should
be regenerated or intentionally synced only through the repo's normal skill
build flow. Do not hand-edit build output as the source of truth.

## Fix Shape

Add one more concept to the shared execution contract: Codex model flags and
Codex profile flags are different.

Recommended resolved shape:

```json
{
  "runtime": "codex",
  "model": "fugu-ultra",
  "effort": "xhigh",
  "codex_profile": "fugu-ultra",
  "model_source": "codex_profile"
}
```

For ordinary Codex models such as `gpt-5.5`, keep:

```json
{
  "runtime": "codex",
  "model": "gpt-5.5",
  "effort": "xhigh",
  "codex_profile": "",
  "model_source": "codex_model"
}
```

When building argv:

- If `runtime=codex` and `codex_profile` is set, pass `-p <codex_profile>`.
- If `runtime=codex` and `codex_profile` is set, do not pass `--model`.
- If the user chose the profile's default effort, omit the explicit
  `-c model_reasoning_effort=...`.
- If the user explicitly chose a supported non-default Fugu Ultra effort, add
  `-c model_reasoning_effort=...` after `-p fugu-ultra`.
- `fugu` supports only `high`. `fugu-ultra` supports `high`, `xhigh`, and
  `max`, with `xhigh` as the profile default.
- For ordinary Codex models, keep the existing `--model <model>` and
  `-c model_reasoning_effort=...` behavior.

## Implementation Status

The plan is implemented in source. The changed runtime surfaces are:

- `skills/_shared/model_resolution.py` now resolves Fugu choices with
  `codex_profile` and exposes `codex_model_or_profile_args(...)`.
- `skills/arch-epic/scripts/run_arch_epic.py` and
  `skills/stepwise/scripts/run_stepwise.py` now use the shared helper when
  building Codex worker and critic argv.
- `tests/test_arch_epic_auto.py` and
  `skills/stepwise/scripts/test_run_stepwise.py` now assert that Fugu uses
  `-p` and ordinary GPT/GBT Codex models still use `--model`.
- The live skill doctrine in `fresh-consult`, `agent-delegate`,
  `model-consensus`, `stepwise`, and `arch-epic` now describes Fugu as Codex
  profiles instead of model-list ids.
- `README.md` and `docs/arch_skill_usage_guide.md` now describe provider
  routing as ordinary Codex model ids plus local Fugu profiles.

## Implementation Steps

1. Update `skills/_shared/model_resolution.py` so Fugu and Fugu Ultra resolve
   as Codex profiles, not as plain Codex model ids.
2. Add helper behavior for argv construction, preferably a small shared helper
   that appends either `["-p", profile]` or `["--model", model]` for Codex.
3. Update `skills/arch-epic/scripts/run_arch_epic.py` to use that helper for
   Codex workers and critics.
4. Update `skills/stepwise/scripts/run_stepwise.py` to use the same helper for
   first turns and critics. Resume commands should keep omitting model/profile
   flags unless an explicit same-profile resume override is required.
5. Update fresh-consult, agent-delegate, model-consensus, stepwise, and
   arch-epic doctrine so the examples say:

```text
Fugu Ultra -> runtime=codex, profile=fugu-ultra, model=fugu-ultra, effort=xhigh
```

6. Update `README.md` and `docs/arch_skill_usage_guide.md` so provider routing
   says Codex runs normal Codex model ids plus local Codex profiles such as
   `fugu` and `fugu-ultra`.
7. Update tests so Fugu/Fugu Ultra assertions check for `-p fugu-ultra` and no
   `--model fugu-ultra` in Codex argv.
8. Regenerate or sync build artifacts only through the repo's established skill
   package flow.

## Validation Plan

Run the deterministic tests for the changed script/helper behavior:

```bash
uv run pytest tests/test_arch_epic_auto.py
uv run pytest skills/stepwise/scripts/test_run_stepwise.py
```

Run package validation because source skill packages under `skills/` will
change:

```bash
npx skills check
```

Run a live profile smoke test after the fix:

```bash
codex exec -p fugu-ultra \
  --ephemeral \
  --skip-git-repo-check \
  --dangerously-bypass-approvals-and-sandbox \
  -C /tmp \
  --json \
  -o /tmp/fugu_ultra_profile_ok.txt \
  "Reply with exactly FUGU_ULTRA_PROFILE_OK." \
  > /tmp/fugu_ultra_profile_events.jsonl \
  2> /tmp/fugu_ultra_profile_stderr.log
```

Expected result:

```text
FUGU_ULTRA_PROFILE_OK
thread.started event present in /tmp/fugu_ultra_profile_events.jsonl
```

Also run one ordinary Codex model smoke test, such as `gpt-5.5`, to prove the
profile fix did not break normal `--model` execution.

## Non-Goals

- Do not change Claude, Cursor Agent, or Grok routing.
- Do not make `codex debug models` responsible for custom profile discovery.
- Do not hand-edit generated build copies as the source of truth.
- Do not silently downgrade `fugu-ultra` to `gpt-5.5` if the profile is absent.

## Acceptance Criteria

- A user phrase such as `Fugu Ultra xhigh` resolves to Codex profile execution.
- Codex argv for Fugu Ultra contains `-p fugu-ultra`.
- Codex argv for Fugu Ultra does not contain `--model fugu-ultra`.
- Codex argv for normal GPT/GBT models still uses `--model <model>`.
- The live sentinel command with `codex exec -p fugu-ultra` succeeds.
- `npx skills check` passes after skill package changes.
