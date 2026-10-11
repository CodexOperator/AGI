#!/bin/sh
# PROOFS of A2. usage: SHA=<the GO sha> [STAGE=$HOME/memguard-A0] sh memguard-a2.proof.sh      (PROOF_ONLY=2: only PROOF 2 is shown; no wait before the first look)
# PROOF 2 runs the trunk's memguard-proof2.py FROM THE A0 ARCHIVE of the GO sha, TWICE, the gap between (and before the first look) DERIVED
# from the installed guard: 2 x its time.sleep + 1. The guard must also be ALIVE: a guard that set the values on tick 1 and then died or crash-loops
# would pass PROOF 2 alone. The verdict, from the two exit codes (a = first look, b = second) and the guard's health:
#   0 0 and the unit active, NRestarts 0, 0 tracebacks since the A2 act began (an UNREADABLE journal is not 0)   PROVEN   exit 0
#   either EXACTLY 1 (and the staged tree is the GO sha)                     UNDO A2      exit 1   a pid is on the wrong side: sh memguard-a2.undo.sh
#   anything else (the proof absent / killed / timed out / exit 2, an unhealthy guard, no derivable gap, a staged tree that is not the GO sha, no SHA given)
#                                                                            NOT PROVEN   exit 3   NO undo, NO 'A2 proven'; a line for the master is printed and kept in $STAGE/not-proven.txt; the leaf stays open
# Exit 1 is reserved for UNDO and nothing else returns it.
set -u
STAGE="${STAGE:-$HOME/memguard-A0}"; GUARD="${GUARD:-/usr/local/sbin/agi-memguard.py}"
SUDO="${SUDO-sudo -n}"; SYSTEMCTL="${SYSTEMCTL:-systemctl}"; JOURNALCTL="${JOURNALCTL:-journalctl}"
PROOF2="${PROOF2:-$STAGE/src/extensions/agi/boxkit/memguard-proof2.py}"        # a test hook; in a run it is the archive's file
[ -n "${SHA:-}" ] || { echo "VERDICT: NOT PROVEN: set SHA to the GO sha (the staged tree must be the one the GO names)"; exit 3; }
gap=$(sed -n 's/.*time[.]sleep[(]\([0-9.]*\)[)].*/\1/p' "$GUARD" 2>/dev/null)
if [ "$(printf '%s\n' "$gap" | grep -c .)" = 1 ]; then gap=$(awk -v t="$gap" 'BEGIN{printf "%.3f", 2*t+1}'); else gap=; fi
if [ "${PROOF_ONLY:-}" != 2 ]; then
  echo "== PROOF 1: active + enabled, no restart loop"; $SYSTEMCTL is-active agi-memguard.service; $SYSTEMCTL is-enabled agi-memguard.service; $SYSTEMCTL show agi-memguard.service -p MainPID -p NRestarts
  [ -n "$gap" ] && sleep "$gap"                                    # >= 2 ticks before the first look
