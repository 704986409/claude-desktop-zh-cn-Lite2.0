#!/usr/bin/env python3
"""Locate Claude Desktop install dirs (Store / winget EXE) and locale configs."""
from __future__ import annotations

import json
import os
from pathlib import Path


def windowsapps_version_key(app_dir: Path) -> tuple[int, ...]:
    parts = app_dir.parent.name.split("_")
    if len(parts) < 2:
        return ()
    version: list[int] = []
    for part in parts[1].split("."):
        try:
            version.append(int(part))
        except ValueError:
            version.append(0)
    return tuple(version)


def find_claude_app_dir() -> Path | None:
    windowsapps = Path(r"C:\Program Files\WindowsApps")
    windows_candidates: list[Path] = []
    if windowsapps.exists():
        windows_candidates.extend(
            path.parent.parent
            for path in windowsapps.glob("Claude_*_x64__*/app/resources/en-US.json")
            if path.is_file()
        )
    if windows_candidates:
        return sorted(
            set(windows_candidates),
            key=lambda path: (windowsapps_version_key(path), str(path)),
            reverse=True,
        )[0]

    localappdata = os.environ.get("LOCALAPPDATA")
    if not localappdata:
        return None
    anthropic = Path(localappdata) / "AnthropicClaude"
    if not anthropic.exists():
        return None
    local_resource_files = [
        anthropic / "resources" / "en-US.json",
        anthropic / "app" / "resources" / "en-US.json",
        *anthropic.glob("app*/resources/en-US.json"),
    ]
    local_candidates = [path.parent.parent for path in local_resource_files if path.is_file()]
    if not local_candidates:
        return None
    return sorted(
        set(local_candidates),
        key=lambda path: (path.stat().st_mtime if path.exists() else 0, str(path)),
        reverse=True,
    )[0]


def assets_dirs(app_resources: Path) -> list[Path]:
    assets_root = app_resources / "ion-dist" / "assets"
    if not assets_root.exists():
        return []
    dirs = {path.parent for path in assets_root.rglob("*.js") if path.is_file()}
    return sorted(dirs, key=lambda path: str(path).lower(), reverse=True)


def locale_config_paths() -> list[Path]:
    roaming = Path(os.environ.get("APPDATA", ""))
    return [
        roaming / "Claude" / "config.json",
        roaming / "Claude-3p" / "config.json",
    ]


def set_locale(locale: str = "zh-CN") -> list[Path]:
    written: list[Path] = []
    for path in locale_config_paths():
        path.parent.mkdir(parents=True, exist_ok=True)
        data: dict = {}
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                data = {}
        if not isinstance(data, dict):
            data = {}
        data["locale"] = locale
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(path)
    return written
