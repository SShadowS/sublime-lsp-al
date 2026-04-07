# LSP-AL

AL language server support for Sublime Text via [LSP](https://packagecontrol.io/packages/LSP).

Provides code intelligence for AL (Microsoft Dynamics 365 Business Central) including go-to-definition, hover, references, and more.

## Prerequisites

- [Sublime Text](https://www.sublimetext.com/) 4
- [LSP](https://packagecontrol.io/packages/LSP) package
- [AL](https://packagecontrol.io/packages/AL) syntax package
- [AL Language extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-dynamics-smb.al) — the language server binary is auto-discovered from here

## Installation

1. Install the `LSP` and `AL` packages via Package Control.
2. Install this package (via Package Control or clone into your `Packages` directory).
3. The [al-lsp-wrapper](https://github.com/SShadowS/al-lsp-for-agents) binary is downloaded automatically on first use.
4. Open an AL project (a folder containing `app.json`) and start editing.

## Features

All features provided by the Microsoft AL Language Server:

- Go to Definition / Implementation
- Hover information
- Find References
- Document / Workspace Symbols
- Diagnostics
- Code Actions
- Call Hierarchy
