# UI Visual Quality Research Notes

Status: research notes for requirements gathering only.

Date: 2026-05-23.

Scope: local psmobile visual-proof methodology, recent X/Grok leads about
agent-assisted UI verification, official tooling docs, and local skills that
contain reusable visual-quality doctrine.

This document is not a proposed architecture. It records observed methods and
requirements pressure for a future coordinated-agent workflow.

## Local Source: psmobile Visual Methodology

Inspected repo:

- `/Users/aelaguiz/workspace/lessons_studio/psmobile`

Relevant governance files:

- `/Users/aelaguiz/workspace/lessons_studio/AGENTS.md`
- `/Users/aelaguiz/workspace/lessons_studio/psmobile/AGENTS.md`
- `/Users/aelaguiz/workspace/lessons_studio/psmobile/docs/AGENTS.md`
- `/Users/aelaguiz/workspace/lessons_studio/psmobile/apps/mobile/AGENTS.md`

Important local constraints found:

- psmobile is Flutter-first. `apps/mobile/**` is deprecated React Native
  reference-only unless explicitly asked.
- The canonical device/simulator control surface is
  `npx tsx scripts/sim.ts`.
- Flutter visual automation uses Flutter `integration_test`, QA commands, and
  simulator/device proof.
- PR-blocking Flutter automation should use checkpoint-driven waits, not fixed
  sleeps or `pumpAndSettle()`.
- The repo distinguishes app-side diagnostic capture from final user-visible
  proof.

### Capture Boundary

The strongest repeated rule is that app-side captures are diagnostic, not final
visual proof.

Evidence:

- `apps/flutter/lib/features/lessons/presentation/playables/v2/surface/lesson_playable_surface_shell.dart`
  states that capture mode may hide lesson chrome for app-side exports and
  should not be used for proof screenshots; final proof should use Mobile MCP
  or another host/device screenshot path for what the user actually saw.
- `apps/flutter/lib/features/lessons/presentation/playables/v2/table/dev/perspective_table_scene_adjustment_host.dart`
  states that app-side capture mode hides authoring chrome and is not a
  substitute for Mobile MCP/user-visible screenshots in visual QA.
- `apps/flutter/lib/features/qa/domain/qa_screenshot_output_writer.dart`
  writes app-side PNGs for developer overlay exports and structural/debug
  modes, but repeats that final visual proof requires Mobile MCP screenshots.
- `apps/flutter/lib/features/lessons/qa/scene_tuning_qa_commands.dart`
  registers `ui.sceneTuning.capture` as a layer-aware app-side path for
  source/mask/capture-mode sanity checks only.

Research implication:

- A future visual reviewer must know which screenshot source can prove which
  claim. "The app produced an image" is not the same as "the user-visible UI
  looked correct."

### Screenshot And Snapshot Pipeline

psmobile already has several artifact-producing visual paths:

- `make flutter-screenshots-list`
- `make flutter-screenshots-smoke`
- `make flutter-screenshots-refresh`
- `make flutter-screenshots-open`
- `make parity-flutter-capture`
- `make parity-grid`
- `make parity-flutter-refresh-latest`
- `npx tsx scripts/sim.ts qa commands list --json`
- `npx tsx scripts/sim.ts go lesson <lessonId> --step-id <stepId> --qa`

Relevant implementation files:

- `scripts/flutter_screenshots/capture.ts`
- `scripts/parity/capture_screenshots.ts`
- `scripts/parity/generate_locator_packs.ts`

Observed methodology:

- `source-mode=latest` in `generate_locator_packs.ts` is read-only and
  headless-safe. It reads checked-in locator packs.
- `source-mode=fresh` drives the Flutter app through `sim` and QA commands,
  takes OS screenshots, and writes screenshot/snapshot artifacts.
- Fresh capture fails loudly on headless environments that do not have the
  required capture tools.
- Captured locator packs include per-surface screenshots plus JSON snapshots.
- Optional ASCII wireframes are generated from screenshots when model support
  is available.
- Parity grids and screenshot contact sheets make broad visual inspection
  cheaper than opening one image at a time.

Research implication:

- A good visual method has to leave browsable artifacts: screenshots, snapshots,
  manifests, contact sheets, and failure reasons. Chat-only assertions are too
  weak.

### Scene-Tuning Proof Matrix

The most mature visual-proof surface is scene tuning.

Relevant sources:

- `docs/PACK/scene_tuning/perspective_lighting_effects_fix_and_sim_test_plan.md`
- `docs/PACKS/scene_tuning_live_audit_2026-05-20/README.md`
- `apps/flutter/lib/features/lessons/qa/scene_tuning_qa_commands.dart`
- `apps/flutter/lib/features/lessons/qa/scene_tuning/scene_tuning_lab_roi_registry.dart`
- `apps/flutter/lib/features/lessons/qa/scene_tuning/scene_tuning_lighting_coverage_validation.dart`
- `scripts/sim.ts`
- `scripts/sim_scene_tuning.test.ts`

