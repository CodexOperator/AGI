#!/bin/bash
# agi driver — orchestrates parallel pi agent dispatch + healing.
#
# Lives in the agi engine. Auto-detects the project root by walking up from
# cwd to the nearest enclosing `.agi/` holding config.json (goal:g11); a
# legacy agi-tree.config.json / autoresearch-tree.config.json still resolves.
#
# Usage:
#   driver.sh [--max-iters N] [--delay-mins M] [--smoke] [--no-heal]
#
# Project layout expected (PROJECT_ROOT = <repo>/.agi):
#   <repo>/.agi/config.json
#   <repo>/.agi/context/INJECTION.md
#   <repo>/.agi/nodes/
#   <repo>/.agi/sessions/   (created)
#   NEVER <repo>/.agi/bin/snapshot-build-site.py or render-context.py — a
#   project-local copy shadows the engine's and has wiped a corpus (H0/H0b).

set -euo pipefail

# Resolve real path so symlinks (e.g. ~/.local/bin/agi) point back
# to the plugin dir, not the symlink dir.
SCRIPT_REAL="$(readlink -f "${BASH_SOURCE[0]}")"
PLUGIN_ROOT="$(cd "$(dirname "$SCRIPT_REAL")" && pwd)"
source "$PLUGIN_ROOT/lib/find-root.sh"

MAX_ITERS=1
DELAY_MINS=0
SMOKE=false
NO_HEAL=false
TARGET=""
LEVEL=""
TIER=""

# ---------------------------------------------------------------------------
# Verb router (goal:g1.10, L1.06). `agi <verb> [args]` runs a command the GRAPH
# declares, not one this script hardcodes.
#
# The whole point is that the verb list is graph content: `.geometry/commands.md`
# declares it, `commands.py` resolves it, and adding `agi view` is a node edit
# rather than a change here. A `case` arm per verb would put the list back in
# the shell -- a fifth prose copy of the command table, which is exactly the
# drift `goal:g1.10` measured and ended.
#
# A bare first word that is not a flag IS a verb. Flags keep working untouched,
# so `agi --max-iters 5` and `agi view` are both valid and neither knows about
# the other.
# ---------------------------------------------------------------------------
if [[ $# -gt 0 && "$1" != -* ]]; then
  VERB="$1"; shift
  ROOT_FOR_VERB="$(find_project_root "$PWD" 2>/dev/null)" || {
    echo "ERR: \`agi $VERB\` needs to be run inside a project (no enclosing .agi/)" >&2
    exit 1
  }
  # `--` before the pass-through args, and `--root` before the verb: without
  # both, argparse in commands.py claims a flag meant for the command --
  # `agi write <id> <script> --dry-run` died on "unrecognized arguments:
  # --dry-run", which is the router eating its passenger's mail.
  exec python3 "$PLUGIN_ROOT/bin/commands.py" --root "$ROOT_FOR_VERB" \
    run "$VERB" -- "$@"
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-iters) MAX_ITERS="$2"; shift 2 ;;
    --delay-mins) DELAY_MINS="$2"; shift 2 ;;
    --smoke) SMOKE=true; shift ;;
    --no-heal) NO_HEAL=true; shift ;;
    --target) TARGET="$2"; shift 2 ;;
    --level) LEVEL="$2"; shift 2 ;;
    --tier) TIER="$2"; shift 2 ;;
    -h|--help)
      cat <<HELP
agi driver — the thoughtgraph loop

OPTIONS:
  --max-iters N      Run N iterations (default 1)
  --delay-mins M     Sleep M minutes between iters (default 0)
  --smoke            One dry pass: snapshot+render+METRICs, no agent dispatch
  --no-heal          Skip healer monitoring (debug)
  --target ID        Aim every slot at node ID (default: attractiveness scoring)
  --level L          Zoom level for --target: big|small|auto (default small)
  --tier T           Spawn tier: kid|parent (default kid). Selects the model
                     from harnesses.<h>.models[T] AND the brief from brief.py.

