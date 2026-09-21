---
id: experiment:a00-39aeb1ef-5dd96b
mint_id: faf65d6281c849119b3008aa96eb328f
type: experiment
parents:
  - hypothesis:l4-the-seating-merged-fixture-is-written-and-merged-by-both-rotate-producers-and-read-back-from-disk
next_edges: []
confidence: 0.85
edited_by: a00-4fcaf2ee
evidence_runs:
  - experiment:a00-39aeb1ef-5dd96b
loop: hypothesis:l4-the-seating-merged-fixture-is-written-and-merged-by-both-rotate-producers-and-read-back-from-disk@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "PROBE=writer_suffix pytest extensions/agi/tests/test_sensei_rotate_out_audit.py -q (conftest wraps rotate._write_seating_record to name <seat>.<stamp>.json, a suffix the merger glob *.seating.json cannot see)", "expected": "seating_merged tests fail because the file the fixture wrote is not the file the merger globs", "observed": "2 failed, 28 passed -- test_predecessor_resolves_join_absent_shapes[seating_merged] and test_rotate_out_audit_resolves_near_miss_and_classifies[seating_merged], at 'assert merged_path == str(written)'", "result": "refused"}
  - {"conjunct": 2, "class": "wire", "cmd": "PROBE=wire pytest extensions/agi/tests/test_sensei_rotate_out_audit.py -q (conftest replaces rotate._seating_record_merge_handover with a raiser)", "expected": "the seating_merged fixture fails, proving its call site reaches the REAL merger and is not an inlined copy", "observed": "2 failed, 28 passed -- both seating_merged ids fail with 'WIRE-PROBE: merger reached'", "result": "refused"}
  - {"conjunct": 3, "class": "gate", "cmd": "PROBE=gate_nomatch pytest ... (merger returns \"\") and PROBE=gate_nomerg (merger returns the right path but never writes the handover back)", "expected": "gate_nomatch fails the equality assert; gate_nomerg fails the disk-read assert prev[handover][seating_row_commit]=='abc123' -- a returned path is refused unless the bytes were merged and read back", "observed": "gate_nomatch 2 failed at 'assert merged_path == str(written)' with observed '' == '<path>'; gate_nomerg 2 failed on the disk-read assertion", "result": "refused"}
  - {"conjunct": 4, "class": "wire", "cmd": "PROBE=record_rename pytest ... (rotate._seating_record renames gen_after -> generation_after)", "expected": "a renamed key in the seating record leaves the fixture unresolvable and fails the suite", "observed": "2 failed, 28 passed -- both seating_merged ids fail at 'assert p == tr' (resolved None)", "result": "refused"}
profile: balanced
role: kid
scaffold_hash: 45159dfd6807f540
season: 2
testable_claim: The seating_merged fixture is written by rotate._write_seating_record and merged by rotate._seating_record_merge_handover, the merger returns the file the writer wrote, and the merged bytes are read back from the PREV_STAMP slot on disk -- so a renamed key in _seating_record or a filename suffix the merger glob misses fails the suite.
title: A00 39aeb1ef 5dd96b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-39aeb1ef-5dd96b

## Experiment

Test-only build on ONE file, `extensions/agi/tests/test_sensei_rotate_out_audit.py`.
No production byte moved; `rotate.py` is byte-identical to HEAD after the round
(`git diff --quiet -- extensions/agi/bin/rotate.py` -- and `git diff --stat`
names the test file and nothing else).

### The defect (SL7.128 residue (a))

The `seating_merged` fixture in `_write_root_join_absent` (:623) INLINED the
merger body -- it built the record with `rotate._seating_record`, then copied
`merged = dict(rec.get("handover") or {}); merged.update({"seating_row_commit":
"abc123"})` by hand. A change to `rotate._seating_record_merge_handover`
ITSELF therefore stayed green: the suite tested a copy of the merger, not the
merger.

### The build (both producers, bytes on disk)

`elif shape == "seating_merged":` now drives the two producers end to end:

