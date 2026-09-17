---
id: experiment:a00-a3a07f3f-089026
mint_id: 269d62f21ebd4f3485b4eda1459f5bcb
type: experiment
parents:
  - hypothesis:l5-after-join-greps-the-old-post-name-at-a-rename-boundary
next_edges: []
confidence: 0.8
edited_by: a00-d595594e
evidence_runs:
  - experiment:a00-a3a07f3f-089026
line_ceiling: 40
loop: hypothesis:l5-after-join-greps-the-old-post-name-at-a-rename-boundary@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "scratch probe/probe2_endtoend.py + probe3_crossseat.py (boundary record discovered from OLD seat; no cross-seat leak; name match beats fallback)", "expected": "the boundary record reaches the changed join bytes from the OLD row seat", "observed": "discovered sextest-new.20260101T000000Z.json from sextest; beta keeps its own record — HELD", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "scratch probe/probe6_e2e_join.py (run_after_join_for_seat with REAL discovery, window file varying; spy on _join_successor)", "expected": "unlicensed .prev resolves no @id (named refusal); licensed .prev resolves @9; renamed target @7 wins", "observed": "unlicensed: _join_successor not called; licensed: @9; target: @7 — HELD", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "scratch probe/probe5_prev_e2e.py (_rename_boundary_names licensing: none / handover.successor_window.name == new.prev)", "expected": "<new>.prev is a candidate only when the record own bytes name it the successor", "observed": "unlicensed -> [new]; licensed -> [new, new.prev] — HELD", "result": "held"}
production_lines: 32
profile: balanced
role: kid
scaffold_hash: 09ae4bc4e19d02cd
season: 2
title: The rename boundary licenses .prev only when the record names it the successor
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-a3a07f3f-089026

## Experiment

The L5.15 rename-boundary after_join, finished safely. The claim is a BUILD
ORDER (g15): make the after_join JOIN resolve at a boundary that also renames
the post, WITHOUT ever joining the predecessor.

WHAT WAS UNSAFE (the parent's falsifying gate probe): `_rename_boundary_names`
returned `[<new>, "<new>.prev"]` UNCONDITIONALLY and `run_after_join_for_seat`
passed `.prev` as the last-resort successor alias. But step (2) of the boundary
carries the PREDECESSOR's own window aside to `<name>.prev`, so `.prev` is
never the successor: with only `@9 sextest-new.prev` live and a registry entry
for `@9` carrying the predecessor's pid/session, the join resolved `@9` and
returned the predecessor as the successor. Making an unresolved join become a
WRONG join is worse than refusing.

BUILT (all in `extensions/agi/bin/rotate.py`, no other production file):

1. New `_record_names_prev_as_successor(rec, new)` (rotate.py:11191): True ONLY
   when the record's OWN bytes name `<new>.prev` as its successor window —
   `handover.successor_window.name` (rotate.py:18951, the fact rotate-self
   writes) or the same shape at the TOP level (the crash-recovery record).
   Absent, malformed or a different name -> False.
2. `_rename_boundary_names` now returns `[<new>]` always, and appends
   `<new>.prev` ONLY when that helper licenses it. Unlicensed `.prev` is not a
   candidate, so the existing no-window refusal fires instead of a wrong join.
3. Kid 2's `_latest_rotate_record` rename-boundary fallback (bounded,
   newest-first, matched on the record's own `applied_rename.old`) and the
   renamed-target-first join are kept unchanged. The OLD name is still never a
   candidate.

MEASURED (scratch probe `probe_safe_prev.py`, real `_successor_window_id` and
`_join_successor`, window file holding only `@9 sextest-new.prev`):

```
UNLICENSED names=['sextest-new'] window_id=None
LICENSED   names=['sextest-new', 'sextest-new.prev'] window_id='@9'
REFUSAL    {'found': False, 'window_id': None,
            'note': 'no successor window @id captured (window_id empty)'}
```

## Evidence

`extensions/agi/tests/test_after_join_rename_boundary.py` — 11 passed:
- REWRITTEN (was the unsafe assertion) `test_prev_only_window_is_refused_when_
  the_record_does_not_name_it`: only `.prev` live + record without the fact ->
  `_join_successor` is never handed a window @id, values pid/session stay None,
  the join takes the NAMED refusal path, and the refusal note names
  `window_id empty`. REWRITTEN, not deleted.
- NEW `test_prev_only_window_resolves_when_the_record_names_it_successor`:
  `handover.successor_window.name == "sextest-new.prev"` licenses `.prev` and
  the real alias resolution joins `@9`.
- REWRITTEN `test_boundary_candidates_license_prev_only_from_the_records_own_
  fact`: `.prev` candidate only with the record fact (both record shapes).
- Kid 2's E2E real-discovery test and the renamed-target-first test kept and
  still green.

```
pytest test_after_join_rename_boundary.py -q            -> 11 passed
pytest test_after_join_service.py test_rotate_boundary_rename.py
       test_rotate.py -q                                -> 415 passed
git diff --numstat -- extensions/agi/bin/rotate.py       -> 32  5
```

Production lines: 32 added (ceiling 40; under the 80 = 2x stop line). Test
files excluded.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID: make the .prev candidate safe — the successor window is the renamed target, and step (2) carries the PREDECESSOR own window aside to <name>.prev, so an unlicensed .prev can only join the predecessor. WHAT THE MACHINE ACTUALLY DOES: kid 3 added _record_names_prev_as_successor(rec, new) (rotate.py:11191) which reads the record OWN bytes — handover.successor_window.name, or the top-level successor_window.name of a crash-recovery record — and _rename_boundary_names now returns [new] plus <new>.prev ONLY when that fact names it (rotate.py:11211). The renamed target stays first; the unlicensed .prev is simply not a candidate, so the existing NAMED refusal (no successor window @id captured) fires. NEAR MISS: keeping the old test that asserted .prev-joins-the-predecessor would have certified a wrong join; kid 3 rewrote it to assert the refusal and kept a licensed positive case. MY PROBES (parent-run): probe5_prev_e2e.py HOLDS (unlicensed -> no @id, licensed -> @9, renamed target preferred), probe6_e2e_join.py drives run_after_join_for_seat with REAL discovery and shows _join_successor is never called with the predecessor @id, probe2/probe3 HOLDS (discovery + no cross-seat leak). Neighbour suites 428 passed. IF I DEVIATED: recorded lean_proved:80 not proved — the fix is proven at the seam/unit level and end-to-end through the watch function, but no LIVE rotation was run, so the pin and automatic reap downstream are not measured here.
<!-- THOUGHT:END -->

## Agent Notes
Rename-boundary after_join finished safely: .prev is a successor-window candidate only when the record's own handover.successor_window.name licenses it, so the parent's predecessor-wrong-join probe now refuses by name; renamed-target-first join and kid 2's record fallback kept; unsafe test rewritten, 11+415 tests green, 32 production lines
