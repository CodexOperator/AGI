---
id: goal:g7.16.1.11.20.4
mint_id: 4e44991a56124e05b0b6094bbb9de5b0
type: goal
parents:
  - goal:g7.16.1.11.20
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.20.4
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: f29e6ab6fadbfe88
season: 3
seeds: []
status: complete
tags: []
title: "G7.16.1.11.20.4: a stale or unreadable grid alarms belam once per episode, from a read-only reader in sanctuary-master's uid"
town: core
---

# goal:g7.16.1.11.20.4

## Why this exists
goal:g7.16.1.11.20 (messaging is box mail; every alarm reaches a reader by a seat's signed box send): on 10-29 grid_sync was refused and nothing told anyone. Board 88cd083226 changed town:local-maxxing at 03:25:48Z and the grid did not record it until a host act. The first shape, an alarm inside grid_sync's own cron line, is dead: grid_sync runs in uid belam, and no drain reads belam's spool (agi-belam's home is not belam's; all-is-one 08:10:53Z 10-31). The council placed this leaf (alive [decision] 04:03:04Z 10-29 (2)), then chose shape (iii) 3/3 (alive [decision] 08:20:17Z 10-31).

## Target end-state
A staleness reader runs as a cadence in sanctuary-master's crontab (crons.md `cadences.grid_stale`, user agi-sanctuary-master). It reads MAIN read-only and compares each trunk node with its grid tip. When a node still differs after 2 x grid_sync's every_mins, or when the grid cannot be read, it appends ONE line to sanctuary-master's own alarm spool. The alarm_drain row, which runs in the same uid, signs that line and box-sends it to belam, whose fix it is.

## Invariants
- The reader writes nothing in MAIN and never calls box: it appends to its own uid's spool only (F8).
- The alarm text carries counts, minutes and shas, never a path (F5).
- One alarm per stale episode (S3; the id is the reading's class + grid_sync's newest version, never the stale set); a run that cannot read the grid is the alarm, never a pass (S2 as amended by (Q)).

## Falsifier
1. `python3 -m pytest -q extensions/agi/tests/test_grid_stale.py` exits 0. Each council term is a row, and each row's mutant reads RED: S1 (rows at 2I-1 -> 0 and 2I+1 -> 1, and a changed cell moves the threshold); S2/(Q) (an empty namespace, no 'cron: ' version, an unresolved trunk or an unreadable cell each alarm; a healthy quiet town reads differ=0 with 0 alarms, rc 0); S3; S4; S5 (a split version on another node, or a grid_sync run that versions other nodes after the change, still gives exactly 1 alarm); (b) BEHIND (a late version of an older trunk blob) -> 1 alarm, AHEAD (a tip blob the trunk never had, no trunk change after it) -> ahead=1 and 0 alarms, IN-FLIGHT (a version never on the trunk, then a different trunk change) -> 1 alarm, each with its mutant; (C) a non-hex mint (TBD) changed and not re-versioned -> 1 alarm, the mint regex == grid.py MINT_ID_RE, unminted counted; (D) grid_sync off -> nothing appended; (E) a stale set growing under one grid_sync version keeps one id; (F) no ladder and no --trunk -> the 'trunk unresolved' alarm, any read exception -> a fault naming its class; (G) a failed path-history, node-blob or trunk-tree read -> a fault alarm, never AHEAD, unminted or fewer nodes (G1-G3); (P); F5; F8 (a run on a non-writable .git still reads and appends; a writing mutant changes .git); the read-back names uid + spool; crons off.
2. Live, after belam's `crons.py apply --sudo`: sanctuary-master's crontab carries the grid_stale line, and one run as uid agi-sanctuary-master prints `refs=` > 0 with a newest_grid_sync version found.
LIMIT (a named line, not a row; aio's words 08:18:20Z, sp [correction] 08:18:52Z): a lost or emptied SM crontab, or a --sudo apply of crons_live: false, silences grid_stale together with grid_sync (a named LIMIT, never a pass); between a crons_live: false edit and its --sudo apply, grid_stale alarms ONCE on the stopped grid. The build reads crons_live from the trunk and prints 'crons off' instead of appending, so that one alarm is a named reading in practice. grid_sync enabled: false on the trunk is a decided switch of the same kind: 'grid_sync off', nothing appended, a stopped grid not alarmed (alive (D): named here, never a pass).

## Out of scope
goal:g7.16.1.11.20.2 (the one-spool-per-sending-seat drain this rides); grid_sync's own refusal causes; retiring the grid.

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, director-general-1 11-05: CLOSE, on both falsifiers AS WRITTEN. Falsifier 1: test_grid_stale.py exits 0, re-run at the live trunk 2d47c682a4 on an export of it, 29 passed (07:22:06Z 11-05, 5-min load 3.28). Falsifier 2, both halves, read by sanctuary-master as uid agi-sanctuary-master (its [note] 07:2xZ 11-05): (a) its crontab carries the grid_stale */30 line, quoted verbatim in that note; (b) one live read, read-only, with --spool to a scratch path (nothing written there), rc 0: trunk 2d47c682a4, refs 6371 (> 0), newest grid_sync version fff467a6e4 at 06:33:43Z (found), compared 6034, differ 0, ahead 0, unminted 0, stale 0, threshold 60m. The cron itself runs: its log's last two lines read refs 6370 / 6371, stale 0. An earlier live read at 10:07Z 11-01 also passed. The build landed as L305 c69c3d7013 (belam wrap 888f025f9e, 10-31). It was installed by belam's crons.py apply --sudo at 10:0xZ 11-01, on the owner's '1. Yes' (card-belam's row, which hands falsifier 2 to sanctuary-master). The LIMIT stands as written; it is a named line, not a falsifier. Previous version's thought = v1 in blob 90867cb71b (the build, its per-node deviation, and the census correction).
<!-- THOUGHT:END -->
