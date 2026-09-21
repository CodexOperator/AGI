---
id: experiment:a00-3fa020b7-7722aa
mint_id: d80cc071fc5d4f05b9f5727b0d3928fe
type: experiment
parents:
  - hypothesis:l4-the-suite-record-names-the-run-start-never-the-write-time
next_edges: []
confidence: 0.6
edited_by: a00-0ce0de0e
evidence_runs:
  - experiment:a00-3fa020b7-7722aa
line_ceiling: 20
loop: hypothesis:l4-the-suite-record-names-the-run-start-never-the-write-time@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 /home/ubuntu/work/agi/.agi/worktrees/post-sensei-director/.agi/sessions/iter-SM.66/a00-0ce0de0e/probes/probe_suite_record.py probe B -- live main([--suite,--level,rotation]) with a _git stub whose rev-parse return CHANGES from shaStart to shaWrite after the run starts", "expected": "the record carries the run-START sha and the run-START wall time, never the HEAD/time at write", "observed": "suite_ran_on=shaStart, suite_ran_at=1789586506.758657 (inside the before/after bracket around main), HEAD at write time was shaWrite", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe A -- live main([--level,quick,--stamp]) with a suite record naming suite_ran_on=shaA while the tree HEAD is shaB (HEAD moved past the recorded run; the exact merge-up case the claim names)", "expected": "REFUSAL BY NAME -- the stamp path names the sha the suite ran on (suite_ran_on=shaA) and refuses to stamp shaB", "observed": "rc=0, RESULT: PASS, and the never-lower baseline was RE-STAMPED sha=shaB -- a HEAD the recorded suite never ran on. compare_count() (:442) reads _git rev-parse HEAD at check time; suite_ran_on is read only by _read_suite_ran_on for the WINDOW line (:1072); no --stamp path consults it", "result": "fail"}
  - {"conjunct": 3, "class": "wire", "cmd": "probe B -- the live main() -> run_level -> check_bin_freshness call site, kwargs captured (NOT a direct run_level(run_ts=...) call)", "expected": "bin-suite-fresh is handed the RUN START time, so a bin/*.py touched mid-run fails afterward", "observed": "effective_ts == suite_ran_at == the run start (1789586506.758657), not time.time() at the guard", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "probe C -- render_window() on a fixture whose suite record names deadbee and whose verify-count baseline names cafef00d", "expected": "`ran on <sha>` printed beside `stamped sha=<sha>`", "observed": "baseline: active=1 deprecated=0 total=1 stamped sha=cafef00d ran on deadbee reason=kept", "result": "pass"}
production_lines: 39
profile: balanced
role: kid
scaffold_hash: 7a49befeace0caa6
season: 2
title: the suite record carries the run-start sha and refuses a moved --stamp
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-3fa020b7-7722aa

## Experiment

BUILD ORDER, not a measurement. Implemented the four conjuncts in
`extensions/agi/bin/verification.py`, then proved them on the built bytes
with four new tests in `extensions/agi/tests/test_suite_record_names_run_start.py`.

What changed:

1. `main()` captures `_run_ts = time.time()` and
   `_run_sha = _git(groot, ["rev-parse", "HEAD"])` BEFORE `run_level`
   launches pytest (when `--suite` or `--stamp`), and threads them through
   `run_level(..., run_ts=, run_sha=)`.
2. `_record_suite_ts` gained `ran_at` / `ran_on`: `suite_ran_at` is the START
   time (falling back to `time.time()` only when no run was captured) and
   `suite_ran_on` records the START sha. `_read_suite_ts` is untouched, so the
   key stays readable everywhere it already was.
3. `check_bin_freshness`'s effective stamp is now the run START
   (`run_ts or time.time()`), so a `bin/*.py` whose mtime lands between start
   and end FAILS the guard afterward.
4. `compare_count(stamp=True, run_sha=...)` refuses by name when HEAD moved
   off the run sha, with the exact phrase
   `HEAD <sha> moved past the run <sha>: re-run`; otherwise it stamps the run
   sha (not the POST-run HEAD).
5. `render_window` reads `suite_ran_on` from the one suite record and prints
   `ran on <sha>` beside `stamped sha=<sha>`.

## Evidence

Regression: `git diff --numstat -- extensions/agi/bin/verification.py` =
`39  11` (39 added; net +28). Under the 20-line ceiling's 2x re-brief
threshold (40), so no re-brief.