Observed proof contract:

- `ui.sceneTuning.replayPlan` emits Mobile MCP visual-matrix metadata.
- Each visual case carries fixture, target ROI, protected ROIs, readability
  ROIs when relevant, before/after/off phases, and the required capture tool.
- The required capture tool is `mobile_save_screenshot`.
- The host-side `scripts/sim.ts scene-tuning` surface owns `worklist`, `run`,
  `step`, `verdict`, and `verify`.
- The runner applies QA commands, ingests Mobile MCP screenshots, validates
  provenance, crops the app surface, computes ROI metrics, writes contact
  sheets, and requires a visual inspection verdict.
- A case is green only when the expected visible change is observed, protected
  ROIs stay within threshold, and the off phase returns to baseline.
- The Lighting/Colors full matrix has a documented floor of 92 handles times 3
  screenshots, or 276 user-visible Mobile MCP screenshots before additional
  monotonic or enum checks.

Strict rejection rules found:

- `captureMethod` must be `mobile_mcp`.
- `captureTool` must be `mobile_save_screenshot`.
- Per-phase Mobile MCP provenance must be present.
- Same-target binding must be proven.
- Phase timestamps/order must be coherent.
- Contact sheet proof must exist and be a real PNG.
- Visual inspection verdict must pass.
- Screenshot existence, command success, replay coverage, app-side capture,
  and metric-only pixel deltas are all insufficient by themselves.

Readability-specific finding:

- The plan explicitly says a pixel delta that makes the receiver/floor near
  black is a failing visual result, not proof that a shadow is correct.
- `scripts/sim_scene_tuning.test.ts` includes tests that reject black floor
  readability even when the target delta passes.

Research implication:

- The strongest pattern is not "take screenshots." It is "bind each screenshot
  to a claim, phase, target, ROI, source tool, device, timestamp, metrics,
  contact sheet, and human-or-agent visual verdict."

### psmobile Gaps And Limits

These are not criticisms of psmobile; they are gaps to consider when extracting
the method into a general workflow.

- The strongest visual matrix is domain-specific to scene tuning. It proves
  lighting/color handles, not generic app UI quality.
- Generic UI failures such as overlapping panels, clipped text, weak hierarchy,
  awkward spacing, broken touch targets, and bad mobile adaptation are named in
  audit docs, but are not yet expressed as one general reusable UI-review role.
- App-side captures remain useful for layers/masks/source sanity, but the
  workflow has to keep agents from confusing those with user-visible proof.
- Pixel metrics are useful supporting evidence, but psmobile explicitly treats
  them as insufficient without visual inspection.
- A future UI reviewer will need a broader matrix than scene-tuning ROI deltas:
  viewport/device coverage, long text, empty/loading/error states, interaction
  states, accessibility tree, semantic DOM or Flutter snapshot data, and actual
  rendered screenshots.

## Recent X/Grok Leads On UI Verification

Grok was asked for recent X/Twitter posts from the last 1-2 months about
builders using Codex, Claude Code, or coding agents for UI visual quality and
visual testing. The resulting posts below were opened directly in BrowserOS.

### JinjingLiang: screenshot loop inside coding agents

- Source: `https://x.com/JinjingLiang/status/2058074665139278275`
- Date: 2026-05-23
- Status: verified by BrowserOS direct X page.
- Observed method: use `agent-browser` or `playwright-cli` so Codex/Claude Code
  takes live screenshots of the UI it generated before finalizing.
- Why it matters: directly supports a rendered-screenshot feedback loop for
  UI/UX, instead of asking a code-only agent to infer visual quality.

### bettercallsalva: browser plus Playwright as a verification boundary

- Source: `https://x.com/bettercallsalva/status/2057912603821687039`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page.
- Observed method: wire Claude Code or Codex to Playwright so the agent opens
  the page, clicks through it, and reads the real DOM back.
- Why it matters: reframes UI completion from "looks done" to "verified done"
  with a browser, interactions, and DOM state.

### aakashgupta: Puppeteer builder-validator loop

- Source: `https://x.com/aakashgupta/status/2039442140405895546`
- Date: 2026-04-01
- Status: verified by BrowserOS direct X page.
- Observed method: embed a Puppeteer screenshot tool in a skill so Claude
  renders HTML, captures its own output, measures overflow/page dimensions, and
  iterates before a human sees the output.
- Why it matters: strong support for making visual QA part of the skill or
  role contract, not a manual loop run by the human.

### 49agents: Figma MCP plus Playwright loop

- Source: `https://x.com/49agents/status/2057918881205755904`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page.
- Observed method: combines Claude Code, Playwright, and Figma MCP as a loop
  from design context to working UI to verification.
- Why it matters: points at a three-source visual method: design intent from
  Figma, rendered behavior from Playwright, and code changes from the agent.

### pankona: natural-language E2E through Claude Code and agent browsers

