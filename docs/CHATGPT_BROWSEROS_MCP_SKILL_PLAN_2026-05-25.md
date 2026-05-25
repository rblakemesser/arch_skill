# ChatGPT BrowserOS MCP Skill Plan

Status: planning and research document only. Do not treat this as implemented
behavior.

Date: 2026-05-25

Working skill name: `chatgpt-web`

Implementation note: the later approved helper skill uses the name
`chatgpt-web`, defaults to `Pro` with `Extended` thinking when the user does not
specify mode or effort, and returns ChatGPT's answer with a short receipt. The
research observations below are still useful, but the final skill contract
supersedes earlier draft defaults that preferred Thinking/Standard or saved
run receipts by default.

## 0. User Problem

We need a skill that uses BrowserOS MCP to query ChatGPT through the logged-in
browser session at `https://chatgpt.com/`.

The skill should:

- fail loudly when BrowserOS is not logged in to ChatGPT
- select the requested ChatGPT intelligence mode
- select the requested thinking effort when the mode supports it
- attach local files when requested
- submit the user prompt
- return the ChatGPT answer with enough metadata to know what was run

This plan is only for browser-driven ChatGPT usage through BrowserOS MCP. It is
not an API client, not a replacement for OpenAI API usage, not a general browser
automation framework, and not an implementation plan for hidden scripts.

## 1. Confirmed BrowserOS And ChatGPT State

BrowserOS MCP currently exposes an active ChatGPT tab:

```text
https://chatgpt.com/
```

The page is logged in. Confirmed signs:

- sidebar links are visible: `New chat`, `Search chats`, `Projects`,
  `Library`, `Apps`, `Codex`
- composer textbox is visible: `Chat with ChatGPT`
- account/profile button is visible: `Pro Pro, open profile menu`
- profile menu contains `Profile`, `Settings`, `Help`, and `Log out`

Do not use those visible strings as login proof. The reliable probe is the
session endpoint below.

## 2. Login Detection

Use a page-context fetch from `https://chatgpt.com/`:

```javascript
const res = await fetch('/api/auth/session', { credentials: 'include' });
const data = await res.json();
```

Confirmed logged-in result shape:

```json
{
  "ok": true,
  "status": 200,
  "hasUser": true,
  "hasExpires": true,
  "topLevelKeys": [
    "WARNING_BANNER",
    "user",
    "expires",
    "account",
    "authProvider",
    "rumViewTags"
  ]
}
```

Do not print, save, or summarize `data.user`, `data.account`, tokens, cookies,
or any account-specific values. The skill only needs booleans such as
`hasUser` and `hasExpires`.

Useful negative probe:

```javascript
const res = await fetch('/api/auth/session', { credentials: 'omit' });
const data = await res.json();
```

Observed with credentials omitted:

```json
{
  "ok": true,
  "status": 200,
  "hasUser": false,
  "hasExpires": false,
  "topLevelKeys": ["WARNING_BANNER"]
}
```

This is not a full manual logged-out test, because we did not log out of the
real BrowserOS profile. It does confirm that the endpoint cleanly distinguishes
session-bearing and no-session requests.

V1 fail-loud rule:

- If `/api/auth/session` with `credentials: 'include'` does not return JSON with
  `user` present, stop immediately.
- The error should say:

```text
BrowserOS is not logged in to ChatGPT for this browser profile. Open
https://chatgpt.com/ in BrowserOS, log in manually, then rerun the skill.
```

If the endpoint is unavailable, fail loudly. Do not infer login from visible
page controls.

## 3. Model And Thinking Effort Selection

The ChatGPT composer has a model/effort pill next to the textbox. Observed
labels:

- `Extended`
- `Thinking`

Clicking the pill opens a quick menu. Observed menu items:

```text
Instant
Thinking
Pro - Extended
Configure...
```

When the thinking effort is `Extended`, the quick menu labels can become:

```text
Thinking - Extended
Pro - Extended
```

For precise selection, use `Configure...`. It opens the `Intelligence` dialog.

Observed `Intelligence` dialog controls:

- heading: `Intelligence`
- combobox: `Model`
- radio group: `Model options`
- radio: `Instant For everyday chats`
- radio: `Thinking For complex questions`
- radio: `Pro Research-grade intelligence`
- combobox: `Thinking effort`

Observed model-family combobox options:

```text
5.5
5.4
5.3
5.2
4.5
o3
```

Observed thinking-effort options:

```text
Light
Standard
Extended
Heavy
```

Observed behavior:

- Selecting `Thinking` and `Standard` makes the composer pill read `Thinking`.
- Selecting `Thinking` and `Extended` makes the composer pill read `Extended`
  and the quick menu show `Thinking - Extended`.
