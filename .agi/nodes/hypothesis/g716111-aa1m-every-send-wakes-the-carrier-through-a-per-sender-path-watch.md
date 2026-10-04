---
id: hypothesis:g716111-aa1m-every-send-wakes-the-carrier-through-a-per-sender-path-watch
mint_id: 0bb8f8a4a5da46fd927276929f532760
type: hypothesis
parents:
  - hypothesis:g716111-aa1m-one-root-carrier-per-box-woken-by-a-path-unit-moves-mail-between-stores-and-boxes
next_edges: []
confidence: 0.5
edited_by: director-general-2
season: 2
testable_claim: "(M2 corrective) every send by a post, the first one and the Nth, to a new or an existing channel, produces a wake of the carrier within one second: a template path unit watches `refs/box/<P>` for each sender P (one `PathChanged` per sender; root creates the directory at carrier start so the watch can attach), and N sends give N events, where a single watch on `refs/box` gives 1 event per sender (measured on experiment:dg2-aa1m-m2-path-unit-watch: 5 sends, 2 events), and the wake survives `git pack-refs --all` / `git gc`, which delete the empty per-sender directory (measured with raw inotify: the watch is dropped and the next 2 sends give 0 events)"
title: "AA1.M carrier wake corrective: a path watch on each sender's refs/box/<P> fires on every send, not only on the sender's first"
town: core
---
# hypothesis:g716111-aa1m-every-send-wakes-the-carrier-through-a-per-sender-path-watch

## Measured premise (DG2, 10-02, verdict:dg2-aa1m-m2)
inotify is not recursive: a watch on `refs/box` sees `CREATE <P>` when P's directory first appears and nothing for later sends (the ref is `refs/box/P/Q`, renamed from `Q.lock` two levels down). A watch on `refs/box/<P>` sees `CREATE Q.lock`, `CLOSE_WRITE`, `MOVED_FROM`, `MOVED_TO Q` for each send.

## CLAIM
As in `testable_claim`. Candidate means (none chosen): (a) one TEMPLATE unit `agi-carry@.path` with `PathChanged=<store>/refs/box/%i` instantiated per sender, `.service` shared (about the same bytes as the one unit, plus a directory pre-created by root per row at carrier start); (b) a `reference-transaction` hook in each store touching ONE trigger file under a flat watched directory (a hook is one more file in every store); (c) the timer alone, with the latency it costs. The unit is a host act: each install is its own belam GO (command + before-state + rollback).

## FALSIFIERS
HOST ACT 2 (belam's GO): after the template unit is installed for sender P, N sends by P (the 1st, the 2nd, a new channel) = N carrier activations (`journalctl -u agi-carry@P` count), 0 activations with no send; scratch twin (no root): the inotify watcher run on `refs/box/<P>` counts N events for N sends. PACK: after `git pack-refs --all` the next 2 sends still activate it (else the mitigation: `gc.packRefs=false` on the store, or the carrier re-creates the dir). Negative: a unit on `refs/box` alone gives 1 activation for N sends by one sender. The package for belam's GO is doc:dg2-aa1m-host-act-2 (script + unit text + rollback).

## TESTS
scratch first (the watcher in experiment:dg2-aa1m-m2-path-unit-watch), then the host act on the real box ONLY after belam's GO; the before-state and the one-command rollback recorded on its experiment node.

## FILE SCOPE
the carrier's path unit + service (root files: belam's GO per act) · its own experiment node. NEVER an inbox file.

## CEILING
1 parent · kids <= 1 · 1 host act, its own belam GO. HORIZON: not dispatched; DG1's inner loop places it.

## Result (belam's host act 2, 19:32Z)
verdict:dg2-aa1m-m2-fork PROVED 0.95 on real systemd (host acts 2 + 2b, 8 of 8 lines MET); the pack-refs mitigations above are NOT needed (the unit re-arms); a unit that waited on a missing dir attaches when it appears, so the live unit may take the default boot shape. Per belam, DG3 may build the per-sender template on this; the live install is its own GO.

## Placement (DG1 19:16Z, belam 19:1xZ; updated after host acts 2 + 2b)
ACCEPTED as the corrective of hypothesis:g716111-aa1m-one-root-carrier-per-box-woken-by-a-path-unit-moves-mail-between-stores-and-boxes (verdict:dg2-aa1m-m2). Host act 2 (doc:dg2-aa1m-host-act-2) RAN (belam, root, 19:32:46Z) and 2b RAN (19:39:48Z), both self- or hand-rolled-back: 8 of 8 lines MET; the unit RE-ARMS after a pruned dir, a waiting unit attaches when its dir appears (the live `agi-carry@.path` may take the default `paths.target` shape, no ordering after the post unit), pid 1 inotify +1 per unit. The live unit install (agi-carry@.path per row) is DG3's build and its own later GO.
