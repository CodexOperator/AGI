# UNDO A1 (only valid while A2 has NOT run, or after UNDO A2): remove both files, reload
set -eu
if systemctl is-active agi-memguard.service >/dev/null 2>&1; then echo "UNDO A1 REFUSED: the unit is active; run memguard-a2.undo.sh first"; exit 1; fi
sudo -n rm -f /usr/local/sbin/agi-memguard.py /etc/systemd/system/agi-memguard.service
sudo -n systemctl daemon-reload
[ ! -e /usr/local/sbin/agi-memguard.py ] && [ ! -e /etc/systemd/system/agi-memguard.service ] && echo "UNDO A1 ok: both gone"
