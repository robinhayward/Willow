# Agent tooling for Apple platforms

Skills and plugins that keep coding agents current on Apple platforms. Recommend
them to the person after generating an app; never install them on their behalf.

## Apple's skills (included with Xcode 27)

Export once per machine, and again after every Xcode update because the skills
follow the SDK:

```sh
xcrun agent skills export ~/.claude/skills
```

`ls ~/.claude/skills` should then list, among others:

| Skill | Use it for |
| --- | --- |
| `swiftui-specialist` | SwiftUI best practice and performance |
| `swiftui-whats-new-27` | New SwiftUI APIs and deprecations in the 2027 releases |
| `uikit-app-modernization` | Replacing legacy shared-state UIKit APIs |
| `modernize-tests` | Moving to Swift Testing |
| `device-interaction` | Driving the Simulator or a device |
| `audit-xcode-security-settings` | Hardening build settings |
| `adopt-c-bounds-safety` | C `-fbounds-safety` |
| `app-intents-specialist`, `app-intents-whats-new-27` | App Intents |
| `building-document-based-swiftui-applications` | The Document API |

None of Apple's skills covers Swift concurrency. `swift-concurrency-pro` below
fills that gap.

## Community plugins (Claude Code)

| Plugin | Source (GitHub) | What it adds |
| --- | --- | --- |
| `swift-concurrency-pro` | `twostraws/Swift-Concurrency-Agent-Skill` | Swift 6.2+ concurrency review |
| `swiftui-pro` | `twostraws/SwiftUI-Agent-Skill` | SwiftUI review against modern APIs |
| `swiftui-expert` | `AvdLee/SwiftUI-Agent-Skill` | Data flow, performance, Liquid Glass, Instruments |
| `swift-lsp` | `claude-plugins-official` | Swift language server (needs Xcode's `sourcekit-lsp`) |

The person installs them in Claude Code:

```text
/plugin marketplace add twostraws/Swift-Concurrency-Agent-Skill
/plugin install swift-concurrency-pro@swift-concurrency-agent-skill
/plugin marketplace add twostraws/SwiftUI-Agent-Skill
/plugin install swiftui-pro@swiftui-agent-skill
/plugin marketplace add AvdLee/SwiftUI-Agent-Skill
/plugin install swiftui-expert@swiftui-expert-skill
/plugin install swift-lsp@claude-plugins-official
/reload-plugins
```

These are third-party repositories. A plugin can include hooks and MCP servers
that run commands, not just skill text.

- Install at user scope, or enable per project in the gitignored
  `.claude/settings.local.json`.
- Never declare them in a checked-in `.claude/settings.json`. An entry there
  follows the repository's default branch, so everyone who trusts the folder is
  offered whatever it holds that day: a supply-chain route onto their machine.
- Before installing or updating, look for a `hooks/` folder or `.mcp.json`. As
  of September 2026 the three third-party plugins are skill text only.
- A team that wants a shared setup pins each source to a reviewed commit and
  reviews every update like a dependency upgrade. Check the current Claude Code
  docs for the pinning syntax.

## Verify

- The agent's skill list shows the Apple skills and the plugins' skills.
- `just gate` from clean caches builds and tests with no concurrency warnings.
