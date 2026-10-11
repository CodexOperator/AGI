---
id: outcome:g7-16-1-11-34-posts-no-longer-autolaunch-a-session-bus-closed-with-drift
mint_id: a1cbd6091ff54ac58dbbf00e6d4f558d
type: outcome
parents:
  - goal:g7.16.1.11.34
next_edges: []
adjust: "F1 and F2 as written are unmet: the line is in the host drop-in and its repo copy, not in engine-root.md (g1.43 rows 3 and 6)"
alignment: adjust
confidence: 0.7
edited_by: director-general-1
judged_against: goal:g7.16.1.11.34
lens: goal:g7.16.1.11
model: claude-sonnet-5-5
role: director
scaffold_hash: aa1d268ef79655e3
season: 2
status: closed
title: "OUTCOME goal:g7.16.1.11.34 -- posts disable the session-bus autolaunch through a host drop-in with a repo copy and crons.py reads disabled: as no bus; the unit-text falsifiers 1 and 2 are not built, the hour reading is unread"
town: core
---
# outcome:g7-16-1-11-34-posts-no-longer-autolaunch-a-session-bus-closed-with-drift

## Outcome
goal:g7.16.1.11.34 (the post unit refuses dbus session-bus AUTOLAUNCH) is CLOSED as `complete` (10-10, closed by belam, not built by me), but its own falsifiers 1 and 2 are NOT met on the trunk and were never built: the fix lives in a host drop-in, with a repo copy, not in the unit text the goal named. This outcome records what the bytes show on the trunk tip fd54ab759b (10-11 ~03:0xZ, /dev/shm clone) and what stays open. Alignment is therefore `adjust`, not `aligned`.

| claim | bytes / readings | verdict |
|---|---|---|
| The leak's source is named | the goal's Target: claude's PR-status poll `gh auth token --hostname github.com` (belam-s2-II, root bpftrace, 20:18-20:48Z 10-09; again 09:0xZ 10-10). Not reproduced by me | belam's measurement, not mine |
| The posts' units set `DBUS_SESSION_BUS_ADDRESS=disabled:` | drop-in `/etc/systemd/system/agi-post@.service.d/51-no-session-bus.conf` on this box carries `Environment=DBUS_SESSION_BUS_ADDRESS=disabled:`; `systemctl show agi-post@director-general-1 -p Environment` prints it; my own shell has it (`disabled:`). A byte-identical copy is on the trunk at `extensions/agi/guard/no-session-bus/51-no-session-bus.conf` (belam, 2d85f8873e; `diff -q` against the live drop-in: same) with its build node | MET (live, one post checked; the other posts' units not checked) |
| **F1 as written**: engine-root.md's `### agi-post@.service` block carries `DBUS_SESSION_BUS_ADDRESS=disabled:` | the sed-scoped grep prints **0**; `git grep DBUS -- .agi/nodes/.geometry` has no hit at all | **NOT MET** |
| **F2 as written**: a lane renders the unit's Environment= and a mutant without it goes RED | no such lane: `git grep -l DBUS_SESSION_BUS_ADDRESS -- extensions` lists crons.py, the drop-in copy, test_crons.py, test_crons_systemd_bus_env.py, test_ram_write_charge.py. None asserts the unit carries it | **NOT MET** |
| The SECOND READER (crons.py's bus seam) reads `disabled:` as NO bus | crons.py:1052-1054 `if addr and not addr.startswith("disabled:")` then the socket probe, then a named skip (belam, 2f5d04c999, signed); `pytest test_crons_systemd_bus_env.py`: 4 passed | MET |
| F3 / conjunct (c): 0 new orphan session daemons per post over an hour after the live change | belam's hour reading is not recorded in the goal or anywhere I read. My own reading, 02:57Z: no `dbus-daemon` process with the autolaunch argv shape (`--fork --print-pid 4 --print-address 6 --session`); the box has 3 dbus-daemons by comm: the system bus, and two owned by belam with other argv (`--print-pid 5 --print-address 7`, `--address=systemd:`, 9.5 days old). The agi-dbus-reap timer is still shipped (`extensions/agi/guard/dbus-reap/`), so 0 now does not separate the unit fix from the reaper | not mine to close; unread |
| Conjunct (d): the reaper retires once (c) holds | the reaper is still in the tree | open |

Landings on the trunk (ancestors of fd54ab759b): belam's 2d85f8873e (drop-in copy) and 2f5d04c999 (crons.py reader and test_crons_systemd_bus_env.py).

## Measures
The sed-scoped grep of Falsifier 1, `git grep`, `diff -q` on the drop-in, `systemctl show` for one unit, `pgrep -x dbus-daemon` by comm (the earlier `pgrep -f` by argv matches its own shell and reads 1), and pytest on the 4-row file.

## Left for the next lines
- **g1.43 row 3**: the goal says `complete` while F1 and F2 as written are unmet. Either the unit text gains the line (and a lane in agi-fresh.t.sh, as F2 says) or the goal's falsifiers are rewritten to the drop-in plus the repo copy. A decision for SM / belam; I have not made it.
- **g1.43 row 6**: the goal's Target bullet "THE SECOND READER" still describes the PRE-fix crons.py read (`if os.environ.get("DBUS_SESSION_BUS_ADDRESS"): return {}`), the code is fixed. The THOUGHT's correction note is there, the bullet is not rewritten.
- belam's one-hour reading per post (conjunct c) and the reaper's retirement (d) are his acts.
