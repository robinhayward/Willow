import Testing
import __APP__Core
@testable import __APP__Features

private struct StubWelcomeProvider: WelcomeProviding {
    func message() async -> String {
        "Ready"
    }
}

@Test
@MainActor
func loadPublishesProviderMessage() async {
    let feature = WelcomeFeature(provider: StubWelcomeProvider())

    await feature.load()

    #expect(feature.message == "Ready")
}
