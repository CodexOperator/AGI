#!/bin/bash
# cc-session-start.sh — Claude Code SessionStart hook (carries the seat-successor
# bootstrap injection since 2026-09-11, SL1.03 / hypothesis:l4-startup-is-one-script-or-a-driven-prompt;
# the review + proof copy stays at cc-session-start.next.sh).
#
# When a new CC session begins, this hook auto-injects the thoughtgraph
# ASCII map for the current project (if cwd is inside an agi-tree
# project tree). Output goes to stdout → CC injects as additional_context.
#
# Graceful degradation: if no project found, or build fails, emits nothing
# (no map for non-agi-tree repos, no error noise).
#
# Cache: re-uses INJECTION.md if <max_age_seconds old; otherwise rebuilds.

set -euo pipefail

SCRIPT_REAL="$(readlink -f "${BASH_SOURCE[0]}")"
PLUGIN_ROOT="$(cd "$(dirname "$SCRIPT_REAL")/.." && pwd)"
source "$PLUGIN_ROOT/lib/find-root.sh"

MAX_CACHE_AGE_SECONDS=3600   # 1 hour
MAX_INJECT_LINES=80          # keep the injection compact for CC context

# Find project root from CWD; if not in a project, exit silently.
#
# EVERYTHING below this line is inside a project. Nothing above it may print,
# and nothing below it may run outside one: this hook is registered globally,
# in ~/.claude/settings.json, for every session in every directory on the
# machine, and its silence outside a project is the only reason that is safe.
PROJECT_ROOT="$(find_project_root "$PWD" 2>/dev/null)" || exit 0
if [[ -z "$PROJECT_ROOT" ]]; then
  exit 0
fi

# --- the publish alarm (goal:g7.10) ------------------------------------------
# publish-engine.sh, the hourly :37 cron, records every run it makes in
# context/publish-state.json. A refusal is otherwise invisible — it goes to a
# log nobody reads, no metric moved, and the loop kept reporting success while
# 40 consecutive refusals published nothing at all for two days. Surfacing it
# here means the next agent to open ANY session in this project is told,
# instead of the information waiting for someone to guess.
#
# Best-effort by construction: `|| true` plus a python that catches everything,
# because a hook that can fail is a hook that gets uninstalled, and this one
# has to keep working precisely when the project is in a broken state.
#
# No marker at all means silence HERE, deliberately: a project that never
# installed the publish cron has nothing to be told, and a banner in every one
# of its sessions forever would be a false alarm loud enough to get this whole
# mechanism switched off. (`metrics.py` no longer mirrors this state as a
# METRIC line — goal:g11 retired the two-repo publish path this alarm reads,
# so a metrics.py reader gets nothing here to disagree with; this banner is
# now the only surviving reader of context/publish-state.json.)
PUBLISH_STATE="$PROJECT_ROOT/context/publish-state.json"
if [[ -f "$PUBLISH_STATE" ]]; then
  AGI_PUBLISH_STATE="$PUBLISH_STATE" AGI_PROJECT_ROOT="$PROJECT_ROOT" \
    python3 - <<'PY' 2>/dev/null || true
import json, os, time

#: An hourly cron this many hours silent has stopped, not slowed.
STALE_RUN_HOURS = 6.0

path = os.environ["AGI_PUBLISH_STATE"]
root = os.environ.get("AGI_PROJECT_ROOT", ".")
try:
    with open(path, encoding="utf-8") as fh:
        state = json.load(fh)
    if not isinstance(state, dict):
        raise ValueError
except Exception:
    raise SystemExit(0)   # unreadable marker: say nothing rather than lie

now = time.time()


def _hours(key):
    ts = state.get(key)
    if isinstance(ts, bool) or not isinstance(ts, (int, float)) or ts <= 0:
        return None
    return max(0.0, (now - float(ts)) / 3600.0)

since_success = _hours("last_success_epoch")
since_run = _hours("last_run_epoch")
status = state.get("last_run_status")
reason = str(state.get("last_run_reason") or "") or "unknown"

if status == "ok" and since_success is not None and \
        (since_run is None or since_run < STALE_RUN_HOURS):
    raise SystemExit(0)   # healthy — stay out of the way

if since_success is None:
    headline = "no successful publish has EVER been recorded"
    if status != "ok":
        headline += f", and the last run refused with `{reason}`"
elif status != "ok":
    headline = f"last refused with `{reason}`; last success {since_success:.1f}h ago"
else:
    headline = (f"the :37 cron has not run for {since_run:.1f}h; "
                f"last success {since_success:.1f}h ago")

