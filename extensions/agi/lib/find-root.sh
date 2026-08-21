#!/bin/bash
# find-root.sh — locate project root by walking up looking for agi-tree.config.json.
# Source from any other script: `source <plugin>/lib/find-root.sh && PROJECT_ROOT=$(find_project_root)`
#
# Compatibility window: the legacy marker autoresearch-tree.config.json is still
# accepted so existing projects keep working. New projects use agi-tree.config.json.

# Canonical first, legacy second. Order matters: agi_tree_config_path returns the
# first that exists, so a project carrying both resolves to the canonical one.
AGI_TREE_CONFIG_NAMES=("agi-tree.config.json" "autoresearch-tree.config.json")

# Print the config file path inside $1, or return 1 if the dir is not a project.
agi_tree_config_path() {
  local d="$1" name
  for name in "${AGI_TREE_CONFIG_NAMES[@]}"; do
    if [[ -f "$d/$name" ]]; then
      echo "$d/$name"
      return 0
    fi
  done
  return 1
}

find_project_root() {
  local d="${1:-$PWD}"
  while [[ "$d" != "/" ]]; do
    if agi_tree_config_path "$d" >/dev/null; then
      echo "$d"
      return 0
    fi
    d="$(dirname "$d")"
  done
  return 1
}

# When executed (not sourced), print the resolved root or exit 1.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  PROJECT_ROOT=$(find_project_root "${1:-$PWD}") || {
    echo "ERR: no agi-tree.config.json found above $(pwd)" >&2
    exit 1
  }
  echo "$PROJECT_ROOT"
fi
