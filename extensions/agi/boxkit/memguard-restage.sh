#!/bin/sh
# RESTAGE -- move a RUNNING guard (A2 done) to a newer landed sha in ONE act. Without it a re-stage was done by hand (belam, 10-11 10:5xZ): A0's rm -rf $STAGE drops
# a2.since (the undo scope) and a1.undo refuses an active unit.
# usage: SHA=<the landed 40-hex sha> [STAGE=$HOME/memguard-A0] [MAIN=/data/work/agi] sh memguard-restage.sh
#   bootstrap (like A0, it cannot come from the archive it makes): git -C $MAIN show $SHA:extensions/agi/boxkit/memguard-restage.sh > $HOME/memguard-restage.sh
# Order: refuse without a landed SHA · keep a2.since OUT of the stage · A0 on the sha (a refusal there touches nothing live) · stop the guard · a1.undo · a1 · a2 ·
# put the ORIGINAL a2.since back, so the undo scope stays this A2's first start and not the re-stage's. The proofs are printed, never run: they are the next GO's.
set -u
MAIN="${MAIN:-/data/work/agi}"; STAGE="${STAGE:-$HOME/memguard-A0}"; SUDO="${SUDO-sudo -n}"; SYSTEMCTL="${SYSTEMCTL:-systemctl}"
export MAIN STAGE SUDO SYSTEMCTL
case "${SHA:-}" in *[!0-9a-f]*|"") echo "RESTAGE REFUSED: set SHA to the landed 40-hex sha"; exit 1;; esac
[ "${#SHA}" = 40 ] && git -C "$MAIN" cat-file -e "$SHA^{commit}" 2>/dev/null || { echo "RESTAGE REFUSED: $SHA is not a commit in $MAIN"; exit 1; }
export SHA
saved=$(cat "$STAGE/a2.since" 2>/dev/null)
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