fi
look() {                                                           # $1 = a|b -> prints the exit code of the proof, or `absent` / `nogap`
  [ -n "$gap" ] || { echo nogap; return; }
  [ -f "$PROOF2" ] || { echo absent; return; }
  python3 -I "$PROOF2" "$GUARD" > "$STAGE/proof2$1.out" 2>&1; echo $?
}
echo "== PROOF 2a: pids on the wrong side (exit 0 only when 0)"; ra=$(look a); echo "PROOF 2a exit=$ra"; tail -8 "$STAGE/proof2a.out" 2>/dev/null
[ -n "$gap" ] && sleep "$gap"                                      # a second, independent look
echo "== PROOF 2b"; rb=$(look b); echo "PROOF 2b exit=$rb"; tail -8 "$STAGE/proof2b.out" 2>/dev/null
# the guard's health: part of the verdict, shown in every mode
active=$($SYSTEMCTL is-active agi-memguard.service 2>/dev/null); nrest=$($SYSTEMCTL show agi-memguard.service -p NRestarts --value 2>/dev/null)
# the window is the A2 ACT's, not the unit's latest start: every auto-restart (Restart=always) moves ActiveEnterTimestamp and would hide an earlier traceback
a2since=$(cat "$STAGE/a2.since" 2>/dev/null)
if [ -n "$a2since" ]; then since=$(date -u -d "$a2since" '+%Y-%m-%d %H:%M:%S UTC' 2>/dev/null); else since=$($SYSTEMCTL show agi-memguard.service -p ActiveEnterTimestamp --value 2>/dev/null); fi
# an UNREADABLE journal is not zero tracebacks: journalctl's own exit status (not the pipe's) and a non-empty answer (a running guard has at least its Started line)
jout=$($SUDO $JOURNALCTL -u agi-memguard.service --since "${since:--3 min}" --no-pager -q 2>/dev/null); jrc=$?
if [ "$jrc" != 0 ] || [ -z "$jout" ]; then tb="unreadable(rc=$jrc)"; else tb=$(printf '%s\n' "$jout" | grep -c Traceback); fi
echo "== guard health: active=$active NRestarts=$nrest tracebacks=$tb (since ${since:-the last 3 min})"
if [ "${PROOF_ONLY:-}" != 2 ]; then
  echo "== PROOF 3: journal"; $SUDO $JOURNALCTL -u agi-memguard.service --since '-3 min' --no-pager -q | tail -8
  echo "== PROOF 4: a [memguard-*] line reaches each recipient's own ~/.notice, written by that post's uid"
  for to in sanctuary-master belam; do
    $SUDO timeout 30 runuser -u "agi-$to" -- env "HOME=/var/lib/agi/$to" sh -c '[ -x ~/bin/agi-notice ] && exec ~/bin/agi-notice add "$0" || echo "$0" >> ~/.notice' "[memguard-selftest] DG1 A2 PROOF 4: the guard's delivery command run by hand, not a guard event (ev $(date +%s))"
    echo "$to: rc=$? owner=$(stat -c %U /var/lib/agi/$to/.notice 2>&1)"
  done
  echo "(the post prints + removes its ~/.notice at its next prompt: an absent file after a moment is that; the post then SEES the line)"
fi
why=
if [ "$(cat "$STAGE/SHA" 2>/dev/null)" != "$SHA" ]; then why="the staged tree is $(cat "$STAGE/SHA" 2>/dev/null || echo none), not the GO sha $SHA"; fi
case "$ra $rb" in
  "0 0") verdict=PROVEN ;;
  "1 "*|*" 1") verdict=UNDO ;;                                     # EXACT tokens: only the exit code 1 is a wrong side (137, 124, 127, 10 are not)
  *) verdict=NOTPROVEN ;;
esac
if [ "$verdict" = PROVEN ] && { [ "$active" != active ] || [ "$nrest" != 0 ] || [ "$tb" != 0 ]; }; then
  verdict=NOTPROVEN; why="${why:+$why; }the guard is not healthy (active=$active NRestarts=$nrest tracebacks=$tb): a guard that set the values and died passes PROOF 2"
fi
[ -n "$why" ] && verdict=NOTPROVEN                                 # a proof from the wrong bytes proves nothing, whichever way it points
case $verdict in
  PROVEN) echo "VERDICT: PROVEN (2a and 2b both exit 0, the guard alive)"; exit 0 ;;
  UNDO) echo "VERDICT: UNDO A2 -- a pid is on the wrong side: sh memguard-a2.undo.sh"; exit 1 ;;
  *) line="NOT PROVEN: PROOF 2 gave a=$ra b=$rb${why:+; $why}; the guard is NOT undone and NOT proven, the leaf stays open until a run exits 0"
     echo "$line" > "$STAGE/not-proven.txt"; echo "VERDICT: $line"; echo "send that line to the master (kept in $STAGE/not-proven.txt)"; exit 3 ;;
esac
