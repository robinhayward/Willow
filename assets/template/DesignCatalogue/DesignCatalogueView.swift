import SwiftUI
import __APP__Design

struct DesignCatalogueView: View {
    var body: some View {
        WelcomeScreen(
            presentation: WelcomePresentation(
                appName: "__APP__",
                environmentName: "Catalogue",
                message: "__APP__ is ready."
            ),
            onRefresh: {}
        )
    }
}
