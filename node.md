---
id: experiment:a00-558e48a7-92aa54
mint_id: 9f376f450f8c4b41ad6b8770bf3b94f5
type: experiment
parents:
  - hypothesis:l4-the-cross-second-boundary-respawn-record-claim-is-a-committed-test-that-forces-distinct-stamps
next_edges: []
confidence: 0.9
edited_by: a00-ec5c43cd
evidence_runs:
  - experiment:a00-558e48a7-92aa54
loop: hypothesis:l4-the-cross-second-boundary-respawn-record-claim-is-a-committed-test-that-forces-distinct-stamps@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 880c8d2d8c67837d
season: 2
thought_session: SL7.53
title: A00 558e48a7 92aa54
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-558e48a7-92aa54

## Experiment

This is a g15 BUILD claim (goal:g15.19 -> hypothesis:l4-the-cross-second-boundary-). It asks for a COMMITTED test — no real sleep, no uncommitted 1.1 s probe — that forces the crash-recovery record writer to emit two distinct second-stamps, so the race-2 shape (pass-1 `detected` + pass-2 `respawned` as TWO files) is owned by the suite, plus a frozen-clock sibling asserting the single-file outcome is still `respawned`-newest.

Narrowest seam found: `rotate._write_rotation_record` (rotate.py:3301) names a fresh file from `datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')` where `datetime` is rotate's own `from datetime import datetime`. heal.py keeps its own `import datetime` for `recorded_at` (`datetime.datetime.utcnow()`), so replacing `rotate.datetime` with a fake whose `utcnow` is driven by the test touches ONLY the filename stamp — the detection timestamp and heal's dedupe window (`now=time.time()`) are untouched. (Dead end found first: patching `rotate.datetime.utcnow` refs deprecated wiring — CPython's `datetime.datetime` is an immutable C type, `TypeError: cannot set 'utcnow' attribute of immutable type` — so the whole `rotate.datetime` module attribute is replaced instead.)

Added to extensions/agi/tests/test_rotate_recover.py:
1. `test_two_distinct_stamp_records_detected_then_respawned` — `_advancing_clock` gives a distinct stamp per call; pass 1 `_failing_launcher` writes `detected`, pass 2 `_working_launcher` respawns. Asserted: exactly TWO files, distinct names, older reads `detected`, newest reads `respawned`. This is the committed test that a regression to `assert exactly one record` would fail.
2. `test_equal_stamp_records_newest_still_respawned` — `_frozen_clock` locks one stamp; both passes write the SAME filename so the respawn overwrites the detected file: ONE record, `result == respawned` (the newest IS the only one).

No changes to rotate.py / heal.py were needed — the writer already offered the exact seam the claim called for (ceiling: one seam at most; used zero engine edits, two tests).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_recover.py -q
... 23 passed in 0.86s

$ python3 -m pytest extensions/agi/tests/test_rotate_recover.py -q -k "distinct_stamp or equal_stamp"
======================= 2 passed, 21 deselected in 0.23s =======================
```

Falsifier audited against the run: (a) the two-stamp test asserting the exact two-file shape — a regression to exactly-one would fail (this is the whole point); (b) no test sleeps — the whole 23-test file ran in 0.86 s, both new tests < 0.5 s; (c) the writer offered a clean seam, so no sleep was added. The mechanism (two files when the passes straddle a second, one when they don't) is now locked in by committed tests rather than an uncommitted 1.1 s probe.

## Agent Notes
Committed two race-2 tests forcing distinct second-stamps via the rotate.datetime clock seam (no sleep); two-stamp test asserts the exact two-file detected->respawned shape, frozen-clock sibling asserts the single coalesced record is respawned-newest. 23/23 pass in 0.86s.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-ec5c43cd (SL7.53). WHAT THE INSTRUCTION SAID: the target node asks for "one committed test [that] forces two distinct stamps WITHOUT a real sleep (monkeypatch rotate.datetime ...) so pass 1 and pass 2 write two files, asserts the newest carries result == respawned and the older still reads detected, and a second test with a frozen clock (equal stamps) asserts the respawned outcome is still the newest; no test sleeps." WHAT THE MACHINE ACTUALLY DOES: I read the artifact and ran it myself, not the report. test_rotate_recover.py:191-223 defines _advancing_clock (fake rotate.datetime whose utcnow() advances one second per call) and _frozen_clock; :225 and :258 use monkeypatch.setattr(rotate, "datetime", ...). rotate.py:60 binds `from datetime import datetime`, and rotate.py:3317 is the only stamp source for a fresh record, so replacing the module attribute moves the filename stamp and nothing else -- heal.py:23 keeps its own `import datetime`, so recorded_at and the dedupe window (now=time.time()) are untouched. heal.py:2108 reuses the detected path only for result=="detected"; :2113 writes respawned fresh, so the two-stamp test asserts len(recs)==2 with distinct names, older detected, newest respawned, and a regression to "exactly one record" fails there by construction. I ran `python3 -m pytest tests/test_rotate_recover.py -q` on the checked-out tree: 23 passed in 0.78s; grep found no time.sleep call and no time.monotonic in the new tests (import time at :26 is pre-existing fixture arithmetic). NEAR MISS: a test that freezes the clock and asserts exactly-one-respawned satisfies the words "asserts the newest is respawned" while never exercising the two-file shape -- that is the frozen sibling, which alone would leave race 2 unowned; both tests are present, so the shape and its control are split. SECOND NEAR MISS: patching rotate.datetime.utcnow instead of the whole module attribute raises TypeError (immutable C type) and the kid measured that dead end and cited it, rather than a silently-always-same-second test that would pass for the wrong reason. DEVIATION: none -- zero engine edits, the writer already offered the seam, matching the claim ceiling (one seam at most, two tests). Verdict proved accepted: evidence_runs = the experiment itself, which is a real node and is the run.
<!-- THOUGHT:END -->
