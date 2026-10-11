# UNDO A2: stop + disable the guard, then resume what IT stopped IN THIS A2 (it has no SIGTERM handler: a pid it SIGSTOPped stays stopped).
# This A2 = since STAGE/a2.since, which memguard-a2.sh wrote right before the first start, against the log's own UTC stamps. NOT the unit's latest start:
# Restart=always moves that on every crash, and a pid stopped before a crash is not in the restarted guard's memory, so only the log still names it.
# A pid an earlier A2 stopped, or anyone else stopped, is not ours to continue; nor is a REUSED pid (the SUSPENDED line carries the start time, stat field 22, and it must match). No a2.since = nothing is resumed and the candidates are listed for a human.
set -u
STAGE="${STAGE:-$HOME/memguard-A0}"; SUDO="${SUDO-sudo -n}"; LOG="${LOG:-/var/log/agi-memguard.log}"; SYSTEMCTL="${SYSTEMCTL:-systemctl}"
since=$(cat "$STAGE/a2.since" 2>/dev/null)
$SUDO $SYSTEMCTL disable --now agi-memguard.service
if [ -z "$since" ]; then
  echo "UNDO A2: no $STAGE/a2.since (memguard-a2.sh did not write it): NOTHING resumed. Pids the log names (stopped or not, check by hand):"; $SUDO grep -ho 'SUSPENDED pid [0-9]*' "$LOG" 2>/dev/null | sort -u
else
  for pr in $($SUDO awk -v s="$since" '$1 >= s && $2 == "SUSPENDED" && $3 == "pid" { r = ""; if (match($0, /start [0-9]+/)) r = substr($0, RSTART + 6, RLENGTH - 6); print $4 ":" r }' "$LOG" 2>/dev/null | sort -u); do
    p=${pr%%:*}; rs=${pr#*:}                                                    # the pid and the START TIME the guard logged with it ('' = an older line without one)
    cur=$(sed 's/.*) //' /proc/$p/stat 2>/dev/null | cut -d' ' -f1,20)         # kernel state, and field 22 (start time), after the last ')'
    st=${cur%% *}; cs=${cur#* }
    case "$st" in T|t)
      if [ -z "$rs" ] || [ "$rs" = "$cs" ]; then echo "resuming pid $p ($(cat /proc/$p/comm))"; $SUDO kill -CONT "$p"
      else echo "NOT resuming pid $p: its start time is $cs, the guard logged $rs (a reused pid)"; fi;; esac
  done
fi
[ -n "$since" ] && rm -f "$STAGE/a2.since"                            # the next A2 starts its own scope
echo "UNDO A2 done: active=$($SYSTEMCTL is-active agi-memguard.service 2>&1) enabled=$($SYSTEMCTL is-enabled agi-memguard.service 2>&1)"
echo "left behind (harmless, gone when those processes exit): oom_score_adj -900 / nice -5 the guard set"
