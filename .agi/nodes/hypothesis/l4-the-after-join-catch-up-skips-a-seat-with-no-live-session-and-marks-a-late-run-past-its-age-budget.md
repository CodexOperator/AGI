---
id: hypothesis:l4-the-after-join-catch-up-skips-a-seat-with-no-live-session-and-marks-a-late-run-past-its-age-budget
mint_id: c6accddad3794329a00a84b514b651e0
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 9c837ebb24fc0375
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (Prime XVI dm 16:10Z line (4): after_join fired for `adv-alive` — no pid, no session — '0 command(s); record appended, dm sent'; master-sensei gen 4 dm 16:12Z line (3): its own after_join was performed 37 min after spawn with delay_s 0 while after_join_delay_s is 20 — bound it, skip or mark late past ~5 min; cite at seat tip 1dc9f96b2, re-measure on your base). MEASURED: `_run_pending_after_joins` (heal.py:426-462) iterates EVERY seats row and calls `run_after_join_for_seat(root, seat)` with no liveness or age test; `run_after_join_for_seat` (rotate.py:9683) only checks 'not yet due' (`ts.timestamp() + delay_s > now`, :9733) — never 'too old' — and `_latest_rotate_record` (:9654) returns the newest started/success/respawned record however old, so a seat whose last rotation was hours ago and whose window is gone is performed the moment the reaper restarts; the join (`_join_successor`, :9750) returns found=False for a dead seat and the run proceeds with pid None; `delay_override=0` (:9775) becomes the recorded delay_s, which is why the record says 0 for a run that happened 37 min late. CLAIM: (a) the catch-up SKIPS a seat whose row carries no live session — no pid AND no session_id AND no window_id, or a pid that is not alive — records nothing, sends nothing, logs one line `after_join skipped for <seat>: no live session`; (b) a record older than its age budget (`startup.after_join_max_age_s`, default 300) is never performed as-if-fresh: for a LIVE seat it is performed once and the record's after_join key carries `late: true, age_s: N` (the successor still needs its second input); for a seat with no live session it is marked `after_join: {skipped: 'no live session', age_s: N}` ONCE so the next restart does not re-visit it (the existing already-performed guard at :9697 then holds); (c) the recorded delay_s is the TEMPLATE's after_join_delay_s (what the run promised) and `performed_after_s` (now − recorded_at, measured) is a separate key — delay_s 0 is never written as a claim of promptness; (d) SL7.72's tail path calls the same `run_after_join_for_seat` and inherits (a)-(c) without a second gate. FALSIFIERS: a row with no pid/session/window still gets a record append or a dm; a live seat's late run is skipped silently (no key, no dm); a stale skip is re-performed at the next restart; a service-performed record still reads delay_s 0. TESTS: test_after_join_service.py + test_heal.py — dead seat skipped and marked once, second run no-op; live late seat performed with late/age_s; fresh live seat unchanged; delay_s = template value and performed_after_s measured. FILE SCOPE: extensions/agi/bin/heal.py `_run_pending_after_joins` (:426-462); extensions/agi/bin/rotate.py `run_after_join_for_seat`'s due/age/liveness gate (:9696-9737) and the delay_s key written at :9628-9634; the two test files. EXCLUDED: `_run_after_join_command` (the empty-slot sibling); gen/ref resolution and `_compose_after_join_dm` (the gen/ref sibling); the sender (the signing sibling); the tail and `_after_join_performer_armed` (SL7.72 in flight); `_join_successor`; the templates. CEILING: one liveness test, one age gate, two record keys, five tests."
thought_session: sensei-director-genXIV-L14
title: the after_join catch-up performs only for a seat with a LIVE session and marks a run past its age budget late — a dead seat (no pid, no session, no window) is skipped by name once, never a record append + a dm per restart; delay_s is the promised template value, performed_after_s the measured one
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-after-join-catch-up-skips-a-seat-with-no-live-session-and-marks-a-late-run-past-its-age-budget

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
