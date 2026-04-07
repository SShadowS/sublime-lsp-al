# LSP-AL

AL language server support for Sublime Text via [LSP](https://packagecontrol.io/packages/LSP).

Provides code intelligence for AL (Microsoft Dynamics 365 Business Central) including go-to-definition, hover, references, and more.

## Prerequisites

- [Sublime Text](https://www.sublimetext.com/) 4
- [LSP](https://packagecontrol.io/packages/LSP) package
- [AL](https://packagecontrol.io/packages/AL) syntax package

## Installation

1. Install the `LSP` and `AL` packages via Package Control.
2. Install this package (via Package Control or clone into your `Packages` directory).
3. The [al-lsp-wrapper](https://github.com/SShadowS/al-lsp-for-agents) binary is downloaded automatically on first use.
4. On first startup, the Microsoft AL Language extension is downloaded automatically from the VS Code Marketplace. No VS Code installation required.
5. Open an AL project (a folder containing `app.json`) and start editing.

## AL Extension Management

The wrapper automatically downloads and manages the Microsoft AL Language extension. No VS Code installation is needed.

- **Auto-updates**: The wrapper checks for new versions once per day in the background.
- **Switch channel**: Use the command palette (`LSP-AL: Switch Release Channel`) to toggle between the release and prerelease versions of the AL extension.
- **Force update**: Use `LSP-AL: Force Update AL Extension` from the command palette to restart the server and check for updates immediately.

The extension is stored in `~/.al-language-server/extensions/` and shared across tools.

## Features

All features provided by the Microsoft AL Language Server:

- Go to Definition / Implementation
- Hover information
- Find References
- Document / Workspace Symbols
- Diagnostics
- Code Actions
- Call Hierarchy
