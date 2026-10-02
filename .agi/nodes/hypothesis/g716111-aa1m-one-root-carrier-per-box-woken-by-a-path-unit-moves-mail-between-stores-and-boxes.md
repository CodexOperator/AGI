---
id: hypothesis:g716111-aa1m-one-root-carrier-per-box-woken-by-a-path-unit-moves-mail-between-stores-and-boxes
mint_id: 8629e41201d942b995827239f53eaae1
type: hypothesis
parents:
  - goal:g7.16.1.11.11.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: f5dd822fae1bd12f
season: 2
testable_claim: "(M2) ONE carrier per box (root) reads the post rows' LOCATION cells (box, store): for a recipient Q on this box it moves P's `refs/box/P/Q` into Q's store through a runuser pipe (AA2's agi-carry, 454 B), for Q on another box it pushes `refs/box/P/*` to the remote head and Q's box carrier fetches it; it is woken by a path unit watching each store's `refs/box` (PathChanged, no polling cron) plus ONE timer for remote fetches; a message sent by P reaches Q's store within one wake with no shared file written and no worktree touched."
title: "AA1.M carrier: ONE root carrier per box, woken by a path unit on each store's refs/box (no polling cron) plus one timer for remote fetches, reads the rows' location cells and moves mail store-to-store on a box (runuser pipe, agi-carry) or box-to-box (push / fetch of the remote head)"
town: core
---
# hypothesis:g716111-aa1m-one-root-carrier-per-box-woken-by-a-path-unit-moves-mail-between-stores-and-boxes

## Measured
- doc:rse-aa1-boxes section AA1.M (alive, posts/alive; belam [owner] 18:16Z item M1; designed and scratch-tested by alive 18:1xZ); belam ACCEPTED as designed ([decision] 18:2xZ, owner 18:2xZ GO). The numbers are alive's scratch measurements, not re-run by me. HORIZON: the build is not dispatched; each host act is belam's own GO.
- Bytes (expansion, 0 B in the zygote): the carrier = agi-carry 454 B + one rows-reading line ~200 B + a path unit ~60 B.
- HOST ACT 1 RESULT (belam, as root, 18:27:58Z, script read whole, sha256 OK, rolled back; doc:rse-aa1-boxes AA1.M on posts/alive): rc 0, `CARRIED hello-m1 U`, `BARRIER HOLDS`: the two-uid runuser carry WORKS and the 0700 barrier holds, but the receiver printed U (does not trust the sender's key), not G. Cause measured by alive 18:3xZ: each post's ~/.signers = the trunk's `.agi/keys/*` (3 keys: DT-1, DT-2, TM-new) + its own key, so all-is-one's lacked alive's; and a row's `pubkey` cell is NOT the git signing key (two keys per post).
- SIGNERS FIX (alive 18:29Z, REVISED 18:3xZ on self-perpetuating's objection, INCLUDED in this lane by belam [rule] 18:5xZ): at unit start root (ExecStartPre=+) reads ~<post>/.ssh/id_ed25519.pub and appends `<post>@agi namespaces="git" valid-after=<now> <pub>` to ONE root-owned allowed_signers, only when the key changed, stamping `valid-before` on that post's previous line (old generations still verify at their own dates); `.agi/keys/` stops being a source; the row hex `pubkey` stays send.py's seatsig and retires with it. Cross-box: the allowed_signers file itself TRAVELS as a commit signed by the box's root key (AA2 'keys: Source and travel', refs/agi/ring/BOX in the commons); a receiving box accepts it only if it verifies against the ring.
- NOT MEASURED (alive: needs root): runuser between two real post uids, the path unit firing on a store write, a remote head on a second box. belam: each of the THREE is its OWN HOST ACT = its own GO, ONE line per act with the exact command, the before-state and the one-command rollback; he GOes it the same hour.

## CLAIM
(M2) ONE carrier per box (root) reads the post rows' LOCATION cells (box, store): for a recipient Q on this box it moves P's `refs/box/P/Q` into Q's store through a runuser pipe (AA2's agi-carry, 454 B), for Q on another box it pushes `refs/box/P/*` to the remote head and Q's box carrier fetches it; it is woken by a path unit watching each store's `refs/box` (PathChanged, no polling cron) plus ONE timer for remote fetches; a message sent by P reaches Q's store within one wake with no shared file written and no worktree touched.

## Dispatch line
config-max: the path unit + the one timer (root-installed; host acts) / template-max: none / code: the carrier's rows-reading line. NOT dispatched: HORIZON; the three host acts below are the build's steps and each needs belam's GO first.

## FALSIFIERS
HOST ACT 1 (RUN once, belam 18:27:58Z: CARRIED U + BARRIER HOLDS, rolled back; RE-RUN after the signers fix must read `CARRIED hello-m1 G`, not U, with BARRIER HOLDS; before-state: /tmp/m1 absent, no live store touched; rollback: `rm -rf /tmp/m1`; each re-run is a fresh belam GO) a root `runuser -u <Q uid>` pipe from P's store to Q's store delivers one ref between two REAL post uids · HOST ACT 2: the path unit fires the carrier on a write to a store's `refs/box` and not otherwise (before-state: unit absent; rollback: `systemctl disable --now` the unit + remove the file) · HOST ACT 3: a push to a remote head on a SECOND box is fetched by that box's carrier and the reply returns (before-state: one box; rollback: remove the remote + the timer) · negative: no `cron` entry or polling loop exists for local delivery.

## TESTS
scratch first (alive's two-repo fixture), then each host act on the real box ONLY after belam's GO; each act's result recorded on its experiment node with the before-state it started from.

## FILE SCOPE
the carrier script + the path unit + one timer unit (root files: belam's GO per act) · its own experiment nodes. NEVER an inbox file.

## CEILING
3 host acts, one at a time, each its own belam GO · 1 parent · kids <= 1 · regular review. HORIZON.

## Placement (DG1 inner loop, 10-02 19:16Z, on DG2's return)
(M2) as WRITTEN is DISPROVED on its wake conjunct (verdict:dg2-aa1m-m2, 0.8): a watch on `refs/box` fires only on a sender's FIRST send (inotify is not recursive; the ref is `refs/box/P/Q`, two levels down). The corrective is hypothesis:g716111-aa1m-every-send-wakes-the-carrier-through-a-per-sender-path-watch (a template path unit per sender on `refs/box/P`, the per-row dir pre-created by root): ACCEPTED, and its HOST ACT 2 package (doc:dg2-aa1m-host-act-2) went to belam as ONE line for his GO. Host acts 1 (re-run after the signers fix, must read G) and 3 (a second box) are unchanged and each its own GO. The signers fix above stays part of this hypothesis.
