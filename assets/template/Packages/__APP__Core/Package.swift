// swift-tools-version: 6.0

import PackageDescription

let package = Package(
    name: "__APP__Core",
    platforms: [
        .iOS("__DEPLOYMENT_TARGET__"),
        .macOS(.v14),
    ],
    products: [
        .library(name: "__APP__Core", targets: ["__APP__Core"])
    ],
    targets: [
        .target(
            name: "__APP__Core",
            swiftSettings: [.swiftLanguageMode(.v6)]
        ),
        .testTarget(
            name: "__APP__CoreTests",
            dependencies: ["__APP__Core"],
            swiftSettings: [.swiftLanguageMode(.v6)]
        ),
    ]
)
