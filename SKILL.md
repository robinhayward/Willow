---
name: create-modular-ios-app
description: Create a new modular SwiftUI iOS app with XcodeGen, Swift 6, separate Core, Design, and Features packages, a Design catalogue target, Local/Dev/Test/Prod schemes, xcconfig files, and command-line tests. Use when starting an iOS app or recreating the Digbi-style iOS project foundation. Do not use for adding a feature to an existing app.
---

# Create Modular iOS App

1. Read `references/architecture.md`.
2. Check that `xcodegen`, `swift`, `xcodebuild`, and `just` are available.
3. Collect only missing required values. Never invent production hosts or secrets.
4. Run `python3 scripts/create_app.py` with every required argument.
5. Run `just gate` from the generated app.
6. Report the generated `.xcodeproj` path and any check that did not pass.

Run `python3 scripts/create_app.py --help` for the exact arguments.
