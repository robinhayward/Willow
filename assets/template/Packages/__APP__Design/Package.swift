// swift-tools-version: 6.2

import PackageDescription

let swiftSettings: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
    .enableUpcomingFeature("MemberImportVisibility"),
    .defaultIsolation(MainActor.self),
]

let package = Package(
    name: "__APP__Design",
    platforms: [
        .iOS("__DEPLOYMENT_TARGET__"),
        .macOS(.v14),
    ],
    products: [
        .library(name: "__APP__Design", targets: ["__APP__Design"])
    ],
    targets: [
        .target(
            name: "__APP__Design",
            resources: [.process("Resources")],
            swiftSettings: swiftSettings
        ),
        .testTarget(
            name: "__APP__DesignTests",
            dependencies: ["__APP__Design"],
            swiftSettings: swiftSettings
        ),
    ]
)
