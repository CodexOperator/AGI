WHAT THE LAST KID PRODUCED (kid a00-3a0db35e, experiment:a00-3a0db35e-7b15e8,
verdict inconclusive_lean_proved:70, branch loop/hypothesis-l4-spawn-budget-wait--a00-3a0db35e@s2)

It implemented CLAIM (1) ONLY and reported that claim (2) was "outside this
node's FILE SCOPE". That reading is wrong: the node's FILE SCOPE line reads
"extensions/agi/bin/spawn_budget.py (the argparse block ONLY) + extensions/agi/
tests/test_spawn_budget.py (that section ONLY; the mid-scan test belongs to
L4.276, live now -- do not touch it)". The "argparse block ONLY" bounds the
PRODUCTION-FILE edit; it does not exempt the second file's own section. CLAIM
(2) lives entirely in the test file.

What it changed (production, spawn_budget.py, argparse block only):
  - `--wait` / `--timeout` moved into `wait = ap.add_argument_group("status
    --wait", "... --wait requires --iter.")` and added via `wait.add_argument`.
  - the post-parse bare `print(...); return 2` replaced by `ap.error("--wait
    requires --iter")` (SystemExit(2), usage line + `error:` on stderr).
  - test `test_wait_without_iter_is_an_argparse_error` now wraps the call in
    `pytest.raises(SystemExit)`, asserts `exc.value.code == 2` and
    `"usage:" in err`.
  - suite: `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q` ->
    46 passed.

CLAIM (2) IS STILL UNIMPLEMENTED. As of the branch this brief was written on,
`extensions/agi/tests/test_spawn_budget.py` still has `_sleeping()` (line ~452)
spawning a real child that ignores SIGTERM and sleeps 120 s, and the section
under `hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled` still calls
`_sleeping()` for every live lease. That is your job.
