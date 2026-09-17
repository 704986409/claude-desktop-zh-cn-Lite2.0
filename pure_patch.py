#!/usr/bin/env python3
"""JSON-only zh-CN install: language packs + whitelist + locale. No runtime inject."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import stat
from pathlib import Path

from claude_paths import assets_dirs, find_claude_app_dir, set_locale

ROOT = Path(__file__).resolve().parent
RESOURCES = ROOT / "resources"
BACKUP_ROOT = Path(os.environ["LOCALAPPDATA"]) / "Claude-zh-CN-pure-backup"
WHITELIST_RE = re.compile(r'(\["en-US"(?:,"[a-zA-Z]{2,3}(?:-[a-zA-Z0-9]{2,4})*")+)\]')
LOCALE_MAP_OLD = '{"en-US":"en","de-DE":"de","fr-FR":"fr","ko-KR":"ko","ja-JP":"ja","es-419":"es","es-ES":"es","it-IT":"it","hi-IN":"en","pt-BR":"pt_BR","id-ID":"id"}'
LOCALE_MAP_NEW = '{"en-US":"en","de-DE":"de","fr-FR":"fr","ko-KR":"ko","ja-JP":"ja","es-419":"es","es-ES":"es","it-IT":"it","hi-IN":"en","pt-BR":"pt_BR","id-ID":"id","zh-CN":"zh"}'


def backup_file(path: Path, app_resources: Path) -> None:
    if not path.exists():
        return
    rel = path.relative_to(app_resources)
    dst = BACKUP_ROOT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        try:
            shutil.copy2(path, dst)
        except OSError:
            pass


def copy2_best_effort(src: Path, dst: Path, *, context: str) -> bool:
    try:
        shutil.copy2(src, dst)
        return True
    except PermissionError:
        if dst.exists():
            try:
                dst.chmod(dst.stat().st_mode | stat.S_IWRITE)
            except OSError:
                pass
        try:
            shutil.copy2(src, dst)
            return True
        except OSError as e:
            print(f"  Error: {context}: {e}")
            return False
    except OSError as e:
        print(f"  Error: {context}: {e}")
        return False


def write_text_best_effort(path: Path, text: str, *, context: str) -> bool:
    try:
        path.write_text(text, encoding="utf-8")
        return True
    except PermissionError:
        try:
            path.chmod(path.stat().st_mode | stat.S_IWRITE)
            path.write_text(text, encoding="utf-8")
            return True
        except OSError as e:
            print(f"  Error: {context}: {e}")
            return False
    except OSError as e:
        print(f"  Error: {context}: {e}")
        return False


def patch_whitelist(app_resources: Path) -> list[str]:
    touched: list[str] = []
    for assets_dir in assets_dirs(app_resources):
        for path in sorted(assets_dir.glob("*.js")):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            original = text
            if WHITELIST_RE.search(text) and '"zh-CN"' not in text:
                backup_file(path, app_resources)
                text = WHITELIST_RE.sub(lambda m: m.group(1) + ',"zh-CN"]', text, count=1)
            if LOCALE_MAP_OLD in text and '"zh-CN":"zh"' not in text:
                backup_file(path, app_resources)
                text = text.replace(LOCALE_MAP_OLD, LOCALE_MAP_NEW, 1)
            if text != original and write_text_best_effort(path, text, context=path.name):
                touched.append(path.name)
    return touched


def install(app_dir: Path) -> int:
    app_resources = app_dir / "resources"
    if not app_resources.exists():
        raise SystemExit(f"resources not found: {app_resources}")

    files = [
        (RESOURCES / "desktop-zh-CN.json", app_resources / "zh-CN.json"),
        (RESOURCES / "frontend-zh-CN.json", app_resources / "ion-dist" / "i18n" / "zh-CN.json"),
        (RESOURCES / "statsig-zh-CN.json", app_resources / "ion-dist" / "i18n" / "statsig" / "zh-CN.json"),
    ]
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

    print("[1/3] Copying zh-CN JSON resources...")
    for src, dst in files:
        if not src.exists():
            raise SystemExit(f"Missing: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        backup_file(dst, app_resources)
        if not copy2_best_effort(src, dst, context=f"copy {dst.name}"):
            return 1
    print("  OK")

    print("[2/3] Patching language whitelist...")
    wl = patch_whitelist(app_resources)
    print(f"  {'OK ' + ', '.join(wl) if wl else 'skipped'}")

    print("[3/3] Setting locale=zh-CN...")
    written = set_locale("zh-CN")
    print("  OK", ", ".join(str(p) for p in written))
    print(f"\nDone. Backup: {BACKUP_ROOT}")
    print("Restart Claude Desktop to apply.")
    return 0


def restore(app_dir: Path) -> int:
    app_resources = app_dir / "resources"
    targets = [
        app_resources / "zh-CN.json",
        app_resources / "ion-dist" / "i18n" / "zh-CN.json",
        app_resources / "ion-dist" / "i18n" / "statsig" / "zh-CN.json",
        app_resources / "ion-dist" / "i18n" / "dynamic" / "zh-CN.json",
    ]
    restored = 0
    for dst in targets:
        if not dst.exists():
            continue
        bak = BACKUP_ROOT / dst.relative_to(app_resources)
        if bak.exists():
            try:
                shutil.copy2(bak, dst)
                restored += 1
            except OSError:
                pass
        else:
            dst.unlink(missing_ok=True)

    for assets_dir in assets_dirs(app_resources):
        for path in sorted(assets_dir.glob("*.js")):
            bak = BACKUP_ROOT / path.relative_to(app_resources)
            if bak.exists():
                try:
                    shutil.copy2(bak, path)
                except OSError:
                    pass

    set_locale("en-US")
    print(f"Restored {restored} JSON files. Locale set to en-US.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Claude Desktop JSON-only zh-CN patch")
    parser.add_argument("--app-dir", type=str, default=None)
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    app_dir = Path(args.app_dir) if args.app_dir else find_claude_app_dir()
    if not app_dir or not app_dir.exists():
        raise SystemExit("Claude app directory not found. Use --app-dir.")
    print("app-dir", app_dir)
    return restore(app_dir) if args.restore else install(app_dir)


if __name__ == "__main__":
    raise SystemExit(main())
