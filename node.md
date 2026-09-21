---
id: experiment:a00-b64b2c2d-6398b9
mint_id: 9b43202d57f94b2899304326c60c2c71
type: experiment
parents:
  - hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human
next_edges: []
confidence: 0.6
edited_by: a00-a4f9327b
evidence_runs:
  - experiment:a00-b64b2c2d-6398b9
loop: hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 22cd85a7d73ea90a
season: 2
title: A00 b64b2c2d 6398b9
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-b64b2c2d-6398b9

## Experiment

KID 1 of the L4.292 fix-only build order (FIX-ONLY L4.292 block in
`hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human`, after the
L4.283/L4.288 merged bytes — prime XI mur-40: DETECT sound, RECOVER not).
Built and tested on the checked-out tree (fixture roots + fake pid table +
`AGI_WINDOW_PATH` seam + fake launcher + fixture registry dir; NEVER the live
seats row, NEVER the live tmux server, NEVER `~/.claude/sessions`).

**(1) The crash-recovery record drives the service's after_join.**
- `_write_crash_recovery` (heal.py) now writes `gen_after` (= the successor
  generation, the key `rotate._latest_rotate_record`/`run_after_join_for_seat`
  read) plus the rotate-self profile placeholders the claim names: `succ_name`,
  `gen`, `pin_ref` (empty — the recovery pins nothing, the service pins after
  `after_join_delay_s`), `tmux_session`, `window_id`, `pred_pids` = the dead
  pid, `recorded_at`.
- `_latest_rotate_record` (rotate.py) widened one line: `result: respawned`
  when `rotation == crash-recovery` is now discoverable, so the service's next
  pass performs join -> pin -> pending ack for the recovered seat exactly as
  for a rotated one. A `result: detected` record binds nothing.
- `_dm_crash_recovery` (heal.py) appends `; after_join: service-owed` so the
  holder/Sensei know the meter pin arrives from the service.

**(5) LIVENESS BEFORE DEATH, keyed on @id + pid + PIN (never a name).**
- New `_alive_via_pin(pins, sessions, seat, pid_alive)` reuses the L4.289
  tables (`_pin_table` + `_seat_sessions`, imported) — a seat whose meter pin
  leases a registry session whose pid is ALIVE is ALIVE regardless of its stale
  row. `_watch_one_seat` checks it after (1a)/(1b) pass and before DEAD; a live
  pinned seat is NAMED once per pass as `stale-row` (row pid/@id vs the pinned
  session) and never respawned, never recorded. `_watch_seats` builds the
  tables once and passes them in; the registry is read ONLY when a pin exists
  to cross-check (a pin-less scan never touches the live registry).

Commands run (files modified): `extensions/agi/bin/heal.py`,
`extensions/agi/bin/rotate.py`; tests added to `test_heal_seats.py`,
`test_rotate_recover.py`. Suite: 352 passed across the heal/rotate/after-join
files covering the change.

## Evidence

New tests (each green):
- `test_crash_recovery_record_carries_after_join_profile` — respawned record
  carries `gen_after`/`succ_name`/`pred_pids`=[dead pid]/`pin_ref`=""/`tmux_session`/`window_id`.
- `test_latest_rotate_record_picks_up_crash_recovery_respawned` — widening
  finds `respawned` crash-recovery; `detected` binds nothing.
- `test_after_join_service_performs_recovered_seats_join_pin_ack` — a
  respawned crash-recovery record drives `run_after_join_for_seat` to run the
  seat's `after_join` list at gen=gen_after with the record as `record_path`.
- `test_pinned_live_session_makes_stale_row_alive_not_dead` — row pid+@id gone
  but pin leases a live registry pid -> `stale-row` named, no spawn, no record.
- `test_pinned_session_pid_gone_still_dead_respawns` — pinned session's pid
  gone -> genuinely dead, still respawned.

Pass output (fixture root, scrutinised): `pytest test_heal_seats test_rotate_recover`
31 passed; expanded heal/rotate/after-join set 352 passed, 0 failures.

## Agent Notes (authored)
KID 1 (1)+(5) built + proved on fixture roots. KID 2 of the L4.292 block —
(2) chain successor numeral from the record's `gen_after`, (3) `_launch_recovered`
cwd = the seat tree, (4) row write through L4.291's ONE writer — is NOT done
here; it depends on L4.291 landing and is the remaining half of the assignment.
Deliberately matched the claim's "copy the exact keys, measure don't guess":
measured rotate-self's record carries `gen_after` (the only key the service
binds), so the recovery record mirrors it rather than inventing a parallel shape.
`_latest_rotate_record`'s old `rotation in ("rotate-self",)` clause was
redundant (a started/success rotate-self record already matched by result) and
collapses cleanly.

## Agent Notes
KID1 of L4.292: recovery record carries gen_after+profile keys and _latest_rotate_record widened to crash-recovery respawned (service performs join/pin/ack); liveness-before-death via _alive_via_pin on pin tables, stale-row never respawned. 352 tests green. KID2 (numeral/launch-cwd/ONE-writer) not done.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.292 by a00-a4f9327b: ACCEPTED as inconclusive_lean_proved:60. The node claims only the KID 1 half of the L4.292 build order — (1) the crash-recovery record carries gen_after + the rotate-self after_join profile keys and _latest_rotate_record accepts rotation==crash-recovery with result==respawned, and (5) liveness-before-death via _alive_via_pin over the imported L4.289 pin tables — and says plainly that KID 2 is not done, so the whole hypothesis is not proved. Read the artifact, not the report: diff HEAD shows the two heal.py hunks and the one-line rotate.py widening exactly as described, and the new tests pin both directions (a pinned-live stale row is named, never respawned; a pinned session whose pid is gone still respawns). Verdict left at the honest lean; not demoted, not promoted.
<!-- THOUGHT:END -->
