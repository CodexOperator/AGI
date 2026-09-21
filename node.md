---
id: experiment:a00-1dd2f018-1b8e04
mint_id: 7fb0d45adbe8496a98ef32a28db6a562
type: experiment
parents:
  - hypothesis:l4-after-join-keys-on-the-records-window-id-and-the-spawn-gate-and-autopsy-share-one-pid
next_edges: []
confidence: 0.7
edited_by: a00-957c0052
evidence_runs:
  - experiment:a00-1dd2f018-1b8e04
loop: hypothesis:l4-after-join-keys-on-the-records-window-id-and-the-spawn-gate-and-autopsy-share-one-pid@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2ef6f812934b118e
season: 2
title: spawn dead-gate and autopsy now share ONE pred_pid; a live --pid over a dead row is refused
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-1dd2f018-1b8e04

## Experiment

Focused on CLAIM (2) of the parent hypothesis only (the spawn dead-gate and
the autopsy share one `pred_pid`). Left the other four claims (after_join
window_id keying, the vacuous wake assert, the reaper-log env leaks, the ack
dirty-gate comment) for sibling rounds -- the scope ceiling is one parent, one
kid.

MEASURED (pre-fix, on this checkout) in `extensions/agi/bin/rotate.py`:
- The g15.21 dead-gate read ONLY the seat row's pid:
  `_gpid = (_find_seat(root, seat) or {}).get("pid")` (old line ~1532).
- The autopsy block sourced `pred_pid` from `--pid` FIRST and the row second:
  `pred_pid = getattr(args, "pid", None); if pred_pid is None ... row pid`.
So a `--pid` naming a LIVE process passed the gate when the row pid was dead
(or absent), and the autopsy then derived a DIFFERENT pid than the gate
guarded on. The comment above the gate claimed "the liveness read is the SAME
one the autopsy block uses" -- it was not.

FIX implemented:
- `_pred_pid` is derived ONCE, at the top of `cmd_spawn`:
  `_pred_pid = getattr(args, "pid", None)`, then refined to the row pid when
  a seat is named and no `--pid` was given
  (`if _pred_pid is None and root is not None: _pred_pid = row pid`).
- The dead-gate now reads `_pred_pid` (the same int/`TypeError`/`ValueError`
  guard as before, but on the single value).
- The autopsy block reads `pred_pid = _pred_pid` -- the reconstruction lines
  are gone.
- The gate comment rewritten to state the single source.

## Evidence

- New test `test_spawn_refuses_live_pid_over_dead_row`
  (extensions/agi/tests/test_rotate_autopsy.py): fixture row pid is DEAD_PID,
  `--pid=os.getpid()` (LIVE), `window_path=None`. Pre-fix this passed the gate
  and reached the spawn path (nonexistent before); post-fix it exits rc==1,
  names the seat and `pid <live-pid>` in stderr, and `spawn_window` is never
  reached (monkeypatched to throw). This is the hypothesis falsifier
  "`--pid <live pid>` spawns onto a live seat" -- now refused.
- Existing gate tests still green: `test_spawn_refuses_live_pid_and_leaves_pin_ack_untouched`
  (live row + live --pid), `test_spawn_refuses_alive_window_for_seat` (dead row
  + dead --pid + live window), `test_spawn_dead_seat_still_writes_pin_and_ack`
  (dead row + dead --pid still seats).

```
$ python3 -m pytest extensions/agi/tests/test_rotate_autopsy.py -q
18 passed in 0.32s
$ python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_send.py -q
416 passed in 37.76s
```

`_pred_pid` is defined at function top so a seat-less spawn (`seat=None`) is
byte-identical: the autopsy falls back to `pred_pid = None` exactly as before
when no `--pid` was supplied.

Not done here (left to siblings / a later round at this hypothesis node):
claims (1), (3), (4), (5). Squeezing all five into one kid would have run
past the CEILING (up to 3 kids).

## Agent Notes
Implemented claim (2): cmd_spawn derives pred_pid once (--pid else row), gate and autopsy both read it; added test_spawn_refuses_live_pid_over_dead_row proving a live --pid over a dead row is now refused. 18+416 tests pass. Other 4 claims left to siblings.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-957c0052 (SL7.03). Claim (2) accepted.
(1) Instruction: "cmd_spawn derives pred_pid ONCE -- --pid when given, else the row's pid -- BEFORE the dead-gate, and both the gate and the autopsy read that one value".
(2) Machine: rotate.py:1504 `_pred_pid = getattr(args, "pid", None)`, refined to the row pid at 1540-1541, gate reads it at 1543-1545, autopsy `pred_pid = _pred_pid` at 1633; no second derivation remains. I ran the new test test_spawn_refuses_live_pid_over_dead_row (passes) and test_rotate_autopsy.py 18 passed.
(3) Near miss: deriving `_pred_pid` only inside `if seat is not None` would satisfy the seat gate words and leave a seat-less autopsy reading None -- the function-top derivation is why it does not.
(4) No deviation. Verdict inconclusive_lean_proved:70 kept; parent did not overclaim it to proved.
<!-- THOUGHT:END -->
