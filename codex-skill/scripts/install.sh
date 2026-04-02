#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEST_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
DEST_DIR="${DEST_ROOT}/cli-anything"

FORCE=0
VERIFY=0
SYNC=0

usage() {
  cat <<'EOF'
Usage: install.sh [--force] [--verify] [--sync] [--dest-root PATH]

Options:
  --force        Replace an existing installation.
  --verify       Run bundle verification after install.
  --sync         Refresh bundled HARNESS/command references from cli-anything-plugin first.
  --dest-root    Override the skills root directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.
  -h, --help     Show this help message.
EOF
}

resolve_python() {
  if command -v python3 >/dev/null 2>&1; then
    command -v python3
    return 0
  fi
  if command -v python >/dev/null 2>&1; then
    command -v python
    return 0
  fi
  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE=1
      shift
      ;;
    --verify)
      VERIFY=1
      shift
      ;;
    --sync)
      SYNC=1
      shift
      ;;
    --dest-root)
      if [[ $# -lt 2 ]]; then
        echo "--dest-root requires a path argument" >&2
        exit 1
      fi
      DEST_ROOT="$2"
      DEST_DIR="${DEST_ROOT}/cli-anything"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

PYTHON_BIN="$(resolve_python || true)"
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "Python is required to install or verify the Codex skill." >&2
  exit 1
fi

if [[ "${SYNC}" -eq 1 ]]; then
  "${PYTHON_BIN}" "${SCRIPT_DIR}/sync_from_plugin.py"
fi

mkdir -p "${DEST_ROOT}"

if [[ -e "${DEST_DIR}" ]]; then
  if [[ "${FORCE}" -ne 1 ]]; then
    echo "Refusing to overwrite existing skill: ${DEST_DIR}" >&2
    echo "Re-run with --force to replace it." >&2
    exit 1
  fi
  rm -rf "${DEST_DIR}"
fi

cp -R "${SKILL_DIR}" "${DEST_DIR}"

if [[ "${VERIFY}" -eq 1 ]]; then
  "${PYTHON_BIN}" "${SCRIPT_DIR}/verify_install.py" "${DEST_DIR}"
fi

echo "Installed Codex skill to: ${DEST_DIR}"
echo "Restart Codex to pick up the new skill."
