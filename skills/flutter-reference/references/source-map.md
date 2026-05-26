# Official Source Map

Use this reference when a Flutter answer depends on facts that might change:
framework recommendations, package APIs, platform-view behavior, build modes,
testing commands, rendering defaults, platform policy, or game-library APIs.

This file is a source map, not a reading checklist. Open only the links that
matter for the user's current question, and prefer current official docs over
remembered behavior.

## Flutter Architecture

- App architecture guide: https://docs.flutter.dev/app-architecture/guide
- Architecture recommendations: https://docs.flutter.dev/app-architecture/recommendations
- Data-layer case study: https://docs.flutter.dev/app-architecture/case-study/data-layer

Use these for MVVM, views/view models, repositories, services, optional domain
layers, separation of concerns, testing architecture components, and current
Flutter-team architecture priorities.

## Dart Style And Package Boundaries

- Effective Dart: https://dart.dev/effective-dart
- Effective Dart design guide: https://dart.dev/effective-dart/design
- Package layout conventions: https://dart.dev/tools/pub/package-layout

Use these for naming, API design, `lib/src` boundaries, public package surface,
import hygiene, package layout, and when to treat a source file as public API.

## Performance, Rendering, And DevTools

- Flutter performance best practices: https://docs.flutter.dev/perf/best-practices
- Flutter performance profiling: https://docs.flutter.dev/perf/ui-performance
- Flutter architectural overview: https://docs.flutter.dev/resources/architectural-overview

Use these for profile-mode expectations, real-device profiling, frame budgets,
expensive `build`, layout, paint, opacity, clipping, `saveLayer`, intrinsic
passes, platform channels, platform views, and rendering architecture.

## Testing

- Testing overview: https://docs.flutter.dev/testing/overview
- Widget testing introduction: https://docs.flutter.dev/cookbook/testing/widget/introduction
- Integration testing: https://docs.flutter.dev/testing/integration-tests

Use these for unit/widget/integration boundaries, `flutter_test`,
`WidgetTester`, finders, `integration_test`, test placement, and device-backed
integration-test expectations.

## Accessibility And Internationalization

- Accessibility: https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility
- Internationalization: https://docs.flutter.dev/ui/internationalization

Use these for TalkBack, VoiceOver, semantics, large text, contrast, tappable
targets, recoverable errors, localized messages, pluralization, formatting,
locale handling, and RTL layout.

## Platform Integration

- Android platform views: https://docs.flutter.dev/platform-integration/android/platform-views
- Flutter architectural overview: https://docs.flutter.dev/resources/architectural-overview

Use these for platform channels, native views, hybrid composition,
texture-layer composition, transform/support tradeoffs, accessibility caveats,
and when to prefer a texture or screenshot during animated transitions.

## State Management Packages

- Riverpod docs: https://riverpod.dev/
- Riverpod `(Async)NotifierProvider`: https://riverpod.dev/docs/providers/notifier_provider
- Riverpod migration from `StateNotifier`: https://riverpod.dev/docs/migration/from_state_notifier

Use these for current Riverpod provider patterns, `Notifier`,
`AsyncNotifier`, loading/error handling, testing posture, and migration advice.
For Bloc, Provider, Redux, GetX, or other state libraries, check the package's
own current docs before making package-specific API claims.

## Flame And Game Libraries

- FlameGame: https://docs.flame-engine.org/latest/flame/game.html
- Camera and World: https://docs.flame-engine.org/latest/flame/camera.html
- Flame background music: https://docs.flame-engine.org/latest/bridge_packages/flame_audio/bgm.html
- Flame Forge2D: https://docs.flame-engine.org/latest/bridge_packages/flame_forge2d/forge2d.html

Use these for game-loop ownership, `FlameGame`, component updates/renders,
`World`, `CameraComponent`, overlays/HUD boundaries, background music lifecycle,
and Forge2D physics integration.

## Security And Platform Policy

For secrets, attestation, platform storage, network policy, signing, Android,
and iOS release behavior, prefer current official Flutter, Android, and Apple
docs before making policy claims. These areas change more often than general
Flutter architecture guidance.