- Source: `https://x.com/pankona/status/2057987922671128950`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page; X showed a Japanese-to-English
  translation.
- Observed method: describe desired tests in natural language and let Claude
  Code use Playwright or agent browsers to create E2E tests that tolerate some
  UI changes.
- Caveat: the author says it works but is slow and token-heavy.
- Why it matters: useful reminder that agent-driven visual/E2E loops can be
  powerful but need cost and latency controls.

### hiarun02: Playwright MCP as AI-powered UI testing

- Source: `https://x.com/hiarun02/status/2057877359303500136`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page.
- Observed method: lists Playwright MCP as an "AI-Powered UI Testing" plugin
  inside a Claude Code workflow, alongside live docs, GitHub, browser tools,
  database, terminal, and memory plugins.
- Why it matters: evidence that Playwright MCP is becoming a named specialist
  capability in agent workflows, even if this post is a high-level list rather
  than a detailed case study.

### leaf_sanren: Figma context moves agents beyond code context

- Source: `https://x.com/leaf_sanren/status/2058151455429718093`
- Date: 2026-05-23
- Status: verified by BrowserOS direct X page; original post is Chinese.
- Observed method: Figma-Context-MCP feeds layout information from Figma into
  Cursor-like AI coding agents so they see how designs are arranged, how
  components are placed, and why spacing exists.
- Why it matters: reinforces that agents need design context, not only code and
  rendered screenshots.

### ClaudeCode_love: Hallmark UI skill lead

- Source: `https://x.com/ClaudeCode_love/status/2057944593770139893`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page. Treated as a lead-only source.
- Observed method: shares the `nutlope/hallmark` skill for Claude Code, Codex,
  and Cursor, claiming it can generate cleaner UI/landing pages from the start.
- Why it matters: useful skill lead for later review, but this post did not
  itself prove screenshot extraction, visual QA, or design-DNA persistence.

## Native Mobile Agent UI Verification Addendum

The user clarified that most UI work happens in native mobile apps, through
iOS Simulator and Android Emulator, not web pages. That changes the proof
surface. A web verifier can use DOM geometry and browser screenshots. A native
mobile verifier needs device/simulator state, native accessibility or app
hierarchy data, OS screenshots, app lifecycle evidence, and platform-specific
test artifacts.

### Recent X/Grok Leads On Native Mobile UI Verification

Grok was asked for recent X/Twitter posts from the last one to two months
about builders using Codex, Claude Code, or AI coding agents to build and
verify native mobile UI. The posts below were opened directly in BrowserOS.

### TimJayas: autonomous iOS app testing through screenshots and accessibility

- Source: `https://x.com/TimJayas/status/2056452559863525432`
- Date: 2026-05-18
- Status: verified by BrowserOS direct X page. Medium confidence: the post is
  concrete, but does not name the exact bridge or repo.
- Observed method: run the app in iOS Simulator, connect it to Claude Code,
  give a workflow prompt, let the agent read screenshots and the accessibility
  tree, interact through taps/swipes/text entry, check debug logs, and return a
  structured pass/fail bug report.
- Why it matters: this matches the desired native-mobile proof shape better
  than a browser loop because it uses the simulator, accessibility tree,
  screenshots, runtime logs, and a structured report.

### Bitomule: `mav` CLI for iOS Simulator or device evidence

- Source: `https://x.com/Bitomule/status/2056113873724535104`
- Date: 2026-05-17
- Status: verified by BrowserOS direct X page. Strong lead.
- Observed method: `mav` is described as a small CLI that lets coding agents
  drive an iOS Simulator or device, run repeatable flows, and create
  human-reviewable evidence.
- Why it matters: "repeatable flows plus reviewable evidence" is the missing
  bridge between "agent saw a screenshot" and "the mobile UI change was proven
  on a real target."

### BeauJohnson89: Android Claude Code skill pack with a UI quality gate

- Source: `https://x.com/BeauJohnson89/status/2057265529732104406`
- Date: 2026-05-20
- Status: verified by BrowserOS direct X page. Medium confidence: the post
  points at `ayush016/android-lead-agent-skills`, but this pass did not audit
  the repository contents.
- Observed method: an Android team skill pack for Claude Code encodes Compose,
  Material 3, Hilt, Room, Navigation, WorkManager, MCP, testing, security,
  accessibility, and a 29-item UI quality gate.
- Why it matters: this is closer to a reusable native-mobile role contract
  than a one-off prompt. It suggests that platform-specific UI standards should
  live in skills/checklists, not only in chat instructions.

### kalvinmizzi: Claude Code researches XCUITest and runs simulator tests

- Source: `https://x.com/kalvinmizzi/status/2054245310155862381`
- Date: 2026-05-12
- Status: verified by BrowserOS direct X page. Medium confidence: brief
  report, but it names SwiftUI, XCUITest, and simulator execution.
