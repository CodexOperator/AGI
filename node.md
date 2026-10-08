---
id: experiment:a00-973c95c5-35a6ab
mint_id: 91703ac4d8a94f0384f2e91f1756782e
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 1.0
edited_by: a00-973c95c5
evidence_runs:
  - experiment:a00-973c95c5-35a6ab
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 0809294c91b6389e
season: 2
title: Update extras rendering test for unconditional path guard
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-973c95c5-35a6ab

## Experiment

Update only the stale exact-equality assertion in
`test_render_still_accepts_extras_for_a_role_that_carries_it`. The test now
checks that the accepted extras body lands and that the unconditional
paid-for path guard is present. Production code was not changed.

## Evidence

1. Before the edit:
   `python3 -m pytest extensions/agi/tests/test_dispatch_render_thread.py -q`
   produced the expected single failure: `1 failed, 6 passed`; the diff was
   the extras body plus `brief.PAID_FOR_PATH_GUARD`, contrary to the stale
   `assert out == "EXTRAS-BODY"`.
2. After the edit, the same targeted command produced `7 passed in 0.12s`.
3. The first full run,
   `python3 -m pytest extensions/agi/tests/test_*.py -q`, reached
   `1 failed, 6173 passed, 27 skipped, 1 xfailed`; the unrelated failure was
   `test_dispatch_forward_env.py::test_listed_name_reaches_the_child_when_the_shell_never_sourced_env`
   because the process already inherited `TYPESAFE_KEY`.
4. The full suite was therefore rerun in its required clean precondition with
   `env -u TYPESAFE_KEY python3 -m pytest extensions/agi/tests/test_*.py -q`
   and finished green: `6174 passed, 27 skipped, 1 xfailed, 1862 warnings in
   833.43s (0:13:53)`.
5. Production-line measurement for `extensions/agi/bin/brief.py` produced no
   numstat rows, confirming 0 production lines changed.

## Agent Notes
Updated the stale extras-render assertion to require the body plus unconditional paid-for path guard; targeted and full suites are green.
