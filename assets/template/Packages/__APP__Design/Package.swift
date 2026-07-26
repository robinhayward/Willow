// swift-tools-version: 6.0

import PackageDescription

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
            swiftSettings: [.swiftLanguageMode(.v6)]
        ),
        .testTarget(
            name: "__APP__DesignTests",
            dependencies: ["__APP__Design"],
            swiftSettings: [.swiftLanguageMode(.v6)]
        ),
    ]
)
