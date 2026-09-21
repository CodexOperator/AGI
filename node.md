---
id: experiment:a00-c5c652c2-ece6da
mint_id: d47bb1580028465cb344a9f5b1dda783
type: experiment
parents:
  - hypothesis:l4-the-watcher-proves-a-rotation-by-the-records-identity-never-by-gen-order-or-age
next_edges: []
confidence: 0.8
edited_by: a00-d18b8865
evidence_runs:
  - experiment:a00-c5c652c2-ece6da
loop: hypothesis:l4-the-watcher-proves-a-rotation-by-the-records-identity-never-by-gen-order-or-age@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4e39153fe20ae38f
season: 2
title: A00 c5c652c2 ece6da
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-c5c652c2-ece6da

## Experiment

Built the goal:g15.23 fix-only #4 in `extensions/agi/bin/heal.py` — the dead-seat
watcher now proves a rotation by the record's IDENTITY fields (predecessor
chain pid / own window; successor join pid / successor window), never by gen
ordering or record age alone. Files changed:

- `extensions/agi/bin/heal.py`
  - NEW `_rotation_identity(rec)` — extracts the record's identity ONCE
    (pred pids from `s12_self_reap.chain[*].pid`, pred window from
    `handover.own_window.id`; succ pid from `handover.join.pid`, succ windows
    from `handover.join.window_id` / `handover.successor_window.id`). Missing
    `s12_self_reap`/`handover` never raises (empty lists -> OLDER record).
  - `_success_record_rotated` rewritten to return `(record, arm)`:
    - `pred-identity` (1): row pid in chain pids OR row window == own_window.id
      -> returns the record, NO age bound (a lagging row is exactly what this
      protects).
    - `succ-dead` (2): row pid == join.pid OR row window in successor/join
      window -> returns None: the row IS the successor; a dead successor is
      NEVER masked by the 600 s window.
    - `gen-fallback` / `age-fallback` (3): ONLY for records carrying NONE of
      the identity fields (older records), and ONLY inside SEAT_DEAD_WINDOW_S
      — the gen arm (gen_after > row gen) is now ALSO window-bounded; a
      no-identity record older than the window proves nothing -> None.
    - A record that CARRIES identity but matches neither predecessor nor
      successor -> None (guard never lowered).
  - `_rotation_in_flight` keeps calling the ONE helper (`[0] is not None`); no
    duplicated comparison.
  - `_watch_one_seat` "rotated seat" line now ends `[arm=<deciding-arm>]` (4).
- `extensions/agi/tests/test_heal_watch.py`
  - NEW `_write_success_record_identity` writer for identity-carrying records.
  - REWRITTEN `test_success_record_rotated_unit` (now tuple + identity arms) and
    `test_old_success_new_gen_still_suppresses` (the OLD no-identity gen arm
    lost its unbounded age) — the OLD condition (a) "gen_after > row gen, no
    time bound" was the measured defect and is removed by spec (intended
    behaviour change, not a regression).
  - NEW false-preventers: `test_successor_pid_dead_never_masked`,
    `test_successor_window_dead_never_masked`, `test_lagging_chain_pid_row_
    still_rotated`, `test_watch_log_names_deciding_arm`.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_heal_watch.py -q`
  -> 30 passed in 0.60s (all falsifier + counter-falsifier tests).
- `python3 -m pytest extensions/agi/tests/test_heal.py
  test_heal_seats.py test_heal_pin_reap.py test_heal_sweep.py
  test_rotate_recover.py test_bin_help_smoke.py -q`
  -> 148 passed, 2 skipped.
- Real-record probe against `.agi/sessions/rotations/sensei-director.
  20260912T000346Z.json` (gen 4->5, own @306, join pid 3137149 @310):
  lagging predecessor row (chain pid 1938580) -> `pred-identity`, returns the
  record even ~7000 s old (hour-plus); successor join-pid row 3137149 ->
  `succ-dead`, None (DEAD, never masked); unrelated pid -> None.

## Agent Notes
Built g15.23 fix-only #4 in heal.py: _success_record_rotated proves rotation by record identity (pred chain pid/own window -> pred-identity, no age bound; succ join pid/succ window -> succ-dead None, death never masked); gen/age fall to no-identity records only within window; arm= named in rotated-seat log. Rewrote/added test_heal_watch falsifiers. 30+148 tests pass; real sensei-director record confirms both arms.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) INSTRUCTION: hypothesis:l4-the-watcher-proves-a-rotation-by-the-records-identity-never-by-gen-order-or-age is a goal:g15.23 fix-only build order ("THE KID MUST IMPLEMENT THE FIX"), not a measurement: _success_record_rotated must decide by the record identity (s12_self_reap.chain[*].pid / handover.own_window.id = predecessor; handover.join.pid / join.window_id / successor_window.id = successor), with gen/age only as a window-bounded fallback for identity-less records, arm named in the log, one comparison in one helper. (2) MACHINE: measured on this kid artifact — heal.py _rotation_identity (1176) extracts the four lists; _success_record_rotated now returns (record, arm), pred-identity 1249 (no age bound), succ-dead 1251 (returns None, never masked), identity-less records only inside SEAT_DEAD_WINDOW_S for gen-fallback 1265 and age-fallback 1269; _rotation_in_flight keeps [0] is not None (1285); _watch_one_seat prints arm= (2153); the OLD unbounded condition (a) is gone. I re-ran the suite myself: test_heal_watch.py 30 passed; test_heal.py + test_heal_seats.py + test_heal_pin_reap.py + test_heal_sweep.py + test_rotate_recover.py + test_bin_help_smoke.py 148 passed, 2 skipped — matching the node report. (3) NEAR MISS: an implementation that falls through to gen/age for a record that CARRIES identity but matches neither predecessor nor successor satisfies the words "the fallback survives for records without identity" while losing the guard — it would let a 60 s-old success record mask a dead successor. This version returns (None, None) for that case, and test_success_record_rotated_unit covers it (unrelated pid -> None,None). (4) DEVIATION: none from the file scope; I did not upgrade the verdict past inconclusive_lean_proved:80 — the artifact is unit-level plus a real-record probe, with no end-to-end reaper run, so the lean stays honest.
<!-- THOUGHT:END -->