PROJECT ROOT:
  Auto-detected by walking up from \$PWD to the nearest .agi/config.json
  (legacy agi-tree.config.json / autoresearch-tree.config.json still work).

PLUGIN ROOT:
  $PLUGIN_ROOT
HELP
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

PROJECT_ROOT=$(find_project_root "$PWD") || {
  echo "ERR: not inside an agi project (no .agi/config.json or agi-tree.config.json found above $PWD)" >&2
  exit 1
}
echo "[driver] PROJECT_ROOT=$PROJECT_ROOT"
echo "[driver] PLUGIN_ROOT=$PLUGIN_ROOT"

# Provider credentials (goal:g1.8). ONE file holds them, it is sourced here,
# and everything below inherits — dispatch.py, pi, and every pi child. Sourced
# after root resolution and before any dispatch, so the file found belongs to
# the project actually being run.
#
# The path is NOT written here. `nodes/.geometry/secrets.md` declares it and
# `bin/envfile.py` resolves it (goal:g10.2) — the same fact `bin/env-get.sh`
# asks for, stated once in the graph instead of twice in shell. The check runs
# every pass so a missing key is reported by `--smoke`, not discovered later
# inside pi; it reports and never refuses, and it never prints a value.
AGI_ENV_FILE="$(python3 "$PLUGIN_ROOT/bin/envfile.py" "$PROJECT_ROOT" --what env-file 2>/dev/null || true)"
python3 "$PLUGIN_ROOT/bin/envfile.py" "$PROJECT_ROOT" 2>&1 | sed 's/^/[driver] /' || true
if [[ -n "$AGI_ENV_FILE" && -f "$AGI_ENV_FILE" ]]; then
  echo "[driver] env <- $AGI_ENV_FILE"
  set -a
  # shellcheck disable=SC1090
  source "$AGI_ENV_FILE"
  set +a
fi

LOG="$PROJECT_ROOT/loop.log"
mkdir -p "$PROJECT_ROOT/sessions" "$PROJECT_ROOT/context" "$PROJECT_ROOT/nodes"

# Engine drift check (L9 pinning gap, goal:g8.1). Reads engine_commit (or
# engine_ref) from the project config and warns if the engine checkout's HEAD
# does not match. Non-fatal: prints a warning line and continues. Silent when
# the field is absent (i.e. projects that do not use pinning are unaffected).
#
# Config is resolved against PROJECT_ROOT first (.agi/config.json for the
# goal:g11 layout, then agi-tree.config.json for the legacy layout).
# That matters because the same PROJECT_ROOT value the loop uses is the one
# whose engine_commit we mean to check, regardless of layout.
if [[ -z "${SKIP_ENGINE_DRIFT_CHECK:-}" ]]; then
  python3 -c "
import json, subprocess, sys
from pathlib import Path

proot = Path('$PROJECT_ROOT')

# Config is at PROJECT_ROOT/config.json (goal:g11) OR agi-tree.config.json (legacy)
# PROJECT_ROOT is the .agi/ dir itself when resolved by find-root.sh phase 0
for cname in ['config.json', 'agi-tree.config.json', 'autoresearch-tree.config.json']:
    cpath = proot / cname
    if cpath.exists():
        break
else:
    sys.exit(0)

try:
    cfg = json.loads(cpath.read_text())
except Exception:
    sys.exit(0)

engine_commit = cfg.get('engine_commit') or cfg.get('engine_ref')
if not engine_commit:
    sys.exit(0)  # not pinned, silent

try:
    result = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        cwd='$PLUGIN_ROOT',
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        sys.exit(0)
    actual = result.stdout.strip()
except Exception:
    sys.exit(0)

if actual == engine_commit:
    print(f'[driver] engine pinned OK: {actual[:12]} matches engine_commit')
else:
    print(f'[driver] DRIFT WARNING: engine HEAD is {actual[:12]} but config pins {engine_commit[:12]}', file=sys.stderr)
    print(f'[driver]   Fix: git -C $PLUGIN_ROOT pull, or update engine_commit in {cname}', file=sys.stderr)
