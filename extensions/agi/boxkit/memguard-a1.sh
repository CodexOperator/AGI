#!/bin/sh
# A1 -- INSTALL the two staged files (sudo; box-wide live behaviour only once A2 enables it: the unit stays disabled + inactive).
set -eu
STAGE="${STAGE:-$HOME/memguard-A0}"; SUDO="${SUDO:-sudo -n}"; SBIN="${SBIN:-/usr/local/sbin}"; UNITDIR="${UNITDIR:-/etc/systemd/system}"
SYSTEMCTL="${SYSTEMCTL:-systemctl}"; OWN="${OWN--o root -g root}"
cd "$STAGE/out" && sha256sum -c SHA256SUMS                            # the staged bytes are still what A0 hashed (and A0 hashed them against the fixtures)
[ ! -e "$SBIN/agi-memguard.py" ] && [ ! -e "$UNITDIR/agi-memguard.service" ] || { echo "A1 REFUSED: already installed (run memguard-a1.undo.sh first)"; exit 1; }
$SUDO install -m 0755 $OWN agi-memguard.py "$SBIN/agi-memguard.py"
$SUDO install -m 0644 $OWN agi-memguard.service "$UNITDIR/agi-memguard.service"
$SUDO $SYSTEMCTL daemon-reload
echo "A1 OK: installed (not enabled, not started)"
