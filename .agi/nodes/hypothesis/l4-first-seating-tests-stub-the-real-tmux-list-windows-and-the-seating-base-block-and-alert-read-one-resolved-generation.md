---
id: hypothesis:l4-first-seating-tests-stub-the-real-tmux-list-windows-and-the-seating-base-block-and-alert-read-one-resolved-generation
mint_id: a8a0a0d42fcd402ebcf1a2485bba4c56
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 8606646040df5297
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (Prime XVI dm 17:07Z (mur-SL2.23 digest), line numbers measured by the Prime on main tip 36fa24d1d — `git show 36fa24d1d:<file> | sed -n` before trusting one; cite at seat tip d51c9a917, re-measure on your base; line (b), SL7.58 residue). MEASURED: two SL7.58 tests call `rotate._first_seating_announce(` (test_rotate_startup.py:1868 and its sibling) with `_successor_window_id` UNSTUBBED, so the fixture-only suite runs a REAL `tmux list-windows` (a box without tmux, or with a foreign session, changes the result); the `[seating]` base block at rotate.py:4369 (`if root is not None and _seating_record_exists(root, seat):`) checks the record at gen 1 only, so a re-seated seat at gen N reads as never seated; `_first_seating_announce` (:4050 `if generation is None:`) performs a SECOND `_seat_row_generation` read for the record/alert instead of taking the one value its caller already resolved (SL7.58 made record/alert/bootstrap share ONE resolved generation — this read is the leak). CLAIM: (a) both tests stub `_successor_window_id` (monkeypatch, returning a fixed @id) — no tmux subprocess in the suite; a grep of test_rotate_startup.py for an unstubbed call is empty; (b) the base block resolves the generation first and checks `_seating_record_exists(root, seat, generation)` at THAT generation (gen 1 stays the first-seating default); (c) `_first_seating_announce` takes `generation` from its caller and never re-reads the row when a value was passed — the second read stays only as the fallback for a caller that passes None, and the production caller passes the value. FALSIFIERS: `tmux` appears in the suite's process table during test_rotate_startup.py; a gen-3 re-seating reads 'never seated'; the alert prints a generation different from the record's. TESTS: test_rotate_startup.py — stubbed seam (assert the stub was called, no subprocess), base block at gen N, one-read (a counting fake `_seat_row_generation` asserts 1 call per announce). FILE SCOPE: extensions/agi/bin/rotate.py — `_first_seating_announce` (:4050 region), the base block (:4369 region), `_seating_record_exists`'s signature; extensions/agi/tests/test_rotate_startup.py. EXCLUDED: rotate-self's spawn path, the alert dm body, the bootstrap record writer, `_successor_window_id` itself. CEILING: two stubs, one signature, one read removed, four tests."
thought_session: sensei-director-genXIV-L14
title: the first-seating tests never run a real tmux list-windows (the successor-window seam is stubbed), the [seating] base block checks the record at the resolved generation not only gen 1, and the record/alert generation is the ONE value already resolved — no second _seat_row_generation read
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-first-seating-tests-stub-the-real-tmux-list-windows-and-the-seating-base-block-and-alert-read-one-resolved-generation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
