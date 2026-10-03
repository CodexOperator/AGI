---
id: experiment:dg2-aa1m-m2-host-act-2b
mint_id: 5a89deae164a409f810a67256cbcd1fe
type: experiment
parents:
  - hypothesis:g716111-aa1m-every-send-wakes-the-carrier-through-a-per-sender-path-watch
  - experiment:dg2-aa1m-m2-host-act-2
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-aa1m-m2-host-act-2b
season: 2
title: "AA1.M M2 HOST ACT 2b, run by belam as root 19:39:48Z (GO, script read whole, sha256 a53de7d5 verified), self-rolled-back: a per-sender path unit that waited on a missing dir ATTACHES when the dir appears later and fires on each write (8 of 8 with host act 2)"
town: core
---
# experiment:dg2-aa1m-m2-host-act-2b

## What ran
`.agi/context/local-maxxing/aa1m/host-act-2-ghost.sh` (1,674 B, sha256 a53de7d5fdf0437196cbab1d25197ff1af2f2136e3217b835ed3fd7aa8a946c2), as root, by belam, 19:39:48Z: the ghost-AFTER line that host act 2 could not measure (experiment:dg2-aa1m-m2-host-act-2: my mkdir ran as the row user under a root-owned dir). Throwaway unit `agi-act2g@`, stub service, `/tmp/m3`; it rolled itself back (belam verified: units 0, `/tmp/m3` 0, `/run` files 0). The result is belam's, quoted from his [decision] 19:4xZ; I did not run it.

## Result (belam's lines, my reading in brackets)
| line | result | reading |
|---|---|---|
| GHOST before its dir exists | active / waiting | MET (as in act 2) |
| after root creates the dir + the row user writes a file | fired=**1**, still active | MET: a unit that waited on a missing dir ATTACHES when the dir appears |
| a 2nd write later | fired=**2** | MET: it keeps firing, so it re-armed on the new inode, not a one-off |
Host act 2 is now **8 of 8**.

## What follows for the design
The live `agi-carry@.path` may take the DEFAULT shape (enabled to `paths.target`, up at boot, before any post unit has run); no ordering after the post unit's `ExecStartPre=+` is required. Root should still create `refs/box/<P>` at the post unit's start (the sender must own the dir), but the unit does not have to wait for it.

## Not shown
The live install on the real stores and the real carrier (DG3's build, its own belam GO); how long the attach takes (the act slept 2 s and counted: it fired within 2 s, not timed finer).
