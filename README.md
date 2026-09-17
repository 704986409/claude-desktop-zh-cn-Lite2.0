# Claude Desktop zh-CN Lite 2.0

> Windows 版 Claude Desktop 的轻量汉化补丁：**完整词条 + 硬编码界面替换，不注入运行时脚本，不卡顿。**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)

本仓库在两位前人的工作上继续完善，面向 Microsoft Store / WindowsApps，以及 winget / EXE 安装的 `%LOCALAPPDATA%\AnthropicClaude`。

## 致谢与上游

本项目 **不是 Anthropic 官方项目**。界面译文和补丁思路来自：

| 开发者 | 仓库 | 贡献 |
| ------ | ---- | ---- |
| **[Jash (Jyy1529)](https://github.com/Jyy1529)** | [claude-desktop_win-zh_cn](https://github.com/Jyy1529/claude-desktop_win-zh_cn) | 上万条中文词条、硬编码 chunk 替换、Windows 安装器与桌面助手。翻译是一条一条填出来的。 |
| **[Renzic-Stone](https://github.com/Renzic-Stone)** | [claude-desktop_win-zh-Lite](https://github.com/Renzic-Stone/claude-desktop_win-zh-Lite) | Lite 路线：只写 JSON、不注入 JS 运行时，解决原版字体面板 / 会话增强导致的严重卡顿。 |

Lite 2.0 把两套代码合在同一目录，并补上当前 Claude Desktop 缺失的 i18n 键、EXE 安装路径检测，以及 `shared-*.js` 语言白名单。

原始说明备份：

- [`README.jyy1529.md`](README.jyy1529.md)
- [`README.lite.md`](README.lite.md)

也感谢 [javaht/claude-desktop-zh-cn](https://github.com/javaht/claude-desktop-zh-cn) 的早期 macOS 方案，以及 [LINUX DO](https://linux.do/) 社区。

## 为什么有 Lite 2.0

[Jyy1529 原版](https://github.com/Jyy1529/claude-desktop_win-zh_cn) 完成了大规模翻译，但为了字体面板、会话增强、Timeline、CDP 等功能，会向 JS chunk **注入运行时脚本**。在部分版本上，点击任意控件会卡顿十几秒。

[Renzic-Stone Lite](https://github.com/Renzic-Stone/claude-desktop_win-zh-Lite) 确认卡顿全在注入，不在 JSON 汉化本身，于是做成「只装语言包、零卡顿」。代价是：不碰硬编码英文；词条会落后于新版 Claude；默认按商店版 `WindowsApps` 找路径，winget 桌面端经常装不上。

Lite 2.0 走中间路线：

- **沿用 Lite 的原则：不注入字体面板 / 会话增强 / Timeline / CDP**
- **沿用 Jyy1529 的词条和硬编码替换表**（只做字符串替换，不跑注入函数）
- **补全当前桌面端缺失的 i18n key**，减少大面积英文回退
- **同时支持商店版和 `%LOCALAPPDATA%\AnthropicClaude` 的 EXE / winget 安装**

## 对比

| | Jyy1529 原版 | Renzic-Stone Lite | **Lite 2.0（本仓库）** |
| --- | --- | --- | --- |
| JSON 语言包 | 12,700+ keys | 同款上游词条 | 上游词条 + 当前版本缺失键补全 |
| JS 运行时注入 | 字体面板 / 会话增强 / Timeline / CDP | 不注入 | **不注入** |
| 硬编码英文 | `patch_chunks_zh_cn.py` 精确替换 | 不碰 chunk | 使用同一张替换表，**不调用注入函数** |
| 语言白名单 | 视安装器而定 | 主要改 `index-*.js` | `index-*.js` + `shared-*.js`，正则插入 `zh-CN` |
| 安装路径 | WindowsApps + AnthropicClaude | 默认 WindowsApps | 自动检测两种路径 |
| locale | `Claude-3p\config.json` | 同左 | `Claude` 与 `Claude-3p` 都写 |
| 性能 | 注入后可能严重卡顿 | 零额外开销 | 与 Lite 相同，不注入则不卡 |
| 更新后 | 通常要重跑安装器 | 重跑 `install.bat` | 重跑 `install-complete.bat` |

## 做了什么

推荐安装实际是这几步：

1. 写入三份语言包  
   `resources/zh-CN.json`、`ion-dist/i18n/zh-CN.json`、`ion-dist/i18n/statsig/zh-CN.json`
2. 在前端语言列表里插入 `"zh-CN"`（含新版 `shared-*.js`）
3. 把 `locale` 设为 `zh-CN`
4. 按 Jyy1529 的硬编码表替换仍写在 JS 里的英文按钮、设置项、标题（**不注入脚本**）

Claude 的 i18n key 是英文原文的哈希。原文不变则 key 不变；新版本只增加新 key，旧译文继续生效，没译到的键回退英文，不会崩溃。

## 功能一览

- **界面汉化**：聊天、Cowork、Code、设置、侧边栏、连接器等走官方 `i18n.t(key)` 查表
- **词条补全**：对当前安装的 `en-US.json` 里缺失的中文键做补译（可重复跑 `--fill-missing`）
- **硬编码替换**：设置页、任务、项目、会话等未进 JSON 的英文标签
- **双路径检测**：商店版 `C:\Program Files\WindowsApps\Claude_*` 与 winget/EXE 的 `app-*\resources`
- **可逆**：备份后可一键恢复英文
- **可选原版全家桶**：仍保留 Jyy1529 的 `claude-zh-cn.bat`（含运行时注入，部分版本会卡）
- **可选桌面助手**：`ui/`、`src-tauri/` 为 Jyy1529 的图形安装器源码

产品名默认保持英文：`Claude`、`Cowork`、`MCP`、`API`、`CLI` 等。

## 安装

**前置：** Windows 10/11、已安装 Claude Desktop、Python 3.10+（安装时勾选 Add to PATH）。

### 1. 获取本仓库

```bash
git clone https://github.com/704986409/claude-desktop-zh-cn-Lite2.0.git
cd claude-desktop-zh-cn-Lite2.0
```

也可在 GitHub 点 Code → Download ZIP，解压到任意目录。

### 2. 退出 Claude Desktop

托盘图标右键 **Quit**。任务管理器里不能再有 `claude.exe`。

### 3. 运行安装脚本（推荐）

右键 `install-complete.bat` → **以管理员身份运行**。

它会：结束 Claude 进程 → 写入语言包和白名单 → 复制补全后的 JSON → 打硬编码替换（无注入）。

只装 JSON、改动最少：

```bat
install-lite.bat
```

命令行：

```powershell
python pure_patch.py
python enhance_zh_cn.py
```

手动指定 app 目录（目录下必须有 `resources\en-US.json`）：

```powershell
python pure_patch.py --app-dir "C:\Users\你的用户名\AppData\Local\AnthropicClaude\app-2.110.1"
python enhance_zh_cn.py --app-dir "C:\Users\你的用户名\AppData\Local\AnthropicClaude\app-2.110.1"
```

装完后重新打开 Claude Desktop。

### Claude 更新后

官方更新会覆盖汉化文件。再运行一次 `install-complete.bat` 即可，脚本会自动找最新 `Claude_*` / `app-*` 目录。

若更新后又大面积英文：

```powershell
python enhance_zh_cn.py --fill-missing
```

需要能访问 `translate.googleapis.com`（可用系统代理）。缓存在 `tools/mt-cache.json`。

## 恢复英文

右键 `restore-lite.bat` → 以管理员身份运行。

或：

```powershell
python pure_patch.py --restore
```

从备份恢复官方文件，locale 改回 `en-US`。可逆，不留注入残留。

## 不推荐（会卡）

Jyy1529 原版入口仍在仓库里，供对照或需要字体面板 / 会话增强时使用：

```bat
claude-zh-cn.bat
```

交互菜单：`claude-zh-cn.ps1`。该路径会注入运行时脚本，部分 Claude 版本上点击控件会明显卡顿。

## 主要文件

| 文件 | 说明 |
|------|------|
| `install-complete.bat` | **推荐安装**：JSON + 白名单 + 硬编码，无注入 |
| `install-lite.bat` | 仅 JSON + 白名单 |
| `restore-lite.bat` | 恢复英文 |
| `claude_paths.py` | 检测商店版 / EXE 安装路径，写入 locale |
| `pure_patch.py` | Lite 安装核心 |
| `enhance_zh_cn.py` | 补词条、复制资源、硬编码替换 |
| `patch_exe_whitelist.py` | 单独打语言白名单 |
| `apply_hardcoded_only.py` | 只打硬编码替换 |
| `resources/*-zh-CN.json` | 桌面壳层 / 前端 / Statsig 中文资源 |
| `patch_chunks_zh_cn.py` | Jyy1529 原版 chunk 补丁（含注入，供原版安装器使用） |
| `claude-zh-cn.ps1` / `.bat` | Jyy1529 交互安装器 |
| `ui/` `src-tauri/` | Jyy1529 桌面助手 |

## FAQ

**装完还有英文？**  
硬编码的 Electron 原生菜单、产品名、未收录的新 key 会保持英文。先彻底退出再打开。仍大面积英文时重跑 `install-complete.bat`，或加 `--fill-missing`。

**会不会卡？**  
推荐入口不注入运行时，走官方 i18n 查表，没有额外脚本开销。不要用 `claude-zh-cn.bat`，除非你明确需要原版注入功能。

**商店版和官网/winget 版都能用吗？**  
能。`claude_paths.py` 会先找 WindowsApps，再找 `%LOCALAPPDATA%\AnthropicClaude\app-*`。

**更新后汉化没了？**  
正常。官方安装器会覆盖资源，重跑安装脚本即可。

## License

MIT。上游译文与脚本版权归原作者；本仓库在其基础上增加检测、补全与无注入安装入口。
