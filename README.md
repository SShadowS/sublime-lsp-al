# LSP-AL

AL language server support for [Sublime Text](https://www.sublimetext.com/) via [LSP](https://packagecontrol.io/packages/LSP).

[![GitHub release](https://img.shields.io/github/v/release/SShadowS/al-lsp-for-agents)](https://github.com/SShadowS/al-lsp-for-agents/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Provides code intelligence for AL (Microsoft Dynamics 365 Business Central) — no VS Code installation required. The wrapper binary and the Microsoft AL Language extension are both downloaded and managed automatically.

## Features

| Feature | Source |
|---------|--------|
| Go to Definition | AL Language Server |
| Hover information | AL Language Server + al-call-hierarchy |
| Find References | AL Language Server |
| Document / Workspace Symbols | AL Language Server |
| Diagnostics | AL Language Server + al-call-hierarchy |
| Call Hierarchy | al-call-hierarchy |
| Code Lens (reference counts) | al-call-hierarchy |

## Prerequisites

- [Sublime Text 4](https://www.sublimetext.com/)
- [LSP](https://packagecontrol.io/packages/LSP) package
- [AL](https://packagecontrol.io/packages/AL) syntax package

## Installation

1. Install the `LSP` and `AL` packages via Package Control.
2. Install this package (via Package Control or clone into your `Packages` directory).
3. Open an AL project (a folder containing `app.json`) and start editing.

On first startup, the [al-lsp-wrapper](https://github.com/SShadowS/al-lsp-for-agents) binary and the Microsoft AL Language extension are downloaded automatically. No manual setup needed.

## AL Extension Management

The wrapper downloads and manages the Microsoft AL Language extension from the VS Code Marketplace. The extension is stored in `~/.al-language-server/extensions/` and shared across tools.

| Behavior | Details |
|----------|---------|
| **First run** | Downloads the AL extension (blocking, ~30-60s) |
| **Daily check** | Background check for new versions, downloads if available |
| **Channel** | Release (default) or Prerelease |
| **Storage** | `~/.al-language-server/extensions/{channel}/` |

### Command Palette

| Command | Description |
|---------|-------------|
| `LSP-AL: Switch Release Channel` | Toggle between release and prerelease AL extension |
| `LSP-AL: Force Update AL Extension` | Restart server and check for updates immediately |

### Settings

In `LSP-AL.sublime-settings`:

```json
{
    "al_extension_channel": "release"
}
```

Set to `"prerelease"` to use pre-release versions of the AL Language extension.

## How It Works

```
Sublime Text
  |
  v  (stdio)
al-lsp-wrapper (Go)
  |-- Microsoft AL Language Server (auto-downloaded)
  |-- al-call-hierarchy (tree-sitter-based analysis)
```

The wrapper proxies between Sublime Text and the AL Language Server, adding capabilities from [al-call-hierarchy](https://github.com/SShadowS/al-call-hierarchy) (call hierarchy, code lens, enriched hover, code quality diagnostics).

## Key Files

| File | Purpose |
|------|---------|
| `plugin.py` | LSP plugin: binary management, settings, commands |
| `LSP-AL.sublime-settings` | Server configuration and channel selection |
| `Default.sublime-commands` | Command palette entries |

---

**Author**: Torben Leth (sshadows@sshadows.dk)
**License**: MIT (see [LICENSE](LICENSE))
