---
id: experiment:a00-1548d6af-ab97d1
mint_id: 4c09fb1494c14d759156e73a77e149e8
type: experiment
parents:
  - hypothesis:l4-rotation-record-survives-interruption
next_edges: []
confidence: 0.85
edited_by: a00-1e3af37b
evidence_runs:
  - experiment:a00-1548d6af-ab97d1
loop: hypothesis:l4-rotation-record-survives-interruption@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9f66904dd8d8c5f8
season: 2
title: A00 1548d6af ab97d1
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1548d6af-ab97d1

## Experiment

Tested hypothesis:l4-rotation-record-survives-interruption — that a rotation
record written only on the LAST step (step 6 of `cmd_rotate_self`) is absent
exactly when the sequence is interrupted, and that the fix is to open ONE
`started` record up front and update it in place through every step.

**Diagnosis confirmed (claim 1, mechanism).** Read `cmd_rotate_self`
(`extensions/agi/bin/rotate.py`). Records are written ONLY at: step 4 refuse
(successor window absent), step 5 refuse (predecessor gone), step 6 success.
The one real mid-sequence stop that the reaper leaves behind — the successor
spawns and lives, then the read-back at step 5 never settles into `continue`
— returns `1` having written NO record at all. And an interruption at steps
1-3 writes nothing either, because the record file is minted only at the
first refuse/success. Pure read of the code confirmed the hypothesis's
summary: the record is created at the wrong end of the sequence.

**Fix (rotate.py only — no write.py, verification.py, conftest, or engine
touched).**
- `_write_rotation_record(root, record, path=None)` gained an optional
  `path`; when given, the outcome is written to that file (in place) instead
  of a fresh `<seat>.<stamp>.json`.
- `_rotate_self_started_path(root, seat)` captures the timestamp ONCE so the
  whole rotation writes to one stable filename — a `started` file and a
  `success` file can never split into two records.
- `_write_rotate_self_started(path, ...)` writes/refreshes the in-progress
  record: `result: "started"`, `steps_reached: [...]`, `gen_before`/`gen_after`.
- `cmd_rotate_self` now opens the `started` record BEFORE step (1), appends
  to `steps_reached` after steps 1, 2, 3 and at the read-back boundary (step
  4), and rewrites the SAME path at each refuse and at success. So an
  interruption at any point leaves a durable record whose `steps_reached`
  says how far it got; a completed rotation still leaves exactly ONE record
  in today's shape.
- Non-`continue` read-back still returns `1` (leaves the renamed window for
  inspection) but now the started record already exists on disk.

**Red-first test.** Added to `extensions/agi/tests/test_rotate.py`:
`test_rotate_self_interrupted_after_spawn_leaves_started_record` drives a
throwaway fixture where the successor spawns under the plain name then the
read-back returns `still loading` (the surrogate for the harness reaper
killing the wrapper mid-read-back). Against the pre-fix code this wrote NO
file → the `assert records` failed; after the fix it leaves one file with
`result: "started"`, `steps_reached[-1] >= 3`, `gen_before`/`gen_after`.
Second test `test_rotate_self_success_leaves_exactly_one_record` pins the
invariant that a completed rotation still leaves exactly ONE file, in the
`success` state (criterion b).

**Claim 2 (one writer per fact).** The record is still written exclusively
by `_write_rotation_record` / `_rotate_self_record`; the generation is read
by `_read_generation` and carried into the record as `gen_before`/`gen_after`,
not written twice. No fact is written by two writers. Verified by reading the
changed paths; no new writer added.

**Claim 3 (.gitignore handoff-sections).** `.gitignore` lines ~104-109 already
carry `!.agi/sessions/handoff-sections/` and `!.agi/sessions/handoff-sections/*`
beside `rotations/` and `quorum/`. It is ALREADY correct. **No edit made.**
Reported only, per the hypothesis.

**Claim 4 (L4.13 dependency).** `doc:l4-plan` row L4.16 lists `depends: L4.13`
but the owner-go column reads `no — already banked (A:55)`. `.agi/nodes/seat/`
does not exist (L4.13 has not run). The dependency is SPURIOUS for this work:
a rotation record and a generation stamp are files under `.agi/sessions/` and
logic in `rotate.py`, not seat nodes. L4.14-L4.18 may genuinely need L4.13;
L4.16 does not. Did NOT stop; proceeded with claim 1.

## Evidence

- `extensions/agi/tests/test_rotate.py` → **83 passed** (incl. 2 new)
- `extensions/agi/tests/test_rotate_complete.py` + `test_season.py` → **45 passed**
- `test_brief.py` + `test_claude_code_adapter.py` + `test_grid_coverage_check.py`
  (the only other files importing `rotate`) → **139 passed**
- `test_send.py` NOT run (real-window nudge risk with live seats; standing rule)
- Red-first confirmed: pre-fix non-`continue` read-back path wrote no record;
  the new interrupted test fails on `assert records` there and passes after.
- `.gitignore` handoff-sections lines present and unchanged; `node/seat/` absent.

Changed files (all in this worktree): `extensions/agi/bin/rotate.py`,
`extensions/agi/tests/test_rotate.py`.

## Agent Notes
Implemented claim 1 (started record per step, updated in place) in rotate.py; red-first test + single-record regression test; verified gitignore handoff-sections already present (unchanged) and L4.13 dep spurious; 128+139 pytest green (incl 2 new); test_send skipped per standing rule

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-1e3af37b): artifact verified directly — read cmd_rotate_self diff, confirmed started-record opened before step 1 and updated per step with stable single filename; red-first test test_rotate_self_interrupted_after_spawn_leaves_started_record and single-record regression test both present in test_rotate.py; reran 83+45 tests green in this worktree. Claim 3 (.gitignore already correct, no edit) and claim 4 (L4.13 dep spurious for L4.16, files under .agi/sessions/) both verified by reading. verdict proved ACCEPTED — experiment names itself as evidence run, which is permitted.
<!-- THOUGHT:END -->

## Agent Notes
Rotation record opened as 'started' before step 1, updated in place per step; interrupted rotations now leave steps_reached evidence; .gitignore already correct; L4.13 dep spurious; tests green
