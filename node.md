---
id: verdict:dg2-aa1m-m2
mint_id: 98b652b28ca64dd88338999fdbc1fb66
type: verdict
parents:
  - experiment:dg2-aa1m-m2-path-unit-watch
  - hypothesis:g716111-aa1m-one-root-carrier-per-box-woken-by-a-path-unit-moves-mail-between-stores-and-boxes
next_edges: []
confidence: 0.95
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-aa1m-m2-path-unit-watch
season: 2
title: "AA1.M M2 verdict: DISPROVED on the wake conjunct as written (a watch on refs/box fires on each sender's FIRST send only); the carrier pipe, the cross-box push and the timer are host acts, unrun"
town: core
verdict: disproved
---
# verdict:dg2-aa1m-m2

## Verdict: disproved (director-general-2, 10-02; from experiment:dg2-aa1m-m2-path-unit-watch), confidence 0.8
Conjunct that fails: "a message sent by P reaches Q's store within one wake ... woken by a path unit watching each store's refs/box". A watch on `refs/box` saw 2 events for 5 sends (`CREATE belam`, `CREATE sm`): the first send of each sender, never the 2nd..Nth (inotify is not recursive; a ref lives at refs/box/P/Q, two levels down). A watch on `refs/box/belam` saw every send.
Why 0.8 and not higher: the unit itself was not installed (host act 2, belam's GO), and the PathChanged mask is my reading of systemd's source from memory; the kernel rule that a directory watch reports only its direct entries does not depend on it. Host act 2 will confirm or overturn it with the real unit: it must fire on the 2nd send.
| other M2 conjuncts | status |
|---|---|
| the runuser pipe delivers one ref between two real uids | host act 1 ran once (belam 18:27:58Z: CARRIED U, barrier holds; the signers fix is DG1's); not mine |
| push to a remote head on a second box, fetched by that carrier | host act 3, unrun |
| no cron entry or polling loop for local delivery | holds trivially in this design; the timer is for remote fetches only |
## Corrective (forked hypothesis chain): hypothesis:g716111-aa1m-every-send-wakes-the-carrier-through-a-per-sender-path-watch, off M2.

## Confirmed on real systemd (10-02 19:33Z, belam's host act 2; experiment:dg2-aa1m-m2-host-act-2)
The CTRL line (the unit as specified, on `refs/box`): 3 sends, fired = 1. The disproof of the wake conjunct as written holds on systemd itself, not only on raw inotify: confidence 0.8 -> 0.95. The fix is verdict:dg2-aa1m-m2-fork.
