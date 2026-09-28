---
name: create-modular-ios-app
description: Create a new modular SwiftUI iOS app with Xcode 27, XcodeGen, Swift 6 main-actor-by-default concurrency, separate Core, Design, and Features packages, a Design catalogue target, Dev/Staging/Prod schemes, xcconfig files, and command-line tests, all wrapped in an Xcode workspace. Use when starting a new modular iOS app. Do not use for adding a feature to an existing app.
---

# Create Modular iOS App

## Baseline

Created 2026-07-26. Last verified 2026-09-28 against:

- Xcode 27.0 (27A266a), iOS 27.0 SDK
- Swift 6.4 toolchain, Swift 6 language mode, package tools-version 6.2
- XcodeGen 2.46.0

Keep this block in sync with the README's Baseline section.

## Steps

1. Read `references/architecture.md`.
2. Check that `xcodebuild -version` reports Xcode 27 or later, and that `xcodegen`,
   `swift`, and `just` are available. Compare the installed Xcode, iOS SDK
   (`xcrun --sdk iphoneos --show-sdk-version`), Swift and XcodeGen versions with
   the Baseline.
3. Collect only missing required values. Never invent production hosts or secrets.
4. Run `python3 scripts/create_app.py` with every required argument.
5. Run `just gate` from the generated app.
6. Report the generated `.xcworkspace` path and any check that did not pass.
7. If Apple's exported skills or the Swift plugins are missing from your skill
   list, point the person to `references/agent-tooling.md`. Never install
   plugins for them or add them to a checked-in `.claude/settings.json`.

Run `python3 scripts/create_app.py --help` for the exact arguments.

## Self-heal when the toolchain moves on

If step 2 found a newer version than the Baseline, or `just gate` failed
because of the toolchain, do this after reporting the app:

1. Read the matching `*-whats-new-*` skills and re-export Apple's skills
   (see `references/agent-tooling.md`) for deprecations and new defaults.
2. Propose the template changes to the person. Once they agree, edit
   `assets/template`, then run `python3 -m unittest scripts/test_create_app.py` and
   `just gate` on a freshly generated app until both pass without warnings.
3. Update the Baseline here and in `README.md`: the new versions, and today's
   date as "Last verified". Also refresh the version wording in the
   frontmatter description and `references/`.

Never raise the Baseline without a passing gate.
