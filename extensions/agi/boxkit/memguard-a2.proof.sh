#!/bin/sh
# PROOFS of A2. usage: SHA=<the GO sha> [STAGE=$HOME/memguard-A0] sh memguard-a2.proof.sh      (PROOF_ONLY=2: just PROOF 2, no wait before the first look)
# PROOF 2 runs the trunk's memguard-proof2.py FROM THE A0 ARCHIVE of the GO sha, TWICE, the gap between (and before the first look) DERIVED
# from the installed guard: 2 x its time.sleep + 1. The verdict, from the two exit codes (a = first look, b = second):
#   0 0                       PROVEN        exit 0
#   either 1                  UNDO A2       exit 1   a pid is on the wrong side: sh memguard-a2.undo.sh
#   anything else             NOT PROVEN    exit 3   the proof is absent / exit 2 / unreadable, the staged tree is not the GO sha, or the gap cannot be derived:
#                                                    NO undo, NO 'A2 proven'; a line for the master is printed and kept in $STAGE/not-proven.txt; the leaf stays open
set -u
STAGE="${STAGE:-$HOME/memguard-A0}"; GUARD="${GUARD:-/usr/local/sbin/agi-memguard.py}"
PROOF2="${PROOF2:-$STAGE/src/extensions/agi/boxkit/memguard-proof2.py}"        # a test hook; in a run it is the archive's file
gap=$(sed -n 's/.*time[.]sleep[(]\([0-9.]*\)[)].*/\1/p' "$GUARD" 2>/dev/null)
if [ "$(printf '%s\n' "$gap" | grep -c .)" = 1 ]; then gap=$(awk -v t="$gap" 'BEGIN{printf "%.3f", 2*t+1}'); else gap=; fi
if [ "${PROOF_ONLY:-}" != 2 ]; then
  echo "== PROOF 1: active + enabled, no restart loop"; systemctl is-active agi-memguard.service; systemctl is-enabled agi-memguard.service; systemctl show agi-memguard.service -p MainPID -p NRestarts
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
if [ "${PROOF_ONLY:-}" != 2 ]; then
  echo "== PROOF 3: journal"; sudo -n journalctl -u agi-memguard.service --since '-3 min' --no-pager -q | tail -8; echo "tracebacks: $(sudo -n journalctl -u agi-memguard.service --since '-3 min' --no-pager -q | grep -c Traceback)"
  echo "== PROOF 4: a [memguard-*] line reaches each recipient's own ~/.notice, written by that post's uid"
  for to in sanctuary-master belam; do
    sudo -n timeout 30 runuser -u "agi-$to" -- env "HOME=/var/lib/agi/$to" sh -c '[ -x ~/bin/agi-notice ] && exec ~/bin/agi-notice add "$0" || echo "$0" >> ~/.notice' "[memguard-selftest] DG1 A2 PROOF 4: the guard's delivery command run by hand, not a guard event (ev $(date +%s))"
    echo "$to: rc=$? owner=$(stat -c %U /var/lib/agi/$to/.notice 2>&1)"
  done
  echo "(the post prints + removes its ~/.notice at its next prompt: an absent file after a moment is that; the post then SEES the line)"
fi
why=
if [ -n "${SHA:-}" ] && [ "$(cat "$STAGE/SHA" 2>/dev/null)" != "$SHA" ]; then why="the staged tree is $(cat "$STAGE/SHA" 2>/dev/null || echo none), not the GO sha $SHA"; fi
case "$ra $rb" in
  *1*) verdict=UNDO ;;
  "0 0") verdict=PROVEN ;;
  *) verdict=NOTPROVEN ;;
esac
[ -n "$why" ] && [ "$verdict" != UNDO ] && verdict=NOTPROVEN
case $verdict in
  PROVEN) echo "VERDICT: PROVEN (2a and 2b both exit 0)"; exit 0 ;;
  UNDO) echo "VERDICT: UNDO A2 -- a pid is on the wrong side: sh memguard-a2.undo.sh"; exit 1 ;;
  *) line="NOT PROVEN: PROOF 2 gave a=$ra b=$rb${why:+; $why}; the guard is NOT undone and NOT proven, the leaf stays open until a run exits 0"
     echo "$line" > "$STAGE/not-proven.txt"; echo "VERDICT: $line"; echo "send that line to the master (kept in $STAGE/not-proven.txt)"; exit 3 ;;
esac
