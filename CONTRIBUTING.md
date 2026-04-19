# Contributing

Thanks for helping improve `arch_skill`. This repo ships installable agent skills, so changes should keep the runtime surface small, self-contained, and easy to verify.

## Before You Start

- Read [README.md](README.md) for the install surface and shipped skill inventory.
- Read [docs/arch_skill_usage_guide.md](docs/arch_skill_usage_guide.md) when changing workflow routing, install behavior, or auto-controller behavior.
- Read the relevant `skills/<slug>/SKILL.md` before editing a skill package.
- Follow [AGENTS.md](AGENTS.md) for repo-specific development rules.

## Local Checks

After changing skill packages under `skills/`, run:

```bash
npx skills check
```

When changing install behavior or validating the installed runtime surface, run:

```bash
make verify_install
```

When changing only docs or doctrine, re-read the edited files and verify any new commands or paths with `rg`. Do not imply that code verification ran when it did not.

## Contribution Guidelines

- Keep reusable workflow doctrine in `skills/`.
- Keep install behavior in `Makefile`.
- Keep durable user-facing documentation in `README.md` or `docs/`.
- Keep historical material out of the live runtime surface.
- Do not make shipped skills depend on archived command files at runtime.
- Keep `SKILL.md` files concise and move deep reference material into `references/`.
- Update `README.md` and `docs/arch_skill_usage_guide.md` when skill names, routing, supported runtimes, or install behavior change.

## Agent Instructions

- Keep repo-local agent rules in [AGENTS.md](AGENTS.md).
- Keep [CLAUDE.md](CLAUDE.md) as a thin Claude Code shim to `AGENTS.md`; do not duplicate repo rules there.
- Put reusable agent workflows in the owning `skills/<slug>/` package instead of broad research guides under `docs/`.
- Keep instruction docs command-first, current, and free of credentials or private machine paths.

## Pull Requests

A useful pull request includes:

- a short summary of what changed
- the verification commands run and their results
- any docs updated for the changed runtime surface
- any known follow-up work or intentionally deferred cleanup

If you cannot run a required check, say so plainly in the pull request.
