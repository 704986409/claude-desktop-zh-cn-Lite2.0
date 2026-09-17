#!/usr/bin/env python3
"""Insert zh-CN into Claude Desktop language whitelist (index/shared JS)."""
from __future__ import annotations

import argparse
from pathlib import Path

from claude_paths import find_claude_app_dir
from pure_patch import patch_whitelist


def main() -> int:
    parser = argparse.ArgumentParser(description="Patch zh-CN language whitelist")
    parser.add_argument("--app-dir", type=str, default=None)
    args = parser.parse_args()
    app_dir = Path(args.app_dir) if args.app_dir else find_claude_app_dir()
    if not app_dir:
        raise SystemExit("Claude app directory not found. Use --app-dir.")
    touched = patch_whitelist(app_dir / "resources")
    print("whitelist", touched or "no changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
