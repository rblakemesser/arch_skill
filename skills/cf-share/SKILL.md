---
name: cf-share
description: "Upload local artifact files or directories (HTML reports, screenshots, analysis bundles, any static files) to the team's Cloudflare R2 share bucket and return a public unguessable https://share.fun.country/<slug>/... URL. Use when the user says 'upload this to cloudflare somewhere I can share', wants a link to drop in Slack, or wants a local HTML report viewable by teammates. Requires a secret env file at ~/.config/cf-share/env (see references/setup.md). Not for deploying apps or product content (ps-content CDN), not for claude.ai Artifacts, and not for material that must stay private."
metadata:
  short-description: "Share local artifacts via a public Cloudflare URL"
---

# CF Share

Use this skill to put a local artifact at a public, unguessable HTTPS URL on
the team's Cloudflare infrastructure so anyone with the link can view it.

One upload = one immutable share under `https://share.fun.country/<slug>/`.
The slug contains random bytes, so links are unlisted: only people given the
URL can find it, but anyone with the URL can open it. Treat every share as
public.

## When to use

- The user wants a local file or directory shared by link with the team.
- The deliverable is a report, analysis page, screenshot set, video, PDF, or
  any static bundle a browser can render.
- Another workflow produced an artifact and the user asks for "a link I can
  send".

## When not to use

- Product or app content belongs on its own pipeline (for example the
  `ps-content` CDN); this bucket is for ad-hoc team artifacts only.
- The content is sensitive (credentials, customer data, unreleased financials)
  and must not sit at a public URL. Say so and offer a private channel instead.
- The user wants a claude.ai Artifact or an in-app preview, not a hosted URL.

## Requirements

- `curl` and `python3` on PATH.
- A secret env file at `~/.config/cf-share/env` (override with `CF_SHARE_ENV`)
  containing `CF_SHARE_API_TOKEN`, `CF_SHARE_ACCOUNT_ID`, `CF_SHARE_BUCKET`,
  and `CF_SHARE_BASE_URL`. If it is missing, point the user at
  `references/setup.md` for the token scopes and file format instead of
  hunting for other Cloudflare credentials.

## Workflow

1. Identify exactly what needs to be shared. Open an HTML artifact and check
   whether it references sibling assets (`./img/...`, `./shots/...`); if it
   does, share the whole directory so relative links keep working. If it is
   self-contained, share just the file.
2. Think before publishing: the URL is public. If the artifact plausibly
   contains secrets or private data, confirm with the user first.
3. Upload:

```bash
bash "{baseDir}/scripts/cf_share.sh" <file-or-dir> [more paths...]
```

   Useful flags: `--entry <name>` to pick which file the headline URL points
   at, `--slug <slug>` to reuse a slug you already told the user about.
   The script picks an unguessable slug, sets correct content types, uploads
   via the Cloudflare R2 REST API, and verifies the entry URL returns HTTP 200.
4. Give the user the entry URL as the answer. If they wanted it posted
   somewhere (for example Slack), hand off to that workflow with the URL.
5. To take a share down later:

```bash
bash "{baseDir}/scripts/cf_share.sh" --delete <slug>
```

## Verification

The script HEAD-checks the entry URL and prints the HTTP status. If it did not
print `verified HTTP 200`, do not hand the link to the user; read the error,
fix (usually a stale token or missing env file), and re-run.

## Reference map

- `references/setup.md` - one-time setup for a new machine or teammate: token
  scopes, secret file format, what infrastructure exists, and how it was
  created.
