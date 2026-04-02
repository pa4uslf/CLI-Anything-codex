# Installing CLI-Anything In Codex

Use this reference when the task is about the Codex integration itself rather than building a target software harness.

## Install

From the repository root:

```bash
bash codex-skill/scripts/install.sh --sync --verify
```

On Windows PowerShell:

```powershell
.\codex-skill\scripts\install.ps1 -Sync -Verify
```

Default install target:

- `$CODEX_HOME/skills/cli-anything`
- falls back to `~/.codex/skills/cli-anything`

## Upgrade

The installer refuses to overwrite by default. To replace an existing installation:

```bash
bash codex-skill/scripts/install.sh --sync --verify --force
```

```powershell
.\codex-skill\scripts\install.ps1 -Sync -Verify -Force
```

## Verify

Verify a local checkout:

```bash
python3 codex-skill/scripts/verify_install.py codex-skill
```

Verify an installed skill:

```bash
python3 codex-skill/scripts/verify_install.py ~/.codex/skills/cli-anything
```

Add `--json` for machine-readable output.

## Keep References In Sync

When working inside the repository, the Codex skill should stay aligned with the Claude/OpenCode source of truth:

```bash
python3 codex-skill/scripts/sync_from_plugin.py --check
python3 codex-skill/scripts/sync_from_plugin.py
```

This syncs:

- `cli-anything-plugin/HARNESS.md`
- `cli-anything-plugin/commands/*.md`

into the bundled Codex references directory.
