public protocol WelcomeProviding: Sendable {
    func message() async -> String
}

public struct LiveWelcomeProvider: WelcomeProviding {
    private let appName: String
    private let environmentName: String

    public init(appName: String, environmentName: String) {
        self.appName = appName
        self.environmentName = environmentName
    }

    public func message() async -> String {
        "\(appName) is ready for \(environmentName)."
    }
}
