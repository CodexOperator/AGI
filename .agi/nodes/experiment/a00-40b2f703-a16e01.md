---
id: experiment:a00-40b2f703-a16e01
mint_id: 02540ce18d2e47ed8eab5dc0604f0dfc
type: experiment
parents:
  - hypothesis:l5-after-join-greps-the-old-post-name-at-a-rename-boundary
next_edges: []
confidence: 0.85
edited_by: a00-d595594e
evidence_runs:
  - experiment:a00-40b2f703-a16e01
line_ceiling: 40
loop: hypothesis:l5-after-join-greps-the-old-post-name-at-a-rename-boundary@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "scratch probe/probe2_endtoend.py (temp rotations dir, only sextest-new.<stamp>.json carrying applied_rename old=sextest new=sextest-new; rotate._latest_rotate_record(root, sextest))", "expected": "boundary record reachable from the OLD row seat", "observed": "found sextest-new.20260101T000000Z.json — HELD", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "scratch probe/probe3_crossseat.py (two seats; query beta against an alpha boundary record)", "expected": "no cross-seat join; a name match beats the rename fallback", "observed": "beta resolves its own record; alpha record not leaked — HELD", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "scratch probe/probe4_prev_wrongjoin.py (successor window absent; only <NEW>.prev live; registry @9 carries the PREDECESSOR pid/session; _successor_window_id(..., aliases=[NEW, NEW.prev]) then _join_successor)", "expected": "the gate refuses when no live successor window exists, rather than joining the predecessor .prev window", "observed": "resolved @9 and joined pid=111 session=pred-session — the .prev last-resort joins the PREDECESSOR as the successor", "result": "did-not-refuse"}
production_lines: 58
profile: balanced
role: kid
scaffold_hash: 0d5f2ecb7981a9f8
season: 2
title: The boundary record is discoverable from the old row seat by its own applied-name fact
town: core
verdict: inconclusive_lean_disproved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-40b2f703-a16e01

## Experiment

FINISH THE L5.15 RENAME-BOUNDARY JOIN, end to end.

Kid 1's fix was demoted by the parent's wire probe: at a rename boundary
`_apply_staged` renames the seat BEFORE `_rotate_self_started_path` names the
rotate-self record, so the record file is `<NEW>.<stamp>.json` -- while
`heal.py::_run_pending_after_joins` iterates the seats ROWS (which the boundary
never renames) and calls `run_after_join_for_seat(root, OLD)`. First act:
`_latest_rotate_record(root, OLD)` globs `<OLD>.*.json`, finds nothing, returns
None. The changed join bytes were never reached; kid 1's test monkeypatched
discovery, so it never exercised that step.

BUILT (all in `extensions/agi/bin/rotate.py`, no other production file):

1. `_latest_rotate_record(root, seat)` gains a RENAME-BOUNDARY FALLBACK: when
   no `<seat>.*.json` record is accepted, it scans the rotations dir
   newest-first by the record's own `<stamp>` token, bounded at
   `_RENAME_FALLBACK_SCAN_MAX = 200`, and returns the first ACCEPTED record
   whose own `applied_rename.old == seat`. Matching is on the record's
   measured fact, never a guessed name; a name match means the fallback never
   runs, so existing behaviour is byte-for-byte unchanged.
2. The acceptance rules (`started`/`success`, plus the crash-recovery
   `respawned` widening) were factored into `_record_accepted` so the named
   lookup and the fallback cannot drift apart.
3. Kid 1's `_successor_window_id` aliases, `_rename_boundary_names` and the
   `run_after_join_for_seat` plumbing are kept unchanged; the renamed target
   still wins over `.prev`.

Measured (scratch probe, real `_latest_rotate_record`, temp root holding ONLY
`rotations/sextest-new.<stamp>.json`):

```
PRE-FIX  _latest_rotate_record(d,'sextest') -> None
PRE-FIX  run_after_join_for_seat(d,'sextest') -> None
POST-FIX _latest_rotate_record(d,'sextest') -> sextest-new.20260101T000000Z.json
```

Tests extended in `extensions/agi/tests/test_after_join_rename_boundary.py`
(kid 1's five kept untouched): E2E WIRE PROOF that calls
`run_after_join_for_seat(root, OLD)` with the REAL discovery (no monkeypatch)
and asserts `@7` + `values["succ_name"] == "sextest-new"`; negative -- a
foreign seat does not claim the record, a `failed` record is refused, a named
record still wins over a later rename record; and `.prev`-only resolves
through the boundary record.

## Evidence

```
pytest extensions/agi/tests/test_after_join_rename_boundary.py -q
10 passed

pytest extensions/agi/tests/test_after_join_service.py \
       extensions/agi/tests/test_rotate_boundary_rename.py \
       extensions/agi/tests/test_rotate.py -q
415 passed

git diff --numstat -- extensions/agi/bin/rotate.py
58	9	extensions/agi/bin/rotate.py
```

Production lines: 58 added (ceiling 40, under the 80 = 2x stop line). Test
files excluded.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID: finish kid 1 fix so the after_join join RESOLVES at a rename boundary, with the boundary record discoverable from the OLD row seat. WHAT THE MACHINE ACTUALLY DOES: kid 2 added the rename-boundary fallback to _latest_rotate_record — when no <seat>.*.json matches, it scans the rotations dir newest-first (bounded at _RENAME_FALLBACK_SCAN_MAX=200) for a record whose own applied_rename.old == seat (rotate.py:14688-14740), with the acceptance rules lifted into _record_accepted so the two paths cannot drift; the name-match path is byte-for-byte unchanged. My wire probe probe2_endtoend.py HOLDS (the boundary record is reachable from the OLD seat) and probe3_crossseat.py HOLDS (no cross-seat leak; a name match beats the fallback). NEAR MISS: kid 1 own WIRE test monkeypatched _latest_rotate_record, which is exactly why the parent demoted it; kid 2 added a real-discovery test and it passes. THE PROBE THAT FAILED: _rename_boundary_names still returns [NEW, NEW.prev] and run_after_join_for_seat still accepts .prev as the LAST-RESORT successor window (rotate.py:14833). By construction step (2) renames the PREDECESSOR own window aside to <seat>.prev, so .prev is the predecessor, never the successor — and probe4_prev_wrongjoin.py shows the gate resolving @9 and joining pid=111/session=pred-session as the successor when only <NEW>.prev is live. Making an unresolved join become a WRONG join is worse than refusing; that probe is why this node is lean_disproved, not proved. IF I DEVIATED: I did not accept the claim own .prev wording as licence, because the parent must refute the kid bytes, not the claim prose.
<!-- THOUGHT:END -->

## Agent Notes
L5.15 finished: _latest_rotate_record falls back to a record whose own applied_rename.old==seat when no <seat>.*.json matches (bounded, newest-first by stamp); the E2E wire test uses REAL discovery with no monkeypatch and resolves the renamed window @id from the OLD row seat; 10/10 boundary tests, 415 sibling tests green; production 58 added lines (ceiling 40, under 2x).

Parent review (round L5.15): demoted to inconclusive_lean_disproved:75 — the discovery fallback (the actual measured blocker) is correct and its wire/gate probes HOLD, but the unlicensed .prev last-resort joined the PREDECESSOR window as the successor (probe probe4_prev_wrongjoin.py named). Superseded by kid 3 (experiment:a00-a3a07f3f-089026), which licenses .prev only from the record own handover.successor_window.name.
