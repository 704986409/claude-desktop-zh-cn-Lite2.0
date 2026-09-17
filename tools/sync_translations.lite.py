#!/usr/bin/env python3
"""Sync translations from Jyy1529/claude-desktop_win-zh_cn upstream.

Downloads the latest zh-CN JSON resources and compares them to local copies.
Exits with code 1 if changes are detected (for CI use).
"""

import json
import urllib.request
from pathlib import Path

UPSTREAM = "https://raw.githubusercontent.com/Jyy1529/claude-desktop_win-zh_cn/master/resources"
ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "resources"

FILES = [
    "desktop-zh-CN.json",
    "frontend-zh-CN.json",
    "statsig-zh-CN.json",
]


def download(name: str) -> dict:
    url = f"{UPSTREAM}/{name}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    changed = False
    for name in FILES:
        local_path = RESOURCES / name
        local = json.loads(local_path.read_text(encoding="utf-8"))
        upstream = download(name)

        new_keys = set(upstream) - set(local)
        missing_keys = set(local) - set(upstream)

        print(f"{name}: local {len(local)} keys, upstream {len(upstream)} keys")

        if new_keys:
            print(f"  + {len(new_keys)} new keys: {sorted(new_keys)[:10]}{'...' if len(new_keys) > 10 else ''}")
            changed = True
        if missing_keys:
            print(f"  - {len(missing_keys)} removed keys: {sorted(missing_keys)[:10]}{'...' if len(missing_keys) > 10 else ''}")
            changed = True

        if changed:
            local_path.write_text(json.dumps(upstream, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"  -> updated {name}")
        else:
            print(f"  -> unchanged")

    return 1 if changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
