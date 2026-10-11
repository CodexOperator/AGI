# UNDO A2: stop + disable the guard, then resume what IT stopped IN THIS RUN (it has no SIGTERM handler: a pid it SIGSTOPped stays stopped).
# This run = since the unit's ActiveEnterTimestamp (read BEFORE it is stopped), against the log's own UTC stamps: a pid an earlier run stopped, or
# anyone else stopped, is not ours to continue. No start time = nothing is resumed and the candidates are listed for a human.
set -u
SUDO="${SUDO-sudo -n}"; LOG="${LOG:-/var/log/agi-memguard.log}"; SYSTEMCTL="${SYSTEMCTL:-systemctl}"
since=$($SYSTEMCTL show agi-memguard.service -p ActiveEnterTimestamp --value 2>/dev/null)
[ -n "$since" ] && since=$(date -u -d "$since" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null)     # never date -d "": that is midnight today
$SUDO $SYSTEMCTL disable --now agi-memguard.service
if [ -z "$since" ]; then
  echo "UNDO A2: the unit has no start time: NOTHING resumed. Pids the log names (stopped or not, check by hand):"; $SUDO grep -ho 'SUSPENDED pid [0-9]*' "$LOG" 2>/dev/null | sort -u
else
  for p in $($SUDO awk -v s="$since" '$1 >= s && $2 == "SUSPENDED" && $3 == "pid" {print $4}' "$LOG" 2>/dev/null | sort -un); do
    st=$(sed 's/.*) //' /proc/$p/stat 2>/dev/null | cut -c1)                    # kernel state, first field after the last ')'
    case "$st" in T|t) echo "resuming pid $p ($(cat /proc/$p/comm))"; $SUDO kill -CONT "$p";; esac
  done
fi
echo "UNDO A2 done: active=$($SYSTEMCTL is-active agi-memguard.service 2>&1) enabled=$($SYSTEMCTL is-enabled agi-memguard.service 2>&1)"
echo "left behind (harmless, gone when those processes exit): oom_score_adj -900 / nice -5 the guard set"
