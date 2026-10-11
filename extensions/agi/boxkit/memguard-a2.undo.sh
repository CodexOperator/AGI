# UNDO A2: stop + disable the guard, then resume what IT stopped (it has no SIGTERM handler: a pid it SIGSTOPped stays stopped).
set -u
SUDO="${SUDO:-sudo -n}"; LOG="${LOG:-/var/log/agi-memguard.log}"; SYSTEMCTL="${SYSTEMCTL:-systemctl}"
$SUDO $SYSTEMCTL disable --now agi-memguard.service
for p in $($SUDO grep -ho 'SUSPENDED pid [0-9]*' "$LOG" 2>/dev/null | awk '{print $3}' | sort -un); do
  st=$(sed 's/.*) //' /proc/$p/stat 2>/dev/null | cut -c1)                      # kernel state, first field after the last ')'
  case "$st" in T|t) echo "resuming pid $p ($(cat /proc/$p/comm))"; $SUDO kill -CONT "$p";; esac
done
echo "UNDO A2 done: active=$(systemctl is-active agi-memguard.service 2>&1) enabled=$(systemctl is-enabled agi-memguard.service 2>&1)"
echo "left behind (harmless, gone when those processes exit): oom_score_adj -900 / nice -5 the guard set"
