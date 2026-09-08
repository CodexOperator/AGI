#!/bin/bash
# mail-alert.sh — shared mail-alert side channel (hypothesis:l3w4-shared-mail-alert).
#
# Registered on UserPromptSubmit (fires every turn, unlike SessionStart which
# fires once — quorum seats run long). When the current seat has unread agent
# mail (dm, room, or the plain inbox) it prints one system-reminder-tagged
# block on stdout so the harness injects it as additional context at the next
# natural seam — the agent does zero work, nothing is lost if the seam is
# busy, and "another agent needs me" is always distinguishable from the owner.
#
# Silent no-op outside an agi project — same contract cc-session-start.sh
# already has — which is the only reason registering this globally is safe.

set -euo pipefail

SCRIPT_REAL="$(readlink -f "${BASH_SOURCE[0]}")"
PLUGIN_ROOT="$(cd "$(dirname "$SCRIPT_REAL")/.." && pwd)"
source "$PLUGIN_ROOT/lib/find-root.sh"

PROJECT_ROOT="$(find_project_root "$PWD" 2>/dev/null)" || exit 0
if [[ -z "$PROJECT_ROOT" ]]; then
  exit 0
fi

python3 "$PLUGIN_ROOT/bin/mail_alert.py" --root "$PROJECT_ROOT" 2>/dev/null
