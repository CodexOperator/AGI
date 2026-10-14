# UNDO A1 (only valid while A2 has NOT run, or after UNDO A2): disable (drops the multi-user.target.wants link), remove both files and any link left behind, reload.
# A guard stopped by hand is still ENABLED: without the disable the link survives the files and the next A1's proof reads `enabled` for a unit nobody enabled.
set -eu
SUDO="${SUDO-sudo -n}"; SYSTEMCTL="${SYSTEMCTL:-systemctl}"; SBIN="${SBIN:-/usr/local/sbin}"; UNITDIR="${UNITDIR:-/etc/systemd/system}"
if $SYSTEMCTL is-active agi-memguard.service >/dev/null 2>&1; then echo "UNDO A1 REFUSED: the unit is active; run memguard-a2.undo.sh first"; exit 1; fi
$SUDO $SYSTEMCTL disable agi-memguard.service >/dev/null 2>&1 || true        # with the unit file still there this removes the wants link
$SUDO rm -f "$SBIN/agi-memguard.py" "$UNITDIR/agi-memguard.service" "$UNITDIR/multi-user.target.wants/agi-memguard.service"
$SUDO $SYSTEMCTL daemon-reload
[ ! -e "$SBIN/agi-memguard.py" ] && [ ! -e "$UNITDIR/agi-memguard.service" ] && [ ! -L "$UNITDIR/multi-user.target.wants/agi-memguard.service" ] && echo "UNDO A1 ok: both files and the wants link gone"
