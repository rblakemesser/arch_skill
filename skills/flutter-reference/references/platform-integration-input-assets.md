# Platform Integration, Input, And Assets

Use this reference when deciding between platform channels, Pigeon, FFI, platform views, textures, native composition, input routing, focus, gestures, semantic custom controls, assets, image variants, and cache discipline.

## Platform Integration, iOS And Android Specifics, Input, Assets, And Textures

### Platform integration, iOS and Android specifics, input, assets, and textures

Flutter’s platform integration story gives you three main escape hatches: platform channels for ordinary host APIs, FFI for native C/C++ bindings, and platform views or textures for embedding native-rendered content. Architecture reviews get better once those choices are treated as separate tools rather than as one generic “native bridge.”

For app behavior and aesthetics, Flutter supports platform-adaptive navigation and also provides a full Cupertino library for iOS-style widgets. The right standard is not “always make iOS look different” or “always force one brand UI.” The right standard is to preserve native interaction expectations when they materially affect usability, especially transitions, navigation, text editing, focus, haptics, and platform-specific capabilities. Flutter’s adaptive docs and Cupertino catalog both support that approach.

#### Platform channels, FFI, and views

Platform channels are appropriate for host APIs with message-like interactions, such as battery, permissions, sensors, or OS facilities. FFI is more appropriate when binding to native libraries or compute-heavy code where marshaling through repeated channel calls would be awkward. The official docs cover both patterns directly.

Platform views are where many mobile performance surprises happen. On Android, the official docs now describe multiple platform-view implementations with explicit trade-offs. Hybrid composition gives the best performance and fidelity for Android views themselves, but Flutter performance suffers, FPS can drop, and some transformations fail. Texture-layer composition gives better Flutter rendering performance and supports transforms correctly, but fast-scrolling native views such as web views can be janky, `SurfaceView` content may be forced into a virtual display with accessibility consequences, and text magnification has caveats. On iOS, platform views use hybrid composition, and the docs explicitly recommend a placeholder texture or screenshot while a Dart-side animation is running if native-view composition becomes too slow.

The architecture implication is strong: if a native view must remain live and interactive, place it in as static a surrounding scene as possible. If you need fancy transforms, animated overlays, or particle-heavy content around it, consider freezing or snapshotting it to a texture during transitions. Flutter’s docs basically say that, just in API language rather than review language.

#### Gestures, touch, focus, and input routing

Flutter resolves competing gesture recognizers using the gesture arena. If more than one recognizer participates for a pointer, recognizers can eliminate themselves until one wins. Use `GestureDetector` for high-level gestures, `Listener` for low-level raw pointer events, `MouseRegion` for hover, and `FocusableActionDetector` when a custom control must participate correctly in focus, hover, actions, and keyboard bindings.

For custom tappable text or controls, prefer semantic widgets when possible. The `Text` docs specifically suggest `TextButton` or at least `InkWell` in Material apps rather than manually wiring a `GestureDetector` around text. More broadly, the `Semantics` widget is how you annotate important meaning for TalkBack, VoiceOver, and other assistive technologies. That matters even more in games, where custom-rendered controls otherwise vanish from the accessibility tree.

#### Assets, images, and textures

Flutter bundles assets via `pubspec.yaml`, supports resolution-aware variants, and exposes assets asynchronously through asset bundles. That should shape code review in two ways. First, asset declarations should be explicit and organized by feature or asset class rather than sprayed across the project. Second, resolution-specific image variants are worth using intentionally on mobile to avoid over-large decodes and blurry scaling.

Use `precacheImage()` for deliberate warm-up of critical images, and watch the image cache when diagnosing memory growth. If a view or game scene loads many large images and never releases them, the issue is often a live image reference or an over-generous cache policy rather than “GC is broken.” DevTools Memory plus the image-cache APIs are the right debugging stack there.

## Typed Platform Boundaries In Review

#### Stringly typed platform channels mixed into UI code

Flutter’s platform-integration docs explicitly recommend Pigeon for type-safe platform code generation, and the platform-channels guide also emphasizes thread constraints. Hand-written string channel names sprinkled through widgets invite breakage and make reviews much harder. Keep platform interop in a package or service boundary, not in UI code.

**Bad**

```dart
class CameraButton extends StatelessWidget {
  static const channel = MethodChannel('camera_magic');

  const CameraButton({super.key});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () async {
        final result = await channel.invokeMethod('capturePhoto');
        debugPrint('$result');
      },
      child: const Text('Capture'),
    );
  }
}
```

**Better**

```dart
abstract interface class CameraGateway {
  Future<PhotoResult> capturePhoto();
}

final class NativeCameraGateway implements CameraGateway {
  NativeCameraGateway(this._api);

  final CameraApi _api; // generated by Pigeon

  @override
  Future<PhotoResult> capturePhoto() async {
    final dto = await _api.capturePhoto();
    return PhotoResult(path: dto.path, width: dto.width, height: dto.height);
  }
}
```
