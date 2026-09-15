// swift-tools-version: 6.2

import PackageDescription

let swiftSettings: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
    .enableUpcomingFeature("MemberImportVisibility"),
    .defaultIsolation(MainActor.self),
]

let package = Package(
    name: "__APP__Features",
    platforms: [
        .iOS("__DEPLOYMENT_TARGET__"),
        .macOS(.v14),
    ],
    products: [
        .library(name: "__APP__Features", targets: ["__APP__Features"])
    ],
    dependencies: [
        .package(path: "../__APP__Core"),
        .package(path: "../__APP__Design"),
    ],
    targets: [
        .target(
            name: "__APP__Features",
            dependencies: ["__APP__Core", "__APP__Design"],
            swiftSettings: swiftSettings
        ),
        .testTarget(
            name: "__APP__FeaturesTests",
            dependencies: ["__APP__Features", "__APP__Core"],
            swiftSettings: swiftSettings
        ),
    ]
)
