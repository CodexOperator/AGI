#!/bin/sh
# RESTAGE -- move a RUNNING guard (A2 done) to a newer landed sha in ONE act. Without it a re-stage was done by hand (belam, 10-11 10:5xZ): A0's rm -rf $STAGE drops
# a2.since (the undo scope) and a1.undo refuses an active unit.
# usage: SHA=<the landed 40-hex sha> [STAGE=$HOME/memguard-A0] [MAIN=/data/work/agi] sh memguard-restage.sh
#   bootstrap (like A0, it cannot come from the archive it makes): git -C $MAIN show $SHA:extensions/agi/boxkit/memguard-restage.sh > $HOME/memguard-restage.sh
# Order: refuse without a landed SHA · REFUSE while the guard holds stopped pids (see below) · keep a2.since OUT of the stage · A0 on the sha (a refusal there touches nothing live) · stop the guard · a1.undo · a1 · a2 ·
# put the ORIGINAL a2.since back, so the undo scope stays this A2's first start and not the re-stage's. The proofs are printed, never run: they are the next GO's.
# STOPPED PIDS: the guard has no SIGTERM handler, so a pid it SIGSTOPped stays stopped when it is stopped, and the restarted guard's memory of it is EMPTY: it would never resume it.
# So BEFORE anything is touched the log's SUSPENDED pids since a2.since (no a2.since = the whole log) are looked up in the kernel: one still in state T/t, with the START TIME the guard logged for it (a reused pid has another one), REFUSES the re-stage by name
# (resume it, or memguard-a2.undo.sh, first); a log that exists but cannot be read REFUSES too (unreadable is not empty).
# THE RACE: that check runs BEFORE A0 and the stop comes only AFTER A0 (seconds, longer under pressure), so a pid the guard stops in that window passes the first check and would stay
# stopped for ever. So the SAME check runs AGAIN right after `systemctl stop` returns (the old guard is then dead and can stop nothing more) and every held pid is sent SIGCONT, one line each
# to the journal and to the guard's own recipients (the master and belam, read from the guard's rendered source, written by the guard's own mechanism): the invariant is that after this
# script returns, WHATEVER its exit, no pid the old guard stopped since a2.since is still in T/t unless a line naming that pid AND its resume command reached the master.
# Every refusal and every failure line goes to the same recipients. Hooks (tests): NOTICE_BIN=<cmd TO TEXT> replaces the runuser/agi-notice delivery.
set -u
MAIN="${MAIN:-/data/work/agi}"; STAGE="${STAGE:-$HOME/memguard-A0}"; SUDO="${SUDO-sudo -n}"; SYSTEMCTL="${SYSTEMCTL:-systemctl}"; LOG="${LOG:-/var/log/agi-memguard.log}"; SBIN="${SBIN:-/usr/local/sbin}"
export MAIN STAGE SUDO SYSTEMCTL
notice_to() {                                                          # $1 = the line: the journal, then each recipient of the guard (read from its rendered source)
  logger -t agi-memguard-restage "$1" 2>/dev/null
  g="$STAGE/out/agi-memguard.py"; [ -r "$g" ] || g="$SBIN/agi-memguard.py"
  tos=$(sed -n "s/^.*for to in '\([^']*\)'.split().*$/\1/p" "$g" 2>/dev/null | head -1); stores=$(sed -n "s/^.*'HOME=\([^']*\)\/' + to.*$/\1/p" "$g" 2>/dev/null | head -1)
  for to in $tos; do
    case "$to" in *[!A-Za-z0-9._-]*|"") continue;; esac
    if [ -n "${NOTICE_BIN:-}" ]; then "$NOTICE_BIN" "$to" "$1"
    else $SUDO timeout 30 runuser -u "agi-$to" -- env "HOME=$stores/$to" sh -c '[ -x ~/bin/agi-notice ] && exec ~/bin/agi-notice add "$0" || echo "$0" >> ~/.notice' "$1" >/dev/null 2>&1; fi
  done
}
fail() { echo "$1"; notice_to "[memguard-restage] $1"; exit 1; }
case "${SHA:-}" in *[!0-9a-f]*|"") fail "RESTAGE REFUSED: set SHA to the landed 40-hex sha";; esac
[ "${#SHA}" = 40 ] && git -C "$MAIN" cat-file -e "$SHA^{commit}" 2>/dev/null || fail "RESTAGE REFUSED: $SHA is not a commit in $MAIN"
export SHA
saved=$(cat "$STAGE/a2.since" 2>/dev/null)
scan_held() {                                                          # sets held = the pids the log says the guard stopped since a2.since that the kernel still holds in T/t; rc 1 = the log cannot be read
  held=
  if $SUDO test -e "$LOG"; then
    $SUDO test -f "$LOG" && $SUDO test -r "$LOG" || return 1
    cand=$($SUDO awk -v s="$saved" '$1 >= s && $2 == "SUSPENDED" && $3 == "pid" { r = ""; if (match($0, /start [0-9]+/)) r = substr($0, RSTART + 6, RLENGTH - 6); print $4 ":" r }' "$LOG") || return 1
    for pr in $(printf '%s\n' "$cand" | sort -u); do
      p=${pr%%:*}; rs=${pr#*:}                                                 # the pid and the START TIME the guard logged with it ('' = an older line without one)
      cur=$(sed 's/.*) //' /proc/$p/stat 2>/dev/null | cut -d' ' -f1,20)      # kernel state, and field 22 (start time), after the last ')'
      st=${cur%% *}; cs=${cur#* }
      case "$st" in T|t) { [ -z "$rs" ] || [ "$rs" = "$cs" ]; } && held="$held $p";; esac     # a REUSED pid (another start time) is not the guard's stop
    done
  fi
  return 0                                                             # the last case arm's status (a reused pid is NOT held) must not read as 'unreadable'
}
scan_held || fail "RESTAGE REFUSED: $LOG exists but cannot be read (not a readable file, or its read failed), so the stopped pids cannot be known; nothing touched"
[ -z "$held" ] || fail "RESTAGE REFUSED: the guard holds stopped pids:$held -- resume them (memguard-a2.undo.sh resumes what this A2 stopped) before a re-stage; nothing touched"
restore() { [ -n "$saved" ] && { mkdir -p "$STAGE" && printf '%s\n' "$saved" > "$STAGE/a2.since"; }; }
trap restore EXIT                                                      # A0's rm -rf, or any failure below, never costs the scope
B="$STAGE/src/extensions/agi/boxkit"
git -C "$MAIN" show "$SHA:extensions/agi/boxkit/memguard-a0.sh" | sh || fail "RESTAGE STOPPED at A0: the guard was not touched"
$SUDO $SYSTEMCTL stop agi-memguard.service || fail "RESTAGE STOPPED: could not stop the guard (nothing removed)"
scan_held || fail "RESTAGE FAILED after the stop: THE GUARD IS STOPPED and $LOG cannot be read, so the pids it stopped are unknown: run memguard-a2.undo.sh (it resumes them) and read the log by hand"
for p in $held; do                                                     # the race: stopped between the first check and the stop
  c=$(cat /proc/$p/comm 2>/dev/null)
  if $SUDO kill -CONT "$p"; then m="RESTAGE RESUMED pid $p ($c): the old guard SIGSTOPped it in the window before the stop and a restarted guard never resumes it; sent kill -CONT $p"
  else m="RESTAGE COULD NOT RESUME pid $p ($c): it is STILL STOPPED, resume it by hand: kill -CONT $p"; fi
  echo "$m"; notice_to "[memguard-restage] $m"
done
for step in a1.undo a1 a2; do
  sh "$B/memguard-$step.sh" || fail "RESTAGE FAILED at $step: THE GUARD IS STOPPED (a2.since is kept at ${saved:-nothing}); fix the cause and run this again, or $B/memguard-a2.sh"
done
restore
echo "RESTAGE OK: $SHA running; a2.since ${saved:-written fresh}. Next: SHA=$SHA sh $B/memguard-a1.proof.sh; SHA=$SHA sh $B/memguard-a2.proof.sh"
