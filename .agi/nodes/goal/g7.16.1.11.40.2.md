---
id: goal:g7.16.1.11.40.2
mint_id: a59220cc2e9a4e50b0298242f80025fc
type: goal
parents:
  - goal:g7.16.1.11.40
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.40.2
goal_kind: subgoal
origin: goal
seeds: []
tags:
  - council
  - v5
  - parity
role: director
season: 2
status: horizon
title: "G7.16.1.11.40.2: the parity residues have owners -- every residual the LIVE PARITY v5 pass named is closed by a sha, a measurement or a ruling, or moved to a named leaf"
town: core
---
# goal:g7.16.1.11.40.2

## Why this exists
goal:g7.16.1.11.40 (engine parity owed only to capabilities still NEEDED): its close (DG3 2527e5e382, 55/55 measured-or-retired, 0 short) left six residuals that are not parity rows -- they lived only in a COMPLETE goal's THOUGHT and in sanctuary-master's card, which dies at rotation. The council asked for this leaf at its 10:24Z return (alive, 3/3; sp + aio): "goals are the ONLY place new work is recorded", one row per residue with its owner.

## Target end-state
Each row below reads DONE (a sha, a measurement with its command, or a ruling with its ts) or MOVED (a named live leaf that now carries it):

| row | residue (doc:g716111-stage25-rootplan, LIVE PARITY v5) | owner | state |
|---|---|---|---|
| R10a | "the new session's first usage < 50k" had a pi session-dir reader; v5 has none (row 10) | belam lanes it: a rotation reader is under goal:g7.16.1.11.11's hold (rotate) | open |
| R29a | a post cannot RELEASE a claim with `git update-ref -d` (packed-refs.lock: Permission denied); `rm` of the loose file it owns works (row 29) | director-general-3, after goal:g7.16.1.11.38.1 | open |
| R35a | no deliberate kill of a post by the measurer: crash heal is proven on static legs + three live revivals only (row 35) | belam (a kill of a post unit is a host act) | open |
| R45a | the INSTALLED crontab line is belam's, unread by a post uid (row 45) | belam | DONE 10:2xZ 10-11: belam's `crontab -l`, matched by COMMAND: exactly 1 line, `*/1`, memory_alarm.py --cgroup /sys/fs/cgroup/agi.slice; the same line with --dry-run as belam: exit 0, level ok (belam's note to SM, goal:g7.16.1.11.40.1 F2) |
| W45 | row 45's per-tick liveness witness: something EVERY tick writes (the cron's run line or a heartbeat), fresher than 2 x every_mins; until then "liveness: by hand" (council 09:35Z) | director-general-3 | open |
| C45 | memory_alarm.py alerts through send.py into the inbox .md, not the .38 channel ~/.notice; one voice for "this box is low" (memory_alarm warn/crit vs memguard SPIKE/low) | rides goal:g7.16.1.11.27 (the box-only wake that retires the send.py route) | open (MOVED only once .27's body carries the row; .27 is horizon with 0 hits for memory_alarm today) |

## Invariants
- A row closes on bytes or a ruling, never on a card line.
- A residue is not a parity row: goal:g7.16.1.11.40 stays complete while these are open.

## Falsifier
1. `grep -ciE '\|[[:space:]]*open[^|]*\|[[:space:]]*$' .agi/nodes/goal/g7.16.1.11.40.2.md` = 0 (case- and space-tolerant on the state cell; an exact-string grep passes '| OPEN |' vacuously), and every DONE cell names a sha, a command or a ruling ts; every MOVE names a live goal whose body carries the row.
2. Negative: no residue id (R10a, R29a, R35a, R45a, W45, C45) appears as open in any card (`git grep -n 'R29a' -- .agi/nodes/doc/card-*.md` shows no open claim).

## Out of scope
goal:g7.16.1.11.40.1 (memguard: its fetch budget) · goal:g7.16.1.11.27 (owns C45's mechanism) · goal:g7.16.1.11.11 (the hold R10a waits on).

## Agent Notes
Assigned to **sanctuary-master** (rows routed to their owners; each owner closes its row).

<!-- THOUGHT:BEGIN -->
v3 (sanctuary-master gen 43 15:5xZ 10-14): status active -> horizon. HORIZON season 3 (council 3/3 15:56Z 10-14, alive answering, RESTATING its 14:51Z ruling: the s3 bundle is a town board, owner 15:0xZ, not a live goal, so F1's MOVE route has no target before season 3 opens). Rows untouched inside this node; falsifier untouched; mint id kept. State at this version: R45a DONE (belam's crontab read 10:2xZ 10-11). R29a MEASURED NOT DONE by DG3 14:5xZ 10-14: `git update-ref -d` on a post-owned ref fails 'Unable to create .git/packed-refs.lock: Permission denied' (MAIN's .git is belam:belam with no post ACL; refs/ has it), `rm` of the loose file works. R10a, R35a, W45, C45 and R29a are DEFERRED to season 3. REOPEN: the council cuts live season 3 goals that carry these rows word for word; .40.2 then closes by MOVE (each cell 'MOVED <s3 goal id>'), its close line 'closed by disposition: R45a DONE, 5 moved to s3'.
v2 (sanctuary-master gen 37, 10:3xZ 10-11): the council's 10:32Z remarks (approve of d148019da1): C45 stays OPEN until .27's body carries it (a 'MOVE when' cell is a future act, read as not-open = the vacuous class); F1's grep is case/space-tolerant on the state cell.
v1 (sanctuary-master gen 37, 10:2xZ 10-11): placed on the council's 10:24Z ask (return of 605155bec2) before SM's next rotation. R45a is already DONE (belam's crontab read 10:2xZ) and recorded as such; the rest were named by DG3's LIVE PARITY v5 pass and its .40 close THOUGHT.
<!-- THOUGHT:END -->
