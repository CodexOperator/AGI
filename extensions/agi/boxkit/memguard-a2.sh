#!/bin/sh
# A2 -- ENABLE + START (box-wide live behaviour: from the first tick every agi-post@ spine/harness is set to -900 / nice -5)
# It writes STAGE/a2.since (UTC, ISO) right before the first start: the undo resumes what the guard stopped SINCE THEN, across every auto-restart
# (Restart=always moves the unit's own start time; a pid stopped before a crash is not in the restarted guard's memory). A re-run keeps the first stamp.
set -eu
STAGE="${STAGE:-$HOME/memguard-A0}"; SUDO="${SUDO-sudo -n}"; SYSTEMCTL="${SYSTEMCTL:-systemctl}"; SBIN="${SBIN:-/usr/local/sbin}"; UNITDIR="${UNITDIR:-/etc/systemd/system}"
[ -e "$SBIN/agi-memguard.py" ] && [ -e "$UNITDIR/agi-memguard.service" ] || { echo "A2 REFUSED: A1 has not run"; exit 1; }
[ -e "$STAGE/a2.since" ] || date -u +%Y-%m-%dT%H:%M:%SZ > "$STAGE/a2.since"
$SUDO $SYSTEMCTL enable --now agi-memguard.service
echo "A2 started; the undo scope begins at $(cat "$STAGE/a2.since")"
