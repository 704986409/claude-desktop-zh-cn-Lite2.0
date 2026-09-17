# Claude Desktop zh-CN Lite

> **零性能损耗**的 Claude Desktop (Windows) 轻量汉化补丁 — 只装 JSON，不注入脚本。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Sync](https://img.shields.io/badge/translations-auto--sync-green.svg)](#翻译同步)

## 为什么有 Lite 版

[Claude Desktop Windows 中文补丁](https://github.com/Jyy1529/claude-desktop_win-zh_cn) 完成了 12,700+ 条翻译的壮举，由 [Jash (Jyy1529)](https://github.com/Jyy1529) 维护。但为了额外功能，它向每个 JS chunk 注入了字体面板、会话增强、Timeline 等运行时脚本，实测导致 **点击任意控件卡顿 15 秒以上**。

排查后确认 JSON 汉化本身无性能问题——症结全在 chunk 注入。于是诞生了 Lite 版：**同款 12,700 条翻译，去掉一切注入，零卡顿。**

> 翻译数据来自 [Jyy1529/claude-desktop_win-zh_cn](https://github.com/Jyy1529/claude-desktop_win-zh_cn)。感谢 [Jash](https://github.com/Jyy1529) 的卓越工作。

## vs Jyy1529 原版

|                    | Jyy1529 原版                                 | Lite 版 (本项目)                                 |
| ------------------ | -------------------------------------------- | ------------------------------------------------ |
| **JSON 资源**      | 12,700+ keys                                 | 同款，自动同步                                    |
| **JS chunk 注入**  | 字体面板 / 会话增强 / Timeline / CDP          | 不注入任何脚本                                    |
| **硬编码文案**     | `patch_chunks_zh_cn.py` 精确字符串替换        | 不碰 chunk                                       |
| **性能**           | 测试版本 1.10628.0 严重卡顿                    | 零性能影响                                        |
| **稳定性**         | Claude 更新可能破坏 chunk 结构                 | 仅依赖 i18n key 查表，不命中降级英文，不崩溃        |
| **版本适配**       | 需维护 chunk 匹配规则                          | 版本无关，通配自动检测                              |
| **代码量**         | 2998 行 `patch_chunks_zh_cn.py`               | 170 行 `pure_patch.py`                            |

## 做了什么

就三步：

1. 写入三份 `zh-CN.json` → `resources\`
2. 在 `index-*.js` 语言列表里插入 `"zh-CN"`（正则匹配，版本无关）
3. `Claude-3p\config.json` → `"locale": "zh-CN"`

不写 JavaScript。不修改 chunk。不注入运行时。

## 安装

> **前置条件：** Windows 版 Claude Desktop（Microsoft Store / WindowsApps），Python 3.10+

### 三步走

**1. 下载本项目**

```bash
git clone https://github.com/<你的用户名>/claude-desktop_win-zh-Lite.git
cd claude-desktop_win-zh-Lite
```

或直接在 GitHub 点绿色的 Code → Download ZIP，解压到任意位置。

**2. 关闭 Claude Desktop**

任务栏右下角 Claude 图标 → 右键 → Quit。确保 `claude.exe` 不在任务管理器里。

**3. 管理员运行安装脚本**

> 右键 `install.bat` → **以管理员身份运行**

![install](docs/install.png)

等三行 `OK` 出来，回车，重开 Claude Desktop。

### 命令行安装

```powershell
# 自动检测路径
python pure_patch.py

# 手动指定路径
python pure_patch.py --app-dir "C:\Program Files\WindowsApps\Claude_1.10628.0.0_x64__pzs8sxrjxfjjc\app"
```

### Claude 更新后

Windows Store 自动更新 Claude 会覆盖汉化文件，只需重新右键管理员运行 `install.bat` 一次。脚本的 `Claude_*` 通配自动适配最新版本。

## 恢复英文

> 右键 `restore.bat` → 以管理员身份运行

从备份恢复原始文件，locale 恢复 `en-US`。**完全可逆，不留残留。**

### 命令行恢复

```powershell
python pure_patch.py --restore
```

## 翻译同步

**不自行维护翻译数据** — 从上游自动同步，每 6 小时检查更新，有变化自动创建 PR。

启用：仓库 Settings → Actions → 启用。工作流：`.github/workflows/sync-translations.yml`

```bash
python tools/sync_translations.py   # 手动同步
```

## 兼容性原理

Claude 的 i18n key 是对英文原文的哈希（如 `"7fdcqxofEs"` → "Exit"）。只要原文不变 key 就不变。Claude 更新只是增加新 key，旧 key 继续命中；新 key 没翻译降级英文，不崩溃。

## FAQ

**装了还有英文？** 正常——硬编码的 Electron 原生 UI 不进 i18n，保持英文。大段英文请去上游提 key 补充。

**Claude 更新汉化掉了？** 重跑 `install.bat`，通配符自动适配新版本路径。

**真的不影响性能？** 用的是 Claude 自带 i18n 查表（`i18n.t(key)`），就像切语言包，没有额外运行时开销。

## 致谢

- [Jyy1529/claude-desktop_win-zh_cn](https://github.com/Jyy1529/claude-desktop_win-zh_cn) — 翻译源，Jash 一条一条填的
- [javaht/claude-desktop-zh-cn](https://github.com/javaht/claude-desktop-zh-cn) — 早期 macOS 方案
- [LINUX DO](https://linux.do/) 社区

## License

MIT