" 2>&1 | tee -a "$LOG" || true
fi

claim_iter() {
  python3 "$PLUGIN_ROOT/bin/locations.py" "$PROJECT_ROOT" --claim-iter "$@"
}

# Dispatched agents inherit AGI_LOOP as a full spawn label (e.g.
# hypothesis:x@s1), which is never a bare loop label. Honor AGI_LOOP only
# when it is one, so a kid's `driver.sh --smoke` verification never crashes
# on the spawn env it was handed (hypothesis:l3-dispatch-env-leaks-into-tests).
# A conductor passes the loop explicitly via CURRENT_LOOP, which always wins.
pick_loop() {
  # $1 = nameref to fill with the resolved loop ('' means: let
  # locations.py fall back to config loop / newest loop on disk).
  local -n out="$1"
  out="${CURRENT_LOOP:-}"
  # CURRENT_LOOP always wins. Only fall back to AGI_LOOP when it is a bare
  # loop label; a dispatched spawn label is ignored, and locations.py makes
  # the fallback (config loop / newest loop on disk) for an empty loop.
  if [[ -z "$out" ]]; then
    if [[ -n "${AGI_LOOP:-}" && "$AGI_LOOP" =~ ^[A-Za-z][A-Za-z0-9_-]*$ ]]; then
      out="$AGI_LOOP"
    else
      out=""
    fi
  fi
}

