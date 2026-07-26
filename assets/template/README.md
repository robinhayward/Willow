# __APP__

Modular Swift 6 starter with separate Core, Design, and Features packages.

Run `just gate` for package tests and generic simulator builds. Regenerate the
Xcode project after editing `project.yml` with `just generate`.

Local, Dev, Test, and Prod values live in `Configs/`. These files contain
public environment endpoints only; never store secrets in the app bundle.