- The effort setting also appears in the quick `Pro - Extended` label.
- We did not run a Pro prompt. Pro was observed only as a menu/radio option.

V1 selection model:

- `intelligence_mode`: `instant`, `thinking`, or `pro`
- `thinking_effort`: `light`, `standard`, `extended`, or `heavy`
- `model_family`: optional; default to the current selected family, observed as
  `5.5`

Final helper-skill default when the user does not specify:

```text
intelligence_mode = pro
thinking_effort = extended
model_family = current
```

Pro safety rule:

- Do not run `Pro` prompts merely for smoke tests or research.
- Use `Pro` when it is the active default for a real user request or when the
  user explicitly requests `Pro`.
- Do not silently upgrade a `thinking extended` request to `Pro`.
- If `Pro` is requested and the `Pro` radio is missing, fail loudly.
- This research pass did not send any Pro prompts because Pro prompts are slow.

## 4. Attachment Handling

Observed attachment UI:

- button: `Add files and more`
- menu item: `Add photos & files Command U`
- hidden file inputs in the DOM:
  - `input#upload-files`
  - `input#upload-photos`
  - `input#upload-camera`

Observed user-provided constraint:

- Assume ChatGPT accepts at most 10 attachments.
- The skill should preflight attachment count.
- If more than 10 files are requested, fail loudly or require the caller to
  split the run. Do not silently drop files.

Direct BrowserOS `upload_file` against the hidden ChatGPT input did not work
when using the DOM node id returned by `search_dom`; BrowserOS `upload_file`
expects an element id from `take_snapshot`, and hidden inputs are not exposed in
the accessibility snapshot.

Working disk-backed attachment method:

1. Create a visible temporary bridge input in the page:

   ```javascript
   let input = document.querySelector('#browseros-bridge-file');
   if (!input) {
     input = document.createElement('input');
     input.type = 'file';
     input.multiple = true;
     input.id = 'browseros-bridge-file';
     document.body.appendChild(input);
   }
   input.setAttribute('aria-label', 'BrowserOS bridge file input');
   input.style.cssText =
     'position:fixed;left:30px;top:80px;width:360px;height:48px;' +
     'z-index:2147483647;opacity:1;background:white;color:black;' +
     'border:3px solid blue;padding:6px;';
   ```

2. Run `take_snapshot`. BrowserOS exposes the created input as:

   ```text
   button "BrowserOS bridge file input"
   ```

3. Use BrowserOS MCP `upload_file` on that snapshot element with absolute local
   file paths.

   Confirmed with:

   ```text
   /Users/aelaguiz/workspace/arch_skill/skills/exhaustive-code-review/agents/openai.yaml
   ```

   BrowserOS reported:

   ```json
   {
     "action": "upload_file",
     "fileCount": 1
   }
   ```

4. Transfer the selected disk-backed `File` objects from the bridge input to
   ChatGPT's hidden input:

   ```javascript
   const bridge = document.querySelector('#browseros-bridge-file');
   const target = document.querySelector('input#upload-files');
   const dt = new DataTransfer();
   for (const file of bridge.files) dt.items.add(file);
   target.files = dt.files;
   target.dispatchEvent(new Event('input', { bubbles: true }));
   target.dispatchEvent(new Event('change', { bubbles: true }));
   ```

5. Wait until the composer shows attachment chips for each filename.

   Confirmed chip:

   ```text
   openai.yaml
   ```

6. Remove the temporary bridge input after transfer:

   ```javascript
   document.querySelector('#browseros-bridge-file')?.remove();
   ```

Working generated-text attachment method:

```javascript
const target = document.querySelector('input#upload-files');
const dt = new DataTransfer();
dt.items.add(new File(
  ['BrowserOS attachment smoke test.'],
  'browseros-smoke-test.txt',
  { type: 'text/plain' }
));
target.files = dt.files;
target.dispatchEvent(new Event('input', { bubbles: true }));
target.dispatchEvent(new Event('change', { bubbles: true }));
```

Confirmed composer chip:

```text
browseros-smoke-test.txt
```

## 5. Prompt Submission

Confirmed flow:

1. Select `Thinking` with `Standard` effort.
2. Attach `browseros-smoke-test.txt`.
3. Fill textbox `Chat with ChatGPT` with:

   ```text
   Reply with exactly: OK ATTACHMENT TEST
   ```

4. Click `Send prompt`.
5. Wait for response controls such as `Copy response`, `Good response`,
   `Bad response`, and for `Stop answering` to disappear.

Observed result:

```text
OK ATTACHMENT TEST
```

