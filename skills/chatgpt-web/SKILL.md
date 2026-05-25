---
name: chatgpt-web
description: "Query logged-in ChatGPT through BrowserOS MCP after shaping the prompt with prompt-authoring discipline. Use when the user asks to ask ChatGPT, consult ChatGPT in the browser, get a ChatGPT web opinion, or run a prompt through the logged-in ChatGPT UI with optional attachments. Defaults to Pro with Extended thinking when the user does not specify mode or effort; respects explicit Instant, Thinking, Pro, Light, Standard, Extended, or Heavy requests. Not for OpenAI API work, generic browser automation, automated login, scripts, runners, or hidden harnesses."
metadata:
  short-description: "Query logged-in ChatGPT through BrowserOS"
---

# ChatGPT Web

Use this skill when the user wants a head start querying ChatGPT through the
already logged-in BrowserOS browser session.

This is a prose-only helper skill. It uses BrowserOS MCP directly. It ships no
scripts, runners, controllers, harnesses, schemas, or automation infrastructure.

## Use When

- The user asks to ask ChatGPT, consult ChatGPT, get ChatGPT's opinion, or run a
  prompt through the ChatGPT web UI.
- The user wants BrowserOS MCP to drive logged-in ChatGPT instead of using the
  OpenAI API.
- The user wants local attachments included in a ChatGPT web prompt.
- The user has a rough prompt and wants it shaped before sending.

## Do Not Use When

- The user wants OpenAI API usage or product/API guidance.
- The user wants generic web automation unrelated to ChatGPT.
- BrowserOS MCP is unavailable in the current host.
- ChatGPT is not already logged in in BrowserOS.
- The task would require automated login.
- The user requests more than 10 attachments.

## Non-Negotiables

- Use BrowserOS MCP, not `web.run`, OpenAI API calls, shell browser scripts, or
  direct cookie/session handling.
- Use `$prompt-authoring` discipline before submission when the user's prompt is
  rough, underspecified, high-stakes, or likely to benefit from a stronger
  reusable prompt shape.
- Default to ChatGPT `Pro` with `Extended` thinking when the user does not name
  a mode or effort.
- Respect explicit user choices for `Instant`, `Thinking`, `Pro`, `Light`,
  `Standard`, `Extended`, or `Heavy`.
- Do not downgrade or upgrade the requested mode silently.
- Never automate login. If ChatGPT is not logged in, fail loudly and tell the
  user to log in manually in BrowserOS.
- Do not print, save, summarize, or inspect account details, cookies, tokens,
  raw session payloads, or other secrets.
- Enforce a maximum of 10 attachments. Do not silently drop files.
- Keep the result simple: ChatGPT's answer plus a short receipt.

## First Move

1. Resolve the user's desired ChatGPT ask and any explicit mode, effort, model,
   or attachment requests.
2. If the prompt needs shaping, apply `$prompt-authoring` before touching
   ChatGPT. Keep the prompt faithful to the user's intent.
3. Find an existing `https://chatgpt.com/` BrowserOS page or open one.
4. Verify the page is logged in before doing anything else.

## Login Check

From the ChatGPT page, use BrowserOS MCP page JavaScript to fetch:

```javascript
fetch('/api/auth/session', { credentials: 'include' })
```

Use only the safe boolean result: whether the parsed JSON has a `user` value.
Do not display or store the returned user, account, token, cookie, or session
fields.

If the session does not prove a logged-in user, stop with:

```text
BrowserOS is not logged in to ChatGPT. Open https://chatgpt.com/ in BrowserOS,
log in manually, then rerun $chatgpt-web.
```

If the endpoint cannot be checked, fail loudly. Do not infer login from visible
page controls.

## Mode And Effort

Default when the user does not specify:

```text
mode = Pro
effort = Extended
model family = current ChatGPT default
```

Use the ChatGPT model pill beside the composer. Prefer `Configure...` when
available because it exposes the `Intelligence` dialog with explicit model
options and thinking effort.

Observed controls to select from:

- mode: `Instant`, `Thinking`, `Pro`
- effort: `Light`, `Standard`, `Extended`, `Heavy`
- model family: leave as current unless the user explicitly names one

Do not run a Pro prompt merely to test the skill. Only use Pro when the user's
actual request needs the default or explicitly asks for it.

## Attachments

Preflight attachments before browser interaction:

- every path must be absolute
- every path must exist
- count must be 10 or fewer

Use the BrowserOS file-upload path that works with ChatGPT:

1. Create a temporary visible file input in the page for BrowserOS MCP to use.
2. Use BrowserOS MCP `upload_file` with the user's absolute paths.
3. Transfer the selected `File` objects into ChatGPT's hidden `#upload-files`
   input.
4. Dispatch `input` and `change` events on the ChatGPT input.
5. Confirm visible attachment chips by filename.
6. Remove the temporary visible input.

If any requested filename does not appear as an attachment chip, stop before
submitting.

## Submission

1. Fill the ChatGPT composer with the final prompt.
2. Confirm the selected mode and effort match the request or default.
3. Confirm every attachment chip is present.
4. Click `Send prompt`.
5. Wait until generation finishes.
6. Read the latest assistant response from the page.

## Output

Return:

- ChatGPT's answer
- mode and effort used
- attachment filenames, if any
- a short note if the prompt was shaped before submission

If the run fails, name the exact failed condition and the next manual repair.
