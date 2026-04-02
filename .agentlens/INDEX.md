# CLI-Anything Navigation

这个索引给进入仓库的 agent 一个短导航，避免在大仓库里盲找。

## 先看哪里

1. `README.md` / `README_CN.md`
2. `cli-anything-plugin/HARNESS.md`
3. `cli-anything-plugin/README.md`
4. `codex-skill/SKILL.md`

## 按场景导航

### Claude Code 插件

- `cli-anything-plugin/.claude-plugin/plugin.json`
- `cli-anything-plugin/commands/*.md`
- `cli-anything-plugin/verify-plugin.sh`

### OpenCode 命令

- `opencode-commands/*.md`

### Codex 接入

- `codex-skill/SKILL.md`
- `codex-skill/references/HARNESS.md`
- `codex-skill/references/commands/*.md`
- `codex-skill/references/install.md`
- `codex-skill/scripts/install.sh`
- `codex-skill/scripts/install.ps1`
- `codex-skill/scripts/sync_from_plugin.py`
- `codex-skill/scripts/verify_install.py`

### 各软件生成样例

- `<software>/agent-harness/cli_anything/<software>/`
- `<software>/agent-harness/setup.py`
- `<software>/agent-harness/cli_anything/<software>/tests/TEST.md`

## 当前与本次任务相关的关键事实

- 根 `AGENTS.md` 要求开工前读取这个索引；之前仓库里缺失该文件。
- Codex 接入当前是 skill 模式，不是 Claude Code 那种斜杠命令插件。
- `cli-anything-plugin/HARNESS.md` 是方法论单一事实源。
- 如果修改 `codex-skill`，应先运行：
  - `python3 codex-skill/scripts/sync_from_plugin.py --check`
  - 需要刷新时再运行 `python3 codex-skill/scripts/sync_from_plugin.py`

## 建议验证入口

- `python3 codex-skill/scripts/verify_install.py codex-skill`
- `bash codex-skill/scripts/install.sh --sync --verify --dest-root /tmp/codex-skills`
- `python3 codex-skill/scripts/sync_from_plugin.py --check`
