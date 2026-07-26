import XCTest

final class AppUITests: XCTestCase {
    @MainActor
    func testWelcomeScreenAppears() {
        let app = XCUIApplication()

        app.launch()

        XCTAssertTrue(app.staticTexts["Welcome"].waitForExistence(timeout: 5))
        XCTAssertTrue(app.staticTexts["__APP__"].exists)
    }
}
