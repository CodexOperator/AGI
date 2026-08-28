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
# goal:g7.10 — EVERY exit from here is recorded, in machine-readable form, in
# `<project>/context/publish-state.json`. Refusing is a legitimate outcome;
# refusing *quietly* is not. This script is the `:37` cron, and it refused 40
# consecutive times while publishing nothing at all, from install on
# 2026-08-25 until someone checked by hand on 2026-08-27. Nothing caught it:
# the refusal went to a log nobody reads, no metric moved, `driver.sh --smoke`
# said nothing and the injected map said nothing. The marker is what
# `metrics.py` (hours_since_successful_publish, publish_blocked_reason) and
# `hooks/cc-session-start.sh` read, so a stall now moves a number and shouts at
# the next agent to open any session anywhere.
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

# --- the durable marker (goal:g7.10) ------------------------------------------
# One file, two readers: metrics.py turns it into METRIC lines, and the
# SessionStart hook turns it into a banner. It lives under context/ beside
# INJECTION.md — where this repo already keeps generated state — and NOT under
# nodes/, because gate 0 below refuses on any uncommitted change under nodes/,
# so a marker written there would arm the gate it exists to report on, on every
# run, forever.
STATE_FILE="$PROJECT_ROOT/context/publish-state.json"

# record_state <ok|refused> [reason-token] [human detail]
# Never fatal: failing to write the marker must not change the outcome of the
# run, and must not mask the exit code the caller is about to see.
record_state() {
  # --dry-run is a report, not a run. Writing state from it would let a
  # hand-run dry pass overwrite the cron's record of what really happened.
  [[ "$DRY_RUN" == "1" ]] && return 0
  mkdir -p "$(dirname "$STATE_FILE")" 2>/dev/null || true
  AGI_PUBLISH_STATE="$STATE_FILE" \
  AGI_PUBLISH_STATUS="$1" \
  AGI_PUBLISH_REASON="${2:-}" \
  AGI_PUBLISH_DETAIL="${3:-}" \
  AGI_PUBLISH_COMMIT="${GRAPH_COMMIT:-}" \
  python3 - <<'PY' || say "WARNING: could not write $STATE_FILE"
import json, os, time

path = os.environ["AGI_PUBLISH_STATE"]
status = os.environ["AGI_PUBLISH_STATUS"]

# Carry the last real publish forward. A refusal must never erase the record of
# when the engine last actually landed -- that timestamp is the whole alarm.
prior = {}
try:
    with open(path, encoding="utf-8") as fh:
        loaded = json.load(fh)
    if isinstance(loaded, dict):
        prior = loaded
except Exception:
    pass

now = int(time.time())
state = {
    "schema": 1,
    "last_run_epoch": now,
    "last_run_status": status,
    "last_run_reason": os.environ.get("AGI_PUBLISH_REASON", ""),
    "last_run_detail": os.environ.get("AGI_PUBLISH_DETAIL", ""),
    "last_success_epoch": prior.get("last_success_epoch"),
    "last_success_graph_commit": prior.get("last_success_graph_commit"),
}
if status == "ok":
    state["last_success_epoch"] = now
    state["last_success_graph_commit"] = os.environ.get("AGI_PUBLISH_COMMIT", "")

# Written whole then renamed: a hook or a metric reading mid-write would see a
# truncated file, and an unreadable marker reads as "never published".
tmp = path + ".tmp"
with open(tmp, "w", encoding="utf-8") as fh:
    json.dump(state, fh, indent=2, sort_keys=True)
    fh.write("\n")
os.replace(tmp, path)
PY
}

# The reassuring thing, said at the moment the fear arrives. When a publish
# stalls the reasonable assumption is that engine work is evaporating, and it
# is not: `grid.py commit --all` is a separate, ungated, 5-minute cron.
say_bytes_are_safe() {
  say "  Your payload bytes are NOT lost. \`grid.py commit --all\` runs on its own"
  say "  ungated 5-minute cadence, so every byte you edited under payloads/ is"
  say "  already recorded in its node's grid ref. Only the ENGINE PUBLISH is"
  say "  blocked, and it resumes by itself on the next :37 once this clears."
}

# refuse <reason-token> <human explanation...>
refuse() {
  local reason="$1"; shift
  say "REFUSING [$reason]: $*"
  say_bytes_are_safe
  record_state refused "$reason" "$*"
  exit 1
}

# Anything that fails outside a gate -- level3.py crashing, the grid commit
# dying, a python that is not there -- used to exit non-zero with no marker at
# all, which reads downstream as "the cron never ran". Recorded like any other
# refusal so that case is visible too.
on_unexpected_error() {
  local rc=$?
  trap - ERR
  say "REFUSING [unexpected-failure]: a step exited ${rc}. Nothing published."
  say_bytes_are_safe
  record_state refused "unexpected-failure" "a step exited ${rc}"
  exit "$rc"
}
trap on_unexpected_error ERR

# --- gate 0: the graph must be committed --------------------------------------
# A publish is a derivation. If nodes/ has uncommitted changes then the engine
# commit below would cite a graph state that exists nowhere but this machine.
#
# This gate is CORRECT and must not be weakened. A single node whose stored
# contract differs from what level3.py re-derives leaves the graph permanently
# dirty and arms it forever -- one character of YAML quoting did exactly that
# (goal:g6.5), and the 3.11/3.12 f-string flap (goal:s19) then made it
# intermittent, which is worse. The fix for both is upstream of here.
if [[ -n "$(git -C "$PROJECT_ROOT" status --porcelain -- nodes/ GOALS.md)" ]]; then
  refuse "graph-dirty" "the graph has uncommitted changes under nodes/ or GOALS.md; commit them first — a published engine must cite a real graph commit"
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
  refuse "contracts-disagree" "the graph disagrees with its own contracts; nothing published"
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
  # A successful publish that wrote no new bytes. Recorded as success, not as
  # a no-op: the engine matches the graph, which is the entire point, and
  # calling it "nothing happened" is what let a healthy run and a 40-times
  # refusal look identical from outside.
  say "engine already matches the graph; nothing to commit"
  record_state ok "" "engine already matched the graph @ ${GRAPH_COMMIT}"
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
record_state ok "" "committed ${CHANGED} file(s) (graph @ ${GRAPH_COMMIT})"
