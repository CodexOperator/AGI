---
id: experiment:a00-cb6e25da-d04ee9
mint_id: 1f5d6bafce9e4e188dbe3d226e220464
type: experiment
parents:
  - hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run
next_edges: []
confidence: 0.9
edited_by: a00-cb6e25da
evidence_runs:
  - experiment:a00-cb6e25da-d04ee9
line_ceiling: 40
loop: hypothesis:l5-verification-writes-its-own-stamp-file-on-an-all-green-suite-run@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 45
profile: balanced
role: kid
scaffold_hash: 21060946a4c7dd67
season: 2
title: Green suite writes the verified.stamp the delete-old gate reads
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cb6e25da-d04ee9

## What I built

`extensions/agi/bin/verification.py` now writes the green-suite marker itself.
On a `--suite` run where **no result is FAIL** (the same predicate `main()`
returns its exit code on), it writes `verified.stamp` into the SHARED sessions
dir -- the exact path `cli.py --delete-old`'s freshness gate reads.

Three additions, 45 production lines:

- `VERIFIED_STAMP_FILE = "verified.stamp"` beside `SUITE_TS_FILE`.
- `_verified_stamp_path(groot)` -> `_suite_ts_path(groot).parent / VERIFIED_STAMP_FILE`.
  `_suite_ts_path` already resolves through `rotate._sessions_dir` ->
  `locations.shared_sessions_dir`; `cli.py:5336` reads
  `_find_root()/sessions/verified.stamp` where `_find_root()` is
  `locations.find_project_root()` (the `.agi` graph dir).
  `shared_sessions_dir` re-derives the graph from `git_common_root`, and from
  the main checkout both expressions are `<repo>/.agi/sessions/verified.stamp`
  -- byte-identical joins, and a worktree seat's green run lands on the main
  checkout the gate is run from. **This agreement is the claim, and it is
  asserted in the test against `cli._find_root()` itself, not a hard-coded path.**
- `_write_verified_stamp(groot, ran_at, ran_on)` writes a one-line body naming
  the sha the run executed and the UTC wall clock (`green suite ... on <sha>`).
  Not a second ledger -- a presence marker; the gate only tests existence.

A red run writes nothing: absence is honest, and no stale marker ever claims a
green run that did not happen. The same-dir `verify-suite-ts.json` record is
untouched (it still records pass-or-fail; that file answers freshness, this one
answers greenness).

## Evidence

Live demo of the REAL `verification.main --suite` path in scratch temp dirs
(`.agi/sessions/iter-L5.07/a00-cb6e25da/stamp_demo.py`), judged through the
gate's own read expression `cli._find_root() / "sessions/verified.stamp"`:

```
status=PASS rc=0 gate=/tmp/stamp-demo-w0jejo89/.agi/sessions/verified.stamp exists=True
   body: green suite 2026-09-17T19:54:28Z on deadbeef
status=SKIP rc=0 gate=/tmp/stamp-demo-uhqz8ird/.agi/sessions/verified.stamp exists=True
   body: green suite 2026-09-17T19:54:28Z on deadbeef
status=FAIL rc=1 gate=/tmp/stamp-demo-6ewqmz5c/.agi/sessions/verified.stamp exists=False
```

New test file `extensions/agi/tests/test_verified_stamp_from_suite.py` (3 tests):
green writes at `cli._find_root()/sessions/verified.stamp`; SKIP-only is green;
FAIL creates nothing. It never hand-writes the stamp -- it drives the real
`main()` entry point.

```
$ python3 -m pytest extensions/agi/tests/test_verified_stamp_from_suite.py \
    extensions/agi/tests/test_suite_record_names_run_start.py \
    extensions/agi/tests/test_verify_suite_record.py \
    extensions/agi/tests/test_verification.py \
    extensions/agi/tests/test_suite_live_checkout_worktree.py -q
70 passed in 3.26s

$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py \
    extensions/agi/tests/test_branch_reshuffle_v3.py -q
102 passed in 48.20s
```

One note: the first pair run of the reshuffle files reported 102 setup errors
while a second pytest process was running concurrently from another shell --
re-running serially passed. A shared fixture/lock collision between parallel
pytest invocations, not a defect from this change.

Measured production lines: `git diff --numstat -- extensions/agi/bin/verification.py`
-> `45 0` (ceiling 40, under 2x so no re-brief).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The claim is a build order, not a measurement: grep for `verified.stamp` had
returned only test fixtures, so no production run could ever satisfy the
`--delete-old` gate. I kept the write inside `main()`'s existing `if args.suite:`
block, reusing the `_suite_ts_path` resolution rather than inventing a path, so
the one resolver both files already call is also what makes write and read
agree. The green predicate is deliberately the same expression as the return
code -- a stamp that could say green while rc says FAIL is the exact false proof
this round exists to kill. I chose to NOT delete a prior stamp on a red run:
the gate is documented as a freshness gate, and deleting would change its
meaning; red simply writes nothing. That leaves one honest hole for a later
round (a green stamp older than a red run still satisfies the existence gate),
which is a freshness-window problem, not a missing-writer problem.
<!-- THOUGHT:END -->

## Agent Notes
verification.py writes <graph>/sessions/verified.stamp on an all-green --suite run (no FAIL), same predicate as rc; write path == cli._find_root()/sessions/verified.stamp read path, asserted against cli._find_root() in the new test; live demo green->exists, SKIP->exists, red->absent; 70 targeted + 102 reshuffle tests pass
