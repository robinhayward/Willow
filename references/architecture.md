| Module | May import | Owns |
| --- | --- | --- |
| `<App>Core` | Foundation | Services, transport, persistence ports, domain models |
| `<App>Design` | SwiftUI, Foundation | Presentation values, reusable UI, complete screens, previews |
| `<App>Features` | Core, Design, SwiftUI, Observation | Feature state and service-to-UI adaptation |
| `<App>` | Core, Features, SwiftUI | Live dependency construction only |
| `<App> Design` | Design, SwiftUI | Fixed catalogue states only |

Customer-visible SwiftUI lives in Design or composes public Design APIs.
Design must never import Core or Features. Prefer initializer injection for
feature-local services. Add app-wide environment dependencies only when
multiple unrelated descendants genuinely share them.

The starter welcome slice is deliberately disposable. New reusable Design APIs
require representative `#Preview` states plus a catalogue entry.

Concurrency is Swift 6 with Approachable Concurrency. The app, Design, and
Features default to `@MainActor`, so never add `@MainActor` there. Core stays
nonisolated and its service types stay `Sendable`. Mark work that must leave
the caller's actor `@concurrent`.
