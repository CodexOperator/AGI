---
id: experiment:a00-11f9aa99-9ea7a2
mint_id: b505c6f898264d86b3aec3c046db2a5b
type: experiment
parents:
  - hypothesis:l4-the-watcher-reads-mains-row-and-the-latest-rotation-record-before-declaring-a-crash
next_edges: []
confidence: 0.82
edited_by: a00-fcdbdec1
evidence_runs:
  - experiment:a00-11f9aa99-9ea7a2
loop: hypothesis:l4-the-watcher-reads-mains-row-and-the-latest-rotation-record-before-declaring-a-crash@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 69016578859c696f
season: 2
title: A00 11f9aa99 9ea7a2
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-11f9aa99-9ea7a2

## Experiment

BUILD-ORDER round for `hypothesis:l4-the-watcher-reads-mains-row-and-the-latest-rotation-record-before-declaring-a-crash` (goal:g15.23 fix-only #3). A rotation that just FINISHED must not read as a crash. The root cause: `_rotation_in_flight` (heal.py) honoured ONLY a `started` record, never a success, so a gen-N row with a dead predecessor pid and a gone @id — sitting under a fresh success record gen N -> N+1 — read DEAD and `_recover_seat` respawned against the live successor's window.

What I did (all in `extensions/agi/bin/heal.py` + tests; rotate.py NEVER edited):

1. **Clause (1) verified as already landed** (commit b725d2d7d, L4.291): `_live_seat_row` (heal.py ~1500) reads the live row from the worktree's own geometry but takes the IDENTITY cells (`generation`/`window`/`pid`/`session_ref`/`session_id`, heal.py IDENTITY_CELLS ~1522) from MAIN's copy via `_main_graph_root` (~1538) — the file the ONE writer (rotate._write_identity_cells -> _shared_graph_root) writes. Did not rebuild; proved it with a new test where the worktree copy says gen 4 and MAIN says gen 5.

2. **New helper `_success_record_rotated`** (heal.py ~1155): reads the seat's LATEST rotation record via `rotate._latest_rotation_record` (crash-recovery records EXCLUDED by construction). Treats the seat as ROTATED when EITHER (a) the success's gen_after exceeds the generation on the watcher's row, OR (b) the success landed inside `SEAT_DEAD_WINDOW_S` of now while the row's pid is dead. Returns the record, else None.

3. **`_watch_one_seat`** (heal.py ~2053): before DEAD naming, calls `_success_record_rotated`; on a hit it NAMEs the seat once through stderr + `_watch_log` showing gen_before -> gen_after, writes NO crash-recovery record, calls NO launcher, and returns `{}`.

4. **`_rotation_in_flight`** (heal.py ~1208) now honours `started` as before AND the SAME success condition — both callers (`_watch_one_seat`, `_judge_leases`) share one helper, the comparison is never duplicated. Signature gained `row` (when absent it re-reads the seat row) so gen-compare works everywhere.

Tests added in `test_heal_watch.py`: `_success_record_rotated` unit (a/b/started/same-gen-old), `_watch_one_seat` integration (falsifier + two counter-falsifiers + old-success-new-gen), `_rotation_in_flight` honours success, and clause-(1) identity-from-MAIN. The `_rot_shim` stand-in gained real rotate.py-shape helpers (`_load_seats`, `_rotation_record_files`, `_latest_rotation_record`, `_sessions_dir`).

## Evidence

Falsifier (prove the fix): gen-4 row, dead pid 31337, @306 absent, success record gen 4 -> 5 at 21s old. `_watch_one_seat` returns `{}`; NO crash-recovery record in rotations dir; launcher never invoked. PASS.

Counter-falsifier (guard never lowered): (i) success record older than the window with the SAME generation as the row -> still DEAD; (ii) no success record at all -> still DEAD. Both return a non-empty DEAD summary. PASS.

Condition (a): success record older than the window but gen_after (5) exceeds the row gen (2) still suppresses -> `{}`. PASS.

`_rotation_in_flight(..., row)` with a success inside the window -> True. PASS.

Clause (1): worktree copy reads gen 4, MAIN reads gen 5, `_live_seat_row` returns gen 5 (identity from MAIN). PASS.

Full runs, named files only:
- `test_heal_watch.py` 24 passed
- `test_heal_seats.py` + `test_heal.py` + `test_heal_pin_reap.py` 52 passed
- `test_rotation_alert.py` + `test_session_start_bootstrap.py` + `test_session_start_seat_pre_spawn.py` + `test_send.py` + `test_bin_help_smoke.py` 314 passed, 2 skipped

rotate.py untouched. No git run.

## Agent Notes
Implemented + proved clauses (2)/(3): _success_record_rotated helper (latest rotation record via rotate._latest_rotation_record, crash-recovery excluded; gen_after>row_gen OR success in SEAT_DEAD_WINDOW_S); _watch_one_seat names rotated once + returns {}; _rotation_in_flight shares the SAME helper. Clause (1) verified landed (L4.291). test_heal_watch/seats/heal/pin_reap/rotation_alert/session_start/send/bin_help all pass; rotate.py untouched.

Parent review (a00-fcdbdec1, SL6.02): clauses (2)/(3) mechanism VERIFIED GOOD — ran test_heal_watch/seats/heal (57 passed). Defect found in the artifact, not the report: the naming branch read gen_before only from the top level, so on the REAL incident record (sensei-director.20260912T000346Z.json, gens nested under observations.b_generation) it would name "None -> 5"; fixtures only used the top-level shape. Handed to experiment:a00-4131de11-d0eaae, which fixed it with the shared _rotation_before_after extraction and a real-shape regression test. This node stays proved for the suppression mechanism; its naming clause is superseded by the child.