- Observed method: Claude Code built a SwiftUI iOS app, researched XCUITest,
  wrote automated UI tests, and ran them in the simulator.
- Why it matters: this is evidence for agents using the native iOS test stack
  instead of only screenshot inspection.

### Baconbrix: `npx serve-sim` for agent-visible iOS Simulator work

- Source: `https://x.com/Baconbrix/status/2057890427953627598`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page. Medium confidence: the post is
  brief but from a high-signal Expo/React Native builder.
- Observed method: use Claude Desktop or Codex with `npx serve-sim` while
  building mobile apps.
- Why it matters: simulator visibility is becoming part of normal mobile agent
  development, not a separate manual proof step.

### lukasiuu: Flutter network MCP for runtime DevTools gaps

- Source: `https://x.com/lukasiuu/status/2057821247216537855`
- Date: 2026-05-22
- Status: verified by BrowserOS direct X page. Medium confidence: the post is
  about network/runtime visibility, not visual QA specifically.
- Observed method: `flutter_network_mcp` adds Flutter DevTools network traffic
  access for Claude Code, with persistent history, full-text search, alerts,
  and roughly 32 tools.
- Why it matters: native UI proof often fails because the agent cannot see the
  live runtime state behind the screen. Network/state/log context should sit
  beside screenshots and accessibility data.

### y_ogi: iOS Simulator launch is not the same as UI polish

- Source: `https://x.com/y_ogi/status/2057376285433950271`
- Date: 2026-05-21
- Status: verified by BrowserOS direct X page; X showed a Japanese-to-English
  translation. Treated as a lead-only source.
- Observed method: Claude Code with a local Qwen model generated a Swift
  calculator and tested it through launch in the iOS Simulator.
- Caveat: the author explicitly contrasted "it works" with lower UI polish and
  much slower workflow versus Opus 4.7.
- Why it matters: simulator launch proves the app can run; it does not prove
  the UI is good. This is exactly the failure mode the future workflow must
  guard against.

### Native Mobile Official And OSS Tooling Docs Checked

Mobile MCP / Mobile Next:

- Source: `https://github.com/mobile-next/mobile-mcp`
- Relevant facts: Mobile MCP exposes a platform-agnostic interface for iOS and
  Android simulators, emulators, and real devices. Its README says agents can
  interact with native applications through structured accessibility snapshots
  or coordinate-based taps based on screenshots. It documents Codex and Claude
  Code setup commands.
- Research implication: Mobile MCP is a direct fit for a native visual proof
  role, but the role must prefer accessibility snapshots when they exist and
  label coordinate-only steps as weaker evidence.

iOS Simulator MCP:

- Source: `https://github.com/whitesmith/ios-simulator-mcp`
- Relevant facts: this MCP combines `xcrun simctl` for simulator management,
  screenshots, location, and URLs with Facebook `idb` for tap/swipe/type, UI
  hierarchy, and app management. Its limitations call out empty accessibility
  trees, absolute-coordinate interactions, and capped/compressed screenshots.
- Research implication: iOS proof needs target binding, accessibility-tree
  capture, screenshot provenance, and fallback rules when the tree is empty.

Maestro:

- Sources:
  - `https://docs.maestro.dev/get-started/maestro-mcp`
  - `https://docs.maestro.dev/get-started/supported-platform/ios`
  - `https://docs.maestro.dev/get-started/supported-platform/android`
  - `https://docs.maestro.dev/reference/commands-available/takescreenshot`
  - `https://docs.maestro.dev/reference/commands-available/assertwithai`
- Relevant facts: Maestro has an MCP server for AI assistant integration. It
  tests iOS and Android through the accessibility/presentation layer, can
  handle permissions and multi-app journeys, supports screenshots with
  `takeScreenshot`, and has experimental screenshot-plus-LLM assertions through
  `assertWithAI`. `assertWithAI` defaults to optional, so a failed AI assertion
  does not block unless configured otherwise.
- Research implication: Maestro is a good candidate model for native mobile
  flow proof, but AI assertions need explicit blocking semantics and saved
  reports before they can serve as gate evidence.

Appium:

- Sources:
  - `https://appium.io/docs/en/latest/reference/api/webdriver/`
  - `https://appium.io/docs/en/3.1/ecosystem/plugins/`
- Relevant facts: Appium exposes WebDriver endpoints for page/application
  source, element rects, element text, accessible names/roles, full screenshots,
  and element screenshots. Official plugins include `images` for image matching
  and comparison.
- Research implication: Appium can provide both structural hierarchy and
  screenshot/image evidence, but it still needs state/device binding and a
  review layer that knows what claim the image comparison is meant to prove.

Detox:

- Sources:
  - `https://wix.github.io/Detox/docs/introduction/getting-started/`
  - `https://wix.github.io/Detox/docs/guide/taking-screenshots/`
  - `https://wix.github.io/Detox/docs/config/artifacts/`
