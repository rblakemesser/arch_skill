# Accessibility, Localization, And Security

Use this reference when reviewing screen-reader support, semantic labels, large text, RTL, localization readiness, secrets, obfuscation limits, secure storage, transport policy, app signing, or attestation.

## Accessibility, Localization, And Security Defaults

### Accessibility, localization, and security

Accessibility is not a post-processing pass. Flutter’s own accessibility checklist includes screen-reader testing, minimum contrast guidance, avoiding unexpected context changes, tappable targets of at least **48×48**, and making errors recoverable or correctable where possible. Flutter explicitly recommends testing with **TalkBack** on Android and **VoiceOver** on iOS. Android’s accessibility guidance adds automated tools such as Accessibility Scanner, Android Studio checks, and Google Play pre-launch accessibility reports. Apple’s current accessibility guidance also emphasizes VoiceOver, support for larger text sizes, flexible layouts, and responding appropriately to Reduce Motion.

That means every review should ask:

* Does every interactive element have correct semantics/labeling?
* Does the screen still work at large text sizes?
* Does the layout still make sense in portrait and landscape?
* Does the app avoid meaning conveyed only by color?
* Are custom gestures exposed through accessible alternatives when possible?

Localization should start at day one. Flutter’s internationalization docs are unambiguous: if your app may be used by people speaking another language, you need to write it so text and layouts can be localized per language/locale. Flutter’s localization support covers `MaterialApp` and `CupertinoApp`, and widgets should adapt for both messages and correct left-to-right/right-to-left layout.

In practice:

* Never hard-code user-facing strings deep in widgets.
* Localize format-sensitive content such as dates, times, numbers, pluralization, and currency.
* Test large text and RTL early, not after design freeze.
* Avoid layout assumptions that depend on English text length.

Security defaults should be equally conservative. Flutter’s obfuscation docs explicitly warn that storing secrets in an app is poor security practice, and that obfuscation does **not** encrypt resources or truly protect against reverse engineering. On Android, prefer HTTPS/TLS and enforce policy through **network security configuration**; cleartext traffic defaults changed over Android versions and is disabled by default starting with Android 9. For sensitive keys, use **Android Keystore**. On Apple platforms, **App Transport Security** improves privacy and data integrity, and **Keychain Services** is the standard encrypted store for small sensitive items. All release artifacts must be signed. For high-risk server actions, use platform attestation mechanisms such as **Play Integrity API** and **App Attest/DeviceCheck**.

## Secrets And Client-Side Security Anti-Patterns

#### Storing secrets in the app and calling it “secured”

Flutter’s own docs explicitly warn that putting secrets in the app is poor security practice, and that obfuscation only obscures symbol names. Store user/device tokens with the platform’s secure storage primitives where necessary, but keep real secrets server-side.

**Bad**

```dart
const stripeSecretKey = 'sk_live_...';
const internalAdminApiKey = 'prod-...';
```

**Better**

```dart
// client gets a short-lived token or signed request from backend
final publishableKey = const String.fromEnvironment('STRIPE_PUBLISHABLE_KEY');
```