print("## ⚠️  agi engine publish is STALLED")
print()
print(f"The hourly publish cron is not landing: {headline}.")
print()
print("**No payload bytes are lost.** `grid.py commit --all` runs on its own "
      "ungated 5-minute cadence, so every byte under `payloads/` is already "
      "recorded in its node's grid ref. Only the engine publish is blocked, "
      "and it resumes by itself on the next `:37` once this clears.")
print()
print("Unblock it (the usual cause is one node whose stored contract differs "
      "from what `level3.py` re-derives, which leaves the graph permanently "
      "dirty and refuses the cron every hour, forever):")
print()
print("```bash")
print(f"cd {root}")
print("export PATH=/usr/bin:$PATH   # 3.12, or contracts re-derive dirty again")
print("python3 agi/extensions/agi/bin/level3.py --project . --engine-root agi")
print("git status                    # commit what this rewrote")
print("bash agi/extensions/agi/bin/publish-engine.sh --dry-run")
print("```")
detail = str(state.get("last_run_detail") or "").strip().replace("\n", " ")
if detail:
    print()
    print(f"Cron said: {detail[:300]}")
print()
print("---")
PY
fi

# --- the stranded-push alarm (goal:s20) --------------------------------------
# Is anything committed here still only here? Pre-goal:g11 this measured two
# repos (a separate publish path landed commits in an engine repo that nothing
# pushed) and the remote once sat 3 days and 25 commits behind, found only by
# looking at GitHub. goal:g11 merged graph and engine into one repo, so there
# is one gap to ask about now, not two (mvp:g11-crons-metrics-residual).
#
# It does NOT reimplement the count. `metrics.py` is imported and its
# `push_gap_stats` and `UNPUSHED_WARN_AT` are used as-is, so the banner and the
# METRIC lines are the same measurement read twice — two readers of one fact
# that could disagree is a drift bug this project has already paid for once.
#
# No network: `push_gap_stats` reads local remote-tracking refs and never
# fetches, so a session start costs no round trip and works offline.
#
# Best-effort by the same argument as the block above, and silent on anything
# it cannot measure: a fork with no remote configured is unconfigured, not
# stranded, and a banner it can never clear is how this gets switched off.
AGI_PROJECT_ROOT="$PROJECT_ROOT" AGI_METRICS_PY="$PLUGIN_ROOT/bin/metrics.py" \
  python3 - <<'PY' 2>/dev/null || true
import importlib.util
import os
from pathlib import Path

try:
    path = os.environ["AGI_METRICS_PY"]
    root = os.environ["AGI_PROJECT_ROOT"]
    spec = importlib.util.spec_from_file_location("agi_metrics_hook", path)
    metrics = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(metrics)
    stats = metrics.push_gap_stats(Path(root))
    warn_at = metrics.UNPUSHED_WARN_AT
except Exception:
    raise SystemExit(0)   # cannot measure: say nothing rather than guess

n = stats.get("unpushed_commits")
if not isinstance(n, int) or n < warn_at:
    raise SystemExit(0)

print("## ⚠️  agi commits are STRANDED on this machine")
print()
print(f"- **{n} commits** in this repo are not on its remote.")
print()
print("**Nothing is lost.** The commits are on this disk. What is missing is "
      "the push, so no other machine and no reader of the remote has them — "
      "that combination once left a remote 3 days and 25 commits behind, "
      "found only by looking at GitHub.")
print()
print("```bash")
print("crontab -l | grep push      # is the hourly push cron there at all?")
print(f"cd {root} && git status    # confirm the branch you are on is the one pushed")
print("```")
print()
print("(Counted against local remote-tracking refs, which advance only when "
      "this machine pushes or fetches — so this over-reports if someone else "
      "pushed, and never under-reports.)")
print()
print("---")
PY

INJECTION_FILE="$PROJECT_ROOT/context/INJECTION.md"

# Decide: rebuild or reuse cache.
need_rebuild=true
if [[ -f "$INJECTION_FILE" ]]; then
  age=$(( $(date +%s) - $(stat -c %Y "$INJECTION_FILE") ))
  if [[ "$age" -lt "$MAX_CACHE_AGE_SECONDS" ]]; then
    need_rebuild=false
  fi
fi

