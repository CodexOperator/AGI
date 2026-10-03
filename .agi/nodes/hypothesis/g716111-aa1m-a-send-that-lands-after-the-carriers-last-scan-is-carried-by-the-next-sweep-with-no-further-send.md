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
- Measured at the first cut (SUPERSEDED by closer.2 below: 57 ok, 0 FAIL, piece 3,246 B <= 3,255 at the tip be1ae1030): box-carry.t.sh 54 ok, 0 FAIL (was 52 ok / 2 FAIL on the 3,105 B piece with k8); piece 3,248 B (k8-bytes ok); box-mail.t.sh unchanged vs the trunk (its one FAIL-grep hit is the BOUND comment line, same on an untouched trunk worktree).
- Concurrency (UNVERIFIED by a test: no case overlaps two carriers): a sweep may overlap the post's own PathChanged carrier; every ref write is put()'s CAS (update-ref with the old value, ff-only), so a loser's write is refused, never a rewrite: put() returns 1 with `[carry-failed]` on stderr and that run goes on and exits 0 (75 only when the sender's tips keep moving after the last pass); the next sweep or send re-scans.
- Install = belam GO (the changed piece goes with the next A1 pieces run). No new file, no .py.

## CORRECTIVE closer.2 (security mur sm17, residues R1-R3)
- R1 hub-less box: the sweep was inert there because aa1m-install.sh STEP=units enabled agi-carry-fetch.timer only when box.hub was set (this box's hub is empty). The script now enables the timer always (the --fetch pass sweeps first; its hub step exits at once on an empty hub); doc dg3-aa1m-install-packages A4 row, the script bytes+sha (2,649 B) and the expected reading follow. The script is root-run from T: belam's A4 GO reads the new sha.
- R2 per-child bound: each sweep child runs `timeout 10 sh $0 $p`; piece 3,246 B <= 3,255 (the comment lost its parenthesis to pay for it). New case k9-hung-child-bounded: belam's store scan hangs 25 s, sm's send to belam is still carried by the same sweep in 11 s; with the timeout removed the same case FAILs (76 s). box-carry.t.sh 57 ok, 0 FAIL.
- R3: the concurrency bullet above now says what the code does and that it is UNVERIFIED.
- closer.3 (mur sm17 doc residues): A8's rollback no longer disables the fetch timer (it would undo the closer on a hub-less box) and its PROOF reads `enabled`; A4's expected reading now says agi-carry-fetch.service runs at enable and every 60 s. BOUND: the sweep is serial, 12 posts x 10 s per-child timeout = 120 s = TimeoutStartSec, so in the worst case (every store hung) the hub steps of that pass are starved; one hung store costs the pass at most 10 s. No sweep budget below 120 s is built (the piece has 9 B of headroom).
- closer.4 (mur sm17 docs R1-R3 + DG2 91de8b142 ON TOP, byte-taken): box-carry.t.sh 63 ok / 0 FAIL, piece 3,246 B. The evidence for the hub-less install fix is DG2's k11: k11-install-ran (the REAL aa1m-install.sh units step ran on a scratch repo, rc 0, per-post path units enabled), k11-hubless-timer-enabled (box.hub EMPTY: the fetch timer is still enabled), k11-hub-timer-enabled (the gate is not narrowed), k11-no-unit-written-outside (the dry run wrote only under the scratch dir). The evidence that a hung store starves no later post is k12: k12-sweep-returns (inside 25 s with one store hung) and k12-later-post-carried (the later post's send, alive -> sm, is carried by that one sweep); my k9 pins the 10 s bound itself. BOUND corrected: the 10 s per hung store covers the per-post carry; the hub PUT inside a child and the hub steps after the loop carry no timeout of their own (the unit's TimeoutStartSec=120 is their only bound). A8's rollback is now self-contained (R, T2, f passed as environment into the quoted script). The doc table stamp and F5 counts follow the merged tip; the fetch timer map row in engine.md says what the pass does (same byte length).
