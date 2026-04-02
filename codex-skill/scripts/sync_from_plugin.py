#!/usr/bin/env python3
"""Sync Codex skill references from the mature Claude/OpenCode source files."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_mapping(root: Path) -> dict[Path, Path]:
    plugin_dir = root / "cli-anything-plugin"
    refs_dir = root / "codex-skill" / "references"
    commands_dir = refs_dir / "commands"

    return {
        plugin_dir / "HARNESS.md": refs_dir / "HARNESS.md",
        plugin_dir / "commands" / "cli-anything.md": commands_dir / "cli-anything.md",
        plugin_dir / "commands" / "refine.md": commands_dir / "refine.md",
        plugin_dir / "commands" / "test.md": commands_dir / "test.md",
        plugin_dir / "commands" / "validate.md": commands_dir / "validate.md",
        plugin_dir / "commands" / "list.md": commands_dir / "list.md",
    }


def ensure_sources_exist(mapping: dict[Path, Path]) -> None:
    missing = [str(src) for src in mapping if not src.exists()]
    if missing:
        raise FileNotFoundError("Missing source files:\n" + "\n".join(missing))


def sync(mapping: dict[Path, Path]) -> int:
    for src, dest in mapping.items():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"synced {dest.relative_to(repo_root())}")
    return 0


def check(mapping: dict[Path, Path]) -> int:
    drift = []
    for src, dest in mapping.items():
        if not dest.exists() or not filecmp.cmp(src, dest, shallow=False):
            drift.append((src, dest))

    if drift:
        print("Codex skill references are out of sync with cli-anything-plugin:", file=sys.stderr)
        for src, dest in drift:
            print(
                f"  {dest.relative_to(repo_root())} != {src.relative_to(repo_root())}",
                file=sys.stderr,
            )
        return 1

    print("Codex skill references are in sync.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if bundled references drift from cli-anything-plugin.",
    )
    args = parser.parse_args()

    mapping = build_mapping(repo_root())
    ensure_sources_exist(mapping)

    if args.check:
        return check(mapping)
    return sync(mapping)


if __name__ == "__main__":
    raise SystemExit(main())