iter_run() {
  local raw_iter
  # CURRENT_LOOP is optional: --loop is omitted when neither it nor
  # $AGI_LOOP is set, and locations.py falls back to config `loop`, then
  # the newest loop on disk, then legacy numbering (set -u safe).
  # Sanitized so a dispatched AGI_LOOP spawn label is ignored, not crashed on.
  local loop
  pick_loop loop
  if [[ -n "$loop" ]]; then
    raw_iter=$(claim_iter --loop "$loop")
  else
    raw_iter=$(claim_iter)
  fi
  local n="$raw_iter"
  local n_display="$raw_iter"
  if [[ "$raw_iter" =~ ^[0-9]+$ ]]; then
    n_display=$(printf "%03d" "$raw_iter")
  fi
  local ts
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "=== iter $n_display @ $ts ===" | tee -a "$LOG"

  # 1a. Render GOALS.md FROM nodes/goal/ (goal:g6.9 — the nodes are the source;
  #     the document is a flat reading convenience). This direction cannot
  #     prune: it only ever writes the document. The legacy GOALS.md -> nodes
  #     import is `--from-doc` and is NOT run by the loop, because it deletes
  #     every goal node the document fails to mention (H0i's shape).
  #     Plugin-only, no project-local override on purpose — project-local
  #     bin/*.py overrides are the H0 data-loss defect.
  if [[ -f "$PLUGIN_ROOT/bin/snapshot-goals.py" ]]; then
    AGI_TREE_PROJECT_ROOT="$PROJECT_ROOT" AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" \
      python3 "$PLUGIN_ROOT/bin/snapshot-goals.py" --render --strict-goals 2>&1 | tee -a "$LOG"
  fi

  # 1. Refresh nodes/ from build-site (idempotent rebuild)
  # Plugin scripts are canonical; project-local copies override if present.
  local SNAPSHOT_PY="$PLUGIN_ROOT/bin/snapshot-build-site.py"
  [[ -x "$PROJECT_ROOT/bin/snapshot-build-site.py" ]] && SNAPSHOT_PY="$PROJECT_ROOT/bin/snapshot-build-site.py"
  if [[ -f "$SNAPSHOT_PY" ]]; then
    AGI_TREE_PROJECT_ROOT="$PROJECT_ROOT" AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" \
      python3 "$SNAPSHOT_PY" 2>&1 | tee -a "$LOG"
  fi

  # 2. Render context → INJECTION.md, from the viewport's own frame stream.
  #
  # `bin/inject.py` replaced `bin/render-context.py` on 2026-09-03 (L1.05).
  # The map a session is handed is now, by construction, the thing
  # `viewport.py --emit llm` shows — before this, the injected map came from a
  # fourth tree renderer no human ever looked at.
  #
  # The project-root override is KEPT, and so is the rail around it: a stale
  # `<project>/bin/*.py` silently shadows the engine's own and has wiped a
  # node corpus once (H0/H0b, S1). Both names are checked so a project that
  # still ships the old script keeps rendering rather than silently stopping.
  local RENDER_PY="$PLUGIN_ROOT/bin/inject.py"
  [[ -x "$PROJECT_ROOT/bin/inject.py" ]] && RENDER_PY="$PROJECT_ROOT/bin/inject.py"
  [[ -x "$PROJECT_ROOT/bin/render-context.py" ]] && RENDER_PY="$PROJECT_ROOT/bin/render-context.py"
  if [[ -f "$RENDER_PY" ]]; then
    AGI_TREE_PROJECT_ROOT="$PROJECT_ROOT" AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" \
      python3 "$RENDER_PY" "$PROJECT_ROOT/nodes" 2>&1 | tee -a "$LOG"
  fi

  # 3. Emit METRICs
  emit_metrics "$n"

  # 4. Pre-dispatch chain judgment — REMOVED 2026-08-31, see goal:g4.3 (H4b).
  #
  # This line was `benchmark.py "$PROJECT_ROOT" ... || true`, and it could
  # never have worked: `benchmark.py` takes a positional CHAIN ID (`idea:foo`)
  # and was handed a directory path, so even with its `ollama` dependency
  # installed it would have tried to judge a chain named after the project
  # root. Without ollama it printed one ERR line and exited 1, which `|| true`
  # swallowed. Confirmed live on 2026-08-31: one ERR line, every run.
  #
  # The consequence is not cosmetic. `benchmark.py` is what writes
  # `closed_chains.txt`, and `dispatch.py` reads that file to stop re-picking
  # a chain it has already judged finished. Since it never ran, no chain has
  # ever been closed, and target selection has been choosing from the full set
  # every iteration. Re-enabling it needs a per-chain loop, a config gate, and
  # the dependency actually present — a design job, not a fixed argument, so
  # the call is removed rather than repaired in place.
  #
  # It also does NOT reach `src/chain_engine/ranking.py`, contrary to what
  # goal:g4.3 said before this was traced; that module is reached through
  # `chain_engine/queries.py` instead.

  # 4b. Write guard: detect unsanctioned node edits (warn only, non-fatal)
  python3 "$PLUGIN_ROOT/bin/write_guard.py" check 2>&1 | tee -a "$LOG" || true

  if [[ "$SMOKE" == "true" ]]; then
    echo "[smoke] skipping agent dispatch + heal" | tee -a "$LOG"
    return
  fi

  # 5. Spawn pi agents w/ zoom-targeted contexts.
  # --target aims every slot at one node instead of letting attractiveness
  # scoring choose. Without it a single-slot run is unsteerable: _pick_targets
  # short-circuits at n<=1 to an untargeted big-zoom slot, so the one kid you
  # dispatch always scaffolds a parentless idea and explores where scoring
  # points. A dispatch that cannot be aimed cannot be a parent's kid.
  DISPATCH_ARGS=()
  [[ -n "$TARGET" ]] && DISPATCH_ARGS+=(--target "$TARGET")
  [[ -n "$LEVEL" ]] && DISPATCH_ARGS+=(--level "$LEVEL")
  # goal:g4.8 -- `dispatch.py` has taken --tier since goal:g4.6 and the driver
  # never passed it, so the parent tier was unreachable from the documented
  # entry point: `driver.sh --tier parent` silently spawned a kid, on the kid
  # model, with the kid brief. Found 2026-09-02 by checking before trusting it.
  [[ -n "$TIER" ]] && DISPATCH_ARGS+=(--tier "$TIER")
  python3 "$PLUGIN_ROOT/bin/dispatch.py" "$PROJECT_ROOT" "$n" \
    "${DISPATCH_ARGS[@]+"${DISPATCH_ARGS[@]}"}" 2>&1 | tee -a "$LOG"

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
