# __APP__

Modular Swift 6 starter with separate Core, Design, and Features packages.

Open `__APP__.xcworkspace`; it contains the app project and the three local
packages so all of them are editable in one window.

Run `just gate` for lint, package tests, and generic simulator builds of the
app, UI tests, and Design catalogue. `just format` fixes lint style issues. Regenerate the
Xcode project after editing `project.yml` with `just generate`.

Dev, Staging, and Prod values live in `Configs/`. These files contain
public environment endpoints only; never store secrets in the app bundle.

Concurrency uses Swift 6 with Approachable Concurrency. The app, Design, and
Features default to the main actor; Core stays nonisolated.

Before the first App Store upload:

- Replace the placeholder `App/Resources/AppIcon.icon` using Icon Composer.
- Declare every required-reason API in `App/Resources/PrivacyInfo.xcprivacy`.
  For example, UserDefaults needs reason `CA92.1`. Missing declarations fail
  upload with ITMS-91053.
- `ITSAppUsesNonExemptEncryption` is false, which covers HTTPS through
  URLSession. Change it if the app ships its own cryptography.
