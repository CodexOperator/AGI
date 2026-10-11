#!/bin/sh
# RESTAGE -- move a RUNNING guard (A2 done) to a newer landed sha in ONE act. Without it a re-stage was done by hand (belam, 10-11 10:5xZ): A0's rm -rf $STAGE drops
# a2.since (the undo scope) and a1.undo refuses an active unit.
# usage: SHA=<the landed 40-hex sha> [STAGE=$HOME/memguard-A0] [MAIN=/data/work/agi] sh memguard-restage.sh
#   bootstrap (like A0, it cannot come from the archive it makes): git -C $MAIN show $SHA:extensions/agi/boxkit/memguard-restage.sh > $HOME/memguard-restage.sh
# Order: refuse without a landed SHA · REFUSE while the guard holds stopped pids (see below) · keep a2.since OUT of the stage · A0 on the sha (a refusal there touches nothing live) · stop the guard · a1.undo · a1 · a2 ·
# put the ORIGINAL a2.since back, so the undo scope stays this A2's first start and not the re-stage's. The proofs are printed, never run: they are the next GO's.
# STOPPED PIDS: the guard has no SIGTERM handler, so a pid it SIGSTOPped stays stopped when it is stopped, and the restarted guard's memory of it is EMPTY: it would never resume it.
# So BEFORE anything is touched the log's SUSPENDED pids since a2.since (no a2.since = the whole log) are looked up in the kernel: one still in state T/t REFUSES the re-stage by name
# (resume it, or memguard-a2.undo.sh, first); a log that exists but cannot be read REFUSES too (unreadable is not empty).
set -u
MAIN="${MAIN:-/data/work/agi}"; STAGE="${STAGE:-$HOME/memguard-A0}"; SUDO="${SUDO-sudo -n}"; SYSTEMCTL="${SYSTEMCTL:-systemctl}"; LOG="${LOG:-/var/log/agi-memguard.log}"
export MAIN STAGE SUDO SYSTEMCTL
case "${SHA:-}" in *[!0-9a-f]*|"") echo "RESTAGE REFUSED: set SHA to the landed 40-hex sha"; exit 1;; esac
[ "${#SHA}" = 40 ] && git -C "$MAIN" cat-file -e "$SHA^{commit}" 2>/dev/null || { echo "RESTAGE REFUSED: $SHA is not a commit in $MAIN"; exit 1; }
export SHA
saved=$(cat "$STAGE/a2.since" 2>/dev/null)
held=
if $SUDO test -e "$LOG"; then
  $SUDO test -f "$LOG" && $SUDO test -r "$LOG" || { echo "RESTAGE REFUSED: $LOG exists but is not a readable file: it cannot be read, so the stopped pids cannot be known; nothing touched"; exit 1; }
  cand=$($SUDO awk -v s="$saved" '$1 >= s && $2 == "SUSPENDED" && $3 == "pid" {print $4}' "$LOG") || { echo "RESTAGE REFUSED: $LOG exists but cannot be read, so the stopped pids cannot be known; nothing touched"; exit 1; }
  for p in $(printf '%s\n' "$cand" | sort -un); do
    st=$(sed 's/.*) //' /proc/$p/stat 2>/dev/null | cut -c1)                # kernel state, first field after the last ')'
    case "$st" in T|t) held="$held $p";; esac
  done
fi
[ -z "$held" ] || { echo "RESTAGE REFUSED: the guard holds stopped pids:$held -- resume them (memguard-a2.undo.sh resumes what this A2 stopped) before a re-stage; nothing touched"; exit 1; }
restore() { [ -n "$saved" ] && { mkdir -p "$STAGE" && printf '%s\n' "$saved" > "$STAGE/a2.since"; }; }
trap restore EXIT                                                      # A0's rm -rf, or any failure below, never costs the scope
B="$STAGE/src/extensions/agi/boxkit"
git -C "$MAIN" show "$SHA:extensions/agi/boxkit/memguard-a0.sh" | sh || { echo "RESTAGE STOPPED at A0: the guard was not touched"; exit 1; }
$SUDO $SYSTEMCTL stop agi-memguard.service || { echo "RESTAGE STOPPED: could not stop the guard (nothing removed)"; exit 1; }
for step in a1.undo a1 a2; do
  sh "$B/memguard-$step.sh" || { echo "RESTAGE FAILED at $step: THE GUARD IS STOPPED (a2.since is kept at ${saved:-nothing}); fix the cause and run this again, or $B/memguard-a2.sh"; exit 1; }
done
restore
echo "RESTAGE OK: $SHA running; a2.since ${saved:-written fresh}. Next: SHA=$SHA sh $B/memguard-a1.proof.sh; SHA=$SHA sh $B/memguard-a2.proof.sh"
