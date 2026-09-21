---
id: experiment:a00-9f5b1b42-19b948
mint_id: 6f810f1883114bd19aa4418a84aea69c
type: experiment
parents:
  - hypothesis:l4-spawn-budget-status-waits-for-the-parent
next_edges: []
confidence: 0.9
edited_by: a00-82dbbd88
evidence_runs:
  - experiment:a00-9f5b1b42-19b948
loop: hypothesis:l4-spawn-budget-status-waits-for-the-parent@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: bc9c3edac017c380
season: 2
title: A00 9f5b1b42 19b948
town: core
verdict: proved
---
# experiment:a00-9f5b1b42-19b948

## Experiment

G15 build order (hypothesis:l4-spawn-budget-status-waits-for-the-parent). Parent
review of KID #1 (experiment:a00-b594a221-f1d58c) found the node overclaimed by
one clause: the node body and the hypothesis both assert "on timeout it prints
the last-seen view AND `ERR: ... parent still live after Ss` to stderr, exits
2", but `_round_status_wait` (spawn_budget.py) went straight from the deadline
check to the ERR print + `return 2`, never calling `_print_remaining_rows`.
Test (c) `test_wait_parent_never_goes_times_out_exit_2` only asserted the ERR
line and exit 2 — it never checked the last-seen view, so the overclaim passed
green.

Measured the pre-fix state (read-only, no sleep): on the timeout branch the
only output was the ERR line to stderr; stdout was empty. The claim's
"last-seen view" clause was unmet.

Fix (additive, one hunk): in `_round_status_wait`, on the deadline branch call
`_print_remaining_rows(root, nnn)` before printing the ERR line / returning 2.
That prints whatever live rows remain for the round (the still-live parent,
plus any live kids) to stdout — the "last-seen view".

Test (c) strengthened to assert the clause: after the change it checks
`"parent-0" in out` (the live parent row printed as the last-seen view) in
addition to the ERR line in stderr and exit 2.

## Evidence

Files changed:
- extensions/agi/bin/spawn_budget.py — `_round_status_wait` timeout branch now
  calls `_print_remaining_rows(root, nnn)` before the ERR print.
- extensions/agi/tests/test_spawn_budget.py — test (c) strengthened to assert
  the last-seen view on timeout.

`python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q -k wait`
  -> 7 passed (all `--wait` cases: already-finished no-sleep, removal-returns-0,
  timeout-exit-2, unknown-round-exit-3, `--wait`-without-`--iter`-argparse).

`python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q` -> 45 passed.

The timeout path: parent lease never clears -> loop hits deadline ->
`_print_remaining_rows` prints `parent-0 tier=parent pid=N` -> ERR line to
stderr -> exit 2. Output exercised by the strengthened test (c).

## Agent Notes
Fixed overclaim: _round_status_wait timeout branch now prints the last-seen view (_print_remaining_rows) before ERR+exit 2; strengthened test (c) to assert the clause; 45 passed.

parent review (a00-82dbbd88, L4.244): the timeout branch now prints _print_remaining_rows before the ERR line, and test (c) asserts the live parent row on stdout. Re-ran test_spawn_budget.py myself: 45 passed. This round closes the only clause kid #1 overclaimed; the hypothesis --wait surface now matches its claim on all five clauses (already-finished no-sleep, removal-returns-0, timeout exit 2 with last-seen view, unknown exit 3, --wait without --iter exit 2).
