# Open Source — 开源规则

> **首先，感谢 [Jash (Jyy1529)](https://github.com/Jyy1529) 和 [claude-desktop_win-zh_cn](https://github.com/Jyy1529/claude-desktop_win-zh_cn)。**
> 12,700 条翻译是 Jash 一条一条填进去的体力活。没有上游，就没有这个 Lite 版。我们在安装方式上做了减法，取其精华、去其卡顿。

---

本项目始于一次个人踩坑：发现社区最主流的 Claude Desktop 汉化方案在 1.10628.0 上造成严重卡顿，追踪根因后发现是 JS chunk 注入所致。我们的贡献是**做减法** — 把汉化缩减到最小可行单元（JSON + 白名单 + locale），从而在 12,700 条翻译和零性能损耗之间拿到最优解。

## 我们遵循的规则

1. **翻译归翻译，代码归代码。** 翻译来自上游 [Jyy1529/claude-desktop_win-zh_cn](https://github.com/Jyy1529/claude-desktop_win-zh_cn)（MIT License），上游的署名在每一处保留。本项目只维护补丁脚本，不声称拥有翻译内容的著作权。

2. **MIT License。** 补丁脚本（`pure_patch.py`、`sync_translations.py`）和翻译资源的合集以 MIT 协议分发。你可以自由使用、修改、分发，但必须保留原始许可声明。

3. **PR 欢迎。** 如果你发现翻译漏 key 或脚本有 bug：
   - 翻译内容问题 → 去 [上游 Jyy1529](https://github.com/Jyy1529/claude-desktop_win-zh_cn) 提 PR 补 key，本项目会自动同步
   - 补丁脚本问题 → 直接 Issue 或 PR

4. **不造车轮。** 我们不做翻译（那是 Jyy1529 的体力活），我们只做一个更安全的安装器。同理，我们不把 Claude Desktop 本身打包进 Release——"便携版"意味着你绕过了 Anthropic 的安全沙箱，本项目**不会**提供免安装包。

5. **不含 AI 生成代码声明。** 本项目的 Python 和 bat 代码由人类撰写和审查。README 中引用的上游翻译数据是 AI 辅助翻译 + 人工校对（Jyy1529 项目标注）——这在 `CONTRIBUTING.md` 和 README 中均有说明。

## 如何贡献

```bash
# 1. 确保翻译是最新的
python tools/sync_translations.py

# 2. 校验资源完整性
python tools/validate_resources.py

# 3. 本地测试安装（需要管理员 PowerShell）
python pure_patch.py --app-dir "C:\Program Files\WindowsApps\Claude_*\app"

# 4. 恢复
python pure_patch.py --restore --app-dir "..."
```

## 致上游

本项目站在 [Jyy1529](https://github.com/Jyy1529) 的肩膀上。我们取其数据、去了会导致卡顿的注入脚本，这是技术选择，不是否认上游价值。感谢 Jash。
