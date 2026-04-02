---
name: cli-anything
description: Use when the user wants Codex to build, refine, test, validate, list, install, or maintain a CLI-Anything harness for a GUI application or source repository. This skill mirrors the mature CLI-Anything workflow used by Claude Code and OpenCode, but adapts it to Codex's natural-language skill model.
metadata:
  short-description: Mature Codex bridge for CLI-Anything
---

# CLI-Anything for Codex

Use this skill whenever the user wants Codex to act like the `CLI-Anything` builder, reviewer, tester, validator, or installer.

This Codex package is intentionally self-contained:

- `references/HARNESS.md` is the bundled methodology snapshot
- `references/commands/*.md` mirror the mature Claude Code command specs
- `scripts/verify_install.py` mechanically checks the installed skill bundle
- `scripts/sync_from_plugin.py` keeps this skill aligned with the Claude/OpenCode source of truth when working inside the repository

## Rule 1: Read The Bundled HARNESS First

Before doing build, refine, test, or validate work, read `references/HARNESS.md`.

If you are inside the `CLI-Anything` repository and need to maintain this Codex integration itself:

1. Read `.agentlens/INDEX.md`
2. Run `python3 codex-skill/scripts/sync_from_plugin.py --check`
3. If references drifted, run `python3 codex-skill/scripts/sync_from_plugin.py`

## Rule 2: Treat Claude/OpenCode Commands As Semantic Modes

Codex does not provide the same slash-command UX as Claude Code or OpenCode. When using this skill:

- Interpret `references/commands/cli-anything.md` as the `build` mode spec
- Interpret `references/commands/refine.md` as the `refine` mode spec
- Interpret `references/commands/test.md` as the `test` mode spec
- Interpret `references/commands/validate.md` as the `validate` mode spec
- Interpret `references/commands/list.md` as the `list/discovery` mode spec

Do not insist on literal slash commands. Natural-language requests should map onto the same behavior.

## Mode Routing

### Build

Use when the user wants a new harness.

Read:

1. `references/HARNESS.md`
2. `references/commands/cli-anything.md`

Accept either a local source path or a repository URL. Follow the same 7-phase workflow used by the mature plugin implementation.

### Refine

Use when the harness already exists and the user wants broader coverage or a focused capability expansion.

Read:

1. `references/HARNESS.md`
2. `references/commands/refine.md`

Present the gap analysis before implementing when the situation is ambiguous.

### Test

Use when the user wants to run or repair the harness test suite.

Read:

1. `references/HARNESS.md`
2. `references/commands/test.md`

Prefer subprocess checks against the installed CLI when possible, not only module imports.

### Validate

Use when the user asks whether a harness is complete, compliant, production-ready, or aligned with the methodology.

Read:

1. `references/HARNESS.md`
2. `references/commands/validate.md`

Map findings directly to file paths and methodology requirements.

### List / Discover

Use when the user wants to know which CLI-Anything tools already exist locally or are installed.

Read:

1. `references/commands/list.md`

Return structured results when requested.

### Install / Maintain This Skill

Use when the user wants to install, upgrade, verify, or debug the Codex integration itself.

Read:

1. `references/install.md`

Use the bundled installers and verification scripts rather than ad-hoc copying.

## Output Expectations

When reporting work, include:

- the target software and source path
- the active mode: build, refine, test, validate, or list
- the files added or changed
- the verification commands actually run
- the remaining risks, backend limitations, or missing coverage

## Constraints

- Keep the generated Python harness format unchanged from the CLI-Anything methodology
- Prefer the real software backend over synthetic reimplementation
- Keep `cli_anything/` as a namespace package without a top-level `__init__.py`
- Expose `cli-anything-<software>` via `console_scripts`
- Update tests and docs whenever commands or behavior change
