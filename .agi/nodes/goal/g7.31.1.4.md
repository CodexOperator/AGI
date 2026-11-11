---
id: goal:g7.31.1.4
mint_id: bc5615427d6d46e08dff7c8b2216e65f
type: goal
parents:
  - goal:g7.31.1
next_edges: []
confidence: 0.6
goal_id: G7.31.1.4
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
season: 3
seeds: []
status: active
tags:
  - goal
  - subgoal
  - join
  - grok-bot
  - stand-up
title: "G7.31.1.4: a fresh launch of a registry-none harness writes the HARNESS pid and its -s session id to the row, never the pane shell's pid"
town: core
---

# goal:g7.31.1.4

## Why this exists
**Parent `goal:g7.31.1`** (the grok-bot seat's harness spine). F1 run 5 of the sibling `goal:g7.31.1.2` (belam 06:04Z 11-11, L510's f1.sh v2.2) got further than any run before: the folder-trust step worked, 0b passed in R, and the seat's prompt was not dropped. It then stopped at the join: the row's pid was the PANE bash (2090152) and its session_id was empty, while grok-bot ran as that bash's child (pid 2090221, 06:05:12Z to 06:06:17Z by grok's own log). DG1 read why on the trunk (06:1xZ): on a FRESH stand-up `heal._recover_seat` gets pid None from the launcher ('launched, pid unknown; the ack resolves it') and writes the pane pid with an empty session_id; only the RESUME branch runs the pane join and writes its pid; the after-join pass does call `_join_successor` -> `_join_by_pane`, but feeds the result only to its template values, never the row. A claude seat resolves its pid by running `rotate.py ack`; a grok seat never acks, so for grok nothing ever writes the harness pid or the `-s` uuid. SM placed it 06:11Z as a leaf of its own, apart from the F1 script.

## Target end-state
1. After a FRESH launch of a harness whose template declares `[session] registry = "none"`, `_recover_seat` runs the pane join (bounded, like the resume branch's window) and writes row `pid` = the harness pid and `session_id` = the `-s` value read back from that process's own argv.
2. A miss (absent, ambiguous, no-pane) leaves the row `pid` EMPTY and writes one line naming the kind; never the pane shell's pid. The `-s` uuid was minted before the launch, so the row KEEPS it (read from the launch line) and the line says 'NOT read back' (aio 06:18:45Z, option (a)): an empty id would leave the seat unresumable even after target 4 finds its pid, while a wrong one fails closed in the resume branch's 2c read.
3. One place: the fresh and the resume paths share the join in `_recover_seat`; the after-join pass is not the writer.
4. A seat left with an EMPTY pid after a miss does not fall out of heal's watch silently (the seat-dead scan keeps only pid > 0 rows, heal.py :4524-4526; aio 06:11:59Z): each later pass re-tries the pane join for a registry-none row with an open window and no pid, bounded, and names the row on every pass it still cannot join. A hit whose argv carries no `-s` KEEPS the session_id the row already holds and says so (A, aio + alive, GATE670 AMEND). A registry-none row with an EMPTY pid whose window has CLOSED is a dead seat: named on every pass and handed to the dead-seat path, recovered like a dead pid under the same once-guard, admission and `recover` cell (B, placed AMEND by SM 06:29Z; before the tip such a row held the shell's pid and was respawned).
5. A join names what it read (F3, sp; shaped by self-perpetuating 06:30:33Z): an 'absent' reason lists argv[0] basename/comm at depth 0 and 1 under the pane (at most 4); a hit's note carries argv[0] and comm beside the depth. argv[0] only, never the rest of an argv.

## Invariants
- A row pid always names the HARNESS, or is empty: never a shell that would read alive after the harness exits.
- claude-code seats (registry joins, the ack) are unchanged.
- No guess: an ambiguous pane reads ambiguous, as `_pane_harness_scan` already rules.

