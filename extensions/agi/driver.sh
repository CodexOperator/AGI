#!/bin/bash
# autoresearch-tree driver — orchestrates parallel pi agent dispatch + healing.
#
# Lives in pi-autoresearch plugin. Auto-detects project root by walking up
# from cwd until it finds autoresearch-tree.config.json.
#
# Usage:
#   driver.sh [--max-iters N] [--delay-mins M] [--smoke] [--no-heal]
#
# Project layout expected:
#   <project>/autoresearch-tree.config.json
#   <project>/context/INJECTION.md
#   <project>/nodes/
#   <project>/sessions/   (created)
#   <project>/bin/snapshot-build-site.py
#   <project>/bin/render-context.py

set -euo pipefail

# Resolve real path so symlinks (e.g. ~/.local/bin/autoresearch-tree) point back
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
autoresearch-tree driver — capillary DAG loop for pi-autoresearch

OPTIONS:
  --max-iters N      Run N iterations (default 1)
  --delay-mins M     Sleep M minutes between iters (default 0)
  --smoke            One dry pass: snapshot+render+METRICs, no agent dispatch
  --no-heal          Skip healer monitoring (debug)

PROJECT ROOT:
  Auto-detected by walking up from \$PWD looking for
  autoresearch-tree.config.json.

PLUGIN ROOT:
  $PLUGIN_ROOT
HELP
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

PROJECT_ROOT=$(find_project_root "$PWD") || {
  echo "ERR: not inside an autoresearch-tree project (no autoresearch-tree.config.json found above $PWD)" >&2
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

  # 1. Refresh nodes/ from build-site (idempotent rebuild)
  # Plugin scripts are canonical; project-local copies override if present.
  local SNAPSHOT_PY="$PLUGIN_ROOT/bin/snapshot-build-site.py"
  [[ -x "$PROJECT_ROOT/bin/snapshot-build-site.py" ]] && SNAPSHOT_PY="$PROJECT_ROOT/bin/snapshot-build-site.py"
  if [[ -f "$SNAPSHOT_PY" ]]; then
    AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" python3 "$SNAPSHOT_PY" 2>&1 | tee -a "$LOG"
  fi

  # 2. Render context → INJECTION.md
  local RENDER_PY="$PLUGIN_ROOT/bin/render-context.py"
  [[ -x "$PROJECT_ROOT/bin/render-context.py" ]] && RENDER_PY="$PROJECT_ROOT/bin/render-context.py"
  if [[ -f "$RENDER_PY" ]]; then
    AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" python3 "$RENDER_PY" "$PROJECT_ROOT/nodes" 2>&1 | tee -a "$LOG"
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
  PROJECT_ROOT="$PROJECT_ROOT" PLUGIN_ROOT="$PLUGIN_ROOT" python3 - <<PYEOF | tee -a "$LOG"
import os, sys
from pathlib import Path
root = Path(os.environ["PROJECT_ROOT"])
plugin_root = Path(os.environ["PLUGIN_ROOT"])
# Engine modules live in plugin's src/ (post-migration). Project's src/ wins
# if present, so projects can override engine modules locally.
proj_src = root / "src"
if (proj_src / "graph_core").is_dir():
    sys.path.insert(0, str(proj_src))
sys.path.insert(0, str(plugin_root / "src"))
from collections import defaultdict
from graph_core.loader import load_directory
from graph_core.edge import Edge

g, loaded = load_directory(root / "nodes")
for ln in loaded:
    for parent_id in ln.node.parents:
        if g.has_node(parent_id):
            try:
                g.add_edge(Edge(source_id=parent_id, target_id=ln.node.id, relation="spawns"))
            except Exception:
                pass
            pn = g.get_node(parent_id)
            if pn is not None:
                pn.children.add(ln.node.id)

def longest(g):
    cache = {}
    def d(nid):
        if nid in cache: return cache[nid]
        n = g.get_node(nid)
        if n is None or not n.children:
            cache[nid] = 0; return 0
        best = 0
        for c in n.children:
            if c == nid: continue
            best = max(best, d(c) + 1)
        cache[nid] = best; return best
    if not g.node_ids: return 0
    return max(d(nid) for nid in g.node_ids)

by_type = defaultdict(int)
for n in g.nodes: by_type[n.type] += 1

mvp_count = by_type.get("mvp", 0)
hyp_count = by_type.get("hypothesis", 1)
outcome_coverage = mvp_count / max(hyp_count, 1)
non_leaf = [n for n in g.nodes if n.children]
branching = sum(len(n.children) for n in non_leaf) / max(len(non_leaf), 1)
avg_depth = sum(len(n.parents) for n in g.nodes) / max(len(g), 1)

print(f"METRIC longest_chain_length={longest(g)}")
print(f"METRIC avg_chain_depth={avg_depth:.2f}")
print(f"METRIC mvp_count={mvp_count}")
print(f"METRIC outcome_coverage={outcome_coverage:.3f}")
print(f"METRIC chain_branching_factor={branching:.2f}")
print(f"METRIC node_count={len(g)}")
print(f"METRIC edge_count={g.edge_count}")
PYEOF
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