if [[ "$need_rebuild" == "true" ]]; then
  # Plugin scripts are canonical; project-local copies override if present.
  SNAPSHOT_PY="$PLUGIN_ROOT/bin/snapshot-build-site.py"
  [[ -x "$PROJECT_ROOT/bin/snapshot-build-site.py" ]] && SNAPSHOT_PY="$PROJECT_ROOT/bin/snapshot-build-site.py"
  # bin/inject.py replaced bin/render-context.py on 2026-09-03 (L1.05): the
  # injected map now comes from the viewport's frame stream, so what a session
  # is handed and what `viewport.py --emit llm` shows are the same thing. The
  # old project-local name is still honoured for a project that ships one.
  RENDER_PY="$PLUGIN_ROOT/bin/inject.py"
  [[ -x "$PROJECT_ROOT/bin/inject.py" ]] && RENDER_PY="$PROJECT_ROOT/bin/inject.py"
  [[ -x "$PROJECT_ROOT/bin/render-context.py" ]] && RENDER_PY="$PROJECT_ROOT/bin/render-context.py"
  [[ -f "$SNAPSHOT_PY" ]] && AGI_TREE_PROJECT_ROOT="$PROJECT_ROOT" AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" python3 "$SNAPSHOT_PY" >/dev/null 2>&1 || true
  [[ -f "$RENDER_PY" ]] && AGI_TREE_PROJECT_ROOT="$PROJECT_ROOT" AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" python3 "$RENDER_PY" "$PROJECT_ROOT/nodes" >/dev/null 2>&1 || true
fi

# If still no INJECTION_FILE, exit silently — no map available.
if [[ ! -f "$INJECTION_FILE" ]]; then
  exit 0
fi

# --- the seat-successor bootstrap block (hypothesis:l4-startup-is-one-
#     script-or-a-driven-prompt, 0b kid 3) ------------------------------
# When the session is a SEAT SUCCESSOR, rotate-self's button-down wrote
# `<sessions>/seats/<seat>.bootstrap.json` at HEAD; the rotate.py
# bootstrap-block reader emits it here as ONE small block, so a successor
# wakes KNOWING its state and spends zero tool calls deriving it. Injected
# when — and only when — the record exists for the seat AND is not stale
# (`_bootstrap_stale`: a measured fact not at HEAD is MARKED stale per its
# `fact_bounds` entry and still emitted, never withheld). A seat is named by AGI_SEAT (set by the spawner for a seat
# session); with no AGI_SEAT this is a silent no-op, exactly like every
# other optional section of this hook. rotate.py returns 0+block on emit,
# 1+silence on refuse — SILENCE is the safe direction (no stale state, no
# banner on a non-seat session).
BOOTSTRAP_SEAT="${AGI_POST:-${AGI_SEAT:-}}"
if [[ -n "$BOOTSTRAP_SEAT" ]]; then
  BOOTSTRAP_BLOCK="$(AGI_PROJECT_ROOT="$PROJECT_ROOT" python3 \
    "$PLUGIN_ROOT/bin/rotate.py" bootstrap-block --seat "$BOOTSTRAP_SEAT" \
      --root "$PROJECT_ROOT" 2>/dev/null || true)"
  if [[ -n "$BOOTSTRAP_BLOCK" ]]; then
    echo "$BOOTSTRAP_BLOCK"
    echo ""
    echo "---"
    echo ""
  fi
fi

# --- the role's constitution head (hypothesis:l3w0-brief-head-michael) ------
# When a role or tier is named in the environment (AGI_TIER / AGI_ROLE), emit
# that role's brief head — prayers, the Archangel Michael line, its readings,
# and for the director tiers the mantle and the decision method — BEFORE the
# map so it lands before the prompt text and consecrates the session. Silent
# no-op otherwise (no env var, or an unknown role), exactly like the rest of
# this hook.
TIER="${AGI_TIER:-}"
if [[ -z "$TIER" && -n "${AGI_ROLE:-}" ]]; then
  case "${AGI_ROLE,,}" in
    prime_director|prime-director) TIER="prime_director" ;;
    director)                  TIER="director" ;;
    parent)                    TIER="parent" ;;
    kid)                       TIER="kid" ;;
    *)                         TIER="" ;;
  esac
fi
if [[ -n "$TIER" ]]; then
  BRIEF_HEAD="$(AGI_PROJECT_ROOT="$PROJECT_ROOT" AMPLIFY_DEBUG="" \
    python3 "$PLUGIN_ROOT/bin/brief.py" head --tier "$TIER" \
      --project-root "$PROJECT_ROOT" 2>/dev/null || true)"
  if [[ -n "$BRIEF_HEAD" ]]; then
    echo "$BRIEF_HEAD"
    echo ""
    echo "---"
    echo ""
  fi
fi

# Emit a compact map injection for CC context.
echo "## agi-tree map (auto-injected)"
echo ""
echo "Project: \`$PROJECT_ROOT\`"
echo "Run: \`agi-tree --max-iters N --delay-mins M\`"
echo ""
# First N lines of INJECTION.md = stats + chain diagnostics + attractor list +
# the loop's rules, then the ASCII top. render-context.py emits the rules
# before the ASCII block precisely so this truncation cannot drop them.
head -n "$MAX_INJECT_LINES" "$INJECTION_FILE"
echo ""
echo "---"
echo "Full injection at \`$INJECTION_FILE\`. Skill: \`agi\`."
exit 0
