#!/bin/bash
# find-root.sh — locate project root by walking up looking for autoresearch-tree.config.json.
# Source from any other script: `source <plugin>/lib/find-root.sh && PROJECT_ROOT=$(find_project_root)`

find_project_root() {
  local d="${1:-$PWD}"
  while [[ "$d" != "/" ]]; do
    if [[ -f "$d/autoresearch-tree.config.json" ]]; then
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
    echo "ERR: no autoresearch-tree.config.json found above $(pwd)" >&2
    exit 1
  }
  echo "$PROJECT_ROOT"
fi
