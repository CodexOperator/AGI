---
id: hypothesis:g716111-aa1m-a-send-that-lands-after-the-carriers-last-scan-is-carried-by-the-next-sweep-with-no-further-send
mint_id: c00829f864204c1bbc6e19566bbf8cf9
type: hypothesis
parents:
  - goal:g7.16.1.11.11.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(AA1.M closer) with box-carry's local sweep (the timer pass that already exists for the hub, `--fetch`, also re-carries every local post's own out-refs: one extra loop over the posts of this box that runs box-carry P), a send that lands AFTER the carrier's final for-each-ref and BEFORE its exit, or while a run is in flight and systemd drops the PathChanged event, is carried to the recipient's store by the next sweep with NO further send from the sender: in a test where a shim injects one send right after the carrier's last for-each-ref of the sender's store, the recipient's store holds the ref after ONE sweep and does not on today's carrier (the case is RED before the change); the piece stays <= 3,255 B (3,105 B now + 150); the sweep adds no new unit when the timer already exists, and a hub-less box (box.hub empty) still sweeps locally."
title: "AA1.M closer: a send that lands in the window after the carrier's last scan is carried by the next local sweep, with no further send; box-carry <= 3,255 B"
town: core
---
# hypothesis:g716111-aa1m-a-send-that-lands-after-the-carriers-last-scan-is-carried-by-the-next-sweep-with-no-further-send

## Measured
- A5, the coalescing probe, run by belam gen 27 as a host act (relayed by SM 02:2xZ, T=d57b52bd4; A1 A2 A4 A5 ran): `starts=1`: systemd LOSES PathChanged events that land while the carrier oneshot is running (it does not run the oneshot again for them). DG3's install package expected `starts=2` if it did (doc:dg3-aa1m-install-packages, A5).
- So box-carry's own re-scan is the only cover: it re-scans P's out-tips up to 5 times while they keep moving and exits 75 (the unit restarts it) if they still move after the last pass (### box-carry in .agi/nodes/.geometry/engine-root.md, 3,105 B). A send that lands AFTER its final for-each-ref and before exit wakes nothing until that sender's NEXT send: a lost WAKE, not lost mail (the ref sits in the sender's store, uncarried until the next wake).
- Options belam named (02:2xZ): (a) a final re-scan after exit (loop until a scan finds nothing new), or (b) a slow timer (e.g. agi-carry-sweep.timer). (a) shrinks the window and cannot close it (a send can always land after the newest scan); (b) closes it by time: the lost wake is bounded by the timer period.
- The piece already has a timer mode: `box-carry --fetch` (hub push + fetch) exits at once when box.hub is empty (belam's box.hub = ""), so on this box today that timer does nothing. DG1's recommendation: put the local sweep INTO that timer pass before its hub exit (0 new units, ~+120-150 B), not a second timer.

## CLAIM
(AA1.M closer) with box-carry's local sweep (the timer pass that already exists for the hub, `--fetch`, also re-carries every local post's own out-refs: one extra loop over the posts of this box that runs box-carry P), a send that lands AFTER the carrier's final for-each-ref and BEFORE its exit, or while a run is in flight and systemd drops the PathChanged event, is carried to the recipient's store by the next sweep with NO further send from the sender; the piece stays <= 3,255 B; no new unit when the timer already exists, and a hub-less box still sweeps locally.

## Dispatch line
config-max: none (the timer period is an existing cell or a constant in the unit; a new cell only if DG3 finds none) / template-max: none / code: box-carry (the sweep loop before the `[ -n "$H" ]||exit 0` of --fetch), the timer unit's period if it is not already <= 60 s. Route: DG2 falsifier, DG3 builds, SM gate + a Sonnet SECURITY mur (root code). NOT dispatched until handed. Installing it later = its own belam GO (command, before-state, one-command rollback).

## FALSIFIERS
1. In extensions/agi/tests/box-carry.t.sh (DG2): a shim wraps `git for-each-ref` on the sender's store and, right after the LAST call of a carrier run, injects one send; after ONE `box-carry --fetch` (the sweep) the recipient's store holds the ref with no further send. The same case on today's 3,105 B piece is RED (mutation proof: remove the sweep line and the case reds).
2. `wc -c` of the box-carry piece <= 3,255.
3. Negative: the sweep carries nothing the matrix refuses: the off-matrix and squatted cases of box-carry.t.sh (k0b, k5c-style) stay green; a hub-less box (H empty) still sweeps.
4. On the real box as root (belam's GO, UNVERIFIED until then): A5's probe shape with a send timed into the window: carried within one timer period.

## TESTS
box-carry.t.sh gains the window case + a negative; the existing 44 stay green.

## FILE SCOPE
extensions/agi/tests/box-carry.t.sh · engine-root.md (box-carry, and the timer unit text if its period changes). Never the live trunk ref.

## CEILING
1 parent · kids <= 1 · +150 B in box-carry · +20 test lines · sh + git + jq only · 0 USD.

## RESULT closer (director-general-3, 10-03, trunk dcfe7eec1; falsifier = DG2's k8 block, 0c88e036a, folded byte-equal)
- Built: ONE sweep in box-carry's --fetch pass, BEFORE the hub exit: `for p in $(echo "$W"|awk -v b=$B '$2==b{print $1}');do ok $p&&[ -d $S/$p/g.git ]&&sh $0 $p;done` -- every post whose row is on THIS box and that has a store runs the per-post carry (rows without a store are skipped; the per-post run keeps its own a() and own-prefix rules, so the k8 planted channel and the unknown recipient are neither carried nor pushed). Comment on the --fetch line says so (+~40 B).
- Measured on this tree: box-carry.t.sh 54 ok, 0 FAIL (was 52 ok / 2 FAIL on the 3,105 B piece with k8); piece 3,248 B <= 3,255 (k8-bytes ok); box-mail.t.sh unchanged vs the trunk (its one FAIL-grep hit is the BOUND comment line, same on an untouched trunk worktree).
- Concurrency: a sweep may overlap the post's own PathChanged carrier; every ref write is the per-post run's CAS (update-ref old value, ff-only), so the loser is a no-op or exit 75, never a rewrite.
- Install = belam GO (the changed piece goes with the next A1 pieces run). No new file, no .py.
