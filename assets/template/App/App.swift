import SwiftUI
import __APP__Core
import __APP__Features

@main
struct __APP__App: App {
    private let configuration: AppConfiguration
    private let provider: LiveWelcomeProvider

    init() {
        let configuration = AppConfiguration()
        self.configuration = configuration
        provider = LiveWelcomeProvider(
            appName: "__APP__",
            environmentName: configuration.environmentName
        )
    }

    var body: some Scene {
        WindowGroup {
            RootFeatureView(
                appName: "__APP__",
                environmentName: configuration.environmentName,
                provider: provider
            )
        }
    }
}
