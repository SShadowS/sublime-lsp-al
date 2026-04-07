from __future__ import annotations

from LSP.plugin import AbstractPlugin
from LSP.plugin import register_plugin
from LSP.plugin import unregister_plugin
import os
import platform
import sublime
import sublime_plugin
import tarfile
import tempfile
import urllib.request
import zipfile

SESSION_NAME = "AL"
TAG = "v1.9.9"
REPO = "SShadowS/al-lsp-for-agents"
GITHUB_RELEASE_URL = "https://github.com/{repo}/releases/download/{tag}/{asset}"


def _platform_asset() -> str:
    system = platform.system()
    if system == "Windows":
        return "al-lsp-wrapper-windows-x64.zip"
    elif system == "Linux":
        return "al-lsp-wrapper-linux-x64.tar.gz"
    else:
        raise RuntimeError("Unsupported platform: " + system)


def _wrapper_name() -> str:
    if platform.system() == "Windows":
        return "al-lsp-wrapper.exe"
    return "al-lsp-wrapper"


class LSPAL(AbstractPlugin):
    package_name = "LSP-AL"

    @classmethod
    def name(cls) -> str:
        return SESSION_NAME

    @classmethod
    def basedir(cls) -> str:
        return os.path.join(cls.storage_path(), "server")

    @classmethod
    def version_file(cls) -> str:
        return os.path.join(cls.basedir(), "VERSION")

    @classmethod
    def wrapper_path(cls) -> str:
        return os.path.join(cls.basedir(), _wrapper_name())

    @classmethod
    def needs_update_or_installation(cls) -> bool:
        version_file = cls.version_file()
        if not os.path.isfile(cls.wrapper_path()):
            return True
        if not os.path.isfile(version_file):
            return True
        with open(version_file, "r") as f:
            return f.read().strip() != TAG

    @classmethod
    def install_or_update(cls) -> None:
        basedir = cls.basedir()
        os.makedirs(basedir, exist_ok=True)

        asset = _platform_asset()
        url = GITHUB_RELEASE_URL.format(repo=REPO, tag=TAG, asset=asset)

        sublime.status_message("LSP-AL: Downloading {}...".format(TAG))

        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = os.path.join(tmpdir, asset)
            urllib.request.urlretrieve(url, archive_path)

            if asset.endswith(".zip"):
                with zipfile.ZipFile(archive_path, "r") as zf:
                    zf.extractall(basedir)
            elif asset.endswith(".tar.gz"):
                with tarfile.open(archive_path, "r:gz") as tf:
                    tf.extractall(basedir)

            # Make executable on Unix
            wrapper = cls.wrapper_path()
            if platform.system() != "Windows" and os.path.isfile(wrapper):
                os.chmod(wrapper, 0o755)
                # Also make al-call-hierarchy executable if present
                call_hierarchy = os.path.join(basedir, "al-call-hierarchy")
                if os.path.isfile(call_hierarchy):
                    os.chmod(call_hierarchy, 0o755)

        with open(cls.version_file(), "w") as f:
            f.write(TAG)

        sublime.status_message("LSP-AL: Installed {}".format(TAG))

    @classmethod
    def additional_variables(cls) -> dict[str, str] | None:
        settings = sublime.load_settings("LSP-AL.sublime-settings")
        channel = settings.get("al_extension_channel", "release")
        return {
            "wrapper_path": cls.wrapper_path(),
            "al_extension_channel": channel,
        }


class LspAlSwitchChannelCommand(sublime_plugin.WindowCommand):
    """Switch between release and prerelease AL extension channels."""

    def run(self) -> None:
        settings = sublime.load_settings("LSP-AL.sublime-settings")
        current = settings.get("al_extension_channel", "release")
        new_channel = "prerelease" if current == "release" else "release"
        settings.set("al_extension_channel", new_channel)
        sublime.save_settings("LSP-AL.sublime-settings")
        sublime.status_message("LSP-AL: Switched to {} channel — restart language server to apply".format(new_channel))


class LspAlForceUpdateCommand(sublime_plugin.WindowCommand):
    """Force update the AL extension."""

    def run(self) -> None:
        sublime.status_message("LSP-AL: Restarting server with force update...")
        self.window.run_command("lsp_restart_server", {"config_name": SESSION_NAME})


def plugin_loaded() -> None:
    register_plugin(LSPAL)


def plugin_unloaded() -> None:
    unregister_plugin(LSPAL)