- Relevant facts: Detox runs React Native E2E tests on a real device or
  simulator and simulates real user interactions. It supports device-level and
  element-level screenshots, artifacts, logs, videos, and iOS view hierarchy
  capture. Its screenshot docs call out volatile device chrome and show the
  need to freeze irrelevant status-bar data for stable snapshot comparison.
- Research implication: native visual proof should normalize or intentionally
  record volatile OS chrome, not let time/status/network icons create noisy or
  misleading diffs.

Flutter `integration_test` and Patrol:

- Sources:
  - `https://docs.flutter.dev/testing/integration-tests`
  - `https://patrol.leancode.co/documentation/native/overview`
  - `https://patrol.leancode.co/cli-commands/test`
  - `https://patrol.leancode.co/documentation/other/patrol-devtools-extension`
- Relevant facts: Flutter's official `integration_test` package can verify
  text, tap widgets, and run integration tests on mobile platforms. Patrol
  fills native gaps that `integration_test` does not cover, such as runtime
  permissions, WebView/OAuth login, notifications, app exit/resume, Wi-Fi,
  mobile data, location, and dark mode. `patrol test` builds and installs the
  app under test plus instrumentation, then runs tests natively through Gradle
  or `xcodebuild`. Patrol DevTools can inspect native UI elements and their
  bounds, text, and accessibility properties on Android and iOS devices.
- Research implication: Flutter UI proof needs both Flutter-aware state and
  OS-native proof. A Flutter widget test can prove logic while missing
  permissions, lifecycle, WebView, notifications, keyboard, and native shell
  behavior.

Apple XCUITest / XCTest and Android UI testing:

- Sources:
  - `https://developer.apple.com/documentation/xcuiautomation/xcuiapplication`
  - `https://developer.apple.com/documentation/XCUIAutomation`
  - `https://developer.android.com/training/testing/ui-tests`
  - `https://developer.android.com/training/testing/espresso`
  - `https://developer.android.com/training/testing/other-components/ui-automator`
- Relevant facts: Apple's UI testing APIs launch, monitor, activate, and
  terminate apps; pass launch arguments/environment; wait for app state; and
  expose screenshot/accessibility-audit capabilities. Android docs split UI
  tests into behavior tests that analyze UI hierarchy and screenshot tests that
  compare UI screenshots with approved images; they explicitly call out API
  level, locale, orientation, tablets, foldables, and other device contexts.
  Espresso adds synchronization/idling behavior for in-app Android UI tests,
  while UI Automator helps associate artifacts such as screenshots with test
  results.
- Research implication: a native mobile UI role should not treat "one phone
  simulator in portrait" as enough proof for a user-facing mobile surface.

Marionette MCP:

- Source: `https://github.com/leancodepl/marionette_mcp`
- Relevant facts: Marionette lets agents connect to a running Flutter app's VM
  service, inspect widgets, simulate taps, enter text, scroll, and take
  screenshots through app-side service extensions. Its own docs warn that the
  agent does not automatically understand the product's flows and needs
  preconditions, expected labels/keys, and interaction goals.
- Research implication: app-runtime MCPs are powerful, but they remain
  diagnostic/app-side evidence unless paired with user-visible simulator or
  device screenshots.

QCKFX iOS verification-gap post:

- Source:
  `https://qckfx.com/blog/giving-your-ai-coding-agent-eyes-on-ios`
- Date: 2026-01-30.
- Status: older than the last one to two months, but useful framing.
- Relevant facts: the post argues that screenshots give agents interaction
  ability but do not by themselves tell the agent whether the UI is correct.
  It separates "agents have hands" from deterministic verification and names
  baselines, existing-function checks, repeatable flows, and consistency as
  what agents actually need.
- Research implication: native visual proof should not stop at giving agents
  simulator eyes and hands. It needs a baseline or explicit expected claim.

### Native Mobile Requirements Pressure

- Native mobile proof must be tied to a specific device or simulator ID, app
  bundle/package, build artifact, platform, OS version, orientation, and screen
  size.
- The proof bundle needs user-visible screenshots from the simulator/device,
  not only app-side debug captures.
- Accessibility tree or native UI hierarchy should be captured when available;
  coordinate-only tapping should be treated as weaker and more brittle.
- Screenshots need route/screen, state, interaction sequence, timestamp, and
  source tool provenance.
- For iOS, safe areas, Dynamic Island/notches, status bar, permission sheets,
  keyboard overlays, system gestures, app activation, deep links, and
  terminate/resume behavior can change whether the UI is actually usable.
- For Android, API level, navigation mode, locale, orientation, foldables,
  tablets, soft keyboard, permissions, system back behavior, and OEM-like
  layout differences can change the real UI.
- For Flutter, React Native, Compose, and SwiftUI, the workflow should know
  when it is looking at framework-level state versus OS-level rendered output.
- Native UI proof should include long text, localization, Dynamic Type/font
  scaling, reduced motion, dark mode, empty/loading/error states, keyboard
  state, and offline/slow-network state when relevant.
