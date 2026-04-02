#!/usr/bin/env python3
"""Verify that a CLI-Anything Codex skill bundle is complete."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/HARNESS.md",
    "references/install.md",
    "references/commands/cli-anything.md",
    "references/commands/refine.md",
    "references/commands/test.md",
    "references/commands/validate.md",
    "references/commands/list.md",
    "scripts/install.sh",
    "scripts/install.ps1",
    "scripts/sync_from_plugin.py",
    "scripts/verify_install.py",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skill_dir",
        nargs="?",
        default="codex-skill",
        help="Path to the Codex skill directory to verify.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser.parse_args()


def verify(skill_dir: Path) -> dict[str, object]:
    missing = [path for path in REQUIRED_FILES if not (skill_dir / path).exists()]

    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8") if (skill_dir / "SKILL.md").exists() else ""
    openai_yaml = (
        (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
        if (skill_dir / "agents" / "openai.yaml").exists()
        else ""
    )

    checks = {
        "skill_dir": str(skill_dir.resolve()),
        "missing_files": missing,
        "has_name_frontmatter": "name:" in skill_text,
        "has_description_frontmatter": "description:" in skill_text,
        "has_harness_reference": "references/HARNESS.md" in skill_text,
        "has_mode_routing": "Mode Routing" in skill_text,
        "has_openai_display_name": "display_name:" in openai_yaml,
        "has_openai_default_prompt": "default_prompt:" in openai_yaml,
    }
    checks["ok"] = (
        not checks["missing_files"]
        and checks["has_name_frontmatter"]
        and checks["has_description_frontmatter"]
        and checks["has_harness_reference"]
        and checks["has_mode_routing"]
        and checks["has_openai_display_name"]
        and checks["has_openai_default_prompt"]
    )
    return checks


def main() -> int:
    args = parse_args()
    result = verify(Path(args.skill_dir))

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Skill directory: {result['skill_dir']}")
        if result["missing_files"]:
            print("Missing files:")
            for path in result["missing_files"]:
                print(f"  - {path}")
        else:
            print("Missing files: none")

        print(f"Frontmatter name: {result['has_name_frontmatter']}")
        print(f"Frontmatter description: {result['has_description_frontmatter']}")
        print(f"HARNESS reference: {result['has_harness_reference']}")
        print(f"Mode routing section: {result['has_mode_routing']}")
        print(f"openai.yaml display_name: {result['has_openai_display_name']}")
        print(f"openai.yaml default_prompt: {result['has_openai_default_prompt']}")
        print(f"Overall: {'PASS' if result['ok'] else 'FAIL'}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
