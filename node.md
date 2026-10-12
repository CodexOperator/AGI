---
id: goal:g7.16.1.11.20.2
mint_id: 84f3c796a3d6475cba2f4bdc9017905b
type: goal
parents:
  - goal:g7.16.1.11.20
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.20.2
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: master
season: 2
status: active
title: "G7.16.1.11.20.2: every alarm reaches its reader as signed box mail -- 0 send.py sends, 0 pane writes, ONE message per alarm"
town: core
---
# goal:g7.16.1.11.20.2

## Why this exists
goal:g7.16.1.11.20 (messaging is box mail; send.py retiring one caller at a time): belam measured (19:5xZ 10-11) that the ONLY writer left on the old send.py path is memory_alarm.py (memory_alarm.py:153 calls send.py), run as TWO cron jobs in uid belam's crontab, crons.md memory_alarm + memory_alarm_posts, both '--notify belam': 48 UNSIGNED messages into .agi/sessions/inbox/belam.md since 00:00Z, each alarm doubled. No other inbox, comms/dm or room file has been written since 10-09. At 21:2xZ the owner widened it from memory_alarm to ALL alarms, and from 'off send.py' to 'box mail' (below); belam measured the five alarm writers on the box (Inventory).

## OWNER 2026-10-11 19:5xZ, verbatim (via belam)
"And we need to fix whoever is using the old mail path."

## OWNER 2026-10-11 21:1xZ-21:2xZ, verbatim (via belam)
"Pressure alarm should use new mail system also" · "All alarms".

## Inventory (measured by belam 21:2xZ 10-11; one row per alarm writer)
| # | writer | runs as | path today | target |
|---|---|---|---|---|
| 1 | memory_alarm + memory_alarm_posts | uid belam crontab | send.py inbox, UNSIGNED, doubled | box |
| 2 | `send.py wake --all-local` */2 | uid belam crontab, block agi-3fbc6951; rendered by crons.md job nudge_sweep (crons.py:968-977) | the OLD wake path | retire, or box-wake if it still has a job (agi-boxwake@ x12 already wakes on box mail) |
| 3 | agi-memguard.py | root | journal + /var/log + ~/.notice via runuser | box |
| 4 | agi-rc-keepalive | root timer | types '/rename' and a message INTO the post's pane: not mail | NOT AN ALARM (target 1): stays a named pane write |
| 5 | agi-quiet-watch | root timer | box: runuser -u agi-<SELF> ... 'cd ~/t && box send <TO>' (SELF=belam :9, TO=sanctuary-master, send at :24): root signing with a seat's key | LIVE BREACH of .40.1 item 4 (council 21:3xZ): move onto belam's spool in this build |

## Target end-state
1. EVERY alarm reaches its reader as BOX MAIL (a signed ref, AA1.M), never send.py and never a pane write. A ~/.notice line may stay as a SECOND copy; box mail is the target, not 'cut 2 later' (owner 21:2xZ). Row 4 (agi-rc-keepalive) is NOT an alarm: its product is a turn in the post itself and self-mail is off-matrix (box:6), so it stays a named pane write outside this target.
2. ONE SPOOL PER SENDING SEAT (council 3/3 21:3xZ; .40.1 item 4 SCOPE: a seat's key signs only in the seat's own uid; root signing as a seat = RED):
   (1) a ROOT alarm source (memguard, quiet-watch) only APPENDS a plain line, no key, to the SENDING seat's spool (/var/lib/agi/<seat>/alarm.spool, by runuser as a plain append like ~/.notice);
   (2) ONE drain job in that seat's uid (a crons.md row with `user: agi-<seat>`, or a .path unit User=) signs + box-sends. Alarms to belam -> SM's spool + SM's drain (belam -> belam is off-matrix, box:6). quiet-watch (-> SM) -> BELAM's spool, a drain in agi-belam's uid;
   (3) every alarm message: subject `[alarm <job>]` + trailer `Alarm-job: <name>` (the .42 Board-job pattern), so a reader tells the seat's word from its machine;
   (4) a failed send ([off-matrix] / [squatted] / [unsent] / timeout) leaves the line in the spool + a ~/.notice line, never silent; memguard's append rides the post-stop fire-and-forget path (council (g)), off the stop path.
   The <box>-host identity stays banked; not a precondition.
