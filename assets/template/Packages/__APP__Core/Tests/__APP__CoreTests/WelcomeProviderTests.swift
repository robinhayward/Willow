import Testing
@testable import __APP__Core

@Test
func liveProviderBuildsWelcomeMessage() async {
    let provider = LiveWelcomeProvider(appName: "Sample", environmentName: "Local")

    #expect(await provider.message() == "Sample is ready for Local.")
}
