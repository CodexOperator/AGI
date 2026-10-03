---
id: experiment:dg2-aa1m-m2-host-act-2
mint_id: 2960d3904f6f47c381ebb8a49bdfc016
type: experiment
parents:
  - hypothesis:g716111-aa1m-every-send-wakes-the-carrier-through-a-per-sender-path-watch
  - hypothesis:g716111-aa1m-one-root-carrier-per-box-woken-by-a-path-unit-moves-mail-between-stores-and-boxes
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-aa1m-m2-host-act-2
season: 2
title: "AA1.M M2 HOST ACT 2, run by belam as root 19:32:46Z (GO, script read whole, sha256 9e4180a5 verified), rolled back 19:33:10Z: a per-sender PathChanged unit fires on EVERY send, refs/box fires once, the unit re-arms after a prune, +1 inotify instance per unit"
town: core
---
# experiment:dg2-aa1m-m2-host-act-2

## What ran
`.agi/context/local-maxxing/aa1m/host-act-2.sh` (first version, sha256 9e4180a560f642fbc0e3e0fa88dbb08593518407fa880049bb2efd277417539d), as root, by belam, 19:32:46Z; throwaway units `agi-act2@` / `agi-act2c@` in `/run/systemd/system`, a stub service, stores under `/tmp/m2` for two real uids (alive, all-is-one), no live store, no real carrier. Rolled back 19:33:10Z with the package's one command: units 0, `/tmp/m2` 0, `/run` files 0, pid 1 inotify back to 10 = before. The result is belam's, quoted from his [decision] 19:3xZ; I did not run it and did not touch root.

## Result (belam's lines, my reading in brackets)
| line | result | reading |
|---|---|---|
| ROW alive (watch `refs/box/alive`, dir pre-created) | sends=3 fired=**3** | MET: the real systemd PathChanged fires on EVERY send (my raw-inotify twin said 3 bursts) |
| CTRL all-is-one (watch `refs/box`, sender dir not pre-created) | sends=3 fired=**1** | MET: the unit AS SPECIFIED fires once per sender: the M2 wake bug is real on systemd, not only on inotify |
| NEG no send + a write to `refs/heads/z`, 3 s | 3 -> 3 | MET |
| PACK `git pack-refs --all` pruned the pre-created dir: YES; 2 more sends | fired=**5** | MET, and **my hazard prediction was wrong for systemd**: raw inotify drops the watch (twin: 0 events), but the path unit RE-ARMS. No `gc.packRefs` mitigation is needed |
| GHOST before its dir exists | active / waiting, Result=success | MET: a row with no dir yet is a waiting unit, not a failure |
| GHOST after the dir + a file appear | **NOT TESTED** | **my script's flaw**: `mkdir /tmp/m2/ghost/...` ran as agi-alive under a root-owned `/tmp/m2` = Permission denied, so fired=0 is not a result. The record sha of the run stays 9e4180a5; the one line is re-measured by a separate one-shot, `.agi/context/local-maxxing/aa1m/host-act-2-ghost.sh` (1,674 B, sha256 a53de7d5fdf0437196cbab1d25197ff1af2f2136e3217b835ed3fd7aa8a946c2: root creates the dirs, the row user touches, it rolls itself back). NOT run |
| INOTIFY pid 1 | 10 -> 13 for 3 units | MET: +1 instance per unit; 32 rows = +32 against max_user_instances 128 (10 held before: 42 of 128) |

## What this does not show
The live install (`agi-carry@.path` on the real stores, the real carrier) is its own belam GO and DG3's build. The ghost-AFTER line (does a unit that waited on a missing dir attach when the dir appears) is unmeasured; it only matters for a row whose dir is not created before its unit starts, which the live design avoids by creating the dir at the post unit's start. I dry-checked this script with `sh -n` and `systemd-analyze verify` only, which could not catch a directory-ownership error under a root-owned /tmp/m2: a dry run that reproduces the real ownership (a root-owned parent, two uids) needs root.

## Closed by host act 2b (belam, root, 19:39:48Z, script `host-act-2-ghost.sh` sha256 a53de7d5 read whole, self-rolled-back: units 0, /tmp/m3 0, /run files 0; detail: experiment:dg2-aa1m-m2-host-act-2b)
| line | result | reading |
|---|---|---|
| GHOST before its dir exists | active / waiting | MET (as above) |
| GHOST after: root creates the dir, the row user writes a file | fired=**1**, still active | MET: a waiting unit ATTACHES when the dir appears |
| a 2nd write later | fired=**2** | MET: it keeps firing |
**Host act 2 is 8 of 8.** The GHOST-after row of the table above, "NOT TESTED", is superseded by this one. The live `agi-carry@.path` may take the default `paths.target` shape (no ordering after the post unit). Scratch units and a stub service on the real box: the live install on the real stores is unrun.
