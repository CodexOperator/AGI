---
id: experiment:a00-2b4d0bd6-dcf25f
mint_id: 66af8291abc2434cbf942cc1cf226b55
type: experiment
parents:
  - hypothesis:l4-rotate-self-stamps-the-card-header-itself-and-its-record-names-the-rotated-ack-one-reap-and-a-model-confirm-filled-after-the-join
next_edges: []
confidence: 0.82
edited_by: a00-28a09183
evidence_runs:
  - experiment:a00-2b4d0bd6-dcf25f
loop: hypothesis:l4-rotate-self-stamps-the-card-header-itself-and-its-record-names-the-rotated-ack-one-reap-and-a-model-confirm-filled-after-the-join@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 49674bac68a9f1dd
season: 2
title: A00 2b4d0bd6 dcf25f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2b4d0bd6-dcf25f

## Experiment

Built claims (a) and (b) of hypothesis:l4-rotate-self-stamps-the-card-header-
itself-and-its-record-names-the-rotated-ack-one-reap-and-a-model-confirm-
filled-after-the-join — a g15 build order, not a measurement (base `5515d77f`,
re-measured on this tree). (c) reap_own_pid and (d) model_confirm left to the
second writer and never touched.

**(a) ONE card write on the way out — the header stamp rides
`_write_stops_section`.**
- New `_stamp_rotating_header(full, frac, hmz)`: the FIRST line matching
  `^# SESSION HANDOFF` gains exactly ONE trailing parenthetical
  ` (rotating at <frac> of the line, <HH:MMZ>)`; an already-present
  ` (rotating at …)` parenthetical is REPLACED (never a second one); a card
  with NO such header is returned byte-identical (never invents a header).
- `_write_stops_section` took a `frac: float | None = None` param; when set it
  stamps `full` in BOTH write branches (slot-created and slot-replaced,
  before `write_text`), so the stamp lands in the SAME write/commit as the
  stops slot. `<HH:MMZ>` = `datetime.utcnow().strftime("%H:%MZ")` of this write.
- The rotate-self `--stops` call site measures the meter fraction ONCE via
  `_seat_fraction(root, row)` (the same value rotate-self reads — never
  re-derived a second time) and passes it down.

**(b) The record names the ack file as it exists at record time.**
- After `_rotate_ack_file` returns `ack rotated:` (success), the SAME record's
  `ack_written` is rewritten to the `.ack.gen<N>.json` path (constructed the
  same way the rotate did it) and the spawn-time value is preserved under
  `ack_written_at_spawn`. The record file is rewritten in place via the same
  `_write_rotation_record(root, rec, path=record_path)`. Naming only — the ack
  SHAPE is untouched. Guarded against a `FAILED:` `ack_written` and a
  missing/str record_path.

## Evidence

New tests in `extensions/agi/tests/test_rotate.py`:
- `test_write_stops_section_stamps_rotating_header` — unit: stamp on
  created + replaced, second run replaces (one `rotating at`), no-header card
  stays stamp-free.
- `test_rotate_self_stops_stamps_header_once_in_commit` — one live
  `rotate-self --stops` with a pinned transcript (frac 0.0100): git log -1
  names the card ONCE, the committed `# SESSION HANDOFF` line carries
  `rotating at 0.0100 of the line, `, and the stops text rides the SAME
  write/commit.
- `test_rotate_self_record_names_rotated_ack_after_rotation` — live rotate
  with a `session_ref` seam (so the s6.x ack write really runs): the record
  names `adv-alive.ack.gen1.json`, keeps `adv-alive.ack.json` under
  `ack_written_at_spawn`, and the on-disk `.ack.gen1.json` exists while the
  live ack is gone.

Suite: `test_rotate.py test_heal_ack_rotation.py test_after_join_service.py
  test_bin_help_smoke.py test_rotate_selfreap.py test_rotate_handover.py
  test_rotate_prepare.py test_session_start_*.py` — 371 passed, 3 skipped, 0
  failed.

## Agent Notes
## Caveats
- `<frac>` in the installed header is the meter fraction measured at the
  moment of the stops write (`_seat_fraction`); a run with no meter pin
  writes NO stamp (the header is then left untouched).
## Struggles
- The fixture stops-flow skips the whole s6.x handover block (no @id /
  session_ref -> no ack written), so the record test needed a `session_ref`
  seam to prove (b) — a second run without it is a silent no-op.

## Agent Notes
(a) header stamp rides _write_stops_section (one write/commit, replace not append); (b) record names .ack.genN after rotation, spawn name kept under ack_written_at_spawn. 371 passed 3 skipped.

PARENT REVIEW (a00-28a09183, SL7.24): artifact read, not the report. (a) `_stamp_rotating_header` (rotate.py 10449) is applied in BOTH `_write_stops_section` branches before `write_text` (10503, 10562), frac measured ONCE at the call site (10822 `_seat_fraction`), so one card write + one `_commit_stops_row` carry both the stops slot and the header stamp — verified in the committed blob by `test_rotate_self_stops_stamps_header_once_in_commit`. (b) the rewrite runs only on `_rot.startswith("ack rotated:")` (11756), names `.ack.gen<N>.json` via the same `_ack_path(root, seat).with_name(...)` construction `_rotate_ack_file` uses, keeps the spawn name under `ack_written_at_spawn`, and guards a FAILED/absent ack_written (11757-11772) — real, not cosmetic. Verdict proved upheld; evidence_runs names the run itself (it IS the run). WEAK POINT, not a re-cut: `_stamp_rotating_header` returns `"\n".join(lines) + "\n"`, so a headerless card can gain a trailing newline beyond the stops slot — the claim says byte-identical; the unit test asserts content, not byte-equality. Second weak point: (a) is only measurable when the seat has a meter pin (kid caveat) — correct as designed.
