# Create Modular iOS App

A reusable Codex and Claude skill for creating modular SwiftUI apps with
XcodeGen and Swift 6. It generates a ready-to-open Xcode project without Tuist.

## What it creates

- Separate `<App>Core`, `<App>Design`, and `<App>Features` Swift packages
- A small app-composition target and a fast Design catalogue target
- Local, Dev, Test, and Prod configurations with matching schemes
- Environment-specific xcconfig files
- Package tests, an app UI smoke test, previews, privacy metadata, localization,
  and a `just gate` command

## Requirements

- macOS with Xcode and Swift 6
- Python 3
- [XcodeGen](https://github.com/yonaskolb/XcodeGen)
- [just](https://github.com/casey/just)

Install the command-line dependencies with Homebrew:

```sh
brew install xcodegen just
```

## Install the skill

Clone the repository somewhere permanent:

```sh
git clone <repository-url> ~/Developer/create-modular-ios-app
```

Link it into Codex, Claude, or both:

```sh
mkdir -p ~/.codex/skills ~/.claude/skills
ln -sfn ~/Developer/create-modular-ios-app ~/.codex/skills/create-modular-ios-app
ln -sfn ~/Developer/create-modular-ios-app ~/.claude/skills/create-modular-ios-app
```

Start a new Codex or Claude session so it discovers the skill.

## Use it

Ask your agent:

> Use the create-modular-ios-app skill to create a new app named Acme.

The agent will collect the bundle ID, destination, deployment target, and
Local/Dev/Test/Prod endpoints it still needs. It then generates the project,
runs the full gate, and gives you the `.xcodeproj` path to open.

For a fully specified request:

> Use the create-modular-ios-app skill to create Acme in ~/Developer with bundle
> ID com.example.acme and iOS deployment target 26.0. Use
> http://127.0.0.1:8000 and 127.0.0.1 for Local, and ask me for the remaining
> environment endpoints.

## Verify a generated app

From the generated app directory:

```sh
just gate
```

This runs the Core, Design, and Features package tests and builds both the app
and Design catalogue for a generic iOS Simulator. Run `just generate` after
editing `project.yml`.

The starter deliberately includes no placeholder App Icon. Add a real AppIcon
before distributing the app.
