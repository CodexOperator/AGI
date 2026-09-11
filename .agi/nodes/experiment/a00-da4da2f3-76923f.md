---
id: experiment:a00-da4da2f3-76923f
mint_id: 1fe429d55ed24b66a77eb7be0f4e4b7a
type: experiment
parents:
  - hypothesis:l4-spawn-seats-without-a-root-with-the-rows-role-and-pins-at-the-rows-generation-and-a-first-rotation-is-not-a-first-seating
next_edges: []
confidence: 0.8
edited_by: a00-caef8be5
evidence_runs:
  - experiment:a00-da4da2f3-76923f
loop: hypothesis:l4-spawn-seats-without-a-root-with-the-rows-role-and-pins-at-the-rows-generation-and-a-first-rotation-is-not-a-first-seating@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b3dbfc004a9d2a35
season: 2
title: A00 da4da2f3 76923f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-da4da2f3-76923f

## Experiment

Built the goal:g15.17 residue claim in `extensions/agi/bin/rotate.py` and proved it on the built bytes. Parts a/b/e are in `cmd_spawn`, c in `cmd_ack`, d(ii) in `cmd_rotate_self`; all five falsifiers are now tests.

(a) **`spawn --seat S` with root None.** Before: the seat tail called `_first_seating_run(root, …)` whose `_resolve_template` reached `_rotations_node_path(Path(None))` -> `TypeError` (the SL2.02 refuter's crash). Now: `cmd_spawn` short-circuits when `seat is not None and root is None`, prints `[seating] no project root: template + bootstrap skipped`, and still seats the window (empty `extra`, no template/record/pin).

(b) **role from the seat row, `--tier` only as fallback.** `cmd_spawn` resolves `_fs_role = row.role` when the row exists (else `--tier`) and threads it into `_first_seating_run` and `_first_seating_announce`; the seating record now carries the row role, never a defaulted `prime_director`.

(e) **re-spawn pins at the row's generation.** `_first_seating_spawn_writes` now receives `_spawn_gen` = `_seat_row_generation(root, seat)` when the row carries a generation (row gen 11 -> pin `11	`, ack `gen_after 11`), instead of the hardcoded `FIRST_SEATING_GEN` that re-pinned the prime's gen-11 row back to 1 (SL3.01 residue).

(c) **a first rotation acked at gen 1 is not a first seating.** `cmd_ack`'s hand-launch announce gate now requires BOTH `not _rotation_record_exists(root, seat)` (a new `<seat>.*.json` scan that excludes `.seating.json`) AND no pending ack (`_pending_ack_exists`, a new `<seat>.ack.json` reading `answer: pending`), alongside the existing no-seating-record test. The pending-ack flag is snapshotted BEFORE `cmd_ack`'s own write overwrites it. A rotate-self writes both a rotation record and a pending ack before the successor joins, so its successor acking at gen 1 emits nothing and writes no seating record.

(d)(ii) **join-only rotate-self refused by name.** `cmd_rotate_self` refuses a role template that DECLARES `startup` but strips `first_turn` (join-only — nothing to hand off) with `ERR: … is join-only (startup declared with no first_turn) — rotate-self refused`. Scoped to a declared-but-emptied startup so the legacy plain template (no `startup` key at all — the shape historical rotations and many tests use) is untouched.

## Evidence

- New `extensions/agi/tests/test_rotate_g1517.py` (5 tests): root-less `spawn --seat` seats the window + prints the named skip + exit 0; record role == `director` from the row (row gen 11) while `--tier prime_director` is passed; pin reads `11\t` and ack `gen_after 11`; `ack --gen 1` after a rotate-self rotation-record+pending-ack emits no dm and writes no seating record; join-only rotate-self refused `rc 1` with the reason named; plus a regression that a plain no-startup template still rotates `rc 0`.
- Updated `test_rotate_autopsy.py::test_spawn_pins_meter_gen1_ack_pending_and_three_worktree_facts`: it asserted the FIXED bug (pin `1\t` on a row at gen 11); now asserts `11\t` and `gen_after 11` per claim (e)'s falsifier `row gen 11 -> pin says 11`.
- `python3 -m pytest` on test_rotate*.py + test_session_start*.py + test_after_join_service.py + test_bin_help_smoke.py + test_rotate_g1517.py + test_heal_seats.py + test_sensei_*.py: **552 passed, 1 skipped, 0 failed** across the runs. No falsifier reproduced.

5/5 sub-claims built and green. Caveat: (d)(ii)'s "no bootstrap" half is read as the bootstrapping a declared startup pipeline would otherwise produce, and the refusal is scoped to a startup-bearing template with first_turn stripped — the legacy no-startup template keeps rotating (regression-tested); if the owner intended the refusal to also cover the bare no-startup template, that is one line to loosen.

## Agent Notes
Built all 5 residue sub-claims in rotate.py (spawn role-from-row+pins-at-row-gen, root-less spawn --seat no longer TypeErrors, ack --gen 1 after rotate-self is not a first seating, join-only rotate-self refused); 5 new tests + 1 buggy-pin regression falls under the claim; 552 pass, 0 fail.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-caef8be5 review (SL4.04), reading the ARTIFACT not the report: staged diff of rotate.py + new test_rotate_g1517.py, and `python3 -m pytest test_rotate_g1517.py test_rotate_autopsy.py -q` -> 14 passed, 0 failed. (a) cmd_spawn now short-circuits when seat is not None and root is None, prints the named skip, leaves rc 0; announce/spawn-writes/record-removal are root-guarded. (b) _fs_role = row.role with --tier only as fallback, threaded into _first_seating_run AND _first_seating_announce. (e) _spawn_gen = _seat_row_generation(root, seat), the hardcoded FIRST_SEATING_GEN at the call site replaced. (c) cmd_ack hand-launch gate adds `not _rotation_record_exists` and `not _pending_ack_present`, the pending flag SNAPSHOTTED before cmd_ack overwrites the ack. (d)(ii) cmd_rotate_self refuses a template that DECLARES startup but strips first_turn, naming the reason. NEAR MISS: the tests could have called the new helpers (_rotation_record_exists / _pending_ack_exists) in isolation and certified a bool without driving cmd_ack at all; these drive the real verbs with spawn_window/send_dm monkeypatched end to end, so the gate is exercised. DEVIATION, recorded not rejected: addendum (ii) names a template with no first_turn AND no bootstrap; the kid refuses only a startup-declaring template with first_turn stripped, leaving the legacy no-startup template rotating (regression-tested). A literal reading refuses every pre-startup template and breaks their suites; the narrowing is defensible but is a narrowing. Open residue for a follow-up: _first_seating_run still writes its bootstrap record at generation=1 on a RE-spawn of a gen-11 row even though the pin/ack now follow the row generation -- the bump did not touch _write_bootstrap.
<!-- THOUGHT:END -->

Reviewed by parent a00-caef8be5: all five g15.17 sub-claims (a,b,c,d-ii,e) built in rotate.py and proved on the built bytes; 5 new tests + 1 corrected pin regression; 14 passed locally (552 in the kid full run). Accepted. Two flags for the verdict writer: d-ii is narrowed to startup-declaring templates (legacy no-startup untouched), and _write_bootstrap still stamps generation=1 on a re-spawn even after the pin/ack were moved to the row generation.
