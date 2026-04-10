#!/usr/bin/env bash
set -euo pipefail

REPO_RAW_BASE="${REPO_RAW_BASE:-https://raw.githubusercontent.com/edenSu-git/mc-material-skill/main}"
TARGET_DIR="${HOME}/.codex/skills/minecraft-circle-generator"
SCRIPTS_DIR="${TARGET_DIR}/scripts"

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "缺少依赖命令: $1" >&2
    exit 1
  fi
}

need_cmd curl
need_cmd python3

mkdir -p "${SCRIPTS_DIR}"

echo "Installing minecraft circle generator skill to ${TARGET_DIR} ..."
curl -fsSL "${REPO_RAW_BASE}/SKILL.md" -o "${TARGET_DIR}/SKILL.md"
curl -fsSL "${REPO_RAW_BASE}/scripts/mc_material_calc.py" -o "${SCRIPTS_DIR}/mc_material_calc.py"
chmod +x "${SCRIPTS_DIR}/mc_material_calc.py"

echo
echo "安装完成。"
echo "测试命令："
echo "python3 \"${SCRIPTS_DIR}/mc_material_calc.py\" --diameter 31 --fill-mode hollow --shape-layer 15 --shell-thickness 1 --build-type dome --material glass"
echo
echo "在 Codex 中可用触发词：/minecraft-circle-generator"
