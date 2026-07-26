import SwiftUI
import __APP__Core
import __APP__Design

public struct RootFeatureView: View {
    private let appName: String
    private let environmentName: String
    @State private var feature: WelcomeFeature

    @MainActor
    public init(
        appName: String,
        environmentName: String,
        provider: any WelcomeProviding
    ) {
        self.appName = appName
        self.environmentName = environmentName
        _feature = State(initialValue: WelcomeFeature(provider: provider))
    }

    public var body: some View {
        WelcomeScreen(
            presentation: presentation,
            onRefresh: refresh
        )
        .task {
            await feature.load()
        }
    }

    private var presentation: WelcomePresentation {
        WelcomePresentation(
            appName: appName,
            environmentName: environmentName,
            message: feature.message
        )
    }

    private func refresh() {
        Task {
            await feature.load()
        }
    }
}