1. `rec = rotate._seating_record(seat=SEAT, role="prime_director",
   source="rotate", window_id=None, ref="", pid=None, session_id="",
   transcript_path=str(tr), first_turn=None, generation=GEN)` with
   `rec["recorded_at"] = "2026-09-11T10:00:00Z"` (the PREV_STAMP slot's stamp).
2. `written = rotate._write_seating_record(graph, rec)` -- the REAL writer
   (rotate.py:5286-5305), which names the file by `utcnow`.
3. `merged_path = rotate._seating_record_merge_handover(graph, {"seat": SEAT,
   "recorded_at": rec["recorded_at"], "handover": {"seating_row_commit":
   "abc123"}})` -- the REAL merger (rotate.py:5308-5354) -- and
   `assert merged_path == str(written)`, so a producer drift (a renamed key, a
   dropped merge, a filename suffix the merger's glob no longer sees) fails
   HERE.
4. `written.replace(prev_path)` renames the producer's file onto the
   PREV_STAMP slot. This is the near miss the brief named: the fixture-planted
   record `{SEAT}.{PREV_STAMP}.json` would otherwise survive, sort ahead of a
   2026-09-16 utcnow name, and let the resolver read the WRONG record while the
   test stayed green.
5. `prev = json.loads(prev_path.read_text())` -- the merged file is read back
   FROM DISK, and the fixture asserts on that disk-read dict
   (`handover.seating_row_commit == "abc123"`, no `observations`, no `join`).
   The trailing `prev_path.write_text(json.dumps(prev))` is guarded off for
   `seating_merged`, so what stays on disk is literally the two producers'
   bytes (`indent=2` + `\n`), never a dict built in the test.

The two frozen shapes (`near_miss`, `first_seating`) are untouched
byte-for-byte except for the docstring, and still serialize via the shared
trailing write.

### Falsifier proof -- three mutations of the PRODUCER, applied and reverted in place

Each mutation was applied to `extensions/agi/bin/rotate.py` with a byte backup,
the suite run, then the backup copied back and `cmp` verified.

M1 -- `_seating_record` (rotate.py:5268) writes `rec["generation_after"] =
generation` instead of `rec["gen_after"] = generation`:

```
FAILED .../test_sensei_rotate_out_audit.py::test_predecessor_resolves_join_absent_shapes[seating_merged]
E  assert p == tr, f"{shape}: resolved {p}, expected {tr}"
E  assert None == PosixPath('/tmp/.../.agi/gen14.jsonl')
FAILED .../test_sensei_rotate_out_audit.py::test_rotate_out_audit_resolves_near_miss_and_classifies[seating_merged]
E  assert code == 0
E  assert 2 == 0
2 failed, 28 passed, 4 warnings
```

M3 -- `_write_seating_record` (rotate.py:5303) writes a `...seat.json` suffix so
the merger's `*.seating.json` glob no longer sees the file:

```
FAILED .../test_predecessor_resolves_join_absent_shapes[seating_merged]
E  assert merged_path == str(written), (merged_path, str(written))
E  assert '' == '/tmp/...35Z.seat.json'
FAILED .../test_rotate_out_audit_resolves_near_miss_and_classifies[seating_merged]
E  assert merged_path == str(written), (merged_path, str(written))
2 failed, 28 passed, 4 warnings
```

M2 -- `_seating_record_merge_handover` (rotate.py:5348-5350) replaced by
`rec["handover"] = handover` (drops prior keys):

```
30 passed, 4 warnings
```

**M2 is NOT caught, exactly as the brief predicted, and the reason is
structural:** the prior handover is EMPTY (`_seating_record` never writes a
`handover` key), so `dict({}) ; update(handover)` and `= handover` produce
byte-identical json. The fixture locks the merger's CALL SITE, its
seat+recorded_at match and the path it returns -- not key preservation on a
NON-EMPTY prior. Key-preservation is unreachable through the seating producer
at all; a non-empty prior handover only exists on the rotate-self path
(`handover.spawn_row_commit`), which this fixture does not build.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py -q
..............................                                           [100%]
30 passed, 4 warnings in 0.41s
```

```
$ git diff --stat -- extensions/agi/bin/rotate.py extensions/agi/tests/test_sensei_rotate_out_audit.py
 .../agi/tests/test_sensei_rotate_out_audit.py      | 48 +++++++++++++---------
 1 file changed, 29 insertions(+), 19 deletions(-)
$ git diff --quiet -- extensions/agi/bin/rotate.py && echo "rotate.py UNCHANGED"
rotate.py UNCHANGED
```

<!-- THOUGHT:BEGIN - authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
INSTRUCTION (verbatim, from the SL7.128 residue (a) brief): "the
seating_merged fixture in extensions/agi/tests/test_sensei_rotate_out_audit.py
(_write_root_join_absent, :624-640) INLINES the merger body ... so a change to
rotate._seating_record_merge_handover ITSELF stays green." Fix, test-only, ONE
kid: (1) build prev by `rotate._write_seating_record(graph, rec)`; (2)
`path = rotate._seating_record_merge_handover(graph, {...})` and ASSERT that
path names the file (1) wrote; (3) READ THAT FILE BACK FROM DISK as `prev`.

MECHANISM VERIFIED AT FILE:LINE. `_write_seating_record(root, record)` ->
rotate.py:5286-5305 writes `<rotations>/<seat>.<utcnow>.seating.json` with
`json.dumps(record, indent=2) + "\n"` and returns the Path.
`_seating_record_merge_handover(root, record)` -> rotate.py:5308-5354 globs
`<rotations>/<seat>.*.seating.json`, skips records whose `recorded_at` differs
or that already carry a truthy `handover`, merges
`merged = dict(rec.get("handover") or {}); merged.update(handover)`, rewrites
and returns `str(target)` or `""`. `_seat_rotation_records` (sensei.py:1506)
globs `*.json` and sorts by NAME, so the fixture-planted
`{SEAT}.20260911T100000Z.json` sorts ahead of any 2026-09-16 utcnow name -- the
rename is load-bearing, not cosmetic.

PYTEST OUTPUT LINE ACTUALLY PRODUCED: `30 passed, 4 warnings in 0.41s` for
`python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py -q`;
and under mutation M1 `2 failed, 28 passed` with
`test_predecessor_resolves_join_absent_shapes[seating_merged]` failing at
`assert p == tr`; under M3 the same two ids failing at
`assert merged_path == str(written)`.

NEAR MISS. The fixture's OLD body built half its input from a real producer and
half by hand: it CALLED `rotate._seating_record` (so a key rename in the
record shape WAS caught) and then copied the merger body inline (so the merger
was NOT). One producer was real, the other was a copy, and the copy is what
the suite actually tested. The second near miss was the surviving
fixture-planted record at PREV_STAMP: without `written.replace(prev_path)` the
resolver's filename sort picks the older record and the test can go green
through the WRONG record -- the merged file is never asserted to be the one
read. The rename closes it.

DEVIATIONS. (1) The brief said "the test file only"; I additionally guarded the
shared trailing `prev_path.write_text(json.dumps(prev))` with
`if shape != "seating_merged":` inside the same function, so the merged file on
disk keeps the producers' own bytes instead of being re-serialized by the test.
The other two shapes' behaviour is unchanged. (2) I ran M1/M2/M3 by mutating
`rotate.py` in the shared worktree with a byte backup and `cmp`-verified
restore (the brief forbids editing rotate.py *as a deliverable*; the falsifier
proof requires the mutation, and `git diff --quiet` confirms the file is back
to HEAD). (3) M2 is left uncaught rather than papered over with a synthetic
non-empty prior handover: the seating producer cannot produce one, so faking it
would test a state the code never writes.
<!-- THOUGHT:END -->

## Agent Notes
seating_merged fixture now written by rotate._write_seating_record and merged by rotate._seating_record_merge_handover (asserted to name the written file), renamed onto the PREV_STAMP slot and read back from disk; M1 (renamed gen key) and M3 (filename suffix) both fail the suite; M2 (merger -> rec[handover]=handover) stays green because the seating producer never writes a non-empty prior handover. 30 passed.

PARENT REVIEW SL7.129 (a00-4fcaf2ee): reviewed the DIFF BYTES (git diff --cached on extensions/agi/tests/test_sensei_rotate_out_audit.py), not the report, and re-ran the falsifiers myself in a throwaway copy (/tmp/probe129) with a conftest that wraps the producer/merger seam. ACCEPTED. The seating_merged branch now: (1) `rec = rotate._seating_record(...)`, `rec["recorded_at"] = "2026-09-11T10:00:00Z"`; (2) `written = rotate._write_seating_record(graph, rec)`; (3) `merged_path = rotate._seating_record_merge_handover(graph, {seat, recorded_at, handover:{seating_row_commit:"abc123"}})` with `assert merged_path == str(written)`; (4) `written.replace(prev_path)` onto the PREV_STAMP slot; (5) `prev = json.loads(prev_path.read_text())`, asserted on the disk-read dict; the trailing fixture write is guarded off for this shape so the bytes on disk are literally the producers output. The old in-memory `merged = dict(rec.get(handover) or {}); merged.update(handover)` copy is GONE. FROZEN shapes near_miss / first_seating are untouched except their docstring. rotate.py byte-identical to HEAD (`git diff --stat -- extensions/agi/bin/rotate.py` empty; worktree status names only the new node and the test file). PARENT PROBES (throwaway copy, baseline `30 passed`): record_rename (rotate._seating_record renames gen_after -> generation_after) FAILS 2 [seating_merged]; writer_suffix (writer names `<seat>.<stamp>.json` so the merger glob misses it) FAILS 2 at `assert merged_path == str(written)`; wire (merger raises when reached) FAILS 2 -- the fixture does reach the real merger; gate_nomatch (merger returns "") FAILS 2 at the same assert -- the assert is non-vacuous; gate_nomerg (merger returns the right path but never writes the handover) FAILS 2 on the disk-read `prev[handover][seating_row_commit]` -- the conjunct that matters is the read-back, not the returned path. m2_drop (`rec["handover"] = handover`, dropping prior keys) stays GREEN, confirming the kid own honest caveat: _seating_record never writes a handover, so prior-key preservation is unreachable from this fixture and is NOT locked. RESIDUE (named, out of scope): (a) the merger idempotency/prior-key-merge path is untested because only a rotate-self record carries a non-empty prior handover; (b) the fixture renames the merged file `.seating.json` -> `.json` (the PREV_STAMP slot), so the production suffix is not exercised end to end.