- A simulator launch, a passing build, a generated XCUITest/Espresso test, or
  a single screenshot is not enough to prove polish, readability, spacing,
  overlap, or touch ergonomics.
- Contact sheets are especially important for native mobile because one screen
  can have many meaningful variants: iOS/Android, small/large phone, tablet,
  portrait/landscape, keyboard open/closed, permission accepted/denied, and
  signed-in/signed-out.

### Native Mobile Failure Modes To Prevent

- A web-only UI verifier is used to sign off a native app.
- The proof screenshot came from the wrong simulator, device, build, app ID, or
  logged-in state.
- The agent proves only that the app launched, then treats that as UI quality.
- The screenshot is app-side or layer-isolated, while the user-visible
  simulator has overlays, chrome, keyboard, notches, or clipping.
- Accessibility checks pass, but the rendered UI is unreadable, overlapped, or
  visually poor.
- Screenshot or pixel-diff checks pass because something changed, while the
  actual target state got worse.
- The flow works through coordinate taps but fails when labels, locale, device
  size, or safe area changes.
- The verifier checks iOS only and misses Android-specific back behavior,
  keyboard layout, permission dialogs, or navigation bar issues.
- The verifier checks a Flutter widget tree and misses OS-level permission,
  WebView/OAuth, notification, lifecycle, or device-setting behavior.
- The review artifact does not include enough state to replay or inspect the
  claim later.

## Official Tooling Docs Checked

### Playwright MCP

- Snapshot docs: `https://playwright.dev/mcp/snapshots`
- Screenshot docs: `https://playwright.dev/mcp/tools/screenshots`
- Vision mode docs: `https://playwright.dev/mcp/vision-mode`

Relevant facts:

- Playwright MCP defaults to accessibility snapshots for interactions.
- Accessibility snapshots expose structured accessible elements and stable refs
  within a snapshot.
- Screenshots complement accessibility snapshots for visual layout, canvas or
  chart content, bug documentation, and page appearance.
- Vision mode adds coordinate-based tools that work with screenshots for
  elements not exposed in the accessibility tree.

Research implication:

- A visual reviewer should not choose between accessibility snapshots and
  screenshots. The stronger method uses both: structure/refs for interaction
  and screenshots for appearance.

### Figma MCP

- Guide: `https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server`
- Getting started:
  `https://help.figma.com/hc/en-us/articles/39216419318551-Get-started-with-the-Figma-MCP-server`
- What it is:
  `https://help.figma.com/hc/en-us/articles/35280968300439-Figma-MCP-collection-What-is-the-Figma-MCP-server`

Relevant facts:

- Figma MCP gives AI agents structured design context needed for
  design-informed code.
- Agents can read components, variables, layout data, and other design details.
- Figma positions Dev Mode, Code Connect, and MCP together so agents can use
  connected codebase and design-system context instead of only a flat picture.
- Codex, Claude Code, Cursor, Windsurf, and VS Code are named examples of
  compatible agent/client environments in current help docs.

Research implication:

- If the future workflow touches design-backed UI, "read the rendered page" is
  not enough. The reviewer should also know whether a design source or design
  system exists and whether it was used.

### Storybook And Chromatic

- Storybook visual testing:
  `https://storybook.js.org/docs/8/writing-tests/visual-testing`
- Chromatic Storybook docs: `https://www.chromatic.com/docs/storybook`
- Chromatic test docs: `https://www.chromatic.com/docs/test`

Relevant facts:

- Storybook visual tests can turn stories into tests.
- Visual tests compare screenshots to previous versions and are positioned to
  catch layout, color, size, contrast, and other UI appearance changes.
- Chromatic renders stories in cloud browsers, runs attached interaction
  tests, captures snapshots, and detects visual changes.

Research implication:

- For componentized web UI, stories can become the durable visual-test unit.
  This is different from only testing full app routes.

### Percy

- SDK workflow:
  `https://www.browserstack.com/docs/percy/integrate/percy-sdk-workflow`
- Responsive DOM snapshots:
  `https://www.browserstack.com/docs/percy/advanced-snapshots/responsive-dom`
- Responsive testing:
  `https://www.browserstack.com/docs/percy/visual-testing-workflows/view-percy-build-results/responsive-testing`
- Layout testing:
  `https://www.browserstack.com/docs/percy/visual-testing-workflows/view-percy-build-results/layout-testing`

Relevant facts:

- Percy captures the DOM state and assets in the test browser, sends them to
  Percy, and renders screenshots across browsers and widths.
- Responsive snapshots support multiple breakpoint widths.
- Layout testing is intended to identify misaligned elements, spacing
  discrepancies, and visual-presentation differences.

Research implication:

- DOM capture plus server-side browser rendering is a mature pattern for
  repeatable cross-browser visual proof. Even if not adopted directly, it is a
  useful model for separating capture, render, diff, and review.

