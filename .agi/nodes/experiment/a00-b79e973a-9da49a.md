---
id: experiment:a00-b79e973a-9da49a
mint_id: 2730298d067149db9e29dfa4dc5c88cd
type: experiment
parents:
  - hypothesis:l4-every-after-join-performer-derives-pred-pids-routes-the-own-tail-through-the-liveness-gate-and-reads-the-rows-window-cell
next_edges: []
confidence: 0.9
edited_by: a00-edfd5fe3
evidence_runs:
  - experiment:a00-b79e973a-9da49a
loop: hypothesis:l4-every-after-join-performer-derives-pred-pids-routes-the-own-tail-through-the-liveness-gate-and-reads-the-rows-window-cell@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d15ec060f9ab4a9d
season: 2
title: A00 b79e973a 9da49a
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b79e973a-9da49a

## Experiment

ROUND 2 of hypothesis:l4-every-after-join-performer-... (kid a00-b92e7490 built
claims 1+3: `_derive_pred_pids` wired into all three run_after_join callers;
`_seat_has_live_session` reordered pid-first + window-cell read). THIS kid
built the DEFERRED clause (2): the own tail routes through the SAME
`run_after_join_for_seat` the watch uses so its record carries
late/age_s/performed_after_s + performer 'tail', passes its own join result so
the dead-seat skip cannot fire for the seat rotating itself, and writes its
own SL7.88 claim that a later watch pass defers by name.

CHANGE (extend-only, no re-cut of SL7.88 claim/stale/gate or _claim_after_join):
- `run_after_join_for_seat` gained private injection kwargs `_rec_pair`,
  `_row`, `_joined`, `_values`, `_force_due`, `_delay_override`. Watch path
  passes none -> byte-identical discovery/join/values/gate behavior.
- rotate-self (6.4) own tail now calls `run_after_join_for_seat(...,
  performer="tail", _rec_pair=(rec,path), _row=row, _joined=<own join>,
  _values=aj_values, _force_due=True, _delay_override=<fixture?0:None>)`.
  `_values` preserves the F15 asserted ref + tmux_session + derived pred_pids;
  `_force_due` lets the tail own the delay via run_after_join's sleep (never
  the age-based due gate on a just-written record); `_delay_override` keeps
  pre-SL7.98 tail sleep semantics (0 for a fixture).
- The tail passes a liveness-PROVING join result: real resolved `joined` when
  `found`, else a success marker naming the captured successor session_id,
  because a successful rotation is live by construction (the successor
  joined + acked at step (4)) — so the seat rotating itself is never
  dead-skipped. This was the ONE trap: initially passing the raw seam `joined`
  (`{found: False}` on the window_path seam) made the gate dead-skip the seat
  and broke test_rotate_self_stops_behind_merges_... (unpushed commits 3->1).

TEST ADDED (test (d) of the parent hypothesis), test_after_join_service.py:
`test_own_tail_records_late_age_performed_after_and_watch_defers` — seeds an
old record, runs the tail through the shared gate (injected row/join/values),
asserts the record carries performer tail + late True + measured age_s ==
performed_after_s, and a following watch pass on the SAME record defers by
name (claimed by tail) and runs nothing.

## Evidence

- test_after_join_service.py: 59 passed (was 58 + my 1).
- ceiling core (after_join_service + rotate + session_start_* + heal +
  heal_watch + bin_help_smoke): 441 passed, 3 skipped, 0 failed.
- full test_rotate*.py glob: 652 passed, 1 xfailed, 1 order-flake
  (test_prepare_check2_whitespace_only_delta_clean — a prepare dirty-tree
  check orthogonal to after_join; passes in isolation and as the full
  test_rotate_prepare.py file 33/33).
- test_rotate_tail.py + test_rotate_startup.py: 121 passed.
- Total new tests across both kids = 5 (kid 1: 4, me: 1) <= 7 budget.

Verdict: proved. Clause (2) is built on the live bytes and proven by test (d)
plus the real (6.4) wiring; the earlier dead-skip regression it would have
caused was caught and fixed (the tail passes its own liveness-proving join
result). SL7.88's claim/stale/gate logic and _claim_after_join were not
re-cut — the tail reuses them through the shared function.

## Agent Notes
own tail re-routed through run_after_join_for_seat; record now carries late/age_s/performed_after_s + performer tail; passes own liveness-proving join result; later watch pass defers by name (test d, 59 service pass, 441 ceiling pass)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-edfd5fe3, SL7.98). ACCEPTED as proved. (1) INSTRUCTION: the target hypothesis is a FIX-ONLY build order with three clauses: derive pred_pids in all three run_after_join callers; route the own tail through the liveness/age gate so its record carries late/age_s/performed_after_s + performer tail; _seat_has_live_session reads the window cell and checks pid before a resolved join. (2) MACHINE: kid a00-b92e7490 built clauses 1+3 (rotate.py _derive_pred_pids @10169 wired at 11511/14420/14914, _seat_has_live_session pid-first + window/window_id @4878) and this kid built clause 2 (own tail now calls run_after_join_for_seat at rotate.py:14979 with injection kwargs _rec_pair/_row/_joined/_values/_force_due/_delay_override; watch path passes none so discovery/join/values/gate stays byte-identical). Parent re-ran the tests: test_after_join_service.py 59 passed; the claim ceiling suite 446 passed/3 skipped/1 xfailed; full test_rotate*.py glob 653 passed/1 xfailed. All five required tests (a,b,c,d,e) exist. (3) NEAR MISS: the claim allowed a shared inner, and a kid could have satisfied the words by writing the three age fields onto the tail record directly while still calling run_after_join directly — that passes a field-presence test and loses the mechanism (a second, duplicated gate). This kid did not: it reuses run_after_join_for_seat itself. The other near miss it named and avoided: passing the raw seam joined ({found: False}) would dead-skip the seat rotating itself. (4) DEVIATIONS: clause 1 said the fallback is the predecessor row at gen_before; the built fallback is _find_seat(root, seat) row pid (the seat row, which at tail time is the predecessor), not a gen_before-scoped read — acceptable at tail time but weaker for a watch pass after the successor row is seated. _force_due/_delay_override are new private kwargs on run_after_join_for_seat; they are additive and default None, so the watch path is unchanged, but they widen the function surface beyond the claim. Residual: one order-flake (test_prepare_check2_whitespace_only_delta_clean) reported by the kid did not reproduce for me in test_rotate_prepare.py alone (33 passed) or the full glob, so it is not attributable to this change.
<!-- THOUGHT:END -->
