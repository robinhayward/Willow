import Foundation

struct AppConfiguration {
    let environmentName: String
    let apiBaseURL: String
    let webHost: String

    init(bundle: Bundle = .main) {
        environmentName = Self.requiredString("APP_ENVIRONMENT", in: bundle)
        apiBaseURL = Self.requiredString("API_BASE_URL", in: bundle)
        webHost = Self.requiredString("WEB_HOST", in: bundle)
    }

    private static func requiredString(_ key: String, in bundle: Bundle) -> String {
        guard let value = bundle.object(forInfoDictionaryKey: key) as? String else {
            preconditionFailure("Missing generated build setting: \(key)")
        }
        return value
    }
}