### BrowserOS

- BrowserOS overview and MCP info were checked through the local
  `browseros_info` MCP tool.
- Docs: `https://docs.browseros.com/`
- Claude Code integration docs:
  `https://docs.browseros.com/features/use-with-claude-code`

Relevant facts:

- BrowserOS is an AI-native Chromium browser.
- Its MCP server exposes browser automation tools to Claude Code, Gemini CLI,
  OpenAI Codex CLI, and Claude Desktop.
- It is explicitly positioned for agentic coding tasks such as testing web
  apps, reading console errors, fixing code, extracting data from authenticated
  pages, and programmatic browser control.

Research implication:

- BrowserOS is not only a research tool. It can be part of the future
  visual-review tool surface for authenticated web apps and browser-based
  verification.

## Local Skill Reference List

These skills are not being proposed as-is. They are reference material for
requirements and later skill design.

### Design taste and anti-generic UI

- `/Users/aelaguiz/.agents/skills/frontend-design/SKILL.md`
- Useful patterns: gather audience/use-case/brand context before design work;
  define a clear design direction; avoid generic AI UI tells; treat typography,
  color, layout, motion, interaction, responsive behavior, and UX writing as
  separate quality dimensions.

### Design critique and automated anti-pattern detection

- `/Users/aelaguiz/.agents/skills/critique/SKILL.md`
- Useful patterns: independent design review plus deterministic detector;
  browser visualization; console-readable findings; Nielsen heuristic scoring;
  cognitive-load checklist; persona red flags; severity-ranked findings.

### Final polish and production detail

- `/Users/aelaguiz/.agents/skills/polish/SKILL.md`
- Useful patterns: final pass only after functional completion; check alignment,
  spacing, typography, color, states, motion, copy, icons, forms, edge cases,
  responsiveness, performance, code quality, and accessibility; test actual
  interactions and real devices.

### Layout, spacing, typography, and responsive specialists

- `/Users/aelaguiz/.agents/skills/arrange/SKILL.md`
- `/Users/aelaguiz/.agents/skills/typeset/SKILL.md`
- `/Users/aelaguiz/.agents/skills/adapt/SKILL.md`
- Useful patterns: squint test, spacing rhythm, grid/flex choice, hierarchy,
  line length, type scale, minimum text sizes, touch targets, and device/input
  adaptation.

### Robustness and real-world edge cases

- `/Users/aelaguiz/.agents/skills/harden/SKILL.md`
- `/Users/aelaguiz/.agents/skills/normalize/SKILL.md`
- `/Users/aelaguiz/.agents/skills/optimize/SKILL.md`
- Useful patterns: long text, short/empty data, special characters, RTL/i18n,
  network/API errors, loading/empty/error/success states, design-system token
  alignment, interaction states, CLS/layout shift, animation performance, and
  accessible focus.

### Browser/mobile proof and simulator loops

- `/Users/aelaguiz/.agents/skills/mobile-mcp-app-walkthrough/SKILL.md`
- `/Users/aelaguiz/.agents/skills/flutter-dev-return/SKILL.md`
- `/Users/aelaguiz/.agents/skills/audit-loop-sim/SKILL.md`
- Useful patterns: screenshot every distinct state; keep index and coordinate
  notes; use accessibility data before coordinates where available; keep one
  warm device; capture/restore supported surfaces; map app surfaces and
  automation coverage before edits; do not downgrade real-app proof to weak
  unit/widget checks when the risk is visual or device-level.

### Figma and source-backed visual fidelity

- `/Users/aelaguiz/.agents/skills/figma-best-practices/SKILL.md`
- Useful patterns: classify artifacts before trusting them; source-backed
  parity needs a source pair, render proof, dimensions, normalization, ignored
  regions, and blocker disclosure; tool success is provisional until readback,
  bounds, screenshots, and source-of-truth checks agree.

### Contact sheets and visual comparison artifacts

- `/Users/aelaguiz/.agents/skills/contact-sheet-builder/SKILL.md`
- `/Users/aelaguiz/.agents/skills/theme-preview/SKILL.md`
- `/Users/aelaguiz/.agents/skills/theme_tuner/SKILL.md`
- Useful patterns: labeled dense contact sheets, before/after comparison,
  review boards, anchoring generated variations to real screenshots, and
  carrying forward only approved visual rules.

### Advanced motion/effect discipline

- `/Users/aelaguiz/.agents/skills/overdrive/SKILL.md`
- Useful patterns: ambitious effects require browser automation preview and
  iteration; do not assume technically working effects look right; test
  performance, reduced motion, device behavior, and whether the effect fits the
  product context.

### Image asset QA

- `/Users/aelaguiz/.agents/skills/theme_builder/SKILL.md`
- `/Users/aelaguiz/.agents/skills/chroma-key-transparency/SKILL.md`
- Useful patterns: independent visual QA for generated assets; deterministic
  masks/metrics/previews/contact sheets; visible residue or subject erosion is
  a real failure, not a minor artifact.

