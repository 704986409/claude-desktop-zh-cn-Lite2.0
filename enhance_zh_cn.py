#!/usr/bin/env python3
"""Complete Lite zh-CN JSON coverage and apply hardcoded UI replacements.

Does not inject font/session runtime scripts.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from claude_paths import assets_dirs, find_claude_app_dir, set_locale as write_locale

ROOT = Path(__file__).resolve().parent
RESOURCES = ROOT / "resources"
CACHE_PATH = ROOT / "tools" / "mt-cache.json"
BACKUP = Path(os.environ["LOCALAPPDATA"]) / "Claude-zh-CN-pure-backup"
APP_RES: Path | None = None

KEEP = {
    "Claude", "Cowork", "Artifacts", "MCP", "GitHub", "Git", "Slack", "Google",
    "Drive", "API", "CLI", "SSO", "OIDC", "WSL", "SSH", "VM", "PDF", "CSV",
    "JSON", "HTTP", "HTTPS", "URL", "ID", "PR", "OK", "Max", "Pro", "Team",
    "Enterprise", "Anthropic", "Windows", "macOS", "Linux", "Chrome", "iOS",
    "Android", "Xcode", "npm", "pip", "Node", "Python", "OpenTelemetry",
}

SKIP_EQ = {
    "API", "CLI", "CSV", "PDF", "JSON", "URL", "ID", "PR", "OK", "SSO", "OIDC",
    "WSL", "SSH", "VM", "HTTP", "HTTPS", "MCP", "GitHub", "Claude", "Cowork",
    "N/A", "P/S", "D/E", "MM", "DD", "Cc", "Bcc", "To", "HR", "PIN", "DNA",
    "Tab", "p50", "4xx", "3M", "1M", "JCT", "X", "#", "/",
}

GLOSSARY = {
    "New chat": "新对话",
    "New Chat": "新对话",
    "New task": "新任务",
    "Settings": "设置",
    "Recents": "最近",
    "Projects": "项目",
    "Project": "项目",
    "Chat": "聊天",
    "Code": "代码",
    "Open": "打开",
    "Close": "关闭",
    "Cancel": "取消",
    "Save": "保存",
    "Delete": "删除",
    "Edit": "编辑",
    "Copy": "复制",
    "Cut": "剪切",
    "Paste": "粘贴",
    "Refresh": "刷新",
    "Search": "搜索",
    "Search…": "搜索…",
    "Search...": "搜索...",
    "Next Task": "下一项任务",
    "Manage folders": "管理文件夹",
    "Import complete": "导入完成",
    "Open Extensions Folder": "打开扩展文件夹",
    "Go": "前往",
    "File": "文件",
    "Files": "文件",
    "Folder": "文件夹",
    "Documents": "文档",
    "Comment": "评论",
    "Connector": "连接器",
    "Connectors": "连接器",
    "Skills": "技能",
    "Plugins": "插件",
    "Labels": "标签",
    "Page": "页面",
    "Shared": "已共享",
    "Updated": "已更新",
    "Send feedback": "发送反馈",
    "Not answered": "未回答",
    "Open scheduled tasks": "打开计划任务",
    "Your first task": "你的第一个任务",
    "Show full commit message": "显示完整提交说明",
    "Add": "添加",
    "New": "新建",
    "Fix": "修复",
    "Pin": "固定",
    "pin": "固定",
    "Top": "顶部",
    "Help": "帮助",
    "View": "查看",
    "Window": "窗口",
    "Developer": "开发者",
    "General": "通用",
    "Appearance": "外观",
    "Theme": "主题",
    "Dark": "深色",
    "Light": "浅色",
    "System": "系统",
    "Account": "账户",
    "Sign in": "登录",
    "Sign out": "退出登录",
    "Log out": "退出登录",
    "Upgrade": "升级",
    "Learn more": "了解更多",
    "Try again": "重试",
    "Continue": "继续",
    "Back": "返回",
    "Next": "下一步",
    "Done": "完成",
    "Apply": "应用",
    "Discard": "放弃",
    "Rename": "重命名",
    "Move": "移动",
    "Export": "导出",
    "Import": "导入",
    "Download": "下载",
    "Upload": "上传",
    "Uploading…": "正在上传…",
    "Install": "安装",
    "Uninstall": "卸载",
    "Enable": "启用",
    "Disable": "禁用",
    "Enabled": "已启用",
    "Disabled": "已禁用",
    "On": "开",
    "Off": "关",
    "Yes": "是",
    "No": "否",
    "All": "全部",
    "Active": "活跃",
    "Archived": "已归档",
    "Archive": "归档",
    "Unarchive": "取消归档",
    "Local": "本地",
    "Remote": "远程",
    "Cloud": "云端",
    "Recent": "最近",
    "History": "历史",
    "Memory": "记忆",
    "Instructions": "说明",
    "Permissions": "权限",
    "Privacy": "隐私",
    "Security": "安全",
    "Advanced": "高级",
    "Experimental": "实验性",
    "Beta": "测试版",
    "Preview": "预览",
    "Plan": "计划",
    "Manual": "手动",
    "Auto": "自动",
    "Accept edits": "接受编辑",
    "Stop": "停止",
    "Retry": "重试",
    "Reload": "重新加载",
    "Restart": "重启",
    "Quit": "退出",
    "Exit": "退出",
    "Minimize": "最小化",
    "Maximize": "最大化",
    "Always on top": "始终置顶",
    "Hide": "隐藏",
    "Show": "显示",
    "More": "更多",
    "Less": "更少",
    "Details": "详情",
    "Error": "错误",
    "Warning": "警告",
    "Success": "成功",
    "Loading": "正在加载",
    "Loading…": "正在加载…",
    "Please wait": "请稍候",
    "Not found": "未找到",
    "Unavailable": "不可用",
    "Optional": "可选",
    "Required": "必填",
    "Default": "默认",
    "Custom": "自定义",
    "Browse": "浏览",
    "Select folder": "选择文件夹",
    "Select file": "选择文件",
    "Clear": "清除",
    "Reset": "重置",
    "Restore": "恢复",
    "Confirm": "确认",
    "OK": "确定",
    "Got it": "知道了",
    "Dismiss": "关闭",
    "Skip": "跳过",
    "Later": "稍后",
    "Now": "现在",
    "Today": "今天",
    "Yesterday": "昨天",
    "This week": "本周",
    "Older": "更早",
    "Name": "名称",
    "Description": "描述",
    "Path": "路径",
    "Model": "模型",
    "Usage": "用量",
    "Limit": "额度",
    "Task": "任务",
    "Tasks": "任务",
    "Session": "会话",
    "Sessions": "会话",
    "Conversation": "对话",
    "Message": "消息",
    "Prompt": "提示",
    "Terminal": "终端",
    "Browser": "浏览器",
    "Diff": "差异",
    "Review": "审查",
    "Merge": "合并",
    "Commit": "提交",
    "Branch": "分支",
    "Repository": "仓库",
    "Workspace": "工作区",
    "Sandbox": "沙箱",
    "Extensions": "扩展",
    "Marketplace": "扩展市场",
    "Scheduled tasks": "计划任务",
    "Remote Control": "远程控制",
    "Live artifacts": "实时工件",
    "Artifacts": "工件",
    "Please double-check responses.": "请再次核对回复内容。",
    "Hi, I’m Claude.": "你好，我是 Claude。",
    "Hi, I'm Claude.": "你好，我是 Claude。",
    "Mulling": "正在思考",
    "read": "已读",
    "How": "如何",
    "Why": "为什么",
}

PH_RE = re.compile(r"\{[^{}]+\}|</?[a-zA-Z][^>]*>|%[0-9$]*[sd]|`[^`]+`")
KEEP_RE = re.compile(r"\b(" + "|".join(re.escape(x) for x in sorted(KEEP, key=len, reverse=True)) + r")\b")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")


def should_skip(text: str) -> bool:
    s = text.strip()
    if not s or s in SKIP_EQ:
        return True
    if re.fullmatch(r"[\W\d_]+", s):
        return True
    if re.search(r"[\u4e00-\u9fff]", s):
        return True
    if not re.search(r"[A-Za-z]", s):
        return True
    if re.fullmatch(r"[A-Z0-9][A-Z0-9+./_-]{0,6}", s) and s.upper() == s:
        return True
    return False


def protect(text: str) -> tuple[str, list[str]]:
    ph: list[str] = []

    def put(m: re.Match[str]) -> str:
        ph.append(m.group(0))
        return f"⟦{len(ph) - 1}⟧"

    out = PH_RE.sub(put, text)
    out = KEEP_RE.sub(put, out)
    return out, ph


def restore(text: str, ph: list[str]) -> str:
    def put(m: re.Match[str]) -> str:
        i = int(m.group(1))
        return ph[i] if 0 <= i < len(ph) else m.group(0)

    return re.sub(r"⟦(\d+)⟧", put, text)


def gtx(text: str) -> str:
    q = urllib.parse.quote(text)
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q={q}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return "".join(part[0] for part in data[0] if part and part[0])


def translate_batch(texts: list[str], cache: dict[str, str]) -> None:
    pending: list[tuple[str, str, list[str]]] = []
    for text in texts:
        if text in cache or text in GLOSSARY or should_skip(text):
            continue
        protected, ph = protect(text)
        pending.append((text, protected.replace("\n", " "), ph))
    chunk = 10
    for i in range(0, len(pending), chunk):
        part = pending[i : i + chunk]
        payload = "\n".join(item[1] for item in part)
        try:
            zh_blob = gtx(payload)
            lines = zh_blob.split("\n")
            if len(lines) != len(part):
                # fallback per item
                for text, protected, ph in part:
                    try:
                        cache[text] = restore(gtx(protected), ph) or text
                    except Exception:
                        cache[text] = text
                    time.sleep(0.08)
            else:
                for (text, _protected, ph), zh in zip(part, lines):
                    cache[text] = restore(zh, ph) or text
        except Exception:
            for text, protected, ph in part:
                try:
                    cache[text] = restore(gtx(protected), ph) or text
                except Exception:
                    cache[text] = text
                time.sleep(0.08)
        save_cache(cache)
        print(f"  mt {min(i + chunk, len(pending))}/{len(pending)}")
        time.sleep(0.12)


def resolve(text: str, cache: dict[str, str], tm: dict[str, str]) -> str:
    if text in GLOSSARY:
        return GLOSSARY[text]
    if text in tm:
        return tm[text]
    if text in cache:
        return cache[text]
    if should_skip(text):
        return text
    return cache.get(text, text)


def fill_dict(en: dict, zh: dict, cache: dict[str, str], label: str) -> dict:
    out = dict(zh)
    missing = [k for k in en if k not in out or not str(out.get(k) or "").strip()]
    print(f"[{label}] en={len(en)} zh={len(out)} missing={len(missing)}")
    tm: dict[str, str] = {}
    for k, zv in out.items():
        ev = en.get(k)
        if isinstance(ev, str) and isinstance(zv, str) and ev and zv and ev != zv:
            tm.setdefault(ev, zv)
    need_mt: list[str] = []
    seen: set[str] = set()
    for k in missing:
        ev = en.get(k)
        if not isinstance(ev, str):
            continue
        if ev in tm or ev in GLOSSARY or ev in cache or should_skip(ev):
            continue
        if ev not in seen:
            seen.add(ev)
            need_mt.append(ev)
    print(f"[{label}] mt unique={len(need_mt)}")
    translate_batch(need_mt, cache)
    for k in missing:
        ev = en[k]
        if not isinstance(ev, str):
            out[k] = ev
            continue
        zh_val = resolve(ev, cache, tm)
        out[k] = zh_val
        if zh_val != ev:
            tm.setdefault(ev, zh_val)
    save_cache(cache)
    still = sum(1 for k, v in en.items() if isinstance(v, str) and out.get(k) == v)
    print(f"[{label}] still-english≈{still}")
    return out


def copy_into_app(src: Path, dst: Path) -> None:
    if APP_RES is None:
        raise SystemExit("APP_RES is not set")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        try:
            rel = dst.relative_to(APP_RES)
        except ValueError:
            rel = Path(dst.name)
        bak = BACKUP / rel
        bak.parent.mkdir(parents=True, exist_ok=True)
        if not bak.exists():
            try:
                shutil.copy2(dst, bak)
            except OSError:
                pass
    shutil.copy2(src, dst)
    print("wrote", dst)


def apply_hardcoded() -> int:
    if APP_RES is None:
        raise SystemExit("APP_RES is not set")
    assets_list = assets_dirs(APP_RES)
    assets = assets_list[0] if assets_list else APP_RES / "ion-dist" / "assets" / "v1"
    extra = [
        ('children:"Chat"', 'children:"聊天"'),
        ('children:"New chat"', 'children:"新对话"'),
        ('title:"New chat"', 'title:"新对话"'),
        ('?"New task":"New chat"', '?"新任务":"新对话"'),
        ('children:"Recents"', 'children:"最近"'),
        ('label:"Recents"', 'label:"最近"'),
        ('children:"Projects"', 'children:"项目"'),
        ('label:"Projects"', 'label:"项目"'),
        ('children:"Settings"', 'children:"设置"'),
        ('label:"Settings"', 'label:"设置"'),
        ('title:"Settings"', 'title:"设置"'),
        ('children:"Code"', 'children:"代码"'),
        ('"New Chat"', '"新对话"'),
        ('"Manage folders"', '"管理文件夹"'),
        ('"Remote Control is turned off"', '"远程控制已关闭"'),
        ('"Install Extension…"','"安装扩展…"'),
        ('"Open Extensions Folder"', '"打开扩展文件夹"'),
        ('"Next Task"', '"下一项任务"'),
        ('"Import complete"', '"导入完成"'),
        ('"Device tools access"', '"设备工具访问权限"'),
    ]
    patches: list[tuple[str, str]] = list(extra)
    try:
        sys.path.insert(0, str(ROOT))
        from patch_chunks_zh_cn import PATCHES  # type: ignore
        for items in PATCHES.values():
            patches.extend(items)
    except Exception as e:
        print("upstream PATCHES skipped:", e)

    # longest first to avoid partial overlap
    uniq: dict[str, str] = {}
    for old, new in patches:
        if old and old != new:
            uniq[old] = new
    items = sorted(uniq.items(), key=lambda x: len(x[0]), reverse=True)

    changed_files = 0
    total_repl = 0
    for path in sorted(assets.glob("*.js")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        orig = text
        n = 0
        for old, new in items:
            if old in text:
                c = text.count(old)
                text = text.replace(old, new)
                n += c
        if text != orig:
            rel = path.relative_to(APP_RES)
            bak = BACKUP / rel
            bak.parent.mkdir(parents=True, exist_ok=True)
            if not bak.exists():
                shutil.copy2(path, bak)
            try:
                path.write_text(text, encoding="utf-8")
            except PermissionError:
                os.chmod(path, 0o666)
                path.write_text(text, encoding="utf-8")
            changed_files += 1
            total_repl += n
            print(f"  {path.name}: {n} replacements")
    print(f"hardcoded files={changed_files} replacements={total_repl}")
    return total_repl


def main() -> int:
    import argparse

    global APP_RES
    parser = argparse.ArgumentParser(description="Fill missing zh-CN keys and apply hardcoded UI strings (no runtime inject)")
    parser.add_argument("--app-dir", type=str, default=None)
    parser.add_argument("--fill-missing", action="store_true", help="machine-translate keys still missing from resources/")
    parser.add_argument("--hardcoded-only", action="store_true")
    parser.add_argument("--skip-hardcoded", action="store_true")
    args = parser.parse_args()

    app_dir = Path(args.app_dir) if args.app_dir else find_claude_app_dir()
    if not app_dir:
        raise SystemExit("Claude app directory not found. Use --app-dir.")
    APP_RES = app_dir / "resources"
    print("app-dir", app_dir)

    os.environ.setdefault("HTTP_PROXY", "http://127.0.0.1:7897")
    os.environ.setdefault("HTTPS_PROXY", "http://127.0.0.1:7897")

    if args.hardcoded_only:
        print("[hardcoded] applying replacements without runtime inject")
        apply_hardcoded()
        write_locale("zh-CN")
        return 0

    cache = load_cache()
    desktop_en = load_json(APP_RES / "en-US.json")
    frontend_en = load_json(APP_RES / "ion-dist" / "i18n" / "en-US.json")
    desktop = load_json(RESOURCES / "desktop-zh-CN.json")
    frontend = load_json(RESOURCES / "frontend-zh-CN.json")
    statsig = load_json(RESOURCES / "statsig-zh-CN.json")

    if args.fill_missing:
        desktop = fill_dict(desktop_en, desktop, cache, "desktop")
        frontend = fill_dict(frontend_en, frontend, cache, "frontend")
        dump_json(RESOURCES / "desktop-zh-CN.json", desktop)
        dump_json(RESOURCES / "frontend-zh-CN.json", frontend)

    copy_into_app(RESOURCES / "desktop-zh-CN.json", APP_RES / "zh-CN.json")
    copy_into_app(RESOURCES / "frontend-zh-CN.json", APP_RES / "ion-dist" / "i18n" / "zh-CN.json")
    copy_into_app(RESOURCES / "statsig-zh-CN.json", APP_RES / "ion-dist" / "i18n" / "statsig" / "zh-CN.json")

    dyn_en_path = APP_RES / "ion-dist" / "i18n" / "dynamic" / "en-US.json"
    if dyn_en_path.exists() and args.fill_missing:
        dyn_en = load_json(dyn_en_path)
        dyn_zh = fill_dict(dyn_en, {}, cache, "dynamic")
        dump_json(APP_RES / "ion-dist" / "i18n" / "dynamic" / "zh-CN.json", dyn_zh)

    if not args.skip_hardcoded:
        print("[hardcoded] applying replacements without runtime inject")
        apply_hardcoded()

    written = write_locale("zh-CN")
    print("locale", ", ".join(str(p) for p in written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
