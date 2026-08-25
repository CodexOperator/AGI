#!/usr/bin/env bash
# publish-engine.sh — write the engine repo from the graph, then commit it.
#
# GOALS.md G6.5 step 2: "after G6.3, cron may stitch and commit the engine."
# G6.3 is complete and G6.1's read direction closed, so this is now a legal
# operation. It is still written to refuse far more often than it acts.
#
# The sequence, and every step is a gate rather than a stage:
#
#   1. re-derive contracts FROM THE GRID       (level3.py --from-grid)
#   2. verify the graph against ITSELF         (stitch --verify --from-grid --strict)
#   3. publish                                  (stitch --out ENGINE --from-grid --publish)
#   4. commit the engine, citing the graph commit that produced it
#
# Step 2 is the one that matters. Publishing a graph that disagrees with its own
# contracts would put drift into the engine atomically and cleanly, which is
# worse than not publishing at all — G6.7's own argument about an atomic
# publisher of corrupt content, arriving here first.
#
# What it will NOT do, by construction:
#   - publish into a dirty engine tree (stitch --publish refuses; that is what
#     makes every overwritten byte recoverable with `git checkout .`)
#   - publish when the graph has uncommitted node changes (a publish must be
#     attributable to a graph commit, or step 4's message is a lie)
#   - push. Pushing is the existing hourly cron's job; this only commits.
#
# Usage: publish-engine.sh [--engine-root DIR] [--dry-run]
set -euo pipefail

SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
BIN_DIR="$(dirname "$SCRIPT")"
PLUGIN_ROOT="$(dirname "$BIN_DIR")"
DEFAULT_ENGINE_ROOT="$(dirname "$(dirname "$PLUGIN_ROOT")")"

ENGINE_ROOT="$DEFAULT_ENGINE_ROOT"
DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --engine-root) ENGINE_ROOT="$2"; shift 2 ;;
    --dry-run)     DRY_RUN=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

PROJECT_ROOT="$(bash "$PLUGIN_ROOT/lib/find-root.sh" 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

say() { echo "[publish-engine] $*"; }

# --- gate 0: the graph must be committed --------------------------------------
# A publish is a derivation. If nodes/ has uncommitted changes then the engine
# commit below would cite a graph state that exists nowhere but this machine.
if [[ -n "$(git -C "$PROJECT_ROOT" status --porcelain -- nodes/ GOALS.md)" ]]; then
  say "REFUSING: the graph has uncommitted changes under nodes/ or GOALS.md."
  say "          Commit them first — a published engine must cite a real graph commit."
  exit 1
fi

GRAPH_COMMIT="$(git -C "$PROJECT_ROOT" rev-parse --short HEAD)"

# --- step 1: contracts re-derive from the grid, not from the engine tree ------
say "re-deriving contracts from the grid"
python3 "$BIN_DIR/level3.py" --project "$PROJECT_ROOT" \
        --engine-root "$ENGINE_ROOT" --from-grid

# level3.py rewrites node bodies, so the grid needs the new versions before the
# publish reads them back out. Without this the published tree would be one
# derivation behind the nodes that describe it.
python3 "$BIN_DIR/grid.py" commit --all --prefix "publish: "

# --- gate 2: the graph must agree with itself ---------------------------------
say "verifying the graph against its own payloads"
if ! python3 "$BIN_DIR/stitch.py" --project "$PROJECT_ROOT" --verify --from-grid \
        --engine-root "$ENGINE_ROOT" --strict; then
  say "REFUSING: the graph disagrees with its own contracts. Nothing published."
  exit 1
fi

if [[ "$DRY_RUN" == "1" ]]; then
  say "--dry-run: all gates passed; would publish to $ENGINE_ROOT and commit"
  exit 0
fi

# --- step 3: publish ----------------------------------------------------------
say "publishing to $ENGINE_ROOT"
python3 "$BIN_DIR/stitch.py" --project "$PROJECT_ROOT" --out "$ENGINE_ROOT" \
        --from-grid --publish --engine-root "$ENGINE_ROOT"

# --- step 4: commit the engine, citing what produced it -----------------------
if [[ -z "$(git -C "$ENGINE_ROOT" status --porcelain)" ]]; then
  say "engine already matches the graph; nothing to commit"
  exit 0
fi

CHANGED="$(git -C "$ENGINE_ROOT" status --porcelain | wc -l | tr -d ' ')"
git -C "$ENGINE_ROOT" add -A
git -C "$ENGINE_ROOT" commit -q -m "published from the graph @ ${GRAPH_COMMIT}

${CHANGED} file(s) written by stitch.py --from-grid --publish. This commit is a
derivation, not an edit: every byte came out of a node's grid ref in the graph
repo at ${GRAPH_COMMIT}. See GOALS.md G6.1/G6.5.
"
say "committed ${CHANGED} file(s) to $ENGINE_ROOT (graph @ ${GRAPH_COMMIT})"
