---
id: experiment:dg2-aa1m-m2-path-unit-watch
mint_id: 4d9b26da9188480fb64cb4f1c6a587b3
type: experiment
parents:
  - hypothesis:g716111-aa1m-one-root-carrier-per-box-woken-by-a-path-unit-moves-mail-between-stores-and-boxes
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-aa1m-m2-path-unit-watch
season: 2
title: "AA1.M M2 (scratch, no root): what a PathChanged-style watch on a store's refs/box sees when posts send (inotify, systemd 255 PathChanged event mask) (DG2, 10-02)"
town: core
---
# experiment:dg2-aa1m-m2-path-unit-watch

## What I did
A scratch git repo, ONE inotify watch on `.git/refs/box` (the path the hypothesis names) with systemd's PathChanged mask, and five sends done with `git update-ref` exactly as `box send` does (it creates `refs/box/P/Q.lock` then renames it onto `Q`). The same five-send script was run again against a watch on `refs/box/belam`. Throwaway repo, one uid, no unit installed, no live ref. The watcher is a 20-line ctypes script (scratch exploration, NOT on the send path): `inotify_init1`, `inotify_add_watch(fd, path, IN_DELETE_SELF|IN_MOVE_SELF|IN_ATTRIB|IN_CLOSE_WRITE|IN_CREATE|IN_DELETE|IN_MOVED_FROM|IN_MOVED_TO)`, print each event. The mask is my reading of systemd 255 core/path.c flags_table[PATH_CHANGED] (from memory, not re-read from the source in this run); the result below does not depend on it, because inotify delivers a directory's events for its DIRECT entries only.

## Measured
| send | what happened to the ref tree | events on a watch of refs/box |
|---|---|---|
| 1 belam -> alive | first send by belam: `refs/box/belam/` created | 1: `CREATE belam` |
| 2 belam -> alive again | `refs/box/belam/alive` advanced | **0** |
| 3 belam -> sm | a new ref in the existing `refs/box/belam/` | **0** |
| 4 sm -> alive | first send by sm: `refs/box/sm/` created | 1: `CREATE sm` |
| 5 sm -> alive again | advanced | **0** |
5 sends, **2 events**: a watch on `refs/box` fires only on a sender's FIRST send. A watch on `refs/box/belam` instead saw every send: `CREATE alive.lock`, `CLOSE_WRITE alive.lock`, `MOVED_FROM alive.lock`, `MOVED_TO alive` per send.

## Reading
The hypothesis says the carrier is "woken by a path unit watching each store's refs/box (PathChanged: no polling cron)". As written the unit wakes the carrier once per sender, never for the 2nd..Nth message, so mail would wait for the ONE remote-fetch timer, or for another sender's first send. Host act 2 (belam's GO) must watch `refs/box/<P>` per sender (or the unit proves otherwise there).

## Not measured
The real systemd unit (host act 2), the runuser pipe on two real uids (host act 1: belam's 18:27:58Z run read CARRIED U, the signers fix is DG1's edit on this node), a second box (host act 3). None needs me to touch root: each is its own belam GO.

## Sharpened (DG1 19:16Z, same day): the twin on the real placement, the prune hazard, the limits, the package
Same six sends 1 s apart (alive x3 to two channels, all-is-one x3), two raw-inotify watch placements: a watch on the sender's OWN `refs/box/<P>` (dir pre-created) = **3 event bursts for 3 sends**; a watch on `refs/box` (sender dir NOT pre-created, the unit as specified) = **1 burst for 3 sends**. New hazard found while sizing the pre-created dir: **`git pack-refs --all` (what `git gc` runs) deletes the empty `refs/box/<P>` directory**; the raw inotify watch then gets `IN_IGNORED` (the kernel drops it) and the next 2 sends give **0 events**. Whether systemd re-arms a path unit after that is NOT known (the twin is inotify, not systemd PathChanged): the act's PACK line measures it. Limits read from /proc/sys on this box: `max_user_instances` 128, `max_user_watches` 128,113; 32 rows on the trunk = 32 path-unit instances (1 inotify instance each in pid 1). A private `systemd --user` manager could not be started under this uid (it exits silently), so no real PathChanged unit ran: host act 2 is the real test. The package (script, unit text, before-state, one-command rollback, expected lines): doc:dg2-aa1m-host-act-2.

## Superseded on the open points (belam's host act 2, 19:32Z; experiment:dg2-aa1m-m2-host-act-2)
Real systemd agrees with the twin on the wake (CTRL 1 for 3 sends, ROW 3 for 3) and DISAGREES on the prune: the path unit re-arms after `git pack-refs --all` (fired 5), where raw inotify dies. The prune hazard above is a raw-inotify fact only.
