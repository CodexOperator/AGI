#!/bin/bash
# make_shadow_fixture.sh <fixture-dir> [script-name]
# Build a TMP project in the goal:g11 layout and resolve PROJECT_ROOT the SAME
# way driver.sh does -- by SOURCING the engine's own lib/find-root.sh from
# inside <proj>/.agi/nodes/ and calling find_project_root. The shadow path is
# never retyped here or in the test that drives this script.
#
# find-root.sh is located from THIS SCRIPT's own path (../../lib/find-root.sh),
# never from an env var or an absolute path: the fixture must work in a clean
# checkout, in a worktree, and in a session scratch dir alike.
#
# Prints: "<resolved-project-root>" then "shadow=<path>" ("shadow=" when no
# script was requested).
set -euo pipefail

PROJ="${1:?usage: make_shadow_fixture.sh <fixture-dir> [script-name]}"
NAME="${2:-}"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIND_ROOT="$HERE/../../lib/find-root.sh"
[[ -f "$FIND_ROOT" ]] || { echo "ERR: no find-root.sh at $FIND_ROOT" >&2; exit 2; }

mkdir -p "$PROJ/.agi/nodes" "$PROJ/.agi/bin"
printf '{"metric_primary": "outcome_coverage"}\n' > "$PROJ/.agi/config.json"
printf '# goals\n' > "$PROJ/GOALS.md"

# Resolve exactly as driver.sh does: source the real rule, ask from inside
# the graph's own nodes/ dir.
PROJECT_ROOT="$(
  cd "$PROJ/.agi/nodes"
  source "$FIND_ROOT"
  find_project_root
)"
echo "$PROJECT_ROOT"

SHADOW=""
if [[ -n "$NAME" ]]; then
  SHADOW="$PROJECT_ROOT/bin/$NAME"
  printf '#!/usr/bin/env python3\n# shadow fixture: driver.sh prefers this over the engine copy\n' > "$SHADOW"
  chmod +x "$SHADOW"
fi
echo "shadow=$SHADOW"