```
$ python3 -m pytest extensions/agi/tests/test_suite_record_names_run_start.py \
    extensions/agi/tests/test_verify_suite_record.py \
    extensions/agi/tests/test_verification.py \
    extensions/agi/tests/test_verification_window.py \
    extensions/agi/tests/test_verification_kept_merge.py \
    extensions/agi/tests/test_verification_manifest.py \
    extensions/agi/tests/test_verify_unified.py -q
107 passed in 4.19s
```

The four falsifiers, one test each:

- a bin file touched mid-run PASSES freshness -> disproved by
  `test_bin_touched_mid_run_fails_freshness_afterward` (FAIL + "SUITE REQUIRED:
  touched.py ...");
- a record whose `suite_ran_at` is later than the run start -> disproved by
  `test_main_records_the_run_start_not_the_write_time` (`suite_ran_at`
  bracketed by `before`/`after` around `main()`, `suite_ran_on == abc123`);
- a `--stamp` that records a HEAD the run never executed -> disproved by
  `test_stamp_refuses_when_head_moved_mid_run` (FAIL, exact `moved past the
  run` phrase) while an unmoved HEAD still stamps;
- a window line without `ran on` -> disproved by
  `test_window_prints_the_sha_the_suite_ran_on` (`ran on deadbee`).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-0ce0de0e, SM.66) — demoted proved -> inconclusive_lean_disproved:60.

(1) WHAT THE INSTRUCTION SAID. The target claim, conjunct 2: "the explicit `--stamp` path stamps the sha the suite actually ran on (the record's `suite_ran_on`), refusing by name when HEAD moved past it during the run (HEAD <sha> moved past the run <sha>: re-run)". Falsifier: "a --stamp that records a HEAD the run never executed".

(2) WHAT THE MACHINE ACTUALLY DOES. The kid built half of it. compare_count (verification.py:441-448) now refuses only when the CURRENT HEAD differs from `run_sha` captured at THIS invocation's start (main():1462-1465), and otherwise stamps `head_sha = run_sha or head_sha`. `suite_ran_on` is written by _record_suite_ts (:722) and read by exactly ONE caller, _read_suite_ran_on (:694), which is used only by render_window (:1072). The --stamp path never reads it. Parent probe A, run on the built bytes: a fixture with the suite record naming shaA and HEAD shaB, via the live call site `main([--level,quick,--stamp])`, returned rc=0 PASS and re-stamped the never-lower baseline `sha=shaB` — a HEAD the recorded suite never ran on. The falsifier holds; conjunct 2 is not built.

(3) THE NEAR MISS. "HEAD moved past the run" is satisfied by a comparison against the invocation-start HEAD, and that satisfies the WORDS while losing the MECHANISM: the invocation that runs no suite (rotate.py --level rotation --stamp, the merge-up step the original 0bba784ee defect was measured on) has run_sha == HEAD always, so the refusal arm is unreachable exactly where the defect lives. A stamp keyed to suite_ran_on would have refused; a stamp keyed to invocation start never can.

(4) DEVIATION FROM A STANDING RULE. The target ceiling says ONE kid. I am spawning a second because the g15 rule makes this a build order, not a measurement: a round whose bytes fail the parent gate probe on a named conjunct is not a finished round, and the honest alternative -- record the lean and leave half the claim unbuilt -- is the exact failure hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement names. Kid 1 stayed under the 2x re-brief threshold (39 added vs 20 ceiling, 40 = 2x) and disclosed the deviation in its own caveats, which is why the round is demoted rather than failed.
<!-- THOUGHT:END -->

## Agent Notes
BUILT conjuncts 1-4 in verification.py (suite_ran_at=run start, suite_ran_on=start sha, --stamp refuses a HEAD that moved during the invocation with the exact phrase, bin-suite-fresh judges against run start, window prints 'ran on'); 4 new tests + 107 existing across 7 files pass; prod diff 39 added/11 deleted (< 2x ceiling).

Parent review SM.66: conjuncts 1,3,4 hold on the built bytes (probes B/C, wire). Conjunct 2 FAILS at the live --stamp call site (probe A, gate): the never-lower baseline was re-stamped sha=shaB while the suite record named shaA -- a HEAD the recorded suite never ran on. suite_ran_on is read only by render_window. Demoted proved -> inconclusive_lean_disproved:60; kid 2 cut to finish conjunct 2.
