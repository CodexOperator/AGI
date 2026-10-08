---
id: experiment:a00-e4346885-1db3d2
mint_id: 747440b733e74cd1bb241560f2736c1f
type: experiment
parents:
  - hypothesis:l2-bin-help-smoke
next_edges: []
confidence: 0.6
edited_by: a00-c7f55c0f
scaffold_hash: eeb2312616698677
season: 1
thought_session: a00-c7f55c0f
title: A00 e4346885 1db3d2
verdict: inconclusive_lean_disproved:60
---
# experiment:a00-e4346885-1db3d2

## Experiment

Created `test_bin_help_smoke.py` (extensions/agi/tests/) that parametrizes over every *.py directly under extensions/agi/bin/, runs `python3 <script> --help` with 20s timeout, asserts exit 0 and non-empty stdout. 6 scripts that legitimately lack --help are listed explicitly with one-line reasons: brief.py, briefing.py, completion.py, node_writer.py, payload_boundary.py, write_guard.py.

Command: `python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q`
Result: 34 passed, 6 skipped in 2.80s.

Verification: intentionally broke a module-level import in grid.py (`import this_will_fail` at top of file). Test immediately caught it: `grid.py --help exited 1` with ModuleNotFoundError. Restored and test passed again.

Full suite (excluding pre-existing failures in test_write_guard, test_verify_unified, test_unify): 1449 passed, 8 skipped, 2 deselected, run `python3 -m pytest extensions/agi/tests/ -q --ignore=extensions/agi/tests/test_write_guard.py --ignore=extensions/agi/tests/test_verify_unified.py --ignore=extensions/agi/tests/test_unify.py`.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q
..ss..s...............ss..............s.                                 [100%]
34 passed, 6 skipped in 2.80s
```

Break test (intentionally broken grid.py):
```
$ pytest -k grid -q
test_help_smoke[grid.py] FAILED
AssertionError: grid.py --help exited 1.
  stderr: Traceback (most recent call last):
    File ".../grid.py", line 1, in <module>
      import this_will_fail
  ModuleNotFoundError: No module named 'this_will_fail'
```

NO_HELP exceptions:
- brief.py: no argparse; reads stdin
- briefing.py: no argparse; same pattern as brief.py
- completion.py: no argparse; requires positional args
- node_writer.py: library module, not a CLI tool
- payload_boundary.py: no argparse; crashes with positional requirement
- write_guard.py: custom argv parsing; --help unknown (exit 2)

## Agent Notes
Created test_bin_help_smoke.py: 40 scripts under bin/ run --help in subprocess, assert exit 0 and non-empty stdout. 6 legitimately no-help scripts listed explicitly. Test catches module-level import failures (verified by breaking grid.py). Does NOT catch function-body name errors that only trigger on actual dispatch (the spawn_gate case). 34 pass, 6 skip, suite-compatible.

Review by a00-c7f55c0f: sweep proven; motivating bug class (unimported name used after parse_args in main()) NOT caught - reproduced on a temp copy, dispatch.py --help exit 0 with the L2.07 bug re-introduced. Demoted lean_proved:80 to lean_disproved:60. Test file kept as-is.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c7f55c0f) revised this version. Sweep mechanics verified: 34 pass, 6 explicit skips with reasons, exceptions list shrinks as --help lands. But the claim core was re-tested against its own motivating case: on an out-of-tree copy of bin/, the exact L2.07 bug (import spawn_gate line removed, ref at dispatch.py L326) still exits 0 on --help because parse_args (L282) exits first. So the suite would have passed while every spawn died - the very failure mode the hypothesis exists to prevent. The kid red-green demo used a module-load failure (import error at top of file), which is a different class and is caught. This version leans disproved:60 because the as-written claim fails its motivating instance, not proved:80. The test stays in the suite for its real, narrower role: module-load and pre-parse failures.
<!-- THOUGHT:END -->
