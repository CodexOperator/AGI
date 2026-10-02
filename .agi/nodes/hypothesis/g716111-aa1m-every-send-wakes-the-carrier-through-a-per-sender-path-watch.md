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

## Placement (DG1 19:16Z, belam 19:1xZ)
ACCEPTED as the corrective of hypothesis:g716111-aa1m-one-root-carrier-per-box-woken-by-a-path-unit-moves-mail-between-stores-and-boxes (verdict:dg2-aa1m-m2). Its host act 2 = doc:dg2-aa1m-host-act-2 (scratch units, stub service, one command + one-command rollback), sent to belam as ONE line for his GO; the live unit install (agi-carry@.path per row) is DG3's build and its own later GO. HORIZON until belam GOes act 2: the PACK line decides whether the live design needs the store's gc.packRefs=false or the carrier re-creating the dir.

## HOST ACT 2 RESULT (belam [decision] 19:3xZ 10-02: RAN as root 19:32:46Z with his GO, script read whole first, sha256 9e4180a5 OK; ROLLED BACK 19:33:10Z: units 0, /tmp/m2 0, /run files 0, pid 1 inotify back to 10 = before)
| line | result | reads |
|---|---|---|
| ROW alive | sends=3 fired=3 | MET: the per-sender PathChanged fires on EVERY send |
| CTRL all-is-one | sends=3 fired=1 | MET: a watch on refs/box fires only on the first send; the M2 bug is real |
| NEG | no send + a write elsewhere: 3 -> 3 | MET |
| PACK | `pack-refs --all` pruned the dir: YES; 2 more sends: fired=5 | MET: systemd RE-ARMS the unit across a pruned and re-created dir; NO gc.packRefs mitigation is needed (the twin's raw inotify died with the dir; the real unit does not) |
| GHOST before | a row with no dir yet: active / waiting, Result success | MET: the unit waits, it does not fail |
| GHOST after | HOST ACT 2b RAN (belam, root, 19:39:48Z, script read whole, sha256 a53de7d5 OK, self-rolled-back: units 0, /tmp/m3 0, /run files 0): root made the dir, the row user wrote: fired=1 and still active; a 2nd write: fired=2 | MET: a waiting per-sender path unit ATTACHES when its dir appears later. The first run's GHOST-after flaw (mkdir as the row user under a root-owned /tmp/m2) is closed by this separate one-shot |
| INOTIFY pid 1 | 10 -> 13 for 3 units | MET: +1 instance per unit; 32 rows = +32 against max_user_instances 128 |
DG3 may build the per-sender template (`agi-carry@.path`, `PathChanged=STORE/refs/box/%i`) on this; the LIVE install is its own belam GO. The twin's PACK hazard (the watch died with the dir) did NOT hold for systemd: the mitigation candidates (a) gc.packRefs=false and (b) the carrier re-creating the dir are NOT needed. HOST ACT 2 IS NOW 8 of 8 MET (7 lines + the ghost-after of 2b). The live `agi-carry@.path` may take the DEFAULT shape (`WantedBy=paths.target`, up at boot): NO ordering after the post unit is required (belam [decision] 19:4xZ). The verdict is DG2's: the evidence now supports PROVED, not lean, on the real box (scratch units, a stub service; the live install is DG3's build and its own GO).
