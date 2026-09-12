---
id: goal:g15.19
mint_id: 88fe7970147c4c8aaaabbde7865c5c93
type: goal
parents:
  - goal:g15
  - build:bin-heal
next_edges: []
confidence: 0.7
edited_by: sensei-director
goal_id: G15.19
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: c562626d89e84cb6
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - l4
  - sanctuary-director
title: "G15.19: Graceful recovery when a seat's process dies without a rotation — the watch pass detects the dead seat, respawns it on its own brief, writes its row, and tells its rotator"
town: core
---
<!-- BODY:BEGIN -->
# goal:g15.19

## Agent Notes
**A seat whose process dies is recovered by the loop, not by a human noticing.** Measured 2026-09-11: prime X (`belam` gen 10, @281, pid 3526521) died ~17:51:50Z with no rotation record (last: 14:03Z), no successor, and the seat stayed dead until the owner saw the GUI go blank and the sanctuary director spawned XI by hand at 17:58Z (`rotate.py spawn --tier prime_director`, row written on the owner's GO). Seven minutes of a headless loop, recovered only because a human was watching.

## Why this exists

- `goal:g15` is the parent because this is a fix to a live failure of the loop's own machinery, done in-loop (owner 2026-09-11 17:5xZ: "add doing graceful recovery in case of crashes").
- `build:bin-heal` is the parent because `heal.py watch` is the persistent pass that already reads every seat row each poll (`_repair_stranded_wakes`, 30 s) — detection belongs there, not in a new daemon.

## Testable claim (a build order)

(1) DETECT: on each watch pass, for every seat row with a `pid`, a seat is DEAD when its pid is gone AND its `window` @id is absent from tmux AND no rotation record for that seat is `started` within the last 10 minutes (a rotation in flight is not a crash); a dead seat is named ONCE on stderr and in the watch log with the row's cells. (2) RECOVER: the pass respawns the seat through the existing spawn path for its tier (`spawn_window` with the row's model/effort/settings, the prime on the standing prime brief, a director/helper on its quorum scratchpad via the same template `rotate-self` uses), names the successor by the seat's rule (numeral chain for `belam`: next numeral; plain seats: the seat name), writes the row's `generation`/`window`/`pid`/`session_id` exactly as rotate-self does at spawn (session_ref stays empty for the successor's ack), pins the meter, and dms the seat's `rotated_by` holder AND the Sensei one line (`[crash-recovery] <seat> pid <old> dead at <ts>; respawned <name> @id <id>`); the successor wakes on its ordinary handoff (the prime's live `HANDOFF.md`, a director's quorum scratchpad) — nothing is composed specially. (3) GRACEFUL: what the dead seat held is released, never lost — a stale `verify-suite.lock` under the dead seat's tree is removed with a log line; rounds it dispatched keep running (dispatch already exits after the spawn); its inbox unread stays unread for the successor; the recovery is recorded as a rotation record with `rotation: crash-recovery` so `status --record latest` and the Sensei audit see it. (4) NEVER: a seat with `crons_live`-style opt-out (`recover: false` in its row) is named, not respawned; a seat whose pid is alive is never touched; two passes never spawn twice (the record from (3) is the guard). TESTS: fixture rows + a fake process table + a fake window list: dead seat -> one spawn, one row write, one dm, one record; alive seat -> nothing; in-flight rotation -> nothing; second pass -> nothing. PROOF ON THE REAL TREE: kill a throwaway seat's spawned window and watch one pass recover it (paste). CEILING: 2 kids serial (detect+record, then respawn+row). FILE SCOPE: extensions/agi/bin/heal.py, extensions/agi/bin/rotate.py (spawn_window callers ONLY; nothing in first_turn/bootstrap/handoff — the sensei-director's regions), tests. EXCLUDED: the ladder, config:seats schema (a `recover` cell is the prime's edit), moral:*.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 2026-09-11 17:5xZ, verbatim to sanctuary-director after prime X died: 'add doing graceful recovery in case of crashes. Also do a goal to figure out why the crash happened if there's a good, preventable reason other than something somewhat random due to VPS cloud environment.' and 'Make sure both the goals I just shared go as subgoals under g15'.
<!-- THOUGHT:END -->

2026-09-12T00:33Z P2 recorded, not cut (Prime XIII 00:20Z, L4.292 residue 1): run_after_join_for_seat feeds the service's pin/ack an EMPTY succ_transcript/succ_ref — the join must key on the record's window_id. Brief when the P1 rounds (SL6.01-03) land; measure run_after_join_for_seat and the record's window_id on the merge-up commit that carries them.

2026-09-12T03:24Z P2 cut as SL7.03 (sensei-director gen VII) under hypothesis:l4-after-join-keys-on-the-records-window-id-and-the-spawn-gate-and-autopsy-share-one-pid: run_after_join_for_seat re-joins by the record's handover.join.window_id through _join_successor, fills succ_transcript, never puts a session id in the ref slot; bundled with the g15.21 and g15.24 residues (one pred_pid for gate + autopsy; test hygiene). Functions disjoint from F1's mint legs by an explicit EXCLUDED list.

2026-09-12T04:00Z SL7.03 harvested on the seat (sensei-director gen VII): after_join keys the successor on the record's handover.join.window_id through _join_successor (succ_transcript filled; succ_ref only from the row's own session_ref cell — never a session id); cmd_spawn derives _pred_pid once before the dead-gate (a live --pid over a dead row refuses); the vacuous wake assert now runs after wake(); AGI_REAPER_LOG writes are monkeypatch with a leak detector; the ack dirty-gate comment states SL6.09's own-row scope. Kids a00-1dd2f018 lean:70 + a00-7f1b92e3 lean:80; 834 green rotate+send+heal on the seat. Found and documented: _join_successor(poll_secs=0) never reads the registry. Lands at SL2#13.
