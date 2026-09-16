---
name: create-modular-ios-app
description: Create a new modular SwiftUI iOS app with Xcode 27, XcodeGen, Swift 6 main-actor-by-default concurrency, separate Core, Design, and Features packages, a Design catalogue target, Dev/Staging/Prod schemes, xcconfig files, and command-line tests, all wrapped in an Xcode workspace. Use when starting a new modular iOS app. Do not use for adding a feature to an existing app.
---

# Create Modular iOS App

1. Read `references/architecture.md`.
2. Check that `xcodebuild -version` reports Xcode 27 or later, and that `xcodegen`,
   `swift`, and `just` are available.
3. Collect only missing required values. Never invent production hosts or secrets.
4. Run `python3 scripts/create_app.py` with every required argument.
5. Run `just gate` from the generated app.
6. Report the generated `.xcworkspace` path and any check that did not pass.

Run `python3 scripts/create_app.py --help` for the exact arguments.
