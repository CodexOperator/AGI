#!/bin/bash
# cc-session-start.sh — Claude Code SessionStart hook.
#
# When a new CC session begins, this hook auto-injects the capillary DAG
# ASCII map for the current project (if cwd is inside an autoresearch-tree
# project tree). Output goes to stdout → CC injects as additional_context.
#
# Graceful degradation: if no project found, or build fails, emits nothing
# (no map for non-autoresearch repos, no error noise).
#
# Cache: re-uses INJECTION.md if <max_age_seconds old; otherwise rebuilds.

set -euo pipefail

SCRIPT_REAL="$(readlink -f "${BASH_SOURCE[0]}")"
PLUGIN_ROOT="$(cd "$(dirname "$SCRIPT_REAL")/.." && pwd)"
source "$PLUGIN_ROOT/lib/find-root.sh"

MAX_CACHE_AGE_SECONDS=3600   # 1 hour
MAX_INJECT_LINES=80          # keep the injection compact for CC context

# Find project root from CWD; if not in a project, exit silently.
PROJECT_ROOT="$(find_project_root "$PWD" 2>/dev/null)" || exit 0
if [[ -z "$PROJECT_ROOT" ]]; then
  exit 0
fi

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
  RENDER_PY="$PLUGIN_ROOT/bin/render-context.py"
  [[ -x "$PROJECT_ROOT/bin/render-context.py" ]] && RENDER_PY="$PROJECT_ROOT/bin/render-context.py"
  [[ -f "$SNAPSHOT_PY" ]] && AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" python3 "$SNAPSHOT_PY" >/dev/null 2>&1 || true
  [[ -f "$RENDER_PY" ]] && AUTORESEARCH_TREE_PROJECT_ROOT="$PROJECT_ROOT" python3 "$RENDER_PY" "$PROJECT_ROOT/nodes" >/dev/null 2>&1 || true
fi

# If still no INJECTION_FILE, exit silently — no map available.
if [[ ! -f "$INJECTION_FILE" ]]; then
  exit 0
fi

# Emit a compact map injection for CC context.
echo "## autoresearch-tree map (auto-injected)"
echo ""
echo "Project: \`$PROJECT_ROOT\`"
echo "Run: \`autoresearch-tree --max-iters N --delay-mins M\`"
echo ""
# First N lines of INJECTION.md = stats + attractor list + ASCII top.
head -n "$MAX_INJECT_LINES" "$INJECTION_FILE"
echo ""
echo "---"
echo "Full injection at \`$INJECTION_FILE\`. Skill: \`autoresearch-tree\`."
exit 0
