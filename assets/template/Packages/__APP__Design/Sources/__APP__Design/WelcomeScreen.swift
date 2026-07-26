import SwiftUI

public struct WelcomeScreen: View {
    public let presentation: WelcomePresentation
    public let onRefresh: () -> Void

    public init(
        presentation: WelcomePresentation,
        onRefresh: @escaping () -> Void
    ) {
        self.presentation = presentation
        self.onRefresh = onRefresh
    }

    public var body: some View {
        VStack(spacing: 16) {
            Text("welcome.title", bundle: .module)
                .font(.largeTitle.bold())
            Text(presentation.appName)
                .font(.title2)
            Text(presentation.message)
            Text(presentation.environmentName)
                .foregroundStyle(.secondary)
            Button(action: onRefresh) {
                Text("welcome.refresh", bundle: .module)
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}

#Preview("Loading") {
    WelcomeScreen(
        presentation: WelcomePresentation(
            appName: "Sample",
            environmentName: "Local",
            message: "Loading…"
        ),
        onRefresh: {}
    )
}

#Preview("Ready") {
    WelcomeScreen(
        presentation: WelcomePresentation(
            appName: "Sample",
            environmentName: "Dev",
            message: "Sample is ready for Dev."
        ),
        onRefresh: {}
    )
}