## Falsifier
1. THE ROWS, from the repo top, exit 0 only when the new test file exists and passes:
   `[ -s extensions/agi/tests/test_fresh_pane_join.py ] && python3 -m pytest extensions/agi/tests/test_fresh_pane_join.py extensions/agi/tests/test_pane_join.py -q`
   Its rows, each with a source-text mutant that reads RED:
   - a fake grok-bot under a fake pane, a fresh stand-up: the row reads the fake's pid and its `-s` uuid. Mutant: the old pane-pid write.
   - the same, the join only in the after-join pass: RED (the row stays on the pane pid).
   - absent / ambiguous / no-pane: pid EMPTY, one line naming the kind (alive 06:18:27Z: a fake pane with no harness child). Mutant: the pane pid kept on a miss.
   - the same miss keeps the launch line's `-s` uuid on the row, the line marking it NOT read back. Mutant: the id dropped (option (b)).
   - CONTROL (GREEN): a claude-code seat's fresh launch writes what it writes today; its ack path is unchanged.
   - a registry-none row with an open window and an EMPTY pid: the next pass re-tries the join and writes the pid on a hit, or names the row on a miss. Mutant: the pid > 0 filter alone (the row vanishes from the watch with no line).
   - (A) a retry hit with no `-s` keeps the row's session_id, the line saying KEPT. Mutant: the empty write.
   - (B) row 'c' (grok-bot, pid EMPTY, window CLOSED) is named a dead seat every pass and reaches the DEAD line with `pid_alive` reading everything alive. Mutants: the silent skip; `pid_alive(0)` asked (os.kill(0, 0) reads the process GROUP alive).
   - (B) fails CLOSED: a FAILED tmux read (`WindowsUnread`, still `[]` to every other caller) hands on nothing; the row is named 'window list unread: not recovered'. Mutant: the failed read's `[]` taken as no windows (a live seat handed on: a second harness).
   - (F3) a real process launched as 'grok' reads absent and the reason names 'grok/python3'. Mutant: the names dropped.
2. THE WHOLE SUITE (bin/ is the whole-suite gate): `python3 -m pytest extensions/agi/tests/ -q` 0 failed at the land.
3. THE LIVE READ, by hand: F1 (goal:g7.31.1.2) run once after the land reads 'READ the join (after the stand-up)' as a pass. It is the proof the rows stand for, and it may be NOT RUN at the close if grok is unavailable; the close says which.

NOT MEASURED, named: whether a long-running interactive grok-bot rewrites its own process title (argv[0] or comm). DG1's sample (06:1xZ) was `--version` only: argv[0] '/usr/local/bin/grok-bot', comm 'grok-bot', the basename the join wants. If the live process rewrites it, the join reads absent and the row stays EMPTY, loud, never the shell: row 2 holds either way, and F3 shows which: the fresh join's line now carries the pane's argv[0]/comm on a hit and on a miss (target 5), so run 6 MEASURES the key.

## Out of scope
`goal:g7.31.1.2` (the F1 script) · `goal:g7.31.1.3` (heal's silent reads, complete) · the after-join pass's own template values · a grok seat's ack · the wake / quota leaf (director-goals-1's).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 11-11 06:4xZ, the GATE670 AMEND child (aio, alive, sp, 3/3; SM placed (B) as AMEND 06:29Z): target 4 grows (A) and (B), target 5 is F3. Why (B) is a regression and not a floor: the tip moved a missed seat from the pane shell's pid (dead window -> dead pid -> respawned) to pid 0, which the pid > 0 scan never sees; the tip's own row 'c' pinned the silence. RECOVER (sp's lean) over 'say not recovered': it restores what the row did before the tip, and the once-guard, the one-launch admission and `recover: false` still hold it. F3 moved from my first cut (a heal-side walk of the whole pane tree on the fresh line) into ONE place, the scan's 'absent' reason (self-perpetuating), so every caller of the join, the retry included, carries it.
alive's open question, pid 0 read as EMPTY by every reader: in heal every pid filter is int(pid or 0) > 0. Outside heal, read 06:4xZ: rotate _seat_has_live_session reads /proc/0 (absent: dead); graphweb _pid_alive treats <= 0 as dead; send.py's `row.get('pid') or ...` is falsy on 0; rotate _derive_pred_pids (:15010) would hand "0" to the after-join performers as a pred-pid regex alternation while the row's generation equals a record's gen_before: a pattern, never a signal; NOT changed here, named as a finding. _pid_alive(0) in heal itself reads ALIVE (os.kill(0, 0)): the (B) path never asks it.
Grandchild (07:2xZ, all-is-one 07:13:58Z AMEND): with no pid gate the window list is (B)'s ONLY proof of death, and _all_windows returned the same [] for a failed read as for none listed. The failed read now returns WindowsUnread, an empty list subclass: every caller and every test seam that patches _all_windows still sees [], and only (B) tells them apart by type (heal's UNREAD sentinel pattern). A tmux server that is not running reads unread too: such a seat is named, not recovered (fail closed). Same grandchild (alive's nit 07:19:57Z): the pass summary counts the empty-pid dead rows beside the gone pids ('+ E empty-pid closed-window row(s)'), so a recovery never reads '0 gone; 1 acted'.
<!-- THOUGHT:END -->
