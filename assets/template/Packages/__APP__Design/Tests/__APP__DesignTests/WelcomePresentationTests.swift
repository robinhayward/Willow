import Testing
@testable import __APP__Design

@Test
func presentationPreservesValues() {
    let presentation = WelcomePresentation(
        appName: "Sample",
        environmentName: "Local",
        message: "Ready"
    )

    #expect(presentation.appName == "Sample")
    #expect(presentation.environmentName == "Local")
    #expect(presentation.message == "Ready")
}