## Cross-Source Requirements Pressure

The following are requirements pressure, not final design:

- Visual proof must be claim-bound. A screenshot proves only the screen it
  captured, from its source tool, at its device/viewport/state, for the claim
  it was inspected against.
- Pixel deltas are supporting evidence, not a pass condition by themselves.
- Screenshot existence is not proof of quality.
- App-side diagnostic captures must be labeled as diagnostic and cannot pass a
  user-visible claim unless the claim is specifically about that diagnostic
  layer.
- A visual reviewer needs at least three information channels when available:
  rendered screenshot, semantic/accessibility/DOM or app snapshot data, and
  design-system or Figma/source context.
- Browser/UI agents should interact with the surface, not only load it. Clicks,
  navigation, form states, scroll states, and error/loading states matter.
- Generic UI proof needs viewport/device matrices, not only one happy-path
  desktop or simulator screenshot.
- Native mobile proof needs simulator/device identity, platform, app
  bundle/package, build artifact, OS version, orientation, screen size,
  accessibility/UI hierarchy when available, and app lifecycle state.
- Native mobile evidence must distinguish OS-visible screenshots from
  framework-level state and app-side diagnostic captures.
- Long text, empty data, loading state, error state, keyboard focus, touch
  target size, and reduced motion should be treated as first-class visual
  states when relevant.
- Safe areas/notches, status/navigation bars, soft keyboard overlays,
  permissions, deep links, background/resume, system back behavior, Dynamic
  Type/font scaling, locale/RTL, dark mode, tablets/foldables, WebView/OAuth,
  notifications, and offline/slow-network states are native-mobile visual or
  interaction states, not optional polish when the feature touches them.
- Contact sheets and manifests reduce review friction and make evidence
  auditable after the run.
- Visual specialists should be independent from implementers. A role that just
  confirms its own code is likely to accept weak proof.
- The future coordinator should preserve visual-review results as structured
  receipts: source tool, path, viewport/device, route/surface, interaction
  sequence, timestamp, pass/fail verdict, reviewer notes, and linked issue
  list.
- Cost and latency matter. Agent-browser and Playwright loops can be slow and
  token-heavy, so the future workflow needs a way to scale visual rigor to risk.

## Failure Modes To Prevent

- "It looks fine" with no screenshot, route, state, or viewport.
- "The pixels changed" without a user-visible quality claim.
- "Screenshot captured" without inspecting overlap, clipping, readability, and
  interaction state.
- App-side hidden-chrome capture used as final proof of normal app UI.
- Web-only UI verifier used as signoff for a native mobile app.
- Native mobile screenshot captured from the wrong simulator, device, app ID,
  build, logged-in state, orientation, or OS version.
- Simulator launch treated as proof of UI quality.
- Visual diff passing while the UI becomes unreadable or unpleasant.
- Agent claims an effect works because an internal layer changed, even though
  the user-facing screen did not improve.
- Reviewer only checks one viewport and misses mobile overlap or desktop
  density failures.
- Design-backed UI built without checking Figma/design-system source when that
  source exists.
- Automated visual tools produce noisy diffs that humans or agents
  rubber-stamp.
- A beautiful static screenshot hides broken keyboard, focus, tap, loading, or
  error behavior.
- Flutter/widget-level evidence hides OS-level failure in permissions,
  WebView/OAuth, notifications, app lifecycle, keyboard, safe areas, or native
  shell behavior.

## Open Questions For Later Design

- What is the minimum visual-proof bundle for web UI, Flutter mobile UI, and
  generated image/theme assets?
- What is the minimum native-mobile proof bundle for iOS Simulator, Android
  Emulator, physical device, Flutter, React Native, Compose, and SwiftUI work?
- How should the coordinator decide between cheap screenshot review, full
  browser interaction, Mobile MCP device proof, Maestro/Appium/Detox/native
  test execution, Storybook/Chromatic/Percy visual testing, and fresh visual
  arbiter review?
- Which native-mobile conditions are always required versus risk-scaled:
  iOS/Android parity, phone/tablet/foldable, portrait/landscape, keyboard,
  permission accepted/denied, app resume, deep link, dynamic type, locale/RTL,
  dark mode, and offline/slow-network?
- Can a single UI specialist cover both taste critique and deterministic
  geometry/accessibility proof, or should those be separate roles?
- How should the workflow encode "human visual inspection" when the inspector
  is a fresh visual-review agent?
- What evidence schema should unify screenshots, accessibility snapshots, DOM
  geometry, Flutter QA snapshots, Figma nodes, and contact sheets?
- Which visual failures are blocking by default: overlap, clipping, unreadable
  text, broken touch target, broken focus, bad visual hierarchy, poor taste,
  or mismatch to design source?
- How should the coordinator prevent overuse of slow screenshot loops on tiny
  code changes while still catching high-risk UI regressions?
