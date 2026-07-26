public struct WelcomePresentation: Equatable, Sendable {
    public let appName: String
    public let environmentName: String
    public let message: String

    public init(appName: String, environmentName: String, message: String) {
        self.appName = appName
        self.environmentName = environmentName
        self.message = message
    }
}
