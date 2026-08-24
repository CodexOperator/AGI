#!/bin/bash
# agi-tree driver — orchestrates parallel pi agent dispatch + healing.
#
# Lives in the agi engine. Auto-detects project root by walking up
# from cwd until it finds agi-tree.config.json (legacy: autoresearch-tree.config.json).
#
# Usage:
#   driver.sh [--max-iters N] [--delay-mins M] [--smoke] [--no-heal]
#
# Project layout expected:
#   <project>/agi-tree.config.json
#   <project>/context/INJECTION.md
#   <project>/nodes/
#   <project>/sessions/   (created)
#   <project>/bin/snapshot-build-site.py
#   <project>/bin/render-context.py

set -euo pipefail

# Resolve real path so symlinks (e.g. ~/.local/bin/agi-tree) point back
# to the plugin dir, not the symlink dir.
SCRIPT_REAL="$(readlink -f "${BASH_SOURCE[0]}")"
PLUGIN_ROOT="$(cd "$(dirname "$SCRIPT_REAL")" && pwd)"
source "$PLUGIN_ROOT/lib/find-root.sh"

MAX_ITERS=1
DELAY_MINS=0
SMOKE=false
NO_HEAL=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-iters) MAX_ITERS="$2"; shift 2 ;;
    --delay-mins) DELAY_MINS="$2"; shift 2 ;;
    --smoke) SMOKE=true; shift ;;
    --no-heal) NO_HEAL=true; shift ;;
    -h|--help)
      cat <<HELP
agi-tree driver — thoughtgraph loop for agi

OPTIONS:
  --max-iters N      Run N iterations (default 1)
  --delay-mins M     Sleep M minutes between iters (default 0)
  --smoke            One dry pass: snapshot+render+METRICs, no agent dispatch
  --no-heal          Skip healer monitoring (debug)

PROJECT ROOT:
  Auto-detected by walking up from \$PWD looking for
  agi-tree.config.json (legacy name autoresearch-tree.config.json still works).

PLUGIN ROOT:
  $PLUGIN_ROOT
HELP
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

PROJECT_ROOT=$(find_project_root "$PWD") || {
  echo "ERR: not inside an agi-tree project (no agi-tree.config.json found above $PWD)" >&2
  exit 1
}
echo "[driver] PROJECT_ROOT=$PROJECT_ROOT"
echo "[driver] PLUGIN_ROOT=$PLUGIN_ROOT"

LOG="$PROJECT_ROOT/loop.log"
mkdir -p "$PROJECT_ROOT/sessions" "$PROJECT_ROOT/context" "$PROJECT_ROOT/nodes"

iter_run() {
  local n="$1"
  local ts
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "=== iter $n @ $ts ===" | tee -a "$LOG"

  # 1a. Derive nodes/goal/ from GOALS.md (plugin-only; no project-local override
  #     on purpose — project-local bin/*.py overrides are the H0 data-loss defect)
  if [[ -f "$PLUGIN_ROOT/bin/snapshot-goals.py" ]]; then
    AGI_TREE_PROJECT_ROOT="$PROJECT_ROOT" AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" \
      python3 "$PLUGIN_ROOT/bin/snapshot-goals.py" --strict-goals 2>&1 | tee -a "$LOG"
  fi

  # 1. Refresh nodes/ from build-site (idempotent rebuild)
  # Plugin scripts are canonical; project-local copies override if present.
  local SNAPSHOT_PY="$PLUGIN_ROOT/bin/snapshot-build-site.py"
  [[ -x "$PROJECT_ROOT/bin/snapshot-build-site.py" ]] && SNAPSHOT_PY="$PROJECT_ROOT/bin/snapshot-build-site.py"
  if [[ -f "$SNAPSHOT_PY" ]]; then
    AGI_TREE_PROJECT_ROOT="$PROJECT_ROOT" AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" \
      python3 "$SNAPSHOT_PY" 2>&1 | tee -a "$LOG"
  fi

  # 2. Render context → INJECTION.md
  local RENDER_PY="$PLUGIN_ROOT/bin/render-context.py"
  [[ -x "$PROJECT_ROOT/bin/render-context.py" ]] && RENDER_PY="$PROJECT_ROOT/bin/render-context.py"
  if [[ -f "$RENDER_PY" ]]; then
    AGI_TREE_PROJECT_ROOT="$PROJECT_ROOT" AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" \
      python3 "$RENDER_PY" "$PROJECT_ROOT/nodes" 2>&1 | tee -a "$LOG"
  fi

  # 3. Emit METRICs
  emit_metrics "$n"

  # 4. Pre-dispatch benchmark (attractiveness scores for transparency)
  python3 "$PLUGIN_ROOT/bin/benchmark.py" "$PROJECT_ROOT" 2>&1 | tee -a "$LOG" || true

  if [[ "$SMOKE" == "true" ]]; then
    echo "[smoke] skipping agent dispatch + heal" | tee -a "$LOG"
    return
  fi

  # 5. Spawn parallel pi agents w/ zoom-targeted contexts
  python3 "$PLUGIN_ROOT/bin/dispatch.py" "$PROJECT_ROOT" "$n" 2>&1 | tee -a "$LOG"

  # 6. Monitor + heal
  if [[ "$NO_HEAL" != "true" ]]; then
    python3 "$PLUGIN_ROOT/bin/heal.py" "$PROJECT_ROOT" "$n" 2>&1 | tee -a "$LOG"
  fi

  # 7. Post-wire: push agent verdicts back into node graph
  python3 "$PLUGIN_ROOT/bin/post_wire.py" "$PROJECT_ROOT" "$n" 2>&1 | tee -a "$LOG" || true

  # 8. Print summary
  python3 "$PLUGIN_ROOT/bin/cli.py" status "$n" 2>&1 | tee -a "$LOG" || true
}

emit_metrics() {
  local iter_n="$1"
  # Metric computation lives in bin/metrics.py (TODO.md H3) so it is testable
  # and so the primary metric is config-driven, never chain length.
  python3 "$PLUGIN_ROOT/bin/metrics.py" "$PROJECT_ROOT" 2>&1 | tee -a "$LOG"
}

for i in $(seq 1 "$MAX_ITERS"); do
  iter_run "$i"
  if [[ "$i" -lt "$MAX_ITERS" && "$DELAY_MINS" -gt 0 ]]; then
    echo "[driver] sleeping ${DELAY_MINS}m before iter $((i+1))..." | tee -a "$LOG"
    sleep "$((DELAY_MINS * 60))"
  fi
done

echo "INJECTION_FILE=$PROJECT_ROOT/context/INJECTION.md"
echo "SESSIONS_DIR=$PROJECT_ROOT/sessions"
exit 0
