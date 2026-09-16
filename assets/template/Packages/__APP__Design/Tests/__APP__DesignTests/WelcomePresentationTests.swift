import Testing
@testable import __APP__Design

@Test
func presentationPreservesValues() {
    let presentation = WelcomePresentation(
        appName: "Sample",
        environmentName: "Dev",
        message: "Ready"
    )

    #expect(presentation.appName == "Sample")
    #expect(presentation.environmentName == "Dev")
    #expect(presentation.message == "Ready")
}
