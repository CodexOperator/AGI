# PROOF A1: installed bytes == staged bytes; the unit is known to systemd and still off
set -eu
STAGE="${STAGE:-$HOME/memguard-A0}"; SBIN="${SBIN:-/usr/local/sbin}"; UNITDIR="${UNITDIR:-/etc/systemd/system}"
{ sha256sum "$SBIN/agi-memguard.py" "$UNITDIR/agi-memguard.service"; } | awk '{print $1}' > "$STAGE/installed.sums"
awk '{print $1}' "$STAGE/out/SHA256SUMS" | cmp - "$STAGE/installed.sums" && echo "PROOF A1.1 ok: installed bytes == staged bytes"
stat -c '%U:%G %a %n' "$SBIN/agi-memguard.py" "$UNITDIR/agi-memguard.service"                 # root:root 755 / 644
systemctl is-enabled agi-memguard.service || true; systemctl is-active agi-memguard.service || true     # disabled / inactive
