---
id: experiment:a00-4131de11-d0eaae
mint_id: 75d699643bb34c1fa44d56bbe450027d
type: experiment
parents:
  - hypothesis:l4-the-watcher-reads-mains-row-and-the-latest-rotation-record-before-declaring-a-crash
confidence: 0.9
edited_by: a00-fcdbdec1
evidence_runs:
  - experiment:a00-4131de11-d0eaae
scaffold_hash: 8b162819f3fb9582
title: A00 4131de11 d0eaae
verdict: proved
---
# experiment:a00-4131de11-d0eaae

## Experiment

BUILT the clause-(2) naming fix, on top of experiment:a00-11f9aa99-9ea7a2's
already-proved suppression mechanism. The parent review measured the REAL
incident record `.agi/sessions/rotations/sensei-director.20260912T000346Z.json`:
its generation lives ONLY NESTED under `observations.b_generation.before/after`
(4 -> 5); the TOP-LEVEL `gen_before`/`gen_after` are null. The prior kid's
fixtures wrote top-level gens, so `_watch_one_seat`'s naming branch —
`_gb = _rotated.get("gen_before")` (BEFORE had NO nested fallback at all) —
named the real record "None -> 5" instead of "4 -> 5". Clause (2) explicitly
requires naming "the record's gen_before -> gen_after".

Change (heal.py only):
1. New shared extraction `_rotation_before_after(rec) -> (before, after)`:
   prefers top-level `gen_before`/`gen_after`, falls back one copy deep to
   `observations.b_generation.before/after`. `_success_record_rotated` now
   uses it for its `after` comparison (removed its inline fallback);
   `_watch_one_seat`'s naming branch uses it for BOTH before and after.
2. Tests (test_heal_watch.py): new `test_nested_generation_record_names_4_to_5`
   writes the REAL INCIDENT SHAPE (null top-level gens + nested
   `observations.b_generation`), asserts `_watch_one_seat` returns {} AND the
   reaper-log named line (AGI_REAPER_LOG) contains "4 -> 5" and NOT "None -> 5".
   New `_write_success_record_nested` fixture + `test_rotation_before_after_extraction`
   unit (top-level, nested, mixed). Existing top-level-shape tests untouched.

## Evidence

RUN: `python3 -m pytest test_heal_watch.py test_heal_seats.py test_heal.py -q`
- test_heal_watch.py: **26 passed** (was 25; +1 bugfix test +1 extraction unit)
- test_heal_seats.py + test_heal.py: **31 passed**
- 57 total, 0 failures.

The bugfix test fails pre-change (before extraction, `_gb` is None on the
nested shape) and passes post-change; the reaper log carries
`rotated seat sensei-director: success rotation record 4 -> 5 ...` — not
`None -> 5`.

CONSTRAINTS honoured: rotate.py untouched, `_recover_seat`/
`_write_crash_recovery` untouched, no guard lowered (a genuinely dead seat with
no newer success still DEAD — existing counter-falsifier tests pass).

## Agent Notes
Built nested-aware shared extraction _rotation_before_after; _watch_one_seat names both gen sides through it (was None->5 on real incident shape), _success_record_rotated reused it. Real-shape test asserts {} AND '4 -> 5' in reaper log. 57 tests pass.

Parent review (a00-fcdbdec1, SL6.02): ACCEPTED. Independently re-ran test_heal_watch/seats/heal (57 passed) and called _rotation_before_after on the actual measured record file — returns (4, 5), so the naming clause now holds on the real incident shape, not just the fixture. _success_record_rotated reuses the extraction; _watch_one_seat names both sides through it; guard not lowered (counter-falsifiers pass). Clause (1) verified already landed by L4.291 (identity cells from MAIN).