Observed thinking indicator:

```text
Thought for a couple of seconds
```

No Pro prompt was run during this research.

## 6. Proposed V1 Skill Contract

Use when the user wants the agent to query ChatGPT through the already logged-in
BrowserOS profile.

Do not use when:

- the user wants OpenAI API usage
- the user wants a generic web automation skill
- ChatGPT is not logged in in BrowserOS
- the prompt would require automated login
- the user asks for more than 10 attachments

Non-negotiables:

- Use BrowserOS MCP, not direct OpenAI API calls.
- Never automate ChatGPT login.
- Fail loudly if ChatGPT session is absent.
- Never log cookies, tokens, account details, or raw session JSON.
- Default to Pro with Extended thinking unless the user specifies a different
  mode or effort.
- Respect explicit mode and effort requests.
- Never run Pro in tests or smoke checks.
- Preflight all attachment paths before touching the browser.
- Enforce the 10-attachment maximum.
- Confirm attachment chips by filename before submitting.
- Return ChatGPT's answer, the mode and effort used, attachment filenames if
  any, and a short note if the prompt was shaped before submission.

Do not save secrets, cookies, auth JSON, or full account metadata.

## 7. Proposed V1 Workflow

1. Resolve the ChatGPT tab:
   - Use an existing `https://chatgpt.com/` page when present.
   - Otherwise open `https://chatgpt.com/`.
2. Verify login:
   - Run `/api/auth/session` with `credentials: 'include'`.
   - Fail loudly unless `data.user` exists.
3. Normalize requested settings:
   - mode: `instant`, `thinking`, or `pro`
   - effort: `light`, `standard`, `extended`, or `heavy`
   - family: optional model family, default current
4. Open the model/effort pill.
5. Use `Configure...` for reliable selection.
6. Select model family if requested.
7. Select mode radio.
8. Select thinking effort when requested or when defaulting to Pro Extended.
9. Close the dialog and verify the composer pill reflects the requested mode.
10. Preflight attachments:
    - all paths are absolute
    - all paths exist
    - count is 10 or fewer
11. Attach files through the bridge-input method.
12. Confirm visible attachment chips by filename.
13. Fill the composer textbox.
14. Click `Send prompt`.
15. Wait until generation finishes.
16. Extract the assistant response.
17. Reply with:
    - ChatGPT mode and effort used
    - attachment filenames
    - ChatGPT's answer
    - one-line status

## 8. Failure Conditions

Fail loudly when:

- no ChatGPT page can be opened
- `/api/auth/session` does not prove a logged-in user
- the composer textbox is missing
- model or effort controls are missing
- requested mode or effort cannot be selected
- Pro is requested but not available
- any attachment path is missing
- more than 10 attachments are requested
- attachment chips do not appear for every requested file
- the send button remains disabled after prompt and attachments are ready
- generation errors, stalls, or shows a rate/limit message

The failure should name the exact missing condition and the next manual repair,
for example:

```text
ChatGPT is open but not logged in in BrowserOS. Log in manually at
https://chatgpt.com/ in BrowserOS, then rerun the skill.
```

## 9. Open Questions For Implementation

- Logged-out UI was not manually tested because we did not log out of the real
  BrowserOS profile. The session endpoint with omitted credentials returned
  `hasUser: false`, which is enough to design the fail-loud gate.
- The exact behavior of `Pro` plus each effort level was not tested. The UI
  exposes `Pro` and the shared thinking effort combobox, but no Pro prompt was
  sent.
- The exact maximum attachment count was not tested. Treat the user's note as
  the V1 constraint: maximum 10 attachments.
- The response extraction method should prefer DOM text from the latest
  assistant message and fall back to the `Copy response` button only if needed.
- The skill should avoid leaving temporary bridge inputs or unsent attachment
  chips behind after failures.

## 10. Research Log

Observed with BrowserOS MCP:

- `list_pages` found active ChatGPT page id `408`.
- `take_snapshot` showed logged-in ChatGPT controls.
- `/api/auth/session` with credentials included returned `hasUser: true`.
- `/api/auth/session` with credentials omitted returned `hasUser: false`.
- Model quick menu exposed `Instant`, `Thinking`, `Pro`, and `Configure...`.
- `Configure...` opened the `Intelligence` dialog.
- Thinking effort options were `Light`, `Standard`, `Extended`, and `Heavy`.
- A generated text file attachment created a visible attachment chip.
- A disk-backed local file was selected via a temporary bridge input and then
  transferred into ChatGPT's hidden upload input.
- A non-Pro Thinking/Standard prompt with an attachment succeeded and returned
  `OK ATTACHMENT TEST`.
