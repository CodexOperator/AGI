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
- NOT MEASURED (alive: needs root): runuser between two real post uids, the path unit firing on a store write, a remote head on a second box. belam: each of the THREE is its OWN HOST ACT = its own GO, ONE line per act with the exact command, the before-state and the one-command rollback; he GOes it the same hour.

## CLAIM
(M2) ONE carrier per box (root) reads the post rows' LOCATION cells (box, store): for a recipient Q on this box it moves P's `refs/box/P/Q` into Q's store through a runuser pipe (AA2's agi-carry, 454 B), for Q on another box it pushes `refs/box/P/*` to the remote head and Q's box carrier fetches it; it is woken by a path unit watching each store's `refs/box` (PathChanged, no polling cron) plus ONE timer for remote fetches; a message sent by P reaches Q's store within one wake with no shared file written and no worktree touched.

## Dispatch line
config-max: the path unit + the one timer (root-installed; host acts) / template-max: none / code: the carrier's rows-reading line. NOT dispatched: HORIZON; the three host acts below are the build's steps and each needs belam's GO first.

## FALSIFIERS
HOST ACT 1: a root `runuser -u <Q uid>` pipe from P's store to Q's store delivers one ref between two REAL post uids (before-state: no ref in Q's store; rollback: delete the one ref) · HOST ACT 2: the path unit fires the carrier on a write to a store's `refs/box` and not otherwise (before-state: unit absent; rollback: `systemctl disable --now` the unit + remove the file) · HOST ACT 3: a push to a remote head on a SECOND box is fetched by that box's carrier and the reply returns (before-state: one box; rollback: remove the remote + the timer) · negative: no `cron` entry or polling loop exists for local delivery.

## TESTS
scratch first (alive's two-repo fixture), then each host act on the real box ONLY after belam's GO; each act's result recorded on its experiment node with the before-state it started from.

## FILE SCOPE
the carrier script + the path unit + one timer unit (root files: belam's GO per act) · its own experiment nodes. NEVER an inbox file.

## CEILING
3 host acts, one at a time, each its own belam GO · 1 parent · kids <= 1 · regular review. HORIZON.
