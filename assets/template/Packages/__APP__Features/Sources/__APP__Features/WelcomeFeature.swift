import Observation
import __APP__Core

@MainActor
@Observable
public final class WelcomeFeature {
    public private(set) var message = "Loading…"
    private let provider: any WelcomeProviding

    public init(provider: any WelcomeProviding) {
        self.provider = provider
    }

    public func load() async {
        message = await provider.message()
    }
}