3. ONE message per alarm, not two: one job owns the notify for a given alarm kind, the other reports nothing.
4. FLAP (belam 20:0xZ 10-11: WARN 20:02:01Z -> CLEARED 20:03:02Z while his own read at 20:03:21Z was PSI some avg60 16.70; each episode = 4 unsigned messages): a CLEARED is sent only below the line, in the WARN's units, with a margin and a hold named in crons.md. Built in DG1 571f300635 (--clear-margin-frac 0.8, --clear-hold-mins 3).
5. Row 3 (agi-memguard -> SM's spool, post-stop fire-and-forget, council (g)) is NOT built by item 2 (DG1 ..de08f0dcd8): it is the next cut (C3); no merge-up says "all alarms on box mail" while memguard is on journal + ~/.notice.
6. Cut 1 (DG1 1284b57f98 -> 571f300635: send.py out of memory_alarm.py, notice via agi-notice in uid agi-belam, one notice per alarm, the flap hold) is a step on this path, not its end: the box send for rows 1-4 follows it at once.
## Invariants
- Every threshold stays in crons.md (none in code), including SM's warn-psi-some 10 -> 30 on both rows: no cut reverts it.
- An alarm that cannot notify says so on stderr and in its log, and never fails the job silently.
- A root unit's install and `crons.py apply --sudo` are HOST ACTS by belam at the ff, never a builder's.

## Falsifier
1. (a) grep the box's crontabs + units + /usr/local/sbin + /opt/agi/bin: 0 'send.py' sends and 0 pane writes for alarms (belam measures; rows 1-3; row 4 is not an alarm, target 1).
2. (b) each alarm kind arrives ONCE (not doubled) as a G-signed box message at its reader; a row per kind. Mutant: both memory_alarm jobs notify = RED.
3. (c) a CLEARED is sent only below the line (target 4): a reading that dips under for one tick and returns sends no CLEARED; mutant 'clear on the first tick below' = RED.
4. (r1) the scripts every root unit/timer ExecStart's (/usr/local/sbin, /opt/agi/bin): 0 `box send`, 0 `ssh-keygen -Y sign`, else RED (21:3xZ: 1 hit, quiet-watch:24).
5. (r2) every alarm message's signer = the spool owner's key, never from root's process tree; the .40.1 mutant stays GREEN.
6. (r3) a spool line is sent exactly once: a failed send is retried next run, a sent one never twice. Mutant: a drain that re-sends a sent line = RED.
7. After the first live hour: 0 new lines in .agi/sessions/inbox/belam.md from any alarm, and `git grep -n "send.py" extensions/agi/bin/memory_alarm.py` = 0.

## Out of scope
The rest of send.py's retirement (goal:g7.16.1.11.20, .27) · the <box>-host identity (council design, banked; not needed here).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 40 23:0xZ 10-11: council 3/3 fix-forward on landing item 3: inventory row 4's cell and falsifier 1(a) ('rows 1-4') contradicted target 1 (row 4 NOT AN ALARM), so 1(a) would be RED by design on the keepalive we kept -> row 4 cell = NOT AN ALARM, 1(a) = rows 1-3; target 5 names row 3 (memguard) as not built by item 2. Item 2 itself RETURNED by the council (a silent loss: an append through an fd opened before drain's rename lands in the unlinked .draining inode); DG1 re-cuts.
sanctuary-master gen 40 21:3xZ 10-11: council 3/3 (alive answering) on SM's signer [decision]: not A/B/C but A-AMENDED, one spool per sending seat. Target 2 of the previous version named row 5's shape (root runuser's into a seat and box-sends as it) as THE pattern; that is root signing with a seat's key, which .40.1 item 4's falsifier reds, so this version replaces it with spool (root appends, no key) + drain (the seat's own uid signs), marks row 5 a LIVE BREACH to move in this build, adds [alarm <job>] + Alarm-job trailer and spool retry, rows r1-r3, and states row 4 as not-an-alarm in target 1 (else target 1 reds it). Rows 2 (nudge_sweep retired) and 4 unopposed. Previous (21:2xZ): owner "All alarms" moved the target to signed box mail for every alarm; belam's 5-row inventory; DG1 found belam -> belam off-matrix (box:6). Earlier: DG1 picked .42's user: field for cut 1; minted on the owner's 19:5xZ order via belam.
<!-- THOUGHT:END -->
